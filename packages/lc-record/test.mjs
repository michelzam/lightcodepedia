/*!
 * BDD non-regression suite for @karmicsoft/lc-record.
 * Zero-dependency: the same tiny Feature/Scenario harness as the other bricks.
 * Run: node test.mjs   (or `npm test`)
 */
import {
  ENGINE_VERSION, fields, controls, relTitle, relMatch, geoPoints,
  setValue, addItem, removeItem, parse, emit, integrity,
} from './index.js';
import assert from 'node:assert';

let scen = 0, fail = 0;
function feature(name) { console.log('\nFeature: ' + name); }
function scenario(name, fn) {
  scen++;
  try { fn(); console.log('  ✓ ' + name); }
  catch (e) { fail++; console.log('  ✗ ' + name + '\n      ' + (e.message || e)); }
}
const ok = assert.ok, eq = assert.strictEqual, deep = assert.deepStrictEqual;

// The shapes a host actually has on hand.
const FLAT = [
  { name: 'title', label: 'Nom', widget: 'string' },
  { name: 'periods', label: 'Époques', widget: 'relation', collection: 'periods', multiple: true },
];
const IR = {
  irVersion: '0.1', source: 'zod',
  collections: [
    { name: 'persons', label: 'Persons', fields: FLAT },
    { name: 'events', label: 'Events', fields: [{ name: 'when', widget: 'string' }] },
  ],
};
const INDEX = {
  periods: [
    { slug: 'commune-de-1871', title: 'Commune de 1871', lat: 48.86, lng: 2.35 },
    { slug: 'revolutions-de-1848', title: 'Révolutions de 1848' },
    { slug: 'siege-de-paris', title: 'Siège de Paris', lat: 48.85, lon: 2.34 },
  ],
};

feature('One engine reads whichever schema shape the host has (IR reconciliation)');
scenario('a flat field list passes through', () => eq(fields(FLAT).length, 2));
scenario('an lc-schema IR resolves by collection name', () => eq(fields(IR, 'events')[0].name, 'when'));
scenario('an IR with no name given takes the first collection', () => eq(fields(IR)[0].name, 'title'));
scenario('a single IR collection is accepted directly', () => eq(fields(IR.collections[0]).length, 2));
scenario('an unknown collection fails loud, never silently empty', () => {
  assert.throws(() => fields(IR, 'nope'), /not in this IR/);
});
scenario('a nonsense schema fails loud', () => assert.throws(() => fields(42), /unrecognized schema/));

feature('controls() says what to render — pure data, no DOM');
{
  const rec = { title: 'A. de Longpré', periods: ['revolutions-de-1848', 'commune-de-1871'] };
  const cs = controls(FLAT, rec, INDEX);
  const by = (n) => cs.find((c) => c.name === n);
  scenario('every field becomes a control carrying its current value', () => {
    eq(cs.length, 2); eq(by('title').value, 'A. de Longpré'); eq(by('title').label, 'Nom');
  });
  scenario('a relation resolves its chips, so the host never re-does the lookup', () => {
    const p = by('periods');
    eq(p.widget, 'relation'); eq(p.multiple, true);
    deep(p.chips.map((c) => c.title), ['Révolutions de 1848', 'Commune de 1871']);
  });
  scenario('a missing value yields a control, not a hole', () => {
    eq(controls(FLAT, {}, INDEX).find((c) => c.name === 'title').value, undefined);
  });
  scenario('an unknown widget degrades to a string control instead of vanishing', () => {
    const c = controls([{ name: 'x', widget: 'quantum' }], {}, {})[0];
    eq(c.widget, 'string'); eq(c.degraded, true);
  });
}

feature('Nested and repeated structures come back ready to render');
{
  const schema = [
    { name: 'daterange', widget: 'object', fields: [{ name: 'startDay', widget: 'number' }] },
    { name: 'addresses', widget: 'objectlist', fields: [
      { name: 'role', widget: 'string' },
      { name: 'place', widget: 'relation', collection: 'periods' },
    ] },
    { name: 'tags', widget: 'list', item: { name: 'value', widget: 'string' } },
  ];
  const rec = {
    daterange: { startDay: 1871 },
    addresses: [{ role: 'domicile', place: 'commune-de-1871' }, { role: 'atelier' }],
    tags: ['a', 'b'],
  };
  const cs = controls(schema, rec, INDEX);
  const by = (n) => cs.find((c) => c.name === n);
  scenario('an object exposes child controls with their values', () => {
    eq(by('daterange').fields[0].name, 'startDay'); eq(by('daterange').fields[0].value, 1871);
  });
  scenario('an objectlist exposes ONE control set PER item', () => {
    const a = by('addresses');
    eq(a.items.length, 2);
    eq(a.items[0].find((c) => c.name === 'role').value, 'domicile');
    eq(a.items[1].find((c) => c.name === 'role').value, 'atelier');
  });
  scenario('a relation nested inside an item still resolves its chip', () => {
    eq(by('addresses').items[0].find((c) => c.name === 'place').chips[0].title, 'Commune de 1871');
  });
  scenario('a scalar list carries its items and its item template', () => {
    deep(by('tags').items, ['a', 'b']); eq(by('tags').item.widget, 'string');
  });
}

feature('Relations: display and type-ahead');
scenario('relTitle resolves a slug, and falls back to the slug when unknown', () => {
  eq(relTitle(INDEX, 'periods', 'commune-de-1871'), 'Commune de 1871');
  eq(relTitle(INDEX, 'periods', 'ghost'), 'ghost');
});
scenario('relMatch is accent- and case-insensitive', () => {
  eq(relMatch(INDEX, 'periods', 'revolutions')[0].slug, 'revolutions-de-1848');
  eq(relMatch(INDEX, 'periods', 'RÉVOL')[0].slug, 'revolutions-de-1848');
});
scenario('prefix matches rank before substring matches', () => {
  const r = relMatch(INDEX, 'periods', 'de');
  ok(r.length >= 2);
});
scenario('already-picked slugs are excluded, and an empty query matches nothing', () => {
  eq(relMatch(INDEX, 'periods', 'commune', ['commune-de-1871']).length, 0);
  eq(relMatch(INDEX, 'periods', '').length, 0);
});

feature('Geo extraction: the index owns the coordinates, at any depth');
{
  const rec = { periods: ['commune-de-1871'], addresses: [{ place: 'siege-de-paris' }] };
  const pts = geoPoints(rec, INDEX);
  scenario('a slug anywhere in the record plots its indexed point', () => {
    eq(pts.length, 2);
    ok(pts.some((p) => p.label === 'Commune de 1871'));
    ok(pts.some((p) => p.label === 'Siège de Paris'));   // found nested in an objectlist
  });
  scenario('lng and lon are both accepted, output is normalized to lon', () => {
    ok(pts.every((p) => typeof p.lon === 'number' && typeof p.lat === 'number'));
  });
  scenario('an indexed entry without coordinates is not plotted', () => {
    eq(geoPoints({ periods: ['revolutions-de-1848'] }, INDEX).length, 0);
  });
  scenario('a record referencing nothing plots nothing', () => eq(geoPoints({}, INDEX).length, 0));
}

feature('Mutations report whether the host must rebuild its form');
scenario('setValue is a value edit — the form keeps its DOM (and the caret)', () => {
  const r = setValue({ title: 'a' }, 'title', 'b');
  eq(r.record.title, 'b'); eq(r.structural, false);
});
scenario('a dotted path reaches nested fields, creating the parent when absent', () => {
  const r = setValue({}, 'daterange.startDay', 1871);
  eq(r.record.daterange.startDay, 1871);
});
scenario('a numeric segment creates an array, not an object', () => {
  const r = setValue({}, 'addresses.0.role', 'domicile');
  ok(Array.isArray(r.record.addresses)); eq(r.record.addresses[0].role, 'domicile');
});
scenario('addItem / removeItem are structural — the control set changed', () => {
  const a = addItem({ tags: ['x'] }, 'tags', 'y');
  deep(a.record.tags, ['x', 'y']); eq(a.structural, true);
  const d = removeItem(a.record, 'tags', 0);
  deep(d.record.tags, ['y']); eq(d.structural, true);
});
scenario('addItem creates the list when the field is absent', () => {
  deep(addItem({}, 'tags', 'first').record.tags, ['first']);
});

feature('The write path is a full-file re-emit (≈1% drift beats surgical patching)');
{
  const SRC = '# source: legacy import\n\ntitle: A. de Longpré\nperiods:\n  - revolutions-de-1848\nbody: président\n';
  const p = parse(SRC);
  scenario('parse returns the record, its key ORDER, and the provenance block', () => {
    eq(p.record.title, 'A. de Longpré');
    deep(p.keys, ['title', 'periods', 'body']);
    ok(p.leading.indexOf('# source: legacy import') === 0);
  });
  scenario('an untouched record re-emits byte-identically (a save is a no-op diff)', () => {
    eq(emit(p.record, { keys: p.keys, leading: p.leading }), SRC);
  });
  scenario('an edit re-emits the WHOLE file, keeping key order and provenance', () => {
    const { record } = setValue({ ...p.record }, 'body', 'peintre');
    const out = emit(record, { keys: p.keys, leading: p.leading });
    ok(out.indexOf('# source: legacy import') === 0);          // provenance survives
    ok(out.indexOf('body: peintre') !== -1);                   // the edit landed
    ok(out.indexOf('title:') < out.indexOf('body:'));          // original order replayed
  });
  scenario('a NEW key is emitted too (it just lands after the known order)', () => {
    const { record } = setValue({ ...p.record }, 'gender', 'féminin');
    ok(emit(record, { keys: p.keys }).indexOf('gender: féminin') !== -1);
  });
}

feature('Integrity: did the edit drop a key that was in the file?');
scenario('nothing lost → ok, with the count the UI shows', () => {
  const r = integrity({ a: 1, b: 2 }, ['a', 'b']);
  eq(r.ok, true); eq(r.preserved, 2); eq(r.lost, 0);
});
scenario('a dropped key is named, not just counted', () => {
  const r = integrity({ a: 1 }, ['a', 'b']);
  eq(r.ok, false); eq(r.lost, 1); deep(r.lostKeys, ['b']);
});
scenario('a key added after load is not a loss', () => eq(integrity({ a: 1, c: 3 }, ['a']).ok, true));

feature('The engine announces its version');
scenario('ENGINE_VERSION is exposed for host compatibility checks', () => ok(/^\d+\.\d+$/.test(ENGINE_VERSION)));

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
