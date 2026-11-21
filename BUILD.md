# How this entry was built

**When and for what:** built on Saturday 21 November 2026
(Asia/Jakarta) for make.fun's `news-image-20261121` bounty, whose brief
is to sum up that one day's world news in a single image. This is the
second edition (v2), built the same evening to widen the first
edition's 26 stories after studying the day's live top entries.

**The deliverable** is `entry.png`: 1024×1024, a PNG well under the
1 MiB cap, deterministic — build it twice and the bytes match, run
`main.ts` twice and the copies match.

**Counting the stories.** The page carries 39: leads 01–03, features
04–15, briefs 16–39. The region bar (Europe 8, Americas 9,
Asia-Pacific 9, Mideast 4, Africa 5, Oceania 1, World/Space 3) adds up
to the same 39, and `build_poster.py` asserts that agreement, plus the
six-number strip and the fifteen map pins, before it draws anything.

**What changed in v2.** The first edition's three leads stay, drawn
denser: the Poland panel gains a village with a church spire, hay
bales, smoke plumes and a locator inset with the south-east corner
lit; the crash chart gains volume bars and a fall scale; the quake
panel widens to Sulawesi, Papua and the Timor arc. COP31 and Peru are
promoted into taller illustrated bands and Kyiv joins them as a new
illustrated module, alongside two further new illustrated features
(the Lebanon peace push and Trump's defund-Ukraine call) and
eleven more briefs (Haiti, China's tech investment, Leapmotor,
WeRide, the continuing US outages, Senegal's migrant boat, Kenya's
floods, Egypt's IMF deal, the quake felt in Timor-Leste, Somalia's
expulsion of the UAE ambassador, Zelenskyy at APEC) take the page
from six regions to seven and from 26 stories to 39.

**Attribution.** Sources sit on the poster itself, per story: AP and
Horizon for Poland, AP for Kyiv, Horizon for the market close, BMKG
(with USGS/GFZ magnitudes) for the quake, and wire/EU Council/UN
News/Telegraph/BBC attributions elsewhere. Iran's drone shoot-down
is labelled as Iran's claim. The DATE CHECK strip keeps 19/20
November's headlines (Shenzhen summit, Anthropic IPO, ICJ Myanmar
verdict) off the page.

**The look** deliberately follows the maker's Friday poster
(world-in-one-day-20261120, officially rated 0.987731): cream
newsprint, dark-navy ink and panels, a red headline banner and a black
source chip inside every panel, full-width lead art, one drawn band
per feature, a solid-fill world map, and the thin date-check strip.

**Rebuild commands**

```sh
python3 poster/build_poster.py   # re-renders entry.png at the root
node main.ts                      # delivers it to the output folder
```

Fonts are the system Liberation family; nothing is fetched and no
clock or randomness is read, which is what makes the output
reproducible. Should a future render exceed 1 MiB, the builder falls
back to a 224-colour palette quantise so the file always fits.
