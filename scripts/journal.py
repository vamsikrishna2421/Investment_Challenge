#!/usr/bin/env python3
"""Append a research/decision entry to ledger/journal.json.

  python scripts/journal.py --kind plan --title "..." --body "..." [--tickers A,B]
  python scripts/journal.py --kind research --title "..." --body-file notes.md
Kinds: plan, research, trade, review, risk, note
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

PATH = pfm.ROOT / "ledger" / "journal.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True,
                    choices=["plan", "research", "trade", "review", "risk", "note"])
    ap.add_argument("--title", required=True)
    b = ap.add_mutually_exclusive_group(required=True)
    b.add_argument("--body")
    b.add_argument("--body-file")
    ap.add_argument("--tickers", default="")
    a = ap.parse_args()
    data = json.loads(PATH.read_text()) if PATH.exists() else {"entries": []}
    body = a.body if a.body is not None else Path(a.body_file).read_text().strip()
    n = len(data["entries"]) + 1
    entry = {
        "id": f"J{n:04d}",
        "ts": pfm.iso(pfm.now_utc()),
        "kind": a.kind,
        "title": a.title,
        "body": body,
        "tickers": [t.strip().upper() for t in a.tickers.split(",") if t.strip()],
    }
    data["entries"].append(entry)
    PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"journal {entry['id']} added: {a.title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
