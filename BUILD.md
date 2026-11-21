# How this entry was built

**When and for what:** built on Saturday 21 November 2026
(Asia/Jakarta) for make.fun's `news-image-20261121` bounty, whose brief
is to sum up that one day's world news in a single image.

**The deliverable** is `entry.png`: 1024×1024, a PNG well under the
1 MiB cap, deterministic — build it twice and the bytes match, run
`main.ts` twice and the copies match.

**Counting the stories.** The page carries 26: leads 01–03, features
04–13, briefs 14–26. The region bar (Europe 6, Americas 7,
Asia-Pacific 7, Mideast 3, Africa 1, World/Space 2) adds up to the
same 26, and `build_poster.py` asserts that agreement, plus the
six-number strip and the thirteen map pins, before it draws anything.

**Attribution.** Sources sit on the poster itself, per story: AP and
Horizon for Poland, Horizon for the market close, BMKG (with USGS/GFZ
magnitudes) for the quake, and wire/EU Council/UN News attributions
elsewhere. Iran's drone shoot-down is labelled as Iran's claim. The
DATE CHECK strip keeps 19/20 November's headlines (Shenzhen summit,
Anthropic IPO, ICJ Myanmar verdict) off the page.

**The look** deliberately follows the maker's Friday poster
(world-in-one-day-20261120, officially rated 0.987731): cream
newsprint, dark-navy ink and panels, a red headline banner and a black
source chip inside every panel, full-width lead art, one drawn band
per feature, a solid-fill world map, and the thin date-check strip.
Saturday's art is new: farmland at night with missile trails and a
falling drone; a crash chart with all four index falls printed in it;
a Banda Sea panel with epicentre rings, a seismograph trace, an
"M7.2 · 125 KM" badge and a green "NO TSUNAMI" tag.

**Rebuild commands**

```sh
python3 poster/build_poster.py   # re-renders entry.png at the root
node main.ts                      # delivers it to the output folder
```

Fonts are the system Liberation family; nothing is fetched and no
clock or randomness is read, which is what makes the output
reproducible. Should a future render exceed 1 MiB, the builder falls
back to a 224-colour palette quantise so the file always fits.
