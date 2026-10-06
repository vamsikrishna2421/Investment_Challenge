#!/usr/bin/env python3
"""Is buying the opening dip an edge? (Vamsi, Mon Oct 5: buy when a stock has dipped a lot in the opening
minutes, inside its buy zone, and sell when it gets back to neutral; the opening panic often fades.)

  python scripts/dip_backtest.py [--tickers A,B] [--save]

Three tests on the radar candidates, each measured from the prior regular-session close:
  9:55   5-minute bars, last 60 sessions: buy at the 9:55 price (the radar's first entry run)
  10:30  hourly bars, last ~2 years: buy at the end of the first hour
  open   daily bars, 5 years: buy at the opening print (a gap only)
Exits: "close" sells at the day's close; "neutral" is a limit sell at the prior close if the price gets back
there after the entry, otherwise the close (only for entries below the prior close).
Only days on which the radar's filters pass at the prior close (ATR at least 4% of the price, $15M a day).
Groups: the entry's distance below the prior close in ATR units (the stock's normal daily range), and the
radar version: inside the buy zone of the radar built from the prior close (tested support, R:R 1.5+),
dipped 0.5+ ATR by the entry or not.
Costs: trade.py slippage on both sides. Each trade's return is capped at +/-25% so a handful of extreme days
(SBET +171% on May 29, 2025) don't swamp the averages; the median is shown too. Dips come market-wide on the
same days, so standard errors are clustered by date. No stop is used. Caveat: today's list of popular volatile stocks (survivorship and
selection bias), and 60 sessions of 5-minute bars is one market regime.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import levels as lv  # noqa: E402
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
BUCKETS = [("up 0.25+ ATR", 0.25, 99), ("flat (within 0.25 ATR)", -0.25, 0.25), ("down 0.25-0.5 ATR", -0.5, -0.25),
           ("down 0.5-0.75 ATR", -0.75, -0.5), ("down 0.75-1 ATR", -1.0, -0.75), ("down 1+ ATR", -99, -1.0)]


def by_day(r: dict) -> dict[str, list[tuple[int, float, float, float, float]]]:
    """Regular-session bars per ET date: (minute of day at bar start, open, high, low, close)."""
    q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
    out: dict[str, list] = {}
    for i, t in enumerate(r.get("timestamp") or []):
        o, h, lo, c = (q.get(k, [None] * (i + 1))[i] for k in ("open", "high", "low", "close"))
        if None in (o, h, lo, c):
            continue
        d = dt.datetime.fromtimestamp(t, dt.timezone.utc).astimezone(pfm.ET)
        m = d.hour * 60 + d.minute
        if 570 <= m < 960:
            out.setdefault(d.date().isoformat(), []).append((m, o, h, lo, c))
    return out


def load(sym: str):
    daily = sb.daily(sym, "5y")
    try:
        m5 = by_day(md.yahoo_chart(sym, "60d", "5m", False))
    except Exception:  # noqa: BLE001
        m5 = {}
    try:
        h1 = by_day(md.yahoo_chart(sym, "730d", "1h", False))
    except Exception:  # noqa: BLE001
        h1 = {}
    return sym, daily, m5, h1


def trade(e: float, prev: float, close: float, after: list[tuple]) -> dict:
    s_in = sb.slip(e)
    r_close = (close * (1 - sb.slip(close)) / (e * (1 + s_in)) - 1) * 100
    if e < prev and any(b[2] >= prev for b in after):
        r_neutral, hit = (prev * (1 - sb.slip(prev)) / (e * (1 + s_in)) - 1) * 100, 1.0
    else:
        r_neutral, hit = r_close, 0.0
    return {"close": r_close, "neutral": r_neutral, "hit": hit}


def events(sym: str, daily: list[dict], m5: dict, h1: dict) -> list[dict]:
    out = []
    idx = {dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat(): i
           for i, r in enumerate(daily)}
    radar_cache: dict[int, dict | None] = {}

    def radar(i: int) -> dict | None:
        if i not in radar_cache:
            radar_cache[i] = lv.analyse({"sym": sym, "rows": daily[max(0, i - 260):i], "name": sym,
                                         "exchange": "", "type": ""}) if i >= 120 else None
        return radar_cache[i]

    for d, i in idx.items():
        if i < 260:
            continue
        prev = daily[i - 1]["c"]
        win = daily[i - 15:i]
        atr = sum(max(win[k]["h"] - win[k]["l"], abs(win[k]["h"] - win[k - 1]["c"]), abs(win[k]["l"] - win[k - 1]["c"]))
                  for k in range(1, len(win))) / (len(win) - 1)
        atr_pct = atr / prev * 100
        dv = sum(r["c"] * r["v"] for r in daily[i - 20:i]) / 20
        if atr_pct < lv.MIN_ATR_PCT or dv < lv.MIN_DOLLAR_VOL:
            continue
        close = daily[i]["c"]
        tests = [("open", daily[i]["o"], [(570, daily[i]["o"], daily[i]["h"], daily[i]["l"], close)])]
        if d in m5:
            e = next((b[4] for b in m5[d] if b[0] == 590), None)
            if e:
                tests.append(("9:55", e, [b for b in m5[d] if b[0] >= 595]))
        if d in h1:
            e = next((b[4] for b in h1[d] if b[0] == 570), None)
            if e:
                tests.append(("10:30", e, [b for b in h1[d] if b[0] >= 630]))
        a = radar(i)
        for name, e, after in tests:
            if not e or e <= 0:
                continue
            dip = (e / prev - 1) * 100 / atr_pct
            zone = bool(a and a["support_strength"] >= 2 and (a["reward_risk"] or 0) >= 1.5
                        and a["stop"] < e <= a["buy_zone"][1])
            out.append({"sym": sym, "date": d, "test": name, "dip_atr": dip, "zone": zone, **trade(e, prev, close, after)})
    return out


def stats(rows: list[dict]) -> dict:
    out = {"n": len(rows), "dates": len({r["date"] for r in rows})}
    for k in ("close", "neutral", "hit"):
        cap = (lambda v: max(-25.0, min(25.0, v))) if k != "hit" else (lambda v: v)
        m, se = cb.clustered([(r["date"], cap(r[k])) for r in rows])
        out[k], out[k + "_se"] = round(m, 3), round(se, 3)
    if rows:
        srt = sorted(r["neutral"] for r in rows)
        out["median"] = round(srt[len(srt) // 2], 3)
    out["win"] = round(sum(1 for r in rows if r["neutral"] > 0) / len(rows), 3) if rows else None
    return out


def run(syms: list[str]) -> dict:
    with ThreadPoolExecutor(8) as ex:
        loaded = list(ex.map(load, syms))
    rows = []
    for sym, daily, m5, h1 in loaded:
        if daily and len(daily) > 270:
            rows += events(sym, daily, m5, h1)
    res = {"names": sum(1 for _, d, _, _ in loaded if d and len(d) > 270), "tests": {}}
    for t in ("9:55", "10:30", "open"):
        tr = [r for r in rows if r["test"] == t]
        g = {"all eligible": stats(tr)}
        for label, lo, hi in BUCKETS:
            g[label] = stats([r for r in tr if lo <= r["dip_atr"] < hi])
        z = [r for r in tr if r["zone"]]
        g["radar buy zone, all"] = stats(z)
        g["radar buy zone, dipped 0.5+ ATR"] = stats([r for r in z if r["dip_atr"] <= -0.5])
        g["radar buy zone, dipped less"] = stats([r for r in z if r["dip_atr"] > -0.5])
        span = sorted({r["date"] for r in tr})
        res["tests"][t] = {"groups": g, "from": span[0] if span else None, "to": span[-1] if span else None}
    return res


def report(res: dict) -> str:
    names = {"9:55": "Buy at 9:55 (5-minute bars)", "10:30": "Buy at 10:30 (hourly bars)", "open": "Buy at the open (daily bars)"}
    L = [f"# Opening-dip backtest ({dt.date.today().isoformat()})", "",
         f"{res['names']} radar candidates. Method and caveats: `scripts/dip_backtest.py` docstring. Returns are per "
         "trade after slippage, ± 95% intervals clustered by date; \"neutral\" sells at the prior close if the price "
         "gets back there, otherwise at the close.", ""]
    for t, v in res["tests"].items():
        L += [f"## {names[t]}, {v['from']} to {v['to']}", "",
              "| Entry vs prior close | Trades | Days | Hold to close % | Sell at neutral % | Median (neutral) % | Got back to neutral | Winners |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
        for label, g in v["groups"].items():
            if not g["n"]:
                L.append(f"| {label} | 0 | | | | | | |")
                continue
            L.append(f"| {label} | {g['n']:,} | {g['dates']:,} | {g['close']:+.2f} ± {1.96 * g['close_se']:.2f} | "
                     f"{g['neutral']:+.2f} ± {1.96 * g['neutral_se']:.2f} | {g['median']:+.2f} | {g['hit'] * 100:.0f}% | "
                     f"{g['win'] * 100:.0f}% |")
        L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    res = run(syms)
    text = report(res)
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests"
        out.mkdir(parents=True, exist_ok=True)
        stem = f"dip-{dt.date.today().isoformat()}"
        (out / f"{stem}.md").write_text(text)
        (out / f"{stem}.json").write_text(json.dumps(res, indent=1) + "\n")
        print("saved", (out / f"{stem}.md").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
