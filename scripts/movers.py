#!/usr/bin/env python3
"""Big-mover catalyst scanner: find US stocks that moved >= N% today on real
volume, pull the reason (headlines, SEC filings) and the numbers that say
whether the move is a re-rating the market has not finished pricing.

  python scripts/movers.py [--min-move 15] [--min-mcap 100] [--losers] [--save]
Writes .cache/movers.json; --save also writes research/movers/<date>.json so
follow-through can be measured later (python scripts/movers.py --follow-up).

The idea it serves: a large one-day move on material public news (guidance
raise, big order relative to company size, refinancing that removes a default
risk, approval) tends to keep drifting; a large move on no news, a cash
takeover (price capped at the deal) or a dilutive financing does not.
Needs direct internet access (Yahoo Finance via yfinance, Google News, SEC EDGAR).
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SEC_UA = "Investment Challenge research (github.com/vamsikrishna2421/Investment_Challenge)"

# Catalyst tags, checked in order; the first that matches a headline wins for that headline.
TAGS = [
    ("no-news", r"unusual (stock |share )?(trading|market|price)|no (material |new |corporate )*(news|developments|"
                r"announcements)|not aware of any|unaware of any"),
    ("takeover-target", r"to be acquired|agrees? to be acquired|definitive (merger )?agreement to be acquired|"
                        r"take[- ]private|tender offer|buyout|acquired by|to acquire \w+ (for|in) \$|agrees to acquire"),
    ("dilution", r"public offering|registered direct|private placement|priced .*offering|at-the-market|"
                 r"\bATM\b|warrants?\b|shelf"),
    ("refinancing", r"refinanc|debt|maturit|restructur|credit (facility|agreement)|secures \$|recapitaliz|"
                    r"chapter 11|bankruptcy|going concern"),
    ("clinical-regulatory", r"\bFDA\b|approv|phase [123i]|trial|topline|clinical|breakthrough (therapy|device)|"
                            r"clearance|\bEMA\b"),
    ("earnings-guidance", r"guidance|outlook|raises? (its |full[- ]year |annual )?(forecast|guidance|outlook)|"
                          r"record (revenue|quarter|results|sales|bookings|deposits)|\bbeats?\b|"
                          r"(first|second|third|fourth|q[1-4]|fiscal|quarterly|annual)\b[\w ,-]{0,25}\bresults|"
                          r"earnings|preliminary (revenue|results)|(revenue|sales|profit|bookings) "
                          r"(grows?|growth|jumps?|soars?|rises?|surges?|doubles?|triples?)"),
    ("contract-order", r"contract|award(ed|s)?\b|purchase order|orders? (for|from|worth|valued)|"
                       r"(wins|secures|lands|receives|signs)\b.{0,40}\b(order|deal|contract|agreement)|"
                       r"selected (by|as|to)|supply agreement|partners? with|partnership with|strategic "
                       r"(partnership|agreement|alliance|investment)|agreement with|collaborat|deploy"),
    ("product-news", r"launch(es|ed)?\b|unveil|introduc(es|ed)\b|integrat\w* (with|into)|expands? (into|to)\b|"
                     r"roll(s|ed)? ?out|teams? up|tie[- ]up|\blinks?\b.{0,60}\b(to|with)\b|now available|goes live"),
    ("analyst", r"upgrade|initiat\w* (coverage|at|with)|price target|(to|at|an?) outperform|overweight|buy rating|"
                r"reiterat"),
    ("sector-theme", r"quantum|nuclear|uranium|crypto|bitcoin|stablecoin|\bAI\b|artificial intelligence|drone|"
                     r"defen[cs]e|space|rare earth"),
]
# Price-action roundups and "why is X stock up" pieces say that it moved, not why: not a catalyst by themselves.
GENERIC = re.compile(
    r"stocks? (are |that are )?moving|\bmovers\b|stocks to watch|what'?s (going on|happening)|here'?s why|"
    r"here is why|\bwhy\b.{0,60}\b(stock|shares)\b|stock (quote|price|forecast|analysis)|\btrades? (up|down)|"
    r"overbought|oversold|technical|pre-?market|after[- ]hours|intraday|\btop (gainers|losers)|\bjoins\b.*\band other\b|"
    r"moving average|(out|under)performs? (its )?(competitors|the market)|compared to competitors|trading day|"
    r"penny stocks|worth watching|time to buy\?|what'?s next\?|stock (price, )?news", re.I)
SUFFIX = re.compile(r"[,.]?\s+(inc|corp(oration)?|co|company|ltd|limited|plc|holdings?|group|n\.?v|s\.?a|"
                    r"class [a-c]|common stock|ordinary shares|adr)\b\.?", re.I)
CAPPED = {"takeover-target"}
NEGATIVE = {"dilution", "no-news"}


def http(url: str, headers: dict | None = None, timeout: float = 15.0) -> bytes:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def gnews(query: str, limit: int = 8) -> list[dict]:
    q = urllib.parse.quote(f"{query} when:3d")
    try:
        root = ET.fromstring(http(f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"))
    except Exception:  # noqa: BLE001
        return []
    out = []
    for it in root.iter("item"):
        title = html.unescape((it.findtext("title") or "").strip())
        out.append({"title": title, "published": (it.findtext("pubDate") or "").strip(),
                    "source": (it.find("source").text if it.find("source") is not None else None), "via": "google"})
        if len(out) >= limit:
            break
    return out


_CIK: dict | None = None
_SEC_OFF = False


def sec_filings(sym: str, days: int = 4) -> list[dict]:
    """Recent SEC filings (form, date, items/description) for the ticker.
    EDGAR rejects anonymous clients (403); after the first refusal the run skips it."""
    global _CIK, _SEC_OFF
    if _SEC_OFF:
        return []
    try:
        if _CIK is None:
            data = json.loads(http("https://www.sec.gov/files/company_tickers.json", {"User-Agent": SEC_UA}))
            _CIK = {v["ticker"].upper(): int(v["cik_str"]) for v in data.values()}
        cik = _CIK.get(sym.upper())
        if not cik:
            return []
        sub = json.loads(http(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", {"User-Agent": SEC_UA}))
        rec = sub.get("filings", {}).get("recent", {})
        cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
        out = []
        for i, form in enumerate(rec.get("form", [])):
            fdate = rec["filingDate"][i]
            if fdate < cutoff:
                break
            acc = rec["accessionNumber"][i].replace("-", "")
            out.append({"form": form, "date": fdate, "items": rec.get("items", [""] * (i + 1))[i],
                        "desc": rec.get("primaryDocDescription", [""] * (i + 1))[i],
                        "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{rec['primaryDocument'][i]}"})
        return out[:10]
    except Exception as e:  # noqa: BLE001
        if "403" in str(e):
            _SEC_OFF = True
        return [{"error": str(e)[:120]}]


def classify(news: list[dict], filings: list[dict], name: str = "", sym: str = "") -> list[str]:
    # The company's own name can trip theme words ("Stablecoin Development", "Nuclear ..."): drop it first.
    core = SUFFIX.split(name or "")[0].strip()
    first = core.split(" ")[0] if core else ""
    names = sorted({w for w in (core, first if len(first) >= 4 else "") if w}, key=len, reverse=True)
    tags = []
    for n in news:
        t = n.get("title") or ""
        # Google results for "SYM stock" can be about other companies: keep only those naming this one.
        if n.get("via") == "google" and not (
                (sym and re.search(rf"\b{re.escape(sym)}\b", t)) or any(re.search(re.escape(w), t, re.I) for w in names)):
            continue
        for w in names:
            t = re.sub(re.escape(w), " ", t, flags=re.I)
        if sym:
            t = re.sub(rf"\b{re.escape(sym)}\b", " ", t)
        if re.search(TAGS[0][1], t, re.I):
            if "no-news" not in tags:
                tags.append("no-news")
            continue
        if GENERIC.search(t):
            continue
        for tag, pat in TAGS[1:]:
            if re.search(pat, t, re.I):
                if tag not in tags:
                    tags.append(tag)
                break
    for f in filings:
        items = f.get("items") or ""
        form = f.get("form") or ""
        if form in ("S-1", "S-3", "424B5", "424B4", "424B3", "F-1", "F-3") and "dilution" not in tags:
            tags.append("dilution")
        if "1.01" in items and "contract-order" not in tags:
            tags.append("contract-order")  # material definitive agreement
        if "2.02" in items and "earnings-guidance" not in tags:
            tags.append("earnings-guidance")
        if "1.03" in items:
            tags.append("refinancing")  # bankruptcy
    return tags or ["no-clear-news"]


def score(row: dict) -> int:
    s = 0
    tags = set(row["tags"])
    if tags & {"earnings-guidance", "contract-order", "refinancing", "clinical-regulatory"}:
        s += 3
    elif "product-news" in tags:
        s += 1
    if tags & CAPPED:
        s -= 4
    if tags & NEGATIVE:
        s -= 3
    if "no-clear-news" in tags:
        s -= 2
    rv = row.get("rel_volume") or 0
    s += 2 if rv >= 5 else 1 if rv >= 2 else 0
    mc = (row.get("market_cap") or 0) / 1e6
    s += 1 if 300 <= mc <= 20000 else (-1 if mc < 150 else 0)
    g = row.get("revenue_growth")
    if g is not None and g > 0.3:
        s += 1
    if row.get("off_52w_high_pct") is not None and row["off_52w_high_pct"] < -60:
        s += 1  # deeply beaten down: more room for a genuine re-rating
    return s


def enrich(q: dict) -> dict:
    import yfinance as yf  # type: ignore
    sym = q["symbol"]
    row = {"symbol": sym, "name": q.get("shortName") or q.get("longName"),
           "price": q.get("regularMarketPrice"), "change_pct": round(q.get("regularMarketChangePercent") or 0, 2),
           "volume": q.get("regularMarketVolume"), "market_cap": q.get("marketCap"),
           "exchange": q.get("exchange")}
    info = {}
    try:
        info = yf.Ticker(sym).get_info() or {}
    except Exception:  # noqa: BLE001
        pass
    keep = {"sector": "sector", "industry": "industry", "enterpriseValue": "enterprise_value",
            "totalRevenue": "revenue_ttm", "revenueGrowth": "revenue_growth", "grossMargins": "gross_margin",
            "profitMargins": "profit_margin", "totalCash": "cash", "totalDebt": "debt",
            "sharesOutstanding": "shares_out", "floatShares": "float_shares",
            "shortPercentOfFloat": "short_pct_float", "averageVolume": "avg_volume",
            "fiftyTwoWeekHigh": "high_52w", "fiftyTwoWeekLow": "low_52w", "targetMeanPrice": "target_mean",
            "recommendationKey": "rating", "numberOfAnalystOpinions": "analysts",
            "enterpriseToRevenue": "ev_to_revenue", "forwardPE": "forward_pe"}
    for k, v in keep.items():
        if info.get(k) is not None:
            row[v] = info[k]
    if row.get("avg_volume") and row.get("volume"):
        row["rel_volume"] = round(row["volume"] / row["avg_volume"], 1)
    if row.get("high_52w") and row.get("price"):
        row["off_52w_high_pct"] = round((row["price"] / row["high_52w"] - 1) * 100, 1)
    if row.get("target_mean") and row.get("price"):
        row["target_upside_pct"] = round((row["target_mean"] / row["price"] - 1) * 100, 1)
    news = []
    try:
        for n in (yf.Ticker(sym).news or [])[:8]:
            c = n.get("content") or n
            news.append({"title": c.get("title"), "published": c.get("pubDate") or c.get("providerPublishTime"),
                         "source": (c.get("provider") or {}).get("displayName") if isinstance(c.get("provider"), dict) else c.get("publisher"),
                         "via": "yahoo"})
    except Exception:  # noqa: BLE001
        pass
    news += gnews(f"{sym} stock", 6)
    seen, uniq = set(), []
    for n in news:
        t = (n.get("title") or "").strip()
        if t and t not in seen:
            seen.add(t)
            uniq.append(n)
    row["news"] = uniq[:10]
    row["filings"] = sec_filings(sym)
    row["tags"] = classify(row["news"], [f for f in row["filings"] if "error" not in f],
                           row.get("name") or "", sym)
    row["score"] = score(row)
    return row


def screen(min_move: float, losers: bool, size: int = 100) -> list[dict]:
    import yfinance as yf  # type: ignore
    from yfinance import EquityQuery as Q  # type: ignore
    cond = Q("lt", ["percentchange", -min_move]) if losers else Q("gt", ["percentchange", min_move])
    q = Q("and", [cond, Q("eq", ["region", "us"]), Q("gte", ["intradayprice", 1]), Q("gt", ["dayvolume", 300000])])
    r = yf.screen(q, sortField="percentchange", sortAsc=losers, size=size)
    return r.get("quotes", [])


def follow_up() -> int:
    """How did earlier scans' names do since? Tests the idea on our own data."""
    import yfinance as yf  # type: ignore
    files = sorted((ROOT / "research" / "movers").glob("*.json"))
    if not files:
        print("no saved scans yet")
        return 0
    for f in files[-5:]:
        doc = json.loads(f.read_text())
        syms = [r["symbol"] for r in doc["rows"]]
        if not syms:
            continue
        data = yf.download(syms, period="10d", interval="1d", progress=False, auto_adjust=False)["Close"]
        print(f"== scan {doc['date']} ({len(syms)} names)")
        for r in doc["rows"]:
            try:
                ser = data[r["symbol"]].dropna()
                last = float(ser.iloc[-1])
                print(f"  {r['symbol']:6} score {r['score']:+d} {','.join(r['tags'])[:40]:40} "
                      f"scan ${r['price']:.2f} -> ${last:.2f} ({(last / r['price'] - 1) * 100:+.1f}%)")
            except Exception:  # noqa: BLE001
                continue
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-move", type=float, default=15.0)
    ap.add_argument("--min-mcap", type=float, default=100.0, help="$ millions")
    ap.add_argument("--losers", action="store_true")
    ap.add_argument("--extra", default="", help="extra tickers to analyse, comma separated")
    ap.add_argument("--save", action="store_true")
    ap.add_argument("--follow-up", action="store_true")
    a = ap.parse_args()
    if a.follow_up:
        return follow_up()
    quotes = [q for q in screen(a.min_move, a.losers)
              if q.get("quoteType", "EQUITY") == "EQUITY" and not re.search(r"(W|WS|U|R)$", q["symbol"][-2:] if len(q["symbol"]) > 4 else "")]
    picked = [q for q in quotes if (q.get("marketCap") or 0) >= a.min_mcap * 1e6]
    skipped = [q["symbol"] for q in quotes if q not in picked]
    extra = [x.strip().upper() for x in a.extra.split(",") if x.strip()]
    if extra:
        import yfinance as yf  # type: ignore
        for s in extra:
            if any(q["symbol"] == s for q in picked):
                continue
            try:
                fi = yf.Ticker(s).fast_info
                prev = fi.get("previousClose") or fi.get("regularMarketPreviousClose")
                last = fi.get("lastPrice")
                picked.append({"symbol": s, "regularMarketPrice": last, "marketCap": fi.get("marketCap"),
                               "regularMarketChangePercent": (last / prev - 1) * 100 if prev else None,
                               "regularMarketVolume": fi.get("lastVolume")})
            except Exception:  # noqa: BLE001
                continue
    rows = []
    for q in picked:
        try:
            rows.append(enrich(q))
        except Exception as e:  # noqa: BLE001
            rows.append({"symbol": q["symbol"], "error": str(e)[:200], "tags": [], "score": -9})
        time.sleep(0.3)
    rows.sort(key=lambda r: (-r.get("score", -9), -(r.get("change_pct") or 0)))
    now = pfm.now_utc()
    doc = {"generated_at": pfm.iso(now), "date": pfm.et_date(now).isoformat(), "min_move": a.min_move,
           "losers": a.losers, "min_mcap_m": a.min_mcap, "skipped_small": skipped, "rows": rows}
    (ROOT / ".cache").mkdir(exist_ok=True)
    (ROOT / ".cache" / "movers.json").write_text(json.dumps(doc, indent=1, default=str))
    if a.save:
        d = ROOT / "research" / "movers"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{doc['date']}{'-losers' if a.losers else ''}.json").write_text(json.dumps(doc, indent=1, default=str))
    print(f"{len(quotes)} movers >= {a.min_move}% ({'down' if a.losers else 'up'}); {len(rows)} analysed "
          f"(mcap >= ${a.min_mcap:g}M); skipped small: {', '.join(skipped[:15])}")
    for r in rows:
        mc = (r.get("market_cap") or 0) / 1e6
        rev = (r.get("revenue_ttm") or 0) / 1e6
        print(f"\n[{r.get('score', 0):+d}] {r['symbol']} {r.get('change_pct')}% ${r.get('price')} | mcap ${mc:,.0f}M "
              f"rev ${rev:,.0f}M growth {r.get('revenue_growth')} EV/S {r.get('ev_to_revenue')} | relvol {r.get('rel_volume')} "
              f"short {r.get('short_pct_float')} | 52w {r.get('low_52w')}-{r.get('high_52w')} | target {r.get('target_mean')} "
              f"({r.get('rating')}, {r.get('analysts')}) | {r.get('industry')}")
        print(f"   tags: {', '.join(r.get('tags', []))}")
        for f in r.get("filings", [])[:4]:
            if "error" not in f:
                print(f"   SEC {f['date']} {f['form']} items={f.get('items')} {f.get('desc') or ''}")
        for n in r.get("news", [])[:6]:
            print(f"   - {str(n.get('title'))[:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
