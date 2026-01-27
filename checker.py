import requests
import ipaddress
import concurrent.futures
import os
import time

# ================= CONFIG =================

TIMEOUT = 4
MAX_WORKERS = 200

CHECK_URL_GOOGLE = "https://www.google.com"
CHECK_URL_HTTP = "http://icanhazip.com"
CHECK_URL_SOCKS = "http://httpbin.org/ip"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# ================= PROXY CHECK =================

def check_proxy(proxy, p_type, url):
    proxies = {
        "http": f"{p_type}://{proxy}" if p_type != "http" else f"http://{proxy}",
        "https": f"{p_type}://{proxy}" if p_type != "http" else f"http://{proxy}",
    }

    try:
        r = requests.get(url, proxies=proxies, timeout=TIMEOUT, headers=HEADERS)

        if r.status_code != 200:
            return False

        if url == CHECK_URL_GOOGLE:
            return "<title>Google</title>" in r.text

        text = r.text.strip()

        try:
            ipaddress.ip_address(text)
            return True
        except ValueError:
            try:
                return "origin" in r.json()
            except:
                return False

    except requests.RequestException:
        return False

# ================= FILE PROCESSING =================

def process_file(input_file, output_file, p_type):
    if not os.path.exists(input_file):
        print(f"[!] File {input_file} not found. Skipping {p_type}")
        return 0

    with open(input_file, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"[+] Checking {len(proxies)} {p_type} proxies...")
    start_time = time.time()

    def check(proxy):
        if check_proxy(proxy, p_type, CHECK_URL_GOOGLE):
            return proxy

        if p_type == "http":
            if check_proxy(proxy, p_type, CHECK_URL_HTTP):
                return proxy
        else:
            if check_proxy(proxy, p_type, CHECK_URL_SOCKS):
                return proxy

        return None

    live = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i, result in enumerate(executor.map(check, proxies), 1):
            if result:
                live.add(result)

            if i % 50 == 0 or i == len(proxies):
                elapsed = time.time() - start_time
                print(
                    f"  Checked {i}/{len(proxies)} | Live: {len(live)} | {elapsed:.1f}s",
                    end="\r"
                )

    # Save live proxies to output/live
    os.makedirs("output/live", exist_ok=True)
    with open(output_file, "w") as f:
        for p in sorted(live):
            f.write(p + "\n")

    print(f"\n[✓] {len(live)} live {p_type} proxies saved to {output_file}")
    return len(live)

# ================= MAIN =================

def main():
    os.makedirs("output/live", exist_ok=True)

    live_http = process_file("output/raw/http.txt", "output/live/http.txt", "http")
    live_socks4 = process_file("output/raw/socks4.txt", "output/live/socks4.txt", "socks4")
    live_socks5 = process_file("output/raw/socks5.txt", "output/live/socks5.txt", "socks5")

    print(f"\nSummary: HTTP={live_http}, SOCKS4={live_socks4}, SOCKS5={live_socks5}")

if __name__ == "__main__":
    main()
    

