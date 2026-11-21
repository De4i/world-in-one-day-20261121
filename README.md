# World in One Day — Saturday 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/De4i/world-in-one-day-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One page, one image, one day of world news. This entry sums up Saturday
21 November 2026 as a single 1024×1024 newspaper poster: a masthead with
the date, a strip of the day's biggest numbers, three illustrated lead
stories (Russian missiles and a drone falling in south-east Poland, the
deepening global tech-stock crash, and the M7.2 Maluku quake in the
Banda Sea), ten feature modules with original drawn graphics, a solid
world map with numbered pins, and 13 further stories in brief — 26
stories in all, every claim attributed to its source, plus a date-check
box listing the big stories that were actually first reported on
19/20 November and so do not belong here.

Competition: [make.fun — news-image-20261121](https://make.fun/bounty/news-image-20261121)

## Run

```sh
node main.ts
```

`main.ts` (Node, standard library only) copies the baked `entry.png`
beside it to `$MAKEFUN_OUTPUT_DIR/entry.png`, or to `/output/entry.png`
when the variable is not set, creating the output directory if needed.
The output is byte-identical on every run.

## Rebuild the poster

```sh
python3 poster/build_poster.py
```

That re-renders `entry.png` from `poster/data/stories.json` with Pillow.
See [BUILD.md](BUILD.md) for build notes.

## License

MIT — see [LICENSE](LICENSE).

---
*Entered on make.fun in [news-image-20261121](https://make.fun/bounty/news-image-20261121) by [@De4i](https://make.fun/@De4i).*
