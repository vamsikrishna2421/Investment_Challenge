#!/usr/bin/env python3
"""Big-mover catalyst scanner: find US stocks that moved >= N% today on real
volume, pull the reason (headlines, SEC filings) and the numbers that say
whether the move is a re-rating the market has not finished pricing.

  python scripts/movers.py [--min-move 15] [--min-mcap 100] [--losers] [--save]
  python scripts/movers.py --lookback 30 [--min-move 15] [--save]   # every jump in the last 30 sessions
Writes .cache/movers.json (lookback: .cache/movers_lookback.json); --save also writes
research/movers/<date>.json (lookback-<date>.json) so follow-through can be measured
later (python scripts/movers.py --follow-up).

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
import sec  # noqa: E402

ROOT = pfm.ROOT
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Catalyst tags, checked in order; the first that matches a headline wins for that headline.
TAGS = [
    ("no-news", r"unusual (stock |share )?(trading|market|price)|no (material |new |corporate )*(news|developments|"
                r"announcements)|not aware of any|unaware of any"),
    ("takeover-target", r"to be acquired|agrees? to be acquired|definitive (merger )?agreement to be acquired|"
                        r"take[- ]private|tender offer|buyout|acquired by|to acquire \w+ (for|in) \$|agrees to acquire"),
    ("reverse-split", r"reverse (stock |share )?split"),
    ("dilution", r"public offering|registered direct|private placement|priced .*offering|at-the-market|"
                 r"\bATM\b|warrants?\b|shelf|strategic investment|closing of .{0,40}(offering|placement|financing)|"
                 r"(prices|closes|announces) .{0,30}(financing|offering)|convertible (senior )?(notes|preferred)|"
                 r"equity (line|purchase agreement)|\bELOC\b|standby equity"),
    ("refinancing", r"refinanc|debt|maturit|restructur|credit (facility|agreement)|secures \$|recapitaliz|"
                    r"chapter 11|bankruptcy|going concern"),
    ("clinical-regulatory", r"\bFDA\b|(?<!trump )(?<!job )(?<!presidential )approv|phase [123i]|\btrials?\b|topline|clinical|breakthrough (therapy|device)|"
                            r"clearance|\bEMA\b"),
    ("earnings-guidance", r"guidance|outlook|raises? (its |full[- ]year |annual )?(forecast|guidance|outlook)|"
                          r"record (revenue|quarter|results|sales|bookings|deposits)|\bbeats?\b|"
                          r"(first|second|third|fourth|q[1-4]|fiscal|quarterly|annual)\b[\w ,-]{0,25}\bresults|"
                          r"earnings|preliminary (revenue|results)|(revenue|sales|profit|bookings) "
                          r"(grows?|growth|jumps?|soars?|rises?|surges?|doubles?|triples?)"),
    ("contract-order", r"contract|awarded\b.{0,50}\b(order|task order|\$)|purchase order|orders? (for|from|worth|valued)|"
                       r"(wins|secures|lands|receives|signs)\b.{0,40}\b(order|deal|contract|agreement)|"
                       r"selected (by|as|to)|supply agreement|partners? with|partnership with|strategic "
                       r"(partnership|agreement|alliance)|agreement with|collaborat|deploy"),
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
    r"penny stocks|worth watching|time to buy\?|what'?s next\?|stock (price, )?news|"
    # investor-relations calendar items: dates of results, calls, conferences
    r"\bto (announce|release|report|host|hold|present|participate)\b|announces? (the )?(date|dates|timing)\b|"
    r"\bschedules?\b|conference call|webcast|webinar|fireside|investor day|will (report|release|announce|host)\b|"
    r"\bparticipate in\b|\bto ring\b|\brelease dates?\b|"
    # opinion polls a PR or research firm publishes as marketing (Stagwell's Harris Poll)
    r"\bpoll\b", re.I)
SUFFIX = re.compile(r"[,.]?\s+(inc|corp(oration)?|co|company|ltd|limited|plc|holdings?|group|n\.?v|s\.?a|"
                    r"class [a-c]|common stock|ordinary shares|adr)\b\.?", re.I)
DEBT = re.compile(r"\b(senior|secured|unsecured) notes|notes due|term loan|credit facility|\bbonds?\b", re.I)
CAPPED = {"takeover-target"}
NEGATIVE = {"dilution", "no-news", "reverse-split"}


def http(url: str, headers: dict | None = None, timeout: float = 15.0) -> bytes:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def gnews(query: str, limit: int = 8, window: str = "when:3d") -> list[dict]:
    """Google News RSS search; window is "when:3d" or "after:YYYY-MM-DD before:YYYY-MM-DD"."""
    q = urllib.parse.quote(f"{query} {window}".strip())
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


def sec_window(sym: str, start: dt.date, end: dt.date | None = None) -> list[dict]:
    """SEC filings in a date window; empty when EDGAR is unreachable or no contact is configured."""
    try:
        return sec.filings(sym, start, end)
    except Exception as e:  # noqa: BLE001
        return [{"error": str(e)[:120]}]


def classify(news: list[dict], filings: list[dict], name: str = "", sym: str = "", aliases: tuple = ()) -> list[str]:
    # The company's own name can trip theme words ("Stablecoin Development", "Nuclear ..."): drop it first.
    names_set = set()
    for nm in (name, *aliases):
        core = SUFFIX.split(nm or "")[0].strip()
        first = core.split(" ")[0] if core else ""
        names_set |= {w for w in (core, first if len(first) >= 4 else "") if w}
    names = sorted(names_set, key=len, reverse=True)
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
                if tag == "dilution" and DEBT.search(t) and not re.search(r"convertible|exchangeable", t, re.I):
                    tag = "refinancing"  # a notes or loan deal, not new shares
                if tag not in tags:
                    tags.append(tag)
                break
    for t in sec.tags([f for f in filings if "error" not in f]):
        if t not in tags:
            tags.append(t)
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
    s += 1 if 300 <= mc <= 20000 else (-3 if mc < 100 else 0)  # under $100M: median -13% in 10 sessions after a jump
    g = row.get("revenue_growth")
    if g is not None and g > 0.3:
        s += 1
    if row.get("off_52w_high_pct") is not None and row["off_52w_high_pct"] < -60:
        s += 1  # deeply beaten down: more room for a genuine re-rating
    # How unusual the jump is for this stock: a 15% day is news for a quiet stock, routine for a noisy one.
    z = row.get("jump_sigma")
    if z is not None:
        s += 2 if z >= 6 else 1 if z >= 4 else -2 if z < 2.5 else 0
    if row.get("noisy"):
        s -= 3
    if (row.get("shares_change_1y_pct") or 0) > 25:
        s -= 2  # serial issuer: new shares keep capping the price
    if row.get("reverse_split"):
        s -= 2
    if (row.get("price") or 99) < 1:
        s -= 1  # under $1: exchange deficiency notice, usually cured by a reverse split
    if "red-flag" in tags:
        s -= 3
    if row.get("industry") == "Shell Companies":
        s -= 3  # SPAC or shell: trades on deal rumors, not on a business
    if "activist-stake" in tags:
        s += 1
    return s


def fundamentals(sym: str, row: dict) -> dict:
    """Size, growth, valuation, short interest and analyst numbers from Yahoo, merged into row."""
    import yfinance as yf  # type: ignore
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
    return row


def enrich(q: dict) -> dict:
    import yfinance as yf  # type: ignore
    sym = q["symbol"]
    row = {"symbol": sym, "name": q.get("shortName") or q.get("longName"),
           "price": q.get("regularMarketPrice"), "change_pct": round(q.get("regularMarketChangePercent") or 0, 2),
           "volume": q.get("regularMarketVolume"), "market_cap": q.get("marketCap"),
           "exchange": q.get("exchange")}
    fundamentals(sym, row)
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
    row["filings"] = sec_window(sym, dt.date.today() - dt.timedelta(days=4))
    row.update(q.get("_risk") or {})
    row.update(issuance(sym))
    row["tags"] = classify(row["news"], [f for f in row["filings"] if "error" not in f],
                           row.get("name") or "", sym)
    row["score"] = score(row)
    return row


def screen(min_move: float, losers: bool, size: int = 100) -> list[dict]:
    import yfinance as yf  # type: ignore
    from yfinance import EquityQuery as Q  # type: ignore
    cond = Q("lt", ["percentchange", -min_move]) if losers else Q("gt", ["percentchange", min_move])
    q = Q("and", [cond, Q("eq", ["region", "us"]), Q("gt", ["dayvolume", 100000]),
                  Q("is-in", ["exchange", *EXCHANGES])])
    r = yf.screen(q, sortField="percentchange", sortAsc=losers, size=size)
    return r.get("quotes", [])


EXCHANGES = ["NMS", "NYQ", "NGM", "NCM", "ASE"]


def derivative(sym: str) -> bool:
    """Warrants, units and rights (5+ letter symbols ending W/WS/U/R)."""
    return len(sym) > 4 and bool(re.search(r"(W|WS|U|R)$", sym[-2:]))


def universe(min_mcap_m: float, min_avg_vol: int = 100_000, min_dollar_vol: float = 500_000) -> dict[str, dict]:
    """Every NYSE/Nasdaq/NYSE American common stock above the size and liquidity floor. No share-price floor:
    a $0.80 stock with 1B shares is an $800M company; liquidity is judged in dollars traded a day."""
    import yfinance as yf  # type: ignore
    from yfinance import EquityQuery as Q  # type: ignore
    q = Q("and", [Q("eq", ["region", "us"]), Q("gte", ["intradaymarketcap", min_mcap_m * 1e6]),
                  Q("gt", ["avgdailyvol3m", min_avg_vol]), Q("is-in", ["exchange", *EXCHANGES])])
    out: dict[str, dict] = {}
    for off in range(0, 12000, 250):
        qs = yf.screen(q, offset=off, size=250, sortField="intradaymarketcap", sortAsc=False).get("quotes", [])
        for x in qs:
            dv = (x.get("regularMarketPrice") or 0) * (x.get("averageDailyVolume3Month") or 0)
            if x.get("quoteType") == "EQUITY" and not derivative(x["symbol"]) and dv >= min_dollar_vol:
                out[x["symbol"]] = x
        if len(qs) < 250:
            break
    return out


def history(syms: list[str], period: str = "1y", batch: int = 400):
    """Daily closes and volumes (split-adjusted) for many symbols, as two DataFrames. Big pulls are cached
    for the day in .cache/hist-<period>-<date>.pkl so a second scan the same evening is fast."""
    import pandas as pd  # type: ignore
    import yfinance as yf  # type: ignore
    cache = ROOT / ".cache" / f"hist-{period}-{pfm.et_date(pfm.now_utc()).isoformat()}.pkl"
    if len(syms) > 200 and cache.exists():
        c0, v0 = pd.read_pickle(cache)
        if set(syms) <= set(c0.columns):
            return c0[syms], v0[syms]
    closes, vols = [], []
    for i in range(0, len(syms), batch):
        part = syms[i:i + batch]
        try:
            df = yf.download(part, period=period, interval="1d", progress=False, auto_adjust=False, threads=True)
        except Exception as e:  # noqa: BLE001
            print(f"  history batch {i // batch + 1} failed: {str(e)[:120]}", file=sys.stderr)
            continue
        if df is None or df.empty:
            continue
        c, v = df["Close"], df["Volume"]
        if isinstance(c, pd.Series):
            c, v = c.to_frame(part[0]), v.to_frame(part[0])
        closes.append(c)
        vols.append(v)
    c_all, v_all = pd.concat(closes, axis=1), pd.concat(vols, axis=1)
    if len(syms) > 200:
        (ROOT / ".cache").mkdir(exist_ok=True)
        pd.to_pickle((c_all, v_all), cache)
    return c_all, v_all


def find_events(closes, vols, days: int, min_move: float, min_rel_vol: float = 2.0) -> list[dict]:
    """Every close-to-close jump >= min_move% in the last `days` sessions on >= min_rel_vol x the prior
    20-session volume; one row per stock (its biggest jump) with what the price has done since."""
    out = []
    for sym in closes.columns:
        c = closes[sym].dropna()
        if len(c) < days + 21:
            continue  # recent listings: IPO pops are a different animal
        v = vols[sym].reindex(c.index).fillna(0)
        r = c.pct_change()
        jumps = []
        for i in range(len(c) - days, len(c)):
            if r.iloc[i] >= min_move / 100:
                base = v.iloc[i - 20:i].mean()
                rv = float(v.iloc[i] / base) if base else 0.0
                if rv >= min_rel_vol:
                    jumps.append((i, float(r.iloc[i]), rv))
        if not jumps:
            continue
        i, move, rv = max(jumps, key=lambda j: j[1])
        prof = risk_profile(c, i)
        pre, evc, now = float(c.iloc[i - 1]), float(c.iloc[i]), float(c.iloc[-1])
        after = c.iloc[i:]
        since, vs_pre = now / evc - 1, now / pre - 1
        n_since = len(c) - 1 - i
        if n_since == 0:
            status = "new"
        elif vs_pre <= 0:
            status = "round-trip"  # gave back the whole jump: the market rejected it
        elif since >= 0.15:
            status = "extending"
        elif since >= -0.10:
            status = "holding"  # kept the jump, has not run yet: the "signal shown, rally not started" bucket
        else:
            status = "fading"
        out.append({"symbol": sym, "event_date": c.index[i].date().isoformat(), "move_pct": round(move * 100, 1),
                    "event_rel_volume": round(rv, 1), "pre_close": round(pre, 4), "event_close": round(evc, 4),
                    "price": round(now, 4), "since_event_pct": round(since * 100, 1),
                    "vs_pre_event_pct": round(vs_pre * 100, 1),
                    "max_after_pct": round((float(after.max()) / evc - 1) * 100, 1),
                    "min_after_pct": round((float(after.min()) / evc - 1) * 100, 1),
                    "sessions_since": n_since, "run_up_before_pct": round((pre / float(c.iloc[i - 21]) - 1) * 100, 1),
                    "jumps": [{"date": c.index[j].date().isoformat(), "move_pct": round(m * 100, 1),
                               "rel_volume": round(x, 1)} for j, m, x in jumps], "status": status, **prof})
    return out


# Calibrated on 241 jumps (Aug-Sep 2026, research/movers/study-*.json): stocks above either line fell a median
# 16% against the market in the 10 sessions after the jump, the rest about 4%.
NOISY_VOL = 120.0      # annualized daily volatility (%) in the year before the jump
NOISY_SPIKES = 10      # or this many +/-15% days in that year


def risk_profile(c, i: int, lookback: int = 252) -> dict:
    """How the stock behaved in the year before bar i: annualized volatility, the number of +/-15% days,
    and the jump at bar i measured in that history's daily standard deviations."""
    import numpy as np  # type: ignore
    hist = c.iloc[max(0, i - lookback):i]
    r = np.log(hist / hist.shift(1)).dropna()
    if len(r) < 40:
        return {}
    sd = float(r.std())
    jump = float(np.log(c.iloc[i] / c.iloc[i - 1]))
    vol = sd * 252 ** 0.5 * 100
    spikes = int(((r >= np.log(1.15)) | (r <= np.log(0.85))).sum())
    return {"vol_1y": round(vol, 1), "jump_sigma": round(jump / sd, 1) if sd else None, "spike_days_1y": spikes,
            "history_days": len(r), "noisy": bool(vol >= NOISY_VOL or spikes >= NOISY_SPIKES)}


def issuance(sym: str) -> dict:
    """Share count change over about a year, and any reverse split in the last 18 months (Yahoo)."""
    import pandas as pd  # type: ignore
    import yfinance as yf  # type: ignore
    out: dict = {}
    t = yf.Ticker(sym)
    try:
        sh = t.get_shares_full(start=(dt.date.today() - dt.timedelta(days=400)).isoformat())
        if sh is not None and len(sh) >= 6:
            sh = sh[~sh.index.duplicated(keep="last")].sort_index()
            first, last = float(sh.iloc[:5].median()), float(sh.iloc[-5:].median())  # medians: the series has spikes
            if first > 0:
                out["shares_change_1y_pct"] = round((last / first - 1) * 100, 1)
    except Exception:  # noqa: BLE001
        pass
    try:
        sp = t.splits
        if sp is not None and len(sp):
            cutoff = pd.Timestamp.now(tz=sp.index.tz) - pd.Timedelta(days=540)
            rev = sp[(sp.index >= cutoff) & (sp < 1)]
            if len(rev):
                out["reverse_split"] = f"{rev.index[-1].date()} 1-for-{round(1 / float(rev.iloc[-1]))}"
    except Exception:  # noqa: BLE001
        pass
    return out


STATUS_ADJ = {"holding": 2, "new": 1, "extending": 1, "fading": -1, "round-trip": -3}


def enrich_event(ev: dict, quote: dict) -> dict:
    """Fundamentals, the news on the jump day (the catalyst) and the news since (offerings etc.)."""
    import yfinance as yf  # type: ignore
    sym = ev["symbol"]
    row = dict(ev)
    row.update({"name": quote.get("shortName") or quote.get("longName"), "market_cap": quote.get("marketCap"),
                "exchange": quote.get("exchange")})
    aliases = tuple(x for x in (quote.get("displayName"), quote.get("longName")) if x)
    fundamentals(sym, row)
    row["rel_volume"] = ev["event_rel_volume"]  # score() reads the jump day's volume, not today's
    d = dt.date.fromisoformat(ev["event_date"])
    win = f"after:{(d - dt.timedelta(days=2)).isoformat()} before:{(d + dt.timedelta(days=2)).isoformat()}"
    core = SUFFIX.split(row.get("name") or sym)[0].strip()
    news = gnews(f'"{core}"', 8, win) + gnews(f"{sym} stock", 6, win)
    later = gnews(f'"{core}"', 8, f"after:{(d + dt.timedelta(days=1)).isoformat()}")
    try:
        for n in (yf.Ticker(sym).news or [])[:8]:
            c = n.get("content") or n
            later.append({"title": c.get("title"), "published": c.get("pubDate") or c.get("providerPublishTime"),
                          "via": "yahoo"})
    except Exception:  # noqa: BLE001
        pass
    row["news"] = _dedupe(news)[:10]
    row["later_news"] = _dedupe(later)[:10]
    fl = [f for f in sec_window(sym, d - dt.timedelta(days=2), d + dt.timedelta(days=1)) if "error" not in f]
    later_fl = [f for f in sec_window(sym, d + dt.timedelta(days=2), dt.date.today()) if "error" not in f]
    row["filings"] = fl[:8]
    row["later_filings"] = [f for f in later_fl if f["form"] in sec.OFFERING_FORMS or f["items"]][:8]
    row.update(issuance(sym))
    row["tags"] = classify(row["news"], fl, row.get("name") or "", sym, aliases)
    row["later_tags"] = [t for t in classify(row["later_news"], later_fl, row.get("name") or "", sym, aliases)
                         if t != "no-clear-news"]
    s = score(row) + STATUS_ADJ.get(row["status"], 0)
    if {"dilution", "reverse-split"} & set(row["later_tags"]):
        s -= 3  # sold stock into the move, or a reverse split: the classic post-spike traps
    if len(row["jumps"]) >= 3:
        s -= 1  # serial spiker
    row["score"] = s
    return row


def _dedupe(news: list[dict]) -> list[dict]:
    seen, out = set(), []
    for n in news:
        t = (n.get("title") or "").strip()
        if t and t not in seen:
            seen.add(t)
            out.append(n)
    return out


def risk_line(r: dict) -> str:
    bits = []
    if r.get("jump_sigma") is not None:
        bits.append(f"{r['jump_sigma']}sd move")
    if r.get("vol_1y") is not None:
        bits.append(f"1y vol {r['vol_1y']:.0f}%, {r.get('spike_days_1y')} 15% days{' NOISY' if r.get('noisy') else ''}")
    if r.get("shares_change_1y_pct") is not None:
        bits.append(f"shares {r['shares_change_1y_pct']:+.0f}% 1y")
    if r.get("reverse_split"):
        bits.append(f"reverse split {r['reverse_split']}")
    return ", ".join(bits)


def lookback(days: int, min_move: float, min_mcap_m: float, limit: int, save: bool, include_noisy: bool = False) -> int:
    from concurrent.futures import ThreadPoolExecutor
    t0 = time.time()
    uni = universe(min_mcap_m)
    print(f"universe: {len(uni)} NYSE/Nasdaq/NYSE American stocks (mcap >= ${min_mcap_m:g}M, >= $0.5M traded a day, "
          f"no share-price floor)")
    closes, vols = history(sorted(uni))
    events = find_events(closes, vols, days, min_move)
    by_status: dict[str, int] = {}
    for e in events:
        by_status[e["status"]] = by_status.get(e["status"], 0) + 1
    print(f"{len(events)} stocks jumped >= {min_move:g}% in one session (>= 2x volume) in the last {days} sessions: "
          + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items(), key=lambda kv: -kv[1]))
          + f"  [{time.time() - t0:.0f}s]")
    # Enrich the ones the market has not rejected first; round-trips only if there is room.
    n_noisy = sum(1 for e in events if e.get("noisy"))
    print(f"  {n_noisy} of them are noisy stocks (1y vol >= {NOISY_VOL:g}% or >= {NOISY_SPIKES} 15% days)"
          + ("" if include_noisy else ": kept in the file, not researched"))
    events.sort(key=lambda e: (bool(e.get("noisy")), e["status"] == "round-trip",
                               -e["move_pct"] * min(e["event_rel_volume"], 10)))
    pick = [e for e in events if include_noisy or not e.get("noisy")][:limit]
    picked_syms = {e["symbol"] for e in pick}

    def work(e):
        try:
            return enrich_event(e, uni.get(e["symbol"], {}))
        except Exception as ex:  # noqa: BLE001
            return {**e, "error": str(ex)[:200], "tags": [], "score": -9}

    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(work, pick))
    rows += [{**e, "tags": [], "score": None, "not_enriched": True} for e in events if e["symbol"] not in picked_syms]
    order = {"holding": 0, "extending": 1, "new": 2, "fading": 3, "round-trip": 4}
    rows.sort(key=lambda r: (r.get("score") is None, -(r.get("score") or 0), order.get(r["status"], 9)))
    now = pfm.now_utc()
    doc = {"generated_at": pfm.iso(now), "date": pfm.et_date(now).isoformat(), "mode": "lookback",
           "lookback_sessions": days, "min_move": min_move, "min_mcap_m": min_mcap_m, "universe": len(uni),
           "rows": rows}
    (ROOT / ".cache").mkdir(exist_ok=True)
    (ROOT / ".cache" / "movers_lookback.json").write_text(json.dumps(doc, indent=1, default=str))
    if save:
        d = ROOT / "research" / "movers"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"lookback-{doc['date']}.json").write_text(json.dumps(doc, indent=1, default=str))
    for st in ("holding", "extending", "new", "fading", "round-trip"):
        grp = [r for r in rows if r["status"] == st and r.get("score") is not None]
        if not grp:
            continue
        print(f"\n=== {st.upper()} ({len(grp)} enriched)")
        for r in grp:
            mc = (r.get("market_cap") or 0) / 1e6
            rev = (r.get("revenue_ttm") or 0) / 1e6
            print(f"[{r['score']:+d}] {r['symbol']:6} +{r['move_pct']}% on {r['event_date']} (relvol {r['event_rel_volume']}) "
                  f"-> since {r['since_event_pct']:+}% (vs pre-jump {r['vs_pre_event_pct']:+}%) | ${r['price']} "
                  f"mcap ${mc:,.0f}M rev ${rev:,.0f}M g {r.get('revenue_growth')} | target {r.get('target_mean')} "
                  f"| {','.join(r.get('tags', []))}{' | later: ' + ','.join(r['later_tags']) if r.get('later_tags') else ''}"
                  f" | {risk_line(r)}")
            for n in r.get("news", [])[:3]:
                print(f"      - {str(n.get('title'))[:140]}")
    return 0


def follow_up() -> int:
    """How did earlier scans' names do since? Tests the idea on our own data."""
    import yfinance as yf  # type: ignore
    files = sorted((ROOT / "research" / "movers").glob("*.json"))
    if not files:
        print("no saved scans yet")
        return 0
    for f in files[-5:]:
        doc = json.loads(f.read_text())
        doc["rows"] = [r for r in doc["rows"] if r.get("score") is not None and r.get("price")]
        if doc.get("mode") == "lookback":
            doc["rows"] = sorted(doc["rows"], key=lambda r: -r["score"])[:25]  # the researched top of the list
        syms = [r["symbol"] for r in doc["rows"]]
        if not syms:
            continue
        data = yf.download(syms, period="10d", interval="1d", progress=False, auto_adjust=False)["Close"]
        print(f"== {'lookback ' if doc.get('mode') == 'lookback' else ''}scan {doc['date']} ({len(syms)} names)")
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
    ap.add_argument("--min-mcap", type=float, default=30.0, help="$ millions")
    ap.add_argument("--min-dollar-vol", type=float, default=1.0, help="today's $ volume floor, $ millions")
    ap.add_argument("--include-noisy", action="store_true",
                    help=f"also research stocks with 1-year volatility >= {NOISY_VOL:g}% or >= {NOISY_SPIKES} "
                         "15% days (skipped by default)")
    ap.add_argument("--losers", action="store_true")
    ap.add_argument("--extra", default="", help="extra tickers to analyse, comma separated")
    ap.add_argument("--save", action="store_true")
    ap.add_argument("--follow-up", action="store_true")
    ap.add_argument("--lookback", type=int, default=0,
                    help="scan every jump in the last N sessions instead of today's movers")
    ap.add_argument("--limit", type=int, default=150, help="lookback: how many events to research")
    a = ap.parse_args()
    if a.follow_up:
        return follow_up()
    if a.lookback:
        return lookback(a.lookback, a.min_move, a.min_mcap, a.limit, a.save, a.include_noisy)
    quotes = [q for q in screen(a.min_move, a.losers)
              if q.get("quoteType", "EQUITY") == "EQUITY" and not derivative(q["symbol"])]
    picked = [q for q in quotes if (q.get("marketCap") or 0) >= a.min_mcap * 1e6
              and (q.get("regularMarketPrice") or 0) * (q.get("regularMarketVolume") or 0) >= a.min_dollar_vol * 1e6]
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
    # One year of daily history for every candidate: how unusual today's move is for each of them.
    noisy = []
    if picked:
        closes, _ = history([q["symbol"] for q in picked], period="1y")
        for q in picked:
            if q["symbol"] in closes.columns:
                c = closes[q["symbol"]].dropna()
                if len(c) > 41:
                    q["_risk"] = risk_profile(c, len(c) - 1)
        if not a.include_noisy:
            noisy = [q["symbol"] for q in picked if (q.get("_risk") or {}).get("noisy")]
            picked = [q for q in picked if not (q.get("_risk") or {}).get("noisy")]
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
           "losers": a.losers, "min_mcap_m": a.min_mcap, "skipped_small": skipped, "skipped_noisy": noisy,
           "rows": rows}
    (ROOT / ".cache").mkdir(exist_ok=True)
    (ROOT / ".cache" / "movers.json").write_text(json.dumps(doc, indent=1, default=str))
    if a.save:
        d = ROOT / "research" / "movers"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{doc['date']}{'-losers' if a.losers else ''}.json").write_text(json.dumps(doc, indent=1, default=str))
    print(f"{len(quotes)} movers >= {a.min_move}% ({'down' if a.losers else 'up'}); {len(rows)} analysed "
          f"(mcap >= ${a.min_mcap:g}M, >= ${a.min_dollar_vol:g}M traded); skipped small/illiquid: "
          f"{', '.join(skipped[:15])}; skipped noisy (1y vol >= {NOISY_VOL:g}% or >= {NOISY_SPIKES} 15% days): "
          f"{', '.join(noisy[:15]) or '-'}")
    for r in rows:
        mc = (r.get("market_cap") or 0) / 1e6
        rev = (r.get("revenue_ttm") or 0) / 1e6
        print(f"\n[{r.get('score', 0):+d}] {r['symbol']} {r.get('change_pct')}% ${r.get('price')} | mcap ${mc:,.0f}M "
              f"rev ${rev:,.0f}M growth {r.get('revenue_growth')} EV/S {r.get('ev_to_revenue')} | relvol {r.get('rel_volume')} "
              f"short {r.get('short_pct_float')} | 52w {r.get('low_52w')}-{r.get('high_52w')} | target {r.get('target_mean')} "
              f"({r.get('rating')}, {r.get('analysts')}) | {r.get('industry')}")
        print(f"   tags: {', '.join(r.get('tags', []))} | {risk_line(r)}")
        for f in r.get("filings", [])[:4]:
            if "error" not in f:
                print(f"   SEC {f['date']} {f['form']} {'; '.join(f.get('events') or []) or f.get('desc') or ''}")
        for n in r.get("news", [])[:6]:
            print(f"   - {str(n.get('title'))[:150]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
