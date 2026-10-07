# Replay of the rules, 2026-07-15 to 2026-10-06 (59 sessions, 5-minute bars)

$1,000 each; S&P 500 +3.63%, Nasdaq-100 +5.55% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Real-book rules, no S&P gate, limits from the open | +1.94% | 20 | 15.0% | -0.61% | 0.81 | -9.2% | HIMX |
| Real-book rules + S&P gate 0.35% (live real book) | +7.00% | 11 | 18.2% | 0.37% | 1.07 | -9.15% | HIMX, WULF |
| Real-book rules + entries from 9:45 | -5.51% | 24 | 12.5% | -0.93% | 0.71 | -8.65% | UMAC |
| Real-book rules + S&P gate + entries from 9:45 | -10.04% | 18 | 5.6% | -2.52% | 0.27 | -11.65% | UMAC, WULF |
| Real-book rules + 1% gap allowance | +2.77% | 20 | 15.0% | -0.61% | 0.85 | -8.55% | HIMX |
| Real-book rules + S&P gate + 9:45 + 1% gap allowance | -9.71% | 18 | 5.6% | -2.52% | 0.27 | -11.18% | UMAC, WULF |

## Real-book rules, no S&P gate, limits from the open: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1019.37 (+1.94%; realized $-33.46, open positions $+52.83); S&P 500 +3.63%, Nasdaq-100 +5.55%. 20 closed trades, 3 winners (15.0%), average trade -0.61%, average win 20.29%, average loss -4.3%, profit factor 0.81, worst drawdown -9.2%. Exits: target 3, stop 17. Resting orders filled: 21/57.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -2.20%, total $-20.87
- stopped on a later session: 13 trades, 0 won, average -4.95%, total $-155.17
- stopped at the open (gapped through the stop): 8 trades, 0 won, average -5.28%, total $-99.99
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -4.48%, total $-115.52
- crypto-linked: 2 trades, 0 won, average -4.64%, total $-23.04
- bought at the open after a gap down of 0.5+ ATR: 5 trades, 0 won, average -2.15%, total $-26.04
- bought on a dip of 0.5+ ATR (any time): 10 trades, 2 won, average +0.78%, total $+12.63
- bought less than 0.25 ATR under the prior close: 5 trades, 0 won, average -4.59%, total $-58.39
- resting limit fills: 20 trades, 3 won, average -0.61%, total $-33.46
- support tested 3+ times: 20 trades, 3 won, average -0.61%, total $-33.46

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.84% | +0.49 / -0.63 |
| 2026-07-16 11:55 | QBTS | limit | 17.29 | -0.17 / -0.61 | 4.2 | 2026-07-17 9:30 | 16.3 | stop | -5.74% | +0.06 / -0.74 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-22 9:35 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.25 / -0.68 |
| 2026-07-23 9:30 | HIVE (crypto) | limit | 3.1 | -0.36 / -0.36 | 13.88 | 2026-07-24 15:40 | 2.951 | stop | -4.83% | +0.80 / -0.56 |
| 2026-07-27 10:30 | HOOD | limit | 94.56 | +0.33 / -0.05 | 6.05 | 2026-07-28 9:30 | 90.67 | stop | -4.12% | +0.20 / -0.74 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-07-30 9:30 | NOW | limit | 110.5 | -0.79 / -0.79 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -2.11% | +0.10 / -0.37 |
| 2026-08-11 9:30 | RKLB | limit | 76.27 | -0.63 / -0.63 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -1.01% | +0.44 / -0.14 |
| 2026-08-12 9:30 | RKLB | limit | 79.14 | +0.02 / -0.14 | 18.98 | 2026-08-19 9:35 | 75.41 | stop | -4.72% | +1.04 / -0.70 |
| 2026-08-20 15:00 | HOOD | limit | 93.67 | +1.11 / -0.46 | 9.0 | 2026-09-03 9:50 | 119 | target | +27.08% | +6.23 / -0.00 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-14 9:30 | QUBT | limit | 7.72 | -0.73 / -0.73 | 4.36 | 2026-09-14 9:30 | 7.624 | stop | -1.25% | +0.00 / -0.24 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.98% | +1.12 / -0.42 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-10-01 9:45 | 1.596 | stop | -4.46% | +0.51 / -0.59 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.06 | 11.57 | 15.81 | 14.85 | +23.13% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $1000.00 | - |
| 2026-07-16 | $989.48 | IONQ, POET, QBTS |
| 2026-07-17 | $967.67 | IONQ |
| 2026-07-20 | $963.87 | IONQ |
| 2026-07-21 | $972.82 | IONQ |
| 2026-07-22 | $955.75 | IONQ, POET |
| 2026-07-23 | $953.19 | HIVE, IONQ |
| 2026-07-24 | $927.90 | - |
| 2026-07-27 | $930.57 | HOOD |
| 2026-07-28 | $908.04 | - |
| 2026-07-29 | $908.62 | AFRM, PCVX |
| 2026-07-30 | $926.78 | AFRM, PCVX |
| 2026-07-31 | $913.08 | AFRM, PCVX |
| 2026-08-03 | $937.74 | AFRM, HIMX, PCVX |
| 2026-08-04 | $977.29 | AFRM, HIMX, PCVX |
| 2026-08-05 | $967.99 | AFRM, HIMX, PCVX |
| 2026-08-06 | $982.07 | AFRM, HIMX |
| 2026-08-07 | $993.84 | AFRM, HIMX |
| 2026-08-10 | $997.05 | AFRM, HIMX |
| 2026-08-11 | $1003.04 | AFRM, HIMX |
| 2026-08-12 | $1000.82 | AFRM, HIMX, RKLB |
| 2026-08-13 | $1005.27 | AFRM, HIMX, RKLB |
| 2026-08-14 | $1016.64 | AFRM, HIMX, RKLB |
| 2026-08-17 | $1013.40 | AFRM, HIMX, RKLB |
| 2026-08-18 | $981.34 | AFRM, HIMX, RKLB |
| 2026-08-19 | $972.80 | AFRM, HIMX |
| 2026-08-20 | $964.76 | AFRM, HIMX, HOOD |
| 2026-08-21 | $1007.29 | AFRM, HIMX, HOOD |
| 2026-08-24 | $988.47 | AFRM, HIMX, HOOD |
| 2026-08-25 | $1018.27 | AFRM, HIMX, HOOD |
| 2026-08-26 | $1007.45 | AFRM, HIMX, HOOD |
| 2026-08-27 | $1018.32 | AFRM, HIMX, HOOD |
| 2026-08-28 | $1023.03 | HIMX, HOOD |
| 2026-08-31 | $1025.97 | HIMX, HOOD |
| 2026-09-01 | $1010.81 | AXTI, HIMX, HOOD |
| 2026-09-02 | $1024.13 | AXTI, HIMX, HOOD |
| 2026-09-03 | $1048.94 | HIMX |
| 2026-09-04 | $1048.12 | HIMX, RCAT |
| 2026-09-08 | $1066.51 | HIMX, RCAT |
| 2026-09-09 | $1039.14 | HIMX, RCAT, RGTI |
| 2026-09-10 | $1027.62 | HIMX |
| 2026-09-11 | $1045.60 | HIMX |
| 2026-09-14 | $1020.96 | HIMX |
| 2026-09-15 | $1013.76 | HIMX |
| 2026-09-16 | $1010.55 | HIMX |
| 2026-09-17 | $1022.28 | HIMX |
| 2026-09-18 | $1033.53 | HIMX, RGTI |
| 2026-09-21 | $1057.41 | HIMX, RGTI |
| 2026-09-22 | $1059.14 | HIMX, RGTI |
| 2026-09-23 | $1042.50 | HIMX, RGTI |
| 2026-09-24 | $1056.46 | HIMX, QUBT, RGTI |
| 2026-09-25 | $1059.28 | HIMX, QUBT, RGTI |
| 2026-09-28 | $1030.36 | HIMX, RGTI |
| 2026-09-29 | $1026.46 | BTBT, HIMX, RGTI |
| 2026-09-30 | $1022.80 | BTBT, HIMX, RGTI |
| 2026-10-01 | $1022.69 | HIMX, RGTI |
| 2026-10-02 | $1031.53 | HIMX, RGTI |
| 2026-10-05 | $1016.72 | HIMX |
| 2026-10-06 | $1019.37 | HIMX |

## Real-book rules + S&P gate 0.35% (live real book): 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1070.00 (+7.00%; realized $+6.99, open positions $+63.01); S&P 500 +3.63%, Nasdaq-100 +5.55%. 11 closed trades, 2 winners (18.2%), average trade 0.37%, average win 22.21%, average loss -4.49%, profit factor 1.07, worst drawdown -9.15%. Exits: target 2, stop 9. Resting orders filled: 13/79.

### What the trades had in common

- stopped the session it was bought: 3 trades, 0 won, average -2.83%, total $-20.74
- stopped on a later session: 6 trades, 0 won, average -5.31%, total $-81.21
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -5.20%, total $-39.65
- never rose 0.5 ATR above the entry: 7 trades, 0 won, average -4.39%, total $-77.73
- crypto-linked: 2 trades, 1 won, average +8.52%, total $+42.20
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 0 won, average -3.26%, total $-15.92
- bought on a dip of 0.5+ ATR (any time): 4 trades, 0 won, average -4.04%, total $-40.14
- bought less than 0.25 ATR under the prior close: 4 trades, 2 won, average +8.28%, total $+80.04
- resting limit fills: 11 trades, 2 won, average +0.37%, total $+6.99
- support tested 3+ times: 11 trades, 2 won, average +0.37%, total $+6.99

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-22 9:35 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.25 / -0.68 |
| 2026-07-24 9:30 | APLD | limit | 29.18 | -0.29 / -0.29 | 5.09 | 2026-07-24 9:35 | 28.61 | stop | -1.96% | +0.00 / -0.25 |
| 2026-07-24 10:30 | HOOD | limit | 94.37 | -0.28 / -1.14 | 6.19 | 2026-07-28 9:30 | 90.53 | stop | -4.07% | +0.80 / -0.72 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-30 9:30 | NOW | limit | 110.5 | -0.79 / -0.79 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -2.11% | +0.10 / -0.37 |
| 2026-07-30 9:35 | AFRM | limit | 69.88 | +0.24 / -0.07 | 7.84 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +6.08 / -0.01 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-09-02 9:30 | MARA (crypto) | limit | 10.01 | -0.24 / -0.24 | 3.48 | 2026-09-11 10:05 | 12.17 | target | +21.58% | +2.55 / -0.02 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.06 | 11.57 | 15.81 | 14.85 | +23.13% |
| WULF | 2026-09-30 | 14.55 | 13.94 | 17.76 | 14.97 | +2.89% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $1000.00 | - |
| 2026-07-16 | $1000.00 | - |
| 2026-07-17 | $1000.00 | - |
| 2026-07-20 | $1000.00 | - |
| 2026-07-21 | $1000.00 | - |
| 2026-07-22 | $988.47 | POET |
| 2026-07-23 | $983.93 | - |
| 2026-07-24 | $980.51 | HOOD |
| 2026-07-27 | $982.44 | HOOD |
| 2026-07-28 | $958.22 | - |
| 2026-07-29 | $958.22 | - |
| 2026-07-30 | $964.72 | AFRM |
| 2026-07-31 | $958.75 | AFRM |
| 2026-08-03 | $987.19 | AFRM, HIMX |
| 2026-08-04 | $1023.55 | AFRM, HIMX |
| 2026-08-05 | $1006.37 | AFRM, HIMX, POET |
| 2026-08-06 | $1021.85 | AFRM, HIMX, POET |
| 2026-08-07 | $1046.12 | AFRM, HIMX, POET |
| 2026-08-10 | $1038.51 | AFRM, HIMX, POET |
| 2026-08-11 | $1048.41 | AFRM, HIMX, POET |
| 2026-08-12 | $1048.06 | AFRM, HIMX, POET |
| 2026-08-13 | $1057.63 | AFRM, HIMX, POET |
| 2026-08-14 | $1090.10 | AFRM, HIMX, POET |
| 2026-08-17 | $1074.90 | AFRM, HIMX, POET |
| 2026-08-18 | $1022.05 | AFRM, HIMX, POET |
| 2026-08-19 | $1024.38 | AFRM, HIMX, POET |
| 2026-08-20 | $1006.65 | AFRM, HIMX, POET |
| 2026-08-21 | $1015.20 | AFRM, HIMX, POET |
| 2026-08-24 | $990.39 | AFRM, HIMX |
| 2026-08-25 | $1003.31 | AFRM, HIMX, LUNR |
| 2026-08-26 | $994.18 | AFRM, HIMX, LUNR |
| 2026-08-27 | $1003.34 | AFRM, HIMX, LUNR |
| 2026-08-28 | $1009.75 | HIMX |
| 2026-08-31 | $1011.34 | HIMX |
| 2026-09-01 | $1005.18 | HIMX |
| 2026-09-02 | $1018.51 | HIMX, MARA |
| 2026-09-03 | $1048.07 | HIMX, MARA |
| 2026-09-04 | $1043.18 | HIMX, MARA |
| 2026-09-08 | $1064.98 | HIMX, MARA |
| 2026-09-09 | $1057.21 | HIMX, MARA, RGTI |
| 2026-09-10 | $1034.62 | HIMX, MARA |
| 2026-09-11 | $1072.07 | HIMX |
| 2026-09-14 | $1049.62 | HIMX |
| 2026-09-15 | $1042.06 | HIMX |
| 2026-09-16 | $1038.68 | HIMX |
| 2026-09-17 | $1051.01 | HIMX |
| 2026-09-18 | $1057.96 | HIMX |
| 2026-09-21 | $1069.69 | HIMX |
| 2026-09-22 | $1071.68 | HIMX |
| 2026-09-23 | $1063.13 | HIMX |
| 2026-09-24 | $1059.95 | HIMX |
| 2026-09-25 | $1067.82 | BTBT, HIMX |
| 2026-09-28 | $1046.17 | BTBT, HIMX |
| 2026-09-29 | $1047.54 | HIMX |
| 2026-09-30 | $1051.44 | HIMX, WULF |
| 2026-10-01 | $1060.97 | HIMX, WULF |
| 2026-10-02 | $1087.11 | HIMX, WULF |
| 2026-10-05 | $1063.98 | HIMX, WULF |
| 2026-10-06 | $1070.00 | HIMX, WULF |

## Real-book rules + entries from 9:45: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $944.93 (-5.51%; realized $-58.81, open positions $+3.74); S&P 500 +3.63%, Nasdaq-100 +5.55%. 24 closed trades, 3 winners (12.5%), average trade -0.93%, average win 20.29%, average loss -3.97%, profit factor 0.71, worst drawdown -8.65%. Exits: target 3, stop 21. Resting orders filled: 25/75.

### What the trades had in common

- stopped the session it was bought: 5 trades, 0 won, average -1.87%, total $-22.03
- stopped on a later session: 16 trades, 0 won, average -4.62%, total $-178.55
- stopped at the open (gapped through the stop): 9 trades, 0 won, average -4.33%, total $-93.65
- never rose 0.5 ATR above the entry: 14 trades, 0 won, average -4.01%, total $-136.16
- crypto-linked: 3 trades, 0 won, average -4.23%, total $-30.57
- bought on a dip of 0.5+ ATR (any time): 14 trades, 2 won, average -0.58%, total $-23.15
- bought less than 0.25 ATR under the prior close: 5 trades, 0 won, average -4.75%, total $-57.93
- resting limit fills: 24 trades, 3 won, average -0.93%, total $-58.81
- support tested 3+ times: 24 trades, 3 won, average -0.93%, total $-58.81

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-16 9:45 | POET | limit | 7.785 | -0.38 / -0.55 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.19% | +0.55 / -0.57 |
| 2026-07-16 11:55 | QBTS | limit | 17.29 | -0.17 / -0.61 | 4.2 | 2026-07-17 9:30 | 16.3 | stop | -5.74% | +0.06 / -0.74 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-22 12:25 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.01 / -0.68 |
| 2026-07-23 11:25 | HIVE (crypto) | limit | 3.12 | -0.36 / -0.28 | 13.88 | 2026-07-24 15:40 | 2.951 | stop | -5.44% | +0.34 / -0.64 |
| 2026-07-27 10:30 | HOOD | limit | 94.56 | +0.33 / -0.05 | 6.05 | 2026-07-28 9:30 | 90.67 | stop | -4.12% | +0.20 / -0.74 |
| 2026-07-28 9:45 | HIMX | limit | 11.78 | -0.73 / -1.05 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -2.07% | +0.06 / -0.26 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-07-30 9:45 | NOW | limit | 110.1 | -0.79 / -0.85 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -1.76% | +0.00 / -0.31 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-11 9:45 | RKLB | limit | 76.26 | -0.63 / -0.63 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -1.00% | +0.00 / -0.13 |
| 2026-08-18 9:45 | HOOD | limit | 93.28 | -0.59 / -0.67 | 8.96 | 2026-08-18 15:55 | 91.65 | stop | -1.75% | +0.18 / -0.41 |
| 2026-08-19 9:45 | CLSK (crypto) | limit | 11.4 | -0.04 / -0.27 | 3.93 | 2026-08-19 9:50 | 11.09 | stop | -2.78% | +0.00 / -0.28 |
| 2026-08-20 15:00 | HOOD | limit | 93.67 | +1.11 / -0.46 | 9.0 | 2026-09-03 9:50 | 119 | target | +27.08% | +6.23 / -0.00 |
| 2026-08-25 9:45 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-09-01 9:45 | RCAT | limit | 8.325 | -0.35 / -0.35 | 4.58 | 2026-09-02 9:30 | 8.083 | stop | -2.92% | +0.03 / -0.37 |
| 2026-09-01 9:45 | AXTI | limit | 55.2 | -0.30 / -0.63 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -1.29% | +0.55 / -0.14 |
| 2026-09-04 9:45 | RCAT | limit | 8.39 | -0.07 / -0.24 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -3.63% | +0.84 / -0.50 |
| 2026-09-08 11:05 | RXRX | limit | 3.48 | -0.23 / -0.68 | 3.82 | 2026-09-09 10:20 | 3.327 | stop | -4.41% | +0.23 / -0.68 |
| 2026-09-09 9:45 | RGTI | limit | 15.67 | -0.18 / -0.14 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.33% | +0.27 / -0.81 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-24 9:50 | QUBT | limit | 8.93 | -0.68 / -0.50 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -2.75% | +0.94 / -0.60 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-10-01 9:45 | 1.596 | stop | -4.46% | +0.51 / -0.59 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| UMAC | 2026-09-16 | 22.02 | 20.98 | 26.12 | 22.36 | +1.54% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $1000.00 | - |
| 2026-07-16 | $991.04 | IONQ, POET, QBTS |
| 2026-07-17 | $969.16 | IONQ |
| 2026-07-20 | $965.35 | IONQ |
| 2026-07-21 | $974.30 | IONQ |
| 2026-07-22 | $957.22 | IONQ, POET |
| 2026-07-23 | $953.09 | HIVE, IONQ |
| 2026-07-24 | $927.88 | - |
| 2026-07-27 | $930.55 | HOOD |
| 2026-07-28 | $913.50 | - |
| 2026-07-29 | $914.08 | AFRM, PCVX |
| 2026-07-30 | $933.17 | AFRM, PCVX |
| 2026-07-31 | $919.38 | AFRM, PCVX |
| 2026-08-03 | $930.48 | AFRM, PCVX |
| 2026-08-04 | $943.61 | AFRM, PCVX |
| 2026-08-05 | $948.32 | AFRM, PCVX, POET |
| 2026-08-06 | $967.42 | AFRM, POET |
| 2026-08-07 | $974.07 | AFRM, POET |
| 2026-08-10 | $964.89 | AFRM, POET |
| 2026-08-11 | $967.15 | AFRM, POET |
| 2026-08-12 | $964.45 | AFRM, POET |
| 2026-08-13 | $981.69 | AFRM, POET |
| 2026-08-14 | $1001.18 | AFRM, POET |
| 2026-08-17 | $983.45 | AFRM, POET |
| 2026-08-18 | $949.39 | AFRM, POET |
| 2026-08-19 | $954.04 | AFRM, POET |
| 2026-08-20 | $945.31 | AFRM, HOOD, POET |
| 2026-08-21 | $984.38 | AFRM, HOOD, POET |
| 2026-08-24 | $956.42 | AFRM, HOOD |
| 2026-08-25 | $986.00 | AFRM, HOOD, LUNR |
| 2026-08-26 | $964.95 | AFRM, HOOD, LUNR |
| 2026-08-27 | $972.44 | AFRM, HOOD, LUNR |
| 2026-08-28 | $972.53 | HOOD |
| 2026-08-31 | $973.93 | HOOD |
| 2026-09-01 | $971.21 | AXTI, HOOD, RCAT |
| 2026-09-02 | $977.75 | AXTI, HOOD |
| 2026-09-03 | $1000.83 | - |
| 2026-09-04 | $1000.24 | RCAT |
| 2026-09-08 | $1007.05 | RCAT, RXRX |
| 2026-09-09 | $975.14 | RCAT, RGTI |
| 2026-09-10 | $967.29 | - |
| 2026-09-11 | $967.29 | - |
| 2026-09-14 | $967.29 | - |
| 2026-09-15 | $967.29 | - |
| 2026-09-16 | $967.18 | UMAC |
| 2026-09-17 | $987.72 | UMAC |
| 2026-09-18 | $984.50 | RGTI, UMAC |
| 2026-09-21 | $1008.53 | RGTI, UMAC |
| 2026-09-22 | $1005.95 | RGTI, UMAC |
| 2026-09-23 | $983.02 | RGTI, UMAC |
| 2026-09-24 | $1010.87 | QUBT, RGTI, UMAC |
| 2026-09-25 | $1009.23 | QUBT, RGTI, UMAC |
| 2026-09-28 | $989.33 | RGTI, UMAC |
| 2026-09-29 | $993.78 | BTBT, RGTI, UMAC |
| 2026-09-30 | $985.76 | BTBT, RGTI, UMAC |
| 2026-10-01 | $949.08 | RGTI, UMAC |
| 2026-10-02 | $949.66 | RGTI, UMAC |
| 2026-10-05 | $939.11 | UMAC |
| 2026-10-06 | $944.93 | UMAC |

## Real-book rules + S&P gate + entries from 9:45: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $899.59 (-10.04%; realized $-110.49, open positions $+10.08); S&P 500 +3.63%, Nasdaq-100 +5.55%. 18 closed trades, 1 winners (5.6%), average trade -2.52%, average win 18.96%, average loss -3.78%, profit factor 0.27, worst drawdown -11.65%. Exits: target 1, stop 17. Resting orders filled: 20/108.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -1.01%, total $-14.61
- stopped on a later session: 11 trades, 0 won, average -5.30%, total $-137.76
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -5.19%, total $-62.26
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -3.19%, total $-83.26
- crypto-linked: 3 trades, 1 won, average +2.68%, total $+16.72
- bought on a dip of 0.5+ ATR (any time): 8 trades, 0 won, average -1.96%, total $-38.01
- bought less than 0.25 ATR under the prior close: 6 trades, 1 won, average -0.98%, total $-15.61
- resting limit fills: 18 trades, 1 won, average -2.52%, total $-110.49
- support tested 3+ times: 18 trades, 1 won, average -2.52%, total $-110.49

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-22 12:25 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.01 / -0.68 |
| 2026-07-24 9:45 | APLD | limit | 28.59 | -0.29 / -0.53 | 5.09 | 2026-07-24 9:45 | 28.58 | stop | -0.06% | +0.00 / -0.11 |
| 2026-07-24 10:30 | HOOD | limit | 94.37 | -0.28 / -1.14 | 6.19 | 2026-07-28 9:30 | 90.53 | stop | -4.07% | +0.80 / -0.72 |
| 2026-07-28 9:45 | HIMX | limit | 11.78 | -0.73 / -1.05 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -2.07% | +0.06 / -0.26 |
| 2026-07-30 9:45 | NOW | limit | 110.1 | -0.79 / -0.85 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -1.76% | +0.00 / -0.31 |
| 2026-08-05 9:45 | QUBT | limit | 9.06 | -0.20 / -0.31 | 6.66 | 2026-08-06 9:30 | 8.473 | stop | -6.49% | +0.20 / -1.08 |
| 2026-08-05 9:45 | ONDS | limit | 8.93 | +0.17 / +0.09 | 5.66 | 2026-08-20 9:50 | 8.466 | stop | -5.21% | +1.42 / -0.63 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-11 9:45 | RKLB | limit | 76.26 | -0.63 / -0.63 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -1.00% | +0.00 / -0.13 |
| 2026-08-24 9:45 | SMCI | limit | 34.87 | -0.28 / -0.93 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -0.64% | +0.00 / -0.09 |
| 2026-08-24 9:45 | RXRX | limit | 3.235 | -0.48 / -1.43 | 5.59 | 2026-08-24 9:45 | 3.219 | stop | -0.51% | +0.00 / -0.08 |
| 2026-08-25 9:45 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-25 9:45 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 10:40 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-09-02 9:45 | MARA (crypto) | limit | 10.23 | -0.24 / +0.00 | 3.48 | 2026-09-11 10:05 | 12.17 | target | +18.96% | +2.31 / -0.20 |
| 2026-09-04 9:45 | RCAT | limit | 8.39 | -0.07 / -0.24 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -3.63% | +0.84 / -0.50 |
| 2026-09-09 9:45 | RGTI | limit | 15.67 | -0.18 / -0.14 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.34% | +0.27 / -0.81 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| UMAC | 2026-09-16 | 22.02 | 20.98 | 26.12 | 22.36 | +1.54% |
| WULF | 2026-10-01 | 14.55 | 13.95 | 17.75 | 14.97 | +2.89% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $1000.00 | - |
| 2026-07-16 | $1000.00 | - |
| 2026-07-17 | $1000.00 | - |
| 2026-07-20 | $1000.00 | - |
| 2026-07-21 | $1000.00 | - |
| 2026-07-22 | $988.47 | POET |
| 2026-07-23 | $983.93 | - |
| 2026-07-24 | $985.19 | HOOD |
| 2026-07-27 | $987.12 | HOOD |
| 2026-07-28 | $968.66 | - |
| 2026-07-29 | $968.66 | - |
| 2026-07-30 | $964.41 | - |
| 2026-07-31 | $964.41 | - |
| 2026-08-03 | $964.41 | - |
| 2026-08-04 | $964.41 | - |
| 2026-08-05 | $956.22 | ONDS, POET, QUBT |
| 2026-08-06 | $954.88 | ONDS, POET |
| 2026-08-07 | $976.11 | ONDS, POET |
| 2026-08-10 | $971.16 | ONDS, POET |
| 2026-08-11 | $981.22 | ONDS, POET |
| 2026-08-12 | $990.32 | ONDS, POET |
| 2026-08-13 | $968.28 | ONDS, POET |
| 2026-08-14 | $997.01 | ONDS, POET |
| 2026-08-17 | $985.21 | ONDS, POET |
| 2026-08-18 | $959.61 | ONDS, POET |
| 2026-08-19 | $954.11 | ONDS, POET |
| 2026-08-20 | $937.33 | POET |
| 2026-08-21 | $936.74 | POET |
| 2026-08-24 | $917.71 | - |
| 2026-08-25 | $923.37 | LUNR, SOUN |
| 2026-08-26 | $922.83 | BTBT, LUNR, SOUN |
| 2026-08-27 | $935.27 | BTBT, LUNR, SOUN |
| 2026-08-28 | $892.04 | SOUN |
| 2026-08-31 | $893.68 | SOUN |
| 2026-09-01 | $883.53 | SOUN |
| 2026-09-02 | $886.42 | MARA, SOUN |
| 2026-09-03 | $908.17 | MARA |
| 2026-09-04 | $901.37 | MARA, RCAT |
| 2026-09-08 | $921.40 | MARA, RCAT |
| 2026-09-09 | $901.73 | MARA, RCAT, RGTI |
| 2026-09-10 | $883.97 | MARA |
| 2026-09-11 | $899.94 | - |
| 2026-09-14 | $899.94 | - |
| 2026-09-15 | $899.94 | - |
| 2026-09-16 | $899.84 | UMAC |
| 2026-09-17 | $918.95 | UMAC |
| 2026-09-18 | $911.79 | UMAC |
| 2026-09-21 | $922.73 | UMAC |
| 2026-09-22 | $920.48 | UMAC |
| 2026-09-23 | $906.79 | UMAC |
| 2026-09-24 | $919.46 | UMAC |
| 2026-09-25 | $922.00 | BTBT, UMAC |
| 2026-09-28 | $910.57 | BTBT, UMAC |
| 2026-09-29 | $919.35 | UMAC |
| 2026-09-30 | $914.65 | UMAC |
| 2026-10-01 | $892.72 | UMAC, WULF |
| 2026-10-02 | $907.86 | UMAC, WULF |
| 2026-10-05 | $891.34 | UMAC, WULF |
| 2026-10-06 | $899.59 | UMAC, WULF |

## Real-book rules + 1% gap allowance: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $1027.72 (+2.77%; realized $-25.44, open positions $+53.16); S&P 500 +3.63%, Nasdaq-100 +5.55%. 20 closed trades, 3 winners (15.0%), average trade -0.61%, average win 20.29%, average loss -4.3%, profit factor 0.85, worst drawdown -8.55%. Exits: target 3, stop 17. Resting orders filled: 21/57.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -2.20%, total $-21.01
- stopped on a later session: 13 trades, 0 won, average -4.95%, total $-148.03
- stopped at the open (gapped through the stop): 8 trades, 0 won, average -5.28%, total $-94.73
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -4.48%, total $-108.09
- crypto-linked: 2 trades, 0 won, average -4.64%, total $-23.19
- bought at the open after a gap down of 0.5+ ATR: 5 trades, 0 won, average -2.15%, total $-26.22
- bought on a dip of 0.5+ ATR (any time): 10 trades, 2 won, average +0.78%, total $+16.27
- bought less than 0.25 ATR under the prior close: 5 trades, 0 won, average -4.59%, total $-58.82
- resting limit fills: 20 trades, 3 won, average -0.61%, total $-25.44
- support tested 3+ times: 20 trades, 3 won, average -0.61%, total $-25.44

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-16 9:35 | POET | limit | 7.84 | -0.38 / -0.49 | 6.82 | 2026-07-17 9:30 | 7.304 | stop | -6.85% | +0.49 / -0.63 |
| 2026-07-16 11:55 | QBTS | limit | 17.29 | -0.17 / -0.61 | 4.2 | 2026-07-17 9:30 | 16.3 | stop | -5.74% | +0.06 / -0.74 |
| 2026-07-16 13:05 | IONQ | limit | 35.14 | -0.14 / -0.67 | 6.11 | 2026-07-24 9:50 | 33 | stop | -6.11% | +0.33 / -0.65 |
| 2026-07-22 9:35 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.25 / -0.68 |
| 2026-07-23 9:30 | HIVE (crypto) | limit | 3.1 | -0.36 / -0.36 | 13.88 | 2026-07-24 15:40 | 2.951 | stop | -4.83% | +0.80 / -0.56 |
| 2026-07-27 10:30 | HOOD | limit | 94.56 | +0.33 / -0.05 | 6.05 | 2026-07-28 9:30 | 90.67 | stop | -4.12% | +0.20 / -0.74 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-29 10:10 | AFRM | limit | 69.88 | -0.41 / -0.73 | 7.68 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +5.96 / -0.08 |
| 2026-07-29 10:20 | PCVX | limit | 53.02 | -0.05 / -0.72 | 4.0 | 2026-08-06 10:05 | 58.84 | target | +10.96% | +2.70 / -0.25 |
| 2026-07-30 9:30 | NOW | limit | 110.5 | -0.79 / -0.79 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -2.11% | +0.10 / -0.37 |
| 2026-08-11 9:30 | RKLB | limit | 76.27 | -0.63 / -0.63 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -1.01% | +0.44 / -0.14 |
| 2026-08-12 9:30 | RKLB | limit | 79.14 | +0.02 / -0.14 | 18.98 | 2026-08-19 9:35 | 75.41 | stop | -4.72% | +1.04 / -0.70 |
| 2026-08-20 15:00 | HOOD | limit | 93.67 | +1.11 / -0.46 | 9.0 | 2026-09-03 9:50 | 119 | target | +27.08% | +6.23 / -0.00 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.11% | +0.22 / -0.47 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-14 9:30 | QUBT | limit | 7.72 | -0.73 / -0.73 | 4.36 | 2026-09-14 9:30 | 7.624 | stop | -1.25% | +0.00 / -0.24 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.35% | +2.65 / -0.75 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.98% | +1.12 / -0.42 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-10-01 9:45 | 1.596 | stop | -4.46% | +0.51 / -0.59 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.06 | 11.57 | 15.81 | 14.85 | +23.13% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $1000.00 | - |
| 2026-07-16 | $990.60 | IONQ, POET, QBTS |
| 2026-07-17 | $971.24 | IONQ |
| 2026-07-20 | $967.97 | IONQ |
| 2026-07-21 | $975.65 | IONQ |
| 2026-07-22 | $960.36 | IONQ, POET |
| 2026-07-23 | $958.82 | HIVE, IONQ |
| 2026-07-24 | $934.51 | - |
| 2026-07-27 | $937.20 | HOOD |
| 2026-07-28 | $914.51 | - |
| 2026-07-29 | $915.09 | AFRM, PCVX |
| 2026-07-30 | $933.39 | AFRM, PCVX |
| 2026-07-31 | $919.59 | AFRM, PCVX |
| 2026-08-03 | $944.42 | AFRM, HIMX, PCVX |
| 2026-08-04 | $984.26 | AFRM, HIMX, PCVX |
| 2026-08-05 | $974.88 | AFRM, HIMX, PCVX |
| 2026-08-06 | $989.07 | AFRM, HIMX |
| 2026-08-07 | $1000.92 | AFRM, HIMX |
| 2026-08-10 | $1004.16 | AFRM, HIMX |
| 2026-08-11 | $1010.19 | AFRM, HIMX |
| 2026-08-12 | $1007.95 | AFRM, HIMX, RKLB |
| 2026-08-13 | $1012.44 | AFRM, HIMX, RKLB |
| 2026-08-14 | $1023.88 | AFRM, HIMX, RKLB |
| 2026-08-17 | $1020.62 | AFRM, HIMX, RKLB |
| 2026-08-18 | $988.34 | AFRM, HIMX, RKLB |
| 2026-08-19 | $979.74 | AFRM, HIMX |
| 2026-08-20 | $971.63 | AFRM, HIMX, HOOD |
| 2026-08-21 | $1014.47 | AFRM, HIMX, HOOD |
| 2026-08-24 | $995.51 | AFRM, HIMX, HOOD |
| 2026-08-25 | $1025.53 | AFRM, HIMX, HOOD |
| 2026-08-26 | $1014.63 | AFRM, HIMX, HOOD |
| 2026-08-27 | $1025.57 | AFRM, HIMX, HOOD |
| 2026-08-28 | $1030.32 | HIMX, HOOD |
| 2026-08-31 | $1033.28 | HIMX, HOOD |
| 2026-09-01 | $1018.63 | AXTI, HIMX, HOOD |
| 2026-09-02 | $1031.78 | AXTI, HIMX, HOOD |
| 2026-09-03 | $1057.56 | HIMX |
| 2026-09-04 | $1056.73 | HIMX, RCAT |
| 2026-09-08 | $1075.26 | HIMX, RCAT |
| 2026-09-09 | $1047.67 | HIMX, RCAT, RGTI |
| 2026-09-10 | $1036.06 | HIMX |
| 2026-09-11 | $1054.17 | HIMX |
| 2026-09-14 | $1029.34 | HIMX |
| 2026-09-15 | $1022.10 | HIMX |
| 2026-09-16 | $1018.86 | HIMX |
| 2026-09-17 | $1030.68 | HIMX |
| 2026-09-18 | $1042.01 | HIMX, RGTI |
| 2026-09-21 | $1066.08 | HIMX, RGTI |
| 2026-09-22 | $1067.82 | HIMX, RGTI |
| 2026-09-23 | $1051.05 | HIMX, RGTI |
| 2026-09-24 | $1065.13 | HIMX, QUBT, RGTI |
| 2026-09-25 | $1067.96 | HIMX, QUBT, RGTI |
| 2026-09-28 | $1038.82 | HIMX, RGTI |
| 2026-09-29 | $1034.88 | BTBT, HIMX, RGTI |
| 2026-09-30 | $1031.20 | BTBT, HIMX, RGTI |
| 2026-10-01 | $1031.07 | HIMX, RGTI |
| 2026-10-02 | $1039.97 | HIMX, RGTI |
| 2026-10-05 | $1025.06 | HIMX |
| 2026-10-06 | $1027.72 | HIMX |

## Real-book rules + S&P gate + 9:45 + 1% gap allowance: 2026-07-15 to 2026-10-06 (59 sessions)

$1000 -> $902.91 (-9.71%; realized $-107.20, open positions $+10.11); S&P 500 +3.63%, Nasdaq-100 +5.55%. 18 closed trades, 1 winners (5.6%), average trade -2.52%, average win 18.96%, average loss -3.78%, profit factor 0.27, worst drawdown -11.18%. Exits: target 1, stop 17. Resting orders filled: 20/108.

### What the trades had in common

- stopped the session it was bought: 6 trades, 0 won, average -1.01%, total $-14.63
- stopped on a later session: 11 trades, 0 won, average -5.30%, total $-131.95
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -5.19%, total $-61.00
- never rose 0.5 ATR above the entry: 11 trades, 0 won, average -3.19%, total $-80.00
- crypto-linked: 3 trades, 1 won, average +2.68%, total $+16.06
- bought on a dip of 0.5+ ATR (any time): 8 trades, 0 won, average -1.96%, total $-37.33
- bought less than 0.25 ATR under the prior close: 6 trades, 1 won, average -0.98%, total $-16.21
- resting limit fills: 18 trades, 1 won, average -2.52%, total $-107.20
- support tested 3+ times: 18 trades, 1 won, average -2.52%, total $-107.20

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-22 12:25 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.01 / -0.68 |
| 2026-07-24 9:45 | APLD | limit | 28.59 | -0.29 / -0.53 | 5.09 | 2026-07-24 9:45 | 28.58 | stop | -0.06% | +0.00 / -0.11 |
| 2026-07-24 10:30 | HOOD | limit | 94.37 | -0.28 / -1.14 | 6.19 | 2026-07-28 9:30 | 90.53 | stop | -4.07% | +0.80 / -0.72 |
| 2026-07-28 9:45 | HIMX | limit | 11.78 | -0.73 / -1.05 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -2.07% | +0.06 / -0.26 |
| 2026-07-30 9:45 | NOW | limit | 110.1 | -0.79 / -0.85 | 6.31 | 2026-07-30 9:50 | 108.2 | stop | -1.76% | +0.00 / -0.31 |
| 2026-08-05 9:45 | QUBT | limit | 9.06 | -0.20 / -0.31 | 6.66 | 2026-08-06 9:30 | 8.473 | stop | -6.49% | +0.20 / -1.08 |
| 2026-08-05 9:45 | ONDS | limit | 8.93 | +0.17 / +0.09 | 5.66 | 2026-08-20 9:50 | 8.466 | stop | -5.21% | +1.42 / -0.63 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-11 9:45 | RKLB | limit | 76.26 | -0.63 / -0.63 | 19.47 | 2026-08-11 9:45 | 75.5 | stop | -1.00% | +0.00 / -0.13 |
| 2026-08-24 9:45 | SMCI | limit | 34.87 | -0.28 / -0.93 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -0.64% | +0.00 / -0.09 |
| 2026-08-24 9:45 | RXRX | limit | 3.235 | -0.48 / -1.43 | 5.59 | 2026-08-24 9:45 | 3.219 | stop | -0.51% | +0.00 / -0.08 |
| 2026-08-25 9:45 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-25 9:45 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 10:40 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-09-02 9:45 | MARA (crypto) | limit | 10.23 | -0.24 / +0.00 | 3.48 | 2026-09-11 10:05 | 12.17 | target | +18.96% | +2.31 / -0.20 |
| 2026-09-04 9:45 | RCAT | limit | 8.39 | -0.07 / -0.24 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -3.63% | +0.84 / -0.50 |
| 2026-09-09 9:45 | RGTI | limit | 15.67 | -0.18 / -0.14 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.34% | +0.27 / -0.81 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| UMAC | 2026-09-16 | 22.02 | 20.98 | 26.12 | 22.36 | +1.54% |
| WULF | 2026-10-01 | 14.55 | 13.95 | 17.75 | 14.97 | +2.89% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-15 | $1000.00 | - |
| 2026-07-16 | $1000.00 | - |
| 2026-07-17 | $1000.00 | - |
| 2026-07-20 | $1000.00 | - |
| 2026-07-21 | $1000.00 | - |
| 2026-07-22 | $989.47 | POET |
| 2026-07-23 | $985.32 | - |
| 2026-07-24 | $986.59 | HOOD |
| 2026-07-27 | $988.52 | HOOD |
| 2026-07-28 | $970.04 | - |
| 2026-07-29 | $970.04 | - |
| 2026-07-30 | $965.78 | - |
| 2026-07-31 | $965.78 | - |
| 2026-08-03 | $965.78 | - |
| 2026-08-04 | $965.78 | - |
| 2026-08-05 | $957.68 | ONDS, POET, QUBT |
| 2026-08-06 | $955.62 | ONDS, POET |
| 2026-08-07 | $976.25 | ONDS, POET |
| 2026-08-10 | $971.85 | ONDS, POET |
| 2026-08-11 | $981.87 | ONDS, POET |
| 2026-08-12 | $990.51 | ONDS, POET |
| 2026-08-13 | $968.42 | ONDS, POET |
| 2026-08-14 | $996.08 | ONDS, POET |
| 2026-08-17 | $984.56 | ONDS, POET |
| 2026-08-18 | $960.43 | ONDS, POET |
| 2026-08-19 | $954.99 | ONDS, POET |
| 2026-08-20 | $938.49 | POET |
| 2026-08-21 | $937.93 | POET |
| 2026-08-24 | $919.78 | - |
| 2026-08-25 | $924.83 | LUNR, SOUN |
| 2026-08-26 | $924.27 | BTBT, LUNR, SOUN |
| 2026-08-27 | $936.01 | BTBT, LUNR, SOUN |
| 2026-08-28 | $897.99 | SOUN |
| 2026-08-31 | $899.63 | SOUN |
| 2026-09-01 | $889.46 | SOUN |
| 2026-09-02 | $892.04 | MARA, SOUN |
| 2026-09-03 | $912.33 | MARA |
| 2026-09-04 | $905.90 | MARA, RCAT |
| 2026-09-08 | $925.29 | MARA, RCAT |
| 2026-09-09 | $905.41 | MARA, RCAT, RGTI |
| 2026-09-10 | $888.25 | MARA |
| 2026-09-11 | $903.27 | - |
| 2026-09-14 | $903.27 | - |
| 2026-09-15 | $903.27 | - |
| 2026-09-16 | $903.17 | UMAC |
| 2026-09-17 | $922.34 | UMAC |
| 2026-09-18 | $915.16 | UMAC |
| 2026-09-21 | $926.14 | UMAC |
| 2026-09-22 | $923.88 | UMAC |
| 2026-09-23 | $910.14 | UMAC |
| 2026-09-24 | $922.86 | UMAC |
| 2026-09-25 | $925.40 | BTBT, UMAC |
| 2026-09-28 | $913.93 | BTBT, UMAC |
| 2026-09-29 | $922.75 | UMAC |
| 2026-09-30 | $918.03 | UMAC |
| 2026-10-01 | $896.02 | UMAC, WULF |
| 2026-10-02 | $911.22 | UMAC, WULF |
| 2026-10-05 | $894.64 | UMAC, WULF |
| 2026-10-06 | $902.91 | UMAC, WULF |

