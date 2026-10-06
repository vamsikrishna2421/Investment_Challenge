# Replay of the rules, 2026-08-24 to 2026-10-05 (30 sessions, 5-minute bars)

$1,000 each; S&P 500 +1.19%, Nasdaq-100 +5.99% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Live rules (Oct 6): limits at support, stop 0.6 ATR under it | -6.41% | 14 | 7.1% | -3.35% | 0.25 | -13.08% | SMCI, NOW, WULF |
| Limits at the zone top | -16.27% | 13 | 0.0% | -7.4% | - | -17.6% | SMCI, HIMX, WULF |
| No resting limits: run entries only (the Oct 5 rules) | +8.59% | 31 | 25.8% | 0.93% | 1.12 | -8.64% | AXTI, NOW, RIOT, LUNR |
| Resting limits only, no run entries | -6.41% | 14 | 7.1% | -3.35% | 0.25 | -13.08% | SMCI, NOW, WULF |
| Stop 1.0 ATR under support | -11.52% | 12 | 8.3% | -5.64% | 0.16 | -18.19% | SMCI, RGTI, WULF, PATH |
| Stop 1.5 ATR under support | -13.46% | 5 | 0.0% | -12.83% | - | -16.38% | SMCI, RGTI, GPUS, PATH |
| Sell after 3 sessions if neither target nor stop | -12.91% | 31 | 29.0% | -1.75% | 0.43 | -12.91% | - |
| Bitcoin gate off | -5.98% | 14 | 7.1% | -3.35% | 0.28 | -13.08% | SMCI, NOW, WULF |
| Rank run entries by R:R instead of dip | -6.41% | 14 | 7.1% | -3.35% | 0.25 | -13.08% | SMCI, NOW, WULF |
| Opening gap-down 0.5+ ATR, sell at the prior close or the close | -13.55% | 45 | 40.0% | -1.25% | 0.38 | -15.29% | - |
| Limits cancelled at 10:00 (the first 30 minutes), runs after | -4.27% | 22 | 18.2% | -2.03% | 0.47 | -14.28% | SMCI, NOW, AXTI, RIOT |
| GPUS, IREN, BTDR only with a tested support | -3.14% | 13 | 7.7% | -2.59% | 0.33 | -10.07% | SMCI, NOW, WULF |
| Both of the above | +1.67% | 18 | 22.2% | -0.28% | 0.77 | -8.47% | SMCI, NOW, AXTI, WULF |
| Both, stop 1.0 ATR under support | +9.95% | 7 | 14.3% | -4.56% | 0.3 | -11.4% | SMCI, AXTI, HIMX, WULF |
| Run entries only, GPUS/IREN/BTDR only with a tested support | +10.63% | 30 | 26.7% | 1.22% | 1.2 | -8.64% | AXTI, NOW, RIOT, LUNR |

## Live rules (Oct 6): limits at support, stop 0.6 ATR under it: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $935.94 (-6.41%; realized $-120.40, open positions $+56.34); S&P 500 +1.19%, Nasdaq-100 +5.99%. 14 closed trades, 1 winners (7.1%), average trade -3.35%, average win 21.6%, average loss -5.27%, profit factor 0.25, worst drawdown -13.08%. Exits: target 1, stop 13. Resting orders filled: 17/40.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -6.83%, total $-65.39
- stopped on a later session: 9 trades, 0 won, average -4.58%, total $-95.06
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -4.26%, total $-37.30
- never rose 0.5 ATR above the entry: 9 trades, 0 won, average -5.53%, total $-116.68
- crypto-linked: 2 trades, 0 won, average -5.46%, total $-25.68
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+40.05
- bought on a dip of 0.5+ ATR (any time): 5 trades, 1 won, average -0.08%, total $-12.87
- bought less than 0.25 ATR under the prior close: 3 trades, 0 won, average -4.69%, total $-32.84
- resting limit fills: 14 trades, 1 won, average -3.35%, total $-120.40
- support tested 3+ times: 10 trades, 0 won, average -4.62%, total $-108.37
- support tested twice: 2 trades, 1 won, average +9.30%, total $+33.36
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-45.39

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
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.36% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

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
| 2026-09-01 | $923.75 | SMCI, SOUN |
| 2026-09-02 | $899.63 | SMCI, SOUN |
| 2026-09-03 | $902.49 | SMCI |
| 2026-09-04 | $911.05 | RCAT, SMCI |
| 2026-09-08 | $924.08 | RCAT, SMCI |
| 2026-09-09 | $893.13 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $869.25 | SMCI |
| 2026-09-11 | $890.43 | NOW, SMCI |
| 2026-09-14 | $890.93 | NOW, RKLB, SMCI |
| 2026-09-15 | $882.30 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $884.26 | NOW, RKLB, SMCI |
| 2026-09-17 | $917.46 | NOW, RKLB, SMCI |
| 2026-09-18 | $898.20 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $942.68 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $950.02 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $943.37 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $955.96 | NOW, RGTI, SMCI |
| 2026-09-25 | $967.30 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $930.49 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $918.88 | NOW, RGTI, SMCI |
| 2026-09-30 | $925.98 | NOW, RGTI, SMCI |
| 2026-10-01 | $941.42 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $950.76 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $935.94 | NOW, SMCI, WULF |

## Limits at the zone top: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $837.27 (-16.27%; realized $-219.62, open positions $+56.89); S&P 500 +1.19%, Nasdaq-100 +5.99%. 13 closed trades, 0 winners (0.0%), average trade -7.4%, average win None%, average loss -7.4%, profit factor 0.0, worst drawdown -17.6%. Exits: stop 13. Resting orders filled: 16/34.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -7.49%, total $-70.87
- stopped on a later session: 9 trades, 0 won, average -7.36%, total $-148.75
- stopped at the open (gapped through the stop): 1 trade, 0 won, average -5.09%, total $-11.41
- never rose 0.5 ATR above the entry: 10 trades, 0 won, average -7.69%, total $-175.42
- crypto-linked: 2 trades, 0 won, average -6.87%, total $-31.26
- bought on a dip of 0.5+ ATR (any time): 2 trades, 0 won, average -7.05%, total $-33.36
- bought less than 0.25 ATR under the prior close: 7 trades, 0 won, average -8.20%, total $-127.18
- resting limit fills: 13 trades, 0 won, average -7.40%, total $-219.62
- support tested 3+ times: 7 trades, 0 won, average -5.91%, total $-98.52
- support tested twice: 3 trades, 0 won, average -5.65%, total $-35.50
- radar keeps (GPUS, IREN, BTDR) without a tested support: 3 trades, 0 won, average -12.64%, total $-85.60

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.41 | -0.48 / -0.48 | 3.25 | 2026-08-24 9:35 | 3.274 | stop | -3.99% | +0.00 / -0.70 |
| 2026-08-24 9:30 | SMCI | limit | 36.52 | -0.28 / -0.28 | 5.97 | 2026-08-24 9:45 | 34.65 | stop | -5.13% | +0.00 / -0.74 |
| 2026-08-24 9:30 | LUNR | limit | 17.45 | -0.45 / -0.54 | 3.04 | 2026-08-26 11:15 | 15.98 | stop | -8.42% | +0.00 / -0.92 |
| 2026-08-25 9:30 | SOUN | limit | 7.05 | +0.10 / +0.10 | 3.31 | 2026-09-03 11:10 | 6.7 | stop | -4.98% | +0.69 / -0.71 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.53 | -0.35 / -0.35 | 4.58 | 2026-08-28 14:35 | 1.414 | stop | -7.60% | +0.95 / -0.77 |
| 2026-09-01 9:50 | GPUS | limit | 0.2711 | -0.05 / -0.24 | 5.09 | 2026-09-01 14:45 | 0.2366 | stop | -12.81% | +0.00 / -0.96 |
| 2026-09-02 9:30 | GPUS | limit | 0.2245 | -0.42 / -0.42 | 5.99 | 2026-09-02 11:10 | 0.2067 | stop | -8.01% | +0.37 / -0.54 |
| 2026-09-03 9:50 | GPUS | limit | 0.2011 | +0.42 / +0.03 | 7.19 | 2026-09-24 9:35 | 0.1669 | stop | -17.10% | +0.20 / -0.94 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 12.67 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-15 14:40 | BULL | limit | 8.54 | -0.35 / -0.96 | 2.69 | 2026-09-16 10:55 | 8.055 | stop | -5.69% | +0.33 / -0.93 |
| 2026-09-17 9:30 | PATH | limit | 13.47 | -0.15 / -0.15 | 5.14 | 2026-09-24 9:40 | 12.56 | stop | -6.73% | +0.53 / -0.90 |
| 2026-09-25 9:30 | BTBT (crypto) | limit | 1.78 | +0.09 / -0.09 | 5.71 | 2026-09-29 12:05 | 1.671 | stop | -6.14% | +0.13 / -0.94 |
| 2026-10-02 9:30 | PATH | limit | 13.41 | +0.14 / +0.14 | 8.73 | 2026-10-05 11:00 | 12.81 | stop | -4.53% | +0.00 / -0.90 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-26 | 37.41 | 34.99 | 50.59 | 43.19 | +15.45% |
| HIMX | 2026-09-03 | 13.27 | 12.75 | 15.9 | 14.71 | +10.85% |
| WULF | 2026-09-30 | 14.86 | 13.94 | 17.76 | 14.79 | -0.47% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $965.88 | LUNR |
| 2026-08-25 | $965.03 | LUNR, SOUN |
| 2026-08-26 | $959.39 | BTBT, SMCI, SOUN |
| 2026-08-27 | $978.21 | BTBT, SMCI, SOUN |
| 2026-08-28 | $937.74 | SMCI, SOUN |
| 2026-08-31 | $940.74 | SMCI, SOUN |
| 2026-09-01 | $896.32 | SMCI, SOUN |
| 2026-09-02 | $877.85 | SMCI, SOUN |
| 2026-09-03 | $872.67 | GPUS, HIMX, SMCI |
| 2026-09-04 | $885.46 | GPUS, HIMX, SMCI |
| 2026-09-08 | $896.00 | GPUS, HIMX, SMCI |
| 2026-09-09 | $890.34 | GPUS, HIMX, RGTI, SMCI |
| 2026-09-10 | $861.21 | GPUS, HIMX, SMCI |
| 2026-09-11 | $892.18 | GPUS, HIMX, SMCI |
| 2026-09-14 | $865.45 | GPUS, HIMX, SMCI |
| 2026-09-15 | $845.11 | BULL, GPUS, HIMX, SMCI |
| 2026-09-16 | $824.24 | GPUS, HIMX, SMCI |
| 2026-09-17 | $860.08 | GPUS, HIMX, PATH, SMCI |
| 2026-09-18 | $851.25 | GPUS, HIMX, PATH, SMCI |
| 2026-09-21 | $887.16 | GPUS, HIMX, PATH, SMCI |
| 2026-09-22 | $874.66 | GPUS, HIMX, PATH, SMCI |
| 2026-09-23 | $853.82 | GPUS, HIMX, PATH, SMCI |
| 2026-09-24 | $841.08 | HIMX, SMCI |
| 2026-09-25 | $854.52 | BTBT, HIMX, SMCI |
| 2026-09-28 | $828.75 | BTBT, HIMX, SMCI |
| 2026-09-29 | $824.72 | HIMX, SMCI |
| 2026-09-30 | $823.99 | HIMX, SMCI, WULF |
| 2026-10-01 | $835.99 | HIMX, SMCI, WULF |
| 2026-10-02 | $860.07 | HIMX, PATH, SMCI, WULF |
| 2026-10-05 | $837.27 | HIMX, SMCI, WULF |

## No resting limits: run entries only (the Oct 5 rules): 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1085.86 (+8.59%; realized $+32.84, open positions $+53.02); S&P 500 +1.19%, Nasdaq-100 +5.99%. 31 closed trades, 8 winners (25.8%), average trade 0.93%, average win 17.44%, average loss -4.82%, profit factor 1.12, worst drawdown -8.64%. Exits: target 8, stop 23.

### What the trades had in common

- stopped the session it was bought: 8 trades, 0 won, average -2.81%, total $-54.59
- stopped on a later session: 15 trades, 0 won, average -5.89%, total $-219.76
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -8.15%, total $-148.92
- never rose 0.5 ATR above the entry: 18 trades, 0 won, average -4.87%, total $-216.96
- crypto-linked: 5 trades, 2 won, average +5.13%, total $+57.17
- bought on a dip of 0.5+ ATR (any time): 15 trades, 3 won, average -0.62%, total $-36.29
- bought less than 0.25 ATR under the prior close: 7 trades, 3 won, average +5.76%, total $+90.20
- run entries inside the buy zone: 26 trades, 8 won, average +2.58%, total $+130.83
- run entries on a bounce (touched the zone, back above it): 5 trades, 0 won, average -7.68%, total $-97.99
- support tested 3+ times: 24 trades, 7 won, average +2.01%, total $+80.79
- support tested twice: 6 trades, 1 won, average -1.97%, total $-29.43
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -7.79%, total $-18.52

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:50 | POET | buy zone | 7.786 | -0.39 / -0.66 | 37.41 | 2026-08-24 10:00 | 7.699 | stop | -1.12% | +0.08 / -0.15 |
| 2026-08-24 9:50 | UMAC | buy zone | 24.92 | -0.25 / -0.76 | 14.36 | 2026-08-25 15:55 | 24.28 | stop | -2.56% | +0.13 / -0.23 |
| 2026-08-24 9:50 | LUNR | buy zone | 16.87 | -0.45 / -0.91 | 6.02 | 2026-08-26 11:15 | 15.98 | stop | -5.29% | +0.19 / -0.56 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:50 | CRCL (crypto) | buy zone | 86.33 | -0.53 / -0.25 | 3.65 | 2026-09-03 10:05 | 98.9 | target | +14.55% | +2.27 / -0.08 |
| 2026-08-26 9:50 | IONQ | bounce | 41.39 | -0.34 / -0.23 | 2.07 | 2026-09-01 9:30 | 37.85 | stop | -8.56% | +0.54 / -1.28 |
| 2026-08-27 11:20 | DELL | bounce | 465 | +0.11 / +0.04 | 1.52 | 2026-09-01 10:10 | 437.5 | stop | -5.93% | +0.36 / -1.05 |
| 2026-09-02 9:50 | GPUS | buy zone | 0.224 | -0.42 / -0.43 | 14.43 | 2026-09-02 11:10 | 0.2067 | stop | -7.79% | +0.39 / -0.53 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-04 9:50 | BULL | buy zone | 9.669 | -0.40 / -0.52 | 7.47 | 2026-09-08 15:35 | 9.44 | stop | -2.38% | +0.54 / -0.34 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.37% | +0.37 / -0.79 |
| 2026-09-09 9:50 | NNE | buy zone | 18.92 | -0.09 / -0.37 | 5.78 | 2026-09-09 11:00 | 18.39 | stop | -2.85% | +0.01 / -0.48 |
| 2026-09-09 9:50 | SMR | buy zone | 10.89 | -0.24 / -0.42 | 8.09 | 2026-09-10 9:30 | 10.45 | stop | -4.01% | +0.20 / -0.87 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-10 9:50 | NBIS | buy zone | 230.1 | -0.61 / -0.75 | 5.38 | 2026-09-14 9:30 | 204.9 | stop | -10.98% | +0.34 / -1.93 |
| 2026-09-10 9:50 | AXTI | bounce | 66.01 | -0.48 / -0.47 | 3.72 | 2026-09-14 9:30 | 59.65 | stop | -9.65% | +0.46 / -1.26 |
| 2026-09-11 9:50 | SOFI | buy zone | 17.24 | +0.14 / +0.03 | 3.2 | 2026-09-16 14:55 | 16.65 | stop | -3.39% | +0.64 / -0.80 |
| 2026-09-11 9:50 | GRAL | buy zone | 77.1 | +0.01 / -0.10 | 1.95 | 2026-09-21 9:50 | 98.6 | target | +27.88% | +5.49 / -0.82 |
| 2026-09-15 9:50 | RXRX | buy zone | 3.306 | -0.27 / -0.55 | 1.95 | 2026-09-18 10:50 | 3.592 | target | +8.62% | +1.64 / -0.78 |
| 2026-09-15 9:50 | APLD | buy zone | 24.36 | -0.18 / -0.14 | 2.81 | 2026-09-21 11:20 | 28.34 | target | +16.33% | +2.62 / -0.60 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-10-02 10:05 | 91.76 | target | +14.93% | +2.37 / -0.29 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 2.69 | 2026-09-24 13:40 | 9.158 | stop | -4.11% | +1.10 / -0.90 |
| 2026-09-22 9:50 | AXTI | bounce | 77.49 | -0.55 / -0.41 | 1.92 | 2026-09-24 9:30 | 70.06 | stop | -9.60% | +0.21 / -1.32 |
| 2026-09-22 9:50 | GPUS | buy zone | 0.1812 | -0.01 / -0.38 | 17.16 | 2026-09-25 9:30 | 0.164 | stop | -9.57% | +0.14 / -1.00 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.17% | +1.68 / -0.01 |
| 2026-09-25 9:50 | IREN (crypto) | buy zone | 44.44 | -0.33 / -0.62 | 4.8 | 2026-09-25 10:00 | 43.55 | stop | -2.00% | +0.01 / -0.32 |
| 2026-09-25 9:50 | BTDR (crypto) | buy zone | 11.72 | +0.06 / -0.51 | 5.82 | 2026-09-25 10:00 | 11.47 | stop | -2.17% | +0.00 / -0.34 |
| 2026-09-28 9:50 | POET | buy zone | 7.515 | -0.54 / -0.57 | 7.47 | 2026-09-28 10:45 | 7.359 | stop | -2.08% | +0.01 / -0.43 |
| 2026-09-28 9:50 | SMCI | buy zone | 42.29 | -0.20 / -0.42 | 4.81 | 2026-09-30 11:55 | 40.49 | stop | -4.26% | +0.17 / -0.78 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| AXTI | 2026-09-28 | 74.11 | 71.04 | 89.34 | 86.66 | +16.94% |
| NOW | 2026-09-29 | 130.6 | 127.1 | 146.9 | 136.1 | +4.16% |
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 19.32 | -1.78% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 14.29 | +1.07% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $991.07 | CRSP, LUNR, UMAC |
| 2026-08-25 | $1020.34 | CRCL, CRSP, LUNR |
| 2026-08-26 | $989.82 | CRCL, CRSP, IONQ |
| 2026-08-27 | $1020.82 | CRCL, CRSP, DELL, IONQ |
| 2026-08-28 | $965.90 | CRCL, CRSP, DELL, IONQ |
| 2026-08-31 | $987.27 | CRCL, CRSP, DELL, IONQ |
| 2026-09-01 | $951.09 | CRCL, CRSP |
| 2026-09-02 | $936.90 | CRCL, CRSP, WULF |
| 2026-09-03 | $981.76 | AEHR, CRSP, WULF |
| 2026-09-04 | $1012.86 | AEHR, BULL, CRSP, WULF |
| 2026-09-08 | $1018.56 | AEHR, DUOL |
| 2026-09-09 | $1031.73 | SMR |
| 2026-09-10 | $1011.64 | AXTI, NBIS |
| 2026-09-11 | $1006.29 | AXTI, GRAL, NBIS, SOFI |
| 2026-09-14 | $966.69 | GRAL, SOFI |
| 2026-09-15 | $946.09 | APLD, GRAL, RXRX, SOFI |
| 2026-09-16 | $942.61 | APLD, GRAL, RXRX |
| 2026-09-17 | $1002.26 | APLD, CRWV, GRAL, RXRX |
| 2026-09-18 | $1028.87 | APLD, CRWV, GRAL |
| 2026-09-21 | $1105.64 | CRWV, STNE |
| 2026-09-22 | $1112.85 | AXTI, CRWV, GPUS, STNE |
| 2026-09-23 | $1070.88 | AXTI, CRWV, GPUS, STNE |
| 2026-09-24 | $1078.94 | CRWV, GPUS, HIMS |
| 2026-09-25 | $1036.98 | CRWV |
| 2026-09-28 | $1019.52 | AXTI, CRWV, SMCI |
| 2026-09-29 | $1031.80 | AXTI, CRWV, NOW, SMCI |
| 2026-09-30 | $1037.28 | AXTI, CRWV, NOW |
| 2026-10-01 | $1063.51 | AXTI, CRWV, NOW, RIOT |
| 2026-10-02 | $1082.05 | AXTI, NOW, RIOT |
| 2026-10-05 | $1085.86 | AXTI, LUNR, NOW, RIOT |

## Resting limits only, no run entries: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $935.94 (-6.41%; realized $-120.40, open positions $+56.34); S&P 500 +1.19%, Nasdaq-100 +5.99%. 14 closed trades, 1 winners (7.1%), average trade -3.35%, average win 21.6%, average loss -5.27%, profit factor 0.25, worst drawdown -13.08%. Exits: target 1, stop 13. Resting orders filled: 17/40.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -6.83%, total $-65.39
- stopped on a later session: 9 trades, 0 won, average -4.58%, total $-95.06
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -4.26%, total $-37.30
- never rose 0.5 ATR above the entry: 9 trades, 0 won, average -5.53%, total $-116.68
- crypto-linked: 2 trades, 0 won, average -5.46%, total $-25.68
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+40.05
- bought on a dip of 0.5+ ATR (any time): 5 trades, 1 won, average -0.08%, total $-12.87
- bought less than 0.25 ATR under the prior close: 3 trades, 0 won, average -4.69%, total $-32.84
- resting limit fills: 14 trades, 1 won, average -3.35%, total $-120.40
- support tested 3+ times: 10 trades, 0 won, average -4.62%, total $-108.37
- support tested twice: 2 trades, 1 won, average +9.30%, total $+33.36
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-45.39

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
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.36% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

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
| 2026-09-01 | $923.75 | SMCI, SOUN |
| 2026-09-02 | $899.63 | SMCI, SOUN |
| 2026-09-03 | $902.49 | SMCI |
| 2026-09-04 | $911.05 | RCAT, SMCI |
| 2026-09-08 | $924.08 | RCAT, SMCI |
| 2026-09-09 | $893.13 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $869.25 | SMCI |
| 2026-09-11 | $890.43 | NOW, SMCI |
| 2026-09-14 | $890.93 | NOW, RKLB, SMCI |
| 2026-09-15 | $882.30 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $884.26 | NOW, RKLB, SMCI |
| 2026-09-17 | $917.46 | NOW, RKLB, SMCI |
| 2026-09-18 | $898.20 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $942.68 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $950.02 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $943.37 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $955.96 | NOW, RGTI, SMCI |
| 2026-09-25 | $967.30 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $930.49 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $918.88 | NOW, RGTI, SMCI |
| 2026-09-30 | $925.98 | NOW, RGTI, SMCI |
| 2026-10-01 | $941.42 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $950.76 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $935.94 | NOW, SMCI, WULF |

## Stop 1.0 ATR under support: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $884.79 (-11.52%; realized $-161.60, open positions $+46.39); S&P 500 +1.19%, Nasdaq-100 +5.99%. 12 closed trades, 1 winners (8.3%), average trade -5.64%, average win 18.45%, average loss -7.83%, profit factor 0.16, worst drawdown -18.19%. Exits: target 1, stop 11. Resting orders filled: 16/37.

### What the trades had in common

- stopped the session it was bought: 1 trade, 0 won, average -5.89%, total $-14.71
- stopped on a later session: 10 trades, 0 won, average -8.02%, total $-177.60
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -8.41%, total $-69.78
- never rose 0.5 ATR above the entry: 6 trades, 0 won, average -8.12%, total $-113.13
- crypto-linked: 2 trades, 0 won, average -8.35%, total $-35.29
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -3.71%, total $-8.35
- bought on a dip of 0.5+ ATR (any time): 4 trades, 0 won, average -8.49%, total $-80.40
- bought less than 0.25 ATR under the prior close: 3 trades, 0 won, average -8.07%, total $-52.12
- resting limit fills: 12 trades, 1 won, average -5.64%, total $-161.60
- support tested 3+ times: 9 trades, 0 won, average -7.41%, total $-149.12
- support tested twice: 2 trades, 1 won, average +6.89%, total $+20.90
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -14.77%, total $-33.38

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 3.33 | 2026-08-24 9:50 | 3.2 | stop | -5.89% | +0.00 / -1.00 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 3.04 | 2026-08-28 12:00 | 15.35 | stop | -9.58% | +0.13 / -1.01 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 3.29 | 2026-09-08 10:35 | 6.503 | stop | -7.24% | +0.77 / -1.01 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 4.32 | 2026-09-01 9:30 | 1.357 | stop | -10.14% | +1.09 / -1.05 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 4.88 | 2026-09-02 9:40 | 0.2218 | stop | -14.77% | +0.00 / -1.01 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 3.34 | 2026-09-14 9:30 | 7.645 | stop | -9.75% | +0.71 / -1.35 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 11.63 | 2026-09-14 9:30 | 14.5 | stop | -7.22% | +0.30 / -1.09 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 4.52 | 2026-09-10 14:15 | 10.17 | stop | -6.60% | +0.20 / -1.00 |
| 2026-09-15 10:50 | APLD | limit | 23.92 | -0.18 / -0.41 | 2.69 | 2026-09-21 11:20 | 28.34 | target | +18.45% | +2.89 / -0.33 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 2.79 | 2026-09-17 15:25 | 2.822 | stop | -4.67% | +0.24 / -1.05 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 14.2 | 2026-09-28 15:50 | 8.532 | stop | -3.71% | +1.12 / -0.89 |
| 2026-09-24 9:30 | BTBT (crypto) | limit | 1.725 | -0.35 / -0.35 | 4.64 | 2026-10-01 9:30 | 1.612 | stop | -6.55% | +0.74 / -0.81 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-24 | 36.2 | 33.65 | 50.64 | 43.19 | +19.31% |
| RGTI | 2026-09-18 | 15.48 | 14.66 | 27.68 | 15.15 | -2.13% |
| WULF | 2026-10-01 | 14.55 | 13.54 | 17.75 | 14.79 | +1.65% |
| PATH | 2026-10-02 | 13.23 | 12.57 | 18.63 | 13.16 | -0.53% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $973.61 | LUNR, SMCI |
| 2026-08-25 | $996.83 | LUNR, SMCI, SOUN |
| 2026-08-26 | $988.85 | BTBT, LUNR, SMCI, SOUN |
| 2026-08-27 | $1009.36 | BTBT, LUNR, SMCI, SOUN |
| 2026-08-28 | $958.06 | BTBT, SMCI, SOUN |
| 2026-08-31 | $961.18 | BTBT, SMCI, SOUN |
| 2026-09-01 | $917.37 | GPUS, SMCI, SOUN |
| 2026-09-02 | $900.95 | SMCI, SOUN |
| 2026-09-03 | $905.57 | SMCI, SOUN |
| 2026-09-04 | $915.28 | RCAT, SMCI, SOUN |
| 2026-09-08 | $918.70 | RCAT, SMCI |
| 2026-09-09 | $889.90 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $863.88 | RCAT, RGTI, SMCI |
| 2026-09-11 | $881.68 | RCAT, RGTI, SMCI |
| 2026-09-14 | $840.33 | SMCI |
| 2026-09-15 | $825.71 | APLD, GRAB, SMCI |
| 2026-09-16 | $837.97 | APLD, GRAB, SMCI |
| 2026-09-17 | $872.57 | APLD, SMCI |
| 2026-09-18 | $879.92 | APLD, RGTI, SMCI |
| 2026-09-21 | $906.83 | RGTI, SMCI |
| 2026-09-22 | $909.04 | RGTI, SMCI |
| 2026-09-23 | $901.09 | RGTI, SMCI |
| 2026-09-24 | $922.36 | BTBT, QUBT, RGTI, SMCI |
| 2026-09-25 | $928.76 | BTBT, QUBT, RGTI, SMCI |
| 2026-09-28 | $890.03 | BTBT, RGTI, SMCI |
| 2026-09-29 | $878.97 | BTBT, RGTI, SMCI |
| 2026-09-30 | $877.41 | BTBT, RGTI, SMCI |
| 2026-10-01 | $885.24 | RGTI, SMCI, WULF |
| 2026-10-02 | $899.62 | PATH, RGTI, SMCI, WULF |
| 2026-10-05 | $884.79 | PATH, RGTI, SMCI, WULF |

## Stop 1.5 ATR under support: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $865.37 (-13.46%; realized $-150.73, open positions $+16.10); S&P 500 +1.19%, Nasdaq-100 +5.99%. 5 closed trades, 0 winners (0.0%), average trade -12.83%, average win None%, average loss -12.83%, profit factor 0.0, worst drawdown -16.38%. Exits: stop 5. Resting orders filled: 8/17.

### What the trades had in common

- stopped on a later session: 5 trades, 0 won, average -12.83%, total $-150.73
- stopped at the open (gapped through the stop): 1 trade, 0 won, average -8.60%, total $-21.51
- never rose 0.5 ATR above the entry: 2 trades, 0 won, average -19.46%, total $-89.93
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -5.86%, total $-13.02
- bought on a dip of 0.5+ ATR (any time): 3 trades, 0 won, average -9.58%, total $-70.23
- bought less than 0.25 ATR under the prior close: 1 trade, 0 won, average -10.75%, total $-26.27
- resting limit fills: 5 trades, 0 won, average -12.83%, total $-150.73
- support tested 3+ times: 4 trades, 0 won, average -9.87%, total $-96.50
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -24.65%, total $-54.23

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 2.02 | 2026-09-01 12:30 | 14.55 | stop | -14.28% | +0.13 / -1.50 |
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 2.21 | 2026-09-10 9:30 | 3.108 | stop | -8.60% | +1.62 / -1.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 2.2 | 2026-09-10 14:45 | 6.257 | stop | -10.75% | +0.77 / -1.52 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 3.79 | 2026-09-04 10:00 | 0.1735 | stop | -24.65% | +0.00 / -1.56 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 9.45 | 2026-10-01 10:05 | 8.341 | stop | -5.86% | +1.12 / -1.36 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-24 | 36.2 | 32.37 | 50.64 | 43.19 | +19.31% |
| RGTI | 2026-09-09 | 15.63 | 14.24 | 27.62 | 15.15 | -3.07% |
| GPUS | 2026-09-11 | 0.1818 | 0.1132 | 0.4407 | 0.16 | -11.99% |
| PATH | 2026-10-02 | 13.23 | 12.24 | 18.63 | 13.16 | -0.53% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $977.29 | LUNR, RXRX, SMCI |
| 2026-08-25 | $1023.32 | LUNR, RXRX, SMCI, SOUN |
| 2026-08-26 | $1002.17 | LUNR, RXRX, SMCI, SOUN |
| 2026-08-27 | $1014.23 | LUNR, RXRX, SMCI, SOUN |
| 2026-08-28 | $981.58 | LUNR, RXRX, SMCI, SOUN |
| 2026-08-31 | $988.97 | LUNR, RXRX, SMCI, SOUN |
| 2026-09-01 | $957.10 | RXRX, SMCI, SOUN |
| 2026-09-02 | $931.65 | GPUS, RXRX, SMCI, SOUN |
| 2026-09-03 | $931.11 | GPUS, RXRX, SMCI, SOUN |
| 2026-09-04 | $940.99 | RXRX, SMCI, SOUN |
| 2026-09-08 | $925.72 | RXRX, SMCI, SOUN |
| 2026-09-09 | $892.71 | RGTI, RXRX, SMCI, SOUN |
| 2026-09-10 | $865.46 | RGTI, SMCI |
| 2026-09-11 | $895.17 | GPUS, RGTI, SMCI |
| 2026-09-14 | $883.87 | GPUS, RGTI, SMCI |
| 2026-09-15 | $862.46 | GPUS, RGTI, SMCI |
| 2026-09-16 | $855.73 | GPUS, RGTI, SMCI |
| 2026-09-17 | $892.63 | GPUS, RGTI, SMCI |
| 2026-09-18 | $881.49 | GPUS, RGTI, SMCI |
| 2026-09-21 | $916.13 | GPUS, RGTI, SMCI |
| 2026-09-22 | $906.47 | GPUS, RGTI, SMCI |
| 2026-09-23 | $888.42 | GPUS, RGTI, SMCI |
| 2026-09-24 | $913.57 | GPUS, QUBT, RGTI, SMCI |
| 2026-09-25 | $910.44 | GPUS, QUBT, RGTI, SMCI |
| 2026-09-28 | $882.91 | GPUS, QUBT, RGTI, SMCI |
| 2026-09-29 | $860.78 | GPUS, QUBT, RGTI, SMCI |
| 2026-09-30 | $860.87 | GPUS, QUBT, RGTI, SMCI |
| 2026-10-01 | $862.73 | GPUS, RGTI, SMCI |
| 2026-10-02 | $881.13 | GPUS, PATH, RGTI, SMCI |
| 2026-10-05 | $865.37 | GPUS, PATH, RGTI, SMCI |

## Sell after 3 sessions if neither target nor stop: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $870.93 (-12.91%; realized $-129.06, open positions $-0.01); S&P 500 +1.19%, Nasdaq-100 +5.99%. 31 closed trades, 9 winners (29.0%), average trade -1.75%, average win 4.83%, average loss -4.44%, profit factor 0.43, worst drawdown -12.91%. Exits: stop 18, time 13. Resting orders filled: 30/77.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -5.58%, total $-92.17
- stopped on a later session: 11 trades, 0 won, average -4.38%, total $-110.60
- stopped at the open (gapped through the stop): 3 trades, 0 won, average -5.08%, total $-35.21
- never rose 0.5 ATR above the entry: 16 trades, 0 won, average -4.75%, total $-176.58
- crypto-linked: 5 trades, 1 won, average -3.26%, total $-37.67
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 1 won, average +1.55%, total $+6.78
- bought on a dip of 0.5+ ATR (any time): 9 trades, 2 won, average -1.74%, total $-38.72
- bought less than 0.25 ATR under the prior close: 12 trades, 5 won, average -0.01%, total $-1.04
- resting limit fills: 30 trades, 9 won, average -1.76%, total $-125.56
- run entries on a bounce (touched the zone, back above it): 1 trade, 0 won, average -1.60%, total $-3.50
- support tested 3+ times: 22 trades, 5 won, average -2.30%, total $-119.14
- support tested twice: 7 trades, 4 won, average +2.23%, total $+35.05
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-44.97

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-08-27 15:55 | 7.21 | time | +2.85% | +0.77 / -0.31 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-08-28 9:30 | LUNR | limit | 16 | -0.12 / -0.12 | 6.49 | 2026-08-28 14:20 | 15.18 | stop | -5.11% | +0.00 / -0.55 |
| 2026-08-31 9:30 | SMCI | limit | 36.53 | -0.21 / -0.21 | 8.81 | 2026-09-02 15:55 | 36.98 | time | +1.21% | +0.51 / -0.34 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.10% | +0.22 / -0.47 |
| 2026-09-01 10:05 | GPUS | limit | 0.26 | -0.05 / -0.54 | 8.13 | 2026-09-01 14:45 | 0.2366 | stop | -9.09% | +0.00 / -0.67 |
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-03 9:30 | SMCI | limit | 36.5 | -0.24 / -0.24 | 11.13 | 2026-09-08 15:55 | 40.23 | time | +10.22% | +2.37 / -0.35 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-09 15:55 | 8.119 | time | -4.16% | +0.71 / -0.59 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-09 10:15 | QBTS | limit | 17.06 | -0.16 / -0.57 | 7.24 | 2026-09-11 15:55 | 16.78 | time | -1.67% | +0.58 / -0.49 |
| 2026-09-11 9:30 | NOW | limit | 130.5 | -0.10 / -0.11 | 4.39 | 2026-09-15 15:55 | 141.8 | time | +8.67% | +2.62 / -0.01 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-16 15:55 | 63.66 | time | +5.09% | +1.79 / +0.00 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-16 15:55 | 36.83 | time | -1.60% | +0.30 / -0.93 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-09-22 15:55 | 16.49 | time | +6.50% | +1.33 / -0.47 |
| 2026-09-22 11:05 | PATH | limit | 13.27 | +0.36 / -0.32 | 8.83 | 2026-09-23 10:05 | 12.65 | stop | -4.69% | +0.24 / -0.62 |
| 2026-09-23 9:30 | CLSK (crypto) | limit | 15.01 | -0.14 / -0.14 | 6.87 | 2026-09-23 15:55 | 14.43 | stop | -3.90% | +0.19 / -0.62 |
| 2026-09-24 9:30 | QUBT | limit | 8.86 | -0.68 / -0.68 | 23.73 | 2026-09-28 10:40 | 8.685 | stop | -1.99% | +1.12 / -0.42 |
| 2026-09-24 9:30 | RGTI | limit | 15.64 | -0.36 / -0.39 | 21.47 | 2026-09-28 15:55 | 15.93 | time | +1.83% | +1.78 / -0.04 |
| 2026-09-24 9:30 | BTBT (crypto) | limit | 1.725 | -0.35 / -0.35 | 7.71 | 2026-09-28 15:55 | 1.672 | time | -3.11% | +0.74 / -0.35 |
| 2026-09-24 10:10 | STNE | limit | 9.43 | -0.03 / -0.15 | 4.4 | 2026-09-24 13:35 | 9.171 | stop | -2.76% | +0.00 / -0.64 |
| 2026-09-28 10:05 | SMCI | limit | 41.9 | -0.20 / -0.59 | 6.33 | 2026-09-30 11:55 | 40.49 | stop | -3.37% | +0.34 / -0.61 |
| 2026-09-29 9:40 | NOW | limit | 130.4 | -0.11 / -0.18 | 4.94 | 2026-10-01 15:55 | 137.7 | time | +5.56% | +1.87 / -0.42 |
| 2026-09-29 12:10 | BTBT (crypto) | limit | 1.67 | +0.25 / -0.08 | 10.33 | 2026-10-01 9:45 | 1.596 | stop | -4.47% | +0.51 / -0.59 |
| 2026-10-01 10:00 | WULF (crypto) | limit | 14.55 | +0.10 / -0.25 | 5.3 | 2026-10-05 15:55 | 14.78 | time | +1.57% | +1.68 / -0.19 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $975.44 | LUNR |
| 2026-08-25 | $975.95 | LUNR, SOUN |
| 2026-08-26 | $973.46 | BTBT, SOUN |
| 2026-08-27 | $985.23 | BTBT |
| 2026-08-28 | $944.81 | - |
| 2026-08-31 | $949.62 | SMCI |
| 2026-09-01 | $916.62 | AXTI, SMCI |
| 2026-09-02 | $898.35 | AXTI |
| 2026-09-03 | $896.86 | SMCI |
| 2026-09-04 | $904.79 | RCAT, SMCI |
| 2026-09-08 | $917.35 | RCAT |
| 2026-09-09 | $895.47 | QBTS, RGTI, SMR |
| 2026-09-10 | $875.77 | QBTS |
| 2026-09-11 | $880.77 | NOW |
| 2026-09-14 | $900.44 | NOW, RKLB, SMCI |
| 2026-09-15 | $892.98 | GRAB, RKLB, SMCI |
| 2026-09-16 | $897.38 | - |
| 2026-09-17 | $897.38 | - |
| 2026-09-18 | $901.43 | RGTI |
| 2026-09-21 | $912.59 | RGTI |
| 2026-09-22 | $911.62 | PATH |
| 2026-09-23 | $892.88 | - |
| 2026-09-24 | $914.97 | BTBT, QUBT, RGTI |
| 2026-09-25 | $908.33 | BTBT, QUBT, RGTI |
| 2026-09-28 | $878.81 | SMCI |
| 2026-09-29 | $871.39 | BTBT, NOW, SMCI |
| 2026-09-30 | $872.84 | BTBT, NOW |
| 2026-10-01 | $879.92 | WULF |
| 2026-10-02 | $886.79 | PATH, WULF |
| 2026-10-05 | $870.93 | - |

## Bitcoin gate off: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $940.20 (-5.98%; realized $-115.27, open positions $+55.47); S&P 500 +1.19%, Nasdaq-100 +5.99%. 14 closed trades, 1 winners (7.1%), average trade -3.35%, average win 21.6%, average loss -5.27%, profit factor 0.28, worst drawdown -13.08%. Exits: target 1, stop 13. Resting orders filled: 17/40.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -6.83%, total $-65.39
- stopped on a later session: 9 trades, 0 won, average -4.58%, total $-95.70
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -4.26%, total $-37.29
- never rose 0.5 ATR above the entry: 9 trades, 0 won, average -5.53%, total $-117.33
- crypto-linked: 2 trades, 0 won, average -5.46%, total $-26.34
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+45.82
- bought on a dip of 0.5+ ATR (any time): 5 trades, 1 won, average -0.08%, total $-7.09
- bought less than 0.25 ATR under the prior close: 3 trades, 0 won, average -4.69%, total $-32.84
- resting limit fills: 14 trades, 1 won, average -3.35%, total $-115.27
- support tested 3+ times: 10 trades, 0 won, average -4.62%, total $-109.02
- support tested twice: 2 trades, 1 won, average +9.30%, total $+39.14
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-45.39

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
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.36% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

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
| 2026-09-01 | $923.75 | SMCI, SOUN |
| 2026-09-02 | $899.63 | SMCI, SOUN |
| 2026-09-03 | $902.49 | SMCI |
| 2026-09-04 | $911.05 | RCAT, SMCI |
| 2026-09-08 | $924.08 | RCAT, SMCI |
| 2026-09-09 | $893.13 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $869.25 | SMCI |
| 2026-09-11 | $890.01 | NOW, SMCI |
| 2026-09-14 | $889.38 | NOW, RKLB, SMCI |
| 2026-09-15 | $881.29 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $883.74 | NOW, RKLB, SMCI |
| 2026-09-17 | $919.03 | NOW, RKLB, SMCI |
| 2026-09-18 | $898.95 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $945.31 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $953.72 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $945.56 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $960.24 | NOW, RGTI, SMCI |
| 2026-09-25 | $972.10 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $935.48 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $924.09 | NOW, RGTI, SMCI |
| 2026-09-30 | $930.37 | NOW, RGTI, SMCI |
| 2026-10-01 | $945.48 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $956.20 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $940.20 | NOW, SMCI, WULF |

## Rank run entries by R:R instead of dip: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $935.94 (-6.41%; realized $-120.40, open positions $+56.34); S&P 500 +1.19%, Nasdaq-100 +5.99%. 14 closed trades, 1 winners (7.1%), average trade -3.35%, average win 21.6%, average loss -5.27%, profit factor 0.25, worst drawdown -13.08%. Exits: target 1, stop 13. Resting orders filled: 17/40.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -6.83%, total $-65.39
- stopped on a later session: 9 trades, 0 won, average -4.58%, total $-95.06
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -4.26%, total $-37.30
- never rose 0.5 ATR above the entry: 9 trades, 0 won, average -5.53%, total $-116.68
- crypto-linked: 2 trades, 0 won, average -5.46%, total $-25.68
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+40.05
- bought on a dip of 0.5+ ATR (any time): 5 trades, 1 won, average -0.08%, total $-12.87
- bought less than 0.25 ATR under the prior close: 3 trades, 0 won, average -4.69%, total $-32.84
- resting limit fills: 14 trades, 1 won, average -3.35%, total $-120.40
- support tested 3+ times: 10 trades, 0 won, average -4.62%, total $-108.37
- support tested twice: 2 trades, 1 won, average +9.30%, total $+33.36
- radar keeps (GPUS, IREN, BTDR) without a tested support: 2 trades, 0 won, average -9.65%, total $-45.39

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
| 2026-09-02 10:50 | GPUS | limit | 0.23 | -0.42 / -0.27 | 9.47 | 2026-09-02 11:10 | 0.2067 | stop | -10.21% | +0.00 / -0.69 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.36% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

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
| 2026-09-01 | $923.75 | SMCI, SOUN |
| 2026-09-02 | $899.63 | SMCI, SOUN |
| 2026-09-03 | $902.49 | SMCI |
| 2026-09-04 | $911.05 | RCAT, SMCI |
| 2026-09-08 | $924.08 | RCAT, SMCI |
| 2026-09-09 | $893.13 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $869.25 | SMCI |
| 2026-09-11 | $890.43 | NOW, SMCI |
| 2026-09-14 | $890.93 | NOW, RKLB, SMCI |
| 2026-09-15 | $882.30 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $884.26 | NOW, RKLB, SMCI |
| 2026-09-17 | $917.46 | NOW, RKLB, SMCI |
| 2026-09-18 | $898.20 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $942.68 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $950.02 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $943.37 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $955.96 | NOW, RGTI, SMCI |
| 2026-09-25 | $967.30 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $930.49 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $918.88 | NOW, RGTI, SMCI |
| 2026-09-30 | $925.98 | NOW, RGTI, SMCI |
| 2026-10-01 | $941.42 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $950.76 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $935.94 | NOW, SMCI, WULF |

## Opening gap-down 0.5+ ATR, sell at the prior close or the close: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $864.45 (-13.55%; realized $-135.54, open positions $-0.01); S&P 500 +1.19%, Nasdaq-100 +5.99%. 45 closed trades, 18 winners (40.0%), average trade -1.25%, average win 2.01%, average loss -3.43%, profit factor 0.38, worst drawdown -15.29%. Exits: neutral 6, close 39.

### What the trades had in common

- never rose 0.5 ATR above the entry: 32 trades, 6 won, average -2.49%, total $-189.67
- crypto-linked: 20 trades, 7 won, average -1.15%, total $-53.32
- bought at the open after a gap down of 0.5+ ATR: 45 trades, 18 won, average -1.25%, total $-135.54
- bought on a dip of 0.5+ ATR (any time): 42 trades, 16 won, average -1.32%, total $-132.21

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | HIMS | gap | 32.46 | -0.69 / -0.68 | 0 | 2026-08-24 15:55 | 31.06 | close | -4.31% | +0.14 / -1.11 |
| 2026-08-24 9:30 | TEM | gap | 69.85 | -0.65 / -0.65 | 0 | 2026-08-24 15:55 | 66.14 | close | -5.33% | +0.49 / -0.90 |
| 2026-08-24 9:30 | QUBT | gap | 8.637 | -0.61 / -0.58 | 0 | 2026-08-24 15:55 | 8.233 | close | -4.68% | +0.17 / -0.94 |
| 2026-08-24 9:30 | IONQ | gap | 43.35 | -0.53 / -0.52 | 0 | 2026-08-24 15:55 | 41.04 | close | -5.34% | +0.07 / -0.83 |
| 2026-08-25 9:30 | MSTR (crypto) | gap | 119.1 | -0.57 / -0.56 | 0 | 2026-08-25 9:35 | 122.6 | neutral | +2.93% | +0.58 / -0.10 |
| 2026-08-25 9:30 | CRCL (crypto) | gap | 84.77 | -0.53 / -0.53 | 0 | 2026-08-25 9:35 | 89.24 | neutral | +5.26% | +0.96 / -0.09 |
| 2026-08-25 9:30 | SBET (crypto) | gap | 8.081 | -0.51 / -0.47 | 0 | 2026-08-25 9:35 | 8.254 | neutral | +2.12% | +0.70 / -0.18 |
| 2026-08-26 9:30 | GLXY (crypto) | gap | 23.87 | -0.57 / -0.56 | 0 | 2026-08-26 15:35 | 24.78 | neutral | +3.79% | +0.57 / -0.10 |
| 2026-08-26 9:30 | NOW | gap | 122.4 | -0.82 / -0.81 | 0 | 2026-08-26 15:55 | 125.8 | close | +2.74% | +0.73 / -0.09 |
| 2026-08-26 9:30 | COIN (crypto) | gap | 181.7 | -0.57 / -0.56 | 0 | 2026-08-26 15:55 | 181.6 | close | -0.06% | +0.38 / -0.24 |
| 2026-08-26 9:30 | MSTR (crypto) | gap | 123.3 | -0.53 / -0.52 | 0 | 2026-08-26 15:55 | 123.1 | close | -0.14% | +0.33 / -0.35 |
| 2026-08-28 9:30 | IREN (crypto) | gap | 37.61 | -0.90 / -0.90 | 0 | 2026-08-28 15:55 | 35.41 | close | -5.86% | +0.13 / -0.86 |
| 2026-08-28 9:30 | SBET (crypto) | gap | 8.659 | -0.52 / -0.48 | 0 | 2026-08-28 15:55 | 8.194 | close | -5.39% | +0.21 / -1.18 |
| 2026-08-31 9:30 | AFRM | gap | 75.68 | -0.53 / -0.52 | 0 | 2026-08-31 15:55 | 74.37 | close | -1.73% | +0.32 / -1.11 |
| 2026-09-01 9:30 | SBET (crypto) | gap | 8.307 | -0.67 / -0.64 | 0 | 2026-09-01 15:55 | 8.139 | close | -2.03% | +0.30 / -0.46 |
| 2026-09-01 9:30 | HIMX | gap | 13.35 | -0.63 / -0.59 | 0 | 2026-09-01 15:55 | 13.39 | close | +0.34% | +0.24 / -0.20 |
| 2026-09-01 9:30 | BMNR (crypto) | gap | 24.4 | -0.62 / -0.61 | 0 | 2026-09-01 15:55 | 23.38 | close | -4.18% | +0.12 / -0.90 |
| 2026-09-01 9:30 | NNE | gap | 17.54 | -0.62 / -0.59 | 0 | 2026-09-01 15:55 | 17.43 | close | -0.64% | +0.21 / -0.40 |
| 2026-09-04 9:30 | PATH | gap | 16.27 | -2.61 / -2.57 | 0 | 2026-09-04 15:55 | 15.17 | close | -6.76% | +0.58 / -1.98 |
| 2026-09-04 9:30 | MSTR (crypto) | gap | 137.3 | -0.77 / -0.76 | 0 | 2026-09-04 15:55 | 142.6 | close | +3.87% | +0.72 / -0.02 |
| 2026-09-04 9:30 | SBET (crypto) | gap | 8.637 | -0.62 / -0.59 | 0 | 2026-09-04 15:55 | 8.663 | close | +0.29% | +0.11 / -0.50 |
| 2026-09-04 9:30 | BMNR (crypto) | gap | 25.35 | -0.62 / -0.61 | 0 | 2026-09-04 15:55 | 24.97 | close | -1.49% | +0.08 / -0.46 |
| 2026-09-08 9:30 | NOW | gap | 136.8 | -0.68 / -0.67 | 0 | 2026-09-08 15:55 | 134.2 | close | -1.94% | +0.03 / -0.64 |
| 2026-09-08 9:30 | MSTR (crypto) | gap | 137.7 | -0.51 / -0.51 | 0 | 2026-09-08 15:55 | 136.4 | close | -0.91% | +0.16 / -0.23 |
| 2026-09-10 9:30 | CRWV | gap | 89.94 | -0.96 / -0.95 | 0 | 2026-09-10 15:55 | 89.12 | close | -0.93% | +0.43 / -0.23 |
| 2026-09-10 9:30 | POET | gap | 7.747 | -0.62 / -0.59 | 0 | 2026-09-10 15:55 | 7.585 | close | -2.11% | +0.45 / -0.41 |
| 2026-09-10 9:30 | NBIS | gap | 232.1 | -0.61 / -0.61 | 0 | 2026-09-10 15:55 | 227.8 | close | -1.87% | +0.46 / -0.45 |
| 2026-09-10 9:30 | CIFR (crypto) | gap | 16.08 | -0.59 / -0.57 | 0 | 2026-09-10 15:55 | 15.9 | close | -1.15% | +0.26 / -0.56 |
| 2026-09-11 9:30 | SMR | gap | 9.679 | -0.80 / -0.77 | 0 | 2026-09-11 15:55 | 8.593 | close | -11.23% | +0.13 / -1.61 |
| 2026-09-14 9:30 | NBIS | gap | 205.1 | -1.43 / -1.43 | 0 | 2026-09-14 15:55 | 212.2 | close | +3.48% | +1.04 / -0.09 |
| 2026-09-14 9:30 | APLD | gap | 24.45 | -1.26 / -1.25 | 0 | 2026-09-14 15:55 | 24.56 | close | +0.44% | +0.66 / -0.04 |
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

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $950.84 | - |
| 2026-08-25 | $975.34 | - |
| 2026-08-26 | $990.77 | - |
| 2026-08-27 | $990.77 | - |
| 2026-08-28 | $962.91 | - |
| 2026-08-31 | $958.73 | - |
| 2026-09-01 | $943.13 | - |
| 2026-09-02 | $943.13 | - |
| 2026-09-03 | $943.13 | - |
| 2026-09-04 | $933.49 | - |
| 2026-09-08 | $926.85 | - |
| 2026-09-09 | $926.85 | - |
| 2026-09-10 | $912.82 | - |
| 2026-09-11 | $887.19 | - |
| 2026-09-14 | $897.41 | - |
| 2026-09-15 | $847.14 | - |
| 2026-09-16 | $847.14 | - |
| 2026-09-17 | $847.14 | - |
| 2026-09-18 | $847.14 | - |
| 2026-09-21 | $847.14 | - |
| 2026-09-22 | $850.12 | - |
| 2026-09-23 | $850.12 | - |
| 2026-09-24 | $863.60 | - |
| 2026-09-25 | $863.60 | - |
| 2026-09-28 | $864.45 | - |
| 2026-09-29 | $864.45 | - |
| 2026-09-30 | $864.45 | - |
| 2026-10-01 | $864.45 | - |
| 2026-10-02 | $864.45 | - |
| 2026-10-05 | $864.45 | - |

## Limits cancelled at 10:00 (the first 30 minutes), runs after: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $957.28 (-4.27%; realized $-123.08, open positions $+80.36); S&P 500 +1.19%, Nasdaq-100 +5.99%. 22 closed trades, 4 winners (18.2%), average trade -2.03%, average win 14.86%, average loss -5.78%, profit factor 0.47, worst drawdown -14.28%. Exits: target 4, stop 18. Resting orders filled: 9/21.

### What the trades had in common

- stopped the session it was bought: 3 trades, 0 won, average -6.62%, total $-45.34
- stopped on a later session: 15 trades, 0 won, average -5.61%, total $-185.42
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -6.83%, total $-110.43
- never rose 0.5 ATR above the entry: 13 trades, 0 won, average -6.37%, total $-181.21
- crypto-linked: 3 trades, 0 won, average -4.71%, total $-23.85
- bought on a dip of 0.5+ ATR (any time): 11 trades, 3 won, average -1.52%, total $-62.01
- bought less than 0.25 ATR under the prior close: 8 trades, 1 won, average -1.88%, total $-30.39
- resting limit fills: 7 trades, 0 won, average -4.56%, total $-77.11
- run entries inside the buy zone: 10 trades, 4 won, average +1.97%, total $+29.45
- run entries on a bounce (touched the zone, back above it): 5 trades, 0 won, average -6.48%, total $-75.42
- support tested 3+ times: 17 trades, 4 won, average -0.44%, total $-38.46
- support tested twice: 4 trades, 0 won, average -6.33%, total $-59.28
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -11.85%, total $-25.34

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-24 10:05 | CRSP | bounce | 57.23 | -0.34 / -0.87 | 2.0 | 2026-09-08 9:30 | 54.3 | stop | -5.12% | +1.65 / -1.69 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-25 10:05 | UPST | buy zone | 29.94 | +0.09 / +0.03 | 2.72 | 2026-08-31 9:30 | 28.55 | stop | -4.67% | +1.00 / -0.93 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.14% | +0.45 / -1.38 |
| 2026-09-02 10:05 | GPUS | buy zone | 0.2343 | -0.42 / -0.15 | 8.19 | 2026-09-02 11:10 | 0.2067 | stop | -11.85% | +0.11 / -0.80 |
| 2026-09-03 10:05 | SMTC | buy zone | 127.1 | -0.07 / -0.60 | 1.74 | 2026-09-04 10:50 | 144.2 | target | +13.38% | +1.55 / -0.02 |
| 2026-09-04 10:05 | BULL | buy zone | 9.684 | -0.40 / -0.50 | 6.85 | 2026-09-08 15:35 | 9.44 | stop | -2.53% | +0.52 / -0.36 |
| 2026-09-08 10:05 | DUOL | bounce | 148.2 | -0.26 / -0.84 | 2.35 | 2026-09-09 10:15 | 140.8 | stop | -4.98% | +0.00 / -1.13 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-10 10:05 | NBIS | buy zone | 230.4 | -0.61 / -0.73 | 5.2 | 2026-09-14 9:30 | 204.9 | stop | -11.07% | +0.33 / -1.95 |
| 2026-09-11 10:05 | GRAL | buy zone | 77.28 | +0.01 / -0.06 | 1.81 | 2026-09-21 9:50 | 98.6 | target | +27.58% | +5.45 / -0.86 |
| 2026-09-15 10:05 | RXRX | buy zone | 3.256 | -0.27 / -0.82 | 3.35 | 2026-09-18 10:50 | 3.592 | target | +10.30% | +1.90 / -0.51 |
| 2026-09-21 10:05 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-24 13:40 | 9.158 | stop | -4.46% | +1.01 / -0.98 |
| 2026-09-22 10:05 | AXTI | bounce | 76.71 | -0.55 / -0.54 | 2.34 | 2026-09-24 9:30 | 70.06 | stop | -8.68% | +0.34 / -1.19 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.16% | +1.68 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.98% | +0.40 / -0.50 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-09-01 | 36.39 | 35.01 | 50.6 | 43.19 | +18.69% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 136.1 | +4.30% |
| AXTI | 2026-09-30 | 75.92 | 70.99 | 89.31 | 86.66 | +14.14% |
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 19.32 | -1.78% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $974.77 | CRSP, LUNR |
| 2026-08-25 | $997.00 | CRSP, LUNR, SOUN, UPST |
| 2026-08-26 | $978.33 | CRSP, SOUN, UPST |
| 2026-08-27 | $990.73 | CRSP, IONQ, SOUN, UPST |
| 2026-08-28 | $950.38 | CRSP, IONQ, SOUN, UPST |
| 2026-08-31 | $945.29 | CRSP, IONQ, SOUN |
| 2026-09-01 | $927.50 | CRSP, SMCI, SOUN |
| 2026-09-02 | $901.96 | CRSP, SMCI, SOUN |
| 2026-09-03 | $914.93 | CRSP, SMCI, SMTC |
| 2026-09-04 | $936.80 | BULL, CRSP, SMCI |
| 2026-09-08 | $924.66 | DUOL, SMCI |
| 2026-09-09 | $900.80 | RGTI, SMCI, SMR |
| 2026-09-10 | $875.60 | NBIS, SMCI |
| 2026-09-11 | $889.73 | GRAL, NBIS, NOW, SMCI |
| 2026-09-14 | $865.72 | GRAL, NOW, SMCI |
| 2026-09-15 | $858.25 | GRAL, NOW, RXRX, SMCI |
| 2026-09-16 | $857.19 | GRAL, NOW, RXRX, SMCI |
| 2026-09-17 | $910.24 | GRAL, NOW, RXRX, SMCI |
| 2026-09-18 | $902.67 | GRAL, NOW, SMCI |
| 2026-09-21 | $972.61 | NOW, SMCI, STNE |
| 2026-09-22 | $980.21 | AXTI, NOW, SMCI, STNE |
| 2026-09-23 | $962.79 | AXTI, NOW, SMCI, STNE |
| 2026-09-24 | $944.27 | HIMS, NOW, SMCI |
| 2026-09-25 | $953.87 | BTBT, CRCL, NOW, SMCI |
| 2026-09-28 | $920.38 | BTBT, CRCL, NOW, SMCI |
| 2026-09-29 | $907.58 | CRCL, IREN, NOW, SMCI |
| 2026-09-30 | $916.93 | AXTI, IREN, NOW, SMCI |
| 2026-10-01 | $940.34 | AXTI, NOW, RIOT, SMCI |
| 2026-10-02 | $958.71 | AXTI, NOW, RIOT, SMCI |
| 2026-10-05 | $957.28 | AXTI, NOW, RIOT, SMCI |

## GPUS, IREN, BTDR only with a tested support: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $968.60 (-3.14%; realized $-88.34, open positions $+56.94); S&P 500 +1.19%, Nasdaq-100 +5.99%. 13 closed trades, 1 winners (7.7%), average trade -2.59%, average win 21.6%, average loss -4.61%, profit factor 0.33, worst drawdown -10.07%. Exits: target 1, stop 12. Resting orders filled: 16/38.

### What the trades had in common

- stopped the session it was bought: 2 trades, 0 won, average -4.00%, total $-20.00
- stopped on a later session: 10 trades, 0 won, average -4.73%, total $-111.64
- stopped at the open (gapped through the stop): 5 trades, 0 won, average -4.63%, total $-52.82
- never rose 0.5 ATR above the entry: 8 trades, 0 won, average -4.58%, total $-87.28
- crypto-linked: 2 trades, 0 won, average -5.46%, total $-26.51
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 1 won, average +21.60%, total $+43.30
- bought on a dip of 0.5+ ATR (any time): 4 trades, 1 won, average +2.18%, total $+11.96
- bought less than 0.25 ATR under the prior close: 3 trades, 0 won, average -4.69%, total $-33.59
- resting limit fills: 13 trades, 1 won, average -2.59%, total $-88.34
- support tested 3+ times: 11 trades, 0 won, average -4.76%, total $-124.72
- support tested twice: 2 trades, 1 won, average +9.30%, total $+36.38

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-26 9:30 | BTBT (crypto) | limit | 1.51 | -0.35 / -0.49 | 7.09 | 2026-08-28 14:35 | 1.414 | stop | -6.38% | +1.09 / -0.63 |
| 2026-09-01 9:30 | AXTI | limit | 58.03 | -0.30 / -0.30 | 5.65 | 2026-09-03 9:30 | 54.49 | stop | -6.10% | +0.22 / -0.47 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-14 9:30 | RKLB | limit | 60.57 | -0.83 / -0.83 | 6.61 | 2026-09-24 12:20 | 73.66 | target | +21.60% | +4.59 / +0.00 |
| 2026-09-15 12:00 | GRAB | limit | 2.96 | +0.44 / -0.49 | 4.64 | 2026-09-16 15:20 | 2.871 | stop | -3.01% | +0.24 / -0.65 |
| 2026-09-18 9:55 | RGTI | limit | 15.48 | +0.32 / -0.62 | 24.99 | 2026-10-05 9:30 | 14.96 | stop | -3.36% | +2.65 / -0.75 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.54% | +0.38 / -0.68 |

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
| 2026-09-01 | $938.03 | AXTI, SMCI, SOUN |
| 2026-09-02 | $940.78 | AXTI, SMCI, SOUN |
| 2026-09-03 | $933.98 | SMCI |
| 2026-09-04 | $942.45 | RCAT, SMCI |
| 2026-09-08 | $955.78 | RCAT, SMCI |
| 2026-09-09 | $923.99 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $899.35 | SMCI |
| 2026-09-11 | $920.65 | NOW, SMCI |
| 2026-09-14 | $922.20 | NOW, RKLB, SMCI |
| 2026-09-15 | $913.67 | GRAB, NOW, RKLB, SMCI |
| 2026-09-16 | $915.45 | NOW, RKLB, SMCI |
| 2026-09-17 | $949.59 | NOW, RKLB, SMCI |
| 2026-09-18 | $929.48 | NOW, RGTI, RKLB, SMCI |
| 2026-09-21 | $975.77 | NOW, RGTI, RKLB, SMCI |
| 2026-09-22 | $983.59 | NOW, RGTI, RKLB, SMCI |
| 2026-09-23 | $976.50 | NOW, RGTI, RKLB, SMCI |
| 2026-09-24 | $989.98 | NOW, RGTI, SMCI |
| 2026-09-25 | $1001.38 | BTBT, NOW, RGTI, SMCI |
| 2026-09-28 | $963.16 | BTBT, NOW, RGTI, SMCI |
| 2026-09-29 | $951.26 | NOW, RGTI, SMCI |
| 2026-09-30 | $958.60 | NOW, RGTI, SMCI |
| 2026-10-01 | $974.63 | NOW, RGTI, SMCI, WULF |
| 2026-10-02 | $984.30 | NOW, RGTI, SMCI, WULF |
| 2026-10-05 | $968.60 | NOW, SMCI, WULF |

## Both of the above: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1016.74 (+1.67%; realized $-40.93, open positions $+57.67); S&P 500 +1.19%, Nasdaq-100 +5.99%. 18 closed trades, 4 winners (22.2%), average trade -0.28%, average win 17.25%, average loss -5.29%, profit factor 0.77, worst drawdown -8.47%. Exits: target 4, stop 14. Resting orders filled: 9/17.

### What the trades had in common

- stopped the session it was bought: 2 trades, 0 won, average -4.00%, total $-20.00
- stopped on a later session: 12 trades, 0 won, average -5.51%, total $-159.06
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -5.90%, total $-100.47
- never rose 0.5 ATR above the entry: 10 trades, 0 won, average -5.53%, total $-133.83
- crypto-linked: 2 trades, 1 won, average +5.21%, total $+20.93
- bought on a dip of 0.5+ ATR (any time): 7 trades, 2 won, average -0.79%, total $-36.03
- bought less than 0.25 ATR under the prior close: 9 trades, 2 won, average +0.98%, total $+15.65
- resting limit fills: 7 trades, 0 won, average -4.56%, total $-78.21
- run entries inside the buy zone: 7 trades, 4 won, average +7.77%, total $+104.29
- run entries on a bounce (touched the zone, back above it): 4 trades, 0 won, average -6.88%, total $-67.01
- support tested 3+ times: 15 trades, 4 won, average +1.07%, total $+10.20
- support tested twice: 3 trades, 0 won, average -7.06%, total $-51.13

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.29% | +0.00 / -0.62 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 5.07 | 2026-08-26 11:15 | 15.98 | stop | -5.83% | +0.13 / -0.62 |
| 2026-08-24 10:05 | CRSP | bounce | 57.23 | -0.34 / -0.87 | 2.0 | 2026-09-08 9:30 | 54.3 | stop | -5.12% | +1.65 / -1.69 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.44% | +0.77 / -0.63 |
| 2026-08-25 10:05 | UPST | buy zone | 29.94 | +0.09 / +0.03 | 2.72 | 2026-08-31 9:30 | 28.55 | stop | -4.67% | +1.00 / -0.93 |
| 2026-08-27 10:05 | IONQ | bounce | 41.65 | +0.35 / +0.56 | 1.83 | 2026-09-01 9:30 | 37.85 | stop | -9.14% | +0.45 / -1.38 |
| 2026-09-02 10:05 | WULF (crypto) | buy zone | 14.51 | -0.17 / -0.12 | 3.7 | 2026-09-08 9:50 | 16.98 | target | +17.02% | +2.22 / -0.11 |
| 2026-09-04 9:35 | RCAT | limit | 8.47 | -0.07 / -0.11 | 5.58 | 2026-09-10 9:30 | 8.086 | stop | -4.54% | +0.71 / -0.63 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-09 9:40 | SMR | limit | 10.89 | -0.24 / -0.41 | 7.55 | 2026-09-10 9:30 | 10.45 | stop | -4.04% | +0.20 / -0.87 |
| 2026-09-11 10:05 | SOFI | bounce | 17.45 | +0.14 / +0.30 | 1.98 | 2026-09-16 14:55 | 16.65 | stop | -4.57% | +0.37 / -1.06 |
| 2026-09-11 10:05 | GRAL | buy zone | 77.28 | +0.01 / -0.06 | 1.81 | 2026-09-21 9:50 | 98.6 | target | +27.58% | +5.45 / -0.86 |
| 2026-09-17 10:05 | CRWV | buy zone | 78.93 | -0.35 / -0.81 | 18.33 | 2026-10-02 10:05 | 91.76 | target | +16.25% | +2.54 / -0.08 |
| 2026-09-22 10:05 | AXTI | bounce | 76.71 | -0.55 / -0.54 | 2.34 | 2026-09-24 9:30 | 70.06 | stop | -8.68% | +0.34 / -1.19 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.16% | +1.68 / -0.01 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.60% | +0.07 / -0.90 |
| 2026-10-02 10:05 | PATH | buy zone | 13.25 | +0.14 / -0.10 | 13.84 | 2026-10-05 11:00 | 12.81 | stop | -3.35% | +0.00 / -0.66 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-09-01 | 36.39 | 35.01 | 50.6 | 43.19 | +18.69% |
| NOW | 2026-09-11 | 130.5 | 126.6 | 147.6 | 136.1 | +4.30% |
| AXTI | 2026-09-30 | 75.92 | 70.99 | 89.31 | 86.66 | +14.14% |
| WULF | 2026-10-05 | 14.78 | 13.93 | 17.77 | 14.79 | +0.04% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $974.77 | CRSP, LUNR |
| 2026-08-25 | $997.00 | CRSP, LUNR, SOUN, UPST |
| 2026-08-26 | $978.33 | CRSP, SOUN, UPST |
| 2026-08-27 | $990.73 | CRSP, IONQ, SOUN, UPST |
| 2026-08-28 | $950.38 | CRSP, IONQ, SOUN, UPST |
| 2026-08-31 | $945.29 | CRSP, IONQ, SOUN |
| 2026-09-01 | $927.50 | CRSP, SMCI, SOUN |
| 2026-09-02 | $931.81 | CRSP, SMCI, SOUN, WULF |
| 2026-09-03 | $953.29 | CRSP, SMCI, WULF |
| 2026-09-04 | $962.25 | CRSP, RCAT, SMCI, WULF |
| 2026-09-08 | $975.81 | RCAT, SMCI |
| 2026-09-09 | $944.16 | RCAT, RGTI, SMCI, SMR |
| 2026-09-10 | $918.96 | SMCI |
| 2026-09-11 | $934.63 | GRAL, NOW, SMCI, SOFI |
| 2026-09-14 | $933.35 | GRAL, NOW, SMCI, SOFI |
| 2026-09-15 | $919.24 | GRAL, NOW, SMCI, SOFI |
| 2026-09-16 | $915.28 | GRAL, NOW, SMCI |
| 2026-09-17 | $951.58 | CRWV, GRAL, NOW, SMCI |
| 2026-09-18 | $945.02 | CRWV, GRAL, NOW, SMCI |
| 2026-09-21 | $1026.18 | CRWV, NOW, SMCI |
| 2026-09-22 | $1034.38 | AXTI, CRWV, NOW, SMCI |
| 2026-09-23 | $1024.71 | AXTI, CRWV, NOW, SMCI |
| 2026-09-24 | $1021.48 | CRWV, HIMS, NOW, SMCI |
| 2026-09-25 | $1022.73 | CRCL, CRWV, NOW, SMCI |
| 2026-09-28 | $990.83 | CRCL, CRWV, NOW, SMCI |
| 2026-09-29 | $980.29 | CRCL, CRWV, NOW, SMCI |
| 2026-09-30 | $989.60 | AXTI, CRWV, NOW, SMCI |
| 2026-10-01 | $1007.75 | AXTI, CRWV, NOW, SMCI |
| 2026-10-02 | $1021.49 | AXTI, NOW, PATH, SMCI |
| 2026-10-05 | $1016.74 | AXTI, NOW, SMCI, WULF |

## Both, stop 1.0 ATR under support: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1099.52 (+9.95%; realized $-82.62, open positions $+182.14); S&P 500 +1.19%, Nasdaq-100 +5.99%. 7 closed trades, 1 winners (14.3%), average trade -4.56%, average win 17.08%, average loss -8.16%, profit factor 0.3, worst drawdown -11.4%. Exits: target 1, stop 6. Resting orders filled: 6/12.

### What the trades had in common

- stopped the session it was bought: 1 trade, 0 won, average -5.89%, total $-14.71
- stopped on a later session: 5 trades, 0 won, average -8.62%, total $-102.49
- stopped at the open (gapped through the stop): 1 trade, 0 won, average -7.22%, total $-15.76
- never rose 0.5 ATR above the entry: 4 trades, 0 won, average -9.35%, total $-89.32
- bought on a dip of 0.5+ ATR (any time): 3 trades, 0 won, average -6.60%, total $-49.51
- bought less than 0.25 ATR under the prior close: 3 trades, 1 won, average +0.87%, total $+1.78
- resting limit fills: 4 trades, 0 won, average -7.48%, total $-71.47
- run entries inside the buy zone: 3 trades, 1 won, average -0.66%, total $-11.15
- support tested 3+ times: 6 trades, 0 won, average -8.16%, total $-117.20
- support tested twice: 1 trade, 1 won, average +17.08%, total $+34.58

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 3.33 | 2026-08-24 9:50 | 3.2 | stop | -5.89% | +0.00 / -1.00 |
| 2026-08-24 9:30 | LUNR | limit | 16.97 | -0.45 / -0.85 | 3.04 | 2026-08-28 12:00 | 15.35 | stop | -9.58% | +0.13 / -1.01 |
| 2026-08-24 10:05 | POET | buy zone | 7.755 | -0.39 / -0.71 | 6.87 | 2026-08-31 10:35 | 7.42 | stop | -4.34% | +0.95 / -0.46 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 3.29 | 2026-09-08 10:35 | 6.503 | stop | -7.24% | +0.77 / -1.01 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 11.63 | 2026-09-14 9:30 | 14.5 | stop | -7.22% | +0.30 / -1.09 |
| 2026-09-15 10:05 | APLD | buy zone | 24.2 | -0.18 / -0.23 | 2.16 | 2026-09-21 11:20 | 28.34 | target | +17.08% | +2.72 / -0.50 |
| 2026-09-22 10:05 | GPUS | buy zone | 0.1815 | -0.01 / -0.37 | 10.65 | 2026-09-29 15:55 | 0.1549 | stop | -14.72% | +0.13 / -1.13 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| SMCI | 2026-08-24 | 36.2 | 33.65 | 50.64 | 43.19 | +19.31% |
| AXTI | 2026-09-01 | 58.03 | 51.1 | 88.66 | 86.66 | +49.34% |
| HIMX | 2026-09-01 | 13.31 | 12.39 | 15.88 | 14.71 | +10.51% |
| WULF | 2026-09-30 | 14.95 | 13.53 | 17.76 | 14.79 | -1.07% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $973.43 | LUNR, POET, SMCI |
| 2026-08-25 | $1007.25 | LUNR, POET, SMCI, SOUN |
| 2026-08-26 | $991.30 | LUNR, POET, SMCI, SOUN |
| 2026-08-27 | $1010.31 | LUNR, POET, SMCI, SOUN |
| 2026-08-28 | $962.53 | POET, SMCI, SOUN |
| 2026-08-31 | $962.98 | SMCI, SOUN |
| 2026-09-01 | $943.00 | AXTI, HIMX, SMCI, SOUN |
| 2026-09-02 | $947.53 | AXTI, HIMX, SMCI, SOUN |
| 2026-09-03 | $950.38 | AXTI, HIMX, SMCI, SOUN |
| 2026-09-04 | $985.47 | AXTI, HIMX, SMCI, SOUN |
| 2026-09-08 | $1020.71 | AXTI, HIMX, SMCI |
| 2026-09-09 | $1000.49 | AXTI, HIMX, RGTI, SMCI |
| 2026-09-10 | $969.31 | AXTI, HIMX, RGTI, SMCI |
| 2026-09-11 | $1007.09 | AXTI, HIMX, RGTI, SMCI |
| 2026-09-14 | $922.89 | AXTI, HIMX, SMCI |
| 2026-09-15 | $904.35 | APLD, AXTI, HIMX, SMCI |
| 2026-09-16 | $943.28 | APLD, AXTI, HIMX, SMCI |
| 2026-09-17 | $1008.66 | APLD, AXTI, HIMX, SMCI |
| 2026-09-18 | $1029.66 | APLD, AXTI, HIMX, SMCI |
| 2026-09-21 | $1094.99 | AXTI, HIMX, SMCI |
| 2026-09-22 | $1088.98 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-23 | $1048.84 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-24 | $1070.79 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-25 | $1087.35 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-28 | $1048.07 | AXTI, GPUS, HIMX, SMCI |
| 2026-09-29 | $1042.87 | AXTI, HIMX, SMCI |
| 2026-09-30 | $1037.66 | AXTI, HIMX, SMCI, WULF |
| 2026-10-01 | $1068.91 | AXTI, HIMX, SMCI, WULF |
| 2026-10-02 | $1118.97 | AXTI, HIMX, SMCI, WULF |
| 2026-10-05 | $1099.52 | AXTI, HIMX, SMCI, WULF |

## Run entries only, GPUS/IREN/BTDR only with a tested support: 2026-08-24 to 2026-10-05 (30 sessions)

$1000 -> $1106.26 (+10.63%; realized $+52.25, open positions $+54.01); S&P 500 +1.19%, Nasdaq-100 +5.99%. 30 closed trades, 8 winners (26.7%), average trade 1.22%, average win 17.44%, average loss -4.68%, profit factor 1.2, worst drawdown -8.64%. Exits: target 8, stop 22.

### What the trades had in common

- stopped the session it was bought: 7 trades, 0 won, average -2.10%, total $-37.43
- stopped on a later session: 15 trades, 0 won, average -5.89%, total $-222.49
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -8.15%, total $-151.13
- never rose 0.5 ATR above the entry: 17 trades, 0 won, average -4.70%, total $-202.03
- crypto-linked: 5 trades, 2 won, average +5.13%, total $+61.58
- bought on a dip of 0.5+ ATR (any time): 15 trades, 3 won, average -0.63%, total $-36.88
- bought less than 0.25 ATR under the prior close: 7 trades, 3 won, average +5.76%, total $+97.29
- run entries inside the buy zone: 25 trades, 8 won, average +3.00%, total $+151.21
- run entries on a bounce (touched the zone, back above it): 5 trades, 0 won, average -7.68%, total $-98.96
- support tested 3+ times: 24 trades, 7 won, average +2.01%, total $+81.66
- support tested twice: 6 trades, 1 won, average -1.98%, total $-29.41

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-08-24 9:50 | POET | buy zone | 7.786 | -0.39 / -0.66 | 37.41 | 2026-08-24 10:00 | 7.699 | stop | -1.12% | +0.08 / -0.15 |
| 2026-08-24 9:50 | UMAC | buy zone | 24.92 | -0.25 / -0.76 | 14.36 | 2026-08-25 15:55 | 24.28 | stop | -2.56% | +0.13 / -0.23 |
| 2026-08-24 9:50 | LUNR | buy zone | 16.87 | -0.45 / -0.91 | 6.02 | 2026-08-26 11:15 | 15.98 | stop | -5.29% | +0.19 / -0.56 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:50 | CRCL (crypto) | buy zone | 86.33 | -0.53 / -0.25 | 3.65 | 2026-09-03 10:05 | 98.9 | target | +14.55% | +2.27 / -0.08 |
| 2026-08-26 9:50 | IONQ | bounce | 41.39 | -0.34 / -0.23 | 2.07 | 2026-09-01 9:30 | 37.85 | stop | -8.56% | +0.54 / -1.28 |
| 2026-08-27 11:20 | DELL | bounce | 465 | +0.11 / +0.04 | 1.52 | 2026-09-01 10:10 | 437.5 | stop | -5.93% | +0.36 / -1.05 |
| 2026-09-02 9:50 | WULF (crypto) | buy zone | 14.38 | -0.17 / -0.23 | 5.04 | 2026-09-08 9:50 | 16.98 | target | +18.08% | +2.33 / -0.07 |
| 2026-09-03 9:50 | AEHR | buy zone | 77.32 | -0.11 / -0.27 | 4.1 | 2026-09-09 10:05 | 101.3 | target | +30.95% | +2.20 / -0.25 |
| 2026-09-04 9:50 | BULL | buy zone | 9.669 | -0.40 / -0.52 | 7.47 | 2026-09-08 15:35 | 9.44 | stop | -2.38% | +0.54 / -0.34 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.38% | +0.37 / -0.79 |
| 2026-09-09 9:50 | NNE | buy zone | 18.92 | -0.09 / -0.37 | 5.78 | 2026-09-09 11:00 | 18.39 | stop | -2.85% | +0.01 / -0.48 |
| 2026-09-09 9:50 | SMR | buy zone | 10.89 | -0.24 / -0.42 | 8.09 | 2026-09-10 9:30 | 10.45 | stop | -4.01% | +0.20 / -0.87 |
| 2026-09-09 10:05 | GLXY (crypto) | buy zone | 26.05 | +0.02 / -0.56 | 6.31 | 2026-09-09 14:05 | 25.33 | stop | -2.80% | +0.11 / -0.42 |
| 2026-09-10 9:50 | ORCL | buy zone | 156 | -0.50 / -0.87 | 9.02 | 2026-09-10 15:55 | 153.4 | stop | -1.67% | +0.48 / -0.54 |
| 2026-09-10 9:50 | NBIS | buy zone | 230.1 | -0.61 / -0.75 | 5.38 | 2026-09-14 9:30 | 204.9 | stop | -10.98% | +0.34 / -1.93 |
| 2026-09-10 9:50 | AXTI | bounce | 66.01 | -0.48 / -0.47 | 3.72 | 2026-09-14 9:30 | 59.65 | stop | -9.65% | +0.46 / -1.26 |
| 2026-09-11 9:50 | SOFI | buy zone | 17.24 | +0.14 / +0.03 | 3.2 | 2026-09-16 14:55 | 16.65 | stop | -3.39% | +0.64 / -0.80 |
| 2026-09-11 9:50 | GRAL | buy zone | 77.1 | +0.01 / -0.10 | 1.95 | 2026-09-21 9:50 | 98.6 | target | +27.88% | +5.49 / -0.82 |
| 2026-09-15 9:50 | RXRX | buy zone | 3.306 | -0.27 / -0.55 | 1.95 | 2026-09-18 10:50 | 3.592 | target | +8.62% | +1.64 / -0.78 |
| 2026-09-15 9:50 | APLD | buy zone | 24.36 | -0.18 / -0.14 | 2.81 | 2026-09-21 11:20 | 28.34 | target | +16.33% | +2.62 / -0.60 |
| 2026-09-17 9:50 | CRWV | buy zone | 79.83 | -0.35 / -0.64 | 7.43 | 2026-10-02 10:05 | 91.76 | target | +14.93% | +2.37 / -0.29 |
| 2026-09-21 9:50 | STNE | buy zone | 9.549 | +0.17 / +0.05 | 2.69 | 2026-09-24 13:40 | 9.158 | stop | -4.11% | +1.10 / -0.90 |
| 2026-09-22 9:50 | AXTI | bounce | 77.49 | -0.55 / -0.41 | 1.92 | 2026-09-24 9:30 | 70.06 | stop | -9.60% | +0.21 / -1.32 |
| 2026-09-22 9:50 | GPUS | buy zone | 0.1812 | -0.01 / -0.38 | 17.16 | 2026-09-25 9:30 | 0.164 | stop | -9.57% | +0.14 / -1.00 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.17% | +1.68 / -0.01 |
| 2026-09-25 9:50 | IREN (crypto) | buy zone | 44.44 | -0.33 / -0.62 | 4.8 | 2026-09-25 10:00 | 43.55 | stop | -2.00% | +0.01 / -0.32 |
| 2026-09-25 9:50 | BTDR (crypto) | buy zone | 11.72 | +0.06 / -0.51 | 5.82 | 2026-09-25 10:00 | 11.47 | stop | -2.17% | +0.00 / -0.34 |
| 2026-09-28 9:50 | POET | buy zone | 7.515 | -0.54 / -0.57 | 7.47 | 2026-09-28 10:45 | 7.359 | stop | -2.08% | +0.01 / -0.43 |
| 2026-09-28 9:50 | SMCI | buy zone | 42.29 | -0.20 / -0.42 | 4.81 | 2026-09-30 11:55 | 40.49 | stop | -4.26% | +0.17 / -0.78 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| AXTI | 2026-09-28 | 74.11 | 71.04 | 89.34 | 86.66 | +16.94% |
| NOW | 2026-09-29 | 130.6 | 127.1 | 146.9 | 136.1 | +4.16% |
| RIOT | 2026-10-01 | 19.67 | 18.39 | 21.78 | 19.32 | -1.78% |
| LUNR | 2026-10-05 | 14.14 | 13.35 | 15.84 | 14.29 | +1.07% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-08-24 | $991.07 | CRSP, LUNR, UMAC |
| 2026-08-25 | $1020.34 | CRCL, CRSP, LUNR |
| 2026-08-26 | $989.82 | CRCL, CRSP, IONQ |
| 2026-08-27 | $1020.82 | CRCL, CRSP, DELL, IONQ |
| 2026-08-28 | $965.90 | CRCL, CRSP, DELL, IONQ |
| 2026-08-31 | $987.27 | CRCL, CRSP, DELL, IONQ |
| 2026-09-01 | $951.09 | CRCL, CRSP |
| 2026-09-02 | $956.33 | CRCL, CRSP, WULF |
| 2026-09-03 | $1004.30 | AEHR, CRSP, WULF |
| 2026-09-04 | $1034.53 | AEHR, BULL, CRSP, WULF |
| 2026-09-08 | $1040.34 | AEHR, DUOL |
| 2026-09-09 | $1051.13 | SMR |
| 2026-09-10 | $1030.64 | AXTI, NBIS |
| 2026-09-11 | $1025.19 | AXTI, GRAL, NBIS, SOFI |
| 2026-09-14 | $984.84 | GRAL, SOFI |
| 2026-09-15 | $963.86 | APLD, GRAL, RXRX, SOFI |
| 2026-09-16 | $960.31 | APLD, GRAL, RXRX |
| 2026-09-17 | $1021.08 | APLD, CRWV, GRAL, RXRX |
| 2026-09-18 | $1048.20 | APLD, CRWV, GRAL |
| 2026-09-21 | $1126.41 | CRWV, STNE |
| 2026-09-22 | $1133.75 | AXTI, CRWV, GPUS, STNE |
| 2026-09-23 | $1091.00 | AXTI, CRWV, GPUS, STNE |
| 2026-09-24 | $1099.20 | CRWV, GPUS, HIMS |
| 2026-09-25 | $1056.46 | CRWV |
| 2026-09-28 | $1038.68 | AXTI, CRWV, SMCI |
| 2026-09-29 | $1051.19 | AXTI, CRWV, NOW, SMCI |
| 2026-09-30 | $1056.77 | AXTI, CRWV, NOW |
| 2026-10-01 | $1083.50 | AXTI, CRWV, NOW, RIOT |
| 2026-10-02 | $1102.38 | AXTI, NOW, RIOT |
| 2026-10-05 | $1106.26 | AXTI, LUNR, NOW, RIOT |

