// news-image-20261126 entry (Node 22, standard library only).
//
// The entry is a single picture: entry.png sits next to this file,
// drawn by draw_entry.py (Python + Pillow) from the verified world
// news of Thursday 26 November 2026. All this program does is copy
// that picture to the output directory, so every run writes the
// exact same bytes: a 1024x1024 PNG of about 120 KB, inside the
// gate's 1 MiB limit.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in
// for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(outDir, "entry.png"),
);
