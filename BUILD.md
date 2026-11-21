# How this entry was built

**When and for what:** built on Saturday 21 November 2026
(Asia/Jakarta) for make.fun's `news-image-20261121` bounty, whose brief
is to sum up that one day's world news in a single image. This is the
fourth edition (v4). The first edition (26 stories) scored dev rate
0.985964; a denser second edition (39 stories, 15 illustrated modules)
scored clearly worse at 0.972784; a third restored the first edition's
page with six more briefs (32 stories). For v4 the live top 10 of the
board was read image by image, and their shared pattern was followed:
every one of the ten carries 30–36 stories with exactly 13
illustrated modules (3 leads + 10 features), a six-number strip, a
seven-region bar, a map pinned for the illustrated stories only,
one-line briefs that end with their source, and COP31 plus the
Ukraine war among the leads.

**The deliverable** is `entry.png`: 1024×1024, a PNG well under the
1 MiB cap, deterministic — build it twice and the bytes match, run
`main.ts` twice and the copies match.

**Counting the stories.** The page carries 35: leads 01–03, features
04–13, briefs 14–35. The region bar (Europe 8, Americas 8,
Asia-Pacific 6, Mideast 4, Africa 5, Oceania 1, World/Space 3) adds
up to the same 35, and `build_poster.py` asserts that agreement, plus
the six-number strip and the thirteen map pins, before it draws
anything.

**What changed in v4.** The lead slots now carry the topics the
top 10 lead with, drawn from this page's own verified pool: COP31 in
overtime (new pale-panel art: globe, thermometer, clock), the Kyiv
strikes (new night-skyline art with missile trails) and Peru's M6.9
(new ridge-and-seismograph art). The first edition's leads — Poland,
the markets crash, the Maluku quake — stay on the page as features
04–06 with their own drawn bands. Zelenskyy's APEC line, Trump's
defund-Ukraine call, the Lebanon peace push, China's tech FDI rise
and the Timor-Leste quake-felt report join the briefs; the briefs now
print their sources in parentheses, and the numbers strip prints all
six numerals in red. Layout geometry, fonts, panel sizes, the map
and the DATE CHECK strip are unchanged from the earlier editions.

**Attribution.** Sources sit on the poster itself, per story: UN
News/Reuters for COP31, AP for Kyiv, USGS for Peru, AP and Horizon
for Poland, Horizon for the market close, BMKG (with USGS/GFZ
magnitudes) for Maluku, and wire/EU Council/BBC/UK Telegraph
attributions elsewhere. Iran's drone shoot-down is labelled as
Iran's claim. The DATE CHECK strip keeps 19/20 November's headlines
(Shenzhen summit, Anthropic IPO, ICJ Myanmar verdict) off the page.

**The look** follows the same family as the maker's Friday poster
(world-in-one-day-20261120, officially rated 0.987731) and the day's
top finishers: cream newsprint, dark-navy ink and panels, a red
headline banner and a black source chip inside every illustrated
panel, full-width lead art, one drawn band per feature, a solid-fill
world map, and the thin date-check strip.

**Rebuild commands**

```sh
python3 poster/build_poster.py   # re-renders entry.png at the root
node main.ts                      # delivers it to the output folder
```

Fonts are the system Liberation family; nothing is fetched and no
clock or randomness is read, which is what makes the output
reproducible. Should a future render exceed 1 MiB, the builder falls
back to a 224-colour palette quantise so the file always fits.
