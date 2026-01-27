import requests
from bs4 import BeautifulSoup
import re
import os
import concurrent.futures

# ================= CONFIG =================

SOURCES = [
    # HTTP / HTTPS
    ("http", "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000"),
    ("http", "https://proxyspace.pro/http.txt"),
    ("http", "https://vakhov.github.io/fresh-proxy-list/http.txt"),
    ("http", "https://raw.githubusercontent.com/0x1881/Free-Proxy-List/main/http.txt"),
    ("http", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"),
    ("http", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"),
    ("http", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"),
    ("http", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"),
    ("http", "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt"),
    ("http", "https://raw.githubusercontent.com/zeroxeclipse/freeproxy24/refs/heads/main/http.txt"),
    ("http", "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/http_proxies.txt"),
    ("http", "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/http.txt"),
    ("http", "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/HTTPS.txt"),
    ("http", "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt"),

    # SOCKS4
    ("socks4", "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks4&timeout=10000"),
    ("socks4", "https://proxyspace.pro/socks4.txt"),
    ("socks4", "https://vakhov.github.io/fresh-proxy-list/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/0x1881/Free-Proxy-List/main/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt"),
    ("socks4", "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt"),
    ("socks4", "https://raw.githubusercontent.com/zeroxeclipse/freeproxy24/refs/heads/main/socks4.txt"),
    ("socks4", "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks4_proxies.txt"),
    ("socks4", "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/socks4.txt"),
     ("socks4", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4.txt"),
    ("socks4", "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt"),

    # SOCKS5
    ("socks5", "https://api.proxyscrape.com/v4/free-proxy-list/get?request=displayproxies&protocol=socks5&timeout=10000"),
    ("socks5", "https://proxyspace.pro/socks5.txt"),
    ("socks5", "https://vakhov.github.io/fresh-proxy-list/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/0x1881/Free-Proxy-List/main/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/zloi-user/hideip.me/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt"),
    ("socks5", "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt"),
    ("socks5", "https://raw.githubusercontent.com/zeroxeclipse/freeproxy24/refs/heads/main/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/refs/heads/main/socks5_proxies.txt"),
    ("socks5", "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/socks5.txt"),
    ("socks5", "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5.txt"),
    ("socks5", "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt")
]

MAX_WORKERS = 12
TIMEOUT = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

PROXY_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}$")

# ================= FUNCTIONS =================

def fetch_source(p_type, url):
    """Fetch a single proxy source and extract IP:PORTs."""
    found = set()
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            print(f"[!] Failed to fetch {url}: Status {r.status_code}")
            return p_type, found

        text = r.text.replace("\ufeff", "")

        # If HTML, extract text
        if "<" in text and ">" in text:
            text = BeautifulSoup(text, "lxml").get_text()

        for line in text.splitlines():
            line = line.strip()
            if PROXY_PATTERN.match(line):
                found.add(line)

    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")

    return p_type, found


def scrape_proxies():
    proxies = {"http": set(), "socks4": set(), "socks5": set()}
    print(f"[+] Scraping {len(SOURCES)} sources with {MAX_WORKERS} workers...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_source, p_type, url) for p_type, url in SOURCES]

        for future in concurrent.futures.as_completed(futures):
            p_type, found = future.result()
            proxies[p_type].update(found)

    os.makedirs("output/raw", exist_ok=True)
    
    save("output/raw/http.txt", proxies["http"])
    save("output/raw/socks4.txt", proxies["socks4"])
    save("output/raw/socks5.txt", proxies["socks5"])

    print(
        f"[✓] Scraped {len(proxies['http'])} HTTP | "
        f"{len(proxies['socks4'])} SOCKS4 | "
        f"{len(proxies['socks5'])} SOCKS5 proxies"
    )


def save(path, data):
    with open(path, "w") as f:
        for item in sorted(data):
            f.write(item + "\n")


# ================= MAIN =================

if __name__ == "__main__":
    scrape_proxies()




