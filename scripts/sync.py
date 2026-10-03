#!/usr/bin/env python3
"""Pull the latest market data written by GitHub Actions into .cache/.

  python scripts/sync.py            fetch origin/market-data and copy data files
  python scripts/sync.py --wait 150 wait up to N seconds for a NEW data commit first
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
FILES = ["quotes.json", "portfolio.json", "equity.jsonl", "scan.json", "news.json", "alerts.json",
         "portfolio_free.json", "equity_free.jsonl", "portfolio_guided.json", "equity_guided.jsonl",
         "options.json"]


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def remote_sha() -> str:
    out = git("ls-remote", "origin", "refs/heads/market-data", check=False)
    return out.split()[0] if out.strip() else ""


def pull_history() -> None:
    """Refresh the equity curves from the market-data branch; the Actions job owns them."""
    if subprocess.run(["git", "fetch", "--quiet", "origin", "market-data"], cwd=ROOT).returncode != 0:
        return
    for f in ("equity.jsonl", "equity_free.jsonl", "equity_guided.jsonl"):
        r = subprocess.run(["git", "show", f"origin/market-data:data/{f}"], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            (CACHE / f).write_text(r.stdout)


def fetch_local(mode: str, tickers: str) -> int:
    """Run the data pump here (needs internet access) into a scratch copy of the
    cache, then copy the fresh quotes/chains/news back. Equity history stays the
    one published by the Actions job on the market-data branch."""
    import shutil
    tmp = ROOT / ".cache-local" / "data"
    tmp.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        if (CACHE / f).exists():
            shutil.copy(CACHE / f, tmp / f)
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "marketdata.py"), "--root", str(ROOT),
                        "--out", str(ROOT / ".cache-local"), "--mode", mode, "--extra", tickers],
                       cwd=ROOT, capture_output=True, text=True, timeout=420)
    if r.returncode != 0:
        print(r.stdout[-800:], r.stderr[-1500:])
        return 1
    CACHE.mkdir(exist_ok=True)
    for f in ("quotes.json", "options.json", "news.json", "alerts.json", "scan.json",
              "portfolio.json", "portfolio_free.json"):
        if (tmp / f).exists():
            shutil.copy(tmp / f, CACHE / f)
    pull_history()
    q = json.loads((CACHE / "quotes.json").read_text())
    print(f"local {mode}: generated_at={q['generated_at']} session={q['session']} quotes={len(q['quotes'])} "
          f"errors={list(q.get('errors', {}))} | {r.stdout.strip().splitlines()[-1][:160] if r.stdout.strip() else ''}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait", type=int, default=0)
    ap.add_argument("--since", default="", help="SHA to wait past (default: current remote)")
    ap.add_argument("--local", action="store_true",
                    help="fetch quotes directly from this machine instead of waiting for the Actions job")
    ap.add_argument("--mode", default="quotes", help="with --local: quotes, news or scan")
    ap.add_argument("--tickers", default="", help="with --local: extra tickers or option contracts")
    a = ap.parse_args()
    if a.local:
        return fetch_local(a.mode, a.tickers)
    if a.wait:
        base = a.since or remote_sha()
        deadline = time.time() + a.wait
        while time.time() < deadline:
            cur = remote_sha()
            if cur and cur != base:
                break
            time.sleep(6)
        else:
            print(f"WARN: no new market-data commit within {a.wait}s (still {base[:8]})")
    git("fetch", "--quiet", "origin", "market-data")
    CACHE.mkdir(exist_ok=True)
    for f in FILES:
        r = subprocess.run(["git", "show", f"origin/market-data:data/{f}"], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode == 0:
            (CACHE / f).write_text(r.stdout)
    q = json.loads((CACHE / "quotes.json").read_text())
    sha = git("rev-parse", "--short", "origin/market-data").strip()
    print(f"market-data {sha} generated_at={q['generated_at']} session={q['session']} "
          f"quotes={len(q['quotes'])} errors={list(q.get('errors', {}))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
