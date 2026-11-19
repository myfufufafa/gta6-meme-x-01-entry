// Entry program for the gta6-meme-x-01 bounty.
//
// All it does is carry the post address from this repository into the
// grader's output folder: it reads POST.json next to this file and writes
// an identical copy to MAKEFUN_OUTPUT_DIR/POST.json.
//
// Configuration comes from the environment, with the grader's defaults:
//   MAKEFUN_BOT_DIR    - folder holding POST.json (default "/bot")
//   MAKEFUN_OUTPUT_DIR - folder the copy is written to (default "/output")
// No network, no clock, no files outside those two folders.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir: string = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

try {
  const source = join(botDir, "POST.json");
  const raw = readFileSync(source, "utf8");
  const parsed: unknown = JSON.parse(raw);
  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)
    || typeof (parsed as { url?: unknown }).url !== "string") {
    throw new Error(`${source} must be a JSON object with a string "url"`);
  }
  mkdirSync(outputDir, { recursive: true });
  writeFileSync(join(outputDir, "POST.json"), raw);
} catch (error) {
  const reason = error instanceof Error ? error.message : String(error);
  console.error(`failed to copy POST.json: ${reason}`);
  process.exit(1);
}
