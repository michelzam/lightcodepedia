/*!
 * BDD non-regression suite for @karmicsoft/lc-suggest.  Run: node test.mjs
 */
import { SUGGEST_VERSION, suggest, candidates, payload, normalize, apply } from './index.js';
import assert from 'node:assert';

let scen = 0, fail = 0;
function feature(n) { console.log('\nFeature: ' + n); }
function scenario(n, fn) { scen++; try { fn(); console.log('  ✓ ' + n); } catch (e) { fail++; console.log('  ✗ ' + n + '\n      ' + (e.message || e)); } }
const ok = assert.ok, eq = assert.strictEqual, deep = assert.deepStrictEqual;

const SCHEMA = [
  { name: 'title', label: 'Nom', widget: 'string', required: true },
  { name: 'body', label: 'Biographie', widget: 'markdown', required: false },
  { name: 'periods', label: 'Époques', widget: 'relation', collection: 'periods', multiple: true },
  { name: 'birthplace', label: 'Lieu', widget: 'relation', collection: 'places' },
];
const INDEX = {
  periods: [
    { slug: 'commune-de-1871', title: 'Commune de 1871' },
    { slug: 'revolutions-de-1848', title: 'Révolutions de 1848' },
  ],
  places: [{ slug: 'montmartre', title: 'Montmartre' }],
};

feature('It suggests — it never acts');
scenario('generating suggestions does not touch the record', () => {
  const rec = { title: '' };
  const before = JSON.stringify(rec);
  suggest(SCHEMA, rec, INDEX);
  eq(JSON.stringify(rec), before);
});
scenario('suggestions are DATA, not closures — they survive JSON', () => {
  const s = suggest(SCHEMA, { title: '' }, INDEX)[0];
  const round = JSON.parse(JSON.stringify(s));
  deep(round, s);                       // a remote endpoint can send exactly this
  eq(typeof s.apply, 'undefined');      // no function to lose across the wire
});

feature('stub: an empty required or prose field offers a placeholder');
{
  const out = suggest(SCHEMA, { title: '', body: '   ' }, INDEX, { kinds: ['stub'] });
  const byField = (f) => out.find((s) => s.field === f);
  scenario('an empty required field is proposed', () => {
    ok(byField('title')); eq(byField('title').kind, 'stub');
    ok(byField('title').text.includes('Nom'));
  });
  scenario('a whitespace-only prose field counts as empty', () => ok(byField('body')));
  scenario('a filled field is NOT proposed', () => {
    eq(suggest(SCHEMA, { title: 'A. de Longpré', body: 'x' }, INDEX, { kinds: ['stub'] }).length, 0);
  });
  scenario('relations and containers are never stubbed', () => {
    ok(!out.some((s) => ['periods', 'birthplace'].includes(s.field)));
  });
}

feature('relate: text that names something in the index offers the link');
{
  const rec = { title: 'A. de Longpré', body: 'Actif pendant la Commune de 1871, puis à Montmartre.' };
  const out = suggest(SCHEMA, rec, INDEX, { kinds: ['relate'] });
  scenario('a mentioned title is proposed for its relation field', () => {
    const s = out.find((x) => x.field === 'periods');
    ok(s); eq(s.kind, 'relate'); deep(s.value, ['commune-de-1871']);
  });
  scenario('a single-valued relation proposes the slug itself, not an array', () => {
    eq(out.find((x) => x.field === 'birthplace').value, 'montmartre');
  });
  scenario('a multiple relation KEEPS what is already linked', () => {
    const o = suggest(SCHEMA, { ...rec, periods: ['revolutions-de-1848'] }, INDEX, { kinds: ['relate'] });
    deep(o.find((x) => x.field === 'periods').value, ['revolutions-de-1848', 'commune-de-1871']);
  });
  scenario('an already-linked entry is not proposed again', () => {
    const o = suggest(SCHEMA, { ...rec, periods: ['commune-de-1871'] }, INDEX, { kinds: ['relate'] });
    ok(!o.some((x) => x.id.endsWith('commune-de-1871')));
  });
  scenario('matching ignores accents and case', () => {
    const o = suggest(SCHEMA, { body: 'les REVOLUTIONS DE 1848' }, INDEX, { kinds: ['relate'] });
    ok(o.some((x) => String(x.id).includes('revolutions-de-1848')));
  });
  scenario('a record with no prose proposes no links', () => {
    eq(suggest(SCHEMA, { periods: [] }, INDEX, { kinds: ['relate'] }).length, 0);
  });
}

feature('A remote endpoint speaks the same shape');
scenario('payload() is the agreed request body', () => {
  const p = payload(SCHEMA, { title: 'x' });
  eq(p.record.title, 'x'); eq(p.schema.length, 4); ok(p.suggestVersion);
});
scenario('normalize() accepts {suggestions:[…]} or a bare array', () => {
  const a = normalize({ suggestions: [{ field: 'title', value: 'A' }] });
  const b = normalize([{ field: 'title', value: 'A' }]);
  eq(a.length, 1); eq(b.length, 1); eq(a[0].field, 'title');
});
scenario('a junk answer degrades to nothing — it never throws at the host', () => {
  eq(normalize(null).length, 0);
  eq(normalize({ oops: true }).length, 0);
  eq(normalize([null, 'nope', { text: 'no field' }, { field: 'f' }]).length, 0);   // no applicable edit
});
scenario('remote items get an id and text when the endpoint omitted them', () => {
  const s = normalize([{ field: 'title', value: 'A' }])[0];
  ok(s.id); ok(s.text.includes('title')); eq(s.kind, 'remote');
});

feature('apply() performs only what a human accepted');
scenario('applying sets the field and reports structural-ness', () => {
  const r = apply({ title: '' }, { field: 'title', value: 'A. de Longpré' });
  eq(r.record.title, 'A. de Longpré'); eq(r.structural, false);
});
scenario('applying a relate suggestion writes the whole list', () => {
  const s = suggest(SCHEMA, { body: 'la Commune de 1871' }, INDEX, { kinds: ['relate'] })[0];
  deep(apply({ body: 'la Commune de 1871' }, s).record.periods, ['commune-de-1871']);
});
scenario('a malformed suggestion changes nothing', () => {
  const rec = { title: 'keep' };
  eq(apply(rec, { value: 'x' }).record.title, 'keep');
  eq(apply(rec, null).record.title, 'keep');
});

feature('candidates() is the manual counterpart of relate');
scenario('it type-aheads over the index', () => {
  eq(candidates(INDEX, 'periods', 'commune')[0].slug, 'commune-de-1871');
});
scenario('SUGGEST_VERSION is exposed', () => ok(/^\d+\.\d+$/.test(SUGGEST_VERSION)));

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
