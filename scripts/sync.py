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
FILES = ["quotes.json", "portfolio.json", "equity.jsonl", "scan.json"]


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def remote_sha() -> str:
    out = git("ls-remote", "origin", "refs/heads/market-data", check=False)
    return out.split()[0] if out.strip() else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wait", type=int, default=0)
    ap.add_argument("--since", default="", help="SHA to wait past (default: current remote)")
    a = ap.parse_args()
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
