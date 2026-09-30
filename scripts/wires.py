#!/usr/bin/env python3
"""Live catalyst feed: the newest company press releases (every wire, via Stock Titan, plus PR
Newswire), SEC EDGAR's live filings (8-K events by item number, offering prospectuses, 13D stakes),
Nasdaq trading halts and FDA announcements. Each item is tagged by catalyst type and
joined with the company's size and the stock's price reaction. Items first seen in this run are
marked NEW.

  python scripts/wires.py [--hours 6] [--all]

Writes .cache/wires.json. Speed is not the edge: algorithms read the wires in microseconds and
take the first jump. The edge is judging which releases change a company's value a lot relative
to its size, then acting on the drift that follows over the next days.
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import gzip
import html
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import movers  # noqa: E402
import portfolio as pfm  # noqa: E402
import sec  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36")
FEEDS = {
    "stocktitan": "https://www.stocktitan.net/rss",  # latest 100 releases from all wires, with tickers
    "prnewswire": ["https://www.prnewswire.com/rss/news-releases-list.rss"] + [
        f"https://www.prnewswire.com/rss/{c}-latest-news/{c}-latest-news-list.rss"
        for c in ("financial-services", "health", "technology", "energy", "business-technology")],
    "halts": "https://www.nasdaqtrader.com/rss.aspx?feed=tradehalts",
    "fda": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
}
HALTS = {"T1": "halted, news pending", "T2": "halted, news released", "T12": "halted, info requested",
         "H10": "SEC trading suspension", "H11": "halted, regulatory concern", "LUDP": "volatility pause",
         "LUDS": "volatility pause", "M": "volatility halt", "MWC1": "market-wide halt"}
FUNDAMENTAL = {"earnings-guidance", "contract-order", "refinancing", "clinical-regulatory"}
TICKER_IN_TEXT = re.compile(r"\((?:NYSE|NASDAQ|Nasdaq|NYSE American|NYSE Arca|NYSE MKT|Cboe BZX)\s*:\s*"
                            r"([A-Z]{1,5}(?:\.[A-Z])?)\)")
AMOUNT = re.compile(r"\$\s?(\d+(?:[.,]\d+)?)\s*(billion|million|bn|mm|[BM])\b", re.I)


NAME_STOP = {"the", "and", "inc", "corp", "group", "holdings", "company", "international", "global", "american", "first",
             "united", "national", "technologies", "therapeutics", "pharmaceuticals", "energy", "capital", "financial"}


def names_company(title: str, name: str | None, ticker: str, aliases: tuple = ()) -> bool:
    """Does the headline name the company (ticker or the first distinctive word of its name)?"""
    t = title.lower()
    if re.search(rf"(?<![a-z0-9]){re.escape(ticker.lower())}(?![a-z0-9])", t):
        return True
    for n in (name, *aliases):
        if not n:
            continue
        words = [w for w in re.findall(r"[a-z0-9&]+", movers.SUFFIX.sub("", n).lower()) if len(w) >= 3 and w not in NAME_STOP]
        if words and words[0] in t:
            return True
    return not name  # no name on file: cannot tell, assume it is theirs


def is_html(data: bytes) -> bool:
    head = data.lstrip()[:300].lower()
    return head.startswith(b"<html") or head.startswith(b"<!doctype html")


def fetch(url: str, timeout: float = 20.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip", "Accept": "*/*"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404):
                # A bot filter: fda.gov answers urllib with 401, and PR Newswire's CDN answers it with 404 at
                # times while curl gets the feed. Retry with curl below.
                data = b"<html>"
                break
            if attempt == 2 or e.code < 500:
                raise
            time.sleep(2)
    data = gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
    if is_html(data):
        # Bot wall (Incapsula on the halts page, Akamai on fda.gov): curl sometimes passes where urllib does
        # not, and which user agent gets through changes from hour to hour.
        for ua in (UA, "curl/8.5.0"):
            out = subprocess.run(["curl", "-s", "--compressed", "-A", ua, "--max-time", str(int(timeout)), url],
                                 capture_output=True, timeout=timeout + 5)
            data = out.stdout
            if data and not is_html(data):
                return data
        raise RuntimeError("blocked by the site's bot wall (or the page is gone)")
    return data


def when(s: str | None) -> dt.datetime | None:
    try:
        return email.utils.parsedate_to_datetime(s).astimezone(dt.timezone.utc) if s else None
    except Exception:  # noqa: BLE001
        return None


def items(url: str) -> list[dict]:
    root = ET.fromstring(fetch(url))
    out = []
    for it in root.iter("item"):
        out.append({c.tag.split("}")[-1]: (c.text or "").strip() for c in it})
    return out


def releases() -> tuple[list[dict], list[str]]:
    rows, errors = [], []
    try:
        for it in items(FEEDS["stocktitan"]):
            m = re.search(r"/news/([A-Z0-9.\-]+)/", it.get("link", ""))
            title = re.sub(r"\s*\|\s*[A-Z0-9.\-]+ Stock News\s*$", "", html.unescape(it.get("title", "")))
            rows.append({"src": "stocktitan", "ticker": m.group(1) if m else None, "title": title,
                         "link": it.get("link"), "at": when(it.get("pubDate"))})
    except Exception as e:  # noqa: BLE001
        errors.append(f"stocktitan: {str(e)[:100]}")
    prn_newest = None
    for url in FEEDS["prnewswire"]:
        try:
            for it in items(url):
                at = when(it.get("pubDate"))
                prn_newest = max(prn_newest, at) if prn_newest and at else (at or prn_newest)
                if not (it.get("language") or "en").startswith("en"):
                    continue
                text = html.unescape(it.get("title", "") + " " + re.sub(r"<[^>]+>", " ", it.get("description", "")))
                m = TICKER_IN_TEXT.search(text)
                if not m:
                    continue  # private company, or the ticker is not in the teaser
                rows.append({"src": "prnewswire", "ticker": m.group(1), "title": html.unescape(it.get("title", "")),
                             "link": it.get("link"), "at": at})
        except Exception as e:  # noqa: BLE001
            errors.append(f"prnewswire: {str(e)[:80]}")
    # Stock Titan sometimes serves an hours-old copy of its feed; say so rather than show a silent gap.
    st_newest = max((r["at"] for r in rows if r["src"] == "stocktitan" and r["at"]), default=None)
    if st_newest and prn_newest and prn_newest - st_newest > dt.timedelta(minutes=90):
        errors.append(f"stocktitan feed stale (newest {st_newest.astimezone(pfm.ET).strftime('%H:%M ET')}); "
                      f"PR Newswire only for the gap")
    return rows, errors


def halts() -> tuple[list[dict], list[str]]:
    out = []
    try:
        for it in items(FEEDS["halts"]):
            code = it.get("ReasonCode", "")
            try:
                et = dt.datetime.strptime(f"{it.get('HaltDate')} {it.get('HaltTime', '')[:8]}", "%m/%d/%Y %H:%M:%S")
                at = et.replace(tzinfo=pfm.ET).astimezone(dt.timezone.utc)
            except Exception:  # noqa: BLE001
                at = when(it.get("pubDate"))
            out.append({"src": "halts", "ticker": it.get("IssueSymbol"), "name": it.get("IssueName"), "code": code,
                        "title": f"{HALTS.get(code, 'halt ' + code)}"
                                 + (f"; resumed {it['ResumptionTradeTime']}" if it.get("ResumptionTradeTime") else ""),
                        "at": at})
        return out, []
    except Exception as e:  # noqa: BLE001
        return [], [f"halts: {str(e)[:100]}"]


def fda() -> tuple[list[dict], list[str]]:
    try:
        return [{"src": "fda", "ticker": None, "title": html.unescape(it.get("title", "")), "link": it.get("link"),
                 "at": when(it.get("pubDate"))} for it in items(FEEDS["fda"])], []
    except Exception as e:  # noqa: BLE001
        return [], [f"fda: {str(e)[:100]}"]


SEC_FEEDS = (("8-K", 2), ("424B5", 1), ("SCHEDULE 13D", 1))  # (form, pages of 100)
SEC_TELLING = {"1.01", "1.02", "1.03", "2.01", "2.02", "2.03", "3.01", "3.02", "4.02", "5.01"}
SEC_WARN = {"1.02", "3.01", "3.02", "4.02"}  # agreement ended, delisting notice, share sale, unreliable financials


def sec_feed() -> tuple[list[dict], list[str]]:
    """EDGAR's live feeds: 8-K events (decoded item numbers), offering prospectuses, activist 13D stakes."""
    if not sec.enabled():
        return [], ["sec: no contact configured"]
    rows, errors = [], []
    for form, pages in SEC_FEEDS:
        for start in range(0, pages * 100, 100):
            try:
                for f in sec.current(form, 100, start):
                    try:
                        at = dt.datetime.fromisoformat(f["at"]).astimezone(dt.timezone.utc) if f.get("at") else None
                    except ValueError:
                        at = None
                    what = "; ".join(f["events"]) if f["events"] else (
                        "offering prospectus (shares or notes)" if f["form"].startswith("424B") else
                        "activist stake (13D)" if "13D" in f["form"] else "filed")
                    rows.append({"src": "sec", "ticker": f["ticker"], "name": f["company"], "at": at,
                                 "title": f"{f['form']}: {what}", "link": f.get("link"), "items": f["items"],
                                 "form": f["form"], "sec_tags": sec.tags([{"form": f["form"], "items": f["items"]}])})
            except Exception as e:  # noqa: BLE001
                errors.append(f"sec {form}: {str(e)[:80]}")
    return rows, errors


def load_universe() -> dict:
    """Listed US stocks >= $50M market cap (symbol -> name, size), refreshed once a day."""
    f = CACHE / "universe.json"
    if f.exists():
        doc = json.loads(f.read_text())
        age = pfm.now_utc() - pfm.parse_ts(doc["generated_at"])
        if age < dt.timedelta(hours=20):
            return doc["stocks"]
    uni = movers.universe(50, min_avg_vol=50_000)
    stocks = {s: {"name": q.get("shortName") or q.get("longName"), "display": q.get("displayName"),
                  "mcap": q.get("marketCap"), "avg_volume": q.get("averageDailyVolume3Month"),
                  "exchange": q.get("exchange")} for s, q in uni.items()}
    CACHE.mkdir(exist_ok=True)
    f.write_text(json.dumps({"generated_at": pfm.iso(pfm.now_utc()), "stocks": stocks}))
    return stocks


def held_and_watched() -> set[str]:
    out = set()
    for book in ("h1b", "free"):
        try:
            lots = pfm.Portfolio(pfm.load_ledger(book), pfm.load_config(book)).lots
            out |= {pfm.parse_option(s)["underlying"] if pfm.asset_class(s) == "option" else s
                    for s, ls in lots.items() if ls}
        except Exception:  # noqa: BLE001
            pass
        try:
            w = json.loads(pfm.book_path("watchlist", book).read_text())
            out |= set(w.get("focus", []))
        except Exception:  # noqa: BLE001
            pass
    return out


def amount_usd(title: str) -> float | None:
    best = None
    for num, unit in AMOUNT.findall(title):
        v = float(num.replace(",", "")) * (1e9 if unit.lower() in ("billion", "bn", "b") else 1e6)
        best = v if best is None else max(best, v)
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=6.0, help="look back this many hours")
    ap.add_argument("--all", action="store_true", help="also list items without a catalyst tag")
    a = ap.parse_args()
    now = pfm.now_utc()
    since = now - dt.timedelta(hours=a.hours)
    rel, e1 = releases()
    hl, e2 = halts()
    fd, e3 = fda()
    sf, e4 = sec_feed()
    errors = e1 + e2 + e3 + e4
    uni = load_universe()
    mine = held_and_watched()

    seen_f = CACHE / "wires_seen.json"
    seen = json.loads(seen_f.read_text()) if seen_f.exists() else {}
    keep_after = pfm.iso(now - dt.timedelta(days=3))
    seen = {k: v for k, v in seen.items() if v >= keep_after}

    rows, dup = [], set()
    for r in rel + hl + sf:
        if not r.get("at") or r["at"] < since or not r.get("ticker"):
            continue
        key = (r["ticker"], re.sub(r"\W+", " ", r["title"].lower()).strip()[:80], r.get("code"))
        if key in dup:
            continue
        dup.add(key)
        u = uni.get(r["ticker"])
        r["listed"] = u is not None
        r["mcap"] = (u or {}).get("mcap")
        r["name"] = r.get("name") or (u or {}).get("name")
        aliases = tuple(x for x in ((u or {}).get("display"),) if x)
        r["tags"] = [] if r["src"] == "halts" else r["sec_tags"] if r["src"] == "sec" else [
            t for t in movers.classify([{"title": r["title"]}], [], r.get("name") or "", r["ticker"], aliases)
            if t != "no-clear-news"]
        if r["src"] in ("stocktitan", "prnewswire") and not names_company(r["title"], r.get("name"), r["ticker"], aliases):
            r["tags"].append("third-party")  # another company's release that mentions this one (lender, customer, owner)
        amt = amount_usd(r["title"])
        r["amount_usd"] = amt
        r["amount_to_mcap"] = round(amt / r["mcap"], 3) if amt and r.get("mcap") else None
        gid = f"{r['src']}|{r['ticker']}|{r.get('code') or ''}|{r['title'][:80]}"
        r["new"] = gid not in seen
        seen.setdefault(gid, pfm.iso(now))
        r["mine"] = r["ticker"] in mine
        rows.append(r)

    # Price reaction for the ones worth a look.
    def worth(r):
        if r["mine"]:
            return True
        if not r["listed"]:
            return False
        if r["src"] == "halts":
            return r.get("code") in ("T1", "T2", "LUDP", "LUDS", "M")
        if r["src"] == "sec":
            return telling(r)
        if "third-party" in r["tags"]:
            return False
        return bool(set(r["tags"]) & (FUNDAMENTAL | {"product-news", "takeover-target", "dilution"}))

    def telling(r):
        return (bool(set(r.get("items") or []) & SEC_TELLING) or r.get("form", "").startswith("424B")
                or r.get("form") in ("SCHEDULE 13D", "SC 13D"))

    def warning(r):
        return r.get("form", "").startswith("424B") or bool(set(r.get("items") or []) & SEC_WARN)

    look = sorted({r["ticker"] for r in rows if worth(r)})[:80]
    import marketdata  # noqa: E402  (after sys.path setup)

    def q(sym):
        try:
            return sym, marketdata.quote(sym)
        except Exception:  # noqa: BLE001
            return sym, None

    with ThreadPoolExecutor(max_workers=8) as pool:
        quotes = dict(pool.map(q, look))
    for r in rows:
        qt = quotes.get(r["ticker"])
        if qt:
            r["price"] = qt.get("price")
            r["change_pct"] = qt.get("change_pct")
            r["ext_change_pct"] = qt.get("ext_change_pct")
            r["volume"] = qt.get("volume")
            avg = (uni.get(r["ticker"]) or {}).get("avg_volume")
            r["rel_volume"] = round(qt["volume"] / avg, 1) if avg and qt.get("volume") else None

    def rank(r):
        s = 0
        tags = set(r["tags"])
        if tags & FUNDAMENTAL:
            s += 2
        elif "product-news" in tags:
            s += 1
        if tags & {"takeover-target"}:
            s -= 2
        if tags & {"dilution", "reverse-split", "red-flag"}:
            s -= 2
        if "activist-stake" in tags:
            s += 1
        if "third-party" in tags:
            s -= 3
        mc = (r.get("mcap") or 0) / 1e6
        s += 1 if 100 <= mc <= 20000 else 0
        if r.get("amount_to_mcap") and r["amount_to_mcap"] >= 0.1:
            s += 2  # the dollar figure in the headline is >= 10% of the company's value
        mv = max(abs(r.get("change_pct") or 0), abs(r.get("ext_change_pct") or 0))
        if mv >= 5:
            s += 2 if (r.get("rel_volume") or 0) >= 2 or abs(r.get("ext_change_pct") or 0) >= 5 else 1
        return s

    for r in rows:
        r["rank"] = rank(r)
    CACHE.mkdir(exist_ok=True)
    seen_f.write_text(json.dumps(seen))
    doc = {"generated_at": pfm.iso(now), "hours": a.hours, "errors": errors,
           "items": [{**r, "at": pfm.iso(r["at"])} for r in rows],
           "fda": [{**r, "at": pfm.iso(r["at"])} for r in fd if r.get("at") and r["at"] >= since]}
    (CACHE / "wires.json").write_text(json.dumps(doc, indent=1, default=str))

    def line(r):
        age = int((now - r["at"]).total_seconds() // 60)
        mc = f"${r['mcap'] / 1e6:,.0f}M" if r.get("mcap") else "unlisted/OTC"
        px = ""
        if r.get("change_pct") is not None:
            px = f" | {r['change_pct']:+.1f}%" + (f" ext {r['ext_change_pct']:+.1f}%" if r.get("ext_change_pct") else "")
            px += f" relvol {r['rel_volume']}" if r.get("rel_volume") else ""
        amt = f" | ${r['amount_usd'] / 1e6:,.0f}M = {r['amount_to_mcap'] * 100:.0f}% of mcap" if r.get("amount_to_mcap") else ""
        return (f"{'NEW ' if r['new'] else '    '}{age:>4}m {r['ticker']:6} {mc:>10}{px}{amt} | "
                f"{','.join(r['tags']) or r.get('code') or '-'} | {r['title'][:110]}")

    print(f"wires {now.astimezone(pfm.ET).strftime('%a %H:%M ET')}: {len(rel)} releases, {len(sf)} SEC filings, "
          f"{len(hl)} halts, {len(fd)} FDA items "
          f"(last {a.hours:g}h shown){' | errors: ' + '; '.join(errors) if errors else ''}")
    mine_rows = [r for r in rows if r["mine"] and r["src"] != "halts" and (r["src"] != "sec" or telling(r))]
    if mine_rows:
        print("\nHOLDINGS / WATCHLIST")
        for r in sorted(mine_rows, key=lambda r: r["at"], reverse=True):
            print(line(r))
    hrows = [r for r in rows if r["src"] == "halts" and (r["listed"] or r["mine"]) and r.get("code") in HALTS]
    if hrows:
        print("\nHALTS (listed stocks)")
        for r in sorted(hrows, key=lambda r: r["at"], reverse=True)[:15]:
            print(line(r))
    srows = [r for r in rows if r["src"] == "sec" and not r["mine"] and r["listed"] and telling(r)]
    ev_rows = [r for r in srows if not warning(r)]
    warn_rows = [r for r in srows if warning(r)]
    if ev_rows:
        print("\nSEC EVENTS (listed stocks: material agreements, results, new debt, deals closed, new 13D stakes)")
        for r in sorted(ev_rows, key=lambda r: (-r["rank"], -r["at"].timestamp()))[:20]:
            print(f"[{r['rank']:+d}] " + line(r))
    if warn_rows:
        print("\nSEC WARNINGS (offerings, unregistered share sales, delisting notices, unreliable financials)")
        for r in sorted(warn_rows, key=lambda r: -r["at"].timestamp())[:15]:
            print("     " + line(r))
    mat = [r for r in rows if r["src"] not in ("halts", "sec") and not r["mine"] and r["listed"]
           and (a.all or set(r["tags"]) & (FUNDAMENTAL | {"product-news", "takeover-target", "dilution"}))]
    if mat:
        print("\nCATALYSTS (listed stocks, ranked)")
        for r in sorted(mat, key=lambda r: (-r["rank"], r["at"]), reverse=False)[:25]:
            print(f"[{r['rank']:+d}] " + line(r))
    fd_new = [r for r in doc["fda"]]
    if fd_new:
        print("\nFDA")
        for r in fd_new[:5]:
            print(f"     {r['at'][11:16]}Z {r['title'][:130]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
