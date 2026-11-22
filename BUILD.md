# How this entry was built

**When and for what:** built for make.fun's `news-image-20261121`
bounty (sum up Saturday 21 November 2026's world news in one image);
the v5 edition was built on Sunday 22 November 2026 (Asia/Jakarta),
before the Monday 07:00 WIB close. Edition history: v1 (26 stories)
scored dev rate 0.985964; v2 (39 stories, 15 illustrated modules)
scored clearly worse at 0.972784; v3 restored v1's page with six more
briefs (32 stories) and was never submitted; v4 followed the live
top 10's shared architecture (35 stories, exactly 13 illustrated)
and scored 0.981793. Comparing the provisional rates with the house
error rule, only v2's drop is beyond the intervals: density past
about 35 stories / 13 illustrated modules measurably hurts, while
v1's layout and v4's architecture are statistically
indistinguishable. So v5 changes the content, not the page plan.

**What changed in v5.** A full re-verification of the day against
primary reporting (Reuters, AP, ISW, WSJ, AFP, ESA, CAAP):

- **Riyadh joins the leads.** Reuters reported on Saturday that the
  Saudi-led coalition had intercepted and destroyed three Houthi
  ballistic missiles fired towards Riyadh early that morning, the
  second attack on the capital in a few days. Every top-10 page led
  with it; ours never had it. New night-skyline art with three
  incoming trails and interceptor bursts.
- **Four stories move to DATE CHECK.** AP and ISW date the missiles
  down in Poland to Friday 20 November; AP and the WSJ date Wall
  Street's fall into correction (S&P 500 −3.7%, Nasdaq −5.3%) to the
  same Friday; Le Monde and The Times date the UK–EU reset deals to
  Friday's Brussels summit; CNN and Reuters date the Kyiv bridges
  barrage to the night into Friday. All four are now named in the
  DATE CHECK strip as Fri 20 Nov exclusions instead of being shown
  as Saturday's news.
- **Ukraine stays illustrated, told straight.** The Kryvyi Rih
  feature now reads as it happened: Friday's missile strike on a
  restaurant area (a boy of 7 and a paramedic killed), drones
  striking rescuers overnight, the toll of 2 dead and about 60
  injured as reported on Saturday (AP). The separate Kyiv attack
  early on Saturday (homes ablaze in Podil, two hurt, Ukrinform)
  appears as brief 34.
- **Peru corrected.** USGS: 00:09 UTC Saturday (19:09 Friday local),
  34 km north of Junín, 108 km deep, first read 6.9 and revised to
  6.7; felt in Lima; no damage or casualties immediately reported.
  The badge and headline now say M6.7 and the caption drops v4's
  unsupported "buildings and roads hit".
- **Two verified Saturday stories take the freed feature slots:**
  Air Niugini PX19's emergency landing at Davao just after midnight
  on an engine fire warning, all 146 aboard safe (AP via CAAP), and
  BepiColombo's arrival in orbit at Mercury (ESA). New drawn bands
  for both (jet with slides deployed; cratered planet and probe).
- **Numbers strip rebuilt from Saturday facts only:** 13 (COP31
  day), 3 (missiles over Riyadh), M6.7 (Peru), 146 (Davao), 124*
  (Rahul at Wellington, with brief 33 on the page), $7.25bn (Bayer).
  Friday's −5.3% Nasdaq cell is gone.
- **Typography:** lead and feature headlines are now set in serif
  bold, the pattern on seven of the live top ten; the date headline
  was already serif. Dead art functions for the retired Poland,
  markets and UK–EU modules were removed.

**The deliverable** is `entry.png`: 1024×1024, a PNG well under the
1 MiB cap, deterministic — build it twice and the bytes match, run
`main.ts` twice and the copies match.

**Counting the stories.** The page carries 35: leads 01–03, features
04–13, briefs 14–35. The region bar (Europe 6, Americas 8,
Asia-Pacific 8, Mideast 5, Africa 5, Oceania 1, World/Space 2) adds
up to the same 35, and `build_poster.py` asserts that agreement,
plus the six-number strip and the thirteen map pins, before it
draws anything.

**Attribution.** Sources sit on the poster itself, per story:
UN News/Reuters for COP31, Reuters for Riyadh, USGS for Peru, AP
for Kryvyi Rih, BMKG for Maluku, AP/CAAP for Davao, ESA for
BepiColombo, and wire attributions elsewhere. Iran's drone
shoot-down is labelled as Iran's claim. The DATE CHECK strip keeps
19/20 November's headlines off the page and says why.

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
