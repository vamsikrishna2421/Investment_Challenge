# Replay of the rules, 2023-12-19 to 2026-10-05 (700 sessions, hourly bars)

$1,000 each; S&P 500 +64.17%, Nasdaq-100 +85.76% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules: 25% of equity a position | +179.19% | 368 | 19.0% | 1.44% | 1.33 | -44.67% | SMCI, AXTI, NOW, RIOT |
| Risk 1% of equity to the stop, at most 25% | +53.76% | 455 | 22.0% | 1.05% | 1.1 | -32.57% | HIMX, AXTI, NOW, RIOT |
| Risk 1.5% of equity to the stop, at most 25% | +66.90% | 429 | 20.7% | 1.35% | 1.12 | -38.09% | SMCI, AXTI, NOW, WULF |
| Risk 2% of equity to the stop, at most 25% | +155.08% | 356 | 19.9% | 2.17% | 1.27 | -43.96% | SMCI, AXTI, NOW, RIOT |

