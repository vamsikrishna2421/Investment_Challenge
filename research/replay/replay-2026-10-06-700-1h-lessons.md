# Replay of the rules, 2023-12-20 to 2026-10-06 (700 sessions, hourly bars)

$1,000 each; S&P 500 +64.07%, Nasdaq-100 +85.66% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules | +100.67% | 425 | 21.2% | 1.64% | 1.17 | -38.73% | SMCI, AXTI, NOW, WULF |
| No entries before 9:45 | +9.81% | 450 | 18.9% | 0.48% | 1.01 | -39.59% | HIMX, AXTI, NOW, RIOT |
| No entries while SPY is down 0.35%+ (orders cancelled) | +29.04% | 367 | 22.3% | 0.69% | 1.06 | -35.28% | HIMX, AXTI, NOW, RIOT |
| Both: entries from 9:45, S&P gate 0.35% | +22.07% | 377 | 20.7% | 0.11% | 1.04 | -40.52% | HIMX, AXTI, NOW, RIOT |
| Size on the stop distance plus a 1% gap allowance | +107.03% | 438 | 21.5% | 1.42% | 1.18 | -36.07% | AXTI, NOW, WULF, CIFR |
| Size on the stop distance plus a 2% gap allowance | +101.89% | 454 | 22.0% | 1.34% | 1.17 | -34.77% | AXTI, NOW, WULF, RIOT |
| No entry within 0.3 ATR of its stop | +106.97% | 404 | 23.0% | 1.51% | 1.2 | -39.76% | HIMX, SMCI, NOW, RIOT |
| No entry within 0.45 ATR of its stop | +75.00% | 385 | 23.9% | 1.4% | 1.14 | -37.06% | HIMX, SMCI, RIOT, WULF |
| No entry while down 1.0+ ATR on the day | +49.10% | 414 | 21.3% | 1.35% | 1.09 | -37.21% | HIMX, AXTI, RIOT, WULF |
| No entry while down 1.5+ ATR on the day | +134.75% | 423 | 21.7% | 1.89% | 1.21 | -38.32% | HIMX, AXTI, NOW, WULF |
| Entries only 0.25+ ATR under the prior close | +12.32% | 411 | 17.5% | 0.69% | 1.0 | -39.4% | HIMX, SMCI, BMNR, NOW |
| Gap through the stop: sell at 9:55 if still under | +83.54% | 418 | 20.6% | 1.82% | 1.16 | -39.73% | SMCI, AXTI, WULF, RIOT |

