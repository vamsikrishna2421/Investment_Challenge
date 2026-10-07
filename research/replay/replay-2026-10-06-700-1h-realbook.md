# Replay of the rules, 2023-12-20 to 2026-10-06 (700 sessions, hourly bars)

$1,000 each; S&P 500 +64.07%, Nasdaq-100 +85.66% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Real-book rules, no S&P gate, limits from the open | -2.61% | 260 | 15.4% | -0.13% | 0.99 | -42.48% | WULF |
| Real-book rules + S&P gate 0.35% (live real book) | +20.04% | 212 | 18.4% | 0.17% | 1.06 | -30.42% | HIMX |
| Real-book rules + entries from 9:45 | -20.69% | 266 | 12.4% | -0.65% | 0.88 | -53.96% | WULF |
| Real-book rules + S&P gate + entries from 9:45 | -5.64% | 195 | 15.4% | -0.41% | 0.95 | -31.62% | NOW, WULF |
| Real-book rules + 1% gap allowance | +4.04% | 260 | 15.4% | -0.13% | 1.01 | -38.24% | WULF |
| Real-book rules + S&P gate + 9:45 + 1% gap allowance | +0.30% | 195 | 15.4% | -0.41% | 0.99 | -26.92% | NOW, WULF |

