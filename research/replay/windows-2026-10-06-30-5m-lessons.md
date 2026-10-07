# Replay windows: 30 windows of 30 sessions ending 2026-08-25 to 2026-10-06, 5-minute bars

$1,000 each window. S&P 500 over the same windows: median +1.3%, -2.2% to +4.7%. The windows overlap, so they are not independent tests: the spread shows how much the start date moves the result.

| Rules | Median return | Mean | Worst window | Best window | Beat the S&P 500 | Doubled ($2,000) | Closed trades per window |
|---|---:|---:|---:|---:|---:|---:|---:|
| Live rules | +3.1% | +4.8% | -4.4% | +28.9% | 22/30 | 0/30 | 17 |
| No entries before 9:45 | +2.6% | +3.0% | -7.1% | +31.4% | 20/30 | 0/30 | 19 |
| No entries while SPY is down 0.35%+ (orders cancelled) | +1.0% | +1.4% | -10.8% | +16.7% | 15/30 | 0/30 | 17 |
| Both: entries from 9:45, S&P gate 0.35% | +2.0% | +2.4% | -9.3% | +18.8% | 22/30 | 0/30 | 17 |
| Size on the stop distance plus a 1% gap allowance | +3.5% | +5.2% | -6.6% | +28.2% | 23/30 | 0/30 | 17 |
| Size on the stop distance plus a 2% gap allowance | +5.5% | +4.8% | -13.6% | +30.4% | 18/30 | 0/30 | 20 |
| No entry within 0.3 ATR of its stop | +4.1% | +4.1% | -8.2% | +26.4% | 17/30 | 0/30 | 17 |
| No entry within 0.45 ATR of its stop | +0.6% | +3.5% | -6.3% | +25.8% | 15/30 | 0/30 | 16 |
| No entry while down 1.0+ ATR on the day | +3.7% | +4.8% | -4.4% | +18.0% | 18/30 | 0/30 | 17 |
| No entry while down 1.5+ ATR on the day | +3.1% | +4.5% | -4.4% | +21.0% | 22/30 | 0/30 | 17 |
| Entries only 0.25+ ATR under the prior close | +8.0% | +8.2% | -3.2% | +20.9% | 27/30 | 0/30 | 17 |
| Gap through the stop: sell at 9:55 if still under | +3.1% | +4.9% | -3.5% | +29.0% | 21/30 | 0/30 | 17 |
