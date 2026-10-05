#!/usr/bin/env python3
"""Do the clue flags in scripts/clues.py come before big moves more often than chance? (Vamsi, Mon Oct 5.)

  python scripts/clue_backtest.py [--tickers A,B] [--range 5y] [--save]

For every stock in the candidate list and every session with a year of history on which the radar's volatility
and liquidity filters pass (ATR at least 4% of the price, $15M a day), the clue flags are computed from the bars
through that session's close (clues.features: SUP, COIL, ACC, HL, RES; no look-ahead) and compared with the
next session:
  big up       the next close at least 1 ATR above this close (the post-mortem's "big move")
  next         next close against this close, in %
  open->close  next open to next close after trade.py slippage on both sides (what a buyer at the open keeps)
  max up       next high against this close, in ATR (room for a sell-zone exit)
  big down     the next close at least 1 ATR below (a clue that only raises volatility lifts both)
  5-day        the close 5 sessions later, in %; big up 5d = any close in the next 5 sessions 2+ ATR higher
Groups: every eligible name-day (the base rate), each flag, the bounce score 0-4, SUP+HL and the breakout watch.
Stocks move together, so name-days on the same date are not independent: standard errors are clustered by date.
Same caveat as sr_backtest.py: today's list of popular volatile stocks (survivorship and selection bias).
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
import clues  # noqa: E402
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
WIN = 260


def name_days(sym: str, rows: list[dict]) -> list[dict]:
    out = []
    for i in range(WIN, len(rows) - 5):
        win = rows[i - WIN + 1:i + 1]
        dv = sum(r["c"] * r["v"] for r in win[-20:]) / 20
        if dv < lv.MIN_DOLLAR_VOL:
            continue
        f = clues.features(win)
        if not f or f["atr_pct"] < lv.MIN_ATR_PCT:
            continue
        c, n = win[-1]["c"], rows[i + 1]
        nxt = (n["c"] / c - 1) * 100
        oc = (n["c"] * (1 - sb.slip(n["c"])) / (n["o"] * (1 + sb.slip(n["o"]))) - 1) * 100 if n["o"] else 0.0
        out.append({
            "sym": sym, "date": dt.datetime.fromtimestamp(n["t"], dt.timezone.utc).date().isoformat(),
            "flags": f["flags"], "score": f["score"], "breakout": f["breakout"],
            "big_up": 1.0 if nxt >= f["atr_pct"] else 0.0, "next": nxt, "oc": oc,
            "maxup": (n["h"] / c - 1) * 100 / f["atr_pct"],
            "big_down": 1.0 if nxt <= -f["atr_pct"] else 0.0,
            "next5": (rows[i + 5]["c"] / c - 1) * 100,
            "big_up5": 1.0 if max(r["c"] for r in rows[i + 1:i + 6]) >= c * (1 + 2 * f["atr_pct"] / 100) else 0.0,
        })
    return out


def clustered(xs: list[tuple[str, float]]) -> tuple[float, float]:
    """Mean and its standard error clustered by date."""
    n = len(xs)
    if not n:
        return float("nan"), float("nan")
    m = sum(v for _, v in xs) / n
    by = defaultdict(float)
    for d, v in xs:
        by[d] += v - m
    return m, math.sqrt(sum(s * s for s in by.values())) / n


def group_stats(rows: list[dict]) -> dict:
    out = {"n": len(rows), "dates": len({r["date"] for r in rows})}
    for k in ("big_up", "big_down", "next", "oc", "maxup", "next5", "big_up5"):
        m, se = clustered([(r["date"], r[k]) for r in rows])
        out[k] = round(m, 4)
        out[k + "_se"] = round(se, 4)
    return out


GROUPS = [
    ("all eligible name-days", lambda r: True),
    ("SUP", lambda r: "SUP" in r["flags"]),
    ("COIL", lambda r: "COIL" in r["flags"]),
    ("ACC", lambda r: "ACC" in r["flags"]),
    ("HL", lambda r: "HL" in r["flags"]),
    ("RES", lambda r: "RES" in r["flags"]),
    ("score 0", lambda r: r["score"] == 0),
    ("score 1", lambda r: r["score"] == 1),
    ("score 2", lambda r: r["score"] == 2),
    ("score 3", lambda r: r["score"] == 3),
    ("score 4", lambda r: r["score"] == 4),
    ("score 3+ (scan alert)", lambda r: r["score"] >= 3),
    ("SUP + HL", lambda r: "SUP" in r["flags"] and "HL" in r["flags"]),
    ("breakout watch (RES + COIL)", lambda r: r["breakout"]),
]


def run(syms: list[str], rng: str) -> tuple[list[dict], dict]:
    with ThreadPoolExecutor(8) as ex:
        data = dict(zip(syms, ex.map(lambda s: sb.daily(s, rng), syms)))
    rows: list[dict] = []
    for s, bars in data.items():
        if bars and len(bars) > WIN + 1:
            rows += name_days(s, bars)
    res = {}
    for label, f in GROUPS:
        g = [r for r in rows if f(r)]
        res[label] = group_stats(g)
    years = sorted({r["date"][:4] for r in rows})
    by_year = {}
    for y in years:
        yr = [r for r in rows if r["date"][:4] == y]
        by_year[y] = {"all": group_stats(yr)["big_up"],
                      "score 3+": group_stats([r for r in yr if r["score"] >= 3])["big_up"],
                      "SUP + HL": group_stats([r for r in yr if "SUP" in r["flags"] and "HL" in r["flags"]])["big_up"],
                      "breakout": group_stats([r for r in yr if r["breakout"]])["big_up"]}
    return rows, {"groups": res, "by_year": by_year,
                  "names": len([s for s, b in data.items() if b and len(b) > WIN + 1])}


def report(res: dict, syms: list[str], rng: str) -> str:
    base = res["groups"]["all eligible name-days"]
    L = [f"# Clue backtest ({dt.date.today().isoformat()})", "",
         f"{res['names']} of {len(syms)} candidates, {rng} of daily bars; {base['n']:,} eligible name-days on "
         f"{base['dates']:,} dates. Method and caveats: `scripts/clue_backtest.py` docstring.", "",
         "| Group | Name-days | Big up next session (≥1 ATR) | Lift | Big down (≥1 ATR) | Next close % | Open→close % after costs | 5-day % | Big up within 5 days (≥2 ATR) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for label, g in res["groups"].items():
        if not g["n"]:
            L.append(f"| {label} | 0 | | | | | | | |")
            continue
        lift = g["big_up"] / base["big_up"] if base["big_up"] else float("nan")
        L.append(f"| {label} | {g['n']:,} | {g['big_up'] * 100:.1f}% ± {1.96 * g['big_up_se'] * 100:.1f} | {lift:.2f} | "
                 f"{g['big_down'] * 100:.1f}% | {g['next']:+.2f} ± {1.96 * g['next_se']:.2f} | "
                 f"{g['oc']:+.2f} ± {1.96 * g['oc_se']:.2f} | {g['next5']:+.2f} ± {1.96 * g['next5_se']:.2f} | "
                 f"{g['big_up5'] * 100:.1f}% ± {1.96 * g['big_up5_se'] * 100:.1f} |")
    L += ["", "Big-up rate by year:", "", "| Year | All | Score 3+ | SUP + HL | Breakout watch |", "|---|---:|---:|---:|---:|"]
    for y, v in res["by_year"].items():
        L.append(f"| {y} | " + " | ".join("-" if (x is None or x != x) else f"{x * 100:.1f}%" for x in
                                       (v["all"], v["score 3+"], v["SUP + HL"], v["breakout"])) + " |")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--range", default="5y")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    _, res = run(syms, a.range)
    text = report(res, syms, a.range)
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests"
        out.mkdir(parents=True, exist_ok=True)
        stem = f"clues-{dt.date.today().isoformat()}"
        (out / f"{stem}.md").write_text(text)
        (out / f"{stem}.json").write_text(json.dumps(res, indent=1) + "\n")
        print("saved", (out / f"{stem}.md").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
