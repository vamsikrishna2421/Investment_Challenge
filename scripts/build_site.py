#!/usr/bin/env python3
"""Wrap dashboard/index.html (an artifact page fragment) into a standalone
document for the public Vercel site: site/index.html + site/vercel.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "dashboard" / "index.html"
OUT = ROOT / "site"

DESC = ("Two $1,000 paper portfolios racing to double by the Oct 5 close: an H-1B book (stocks and ETFs) "
        "and an Unrestricted book (options and crypto too). Live holdings, every trade and the research journal.")
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='7' fill='%230f1b21'/%3E"
           "%3Cpath d='M6 23l7-7 5 4 8-10' fill='none' stroke='%23f0a414' stroke-width='3' "
           "stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")
RESET = (":root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
         "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px/1.5 system-ui,"
         "-apple-system,'Segoe UI',sans-serif;background:#f7f7f5}img{max-width:100%}"
         "[hidden]{display:none!important}")


def main() -> None:
    src = SRC.read_text()
    cut = src.index('<div class="page">')
    head, body = src[:cut].strip(), src[cut:].strip()
    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
        f"<meta name=\"description\" content=\"{DESC}\">\n"
        "<meta property=\"og:title\" content=\"H1B $1K Challenge\">\n"
        f"<meta property=\"og:description\" content=\"{DESC}\">\n"
        "<meta property=\"og:type\" content=\"website\">\n"
        "<meta name=\"theme-color\" content=\"#0f1b21\">\n"
        f"<link rel=\"icon\" href=\"{FAVICON}\">\n"
        f"<style>{RESET}</style>\n"
        f"{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )
    # Light minify: drop indentation and blank lines (keeps line breaks, so JS semantics are unchanged).
    doc = "\n".join(line.strip() for line in doc.splitlines() if line.strip()) + "\n"
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(doc)
    (OUT / "vercel.json").write_text(json.dumps({
        "cleanUrls": True,
        "headers": [{
            "source": "/(.*)",
            "headers": [
                {"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"},
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            ],
        }],
    }, indent=2) + "\n")
    print(f"site/index.html {len(doc)} bytes")


if __name__ == "__main__":
    main()
