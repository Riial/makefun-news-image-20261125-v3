# WORLD IN ONE FRAME — November 25, 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Riial/makefun-news-image-20261125-v3/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Riial/makefun-news-image-20261125-v3/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image summing up the world's news of Wednesday, 25 November 2026: 35 verified
stories across 9 regions and 15 sectors, as a data-journalism broadsheet.

- **Masthead + precise world map** (real coastline from Natural Earth / world-atlas
  land-110m) with 35 pins, one per story, coloured by sector, and 9 region labels.
- **5 lead stories** (#01–#05), each with a data chart of its real numbers: Ras Tanura
  capacity bar + 3-phase strip, Shenzhou launch-to-docking timeline, drone
  interception bars, China tariff stacked bar, Asian index sparkline.
- **30-story regional directory** (#06–#35) in 3 balanced columns, region counts
  including the leads (8+7+5+4+3+2+2+2+2 = 35), key numbers in sector colour.
- **Stat strip, Global Pulse ticker, DATE CHECK** of excluded prior-day events,
  15-sector legend, and source attribution.

Built from `build/index.html` (HTML + CSS + hand-drawn SVG data charts, no
text-to-image), rendered to `entry.png` (1024×1024) with headless Chromium.
`main.py` copies `entry.png` to `/output/entry.png` after verifying its SHA-256.
