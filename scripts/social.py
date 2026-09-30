#!/usr/bin/env python3
"""Social attention: what retail traders are piling into (Stocktwits trending, free), how loud the talk is
on given names, and, when an X API token is configured, the latest posts from the accounts in
config/x_accounts.json.

  python scripts/social.py                 # Stocktwits trending US stocks, with size, move and any SEC/news trigger
  python scripts/social.py IOVA MU NKE     # message rate and bull/bear tags on those names
  python scripts/social.py --x             # new posts from the X accounts (needs .secrets/x_bearer; paid API)
  python scripts/social.py --save          # also log today's trending list to research/social/<date>.json

Treat this as an attention and crowding gauge, not a buy signal. A study of 29,000 Stocktwits
"finfluencers" (Kakhbod et al. 2023) found 56% had negative skill (-2.3% a month) and only 28% had
skill; fading their posts earned 1.2% a month. A name trending with no filing or wire release behind it
is a pump-risk flag. The saved lists let us measure what trending names did next on our own data.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36")
ST = "https://api.stocktwits.com/api/2"


def get_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def trending() -> list[dict]:
    out = []
    for s in get_json(f"{ST}/trending/symbols.json").get("symbols", []):
        if s.get("exchange") == "CRYPTO" or s.get("instrument_class") not in (None, "Stock", "ETF", "equity", "Equity"):
            if s.get("exchange") == "CRYPTO":
                continue
        out.append({"symbol": s["symbol"], "name": s.get("title"), "exchange": s.get("exchange"),
                    "score": s.get("trending_score"), "watchers": s.get("watchlist_count"),
                    "why": ((s.get("trends") or {}).get("summary") or "").strip()})
    return out


def buzz(sym: str) -> dict:
    j = get_json(f"{ST}/streams/symbol/{urllib.parse.quote(sym)}.json")
    msgs = j.get("messages", [])
    if not msgs:
        return {"symbol": sym, "messages": 0}
    ts = [dt.datetime.fromisoformat(m["created_at"].replace("Z", "+00:00")) for m in msgs]
    span_h = max((max(ts) - min(ts)).total_seconds() / 3600, 0.1)
    sent = [((m.get("entities") or {}).get("sentiment") or {}).get("basic") for m in msgs]
    top = sorted(msgs, key=lambda m: -(m.get("user") or {}).get("followers", 0))[:3]
    return {"symbol": sym, "messages": len(msgs), "per_hour": round(len(msgs) / span_h, 1),
            "bullish": sent.count("Bullish"), "bearish": sent.count("Bearish"),
            "latest": pfm.iso(max(ts)),
            "loudest": [f"@{(m.get('user') or {}).get('username')} ({(m.get('user') or {}).get('followers', 0):,} "
                        f"followers): {' '.join(html.unescape(m.get('body', '')).split())[:140]}" for m in top]}


def x_posts() -> list[dict]:
    """New posts from config/x_accounts.json via the X API (pay per read; token in .secrets/x_bearer)."""
    tok_f = ROOT / ".secrets" / "x_bearer"
    if not tok_f.exists():
        print("X: no API token (.secrets/x_bearer). X sells reads at $0.005 a post; see RUNBOOK 1d.")
        return []
    tok = tok_f.read_text().strip()
    cfg = json.loads((ROOT / "config" / "x_accounts.json").read_text())
    state_f = ROOT / ".cache" / "x_state.json"
    state = json.loads(state_f.read_text()) if state_f.exists() else {}
    h = {"Authorization": f"Bearer {tok}"}
    names = [a["handle"] for a in cfg["accounts"]]
    ids = state.get("ids") or {}
    missing = [n for n in names if n not in ids]
    if missing:
        j = get_json("https://api.x.com/2/users/by?usernames=" + ",".join(missing), h)
        ids.update({u["username"]: u["id"] for u in j.get("data", [])})
    out = []
    for n in names:
        if n not in ids:
            continue
        q = {"max_results": 10, "tweet.fields": "created_at,public_metrics", "exclude": "retweets,replies"}
        if state.get("since", {}).get(n):
            q["since_id"] = state["since"][n]
        j = get_json(f"https://api.x.com/2/users/{ids[n]}/tweets?" + urllib.parse.urlencode(q), h)
        posts = j.get("data", [])
        if posts:
            state.setdefault("since", {})[n] = posts[0]["id"]
        out += [{"handle": n, "at": p.get("created_at"), "text": " ".join(p.get("text", "").split())} for p in posts]
    state["ids"] = ids
    (ROOT / ".cache").mkdir(exist_ok=True)
    state_f.write_text(json.dumps(state))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("symbols", nargs="*")
    ap.add_argument("--x", action="store_true")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    if a.x:
        for p in x_posts():
            print(f"{(p['at'] or '')[:16]} @{p['handle']}: {p['text'][:220]}")
        return 0
    if a.symbols:
        for s in a.symbols:
            try:
                b = buzz(s.upper())
            except Exception as e:  # noqa: BLE001
                print(f"{s.upper():6} error {str(e)[:80]}")
                continue
            if not b["messages"]:
                print(f"{b['symbol']:6} no messages")
                continue
            print(f"{b['symbol']:6} {b['per_hour']:>6.1f} msgs/hour (last 30) | bullish {b['bullish']} bearish {b['bearish']} "
                  f"| latest {b['latest']}")
            for x in b["loudest"]:
                print(f"         {x}")
        return 0
    rows = trending()
    uni = {}
    uf = ROOT / ".cache" / "universe.json"
    if uf.exists():
        uni = json.loads(uf.read_text()).get("stocks", {})
    wires = {}
    wf = ROOT / ".cache" / "wires.json"
    if wf.exists():
        for it in json.loads(wf.read_text()).get("items", []):
            if it.get("ticker") and (it.get("tags") or it.get("src") == "sec"):
                wires.setdefault(it["ticker"], []).append(it.get("src"))
    print(f"Stocktwits trending, {pfm.fmt_et(pfm.now_utc())} (attention, not advice; no filing or wire release = pump-risk flag)")
    for r in rows:
        u = uni.get(r["symbol"]) or {}
        mc = f"${u['mcap'] / 1e6:,.0f}M" if u.get("mcap") else "not in universe"
        src = ",".join(sorted(set(wires.get(r["symbol"], [])))) or "no wire/SEC item"
        print(f"{r['score'] or 0:>6.2f} {r['symbol']:7} {mc:>16} | {src:22} | {r['why'][:150]}")
    if a.save:
        d = ROOT / "research" / "social"
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{pfm.et_date(pfm.now_utc()).isoformat()}.json"
        prev = json.loads(f.read_text()) if f.exists() else {"snapshots": []}
        prev["snapshots"].append({"at": pfm.iso(pfm.now_utc()), "trending": rows})
        f.write_text(json.dumps(prev, indent=1))
        print(f"saved {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
