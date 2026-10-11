#!/usr/bin/env python3
"""Narrowing test (Vamsi, Oct 11: narrow the strategy to where its predictions work best, to raise the accuracy, and
report the average monthly profit rate). The replay's NARROW set (scripts/replay.py: GROUPS, shadow, allowed): each
live rule set limited to the names, or themes, whose signals worked in the shadow record (every signal of the same
rules, traded with room for all). Hindsight reads the whole record, the future included (a list picked after a
backtest); walk-forward reads only the trades closed before each session.
  signals   out of sample, every shadow signal with a full year of record before it: the names the walk-forward
            rule allowed that day against the names it excluded (does past success predict the next trade?), and
            the names' first-half against second-half averages (rank correlation)
  book      $1,000 over the last 700 hourly sessions: return, trades, win rate, drawdown, and calendar months
            (full months only): mean, median, compounded rate, months up, worst and best
  windows   the 33 separate hourly 22-session windows (all, and those with a full year of record before them) and
            every 22-session window of the 5-minute data (RUNBOOK 2d's adoption rule)
  python scripts/narrow_test.py [--save]
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import replay as rp  # noqa: E402

ROOT = rp.ROOT
RADAR, NIGHT = ("limit", "run"), ("night",)


def months(curve: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Calendar-month returns % from (day, value) pairs; a last month ending before the 25th is dropped as partial,
    and the first month only serves as the base."""
    last: dict[str, float] = {}
    end: dict[str, str] = {}
    for d, v in curve:
        last[d[:7]], end[d[:7]] = v, d
    ms = sorted(last)
    out = [(b, (last[b] / last[a] - 1) * 100) for a, b in zip(ms, ms[1:])]
    if out and int(end[ms[-1]][8:]) < 25:
        out = out[:-1]
    return out


def mstats(ms: list[tuple[str, float]]) -> dict:
    v = [x for _, x in ms]
    g = 1.0
    for x in v:
        g *= 1 + x / 100
    return {"n": len(v), "mean": round(st.mean(v), 2), "median": round(st.median(v), 2),
            "compound": round((g ** (1 / len(v)) - 1) * 100, 2), "up": sum(x > 0 for x in v),
            "worst": round(min(v), 1), "best": round(max(v), 1),
            "years": {y: round((st.mean(x for m, x in ms if m.startswith(y))), 2) for y in sorted({m[:4] for m, _ in ms})}}


def bench_curve(data: dict, sym: str, first: str, last: str) -> list[tuple[str, float]]:
    rows = [(rp.et_day(r["t"]), r["c"]) for r in data["daily"][sym]]
    prior = [x for x in rows if x[0] < first][-1:]
    return prior + [x for x in rows if first <= x[0] <= last]


def signals(data: dict, title: str, o: dict, kinds: tuple) -> dict:
    """Out-of-sample check of the walk-forward rule at the signal level, and first-half/second-half persistence."""
    tr = [t for t in rp.shadow(data, o) if t["kind"] in kinds]
    if not tr:
        return {}
    days = sorted(data["1h"]["SPY"])
    full = days[min(len(days) - 1, 252)]
    inn, out = [], []
    for t in tr:
        if t["day"] < full:
            continue
        (inn if t["ticker"] in rp.allowed(data, o, t["day"], kinds) else out).append(t)

    def mean_ci(g):
        if len(g) < 5:
            return None
        m, se = cb.clustered([(t["day"], t["ret_pct"]) for t in g])
        return {"n": len(g), "mean": round(m, 2), "ci": round(1.96 * se, 2), "won": round(100 * sum(t["ret_pct"] > 0 for t in g) / len(g), 1)}

    ex = sorted(t["exit_day"] for t in tr)
    split = ex[len(ex) // 2]
    h: dict[str, tuple[list, list]] = {}
    for t in tr:
        h.setdefault(t["ticker"], ([], []))[0 if t["exit_day"] < split else 1].append(t["ret_pct"])
    pairs = [(st.mean(a), st.mean(b)) for a, b in h.values() if len(a) >= 3 and len(b) >= 3]

    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for k, i in enumerate(order):
            r[i] = k
        return r
    rho = None
    if len(pairs) >= 5:
        ra, rb = ranks([a for a, _ in pairs]), ranks([b for _, b in pairs])
        rho = round(st.correlation(ra, rb), 2)
    srt = sorted(pairs, key=lambda p: -p[0])
    third = max(1, len(srt) // 3)
    return {"title": title, "allowed": mean_ci(inn), "excluded": mean_ci(out), "all": mean_ci(inn + out),
            "split": split, "names": len(pairs), "rho": rho,
            "top_third_h2": round(st.mean(b for _, b in srt[:third]), 2) if pairs else None,
            "bottom_third_h2": round(st.mean(b for _, b in srt[-third:]), 2) if pairs else None}


def windows(data: dict, o: dict, ends: list[str], res: str) -> list[tuple[str, float]]:
    return [(e, rp.summarize(rp.replay(data, 22, o, 1000.0, e, res))["ret_pct"]) for e in ends]


def wstats(rets: list[tuple[str, float]], spy: dict | None = None) -> dict:
    v = sorted(x for _, x in rets)
    out = {"n": len(v), "median": round(st.median(v), 1), "mean": round(st.mean(v), 1), "worst": round(v[0], 1),
           "best": round(v[-1], 1), "doubled": sum(x >= 100 for x in v)}
    if spy:
        out["beat"] = sum(1 for e, x in rets if x > spy.get(e, 0))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    data = rp.load_data(rp.lv.CANDIDATES, False)
    res_days = sorted(data["1h"]["SPY"])
    now = rp.pfm.now_utc()
    today = rp.pfm.et_date(now).isoformat()
    res_days = [d for d in res_days if d < today or now.astimezone(rp.pfm.ET).hour >= 16]
    ends_h = res_days[21:][::-1][::22][::-1]
    full_from = res_days[min(len(res_days) - 1, 252 + 21)]
    d5 = sorted(d for d in data["5m"]["SPY"] if d < today or now.astimezone(rp.pfm.ET).hour >= 16)
    ends_5 = d5[21:]
    spy_h = {e: rp.replay(data, 22, rp.DEFAULTS, 1000.0, e, "1h")["bench"].get("SPY", 0) for e in ends_h}
    out = {"asof": today, "variants": [], "signals": []}
    for title, ov in rp.NARROW:
        o = {**rp.DEFAULTS, **ov}
        res = rp.replay(data, 700, o, 1000.0, None, "1h")
        s = rp.summarize(res)
        ms = months([(e["day"], e["equity"]) for e in res["equity"]])
        wh = windows(data, o, ends_h, "1h")
        w5 = windows(data, o, ends_5, "5m")
        v = {"title": title, "options": {k: x for k, x in o.items() if rp.DEFAULTS.get(k) != x}, "summary": s,
             "sessions": res["sessions"], "bench": res["bench"], "months": mstats(ms), "monthly": ms,
             "windows_1h": wstats(wh, spy_h), "windows_1h_full": wstats([x for x in wh if x[0] >= full_from], spy_h),
             "windows_5m": wstats(w5), "returns_1h": wh, "returns_5m": w5}
        out["variants"].append(v)
        print(f"{title[:72]:72s} {s['ret_pct']:+8.2f}%  month {v['months']['mean']:+.2f}% (compound "
              f"{v['months']['compound']:+.2f}%)  1h mean {v['windows_1h']['mean']:+.1f} worst {v['windows_1h']['worst']:+.1f}  "
              f"5m mean {v['windows_5m']['mean']:+.1f} worst {v['windows_5m']['worst']:+.1f}", flush=True)
        if o["narrow"] == "wf":
            for kinds, nm in ((RADAR, "radar"), (NIGHT, "night")):
                sg = signals(data, f"{title} ({nm} signals)", o, kinds)
                if sg:
                    out["signals"].append(sg)
    v0 = out["variants"][0]
    first, last = v0["sessions"][0], v0["sessions"][1]
    out["bench_months"] = {s: mstats(months(bench_curve(data, s, first, last))) for s in ("SPY", "QQQ")}
    out["spy_windows"] = wstats([(e, x) for e, x in spy_h.items()])
    text = report(out, first, last, full_from, ends_5)
    print(text)
    if a.save:
        stem = ROOT / "research" / "replay" / f"narrow-{last}"
        stem.with_suffix(".json").write_text(json.dumps(out, indent=1) + "\n")
        stem.with_suffix(".md").write_text(text)
        print("saved", stem.with_suffix(".md").relative_to(ROOT))
    return 0


def report(out: dict, first: str, last: str, full_from: str, ends_5: list[str]) -> str:
    bm = out["bench_months"]
    L = [f"# Narrowing the rules to where they worked, {out['asof']}", "",
         f"Method: `scripts/narrow_test.py` docstring. $1,000; hourly replay {first} to {last}; months are calendar "
         f"months (full ones). Holding the S&P 500: a month {bm['SPY']['mean']:+.2f}% on average (compounded "
         f"{bm['SPY']['compound']:+.2f}%), up in {bm['SPY']['up']} of {bm['SPY']['n']}; the Nasdaq-100 "
         f"{bm['QQQ']['mean']:+.2f}% ({bm['QQQ']['compound']:+.2f}%), up in {bm['QQQ']['up']}.", "",
         "## Does past success pick the next winners? (signals, out of sample)", "",
         "Every shadow signal with a year of record before it, split by whether the walk-forward rule allowed its name "
         "that day. Average trade % ± 95% (clustered by entry date); rank correlation of the names' first-half and "
         "second-half averages (names with 3+ trades in each).", "",
         "| Rule | Allowed names: trades, average, won | Excluded names | Rank correlation, halves | 2nd half: top third of 1st / bottom third |",
         "|---|---|---|---|---|"]

    def f(x):
        return f"{x['n']}, {x['mean']:+.2f}% ± {x['ci']:.2f}, {x['won']}%" if x else "-"
    for sg in out["signals"]:
        rho = f"{sg['rho']} ({sg['names']} names)" if sg["rho"] is not None else "-"
        thirds = (f"{sg['top_third_h2']:+.2f}% / {sg['bottom_third_h2']:+.2f}%" if sg["top_third_h2"] is not None
                  else "-")
        L.append(f"| {sg['title']} | {f(sg['allowed'])} | {f(sg['excluded'])} | {rho} | {thirds} |")
    L += ["", "## The book over 700 sessions, by month", "",
          "| Rules | Return | Trades | Won | Average trade | Worst drawdown | Average month | Median month | "
          "Compounded a month | Months up | Worst month | Best month |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for v in out["variants"]:
        s, m = v["summary"], v["months"]
        L.append(f"| {v['title']} | {s['ret_pct']:+.1f}% | {s['trades']} | {s['win_rate']}% | {s['avg_trade']:+.2f}% | "
                 f"{s['max_drawdown_pct']:.1f}% | {m['mean']:+.2f}% | {m['median']:+.2f}% | {m['compound']:+.2f}% | "
                 f"{m['up']}/{m['n']} | {m['worst']:+.1f}% | {m['best']:+.1f}% |")
    L += ["", "Average month by year:", "", "| Rules | " + " | ".join(sorted(bm["SPY"]["years"])) + " |",
          "|---|" + "---:|" * len(bm["SPY"]["years"])]
    for name, m in [("S&P 500", bm["SPY"]), ("Nasdaq-100", bm["QQQ"])] + [(v["title"], v["months"]) for v in out["variants"]]:
        L.append(f"| {name} | " + " | ".join(f"{m['years'].get(y, 0):+.2f}%" for y in sorted(bm["SPY"]["years"])) + " |")
    sw = out["spy_windows"]
    L += ["", "## 22-session windows (RUNBOOK 2d)", "",
          f"Hourly: the 33 separate windows, and the {out['variants'][0]['windows_1h_full']['n']} ending from {full_from} "
          f"(a full year of record before them). 5-minute: every 22-session window ending {ends_5[0]} to {ends_5[-1]} "
          f"(overlapping). S&P 500 over the hourly windows: median {sw['median']:+.1f}%, mean {sw['mean']:+.1f}%.", "",
          "| Rules | Hourly mean | Hourly worst | Hourly median | Beat the S&P | Doubled | With a year of record: mean | worst | "
          "5-minute mean | 5-minute worst |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for v in out["variants"]:
        h, hf, w5 = v["windows_1h"], v["windows_1h_full"], v["windows_5m"]
        L.append(f"| {v['title']} | {h['mean']:+.1f}% | {h['worst']:+.1f}% | {h['median']:+.1f}% | {h['beat']}/{h['n']} | "
                 f"{h['doubled']}/{h['n']} | {hf['mean']:+.1f}% | {hf['worst']:+.1f}% | {w5['mean']:+.1f}% | {w5['worst']:+.1f}% |")
    L += ["", "## Reading", ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
