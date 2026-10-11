# Replay of the rules, 2026-08-28 to 2026-10-09 (30 sessions, 5-minute bars)

$1,000 each; S&P 500 +0.97%, Nasdaq-100 +4.18% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules: limits at support, stop 0.6 ATR under it | +5.27% | 18 | 16.7% | -0.13% | 0.96 | -6.29% | SMCI, NOW, APLD |
| Limits at the zone top | +0.16% | 19 | 21.1% | -2.03% | 0.74 | -7.33% | SMCI, NOW |
| No resting limits: run entries only (the Oct 5 rules) | +1.43% | 21 | 23.8% | 0.14% | 0.76 | -6.86% | SMCI, NOW, APLD |
| Resting limits only, no run entries | -5.40% | 15 | 6.7% | -3.48% | 0.27 | -9.34% | SMCI, NOW, APLD |
| Stop 1.0 ATR under support | -6.20% | 8 | 12.5% | -5.38% | 0.16 | -7.74% | SMCI, COIN, GPUS, POET |
| Stop 1.5 ATR under support | -2.86% | 6 | 16.7% | -8.39% | 0.43 | -7.74% | SMCI, WULF, APLD |
| Sell after 3 sessions if neither target nor stop | -5.36% | 36 | 30.6% | -0.62% | 0.75 | -8.67% | SMCI, APLD, NNE |
| Bitcoin gate off | +5.34% | 18 | 16.7% | -0.12% | 0.96 | -6.22% | SMCI, NOW, APLD |
| Rank run entries by R:R instead of dip | +5.15% | 18 | 16.7% | -0.17% | 0.95 | -6.29% | SMCI, NOW, APLD |
| Opening gap-down 0.5+ ATR, sell at the prior close or the close | -13.74% | 38 | 39.5% | -1.52% | 0.28 | -13.74% | - |
| Limits cancelled at 10:00 (the first 30 minutes), runs after | -3.62% | 28 | 21.4% | -1.33% | 0.64 | -11.27% | SMCI, APLD, NNE, GPUS |
| GPUS, IREN, BTDR only with a tested support | +10.02% | 18 | 22.2% | 1.12% | 1.32 | -5.48% | SMCI, NOW, APLD |
| Both of the above | +14.27% | 24 | 29.2% | 1.5% | 1.42 | -6.73% | SMCI, NOW, APLD |
| Both, stop 1.0 ATR under support | -0.94% | 7 | 14.3% | -2.49% | 0.2 | -5.38% | SMCI, COIN, HIMX, NOW |
| Run entries only, GPUS/IREN/BTDR only with a tested support | +10.28% | 27 | 25.9% | 0.92% | 1.31 | -8.92% | SMCI, APLD, NNE |

## Live rules: limits at support, stop 0.6 ATR under it: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1052.65 (+5.27%; realized $-6.32, open positions $+58.97); S&P 500 +0.97%, Nasdaq-100 +4.18%. 18 closed trades, 3 winners (16.7%), average trade -0.13%, average win 23.36%, average loss -4.83%, profit factor 0.96, worst drawdown -6.29%. Exits: target 3, stop 15. Resting orders filled: 16/33.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -6.23%, total $-76.04
- stopped on a later session: 9 trades, 0 won, average -3.90%, total $-76.84
- stopped at the open (gapped through the stop): 6 trades, 0 won, average -4.03%, total $-55.47
- never rose 0.5 ATR above the entry: 13 trades, 0 won, average -4.98%, total $-132.77
- crypto-linked: 6 trades, 1 won, average -0.24%, total $-6.13
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.04%, total $+52.28
- bought on a dip of 0.5+ ATR (any time): 7 trades, 1 won, average -0.77%, total $+2.35
- bought less than 0.25 ATR under the prior close: 5 trades, 1 won, average +0.05%, total $-2.25
- resting limit fills: 13 trades, 1 won, average -3.35%, total $-90.05
- run entries inside the buy zone: 5 trades, 2 won, average +8.24%, total $+83.73
- support tested 3+ times: 12 trades, 2 won, average +0.49%, total $-9.62
- support tested twice: 4 trades, 1 won, average +2.75%, total $+33.98
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.68

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.64% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.38% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.04% | +4.49 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-08 9:30 | 13.92 | stop | -4.35% | +1.68 / -0.76 |
| 2026-10-06 10:40 | RCAT | limit | 6.32 | +0.11 / -0.07 | 8.06 | 2026-10-07 9:30 | 6.09 | stop | -3.66% | +0.33 / -0.77 |
| 2026-10-08 9:35 | APLD | limit | 23.55 | +0.35 / -0.17 | 5.53 | 2026-10-08 13:25 | 22.61 | stop | -3.98% | +0.15 / -0.60 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 140.9 | +7.96% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.81 | - |
| 2026-08-31 | $978.57 | SMCI |
| 2026-09-01 | $954.15 | AXTI, BMNR, SMCI |
| 2026-09-02 | $947.74 | AXTI, SMCI, WULF |
| 2026-09-03 | $967.46 | AEHR, SMCI, WULF |
| 2026-09-04 | $1004.98 | AEHR, SMCI, WULF |
| 2026-09-08 | $1027.16 | AEHR, DUOL, SMCI |
| 2026-09-09 | $1025.84 | RGTI, SMCI |
| 2026-09-10 | $1008.79 | SMCI |
| 2026-09-11 | $1030.99 | NOW, SMCI |
| 2026-09-14 | $1034.41 | NOW, RKLB, SMCI |
| 2026-09-15 | $1025.90 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $1027.20 | NOW, RKLB, SMCI |
| 2026-09-17 | $1064.86 | NOW, RKLB, SMCI |
| 2026-09-18 | $1041.87 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $1094.44 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $1103.77 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $1095.27 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $1111.59 | NOW, RGTI, SMCI |
| 2026-09-25 | $1123.31 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $1081.16 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $1068.28 | NOW, RGTI, SMCI |
| 2026-09-30 | $1076.48 | NOW, RGTI, SMCI |
| 2026-10-01 | $1094.14 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $1104.22 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $1086.53 | NOW, SMCI, WULF |
| 2026-10-06 | $1096.15 | NOW, RCAT, SMCI, WULF |
| 2026-10-07 | $1084.98 | NOW, SMCI, WULF |
| 2026-10-08 | $1055.14 | NOW, SMCI |
| 2026-10-09 | $1052.65 | APLD, NOW, SMCI |

## Limits at the zone top: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1001.63 (+0.16%; realized $-45.92, open positions $+47.55); S&P 500 +0.97%, Nasdaq-100 +4.18%. 19 closed trades, 4 winners (21.1%), average trade -2.03%, average win 15.16%, average loss -6.61%, profit factor 0.74, worst drawdown -7.33%. Exits: target 4, stop 15. Resting orders filled: 12/25.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -7.19%, total $-69.08
- stopped on a later session: 9 trades, 0 won, average -6.22%, total $-107.47
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -5.20%, total $-47.03
- never rose 0.5 ATR above the entry: 12 trades, 0 won, average -6.92%, total $-136.45
- crypto-linked: 6 trades, 2 won, average +2.41%, total $+23.24
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -2.12%, total $-5.53
- bought on a dip of 0.5+ ATR (any time): 8 trades, 3 won, average +2.84%, total $+42.95
- bought less than 0.25 ATR under the prior close: 10 trades, 1 won, average -5.32%, total $-80.57
- resting limit fills: 10 trades, 0 won, average -7.73%, total $-127.26
- run entries inside the buy zone: 9 trades, 4 won, average +4.31%, total $+81.34
- support tested 3+ times: 11 trades, 2 won, average -1.80%, total $-40.57
- support tested twice: 5 trades, 2 won, average +3.85%, total $+33.02
- radar keeps (GPUS, IREN, BTDR) without a tested support: 3 trades, 0 won, average -12.65%, total $-38.37

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 3.97 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 9:30 | BTBT (crypto) | limit | 1.56 | -0.07 / -0.20 | 4.27 | 2026-08-28 14:35 | 1.417 | stop | -9.18% | +0.00 / -0.95 |
| 2026-08-28 14:20 | SBET (crypto) | buy zone | 8.166 | -0.52 / -1.55 | 4.0 | 2026-09-21 9:50 | 9.78 | target | +19.75% | +4.22 / -0.77 |
| 2026-09-01 9:50 | GPUS | limit | 0.2711 | -0.05 / -0.24 | 5.09 | 2026-09-01 14:45 | 0.2366 | stop | -12.82% | +0.00 / -0.96 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.64% | +0.14 / -0.28 |
| 2026-09-02 9:30 | GPUS | limit | 0.2245 | -0.42 / -0.42 | 5.99 | 2026-09-02 11:10 | 0.2067 | stop | -8.02% | +0.37 / -0.54 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-03 9:50 | GPUS | limit | 0.2011 | +0.42 / +0.03 | 7.19 | 2026-09-24 9:35 | 0.1669 | stop | -17.11% | +0.20 / -0.94 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.32% | +0.37 / -0.79 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.51% | +0.64 / -0.85 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.61% | +1.65 / -0.71 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 2.69 | 2026-09-24 13:40 | 9.158 | stop | -4.11% | +1.10 / -0.90 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 9:30 | BTBT (crypto) | limit | 1.78 | +0.09 / -0.09 | 5.71 | 2026-09-29 12:05 | 1.671 | stop | -6.14% | +0.13 / -0.94 |
| 2026-09-28 9:30 | NOW | limit | 129.8 | -1.05 / -1.05 | 2.96 | 2026-09-28 9:35 | 127.1 | stop | -2.12% | +0.00 / -0.55 |
| 2026-09-30 9:35 | WULF (crypto) | limit | 14.86 | +0.18 / -0.22 | 3.14 | 2026-10-08 9:30 | 13.91 | stop | -6.41% | +1.35 / -1.05 |
| 2026-10-02 9:30 | PATH | limit | 13.41 | +0.14 / +0.14 | 8.73 | 2026-10-05 11:00 | 12.81 | stop | -4.53% | +0.00 / -0.90 |
| 2026-10-08 9:30 | APLD | limit | 24.02 | +0.35 / +0.14 | 3.33 | 2026-10-08 13:25 | 22.61 | stop | -5.86% | +0.15 / -0.90 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-28 | 37.4 | 35 | 50.6 | 41.86 | +11.93% |
| NOW | 2026-09-29 | 130.8 | 127.1 | 146.9 | 140.9 | +7.67% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $973.33 | SBET, SMCI |
| 2026-08-31 | $982.89 | SBET, SMCI |
| 2026-09-01 | $955.66 | BMNR, SBET, SMCI |
| 2026-09-02 | $950.93 | SBET, SMCI, WULF |
| 2026-09-03 | $992.04 | GPUS, SBET, SMCI, WULF |
| 2026-09-04 | $1001.66 | GPUS, SBET, SMCI, WULF |
| 2026-09-08 | $1017.56 | DUOL, GPUS, SBET, SMCI |
| 2026-09-09 | $1001.11 | GPUS, QBTS, SBET, SMCI |
| 2026-09-10 | $978.13 | GPUS, QBTS, SBET, SMCI |
| 2026-09-11 | $1005.94 | GPUS, QBTS, SBET, SMCI |
| 2026-09-14 | $974.90 | AEHR, GPUS, SBET, SMCI |
| 2026-09-15 | $942.94 | AEHR, GPUS, SBET, SMCI |
| 2026-09-16 | $946.88 | AEHR, GPUS, SBET, SMCI |
| 2026-09-17 | $991.66 | AEHR, GPUS, SBET, SMCI |
| 2026-09-18 | $1012.98 | AEHR, GPUS, SBET, SMCI |
| 2026-09-21 | $1052.52 | AEHR, GPUS, SMCI, STNE |
| 2026-09-22 | $1063.85 | AXTI, GPUS, SMCI, STNE |
| 2026-09-23 | $1037.30 | AXTI, GPUS, SMCI, STNE |
| 2026-09-24 | $1039.94 | HIMS, SMCI |
| 2026-09-25 | $1051.40 | BTBT, SMCI |
| 2026-09-28 | $1024.93 | BTBT, SMCI |
| 2026-09-29 | $1017.06 | NOW, SMCI |
| 2026-09-30 | $1024.35 | NOW, SMCI, WULF |
| 2026-10-01 | $1038.83 | NOW, SMCI, WULF |
| 2026-10-02 | $1047.15 | NOW, PATH, SMCI, WULF |
| 2026-10-05 | $1029.75 | NOW, SMCI, WULF |
| 2026-10-06 | $1038.11 | NOW, SMCI, WULF |
| 2026-10-07 | $1037.77 | NOW, SMCI, WULF |
| 2026-10-08 | $1005.15 | NOW, SMCI |
| 2026-10-09 | $1001.63 | NOW, SMCI |

## No resting limits: run entries only (the Oct 5 rules): 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1014.30 (+1.43%; realized $-39.66, open positions $+53.96); S&P 500 +0.97%, Nasdaq-100 +4.18%. 21 closed trades, 5 winners (23.8%), average trade 0.14%, average win 16.13%, average loss -4.85%, profit factor 0.76, worst drawdown -6.86%. Exits: target 5, stop 16.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -3.43%, total $-48.89
- stopped on a later session: 10 trades, 0 won, average -5.71%, total $-116.25
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -6.45%, total $-39.89
- never rose 0.5 ATR above the entry: 9 trades, 0 won, average -4.26%, total $-80.67
- crypto-linked: 5 trades, 2 won, average +3.65%, total $+10.85
- bought on a dip of 0.5+ ATR (any time): 13 trades, 3 won, average -0.54%, total $-33.93
- bought less than 0.25 ATR under the prior close: 3 trades, 1 won, average +6.47%, total $+12.52
- run entries inside the buy zone: 20 trades, 5 won, average +0.42%, total $-26.51
- run entries on a bounce (touched the zone, back above it): 1 trade, 0 won, average -5.42%, total $-13.15
- support tested 3+ times: 14 trades, 3 won, average +0.43%, total $-23.31
- support tested twice: 6 trades, 2 won, average +1.22%, total $-0.58
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -10.38%, total $-15.77

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:50 | NNE | buy zone | 18.78 | -0.13 / -0.37 | 7.46 | 2026-08-28 10:05 | 18.32 | stop | -2.41% | +0.00 / -0.41 |
| 2026-08-28 9:50 | LUNR | buy zone | 15.82 | -0.12 / -0.24 | 10.52 | 2026-08-28 14:20 | 15.18 | stop | -4.04% | +0.02 / -0.43 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.86% | +0.00 / -0.80 |
| 2026-08-28 9:50 | IONQ | buy zone | 40.51 | -0.27 / -0.71 | 3.44 | 2026-09-01 9:30 | 37.85 | stop | -6.57% | +0.07 / -1.03 |
| 2026-08-28 10:05 | BTDR (crypto) | buy zone | 10.38 | -0.25 / -0.88 | 2.57 | 2026-09-03 10:35 | 11.79 | target | +13.53% | +1.36 / -0.28 |
| 2026-08-31 9:50 | MARA (crypto) | buy zone | 10.43 | +0.11 / -0.26 | 2.36 | 2026-09-11 10:05 | 12.17 | target | +16.73% | +2.06 / -0.46 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-03 10:35 | GPUS | buy zone | 0.186 | +0.42 / -0.38 | 14.74 | 2026-09-24 9:35 | 0.1669 | stop | -10.38% | +0.61 / -0.54 |
| 2026-09-08 10:20 | DUOL | buy zone | 146.6 | -0.26 / -1.06 | 3.31 | 2026-09-09 10:15 | 140.8 | stop | -3.95% | +0.07 / -0.91 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.52% | +0.64 / -0.85 |
| 2026-09-11 10:05 | GRAL | buy zone | 77.28 | +0.01 / -0.06 | 1.81 | 2026-09-21 9:50 | 98.6 | target | +27.57% | +5.45 / -0.86 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.61% | +1.65 / -0.71 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 2.69 | 2026-09-24 13:40 | 9.158 | stop | -4.11% | +1.10 / -0.90 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.26% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 9:50 | IREN (crypto) | buy zone | 44.44 | +0.02 / -0.62 | 4.8 | 2026-09-25 10:00 | 43.55 | stop | -2.00% | +0.01 / -0.32 |
| 2026-09-25 9:50 | BTDR (crypto) | buy zone | 11.72 | +0.06 / -0.51 | 5.82 | 2026-09-25 10:00 | 11.47 | stop | -2.17% | +0.00 / -0.34 |
| 2026-09-28 9:50 | POET | buy zone | 7.515 | -0.54 / -0.57 | 7.47 | 2026-09-28 10:45 | 7.359 | stop | -2.08% | +0.01 / -0.43 |
| 2026-09-28 9:50 | BBAI | bounce | 2.764 | -0.41 / -0.30 | 1.55 | 2026-10-02 11:20 | 2.614 | stop | -5.42% | +0.78 / -1.19 |
| 2026-09-28 9:50 | AXTI | buy zone | 74.11 | -0.38 / -0.77 | 5.03 | 2026-10-08 15:45 | 71 | stop | -4.20% | +2.27 / -0.49 |
| 2026-10-05 9:50 | LUNR | buy zone | 14.14 | -0.04 / -0.55 | 2.26 | 2026-10-09 11:05 | 13.32 | stop | -5.79% | +1.13 / -0.79 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 37.23 | 35.01 | 50.6 | 41.86 | +12.44% |
| NOW | 2026-09-29 | 130.6 | 127.1 | 146.9 | 140.9 | +7.82% |
| APLD | 2026-10-09 | 23.28 | 22.64 | 28.67 | 23.68 | +1.71% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $958.58 | BTDR, IONQ |
| 2026-08-31 | $967.94 | BTDR, IONQ, MARA, SMCI |
| 2026-09-01 | $945.01 | BTDR, MARA, SMCI, SOUN |
| 2026-09-02 | $950.26 | BTDR, MARA, SMCI, SOUN |
| 2026-09-03 | $982.87 | GPUS, MARA, SMCI, SOUN |
| 2026-09-04 | $988.33 | GPUS, MARA, SMCI, SOUN |
| 2026-09-08 | $995.20 | DUOL, GPUS, MARA, SMCI |
| 2026-09-09 | $993.67 | GPUS, MARA, QBTS, SMCI |
| 2026-09-10 | $959.75 | GPUS, MARA, QBTS, SMCI |
| 2026-09-11 | $991.92 | GPUS, GRAL, QBTS, SMCI |
| 2026-09-14 | $959.01 | AEHR, GPUS, GRAL, SMCI |
| 2026-09-15 | $939.42 | AEHR, GPUS, GRAL, SMCI |
| 2026-09-16 | $945.15 | AEHR, GPUS, GRAL, SMCI |
| 2026-09-17 | $992.04 | AEHR, GPUS, GRAL, SMCI |
| 2026-09-18 | $993.16 | AEHR, GPUS, GRAL, SMCI |
| 2026-09-21 | $1054.46 | AEHR, GPUS, SMCI, STNE |
| 2026-09-22 | $1060.53 | AXTI, GPUS, SMCI, STNE |
| 2026-09-23 | $1033.97 | AXTI, GPUS, SMCI, STNE |
| 2026-09-24 | $1037.63 | HIMS, SMCI |
| 2026-09-25 | $1042.01 | SMCI |
| 2026-09-28 | $1016.43 | AXTI, BBAI, SMCI |
| 2026-09-29 | $1025.14 | AXTI, BBAI, NOW, SMCI |
| 2026-09-30 | $1030.67 | AXTI, BBAI, NOW, SMCI |
| 2026-10-01 | $1066.80 | AXTI, BBAI, NOW, SMCI |
| 2026-10-02 | $1074.83 | AXTI, NOW, SMCI |
| 2026-10-05 | $1080.17 | AXTI, LUNR, NOW, SMCI |
| 2026-10-06 | $1088.99 | AXTI, LUNR, NOW, SMCI |
| 2026-10-07 | $1072.72 | AXTI, LUNR, NOW, SMCI |
| 2026-10-08 | $1019.93 | LUNR, NOW, SMCI |
| 2026-10-09 | $1014.30 | APLD, NOW, SMCI |

## Resting limits only, no run entries: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $945.95 (-5.40%; realized $-110.83, open positions $+56.78); S&P 500 +0.97%, Nasdaq-100 +4.18%. 15 closed trades, 1 winners (6.7%), average trade -3.48%, average win 21.04%, average loss -5.23%, profit factor 0.27, worst drawdown -9.34%. Exits: target 1, stop 14. Resting orders filled: 18/37.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -6.91%, total $-67.19
- stopped on a later session: 9 trades, 0 won, average -4.30%, total $-85.19
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -4.45%, total $-67.37
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -5.55%, total $-124.20
- crypto-linked: 3 trades, 0 won, average -5.02%, total $-36.19
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.04%, total $+41.55
- bought on a dip of 0.5+ ATR (any time): 4 trades, 1 won, average +0.60%, total $+3.01
- bought less than 0.25 ATR under the prior close: 5 trades, 0 won, average -4.48%, total $-52.03
- resting limit fills: 15 trades, 1 won, average -3.48%, total $-110.83
- support tested 3+ times: 10 trades, 0 won, average -4.73%, total $-106.77
- support tested twice: 3 trades, 1 won, average +4.79%, total $+26.61
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.67

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.04% | +4.49 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.36% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-08 9:30 | 13.92 | stop | -4.36% | +1.68 / -0.76 |
| 2026-10-06 10:40 | RCAT | limit | 6.32 | +0.11 / -0.07 | 8.06 | 2026-10-07 9:30 | 6.09 | stop | -3.66% | +0.33 / -0.77 |
| 2026-10-08 9:35 | APLD | limit | 23.55 | +0.35 / -0.17 | 5.53 | 2026-10-08 13:25 | 22.61 | stop | -3.98% | +0.15 / -0.60 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 140.9 | +7.96% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.81 | - |
| 2026-08-31 | $978.57 | SMCI |
| 2026-09-01 | $953.52 | AXTI, SMCI |
| 2026-09-02 | $942.85 | AXTI, SMCI |
| 2026-09-03 | $941.43 | SMCI |
| 2026-09-04 | $950.17 | RCAT, SMCI |
| 2026-09-08 | $963.69 | RCAT, SMCI |
| 2026-09-09 | $931.51 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $906.65 | SMCI |
| 2026-09-11 | $928.44 | NOW, SMCI |
| 2026-09-14 | $928.52 | NOW, RKLB, SMCI |
| 2026-09-15 | $919.69 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $921.61 | NOW, RKLB, SMCI |
| 2026-09-17 | $956.08 | NOW, RKLB, SMCI |
| 2026-09-18 | $935.96 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $982.39 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $990.13 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $983.11 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $996.42 | NOW, RGTI, SMCI |
| 2026-09-25 | $1008.08 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $969.67 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $957.62 | NOW, RGTI, SMCI |
| 2026-09-30 | $965.02 | NOW, RGTI, SMCI |
| 2026-10-01 | $981.13 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $990.83 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $975.25 | NOW, SMCI, WULF |
| 2026-10-06 | $983.85 | NOW, RCAT, SMCI, WULF |
| 2026-10-07 | $976.01 | NOW, SMCI, WULF |
| 2026-10-08 | $948.81 | NOW, SMCI |
| 2026-10-09 | $945.95 | APLD, NOW, SMCI |

## Stop 1.0 ATR under support: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $938.03 (-6.20%; realized $-83.74, open positions $+21.77); S&P 500 +0.97%, Nasdaq-100 +4.18%. 8 closed trades, 1 winners (12.5%), average trade -5.38%, average win 13.01%, average loss -8.01%, profit factor 0.16, worst drawdown -7.74%. Exits: target 1, stop 7. Resting orders filled: 4/7.

### What the trades had in common

- stopped on a later session: 7 trades, 0 won, average -8.01%, total $-99.89
- stopped at the open (gapped through the stop): 2 trades, 0 won, average -8.42%, total $-32.57
- never rose 0.5 ATR above the entry: 3 trades, 0 won, average -11.21%, total $-45.52
- crypto-linked: 2 trades, 0 won, average -8.26%, total $-31.17
- bought on a dip of 0.5+ ATR (any time): 5 trades, 1 won, average -4.39%, total $-39.77
- bought less than 0.25 ATR under the prior close: 2 trades, 0 won, average -7.33%, total $-28.54
- resting limit fills: 3 trades, 0 won, average -11.21%, total $-45.52
- run entries inside the buy zone: 5 trades, 1 won, average -1.89%, total $-38.22
- support tested 3+ times: 7 trades, 1 won, average -4.04%, total $-68.35
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -14.77%, total $-15.39

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 3.89 | 2026-09-01 9:50 | 14.59 | stop | -8.80% | +0.00 / -0.93 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 4.35 | 2026-09-01 9:30 | 1.359 | stop | -10.05% | +0.14 / -1.02 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 2.28 | 2026-09-10 9:30 | 6.337 | stop | -6.79% | +0.82 / -1.45 |
| 2026-09-01 9:50 | QUBT | buy zone | 7.956 | -0.49 / -0.57 | 1.59 | 2026-09-21 9:50 | 8.992 | target | +13.01% | +2.30 / -0.68 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 4.88 | 2026-09-02 9:40 | 0.2218 | stop | -14.77% | +0.00 / -1.01 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 4.36 | 2026-09-11 10:20 | 150.8 | stop | -3.33% | +1.54 / -0.84 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 1.83 | 2026-10-01 11:05 | 8.992 | stop | -5.85% | +1.10 / -1.31 |
| 2026-10-01 11:05 | WULF (crypto) | buy zone | 14.45 | +0.10 / -0.35 | 3.8 | 2026-10-08 11:05 | 13.52 | stop | -6.47% | +1.78 / -0.97 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 33.95 | 50.6 | 41.86 | +15.41% |
| COIN | 2026-09-02 | 177.8 | 157.5 | 209.1 | 179.4 | +0.91% |
| GPUS | 2026-09-11 | 0.1818 | 0.1321 | 0.4407 | 0.16 | -11.99% |
| POET | 2026-10-08 | 7.104 | 6.734 | 8.3 | 6.97 | -1.89% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $985.27 | BTBT, LUNR |
| 2026-08-31 | $990.84 | BTBT, LUNR, SMCI |
| 2026-09-01 | $965.33 | GPUS, QUBT, SMCI, SOUN |
| 2026-09-02 | $954.08 | COIN, QUBT, SMCI, SOUN |
| 2026-09-03 | $972.08 | COIN, QUBT, SMCI, SOUN |
| 2026-09-04 | $976.77 | COIN, QUBT, SMCI, SOUN |
| 2026-09-08 | $973.55 | COIN, QUBT, SMCI, SOUN |
| 2026-09-09 | $956.96 | COIN, QUBT, SMCI, SOUN |
| 2026-09-10 | $933.12 | COIN, ORCL, QUBT, SMCI |
| 2026-09-11 | $952.30 | COIN, GPUS, QUBT, SMCI |
| 2026-09-14 | $947.53 | COIN, GPUS, QUBT, SMCI |
| 2026-09-15 | $922.62 | COIN, GPUS, QUBT, SMCI |
| 2026-09-16 | $923.63 | COIN, GPUS, QUBT, SMCI |
| 2026-09-17 | $956.95 | COIN, GPUS, QUBT, SMCI |
| 2026-09-18 | $968.43 | COIN, GPUS, QUBT, SMCI |
| 2026-09-21 | $996.64 | COIN, GPUS, SMCI, STNE |
| 2026-09-22 | $999.51 | COIN, GPUS, SMCI, STNE |
| 2026-09-23 | $984.61 | COIN, GPUS, SMCI, STNE |
| 2026-09-24 | $980.26 | COIN, GPUS, SMCI, STNE |
| 2026-09-25 | $987.87 | COIN, GPUS, SMCI, STNE |
| 2026-09-28 | $976.41 | COIN, GPUS, SMCI, STNE |
| 2026-09-29 | $968.27 | COIN, GPUS, SMCI, STNE |
| 2026-09-30 | $967.49 | COIN, GPUS, SMCI, STNE |
| 2026-10-01 | $973.09 | COIN, GPUS, SMCI, WULF |
| 2026-10-02 | $990.97 | COIN, GPUS, SMCI, WULF |
| 2026-10-05 | $977.49 | COIN, GPUS, SMCI, WULF |
| 2026-10-06 | $980.20 | COIN, GPUS, SMCI, WULF |
| 2026-10-07 | $973.90 | COIN, GPUS, SMCI, WULF |
| 2026-10-08 | $940.26 | COIN, GPUS, POET, SMCI |
| 2026-10-09 | $938.03 | COIN, GPUS, POET, SMCI |

## Stop 1.5 ATR under support: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $971.41 (-2.86%; realized $-43.19, open positions $+14.60); S&P 500 +0.97%, Nasdaq-100 +4.18%. 6 closed trades, 1 winners (16.7%), average trade -8.39%, average win 18.27%, average loss -13.73%, profit factor 0.43, worst drawdown -7.74%. Exits: target 1, stop 5. Resting orders filled: 5/10.

### What the trades had in common

- stopped on a later session: 5 trades, 0 won, average -13.73%, total $-76.44
- stopped at the open (gapped through the stop): 1 trade, 0 won, average -14.07%, total $-15.32
- never rose 0.5 ATR above the entry: 3 trades, 0 won, average -14.88%, total $-46.77
- crypto-linked: 1 trade, 0 won, average -14.92%, total $-15.47
- bought on a dip of 0.5+ ATR (any time): 2 trades, 0 won, average -18.40%, total $-30.71
- bought less than 0.25 ATR under the prior close: 4 trades, 1 won, average -3.39%, total $-12.48
- resting limit fills: 4 trades, 0 won, average -14.99%, total $-60.23
- run entries inside the buy zone: 1 trade, 1 won, average +18.27%, total $+33.25
- run entries on a bounce (touched the zone, back above it): 1 trade, 0 won, average -8.68%, total $-16.21
- support tested 3+ times: 4 trades, 0 won, average -11.69%, total $-61.20
- support tested twice: 1 trade, 1 won, average +18.27%, total $+33.25
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -21.88%, total $-15.24

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 2.59 | 2026-09-14 9:30 | 13.75 | stop | -14.07% | +0.02 / -1.56 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 2.88 | 2026-10-09 15:55 | 1.285 | stop | -14.92% | +2.51 / -1.56 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 3.25 | 2026-09-02 11:15 | 0.2033 | stop | -21.88% | +0.00 / -1.55 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 7.75 | 2026-10-08 9:50 | 14.21 | stop | -9.08% | +1.99 / -1.43 |
| 2026-09-14 9:50 | RKLB | buy zone | 62.28 | -0.73 / -0.23 | 2.1 | 2026-09-24 12:20 | 73.66 | target | +18.27% | +4.00 / -0.19 |
| 2026-09-24 12:20 | QUBT | bounce | 9.133 | -0.68 / +0.03 | 6.9 | 2026-10-01 10:05 | 8.341 | stop | -8.68% | +0.41 / -2.07 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 32.62 | 50.6 | 41.86 | +15.41% |
| WULF | 2026-10-01 | 14.53 | 13.04 | 17.75 | 13.77 | -5.26% |
| APLD | 2026-10-08 | 23.46 | 21.24 | 28.66 | 23.68 | +0.93% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $990.22 | BTBT, LUNR |
| 2026-08-31 | $993.95 | BTBT, LUNR, SMCI |
| 2026-09-01 | $975.91 | BTBT, GPUS, LUNR, SMCI |
| 2026-09-02 | $971.50 | BTBT, LUNR, SMCI |
| 2026-09-03 | $990.17 | BTBT, LUNR, SMCI |
| 2026-09-04 | $998.09 | BTBT, LUNR, SMCI |
| 2026-09-08 | $1010.66 | BTBT, LUNR, SMCI |
| 2026-09-09 | $993.96 | BTBT, LUNR, RGTI, SMCI |
| 2026-09-10 | $978.27 | BTBT, LUNR, RGTI, SMCI |
| 2026-09-11 | $989.84 | BTBT, LUNR, RGTI, SMCI |
| 2026-09-14 | $969.09 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-15 | $961.94 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-16 | $961.88 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-17 | $1005.99 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-18 | $1003.17 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-21 | $1040.56 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-22 | $1050.60 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-23 | $1034.01 | BTBT, RGTI, RKLB, SMCI |
| 2026-09-24 | $1050.91 | BTBT, QUBT, RGTI, SMCI |
| 2026-09-25 | $1052.96 | BTBT, QUBT, RGTI, SMCI |
| 2026-09-28 | $1026.81 | BTBT, QUBT, RGTI, SMCI |
| 2026-09-29 | $1017.53 | BTBT, QUBT, RGTI, SMCI |
| 2026-09-30 | $1016.14 | BTBT, QUBT, RGTI, SMCI |
| 2026-10-01 | $1019.12 | BTBT, RGTI, SMCI, WULF |
| 2026-10-02 | $1028.79 | BTBT, RGTI, SMCI, WULF |
| 2026-10-05 | $1012.46 | BTBT, RGTI, SMCI, WULF |
| 2026-10-06 | $1014.17 | BTBT, RGTI, SMCI, WULF |
| 2026-10-07 | $1003.90 | BTBT, RGTI, SMCI, WULF |
| 2026-10-08 | $979.92 | APLD, BTBT, SMCI, WULF |
| 2026-10-09 | $971.41 | APLD, SMCI, WULF |

## Sell after 3 sessions if neither target nor stop: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $946.36 (-5.36%; realized $-59.07, open positions $+5.43); S&P 500 +0.97%, Nasdaq-100 +4.18%. 36 closed trades, 11 winners (30.6%), average trade -0.62%, average win 7.36%, average loss -4.13%, profit factor 0.75, worst drawdown -8.67%. Exits: stop 23, time 13. Resting orders filled: 35/77.

### What the trades had in common

- stopped the session it was bought: 11 trades, 0 won, average -4.90%, total $-116.83
- stopped on a later session: 12 trades, 0 won, average -3.74%, total $-106.23
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -4.11%, total $-45.11
- never rose 0.5 ATR above the entry: 21 trades, 0 won, average -4.40%, total $-206.93
- crypto-linked: 7 trades, 2 won, average -0.40%, total $-7.30
- bought at the open after a gap down of 0.5+ ATR: 3 trades, 1 won, average +0.46%, total $+3.32
- bought on a dip of 0.5+ ATR (any time): 11 trades, 3 won, average -0.89%, total $-25.79
- bought less than 0.25 ATR under the prior close: 12 trades, 4 won, average +0.58%, total $+13.75
- resting limit fills: 32 trades, 8 won, average -1.90%, total $-131.48
- run entries inside the buy zone: 4 trades, 3 won, average +9.60%, total $+72.41
- support tested 3+ times: 26 trades, 7 won, average -0.59%, total $-57.23
- support tested twice: 8 trades, 4 won, average +1.53%, total $+28.84
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.68

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-08-31 9:30 | SMCI | limit | 36.27 | -0.30 / -0.30 | 8.81 | 2026-09-02 15:55 | 36.98 | time | +1.95% | +0.61 / -0.24 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.64% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-04 15:55 | 16.49 | time | +14.61% | +1.87 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:30 | SMCI | limit | 36.5 | -0.24 / -0.24 | 11.13 | 2026-09-08 15:55 | 40.23 | time | +10.22% | +2.37 / -0.35 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-08 15:55 | 90.74 | time | +17.35% | +1.58 / -0.25 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:15 | RCAT | limit | 8.47 | -0.21 / -0.42 | 6.47 | 2026-09-09 15:50 | 8.133 | stop | -3.98% | +0.07 / -0.63 |
| 2026-09-09 10:15 | QBTS | limit | 17.06 | -0.16 / -0.57 | 7.24 | 2026-09-11 15:55 | 16.78 | time | -1.67% | +0.58 / -0.49 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-15 15:55 | 141.8 | time | +8.69% | +2.62 / -0.01 |
| 2026-09-14 9:30 | QUBT | limit | 7.72 | -0.73 / -0.73 | 4.36 | 2026-09-14 9:30 | 7.624 | stop | -1.25% | +0.00 / -0.24 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-16 15:55 | 63.66 | time | +4.61% | +1.69 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-16 15:20 | UMAC | buy zone | 21.43 | +0.01 / -0.92 | 10.6 | 2026-09-18 15:55 | 23.17 | time | +8.09% | +1.73 / -0.06 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-22 15:55 | 16.49 | time | +6.50% | +1.33 / -0.47 |
| 2026-09-22 11:05 | PATH | limit | 13.27 | +0.36 / -0.32 | 8.83 | 2026-09-23 10:05 | 12.65 | stop | -4.69% | +0.24 / -0.62 |
| 2026-09-23 9:30 | CLSK (crypto) | limit | 15.01 | -0.14 / -0.14 | 6.87 | 2026-09-23 15:55 | 14.43 | stop | -3.90% | +0.19 / -0.62 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.98% | +1.12 / -0.42 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-28 15:55 | 15.93 | time | +1.83% | +1.78 / -0.04 |
| 2026-09-24 9:30 | BTBT (crypto) | limit | 1.725 | -0.35 / -0.35 | 7.71 | 2026-09-28 15:55 | 1.677 | time | -2.82% | +0.74 / -0.35 |
| 2026-09-24 10:10 | STNE | limit | 9.43 | -0.03 / -0.15 | 4.4 | 2026-09-24 13:35 | 9.171 | stop | -2.76% | +0.00 / -0.64 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-29 9:40 | NOW | limit | 130.4 | -0.11 / -0.18 | 4.94 | 2026-10-01 15:55 | 137.7 | time | +5.57% | +1.87 / -0.42 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-10-01 9:45 | 1.596 | stop | -4.46% | +0.51 / -0.59 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-05 15:55 | 14.78 | time | +1.58% | +1.68 / -0.19 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |
| 2026-10-06 10:40 | RCAT | limit | 6.32 | +0.11 / -0.07 | 8.06 | 2026-10-07 9:30 | 6.09 | stop | -3.66% | +0.33 / -0.77 |
| 2026-10-07 9:30 | UMAC | limit | 21.6 | -0.46 / -0.46 | 4.2 | 2026-10-07 9:35 | 20.82 | stop | -3.62% | +0.00 / -0.51 |
| 2026-10-07 9:30 | QUBT | limit | 7.66 | -0.45 / -0.45 | 4.07 | 2026-10-08 11:10 | 7.38 | stop | -3.66% | +0.00 / -0.61 |
| 2026-10-08 9:30 | POET | limit | 7.17 | -0.45 / -0.57 | 4.36 | 2026-10-08 13:00 | 6.897 | stop | -3.82% | +0.20 / -0.66 |
| 2026-10-08 9:35 | APLD | limit | 23.55 | +0.35 / -0.17 | 5.53 | 2026-10-08 13:25 | 22.61 | stop | -3.98% | +0.15 / -0.60 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-10-08 | 41.9 | 40.63 | 50.76 | 41.86 | -0.10% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |
| NNE | 2026-10-09 | 15.05 | 14.51 | 17.01 | 15.34 | +1.93% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.81 | - |
| 2026-08-31 | $978.57 | SMCI |
| 2026-09-01 | $954.15 | AXTI, BMNR, SMCI |
| 2026-09-02 | $947.60 | AXTI, WULF |
| 2026-09-03 | $970.24 | AEHR, SMCI, WULF |
| 2026-09-04 | $1008.39 | AEHR, SMCI |
| 2026-09-08 | $1022.75 | - |
| 2026-09-09 | $1005.21 | QBTS, RGTI, SMR |
| 2026-09-10 | $983.23 | QBTS |
| 2026-09-11 | $988.83 | NOW |
| 2026-09-14 | $1011.19 | NOW, RKLB |
| 2026-09-15 | $1009.96 | GRAB, RKLB |
| 2026-09-16 | $1010.17 | UMAC |
| 2026-09-17 | $1020.22 | UMAC |
| 2026-09-18 | $1020.99 | RGTI |
| 2026-09-21 | $1033.67 | RGTI |
| 2026-09-22 | $1032.55 | PATH |
| 2026-09-23 | $1010.75 | - |
| 2026-09-24 | $1035.75 | BTBT, QUBT, RGTI |
| 2026-09-25 | $1028.24 | BTBT, QUBT, RGTI |
| 2026-09-28 | $995.56 | SMCI |
| 2026-09-29 | $987.15 | BTBT, NOW, SMCI |
| 2026-09-30 | $988.81 | BTBT, NOW |
| 2026-10-01 | $996.84 | WULF |
| 2026-10-02 | $1004.62 | PATH, WULF |
| 2026-10-05 | $986.66 | - |
| 2026-10-06 | $987.44 | RCAT |
| 2026-10-07 | $967.41 | QUBT |
| 2026-10-08 | $945.95 | SMCI |
| 2026-10-09 | $946.36 | APLD, NNE, SMCI |

## Bitcoin gate off: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1053.43 (+5.34%; realized $-5.54, open positions $+58.97); S&P 500 +0.97%, Nasdaq-100 +4.18%. 18 closed trades, 3 winners (16.7%), average trade -0.12%, average win 23.36%, average loss -4.81%, profit factor 0.96, worst drawdown -6.22%. Exits: target 3, stop 15. Resting orders filled: 16/33.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -6.17%, total $-75.26
- stopped on a later session: 9 trades, 0 won, average -3.90%, total $-76.84
- stopped at the open (gapped through the stop): 6 trades, 0 won, average -4.03%, total $-55.47
- never rose 0.5 ATR above the entry: 13 trades, 0 won, average -4.96%, total $-131.99
- crypto-linked: 7 trades, 1 won, average -0.73%, total $-15.34
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.04%, total $+52.28
- bought on a dip of 0.5+ ATR (any time): 7 trades, 1 won, average -0.77%, total $+2.35
- bought less than 0.25 ATR under the prior close: 4 trades, 1 won, average +1.05%, total $+7.74
- resting limit fills: 13 trades, 1 won, average -3.33%, total $-89.27
- run entries inside the buy zone: 5 trades, 2 won, average +8.24%, total $+83.73
- support tested 3+ times: 12 trades, 2 won, average +0.52%, total $-8.84
- support tested twice: 4 trades, 1 won, average +2.75%, total $+33.98
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.68

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | BMNR (crypto) | buy zone | 23.27 | -0.62 / -1.37 | 9.02 | 2026-09-02 9:30 | 22.89 | stop | -1.64% | +0.14 / -0.28 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.38% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.04% | +4.49 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-08 9:30 | 13.92 | stop | -4.35% | +1.68 / -0.76 |
| 2026-10-06 10:40 | RCAT | limit | 6.32 | +0.11 / -0.07 | 8.06 | 2026-10-07 9:30 | 6.09 | stop | -3.66% | +0.33 / -0.77 |
| 2026-10-08 9:30 | CORZ (crypto) | limit | 15.71 | -0.23 / -0.25 | 6.18 | 2026-10-08 12:50 | 15.13 | stop | -3.67% | +0.00 / -0.71 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 140.9 | +7.96% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.81 | - |
| 2026-08-31 | $978.57 | SMCI |
| 2026-09-01 | $954.15 | AXTI, BMNR, SMCI |
| 2026-09-02 | $947.74 | AXTI, SMCI, WULF |
| 2026-09-03 | $967.46 | AEHR, SMCI, WULF |
| 2026-09-04 | $1004.98 | AEHR, SMCI, WULF |
| 2026-09-08 | $1027.16 | AEHR, DUOL, SMCI |
| 2026-09-09 | $1025.84 | RGTI, SMCI |
| 2026-09-10 | $1008.79 | SMCI |
| 2026-09-11 | $1030.99 | NOW, SMCI |
| 2026-09-14 | $1034.41 | NOW, RKLB, SMCI |
| 2026-09-15 | $1025.90 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $1027.20 | NOW, RKLB, SMCI |
| 2026-09-17 | $1064.86 | NOW, RKLB, SMCI |
| 2026-09-18 | $1041.87 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $1094.44 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $1103.77 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $1095.27 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $1111.59 | NOW, RGTI, SMCI |
| 2026-09-25 | $1123.31 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $1081.16 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $1068.28 | NOW, RGTI, SMCI |
| 2026-09-30 | $1076.48 | NOW, RGTI, SMCI |
| 2026-10-01 | $1094.14 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $1104.22 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $1086.53 | NOW, SMCI, WULF |
| 2026-10-06 | $1096.15 | NOW, RCAT, SMCI, WULF |
| 2026-10-07 | $1084.98 | NOW, SMCI, WULF |
| 2026-10-08 | $1055.92 | NOW, SMCI |
| 2026-10-09 | $1053.43 | APLD, NOW, SMCI |

## Rank run entries by R:R instead of dip: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1051.52 (+5.15%; realized $-7.44, open positions $+58.96); S&P 500 +0.97%, Nasdaq-100 +4.18%. 18 closed trades, 3 winners (16.7%), average trade -0.17%, average win 23.36%, average loss -4.88%, profit factor 0.95, worst drawdown -6.29%. Exits: target 3, stop 15. Resting orders filled: 16/33.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -6.20%, total $-75.55
- stopped on a later session: 9 trades, 0 won, average -4.00%, total $-78.04
- stopped at the open (gapped through the stop): 6 trades, 0 won, average -4.18%, total $-56.68
- never rose 0.5 ATR above the entry: 13 trades, 0 won, average -5.04%, total $-133.50
- crypto-linked: 4 trades, 1 won, average +0.76%, total $+3.35
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.04%, total $+52.17
- bought on a dip of 0.5+ ATR (any time): 5 trades, 1 won, average -0.19%, total $+11.77
- bought less than 0.25 ATR under the prior close: 5 trades, 1 won, average +0.05%, total $-2.25
- resting limit fills: 13 trades, 1 won, average -3.35%, total $-90.05
- run entries inside the buy zone: 5 trades, 2 won, average +8.10%, total $+82.61
- support tested 3+ times: 11 trades, 2 won, average +0.71%, total $-3.93
- support tested twice: 5 trades, 1 won, average +1.67%, total $+27.15
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-30.66

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-01 14:50 | RCAT | buy zone | 8.292 | -0.35 / -0.40 | 13.3 | 2026-09-02 9:30 | 8.083 | stop | -2.53% | +0.06 / -0.32 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.38% | +0.37 / -0.79 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 10:05 | IONQ | buy zone | 39.54 | -0.36 / -0.35 | 8.15 | 2026-09-09 10:15 | 38.5 | stop | -2.63% | +0.00 / -0.46 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.04% | +4.49 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-08 9:30 | 13.92 | stop | -4.35% | +1.68 / -0.76 |
| 2026-10-06 10:40 | RCAT | limit | 6.32 | +0.11 / -0.07 | 8.06 | 2026-10-07 9:30 | 6.09 | stop | -3.66% | +0.33 / -0.77 |
| 2026-10-08 9:35 | APLD | limit | 23.55 | +0.35 / -0.17 | 5.53 | 2026-10-08 13:25 | 22.61 | stop | -3.98% | +0.15 / -0.60 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 140.9 | +7.96% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.81 | - |
| 2026-08-31 | $978.57 | SMCI |
| 2026-09-01 | $952.81 | AXTI, RCAT, SMCI |
| 2026-09-02 | $946.49 | AXTI, SMCI, WULF |
| 2026-09-03 | $966.19 | AEHR, SMCI, WULF |
| 2026-09-04 | $1003.60 | AEHR, SMCI, WULF |
| 2026-09-08 | $1025.73 | AEHR, DUOL, SMCI |
| 2026-09-09 | $1024.76 | RGTI, SMCI |
| 2026-09-10 | $1007.71 | SMCI |
| 2026-09-11 | $1029.91 | NOW, SMCI |
| 2026-09-14 | $1033.29 | NOW, RKLB, SMCI |
| 2026-09-15 | $1024.78 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $1026.09 | NOW, RKLB, SMCI |
| 2026-09-17 | $1063.72 | NOW, RKLB, SMCI |
| 2026-09-18 | $1040.76 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $1093.26 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $1102.58 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $1094.10 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $1110.38 | NOW, RGTI, SMCI |
| 2026-09-25 | $1122.10 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $1079.99 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $1067.11 | NOW, RGTI, SMCI |
| 2026-09-30 | $1075.30 | NOW, RGTI, SMCI |
| 2026-10-01 | $1092.95 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $1103.03 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $1085.36 | NOW, SMCI, WULF |
| 2026-10-06 | $1094.97 | NOW, RCAT, SMCI, WULF |
| 2026-10-07 | $1083.83 | NOW, SMCI, WULF |
| 2026-10-08 | $1054.02 | NOW, SMCI |
| 2026-10-09 | $1051.52 | APLD, NOW, SMCI |

## Opening gap-down 0.5+ ATR, sell at the prior close or the close: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $862.58 (-13.74%; realized $-137.44, open positions $+0.02); S&P 500 +0.97%, Nasdaq-100 +4.18%. 38 closed trades, 15 winners (39.5%), average trade -1.52%, average win 1.57%, average loss -3.54%, profit factor 0.28, worst drawdown -13.74%. Exits: neutral 2, close 36.

### What the trades had in common

- never rose 0.5 ATR above the entry: 28 trades, 7 won, average -2.38%, total $-156.64
- crypto-linked: 14 trades, 4 won, average -2.28%, total $-75.79
- bought at the open after a gap down of 0.5+ ATR: 38 trades, 15 won, average -1.52%, total $-137.44
- bought on a dip of 0.5+ ATR (any time): 36 trades, 14 won, average -1.52%, total $-129.03

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | IREN (crypto) | gap | 37.61 | -0.90 / -0.90 | 0 | 2026-08-28 15:55 | 35.41 | close | -5.86% | +0.13 / -0.86 |
| 2026-08-28 9:30 | SBET (crypto) | gap | 8.659 | -0.52 / -0.48 | 0 | 2026-08-28 15:55 | 8.194 | close | -5.39% | +0.21 / -1.18 |
| 2026-08-31 9:30 | AFRM | gap | 75.68 | -0.53 / -0.52 | 0 | 2026-08-31 15:55 | 74.37 | close | -1.73% | +0.32 / -1.11 |
| 2026-09-01 9:30 | ORCL | gap | 143.8 | -0.91 / -0.90 | 0 | 2026-09-01 15:55 | 141.2 | close | -1.76% | +0.51 / -0.64 |
| 2026-09-01 9:30 | SBET (crypto) | gap | 8.307 | -0.67 / -0.64 | 0 | 2026-09-01 15:55 | 8.139 | close | -2.03% | +0.30 / -0.46 |
| 2026-09-01 9:30 | HIMX | gap | 13.35 | -0.63 / -0.59 | 0 | 2026-09-01 15:55 | 13.39 | close | +0.34% | +0.24 / -0.20 |
| 2026-09-01 9:30 | BMNR (crypto) | gap | 24.4 | -0.62 / -0.61 | 0 | 2026-09-01 15:55 | 23.38 | close | -4.18% | +0.12 / -0.90 |
| 2026-09-04 9:30 | PATH | gap | 16.27 | -2.61 / -2.57 | 0 | 2026-09-04 15:55 | 15.17 | close | -6.76% | +0.58 / -1.98 |
| 2026-09-04 9:30 | MSTR (crypto) | gap | 137.3 | -0.77 / -0.76 | 0 | 2026-09-04 15:55 | 142.6 | close | +3.87% | +0.72 / -0.02 |
| 2026-09-04 9:30 | CRCL (crypto) | gap | 98.03 | -0.71 / -0.70 | 0 | 2026-09-04 15:55 | 101.9 | close | +3.99% | +0.64 / -0.13 |
| 2026-09-04 9:30 | SBET (crypto) | gap | 8.637 | -0.62 / -0.59 | 0 | 2026-09-04 15:55 | 8.663 | close | +0.29% | +0.11 / -0.50 |
| 2026-09-08 9:30 | NOW | gap | 136.8 | -0.68 / -0.67 | 0 | 2026-09-08 15:55 | 134.2 | close | -1.94% | +0.03 / -0.64 |
| 2026-09-10 9:30 | CRWV | gap | 89.94 | -0.96 / -0.95 | 0 | 2026-09-10 15:55 | 89.12 | close | -0.93% | +0.43 / -0.23 |
| 2026-09-10 9:30 | POET | gap | 7.747 | -0.62 / -0.59 | 0 | 2026-09-10 15:55 | 7.58 | close | -2.17% | +0.45 / -0.41 |
| 2026-09-10 9:30 | NBIS | gap | 232.1 | -0.61 / -0.61 | 0 | 2026-09-10 15:55 | 227.8 | close | -1.87% | +0.46 / -0.45 |
| 2026-09-10 9:30 | NVAX | gap | 9.469 | -0.61 / -0.58 | 0 | 2026-09-10 15:55 | 9.291 | close | -1.88% | +0.32 / -0.55 |
| 2026-09-11 9:30 | SMR | gap | 9.679 | -0.80 / -0.77 | 0 | 2026-09-11 15:55 | 8.593 | close | -11.23% | +0.13 / -1.61 |
| 2026-09-14 9:30 | NBIS | gap | 205.1 | -1.43 / -1.43 | 0 | 2026-09-14 15:55 | 212.2 | close | +3.48% | +1.04 / -0.09 |
| 2026-09-14 9:30 | APLD | gap | 24.46 | -1.25 / -1.24 | 0 | 2026-09-14 15:55 | 24.56 | close | +0.39% | +0.66 / -0.05 |
| 2026-09-14 9:30 | POET | gap | 7.4 | -1.25 / -1.22 | 0 | 2026-09-14 15:55 | 7.415 | close | +0.20% | +0.62 / -0.12 |
| 2026-09-14 9:30 | CRWV | gap | 82.51 | -1.24 / -1.23 | 0 | 2026-09-14 15:55 | 82.93 | close | +0.49% | +0.65 / -0.08 |
| 2026-09-15 9:30 | CRCL (crypto) | gap | 92.35 | -0.72 / -0.71 | 0 | 2026-09-15 15:55 | 86.29 | close | -6.57% | +0.13 / -1.06 |
| 2026-09-15 9:30 | COIN (crypto) | gap | 183.7 | -0.67 / -0.66 | 0 | 2026-09-15 15:55 | 172 | close | -6.37% | +0.04 / -1.34 |
| 2026-09-15 9:30 | SBET (crypto) | gap | 8.778 | -0.66 / -0.63 | 0 | 2026-09-15 15:55 | 8.308 | close | -5.35% | +0.04 / -1.13 |
| 2026-09-15 9:30 | BMNR (crypto) | gap | 24.6 | -0.64 / -0.64 | 0 | 2026-09-15 15:55 | 23.59 | close | -4.11% | +0.06 / -0.88 |
| 2026-09-22 9:30 | AXTI | gap | 76.67 | -0.55 / -0.54 | 0 | 2026-09-22 15:55 | 77.76 | close | +1.41% | +0.45 / -0.30 |
| 2026-09-24 9:30 | QUBT | gap | 8.878 | -0.68 / -0.63 | 0 | 2026-09-24 9:35 | 9.102 | neutral | +2.51% | +0.90 / -0.05 |
| 2026-09-24 9:30 | HIVE (crypto) | gap | 3.276 | -0.57 / -0.49 | 0 | 2026-09-24 9:35 | 3.353 | neutral | +2.33% | +0.51 / -0.24 |
| 2026-09-24 9:30 | ORCL | gap | 137.4 | -0.93 / -0.92 | 0 | 2026-09-24 15:55 | 139.5 | close | +1.49% | +0.38 / -0.50 |
| 2026-09-28 9:30 | NOW | gap | 129.9 | -1.05 / -1.04 | 0 | 2026-09-28 15:55 | 131.4 | close | +1.15% | +0.37 / -0.56 |
| 2026-09-28 9:30 | PATH | gap | 12.01 | -0.62 / -0.59 | 0 | 2026-09-28 15:55 | 12.19 | close | +1.42% | +0.45 / -0.59 |
| 2026-09-28 9:30 | ORCL | gap | 132.8 | -0.57 / -0.56 | 0 | 2026-09-28 15:55 | 132.6 | close | -0.18% | +0.38 / -0.16 |
| 2026-09-28 9:30 | POET | gap | 7.545 | -0.54 / -0.50 | 0 | 2026-09-28 15:55 | 7.395 | close | -2.00% | +0.28 / -0.50 |
| 2026-10-07 9:30 | BULL | gap | 5.862 | -4.03 / -3.99 | 0 | 2026-10-07 15:55 | 5.873 | close | +0.19% | +0.47 / -0.99 |
| 2026-10-07 9:30 | LEU | gap | 147.1 | -0.85 / -0.84 | 0 | 2026-10-07 15:55 | 147 | close | -0.08% | +0.25 / -0.53 |
| 2026-10-07 9:30 | BMNR (crypto) | gap | 24.96 | -0.79 / -0.79 | 0 | 2026-10-07 15:55 | 24.65 | close | -1.25% | +0.14 / -0.43 |
| 2026-10-07 9:30 | SBET (crypto) | gap | 9.058 | -0.79 / -0.76 | 0 | 2026-10-07 15:55 | 8.937 | close | -1.34% | +0.11 / -0.40 |
| 2026-10-09 9:30 | ASTS | gap | 54.45 | -0.62 / -0.61 | 0 | 2026-10-09 15:55 | 50.94 | close | -6.45% | +0.34 / -1.70 |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.88 | - |
| 2026-08-31 | $967.67 | - |
| 2026-09-01 | $949.21 | - |
| 2026-09-02 | $949.21 | - |
| 2026-09-03 | $949.21 | - |
| 2026-09-04 | $952.51 | - |
| 2026-09-08 | $947.90 | - |
| 2026-09-09 | $947.90 | - |
| 2026-09-10 | $931.68 | - |
| 2026-09-11 | $905.51 | - |
| 2026-09-14 | $915.83 | - |
| 2026-09-15 | $864.53 | - |
| 2026-09-16 | $864.53 | - |
| 2026-09-17 | $864.53 | - |
| 2026-09-18 | $864.53 | - |
| 2026-09-21 | $864.53 | - |
| 2026-09-22 | $867.58 | - |
| 2026-09-23 | $867.58 | - |
| 2026-09-24 | $881.33 | - |
| 2026-09-25 | $881.33 | - |
| 2026-09-28 | $882.21 | - |
| 2026-09-29 | $882.21 | - |
| 2026-09-30 | $882.21 | - |
| 2026-10-01 | $882.21 | - |
| 2026-10-02 | $882.21 | - |
| 2026-10-05 | $882.21 | - |
| 2026-10-06 | $882.21 | - |
| 2026-10-07 | $876.73 | - |
| 2026-10-08 | $876.73 | - |
| 2026-10-09 | $862.58 | - |

## Limits cancelled at 10:00 (the first 30 minutes), runs after: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $963.76 (-3.62%; realized $-84.69, open positions $+48.45); S&P 500 +0.97%, Nasdaq-100 +4.18%. 28 closed trades, 6 winners (21.4%), average trade -1.33%, average win 12.68%, average loss -5.15%, profit factor 0.64, worst drawdown -11.27%. Exits: target 6, stop 22. Resting orders filled: 6/14.

### What the trades had in common

- stopped the session it was bought: 3 trades, 0 won, average -3.46%, total $-21.32
- stopped on a later session: 19 trades, 0 won, average -5.42%, total $-211.16
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -6.77%, total $-110.15
- never rose 0.5 ATR above the entry: 14 trades, 0 won, average -4.78%, total $-146.10
- crypto-linked: 9 trades, 2 won, average -0.30%, total $+5.57
- bought on a dip of 0.5+ ATR (any time): 20 trades, 5 won, average -0.84%, total $-44.64
- bought less than 0.25 ATR under the prior close: 4 trades, 0 won, average -4.00%, total $-39.46
- resting limit fills: 3 trades, 0 won, average -4.28%, total $-32.79
- run entries inside the buy zone: 25 trades, 6 won, average -0.98%, total $-51.90
- support tested 3+ times: 16 trades, 3 won, average -1.98%, total $-58.20
- support tested twice: 11 trades, 3 won, average +0.44%, total $-10.11
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -10.38%, total $-16.38

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:05 | MSTR (crypto) | buy zone | 132.2 | -0.44 / -0.68 | 8.64 | 2026-08-28 11:40 | 129.8 | stop | -1.85% | +0.31 / -0.38 |
| 2026-08-28 10:05 | IONQ | buy zone | 39.81 | -0.27 / -0.97 | 5.67 | 2026-09-01 9:30 | 37.85 | stop | -4.94% | +0.27 / -0.78 |
| 2026-08-28 10:05 | BTDR (crypto) | buy zone | 10.38 | -0.25 / -0.88 | 2.57 | 2026-09-03 10:35 | 11.79 | target | +13.58% | +1.36 / -0.28 |
| 2026-08-31 10:05 | RIOT (crypto) | buy zone | 18.41 | -0.08 / -0.32 | 2.36 | 2026-09-04 10:05 | 21.56 | target | +17.12% | +1.75 / -0.56 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.95% | +0.82 / -0.78 |
| 2026-09-03 10:35 | GPUS | buy zone | 0.186 | +0.42 / -0.38 | 14.74 | 2026-09-24 9:35 | 0.1669 | stop | -10.38% | +0.61 / -0.54 |
| 2026-09-04 10:05 | BULL | buy zone | 9.684 | -0.40 / -0.50 | 6.85 | 2026-09-08 15:35 | 9.44 | stop | -2.53% | +0.52 / -0.36 |
| 2026-09-08 10:20 | DUOL | buy zone | 146.6 | -0.26 / -1.06 | 3.31 | 2026-09-09 10:15 | 140.8 | stop | -3.94% | +0.07 / -0.91 |
| 2026-09-08 15:35 | RXRX | buy zone | 3.487 | -0.23 / -0.65 | 4.19 | 2026-09-09 10:20 | 3.327 | stop | -4.63% | +0.00 / -0.72 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.51% | +0.64 / -0.85 |
| 2026-09-10 10:05 | NBIS | buy zone | 230.4 | -0.61 / -0.73 | 5.2 | 2026-09-14 9:30 | 204.9 | stop | -11.07% | +0.33 / -1.95 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.59% | +1.65 / -0.71 |
| 2026-09-15 10:05 | RXRX | buy zone | 3.256 | -0.27 / -0.82 | 3.35 | 2026-09-18 10:50 | 3.592 | target | +10.30% | +1.90 / -0.51 |
| 2026-09-18 10:50 | LUNR | buy zone | 13.99 | +0.14 / -1.00 | 9.72 | 2026-09-22 11:20 | 15.71 | target | +12.29% | +2.30 / -0.25 |
| 2026-09-22 11:20 | AXTI | buy zone | 75.39 | -0.55 / -0.76 | 3.4 | 2026-09-24 9:30 | 70.78 | stop | -6.12% | +0.56 / -0.97 |
| 2026-09-23 10:05 | PATH | buy zone | 12.71 | -0.02 / -0.55 | 6.93 | 2026-09-28 9:30 | 11.82 | stop | -7.03% | +0.62 / -1.14 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.20% | +1.68 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.61% | +0.07 / -0.90 |
| 2026-09-28 9:50 | AXTI | buy zone | 74.11 | -0.38 / -0.77 | 5.03 | 2026-10-08 15:45 | 71 | stop | -4.20% | +2.27 / -0.49 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.94% | +0.40 / -0.50 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.76% | +0.07 / -0.70 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-07 9:30 | 18.35 | stop | -6.71% | +1.00 / -1.11 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |
| 2026-10-05 11:05 | WULF (crypto) | buy zone | 14.78 | +0.45 / -0.73 | 3.65 | 2026-10-08 9:30 | 13.9 | stop | -5.99% | +0.41 / -1.04 |
| 2026-10-07 9:50 | SMR | buy zone | 7.545 | -0.56 / -0.92 | 4.7 | 2026-10-08 12:50 | 7.252 | stop | -3.89% | +0.27 / -0.55 |
| 2026-10-08 9:50 | CRWV | buy zone | 84.1 | -0.36 / -0.97 | 2.71 | 2026-10-08 12:45 | 81.24 | stop | -3.42% | +0.38 / -0.69 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |
| NNE | 2026-10-09 | 15.05 | 14.51 | 17.01 | 15.34 | +1.93% |
| GPUS | 2026-10-09 | 0.1562 | 0.1527 | 0.1664 | 0.16 | +2.41% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $977.30 | BTDR, IONQ |
| 2026-08-31 | $1004.26 | BTDR, IONQ, RIOT, SMCI |
| 2026-09-01 | $965.64 | BTDR, RIOT, SMCI, SOUN |
| 2026-09-02 | $986.33 | BTDR, RIOT, SMCI, SOUN |
| 2026-09-03 | $1049.27 | GPUS, RIOT, SMCI, SOUN |
| 2026-09-04 | $1067.13 | BULL, GPUS, SMCI, SOUN |
| 2026-09-08 | $1061.13 | DUOL, GPUS, RXRX, SMCI |
| 2026-09-09 | $1049.79 | GPUS, QBTS, SMCI |
| 2026-09-10 | $1021.13 | GPUS, NBIS, QBTS, SMCI |
| 2026-09-11 | $1037.58 | GPUS, NBIS, QBTS, SMCI |
| 2026-09-14 | $986.35 | AEHR, GPUS, SMCI |
| 2026-09-15 | $967.40 | AEHR, GPUS, RXRX, SMCI |
| 2026-09-16 | $966.02 | AEHR, GPUS, RXRX, SMCI |
| 2026-09-17 | $1022.54 | AEHR, GPUS, RXRX, SMCI |
| 2026-09-18 | $1019.81 | AEHR, GPUS, LUNR, SMCI |
| 2026-09-21 | $1076.57 | AEHR, GPUS, LUNR, SMCI |
| 2026-09-22 | $1080.89 | AXTI, GPUS, SMCI |
| 2026-09-23 | $1060.89 | AXTI, GPUS, PATH, SMCI |
| 2026-09-24 | $1051.00 | HIMS, PATH, SMCI |
| 2026-09-25 | $1063.70 | BTBT, CRCL, PATH, SMCI |
| 2026-09-28 | $1023.83 | AXTI, BTBT, CRCL, SMCI |
| 2026-09-29 | $1022.58 | AXTI, CRCL, IREN, SMCI |
| 2026-09-30 | $1012.19 | AXTI, BTDR, IREN, SMCI |
| 2026-10-01 | $1015.14 | AXTI, RIOT, SMCI |
| 2026-10-02 | $1033.23 | AXTI, PATH, RIOT, SMCI |
| 2026-10-05 | $1022.85 | AXTI, RIOT, SMCI, WULF |
| 2026-10-06 | $1019.92 | AXTI, RIOT, SMCI, WULF |
| 2026-10-07 | $1014.52 | AXTI, SMCI, SMR, WULF |
| 2026-10-08 | $959.09 | SMCI |
| 2026-10-09 | $963.76 | APLD, GPUS, NNE, SMCI |

## GPUS, IREN, BTDR only with a tested support: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1100.15 (+10.02%; realized $+40.12, open positions $+60.03); S&P 500 +0.97%, Nasdaq-100 +4.18%. 18 closed trades, 4 winners (22.2%), average trade 1.12%, average win 20.39%, average loss -4.38%, profit factor 1.32, worst drawdown -5.48%. Exits: target 4, stop 14. Resting orders filled: 11/25.

### What the trades had in common

- stopped the session it was bought: 3 trades, 0 won, average -4.70%, total $-30.57
- stopped on a later session: 11 trades, 0 won, average -4.30%, total $-93.61
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -4.73%, total $-54.64
- never rose 0.5 ATR above the entry: 10 trades, 0 won, average -4.09%, total $-85.07
- crypto-linked: 6 trades, 1 won, average -0.86%, total $-35.88
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.04%, total $+53.97
- bought on a dip of 0.5+ ATR (any time): 8 trades, 2 won, average +0.89%, total $+38.07
- bought less than 0.25 ATR under the prior close: 4 trades, 1 won, average +1.35%, total $-11.66
- resting limit fills: 9 trades, 1 won, average -1.64%, total $-32.12
- run entries inside the buy zone: 9 trades, 3 won, average +3.88%, total $+72.24
- support tested 3+ times: 14 trades, 3 won, average +0.67%, total $+9.30
- support tested twice: 4 trades, 1 won, average +2.70%, total $+30.82

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:00 | BTBT (crypto) | limit | 1.51 | -0.07 / -0.54 | 7.34 | 2026-08-28 14:35 | 1.417 | stop | -6.17% | +0.14 / -0.61 |
| 2026-09-01 9:30 | RCAT | limit | 8.33 | -0.35 / -0.35 | 4.58 | 2026-09-02 9:30 | 8.083 | stop | -2.97% | +0.19 / -0.37 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.06% | +2.33 / -0.07 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.33% | +0.37 / -0.79 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.81% | +0.11 / -0.42 |
| 2026-09-14 9:30 | RKLB | limit | 60.85 | -0.73 / -0.73 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.04% | +4.49 / -0.10 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.00% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -3.00% | +0.40 / -0.50 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-07 9:30 | 18.35 | stop | -6.70% | +1.00 / -1.11 |
| 2026-10-05 9:50 | LUNR | buy zone | 14.14 | -0.04 / -0.55 | 2.26 | 2026-10-09 11:05 | 13.32 | stop | -5.84% | +1.13 / -0.79 |
| 2026-10-07 9:50 | SMR | buy zone | 7.545 | -0.56 / -0.92 | 4.7 | 2026-10-08 12:50 | 7.252 | stop | -3.89% | +0.27 / -0.55 |
| 2026-10-08 12:50 | HIMS | buy zone | 27.62 | -0.21 / -1.16 | 2.1 | 2026-10-09 14:50 | 30.81 | target | +11.51% | +2.01 / -0.08 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 140.9 | +7.96% |
| APLD | 2026-10-09 | 23.46 | 22.64 | 28.67 | 23.68 | +0.93% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $971.81 | - |
| 2026-08-31 | $978.57 | SMCI |
| 2026-09-01 | $966.76 | AXTI, RCAT, SMCI |
| 2026-09-02 | $968.42 | AXTI, SMCI, WULF |
| 2026-09-03 | $971.00 | AEHR, SMCI, WULF |
| 2026-09-04 | $1010.05 | AEHR, RCAT, SMCI, WULF |
| 2026-09-08 | $1040.21 | AEHR, DUOL, RCAT, SMCI |
| 2026-09-09 | $1036.52 | RCAT, SMCI |
| 2026-09-10 | $1024.86 | SMCI |
| 2026-09-11 | $1047.12 | NOW, SMCI |
| 2026-09-14 | $1051.06 | NOW, RKLB, SMCI |
| 2026-09-15 | $1042.61 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $1043.82 | NOW, RKLB, SMCI |
| 2026-09-17 | $1081.97 | NOW, RKLB, SMCI |
| 2026-09-18 | $1058.54 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $1112.06 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $1121.65 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $1112.92 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $1129.71 | NOW, RGTI, SMCI |
| 2026-09-25 | $1141.43 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $1098.77 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $1085.76 | IREN, NOW, RGTI, SMCI |
| 2026-09-30 | $1093.75 | IREN, NOW, RGTI, SMCI |
| 2026-10-01 | $1103.55 | NOW, RGTI, RIOT, SMCI |
| 2026-10-02 | $1104.29 | NOW, RGTI, RIOT, SMCI |
| 2026-10-05 | $1094.52 | LUNR, NOW, RIOT, SMCI |
| 2026-10-06 | $1096.92 | LUNR, NOW, RIOT, SMCI |
| 2026-10-07 | $1101.35 | LUNR, NOW, SMCI, SMR |
| 2026-10-08 | $1078.84 | HIMS, LUNR, NOW, SMCI |
| 2026-10-09 | $1100.15 | APLD, NOW, SMCI |

## Both of the above: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1142.69 (+14.27%; realized $+81.72, open positions $+60.97); S&P 500 +0.97%, Nasdaq-100 +4.18%. 24 closed trades, 7 winners (29.2%), average trade 1.5%, average win 17.19%, average loss -4.95%, profit factor 1.42, worst drawdown -6.73%. Exits: target 7, stop 17. Resting orders filled: 5/15.

### What the trades had in common

- stopped the session it was bought: 3 trades, 0 won, average -3.08%, total $-23.71
- stopped on a later session: 14 trades, 0 won, average -5.36%, total $-173.04
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -7.11%, total $-90.72
- never rose 0.5 ATR above the entry: 12 trades, 0 won, average -5.00%, total $-145.29
- crypto-linked: 7 trades, 2 won, average +1.15%, total $+21.01
- bought on a dip of 0.5+ ATR (any time): 14 trades, 4 won, average -0.37%, total $-17.87
- bought less than 0.25 ATR under the prior close: 5 trades, 1 won, average +1.99%, total $+32.15
- resting limit fills: 3 trades, 0 won, average -4.91%, total $-40.12
- run entries inside the buy zone: 19 trades, 7 won, average +3.32%, total $+153.83
- run entries on a bounce (touched the zone, back above it): 2 trades, 0 won, average -6.10%, total $-31.99
- support tested 3+ times: 18 trades, 6 won, average +2.62%, total $+105.93
- support tested twice: 6 trades, 1 won, average -1.85%, total $-24.21

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-28 10:05 | MSTR (crypto) | buy zone | 132.2 | -0.44 / -0.68 | 8.64 | 2026-08-28 11:40 | 129.8 | stop | -1.85% | +0.31 / -0.38 |
| 2026-08-28 10:05 | IONQ | buy zone | 39.81 | -0.27 / -0.97 | 5.67 | 2026-09-01 9:30 | 37.85 | stop | -4.94% | +0.27 / -0.78 |
| 2026-08-28 10:05 | BTDR (crypto) | buy zone | 10.38 | -0.25 / -0.88 | 2.57 | 2026-09-03 10:35 | 11.79 | target | +13.58% | +1.36 / -0.28 |
| 2026-08-31 10:05 | RIOT (crypto) | buy zone | 18.41 | -0.08 / -0.32 | 2.36 | 2026-09-04 10:05 | 21.56 | target | +17.12% | +1.75 / -0.56 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.95% | +0.82 / -0.78 |
| 2026-09-03 10:35 | AEHR | buy zone | 76.69 | -0.11 / -0.32 | 4.83 | 2026-09-09 10:05 | 101.3 | target | +32.03% | +2.26 / -0.19 |
| 2026-09-04 10:05 | BULL | buy zone | 9.684 | -0.40 / -0.50 | 6.85 | 2026-09-08 15:35 | 9.44 | stop | -2.53% | +0.52 / -0.36 |
| 2026-09-08 10:20 | DUOL | buy zone | 146.6 | -0.26 / -1.06 | 3.31 | 2026-09-09 10:15 | 140.8 | stop | -3.94% | +0.07 / -0.91 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-10 10:05 | ORCL | buy zone | 157 | -0.50 / -0.71 | 6.15 | 2026-09-10 15:55 | 153.4 | stop | -2.28% | +0.33 / -0.69 |
| 2026-09-10 10:05 | NBIS | buy zone | 230.4 | -0.61 / -0.73 | 5.2 | 2026-09-14 9:30 | 204.9 | stop | -11.07% | +0.33 / -1.95 |
| 2026-09-11 10:05 | GRAL | buy zone | 77.28 | +0.01 / -0.06 | 1.81 | 2026-09-21 9:50 | 98.6 | target | +27.58% | +5.45 / -0.86 |
| 2026-09-15 10:05 | RXRX | buy zone | 3.256 | -0.27 / -0.82 | 3.35 | 2026-09-18 10:50 | 3.592 | target | +10.30% | +1.90 / -0.51 |
| 2026-09-21 10:05 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-24 13:40 | 9.158 | stop | -4.46% | +1.01 / -0.98 |
| 2026-09-22 10:05 | AXTI | bounce | 76.71 | -0.55 / -0.54 | 2.34 | 2026-09-24 9:30 | 70.78 | stop | -7.74% | +0.34 / -1.19 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.20% | +1.68 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.95% | +0.40 / -0.50 |
| 2026-09-30 10:35 | AXTI | buy zone | 75.92 | +0.25 / -0.35 | 2.74 | 2026-10-09 9:40 | 70.95 | stop | -6.56% | +1.96 / -0.79 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-07 9:30 | 18.35 | stop | -6.70% | +1.00 / -1.11 |
| 2026-10-07 9:50 | SMR | buy zone | 7.545 | -0.56 / -0.92 | 4.7 | 2026-10-08 12:50 | 7.252 | stop | -3.91% | +0.27 / -0.55 |
| 2026-10-08 12:50 | HIMS | buy zone | 27.62 | -0.21 / -1.16 | 2.1 | 2026-10-09 14:50 | 30.81 | target | +11.51% | +2.01 / -0.08 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 35.01 | 50.6 | 41.86 | +15.41% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 140.9 | +7.96% |
| APLD | 2026-10-09 | 23.28 | 22.64 | 28.67 | 23.68 | +1.71% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $977.30 | BTDR, IONQ |
| 2026-08-31 | $1004.26 | BTDR, IONQ, RIOT, SMCI |
| 2026-09-01 | $965.64 | BTDR, RIOT, SMCI, SOUN |
| 2026-09-02 | $986.33 | BTDR, RIOT, SMCI, SOUN |
| 2026-09-03 | $1044.60 | AEHR, RIOT, SMCI, SOUN |
| 2026-09-04 | $1093.41 | AEHR, BULL, SMCI, SOUN |
| 2026-09-08 | $1102.58 | AEHR, DUOL, SMCI |
| 2026-09-09 | $1108.98 | RGTI, SMCI |
| 2026-09-10 | $1082.36 | NBIS, SMCI |
| 2026-09-11 | $1097.00 | GRAL, NBIS, NOW, SMCI |
| 2026-09-14 | $1068.58 | GRAL, NOW, SMCI |
| 2026-09-15 | $1060.20 | GRAL, NOW, RXRX, SMCI |
| 2026-09-16 | $1057.29 | GRAL, NOW, RXRX, SMCI |
| 2026-09-17 | $1123.11 | GRAL, NOW, RXRX, SMCI |
| 2026-09-18 | $1115.42 | GRAL, NOW, SMCI |
| 2026-09-21 | $1200.29 | NOW, SMCI, STNE |
| 2026-09-22 | $1209.10 | AXTI, NOW, SMCI, STNE |
| 2026-09-23 | $1189.65 | AXTI, NOW, SMCI, STNE |
| 2026-09-24 | $1173.95 | HIMS, NOW, SMCI |
| 2026-09-25 | $1184.94 | BTBT, CRCL, NOW, SMCI |
| 2026-09-28 | $1145.47 | BTBT, CRCL, NOW, SMCI |
| 2026-09-29 | $1130.78 | CRCL, IREN, NOW, SMCI |
| 2026-09-30 | $1141.41 | AXTI, IREN, NOW, SMCI |
| 2026-10-01 | $1167.59 | AXTI, NOW, RIOT, SMCI |
| 2026-10-02 | $1187.83 | AXTI, NOW, RIOT, SMCI |
| 2026-10-05 | $1186.35 | AXTI, NOW, RIOT, SMCI |
| 2026-10-06 | $1178.92 | AXTI, NOW, RIOT, SMCI |
| 2026-10-07 | $1169.50 | AXTI, NOW, SMCI, SMR |
| 2026-10-08 | $1127.78 | AXTI, HIMS, NOW, SMCI |
| 2026-10-09 | $1142.69 | APLD, NOW, SMCI |

## Both, stop 1.0 ATR under support: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $990.61 (-0.94%; realized $-55.19, open positions $+45.80); S&P 500 +0.97%, Nasdaq-100 +4.18%. 7 closed trades, 1 winners (14.3%), average trade -2.49%, average win 14.68%, average loss -5.36%, profit factor 0.2, worst drawdown -5.38%. Exits: target 1, stop 6. Resting orders filled: 2/5.

### What the trades had in common

- stopped the session it was bought: 2 trades, 0 won, average -3.44%, total $-17.21
- stopped on a later session: 4 trades, 0 won, average -6.31%, total $-52.00
- stopped at the open (gapped through the stop): 2 trades, 0 won, average -6.56%, total $-31.96
- never rose 0.5 ATR above the entry: 4 trades, 0 won, average -5.50%, total $-46.85
- crypto-linked: 3 trades, 1 won, average +2.60%, total $-3.19
- bought on a dip of 0.5+ ATR (any time): 6 trades, 1 won, average -1.44%, total $-40.80
- bought less than 0.25 ATR under the prior close: 1 trade, 0 won, average -8.80%, total $-14.39
- resting limit fills: 1 trade, 0 won, average -8.80%, total $-14.39
- run entries inside the buy zone: 6 trades, 1 won, average -1.44%, total $-40.80
- support tested 3+ times: 6 trades, 0 won, average -5.36%, total $-69.21
- support tested twice: 1 trade, 1 won, average +14.68%, total $+14.02

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 3.89 | 2026-09-01 9:50 | 14.59 | stop | -8.80% | +0.00 / -0.93 |
| 2026-08-28 10:05 | IREN (crypto) | buy zone | 36.61 | -0.90 / -1.20 | 7.27 | 2026-08-28 11:50 | 35.62 | stop | -2.71% | +0.24 / -0.33 |
| 2026-08-28 10:05 | MSTR (crypto) | buy zone | 132.2 | -0.44 / -0.68 | 3.71 | 2026-08-28 12:20 | 126.7 | stop | -4.18% | +0.31 / -0.75 |
| 2026-08-28 10:05 | IONQ | buy zone | 39.81 | -0.27 / -0.97 | 3.16 | 2026-09-02 9:30 | 37.3 | stop | -6.33% | +0.27 / -1.08 |
| 2026-08-28 11:50 | BTDR (crypto) | buy zone | 10.28 | -0.25 / -0.97 | 1.69 | 2026-09-03 10:35 | 11.79 | target | +14.68% | +1.46 / -0.19 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 2.28 | 2026-09-10 9:30 | 6.337 | stop | -6.79% | +0.82 / -1.45 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 4.36 | 2026-09-11 10:20 | 150.8 | stop | -3.33% | +1.54 / -0.84 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 36.27 | 33.95 | 50.6 | 41.86 | +15.41% |
| COIN | 2026-09-02 | 177.8 | 157.5 | 209.1 | 179.4 | +0.91% |
| HIMX | 2026-09-03 | 13.4 | 12.51 | 15.9 | 13.3 | -0.72% |
| NOW | 2026-09-11 | 132.1 | 123.9 | 147.6 | 140.9 | +6.63% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $973.03 | BTDR, IONQ, LUNR |
| 2026-08-31 | $984.12 | BTDR, IONQ, LUNR, SMCI |
| 2026-09-01 | $961.06 | BTDR, IONQ, SMCI, SOUN |
| 2026-09-02 | $958.80 | BTDR, COIN, SMCI, SOUN |
| 2026-09-03 | $987.29 | COIN, HIMX, SMCI, SOUN |
| 2026-09-04 | $993.11 | COIN, HIMX, SMCI, SOUN |
| 2026-09-08 | $993.96 | COIN, HIMX, SMCI, SOUN |
| 2026-09-09 | $977.47 | COIN, HIMX, SMCI, SOUN |
| 2026-09-10 | $955.76 | COIN, HIMX, ORCL, SMCI |
| 2026-09-11 | $987.30 | COIN, HIMX, NOW, SMCI |
| 2026-09-14 | $978.36 | COIN, HIMX, NOW, SMCI |
| 2026-09-15 | $951.35 | COIN, HIMX, NOW, SMCI |
| 2026-09-16 | $946.21 | COIN, HIMX, NOW, SMCI |
| 2026-09-17 | $980.39 | COIN, HIMX, NOW, SMCI |
| 2026-09-18 | $988.47 | COIN, HIMX, NOW, SMCI |
| 2026-09-21 | $1018.72 | COIN, HIMX, NOW, SMCI |
| 2026-09-22 | $1021.11 | COIN, HIMX, NOW, SMCI |
| 2026-09-23 | $1017.84 | COIN, HIMX, NOW, SMCI |
| 2026-09-24 | $1011.12 | COIN, HIMX, NOW, SMCI |
| 2026-09-25 | $1019.51 | COIN, HIMX, NOW, SMCI |
| 2026-09-28 | $993.68 | COIN, HIMX, NOW, SMCI |
| 2026-09-29 | $987.91 | COIN, HIMX, NOW, SMCI |
| 2026-09-30 | $992.18 | COIN, HIMX, NOW, SMCI |
| 2026-10-01 | $1011.81 | COIN, HIMX, NOW, SMCI |
| 2026-10-02 | $1024.48 | COIN, HIMX, NOW, SMCI |
| 2026-10-05 | $1019.52 | COIN, HIMX, NOW, SMCI |
| 2026-10-06 | $1024.87 | COIN, HIMX, NOW, SMCI |
| 2026-10-07 | $1015.04 | COIN, HIMX, NOW, SMCI |
| 2026-10-08 | $987.81 | COIN, HIMX, NOW, SMCI |
| 2026-10-09 | $990.61 | COIN, HIMX, NOW, SMCI |

## Run entries only, GPUS/IREN/BTDR only with a tested support: 2026-08-28 to 2026-10-09 (30 sessions)

$1000 -> $1102.77 (+10.28%; realized $+61.94, open positions $+40.83); S&P 500 +0.97%, Nasdaq-100 +4.18%. 27 closed trades, 7 winners (25.9%), average trade 0.92%, average win 17.79%, average loss -4.98%, profit factor 1.31, worst drawdown -8.92%. Exits: target 7, stop 20.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -3.70%, total $-53.67
- stopped on a later session: 14 trades, 0 won, average -5.53%, total $-147.99
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -7.88%, total $-81.35
- never rose 0.5 ATR above the entry: 15 trades, 0 won, average -5.05%, total $-162.36
- crypto-linked: 8 trades, 2 won, average -0.43%, total $-31.86
- bought on a dip of 0.5+ ATR (any time): 15 trades, 4 won, average -0.38%, total $-47.10
- bought less than 0.25 ATR under the prior close: 6 trades, 1 won, average +0.90%, total $+45.63
- run entries inside the buy zone: 26 trades, 7 won, average +1.14%, total $+64.10
- run entries on a bounce (touched the zone, back above it): 1 trade, 0 won, average -4.60%, total $-2.16
- support tested 3+ times: 21 trades, 5 won, average +0.88%, total $+60.04
- support tested twice: 6 trades, 2 won, average +1.07%, total $+1.90

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-28 9:50 | NNE | buy zone | 18.78 | -0.13 / -0.37 | 7.46 | 2026-08-28 10:05 | 18.32 | stop | -2.41% | +0.00 / -0.41 |
| 2026-08-28 9:50 | LUNR | buy zone | 15.82 | -0.12 / -0.24 | 10.52 | 2026-08-28 14:20 | 15.18 | stop | -4.04% | +0.02 / -0.43 |
| 2026-08-28 9:50 | BTBT (crypto) | buy zone | 1.538 | -0.07 / -0.36 | 5.77 | 2026-08-28 14:35 | 1.417 | stop | -7.86% | +0.00 / -0.80 |
| 2026-08-28 9:50 | IONQ | buy zone | 40.51 | -0.27 / -0.71 | 3.44 | 2026-09-01 9:30 | 37.85 | stop | -6.57% | +0.07 / -1.03 |
| 2026-08-28 10:05 | BTDR (crypto) | buy zone | 10.38 | -0.25 / -0.88 | 2.57 | 2026-09-03 10:35 | 11.79 | target | +13.53% | +1.36 / -0.28 |
| 2026-08-31 9:50 | MARA (crypto) | buy zone | 10.43 | +0.11 / -0.26 | 2.36 | 2026-09-11 10:05 | 12.17 | target | +16.73% | +2.06 / -0.46 |
| 2026-09-01 9:50 | SOUN | buy zone | 6.799 | -0.59 / -1.10 | 3.55 | 2026-09-08 10:10 | 6.535 | stop | -3.89% | +0.82 / -0.78 |
| 2026-09-03 10:35 | AEHR | buy zone | 76.69 | -0.11 / -0.32 | 4.83 | 2026-09-09 10:05 | 101.3 | target | +32.03% | +2.26 / -0.19 |
| 2026-09-08 10:20 | DUOL | buy zone | 146.6 | -0.26 / -1.06 | 3.31 | 2026-09-09 10:15 | 140.8 | stop | -3.99% | +0.07 / -0.91 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-10 9:50 | NBIS | buy zone | 230.1 | -0.61 / -0.75 | 5.38 | 2026-09-14 9:30 | 204.9 | stop | -10.98% | +0.34 / -1.93 |
| 2026-09-11 9:50 | GRAL | buy zone | 77.1 | +0.01 / -0.10 | 1.95 | 2026-09-21 9:50 | 98.6 | target | +27.88% | +5.49 / -0.82 |
| 2026-09-11 10:05 | SOFI | bounce | 17.45 | +0.14 / +0.30 | 1.98 | 2026-09-16 14:55 | 16.65 | stop | -4.60% | +0.37 / -1.06 |
| 2026-09-14 9:50 | AEHR | buy zone | 86.42 | -1.19 / -1.07 | 2.27 | 2026-09-22 13:50 | 99.05 | target | +14.61% | +1.65 / -0.71 |
| 2026-09-16 15:05 | UMAC | buy zone | 21.5 | +0.01 / -0.88 | 9.12 | 2026-10-07 9:35 | 20.97 | stop | -2.47% | +2.46 / -0.43 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 2.69 | 2026-09-24 13:40 | 9.158 | stop | -4.14% | +1.10 / -0.90 |
| 2026-09-22 13:50 | AXTI | buy zone | 76.31 | -0.55 / -0.60 | 2.6 | 2026-09-24 9:30 | 70.78 | stop | -7.25% | +0.41 / -1.12 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-24 13:50 | BTBT (crypto) | buy zone | 1.784 | -0.35 / +0.11 | 5.6 | 2026-09-29 12:05 | 1.664 | stop | -6.78% | +0.28 / -0.88 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.93% | +0.40 / -0.50 |
| 2026-09-30 10:35 | AXTI | buy zone | 75.92 | +0.25 / -0.35 | 2.74 | 2026-10-09 9:40 | 70.95 | stop | -6.57% | +1.96 / -0.79 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-07 9:30 | 18.35 | stop | -6.70% | +1.00 / -1.11 |
| 2026-10-07 9:50 | SMR | buy zone | 7.545 | -0.56 / -0.92 | 4.7 | 2026-10-08 12:50 | 7.252 | stop | -3.89% | +0.27 / -0.55 |
| 2026-10-08 9:50 | CRWV | buy zone | 84.1 | -0.36 / -0.97 | 2.71 | 2026-10-08 12:45 | 81.24 | stop | -3.41% | +0.38 / -0.69 |
| 2026-10-08 12:50 | HIMS | buy zone | 27.62 | -0.21 / -1.16 | 2.1 | 2026-10-09 14:50 | 30.81 | target | +11.51% | +2.01 / -0.08 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-31 | 37.23 | 35.01 | 50.6 | 41.86 | +12.44% |
| APLD | 2026-10-09 | 23.28 | 22.64 | 28.67 | 23.68 | +1.71% |
| NNE | 2026-10-09 | 14.98 | 14.51 | 17.01 | 15.34 | +2.37% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-28 | $958.58 | BTDR, IONQ |
| 2026-08-31 | $967.94 | BTDR, IONQ, MARA, SMCI |
| 2026-09-01 | $945.01 | BTDR, MARA, SMCI, SOUN |
| 2026-09-02 | $950.26 | BTDR, MARA, SMCI, SOUN |
| 2026-09-03 | $978.35 | AEHR, MARA, SMCI, SOUN |
| 2026-09-04 | $1014.30 | AEHR, MARA, SMCI, SOUN |
| 2026-09-08 | $1035.12 | AEHR, DUOL, MARA, SMCI |
| 2026-09-09 | $1052.29 | MARA, SMCI |
| 2026-09-10 | $1026.15 | MARA, NBIS, SMCI |
| 2026-09-11 | $1050.67 | GRAL, NBIS, SMCI, SOFI |
| 2026-09-14 | $996.78 | AEHR, GRAL, SMCI, SOFI |
| 2026-09-15 | $984.46 | AEHR, GRAL, SMCI, SOFI |
| 2026-09-16 | $1001.39 | AEHR, GRAL, SMCI, UMAC |
| 2026-09-17 | $1077.56 | AEHR, GRAL, SMCI, UMAC |
| 2026-09-18 | $1072.56 | AEHR, GRAL, SMCI, UMAC |
| 2026-09-21 | $1167.24 | AEHR, SMCI, STNE, UMAC |
| 2026-09-22 | $1178.63 | AXTI, SMCI, STNE, UMAC |
| 2026-09-23 | $1145.01 | AXTI, SMCI, STNE, UMAC |
| 2026-09-24 | $1169.63 | BTBT, HIMS, SMCI, UMAC |
| 2026-09-25 | $1186.06 | BTBT, CRCL, SMCI, UMAC |
| 2026-09-28 | $1163.68 | BTBT, CRCL, SMCI, UMAC |
| 2026-09-29 | $1162.63 | CRCL, IREN, SMCI, UMAC |
| 2026-09-30 | $1153.46 | AXTI, IREN, SMCI, UMAC |
| 2026-10-01 | $1128.42 | AXTI, RIOT, SMCI, UMAC |
| 2026-10-02 | $1152.13 | AXTI, RIOT, SMCI, UMAC |
| 2026-10-05 | $1138.62 | AXTI, RIOT, SMCI, UMAC |
| 2026-10-06 | $1138.35 | AXTI, RIOT, SMCI, UMAC |
| 2026-10-07 | $1125.36 | AXTI, SMCI, SMR |
| 2026-10-08 | $1080.29 | AXTI, HIMS, SMCI |
| 2026-10-09 | $1102.77 | APLD, NNE, SMCI |

