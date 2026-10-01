#!/usr/bin/env python3
"""SEC EDGAR helpers: a ticker's filings in a date window, and the live feed of the latest
filings (8-K events, offering prospectuses, activist 13D stakes).

EDGAR requires a contact email in the User-Agent of every request. It is read from the
SEC_CONTACT environment variable or .secrets/sec_contact (git-ignored) and sent to sec.gov
only. Without it every call here returns nothing.

  python scripts/sec.py JELD [--days 30]      # a ticker's recent filings
  python scripts/sec.py JELD --exhibit        # the press release in its latest 8-K (--n 1 for the one before)
  python scripts/sec.py --current 8-K         # the live 8-K feed
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html
import json
import os
import re
import sys
import threading
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"

# 8-K item numbers -> what kind of event they are.
ITEMS = {
    "1.01": ("contract-order", "material agreement"),
    "1.02": ("negative", "agreement terminated"),
    "1.03": ("refinancing", "bankruptcy or receivership"),
    "2.01": ("deal-closed", "acquisition or sale completed"),
    "2.02": ("earnings-guidance", "results"),
    "2.03": ("refinancing", "new debt"),
    "2.05": ("negative", "restructuring charges"),
    "2.06": ("negative", "impairment"),
    "3.01": ("negative", "delisting notice"),
    "3.02": ("dilution", "unregistered share sale"),
    "3.03": ("negative", "holders' rights modified"),
    "4.01": ("negative", "auditor change"),
    "4.02": ("negative", "financials unreliable"),
    "5.01": ("deal-closed", "change in control"),
    "5.02": ("people", "officer or director change"),
    "5.03": ("charter", "charter amendment (reverse splits are filed here)"),
    "7.01": ("disclosure", "Reg FD disclosure"),
    "8.01": ("disclosure", "other events"),
}
OFFERING_FORMS = ("S-1", "S-1/A", "S-3", "S-3/A", "F-1", "F-3", "424B1", "424B2", "424B3", "424B4", "424B5", "424B7")

_lock = threading.Lock()
_last = [0.0]
_tickers: dict | None = None


def contact() -> str | None:
    c = os.environ.get("SEC_CONTACT")
    f = ROOT / ".secrets" / "sec_contact"
    if not c and f.exists():
        c = f.read_text().strip()
    return c or None


def enabled() -> bool:
    return contact() is not None


def get(url: str, timeout: float = 20.0) -> bytes:
    c = contact()
    if not c:
        raise RuntimeError("no SEC contact configured")
    with _lock:  # fair-access limit is 10 requests a second; stay well under it
        wait = 0.15 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": f"InvestmentChallenge {c}", "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data


def tickers() -> dict:
    """{"by_ticker": {TICKER: cik}, "by_cik": {cik: TICKER}}, cached for a day."""
    global _tickers
    if _tickers is not None:
        return _tickers
    f = CACHE / "sec_tickers.json"
    if f.exists() and time.time() - f.stat().st_mtime < 86400:
        _tickers = json.loads(f.read_text())
        return _tickers
    data = json.loads(get("https://www.sec.gov/files/company_tickers.json"))
    by_t, by_c = {}, {}
    for v in data.values():
        t, c = v["ticker"].upper(), str(int(v["cik_str"]))
        by_t[t] = int(c)
        by_c.setdefault(c, t)  # first listed ticker = the main class
    _tickers = {"by_ticker": by_t, "by_cik": by_c}
    CACHE.mkdir(exist_ok=True)
    f.write_text(json.dumps(_tickers))
    return _tickers


def filings(sym: str, start: dt.date, end: dt.date | None = None) -> list[dict]:
    """The ticker's filings dated start..end (inclusive), newest first, with 8-K items decoded."""
    if not enabled():
        return []
    cik = tickers()["by_ticker"].get(sym.upper().replace("-", "."))
    if not cik:
        cik = tickers()["by_ticker"].get(sym.upper())
    if not cik:
        return []
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))
    rec = sub.get("filings", {}).get("recent", {})
    end_s = (end or dt.date.today()).isoformat()
    out = []
    for i, form in enumerate(rec.get("form", [])):
        fdate = rec["filingDate"][i]
        if fdate > end_s:
            continue
        if fdate < start.isoformat():
            break
        items = [x for x in (rec.get("items") or [""] * (i + 1))[i].split(",") if x]
        acc = rec["accessionNumber"][i].replace("-", "")
        out.append({"form": form, "date": fdate, "items": items,
                    "events": [ITEMS[x][1] for x in items if x in ITEMS],
                    "desc": (rec.get("primaryDocDescription") or [""] * (i + 1))[i],
                    "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{rec['primaryDocument'][i]}"})
    return out


def html_text(raw: str) -> str:
    """Readable text from an EDGAR HTML document."""
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h[1-6]|table)>", "\n", raw)
    raw = re.sub(r"(?i)</t[dh]>", " | ", raw)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\xa0", " ")
    lines = [re.sub(r"[ \t|]+", " ", ln).strip(" |") for ln in txt.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def documents(filing_url: str) -> list[dict]:
    """Every document in a filing (from its folder's index.json)."""
    base = filing_url.rsplit("/", 1)[0]
    idx = json.loads(get(base + "/index.json"))
    return [{"name": it["name"], "size": it.get("size"), "url": f"{base}/{it['name']}"}
            for it in idx.get("directory", {}).get("item", [])]


def typed_exhibits(filing_url: str, kind: str = "EX-99") -> list[str]:
    """Documents the filing index declares as this exhibit type, for file names that don't say so
    (Accenture's press release is q4fy26earnings8-kexhibit.htm)."""
    base = filing_url.rsplit("/", 1)[0]
    idx = [d for d in documents(filing_url) if d["name"].endswith(("-index.htm", "-index.html"))]
    if not idx:
        return []
    page = get(idx[0]["url"]).decode("utf-8", "ignore")
    out = []
    for row in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", page):
        m = re.search(r'href="([^"]+?([^"/]+\.html?))"', row)
        if m and re.search(rf">\s*{kind}", row):
            out.append(f"{base}/{m.group(2)}")
    return out


def exhibit(sym: str, form: str = "8-K", n: int = 0, days: int = 120, max_chars: int = 12000) -> str:
    """Text of the press release (exhibit 99.x) in the ticker's n-th most recent filing of this form,
    or the filing's main document when there is no exhibit 99."""
    fl = [f for f in filings(sym, dt.date.today() - dt.timedelta(days=days)) if f["form"].startswith(form)]
    if len(fl) <= n:
        return f"no {form} filing #{n} in {days} days for {sym}"
    f = fl[n]
    docs = [d for d in documents(f["url"]) if d["name"].lower().endswith((".htm", ".html", ".txt"))]
    ex = [d for d in docs if re.search(r"ex-?_?99|exhibit_?99|dex99", d["name"], re.I)]
    ex_urls = [d["url"] for d in ex] or typed_exhibits(f["url"])
    target = ex_urls[0] if ex_urls else f["url"]
    body = html_text(get(target).decode("utf-8", "ignore"))
    head = f"{sym} {f['form']} filed {f['date']} ({'; '.join(f['events'])})\nsource: {target}\n\n"
    return head + body[:max_chars] + ("\n[... truncated]" if len(body) > max_chars else "")


def tags(fl: list[dict]) -> list[str]:
    """Catalyst tags implied by filings (same vocabulary as movers.TAGS where they overlap)."""
    out = []
    for f in fl:
        form = f.get("form", "")
        if form in OFFERING_FORMS:
            out.append("dilution")
        if form in ("SC 13D", "SCHEDULE 13D"):
            out.append("activist-stake")  # a new 5%+ holder with intent to influence; amendments (/A) are routine
        if form.replace(" ", "").startswith(("SCTO", "SC14D9")) or form in ("DEFM14A", "PREM14A"):
            out.append("takeover-target")  # tender offer or merger vote: the price is capped by the deal
        for x in f.get("items", []):
            t = ITEMS.get(x, (None,))[0]
            if t in ("contract-order", "earnings-guidance", "refinancing", "dilution"):
                out.append(t)
            elif x in ("3.01", "4.02"):
                out.append("red-flag")
    return list(dict.fromkeys(out))


def current(form: str = "8-K", count: int = 100, start: int = 0) -> list[dict]:
    """The latest filings of one form type across all companies (EDGAR's live feed), with tickers."""
    if not enabled():
        return []
    url = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type="
           f"{urllib.request.quote(form)}&company=&dateb=&owner=include&start={start}&count={count}&output=atom")
    atom = get(url).decode("utf-8", "ignore")
    by_cik = tickers()["by_cik"]
    out = []
    for e in re.findall(r"<entry>(.*?)</entry>", atom, re.S):
        title = html.unescape(re.search(r"<title>(.*?)</title>", e, re.S).group(1))
        m = re.match(r"(.+?) - (.+?) \((\d{10})\) \((\w+)\)", title)
        if not m or m.group(4) not in ("Filer", "Subject"):
            continue
        summary = html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(
            (re.search(r"<summary[^>]*>(.*?)</summary>", e, re.S) or re.search(r"(.*)", "")).group(1))))
        items = re.findall(r"Item (\d\.\d\d)", summary)
        upd = re.search(r"<updated>(.*?)</updated>", e)
        link = re.search(r'<link[^>]*href="([^"]+)"', e)
        cik = str(int(m.group(3)))
        out.append({"form": m.group(1), "company": m.group(2), "cik": cik, "ticker": by_cik.get(cik),
                    "role": m.group(4), "items": items, "events": [ITEMS[x][1] for x in items if x in ITEMS],
                    "at": upd.group(1) if upd else None, "link": link.group(1) if link else None})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker", nargs="?")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--current", help="form type for the live feed, e.g. 8-K, 424B5, SCHEDULE 13D")
    ap.add_argument("--exhibit", action="store_true", help="print the press release (exhibit 99) of a recent filing")
    ap.add_argument("--form", default="8-K", help="with --exhibit: form type (default 8-K)")
    ap.add_argument("--n", type=int, default=0, help="with --exhibit: 0 = most recent, 1 = the one before, ...")
    ap.add_argument("--chars", type=int, default=12000)
    a = ap.parse_args()
    if not enabled():
        print("SEC contact not configured (.secrets/sec_contact or SEC_CONTACT)")
        return 1
    if a.current:
        for f in current(a.current):
            print(f"{(f['at'] or '')[:16]} {f['form']:8} {str(f['ticker'] or '-'):6} {f['company'][:40]:40} "
                  f"{'; '.join(f['events'])}")
        return 0
    if a.exhibit:
        print(exhibit(a.ticker.upper(), a.form, a.n, max(a.days, 120), a.chars))
        return 0
    for f in filings(a.ticker, dt.date.today() - dt.timedelta(days=a.days)):
        print(f"{f['date']} {f['form']:10} {','.join(f['items']):16} {'; '.join(f['events'])[:70]} {f['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
