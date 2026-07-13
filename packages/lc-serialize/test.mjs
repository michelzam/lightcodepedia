/*!
 * BDD non-regression suite for @karmicsoft/lc-serialize.
 * Zero-dependency: a tiny Feature/Scenario harness over node:assert.
 * Run: node test.mjs   (or `npm test`)
 */
import { load, dump, roundtrip, isByteIdentical, isLossless } from './index.js';
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

feature('dump options');
scenario('dump(obj, { order }) applies an explicit key order', () => {
  eq(dump({ a: 1, b: 2, c: 3 }, { order: ['c', 'a', 'b'] }).trim(), 'c: 3\na: 1\nb: 2');
});
scenario('dump(obj) with no order preserves the object’s own order', () => {
  eq(dump({ b: 1, a: 2 }).trim(), 'b: 1\na: 2');
});

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
