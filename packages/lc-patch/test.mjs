/*!
 * BDD non-regression suite for @karmicsoft/lc-patch.
 * Zero-dependency: a tiny Feature/Scenario harness over node:assert.
 * Run: node test.mjs   (or `npm test`)
 *
 * The first feature is a partner's acceptance text, run against seven real
 * records kept in the lab (partners/…, never published); their SHA-256 must
 * match their baseline before anything else is believed. Without them the
 * fixture scenarios are skipped by name and the synthetic ones still run.
 */
import { patch, patchWith, changedLines } from './index.js';
import { load } from '@karmicsoft/lc-serialize';
import assert from 'node:assert';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

let scen = 0, fail = 0;
function feature(name) { console.log('\nFeature: ' + name); }
function scenario(name, fn) {
  scen++;
  try { fn(); console.log('  ✓ ' + name); }
  catch (e) { fail++; console.log('  ✗ ' + name + '\n      ' + (e.message || e)); }
}
const eq = assert.strictEqual, ok = assert.ok, deep = assert.deepStrictEqual;

const HERE = dirname(fileURLToPath(import.meta.url));
const FIX = join(HERE, '..', 'partners', 'bluelion', 'fixtures', 'paris-2026-09-24');
const HAVE_FIX = existsSync(join(FIX, 'baseline.json'));
const baseline = HAVE_FIX ? JSON.parse(readFileSync(join(FIX, 'baseline.json'), 'utf8')) : { fiches: [] };
const fiches = {};
if (HAVE_FIX) for (const dir of ['persons', 'events'])
  for (const f of readdirSync(join(FIX, 'fiches', dir)))
    fiches[f.replace(/\.yaml$/, '')] = readFileSync(join(FIX, 'fiches', dir, f), 'utf8');
const withFixtures = (name, fn) => HAVE_FIX ? scenario(name, fn) : console.log('  – ' + name + ' (skipped: partner fixtures absent)');
const sha256 = (t) => createHash('sha256').update(t, 'utf8').digest('hex');
const clone = (v) => JSON.parse(JSON.stringify(v));
const diffCount = (a, b) => changedLines(a, b).length;

feature('Background: the 7 fixture records are the ones the partner froze');
withFixtures('each fixture matches its SHA-256 in baseline.json', () => {
  eq(baseline.fiches.length, 7);
  for (const b of baseline.fiches) {
    const slug = b.file.replace(/^fiches\/(persons|events)\//, '').replace(/\.yaml$/, '');
    ok(fiches[slug], 'missing fixture ' + slug);
    eq(sha256(fiches[slug]), b.sha256, 'hash drift on ' + slug);
  }
});

feature('A contribution changes only the lines it edits');
for (const slug of Object.keys(fiches)) {
  withFixtures('An untouched fiche is written back byte-identical: ' + slug, () => {
    const r = patchWith(fiches[slug], load(fiches[slug]));
    eq(r.fallback, false, r.reason);
    eq(r.text, fiches[slug]);
    deep(r.changed, []);
  });
}

withFixtures('Editing one field leaves single-quoted scalars untouched', () => {
  const t = fiches['premiere-de-l-iphigenie-de-gluck-dont-le-livret-a-ete'];
  const o = load(t);
  eq(o.workflow.reviewRequested, true);
  o.workflow.reviewRequested = false;
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  eq(diffCount(t, r.text), 1);
  ok(r.text.split('\n').includes("title: 'Gluck révolutionne l''opéra français: première en présence de la cour de son Iphigénie sur texte de Racine'"));
  deep(r.changed, ['workflow.reviewRequested']);
});

withFixtures('Editing one field leaves other quoted values untouched', () => {
  const t = fiches['charles-baudelaire'];
  const o = load(t);
  o.professions = o.professions.map((p) => (p === 'critique' ? 'journaliste' : p));
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  const lines = changedLines(t, r.text);
  eq(lines.length, 1);
  eq(r.text.split('\n')[lines[0]], '  - journaliste');
  eq(t.split('\n')[lines[0]], '  - critique');
  const note = t.split('\n').find((l) => l.startsWith('  reviewNote:'));
  ok(note.startsWith('  reviewNote: "'), 'the fixture note is double-quoted');
  ok(r.text.split('\n').includes(note), 'the reviewNote line changed, quotes included');
  deep(r.changed, ['professions[2]']);
});

withFixtures('The provenance comment at the top is kept', () => {
  const t = fiches['4eme-siege-de-la-maison-d-edition-gallimard'];
  const o = load(t);
  o.body = 'Le siège de la NRF, où passèrent Camus, Desnos et Éluard.';
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  eq(r.text.split('\n')[0], '# source: xwiki-export 2026-04-05 (migrate-events) arr:7');
  eq(diffCount(t, r.text), 1);
  deep(load(r.text), o);
});

withFixtures('Legacy XWiki links survive an edit elsewhere in the body', () => {
  const t = fiches['charles-baudelaire'];
  const o = load(t);
  ok(o.body.includes('Il a été l’un des premiers'));
  o.body = o.body.replace('Il a été l’un des premiers', 'Il fut l’un des premiers');
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  ok(r.text.includes('[[Verlaine|paul-verlaine.WebHome]]'));
  ok(r.text.includes('[[cimetière du Montparnasse|doc:cimetiere-du-montparnasse.WebHome]]'));
  ok(!r.text.includes('\\[\\['), 'a [[ was escaped');
  eq(diffCount(t, r.text), 1);
  deep(load(r.text), o);
});

withFixtures('Every edit stays lossless', () => {
  const edits = {
    'louise-michel': (o) => { o.addresses[0].role = 'école communale'; o.aka = ['La Vierge rouge']; },
    'nicolas-de-condorcet': (o) => { o.qualificatifs = ['républicain', 'girondin', 'philosophe']; o.body += '\n\nAjout.'; },
    'charles-baudelaire': (o) => { delete o.sortName; o.death.place = 'Paris'; },
    'surrealistes': (o) => { o.externalLinks.push({ label: 'Centre Pompidou', url: 'https://www.centrepompidou.fr/' }); },
    '4eme-siege-de-la-maison-d-edition-gallimard': (o) => { o.daterange.endYear = 1946; o.people.push('jean-paulhan'); },
    'premiere-de-l-iphigenie-de-gluck-dont-le-livret-a-ete': (o) => { o.location.points[1].note = 'Palais-Royal'; },
    'universite-fondee-apres-l-affaire-dreyfus-par-des-bourgeois-liberaux': (o) => { o.daterange = { startYear: 1899, precision: 'year' }; },
  };
  for (const slug of Object.keys(edits)) {
    const t = fiches[slug], o = load(t), before = clone(o);
    edits[slug](o);
    const r = patchWith(t, o);
    eq(r.fallback, false, slug + ': ' + r.reason);
    deep(load(r.text), o, slug + ' is not lossless');
    ok(!deepEq(load(r.text), before), slug + ': the edit did not land');
  }
});

feature('Only the edited lines move — the reader keeps everything else');
withFixtures('An added key lands at the end of its mapping, in lc-serialize style', () => {
  const t = fiches['louise-michel'];
  const o = load(t);
  o.aka = ['La Vierge rouge'];
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  const ls = r.text.split('\n');
  eq(ls[ls.length - 3], 'aka:');
  eq(ls[ls.length - 2], '  - La Vierge rouge');
  eq(diffCount(t, r.text.split('\n').slice(0, -3).join('\n') + '\n'), 0);
  deep(r.changed, ['aka (added)']);
});

withFixtures('A removed key takes only its own lines with it', () => {
  const t = fiches['charles-baudelaire'];
  const o = load(t);
  delete o.sortName;
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  eq(t.split('\n').length - r.text.split('\n').length, 1);
  ok(!r.text.includes('sortName:'));
  deep(r.changed, ['sortName (removed)']);
});

withFixtures('A field inside a list item changes only that line', () => {
  const t = fiches['louise-michel'];
  const o = load(t);
  o.addresses[0].period = 1871;
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  const lines = changedLines(t, r.text);
  eq(lines.length, 1);
  eq(r.text.split('\n')[lines[0]], '    period: 1871');
  deep(r.changed, ['addresses[0].period']);
});

withFixtures('A list that grows keeps its old items verbatim and appends the new one', () => {
  const t = fiches['4eme-siege-de-la-maison-d-edition-gallimard'];
  const o = load(t);
  o.people.push('jean-paulhan');
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  eq(diffCount(t, r.text.replace('  - jean-paulhan\n', '')), 0);
  ok(r.text.includes('  - max-jacob\n  - jean-paulhan\nbibliography:'));
});

withFixtures('An empty list that fills up is re-emitted as a block list', () => {
  const t = fiches['nicolas-de-condorcet'];
  const o = load(t);
  o.bibliography = [{ id: 'badinter-1988' }];
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  ok(r.text.includes('bibliography:\n  - id: badinter-1988\nexternalLinks:'));
  deep(load(r.text), o);
});

withFixtures('CRLF files stay CRLF', () => {
  const t = fiches['surrealistes'].replace(/\n/g, '\r\n');
  const o = load(t);
  o.gender = 'collectif';
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  ok(!/[^\r]\n/.test(r.text), 'a bare LF appeared');
  eq(diffCount(t, r.text), 1);
  deep(load(r.text), o);
});

scenario('A list at the key\'s own indent is understood', () => {
  const t = 'id: x\ntags:\n- a\n- b\nbody: ""\n';
  const o = load(t);
  o.tags[1] = 'c';
  const r = patchWith(t, o);
  eq(r.fallback, false, r.reason);
  eq(r.text, 'id: x\ntags:\n- a\n- c\nbody: ""\n');
});

scenario('A shape the reader does not know falls back to a full re-emit, and says so', () => {
  const t = '- just\n- a list\n';
  const r = patchWith(t, { a: 1 });
  eq(r.fallback, true);
  ok(r.reason.length > 0);
  deep(load(r.text), { a: 1 });
});

scenario('The fallback is still lossless and keeps the provenance block', () => {
  const t = '# provenance\n? [complex, key]\n: value\n';
  const r = patchWith(t, { a: 1 });
  eq(r.fallback, true);
  ok(r.text.startsWith('# provenance\n'));
  deep(load(r.text), { a: 1 });
});

function deepEq(a, b) { return JSON.stringify(sortDeep(a)) === JSON.stringify(sortDeep(b)); }
function sortDeep(v) {
  if (Array.isArray(v)) return v.map(sortDeep);
  if (v && typeof v === 'object') { const o = {}; for (const k of Object.keys(v).sort()) o[k] = sortDeep(v[k]); return o; }
  return v;
}

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
