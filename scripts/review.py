#!/usr/bin/env python3
"""Compact decision view for a routine run: portfolio, stop/target alerts,
focus-list movers and fresh headlines for held and focus tickers.

  python scripts/review.py [--news-hours 6] [--tickers A,B]
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache"


def pct(x):
    return "   n/a" if x is None else f"{x:+6.2f}%"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--news-hours", type=float, default=6)
    ap.add_argument("--tickers", default="")
    ap.add_argument("--book", default=None, help="h1b (default) or free")
    ap.add_argument("--brief", action="store_true", help="portfolio and positions only")
    a = ap.parse_args()
    book = pfm.current_book(a.book)

    cfg = pfm.load_config(book)
    ledger = pfm.load_ledger(book)
    qdoc = json.loads((CACHE / "quotes.json").read_text())
    quotes = qdoc["quotes"]
    now = pfm.now_utc()
    pf = pfm.Portfolio(ledger, cfg)
    val = pf.valuation(quotes, now)
    gen = pfm.parse_ts(qdoc["generated_at"])
    print(f"== [{book}] {pfm.iso(now)} ({pfm.fmt_et(now)}) session={val['session']} "
          f"quotes_age={int((now - gen).total_seconds() / 60)}m")
    print(f"Equity ${val['equity']:,.2f} | Net {val['net_profit']:+,.2f} ({val['return_pct']:+.2f}%) | "
          f"Cash ${val['cash']:,.2f} (settled {val['settled_cash']:,.2f}) | Day {val['day_pnl']:+,.2f} | "
          f"Realized {val['realized_pnl']:+,.2f} | Orders today {val['counts']['orders_today']} "
          f"total {val['counts']['orders_total']} | DT5d {val['counts']['day_trades_5d']}")
    base = cfg.get("benchmark_base", {})
    print("Benchmarks since book start (latest print): " + "  ".join(
        f"{b} {(pfm.mark(quotes.get(b))[0] / base[b] - 1) * 100:+.2f}%"
        for b in cfg["benchmarks"] if base.get(b) and (quotes.get(b) or {}).get("price")))

    last_buy = {}
    for t in pf.txns:
        if t["type"] == "BUY":
            last_buy[t["ticker"]] = t
    alerts = []
    print("POSITIONS")
    for p in val["positions"]:
        plan = (last_buy.get(p["ticker"]) or {}).get("plan") or {}
        stop, target = plan.get("stop"), plan.get("target")
        q = quotes.get(p["ticker"], {})
        flag = []
        if stop and p["price"] <= stop:
            flag.append("STOP HIT")
        if target and p["price"] >= target:
            flag.append("TARGET HIT")
        if p["unrealized_pct"] >= 25:
            flag.append("TRIM>=25%")
        if flag:
            alerts.append(f"{p['ticker']}: {', '.join(flag)}")
        extra = ""
        if p.get("asset") == "option":
            uq = quotes.get(p["option"]["underlying"]) or {}
            extra = f" [{p['label']}] bid {p.get('bid')} ask {p.get('ask')} und {pfm.mark(uq)[0]}"
        print(f" {p['ticker']:5} qty {p['qty']:<10g} avg {p['avg_cost']:<9.4g} last {p['price']:<9.4g} "
              f"unrl {p['unrealized_pnl']:+8.2f} ({p['unrealized_pct']:+.1f}%) day {pct(q.get('change_pct'))} "
              f"ext {pct(q.get('ext_change_pct'))} wt {p['weight_pct']:.0f}% stop {stop} tgt {target} "
              f"lock {p['sell_locked_until'] or '-'} {' '.join(flag)}{extra}")
    if not val["positions"]:
        print(" (none)")
    print("ALERTS: " + ("; ".join(alerts) if alerts else "none"))
    if a.brief:
        return 0

    wl = json.loads(pfm.book_path("watchlist", book).read_text())
    focus = list(dict.fromkeys(wl.get("focus", []) + [x.strip().upper() for x in a.tickers.split(",") if x.strip()]))
    print("FOCUS (last, day%, ext%, vol)")
    for tk in focus:
        q = quotes.get(tk)
        if not q:
            print(f" {tk:5} no quote")
            continue
        ext = ""
        if q.get("ext_price"):
            ext = (f" | ext {q['ext_price']:<9.4g} vol {q.get('ext_volume') or 0:,} "
                   f"range {q.get('ext_low')}-{q.get('ext_high')}")
        print(f" {tk:5} {q['price']:<10.4g} {pct(q.get('change_pct'))} ext {pct(q.get('ext_change_pct'))} "
              f"vol {q.get('volume') or 0:,}{ext}")
    movers = sorted(((tk, q) for tk, q in quotes.items() if q.get("change_pct") is not None),
                    key=lambda kv: kv[1]["change_pct"], reverse=True)
    print("WATCHLIST TOP: " + ", ".join(f"{tk} {q['change_pct']:+.1f}%" for tk, q in movers[:8]))
    print("WATCHLIST BOTTOM: " + ", ".join(f"{tk} {q['change_pct']:+.1f}%" for tk, q in movers[-6:]))

    apath = CACHE / "alerts.json"
    if apath.exists():
        al = json.loads(apath.read_text())
        print(f"ALERTS (generated {al['generated_at']}, session {al['session']})")
        for m in al.get("movers", [])[:15]:
            print(f" MOVER {m['symbol']:5} {'HELD ' if m.get('held') else ''}day {pct(m.get('change_pct'))} "
                  f"ext {pct(m.get('ext_change_pct'))} px {m.get('ext_price') or m.get('price')} vol {m.get('volume') or 0:,} "
                  f"{(m.get('name') or '')[:30]}")
        disc = [d for d in al.get("discovery", []) if d.get("change_pct") is not None]
        if disc:
            print(" DISCOVERY: " + ", ".join(f"{d['symbol']} {d['change_pct']:+.1f}% ({d['source']})" for d in
                                            sorted(disc, key=lambda d: -abs(d['change_pct']))[:14]))
        trend = [d["symbol"] for d in al.get("discovery", []) if d["source"] == "trending"]
        if trend:
            print(" TRENDING: " + ", ".join(trend[:20]))
        for h in al.get("new_headlines", [])[:25]:
            print(f" NEW {h['about'][:28]:28} {h['title'][:130]}")

    npath = CACHE / "news.json"
    if npath.exists():
        news = json.loads(npath.read_text())
        cutoff = now - dt.timedelta(hours=a.news_hours)
        held = [p["ticker"] for p in val["positions"]]
        print(f"NEWS (generated {news['generated_at']}, last {a.news_hours:g}h)")
        seen = set()
        for tk in held + focus:
            rows = []
            for it in news.get("tickers", {}).get(tk, []):
                if "error" in it or it["title"] in seen:
                    continue
                try:
                    pub = email.utils.parsedate_to_datetime(it["published"]).astimezone(pfm.UTC)
                except Exception:  # noqa: BLE001
                    continue
                if pub >= cutoff:
                    seen.add(it["title"])
                    rows.append(f"   {pub.astimezone(pfm.ET).strftime('%a %H:%M')} {it['title'][:140]}")
            if rows:
                print(f" [{tk}]")
                print("\n".join(rows[:5]))
        for qname, items in news.get("queries", {}).items():
            rows = []
            for it in items:
                if "error" in it or it["title"] in seen:
                    continue
                try:
                    pub = email.utils.parsedate_to_datetime(it["published"]).astimezone(pfm.UTC)
                except Exception:  # noqa: BLE001
                    continue
                if pub >= cutoff:
                    seen.add(it["title"])
                    rows.append(f"   {pub.astimezone(pfm.ET).strftime('%a %H:%M')} {it['title'][:140]}")
            if rows:
                print(f" <{qname}>")
                print("\n".join(rows[:4]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
