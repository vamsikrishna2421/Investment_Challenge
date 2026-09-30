#!/usr/bin/env python3
"""A scored forecasting record: my probability vs the market's, logged before the outcome, scored after.

  python scripts/forecasts.py add --q "Sep payrolls above +100k" --p 0.52 --market 0.47 \
      --source KXPAYROLLS-26SEP-T100000 --resolves 2026-10-02 --why "claims flat, ADP +80k"
  python scripts/forecasts.py resolve F0001 --outcome yes      # or no
  python scripts/forecasts.py score                            # Brier: mine vs the market's, over resolved ones

Edge exists only if my Brier score beats the market's over enough questions (30+ before it means much), and
by more than fees and spreads. Until then nothing gets traded on these forecasts.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

LOG = pfm.ROOT / "research" / "forecasts.json"


def load() -> list[dict]:
    return json.loads(LOG.read_text())["forecasts"] if LOG.exists() else []


def save(rows: list[dict]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps({"forecasts": rows}, indent=1) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("add")
    a1.add_argument("--q", required=True)
    a1.add_argument("--p", type=float, required=True, help="my probability of YES, 0-1")
    a1.add_argument("--market", type=float, help="market probability of YES at the same moment (mid price)")
    a1.add_argument("--source", default="", help="market ticker or where the price came from")
    a1.add_argument("--resolves", required=True, help="YYYY-MM-DD")
    a1.add_argument("--why", default="")
    a2 = sub.add_parser("resolve")
    a2.add_argument("id")
    a2.add_argument("--outcome", choices=["yes", "no"], required=True)
    sub.add_parser("score")
    a = ap.parse_args()
    rows = load()
    if a.cmd == "add":
        fid = f"F{len(rows) + 1:04d}"
        rows.append({"id": fid, "made_at": pfm.iso(pfm.now_utc()), "question": a.q, "p": a.p, "market": a.market,
                     "source": a.source, "resolves": a.resolves, "why": a.why, "outcome": None})
        save(rows)
        print(f"{fid} logged: {a.q} | me {a.p:.2f} vs market {a.market if a.market is not None else '-'}")
    elif a.cmd == "resolve":
        r = next((x for x in rows if x["id"] == a.id), None)
        if not r:
            print(f"no forecast {a.id}")
            return 1
        r["outcome"] = a.outcome
        r["resolved_at"] = pfm.iso(pfm.now_utc())
        save(rows)
        print(f"{a.id} resolved {a.outcome}")
    else:
        done = [r for r in rows if r["outcome"] in ("yes", "no")]
        both = [r for r in done if r.get("market") is not None]
        if not done:
            print(f"{len(rows)} logged, none resolved yet")
            return 0
        y = lambda r: 1.0 if r["outcome"] == "yes" else 0.0  # noqa: E731
        mine = sum((r["p"] - y(r)) ** 2 for r in done) / len(done)
        line = f"{len(done)} resolved of {len(rows)}: my Brier {mine:.4f}"
        if both:
            m_me = sum((r["p"] - y(r)) ** 2 for r in both) / len(both)
            m_mk = sum((r["market"] - y(r)) ** 2 for r in both) / len(both)
            line += f" | on the {len(both)} with a market price: me {m_me:.4f} vs market {m_mk:.4f} " \
                    f"({'better' if m_me < m_mk else 'worse or equal'}; lower is better)"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
