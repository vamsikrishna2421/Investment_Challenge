#!/usr/bin/env python3
"""Do dips without company news recover more than dips with news? (Vamsi, Oct 6: focus on big dips that have no
fundamental reason, find the support where they reverse, and buy the reversal.)
Events: radar candidates' sessions that closed 1+ ATR (14-day, to the prior close) under the prior close, over the
last --years. Company news: an SEC filing of a news form (8-K, 6-K, an offering prospectus or registration, 10-Q,
10-K, 20-F, 40-F) dated from the session before to the session after the dip (an 8-K can follow its press release
by days, so the window trades a little look-ahead for coverage). At support: the dip's low inside the band from the
radar stop to 0.5 ATR above the radar support, levels as of the prior close (support tested twice or more).
Market-wide: SPY closed down 1%+ the same session. Entries: the dip's close; the next open; and "confirmed", the
next close when that session closed up. Exits at the close 1, 3 and 5 sessions after the dip (3 after the confirmed
entry); no stops; returns after trade.py slippage, means +/- 95% clustered by date, against the same names'
average 3-session return as the baseline.
  python scripts/news_dip_backtest.py [--tickers A,B] [--years 4] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402
import sec  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
NEWS_FORMS = ("8-K", "6-K", "424B", "S-1", "S-3", "F-1", "F-3", "10-Q", "10-K", "20-F", "40-F")
CACHE = ROOT / ".cache" / "sec_news"


def news_dates(sym: str, start: str) -> set[str] | None:
    """Dates of the ticker's news-form SEC filings since start (cached a day); None without EDGAR access."""
    f = CACHE / f"{sym}.json"
    if f.exists() and time.time() - f.stat().st_mtime < 86400:
        return set(json.loads(f.read_text()))
    if not sec.enabled():
        return None
    cik = sec.tickers()["by_ticker"].get(sym.upper().replace("-", ".")) or sec.tickers()["by_ticker"].get(sym.upper())
    if not cik:
        return None

    def take(rec: dict) -> list[str]:
        return [d for fm, d in zip(rec.get("form", []), rec.get("filingDate", [])) if fm.startswith(NEWS_FORMS)]

    sub = json.loads(sec.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))
    dates = take(sub.get("filings", {}).get("recent", {}))
    for page in sub.get("filings", {}).get("files", []):
        if page.get("filingTo", "") >= start:
            dates += take(json.loads(sec.get("https://data.sec.gov/submissions/" + page["name"])))
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(sorted(set(dates))))
    return set(dates)


def ret(e: float, x: float) -> float:
    return (x * (1 - sb.slip(x)) / (e * (1 + sb.slip(e))) - 1) * 100


def day(r: dict) -> str:
    return dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat()


def events(sym: str, years: float, spy: dict[str, float]) -> tuple[list[dict], list[tuple[str, float]]]:
    rows = sb.daily(sym, "5y")
    if not rows or len(rows) < 300:
        return [], []
    dates = [day(r) for r in rows]
    start = (dt.date.today() - dt.timedelta(days=int(365 * years))).isoformat()
    news = news_dates(sym, start)
    if news is None:
        return [], []
    out, base = [], []
    for i in range(max(270, 1), len(rows) - 6):
        if dates[i] < start:
            continue
        prev, a = rows[i - 1]["c"], lv.atr(rows[i - 30:i])
        if not a or a <= 0:
            continue
        base.append((dates[i], ret(rows[i]["c"], rows[i + 3]["c"])))
        drop = (rows[i]["c"] - prev) / a
        if drop > -1.0:
            continue
        lvl = lv.analyse({"sym": sym, "rows": rows[max(0, i - 261):i], "name": sym, "exchange": "", "type": ""})
        at_sup = bool(lvl and lvl.get("support_strength", 0) >= 2
                      and lvl["stop"] < rows[i]["l"] <= lvl["support"] + 0.5 * a)
        e = rows[i]["c"]
        ev = {"sym": sym, "date": dates[i], "drop": drop, "pct": (e / prev - 1) * 100,
              "news": any(d in news for d in dates[i - 1:i + 2]), "at_sup": at_sup,
              "spy": spy.get(dates[i]), "d1": ret(e, rows[i + 1]["c"]), "d3": ret(e, rows[i + 3]["c"]),
              "d5": ret(e, rows[i + 5]["c"]), "o3": ret(rows[i + 1]["o"], rows[i + 3]["c"])}
        if rows[i + 1]["c"] > e:
            ev["c3"] = ret(rows[i + 1]["c"], rows[i + 4]["c"])
        out.append(ev)
    return out, base


def line(name: str, g: list[dict]) -> str:
    def cell(k: str) -> str:
        xs = [(r["date"], max(-40.0, min(40.0, r[k]))) for r in g if k in r]
        if not xs:
            return "-"
        m, se = cb.clustered(xs)
        return f"{m:+.2f} ± {1.96 * se:.2f}"
    w3 = sum(1 for r in g if r["d3"] > 0) / len(g) * 100 if g else float("nan")
    nc = sum(1 for r in g if "c3" in r)
    return (f"| {name} | {len(g):,} | {cell('d1')} | {cell('d3')} | {cell('d5')} | {w3:.0f}% | {cell('o3')} | "
            f"{cell('c3')} ({nc:,}) |")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--years", type=float, default=4.0)
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    spy_rows = sb.daily("SPY", "5y") or []
    spy = {day(r): (r["c"] / spy_rows[i - 1]["c"] - 1) * 100 for i, r in enumerate(spy_rows) if i}
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda s: events(s, a.years, spy), syms))
    ev = [e for r, _ in res for e in r]
    base = [b for _, bs in res for b in bs]
    bm, bse = cb.clustered([(d, max(-40.0, min(40.0, v))) for d, v in base])
    nn = [e for e in ev if not e["news"]]
    groups = [
        ("All dips 1+ ATR", ev),
        ("with company news", [e for e in ev if e["news"]]),
        ("without company news", nn),
        ("Big dips 2+ ATR, with news", [e for e in ev if e["news"] and e["drop"] <= -2]),
        ("Big dips 2+ ATR, without news", [e for e in nn if e["drop"] <= -2]),
        ("No news, low at support", [e for e in nn if e["at_sup"]]),
        ("No news, not at support", [e for e in nn if not e["at_sup"]]),
        ("No news, SPY down 1%+ (market-wide)", [e for e in nn if e["spy"] is not None and e["spy"] <= -1]),
        ("No news, SPY not down 1% (stock or sector)", [e for e in nn if e["spy"] is not None and e["spy"] > -1]),
        ("No news, 2+ ATR, at support", [e for e in nn if e["drop"] <= -2 and e["at_sup"]]),
    ]
    L = [f"# Dips with and without company news ({dt.date.today().isoformat()})", "",
         f"{sum(1 for r, _ in res if r)} of {len(syms)} radar candidates with SEC filing history, last {a.years:g} "
         f"years: {len(ev):,} sessions that closed 1+ ATR under the prior close. Method: the "
         "`scripts/news_dip_backtest.py` docstring. Returns % after slippage, ± 95% clustered by date. Baseline: "
         f"the same names' average 3-session return from any close, {bm:+.2f} ± {1.96 * bse:.2f}.", "",
         "| Dips | Count | Close to +1 day | to +3 days | to +5 days | Up after 3 days | Next open to +3 days | "
         "Confirmed (next close up) to +3 more (count) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    L += [line(n, g) for n, g in groups]
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        p = ROOT / "research" / "backtests" / f"news-dips-{dt.date.today().isoformat()}.md"
        p.write_text(text)
        print("saved", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
