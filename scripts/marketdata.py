#!/usr/bin/env python3
"""Market-data pump. Runs inside GitHub Actions (the Claude container cannot
reach quote hosts). Writes into the checked-out `market-data` branch:

  data/quotes.json      latest quote per ticker (holdings + watchlist + benchmarks)
  data/portfolio.json   portfolio valuation at those quotes
  data/equity.jsonl     one line per run: equity curve + benchmark prices
  data/scan.json        (mode=scan) Yahoo screeners + 3-month stats per ticker
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
UTC = dt.timezone.utc


def http_json(url: str, timeout: float = 15.0) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def yahoo_chart(sym: str, rng: str, interval: str, prepost: bool) -> dict:
    last = None
    s = urllib.parse.quote(sym)
    for attempt in range(3):
        host = "query1" if attempt % 2 == 0 else "query2"
        url = (f"https://{host}.finance.yahoo.com/v8/finance/chart/{s}?range={rng}"
               f"&interval={interval}&includePrePost={'true' if prepost else 'false'}")
        try:
            j = http_json(url)
            res = j["chart"]["result"]
            if res:
                return res[0]
            last = RuntimeError(str(j["chart"].get("error")))
        except Exception as e:  # noqa: BLE001
            last = e
        time.sleep(0.6 * (attempt + 1))
    raise RuntimeError(f"{sym}: {last}")


def iso_epoch(e) -> str | None:
    if e is None:
        return None
    return dt.datetime.fromtimestamp(int(e), UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def quote(sym: str) -> dict:
    r = yahoo_chart(sym, "1d", "1m", True)
    m = r.get("meta", {})
    ts = r.get("timestamp") or []
    q = (r.get("indicators", {}).get("quote") or [{}])[0]
    closes = q.get("close") or []
    last_px, last_t = None, None
    for i in range(len(ts) - 1, -1, -1):
        if i < len(closes) and closes[i] is not None:
            last_px, last_t = float(closes[i]), int(ts[i])
            break
    price = m.get("regularMarketPrice")
    rtime = m.get("regularMarketTime")
    prev = m.get("previousClose") or m.get("chartPreviousClose")
    reg = (m.get("currentTradingPeriod") or {}).get("regular") or {}
    ext_px = ext_t = None
    if last_t is not None and reg:
        if last_t < reg.get("start", 0) or last_t >= reg.get("end", 1 << 62):
            ext_px, ext_t = last_px, last_t
    out = {
        "price": float(price) if price is not None else last_px,
        "time": iso_epoch(rtime),
        "prev_close": float(prev) if prev is not None else None,
        "day_high": m.get("regularMarketDayHigh"),
        "day_low": m.get("regularMarketDayLow"),
        "volume": m.get("regularMarketVolume"),
        "name": m.get("shortName") or m.get("longName"),
        "exchange": m.get("fullExchangeName") or m.get("exchangeName"),
        "instrument": m.get("instrumentType"),
        "ext_price": ext_px,
        "ext_time": iso_epoch(ext_t),
        "source": "yahoo-v8-chart",
    }
    if out["price"] and out["prev_close"]:
        out["change_pct"] = round((out["price"] / out["prev_close"] - 1) * 100, 3)
    if ext_px and out["price"]:
        out["ext_change_pct"] = round((ext_px / out["price"] - 1) * 100, 3)
    return out


def stats(sym: str) -> dict:
    r = yahoo_chart(sym, "6mo", "1d", False)
    q = (r.get("indicators", {}).get("quote") or [{}])[0]
    c = [x for x in (q.get("close") or []) if x is not None]
    h = [x for x in (q.get("high") or []) if x is not None]
    lo = [x for x in (q.get("low") or []) if x is not None]
    v = [x for x in (q.get("volume") or []) if x is not None]
    if len(c) < 10:
        return {}

    def ret(n):
        return round((c[-1] / c[-1 - n] - 1) * 100, 2) if len(c) > n else None

    trs = []
    for i in range(1, min(len(c), len(h), len(lo))):
        trs.append(max(h[i] - lo[i], abs(h[i] - c[i - 1]), abs(lo[i] - c[i - 1])))
    atr = sum(trs[-14:]) / min(14, len(trs)) if trs else None
    return {
        "close": round(c[-1], 4),
        "ret_1d": ret(1), "ret_5d": ret(5), "ret_20d": ret(20), "ret_60d": ret(60),
        "atr14_pct": round(atr / c[-1] * 100, 2) if atr else None,
        "avg_vol_20": int(sum(v[-20:]) / min(20, len(v))) if v else None,
        "high_6mo": round(max(h), 4) if h else None,
        "off_high_pct": round((c[-1] / max(h) - 1) * 100, 2) if h else None,
    }


SCREENERS = ["day_gainers", "most_actives", "small_cap_gainers", "aggressive_small_caps",
             "day_losers", "most_shorted_stocks", "growth_technology_stocks"]


def screener(scr: str) -> list:
    url = ("https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
           f"?formatted=false&scrIds={scr}&count=40&lang=en-US&region=US")
    rows = None
    try:
        j = http_json(url)
        rows = j["finance"]["result"][0]["quotes"]
    except Exception:  # noqa: BLE001
        try:
            import yfinance as yf  # type: ignore
            rows = yf.screen(scr, count=40).get("quotes", [])
        except Exception as e:  # noqa: BLE001
            return [{"error": str(e)[:200]}]
    keep = ("symbol", "shortName", "regularMarketPrice", "regularMarketChangePercent",
            "regularMarketVolume", "averageDailyVolume3Month", "marketCap",
            "preMarketPrice", "preMarketChangePercent", "postMarketChangePercent",
            "fiftyTwoWeekHigh", "shortPercentOfFloat", "sharesShort")
    return [{k: row.get(k) for k in keep if row.get(k) is not None} for row in rows]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="checkout of main (ledger/config)")
    ap.add_argument("--out", required=True, help="checkout of market-data branch")
    ap.add_argument("--mode", default="quotes")
    ap.add_argument("--extra", default="")
    a = ap.parse_args()

    root = Path(a.root)
    out = Path(a.out) / "data"
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(root / "scripts"))
    import portfolio as pfm  # noqa: E402

    cfg = json.loads((root / "config" / "challenge.json").read_text())
    ledger = json.loads((root / "ledger" / "transactions.json").read_text())
    wl_path = root / "config" / "watchlist.json"
    watch = json.loads(wl_path.read_text()).get("tickers", []) if wl_path.exists() else []
    held = sorted({t["ticker"] for t in ledger["transactions"] if t.get("ticker")})
    extra = [x.strip().upper() for x in a.extra.replace(" ", ",").split(",") if x.strip()]
    syms = list(dict.fromkeys(cfg["benchmarks"] + held + watch + extra))

    started = time.time()
    quotes, errors = {}, {}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(quote, s): s for s in syms}
        for f in cf.as_completed(futs):
            s = futs[f]
            try:
                quotes[s] = f.result()
            except Exception as e:  # noqa: BLE001
                errors[s] = str(e)[:300]

    now = pfm.now_utc()
    # Keep previous quotes for symbols that failed this run (marked stale).
    qfile = out / "quotes.json"
    if qfile.exists():
        try:
            old = json.loads(qfile.read_text()).get("quotes", {})
            for s in errors:
                if s in old:
                    quotes[s] = {**old[s], "stale": True}
        except Exception:  # noqa: BLE001
            pass
    qfile.write_text(json.dumps({
        "generated_at": pfm.iso(now), "session": pfm.market_session(now),
        "quotes": dict(sorted(quotes.items())), "errors": errors,
        "fetch_seconds": round(time.time() - started, 1),
    }, indent=1))

    pf = pfm.Portfolio(ledger, cfg)
    val = pf.valuation(quotes, now)
    (out / "portfolio.json").write_text(json.dumps(val, indent=1))

    point = {"t": pfm.iso(now), "session": val["session"], "equity": val["equity"],
             "cash": val["cash"], "invested": val["invested_value"]}
    for b in cfg["benchmarks"]:
        if b in quotes and quotes[b].get("price"):
            point[b] = quotes[b]["price"]
    with open(out / "equity.jsonl", "a") as fh:
        fh.write(json.dumps(point) + "\n")

    if a.mode == "scan":
        scan = {"generated_at": pfm.iso(now), "screeners": {}, "stats": {}}
        for scr in SCREENERS:
            scan["screeners"][scr] = screener(scr)
            time.sleep(0.4)
        stat_syms = list(dict.fromkeys(held + watch + extra))
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(stats, s): s for s in stat_syms}
            for f in cf.as_completed(futs):
                try:
                    scan["stats"][futs[f]] = f.result()
                except Exception as e:  # noqa: BLE001
                    scan["stats"][futs[f]] = {"error": str(e)[:200]}
        (out / "scan.json").write_text(json.dumps(scan, indent=1))

    print(f"quotes={len(quotes)} errors={len(errors)} equity={val['equity']} "
          f"session={val['session']} mode={a.mode}")
    if errors:
        print("errors:", json.dumps(errors)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
