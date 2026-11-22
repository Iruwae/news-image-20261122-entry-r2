# Sunday 22 November 2026 — The World in One Day

A single broadsheet image summing up 22 November 2026 world news: the COP31 deal package put to ~200 nations, the Peru quake aftermath, and the Gulf strikes — 35 stories across 7 regions, each dated and checked.

[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/Iruwae/news-image-20261122-entry-r2/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/Iruwae/news-image-20261122-entry-r2/reward.svg)](https://make.fun/bounty/news-image-20261122)

[View the competition on make.fun](https://make.fun/bounty/news-image-20261122)

## How it is built

`draw.py` (Python + PIL, no network) draws `entry.png` at 1024×1024. `main.ts` (Node 22) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy byte-for-byte.

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Verification

Every story names its source beside it. Weekend stories are framed as reported / still developing on Sunday 22 November, with their original dates named in the DATE CHECK box on the image. Verification badges (CONFIRMED / REPORTED / OFFICIAL / FORECAST) and the "HOW WE CHECKED" legend explain how each story was checked.
