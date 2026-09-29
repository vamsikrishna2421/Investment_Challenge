#!/usr/bin/env python3
"""Market-data pump. Runs inside GitHub Actions (the Claude container cannot
reach quote hosts). Writes into the checked-out `market-data` branch:

  data/quotes.json      latest quote per ticker (holdings + watchlists + benchmarks, both books;
                        held option contracts are marked from the option chains)
  data/options.json     option chains (nearest expiries) for the free book's options_watch list
  data/portfolio.json   H-1B book valuation; data/portfolio_free.json for the free book
  data/equity.jsonl     one line per run: equity curve + benchmark prices (equity_free.jsonl)
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
    ext_vol, ext_hi, ext_lo = 0, None, None
    if last_t is not None and reg:
        if last_t < reg.get("start", 0) or last_t >= reg.get("end", 1 << 62):
            ext_px, ext_t = last_px, last_t
            # Volume and range of the current extended session (pre or post).
            pre = last_t < reg.get("start", 0)
            vols = q.get("volume") or []
            highs, lows = q.get("high") or [], q.get("low") or []
            for i, t in enumerate(ts):
                in_session = (t < reg.get("start", 0)) if pre else (t >= reg.get("end", 1 << 62))
                if not in_session:
                    continue
                if i < len(vols) and vols[i]:
                    ext_vol += int(vols[i])
                if i < len(highs) and highs[i] is not None:
                    ext_hi = highs[i] if ext_hi is None else max(ext_hi, highs[i])
                if i < len(lows) and lows[i] is not None:
                    ext_lo = lows[i] if ext_lo is None else min(ext_lo, lows[i])
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
        "ext_volume": ext_vol if ext_px else None,
        "ext_high": round(ext_hi, 4) if ext_hi else None,
        "ext_low": round(ext_lo, 4) if ext_lo else None,
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


FAST_SCREENERS = ["day_gainers", "small_cap_gainers", "most_actives"]
SYM_RE = __import__("re").compile(r"^[A-Z]{1,5}$")


def trending() -> list:
    try:
        j = http_json("https://query1.finance.yahoo.com/v1/finance/trending/US?count=30")
        return [q["symbol"] for q in j["finance"]["result"][0]["quotes"]]
    except Exception:  # noqa: BLE001
        return []


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


def _rss_items(url: str, limit: int) -> list:
    import html
    import re
    import xml.etree.ElementTree as ET
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/xml"})
    with urllib.request.urlopen(req, timeout=15) as r:
        root = ET.fromstring(r.read())
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        desc = re.sub(r"<[^>]+>", " ", html.unescape(it.findtext("description") or ""))
        desc = re.sub(r"\s+", " ", desc).strip()
        src = it.find("source")
        out.append({
            "title": title,
            "source": (src.text or "").strip() if src is not None else None,
            "published": (it.findtext("pubDate") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "summary": desc[:280] if desc and desc not in title else None,
        })
        if len(out) >= limit:
            break
    return out


def ticker_news(sym: str) -> list:
    items = []
    try:
        items += _rss_items(f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={urllib.parse.quote(sym)}"
                            "&region=US&lang=en-US", 8)
    except Exception as e:  # noqa: BLE001
        items.append({"error": f"yahoo: {str(e)[:120]}"})
    try:
        q = urllib.parse.quote(f"{sym} stock when:2d")
        items += _rss_items(f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en", 8)
    except Exception as e:  # noqa: BLE001
        items.append({"error": f"gnews: {str(e)[:120]}"})
    return items


def query_news(query: str) -> list:
    q = urllib.parse.quote(f"{query} when:1d")
    try:
        return _rss_items(f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en", 12)
    except Exception as e:  # noqa: BLE001
        return [{"error": str(e)[:200]}]


def fundamentals(sym: str) -> dict:
    try:
        import yfinance as yf  # type: ignore
        t = yf.Ticker(sym)
        info = t.get_info() or {}
        keep = ("marketCap", "floatShares", "sharesShort", "shortPercentOfFloat", "shortRatio",
                "averageVolume10days", "beta", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
                "targetMeanPrice", "recommendationKey", "sector", "industry", "earningsTimestamp")
        out = {k: info.get(k) for k in keep if info.get(k) is not None}
        try:
            cal = t.calendar or {}
            ed = cal.get("Earnings Date") if isinstance(cal, dict) else None
            if ed:
                out["earnings_dates"] = [str(x) for x in ed]
        except Exception:  # noqa: BLE001
            pass
        return out
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


def _num(x):
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    return None if f != f else f  # NaN -> None


def _chain_rows(rows, spot, band=0.3) -> list:
    out = []
    for r in rows:
        k = _num(r.get("strike"))
        if k is None or (spot and abs(k / spot - 1) > band):
            continue
        lt = r.get("lastTradeDate")
        if hasattr(lt, "timestamp"):
            lt = iso_epoch(lt.timestamp())
        elif isinstance(lt, (int, float)):
            lt = iso_epoch(lt)
        out.append({"contract": r.get("contractSymbol"), "strike": k,
                    "bid": _num(r.get("bid")) or 0.0, "ask": _num(r.get("ask")) or 0.0,
                    "last": _num(r.get("lastPrice")) or 0.0, "change": _num(r.get("change")),
                    "iv": round(_num(r.get("impliedVolatility")) or 0.0, 4),
                    "oi": int(_num(r.get("openInterest")) or 0), "volume": int(_num(r.get("volume")) or 0),
                    "last_trade": lt})
    return out


_YH = {"opener": None, "crumb": None}


def _yahoo_raw_options(sym: str, epoch: int | None = None) -> dict:
    """Yahoo v7 options endpoint with the cookie + crumb handshake (fallback path)."""
    import http.cookiejar
    if _YH["opener"] is None:
        _YH["opener"] = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        for u in ("https://fc.yahoo.com", "https://finance.yahoo.com/"):
            try:
                _YH["opener"].open(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10).read(200)
            except Exception:  # noqa: BLE001  (fc.yahoo.com answers 404 but sets the cookie)
                pass
        for host in ("query2", "query1"):
            try:
                c = _YH["opener"].open(urllib.request.Request(
                    f"https://{host}.finance.yahoo.com/v1/test/getcrumb", headers={"User-Agent": UA}), timeout=10).read().decode().strip()
                if c and "<" not in c and len(c) < 40:
                    _YH["crumb"] = c
                    break
            except Exception:  # noqa: BLE001
                pass
    url = (f"https://query2.finance.yahoo.com/v7/finance/options/{urllib.parse.quote(sym)}"
           f"?crumb={urllib.parse.quote(_YH['crumb'] or '')}" + (f"&date={epoch}" if epoch else ""))
    r = _YH["opener"].open(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"}), timeout=15)
    return json.loads(r.read().decode())["optionChain"]["result"][0]


def option_chains(unders: list, n_exp: int, need: dict, spots: dict, first_live: str) -> dict:
    """Chains for the nearest n_exp live expiries (plus any expiry in need[under]).
    first_live: earliest expiry date (YYYY-MM-DD) still trading."""
    out = {}
    try:
        import yfinance as yf  # type: ignore
    except Exception:  # noqa: BLE001
        yf = None
    for u in unders:
        entry = {"spot": spots.get(u), "expirations": [], "chains": {}, "source": None}
        try:
            if yf is None:
                raise RuntimeError("yfinance unavailable")
            t = yf.Ticker(u)
            exps = [e for e in (t.options or []) if e >= first_live]
            entry["expirations"] = exps[:8]
            want = list(dict.fromkeys(exps[:n_exp] + [e for e in need.get(u, []) if e in exps]))
            for e in want:
                ch = t.option_chain(e)
                entry["chains"][e] = {"calls": _chain_rows(ch.calls.to_dict("records"), entry["spot"]),
                                      "puts": _chain_rows(ch.puts.to_dict("records"), entry["spot"])}
                time.sleep(0.2)
            entry["source"] = "yfinance"
        except Exception as e1:  # noqa: BLE001
            try:
                res = _yahoo_raw_options(u)
                epochs = res.get("expirationDates") or []
                allx = [dt.datetime.fromtimestamp(x, UTC).strftime("%Y-%m-%d") for x in epochs]
                keep = [i for i, e in enumerate(allx) if e >= first_live]
                epochs, exps = [epochs[i] for i in keep], [allx[i] for i in keep]
                entry["expirations"] = exps[:8]
                entry["spot"] = entry["spot"] or (res.get("quote") or {}).get("regularMarketPrice")
                want = list(dict.fromkeys(exps[:n_exp] + [e for e in need.get(u, []) if e in exps]))
                for e in want:
                    r2 = _yahoo_raw_options(u, epochs[exps.index(e)])
                    o = (r2.get("options") or [{}])[0]
                    entry["chains"][e] = {"calls": _chain_rows(o.get("calls", []), entry["spot"]),
                                          "puts": _chain_rows(o.get("puts", []), entry["spot"])}
                    time.sleep(0.2)
                entry["source"] = "yahoo-v7"
            except Exception as e2:  # noqa: BLE001
                entry["error"] = f"yfinance: {str(e1)[:120]} | raw: {str(e2)[:120]}"
        out[u] = entry
    return out


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

    books = {}
    for b in pfm.BOOKS:
        cp = pfm.book_path("config", b, root)
        if not cp.exists():
            continue
        wlp = pfm.book_path("watchlist", b, root)
        books[b] = {"cfg": json.loads(cp.read_text()),
                    "ledger": json.loads(pfm.book_path("ledger", b, root).read_text()),
                    "wl": json.loads(wlp.read_text()) if wlp.exists() else {}}
    cfg = books["h1b"]["cfg"]
    watch, focus, opt_watch, n_exp = [], [], [], 2
    for bd in books.values():
        watch += bd["wl"].get("tickers", [])
        focus += bd["wl"].get("focus", [])
        opt_watch += bd["wl"].get("options_watch", [])
        n_exp = max(n_exp, int(bd["wl"].get("options_expiries", 2)))
    watch, focus = list(dict.fromkeys(watch)), list(dict.fromkeys(focus))
    held_opts, need_exp = set(), {}
    held = set()
    for bd in books.values():
        for t in bd["ledger"]["transactions"]:
            tk = t.get("ticker")
            if not tk:
                continue
            o = pfm.parse_option(tk)
            if o:
                held_opts.add(tk)
                held.add(o["underlying"])
                need_exp.setdefault(o["underlying"], []).append(o["expiry"])
            else:
                held.add(tk)
    held = sorted(held)
    extra = []
    for x in a.extra.replace(" ", ",").split(","):
        x = x.strip().upper()
        if not x:
            continue
        o = pfm.parse_option(x)
        if o:
            extra.append(o["underlying"])
            opt_watch.append(o["underlying"])
            need_exp.setdefault(o["underlying"], []).append(o["expiry"])
        else:
            extra.append(x)
    started = time.time()

    # Discovery (news/scan runs): trending tickers and today's biggest movers, so fresh
    # news-driven names get quotes even when they are not on the watchlist.
    discovery, disc_syms = [], []
    fast = {}
    if a.mode in ("news", "scan"):
        for scr in FAST_SCREENERS:
            fast[scr] = screener(scr)
        seen = set()
        for scr, rows in fast.items():
            rows = [r for r in rows if "symbol" in r and SYM_RE.match(r["symbol"])
                    and (r.get("regularMarketPrice") or 0) >= 1]
            key = (lambda r: abs(r.get("regularMarketChangePercent") or 0)) if scr == "most_actives" \
                else (lambda r: r.get("regularMarketChangePercent") or 0)
            for r in sorted(rows, key=key, reverse=True)[:12]:
                if r["symbol"] not in seen:
                    seen.add(r["symbol"])
                    discovery.append({"symbol": r["symbol"], "source": scr, "name": r.get("shortName"),
                                      "price": r.get("regularMarketPrice"),
                                      "change_pct": r.get("regularMarketChangePercent"),
                                      "volume": r.get("regularMarketVolume"),
                                      "pre_change_pct": r.get("preMarketChangePercent"),
                                      "post_change_pct": r.get("postMarketChangePercent")})
        for sym in trending():
            if SYM_RE.match(sym) and sym not in seen:
                seen.add(sym)
                discovery.append({"symbol": sym, "source": "trending"})
        disc_syms = [d["symbol"] for d in discovery]

    syms = list(dict.fromkeys(cfg["benchmarks"] + held + watch + extra + disc_syms))
    quotes, errors = {}, {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(quote, s): s for s in syms}
        for f in cf.as_completed(futs):
            s = futs[f]
            try:
                quotes[s] = f.result()
            except Exception as e:  # noqa: BLE001
                errors[s] = str(e)[:300]

    now = pfm.now_utc()
    # Option chains (weekdays only; chains do not change on weekends).
    opt_unders = list(dict.fromkeys(opt_watch + list(need_exp)))
    if opt_unders and pfm.is_business_day(pfm.et_date(now)):
        spots = {u: (quotes.get(u) or {}).get("price") for u in opt_unders}
        today = pfm.et_date(now)
        live = today if pfm.market_session(now) in ("pre", "regular") or now.astimezone(pfm.ET).hour < 4 \
            else today + dt.timedelta(days=1)
        chains = option_chains(opt_unders, n_exp, need_exp, spots, live.isoformat())
        (out / "options.json").write_text(json.dumps({"generated_at": pfm.iso(now), "session": pfm.market_session(now),
                                                      "underlyings": chains}, indent=1))
        for c in held_opts:
            o = pfm.parse_option(c)
            rows = ((chains.get(o["underlying"]) or {}).get("chains", {}).get(o["expiry"]) or {}).get(
                "calls" if o["type"] == "call" else "puts", [])
            row = next((r for r in rows if r["contract"] == c), None)
            if not row:
                continue
            bid, ask, last = row["bid"], row["ask"], row["last"]
            mid = round((bid + ask) / 2, 4) if bid > 0 and ask > 0 else (bid if bid > 0 else last)
            quotes[c] = {"price": mid, "time": pfm.iso(now), "bid": bid, "ask": ask, "last": last,
                         "prev_close": round(last - row["change"], 4) if row.get("change") is not None else None,
                         "iv": row.get("iv"), "oi": row.get("oi"), "volume": row.get("volume"),
                         "name": pfm.display_label(c), "underlying": o["underlying"],
                         "instrument": "OPTION", "source": "yahoo-option-chain"}
            if quotes[c]["prev_close"]:
                quotes[c]["change_pct"] = round((mid / quotes[c]["prev_close"] - 1) * 100, 3)
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

    vals = {}
    for b, bd in books.items():
        val = pfm.Portfolio(bd["ledger"], bd["cfg"]).valuation(quotes, now)
        vals[b] = val
        (out / pfm.BOOKS[b]["portfolio"]).write_text(json.dumps(val, indent=1))
        point = {"t": pfm.iso(now), "session": val["session"], "equity": val["equity"],
                 "cash": val["cash"], "invested": val["invested_value"]}
        for bm in bd["cfg"]["benchmarks"]:
            if bm in quotes and quotes[bm].get("price"):
                point[bm] = pfm.mark(quotes[bm])[0]
        with open(out / pfm.BOOKS[b]["equity"], "a") as fh:
            fh.write(json.dumps(point) + "\n")
    val = vals["h1b"]

    if a.mode == "scan":
        scan = {"generated_at": pfm.iso(now), "screeners": dict(fast), "stats": {}}
        for scr in SCREENERS:
            if scr not in scan["screeners"]:
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
        fsyms = list(dict.fromkeys(held + focus + extra))[:30]
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            futs = {ex.submit(fundamentals, s): s for s in fsyms}
            scan["fundamentals"] = {futs[f]: f.result() for f in cf.as_completed(futs)}
        (out / "scan.json").write_text(json.dumps(scan, indent=1))

    if a.mode in ("scan", "news"):
        ncfg_path = root / "config" / "news.json"
        ncfg = json.loads(ncfg_path.read_text()) if ncfg_path.exists() else {}
        top_disc = [d["symbol"] for d in sorted(
            (d for d in discovery if d.get("change_pct") is not None),
            key=lambda d: abs(d["change_pct"]), reverse=True)[:8]]
        nsyms = list(dict.fromkeys(held + extra + focus + top_disc))[:40]
        nfile = out / "news.json"
        prev_titles = set()
        if nfile.exists():
            try:
                prev = json.loads(nfile.read_text())
                for items in list(prev.get("tickers", {}).values()) + list(prev.get("queries", {}).values()):
                    prev_titles.update(i.get("title") for i in items if i.get("title"))
            except Exception:  # noqa: BLE001
                pass
        news = {"generated_at": pfm.iso(now), "tickers": {}, "queries": {}}
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            futs = {ex.submit(ticker_news, s): s for s in nsyms}
            for f in cf.as_completed(futs):
                news["tickers"][futs[f]] = f.result()
            qfuts = {ex.submit(query_news, q): q for q in ncfg.get("queries", [])}
            for f in cf.as_completed(qfuts):
                news["queries"][qfuts[f]] = f.result()
        nfile.write_text(json.dumps(news, indent=1))

        fresh = []
        if prev_titles:
            for key, items in [("$" + k, v) for k, v in news["tickers"].items()] + list(news["queries"].items()):
                for i in items:
                    if i.get("title") and i["title"] not in prev_titles:
                        fresh.append({"about": key, "title": i["title"], "source": i.get("source"),
                                      "published": i.get("published"), "link": i.get("link")})
        movers = []
        for sym, q in quotes.items():
            if sym in cfg["benchmarks"]:
                continue
            ch, ech = q.get("change_pct"), q.get("ext_change_pct")
            if (ch is not None and abs(ch) >= 6) or (ech is not None and abs(ech) >= 4):
                movers.append({"symbol": sym, "name": q.get("name"), "price": q.get("price"),
                               "change_pct": ch, "ext_price": q.get("ext_price"), "ext_change_pct": ech,
                               "volume": q.get("volume"), "held": sym in held})
        movers.sort(key=lambda m: max(abs(m["change_pct"] or 0), abs(m["ext_change_pct"] or 0)), reverse=True)
        (out / "alerts.json").write_text(json.dumps({
            "generated_at": pfm.iso(now), "session": pfm.market_session(now),
            "new_headlines": fresh[:80], "movers": movers[:30], "discovery": discovery,
        }, indent=1))

    print(f"quotes={len(quotes)} errors={len(errors)} "
          + " ".join(f"equity_{b}={v['equity']}" for b, v in vals.items())
          + f" session={val['session']} mode={a.mode} discovery={len(discovery)}")
    if errors:
        print("errors:", json.dumps(errors)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
