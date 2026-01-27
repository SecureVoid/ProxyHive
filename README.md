<p align="center">
    <img src="https://i.imgur.com/vKTQZ3p.png" width="300px">
</p>
<p align="center">
    <img src="https://img.shields.io/badge/Updated_Every_1_Hour-passing-success">
    <img src="https://img.shields.io/github/last-commit/securevoid/ProxyHive.svg">
    <img src="https://img.shields.io/github/license/securevoid/ProxyHive">
  <br>
</p>

**ProxyHive** is an automated proxy scraping and checking tool that supports HTTP, SOCKS4, and SOCKS5 proxies, with automatic updates every hour via GitHub Actions to ensure you always have fresh proxies.

## 🛡️ Proxy Lists

| Proxy Type     | Live / Verified                                                                                  | Raw / Unverified                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **HTTP/HTTPS** | [Live](https://cdn.jsdelivr.net/gh/securevoid/ProxyHive@main/output/live/http.txt)   | [Raw](https://cdn.jsdelivr.net/gh/securevoid/ProxyHive@main/output/raw/http.txt)   |
| **SOCKS4**     | [Live](https://cdn.jsdelivr.net/gh/securevoid/ProxyHive@main/output/live/socks4.txt) | [Raw](https://cdn.jsdelivr.net/gh/securevoid/ProxyHive@main/output/raw/socks4.txt) |
| **SOCKS5**     | [Live](https://cdn.jsdelivr.net/gh/securevoid/ProxyHive@main/output/live/socks5.txt) | [Raw](https://cdn.jsdelivr.net/gh/securevoid/ProxyHive@main/output/raw/socks5.txt) |

## 🚀 Features

- 🌍 **Multi-Source Scraping** — Proxies from multiple free public sources
- ⚡ **Fast Live Checking** — Filters working proxies by connectivity and speed
- 🔌 **Full Protocol Support** — HTTP, SOCKS4, and SOCKS5
- 🛠️ **GitHub Actions Ready** — Hourly automated proxy updates
- 📁 **Organized Output** — Separate files for raw and validated proxies
- 🧹 **Lightweight** — Minimal dependencies, optimized performance

## 🧰 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
git clone https://github.com/securevoid/ProxyHive.git
cd ProxyHive
pip install -r requirements.txt
```
### Scrape proxies:
```bash
python scraper.py
```
### Check proxies:
```bash
python checker.py
```

## Output Structure
```bash
output/
├── live/
│   ├── http.txt
│   ├── socks4.txt
│   └── socks5.txt
└── raw/
    ├── http.txt
    ├── socks4.txt
    └── socks5.txt
```
## 🤝 Contributing
Contributions welcome! Help improve ProxyHive by:
- Adding new proxy sources
- Improve accuracy and reliability of live proxy checks
- Fixing bugs
- Documentation improvements
Feel free to open an issue or submit a pull request.

## 📜 License
This project is licensed under the [GNU License](LICENSE). See the LICENSE file for details.

## 📫 Support

- 🐞 **Report Bugs**: [GitHub Issues](https://github.com/securevoid/ProxyHive/issues)
- ☕ **Support Development**: [Ko-fi](https://ko-fi.com/securevoid)
- 💭 **Discussions**: Use GitHub Discussions for questions and ideas
















