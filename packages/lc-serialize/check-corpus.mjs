#!/usr/bin/env node
/*!
 * lc-serialize-check — "does any of my files lose data?" over a whole corpus.
 * © KarmicSoft — LightCode.
 *
 *   npx @karmicsoft/lc-serialize lc-serialize-check ./content
 *   node check-corpus.mjs <dir-or-file>        (LC_VERBOSE=1 lists every drift)
 *
 * isLossless (the CONTRACT) must be 0 → exit 1 on any loss (use as a CI gate).
 * isByteIdentical is advisory: a lossless file can still reformat (comments are
 * dropped, flow style {a: 1} / [1, 2] becomes block style) — that is drift, not loss.
 *
 * Markdown with a YAML header (0.2.0): a .md file that opens with a --- header
 * is a record and is checked like the others; a .md without one (a README) is
 * not a record and is left out. A header carrying its own body: key fails.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { isLossless, isByteIdentical, splitFrontMatter } from './index.js';

const root = process.argv[2] || '.';
const EXT = ['.yaml', '.yml', '.md'];

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name.startsWith('.') || name === 'node_modules') continue;
    const p = join(dir, name);
    const s = statSync(p);
    if (s.isDirectory()) walk(p, out);
    else if (EXT.some((e) => name.toLowerCase().endsWith(e))) out.push(p);
  }
  return out;
}

let files;
try {
  files = statSync(root).isDirectory() ? walk(root) : [root];
} catch {
  console.error('path not found: ' + root);
  process.exit(2);
}

let loss = 0, drift = 0, checked = 0, mds = 0, notRecords = 0;
for (const f of files) {
  let src;
  try { src = readFileSync(f, 'utf8'); } catch { continue; }
  if (f.toLowerCase().endsWith('.md')) {
    if (!splitFrontMatter(src)) {
      if (/^---\r?\n/.test(src)) { loss++; console.error('ERROR  ' + f + ' — a header opens with --- and never closes'); continue; }
      notRecords++; continue;                                  // no header at all: not a record (a README)
    }
    mds++;
  }
  checked++;
  try {
    if (!isLossless(src)) { loss++; console.error('LOSS   ' + f); }
    else if (!isByteIdentical(src)) { drift++; if (process.env.LC_VERBOSE) console.warn('drift  ' + f); }
  } catch (e) { loss++; console.error('ERROR  ' + f + ' — ' + e.message); }
}

console.log(`\n${checked} file(s) checked${mds ? ` (${mds} .md)` : ''} · ${loss} data-loss · ${drift} byte-drift (advisory)${notRecords ? ` · ${notRecords} .md without a header left out` : ''}`);
console.log(loss
  ? '❌ FAIL — data would be lost on write-back. Fix before deploying.'
  : '✅ PASS — no data lost' + (drift ? ` (${drift} file(s) reformat only — normalization, not loss).` : '.'));
process.exit(loss ? 1 : 0);
