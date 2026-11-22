// news-image-20261122 round-2 entry point.
// Copies the pre-rendered entry.png into the grader's output directory
// and verifies the copy byte-for-byte, so a bad copy can never pass silently.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const here = resolve(import.meta.dirname);
const source = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);

const a = readFileSync(source);
const b = readFileSync(target);
if (a.length !== b.length || !a.equals(b)) {
  throw new Error("entry.png copy mismatch: bytes differ after copy");
}
console.log(`entry.png copied to ${target} (${a.length} bytes, verified)`);
