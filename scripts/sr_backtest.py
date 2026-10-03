#!/usr/bin/env python3
"""Backtest of the support/resistance radar (scripts/levels.py) on daily bars, with no look-ahead:
the levels are rebuilt from the bars up to each day's close and traded from the next session.

  python scripts/sr_backtest.py [--tickers A,B] [--range 5y] [--save]

Entry rules compared:
  touch    buy when the day's low reaches the buy zone: fill at the zone top, or at the open when it
           opens inside the zone (the radar's live rule)
  confirm  wait for a rejection candle at the zone (low inside the zone, close in the top 40% of the day's
           range, no trade at or below the stop) and buy the next open
A trade sells at the sell-zone bottom (or the open when it gaps above), at the stop (or the open when it gaps
below), or at the close after N sessions (N = 0: the entry day's close, the one-session case). Daily bars can't
order a stop and a target hit on the same day, so the stop is assumed first, and a touch entry can't reach its
target on the entry day. One position per stock at a time. Costs: the trade.py slippage table on each side.
Control: the same stop and target distances (in ATR) from random days of the same stock on which the radar's
volatility and liquidity filters pass, to measure what the level timing adds over volatility alone.
Caveat: the stock list is today's, picked for being popular and volatile now (survivorship and selection bias).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
HOLDS = [0, 1, 3, 5, 10, 20]


def daily(sym: str, rng: str) -> list[dict] | None:
    try:
        r = md.yahoo_chart(sym, rng, "1d", False)
    except Exception as e:  # noqa: BLE001
        print(f"  {sym}: {str(e)[:80]}", file=sys.stderr)
        return None
    q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
    ts = r.get("timestamp") or []
    rows = []
    for i, t in enumerate(ts):
        o, h, lo, c, v = (q.get(k, [None] * len(ts))[i] for k in ("open", "high", "low", "close", "volume"))
        if None in (o, h, lo, c):
            continue
        rows.append({"t": t, "o": o, "h": h, "l": lo, "c": c, "v": v or 0})
    return rows


def slip(px: float) -> float:
    return 0.0005 if px >= 20 else 0.002 if px >= 5 else 0.005


def sma(rows: list[dict], i: int, n: int) -> float | None:
    return sum(r["c"] for r in rows[i - n + 1:i + 1]) / n if i + 1 >= n else None


def levels_by_day(sym: str, rows: list[dict]) -> list[dict | None]:
    """Radar levels as of each day's close (None before 120 sessions of history)."""
    out: list[dict | None] = [None] * len(rows)
    for i in range(120, len(rows)):
        r = lv.analyse({"sym": sym, "rows": rows[max(0, i - 260):i + 1], "name": sym, "exchange": "", "type": ""})
        if not r:
            continue
        s50, s50p, s200 = sma(rows, i, 50), sma(rows, i - 10, 50), sma(rows, i, 200)
        r["trend200"] = None if s200 is None else rows[i]["c"] > s200
        r["sma50_up"] = None if s50 is None or s50p is None else s50 > s50p
        r["eligible"] = r["atr_pct"] >= lv.MIN_ATR_PCT and r["dollar_vol_20d"] >= lv.MIN_DOLLAR_VOL
        r["signal"] = (r["eligible"] and r["support_strength"] >= 2 and (r["reward_risk"] or 0) >= 1.5
                       and rows[i]["c"] > r["stop"])
        out[i] = r
    return out


def run_exit(rows: list[dict], j0: int, entry: float, stop: float, target: float, hold: int,
             same_day_target: bool) -> tuple[int, float, str]:
    """Walk forward from the entry day j0; returns (exit day, exit price, reason)."""
    for d in range(j0, len(rows)):
        b = rows[d]
        if d > j0 and b["o"] <= stop:
            return d, b["o"], "stop"
        if b["l"] <= stop:
            return d, stop, "stop"
        if d > j0 or same_day_target:
            if d > j0 and b["o"] >= target:
                return d, b["o"], "target"
            if b["h"] >= target:
                return d, target, "target"
        if d - j0 >= hold:
            return d, b["c"], "time"
    return len(rows) - 1, rows[-1]["c"], "open"


def trade_rec(sym, rows, L, j, d, entry, stop, target, xp, why, extra=None) -> dict:
    gross = xp / entry - 1
    net = (xp * (1 - slip(xp))) / (entry * (1 + slip(entry))) - 1
    risk = (entry - stop) / entry
    rec = {"sym": sym, "date": dt.datetime.fromtimestamp(rows[j]["t"], dt.timezone.utc).strftime("%Y-%m-%d"),
           "entry": round(entry, 4), "stop": round(stop, 4), "target": round(target, 4), "exit": round(xp, 4),
           "why": why, "days": d - j, "ret": round(net * 100, 3), "gross": round(gross * 100, 3),
           "R": round(net / risk, 3) if risk > 0 else 0.0, "atr_pct": L["atr_pct"], "strength": L["support_strength"],
           "rr": L["reward_risk"], "trend200": L["trend200"], "sma50_up": L["sma50_up"],
           "crypto": sym in lv.CRYPTO_LINKED}
    if extra:
        rec.update(extra)
    return rec


def simulate(sym: str, rows: list[dict], lvl: list, rule: str, hold: int) -> list[dict]:
    trades, j = [], 121
    while j < len(rows) - 1:
        L = lvl[j - 1]
        if not L or not L["signal"]:
            j += 1
            continue
        b = rows[j]
        zone_top, stop, target = L["buy_zone"][1], L["stop"], L["sell_zone"][0]
        if b["l"] > zone_top or b["o"] <= stop:
            j += 1
            continue
        vol20 = sum(r["v"] for r in rows[j - 20:j]) / 20 or 1
        extra = {"rvol": round(b["v"] / vol20, 2)}
        if rule == "touch":
            entry = min(b["o"], zone_top)
            if entry >= target:
                j += 1
                continue
            d, xp, why = run_exit(rows, j, entry, stop, target, hold, same_day_target=False)
            trades.append(trade_rec(sym, rows, L, j, d, entry, stop, target, xp, why, extra))
            j = d + 1
        else:  # confirm: rejection candle on the touch day, buy the next open
            rng = b["h"] - b["l"]
            if b["l"] <= stop or rng <= 0 or b["c"] < b["l"] + 0.6 * rng or j + 1 >= len(rows):
                j += 1
                continue
            entry = rows[j + 1]["o"]
            if not stop < entry < target:
                j += 1
                continue
            d, xp, why = run_exit(rows, j + 1, entry, stop, target, hold, same_day_target=True)
            trades.append(trade_rec(sym, rows, L, j + 1, d, entry, stop, target, xp, why, extra))
            j = d + 1
    return trades


def control(sym: str, rows: list[dict], lvl: list, trades: list[dict], hold: int, k: int, rnd) -> list[float]:
    """R of random-day entries (open) with each trade's stop and target distances in ATR."""
    days = [j for j in range(121, len(rows) - 1) if lvl[j - 1] and lvl[j - 1]["eligible"]]
    out = []
    if not days:
        return out
    for t in trades:
        atr = t["atr_pct"] / 100 * t["entry"]
        ds, dtg = (t["entry"] - t["stop"]) / atr, (t["target"] - t["entry"]) / atr
        for _ in range(k):
            j = rnd.choice(days)
            a = lvl[j - 1]["atr"]
            entry = rows[j]["o"]
            stop, target = entry - ds * a, entry + dtg * a
            if stop <= 0:
                continue
            d, xp, _ = run_exit(rows, j, entry, stop, target, hold, same_day_target=True)
            net = (xp * (1 - slip(xp))) / (entry * (1 + slip(entry))) - 1
            out.append(net / ((entry - stop) / entry))
    return out


def ci(xs: list[float], rnd, n: int = 2000) -> tuple[float, float]:
    if len(xs) < 2:
        return (float("nan"), float("nan"))
    means = sorted(st.fmean(rnd.choices(xs, k=len(xs))) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def summary(trades: list[dict], rnd) -> dict:
    if not trades:
        return {"n": 0}
    rs = [t["R"] for t in trades]
    lo, hi = ci(rs, rnd)
    return {"n": len(trades), "win": round(100 * sum(t["ret"] > 0 for t in trades) / len(trades), 1),
            "target": round(100 * sum(t["why"] == "target" for t in trades) / len(trades), 1),
            "stop": round(100 * sum(t["why"] == "stop" for t in trades) / len(trades), 1),
            "avg_R": round(st.fmean(rs), 3), "ci_R": [round(lo, 3), round(hi, 3)],
            "avg_ret": round(st.fmean(t["ret"] for t in trades), 2),
            "med_ret": round(st.median(t["ret"] for t in trades), 2),
            "avg_days": round(st.fmean(t["days"] for t in trades), 1)}


def line(name: str, s: dict) -> str:
    if not s.get("n"):
        return f"{name:34} n=0"
    return (f"{name:34} n={s['n']:4} win {s['win']:5.1f}% target {s['target']:5.1f}% stop {s['stop']:5.1f}% "
            f"avgR {s['avg_R']:+.3f} [{s['ci_R'][0]:+.3f},{s['ci_R'][1]:+.3f}] ret {s['avg_ret']:+.2f}% "
            f"(median {s['med_ret']:+.2f}%) days {s['avg_days']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--range", default="5y")
    ap.add_argument("--control", type=int, default=20, help="random entries per trade for the control")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    with ThreadPoolExecutor(max_workers=8) as ex:
        data = dict(zip(syms, ex.map(lambda s: daily(s, a.range), syms)))
    data = {s: r for s, r in data.items() if r and len(r) > 200}
    print(f"{len(data)} stocks, {sum(len(r) for r in data.values())} daily bars")
    lvls = {s: levels_by_day(s, r) for s, r in data.items()}
    rnd = random.Random(7)
    results: dict = {"generated_at": pfm.iso(pfm.now_utc()), "range": a.range, "stocks": sorted(data), "runs": {}}
    report = []

    def show(text: str) -> None:
        print(text)
        report.append(text)

    for rule in ("touch", "confirm"):
        show(f"\n== {rule}")
        for hold in HOLDS:
            tr = [t for s in data for t in simulate(s, data[s], lvls[s], rule, hold)]
            s = summary(tr, rnd)
            ctrl = [x for sy in data for x in control(sy, data[sy], lvls[sy], [t for t in tr if t["sym"] == sy],
                                                       hold, a.control, rnd)] if hold in (0, 10) else []
            cs = {"n": len(ctrl), "avg_R": round(st.fmean(ctrl), 3), "ci_R": [round(v, 3) for v in ci(ctrl, rnd, 500)]} \
                if ctrl else None
            show(line(f"{rule} hold {hold}", s) + (f" | control avgR {cs['avg_R']:+.3f} "
                                                  f"[{cs['ci_R'][0]:+.3f},{cs['ci_R'][1]:+.3f}]" if cs else ""))
            results["runs"][f"{rule}_{hold}"] = {"summary": s, "control": cs}
            if hold == 10:
                results["runs"][f"{rule}_{hold}"]["trades"] = tr
                for label, f in (("above 200-day", lambda t: t["trend200"] is True),
                                 ("below 200-day", lambda t: t["trend200"] is False),
                                 ("50-day rising", lambda t: t["sma50_up"] is True),
                                 ("50-day falling", lambda t: t["sma50_up"] is False),
                                 ("touch-day volume < 20d avg", lambda t: t["rvol"] < 1),
                                 ("touch-day volume >= 1.5x avg", lambda t: t["rvol"] >= 1.5),
                                 ("support tested 2x", lambda t: t["strength"] == 2),
                                 ("support tested 3x+", lambda t: t["strength"] >= 3),
                                 ("R:R 1.5-2", lambda t: t["rr"] < 2),
                                 ("R:R 2+", lambda t: t["rr"] >= 2),
                                 ("crypto-linked", lambda t: t["crypto"]),
                                 ("not crypto-linked", lambda t: not t["crypto"])):
                    show("   " + line(label, summary([t for t in tr if f(t)], rnd)))
    if a.save:
        d = pfm.et_date(pfm.now_utc()).isoformat()
        out = ROOT / "research" / "backtests"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"sr-{d}.json").write_text(json.dumps(results, indent=1) + "\n")
        (out / f"sr-{d}.md").write_text(
            f"# Support/resistance radar backtest ({d})\n\n{len(data)} stocks, daily bars over {a.range}; method in "
            f"`scripts/sr_backtest.py`. R = net return / risk to the stop; brackets = 95% bootstrap interval.\n\n"
            "```\n" + "\n".join(report) + "\n```\n")
        print(f"saved research/backtests/sr-{d}.md and .json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
