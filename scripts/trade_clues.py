#!/usr/bin/env python3
"""Every support-limit trade the radar would have offered, one by one: which exit works best, and which clues at
entry warned that a trade would be stopped out fast (Vamsi, Tue Oct 6: take the desired profit and move on to the
next opportunity; the trades stopped within 3 sessions must have left clues).

  python scripts/trade_clues.py [--days 700] [--save]

Unlike scripts/replay.py, which runs one $1,000 book with 4 slots (so which trades happen depends on which came
first), this takes every candidate: each session, each radar name (radar rebuilt from the prior closes) within 8%
above its support with R:R 1.5+ from support gets a DAY buy limit at support, as orders.py plan places them; the
9:25 check cancels it when the stock opens at or under the stop. On hourly bars (2.8 years), a fill needs a bar
1 cent through the limit (at the limit, or the bar's open when lower). The exit rules then run on the same entry,
one bar at a time:
  stop      a bar at or under the stop sells at the stop, or at a lower open, less slippage (checked first)
  target    a bar closing at or above the exit's target sells at that close (a run check), less slippage
  plan      target = the sell-zone bottom (the live rule)
  pct N     target = the entry + N%, or the sell-zone bottom if nearer ("take the desired profit")
  r N       target = the entry + N times the entry-to-stop distance (N R), or the sell-zone bottom if nearer
  be        the plan target, with the stop raised to the entry once the price has gained 1 R
  time 3    the plan, sold at the close of the third session if still open
Trades still open after 30 sessions are sold at that close. Clues: the features below, from the daily bars up to
the prior close and the intraday bars up to the fill, compared between the first and second half of the period
(a clue counts only when it points the same way in both halves). Returns are per trade, clustered by entry date.
Caveat: today's candidate list (selection bias), and a fill model on hourly bars.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402
import replay as rp  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
TICK, NEAR, MAX_HOLD = 0.01, 8.0, 30
EXITS = ["plan", "pct 3", "pct 5", "pct 8", "pct 12", "r 1", "r 1.5", "r 2", "be", "time 3"]
FEATURES = {
    "gap_atr": "open against the prior close, ATR",
    "dip_atr": "entry against the prior close, ATR",
    "fill_min": "fill time (minute of the day; 570 = the first hour)",
    "spy_day": "S&P 500 (SPY) at the fill bar's start against its prior close, %",
    "spy_trend": "SPY prior close against its 20-day average, %",
    "spy_ret5": "SPY over the 5 sessions before, %",
    "trend20": "stock's prior close against its 20-day average, %",
    "trend50": "stock's prior close against its 50-day average, %",
    "ret20": "stock over the 20 sessions before, %",
    "ret5_atr": "stock over the 5 sessions before, ATR",
    "rs20": "stock minus SPY over the 20 sessions before, %",
    "atr_pct": "ATR as % of the price",
    "clv": "prior day's close location in its range (0 = at the low, 1 = at the high)",
    "vol_ratio": "prior day's volume against its 20-day average",
    "strength": "swings in the support zone (times tested)",
    "touch_age": "sessions since the price last touched the buy zone",
    "dist_atr": "prior close above support, ATR",
    "rr": "R:R from the limit",
    "room_atr": "entry to the sell-zone bottom, ATR",
    "breadth": "share of radar names under their prior close at the fill bar's start",
    "fills_today": "radar limits filled the same session",
}


def sma(rows: list[dict], i: int, n: int) -> float:
    return sum(r["c"] for r in rows[i - n:i]) / n


def exits(entry: float, stop: float, target: float, atr: float, path: list[tuple[int, int, tuple]]) -> dict:
    """path: (session offset, minute, bar) after the fill bar. Returns each exit rule's (return %, why, sessions)."""
    risk = entry - stop
    out = {}
    for rule in EXITS:
        kind, _, n = rule.partition(" ")
        take = target
        if kind == "pct":
            take = min(target, entry * (1 + float(n) / 100))
        elif kind == "r":
            take = min(target, entry + float(n) * risk)
        stp, res = stop, None
        for k, m, b in path:
            if b[3] <= stp:
                base = b[1] if b[1] < stp else stp
                px = base * (1 - sb.slip(base))
                res = (px / entry - 1) * 100, ("breakeven" if stp > stop else "stop"), k
                break
            if b[4] >= take:
                res = (b[4] * (1 - sb.slip(b[4])) / entry - 1) * 100, "target", k
                break
            if kind == "be" and b[2] >= entry + risk:
                stp = max(stp, entry)
            if kind == "time" and k >= int(n) - 1 and m == 930:
                res = (b[4] * (1 - sb.slip(b[4])) / entry - 1) * 100, "time", k
                break
        if res is None:
            k, m, b = path[-1] if path else (0, 0, (0, entry, entry, entry, entry))
            res = (b[4] * (1 - sb.slip(b[4])) / entry - 1) * 100, "open", k
        out[rule] = {"ret": round(res[0], 3), "why": res[1], "held": res[2] + 1}
    return out


def collect(data: dict, days: int) -> list[dict]:
    src = data["1h"]
    now = pfm.now_utc()
    today = pfm.et_date(now).isoformat()
    closed = now.astimezone(pfm.ET).hour >= 16
    all_days = sorted(d for d in src["SPY"] if d < today or (d == today and closed))
    sessions = all_days[-days:]
    pos = {d: k for k, d in enumerate(all_days)}
    idx = {s: {rp.et_day(r["t"]): i for i, r in enumerate(rows)} for s, rows in data["daily"].items()}
    blocked = set(json.loads((ROOT / "config" / "blocklist.json").read_text()).get("tickers", {}))
    names = [s for s in lv.CANDIDATES if s in data["daily"] and s in src and s not in blocked]
    spy = data["daily"]["SPY"]
    trades = []
    for day in sessions:
        radar, _ = rp.radar_for(data, idx, names, day, lv.STOP_ATR)
        si = idx["SPY"].get(day)
        if not si:
            continue
        spy_prev = spy[si - 1]["c"]
        spy_bars = {b[0]: b for b in src["SPY"].get(day, [])}
        gate = rp.btc_gate(data, day)
        prevs, opens = {}, {}
        for s in radar:
            i = idx[s].get(day)
            if i is not None and src[s].get(day):
                prevs[s] = data["daily"][s][i - 1]["c"]
                opens[s] = {b[0]: b[1] for b in src[s][day]}
        day_trades = []
        for s, r in radar.items():
            i = idx[s].get(day)
            rows = data["daily"][s]
            bars = src[s].get(day)
            if i is None or i < 60 or not bars or abs(bars[0][1] / rows[i]["o"] - 1) > 0.2:
                continue
            prev, S, stop, T, atr = rows[i - 1]["c"], r["S"], r["stop"], r["target"], r["atr"]
            lim = round(S, 2 if S >= 1 else 4)
            if prev <= stop or lim <= stop or (prev / lim - 1) * 100 > NEAR:
                continue
            rr = (T - lim) / (lim - stop)
            if rr < 1.5 or bars[0][1] <= stop:
                continue
            k0 = next((k for k, b in enumerate(bars) if b[3] <= lim - TICK), None)
            if k0 is None:
                continue
            b0 = bars[k0]
            entry = b0[1] if b0[1] <= lim - TICK else lim
            # the path after the fill: the fill bar's own stop first (cautious), then later bars
            path = []
            if b0[3] <= stop:
                path.append((0, b0[0], (b0[0], min(stop, entry), entry, b0[3], b0[4])))
            else:
                path.append((0, b0[0], (b0[0], entry, max(entry, b0[2]), max(b0[3], stop + 1e-9), b0[4])))
            path += [(0, b[0], b) for b in bars[k0 + 1:]]
            for k in range(1, MAX_HOLD):
                j = pos[day] + k
                if j >= len(all_days):
                    break
                path += [(k, b[0], b) for b in src[s].get(all_days[j], [])]
            win = rows[i - 20:i]
            vol20 = sum(x["v"] for x in rows[i - 21:i - 1]) / 20
            lo_zone = S - 0.25 * atr
            touch_age = next((n for n in range(1, 121) if i - n >= 0 and lo_zone <= rows[i - n]["l"] <= r["Z"]), 121)
            spy_open = spy_bars.get(b0[0], (0, spy_prev))[1]
            under = sum(1 for x in prevs if opens[x].get(b0[0], prevs[x]) < prevs[x])
            f = {
                "gap_atr": (bars[0][1] - prev) / atr, "dip_atr": (entry - prev) / atr, "fill_min": b0[0],
                "spy_day": (spy_open / spy_prev - 1) * 100, "spy_trend": (spy_prev / sma(spy, si, 20) - 1) * 100,
                "spy_ret5": (spy_prev / spy[si - 6]["c"] - 1) * 100,
                "trend20": (prev / sma(rows, i, 20) - 1) * 100, "trend50": (prev / sma(rows, i, 50) - 1) * 100,
                "ret20": (prev / rows[i - 21]["c"] - 1) * 100, "ret5_atr": (prev - rows[i - 6]["c"]) / atr,
                "rs20": (prev / rows[i - 21]["c"] - spy_prev / spy[si - 21]["c"]) * 100,
                "atr_pct": atr / prev * 100,
                "clv": (win[-1]["c"] - win[-1]["l"]) / (win[-1]["h"] - win[-1]["l"]) if win[-1]["h"] > win[-1]["l"] else 0.5,
                "vol_ratio": win[-1]["v"] / vol20 if vol20 else 1.0, "strength": r["strength"], "touch_age": touch_age,
                "dist_atr": (prev - S) / atr, "rr": rr, "room_atr": (T - entry) / atr,
                "breadth": under / len(prevs) if prevs else 0.0,
            }
            ex = exits(entry, stop, T, atr, path)
            day_trades.append({"day": day, "ticker": s, "entry": round(entry, 4), "crypto": r["crypto"],
                               "btc_ok": gate["ok"], "btc_d1": gate.get("d1"),
                               "features": {k: round(v, 4) for k, v in f.items()}, "exits": ex})
        for t in day_trades:
            t["features"]["fills_today"] = len(day_trades)
        trades += day_trades
    return trades


def ci(rows: list[tuple[str, float]]) -> str:
    if len(rows) < 5:
        return "-"
    m, se = cb.clustered(rows)
    return f"{m:+.2f} ± {1.96 * se:.2f}"


def exit_table(trades: list[dict]) -> list[str]:
    L = ["| Exit | Average a trade | Median | Winners | Stopped | Sessions held | Average a session held |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for rule in EXITS:
        xs = [(t["day"], t["exits"][rule]["ret"]) for t in trades]
        held = [t["exits"][rule]["held"] for t in trades]
        rets = [x for _, x in xs]
        stopped = sum(1 for t in trades if t["exits"][rule]["why"] == "stop")
        L.append(f"| {rule} | {ci(xs)}% | {st.median(rets):+.2f}% | {sum(1 for x in rets if x > 0) / len(rets) * 100:.0f}% | "
                 f"{stopped / len(rets) * 100:.0f}% | {st.mean(held):.1f} | {st.mean(rets) / st.mean(held):+.3f}% |")
    return L


def clue_table(trades: list[dict]) -> tuple[list[str], list[dict]]:
    """Each feature in terciles (cut points from the first half): quick stops (stopped within 3 sessions) and the
    plan exit's return, first half against second half."""
    days = sorted({t["day"] for t in trades})
    mid = days[len(days) // 2]
    h1 = [t for t in trades if t["day"] < mid]
    h2 = [t for t in trades if t["day"] >= mid]

    def quick(t):
        e = t["exits"]["plan"]
        return 1.0 if e["why"] == "stop" and e["held"] <= 3 else 0.0
    L = [f"First half {days[0]} to {mid} ({len(h1)} trades), second half {mid} to {days[-1]} ({len(h2)}). "
         "Quick stop: stopped within 3 sessions under the plan exit. Each cell: quick-stop rate, then the plan exit's "
         "average return.", "",
         "| Clue | Tercile | First half: quick stops / return | Second half: quick stops / return | Same direction |",
         "|---|---|---|---|---|"]
    found = []
    for k, desc in FEATURES.items():
        vals = sorted(t["features"][k] for t in h1)
        if len(set(vals)) < 3:
            continue
        c1, c2 = vals[len(vals) // 3], vals[2 * len(vals) // 3]
        if c1 == c2:
            continue
        cuts = [(-1e18, c1, f"low (< {c1:.3g})"), (c1, c2, "mid"), (c2, 1e18, f"high (>= {c2:.3g})")]
        cells, diffs = [], []
        for half in (h1, h2):
            row = []
            for lo, hi, _ in cuts:
                g = [t for t in half if lo <= t["features"][k] < hi]
                q = st.mean(quick(t) for t in g) if g else float("nan")
                row.append((g, q))
            cells.append(row)
            diffs.append(row[2][1] - row[0][1])
        same = diffs[0] * diffs[1] > 0
        hi_g = [t for t in trades if t["features"][k] >= c2]
        lo_g = [t for t in trades if t["features"][k] < c1]
        mh, sh = cb.clustered([(t["day"], quick(t)) for t in hi_g])
        ml, sl = cb.clustered([(t["day"], quick(t)) for t in lo_g])
        z = (mh - ml) / ((sh ** 2 + sl ** 2) ** 0.5) if sh and sl else 0.0
        found.append({"feature": k, "desc": desc, "low_cut": c1, "high_cut": c2, "quick_low": ml, "quick_high": mh,
                      "z": round(z, 2), "same_direction": same, "diff_h1": diffs[0], "diff_h2": diffs[1]})
        for n, (lo, hi, lab) in enumerate(cuts):
            a, b = cells[0][n], cells[1][n]
            fmt = lambda g, q: (f"{q * 100:.0f}% / {st.mean(t['exits']['plan']['ret'] for t in g):+.2f}% (n={len(g)})"
                                if g else "-")
            L.append(f"| {desc if n == 0 else ''} | {lab} | {fmt(*a)} | {fmt(*b)} | "
                     f"{('yes' if same else 'no') + f', z {z:+.1f}' if n == 0 else ''} |")
    return L, found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=700)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    data = rp.load_data(lv.CANDIDATES, a.refresh)
    trades = collect(data, a.days)
    days = sorted({t["day"] for t in trades})
    quick = [t for t in trades if t["exits"]["plan"]["why"] == "stop" and t["exits"]["plan"]["held"] <= 3]
    head = [f"# Support-limit trades one by one: exits and clues ({days[0]} to {days[-1]})", "",
            f"{len(trades)} limit fills on {len(days)} sessions (hourly bars). Under the live exit (stop 0.6 ATR under "
            f"support, sell at the sell-zone bottom) {len(quick)} ({len(quick) / len(trades) * 100:.0f}%) were stopped "
            "within 3 sessions. Method and caveats: `scripts/trade_clues.py` docstring. ± is a 95% interval clustered "
            "by entry date.", "", "## Exits on the same entries", ""]
    L = head + exit_table(trades) + ["", "## Clues at entry: what the quick stop-outs had in common", ""]
    ct, found = clue_table(trades)
    L += ct
    keep = sorted((f for f in found if f["same_direction"] and abs(f["z"]) >= 2), key=lambda f: -abs(f["z"]))
    L += ["", "## Clues that held in both halves (|z| >= 2)", ""]
    L += [f"- {f['desc']}: quick stops {f['quick_low'] * 100:.0f}% in the low tercile (< {f['low_cut']:.3g}) against "
          f"{f['quick_high'] * 100:.0f}% in the high tercile (>= {f['high_cut']:.3g}), z {f['z']:+.1f}" for f in keep] or ["- none"]
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests"
        stem = f"trade-clues-{days[-1]}"
        (out / f"{stem}.md").write_text(text)
        (out / f"{stem}.json").write_text(json.dumps({"found": found, "n": len(trades)}, indent=1) + "\n")
        print("saved", (out / f"{stem}.md").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
