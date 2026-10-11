# Replay of the rules, 2026-07-17 to 2026-10-09 (60 sessions, 5-minute bars)

$1,000 each; S&P 500 +3.71%, Nasdaq-100 +6.42% over the same sessions. Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.

| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |
|---|---:|---:|---:|---:|---:|---:|---|
| Paper book: live rules (radar, resting limits, 1% gap allowance) | +7.23% | 40 | 22.5% | 1.65% | 1.17 | -23.01% | HIMX, APLD, SMCI |
| Real book: live rules (S&P gate, night sleeve) | +6.40% | 31 | 41.9% | 0.53% | 1.23 | -8.88% | HIMX, APLD |
| Real book's radar part alone (no night sleeve) | +1.20% | 13 | 15.4% | -0.34% | 0.88 | -8.87% | HIMX, APLD |
| Night sleeve alone (2 slots, down 1.5+ ATR in the lowest quarter, sold at the open) | +4.13% | 24 | 58.3% | 0.69% | 1.74 | -1.99% | - |

## Paper book: live rules (radar, resting limits, 1% gap allowance): 2026-07-17 to 2026-10-09 (60 sessions)

$1000 -> $1072.27 (+7.23%; realized $+65.62, open positions $+6.65); S&P 500 +3.71%, Nasdaq-100 +6.42%. 40 closed trades, 9 winners (22.5%), average trade 1.65%, average win 24.55%, average loss -5.0%, profit factor 1.17, worst drawdown -23.01%. Exits: target 9, stop 31. Resting orders filled: 13/16.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -3.23%, total $-34.72
- stopped on a later session: 27 trades, 0 won, average -5.26%, total $-345.79
- stopped at the open (gapped through the stop): 7 trades, 0 won, average -5.56%, total $-87.77
- never rose 0.5 ATR above the entry: 17 trades, 0 won, average -4.75%, total $-195.49
- crypto-linked: 9 trades, 1 won, average -2.59%, total $-77.25
- bought on a dip of 0.5+ ATR (any time): 25 trades, 5 won, average +0.43%, total $+2.00
- bought less than 0.25 ATR under the prior close: 9 trades, 2 won, average -1.35%, total $-47.38
- resting limit fills: 11 trades, 2 won, average +4.19%, total $+42.90
- run entries inside the buy zone: 21 trades, 4 won, average +0.23%, total $+23.80
- run entries on a bounce (touched the zone, back above it): 8 trades, 3 won, average +1.90%, total $-1.08
- support tested 3+ times: 30 trades, 8 won, average +2.17%, total $+73.20
- support tested twice: 9 trades, 1 won, average +0.98%, total $+10.90
- radar keeps (GPUS, IREN, BTDR) without a tested support: 1 trade, 0 won, average -7.89%, total $-18.48

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-17 9:30 | UMAC | limit | 16.05 | -0.25 / -0.25 | 6.28 | 2026-08-04 12:50 | 26.22 | target | +63.33% | +4.35 / -0.11 |
| 2026-07-17 9:30 | CRSP | limit | 47.51 | -0.30 / -0.30 | 5.0 | 2026-08-19 15:05 | 59 | target | +24.19% | +3.28 / -0.46 |
| 2026-07-17 9:40 | HIMX | limit | 12.11 | -0.58 / -0.70 | 5.34 | 2026-07-29 12:10 | 11.41 | stop | -5.81% | +1.57 / -0.64 |
| 2026-07-17 10:50 | META | limit | 631.3 | -0.58 / -1.14 | 5.96 | 2026-07-23 9:30 | 608.1 | stop | -3.68% | +0.85 / -0.87 |
| 2026-07-23 9:50 | DUOL | bounce | 119.1 | +0.09 / -0.05 | 2.17 | 2026-07-27 14:50 | 134.2 | target | +12.67% | +1.97 / -0.25 |
| 2026-07-27 14:50 | NBIS | buy zone | 185.9 | +0.41 / -0.08 | 1.98 | 2026-07-28 9:50 | 166.9 | stop | -10.26% | +0.26 / -0.85 |
| 2026-07-28 9:50 | DELL | buy zone | 365.8 | -0.82 / -1.94 | 4.83 | 2026-08-04 9:50 | 459.5 | target | +25.61% | +3.02 / -0.22 |
| 2026-07-29 12:20 | HUT (crypto) | bounce | 89.1 | -0.11 / -1.18 | 1.64 | 2026-07-30 11:50 | 106.8 | target | +19.86% | +1.75 / -0.19 |
| 2026-07-30 11:50 | UPST | buy zone | 26.28 | -0.06 / -0.20 | 2.72 | 2026-08-03 11:50 | 29.29 | target | +11.41% | +1.95 / -0.05 |
| 2026-08-04 9:50 | AXTI | buy zone | 61.44 | -0.47 / -0.81 | 11.84 | 2026-08-07 15:50 | 89.24 | target | +45.25% | +3.12 / -0.10 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-07 15:50 | MARA (crypto) | buy zone | 10.03 | +0.00 / -0.61 | 3.13 | 2026-08-13 10:55 | 9.303 | stop | -7.21% | +0.24 / -0.69 |
| 2026-08-13 11:05 | ONDS | bounce | 9.193 | -1.15 / -0.84 | 3.29 | 2026-08-17 9:30 | 8.519 | stop | -7.35% | +0.65 / -0.98 |
| 2026-08-17 9:50 | UPST | buy zone | 29.73 | -0.04 / -0.39 | 3.07 | 2026-08-20 10:10 | 28.42 | stop | -4.43% | +1.06 / -0.74 |
| 2026-08-19 15:05 | NBIS | buy zone | 219.2 | -0.59 / -1.07 | 10.87 | 2026-08-20 9:50 | 213.4 | stop | -2.63% | +0.21 / -0.24 |
| 2026-08-20 9:50 | RXRX | buy zone | 3.332 | -0.58 / -0.97 | 40.55 | 2026-08-20 10:05 | 3.281 | stop | -1.52% | +0.00 / -0.24 |
| 2026-08-24 9:30 | RXRX | limit | 3.4 | -0.48 / -0.54 | 5.59 | 2026-08-24 9:35 | 3.274 | stop | -3.71% | +0.00 / -0.65 |
| 2026-08-24 9:30 | SMCI | limit | 36.2 | -0.28 / -0.41 | 9.43 | 2026-08-24 9:45 | 34.65 | stop | -4.28% | +0.00 / -0.62 |
| 2026-08-24 9:50 | CRSP | bounce | 56.96 | -0.34 / -0.97 | 2.33 | 2026-09-08 9:30 | 54.3 | stop | -4.67% | +1.75 / -1.59 |
| 2026-08-25 9:30 | SOUN | limit | 7.01 | +0.10 / +0.02 | 5.48 | 2026-09-03 11:10 | 6.7 | stop | -4.43% | +0.77 / -0.63 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-28 12:50 | COIN (crypto) | buy zone | 177.4 | -0.46 / -1.31 | 4.18 | 2026-09-15 14:45 | 169.6 | stop | -4.45% | +1.82 / -0.92 |
| 2026-09-03 11:20 | GPUS | buy zone | 0.181 | +0.42 / -0.51 | 21.1 | 2026-09-24 9:35 | 0.1669 | stop | -7.89% | +0.74 / -0.40 |
| 2026-09-08 9:50 | DUOL | buy zone | 145.7 | -0.26 / -1.18 | 4.17 | 2026-09-09 10:15 | 140.8 | stop | -3.32% | +0.37 / -0.79 |
| 2026-09-09 10:20 | QBTS | buy zone | 17 | -0.16 / -0.62 | 8.65 | 2026-09-14 9:30 | 16.06 | stop | -5.52% | +0.64 / -0.85 |
| 2026-09-14 9:50 | SMCI | bounce | 37.43 | -1.21 / -1.20 | 1.74 | 2026-09-21 10:20 | 41.33 | target | +10.43% | +1.82 / -0.93 |
| 2026-09-15 14:50 | BULL | bounce | 8.592 | -0.35 / -0.86 | 2.43 | 2026-09-16 10:55 | 8.055 | stop | -6.27% | +0.23 / -1.03 |
| 2026-09-16 11:05 | DUOL | bounce | 147.9 | -0.45 / -0.76 | 2.37 | 2026-09-28 9:30 | 140.6 | stop | -5.00% | +0.64 / -1.24 |
| 2026-09-21 10:20 | STNE | bounce | 9.584 | +0.17 / +0.13 | 2.36 | 2026-09-24 13:40 | 9.158 | stop | -4.46% | +1.01 / -0.98 |
| 2026-09-24 9:50 | HIMS | buy zone | 27.39 | -0.28 / -0.71 | 1.79 | 2026-09-25 12:05 | 29.65 | target | +8.21% | +1.68 / -0.01 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-09-25 12:05 | CRCL (crypto) | buy zone | 88.71 | -0.15 / -0.65 | 1.91 | 2026-09-30 10:30 | 82.87 | stop | -6.61% | +0.07 / -0.90 |
| 2026-09-28 9:50 | AXTI | buy zone | 74.11 | -0.38 / -0.77 | 5.03 | 2026-10-08 15:45 | 71 | stop | -4.20% | +2.27 / -0.49 |
| 2026-09-29 12:05 | IREN (crypto) | buy zone | 41.38 | +0.32 / -0.13 | 2.65 | 2026-10-01 9:40 | 40.17 | stop | -2.93% | +0.40 / -0.50 |
| 2026-09-30 10:35 | BTDR (crypto) | buy zone | 10.72 | +0.34 / -0.22 | 2.25 | 2026-10-01 10:00 | 10.21 | stop | -4.76% | +0.07 / -0.70 |
| 2026-10-01 9:50 | RIOT (crypto) | buy zone | 19.67 | +0.07 / -0.34 | 1.73 | 2026-10-07 9:30 | 18.35 | stop | -6.71% | +1.00 / -1.11 |
| 2026-10-02 9:35 | PATH | limit | 13.23 | +0.14 / -0.14 | 13.66 | 2026-10-05 11:00 | 12.81 | stop | -3.19% | +0.14 / -0.62 |
| 2026-10-05 11:05 | WULF (crypto) | buy zone | 14.78 | +0.45 / -0.73 | 3.65 | 2026-10-08 9:30 | 13.9 | stop | -5.98% | +0.41 / -1.04 |
| 2026-10-07 9:50 | SMR | buy zone | 7.545 | -0.56 / -0.92 | 4.7 | 2026-10-08 12:50 | 7.252 | stop | -3.89% | +0.27 / -0.55 |
| 2026-10-08 9:50 | CRWV | buy zone | 84.1 | -0.36 / -0.97 | 2.71 | 2026-10-08 12:45 | 81.24 | stop | -3.42% | +0.38 / -0.69 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.82 | 11.57 | 15.81 | 13.3 | +3.78% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |
| SMCI | 2026-10-09 | 41.9 | 40.59 | 50.74 | 41.86 | -0.10% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-17 | $1028.94 | CRSP, HIMX, META, UMAC |
| 2026-07-20 | $1027.13 | CRSP, HIMX, META, UMAC |
| 2026-07-21 | $1072.33 | CRSP, HIMX, META, UMAC |
| 2026-07-22 | $1061.21 | CRSP, HIMX, META, UMAC |
| 2026-07-23 | $1068.46 | CRSP, DUOL, HIMX, UMAC |
| 2026-07-24 | $1031.12 | CRSP, DUOL, HIMX, UMAC |
| 2026-07-27 | $1059.38 | CRSP, HIMX, NBIS, UMAC |
| 2026-07-28 | $1043.78 | CRSP, DELL, HIMX, UMAC |
| 2026-07-29 | $991.72 | CRSP, DELL, HUT, UMAC |
| 2026-07-30 | $1081.57 | CRSP, DELL, UMAC, UPST |
| 2026-07-31 | $1089.34 | CRSP, DELL, UMAC, UPST |
| 2026-08-03 | $1146.56 | CRSP, DELL, HIMX, UMAC |
| 2026-08-04 | $1246.08 | AXTI, CRSP, HIMX |
| 2026-08-05 | $1244.66 | AXTI, CRSP, HIMX, POET |
| 2026-08-06 | $1286.90 | AXTI, CRSP, HIMX, POET |
| 2026-08-07 | $1377.44 | CRSP, HIMX, MARA, POET |
| 2026-08-10 | $1353.05 | CRSP, HIMX, MARA, POET |
| 2026-08-11 | $1362.82 | CRSP, HIMX, MARA, POET |
| 2026-08-12 | $1372.75 | CRSP, HIMX, MARA, POET |
| 2026-08-13 | $1353.13 | CRSP, HIMX, ONDS, POET |
| 2026-08-14 | $1390.64 | CRSP, HIMX, ONDS, POET |
| 2026-08-17 | $1369.86 | CRSP, HIMX, POET, UPST |
| 2026-08-18 | $1310.97 | CRSP, HIMX, POET, UPST |
| 2026-08-19 | $1357.85 | HIMX, NBIS, POET, UPST |
| 2026-08-20 | $1308.52 | HIMX, POET |
| 2026-08-21 | $1309.14 | HIMX, POET |
| 2026-08-24 | $1259.55 | CRSP, HIMX |
| 2026-08-25 | $1282.66 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-26 | $1268.72 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-27 | $1282.37 | CRSP, HIMX, LUNR, SOUN |
| 2026-08-28 | $1254.01 | COIN, CRSP, HIMX, SOUN |
| 2026-08-31 | $1271.64 | COIN, CRSP, HIMX, SOUN |
| 2026-09-01 | $1233.28 | COIN, CRSP, HIMX, SOUN |
| 2026-09-02 | $1228.13 | COIN, CRSP, HIMX, SOUN |
| 2026-09-03 | $1267.34 | COIN, CRSP, GPUS, HIMX |
| 2026-09-04 | $1251.62 | COIN, CRSP, GPUS, HIMX |
| 2026-09-08 | $1242.46 | COIN, DUOL, GPUS, HIMX |
| 2026-09-09 | $1235.38 | COIN, GPUS, HIMX, QBTS |
| 2026-09-10 | $1210.69 | COIN, GPUS, HIMX, QBTS |
| 2026-09-11 | $1228.32 | COIN, GPUS, HIMX, QBTS |
| 2026-09-14 | $1244.23 | COIN, GPUS, HIMX, SMCI |
| 2026-09-15 | $1181.34 | BULL, GPUS, HIMX, SMCI |
| 2026-09-16 | $1159.81 | DUOL, GPUS, HIMX, SMCI |
| 2026-09-17 | $1189.68 | DUOL, GPUS, HIMX, SMCI |
| 2026-09-18 | $1174.17 | DUOL, GPUS, HIMX, SMCI |
| 2026-09-21 | $1227.68 | DUOL, GPUS, HIMX, STNE |
| 2026-09-22 | $1215.90 | DUOL, GPUS, HIMX, STNE |
| 2026-09-23 | $1186.16 | DUOL, GPUS, HIMX, STNE |
| 2026-09-24 | $1196.38 | DUOL, HIMS, HIMX |
| 2026-09-25 | $1197.54 | BTBT, CRCL, DUOL, HIMX |
| 2026-09-28 | $1166.20 | AXTI, BTBT, CRCL, HIMX |
| 2026-09-29 | $1181.37 | AXTI, CRCL, HIMX, IREN |
| 2026-09-30 | $1166.94 | AXTI, BTDR, HIMX, IREN |
| 2026-10-01 | $1175.73 | AXTI, HIMX, RIOT |
| 2026-10-02 | $1199.23 | AXTI, HIMX, PATH, RIOT |
| 2026-10-05 | $1187.17 | AXTI, HIMX, RIOT, WULF |
| 2026-10-06 | $1179.14 | AXTI, HIMX, RIOT, WULF |
| 2026-10-07 | $1144.16 | AXTI, HIMX, SMR, WULF |
| 2026-10-08 | $1070.60 | HIMX |
| 2026-10-09 | $1072.27 | APLD, HIMX, SMCI |

## Real book: live rules (S&P gate, night sleeve): 2026-07-17 to 2026-10-09 (60 sessions)

$1000 -> $1064.02 (+6.40%; realized $+36.74, open positions $+27.28); S&P 500 +3.71%, Nasdaq-100 +6.42%. 31 closed trades, 13 winners (41.9%), average trade 0.53%, average win 6.02%, average loss -3.44%, profit factor 1.23, worst drawdown -8.88%. Exits: target 2, stop 10, open 19. Resting orders filled: 14/62.

### What the trades had in common

- stopped the session it was bought: 3 trades, 0 won, average -3.45%, total $-26.67
- stopped on a later session: 7 trades, 0 won, average -5.19%, total $-91.50
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -5.00%, total $-51.07
- never rose 0.5 ATR above the entry: 24 trades, 9 won, average -1.14%, total $-68.92
- crypto-linked: 8 trades, 5 won, average +3.72%, total $+70.69
- bought at the open after a gap down of 0.5+ ATR: 1 trade, 0 won, average -4.42%, total $-10.96
- bought on a dip of 0.5+ ATR (any time): 23 trades, 11 won, average +0.00%, total $-0.84
- bought less than 0.25 ATR under the prior close: 5 trades, 2 won, average +5.83%, total $+69.69
- resting limit fills: 12 trades, 2 won, average -0.19%, total $-9.61
- support tested 3+ times: 12 trades, 2 won, average -0.19%, total $-9.61
- radar keeps (GPUS, IREN, BTDR) without a tested support: 19 trades, 11 won, average +0.98%, total $+46.35

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-22 9:35 | POET | limit | 8.02 | -0.44 / -0.47 | 7.64 | 2026-07-23 9:30 | 7.505 | stop | -6.43% | +0.25 / -0.68 |
| 2026-07-22 15:50 | PATH | night | 10.58 | -0.03 / -2.03 | 0 | 2026-07-23 9:30 | 10.75 | open | +1.62% | +0.27 / +0.00 |
| 2026-07-24 9:30 | APLD | limit | 29.18 | -0.29 / -0.29 | 5.09 | 2026-07-24 9:35 | 28.61 | stop | -1.96% | +0.00 / -0.25 |
| 2026-07-24 10:30 | HOOD | limit | 94.37 | -0.28 / -1.14 | 6.19 | 2026-07-28 9:30 | 90.53 | stop | -4.07% | +0.80 / -0.72 |
| 2026-07-24 15:50 | HIMS | night | 28.21 | +0.30 / -1.86 | 0 | 2026-07-27 9:30 | 28.72 | open | +1.77% | +0.21 / +0.00 |
| 2026-07-28 9:30 | HIMX | limit | 12.07 | -0.73 / -0.73 | 6.87 | 2026-07-28 9:55 | 11.54 | stop | -4.42% | +0.11 / -0.58 |
| 2026-07-29 15:50 | ONDS | night | 6.794 | -0.10 / -1.75 | 0 | 2026-07-30 9:30 | 6.996 | open | +2.97% | +0.36 / +0.00 |
| 2026-07-29 15:50 | RIOT (crypto) | night | 18.23 | -0.13 / -1.72 | 0 | 2026-07-30 9:30 | 20.02 | open | +9.80% | +1.03 / +0.00 |
| 2026-07-30 9:35 | AFRM | limit | 69.88 | +0.24 / -0.07 | 7.84 | 2026-08-28 9:50 | 85.85 | target | +22.84% | +6.08 / -0.01 |
| 2026-08-05 15:45 | POET | limit | 8.15 | -0.46 / -0.58 | 7.54 | 2026-08-24 10:00 | 7.699 | stop | -5.55% | +2.53 / -0.64 |
| 2026-08-05 15:50 | SNAP | night | 5.346 | -0.36 / -1.80 | 0 | 2026-08-06 9:30 | 5.19 | open | -2.93% | +0.00 / -0.59 |
| 2026-08-10 15:50 | BTDR (crypto) | night | 8.853 | +0.19 / -1.59 | 0 | 2026-08-11 9:30 | 9.211 | open | +4.05% | +0.30 / +0.00 |
| 2026-08-18 15:50 | SMTC | night | 135.7 | -0.75 / -1.70 | 0 | 2026-08-19 9:30 | 135.4 | open | -0.20% | +0.00 / -0.02 |
| 2026-08-25 9:40 | LUNR | limit | 16.29 | +0.19 / -0.23 | 5.62 | 2026-08-28 12:40 | 15.28 | stop | -6.22% | +0.28 / -0.62 |
| 2026-08-26 15:50 | SNAP | night | 5.471 | +0.19 / -1.73 | 0 | 2026-08-27 9:30 | 5.419 | open | -0.95% | +0.00 / -0.16 |
| 2026-08-28 15:50 | IREN (crypto) | night | 35.2 | -0.90 / -1.64 | 0 | 2026-08-31 9:30 | 35.71 | open | +1.45% | +0.16 / +0.00 |
| 2026-09-02 9:30 | MARA (crypto) | limit | 10.01 | -0.24 / -0.24 | 3.48 | 2026-09-11 10:05 | 12.17 | target | +21.58% | +2.55 / -0.02 |
| 2026-09-04 15:50 | PATH | night | 15.24 | -2.61 / -3.93 | 0 | 2026-09-08 9:30 | 15.13 | open | -0.73% | +0.00 / -0.11 |
| 2026-09-09 9:30 | RGTI | limit | 15.63 | -0.18 / -0.18 | 19.37 | 2026-09-10 9:30 | 14.84 | stop | -5.09% | +0.30 / -0.77 |
| 2026-09-11 15:50 | SMR | night | 8.722 | -0.80 / -2.15 | 0 | 2026-09-14 9:30 | 8.293 | open | -4.93% | +0.00 / -0.60 |
| 2026-09-14 15:50 | SMTC | night | 148 | -1.15 / -1.81 | 0 | 2026-09-15 9:30 | 149.4 | open | +0.94% | +0.14 / +0.00 |
| 2026-09-15 15:50 | CRCL (crypto) | night | 86.4 | -0.72 / -1.55 | 0 | 2026-09-16 9:30 | 85.67 | open | -0.85% | +0.00 / -0.10 |
| 2026-09-16 15:50 | BULL | night | 7.7 | -0.29 / -1.87 | 0 | 2026-09-17 9:30 | 7.934 | open | +3.03% | +0.49 / +0.00 |
| 2026-09-16 15:50 | RCAT | night | 7.119 | -0.05 / -1.80 | 0 | 2026-09-17 9:30 | 7.375 | open | +3.59% | +0.58 / +0.00 |
| 2026-09-23 15:50 | RXRX | night | 3.732 | -0.09 / -1.42 | 0 | 2026-09-24 9:30 | 3.652 | open | -2.16% | +0.00 / -0.28 |
| 2026-09-25 9:45 | BTBT (crypto) | limit | 1.75 | +0.09 / -0.34 | 8.56 | 2026-09-29 12:05 | 1.671 | stop | -4.53% | +0.38 / -0.68 |
| 2026-09-30 9:40 | WULF (crypto) | limit | 14.55 | +0.18 / -0.53 | 5.23 | 2026-10-08 9:30 | 13.91 | stop | -4.42% | +1.65 / -0.75 |
| 2026-10-01 15:50 | UMAC | night | 21.8 | +0.14 / -1.75 | 0 | 2026-10-02 9:30 | 22.22 | open | +1.91% | +0.28 / +0.00 |
| 2026-10-06 15:50 | TEM | night | 71.71 | +0.26 / -2.15 | 0 | 2026-10-07 9:30 | 69.91 | open | -2.52% | +0.00 / -0.32 |
| 2026-10-08 9:35 | APLD | limit | 23.55 | +0.35 / -0.17 | 5.53 | 2026-10-08 13:25 | 22.61 | stop | -3.98% | +0.15 / -0.60 |
| 2026-10-08 15:50 | HUT (crypto) | night | 79.06 | -0.31 / -1.55 | 0 | 2026-10-09 9:30 | 81.21 | open | +2.71% | +0.33 / +0.00 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.06 | 11.57 | 15.81 | 13.3 | +10.28% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-17 | $1000.00 | - |
| 2026-07-20 | $1000.00 | - |
| 2026-07-21 | $1000.00 | - |
| 2026-07-22 | $992.37 | PATH, POET |
| 2026-07-23 | $989.34 | - |
| 2026-07-24 | $984.82 | HIMS, HOOD |
| 2026-07-27 | $992.20 | HOOD |
| 2026-07-28 | $967.80 | - |
| 2026-07-29 | $968.15 | ONDS, RIOT |
| 2026-07-30 | $1010.38 | AFRM |
| 2026-07-31 | $1004.35 | AFRM |
| 2026-08-03 | $1033.61 | AFRM, HIMX |
| 2026-08-04 | $1071.39 | AFRM, HIMX |
| 2026-08-05 | $1052.71 | AFRM, HIMX, POET, SNAP |
| 2026-08-06 | $1061.71 | AFRM, HIMX, POET |
| 2026-08-07 | $1086.60 | AFRM, HIMX, POET |
| 2026-08-10 | $1074.87 | AFRM, BTDR, HIMX, POET |
| 2026-08-11 | $1099.33 | AFRM, HIMX, POET |
| 2026-08-12 | $1098.86 | AFRM, HIMX, POET |
| 2026-08-13 | $1108.19 | AFRM, HIMX, POET |
| 2026-08-14 | $1140.97 | AFRM, HIMX, POET |
| 2026-08-17 | $1125.86 | AFRM, HIMX, POET |
| 2026-08-18 | $1071.48 | AFRM, HIMX, POET, SMTC |
| 2026-08-19 | $1073.83 | AFRM, HIMX, POET |
| 2026-08-20 | $1055.87 | AFRM, HIMX, POET |
| 2026-08-21 | $1064.60 | AFRM, HIMX, POET |
| 2026-08-24 | $1039.65 | AFRM, HIMX |
| 2026-08-25 | $1052.35 | AFRM, HIMX, LUNR |
| 2026-08-26 | $1041.64 | AFRM, HIMX, LUNR, SNAP |
| 2026-08-27 | $1050.89 | AFRM, HIMX, LUNR |
| 2026-08-28 | $1060.45 | HIMX, IREN |
| 2026-08-31 | $1064.07 | HIMX |
| 2026-09-01 | $1057.61 | HIMX |
| 2026-09-02 | $1070.84 | HIMX, MARA |
| 2026-09-03 | $1099.96 | HIMX, MARA |
| 2026-09-04 | $1094.40 | HIMX, MARA, PATH |
| 2026-09-08 | $1115.29 | HIMX, MARA |
| 2026-09-09 | $1107.01 | HIMX, MARA, RGTI |
| 2026-09-10 | $1084.14 | HIMX, MARA |
| 2026-09-11 | $1119.03 | HIMX, SMR |
| 2026-09-14 | $1084.82 | HIMX, SMTC |
| 2026-09-15 | $1080.94 | CRCL, HIMX |
| 2026-09-16 | $1074.15 | BULL, HIMX, RCAT |
| 2026-09-17 | $1106.06 | HIMX |
| 2026-09-18 | $1113.35 | HIMX |
| 2026-09-21 | $1125.63 | HIMX |
| 2026-09-22 | $1127.71 | HIMX |
| 2026-09-23 | $1116.38 | HIMX, RXRX |
| 2026-09-24 | $1109.39 | HIMX |
| 2026-09-25 | $1117.64 | BTBT, HIMX |
| 2026-09-28 | $1094.97 | BTBT, HIMX |
| 2026-09-29 | $1096.40 | HIMX |
| 2026-09-30 | $1100.49 | HIMX, WULF |
| 2026-10-01 | $1110.20 | HIMX, UMAC, WULF |
| 2026-10-02 | $1143.14 | HIMX, WULF |
| 2026-10-05 | $1118.92 | HIMX, WULF |
| 2026-10-06 | $1126.20 | HIMX, TEM, WULF |
| 2026-10-07 | $1092.26 | HIMX, WULF |
| 2026-10-08 | $1056.53 | HIMX, HUT |
| 2026-10-09 | $1064.02 | APLD, HIMX |

## Real book's radar part alone (no night sleeve): 2026-07-17 to 2026-10-09 (60 sessions)

$1000 -> $1012.04 (+1.20%; realized $-14.04, open positions $+26.08); S&P 500 +3.71%, Nasdaq-100 +6.42%. 13 closed trades, 2 winners (15.4%), average trade -0.34%, average win 22.21%, average loss -4.43%, profit factor 0.88, worst drawdown -8.87%. Exits: target 2, stop 11. Resting orders filled: 15/77.

### What the trades had in common

- stopped the session it was bought: 4 trades, 0 won, average -3.12%, total $-31.16
- stopped on a later session: 7 trades, 0 won, average -5.19%, total $-88.53
- stopped at the open (gapped through the stop): 4 trades, 0 won, average -5.00%, total $-49.88
- never rose 0.5 ATR above the entry: 8 trades, 0 won, average -4.34%, total $-84.64
- crypto-linked: 3 trades, 1 won, average +4.21%, total $+27.25
- bought at the open after a gap down of 0.5+ ATR: 2 trades, 0 won, average -3.26%, total $-15.93
- bought on a dip of 0.5+ ATR (any time): 5 trades, 0 won, average -4.11%, total $-50.98
- bought less than 0.25 ATR under the prior close: 5 trades, 2 won, average +5.83%, total $+68.48
- resting limit fills: 13 trades, 2 won, average -0.34%, total $-14.04
- support tested 3+ times: 13 trades, 2 won, average -0.34%, total $-14.04

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
| 2026-09-30 9:40 | WULF (crypto) | limit | 14.55 | +0.18 / -0.53 | 5.23 | 2026-10-08 9:30 | 13.91 | stop | -4.42% | +1.65 / -0.75 |
| 2026-10-08 9:35 | APLD | limit | 23.55 | +0.35 / -0.17 | 5.53 | 2026-10-08 13:25 | 22.61 | stop | -3.98% | +0.15 / -0.60 |

### Still open at the end

| Name | Bought | Entry | Stop | Target | Last | Return |
|---|---|---:|---:|---:|---:|---:|
| HIMX | 2026-08-03 | 12.06 | 11.57 | 15.81 | 13.3 | +10.28% |
| APLD | 2026-10-09 | 23.55 | 22.64 | 28.67 | 23.68 | +0.55% |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-17 | $1000.00 | - |
| 2026-07-20 | $1000.00 | - |
| 2026-07-21 | $1000.00 | - |
| 2026-07-22 | $989.47 | POET |
| 2026-07-23 | $985.32 | - |
| 2026-07-24 | $981.90 | HOOD |
| 2026-07-27 | $983.83 | HOOD |
| 2026-07-28 | $959.58 | - |
| 2026-07-29 | $959.58 | - |
| 2026-07-30 | $966.09 | AFRM |
| 2026-07-31 | $960.12 | AFRM |
| 2026-08-03 | $988.59 | AFRM, HIMX |
| 2026-08-04 | $1025.00 | AFRM, HIMX |
| 2026-08-05 | $1007.90 | AFRM, HIMX, POET |
| 2026-08-06 | $1022.64 | AFRM, HIMX, POET |
| 2026-08-07 | $1046.28 | AFRM, HIMX, POET |
| 2026-08-10 | $1039.27 | AFRM, HIMX, POET |
| 2026-08-11 | $1049.14 | AFRM, HIMX, POET |
| 2026-08-12 | $1048.30 | AFRM, HIMX, POET |
| 2026-08-13 | $1057.82 | AFRM, HIMX, POET |
| 2026-08-14 | $1089.17 | AFRM, HIMX, POET |
| 2026-08-17 | $1074.25 | AFRM, HIMX, POET |
| 2026-08-18 | $1022.93 | AFRM, HIMX, POET |
| 2026-08-19 | $1025.33 | AFRM, HIMX, POET |
| 2026-08-20 | $1007.88 | AFRM, HIMX, POET |
| 2026-08-21 | $1016.47 | AFRM, HIMX, POET |
| 2026-08-24 | $992.58 | AFRM, HIMX |
| 2026-08-25 | $1004.85 | AFRM, HIMX, LUNR |
| 2026-08-26 | $996.76 | AFRM, HIMX, LUNR |
| 2026-08-27 | $1005.79 | AFRM, HIMX, LUNR |
| 2026-08-28 | $1014.14 | HIMX |
| 2026-08-31 | $1015.73 | HIMX |
| 2026-09-01 | $1009.56 | HIMX |
| 2026-09-02 | $1022.19 | HIMX, MARA |
| 2026-09-03 | $1049.99 | HIMX, MARA |
| 2026-09-04 | $1045.55 | HIMX, MARA |
| 2026-09-08 | $1066.56 | HIMX, MARA |
| 2026-09-09 | $1058.64 | HIMX, MARA, RGTI |
| 2026-09-10 | $1036.79 | HIMX, MARA |
| 2026-09-11 | $1073.12 | HIMX |
| 2026-09-14 | $1050.63 | HIMX |
| 2026-09-15 | $1043.07 | HIMX |
| 2026-09-16 | $1039.68 | HIMX |
| 2026-09-17 | $1052.02 | HIMX |
| 2026-09-18 | $1058.99 | HIMX |
| 2026-09-21 | $1070.73 | HIMX |
| 2026-09-22 | $1072.72 | HIMX |
| 2026-09-23 | $1064.16 | HIMX |
| 2026-09-24 | $1060.98 | HIMX |
| 2026-09-25 | $1068.86 | BTBT, HIMX |
| 2026-09-28 | $1047.19 | BTBT, HIMX |
| 2026-09-29 | $1048.55 | HIMX |
| 2026-09-30 | $1052.46 | HIMX, WULF |
| 2026-10-01 | $1062.01 | HIMX, WULF |
| 2026-10-02 | $1088.18 | HIMX, WULF |
| 2026-10-05 | $1065.02 | HIMX, WULF |
| 2026-10-06 | $1071.05 | HIMX, WULF |
| 2026-10-07 | $1045.65 | HIMX, WULF |
| 2026-10-08 | $1009.85 | HIMX |
| 2026-10-09 | $1012.04 | APLD, HIMX |

## Night sleeve alone (2 slots, down 1.5+ ATR in the lowest quarter, sold at the open): 2026-07-17 to 2026-10-09 (60 sessions)

$1000 -> $1041.30 (+4.13%; realized $+41.30, open positions $-0.00); S&P 500 +3.71%, Nasdaq-100 +6.42%. 24 closed trades, 14 winners (58.3%), average trade 0.69%, average win 2.72%, average loss -2.14%, profit factor 1.74, worst drawdown -1.99%. Exits: open 24.

### What the trades had in common

- never rose 0.5 ATR above the entry: 22 trades, 12 won, average +0.15%, total $+7.16
- crypto-linked: 5 trades, 4 won, average +3.43%, total $+43.97
- bought on a dip of 0.5+ ATR (any time): 24 trades, 14 won, average +0.69%, total $+41.30
- radar keeps (GPUS, IREN, BTDR) without a tested support: 24 trades, 14 won, average +0.69%, total $+41.30

### Trades

Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the highest high and lowest low while held, in ATR from the entry.

| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |
|---|---|---|---:|---:|---:|---|---:|---|---:|---:|
| 2026-07-22 15:50 | PATH | night | 10.58 | -0.03 / -2.03 | 0 | 2026-07-23 9:30 | 10.75 | open | +1.62% | +0.27 / +0.00 |
| 2026-07-24 15:50 | HIMS | night | 28.21 | +0.30 / -1.86 | 0 | 2026-07-27 9:30 | 28.72 | open | +1.77% | +0.21 / +0.00 |
| 2026-07-24 15:50 | CRWV | night | 71.98 | -0.28 / -1.52 | 0 | 2026-07-27 9:30 | 73.67 | open | +2.35% | +0.29 / +0.00 |
| 2026-07-29 15:50 | ONDS | night | 6.794 | -0.10 / -1.75 | 0 | 2026-07-30 9:30 | 6.996 | open | +2.97% | +0.36 / +0.00 |
| 2026-07-29 15:50 | RIOT (crypto) | night | 18.23 | -0.13 / -1.72 | 0 | 2026-07-30 9:30 | 20.02 | open | +9.80% | +1.03 / +0.00 |
| 2026-08-05 15:50 | SNAP | night | 5.346 | -0.36 / -1.80 | 0 | 2026-08-06 9:30 | 5.19 | open | -2.93% | +0.00 / -0.59 |
| 2026-08-10 15:50 | BTDR (crypto) | night | 8.853 | +0.19 / -1.59 | 0 | 2026-08-11 9:30 | 9.211 | open | +4.05% | +0.30 / +0.00 |
| 2026-08-18 15:50 | SMTC | night | 135.7 | -0.75 / -1.70 | 0 | 2026-08-19 9:30 | 135.4 | open | -0.20% | +0.00 / -0.02 |
| 2026-08-18 15:50 | AEHR | night | 122.9 | -0.69 / -1.61 | 0 | 2026-08-19 9:30 | 123.6 | open | +0.58% | +0.06 / +0.00 |
| 2026-08-26 15:50 | SNAP | night | 5.471 | +0.19 / -1.73 | 0 | 2026-08-27 9:30 | 5.419 | open | -0.95% | +0.00 / -0.16 |
| 2026-08-28 15:50 | IREN (crypto) | night | 35.2 | -0.90 / -1.64 | 0 | 2026-08-31 9:30 | 35.71 | open | +1.45% | +0.16 / +0.00 |
| 2026-08-28 15:50 | LEU | night | 175.9 | -0.11 / -1.58 | 0 | 2026-08-31 9:30 | 174.2 | open | -0.97% | +0.00 / -0.13 |
| 2026-09-04 15:50 | PATH | night | 15.24 | -2.61 / -3.93 | 0 | 2026-09-08 9:30 | 15.13 | open | -0.73% | +0.00 / -0.11 |
| 2026-09-11 15:50 | SMR | night | 8.722 | -0.80 / -2.15 | 0 | 2026-09-14 9:30 | 8.293 | open | -4.93% | +0.00 / -0.60 |
| 2026-09-14 15:50 | SMTC | night | 148 | -1.15 / -1.81 | 0 | 2026-09-15 9:30 | 149.4 | open | +0.94% | +0.14 / +0.00 |
| 2026-09-15 15:50 | CRCL (crypto) | night | 86.4 | -0.72 / -1.55 | 0 | 2026-09-16 9:30 | 85.67 | open | -0.85% | +0.00 / -0.10 |
| 2026-09-16 15:50 | BULL | night | 7.7 | -0.29 / -1.87 | 0 | 2026-09-17 9:30 | 7.934 | open | +3.03% | +0.49 / +0.00 |
| 2026-09-16 15:50 | RCAT | night | 7.119 | -0.05 / -1.80 | 0 | 2026-09-17 9:30 | 7.375 | open | +3.59% | +0.58 / +0.00 |
| 2026-09-23 15:50 | RXRX | night | 3.732 | -0.09 / -1.42 | 0 | 2026-09-24 9:30 | 3.652 | open | -2.16% | +0.00 / -0.28 |
| 2026-10-01 15:50 | UMAC | night | 21.8 | +0.14 / -1.75 | 0 | 2026-10-02 9:30 | 22.22 | open | +1.91% | +0.28 / +0.00 |
| 2026-10-06 15:50 | TEM | night | 71.71 | +0.26 / -2.15 | 0 | 2026-10-07 9:30 | 69.91 | open | -2.52% | +0.00 / -0.32 |
| 2026-10-06 15:50 | DNA | night | 12.42 | +0.08 / -1.97 | 0 | 2026-10-07 9:30 | 11.78 | open | -5.19% | +0.00 / -0.48 |
| 2026-10-08 15:50 | HUT (crypto) | night | 79.06 | -0.31 / -1.55 | 0 | 2026-10-09 9:30 | 81.21 | open | +2.71% | +0.33 / +0.00 |
| 2026-10-08 15:50 | CRWV | night | 81.65 | -0.36 / -1.51 | 0 | 2026-10-09 9:30 | 82.71 | open | +1.29% | +0.25 / +0.00 |

### Equity by session

| Session | Equity | Holding at the close |
|---|---:|---|
| 2026-07-17 | $1000.00 | - |
| 2026-07-20 | $1000.00 | - |
| 2026-07-21 | $1000.00 | - |
| 2026-07-22 | $1002.93 | PATH |
| 2026-07-23 | $1004.05 | - |
| 2026-07-24 | $1002.62 | CRWV, HIMS |
| 2026-07-27 | $1014.39 | - |
| 2026-07-28 | $1014.39 | - |
| 2026-07-29 | $1014.76 | ONDS, RIOT |
| 2026-07-30 | $1046.79 | - |
| 2026-07-31 | $1046.79 | - |
| 2026-08-03 | $1046.79 | - |
| 2026-08-04 | $1046.79 | - |
| 2026-08-05 | $1046.02 | SNAP |
| 2026-08-06 | $1039.13 | - |
| 2026-08-07 | $1039.13 | - |
| 2026-08-10 | $1034.50 | BTDR |
| 2026-08-11 | $1049.64 | - |
| 2026-08-12 | $1049.64 | - |
| 2026-08-13 | $1049.64 | - |
| 2026-08-14 | $1049.64 | - |
| 2026-08-17 | $1049.64 | - |
| 2026-08-18 | $1049.62 | AEHR, SMTC |
| 2026-08-19 | $1050.63 | - |
| 2026-08-20 | $1050.63 | - |
| 2026-08-21 | $1050.63 | - |
| 2026-08-24 | $1050.63 | - |
| 2026-08-25 | $1050.63 | - |
| 2026-08-26 | $1048.18 | SNAP |
| 2026-08-27 | $1048.12 | - |
| 2026-08-28 | $1049.86 | IREN, LEU |
| 2026-08-31 | $1049.40 | - |
| 2026-09-01 | $1049.40 | - |
| 2026-09-02 | $1049.40 | - |
| 2026-09-03 | $1049.40 | - |
| 2026-09-04 | $1048.54 | PATH |
| 2026-09-08 | $1047.48 | - |
| 2026-09-09 | $1047.48 | - |
| 2026-09-10 | $1047.48 | - |
| 2026-09-11 | $1044.10 | SMR |
| 2026-09-14 | $1032.87 | SMTC |
| 2026-09-15 | $1036.70 | CRCL |
| 2026-09-16 | $1033.57 | BULL, RCAT |
| 2026-09-17 | $1051.91 | - |
| 2026-09-18 | $1051.91 | - |
| 2026-09-21 | $1051.91 | - |
| 2026-09-22 | $1051.91 | - |
| 2026-09-23 | $1049.67 | RXRX |
| 2026-09-24 | $1046.23 | - |
| 2026-09-25 | $1046.23 | - |
| 2026-09-28 | $1046.23 | - |
| 2026-09-29 | $1046.23 | - |
| 2026-09-30 | $1046.23 | - |
| 2026-10-01 | $1045.98 | UMAC |
| 2026-10-02 | $1051.23 | - |
| 2026-10-05 | $1051.23 | - |
| 2026-10-06 | $1051.92 | DNA, TEM |
| 2026-10-07 | $1030.98 | - |
| 2026-10-08 | $1032.50 | CRWV, HUT |
| 2026-10-09 | $1041.30 | - |

