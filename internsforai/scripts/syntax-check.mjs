// Syntax-check every Pages Function + helper module.
// Pure ESM; uses dynamic import to surface parse errors.
import { readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const ROOT = new URL("..", import.meta.url).pathname;
const TARGETS = [
  "functions/_lib",
  "functions/api"
];

function walk(dir, acc = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const s = statSync(p);
    if (s.isDirectory()) walk(p, acc);
    else if (p.endsWith(".js") || p.endsWith(".mjs")) acc.push(p);
  }
  return acc;
}

let errors = 0;
for (const t of TARGETS) {
  const dir = join(ROOT, t);
  for (const f of walk(dir)) {
    try {
      await import(pathToFileURL(f).href);
      console.log("ok    " + f.replace(ROOT, ""));
    } catch (e) {
      // Only syntax / parse errors count; runtime errors (like missing globals on import) are ok.
      if (e instanceof SyntaxError) {
        errors++;
        console.error("FAIL  " + f.replace(ROOT, "") + " :: " + e.message);
      } else {
        // Cloudflare globals (crypto.subtle, etc.) may not exist in plain node — that's fine.
        console.log("ok*   " + f.replace(ROOT, "") + "  (runtime-only: " + (e && e.message ? e.message.slice(0, 60) : e) + ")");
      }
    }
  }
}
if (errors) { console.error("\n" + errors + " syntax error(s)."); process.exit(1); }
else console.log("\nAll modules parsed cleanly.");
