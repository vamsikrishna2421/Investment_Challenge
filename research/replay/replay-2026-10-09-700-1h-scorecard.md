# Replay of the rules, 2023-12-26 to 2026-10-09 (700 sessions, hourly bars)

$1,000 each; S&P 500 +64.38%, Nasdaq-100 +83.96% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Paper book: live rules (radar, resting limits, 1% gap allowance) | +83.86% | 438 | 21.5% | 1.3% | 1.15 | -36.07% | SMCI, NOW, APLD, GPUS |
| Real book: live rules (S&P gate, night sleeve) | +53.65% | 400 | 39.5% | 0.44% | 1.17 | -24.47% | HIMX, APLD |
| Real book's radar part alone (no night sleeve) | +8.97% | 211 | 17.5% | -0.08% | 1.03 | -28.95% | HIMX, APLD |
| Night sleeve alone (2 slots, down 1.5+ ATR in the lowest quarter, sold at the open) | +19.65% | 240 | 57.9% | 0.33% | 1.24 | -11.2% | - |

