// World in One Day, Saturday edition, v5 — news-image-20261121.
//
// Saturday 21 November 2026 in one image, 35 stories. The picture is
// baked ahead of time: poster/build_poster.py renders entry.png from
// poster/data/stories.json, and entry.png sits beside this file in the
// repository. All this program does at run time is deliver that file.
// The v5 edition leads with COP31 in overtime, the Saudi interception
// of three Houthi missiles over Riyadh and the M6.7 Peru quake, and
// moves Friday 20 November's biggest stories (Poland, Wall Street,
// the UK-EU deals, the Kyiv bridges barrage) into its DATE CHECK
// strip, where they are named as exclusions, not as Saturday's news.
//
// Delivery address: the folder named by MAKEFUN_OUTPUT_DIR, falling
// back to /output when the variable is unset. The folder is created
// when missing. Node standard library only, and the transfer is a
// straight byte copy, so two runs hand over exactly the same bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const baked = join(repoDir, "entry.png");

const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(destDir, { recursive: true });

const dest = join(destDir, "entry.png");
copyFileSync(baked, dest);

console.log(`world-in-one-day-20261121: entry.png delivered to ${dest}`);
