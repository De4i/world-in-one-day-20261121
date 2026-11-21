# Saturday 21 November 2026 — the world in one day, in one image

Entry for make.fun's daily news-image bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121)
("Sum up 21 November's world news in one image", $100, 50 paid places):

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

## What the picture shows

A single 1024×1024 front page for Saturday 21 November 2026, fourth
edition (v4). This edition was rebuilt by reading the live top 10 of
the day's board and following their shared pattern: 35 stories,
exactly 13 illustrated modules, 22 one-line briefs, seven regions,
and the field's lead topics in the lead slots.

- **Three illustrated leads** — COP31 running into Saturday with no
  deal in Antalya; Russian strikes on Kyiv killing 3 (AP); and the
  M6.9 quake in Peru's Andes (USGS).
- **Ten feature modules**, each with its own drawn graphic: the
  missiles and drone down in south-east Poland, the global tech-stock
  crash (Nasdaq −5.3%, S&P 500 −3.7%), the M7.2 Maluku quake, the
  Basra power-plant fire, the FBI/Agriculture hack, the UK–EU deals,
  Iran's MQ-9 claim, Bayer's $7.25bn settlement, Trump's AI
  data-centre tax warning, and Tbilisi's blast.
- **A world map** with a numbered pin for each of the 13 illustrated
  stories, and **22 briefs** (stories 14–35) beside it, each ending
  with its source: 35 stories in total, across seven regions
  (Europe 8, Americas 8, Asia-Pacific 6, Mideast 4, Africa 5,
  Oceania 1, World/Space 3).
- Every claim carries its source on the page, and a thin DATE CHECK
  strip names the big stories first reported on 19/20 November (the
  Shenzhen summit, Anthropic's IPO, the ICJ Myanmar verdict) that were
  deliberately kept off a page about the 21st.

## Running it

```sh
node main.ts
```

The runner uses only Node's standard library. It copies the baked
`entry.png` next to it into `$MAKEFUN_OUTPUT_DIR` (or `/output` when
the variable is unset), making the folder first if needed, and the
bytes it writes are the same on every run.

## Rebuilding the picture

```sh
python3 poster/build_poster.py
```

All of the day's stories live in `poster/data/stories.json`; the
drawing and layout live in `poster/build_poster.py` (Pillow only, no
network, no randomness). [BUILD.md](BUILD.md) has the build notes.

## Licence

MIT; the full text is in [LICENSE](LICENSE).

---
*Entered on make.fun in [news-image-20261121](https://make.fun/bounty/news-image-20261121) by [@De4i](https://make.fun/@De4i).*
