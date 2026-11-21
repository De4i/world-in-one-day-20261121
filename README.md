# Saturday 21 November 2026 — the world in one day, in one image

Entry for make.fun's daily news-image bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121)
("Sum up 21 November's world news in one image", $100, 50 paid places):

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

## What the picture shows

A single 1024×1024 front page for Saturday 21 November 2026, second
edition (v2: broader and denser than the morning's first edition):

- **Three illustrated leads** — Russian missiles and a drone down in
  south-east Poland, with a locator inset; the global tech-stock crash
  (Nasdaq −5.3%, S&P 500 −3.7%, Nikkei −5.1%, Hang Seng −1.9%); and the
  M7.2 Maluku quake in the Banda Sea (BMKG; no tsunami), drawn across a
  wider archipelago.
- **Twelve feature modules**, each with its own drawn graphic: COP31
  deadlocked into overtime and Peru's M6.9 in taller promoted bands,
  the Kyiv strikes, the Basra power-plant fire, the FBI/Agriculture
  hack, the UK–EU deals, Iran's MQ-9 claim, Bayer's $7.25bn settlement,
  Europe's Lebanon peace push, Trump's AI data-centre tax warning,
  Tbilisi's blast, and Trump's "defund Ukraine" call to Europe.
- **A world map** with a numbered pin for every lead and feature, and
  **24 briefs** (stories 16–39) beside it: 39 stories in total, across
  seven regions (Europe 8, Americas 9, Asia-Pacific 9, Mideast 4,
  Africa 5, Oceania 1, World/Space 3).
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
