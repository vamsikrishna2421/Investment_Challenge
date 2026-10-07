# Replay of the rules, 2026-07-15 to 2026-10-06 (59 sessions, 5-minute bars)

$1,000 each; S&P 500 +3.63%, Nasdaq-100 +5.55% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules | +14.73% | 40 | 25.0% | 1.89% | 1.14 | -14.0% | SMCI, NOW, UMAC, AXTI |
| No entries before 9:45 | +15.97% | 41 | 24.4% | 1.87% | 1.2 | -16.02% | SMCI, UMAC, AXTI, LUNR |
| No entries while SPY is down 0.35%+ (orders cancelled) | -1.61% | 38 | 18.4% | -0.72% | 0.85 | -18.78% | HIMX, NOW, RIOT, LUNR |
| Both: entries from 9:45, S&P gate 0.35% | +0.11% | 38 | 18.4% | -0.54% | 0.89 | -17.32% | HIMX, NOW, RIOT, LUNR |
| Size on the stop distance plus a 1% gap allowance | +25.94% | 34 | 23.5% | 2.31% | 1.47 | -16.76% | HIMX, SMCI, UMAC, AXTI |
| Size on the stop distance plus a 2% gap allowance | +15.84% | 43 | 16.3% | -0.04% | 1.13 | -16.63% | HIMX, SMCI, AXTI, RIOT |
| No entry within 0.3 ATR of its stop | +3.30% | 43 | 20.9% | 0.43% | 0.86 | -13.08% | SMCI, NOW, AXTI, RIOT |
| No entry within 0.45 ATR of its stop | +3.06% | 43 | 20.9% | -0.15% | 0.85 | -17.13% | SMCI, AXTI, RIOT, SMR |
| No entry while down 1.0+ ATR on the day | +10.84% | 37 | 27.0% | 2.3% | 1.17 | -11.38% | HIMX, UMAC, AXTI, WULF |
| No entry while down 1.5+ ATR on the day | +11.71% | 41 | 22.0% | 1.27% | 1.17 | -12.74% | HIMX, AXTI, RIOT, LUNR |
| Entries only 0.25+ ATR under the prior close | +24.10% | 29 | 20.7% | 2.44% | 1.47 | -9.7% | HIMX, SMCI, NOW, LUNR |
| Gap through the stop: sell at 9:55 if still under | +19.90% | 38 | 26.3% | 2.45% | 1.32 | -13.31% | SMCI, NOW, UMAC, AXTI |

## Live rules: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1147.27 (+14.73%; realized $+52.12, open positions $+95.15); S&P 500 +3.63%, Nasdaq-100 +5.55%. 40 closed trades, 10 winners (25.0%), average trade 1.89%, average win 24.3%, average loss -5.57%, profit factor 1.14, worst drawdown -14.0%. Exits: target 10, stop 30. Resting orders filled: 17/25.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -6.27%, total $-65.65
- stopped on a later session: 24 trades, 0 won, average -5.40%, total $-301.05
- stopped at the open (gapped through the stop): 13 trades, 0 won, average -5.63%, total $-175.68
- never rose 0.5 ATR above the entry: 21 trades, 0 won, average -5.66%, total $-265.46
- crypto-linked: 4 trades, 1 won, average -1.03%, total $-3.56
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-11.02
- bought on a dip of 0.5+ ATR (any time): 26 trades, 7 won, average +1.76%, total $+15.46
- bought less than 0.25 ATR under the prior close: 5 trades, 2 won, average +1.95%, total $+15.53
- resting limit fills: 15 trades, 3 won, average +1.75%, total $+22.07
- run entries inside the buy zone: 21 trades, 6 won, average +2.76%, total $+51.69
- run entries on a bounce (touched the zone, back above it): 4 trades, 1 won, average -2.12%, total $-21.64
- support tested 3+ times: 29 trades, 8 won, average +2.48%, total $+48.18
- support tested twice: 9 trades, 2 won, average +2.56%, total $+39.44
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-35.50

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.56% | +3.02 / -0.22 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.00% | +3.69 / -0.02 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.34% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.54% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.14% | +0.45 / -1.38 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.86% | +0.00 / -0.80 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-02 11:20 | WULF (crypto) | buy zone | 14.45 | -0.17 / -0.17 | 4.29 | 2026-09-08 9:50 | 16.98 | target | +17.54% | +2.27 / -0.05 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.53% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.60% | +1.65 / -0.71 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 138 | +5.75% |
| UMAC | 2026-09-16 | 21.43 | 20.98 | 26.12 | 22.36 | +4.34% |
| AXTI | 2026-09-30 | 75.92 | 70.99 | 89.31 | 84.06 | +10.72% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $962.97 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $961.19 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $984.78 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $975.53 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $987.05 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $957.22 | DUOL, HOOD, UMAC |
| 2026-07-27 | $996.99 | HOOD, UMAC |
| 2026-07-28 | $968.20 | DELL, UMAC |
| 2026-07-29 | $938.04 | AFRM, DELL, PCVX, UMAC |
| 2026-07-30 | $1000.86 | AFRM, DELL, PCVX, UMAC |
| 2026-07-31 | $993.30 | AFRM, DELL, PCVX, UMAC |
| 2026-08-03 | $1027.98 | AFRM, DELL, PCVX, UMAC |
| 2026-08-04 | $1093.03 | AFRM, AXTI, PCVX |
| 2026-08-05 | $1110.47 | AFRM, AXTI, PCVX, POET |
| 2026-08-06 | $1158.69 | AFRM, AXTI, NOW, POET |
| 2026-08-07 | $1225.16 | AFRM, MARA, NOW, POET |
| 2026-08-10 | $1202.17 | AFRM, MARA, NOW, POET |
| 2026-08-11 | $1210.30 | AFRM, MARA, NOW, POET |
| 2026-08-12 | $1206.01 | AFRM, MARA, NOW, POET |
| 2026-08-13 | $1208.89 | AFRM, NOW, ONDS, POET |
| 2026-08-14 | $1239.27 | AFRM, NOW, ONDS, POET |
| 2026-08-17 | $1196.80 | AFRM, NOW, POET, UPST |
| 2026-08-18 | $1156.79 | AFRM, NOW, POET, UPST |
| 2026-08-19 | $1187.63 | AFRM, NOW, POET, UPST |
| 2026-08-20 | $1149.73 | AFRM, NOW, POET, UMAC |
| 2026-08-21 | $1169.61 | AFRM, NOW, POET, UMAC |
| 2026-08-24 | $1125.09 | AFRM, CRSP, NOW |
| 2026-08-25 | $1153.26 | AFRM, CRSP, LUNR, NOW |
| 2026-08-26 | $1130.56 | AFRM, CRSP, LUNR, NOW |
| 2026-08-27 | $1146.02 | AFRM, CRSP, IONQ, LUNR |
| 2026-08-28 | $1128.19 | CRSP, IONQ |
| 2026-08-31 | $1132.81 | CRSP, IONQ, SMCI |
| 2026-09-01 | $1102.98 | CRSP, SMCI, SOUN |
| 2026-09-02 | $1092.08 | CRSP, SMCI, SOUN, WULF |
| 2026-09-03 | $1115.95 | CRSP, SMCI, SOUN, WULF |
| 2026-09-04 | $1129.73 | CRSP, SMCI, SOUN, WULF |
| 2026-09-08 | $1130.37 | DUOL, SMCI |
| 2026-09-09 | $1105.73 | QBTS, RGTI, SMCI, SMR |
| 2026-09-10 | $1071.88 | QBTS, SMCI |
| 2026-09-11 | $1098.07 | NOW, QBTS, SMCI |
| 2026-09-14 | $1082.81 | AEHR, NOW, SMCI |
| 2026-09-15 | $1065.80 | AEHR, GRAB, NOW, SMCI |
| 2026-09-16 | $1074.39 | AEHR, NOW, SMCI, UMAC |
| 2026-09-17 | $1117.65 | AEHR, NOW, SMCI, UMAC |
| 2026-09-18 | $1103.40 | AEHR, NOW, SMCI, UMAC |
| 2026-09-21 | $1134.84 | AEHR, NOW, SMCI, UMAC |
| 2026-09-22 | $1143.57 | AXTI, NOW, SMCI, UMAC |
| 2026-09-23 | $1128.36 | AXTI, NOW, SMCI, UMAC |
| 2026-09-24 | $1132.57 | HIMS, NOW, SMCI, UMAC |
| 2026-09-25 | $1145.29 | CRCL, NOW, SMCI, UMAC |
| 2026-09-28 | $1116.23 | CRCL, NOW, SMCI, UMAC |
| 2026-09-29 | $1105.98 | CRCL, NOW, SMCI, UMAC |
| 2026-09-30 | $1114.00 | AXTI, NOW, SMCI, UMAC |
| 2026-10-01 | $1126.82 | AXTI, NOW, SMCI, UMAC |
| 2026-10-02 | $1146.11 | AXTI, NOW, SMCI, UMAC |
| 2026-10-05 | $1145.19 | AXTI, NOW, SMCI, UMAC |
| 2026-10-06 | $1147.27 | AXTI, NOW, SMCI, UMAC |

## No entries before 9:45: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1159.74 (+15.97%; realized $+69.75, open positions $+89.99); S&P 500 +3.63%, Nasdaq-100 +5.55%. 41 closed trades, 10 winners (24.4%), average trade 1.87%, average win 24.43%, average loss -5.41%, profit factor 1.2, worst drawdown -16.02%. Exits: target 10, stop 31. Resting orders filled: 17/30.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -5.88%, total $-60.14
- stopped on a later session: 25 trades, 0 won, average -5.29%, total $-292.44
- stopped at the open (gapped through the stop): 14 trades, 0 won, average -5.43%, total $-174.92
- never rose 0.5 ATR above the entry: 20 trades, 0 won, average -5.49%, total $-226.97
- crypto-linked: 4 trades, 1 won, average -1.04%, total $+5.01
- bought on a dip of 0.5+ ATR (any time): 28 trades, 7 won, average +1.38%, total $+15.74
- bought less than 0.25 ATR under the prior close: 5 trades, 2 won, average +1.91%, total $+14.82
- resting limit fills: 16 trades, 3 won, average +1.70%, total $+22.36
- run entries inside the buy zone: 21 trades, 6 won, average +2.76%, total $+69.43
- run entries on a bounce (touched the zone, back above it): 4 trades, 1 won, average -2.12%, total $-22.04
- support tested 3+ times: 30 trades, 8 won, average +2.43%, total $+55.18
- support tested twice: 9 trades, 2 won, average +2.56%, total $+50.34
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-35.77

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:45 | POET | limit | 7.785 | -0.38 / -0.55 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.19% | +0.55 / -0.57 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:45 | UMAC | limit | 15.92 | -0.25 / -0.31 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +64.67% | +4.40 / -0.03 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:45 | HIMX | limit | 11.78 | -0.73 / -1.05 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -2.07% | +0.06 / -0.26 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.56% | +3.02 / -0.22 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.00% | +3.69 / -0.02 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.34% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.54% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:45 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.14% | +0.45 / -1.38 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.86% | +0.00 / -0.80 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-02 11:20 | WULF (crypto) | buy zone | 14.45 | -0.17 / -0.17 | 4.29 | 2026-09-08 9:50 | 16.98 | target | +17.54% | +2.27 / -0.05 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:45 | RGTI | limit | 15.67 | -0.18 / -0.14 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.33% | +0.27 / -0.81 |
| 2026-09-09 9:45 | SMR | limit | 10.87 | -0.24 / -0.44 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -3.86% | +0.23 / -0.84 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.53% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.60% | +1.65 / -0.71 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.26% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.61% | +0.07 / -0.90 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.48 | 35.01 | 50.6 | 43.46 | +19.13% |
| UMAC | 2026-09-16 | 21.43 | 20.98 | 26.12 | 22.36 | +4.34% |
| AXTI | 2026-09-30 | 75.92 | 70.99 | 89.31 | 84.06 | +10.72% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 15.06 | +6.52% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $970.50 | CRSP, IONQ, POET |
| 2026-07-17 | $965.95 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $964.22 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $988.02 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $978.76 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $990.47 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $960.42 | DUOL, HOOD, UMAC |
| 2026-07-27 | $1000.40 | HOOD, UMAC |
| 2026-07-28 | $977.31 | DELL, UMAC |
| 2026-07-29 | $946.92 | AFRM, DELL, PCVX, UMAC |
| 2026-07-30 | $1010.24 | AFRM, DELL, PCVX, UMAC |
| 2026-07-31 | $1002.61 | AFRM, DELL, PCVX, UMAC |
| 2026-08-03 | $1037.55 | AFRM, DELL, PCVX, UMAC |
| 2026-08-04 | $1103.20 | AFRM, AXTI, PCVX |
| 2026-08-05 | $1120.87 | AFRM, AXTI, PCVX, POET |
| 2026-08-06 | $1169.61 | AFRM, AXTI, NOW, POET |
| 2026-08-07 | $1236.88 | AFRM, MARA, NOW, POET |
| 2026-08-10 | $1213.65 | AFRM, MARA, NOW, POET |
| 2026-08-11 | $1221.85 | AFRM, MARA, NOW, POET |
| 2026-08-12 | $1217.56 | AFRM, MARA, NOW, POET |
| 2026-08-13 | $1220.43 | AFRM, NOW, ONDS, POET |
| 2026-08-14 | $1251.13 | AFRM, NOW, ONDS, POET |
| 2026-08-17 | $1208.33 | AFRM, NOW, POET, UPST |
| 2026-08-18 | $1167.93 | AFRM, NOW, POET, UPST |
| 2026-08-19 | $1198.97 | AFRM, NOW, POET, UPST |
| 2026-08-20 | $1160.67 | AFRM, NOW, POET, UMAC |
| 2026-08-21 | $1180.84 | AFRM, NOW, POET, UMAC |
| 2026-08-24 | $1135.75 | AFRM, CRSP, NOW |
| 2026-08-25 | $1164.20 | AFRM, CRSP, LUNR, NOW |
| 2026-08-26 | $1141.30 | AFRM, CRSP, LUNR, NOW |
| 2026-08-27 | $1156.76 | AFRM, CRSP, IONQ, LUNR |
| 2026-08-28 | $1138.77 | CRSP, IONQ |
| 2026-08-31 | $1141.76 | CRSP, IONQ, SMCI |
| 2026-09-01 | $1111.70 | CRSP, SMCI, SOUN |
| 2026-09-02 | $1100.72 | CRSP, SMCI, SOUN, WULF |
| 2026-09-03 | $1124.77 | CRSP, SMCI, SOUN, WULF |
| 2026-09-04 | $1138.60 | CRSP, SMCI, SOUN, WULF |
| 2026-09-08 | $1139.20 | DUOL, SMCI |
| 2026-09-09 | $1114.24 | QBTS, RGTI, SMCI, SMR |
| 2026-09-10 | $1080.14 | QBTS, SMCI |
| 2026-09-11 | $1102.19 | QBTS, SMCI |
| 2026-09-14 | $1066.70 | AEHR, SMCI |
| 2026-09-15 | $1050.72 | AEHR, GRAB, SMCI |
| 2026-09-16 | $1067.39 | AEHR, SMCI, UMAC |
| 2026-09-17 | $1125.61 | AEHR, SMCI, UMAC |
| 2026-09-18 | $1117.85 | AEHR, RGTI, SMCI, UMAC |
| 2026-09-21 | $1165.73 | AEHR, RGTI, SMCI, UMAC |
| 2026-09-22 | $1171.46 | AXTI, RGTI, SMCI, UMAC |
| 2026-09-23 | $1138.99 | AXTI, RGTI, SMCI, UMAC |
| 2026-09-24 | $1169.86 | HIMS, RGTI, SMCI, UMAC |
| 2026-09-25 | $1190.22 | CRCL, RGTI, SMCI, UMAC |
| 2026-09-28 | $1160.81 | CRCL, RGTI, SMCI, UMAC |
| 2026-09-29 | $1159.33 | CRCL, RGTI, SMCI, UMAC |
| 2026-09-30 | $1156.95 | AXTI, RGTI, SMCI, UMAC |
| 2026-10-01 | $1141.47 | AXTI, RGTI, SMCI, UMAC |
| 2026-10-02 | $1164.34 | AXTI, RGTI, SMCI, UMAC |
| 2026-10-05 | $1152.09 | AXTI, LUNR, SMCI, UMAC |
| 2026-10-06 | $1159.74 | AXTI, LUNR, SMCI, UMAC |

## No entries while SPY is down 0.35%+ (orders cancelled): 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $983.92 (-1.61%; realized $-52.67, open positions $+36.59); S&P 500 +3.63%, Nasdaq-100 +5.55%. 38 closed trades, 7 winners (18.4%), average trade -0.72%, average win 21.13%, average loss -5.66%, profit factor 0.85, worst drawdown -18.78%. Exits: target 7, stop 31. Resting orders filled: 9/34.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -3.21%, total $-32.04
- stopped on a later session: 27 trades, 0 won, average -6.02%, total $-318.58
- stopped at the open (gapped through the stop): 10 trades, 0 won, average -5.90%, total $-111.12
- never rose 0.5 ATR above the entry: 12 trades, 0 won, average -4.86%, total $-131.92
- crypto-linked: 6 trades, 1 won, average -2.12%, total $-52.14
- bought on a dip of 0.5+ ATR (any time): 26 trades, 6 won, average +0.56%, total $+44.35
- bought less than 0.25 ATR under the prior close: 6 trades, 1 won, average -2.12%, total $-23.77
- resting limit fills: 9 trades, 0 won, average -5.02%, total $-113.46
- run entries inside the buy zone: 24 trades, 7 won, average +2.56%, total $+114.51
- run entries on a bounce (touched the zone, back above it): 5 trades, 0 won, average -8.74%, total $-53.72
- support tested 3+ times: 29 trades, 4 won, average -2.17%, total $-160.88
- support tested twice: 8 trades, 3 won, average +5.43%, total $+125.15
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -7.89%, total $-16.94

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 10:05 | SMCI | buy zone | 25.94 | -0.21 / -0.54 | 2.23 | 2026-07-17 9:30 | 24.29 | stop | -6.39% | +0.54 / -1.29 |
| 2026-07-16 10:05 | POET | buy zone | 7.826 | -0.38 / -0.51 | 7.3 | 2026-07-17 9:30 | 7.304 | stop | -6.68% | +0.51 / -0.61 |
| 2026-07-16 10:05 | CRSP | buy zone | 49.08 | -0.19 / -0.65 | 2.17 | 2026-07-24 15:10 | 45.98 | stop | -6.32% | +0.65 / -0.90 |
| 2026-07-16 10:05 | AXTI | bounce | 48.62 | -0.30 / -0.57 | 1.51 | 2026-07-29 10:35 | 39.75 | stop | -18.27% | +1.07 / -1.05 |
| 2026-07-22 9:35 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.25 / -0.68 |
| 2026-07-24 10:30 | HOOD | limit | 94.37 | -0.28 / -1.14 | 6.19 | 2026-07-28 9:30 | 90.53 | stop | -4.07% | +0.80 / -0.72 |
| 2026-07-24 15:20 | SMTC | bounce | 127.2 | -0.26 / -1.13 | 1.56 | 2026-07-27 10:30 | 117.6 | stop | -7.55% | +0.09 / -0.98 |
| 2026-07-27 10:35 | HIMX | buy zone | 12.23 | +0.10 / -0.42 | 5.4 | 2026-07-29 10:25 | 11.52 | stop | -5.83% | +0.56 / -0.80 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.60% | +3.02 / -0.22 |
| 2026-07-29 14:35 | BTDR (crypto) | buy zone | 9.203 | -0.07 / -0.92 | 2.08 | 2026-07-30 9:50 | 10.55 | target | +14.62% | +1.33 / -0.36 |
| 2026-07-29 14:35 | APLD | buy zone | 24.19 | +0.07 / -1.01 | 4.18 | 2026-08-03 10:50 | 29.64 | target | +22.54% | +2.51 / -0.52 |
| 2026-07-29 14:35 | RIOT (crypto) | buy zone | 19.34 | -0.13 / -1.09 | 4.18 | 2026-08-19 10:10 | 17.91 | stop | -7.42% | +2.57 / -0.84 |
| 2026-07-30 9:50 | UPST | buy zone | 26.43 | -0.06 / -0.10 | 2.28 | 2026-08-03 11:50 | 29.29 | target | +10.78% | +1.85 / -0.34 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.35% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-19 10:20 | NBIS | buy zone | 217.8 | -0.59 / -1.12 | 14.82 | 2026-08-20 9:50 | 213.4 | stop | -2.01% | +0.51 / -0.19 |
| 2026-08-20 9:50 | RXRX | buy zone | 3.332 | -0.58 / -0.97 | 40.55 | 2026-08-20 10:05 | 3.281 | stop | -1.52% | +0.00 / -0.24 |
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.68% | +1.75 / -1.59 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-28 12:50 | COIN (crypto) | buy zone | 177.4 | -0.46 / -1.31 | 4.18 | 2026-09-15 14:45 | 169.6 | stop | -4.45% | +1.82 / -0.92 |
| 2026-09-03 11:20 | GPUS | buy zone | 0.181 | +0.42 / -0.51 | 21.1 | 2026-09-24 9:35 | 0.1669 | stop | -7.89% | +0.74 / -0.40 |
| 2026-09-08 10:50 | DUOL | buy zone | 146.7 | -0.26 / -1.05 | 3.26 | 2026-09-09 10:15 | 140.8 | stop | -3.98% | +0.06 / -0.92 |
| 2026-09-09 10:35 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.52% | +0.64 / -0.85 |
| 2026-09-14 11:50 | AEHR | buy zone | 85.23 | -1.19 / -1.22 | 3.18 | 2026-09-22 13:50 | 99.05 | target | +16.20% | +1.80 / -0.55 |
| 2026-09-18 14:20 | LUNR | buy zone | 13.91 | +0.14 / -1.11 | 18.39 | 2026-09-22 11:20 | 15.71 | target | +12.95% | +2.41 / -0.07 |
| 2026-09-22 11:20 | AXTI | buy zone | 75.39 | -0.55 / -0.76 | 3.4 | 2026-09-24 9:30 | 70.78 | stop | -6.13% | +0.56 / -0.97 |
| 2026-09-24 10:05 | STNE | buy zone | 9.483 | -0.03 / -0.02 | 3.73 | 2026-09-24 13:35 | 9.171 | stop | -3.30% | +0.00 / -0.77 |
| 2026-09-24 10:05 | QUBT | buy zone | 9.023 | -0.68 / -0.25 | 17.61 | 2026-09-28 10:40 | 8.685 | stop | -3.76% | +0.70 / -0.84 |
| 2026-09-24 10:05 | RGTI | bounce | 15.98 | -0.36 / -0.03 | 13.54 | 2026-10-05 9:30 | 15.05 | stop | -5.84% | +1.42 / -1.20 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-29 11:35 | IREN (crypto) | buy zone | 41.7 | +0.32 / -0.01 | 1.86 | 2026-10-01 9:40 | 40.17 | stop | -3.69% | +0.27 / -0.63 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.93 | 11.57 | 15.81 | 14.85 | +14.89% |
| NOW | 2026-09-29 | 131.4 | 127.1 | 146.9 | 138 | +5.01% |
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 18.93 | -3.76% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 15.06 | +6.52% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $961.90 | AXTI, CRSP, POET, SMCI |
| 2026-07-17 | $946.41 | AXTI, CRSP |
| 2026-07-20 | $947.57 | AXTI, CRSP |
| 2026-07-21 | $966.28 | AXTI, CRSP |
| 2026-07-22 | $944.69 | AXTI, CRSP, POET |
| 2026-07-23 | $941.64 | AXTI, CRSP |
| 2026-07-24 | $924.19 | AXTI, HOOD, SMTC |
| 2026-07-27 | $926.90 | AXTI, HIMX, HOOD |
| 2026-07-28 | $901.14 | AXTI, DELL, HIMX |
| 2026-07-29 | $857.70 | APLD, BTDR, DELL, RIOT |
| 2026-07-30 | $965.68 | APLD, DELL, RIOT, UPST |
| 2026-07-31 | $944.37 | APLD, DELL, RIOT, UPST |
| 2026-08-03 | $1000.17 | DELL, HIMX, RIOT |
| 2026-08-04 | $1040.99 | AXTI, HIMX, RIOT |
| 2026-08-05 | $1044.65 | AXTI, HIMX, POET, RIOT |
| 2026-08-06 | $1086.18 | AXTI, HIMX, POET, RIOT |
| 2026-08-07 | $1157.43 | HIMX, MARA, POET, RIOT |
| 2026-08-10 | $1127.00 | HIMX, MARA, POET, RIOT |
| 2026-08-11 | $1140.62 | HIMX, MARA, POET, RIOT |
| 2026-08-12 | $1150.64 | HIMX, MARA, POET, RIOT |
| 2026-08-13 | $1123.54 | HIMX, ONDS, POET, RIOT |
| 2026-08-14 | $1156.99 | HIMX, ONDS, POET, RIOT |
| 2026-08-17 | $1143.71 | HIMX, POET, RIOT, UPST |
| 2026-08-18 | $1087.85 | HIMX, POET, RIOT, UPST |
| 2026-08-19 | $1092.68 | HIMX, NBIS, POET, UPST |
| 2026-08-20 | $1051.11 | HIMX, POET |
| 2026-08-21 | $1051.54 | HIMX, POET |
| 2026-08-24 | $1010.04 | CRSP, HIMX |
| 2026-08-25 | $1027.66 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-26 | $1016.10 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-27 | $1027.14 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-28 | $1003.03 | COIN, CRSP, HIMX, SOUN |
| 2026-08-31 | $1016.91 | COIN, CRSP, HIMX, SOUN |
| 2026-09-01 | $986.88 | COIN, CRSP, HIMX, SOUN |
| 2026-09-02 | $982.83 | COIN, CRSP, HIMX, SOUN |
| 2026-09-03 | $1014.73 | COIN, CRSP, GPUS, HIMX |
| 2026-09-04 | $1002.89 | COIN, CRSP, GPUS, HIMX |
| 2026-09-08 | $994.78 | COIN, DUOL, GPUS, HIMX |
| 2026-09-09 | $990.79 | COIN, GPUS, HIMX, QBTS |
| 2026-09-10 | $970.11 | COIN, GPUS, HIMX, QBTS |
| 2026-09-11 | $983.93 | COIN, GPUS, HIMX, QBTS |
| 2026-09-14 | $996.66 | AEHR, COIN, GPUS, HIMX |
| 2026-09-15 | $945.89 | AEHR, GPUS, HIMX |
| 2026-09-16 | $940.04 | AEHR, GPUS, HIMX |
| 2026-09-17 | $963.38 | AEHR, GPUS, HIMX |
| 2026-09-18 | $975.05 | AEHR, GPUS, HIMX, LUNR |
| 2026-09-21 | $1033.08 | AEHR, GPUS, HIMX, LUNR |
| 2026-09-22 | $1032.03 | AXTI, GPUS, HIMX |
| 2026-09-23 | $1007.96 | AXTI, GPUS, HIMX |
| 2026-09-24 | $995.88 | HIMX, QUBT, RGTI |
| 2026-09-25 | $995.05 | BTBT, HIMX, QUBT, RGTI |
| 2026-09-28 | $969.55 | BTBT, HIMX, RGTI |
| 2026-09-29 | $964.31 | HIMX, IREN, NOW, RGTI |
| 2026-09-30 | $968.64 | HIMX, IREN, NOW, RGTI |
| 2026-10-01 | $973.74 | HIMX, NOW, RGTI, RIOT |
| 2026-10-02 | $974.86 | HIMX, NOW, RGTI, RIOT |
| 2026-10-05 | $970.47 | HIMX, LUNR, NOW, RIOT |
| 2026-10-06 | $983.92 | HIMX, LUNR, NOW, RIOT |

## Both: entries from 9:45, S&P gate 0.35%: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1001.15 (+0.11%; realized $-35.79, open positions $+36.94); S&P 500 +3.63%, Nasdaq-100 +5.55%. 38 closed trades, 7 winners (18.4%), average trade -0.54%, average win 21.13%, average loss -5.44%, profit factor 0.89, worst drawdown -17.32%. Exits: target 7, stop 31. Resting orders filled: 9/34.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -1.49%, total $-14.17
- stopped on a later session: 27 trades, 0 won, average -6.02%, total $-320.83
- stopped at the open (gapped through the stop): 10 trades, 0 won, average -5.90%, total $-111.47
- never rose 0.5 ATR above the entry: 12 trades, 0 won, average -4.29%, total $-114.87
- crypto-linked: 6 trades, 1 won, average -2.12%, total $-52.90
- bought on a dip of 0.5+ ATR (any time): 27 trades, 6 won, average +0.63%, total $+51.17
- bought less than 0.25 ATR under the prior close: 6 trades, 1 won, average -2.12%, total $-24.61
- resting limit fills: 9 trades, 0 won, average -4.26%, total $-96.13
- run entries inside the buy zone: 24 trades, 7 won, average +2.56%, total $+114.12
- run entries on a bounce (touched the zone, back above it): 5 trades, 0 won, average -8.74%, total $-53.78
- support tested 3+ times: 29 trades, 4 won, average -1.93%, total $-144.49
- support tested twice: 8 trades, 3 won, average +5.43%, total $+125.95
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -7.89%, total $-17.25

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 10:05 | SMCI | buy zone | 25.94 | -0.21 / -0.54 | 2.23 | 2026-07-17 9:30 | 24.29 | stop | -6.39% | +0.54 / -1.29 |
| 2026-07-16 10:05 | POET | buy zone | 7.826 | -0.38 / -0.51 | 7.3 | 2026-07-17 9:30 | 7.304 | stop | -6.68% | +0.51 / -0.61 |
| 2026-07-16 10:05 | CRSP | buy zone | 49.08 | -0.19 / -0.65 | 2.17 | 2026-07-24 15:10 | 45.98 | stop | -6.32% | +0.65 / -0.90 |
| 2026-07-16 10:05 | AXTI | bounce | 48.62 | -0.30 / -0.57 | 1.51 | 2026-07-29 10:35 | 39.75 | stop | -18.27% | +1.07 / -1.05 |
| 2026-07-22 12:25 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.01 / -0.68 |
| 2026-07-24 10:30 | HOOD | limit | 94.37 | -0.28 / -1.14 | 6.19 | 2026-07-28 9:30 | 90.53 | stop | -4.07% | +0.80 / -0.72 |
| 2026-07-24 15:20 | SMTC | bounce | 127.2 | -0.26 / -1.13 | 1.56 | 2026-07-27 10:30 | 117.6 | stop | -7.55% | +0.09 / -0.98 |
| 2026-07-27 10:35 | HIMX | buy zone | 12.23 | +0.10 / -0.42 | 5.4 | 2026-07-29 10:25 | 11.52 | stop | -5.83% | +0.56 / -0.80 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.60% | +3.02 / -0.22 |
| 2026-07-29 14:35 | BTDR (crypto) | buy zone | 9.203 | -0.07 / -0.92 | 2.08 | 2026-07-30 9:50 | 10.55 | target | +14.62% | +1.33 / -0.36 |
| 2026-07-29 14:35 | APLD | buy zone | 24.19 | +0.07 / -1.01 | 4.18 | 2026-08-03 10:50 | 29.64 | target | +22.54% | +2.51 / -0.52 |
| 2026-07-29 14:35 | RIOT (crypto) | buy zone | 19.34 | -0.13 / -1.09 | 4.18 | 2026-08-19 10:10 | 17.91 | stop | -7.42% | +2.57 / -0.84 |
| 2026-07-30 9:50 | UPST | buy zone | 26.43 | -0.06 / -0.10 | 2.28 | 2026-08-03 11:50 | 29.29 | target | +10.78% | +1.85 / -0.34 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.35% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-19 10:20 | NBIS | buy zone | 217.8 | -0.59 / -1.12 | 14.82 | 2026-08-20 9:50 | 213.4 | stop | -2.01% | +0.51 / -0.19 |
| 2026-08-20 9:50 | RXRX | buy zone | 3.332 | -0.58 / -0.97 | 40.55 | 2026-08-20 10:05 | 3.281 | stop | -1.52% | +0.00 / -0.24 |
| 2026-08-24 9:45 | SMCI | limit | 34.87 | -0.28 / -0.93 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -0.64% | +0.00 / -0.09 |
| 2026-08-24 9:45 | RXRX | limit | 3.235 | -0.48 / -1.43 | 5.59 | 2026-08-24 9:45 | 3.219 | stop | -0.51% | +0.00 / -0.08 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.68% | +1.75 / -1.59 |
| 2026-08-25 9:45 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-25 9:45 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-28 12:50 | COIN (crypto) | buy zone | 177.4 | -0.46 / -1.31 | 4.18 | 2026-09-15 14:45 | 169.6 | stop | -4.45% | +1.82 / -0.92 |
| 2026-09-03 11:20 | GPUS | buy zone | 0.181 | +0.42 / -0.51 | 21.1 | 2026-09-24 9:35 | 0.1669 | stop | -7.89% | +0.74 / -0.40 |
| 2026-09-08 10:50 | DUOL | buy zone | 146.7 | -0.26 / -1.05 | 3.26 | 2026-09-09 10:15 | 140.8 | stop | -3.98% | +0.06 / -0.92 |
| 2026-09-09 10:35 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.52% | +0.64 / -0.85 |
| 2026-09-14 11:50 | AEHR | buy zone | 85.23 | -1.19 / -1.22 | 3.18 | 2026-09-22 13:50 | 99.05 | target | +16.20% | +1.80 / -0.55 |
| 2026-09-18 14:20 | LUNR | buy zone | 13.91 | +0.14 / -1.11 | 18.39 | 2026-09-22 11:20 | 15.71 | target | +12.95% | +2.41 / -0.07 |
| 2026-09-22 11:20 | AXTI | buy zone | 75.39 | -0.55 / -0.76 | 3.4 | 2026-09-24 9:30 | 70.78 | stop | -6.13% | +0.56 / -0.97 |
| 2026-09-24 10:05 | STNE | buy zone | 9.483 | -0.03 / -0.02 | 3.73 | 2026-09-24 13:35 | 9.171 | stop | -3.30% | +0.00 / -0.77 |
| 2026-09-24 10:05 | QUBT | buy zone | 9.023 | -0.68 / -0.25 | 17.61 | 2026-09-28 10:40 | 8.685 | stop | -3.76% | +0.70 / -0.84 |
| 2026-09-24 10:05 | RGTI | bounce | 15.98 | -0.36 / -0.03 | 13.54 | 2026-10-05 9:30 | 15.05 | stop | -5.84% | +1.42 / -1.20 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-29 11:35 | IREN (crypto) | buy zone | 41.7 | +0.32 / -0.01 | 1.86 | 2026-10-01 9:40 | 40.17 | stop | -3.69% | +0.27 / -0.63 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.93 | 11.57 | 15.81 | 14.85 | +14.89% |
| NOW | 2026-09-29 | 131.4 | 127.1 | 146.9 | 138 | +5.01% |
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 18.93 | -3.76% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 15.06 | +6.52% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $961.90 | AXTI, CRSP, POET, SMCI |
| 2026-07-17 | $946.41 | AXTI, CRSP |
| 2026-07-20 | $947.57 | AXTI, CRSP |
| 2026-07-21 | $966.28 | AXTI, CRSP |
| 2026-07-22 | $944.69 | AXTI, CRSP, POET |
| 2026-07-23 | $941.64 | AXTI, CRSP |
| 2026-07-24 | $924.19 | AXTI, HOOD, SMTC |
| 2026-07-27 | $926.90 | AXTI, HIMX, HOOD |
| 2026-07-28 | $901.14 | AXTI, DELL, HIMX |
| 2026-07-29 | $857.70 | APLD, BTDR, DELL, RIOT |
| 2026-07-30 | $965.68 | APLD, DELL, RIOT, UPST |
| 2026-07-31 | $944.37 | APLD, DELL, RIOT, UPST |
| 2026-08-03 | $1000.17 | DELL, HIMX, RIOT |
| 2026-08-04 | $1040.99 | AXTI, HIMX, RIOT |
| 2026-08-05 | $1044.65 | AXTI, HIMX, POET, RIOT |
| 2026-08-06 | $1086.18 | AXTI, HIMX, POET, RIOT |
| 2026-08-07 | $1157.43 | HIMX, MARA, POET, RIOT |
| 2026-08-10 | $1127.00 | HIMX, MARA, POET, RIOT |
| 2026-08-11 | $1140.62 | HIMX, MARA, POET, RIOT |
| 2026-08-12 | $1150.64 | HIMX, MARA, POET, RIOT |
| 2026-08-13 | $1123.54 | HIMX, ONDS, POET, RIOT |
| 2026-08-14 | $1156.99 | HIMX, ONDS, POET, RIOT |
| 2026-08-17 | $1143.71 | HIMX, POET, RIOT, UPST |
| 2026-08-18 | $1087.85 | HIMX, POET, RIOT, UPST |
| 2026-08-19 | $1092.68 | HIMX, NBIS, POET, UPST |
| 2026-08-20 | $1051.11 | HIMX, POET |
| 2026-08-21 | $1051.54 | HIMX, POET |
| 2026-08-24 | $1028.05 | CRSP, HIMX |
| 2026-08-25 | $1045.78 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-26 | $1034.06 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-27 | $1045.26 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-28 | $1020.89 | COIN, CRSP, HIMX, SOUN |
| 2026-08-31 | $1035.28 | COIN, CRSP, HIMX, SOUN |
| 2026-09-01 | $1004.48 | COIN, CRSP, HIMX, SOUN |
| 2026-09-02 | $1000.28 | COIN, CRSP, HIMX, SOUN |
| 2026-09-03 | $1033.22 | COIN, CRSP, GPUS, HIMX |
| 2026-09-04 | $1020.98 | COIN, CRSP, GPUS, HIMX |
| 2026-09-08 | $1012.57 | COIN, DUOL, GPUS, HIMX |
| 2026-09-09 | $1008.40 | COIN, GPUS, HIMX, QBTS |
| 2026-09-10 | $987.38 | COIN, GPUS, HIMX, QBTS |
| 2026-09-11 | $1001.36 | COIN, GPUS, HIMX, QBTS |
| 2026-09-14 | $1015.01 | AEHR, COIN, GPUS, HIMX |
| 2026-09-15 | $962.83 | AEHR, GPUS, HIMX |
| 2026-09-16 | $956.91 | AEHR, GPUS, HIMX |
| 2026-09-17 | $980.57 | AEHR, GPUS, HIMX |
| 2026-09-18 | $992.39 | AEHR, GPUS, HIMX, LUNR |
| 2026-09-21 | $1051.37 | AEHR, GPUS, HIMX, LUNR |
| 2026-09-22 | $1050.35 | AXTI, GPUS, HIMX |
| 2026-09-23 | $1025.79 | AXTI, GPUS, HIMX |
| 2026-09-24 | $1013.45 | HIMX, QUBT, RGTI |
| 2026-09-25 | $1012.56 | BTBT, HIMX, QUBT, RGTI |
| 2026-09-28 | $986.68 | BTBT, HIMX, RGTI |
| 2026-09-29 | $981.32 | HIMX, IREN, NOW, RGTI |
| 2026-09-30 | $985.74 | HIMX, IREN, NOW, RGTI |
| 2026-10-01 | $990.86 | HIMX, NOW, RGTI, RIOT |
| 2026-10-02 | $991.88 | HIMX, NOW, RGTI, RIOT |
| 2026-10-05 | $987.49 | HIMX, LUNR, NOW, RIOT |
| 2026-10-06 | $1001.15 | HIMX, LUNR, NOW, RIOT |

## Size on the stop distance plus a 1% gap allowance: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1259.36 (+25.94%; realized $+152.21, open positions $+107.15); S&P 500 +3.63%, Nasdaq-100 +5.55%. 34 closed trades, 8 winners (23.5%), average trade 2.31%, average win 26.87%, average loss -5.25%, profit factor 1.47, worst drawdown -16.76%. Exits: target 8, stop 26. Resting orders filled: 11/18.

### What the trades had in common

- stopped the session it was bought: 2 trades, 0 won, average -3.02%, total $-15.32
- stopped on a later session: 24 trades, 0 won, average -5.44%, total $-309.26
- stopped at the open (gapped through the stop): 12 trades, 0 won, average -5.55%, total $-168.54
- never rose 0.5 ATR above the entry: 17 trades, 0 won, average -5.19%, total $-203.77
- crypto-linked: 2 trades, 0 won, average -6.90%, total $-32.44
- bought on a dip of 0.5+ ATR (any time): 24 trades, 6 won, average +1.77%, total $+116.79
- bought less than 0.25 ATR under the prior close: 4 trades, 1 won, average -1.56%, total $-10.10
- resting limit fills: 10 trades, 2 won, average +4.31%, total $+48.06
- run entries inside the buy zone: 20 trades, 5 won, average +2.12%, total $+115.40
- run entries on a bounce (touched the zone, back above it): 4 trades, 1 won, average -1.74%, total $-11.25
- support tested 3+ times: 26 trades, 6 won, average +1.78%, total $+60.18
- support tested twice: 8 trades, 2 won, average +4.03%, total $+92.03

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.85% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.16% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-27 14:50 | HIMX | bounce | 12.46 | +0.10 / -0.17 | 3.73 | 2026-07-29 10:25 | 11.52 | stop | -7.63% | +0.30 / -1.05 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.61% | +3.02 / -0.22 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:35 | APLD | buy zone | 24.2 | +0.07 / -1.00 | 4.12 | 2026-08-03 10:50 | 29.64 | target | +22.46% | +2.50 / -0.53 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.35% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.54% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-28 9:50 | IONQ | buy zone | 40.51 | -0.27 / -0.71 | 3.44 | 2026-09-01 9:30 | 37.85 | stop | -6.57% | +0.07 / -1.03 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.32% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.52% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.61% | +1.65 / -0.71 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.93 | 11.57 | 15.81 | 14.85 | +14.89% |
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| UMAC | 2026-09-16 | 21.43 | 20.98 | 26.12 | 22.36 | +4.34% |
| AXTI | 2026-09-30 | 75.92 | 70.99 | 89.31 | 84.06 | +10.72% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $998.12 | RCAT |
| 2026-07-16 | $970.38 | CRSP, IONQ, POET |
| 2026-07-17 | $963.64 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $960.43 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $982.58 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $972.48 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $983.03 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $953.44 | DUOL, HOOD, UMAC |
| 2026-07-27 | $990.12 | HIMX, HOOD, UMAC |
| 2026-07-28 | $982.88 | DELL, HIMX, UMAC |
| 2026-07-29 | $931.94 | AFRM, APLD, DELL, UMAC |
| 2026-07-30 | $1041.40 | AFRM, APLD, DELL, UMAC |
| 2026-07-31 | $1036.40 | AFRM, APLD, DELL, UMAC |
| 2026-08-03 | $1104.79 | AFRM, DELL, HIMX, UMAC |
| 2026-08-04 | $1187.33 | AFRM, AXTI, HIMX |
| 2026-08-05 | $1197.22 | AFRM, AXTI, HIMX, POET |
| 2026-08-06 | $1237.33 | AFRM, AXTI, HIMX, POET |
| 2026-08-07 | $1314.89 | AFRM, HIMX, MARA, POET |
| 2026-08-10 | $1291.95 | AFRM, HIMX, MARA, POET |
| 2026-08-11 | $1301.21 | AFRM, HIMX, MARA, POET |
| 2026-08-12 | $1298.85 | AFRM, HIMX, MARA, POET |
| 2026-08-13 | $1299.77 | AFRM, HIMX, ONDS, POET |
| 2026-08-14 | $1334.66 | AFRM, HIMX, ONDS, POET |
| 2026-08-17 | $1296.89 | AFRM, HIMX, POET, UPST |
| 2026-08-18 | $1249.30 | AFRM, HIMX, POET, UPST |
| 2026-08-19 | $1275.47 | AFRM, HIMX, POET, UPST |
| 2026-08-20 | $1232.77 | AFRM, HIMX, POET, UMAC |
| 2026-08-21 | $1256.08 | AFRM, HIMX, POET, UMAC |
| 2026-08-24 | $1205.66 | AFRM, CRSP, HIMX |
| 2026-08-25 | $1236.58 | AFRM, CRSP, HIMX, LUNR |
| 2026-08-26 | $1215.29 | AFRM, CRSP, HIMX, LUNR |
| 2026-08-27 | $1221.98 | AFRM, CRSP, HIMX, LUNR |
| 2026-08-28 | $1216.29 | CRSP, HIMX, IONQ |
| 2026-08-31 | $1221.87 | CRSP, HIMX, IONQ, SMCI |
| 2026-09-01 | $1205.79 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-02 | $1206.77 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-03 | $1210.60 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-04 | $1221.78 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-08 | $1215.56 | DUOL, HIMX, SMCI |
| 2026-09-09 | $1187.09 | HIMX, QBTS, RGTI, SMCI |
| 2026-09-10 | $1154.81 | HIMX, QBTS, SMCI |
| 2026-09-11 | $1184.38 | HIMX, QBTS, SMCI |
| 2026-09-14 | $1131.99 | AEHR, HIMX, SMCI |
| 2026-09-15 | $1110.98 | AEHR, GRAB, HIMX, SMCI |
| 2026-09-16 | $1130.42 | AEHR, HIMX, SMCI, UMAC |
| 2026-09-17 | $1201.29 | AEHR, HIMX, SMCI, UMAC |
| 2026-09-18 | $1193.12 | AEHR, HIMX, SMCI, UMAC |
| 2026-09-21 | $1235.32 | AEHR, HIMX, SMCI, UMAC |
| 2026-09-22 | $1246.94 | AXTI, HIMX, SMCI, UMAC |
| 2026-09-23 | $1213.84 | AXTI, HIMX, SMCI, UMAC |
| 2026-09-24 | $1241.11 | HIMS, HIMX, SMCI, UMAC |
| 2026-09-25 | $1263.53 | CRCL, HIMX, SMCI, UMAC |
| 2026-09-28 | $1239.27 | CRCL, HIMX, SMCI, UMAC |
| 2026-09-29 | $1238.90 | CRCL, HIMX, SMCI, UMAC |
| 2026-09-30 | $1236.78 | AXTI, HIMX, SMCI, UMAC |
| 2026-10-01 | $1230.61 | AXTI, HIMX, SMCI, UMAC |
| 2026-10-02 | $1269.35 | AXTI, HIMX, SMCI, UMAC |
| 2026-10-05 | $1259.07 | AXTI, HIMX, SMCI, UMAC |
| 2026-10-06 | $1259.36 | AXTI, HIMX, SMCI, UMAC |

## Size on the stop distance plus a 2% gap allowance: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1158.45 (+15.84%; realized $+43.69, open positions $+114.76); S&P 500 +3.63%, Nasdaq-100 +5.55%. 43 closed trades, 7 winners (16.3%), average trade -0.04%, average win 27.45%, average loss -5.38%, profit factor 1.13, worst drawdown -16.63%. Exits: target 7, stop 36. Resting orders filled: 8/14.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -2.66%, total $-31.96
- stopped on a later session: 31 trades, 0 won, average -5.82%, total $-311.46
- stopped at the open (gapped through the stop): 11 trades, 0 won, average -6.23%, total $-121.95
- never rose 0.5 ATR above the entry: 22 trades, 0 won, average -5.42%, total $-208.33
- crypto-linked: 4 trades, 0 won, average -5.09%, total $-38.88
- bought on a dip of 0.5+ ATR (any time): 31 trades, 5 won, average -0.64%, total $+36.54
- bought less than 0.25 ATR under the prior close: 5 trades, 1 won, average -3.41%, total $-18.76
- resting limit fills: 7 trades, 1 won, average +4.48%, total $+19.44
- run entries inside the buy zone: 31 trades, 5 won, average -0.51%, total $+40.09
- run entries on a bounce (touched the zone, back above it): 5 trades, 1 won, average -3.44%, total $-15.84
- support tested 3+ times: 32 trades, 5 won, average -0.47%, total $-24.20
- support tested twice: 10 trades, 2 won, average +2.11%, total $+81.26
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -7.89%, total $-13.37

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.85% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.16% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.79% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-24 15:20 | SMTC | bounce | 127.2 | -0.26 / -1.13 | 1.56 | 2026-07-27 10:30 | 117.6 | stop | -7.59% | +0.09 / -0.98 |
| 2026-07-27 10:35 | HIMX | buy zone | 12.23 | +0.10 / -0.42 | 5.4 | 2026-07-29 10:25 | 11.52 | stop | -5.84% | +0.56 / -0.80 |
| 2026-07-27 14:50 | NBIS | buy zone | 185.9 | +0.41 / -0.08 | 1.98 | 2026-07-28 9:50 | 166.9 | stop | -10.27% | +0.26 / -0.85 |
| 2026-07-28 9:50 | QBTS | buy zone | 17.34 | -0.61 / -1.62 | 3.89 | 2026-07-29 15:40 | 16.24 | stop | -6.43% | +0.66 / -0.82 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.61% | +3.02 / -0.22 |
| 2026-07-29 10:35 | APLD | buy zone | 24.2 | +0.07 / -1.00 | 4.12 | 2026-08-03 10:50 | 29.64 | target | +22.46% | +2.50 / -0.53 |
| 2026-07-29 15:50 | RIOT (crypto) | buy zone | 18.23 | -0.13 / -1.72 | 26.74 | 2026-08-19 10:10 | 17.91 | stop | -1.81% | +3.20 / -0.21 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-04 12:50 | SMR | bounce | 9.544 | +0.25 / +0.74 | 1.66 | 2026-08-18 15:10 | 8.566 | stop | -10.27% | +0.82 / -1.34 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.35% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-18 15:20 | CRWV | buy zone | 93.79 | -0.48 / -1.30 | 5.25 | 2026-08-19 10:10 | 89 | stop | -5.12% | +0.06 / -0.52 |
| 2026-08-19 10:20 | NBIS | buy zone | 217.8 | -0.59 / -1.12 | 14.82 | 2026-08-20 9:50 | 213.4 | stop | -2.01% | +0.51 / -0.19 |
| 2026-08-19 10:20 | AEHR | buy zone | 109.8 | +0.03 / -0.88 | 2.71 | 2026-08-24 9:30 | 95.71 | stop | -12.86% | +0.24 / -1.06 |
| 2026-08-20 9:50 | RXRX | buy zone | 3.332 | -0.58 / -0.97 | 40.55 | 2026-08-20 10:05 | 3.281 | stop | -1.52% | +0.00 / -0.24 |
| 2026-08-20 10:05 | UMAC | buy zone | 26.47 | +0.01 / -0.57 | 4.43 | 2026-08-24 9:30 | 24.81 | stop | -6.32% | +0.48 / -0.56 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:50 | POET | buy zone | 7.786 | -0.39 / -0.66 | 37.41 | 2026-08-24 10:00 | 7.699 | stop | -1.14% | +0.08 / -0.15 |
| 2026-08-24 9:50 | LUNR | buy zone | 16.87 | -0.45 / -0.91 | 6.02 | 2026-08-26 11:15 | 15.98 | stop | -5.29% | +0.19 / -0.56 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.43% | +0.77 / -0.63 |
| 2026-08-26 11:20 | NNE | buy zone | 18.57 | -0.05 / -0.54 | 10.22 | 2026-08-26 12:50 | 18.2 | stop | -2.00% | +0.00 / -0.30 |
| 2026-09-03 11:20 | GPUS | buy zone | 0.181 | +0.42 / -0.51 | 21.1 | 2026-09-24 9:35 | 0.1669 | stop | -7.89% | +0.74 / -0.40 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.32% | +0.37 / -0.79 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.51% | +0.64 / -0.85 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.61% | +1.65 / -0.71 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-24 9:50 | QUBT | buy zone | 8.918 | -0.68 / -0.53 | 27.49 | 2026-09-28 10:40 | 8.685 | stop | -2.64% | +0.97 / -0.57 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.76% | +0.07 / -0.70 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.93 | 11.57 | 15.81 | 14.85 | +14.89% |
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| AXTI | 2026-09-28 | 71.84 | 71.04 | 89.34 | 84.06 | +17.02% |
| RIOT | 2026-10-01 | 19.31 | 18.39 | 21.78 | 18.93 | -1.99% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $998.36 | RCAT |
| 2026-07-16 | $972.03 | CRSP, IONQ, POET |
| 2026-07-17 | $964.69 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $960.39 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $981.66 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $971.02 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $980.37 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $950.87 | DUOL, HOOD, SMTC, UMAC |
| 2026-07-27 | $988.64 | HIMX, HOOD, NBIS, UMAC |
| 2026-07-28 | $963.85 | DELL, HIMX, QBTS, UMAC |
| 2026-07-29 | $906.99 | APLD, DELL, RIOT, UMAC |
| 2026-07-30 | $1018.69 | APLD, DELL, RIOT, UMAC |
| 2026-07-31 | $1008.87 | APLD, DELL, RIOT, UMAC |
| 2026-08-03 | $1064.75 | DELL, HIMX, RIOT, UMAC |
| 2026-08-04 | $1141.45 | AXTI, HIMX, RIOT, SMR |
| 2026-08-05 | $1146.69 | AXTI, HIMX, RIOT, SMR |
| 2026-08-06 | $1178.18 | AXTI, HIMX, RIOT, SMR |
| 2026-08-07 | $1247.72 | HIMX, MARA, RIOT, SMR |
| 2026-08-10 | $1226.25 | HIMX, MARA, RIOT, SMR |
| 2026-08-11 | $1242.10 | HIMX, MARA, RIOT, SMR |
| 2026-08-12 | $1240.14 | HIMX, MARA, RIOT, SMR |
| 2026-08-13 | $1218.92 | HIMX, ONDS, RIOT, SMR |
| 2026-08-14 | $1226.61 | HIMX, ONDS, RIOT, SMR |
| 2026-08-17 | $1216.20 | HIMX, RIOT, SMR, UPST |
| 2026-08-18 | $1186.34 | CRWV, HIMX, RIOT, UPST |
| 2026-08-19 | $1185.69 | AEHR, HIMX, NBIS, UPST |
| 2026-08-20 | $1140.57 | AEHR, HIMX, UMAC |
| 2026-08-21 | $1140.59 | AEHR, HIMX, UMAC |
| 2026-08-24 | $1111.33 | CRSP, HIMX, LUNR |
| 2026-08-25 | $1132.32 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-26 | $1111.39 | CRSP, HIMX, SOUN |
| 2026-08-27 | $1122.26 | CRSP, HIMX, SOUN |
| 2026-08-28 | $1106.13 | CRSP, HIMX, SOUN |
| 2026-08-31 | $1112.56 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-01 | $1092.91 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-02 | $1093.67 | CRSP, HIMX, SMCI, SOUN |
| 2026-09-03 | $1103.81 | CRSP, GPUS, HIMX, SMCI |
| 2026-09-04 | $1114.04 | CRSP, GPUS, HIMX, SMCI |
| 2026-09-08 | $1117.25 | DUOL, GPUS, HIMX, SMCI |
| 2026-09-09 | $1107.49 | GPUS, HIMX, QBTS, SMCI |
| 2026-09-10 | $1078.35 | GPUS, HIMX, QBTS, SMCI |
| 2026-09-11 | $1109.15 | GPUS, HIMX, QBTS, SMCI |
| 2026-09-14 | $1065.24 | AEHR, GPUS, HIMX, SMCI |
| 2026-09-15 | $1040.17 | AEHR, GPUS, HIMX, SMCI |
| 2026-09-16 | $1044.10 | AEHR, GPUS, HIMX, SMCI |
| 2026-09-17 | $1089.87 | AEHR, GPUS, HIMX, SMCI |
| 2026-09-18 | $1090.94 | AEHR, GPUS, HIMX, SMCI |
| 2026-09-21 | $1129.13 | AEHR, GPUS, HIMX, SMCI |
| 2026-09-22 | $1131.88 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-23 | $1105.33 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-24 | $1115.27 | HIMS, HIMX, QUBT, SMCI |
| 2026-09-25 | $1133.66 | CRCL, HIMX, QUBT, SMCI |
| 2026-09-28 | $1116.62 | AXTI, CRCL, HIMX, SMCI |
| 2026-09-29 | $1125.61 | AXTI, CRCL, HIMX, SMCI |
| 2026-09-30 | $1116.52 | AXTI, BTDR, HIMX, SMCI |
| 2026-10-01 | $1141.12 | AXTI, HIMX, RIOT, SMCI |
| 2026-10-02 | $1178.58 | AXTI, HIMX, RIOT, SMCI |
| 2026-10-05 | $1169.13 | AXTI, HIMX, RIOT, SMCI |
| 2026-10-06 | $1158.45 | AXTI, HIMX, RIOT, SMCI |

## No entry within 0.3 ATR of its stop: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1032.97 (+3.30%; realized $-50.63, open positions $+83.60); S&P 500 +3.63%, Nasdaq-100 +5.55%. 43 closed trades, 9 winners (20.9%), average trade 0.43%, average win 21.64%, average loss -5.18%, profit factor 0.86, worst drawdown -13.08%. Exits: target 9, stop 34. Resting orders filled: 18/28.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -5.85%, total $-74.19
- stopped on a later session: 27 trades, 0 won, average -5.00%, total $-278.54
- stopped at the open (gapped through the stop): 14 trades, 0 won, average -5.22%, total $-156.14
- never rose 0.5 ATR above the entry: 23 trades, 0 won, average -5.31%, total $-255.26
- crypto-linked: 4 trades, 1 won, average -0.43%, total $+6.06
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-10.97
- bought on a dip of 0.5+ ATR (any time): 25 trades, 6 won, average +0.31%, total $-56.82
- bought less than 0.25 ATR under the prior close: 8 trades, 3 won, average +7.50%, total $+104.48
- resting limit fills: 16 trades, 3 won, average +1.25%, total $+15.59
- run entries inside the buy zone: 23 trades, 5 won, average +0.21%, total $-65.30
- run entries on a bounce (touched the zone, back above it): 4 trades, 1 won, average -1.53%, total $-0.92
- support tested 3+ times: 31 trades, 8 won, average +2.26%, total $+52.68
- support tested twice: 10 trades, 1 won, average -3.20%, total $-71.01
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-32.30

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-17 9:50 | UMAC | limit | 16.35 | -0.25 / -0.12 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +60.35% | +4.22 / -0.03 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.56% | +3.02 / -0.22 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-08-04 9:50 | LEU | buy zone | 187.1 | +0.44 / +0.20 | 2.04 | 2026-08-06 12:55 | 177.1 | stop | -5.37% | +1.34 / -0.85 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.00% | +3.69 / -0.02 |
| 2026-08-11 9:40 | RKLB | limit | 78.1 | -0.63 / -0.32 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -3.33% | +0.00 / -0.44 |
| 2026-08-11 9:50 | TEM | buy zone | 53.57 | -0.26 / -0.46 | 6.3 | 2026-08-14 13:50 | 52.13 | stop | -2.69% | +1.07 / -0.45 |
| 2026-08-14 13:50 | DUOL | buy zone | 134 | -0.02 / -1.09 | 8.94 | 2026-08-17 9:30 | 131 | stop | -2.28% | +0.16 / -0.44 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.44% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.54% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.15% | +0.45 / -1.38 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.86% | +0.00 / -0.80 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-02 11:20 | WULF (crypto) | buy zone | 14.45 | -0.17 / -0.17 | 4.29 | 2026-09-08 9:50 | 16.98 | target | +17.54% | +2.27 / -0.05 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.53% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.60% | +1.65 / -0.71 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | DUOL | bounce | 147.9 | -0.45 / -0.77 | 2.4 | 2026-09-28 9:30 | 140.6 | stop | -4.97% | +0.65 / -1.23 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.78% | +0.07 / -0.70 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 138 | +5.75% |
| AXTI | 2026-09-28 | 74.11 | 71.04 | 89.34 | 84.06 | +13.43% |
| RIOT | 2026-10-01 | 19.31 | 18.39 | 21.78 | 18.93 | -1.99% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $959.63 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $957.77 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $980.96 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $971.69 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $982.87 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $953.44 | DUOL, HOOD, UMAC |
| 2026-07-27 | $992.87 | HOOD, UMAC |
| 2026-07-28 | $964.28 | DELL, UMAC |
| 2026-07-29 | $934.58 | AFRM, DELL, PCVX, UMAC |
| 2026-07-30 | $996.75 | AFRM, DELL, PCVX, UMAC |
| 2026-07-31 | $989.13 | AFRM, DELL, PCVX, UMAC |
| 2026-08-03 | $1023.45 | AFRM, DELL, PCVX, UMAC |
| 2026-08-04 | $1076.03 | AFRM, LEU, PCVX |
| 2026-08-05 | $1078.84 | AFRM, LEU, PCVX, POET |
| 2026-08-06 | $1088.85 | AFRM, NOW, POET |
| 2026-08-07 | $1100.33 | AFRM, NOW, POET |
| 2026-08-10 | $1090.98 | AFRM, NOW, POET |
| 2026-08-11 | $1095.49 | AFRM, NOW, POET, TEM |
| 2026-08-12 | $1087.77 | AFRM, NOW, POET, TEM |
| 2026-08-13 | $1105.85 | AFRM, NOW, POET, TEM |
| 2026-08-14 | $1115.50 | AFRM, DUOL, NOW, POET |
| 2026-08-17 | $1089.83 | AFRM, NOW, POET, UPST |
| 2026-08-18 | $1052.48 | AFRM, NOW, POET, UPST |
| 2026-08-19 | $1078.28 | AFRM, NOW, POET, UPST |
| 2026-08-20 | $1047.87 | AFRM, NOW, POET, UMAC |
| 2026-08-21 | $1067.67 | AFRM, NOW, POET, UMAC |
| 2026-08-24 | $1023.37 | AFRM, CRSP, NOW |
| 2026-08-25 | $1044.85 | AFRM, CRSP, LUNR, NOW |
| 2026-08-26 | $1025.63 | AFRM, CRSP, LUNR, NOW |
| 2026-08-27 | $1040.37 | AFRM, CRSP, IONQ, LUNR |
| 2026-08-28 | $1025.16 | CRSP, IONQ |
| 2026-08-31 | $1030.20 | CRSP, IONQ, SMCI |
| 2026-09-01 | $1003.78 | CRSP, SMCI, SOUN |
| 2026-09-02 | $993.04 | CRSP, SMCI, SOUN, WULF |
| 2026-09-03 | $1014.79 | CRSP, SMCI, SOUN, WULF |
| 2026-09-04 | $1028.11 | CRSP, SMCI, SOUN, WULF |
| 2026-09-08 | $1028.37 | DUOL, SMCI |
| 2026-09-09 | $1005.97 | QBTS, RGTI, SMCI, SMR |
| 2026-09-10 | $975.17 | QBTS, SMCI |
| 2026-09-11 | $998.98 | NOW, QBTS, SMCI |
| 2026-09-14 | $985.11 | AEHR, NOW, SMCI |
| 2026-09-15 | $969.64 | AEHR, GRAB, NOW, SMCI |
| 2026-09-16 | $975.26 | AEHR, DUOL, NOW, SMCI |
| 2026-09-17 | $1006.31 | AEHR, DUOL, NOW, SMCI |
| 2026-09-18 | $993.13 | AEHR, DUOL, NOW, SMCI |
| 2026-09-21 | $1021.81 | AEHR, DUOL, NOW, SMCI |
| 2026-09-22 | $1029.58 | AXTI, DUOL, NOW, SMCI |
| 2026-09-23 | $1020.35 | AXTI, DUOL, NOW, SMCI |
| 2026-09-24 | $1020.40 | DUOL, HIMS, NOW, SMCI |
| 2026-09-25 | $1028.97 | CRCL, DUOL, NOW, SMCI |
| 2026-09-28 | $1000.21 | AXTI, CRCL, NOW, SMCI |
| 2026-09-29 | $997.27 | AXTI, CRCL, NOW, SMCI |
| 2026-09-30 | $999.66 | AXTI, BTDR, NOW, SMCI |
| 2026-10-01 | $1023.60 | AXTI, NOW, RIOT, SMCI |
| 2026-10-02 | $1040.32 | AXTI, NOW, RIOT, SMCI |
| 2026-10-05 | $1037.53 | AXTI, NOW, RIOT, SMCI |
| 2026-10-06 | $1032.97 | AXTI, NOW, RIOT, SMCI |

## No entry within 0.45 ATR of its stop: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1030.58 (+3.06%; realized $-53.94, open positions $+84.52); S&P 500 +3.63%, Nasdaq-100 +5.55%. 43 closed trades, 9 winners (20.9%), average trade -0.15%, average win 21.07%, average loss -5.76%, profit factor 0.85, worst drawdown -17.13%. Exits: target 9, stop 34. Resting orders filled: 15/23.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.48%, total $-57.29
- stopped on a later session: 29 trades, 0 won, average -5.64%, total $-310.42
- stopped at the open (gapped through the stop): 14 trades, 0 won, average -6.18%, total $-177.23
- never rose 0.5 ATR above the entry: 21 trades, 0 won, average -6.08%, total $-249.11
- crypto-linked: 5 trades, 1 won, average -1.34%, total $-13.10
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-10.92
- bought on a dip of 0.5+ ATR (any time): 28 trades, 6 won, average -0.79%, total $-80.44
- bought less than 0.25 ATR under the prior close: 8 trades, 3 won, average +7.09%, total $+106.63
- resting limit fills: 14 trades, 3 won, average +1.94%, total $+35.68
- run entries inside the buy zone: 25 trades, 5 won, average -1.10%, total $-87.69
- run entries on a bounce (touched the zone, back above it): 4 trades, 1 won, average -1.53%, total $-1.93
- support tested 3+ times: 29 trades, 8 won, average +2.04%, total $+53.53
- support tested twice: 11 trades, 1 won, average -3.27%, total $-59.93
- radar keeps (GPUS, IREN, BTDR) without a tested support: 3 trades, 0 won, average -9.89%, total $-47.54

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-17 10:00 | UMAC | limit | 16.64 | -0.25 / -0.00 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +57.56% | +4.10 / -0.05 |
| 2026-07-21 12:35 | GRAB | buy zone | 3.578 | -0.03 / -0.26 | 5.01 | 2026-07-22 9:30 | 3.468 | stop | -3.07% | +0.00 / -0.66 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.56% | +3.02 / -0.22 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-08-04 9:50 | LEU | buy zone | 187.1 | +0.44 / +0.20 | 2.04 | 2026-08-06 12:55 | 177.1 | stop | -5.37% | +1.34 / -0.85 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.00% | +3.69 / -0.02 |
| 2026-08-11 10:10 | RKLB | limit | 78.29 | -0.63 / -0.29 | 19.47 | 2026-08-19 9:30 | 75.5 | stop | -3.57% | +1.21 / -0.47 |
| 2026-08-19 9:50 | UMAC | buy zone | 27.67 | -0.15 / -0.90 | 2.13 | 2026-08-24 9:30 | 24.8 | stop | -10.39% | +0.45 / -0.93 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-24 10:05 | LUNR | buy zone | 16.85 | -0.45 / -0.92 | 6.24 | 2026-08-26 11:15 | 15.98 | stop | -5.18% | +0.21 / -0.54 |
| 2026-08-26 11:20 | BTBT (crypto) | buy zone | 1.507 | -0.35 / -0.51 | 8.12 | 2026-08-28 14:35 | 1.414 | stop | -6.22% | +1.10 / -0.61 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.15% | +0.45 / -1.38 |
| 2026-08-28 9:50 | MSTR (crypto) | buy zone | 135.6 | -0.44 / -0.24 | 2.94 | 2026-08-28 11:40 | 129.8 | stop | -4.30% | +0.05 / -0.81 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-02 11:20 | BTDR (crypto) | buy zone | 10.24 | -0.01 / -0.12 | 1.74 | 2026-09-03 10:35 | 11.79 | target | +15.19% | +1.69 / -0.04 |
| 2026-09-03 10:35 | GPUS | buy zone | 0.186 | +0.42 / -0.38 | 14.74 | 2026-09-24 9:35 | 0.1669 | stop | -10.38% | +0.61 / -0.54 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.52% | +0.64 / -0.85 |
| 2026-09-10 9:50 | NBIS | buy zone | 230.1 | -0.61 / -0.75 | 5.38 | 2026-09-14 9:30 | 204.9 | stop | -10.98% | +0.34 / -1.93 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.61% | +1.65 / -0.71 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | DUOL | bounce | 147.9 | -0.45 / -0.77 | 2.4 | 2026-09-28 9:30 | 140.6 | stop | -4.97% | +0.65 / -1.23 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-24 9:50 | QUBT | buy zone | 8.918 | -0.68 / -0.53 | 27.49 | 2026-09-28 10:40 | 8.685 | stop | -2.68% | +0.97 / -0.57 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-09-28 10:50 | BBAI | buy zone | 2.724 | -0.41 / -0.63 | 2.77 | 2026-10-02 11:20 | 2.614 | stop | -4.03% | +1.11 / -0.86 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.77% | +0.07 / -0.70 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| AXTI | 2026-09-28 | 74.11 | 71.04 | 89.34 | 84.06 | +13.43% |
| RIOT | 2026-10-01 | 19.31 | 18.39 | 21.78 | 18.93 | -1.99% |
| SMR | 2026-10-02 | 7.785 | 7.371 | 8.756 | 8.02 | +3.01% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $956.53 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $954.58 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $976.73 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $967.46 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $978.32 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $949.27 | DUOL, HOOD, UMAC |
| 2026-07-27 | $988.37 | HOOD, UMAC |
| 2026-07-28 | $960.00 | DELL, UMAC |
| 2026-07-29 | $930.73 | AFRM, DELL, PCVX, UMAC |
| 2026-07-30 | $992.30 | AFRM, DELL, PCVX, UMAC |
| 2026-07-31 | $984.62 | AFRM, DELL, PCVX, UMAC |
| 2026-08-03 | $1018.60 | AFRM, DELL, PCVX, UMAC |
| 2026-08-04 | $1070.64 | AFRM, LEU, PCVX |
| 2026-08-05 | $1073.43 | AFRM, LEU, PCVX, POET |
| 2026-08-06 | $1083.24 | AFRM, NOW, POET |
| 2026-08-07 | $1094.53 | AFRM, NOW, POET |
| 2026-08-10 | $1085.19 | AFRM, NOW, POET |
| 2026-08-11 | $1096.18 | AFRM, NOW, POET, RKLB |
| 2026-08-12 | $1096.87 | AFRM, NOW, POET, RKLB |
| 2026-08-13 | $1112.41 | AFRM, NOW, POET, RKLB |
| 2026-08-14 | $1133.58 | AFRM, NOW, POET, RKLB |
| 2026-08-17 | $1118.02 | AFRM, NOW, POET, RKLB |
| 2026-08-18 | $1075.20 | AFRM, NOW, POET, RKLB |
| 2026-08-19 | $1081.18 | AFRM, NOW, POET, UMAC |
| 2026-08-20 | $1055.77 | AFRM, NOW, POET, UMAC |
| 2026-08-21 | $1069.56 | AFRM, NOW, POET, UMAC |
| 2026-08-24 | $1035.73 | AFRM, CRSP, LUNR, NOW |
| 2026-08-25 | $1056.68 | AFRM, CRSP, LUNR, NOW |
| 2026-08-26 | $1050.42 | AFRM, BTBT, CRSP, NOW |
| 2026-08-27 | $1068.92 | AFRM, BTBT, CRSP, IONQ |
| 2026-08-28 | $1042.21 | CRSP, IONQ |
| 2026-08-31 | $1046.46 | CRSP, IONQ, SMCI |
| 2026-09-01 | $1019.80 | CRSP, SMCI, SOUN |
| 2026-09-02 | $1013.07 | BTDR, CRSP, SMCI, SOUN |
| 2026-09-03 | $1037.05 | CRSP, GPUS, SMCI, SOUN |
| 2026-09-04 | $1046.12 | CRSP, GPUS, SMCI, SOUN |
| 2026-09-08 | $1040.12 | DUOL, GPUS, SMCI |
| 2026-09-09 | $1025.19 | GPUS, QBTS, RGTI, SMCI |
| 2026-09-10 | $994.02 | GPUS, NBIS, QBTS, SMCI |
| 2026-09-11 | $1011.81 | GPUS, NBIS, QBTS, SMCI |
| 2026-09-14 | $964.01 | AEHR, GPUS, SMCI |
| 2026-09-15 | $939.42 | AEHR, GPUS, GRAB, SMCI |
| 2026-09-16 | $944.91 | AEHR, DUOL, GPUS, SMCI |
| 2026-09-17 | $987.09 | AEHR, DUOL, GPUS, SMCI |
| 2026-09-18 | $983.64 | AEHR, DUOL, GPUS, SMCI |
| 2026-09-21 | $1019.78 | AEHR, DUOL, GPUS, SMCI |
| 2026-09-22 | $1024.12 | AXTI, DUOL, GPUS, SMCI |
| 2026-09-23 | $1000.37 | AXTI, DUOL, GPUS, SMCI |
| 2026-09-24 | $1010.60 | DUOL, HIMS, QUBT, SMCI |
| 2026-09-25 | $1024.46 | CRCL, DUOL, QUBT, SMCI |
| 2026-09-28 | $998.62 | AXTI, BBAI, CRCL, SMCI |
| 2026-09-29 | $1002.78 | AXTI, BBAI, CRCL, SMCI |
| 2026-09-30 | $996.17 | AXTI, BBAI, BTDR, SMCI |
| 2026-10-01 | $1022.25 | AXTI, BBAI, RIOT, SMCI |
| 2026-10-02 | $1044.25 | AXTI, RIOT, SMCI, SMR |
| 2026-10-05 | $1037.91 | AXTI, RIOT, SMCI, SMR |
| 2026-10-06 | $1030.58 | AXTI, RIOT, SMCI, SMR |

## No entry while down 1.0+ ATR on the day: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1108.38 (+10.84%; realized $+51.96, open positions $+56.42); S&P 500 +3.63%, Nasdaq-100 +5.55%. 37 closed trades, 10 winners (27.0%), average trade 2.3%, average win 22.89%, average loss -5.32%, profit factor 1.17, worst drawdown -11.38%. Exits: target 10, stop 27. Resting orders filled: 10/20.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -5.22%, total $-65.86
- stopped on a later session: 22 trades, 0 won, average -5.35%, total $-235.46
- stopped at the open (gapped through the stop): 14 trades, 0 won, average -5.49%, total $-146.29
- never rose 0.5 ATR above the entry: 18 trades, 0 won, average -5.27%, total $-224.40
- crypto-linked: 4 trades, 1 won, average -0.47%, total $-42.54
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-11.02
- bought on a dip of 0.5+ ATR (any time): 21 trades, 5 won, average -0.05%, total $+21.02
- bought less than 0.25 ATR under the prior close: 6 trades, 3 won, average +4.97%, total $+15.65
- resting limit fills: 10 trades, 3 won, average +6.14%, total $+101.77
- run entries inside the buy zone: 20 trades, 5 won, average +1.36%, total $-30.81
- run entries on a bounce (touched the zone, back above it): 7 trades, 2 won, average -0.48%, total $-19.00
- support tested 3+ times: 28 trades, 9 won, average +3.25%, total $+128.26
- support tested twice: 8 trades, 1 won, average +0.23%, total $-56.67
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -7.79%, total $-19.63

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-28 9:50 | UPST | buy zone | 26.35 | +0.00 / -0.68 | 2.61 | 2026-08-03 9:50 | 29.26 | target | +10.98% | +1.75 / -0.27 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-08-04 12:50 | AXTI | buy zone | 65.41 | -0.47 / -0.36 | 3.75 | 2026-08-07 15:50 | 89.24 | target | +36.38% | +2.68 / -0.31 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.03% | +3.69 / -0.02 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.36% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.56% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.16% | +0.45 / -1.38 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.85% | +0.00 / -0.80 |
| 2026-08-28 14:35 | RCAT | buy zone | 8.507 | -0.16 / -0.97 | 5.32 | 2026-09-02 9:30 | 8.077 | stop | -5.08% | +0.59 / -0.57 |
| 2026-09-01 9:50 | BMNR (crypto) | buy zone | 24.06 | -0.62 / -0.84 | 2.1 | 2026-09-02 9:30 | 22.89 | stop | -4.89% | +0.24 / -0.81 |
| 2026-09-02 9:50 | GPUS | buy zone | 0.224 | -0.42 / -0.43 | 14.43 | 2026-09-02 11:10 | 0.2067 | stop | -7.79% | +0.39 / -0.53 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.05% | +2.33 / -0.07 |
| 2026-09-08 9:50 | RXRX | bounce | 3.563 | -0.23 / -0.31 | 2.26 | 2026-09-09 10:20 | 3.327 | stop | -6.63% | +0.00 / -1.06 |
| 2026-09-08 9:50 | SMTC | bounce | 151.7 | +0.38 / +0.35 | 1.72 | 2026-09-17 9:50 | 177.2 | target | +16.70% | +2.33 / -0.43 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.51% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-16 15:20 | DUOL | bounce | 147.9 | -0.45 / -0.77 | 2.4 | 2026-09-28 9:30 | 140.6 | stop | -4.95% | +0.65 / -1.23 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-10-02 10:05 | 91.76 | target | +14.93% | +2.37 / -0.29 |
| 2026-10-02 10:05 | PATH | buy zone | 13.25 | +0.14 / -0.10 | 13.84 | 2026-10-05 11:00 | 12.81 | stop | -3.35% | +0.00 / -0.66 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.28 | 11.57 | 15.81 | 14.85 | +20.88% |
| UMAC | 2026-09-14 | 22.33 | 20.89 | 26.08 | 22.36 | +0.13% |
| AXTI | 2026-09-28 | 74.11 | 71.04 | 89.34 | 84.06 | +13.43% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 17.77 | 14.97 | +1.25% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $962.97 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $961.19 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $984.78 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $975.53 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $987.05 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $957.22 | DUOL, HOOD, UMAC |
| 2026-07-27 | $996.99 | HOOD, UMAC |
| 2026-07-28 | $967.64 | UMAC, UPST |
| 2026-07-29 | $938.00 | AFRM, PCVX, UMAC, UPST |
| 2026-07-30 | $998.04 | AFRM, PCVX, UMAC, UPST |
| 2026-07-31 | $990.96 | AFRM, PCVX, UMAC, UPST |
| 2026-08-03 | $1035.14 | AFRM, HIMX, PCVX, UMAC |
| 2026-08-04 | $1109.22 | AFRM, AXTI, HIMX, PCVX |
| 2026-08-05 | $1102.31 | AFRM, AXTI, HIMX, PCVX |
| 2026-08-06 | $1130.70 | AFRM, AXTI, HIMX, NOW |
| 2026-08-07 | $1170.43 | AFRM, HIMX, MARA, NOW |
| 2026-08-10 | $1166.81 | AFRM, HIMX, MARA, NOW |
| 2026-08-11 | $1178.79 | AFRM, HIMX, MARA, NOW |
| 2026-08-12 | $1162.11 | AFRM, HIMX, MARA, NOW |
| 2026-08-13 | $1165.81 | AFRM, HIMX, NOW, ONDS |
| 2026-08-14 | $1171.65 | AFRM, HIMX, NOW, ONDS |
| 2026-08-17 | $1140.32 | AFRM, HIMX, NOW, UPST |
| 2026-08-18 | $1116.71 | AFRM, HIMX, NOW, UPST |
| 2026-08-19 | $1151.17 | AFRM, HIMX, NOW, UPST |
| 2026-08-20 | $1127.43 | AFRM, HIMX, NOW, UMAC |
| 2026-08-21 | $1137.53 | AFRM, HIMX, NOW, UMAC |
| 2026-08-24 | $1122.41 | AFRM, CRSP, HIMX, NOW |
| 2026-08-25 | $1142.68 | AFRM, CRSP, HIMX, NOW |
| 2026-08-26 | $1131.38 | AFRM, CRSP, HIMX, NOW |
| 2026-08-27 | $1171.33 | AFRM, CRSP, HIMX, IONQ |
| 2026-08-28 | $1160.14 | CRSP, HIMX, IONQ, RCAT |
| 2026-08-31 | $1159.95 | CRSP, HIMX, IONQ, RCAT |
| 2026-09-01 | $1139.37 | BMNR, CRSP, HIMX, RCAT |
| 2026-09-02 | $1115.91 | CRSP, HIMX, WULF |
| 2026-09-03 | $1120.54 | CRSP, HIMX, WULF |
| 2026-09-04 | $1121.13 | CRSP, HIMX, WULF |
| 2026-09-08 | $1117.60 | HIMX, RXRX, SMTC |
| 2026-09-09 | $1100.65 | HIMX, QBTS, RGTI, SMTC |
| 2026-09-10 | $1077.62 | HIMX, QBTS, SMTC |
| 2026-09-11 | $1099.22 | HIMX, QBTS, SMTC |
| 2026-09-14 | $1066.22 | HIMX, SMTC, UMAC |
| 2026-09-15 | $1059.28 | GRAB, HIMX, SMTC, UMAC |
| 2026-09-16 | $1044.59 | DUOL, HIMX, SMTC, UMAC |
| 2026-09-17 | $1076.91 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-18 | $1071.27 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-21 | $1121.02 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-22 | $1121.74 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-23 | $1096.09 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-24 | $1120.50 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-25 | $1112.03 | CRWV, DUOL, HIMX, UMAC |
| 2026-09-28 | $1088.25 | AXTI, CRWV, HIMX, UMAC |
| 2026-09-29 | $1106.39 | AXTI, CRWV, HIMX, UMAC |
| 2026-09-30 | $1104.28 | AXTI, CRWV, HIMX, UMAC |
| 2026-10-01 | $1088.01 | AXTI, CRWV, HIMX, UMAC |
| 2026-10-02 | $1119.03 | AXTI, HIMX, PATH, UMAC |
| 2026-10-05 | $1097.49 | AXTI, HIMX, UMAC, WULF |
| 2026-10-06 | $1108.38 | AXTI, HIMX, UMAC, WULF |

## No entry while down 1.5+ ATR on the day: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1117.07 (+11.71%; realized $+59.80, open positions $+57.27); S&P 500 +3.63%, Nasdaq-100 +5.55%. 41 closed trades, 9 winners (22.0%), average trade 1.27%, average win 23.33%, average loss -4.93%, profit factor 1.17, worst drawdown -12.74%. Exits: target 9, stop 32. Resting orders filled: 10/18.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -4.58%, total $-47.44
- stopped on a later session: 28 trades, 0 won, average -4.99%, total $-307.26
- stopped at the open (gapped through the stop): 13 trades, 0 won, average -5.38%, total $-159.33
- never rose 0.5 ATR above the entry: 19 trades, 0 won, average -5.11%, total $-231.89
- crypto-linked: 6 trades, 1 won, average -1.49%, total $-41.07
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-11.02
- bought on a dip of 0.5+ ATR (any time): 26 trades, 5 won, average -0.52%, total $-25.08
- bought less than 0.25 ATR under the prior close: 6 trades, 2 won, average +0.13%, total $-4.87
- resting limit fills: 10 trades, 3 won, average +6.31%, total $+106.29
- run entries inside the buy zone: 22 trades, 3 won, average -0.78%, total $-49.30
- run entries on a bounce (touched the zone, back above it): 9 trades, 3 won, average +0.67%, total $+2.81
- support tested 3+ times: 32 trades, 8 won, average +1.76%, total $+95.26
- support tested twice: 9 trades, 1 won, average -0.49%, total $-35.46

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-28 9:50 | IONQ | buy zone | 32.35 | -0.69 / -1.43 | 21.14 | 2026-07-29 12:15 | 32 | stop | -1.14% | +0.78 / -0.14 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-07-29 12:20 | HUT (crypto) | bounce | 89.1 | -0.11 / -1.18 | 1.64 | 2026-07-30 11:50 | 106.8 | target | +19.86% | +1.75 / -0.19 |
| 2026-07-30 11:50 | UPST | buy zone | 26.28 | -0.06 / -0.20 | 2.72 | 2026-08-03 11:50 | 29.29 | target | +11.41% | +1.95 / -0.05 |
| 2026-08-04 12:50 | AXTI | buy zone | 65.41 | -0.47 / -0.36 | 3.75 | 2026-08-07 15:50 | 89.24 | target | +36.41% | +2.68 / -0.31 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.03% | +3.69 / -0.02 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.35% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.54% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.14% | +0.45 / -1.38 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.85% | +0.00 / -0.80 |
| 2026-08-28 14:35 | COIN (crypto) | buy zone | 176.6 | -0.46 / -1.39 | 4.79 | 2026-09-15 14:45 | 169.6 | stop | -4.03% | +1.90 / -0.84 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.32% | +0.37 / -0.79 |
| 2026-09-08 10:20 | RXRX | buy zone | 3.543 | -0.23 / -0.40 | 2.62 | 2026-09-09 10:20 | 3.327 | stop | -6.10% | +0.00 / -0.97 |
| 2026-09-09 10:20 | ASTS | buy zone | 63.57 | +0.11 / -0.64 | 4.46 | 2026-09-10 9:30 | 60.57 | stop | -4.73% | +0.24 / -0.78 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.51% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-21 10:20 | 41.33 | target | +10.43% | +1.82 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-15 14:50 | BULL | bounce | 8.592 | -0.35 / -0.86 | 2.43 | 2026-09-16 10:55 | 8.055 | stop | -6.27% | +0.23 / -1.03 |
| 2026-09-16 11:05 | DUOL | bounce | 147.9 | -0.45 / -0.76 | 2.37 | 2026-09-28 9:30 | 140.6 | stop | -5.01% | +0.64 / -1.24 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-21 10:20 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-24 13:40 | 9.158 | stop | -4.46% | +1.01 / -0.98 |
| 2026-09-24 13:50 | BTBT (crypto) | buy zone | 1.784 | -0.35 / +0.11 | 5.6 | 2026-09-29 12:05 | 1.664 | stop | -6.75% | +0.28 / -0.88 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.95% | +0.40 / -0.50 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.82 | 11.57 | 15.81 | 14.85 | +15.87% |
| AXTI | 2026-09-28 | 74.11 | 71.04 | 89.34 | 84.06 | +13.43% |
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 18.93 | -3.76% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 15.06 | +6.52% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $962.97 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $961.19 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $984.78 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $975.53 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $987.05 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $957.22 | DUOL, HOOD, UMAC |
| 2026-07-27 | $996.99 | HOOD, UMAC |
| 2026-07-28 | $967.34 | IONQ, UMAC |
| 2026-07-29 | $936.03 | AFRM, HUT, PCVX, UMAC |
| 2026-07-30 | $1024.72 | AFRM, PCVX, UMAC, UPST |
| 2026-07-31 | $1019.37 | AFRM, PCVX, UMAC, UPST |
| 2026-08-03 | $1061.73 | AFRM, HIMX, PCVX, UMAC |
| 2026-08-04 | $1124.69 | AFRM, AXTI, HIMX, PCVX |
| 2026-08-05 | $1130.62 | AFRM, AXTI, HIMX, PCVX |
| 2026-08-06 | $1168.68 | AFRM, AXTI, HIMX, NOW |
| 2026-08-07 | $1229.36 | AFRM, HIMX, MARA, NOW |
| 2026-08-10 | $1224.52 | AFRM, HIMX, MARA, NOW |
| 2026-08-11 | $1234.67 | AFRM, HIMX, MARA, NOW |
| 2026-08-12 | $1216.96 | AFRM, HIMX, MARA, NOW |
| 2026-08-13 | $1219.01 | AFRM, HIMX, NOW, ONDS |
| 2026-08-14 | $1225.86 | AFRM, HIMX, NOW, ONDS |
| 2026-08-17 | $1180.51 | AFRM, HIMX, NOW, UPST |
| 2026-08-18 | $1164.89 | AFRM, HIMX, NOW, UPST |
| 2026-08-19 | $1203.82 | AFRM, HIMX, NOW, UPST |
| 2026-08-20 | $1179.91 | AFRM, HIMX, NOW, UMAC |
| 2026-08-21 | $1197.02 | AFRM, HIMX, NOW, UMAC |
| 2026-08-24 | $1170.10 | AFRM, CRSP, HIMX, NOW |
| 2026-08-25 | $1189.02 | AFRM, CRSP, HIMX, NOW |
| 2026-08-26 | $1176.12 | AFRM, CRSP, HIMX, NOW |
| 2026-08-27 | $1217.69 | AFRM, CRSP, HIMX, IONQ |
| 2026-08-28 | $1199.18 | COIN, CRSP, HIMX, IONQ |
| 2026-08-31 | $1201.96 | COIN, CRSP, HIMX, IONQ |
| 2026-09-01 | $1187.73 | COIN, CRSP, HIMX, SOUN |
| 2026-09-02 | $1185.20 | COIN, CRSP, HIMX, SOUN |
| 2026-09-03 | $1190.42 | COIN, CRSP, HIMX, SOUN |
| 2026-09-04 | $1185.32 | COIN, CRSP, HIMX, SOUN |
| 2026-09-08 | $1170.26 | COIN, DUOL, HIMX, RXRX |
| 2026-09-09 | $1149.15 | ASTS, COIN, HIMX, QBTS |
| 2026-09-10 | $1127.21 | COIN, HIMX, QBTS |
| 2026-09-11 | $1141.60 | COIN, HIMX, QBTS |
| 2026-09-14 | $1118.34 | COIN, HIMX, SMCI |
| 2026-09-15 | $1093.24 | BULL, GRAB, HIMX, SMCI |
| 2026-09-16 | $1077.35 | DUOL, HIMX, SMCI |
| 2026-09-17 | $1110.13 | DUOL, HIMX, SMCI |
| 2026-09-18 | $1105.34 | DUOL, HIMX, RGTI, SMCI |
| 2026-09-21 | $1152.14 | DUOL, HIMX, RGTI, STNE |
| 2026-09-22 | $1155.74 | DUOL, HIMX, RGTI, STNE |
| 2026-09-23 | $1130.45 | DUOL, HIMX, RGTI, STNE |
| 2026-09-24 | $1131.02 | BTBT, DUOL, HIMX, RGTI |
| 2026-09-25 | $1129.36 | BTBT, DUOL, HIMX, RGTI |
| 2026-09-28 | $1094.60 | AXTI, BTBT, HIMX, RGTI |
| 2026-09-29 | $1106.63 | AXTI, HIMX, IREN, RGTI |
| 2026-09-30 | $1102.08 | AXTI, HIMX, IREN, RGTI |
| 2026-10-01 | $1117.89 | AXTI, HIMX, RGTI, RIOT |
| 2026-10-02 | $1136.86 | AXTI, HIMX, RGTI, RIOT |
| 2026-10-05 | $1124.43 | AXTI, HIMX, LUNR, RIOT |
| 2026-10-06 | $1117.07 | AXTI, HIMX, LUNR, RIOT |

## Entries only 0.25+ ATR under the prior close: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1241.01 (+24.10%; realized $+110.84, open positions $+130.17); S&P 500 +3.63%, Nasdaq-100 +5.55%. 29 closed trades, 6 winners (20.7%), average trade 2.44%, average win 29.03%, average loss -4.5%, profit factor 1.47, worst drawdown -9.7%. Exits: target 6, stop 23. Resting orders filled: 21/38.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -4.51%, total $-65.55
- stopped on a later session: 16 trades, 0 won, average -4.49%, total $-167.90
- stopped at the open (gapped through the stop): 8 trades, 0 won, average -4.16%, total $-80.17
- never rose 0.5 ATR above the entry: 18 trades, 0 won, average -4.42%, total $-185.23
- crypto-linked: 3 trades, 0 won, average -3.00%, total $-20.15
- bought at the open after a gap down of 0.5+ ATR: 4 trades, 1 won, average +3.38%, total $+41.01
- bought on a dip of 0.5+ ATR (any time): 17 trades, 3 won, average -0.51%, total $+5.42
- resting limit fills: 19 trades, 4 won, average +2.79%, total $+91.72
- run entries inside the buy zone: 9 trades, 1 won, average -0.35%, total $-31.71
- run entries on a bounce (touched the zone, back above it): 1 trade, 1 won, average +20.84%, total $+50.83
- support tested 3+ times: 22 trades, 5 won, average +3.80%, total $+126.08
- support tested twice: 5 trades, 1 won, average +0.80%, total $+16.04
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -8.44%, total $-31.28

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:30 | 608.1 | stop | -3.93% | +0.12 / -0.89 |
| 2026-07-23 10:05 | AFRM | bounce | 71.04 | -0.58 / -0.81 | 4.52 | 2026-08-28 9:50 | 85.85 | target | +20.84% | +5.43 / -0.40 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-07-30 9:30 | NOW | limit | 110.5 | -0.79 / -0.79 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -2.11% | +0.10 / -0.37 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-11 9:30 | RKLB | limit | 76.27 | -0.63 / -0.63 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -1.01% | +0.44 / -0.14 |
| 2026-08-12 9:35 | RKLB | limit | 78.2 | +0.02 / -0.29 | 18.98 | 2026-08-19 9:35 | 75.41 | stop | -3.57% | +1.20 / -0.55 |
| 2026-08-20 15:00 | HOOD | limit | 93.67 | +1.11 / -0.46 | 9.0 | 2026-09-03 9:50 | 119 | target | +27.08% | +6.23 / -0.00 |
| 2026-08-25 10:05 | LUNR | limit | 16.22 | +0.19 / -0.27 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -5.81% | +0.33 / -0.57 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | GPUS | buy zone | 0.224 | -0.42 / -0.43 | 14.43 | 2026-09-02 11:10 | 0.2067 | stop | -7.79% | +0.39 / -0.53 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.94% | +2.20 / -0.25 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-09 10:20 | RGTI | limit | 15.4 | -0.18 / -0.40 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -3.67% | +0.43 / -0.54 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.04% | +4.49 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.06 | 11.57 | 15.81 | 14.85 | +23.13% |
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| NOW | 2026-09-29 | 130.1 | 127.1 | 146.9 | 138 | +6.05% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 15.06 | +6.52% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $962.97 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $961.19 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $984.78 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $975.53 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $984.48 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-24 | $948.07 | AFRM, HOOD, UMAC |
| 2026-07-27 | $972.97 | AFRM, HOOD, UMAC |
| 2026-07-28 | $939.71 | AFRM, UMAC |
| 2026-07-29 | $903.03 | AFRM, PCVX, UMAC |
| 2026-07-30 | $957.24 | AFRM, PCVX, UMAC |
| 2026-07-31 | $949.93 | AFRM, PCVX, UMAC |
| 2026-08-03 | $996.45 | AFRM, HIMX, PCVX, UMAC |
| 2026-08-04 | $1071.40 | AFRM, HIMX, PCVX |
| 2026-08-05 | $1059.77 | AFRM, HIMX, PCVX, POET |
| 2026-08-06 | $1088.70 | AFRM, HIMX, POET |
| 2026-08-07 | $1113.33 | AFRM, HIMX, POET |
| 2026-08-10 | $1105.18 | AFRM, HIMX, POET |
| 2026-08-11 | $1112.29 | AFRM, HIMX, POET |
| 2026-08-12 | $1122.64 | AFRM, HIMX, POET, RKLB |
| 2026-08-13 | $1128.67 | AFRM, HIMX, POET, RKLB |
| 2026-08-14 | $1162.52 | AFRM, HIMX, POET, RKLB |
| 2026-08-17 | $1153.36 | AFRM, HIMX, POET, RKLB |
| 2026-08-18 | $1089.22 | AFRM, HIMX, POET, RKLB |
| 2026-08-19 | $1078.55 | AFRM, HIMX, POET |
| 2026-08-20 | $1064.63 | AFRM, HIMX, HOOD, POET |
| 2026-08-21 | $1109.64 | AFRM, HIMX, HOOD, POET |
| 2026-08-24 | $1071.46 | AFRM, HIMX, HOOD |
| 2026-08-25 | $1109.33 | AFRM, HIMX, HOOD, LUNR |
| 2026-08-26 | $1089.98 | AFRM, HIMX, HOOD, LUNR |
| 2026-08-27 | $1102.55 | AFRM, HIMX, HOOD, LUNR |
| 2026-08-28 | $1093.26 | HIMX, HOOD |
| 2026-08-31 | $1103.98 | HIMX, HOOD, SMCI |
| 2026-09-01 | $1072.66 | BMNR, HIMX, HOOD, SMCI |
| 2026-09-02 | $1071.27 | HIMX, HOOD, SMCI |
| 2026-09-03 | $1111.53 | AEHR, HIMX, SMCI |
| 2026-09-04 | $1138.50 | AEHR, HIMX, SMCI |
| 2026-09-08 | $1157.48 | AEHR, HIMX, SMCI |
| 2026-09-09 | $1148.22 | HIMX, RGTI, SMCI |
| 2026-09-10 | $1125.57 | HIMX, SMCI |
| 2026-09-11 | $1164.74 | HIMX, SMCI |
| 2026-09-14 | $1125.08 | HIMX, RKLB, SMCI |
| 2026-09-15 | $1109.21 | GRAB, HIMX, RKLB, SMCI |
| 2026-09-16 | $1111.98 | HIMX, RKLB, SMCI |
| 2026-09-17 | $1169.63 | HIMX, RKLB, SMCI |
| 2026-09-18 | $1157.07 | HIMX, RGTI, RKLB, SMCI |
| 2026-09-21 | $1223.27 | HIMX, RGTI, RKLB, SMCI |
| 2026-09-22 | $1237.30 | HIMX, RGTI, RKLB, SMCI |
| 2026-09-23 | $1210.95 | HIMX, RGTI, RKLB, SMCI |
| 2026-09-24 | $1232.87 | HIMX, RGTI, SMCI |
| 2026-09-25 | $1257.03 | BTBT, HIMX, RGTI, SMCI |
| 2026-09-28 | $1209.38 | BTBT, HIMX, RGTI, SMCI |
| 2026-09-29 | $1200.89 | HIMX, NOW, RGTI, SMCI |
| 2026-09-30 | $1201.71 | HIMX, NOW, RGTI, SMCI |
| 2026-10-01 | $1214.34 | HIMX, NOW, RGTI, SMCI |
| 2026-10-02 | $1235.59 | HIMX, NOW, RGTI, SMCI |
| 2026-10-05 | $1219.72 | HIMX, LUNR, NOW, SMCI |
| 2026-10-06 | $1241.01 | HIMX, LUNR, NOW, SMCI |

## Gap through the stop: sell at 9:55 if still under: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1199.03 (+19.90%; realized $+104.97, open positions $+94.06); S&P 500 +3.63%, Nasdaq-100 +5.55%. 38 closed trades, 10 winners (26.3%), average trade 2.45%, average win 24.31%, average loss -5.36%, profit factor 1.32, worst drawdown -13.31%. Exits: target 10, stop 28. Resting orders filled: 17/25.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -6.27%, total $-65.69
- stopped on a later session: 22 trades, 0 won, average -5.12%, total $-261.93
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -5.37%, total $-94.22
- never rose 0.5 ATR above the entry: 19 trades, 0 won, average -5.43%, total $-226.30
- crypto-linked: 3 trades, 1 won, average +0.82%, total $+12.31
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-11.03
- bought on a dip of 0.5+ ATR (any time): 24 trades, 7 won, average +2.54%, total $+63.27
- bought less than 0.25 ATR under the prior close: 5 trades, 2 won, average +2.27%, total $+19.88
- resting limit fills: 15 trades, 3 won, average +1.83%, total $+25.20
- run entries inside the buy zone: 19 trades, 6 won, average +3.90%, total $+102.24
- run entries on a bounce (touched the zone, back above it): 4 trades, 1 won, average -2.16%, total $-22.47
- support tested 3+ times: 28 trades, 8 won, average +2.99%, total $+69.43
- support tested twice: 8 trades, 2 won, average +3.56%, total $+71.07
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-35.53

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-15 12:10 | RCAT | limit | 8.31 | +0.03 / -0.61 | 4.95 | 2026-07-16 9:30 | 7.82 | stop | -5.90% | +0.29 / -0.62 |
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 9:45 | BBAI | limit | 3.03 | -0.16 / -0.57 | 5.56 | 2026-07-16 15:45 | 2.898 | stop | -4.37% | +0.21 / -0.63 |
| 2026-07-16 9:50 | CRSP | buy zone | 48.99 | -0.19 / -0.68 | 2.26 | 2026-07-24 15:10 | 45.98 | stop | -6.22% | +0.68 / -0.88 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:50 | AFRM | buy zone | 76.77 | -0.80 / -0.81 | 3.15 | 2026-07-21 12:00 | 73.87 | stop | -3.79% | +0.18 / -0.77 |
| 2026-07-21 12:05 | GRAB | buy zone | 3.568 | -0.03 / -0.32 | 5.95 | 2026-07-22 9:30 | 3.468 | stop | -2.80% | +0.00 / -0.60 |
| 2026-07-22 9:50 | META | buy zone | 632.9 | +0.13 / -0.36 | 5.32 | 2026-07-23 9:50 | 610.2 | stop | -3.59% | +0.12 / -0.91 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.68% | +1.97 / -0.25 |
| 2026-07-24 9:50 | HOOD | buy zone | 95.43 | -0.28 / -0.97 | 4.68 | 2026-07-28 9:30 | 90.53 | stop | -5.14% | +0.64 / -0.89 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.56% | +3.02 / -0.22 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-06 10:05 | NOW | buy zone | 113.2 | -0.61 / -0.58 | 4.73 | 2026-08-27 10:05 | 138.2 | target | +22.00% | +3.69 / -0.02 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.34% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-20 10:20 | UMAC | buy zone | 26.26 | +0.01 / -0.63 | 5.23 | 2026-08-24 9:30 | 24.81 | stop | -5.54% | +0.54 / -0.49 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:50 | 53.96 | stop | -5.27% | +1.75 / -1.59 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:50 | 38.03 | stop | -8.70% | +0.45 / -1.38 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.86% | +0.00 / -0.80 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-02 11:20 | WULF (crypto) | buy zone | 14.45 | -0.17 / -0.17 | 4.29 | 2026-09-08 9:50 | 16.98 | target | +17.54% | +2.27 / -0.05 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:50 | 15.01 | stop | -3.94% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-15 10:45 | 16.38 | stop | -3.69% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-15 10:50 | RXRX | buy zone | 3.246 | -0.27 / -0.87 | 3.82 | 2026-09-18 10:50 | 3.592 | target | +10.64% | +1.96 / -0.46 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 10:50 | LUNR | buy zone | 13.99 | +0.14 / -1.00 | 9.72 | 2026-09-22 11:20 | 15.71 | target | +12.29% | +2.30 / -0.25 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 43.46 | +19.82% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 138 | +5.75% |
| UMAC | 2026-09-16 | 21.43 | 20.98 | 26.12 | 22.36 | +4.34% |
| AXTI | 2026-09-22 | 75.39 | 71.21 | 89.42 | 84.06 | +11.50% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $997.89 | RCAT |
| 2026-07-16 | $968.95 | CRSP, IONQ, POET |
| 2026-07-17 | $962.97 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-20 | $961.19 | AFRM, CRSP, IONQ, UMAC |
| 2026-07-21 | $984.78 | CRSP, GRAB, IONQ, UMAC |
| 2026-07-22 | $975.53 | CRSP, IONQ, META, UMAC |
| 2026-07-23 | $987.88 | CRSP, DUOL, IONQ, UMAC |
| 2026-07-24 | $958.05 | DUOL, HOOD, UMAC |
| 2026-07-27 | $997.82 | HOOD, UMAC |
| 2026-07-28 | $968.95 | DELL, UMAC |
| 2026-07-29 | $938.81 | AFRM, DELL, PCVX, UMAC |
| 2026-07-30 | $1001.61 | AFRM, DELL, PCVX, UMAC |
| 2026-07-31 | $994.04 | AFRM, DELL, PCVX, UMAC |
| 2026-08-03 | $1028.70 | AFRM, DELL, PCVX, UMAC |
| 2026-08-04 | $1093.78 | AFRM, AXTI, PCVX |
| 2026-08-05 | $1111.27 | AFRM, AXTI, PCVX, POET |
| 2026-08-06 | $1159.56 | AFRM, AXTI, NOW, POET |
| 2026-08-07 | $1226.18 | AFRM, MARA, NOW, POET |
| 2026-08-10 | $1203.15 | AFRM, MARA, NOW, POET |
| 2026-08-11 | $1211.29 | AFRM, MARA, NOW, POET |
| 2026-08-12 | $1207.02 | AFRM, MARA, NOW, POET |
| 2026-08-13 | $1209.89 | AFRM, NOW, ONDS, POET |
| 2026-08-14 | $1240.31 | AFRM, NOW, ONDS, POET |
| 2026-08-17 | $1197.85 | AFRM, NOW, POET, UPST |
| 2026-08-18 | $1157.80 | AFRM, NOW, POET, UPST |
| 2026-08-19 | $1188.60 | AFRM, NOW, POET, UPST |
| 2026-08-20 | $1150.65 | AFRM, NOW, POET, UMAC |
| 2026-08-21 | $1170.61 | AFRM, NOW, POET, UMAC |
| 2026-08-24 | $1125.97 | AFRM, CRSP, NOW |
| 2026-08-25 | $1154.17 | AFRM, CRSP, LUNR, NOW |
| 2026-08-26 | $1131.45 | AFRM, CRSP, LUNR, NOW |
| 2026-08-27 | $1146.84 | AFRM, CRSP, IONQ, LUNR |
| 2026-08-28 | $1129.01 | CRSP, IONQ |
| 2026-08-31 | $1133.63 | CRSP, IONQ, SMCI |
| 2026-09-01 | $1104.74 | CRSP, SMCI, SOUN |
| 2026-09-02 | $1093.85 | CRSP, SMCI, SOUN, WULF |
| 2026-09-03 | $1117.81 | CRSP, SMCI, SOUN, WULF |
| 2026-09-04 | $1131.62 | CRSP, SMCI, SOUN, WULF |
| 2026-09-08 | $1130.53 | DUOL, SMCI |
| 2026-09-09 | $1105.87 | QBTS, RGTI, SMCI, SMR |
| 2026-09-10 | $1075.27 | QBTS, SMCI |
| 2026-09-11 | $1101.48 | NOW, QBTS, SMCI |
| 2026-09-14 | $1095.74 | NOW, QBTS, SMCI |
| 2026-09-15 | $1078.72 | GRAB, NOW, RXRX, SMCI |
| 2026-09-16 | $1080.54 | NOW, RXRX, SMCI, UMAC |
| 2026-09-17 | $1128.94 | NOW, RXRX, SMCI, UMAC |
| 2026-09-18 | $1110.91 | LUNR, NOW, SMCI, UMAC |
| 2026-09-21 | $1170.76 | LUNR, NOW, SMCI, UMAC |
| 2026-09-22 | $1175.96 | AXTI, NOW, SMCI, UMAC |
| 2026-09-23 | $1166.78 | AXTI, NOW, SMCI, UMAC |
| 2026-09-24 | $1172.84 | AXTI, NOW, SMCI, UMAC |
| 2026-09-25 | $1189.05 | AXTI, NOW, SMCI, UMAC |
| 2026-09-28 | $1157.25 | AXTI, NOW, SMCI, UMAC |
| 2026-09-29 | $1162.19 | AXTI, NOW, SMCI, UMAC |
| 2026-09-30 | $1167.30 | AXTI, NOW, SMCI, UMAC |
| 2026-10-01 | $1179.24 | AXTI, NOW, SMCI, UMAC |
| 2026-10-02 | $1197.34 | AXTI, NOW, SMCI, UMAC |
| 2026-10-05 | $1196.28 | AXTI, NOW, SMCI, UMAC |
| 2026-10-06 | $1199.03 | AXTI, NOW, SMCI, UMAC |

