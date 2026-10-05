#!/usr/bin/env python3
"""Clue scan: what a watched name showed before it moved (Vamsi, Mon Oct 5: when a name on the watchlist makes a
big move, check whether it left clues beforehand and why the routines missed them, then watch for those clues).

  python scripts/clues.py scan [--min-score 3] [--save]   morning (8:40 run): names whose last close shows clues
  python scripts/clues.py movers [--min-atr 1.0]          any run: names moving at least 1 ATR today, with the
                                                          clues they showed at the last close
  python scripts/clues.py postmortem [--save] [--journal] post-close: today's big movers, their clues at the
                                                          prior close and why the routines missed them

Universe: the radar (config/radar.json) plus the candidates in scripts/levels.py.
Clues, from daily bars through the last completed session before the one being judged (no look-ahead):
  SUP   within 0.5 ATR above a support tested at least twice (a zone at the price counts if two swings are lows)
  COIL  the last 5 sessions' average range at most 75% of the 14-day ATR, or the last session the narrowest of 7
  ACC   up-day volume at least 1.5x down-day volume over the last 10 sessions
  HL    higher lows: the last 5 sessions' low above the 5 before
  RES   within 0.5 ATR under a resistance tested at least twice (breakout watch; the radar does not buy these)
  GAP   (scan, movers) today's pre-market or opening move is at least 0.5 ATR
Bounce score = SUP + COIL + ACC + HL. The scan lists bounce scores of 3+ and RES + COIL breakout watches.
These describe past prices. Whether any of them comes before big moves more often than chance is tested in
research/backtests/clues-*.md; until a clue passes that test it is an alert for Vamsi, not a trade rule.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
OUT = ROOT / "research" / "clues"
SUP_ATR = 0.5
RES_ATR = 0.5
COIL_MAX = 0.75
ACC_MIN = 1.5
GAP_ATR = 0.5


def radar_in_force() -> dict:
    """The radar the routines traded on today: the newest build from closes before today's session (the 16:20
    rebuild writes tomorrow's radar, so a post-mortem after it must read the one before)."""
    today = today_et()
    best = None
    for p in (ROOT / "research" / "radar").glob("*.json"):
        try:
            d = json.loads(p.read_text())
        except Exception:  # noqa: BLE001
            continue
        if (d.get("asof") or "9999") < today and (best is None or d.get("generated_at", "") > best.get("generated_at", "")):
            best = d
    if best is None and lv.RADAR.exists():
        best = json.loads(lv.RADAR.read_text())
    return best or {}


def universe() -> list[tuple[str, bool]]:
    names = [x["ticker"] for x in radar_in_force().get("names", [])]
    out = [(s, True) for s in names]
    out += [(s, False) for s in lv.CANDIDATES if s not in names]
    return out


def radar_map() -> dict:
    return {x["ticker"]: x for x in radar_in_force().get("names", [])}


def held() -> set[str]:
    p = ROOT / ".cache" / "portfolio_guided.json"
    try:
        return {x.get("ticker") or x.get("symbol") for x in json.loads(p.read_text()).get("positions", [])}
    except Exception:  # noqa: BLE001
        return set()


def today_et() -> str:
    return pfm.et_date(pfm.now_utc()).isoformat()


def bar_date(r: dict) -> str:
    return pfm.et_date(dt.datetime.fromtimestamp(r["t"], dt.timezone.utc)).isoformat()


def features(rows: list[dict]) -> dict | None:
    """Clue flags on completed sessions only (the caller drops the session being judged)."""
    if len(rows) < 60:
        return None
    px = rows[-1]["c"]
    a = lv.atr(rows)
    if not a or not px:
        return None
    win = rows[-lv.LOOKBACK:]
    lows, highs = lv.pivots(win)
    zs = [z for z in lv.zones(lows + highs, max(0.5 * a, 0.015 * px), len(win)) if z["strength"] >= 2]
    def n_lows(z: dict) -> int:
        return sum(1 for _, p in lows if z["lo"] <= p <= z["hi"])
    sup = max((z for z in zs if z["level"] < px - 0.1 * a or (z["level"] <= px + 0.1 * a and n_lows(z) >= 2)),
              key=lambda z: z["level"], default=None)
    res = min((z for z in zs if z["level"] > px + 0.1 * a), key=lambda z: z["level"], default=None)
    rng = [r["h"] - r["l"] for r in rows]
    coil = sum(rng[-5:]) / 5 / a
    nr7 = rng[-1] == min(rng[-7:])
    up = sum(rows[i]["v"] for i in range(-10, 0) if rows[i]["c"] > rows[i - 1]["c"])
    dn = sum(rows[i]["v"] for i in range(-10, 0) if rows[i]["c"] < rows[i - 1]["c"])
    udv = up / dn if dn else (9.99 if up else 1.0)
    hl = min(r["l"] for r in rows[-5:]) > min(r["l"] for r in rows[-10:-5])
    sup_d = (px - sup["level"]) / a if sup else None
    res_d = (res["level"] - px) / a if res else None
    flags = {
        "SUP": sup_d is not None and sup_d <= SUP_ATR,
        "COIL": coil <= COIL_MAX or nr7,
        "ACC": udv >= ACC_MIN,
        "HL": hl,
        "RES": res_d is not None and res_d <= RES_ATR,
    }
    return {
        "close": round(px, 4), "asof": bar_date(rows[-1]), "atr": round(a, 4), "atr_pct": round(a / px * 100, 2),
        "sup": round(sup["level"], 4) if sup else None, "sup_n": sup["strength"] if sup else 0,
        "sup_atr": round(sup_d, 2) if sup_d is not None else None,
        "res": round(res["level"], 4) if res else None, "res_n": res["strength"] if res else 0,
        "res_atr": round(res_d, 2) if res_d is not None else None,
        "coil": round(coil, 2), "nr7": nr7, "udv": round(udv, 2), "hl": hl,
        "flags": [k for k, v in flags.items() if v],
        "score": sum(flags[k] for k in ("SUP", "COIL", "ACC", "HL")),
        "breakout": flags["RES"] and flags["COIL"],
    }


def load(sym_onradar: tuple[str, bool]) -> dict | None:
    sym, on_radar = sym_onradar
    b = lv.bars(sym)
    if not b or not b["rows"]:
        return None
    rows = b["rows"]
    today = today_et()
    today_bar = rows[-1] if bar_date(rows[-1]) == today else None
    prior = rows[:-1] if today_bar else rows
    f = features(prior)
    if not f:
        return None
    try:
        q = md.quote(sym)
    except Exception:  # noqa: BLE001
        q = {}
    prev = q.get("prev_close") or f["close"]
    last = q.get("price")
    pre = q.get("ext_price") if pfm.market_session(pfm.now_utc()) == "pre" else None
    out = {"ticker": sym, "radar": on_radar, "crypto": sym in lv.CRYPTO_LINKED, **f, "prev_close": prev,
           "last": last, "day_low": q.get("day_low"), "day_high": q.get("day_high"), "volume": q.get("volume")}
    if today_bar and last:
        out["chg_pct"] = round((last / prev - 1) * 100, 2)
        out["move_atr"] = round(out["chg_pct"] / f["atr_pct"], 2)
        out["gap_pct"] = round((today_bar["o"] / prev - 1) * 100, 2) if today_bar.get("o") else None
        out["vol_pace"] = round((q.get("volume") or today_bar["v"]) / (sum(r["v"] for r in prior[-20:]) / 20 or 1), 2)
    if pre:
        out["pre_pct"] = round((pre / prev - 1) * 100, 2)
    move = out.get("pre_pct") if pre else out.get("gap_pct")
    out["gap"] = move is not None and abs(move) >= GAP_ATR * f["atr_pct"]
    out["prior_rows"] = prior
    return out


def collect() -> list[dict]:
    with ThreadPoolExecutor(12) as ex:
        return [r for r in ex.map(load, universe()) if r]


def miss_reason(r: dict, rmap: dict, holdings: set[str]) -> str:
    sym = r["ticker"]
    if sym in holdings:
        return "held"
    if r["radar"] and sym in rmap:
        z = rmap[sym]
        top, stop = z["buy_zone"][1], z["stop"]
        lo = r.get("day_low")
        if r.get("chg_pct", 0) < 0:
            return "on the radar; a down move" + (" through the stop" if lo is not None and lo <= stop else "")
        if lo is not None and lo > top:
            return f"on the radar; low {lo:.4g} stayed above the buy zone top {top:.4g}, so no entry"
        return "on the radar and reached the buy zone; not bought (no free slot or settled cash)"
    a = lv.analyse({"sym": sym, "rows": r["prior_rows"], "name": sym, "exchange": "", "type": ""})
    why = []
    if a:
        if a["atr_pct"] < lv.MIN_ATR_PCT:
            why.append(f"daily range {a['atr_pct']}% < {lv.MIN_ATR_PCT}%")
        if a["dollar_vol_20d"] < lv.MIN_DOLLAR_VOL:
            why.append(f"${a['dollar_vol_20d'] / 1e6:.0f}M a day < $15M")
        if a["support_strength"] < 2:
            why.append("no tested support")
        if (a["reward_risk"] or 0) < 1.5:
            why.append(f"R:R {a['reward_risk']} < 1.5")
    return "candidate, not on the radar: " + ("; ".join(why) if why else "passes the filters now (joins at the next build)")


def fmt_line(r: dict) -> str:
    bits = [f"{r['ticker']:6}", f"{(r.get('last') or r['close']):>9.4g}"]
    if r.get("chg_pct") is not None:
        bits.append(f"today {r['chg_pct']:+.1f}% ({r['move_atr']:+.1f} ATR)")
    if r.get("pre_pct") is not None:
        bits.append(f"pre-mkt {r['pre_pct']:+.1f}%")
    bits.append(f"score {r['score']} [{' '.join(r['flags']) or '-'}]")
    if r["sup"] is not None:
        bits.append(f"sup {r['sup']:.4g} x{r['sup_n']} ({r['sup_atr']:+.1f} ATR)")
    if r["res"] is not None:
        bits.append(f"res {r['res']:.4g} x{r['res_n']} ({r['res_atr']:+.1f} ATR)")
    bits.append(f"coil {r['coil']:.2f} upvol/dnvol {r['udv']:.2f}")
    bits.append("radar" if r["radar"] else "candidate")
    if r["crypto"]:
        bits.append("crypto")
    return "  " + " | ".join(bits)


def strip(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "prior_rows"}


def save(kind: str, rows: list[dict], extra: dict | None = None) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{today_et()}-{kind}.json"
    p.write_text(json.dumps({"generated_at": pfm.iso(pfm.now_utc()), "kind": kind, **(extra or {}),
                             "names": [strip(r) for r in rows]}, indent=1) + "\n")
    return p


def cmd_scan(a) -> int:
    rows = collect()
    asof = max((r["asof"] for r in rows), default="?")
    bounce = sorted([r for r in rows if r["score"] >= a.min_score], key=lambda r: (-r["score"], r["sup_atr"] or 9))
    brk = sorted([r for r in rows if r["breakout"] and r not in bounce], key=lambda r: r["res_atr"])
    gaps = sorted([r for r in rows if r.get("gap") and r.get("pre_pct") is not None], key=lambda r: -abs(r["pre_pct"]))
    print(f"clue scan {pfm.iso(pfm.now_utc())} (closes of {asof}): {len(rows)} names")
    print(f"BOUNCE SETUPS (score {a.min_score}+ of SUP COIL ACC HL): {len(bounce)}")
    for r in bounce:
        print(fmt_line(r))
    print(f"BREAKOUT WATCH (RES + COIL; alert only): {len(brk)}")
    for r in brk:
        print(fmt_line(r))
    if gaps:
        print(f"PRE-MARKET MOVES (>= {GAP_ATR} ATR): {len(gaps)}")
        for r in gaps:
            print(fmt_line(r))
    if a.save:
        print("saved", save("scan", bounce + brk + [g for g in gaps if g not in bounce and g not in brk]).relative_to(ROOT))
    return 0


def big_movers(rows: list[dict], min_atr: float) -> list[dict]:
    return sorted([r for r in rows if r.get("move_atr") is not None and abs(r["move_atr"]) >= min_atr],
                  key=lambda r: -abs(r["move_atr"]))


def cmd_movers(a) -> int:
    rows = collect()
    mv = big_movers(rows, a.min_atr)
    rmap, hold = radar_map(), held()
    print(f"movers {pfm.iso(pfm.now_utc())}: {len(mv)} of {len(rows)} names moved {a.min_atr}+ ATR today")
    for r in mv:
        print(fmt_line(r))
        print(f"      why: {miss_reason(r, rmap, hold)}")
    return 0


def cmd_postmortem(a) -> int:
    rows = collect()
    mv = big_movers(rows, a.min_atr)
    rmap, hold = radar_map(), held()
    ups = [r for r in mv if r["chg_pct"] > 0]
    downs = [r for r in mv if r["chg_pct"] <= 0]
    with_clues = [r for r in rows if r["score"] >= 2 or r["breakout"]]
    hit = [r for r in with_clues if (r.get("move_atr") or 0) >= a.min_atr]
    base = [r for r in rows if r not in with_clues]
    base_hit = [r for r in base if (r.get("move_atr") or 0) >= a.min_atr]
    lines = []
    for r in ups:
        r["why"] = miss_reason(r, rmap, hold)
        lines.append(f"{r['ticker']} {r['chg_pct']:+.1f}% ({r['move_atr']:.1f} ATR): clues at the prior close "
                     f"{' '.join(r['flags']) or 'none'} (score {r['score']}); {r['why']}.")
    for r in downs:
        r["why"] = miss_reason(r, rmap, hold)
    summary = (f"{len(hit)} of {len(with_clues)} names with 2+ clues (or a breakout watch) moved up {a.min_atr}+ ATR; "
               f"{len(base_hit)} of {len(base)} without did.")
    print(f"post-mortem {today_et()}: {len(ups)} up and {len(downs)} down movers of {a.min_atr}+ ATR among {len(rows)} names")
    for r in ups + downs:
        print(fmt_line(r))
        print(f"      why: {r['why']}")
    print(summary)
    if a.save:
        print("saved", save("postmortem", ups + downs, {"summary": summary}).relative_to(ROOT))
    if a.journal and (ups or downs):
        body = "\n".join(
            ["Big moves today (at least one daily range, ATR) among the radar and its candidates, with the clues each "
             "showed at the prior close and why the routines did not catch it (clues.py postmortem; method in the "
             "script docstring)."]
            + lines
            + ([("Down: " + ", ".join(f"{r['ticker']} {r['chg_pct']:+.1f}%" + (" (held)" if r["ticker"] in hold else "")
                                      for r in downs) + ".")] if downs else [])
            + [f"Base rate today: {summary} One session is an anecdote; the 5-year clue backtest decides which clues count."])
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "journal.py"), "--kind", "research", "--title",
                        f"Mover post-mortem {today_et()}: " + (", ".join(f"{r['ticker']} {r['chg_pct']:+.0f}%" for r in ups[:5]) or "no big up-moves"),
                        "--body", body, "--tickers", ",".join(r["ticker"] for r in (ups + downs)[:12])], check=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("scan")
    s.add_argument("--min-score", type=int, default=3)
    s.add_argument("--save", action="store_true")
    m = sp.add_parser("movers")
    m.add_argument("--min-atr", type=float, default=1.0)
    p = sp.add_parser("postmortem")
    p.add_argument("--min-atr", type=float, default=1.0)
    p.add_argument("--save", action="store_true")
    p.add_argument("--journal", action="store_true")
    a = ap.parse_args()
    return {"scan": cmd_scan, "movers": cmd_movers, "postmortem": cmd_postmortem}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
