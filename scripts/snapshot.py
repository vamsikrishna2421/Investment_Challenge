#!/usr/bin/env python3
"""Build one dashboard snapshot document for a book (artifact collection
`snapshots` for h1b, `snapshots_free` for free) from the ledger, journal and
the latest synced market data.

  python scripts/snapshot.py [--book free] [--note "..."]
Prints the doc id and writes .cache/snapshot.json (.cache/snapshot_free.json).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache"
MAX_POINTS = 700


def load_equity(cfg: dict, cache: Path, book: str) -> list[dict]:
    path = cache / pfm.BOOKS[book]["equity"]
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
    ap.add_argument("--out", default="", help="output path (default <cache>/snapshot[_free].json)")
    ap.add_argument("--book", default=None, help="h1b (default), free or guided")
    a = ap.parse_args()
    cache = Path(a.cache)
    book = pfm.current_book(a.book)

    cfg = pfm.load_config(book)
    ledger = pfm.load_ledger(book)
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
        if t["type"] not in ("BUY", "SELL", "EXPIRE"):
            continue
        row = {k: t.get(k) for k in ("id", "type", "ts", "ticker", "name", "qty", "price",
                                     "quote_price", "quote_time", "slippage_bps", "gross",
                                     "fees", "net_cash", "settle_date", "rationale", "tags",
                                     "plan", "compliance", "option", "quote_detail")}
        row["label"] = pfm.display_label(t["ticker"])
        row["asset"] = pfm.asset_class(t["ticker"])
        row["multiplier"] = pfm.multiplier(t["ticker"])
        row.update(pf.sell_results.get(t["id"], {}))
        trades.append(row)
    trades.reverse()

    pts = load_equity(cfg, cache, book)
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

    jpath = pfm.book_path("journal", book)
    journal = json.loads(jpath.read_text())["entries"] if jpath.exists() else []
    journal = sorted(journal, key=lambda e: (e["ts"], e["id"]), reverse=True)[:40]

    wl_path = pfm.book_path("watchlist", book)
    watch = json.loads(wl_path.read_text()) if wl_path.exists() else {}
    radar = []
    for tk in watch.get("focus", []):
        qq = quotes.get(tk) or {}
        if qq.get("price"):
            radar.append({"ticker": tk, "label": pfm.display_label(tk), "name": qq.get("name"), "price": qq["price"],
                          "change_pct": qq.get("change_pct"),
                          "ext_change_pct": qq.get("ext_change_pct")})

    # Support/resistance radar (config/radar.json, shared by every book) against the latest quotes.
    levels = None
    if lv.RADAR.exists():
        rd = json.loads(lv.RADAR.read_text())
        held_tk = {p["ticker"] for p in val["positions"]}
        rows = []
        for r in rd["names"]:
            c = lv.classify(r, quotes.get(r["ticker"]), rd["asof"])
            rows.append({"ticker": r["ticker"], "name": r["name"], "price": c.get("price"), "status": c["status"],
                         "to_zone_pct": c.get("to_zone_pct"), "rr_now": c.get("rr_now"),
                         "buy_zone": r["buy_zone"], "stop": r["stop"], "sell_zone": r["sell_zone"],
                         "reward_risk": r["reward_risk"], "upside_pct": r["upside_to_target_pct"],
                         "atr_pct": r["atr_pct"], "note": r.get("note") or "", "held": r["ticker"] in held_tk})
        rows.sort(key=lambda x: (lv.STATUS_ORDER.index(x["status"]), x.get("to_zone_pct") or 0))
        levels = {"generated_at": rd["generated_at"], "asof": rd["asof"], "names": rows}

    sched_path = ROOT / "config" / "schedule.json"
    sched = json.loads(sched_path.read_text()) if sched_path.exists() else {}
    rules = cfg["rules"]
    c = val["counts"]
    checks_h1b = {
        "checks": [
            {"id": "cash", "label": "Cash account only (no margin, no shorting)", "ok": True,
             "detail": "Balance under the $2,000 FINRA margin minimum, so margin isn't available anyway."},
            {"id": "instruments", "label": "Stocks and ETFs only", "ok": True,
             "detail": "Includes leveraged and inverse ETFs. No options or other derivatives."},
            {"id": "gfv", "label": "No good-faith violations (T+1 settlement)", "ok": c["gfv"] == 0,
             "detail": f"{c['gfv']} violations. Shares bought with unsettled sale proceeds are not sold before those proceeds settle."},
            {"id": "personal", "label": "Personal account, investor tax treatment", "ok": True,
             "detail": "No trading for others, no pay, no trader-tax-status (IRC 475) election. Those, not trade count, are what would turn trading into unauthorized self-employment on H-1B."},
            {"id": "activity", "label": "Activity tracked in the open", "ok": True,
             "detail": f"{c['orders_total']} orders so far ({c['orders_today']} today), {c['day_trades_total']} day trades. No legal cap applies to trading your own account."},
            {"id": "ofac", "label": "No OFAC-restricted (NS-CMIC) securities", "ok": True,
             "detail": "Rule for anyone physically in the US, H-1B holders included."},
        ],
        "wash_sale_flags": c["wash_sale_flags"],
    }
    checks_free = {
        "checks": [
            {"id": "cash", "label": "Cash account, no margin", "ok": True,
             "detail": "FINRA requires $2,000 of equity for margin, so at $1,000 there is no borrowing and no short selling. Bearish bets use puts or inverse ETFs."},
            {"id": "instruments", "label": "Stocks, ETFs, listed options, spot crypto", "ok": True,
             "detail": "Options are bought (calls and puts), so the most a contract can lose is its premium. No naked option writing."},
            {"id": "gfv", "label": "No good-faith violations (T+1 settlement)", "ok": c["gfv"] == 0,
             "detail": f"{c['gfv']} violations. Stocks and options settle T+1; crypto settles instantly."},
            {"id": "activity", "label": "Activity tracked in the open", "ok": True,
             "detail": f"{c['orders_total']} orders so far ({c['orders_today']} today), {c['day_trades_total']} day trades. No pattern-day-trader limit in a cash account."},
            {"id": "law", "label": "Public information only", "ok": True,
             "detail": "Trades act on published news and prices: no insider information, no coordinated pumping."},
            {"id": "ofac", "label": "No OFAC-restricted (NS-CMIC) securities", "ok": True,
             "detail": "Applies to every US person and anyone physically in the US."},
        ],
        "wash_sale_flags": c["wash_sale_flags"],
    }
    compliance = checks_h1b if book == "h1b" else checks_free

    doc_id = now.strftime("%Y%m%dT%H%M%SZ")
    snap = {
        "id": doc_id,
        "book": book,
        "as_of": val["as_of"],
        "quotes_generated_at": qdoc.get("generated_at"),
        "session": val["session"],
        "challenge": {
            "name": cfg["name"], "short_name": cfg.get("short_name"), "start_capital": cfg["start_capital"],
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
        "levels": levels,
        "strategy": watch.get("strategy", ""),
        "schedule": {"next_update": next_update(now, sched), "cadence": sched.get("cadence", "")},
        "note": a.note,
    }
    out = Path(a.out) if a.out else cache / pfm.BOOKS[book]["snapshot"]
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
