#!/usr/bin/env python3
"""Build one dashboard snapshot document (for the artifact's `snapshots`
collection) from the ledger, journal and the latest synced market data.

  python scripts/snapshot.py [--note "..."]
Prints the doc id and writes .cache/snapshot.json.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache"
MAX_POINTS = 700


def load_equity(cfg: dict, cache: Path) -> list[dict]:
    path = cache / "equity.jsonl"
    pts = []
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                pts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    start = cfg["accepted_utc"]
    pts = [p for p in pts if p["t"] >= start]
    pts.sort(key=lambda p: p["t"])
    return pts


def next_update(now: dt.datetime, sched: dict) -> str | None:
    """Next scheduled routine time (ET clock times on business days)."""
    times = sorted(sched.get("routine_times_et", []))
    d = pfm.et_date(now)
    for _ in range(8):
        if pfm.is_business_day(d):
            for hm in times:
                h, m = map(int, hm.split(":"))
                t = dt.datetime(d.year, d.month, d.day, h, m, tzinfo=pfm.ET)
                if t > now:
                    return pfm.iso(t)
        d += dt.timedelta(days=1)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--note", default="")
    ap.add_argument("--cache", default=str(CACHE), help="dir holding quotes.json and equity.jsonl")
    ap.add_argument("--out", default="", help="output path (default <cache>/snapshot.json)")
    a = ap.parse_args()
    cache = Path(a.cache)

    cfg = pfm.load_config()
    ledger = pfm.load_ledger()
    qdoc = json.loads((cache / "quotes.json").read_text()) if (cache / "quotes.json").exists() else {"quotes": {}}
    quotes = qdoc.get("quotes", {})
    now = pfm.now_utc()
    pf = pfm.Portfolio(ledger, cfg)
    val = pf.valuation(quotes, now)

    # Latest plan/thesis per open position comes from its most recent BUY.
    last_buy = {}
    for t in pf.txns:
        if t["type"] == "BUY":
            last_buy[t["ticker"]] = t
    for p in val["positions"]:
        b = last_buy.get(p["ticker"], {})
        p["name"] = b.get("name")
        p["thesis"] = b.get("rationale")
        p["stop"] = (b.get("plan") or {}).get("stop")
        p["target"] = (b.get("plan") or {}).get("target")

    trades = []
    for t in pf.txns:
        if t["type"] not in ("BUY", "SELL"):
            continue
        row = {k: t.get(k) for k in ("id", "type", "ts", "ticker", "name", "qty", "price",
                                     "quote_price", "quote_time", "slippage_bps", "gross",
                                     "fees", "net_cash", "settle_date", "rationale", "tags",
                                     "plan", "compliance")}
        row.update(pf.sell_results.get(t["id"], {}))
        trades.append(row)
    trades.reverse()

    pts = load_equity(cfg, cache)
    base = cfg.get("benchmark_base", {})
    series = {"t": [cfg["accepted_utc"]], "equity": [cfg["start_capital"]]}
    for b in cfg["benchmarks"]:
        series[b] = [0.0]
    if len(pts) > MAX_POINTS:
        step = len(pts) / MAX_POINTS
        pts = [pts[int(i * step)] for i in range(MAX_POINTS - 1)] + [pts[-1]]
    for p in pts:
        series["t"].append(p["t"])
        series["equity"].append(p["equity"])
        for b in cfg["benchmarks"]:
            px = p.get(b)
            series[b].append(round((px / base[b] - 1) * 100, 3) if px and base.get(b) else None)
    # Live point from this snapshot's quotes.
    series["t"].append(val["as_of"])
    series["equity"].append(val["equity"])
    bench = {}
    for b in cfg["benchmarks"]:
        px = (quotes.get(b) or {}).get("price")
        r = round((px / base[b] - 1) * 100, 3) if px and base.get(b) else None
        series[b].append(r)
        bench[b] = {"base": base.get(b), "last": px, "ret_pct": r}

    jpath = ROOT / "ledger" / "journal.json"
    journal = json.loads(jpath.read_text())["entries"] if jpath.exists() else []
    journal = sorted(journal, key=lambda e: e["ts"], reverse=True)[:40]

    wl_path = ROOT / "config" / "watchlist.json"
    watch = json.loads(wl_path.read_text()) if wl_path.exists() else {}
    radar = []
    for tk in watch.get("focus", []):
        qq = quotes.get(tk) or {}
        if qq.get("price"):
            radar.append({"ticker": tk, "name": qq.get("name"), "price": qq["price"],
                          "change_pct": qq.get("change_pct"),
                          "ext_change_pct": qq.get("ext_change_pct")})

    sched_path = ROOT / "config" / "schedule.json"
    sched = json.loads(sched_path.read_text()) if sched_path.exists() else {}
    rules = cfg["rules"]
    c = val["counts"]
    compliance = {
        "checks": [
            {"id": "cash", "label": "Cash account only (no margin, no shorting)", "ok": True,
             "detail": "Balance under the $2,000 FINRA margin minimum, so margin isn't available anyway."},
            {"id": "instruments", "label": "Stocks and ETFs only", "ok": True,
             "detail": "No options or other derivatives."},
            {"id": "gfv", "label": "No good-faith violations (T+1 settlement)", "ok": c["gfv"] == 0,
             "detail": f"{c['gfv']} violations. Shares bought with unsettled sale proceeds are not sold before those proceeds settle."},
            {"id": "daytrades", "label": f"Day trades ≤ {rules['max_day_trades_rolling_5d']} per rolling 5 days",
             "ok": c["day_trades_5d"] <= rules["max_day_trades_rolling_5d"],
             "detail": f"{c['day_trades_5d']} in the window. Keeps activity clearly passive investing, not a trading business."},
            {"id": "orders", "label": f"Order count ≤ {rules['max_orders_per_day']}/day and ≤ {rules['max_orders_total']} total",
             "ok": c["orders_today"] <= rules["max_orders_per_day"] and c["orders_total"] <= rules["max_orders_total"],
             "detail": f"{c['orders_today']} today, {c['orders_total']} total."},
            {"id": "ofac", "label": "No OFAC-restricted (NS-CMIC) securities", "ok": True,
             "detail": "Rule for anyone physically in the US, H-1B holders included."},
        ],
        "wash_sale_flags": c["wash_sale_flags"],
    }

    doc_id = now.strftime("%Y%m%dT%H%M%SZ")
    snap = {
        "id": doc_id,
        "as_of": val["as_of"],
        "quotes_generated_at": qdoc.get("generated_at"),
        "session": val["session"],
        "challenge": {
            "name": cfg["name"], "start_capital": cfg["start_capital"],
            "accepted_utc": cfg["accepted_utc"], "trading_start_utc": cfg["trading_start_utc"],
            "end_utc": cfg["end_utc"], "goal_equity": val["goal_equity"],
            "account": cfg["account"],
        },
        "summary": {k: v for k, v in val.items() if k not in ("positions",)},
        "positions": val["positions"],
        "trades": trades,
        "equity": series,
        "benchmarks": bench,
        "journal": journal,
        "compliance": compliance,
        "radar": radar,
        "strategy": watch.get("strategy", ""),
        "schedule": {"next_update": next_update(now, sched), "cadence": sched.get("cadence", "")},
        "note": a.note,
    }
    out = Path(a.out) if a.out else cache / "snapshot.json"
    out.write_text(json.dumps(snap, separators=(",", ":")))
    size = out.stat().st_size
    print(f"doc_id={doc_id} bytes={size} equity={val['equity']} net={val['net_profit']} "
          f"ret={val['return_pct']}% positions={len(val['positions'])} trades={len(trades)} "
          f"points={len(series['t'])}")
    if size > 250_000:
        print("WARN: snapshot exceeds 250 KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
