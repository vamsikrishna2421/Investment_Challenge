# Replay of the rules, 2026-08-24 to 2026-10-05 (30 sessions, 5-minute bars)

$1,000 each; S&P 500 +1.19%, Nasdaq-100 +5.99% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules: target at the bottom of the sell zone | +3.17% | 17 | 17.6% | 0.02% | 0.82 | -7.89% | SMCI, NOW, WULF |
| First resistance above the entry (any touches, 0.5+ ATR up) | +4.08% | 32 | 37.5% | 1.24% | 1.2 | -7.89% | UMAC, RIOT, SMR, WULF |
| Entry + 1 ATR | +3.88% | 39 | 41.0% | 0.53% | 1.18 | -6.57% | - |
| Entry + 1.5 ATR | +4.71% | 33 | 33.3% | 0.8% | 1.24 | -7.89% | RIOT, LUNR |
| Entry + 2 ATR | +5.61% | 28 | 32.1% | 1.63% | 1.3 | -7.89% | RIOT, WULF |
| Entry + 3 ATR | -0.07% | 19 | 15.8% | -0.61% | 0.65 | -7.89% | SMCI, NOW |

## Live rules: target at the bottom of the sell zone: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1031.71 (+3.17%; realized $-26.21, open positions $+57.92); S&P 500 +1.19%, Nasdaq-100 +5.99%. 17 closed trades, 3 winners (17.6%), average trade 0.02%, average win 22.68%, average loss -4.84%, profit factor 0.82, worst drawdown -7.89%. Exits: target 3, stop 14. Resting orders filled: 15/36.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.02%, total $-56.93
- stopped on a later session: 9 trades, 0 won, average -4.18%, total $-85.29
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -3.37%, total $-21.53
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -4.87%, total $-107.99
- crypto-linked: 5 trades, 1 won, average +0.54%, total $+6.74
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+49.52
- bought on a dip of 0.5+ ATR (any time): 8 trades, 1 won, average -1.02%, total $-9.09
- bought less than 0.25 ATR under the prior close: 4 trades, 2 won, average +9.22%, total $+43.09
- resting limit fills: 12 trades, 1 won, average -3.19%, total $-81.19
- run entries inside the buy zone: 5 trades, 2 won, average +7.73%, total $+54.98
- support tested 3+ times: 12 trades, 2 won, average +0.36%, total $-34.75
- support tested twice: 3 trades, 1 won, average +5.09%, total $+38.56
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.02

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.53 | 35.01 | 50.6 | 43.19 | +18.22% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 136.1 | +4.30% |
| WULF | 2026-10-01 | 14.55 | 13.95 | 17.75 | 14.79 | +1.65% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $953.47 | SOUN |
| 2026-08-31 | $960.07 | SMCI, SOUN |
| 2026-09-01 | $930.54 | BMNR, SMCI, SOUN |
| 2026-09-02 | $921.07 | SMCI, SOUN, WULF |
| 2026-09-03 | $943.89 | AEHR, SMCI, WULF |
| 2026-09-04 | $970.55 | AEHR, SMCI, WULF |
| 2026-09-08 | $988.07 | AEHR, DUOL, SMCI |
| 2026-09-09 | $973.59 | RGTI, SMCI |
| 2026-09-10 | $957.06 | SMCI |
| 2026-09-11 | $978.59 | NOW, SMCI |
| 2026-09-14 | $982.17 | NOW, RKLB, SMCI |
| 2026-09-15 | $973.82 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $975.25 | NOW, RKLB, SMCI |
| 2026-09-17 | $1011.20 | NOW, RKLB, SMCI |
| 2026-09-18 | $989.47 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $1039.23 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $1047.96 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $1040.02 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $1055.22 | NOW, RGTI, SMCI |
| 2026-09-25 | $1066.63 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $1026.39 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $1014.03 | NOW, RGTI, SMCI |
| 2026-09-30 | $1021.82 | NOW, RGTI, SMCI |
| 2026-10-01 | $1038.72 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $1048.58 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $1031.71 | NOW, SMCI, WULF |

## First resistance above the entry (any touches, 0.5+ ATR up): 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1040.84 (+4.08%; realized $+40.76, open positions $+0.08); S&P 500 +1.19%, Nasdaq-100 +5.99%. 32 closed trades, 12 winners (37.5%), average trade 1.24%, average win 10.82%, average loss -4.51%, profit factor 1.2, worst drawdown -7.89%. Exits: target 12, stop 20. Resting orders filled: 19/51.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.02%, total $-56.86
- stopped on a later session: 15 trades, 0 won, average -4.00%, total $-142.27
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -3.67%, total $-33.36
- never rose 0.5 ATR above the entry: 17 trades, 0 won, average -4.55%, total $-167.78
- crypto-linked: 7 trades, 2 won, average +1.00%, total $+19.19
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 1 won, average +2.30%, total $+10.66
- bought on a dip of 0.5+ ATR (any time): 14 trades, 5 won, average +0.41%, total $-0.45
- bought less than 0.25 ATR under the prior close: 9 trades, 5 won, average +5.38%, total $+63.45
- resting limit fills: 19 trades, 6 won, average -0.97%, total $-27.90
- run entries inside the buy zone: 12 trades, 5 won, average +3.97%, total $+43.99
- run entries on a bounce (touched the zone, back above it): 1 trade, 1 won, average +10.43%, total $+24.67
- support tested 3+ times: 19 trades, 8 won, average +2.51%, total $+57.04
- support tested twice: 11 trades, 4 won, average +1.03%, total $+13.74
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.02

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-04 10:20 | 39.49 | target | +8.07% | +1.12 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-04 10:20 | BULL | buy zone | 9.704 | -0.40 / -0.47 | 6.16 | 2026-09-08 15:35 | 9.44 | stop | -2.73% | +0.48 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-14 10:50 | 139.5 | target | +6.92% | +1.64 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-15 12:50 | 64.56 | target | +6.58% | +1.79 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-21 10:20 | 41.33 | target | +10.43% | +1.82 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-21 9:50 | 16.18 | target | +4.51% | +1.31 / -0.47 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 2.69 | 2026-09-23 9:50 | 9.975 | target | +4.44% | +1.10 / -0.05 |
| 2026-09-23 9:50 | OKLO | buy zone | 39.47 | -0.09 / -0.39 | 3.09 | 2026-09-24 9:30 | 37.94 | stop | -3.89% | +0.26 / -0.62 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-25 11:20 | 17.11 | target | +9.36% | +1.67 / -0.04 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.98% | +1.12 / -0.42 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.20% | +1.68 / -0.01 |
| 2026-09-25 11:20 | CRCL (crypto) | buy zone | 88.43 | -0.15 / -0.69 | 2.05 | 2026-09-30 10:30 | 82.87 | stop | -6.31% | +0.11 / -0.85 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-28 10:50 | AXTI | buy zone | 71.84 | -0.38 / -1.13 | 22.99 | 2026-10-01 10:35 | 81.96 | target | +14.08% | +1.93 / -0.02 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.76% | +0.07 / -0.70 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-02 10:05 | 16.12 | target | +10.80% | +1.60 / -0.19 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| UMAC | 2026-09-16 | 21.43 | 20.98 | 26.12 | 21.83 | +1.86% |
| RIOT | 2026-10-01 | 19.31 | 18.39 | 21.78 | 19.32 | +0.03% |
| SMR | 2026-10-02 | 7.826 | 7.371 | 8.756 | 7.68 | -1.86% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 16.01 | 14.79 | +0.04% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $953.47 | SOUN |
| 2026-08-31 | $960.07 | SMCI, SOUN |
| 2026-09-01 | $930.54 | BMNR, SMCI, SOUN |
| 2026-09-02 | $921.07 | SMCI, SOUN, WULF |
| 2026-09-03 | $943.89 | AEHR, SMCI, WULF |
| 2026-09-04 | $970.67 | AEHR, BULL, WULF |
| 2026-09-08 | $977.11 | AEHR, DUOL |
| 2026-09-09 | $968.30 | RGTI, SMR |
| 2026-09-10 | $953.89 | - |
| 2026-09-11 | $957.66 | NOW |
| 2026-09-14 | $973.87 | RKLB, SMCI |
| 2026-09-15 | $970.72 | GRAB, SMCI |
| 2026-09-16 | $978.76 | SMCI, UMAC |
| 2026-09-17 | $1012.50 | SMCI, UMAC |
| 2026-09-18 | $1004.76 | RGTI, SMCI, UMAC |
| 2026-09-21 | $1034.19 | STNE, UMAC |
| 2026-09-22 | $1034.47 | STNE, UMAC |
| 2026-09-23 | $1023.14 | OKLO, UMAC |
| 2026-09-24 | $1055.75 | HIMS, QUBT, RGTI, UMAC |
| 2026-09-25 | $1063.73 | CRCL, QUBT, UMAC |
| 2026-09-28 | $1049.02 | AXTI, CRCL, SMCI, UMAC |
| 2026-09-29 | $1053.15 | AXTI, CRCL, SMCI, UMAC |
| 2026-09-30 | $1037.75 | AXTI, BTDR, UMAC |
| 2026-10-01 | $1033.13 | RIOT, UMAC, WULF |
| 2026-10-02 | $1056.33 | PATH, RIOT, SMR, UMAC |
| 2026-10-05 | $1040.84 | RIOT, SMR, UMAC, WULF |

## Entry + 1 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1038.76 (+3.88%; realized $+38.73, open positions $+0.03); S&P 500 +1.19%, Nasdaq-100 +5.99%. 39 closed trades, 16 winners (41.0%), average trade 0.53%, average win 7.68%, average loss -4.44%, profit factor 1.18, worst drawdown -6.57%. Exits: target 16, stop 23. Resting orders filled: 24/62.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -5.32%, total $-73.93
- stopped on a later session: 16 trades, 0 won, average -4.05%, total $-136.04
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -4.17%, total $-39.71
- never rose 0.5 ATR above the entry: 18 trades, 0 won, average -4.48%, total $-170.30
- crypto-linked: 6 trades, 3 won, average +2.35%, total $+35.74
- bought at the open after a gap down of 0.5+ ATR: 3 trades, 2 won, average +2.70%, total $+19.27
- bought on a dip of 0.5+ ATR (any time): 21 trades, 10 won, average +1.15%, total $+56.23
- bought less than 0.25 ATR under the prior close: 9 trades, 3 won, average -0.50%, total $-2.66
- resting limit fills: 24 trades, 9 won, average -0.50%, total $-14.95
- run entries inside the buy zone: 13 trades, 6 won, average +2.32%, total $+50.55
- run entries on a bounce (touched the zone, back above it): 2 trades, 1 won, average +1.33%, total $+3.13
- support tested 3+ times: 27 trades, 12 won, average +1.22%, total $+50.22
- support tested twice: 10 trades, 4 won, average +0.71%, total $+19.22
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.71

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-27 11:05 | 1.647 | target | +9.04% | +1.05 / -0.21 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-04 10:05 | 39.23 | target | +7.36% | +1.09 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-03 10:35 | 15.54 | target | +8.02% | +1.02 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 10:35 | AEHR | buy zone | 76.69 | -0.11 / -0.32 | 4.83 | 2026-09-08 9:50 | 90.27 | target | +17.70% | +1.64 / -0.19 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-04 10:05 | BULL | buy zone | 9.684 | -0.40 / -0.50 | 6.85 | 2026-09-08 15:35 | 9.44 | stop | -2.53% | +0.52 / -0.36 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.53% | +0.64 / -0.85 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-14 9:50 | 138.1 | target | +5.86% | +1.64 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-15 9:50 | 64.27 | target | +6.10% | +1.79 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-17 10:35 | 40.09 | target | +7.11% | +1.22 / -0.93 |
| 2026-09-15 9:50 | RXRX | buy zone | 3.306 | -0.27 / -0.55 | 1.95 | 2026-09-17 10:35 | 3.507 | target | +6.04% | +1.35 / -0.78 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | UMAC | buy zone | 21.43 | +0.01 / -0.92 | 10.6 | 2026-09-17 9:50 | 23.61 | target | +10.14% | +1.52 / -0.06 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-09-21 11:20 | 85.42 | target | +6.98% | +1.11 / -0.29 |
| 2026-09-17 10:35 | AFRM | buy zone | 72.15 | +0.57 / +0.13 | 2.49 | 2026-09-23 9:55 | 69.27 | stop | -4.01% | +0.29 / -0.78 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-21 10:05 | 16.35 | target | +5.60% | +1.31 / -0.47 |
| 2026-09-21 10:05 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-24 13:40 | 9.158 | stop | -4.46% | +1.01 / -0.98 |
| 2026-09-23 10:05 | RCAT | buy zone | 6.769 | -0.07 / -0.37 | 3.96 | 2026-09-24 9:40 | 6.415 | stop | -5.24% | +0.22 / -0.76 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-24 14:05 | 9.226 | target | +4.13% | +1.12 / +0.00 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-24 15:50 | 16.54 | target | +5.72% | +1.01 / -0.04 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-24 13:20 | 28.82 | target | +5.19% | +1.07 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-28 9:30 | NOW | limit | 129.8 | -1.05 / -1.05 | 4.94 | 2026-09-28 9:35 | 127.1 | stop | -2.12% | +0.00 / -0.55 |
| 2026-09-28 9:35 | AXTI | limit | 74.8 | -0.38 / -0.66 | 3.86 | 2026-10-01 9:50 | 81.11 | target | +8.43% | +1.46 / -0.52 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-30 9:40 | WULF (crypto) | limit | 14.55 | +0.18 / -0.53 | 5.23 | 2026-10-02 9:50 | 15.92 | target | +9.39% | +1.38 / -0.19 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $994.63 | SOUN |
| 2026-08-28 | $975.47 | SOUN |
| 2026-08-31 | $982.18 | SMCI, SOUN |
| 2026-09-01 | $952.25 | BMNR, SMCI, SOUN |
| 2026-09-02 | $942.50 | SMCI, SOUN, WULF |
| 2026-09-03 | $956.86 | AEHR, SMCI |
| 2026-09-04 | $976.65 | AEHR, BULL, RCAT |
| 2026-09-08 | $984.03 | DUOL, RCAT |
| 2026-09-09 | $955.07 | QBTS, RCAT, RGTI, SMR |
| 2026-09-10 | $934.28 | QBTS |
| 2026-09-11 | $938.76 | NOW, QBTS |
| 2026-09-14 | $949.74 | RKLB, SMCI |
| 2026-09-15 | $946.36 | GRAB, RXRX, SMCI |
| 2026-09-16 | $952.61 | RXRX, SMCI, UMAC |
| 2026-09-17 | $988.79 | AFRM, CRWV |
| 2026-09-18 | $999.06 | AFRM, CRWV, RGTI |
| 2026-09-21 | $1022.23 | AFRM, STNE |
| 2026-09-22 | $1025.63 | AFRM, STNE |
| 2026-09-23 | $1009.47 | RCAT, STNE |
| 2026-09-24 | $1028.34 | - |
| 2026-09-25 | $1029.81 | BTBT |
| 2026-09-28 | $1007.99 | AXTI, BTBT, SMCI |
| 2026-09-29 | $1017.40 | AXTI, SMCI |
| 2026-09-30 | $1015.66 | AXTI, WULF |
| 2026-10-01 | $1030.16 | WULF |
| 2026-10-02 | $1044.84 | PATH |
| 2026-10-05 | $1038.76 | - |

## Entry + 1.5 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1047.13 (+4.71%; realized $+48.63, open positions $-1.50); S&P 500 +1.19%, Nasdaq-100 +5.99%. 33 closed trades, 11 winners (33.3%), average trade 0.8%, average win 11.67%, average loss -4.63%, profit factor 1.24, worst drawdown -7.89%. Exits: target 11, stop 22. Resting orders filled: 18/56.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.03%, total $-56.23
- stopped on a later session: 17 trades, 0 won, average -4.22%, total $-145.25
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -4.78%, total $-29.00
- never rose 0.5 ATR above the entry: 17 trades, 0 won, average -4.89%, total $-155.38
- crypto-linked: 7 trades, 1 won, average -1.79%, total $-18.18
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 1 won, average +4.56%, total $+21.08
- bought on a dip of 0.5+ ATR (any time): 17 trades, 7 won, average +1.63%, total $+79.25
- bought less than 0.25 ATR under the prior close: 9 trades, 4 won, average +3.68%, total $+42.92
- resting limit fills: 18 trades, 4 won, average -1.67%, total $-60.75
- run entries inside the buy zone: 14 trades, 6 won, average +3.38%, total $+87.73
- run entries on a bounce (touched the zone, back above it): 1 trade, 1 won, average +9.25%, total $+21.65
- support tested 3+ times: 20 trades, 7 won, average +1.55%, total $+32.57
- support tested twice: 11 trades, 4 won, average +1.34%, total $+46.08
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.02

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-04 12:20 | 40.55 | target | +10.98% | +1.53 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-04 9:50 | 16.33 | target | +13.54% | +1.76 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 9:50 | 95.73 | target | +21.34% | +1.58 / -0.39 |
| 2026-09-04 9:50 | BULL | buy zone | 9.669 | -0.40 / -0.52 | 7.47 | 2026-09-08 15:35 | 9.44 | stop | -2.38% | +0.54 / -0.34 |
| 2026-09-08 15:35 | DUOL | buy zone | 146.8 | -0.26 / -1.04 | 3.19 | 2026-09-09 10:15 | 140.8 | stop | -4.05% | +0.03 / -0.93 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 9:50 | NNE | buy zone | 18.92 | -0.09 / -0.37 | 5.78 | 2026-09-09 11:00 | 18.39 | stop | -2.85% | +0.01 / -0.48 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-14 11:05 | 140.5 | target | +7.66% | +1.64 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-17 9:50 | 67.3 | target | +11.10% | +2.43 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-17 10:50 | 40.89 | target | +9.25% | +1.59 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | UMAC | buy zone | 21.43 | +0.01 / -0.92 | 10.6 | 2026-09-17 14:50 | 24.19 | target | +12.85% | +1.60 / -0.06 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-09-22 10:20 | 88.68 | target | +11.06% | +1.72 / -0.29 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-25 11:05 | 16.77 | target | +8.32% | +2.65 / -0.47 |
| 2026-09-22 10:20 | AXTI | buy zone | 76.4 | -0.55 / -0.59 | 2.54 | 2026-09-24 9:30 | 70.06 | stop | -8.33% | +0.39 / -1.13 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.98% | +1.12 / -0.42 |
| 2026-09-24 9:30 | BTBT (crypto) | limit | 1.725 | -0.35 / -0.35 | 7.71 | 2026-09-29 12:05 | 1.664 | stop | -3.57% | +0.74 / -0.43 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 11:05 | CRCL (crypto) | buy zone | 88.84 | -0.15 / -0.63 | 1.84 | 2026-09-30 10:30 | 82.87 | stop | -6.76% | +0.05 / -0.91 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-28 10:50 | AXTI | buy zone | 71.84 | -0.38 / -1.13 | 22.99 | 2026-10-01 10:35 | 81.96 | target | +14.08% | +1.93 / -0.02 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.76% | +0.07 / -0.70 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 19.32 | -1.78% |
| LUNR | 2026-10-05 | 14.32 | 13.35 | 15.84 | 14.29 | -0.23% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $953.47 | SOUN |
| 2026-08-31 | $960.07 | SMCI, SOUN |
| 2026-09-01 | $930.54 | BMNR, SMCI, SOUN |
| 2026-09-02 | $921.07 | SMCI, SOUN, WULF |
| 2026-09-03 | $943.89 | AEHR, SMCI, WULF |
| 2026-09-04 | $975.51 | AEHR, BULL |
| 2026-09-08 | $973.12 | AEHR, DUOL |
| 2026-09-09 | $957.99 | RGTI, SMR |
| 2026-09-10 | $943.63 | - |
| 2026-09-11 | $947.36 | NOW |
| 2026-09-14 | $965.15 | RKLB, SMCI |
| 2026-09-15 | $958.10 | GRAB, RKLB, SMCI |
| 2026-09-16 | $966.35 | RKLB, SMCI, UMAC |
| 2026-09-17 | $1018.05 | CRWV |
| 2026-09-18 | $1026.85 | CRWV, RGTI |
| 2026-09-21 | $1051.04 | CRWV, RGTI |
| 2026-09-22 | $1061.31 | AXTI, RGTI |
| 2026-09-23 | $1048.46 | AXTI, RGTI |
| 2026-09-24 | $1086.07 | BTBT, HIMS, QUBT, RGTI |
| 2026-09-25 | $1082.68 | BTBT, CRCL, QUBT |
| 2026-09-28 | $1064.79 | AXTI, BTBT, CRCL, SMCI |
| 2026-09-29 | $1069.40 | AXTI, CRCL, IREN, SMCI |
| 2026-09-30 | $1054.58 | AXTI, BTDR, IREN |
| 2026-10-01 | $1056.90 | RIOT |
| 2026-10-02 | $1055.05 | PATH, RIOT |
| 2026-10-05 | $1047.13 | LUNR, RIOT |

## Entry + 2 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1056.14 (+5.61%; realized $+60.54, open positions $-4.40); S&P 500 +1.19%, Nasdaq-100 +5.99%. 28 closed trades, 9 winners (32.1%), average trade 1.63%, average win 15.56%, average loss -4.97%, profit factor 1.3, worst drawdown -7.89%. Exits: target 9, stop 19. Resting orders filled: 15/39.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.02%, total $-56.93
- stopped on a later session: 14 trades, 0 won, average -4.60%, total $-143.31
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -4.60%, total $-23.11
- never rose 0.5 ATR above the entry: 16 trades, 0 won, average -4.79%, total $-164.43
- crypto-linked: 8 trades, 1 won, average -1.72%, total $-31.95
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +11.10%, total $+25.44
- bought on a dip of 0.5+ ATR (any time): 14 trades, 5 won, average +1.80%, total $+47.74
- bought less than 0.25 ATR under the prior close: 10 trades, 4 won, average +4.43%, total $+61.05
- resting limit fills: 15 trades, 4 won, average -0.78%, total $-15.58
- run entries inside the buy zone: 13 trades, 5 won, average +4.41%, total $+76.12
- support tested 3+ times: 16 trades, 5 won, average +2.27%, total $+26.12
- support tested twice: 10 trades, 4 won, average +2.86%, total $+64.44
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.02

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-23 10:05 | 42.08 | target | +15.18% | +2.32 / -0.44 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-15 11:05 | 143.7 | target | +10.12% | +2.07 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-17 9:50 | 67.3 | target | +11.10% | +2.43 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | UMAC | buy zone | 21.43 | +0.01 / -0.92 | 10.6 | 2026-09-25 12:05 | 24.9 | target | +16.19% | +2.02 / -0.06 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-09-24 14:50 | 90.76 | target | +13.68% | +2.05 / -0.29 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-25 11:20 | 17.11 | target | +10.49% | +2.65 / -0.47 |
| 2026-09-23 10:05 | PATH | buy zone | 12.71 | -0.02 / -0.55 | 6.93 | 2026-09-28 9:30 | 11.82 | stop | -7.04% | +0.62 / -1.14 |
| 2026-09-24 14:50 | BTBT (crypto) | buy zone | 1.789 | -0.35 / +0.15 | 5.29 | 2026-09-29 12:05 | 1.664 | stop | -7.01% | +0.24 / -0.92 |
| 2026-09-25 11:20 | CRCL (crypto) | buy zone | 88.43 | -0.15 / -0.69 | 2.05 | 2026-09-30 10:30 | 82.87 | stop | -6.30% | +0.11 / -0.85 |
| 2026-09-28 9:50 | AXTI | buy zone | 74.11 | -0.38 / -0.77 | 5.03 | 2026-10-05 15:50 | 86.63 | target | +16.88% | +2.20 / -0.41 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.76% | +0.07 / -0.70 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 19.32 | -1.78% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 16.71 | 14.79 | +0.04% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $953.47 | SOUN |
| 2026-08-31 | $960.07 | SMCI, SOUN |
| 2026-09-01 | $930.54 | BMNR, SMCI, SOUN |
| 2026-09-02 | $921.07 | SMCI, SOUN, WULF |
| 2026-09-03 | $943.89 | AEHR, SMCI, WULF |
| 2026-09-04 | $970.55 | AEHR, SMCI, WULF |
| 2026-09-08 | $988.07 | AEHR, DUOL, SMCI |
| 2026-09-09 | $973.59 | RGTI, SMCI |
| 2026-09-10 | $957.06 | SMCI |
| 2026-09-11 | $978.59 | NOW, SMCI |
| 2026-09-14 | $982.17 | NOW, RKLB, SMCI |
| 2026-09-15 | $977.07 | GRAB, RKLB, SMCI |
| 2026-09-16 | $985.88 | RKLB, SMCI, UMAC |
| 2026-09-17 | $1033.98 | CRWV, SMCI, UMAC |
| 2026-09-18 | $1030.37 | CRWV, RGTI, SMCI, UMAC |
| 2026-09-21 | $1075.28 | CRWV, RGTI, SMCI, UMAC |
| 2026-09-22 | $1079.79 | CRWV, RGTI, SMCI, UMAC |
| 2026-09-23 | $1070.36 | CRWV, PATH, RGTI, UMAC |
| 2026-09-24 | $1092.83 | BTBT, PATH, RGTI, UMAC |
| 2026-09-25 | $1104.67 | BTBT, CRCL, PATH |
| 2026-09-28 | $1074.61 | AXTI, BTBT, CRCL, SMCI |
| 2026-09-29 | $1071.17 | AXTI, CRCL, IREN, SMCI |
| 2026-09-30 | $1056.67 | AXTI, BTDR, IREN |
| 2026-10-01 | $1057.25 | AXTI, RIOT |
| 2026-10-02 | $1065.85 | AXTI, PATH, RIOT |
| 2026-10-05 | $1056.14 | RIOT, WULF |

## Entry + 3 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $999.31 (-0.07%; realized $-54.40, open positions $+53.71); S&P 500 +1.19%, Nasdaq-100 +5.99%. 19 closed trades, 3 winners (15.8%), average trade -0.61%, average win 20.38%, average loss -4.55%, profit factor 0.65, worst drawdown -7.89%. Exits: target 3, stop 16. Resting orders filled: 16/38.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.02%, total $-56.93
- stopped on a later session: 11 trades, 0 won, average -3.88%, total $-97.68
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -3.37%, total $-21.53
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -4.75%, total $-103.90
- crypto-linked: 5 trades, 1 won, average +0.56%, total $+7.36
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 1 won, average +6.37%, total $+28.58
- bought on a dip of 0.5+ ATR (any time): 9 trades, 1 won, average -1.89%, total $-30.03
- bought less than 0.25 ATR under the prior close: 6 trades, 2 won, average +4.88%, total $+23.88
- resting limit fills: 14 trades, 1 won, average -3.59%, total $-109.38
- run entries inside the buy zone: 5 trades, 2 won, average +7.73%, total $+54.98
- support tested 3+ times: 13 trades, 2 won, average +0.19%, total $-39.27
- support tested twice: 4 trades, 1 won, average +1.30%, total $+14.89
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.02

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-21 11:05 | 69.48 | target | +14.71% | +3.28 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.98% | +1.12 / -0.42 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-10-01 9:45 | 1.596 | stop | -4.46% | +0.51 / -0.59 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.53 | 35.01 | 44.5 | 43.19 | +18.22% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 136.1 | +4.30% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $953.47 | SOUN |
| 2026-08-31 | $960.07 | SMCI, SOUN |
| 2026-09-01 | $930.54 | BMNR, SMCI, SOUN |
| 2026-09-02 | $921.07 | SMCI, SOUN, WULF |
| 2026-09-03 | $943.89 | AEHR, SMCI, WULF |
| 2026-09-04 | $970.55 | AEHR, SMCI, WULF |
| 2026-09-08 | $988.07 | AEHR, DUOL, SMCI |
| 2026-09-09 | $973.59 | RGTI, SMCI |
| 2026-09-10 | $957.06 | SMCI |
| 2026-09-11 | $978.59 | NOW, SMCI |
| 2026-09-14 | $982.17 | NOW, RKLB, SMCI |
| 2026-09-15 | $973.82 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $975.25 | NOW, RKLB, SMCI |
| 2026-09-17 | $1011.20 | NOW, RKLB, SMCI |
| 2026-09-18 | $989.47 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $1037.67 | NOW, RGTI, SMCI |
| 2026-09-22 | $1038.49 | NOW, RGTI, SMCI |
| 2026-09-23 | $1036.87 | NOW, RGTI, SMCI |
| 2026-09-24 | $1048.19 | NOW, QUBT, RGTI, SMCI |
| 2026-09-25 | $1052.25 | NOW, QUBT, RGTI, SMCI |
| 2026-09-28 | $1015.99 | NOW, RGTI, SMCI |
| 2026-09-29 | $1002.00 | BTBT, NOW, RGTI, SMCI |
| 2026-09-30 | $1006.75 | BTBT, NOW, RGTI, SMCI |
| 2026-10-01 | $1012.08 | NOW, RGTI, SMCI |
| 2026-10-02 | $1009.71 | NOW, PATH, RGTI, SMCI |
| 2026-10-05 | $999.31 | NOW, SMCI |

