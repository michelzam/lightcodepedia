import { load, dump, roundtrip, isByteIdentical, isLossless } from './index.js';
import assert from 'node:assert';

let pass = 0;
const ok = (name, cond) => { assert.ok(cond, name); console.log('  ✓ ' + name); pass++; };

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

const out = roundtrip(fiche);
ok('dates stay strings (no ...Z)', out.includes('date: 1830-05-29') && !out.includes('T00:00:00'));
ok('null preserved', /aiText: null/.test(out));
ok('mixed-form address list preserved', /- id: 24-rue-houdon/.test(out) && /period: 1871/.test(out) && /- id: cimetiere-de-levallois/.test(out));
ok('special chars ·/— preserved', out.includes('BnF · domaine public — Gallica'));
ok('empty array kept as []', /externalLinks: \[\]/.test(out));
ok('block scalar body: | stays | (not |-)', /body: \|\n/.test(out) && !/body: \|-/.test(out));
ok('byte-identical on canonical source', isByteIdentical(fiche));
ok('semantically lossless', isLossless(fiche));
ok('idempotent (roundtrip is a fixpoint)', roundtrip(out) === out);

// strip case
ok('block | - preserved (no trailing newline)', roundtrip('x: |-\n  a\n  b\n') === 'x: |-\n  a\n  b\n');

console.log(`\n${pass} checks passed.`);
