# Saturday 21 November 2026 — the world in one day, in one image

Entry for make.fun's daily news-image bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121)
("Sum up 21 November's world news in one image", $100, 50 paid places):

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

## What the picture shows

A single 1024×1024 front page for Saturday 21 November 2026, fifth
edition (v5). The page keeps the architecture the live top 10 share
(35 stories, exactly 13 illustrated modules, 22 one-line briefs,
seven regions, a six-number strip, a map pinned for the illustrated
stories only), and v5's work went into the dating: every story on the
page was checked against primary reporting, and the big stories that
turned out to be Friday 20 November's news were moved off the page
and into the DATE CHECK strip, named there as exclusions.

- **Three illustrated leads** — COP31 running into Saturday with no
  deal in Antalya (UN News, Reuters); Saudi air defences
  intercepting three Houthi ballistic missiles over Riyadh early on
  Saturday (Reuters); and the M6.7 quake in Peru's Andes, with the
  corrected facts: 00:09 UTC Saturday, 34 km north of Junín, felt in
  Lima, no damage or casualties immediately reported (USGS).
- **Ten feature modules**, each with its own drawn graphic: the
  Kryvyi Rih toll (Friday's missiles, overnight strikes on rescuers,
  2 dead and 60 hurt as reported Saturday, AP), the M7.2 Maluku
  quake, the Air Niugini jet's emergency landing at Davao with all
  146 aboard safe (AP, CAAP), the Basra power-plant fire, the
  FBI/Agriculture hack, Iran's MQ-9 claim, Bayer's $7.25bn
  settlement, Trump's AI data-centre tax warning, Tbilisi's blast,
  and BepiColombo's arrival at Mercury after eight years (ESA).
- **A world map** with a numbered pin for each of the 13 illustrated
  stories, and **22 briefs** (stories 14–35) beside it, each ending
  with its source: 35 stories in total, across seven regions
  (Europe 6, Americas 8, Asia-Pacific 8, Mideast 5, Africa 5,
  Oceania 1, World/Space 2).
- Every claim carries its source on the page, and the DATE CHECK
  strip names what was deliberately kept off a page about the 21st
  because it was first reported earlier: the missiles down in Poland,
  Wall Street's fall into correction, the UK–EU reset deals and the
  Kyiv bridges barrage (all Friday 20 November), plus the Shenzhen
  summit, Anthropic's IPO and the ICJ Myanmar verdict (Thursday 19
  November).

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
