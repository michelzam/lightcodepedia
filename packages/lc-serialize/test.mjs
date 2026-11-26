/*!
 * BDD non-regression suite for @karmicsoft/lc-serialize.
 * Zero-dependency: a tiny Feature/Scenario harness over node:assert.
 * Run: node test.mjs   (or `npm test`)
 */
import { load, dump, roundtrip, isByteIdentical, isLossless, leadingComments, splitFrontMatter, formatOf } from './index.js';
import * as lib from './index.js';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert';

let scen = 0, fail = 0;
function feature(name) { console.log('\nFeature: ' + name); }
function scenario(name, fn) {
  scen++;
  try { fn(); console.log('  ✓ ' + name); }
  catch (e) { fail++; console.log('  ✗ ' + name + '\n      ' + (e.message || e)); }
}
const eq = assert.strictEqual, ok = assert.ok, deep = assert.deepStrictEqual;

// A rich fiche in canonical block style (Louise Michel shape).
const fiche = `id: louise-michel
slug: louise-michel
type: person
title: Louise Michel
gender: féminin
birth:
  date: 1830-05-29
  year: 1830
  place: Vroncourt-la-Côte
death:
  date: 1905-01-09
professions:
  - institutrice
  - anarchiste
nationalities:
  - France
addresses:
  - id: 24-rue-houdon
    role: résidence
    period: 1871
  - id: cimetiere-de-levallois
    role: mémoire
image:
  src: /fiches/louise-michel.jpg
  credit: BnF · domaine public — Gallica
externalLinks: []
body: |
  Institutrice et militante anarchiste.

  Surnommée « la Vierge rouge ».
workflow:
  draft: false
  aiText: null
`;

feature('A real fiche round-trips with nothing lost');
scenario('Given a canonical block-style fiche, When round-tripped, Then it is byte-identical', () => {
  ok(isByteIdentical(fiche));
});
scenario('And it is semantically lossless', () => ok(isLossless(fiche)));
scenario('And the round-trip is idempotent (a fixpoint)', () => eq(roundtrip(roundtrip(fiche)), roundtrip(fiche)));

feature('Data fidelity — the things a naive YAML lib gets wrong');
scenario('Unquoted dates stay STRINGS (no timestamp→ISO coercion)', () => {
  const o = load('d: 1830-05-29');
  eq(typeof o.d, 'string'); eq(o.d, '1830-05-29');
  ok(!roundtrip(fiche).includes('T00:00:00'));
});
scenario('null is preserved (not dropped, not "null" string)', () => {
  eq(load('a: null').a, null);
  ok(/aiText: null/.test(roundtrip(fiche)));
});
scenario('empty array stays []', () => ok(/externalLinks: \[\]/.test(roundtrip(fiche))));
scenario('key order is preserved (minimal git diffs)', () => {
  eq(dump(load('z: 1\na: 2\nm: 3')).trim(), 'z: 1\na: 2\nm: 3');
});
scenario('nested objects and mixed-shape lists survive', () => {
  deep(load(roundtrip(fiche)).addresses, load(fiche).addresses);
});
scenario('special characters (·, —, «») are preserved', () => {
  ok(roundtrip(fiche).includes('BnF · domaine public — Gallica'));
  ok(roundtrip(fiche).includes('« la Vierge rouge »'));
});

feature('Block-scalar chomping is faithful (| / |- / |+)');
scenario('strip |- keeps NO trailing newline', () => eq(roundtrip('x: |-\n  a\n  b\n'), 'x: |-\n  a\n  b\n'));
scenario('clip | keeps ONE trailing newline', () => eq(roundtrip('x: |\n  a\n  b\n'), 'x: |\n  a\n  b\n'));
scenario('keep |+ keeps trailing blank lines', () => {
  const y = 'x: |+\n  a\n  b\n\n';
  eq(load(roundtrip(y)).x, load(y).x);
});
scenario('the fiche body: | stays | (not coerced to |-)', () => {
  ok(/body: \|\n/.test(roundtrip(fiche)) && !/body: \|-/.test(roundtrip(fiche)));
});

feature('isLossless is the contract; isByteIdentical is advisory');
scenario('flow style is LOSSLESS but drifts to block (advisory, not a failure)', () => {
  const flow = 'tags: [a, b, c]\nmeta: {k: 1}\n';
  ok(isLossless(flow));            // data survives
  ok(!isByteIdentical(flow));      // but it reformats to block
  deep(load(roundtrip(flow)), load(flow));
});
scenario('comments are dropped but data is LOSSLESS (advisory drift)', () => {
  const commented = 'a: 1 # inline note\n# leading note\nb: 2\n';
  ok(isLossless(commented));
  ok(!isByteIdentical(commented)); // the comment is gone → drift, not loss
});

feature('Leading provenance comments survive round-trip byte-identically');
scenario('a "# source:" header + blank line round-trips exactly', () => {
  const src = '# source: xwiki-export 2026-04-05\n# reviewed: no\n\ntitle: A. de Longpré\nbody: président\n';
  ok(isByteIdentical(src));
  ok(roundtrip(src).startsWith('# source: xwiki-export 2026-04-05\n# reviewed: no\n\n'));
});
scenario('leadingComments captures only the leading block (not inline comments)', () => {
  eq(leadingComments('# a\n# b\n\nk: 1\n# not-leading\n'), '# a\n# b\n\n');
  eq(leadingComments('k: 1\n'), '');            // file starts with data → empty
});
scenario('dump(obj) stays pure — no comments unless you pass leading', () => {
  eq(dump({ k: 1 }), 'k: 1\n');
  eq(dump({ k: 1 }, { leading: '# hi\n' }), '# hi\nk: 1\n');
});
scenario('the body is still byte-identical (comments do not disturb data)', () => {
  const src = '# note\nk: 1\nlist:\n  - a\n  - b\n';
  eq(roundtrip(src), src);
});

feature('dump options');
scenario('dump(obj, { order }) applies an explicit key order', () => {
  eq(dump({ a: 1, b: 2, c: 3 }, { order: ['c', 'a', 'b'] }).trim(), 'c: 3\na: 1\nb: 2');
});
scenario('dump(obj) with no order preserves the object’s own order', () => {
  eq(dump({ b: 1, a: 2 }).trim(), 'b: 1\na: 2');
});

feature('Markdown with a YAML header (0.2.0, Toni: the long texts move after the header)');
{
  const md = "---\n# source: xwiki-export\nid: mort-de-segur\ntitle: Mort de la comtesse de Ségur\ndaterange:\n  startYear: 1874\n  startDay: 1874-02-09\n---\n\nLe 9 février 1874, elle s’éteint.\n\nElle est inhumée à Pluneret.\n";
  scenario('the header reads as the record and the text after the fence as body', () => {
    const r = load(md);
    deep(Object.keys(r), ['id', 'title', 'daterange', 'body']);
    eq(r.daterange.startDay, '1874-02-09', 'an unquoted date stays a string in the header');
    eq(r.body, 'Le 9 février 1874, elle s’éteint.\n\nElle est inhumée à Pluneret.');
  });
  scenario('it round-trips byte-identical, provenance comment included', () => {
    eq(roundtrip(md), md); ok(isByteIdentical(md)); ok(isLossless(md));
  });
  scenario('dump(record, { format: "md" }) writes the header, a blank line, the text, a final newline', () => {
    eq(dump({ id: 'x', title: 'T', body: 'Text.' }, { format: 'md' }), '---\nid: x\ntitle: T\n---\n\nText.\n');
    eq(dump({ id: 'x', body: '' }, { format: 'md' }), '---\nid: x\n---\n');
  });
  scenario('a header that also carries a body: key is refused — the text has one home', () => {
    assert.throws(() => load('---\nid: x\nbody: hidden\n---\n\nText\n'), /never in a body: key/);
  });
  scenario('plain YAML reads as before, a lone opening --- marker included', () => {
    eq(formatOf(fiche), 'yaml'); eq(splitFrontMatter('---\nid: x\n'), null); deep(load('---\nid: x\n'), { id: 'x' });
    eq(formatOf(md), 'md');
  });
  scenario('the browser copy keeps a single js-yaml call (gen-includes rewrites exactly one)', () => {
    const src = String(lib.load).length && require_src();
    eq((src.match(/yaml\.load\(/g) || []).length, 1);
  });
  scenario('lc-serialize-check reads .md records beside .yaml, and fails on a refused one', () => {
    const d = mkdtempSync(join(tmpdir(), 'lcs-'));
    writeFileSync(join(d, 'a.yaml'), fiche); writeFileSync(join(d, 'b.md'), md); writeFileSync(join(d, 'README.md'), '# not a record\n');
    const out = execFileSync(process.execPath, [new URL('./check-corpus.mjs', import.meta.url).pathname, d], { encoding: 'utf8' });
    ok(/2 file\(s\) checked/.test(out), out); ok(/1 \.md/.test(out), out); ok(/PASS/.test(out), out);
    writeFileSync(join(d, 'c.md'), '---\nid: x\nbody: hidden\n---\n\nText\n');
    let code = 0; try { execFileSync(process.execPath, [new URL('./check-corpus.mjs', import.meta.url).pathname, d], { stdio: 'pipe' }); } catch (e) { code = e.status; }
    eq(code, 1);
  });
}
{
  const md = "---\n# source: x\nid: x\ntitle: T\n---\n\nLine one.\n\nLine two.\n", crlf = md.replace(/\n/g, '\r\n');
  scenario('a Windows checkout (CRLF) reads the same record, and round-trips without loss', () => {
    deep(load(crlf), load(md)); ok(isLossless(crlf)); eq(roundtrip(crlf), md);
  });
  scenario('lc-serialize-check fails a .md whose header opens and never closes, and takes CRLF records', () => {
    const d = mkdtempSync(join(tmpdir(), 'lcs-'));
    writeFileSync(join(d, 'w.md'), crlf);
    const out = execFileSync(process.execPath, [new URL('./check-corpus.mjs', import.meta.url).pathname, d], { encoding: 'utf8' });
    ok(/1 file\(s\) checked \(1 \.md\)/.test(out), out);
    writeFileSync(join(d, 'open.md'), '---\nid: x\ntitle: never closed\n');
    let code = 0; try { execFileSync(process.execPath, [new URL('./check-corpus.mjs', import.meta.url).pathname, d], { stdio: 'pipe' }); } catch (e) { code = e.status; }
    eq(code, 1);
  });
}
function require_src() { return readFileSync(new URL('./index.js', import.meta.url), 'utf8'); }

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
