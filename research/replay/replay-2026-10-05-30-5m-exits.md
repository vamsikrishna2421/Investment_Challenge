# Replay of the rules, 2026-08-24 to 2026-10-05 (30 sessions, 5-minute bars)

$1,000 each; S&P 500 +1.19%, Nasdaq-100 +5.99% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules: hold to the target or the plan stop | +3.17% | 17 | 17.6% | 0.02% | 0.82 | -7.89% | SMCI, NOW, WULF |
| Stop to break-even after +0.5 ATR | +2.83% | 26 | 11.5% | -0.13% | 0.99 | -7.67% | UMAC, AXTI, WULF |
| Stop to break-even after +1 ATR | +0.55% | 23 | 13.0% | 0.05% | 0.85 | -6.51% | UMAC, AXTI, WULF |
| Trail 0.75 ATR under the high after +0.5 ATR | +6.56% | 40 | 37.5% | 0.78% | 1.34 | -7.58% | LUNR |
| Trail 0.5 ATR under the high after +1 ATR | +5.77% | 39 | 46.2% | 0.98% | 1.32 | -6.69% | BMNR, UMAC, LUNR, WULF |
| Trail 1 ATR under the high after +1 ATR | -3.54% | 30 | 33.3% | -0.22% | 0.81 | -6.32% | - |
| Trail 1.5 ATR under the high after +1.5 ATR | +1.77% | 30 | 33.3% | 0.55% | 0.95 | -7.89% | AXTI, WULF, RIOT, LUNR |

## Live rules: hold to the target or the plan stop: 2026-08-24 to 2026-10-05 (30 sessions)

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

## Stop to break-even after +0.5 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1028.35 (+2.83%; realized $-0.85, open positions $+29.20); S&P 500 +1.19%, Nasdaq-100 +5.99%. 26 closed trades, 3 winners (11.5%), average trade -0.13%, average win 23.54%, average loss -3.22%, profit factor 0.99, worst drawdown -7.67%. Exits: target 3, stop 16. Resting orders filled: 17/42.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -5.27%, total $-71.07
- stopped on a later session: 9 trades, 0 won, average -3.92%, total $-74.65
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -4.28%, total $-25.28
- never rose 0.5 ATR above the entry: 16 trades, 0 won, average -4.51%, total $-145.72
- crypto-linked: 7 trades, 1 won, average +0.78%, total $+11.71
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+54.53
- bought on a dip of 0.5+ ATR (any time): 8 trades, 1 won, average -0.63%, total $+4.59
- bought less than 0.25 ATR under the prior close: 9 trades, 1 won, average +0.14%, total $+1.15
- resting limit fills: 17 trades, 1 won, average -2.18%, total $-68.70
- run entries inside the buy zone: 9 trades, 2 won, average +3.73%, total $+67.85
- support tested 3+ times: 17 trades, 2 won, average +0.24%, total $-8.25
- support tested twice: 7 trades, 1 won, average +1.68%, total $+37.39
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-29.99

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-08-26 10:25 | 6.996 | protect | -0.21% | +0.61 / -0.14 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 9:45 | 1.502 | protect | -0.52% | +1.09 / -0.21 |
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-02 9:50 | 36.52 | protect | -0.06% | +0.51 / -0.31 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.64% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:30 | SMCI | limit | 36.5 | -0.24 / -0.24 | 11.13 | 2026-09-14 9:30 | 36.48 | protect | -0.06% | +2.37 / -0.35 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.38% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-28 9:30 | 129.7 | protect | -0.57% | +2.62 / -0.39 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-02 13:20 | 15.45 | protect | -0.21% | +2.65 / -0.47 |
| 2026-09-24 12:20 | STNE | buy zone | 9.328 | -0.03 / -0.41 | 9.87 | 2026-09-24 13:35 | 9.171 | stop | -1.70% | +0.00 / -0.37 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-02 12:40 | 19.63 | protect | -0.21% | +1.00 / -0.64 |
| 2026-10-02 12:50 | PATH | buy zone | 13.17 | +0.14 / -0.23 | 17.67 | 2026-10-05 11:00 | 12.81 | stop | -2.76% | +0.12 / -0.53 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| UMAC | 2026-09-16 | 21.43 | 21.43 | 26.12 | 21.83 | +1.86% |
| AXTI | 2026-09-28 | 74.11 | 74.11 | 89.34 | 86.66 | +16.94% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 17.77 | 14.79 | +0.04% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $972.95 | BTBT |
| 2026-08-27 | $977.76 | BTBT |
| 2026-08-28 | $951.73 | - |
| 2026-08-31 | $956.58 | SMCI |
| 2026-09-01 | $932.74 | AXTI, BMNR, SMCI |
| 2026-09-02 | $923.26 | AXTI, WULF |
| 2026-09-03 | $945.39 | AEHR, SMCI, WULF |
| 2026-09-04 | $982.80 | AEHR, SMCI, WULF |
| 2026-09-08 | $1004.83 | AEHR, DUOL, SMCI |
| 2026-09-09 | $1005.02 | RGTI, SMCI |
| 2026-09-10 | $988.70 | SMCI |
| 2026-09-11 | $1009.80 | NOW, SMCI |
| 2026-09-14 | $1013.75 | NOW, RKLB |
| 2026-09-15 | $1012.79 | GRAB, NOW, RKLB |
| 2026-09-16 | $1008.68 | NOW, RKLB, UMAC |
| 2026-09-17 | $1031.49 | NOW, RKLB, UMAC |
| 2026-09-18 | $1013.86 | NOW, RGTI, RKLB, UMAC |
| 2026-09-21 | $1057.73 | NOW, RGTI, RKLB, UMAC |
| 2026-09-22 | $1064.03 | NOW, RGTI, RKLB, UMAC |
| 2026-09-23 | $1049.77 | NOW, RGTI, RKLB, UMAC |
| 2026-09-24 | $1069.60 | NOW, RGTI, UMAC |
| 2026-09-25 | $1070.23 | BTBT, NOW, RGTI, UMAC |
| 2026-09-28 | $1033.66 | AXTI, BTBT, RGTI, UMAC |
| 2026-09-29 | $1042.87 | AXTI, IREN, RGTI, UMAC |
| 2026-09-30 | $1036.21 | AXTI, IREN, RGTI, UMAC |
| 2026-10-01 | $1026.95 | AXTI, RGTI, RIOT, UMAC |
| 2026-10-02 | $1034.78 | AXTI, PATH, UMAC |
| 2026-10-05 | $1028.35 | AXTI, UMAC, WULF |

## Stop to break-even after +1 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1005.47 (+0.55%; realized $-20.48, open positions $+25.95); S&P 500 +1.19%, Nasdaq-100 +5.99%. 23 closed trades, 3 winners (13.0%), average trade 0.05%, average win 22.68%, average loss -3.35%, profit factor 0.85, worst drawdown -6.51%. Exits: target 3, stop 15. Resting orders filled: 14/37.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -5.30%, total $-59.56
- stopped on a later session: 9 trades, 0 won, average -3.73%, total $-76.01
- stopped at the open (gapped through the stop): 2 trades, 0 won, average -3.38%, total $-13.84
- never rose 0.5 ATR above the entry: 14 trades, 0 won, average -4.35%, total $-124.75
- crypto-linked: 7 trades, 1 won, average +0.77%, total $+13.84
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+50.40
- bought on a dip of 0.5+ ATR (any time): 8 trades, 1 won, average -0.63%, total $-1.13
- bought less than 0.25 ATR under the prior close: 8 trades, 2 won, average +3.82%, total $+29.54
- resting limit fills: 14 trades, 1 won, average -2.14%, total $-60.95
- run entries inside the buy zone: 9 trades, 2 won, average +3.45%, total $+40.47
- support tested 3+ times: 15 trades, 2 won, average +0.57%, total $-21.11
- support tested twice: 6 trades, 1 won, average +1.98%, total $+31.10
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.47

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 9:45 | 1.502 | protect | -0.52% | +1.09 / -0.21 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-14 9:30 | 36.52 | protect | -0.06% | +1.88 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-28 9:30 | 129.7 | protect | -0.57% | +2.62 / -0.39 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-02 13:20 | 15.45 | protect | -0.21% | +2.65 / -0.47 |
| 2026-09-24 12:20 | STNE | buy zone | 9.328 | -0.03 / -0.41 | 9.87 | 2026-09-24 13:35 | 9.171 | stop | -1.70% | +0.00 / -0.37 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-02 12:40 | 19.63 | protect | -0.21% | +1.00 / -0.64 |
| 2026-10-02 12:50 | PATH | buy zone | 13.17 | +0.14 / -0.23 | 17.67 | 2026-10-05 11:00 | 12.81 | stop | -2.76% | +0.12 / -0.53 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| UMAC | 2026-09-16 | 21.43 | 21.43 | 26.12 | 21.83 | +1.86% |
| AXTI | 2026-09-28 | 74.11 | 74.11 | 89.34 | 86.66 | +16.94% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 17.77 | 14.79 | +0.04% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $967.67 | SOUN |
| 2026-08-31 | $974.34 | SMCI, SOUN |
| 2026-09-01 | $944.55 | BMNR, SMCI, SOUN |
| 2026-09-02 | $934.90 | SMCI, SOUN, WULF |
| 2026-09-03 | $957.98 | AEHR, SMCI, WULF |
| 2026-09-04 | $985.50 | AEHR, SMCI, WULF |
| 2026-09-08 | $1003.47 | AEHR, DUOL, SMCI |
| 2026-09-09 | $989.38 | RGTI, SMCI |
| 2026-09-10 | $972.60 | SMCI |
| 2026-09-11 | $994.45 | NOW, SMCI |
| 2026-09-14 | $996.63 | NOW, RKLB |
| 2026-09-15 | $995.43 | GRAB, NOW, RKLB |
| 2026-09-16 | $991.76 | NOW, RKLB, UMAC |
| 2026-09-17 | $1014.50 | NOW, RKLB, UMAC |
| 2026-09-18 | $997.47 | NOW, RGTI, RKLB, UMAC |
| 2026-09-21 | $1040.07 | NOW, RGTI, RKLB, UMAC |
| 2026-09-22 | $1045.58 | NOW, RGTI, RKLB, UMAC |
| 2026-09-23 | $1031.03 | NOW, RGTI, RKLB, UMAC |
| 2026-09-24 | $1050.59 | NOW, RGTI, UMAC |
| 2026-09-25 | $1051.28 | BTBT, NOW, RGTI, UMAC |
| 2026-09-28 | $1015.38 | AXTI, BTBT, RGTI, UMAC |
| 2026-09-29 | $1024.03 | AXTI, IREN, RGTI, UMAC |
| 2026-09-30 | $1017.33 | AXTI, IREN, RGTI, UMAC |
| 2026-10-01 | $1005.25 | AXTI, RGTI, RIOT, UMAC |
| 2026-10-02 | $1012.38 | AXTI, PATH, UMAC |
| 2026-10-05 | $1005.47 | AXTI, UMAC, WULF |

## Trail 0.75 ATR under the high after +0.5 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1065.62 (+6.56%; realized $+63.80, open positions $+1.82); S&P 500 +1.19%, Nasdaq-100 +5.99%. 40 closed trades, 15 winners (37.5%), average trade 0.78%, average win 8.38%, average loss -3.78%, profit factor 1.34, worst drawdown -7.58%. Exits: target 3, stop 19. Resting orders filled: 24/67.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -5.33%, total $-72.51
- stopped on a later session: 12 trades, 0 won, average -4.08%, total $-97.00
- stopped at the open (gapped through the stop): 6 trades, 0 won, average -4.44%, total $-47.62
- never rose 0.5 ATR above the entry: 19 trades, 0 won, average -4.54%, total $-169.51
- crypto-linked: 8 trades, 3 won, average +2.19%, total $+40.80
- bought at the open after a gap down of 0.5+ ATR: 3 trades, 2 won, average +1.39%, total $+10.01
- bought on a dip of 0.5+ ATR (any time): 18 trades, 8 won, average +0.72%, total $+19.92
- bought less than 0.25 ATR under the prior close: 10 trades, 3 won, average +1.05%, total $+30.36
- resting limit fills: 24 trades, 7 won, average -1.43%, total $-64.24
- run entries inside the buy zone: 15 trades, 7 won, average +4.04%, total $+115.72
- run entries on a bounce (touched the zone, back above it): 1 trade, 1 won, average +5.04%, total $+12.32
- support tested 3+ times: 25 trades, 10 won, average +1.38%, total $+59.27
- support tested twice: 13 trades, 5 won, average +1.23%, total $+34.70
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.17

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-08-26 10:40 | 6.926 | protect | -1.20% | +0.61 / -0.22 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 9:30 | 1.55 | protect | +2.64% | +1.09 / -0.21 |
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-02 10:10 | 35.87 | protect | -1.82% | +0.51 / -0.31 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.64% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:30 | SMCI | limit | 36.5 | -0.24 / -0.24 | 11.13 | 2026-09-04 15:10 | 39.3 | protect | +7.65% | +2.08 / -0.35 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-04 15:20 | BULL | buy zone | 9.785 | -0.40 / -0.34 | 4.28 | 2026-09-08 15:35 | 9.44 | stop | -3.53% | +0.36 / -0.52 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-15 15:05 | 142.6 | protect | +9.29% | +2.62 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-15 9:50 | 63.53 | protect | +4.87% | +1.79 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-18 9:35 | 39.32 | protect | +5.04% | +1.61 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | UMAC | buy zone | 21.43 | +0.01 / -0.92 | 10.6 | 2026-09-18 9:40 | 23.12 | protect | +7.88% | +1.73 / -0.06 |
| 2026-09-18 9:50 | LUNR | buy zone | 14.15 | +0.14 / -0.80 | 4.62 | 2026-09-22 11:20 | 15.71 | target | +10.98% | +2.10 / -0.45 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-23 9:35 | 16.38 | protect | +5.82% | +2.65 / -0.47 |
| 2026-09-22 11:20 | AXTI | buy zone | 75.39 | -0.55 / -0.76 | 3.4 | 2026-09-23 15:15 | 74.22 | protect | -1.57% | +0.56 / -0.25 |
| 2026-09-23 9:50 | OKLO | buy zone | 39.47 | -0.09 / -0.39 | 3.09 | 2026-09-24 9:30 | 37.94 | stop | -3.90% | +0.26 / -0.62 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-25 10:00 | 8.985 | protect | +1.41% | +1.12 / +0.00 |
| 2026-09-24 9:30 | BTBT (crypto) | limit | 1.725 | -0.35 / -0.35 | 7.71 | 2026-09-25 10:00 | 1.715 | protect | -0.62% | +0.74 / -0.19 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-28 9:30 | 16.42 | protect | +4.96% | +1.78 / -0.04 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 10:00 | 28.58 | protect | +4.31% | +1.60 / -0.01 |
| 2026-09-25 10:05 | BTBT (crypto) | buy zone | 1.714 | +0.09 / -0.65 | 25.29 | 2026-09-28 10:40 | 1.699 | protect | -0.88% | +0.70 / -0.29 |
| 2026-09-28 9:30 | NOW | limit | 129.8 | -1.05 / -1.05 | 4.94 | 2026-09-28 9:35 | 127.1 | stop | -2.12% | +0.00 / -0.55 |
| 2026-09-28 9:50 | AXTI | buy zone | 74.11 | -0.38 / -0.77 | 5.03 | 2026-09-30 9:35 | 79.23 | protect | +6.90% | +1.57 / -0.41 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-09-30 10:15 | 1.633 | protect | -2.22% | +0.51 / -0.25 |
| 2026-09-30 9:50 | WULF (crypto) | buy zone | 14.71 | +0.18 / -0.37 | 4.14 | 2026-10-02 11:40 | 15.44 | protect | +4.97% | +1.50 / -0.34 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |
| 2026-10-02 11:50 | QBTS | buy zone | 16.42 | +0.43 / -0.14 | 1.89 | 2026-10-05 9:30 | 15.46 | stop | -5.87% | +0.09 / -1.11 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 14.29 | +1.07% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $970.53 | BTBT |
| 2026-08-27 | $975.34 | BTBT |
| 2026-08-28 | $957.02 | - |
| 2026-08-31 | $961.90 | SMCI |
| 2026-09-01 | $937.92 | AXTI, BMNR, SMCI |
| 2026-09-02 | $924.17 | AXTI, WULF |
| 2026-09-03 | $946.41 | AEHR, SMCI, WULF |
| 2026-09-04 | $981.10 | AEHR, BULL, WULF |
| 2026-09-08 | $994.85 | AEHR, DUOL |
| 2026-09-09 | $999.89 | RGTI, SMR |
| 2026-09-10 | $985.21 | - |
| 2026-09-11 | $989.10 | NOW |
| 2026-09-14 | $1011.23 | NOW, RKLB, SMCI |
| 2026-09-15 | $1004.30 | GRAB, SMCI |
| 2026-09-16 | $1012.80 | SMCI, UMAC |
| 2026-09-17 | $1048.09 | SMCI, UMAC |
| 2026-09-18 | $1037.78 | LUNR, RGTI |
| 2026-09-21 | $1075.81 | LUNR, RGTI |
| 2026-09-22 | $1078.62 | AXTI, RGTI |
| 2026-09-23 | $1068.96 | OKLO |
| 2026-09-24 | $1106.96 | BTBT, HIMS, QUBT, RGTI |
| 2026-09-25 | $1093.88 | BTBT, RGTI |
| 2026-09-28 | $1077.05 | AXTI, SMCI |
| 2026-09-29 | $1075.37 | AXTI, BTBT, SMCI |
| 2026-09-30 | $1071.62 | WULF |
| 2026-10-01 | $1072.82 | WULF |
| 2026-10-02 | $1072.18 | PATH, QBTS |
| 2026-10-05 | $1065.62 | LUNR |

## Trail 0.5 ATR under the high after +1 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1057.69 (+5.77%; realized $+61.57, open positions $-3.88); S&P 500 +1.19%, Nasdaq-100 +5.99%. 39 closed trades, 18 winners (46.2%), average trade 0.98%, average win 7.43%, average loss -4.54%, profit factor 1.32, worst drawdown -6.69%. Exits: target 2, stop 21. Resting orders filled: 18/50.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -6.04%, total $-72.39
- stopped on a later session: 15 trades, 0 won, average -3.94%, total $-118.76
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -4.71%, total $-45.65
- never rose 0.5 ATR above the entry: 18 trades, 0 won, average -4.56%, total $-157.27
- crypto-linked: 8 trades, 3 won, average +1.07%, total $+25.04
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 2 won, average +4.27%, total $+21.18
- bought on a dip of 0.5+ ATR (any time): 17 trades, 8 won, average +0.32%, total $+1.09
- bought less than 0.25 ATR under the prior close: 12 trades, 7 won, average +4.22%, total $+84.79
- resting limit fills: 18 trades, 7 won, average -1.19%, total $-36.43
- run entries inside the buy zone: 17 trades, 7 won, average +2.51%, total $+63.11
- run entries on a bounce (touched the zone, back above it): 4 trades, 4 won, average +4.31%, total $+34.89
- support tested 3+ times: 25 trades, 12 won, average +1.83%, total $+65.49
- support tested twice: 12 trades, 6 won, average +0.99%, total $+26.49
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.41

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-27 13:40 | 1.586 | protect | +4.99% | +1.09 / -0.21 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-04 15:00 | 39.56 | protect | +8.28% | +1.65 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-04 15:05 | BULL | buy zone | 9.795 | -0.40 / -0.32 | 4.12 | 2026-09-08 15:35 | 9.44 | stop | -3.63% | +0.34 / -0.54 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-14 9:45 | 137.8 | protect | +5.62% | +1.64 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-15 9:45 | 64.25 | protect | +6.06% | +1.79 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-17 12:05 | 39.87 | protect | +6.51% | +1.61 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 15:20 | UMAC | buy zone | 21.43 | +0.01 / -0.92 | 10.6 | 2026-09-18 9:35 | 23.56 | protect | +9.91% | +1.73 / -0.06 |
| 2026-09-17 12:05 | CRWV | buy zone | 80.47 | -0.35 / -0.53 | 5.04 | 2026-09-22 10:55 | 86.45 | protect | +7.42% | +1.60 / -0.36 |
| 2026-09-18 9:50 | LUNR | buy zone | 14.15 | +0.14 / -0.80 | 4.62 | 2026-09-21 9:55 | 14.82 | protect | +4.67% | +1.37 / -0.45 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-21 12:35 | 16.12 | protect | +4.11% | +1.31 / -0.47 |
| 2026-09-21 10:05 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-23 10:25 | 9.778 | protect | +1.98% | +1.01 / -0.13 |
| 2026-09-22 11:05 | AXTI | buy zone | 75.73 | -0.55 / -0.70 | 3.06 | 2026-09-24 9:30 | 70.06 | stop | -7.50% | +0.50 / -1.02 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-24 15:15 | 9.081 | protect | +2.48% | +1.12 / +0.00 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-25 13:35 | 16.8 | protect | +7.39% | +1.78 / -0.04 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 9:30 | 28.93 | protect | +5.58% | +1.60 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-09-25 9:50 | AXTI | bounce | 76.94 | +0.24 / +0.16 | 2.1 | 2026-09-30 9:35 | 80.38 | protect | +4.46% | +1.11 / -0.85 |
| 2026-09-25 15:50 | QUBT | buy zone | 9.018 | -0.27 / -0.36 | 1.98 | 2026-09-28 10:45 | 8.676 | stop | -3.84% | +0.00 / -0.90 |
| 2026-09-28 10:50 | SMCI | buy zone | 41 | -0.20 / -0.97 | 20.7 | 2026-09-30 11:55 | 40.49 | stop | -1.25% | +0.73 / -0.22 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-09-30 10:05 | AXTI | bounce | 76.78 | +0.25 / -0.22 | 2.19 | 2026-10-01 14:05 | 80.07 | protect | +4.28% | +1.02 / -0.23 |
| 2026-09-30 12:05 | RGTI | buy zone | 15.91 | +0.14 / +0.18 | 1.99 | 2026-10-05 9:30 | 15.08 | stop | -5.26% | +0.22 / -1.14 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-02 10:50 | 20.37 | protect | +3.56% | +1.00 / -0.64 |
| 2026-10-02 10:50 | PATH | buy zone | 13.17 | +0.14 / -0.23 | 17.97 | 2026-10-05 11:00 | 12.81 | stop | -2.72% | +0.13 / -0.53 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| BMNR | 2026-09-23 | 27.67 | 25.71 | 31.94 | 26.79 | -3.19% |
| UMAC | 2026-10-01 | 21.85 | 20.96 | 26.18 | 21.83 | -0.07% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 14.29 | +1.07% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 17.77 | 14.79 | +0.04% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $984.83 | SOUN |
| 2026-08-28 | $965.83 | SOUN |
| 2026-08-31 | $972.49 | SMCI, SOUN |
| 2026-09-01 | $942.73 | BMNR, SMCI, SOUN |
| 2026-09-02 | $933.11 | SMCI, SOUN, WULF |
| 2026-09-03 | $956.16 | AEHR, SMCI, WULF |
| 2026-09-04 | $982.13 | AEHR, BULL, WULF |
| 2026-09-08 | $989.01 | AEHR, DUOL |
| 2026-09-09 | $980.59 | RGTI, SMR |
| 2026-09-10 | $966.01 | - |
| 2026-09-11 | $969.82 | NOW |
| 2026-09-14 | $983.10 | RKLB, SMCI |
| 2026-09-15 | $978.68 | GRAB, SMCI |
| 2026-09-16 | $986.78 | SMCI, UMAC |
| 2026-09-17 | $1016.01 | CRWV, UMAC |
| 2026-09-18 | $1019.07 | CRWV, LUNR, RGTI |
| 2026-09-21 | $1051.39 | CRWV, STNE |
| 2026-09-22 | $1062.26 | AXTI, STNE |
| 2026-09-23 | $1043.49 | AXTI, BMNR |
| 2026-09-24 | $1062.77 | BMNR, HIMS, RGTI |
| 2026-09-25 | $1070.06 | AXTI, BMNR, BTBT, QUBT |
| 2026-09-28 | $1042.22 | AXTI, BMNR, BTBT, SMCI |
| 2026-09-29 | $1047.20 | AXTI, BMNR, IREN, SMCI |
| 2026-09-30 | $1047.26 | AXTI, BMNR, IREN, RGTI |
| 2026-10-01 | $1052.94 | BMNR, RGTI, RIOT, UMAC |
| 2026-10-02 | $1063.42 | BMNR, PATH, RGTI, UMAC |
| 2026-10-05 | $1057.69 | BMNR, LUNR, UMAC, WULF |

## Trail 1 ATR under the high after +1 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $964.64 (-3.54%; realized $-35.35, open positions $-0.01); S&P 500 +1.19%, Nasdaq-100 +5.99%. 30 closed trades, 10 winners (33.3%), average trade -0.22%, average win 8.16%, average loss -4.42%, profit factor 0.81, worst drawdown -6.32%. Exits: target 2, stop 19. Resting orders filled: 24/69.

### What the trades had in common

- stopped the session it was bought: 8 trades, 0 won, average -4.85%, total $-75.40
- stopped on a later session: 11 trades, 0 won, average -4.45%, total $-112.85
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -5.85%, total $-40.61
- never rose 0.5 ATR above the entry: 17 trades, 0 won, average -4.69%, total $-168.80
- crypto-linked: 7 trades, 3 won, average +1.54%, total $+27.98
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 1 won, average +1.57%, total $+7.70
- bought on a dip of 0.5+ ATR (any time): 13 trades, 3 won, average -2.25%, total $-55.40
- bought less than 0.25 ATR under the prior close: 10 trades, 5 won, average +4.37%, total $+61.99
- resting limit fills: 24 trades, 8 won, average -1.80%, total $-90.50
- run entries inside the buy zone: 6 trades, 2 won, average +6.10%, total $+55.15
- support tested 3+ times: 20 trades, 7 won, average +0.54%, total $-16.95
- support tested twice: 8 trades, 3 won, average +0.21%, total $+12.13
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.53

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 9:35 | 1.515 | protect | +0.29% | +1.09 / -0.21 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-09 15:25 | 38.86 | protect | +6.35% | +1.88 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-10 9:50 | NBIS | limit | 229.6 | -0.61 / -0.79 | 5.66 | 2026-09-14 9:30 | 204.9 | stop | -10.79% | +0.38 / -1.89 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-16 9:30 | 139.1 | protect | +6.63% | +2.62 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-15 10:05 | 62.81 | protect | +3.69% | +1.79 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-16 9:50 | BULL | buy zone | 8.225 | -0.29 / -0.85 | 11.78 | 2026-09-16 10:55 | 8.057 | stop | -2.06% | +0.03 / -0.32 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-23 9:35 | 16.38 | protect | +5.82% | +2.65 / -0.47 |
| 2026-09-22 11:05 | PATH | limit | 13.27 | +0.36 / -0.32 | 8.83 | 2026-09-23 10:05 | 12.65 | stop | -4.69% | +0.24 / -0.62 |
| 2026-09-23 9:30 | CLSK (crypto) | limit | 15.01 | -0.14 / -0.14 | 6.87 | 2026-09-23 15:55 | 14.43 | stop | -3.90% | +0.19 / -0.62 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 9:30 | 8.812 | protect | -0.55% | +1.12 / -0.21 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-28 9:30 | 16.33 | protect | +4.43% | +1.78 / -0.04 |
| 2026-09-24 9:30 | BTBT (crypto) | limit | 1.725 | -0.35 / -0.35 | 7.71 | 2026-09-29 12:05 | 1.664 | stop | -3.57% | +0.74 / -0.43 |
| 2026-09-24 10:10 | STNE | limit | 9.43 | -0.03 / -0.15 | 4.4 | 2026-09-24 13:35 | 9.171 | stop | -2.76% | +0.00 / -0.64 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-29 9:40 | NOW | limit | 130.4 | -0.11 / -0.18 | 4.94 | 2026-10-01 10:45 | 135.2 | protect | +3.62% | +1.87 / -0.42 |
| 2026-09-30 9:40 | WULF (crypto) | limit | 14.55 | +0.18 / -0.53 | 5.23 | 2026-10-02 13:10 | 15.19 | protect | +4.37% | +1.65 / -0.19 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.57 | BTBT, SOUN |
| 2026-08-28 | $969.61 | SOUN |
| 2026-08-31 | $976.30 | SMCI, SOUN |
| 2026-09-01 | $946.47 | BMNR, SMCI, SOUN |
| 2026-09-02 | $936.80 | SMCI, SOUN, WULF |
| 2026-09-03 | $959.92 | AEHR, SMCI, WULF |
| 2026-09-04 | $987.55 | AEHR, SMCI, WULF |
| 2026-09-08 | $1005.58 | AEHR, DUOL, SMCI |
| 2026-09-09 | $991.03 | RGTI |
| 2026-09-10 | $982.85 | NBIS |
| 2026-09-11 | $982.89 | NBIS, NOW |
| 2026-09-14 | $988.16 | NOW, RKLB |
| 2026-09-15 | $984.16 | GRAB, NOW |
| 2026-09-16 | $973.70 | - |
| 2026-09-17 | $973.70 | - |
| 2026-09-18 | $978.10 | RGTI |
| 2026-09-21 | $990.21 | RGTI |
| 2026-09-22 | $989.68 | PATH, RGTI |
| 2026-09-23 | $967.07 | - |
| 2026-09-24 | $990.99 | BTBT, QUBT, RGTI |
| 2026-09-25 | $983.80 | BTBT, QUBT, RGTI |
| 2026-09-28 | $962.80 | BTBT, SMCI |
| 2026-09-29 | $955.27 | NOW, SMCI |
| 2026-09-30 | $963.89 | NOW, WULF |
| 2026-10-01 | $967.84 | WULF |
| 2026-10-02 | $970.35 | PATH |
| 2026-10-05 | $964.64 | - |

## Trail 1.5 ATR under the high after +1.5 ATR: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1017.71 (+1.77%; realized $-10.38, open positions $+28.09); S&P 500 +1.19%, Nasdaq-100 +5.99%. 30 closed trades, 10 winners (33.3%), average trade 0.55%, average win 11.25%, average loss -4.8%, profit factor 0.95, worst drawdown -7.89%. Exits: target 6, stop 20. Resting orders filled: 15/38.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.02%, total $-56.93
- stopped on a later session: 15 trades, 0 won, average -4.40%, total $-146.18
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -4.43%, total $-38.43
- never rose 0.5 ATR above the entry: 16 trades, 0 won, average -4.61%, total $-147.20
- crypto-linked: 7 trades, 1 won, average -0.98%, total $-9.11
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +6.06%, total $+14.57
- bought on a dip of 0.5+ ATR (any time): 15 trades, 6 won, average +0.96%, total $+19.87
- bought less than 0.25 ATR under the prior close: 9 trades, 4 won, average +3.82%, total $+35.86
- resting limit fills: 15 trades, 4 won, average -2.65%, total $-82.00
- run entries inside the buy zone: 13 trades, 5 won, average +3.87%, total $+57.94
- run entries on a bounce (touched the zone, back above it): 2 trades, 1 won, average +2.98%, total $+13.68
- support tested 3+ times: 18 trades, 6 won, average +1.84%, total $+21.11
- support tested twice: 10 trades, 4 won, average +0.27%, total $-1.47
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
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-10 15:55 | 37.53 | protect | +2.72% | +1.88 / -0.34 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.66% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 11:20 | AEHR | buy zone | 78.88 | -0.11 / -0.12 | 2.89 | 2026-09-09 10:05 | 101.3 | target | +28.35% | +2.06 / -0.39 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-17 9:30 | 137.7 | protect | +5.54% | +2.62 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-18 10:05 | 64.25 | protect | +6.06% | +2.79 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-21 10:20 | 41.33 | target | +10.43% | +1.82 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-10-02 10:05 | 91.76 | target | +14.92% | +2.37 / -0.29 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-23 9:35 | 16.38 | protect | +5.82% | +2.65 / -0.47 |
| 2026-09-18 10:05 | LUNR | buy zone | 13.98 | +0.14 / -1.02 | 10.47 | 2026-09-22 11:20 | 15.71 | target | +12.38% | +2.32 / -0.23 |
| 2026-09-21 10:20 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-24 13:40 | 9.158 | stop | -4.46% | +1.01 / -0.98 |
| 2026-09-22 11:20 | AXTI | buy zone | 75.39 | -0.55 / -0.76 | 3.4 | 2026-09-24 9:30 | 70.06 | stop | -7.08% | +0.56 / -0.97 |
| 2026-09-23 9:50 | OKLO | buy zone | 39.47 | -0.09 / -0.39 | 3.09 | 2026-09-24 9:30 | 37.94 | stop | -3.90% | +0.26 / -0.62 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.61% | +0.07 / -0.90 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-10-02 10:05 | PATH | buy zone | 13.25 | +0.14 / -0.10 | 13.84 | 2026-10-05 11:00 | 12.81 | stop | -3.35% | +0.00 / -0.66 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| AXTI | 2026-09-30 | 75.92 | 78.4 | 89.31 | 86.66 | +14.14% |
| WULF | 2026-09-30 | 14.84 | 13.94 | 17.76 | 14.79 | -0.33% |
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
| 2026-09-04 | $970.55 | AEHR, SMCI, WULF |
| 2026-09-08 | $988.07 | AEHR, DUOL, SMCI |
| 2026-09-09 | $973.59 | RGTI, SMCI |
| 2026-09-10 | $958.03 | - |
| 2026-09-11 | $961.81 | NOW |
| 2026-09-14 | $983.32 | NOW, RKLB, SMCI |
| 2026-09-15 | $975.42 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $976.72 | NOW, RKLB, SMCI |
| 2026-09-17 | $1011.45 | CRWV, RKLB, SMCI |
| 2026-09-18 | $995.03 | CRWV, LUNR, RGTI, SMCI |
| 2026-09-21 | $1047.72 | CRWV, LUNR, RGTI, STNE |
| 2026-09-22 | $1061.25 | AXTI, CRWV, RGTI, STNE |
| 2026-09-23 | $1030.16 | AXTI, CRWV, OKLO, STNE |
| 2026-09-24 | $1029.28 | CRWV, HIMS |
| 2026-09-25 | $1031.56 | BTBT, CRCL, CRWV |
| 2026-09-28 | $1011.29 | BTBT, CRCL, CRWV, SMCI |
| 2026-09-29 | $1003.15 | CRCL, CRWV, IREN, SMCI |
| 2026-09-30 | $1001.44 | AXTI, CRWV, IREN, WULF |
| 2026-10-01 | $1011.86 | AXTI, CRWV, RIOT, WULF |
| 2026-10-02 | $1028.54 | AXTI, PATH, RIOT, WULF |
| 2026-10-05 | $1017.71 | AXTI, LUNR, RIOT, WULF |

