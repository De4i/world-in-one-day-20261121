// World in One Day, Saturday edition — entry runner for
// news-image-20261121 ("Sum up 21 November's world news in one image").
//
// The poster itself (entry.png, sitting next to this file) is rendered
// ahead of time by poster/build_poster.py from poster/data/stories.json:
// Saturday 21 November 2026 in one image, 26 stories.
// This program's only job is the competition hand-off: place a copy of
// that baked image where the runner expects to find it.
//
// The destination is $MAKEFUN_OUTPUT_DIR when that variable is set, and
// /output otherwise. The directory is created when it does not exist yet.
// Only Node's standard library is used, and the copy is a plain byte
// copy, so running this twice yields two byte-identical outputs.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the folder this file lives in, so the baked image is found
// relative to main.ts itself rather than the caller's working directory.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

// Work out where the runner wants the deliverable, then make sure the
// folder is there before copying into it.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(source, target);

console.log(`world-in-one-day: copied entry.png to ${target}`);
