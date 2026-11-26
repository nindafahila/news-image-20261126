// Tai Po Fire — make.fun news-image-20261126 entry.
//
// Entry point: runs draw_entry.py (the Pillow program that draws the
// 1024x1024 newspaper front page) and writes the result to
// $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
// Node 22, stdlib only. The drawing is fully deterministic, so running
// this twice produces byte-identical PNGs.

import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const script = join(here, "draw_entry.py");

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outFile = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });

if (!existsSync(script)) {
  console.error(`draw_entry.py not found next to main.ts: ${script}`);
  process.exit(1);
}

execFileSync("python3", [script, outFile], { stdio: "inherit" });
console.log(`wrote ${outFile}`);
