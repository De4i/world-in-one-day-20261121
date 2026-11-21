# Build notes

- **Built:** Saturday 21 November 2026 (Asia/Jakarta), for the make.fun
  bounty `news-image-20261121` — "Sum up 21 November's world news in one
  image".
- **Deliverable:** `entry.png`, a 1024×1024 PNG (≤ 1,048,576 bytes),
  copied to the output directory by `main.ts` (Node, standard library
  only). Two runs of `main.ts` produce byte-identical output.
- **Story count:** 26 stories — 3 illustrated leads, 10 feature modules,
  and 13 one-line briefs (numbered 14–26). Region counts printed on the
  poster (Europe 6 · Americas 7 · Asia-Pacific 7 · Mideast 3 · Africa 1 ·
  World/Space 2) sum to the same 26 and are asserted against the story
  list at build time.
- **Sources:** AP, Horizon, BMKG, USGS, GFZ, Reuters, UN News and the
  EU Council, as attributed per story on the poster. Claims are
  attributed, not stated as fact (Iran's MQ-9 claim is labelled as a
  claim). A date-check box excludes stories first reported on
  19/20 November (the Shenzhen summit, Anthropic's IPO, the ICJ
  Myanmar verdict).
- **Design:** the same visual system as the maker's
  world-in-one-day-20261120 poster (officially rated 0.987731 there):
  cream newsprint, dark-navy ink, red in-art headline banner and black
  source chip on every panel, full illustrated lead bands, a drawn
  graphic band per feature module, a solid-fill world map with numbered
  pins 1–13, and a thin date-check strip.
- **Artwork:** all original and drawn in code with Pillow shapes — a
  night farmland panel with missile trails and a falling drone for
  Poland, a plunging-lines crash chart with all four index falls for
  the markets lead, and a Banda Sea panel with epicentre rings, a
  seismograph trace and "NO TSUNAMI" tag for the Maluku quake.

## How to re-render

```sh
python3 poster/build_poster.py   # writes entry.png at the repo root
node main.ts                      # copies entry.png to the output dir
```

All poster content lives in `poster/data/stories.json`; all layout and
drawing lives in `poster/build_poster.py`. The render uses only the
system Liberation fonts and is fully deterministic (no randomness, no
network, no timestamps): re-running the build reproduces the same bytes.
If the plain PNG ever exceeds 1 MiB, the build script palette-quantises
it (224 colours, median-cut, Floyd–Steinberg dithering) so the output
always stays within the limit.
