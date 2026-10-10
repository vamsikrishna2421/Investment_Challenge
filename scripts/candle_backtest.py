#!/usr/bin/env python3
"""Hourly candlestick patterns (Vamsi, Oct 10: do 1-hour candle patterns tell the next move, and would one +0.5% trade a
day be enough?). For each radar candidate's regular-session hourly bars over the last ~2 years (Yahoo 1h, 730 days;
bars start 9:30, 10:30 ... 15:30, the last one half an hour), the classic patterns are detected on each completed bar
and bought at the next bar's open in the same session (the best case: the routines act up to 15 minutes later).
Bullish reversals need a decline into the pattern (the close before it under the close 3 bars earlier), bearish ones
a rise; "long" and "small" bodies are measured against the mean body of the 10 bars before.
Measured for each signal and for the baseline (every bar of the same names, bought at the next open regardless):
  - returns to the next bar's close (1 hour), the session close and the next session's close;
  - the scalp Vamsi proposed: sell at +0.5% (a limit, filled when a bar trades a cent through it) with a stop at
    -0.5%, at the pattern's low, or no stop; else at the close. Simulated on 5-minute bars (Yahoo keeps 60 days):
    hourly bars of these names span 1-2%, so they cannot tell which of +0.5% and -0.5% came first. A 5-minute bar
    holding both counts as the stop (the share of such trades is reported).
Returns % after trade.py-style slippage on market fills (the entry, stops, closes) and gross; means +/- 95% clustered
by date. The first and second half of the dates are reported apart: an edge has to show in both.
--daily: the same patterns on daily candles over 5 years (the textbooks' timeframe), bought at the next day's open and
sold at that day's close, 3 sessions later or 5 sessions later (no scalp).
  python scripts/candle_backtest.py [--tickers A,B | --large-caps] [--daily] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import dip_backtest as db  # noqa: E402
import levels as lv  # noqa: E402
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
TICK = 0.01
SCALP = 0.005
BULL = ("hammer", "bullish engulfing", "piercing line", "morning star", "bullish harami", "three white soldiers",
        "big green bar")
BEAR = ("shooting star", "bearish engulfing", "dark cloud cover", "evening star", "three black crows", "big red bar")
MEASURES = ("1h", "close", "next", "s_tight", "s_low", "s_nostop")
# Oct 10 (Vamsi: "maybe these patterns only work on large caps?"): the 60 largest US stocks by market value, plus the two
# index funds.
LARGE = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "BRK-B", "JPM", "LLY", "V", "UNH",
         "XOM", "MA", "JNJ", "PG", "HD", "COST", "ABBV", "WMT", "NFLX", "CRM", "BAC", "ORCL", "KO", "CVX", "MRK", "AMD",
         "PEP", "ADBE", "TMO", "LIN", "ACN", "MCD", "CSCO", "ABT", "WFC", "DIS", "INTU", "IBM", "QCOM", "TXN", "GE", "CAT",
         "AMGN", "VZ", "PFE", "NOW", "ISRG", "PM", "UBER", "SPGI", "RTX", "GS", "HON", "NEE", "T", "LOW", "BKNG"]
LABELS = {"1h": "next hour", "close": "to the close", "next": "next close", "s_tight": "+0.5%/-0.5%",
          "s_low": "+0.5%/pattern low", "s_nostop": "+0.5%/no stop"}


def load(sym: str):
    try:
        h1 = db.by_day(md.yahoo_chart(sym, "730d", "1h", False))
    except Exception:  # noqa: BLE001
        h1 = {}
    try:
        m5 = db.by_day(md.yahoo_chart(sym, "60d", "5m", False))
    except Exception:  # noqa: BLE001
        m5 = {}
    return sym, (h1, m5)


def signals(b: list[tuple], i: int, avg: float) -> list[str]:
    """Patterns completed by bar i (each bar: date, minute, open, high, low, close)."""
    def body(k): return abs(b[k][5] - b[k][2])
    def rng(k): return b[k][3] - b[k][4]
    def green(k): return b[k][5] > b[k][2]
    def red(k): return b[k][5] < b[k][2]
    def top(k): return max(b[k][2], b[k][5])
    def bot(k): return min(b[k][2], b[k][5])
    def mid(k): return (b[k][2] + b[k][5]) / 2
    down = lambda k: b[k - 1][5] < b[k - 4][5]  # noqa: E731 (a decline into bar k)
    up = lambda k: b[k - 1][5] > b[k - 4][5]  # noqa: E731
    out = []
    r, bd = rng(i), body(i)
    if r <= 0 or avg <= 0:
        return out
    lower, upper = bot(i) - b[i][4], b[i][3] - top(i)
    if bd <= r / 3 and lower >= 2 * bd and upper <= 0.1 * r and down(i):
        out.append("hammer")
    if bd <= r / 3 and upper >= 2 * bd and lower <= 0.1 * r and up(i):
        out.append("shooting star")
    p = i - 1
    if red(p) and green(i) and b[i][2] <= b[p][5] and b[i][5] >= b[p][2] and bd > body(p) and down(p):
        out.append("bullish engulfing")
    if green(p) and red(i) and b[i][2] >= b[p][5] and b[i][5] <= b[p][2] and bd > body(p) and up(p):
        out.append("bearish engulfing")
    if red(p) and body(p) > avg and green(i) and b[i][2] <= b[p][5] and mid(p) < b[i][5] < b[p][2] and down(p):
        out.append("piercing line")
    if green(p) and body(p) > avg and red(i) and b[i][2] >= b[p][5] and b[p][2] < b[i][5] < mid(p) and up(p):
        out.append("dark cloud cover")
    if red(p) and body(p) > avg and green(i) and bd < 0.5 * body(p) and top(i) <= b[p][2] and bot(i) >= b[p][5] \
            and down(p):
        out.append("bullish harami")
    q = i - 2
    if red(q) and body(q) > avg and body(p) < 0.3 * avg and green(i) and b[i][5] > mid(q) and down(q):
        out.append("morning star")
    if green(q) and body(q) > avg and body(p) < 0.3 * avg and red(i) and b[i][5] < mid(q) and up(q):
        out.append("evening star")
    three = (q, p, i)
    if all(green(k) and body(k) > 0.5 * avg and b[k][5] >= b[k][3] - 0.25 * rng(k) for k in three) \
            and b[q][5] < b[p][5] < b[i][5] and bot(q) < b[p][2] <= top(q) and bot(p) < b[i][2] <= top(p):
        out.append("three white soldiers")
    if all(red(k) and body(k) > 0.5 * avg and b[k][5] <= b[k][4] + 0.25 * rng(k) for k in three) \
            and b[q][5] > b[p][5] > b[i][5] and bot(q) <= b[p][2] < top(q) and bot(p) <= b[i][2] < top(p):
        out.append("three black crows")
    if green(i) and bd > 2 * avg and b[i][5] >= b[i][3] - 0.1 * r:
        out.append("big green bar")
    if red(i) and bd > 2 * avg and b[i][5] <= b[i][4] + 0.1 * r:
        out.append("big red bar")
    return out


def scalp(e: float, stop: float | None, bars: list[tuple], net: bool) -> tuple[float, str]:
    """Bought at e (the first bar's open): +0.5% limit, stop (checked first), else the last bar's close."""
    tgt = e * (1 + SCALP)
    cost_in = sb.slip(e) if net else 0.0
    for j, (_, _, o, h, lo, c) in enumerate(bars):
        if stop is not None and lo <= stop:
            x = min(o, stop) if j else stop
            how = "both" if h >= tgt + TICK else "stop"
            return (x * (1 - (sb.slip(x) if net else 0)) / (e * (1 + cost_in)) - 1) * 100, how
        if h >= tgt + TICK:
            return (tgt / (e * (1 + cost_in)) - 1) * 100, "target"
    c = bars[-1][5]
    return (c * (1 - (sb.slip(c) if net else 0)) / (e * (1 + cost_in)) - 1) * 100, "close"


def ret(e: float, x: float, net: bool) -> float:
    return (x * (1 - sb.slip(x)) / (e * (1 + sb.slip(e))) - 1) * 100 if net else (x / e - 1) * 100


def run(sym: str, h1: dict, m5: dict) -> tuple[dict, list]:
    """Per-signal rows {signal: [row]} and the baseline rows, for one name. The scalps only where 5-minute bars exist."""
    days = sorted(h1)
    nxt = {d: days[k + 1] for k, d in enumerate(days[:-1])}
    b = [(d, *bar) for d in days for bar in h1[d]]
    pos: dict[str, list[int]] = {}
    for k, x in enumerate(b):
        pos.setdefault(x[0], []).append(k)
    sig_rows: dict[str, list] = defaultdict(list)
    base: list = []
    for i in range(14, len(b) - 1):
        d = b[i][0]
        if b[i + 1][0] != d:
            continue
        avg = sum(abs(b[k][5] - b[k][2]) for k in range(i - 10, i)) / 10
        e = b[i + 1][2]
        if e <= 0:
            continue
        rest = [b[k] for k in pos[d] if k > i]
        nd = nxt.get(d)
        row = {"date": d, "price": e}
        for net in (True, False):
            sfx = "" if net else "_g"
            row["1h" + sfx] = ret(e, b[i + 1][5], net)
            row["close" + sfx] = ret(e, rest[-1][5], net)
            row["next" + sfx] = ret(e, h1[nd][-1][4], net) if nd and h1.get(nd) else None
        fine = [(d, *x) for x in m5.get(d, []) if x[0] >= b[i + 1][1]]
        e5 = fine[0][2] if fine else None
        if e5:
            for net in (True, False):
                sfx = "" if net else "_g"
                row["s_tight" + sfx], row["s_tight_how" + sfx] = scalp(e5, e5 * (1 - SCALP), fine, net)
                row["s_nostop" + sfx], row["s_nostop_how" + sfx] = scalp(e5, None, fine, net)
        base.append(row)
        for s in signals(b, i, avg):
            r = dict(row)
            span = 3 if s in ("morning star", "evening star", "three white soldiers", "three black crows") else \
                2 if s in ("bullish engulfing", "bearish engulfing", "piercing line", "dark cloud cover",
                           "bullish harami") else 1
            low = min(b[k][4] for k in range(i - span + 1, i + 1))
            if e5 and low < e5:
                for net in (True, False):
                    sfx = "" if net else "_g"
                    r["s_low" + sfx], r["s_low_how" + sfx] = scalp(e5, low, fine, net)
            sig_rows[s].append(r)
    return sig_rows, base


def summarize(rows: list[dict], split: str | None = None, measures: tuple = MEASURES,
              halves: tuple = ("1h_g", "close_g")) -> dict:
    out = {"n": len(rows)}
    for m in measures:
        for sfx in ("", "_g"):
            xs = [(r["date"], r[m + sfx]) for r in rows if r.get(m + sfx) is not None]
            if not xs:
                continue
            mean, se = cb.clustered(xs)
            out[m + sfx] = {"mean": round(mean, 3), "ci": round(1.96 * se, 3) if not math.isnan(se) else None,
                            "pos": round(100 * sum(v > 0 for _, v in xs) / len(xs), 1), "n": len(xs)}
            if m.startswith("s_"):
                hows = [r.get(m + "_how" + sfx) for r in rows if r.get(m + "_how" + sfx)]
                k = len(hows) or 1
                out[m + sfx]["target"] = round(100 * hows.count("target") / k, 1)
                out[m + sfx]["stop"] = round(100 * (hows.count("stop") + hows.count("both")) / k, 1)
                out[m + sfx]["both"] = round(100 * hows.count("both") / k, 1)
    if split:
        out["halves"] = {}
        for m in halves:
            ma = [(r["date"], r[m]) for r in rows if r["date"] < split and r.get(m) is not None]
            mz = [(r["date"], r[m]) for r in rows if r["date"] >= split and r.get(m) is not None]
            out["halves"][m] = [round(cb.clustered(ma)[0], 3) if ma else None,
                                round(cb.clustered(mz)[0], 3) if mz else None]
    return out


def report(res: dict) -> str:
    base = res["baseline"]
    lines = [f"# Hourly candlestick patterns, {res['asof']}", "",
             f"{res['names']} {res['universe']}, hourly bars {res['first']} to {res['last']} ({res['sessions']} sessions); "
             f"method in the `scripts/candle_backtest.py` docstring. 'net' is after slippage on market fills (entry, "
             f"stops, closes; 5 bps a side at $20+, 20 at $5-20, 50 under $5), 'gross' before any cost; means % "
             f"± 95% clustered by date. 'up' is the share of trades that rose (gross). Edge = signal minus baseline "
             f"(gross), also for each half of the dates (split {res['split']}).", "",
             "## Next hour and the rest of the session (all sessions)", "",
             "| signal | n | per day | next hour net | gross | up | to the close net | gross | next close net | "
             "edge 1h | edge 1h by half | edge to the close |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def cell(s, m):
        x = s.get(m)
        return f"{x['mean']:+.2f} ± {x['ci']:.2f}" if x and x.get("ci") is not None else "-"

    def edge(s, m):
        x, y = s.get(m), base.get(m)
        return f"{x['mean'] - y['mean']:+.2f}" if x and y else "-"

    def halves(s, m):
        hs, hb = s.get("halves", {}).get(m), base.get("halves", {}).get(m)
        if not hs or not hb or None in hs or None in hb:
            return "-"
        return f"{hs[0] - hb[0]:+.2f} / {hs[1] - hb[1]:+.2f}"

    for name, s in [("baseline (every bar)", base)] + [(k, res["signals"][k]) for k in BULL + BEAR
                                                       if k in res["signals"]]:
        up = s.get("1h_g", {}).get("pos")
        lines.append(f"| {name} | {s['n']} | {s['n'] / res['sessions']:.1f} | {cell(s, '1h')} | {cell(s, '1h_g')} | "
                     f"{up:.0f}% | {cell(s, 'close')} | {cell(s, 'close_g')} | {cell(s, 'next')} | "
                     f"{edge(s, '1h_g')} | {halves(s, '1h_g')} | {edge(s, 'close_g')} |")
    lines += ["", f"## The +0.5% scalp on 5-minute bars ({res['m5_first']} to {res['last']}, {res['m5_sessions']} "
              f"sessions)", "",
              "Bought at the next hour's open; sold at +0.5%, else at the stop, else at the session close. 'both' is "
              "the share of trades whose stop and target fell inside one 5-minute bar (counted as the stop).", "",
              "| signal | n | +0.5%/-0.5% net | gross | target / stop (both) | +0.5%/pattern low net | gross | "
              "target / stop | +0.5%/no stop net | gross | target hit |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, s in [("baseline (every bar)", base)] + [(k, res["signals"][k]) for k in BULL if k in res["signals"]]:
        t, lw, ns = s.get("s_tight_g") or {}, s.get("s_low_g") or {}, s.get("s_nostop_g") or {}
        lines.append(f"| {name} | {t.get('n', 0)} | {cell(s, 's_tight')} | {cell(s, 's_tight_g')} | "
                     f"{t.get('target', '-')}% / {t.get('stop', '-')}% ({t.get('both', '-')}%) | {cell(s, 's_low')} | "
                     f"{cell(s, 's_low_g')} | {lw.get('target', '-')}% / {lw.get('stop', '-')}% | "
                     f"{cell(s, 's_nostop')} | {cell(s, 's_nostop_g')} | {ns.get('target', '-')}% |")
    lines += ["", "## Reading", ""] + res.get("reading", [])
    return "\n".join(lines) + "\n"


DAILY = ("d1", "d3", "d5")


def run_daily(rows: list[dict]) -> tuple[dict, list]:
    """The same signals on daily candles: bought at the next day's open, sold at its close, 3 or 5 sessions later."""
    b = [(dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat(), 0,
          r["o"], r["h"], r["l"], r["c"]) for r in rows]
    sig_rows: dict[str, list] = defaultdict(list)
    base: list = []
    for i in range(14, len(b) - 5):
        e = b[i + 1][2]
        if e <= 0:
            continue
        avg = sum(abs(b[k][5] - b[k][2]) for k in range(i - 10, i)) / 10
        row = {"date": b[i][0]}
        for net in (True, False):
            sfx = "" if net else "_g"
            for m, k in (("d1", 1), ("d3", 3), ("d5", 5)):
                row[m + sfx] = ret(e, b[i + k][5], net)
        base.append(row)
        for s_ in signals(b, i, avg):
            sig_rows[s_].append(row)
    return sig_rows, base


def report_daily(res: dict) -> str:
    base = res["baseline"]
    lines = [f"# Daily candlestick patterns, {res['asof']}", "",
             f"{res['names']} {res['universe']}, daily bars {res['first']} to {res['last']} ({res['sessions']} sessions); "
             f"method in the `scripts/candle_backtest.py` docstring (--daily). Bought at the next day's open; 'net' "
             f"after slippage (5 bps a side at $20+, 20 at $5-20, 50 under $5), 'gross' before costs; means % ± 95% "
             f"clustered by date. 'up' is the share that rose by the day's close (gross). Edge = signal minus baseline "
             f"(gross), also for each half of the dates (split {res['split']}).", "",
             "| signal | n | per day | that day net | gross | up | 3 days gross | 5 days net | gross | edge 1 day | "
             "edge 1 day by half | edge 5 days | edge 5 days by half |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def cell(s, m):
        x = s.get(m)
        return f"{x['mean']:+.2f} ± {x['ci']:.2f}" if x and x.get("ci") is not None else "-"

    def edge(s, m):
        x, y = s.get(m), base.get(m)
        return f"{x['mean'] - y['mean']:+.2f}" if x and y else "-"

    def halves(s, m):
        hs, hb = s.get("halves", {}).get(m), base.get("halves", {}).get(m)
        if not hs or not hb or None in hs or None in hb:
            return "-"
        return f"{hs[0] - hb[0]:+.2f} / {hs[1] - hb[1]:+.2f}"

    for name, s in [("baseline (every day)", base)] + [(k, res["signals"][k]) for k in BULL + BEAR
                                                       if k in res["signals"]]:
        up = s.get("d1_g", {}).get("pos")
        lines.append(f"| {name} | {s['n']} | {s['n'] / res['sessions']:.1f} | {cell(s, 'd1')} | {cell(s, 'd1_g')} | "
                     f"{up:.0f}% | {cell(s, 'd3_g')} | {cell(s, 'd5')} | {cell(s, 'd5_g')} | {edge(s, 'd1_g')} | "
                     f"{halves(s, 'd1_g')} | {edge(s, 'd5_g')} | {halves(s, 'd5_g')} |")
    lines += ["", "## Reading", ""] + res.get("reading", [])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tickers", help="comma list (default: the radar candidates)")
    ap.add_argument("--large-caps", action="store_true", help="the 60 largest US stocks plus SPY and QQQ")
    ap.add_argument("--daily", action="store_true", help="daily candles over 5 years instead of hourly")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [t.strip().upper() for t in a.tickers.split(",")] if a.tickers else LARGE if a.large_caps \
        else list(lv.CANDIDATES)
    universe = "large caps (60 largest US stocks, SPY, QQQ)" if a.large_caps and not a.tickers else \
        "names" if a.tickers else "radar candidates"
    if a.daily:
        with ThreadPoolExecutor(6) as ex:
            daily = dict(zip(syms, ex.map(lambda t: sb.daily(t, "5y"), syms)))
        sig_d: dict[str, list] = defaultdict(list)
        base_d: list = []
        for sym, rows in daily.items():
            if not rows or len(rows) < 60:
                print(f"  {sym}: no daily bars", file=sys.stderr)
                continue
            s_, bs = run_daily(rows)
            for k, v in s_.items():
                sig_d[k].extend(v)
            base_d.extend(bs)
        ds = sorted({r["date"] for r in base_d})
        split = ds[len(ds) // 2]
        res = {"asof": dt.date.today().isoformat(), "universe": universe,
               "names": sum(1 for r in daily.values() if r and len(r) >= 60), "first": ds[0], "last": ds[-1],
               "sessions": len(ds), "split": split,
               "baseline": summarize(base_d, split, DAILY, ("d1_g", "d5_g")),
               "signals": {k: summarize(v, split, DAILY, ("d1_g", "d5_g")) for k, v in sig_d.items()}}
        text = report_daily(res)
        print(text)
        if a.save:
            out = ROOT / "research" / "backtests" / f"candles-daily-{res['asof']}{'-large' if a.large_caps else ''}"
            out.with_suffix(".json").write_text(json.dumps(res, indent=2) + "\n")
            out.with_suffix(".md").write_text(text)
            print(f"saved {out.with_suffix('.md').relative_to(ROOT)}")
        return 0
    with ThreadPoolExecutor(6) as ex:
        data = dict(ex.map(load, syms))
    sig: dict[str, list] = defaultdict(list)
    base: list = []
    dates: set[str] = set()
    fine: set[str] = set()
    for sym, (h1, m5) in data.items():
        if not h1:
            print(f"  {sym}: no hourly bars", file=sys.stderr)
            continue
        s, bs = run(sym, h1, m5)
        for k, v in s.items():
            sig[k].extend(v)
        base.extend(bs)
        dates.update(h1)
        fine.update(m5)
    ds = sorted(dates)
    split = ds[len(ds) // 2]
    res = {"asof": dt.date.today().isoformat(), "universe": universe,
           "names": sum(1 for h, _ in data.values() if h), "first": ds[0],
           "last": ds[-1], "sessions": len(ds), "split": split, "m5_first": min(fine) if fine else None,
           "m5_sessions": len(fine), "baseline": summarize(base, split),
           "signals": {k: summarize(v, split) for k, v in sig.items()}}
    text = report(res)
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests" / f"candles-{res['asof']}{'-large' if a.large_caps else ''}"
        out.with_suffix(".json").write_text(json.dumps(res, indent=2) + "\n")
        out.with_suffix(".md").write_text(text)
        print(f"saved {out.with_suffix('.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
