/*!
 * BDD non-regression suite for @karmicsoft/lc-schema.
 * Zero-dependency: a tiny Feature/Scenario harness over node:assert.
 * Run: node test.mjs   (or `npm test`)
 */
import { fromSveltiaConfig, widgets, collections, IR_VERSION } from './index.js';
import { readFileSync } from 'node:fs';
import assert from 'node:assert';

let scen = 0, fail = 0;
function feature(name) { console.log('\nFeature: ' + name); }
function scenario(name, fn) {
  scen++;
  try { fn(); console.log('  ✓ ' + name); }
  catch (e) { fail++; console.log('  ✗ ' + name + '\n      ' + (e.message || e)); }
}
const ok = assert.ok, eq = assert.strictEqual;

const ir = fromSveltiaConfig(readFileSync(new URL('./example.config.yml', import.meta.url), 'utf8'));
const w = widgets(ir, 'persons');
const by = (n) => w.find((f) => f.name === n);

feature('A Sveltia config compiles to the neutral IR');
scenario('Given the example config, When compiled, Then the IR carries a version + source', () => {
  eq(ir.irVersion, IR_VERSION); eq(ir.source, 'sveltia');
});
scenario('And its collections are detected', () => ok(collections(ir).includes('persons')));
scenario('And widgets(ir, "persons") returns the field list', () => ok(Array.isArray(w) && w.length >= 6));

feature('Each widget maps to the neutral IR shape the renderer expects');
scenario('string → string', () => eq(by('title').widget, 'string'));
scenario('markdown → markdown', () => eq(by('body').widget, 'markdown'));
scenario('select carries {label, value} options', () => {
  eq(by('gender').widget, 'select');
  ok(by('gender').options.some((o) => o.value === 'féminin' && typeof o.label === 'string'));
});
scenario('relation carries collection + multiple + displayField', () => {
  const p = by('periods');
  eq(p.widget, 'relation'); eq(p.collection, 'periods'); eq(p.multiple, true); eq(p.displayField, 'title');
});
scenario('list of scalars → list with an item descriptor', () => {
  eq(by('professions').widget, 'list'); eq(by('professions').item.widget, 'string');
});
scenario('list of objects → objectlist with nested fields (incl. a nested relation)', () => {
  const a = by('addresses');
  eq(a.widget, 'objectlist');
  eq(a.fields.find((f) => f.name === 'id').widget, 'relation');
});

feature('Robustness');
scenario('required defaults to true unless explicitly false', () => {
  eq(by('title').required, true);       // not specified → required
  eq(by('gender').required, false);     // required: false in config
});
scenario('an object config (not a string) is accepted too', () => {
  const ir2 = fromSveltiaConfig({ collections: [{ name: 'x', fields: [{ name: 'n', widget: 'number' }] }] });
  eq(widgets(ir2, 'x')[0].widget, 'number');
});
scenario('a non-config throws a clear error', () => {
  assert.throws(() => fromSveltiaConfig('not: a config'), /collections/);
});
scenario('an unknown widget falls back to string (never crashes the form)', () => {
  const ir2 = fromSveltiaConfig({ collections: [{ name: 'x', fields: [{ name: 'n', widget: 'totally-unknown' }] }] });
  eq(widgets(ir2, 'x')[0].widget, 'string');
});
scenario('asking for an unknown collection throws', () => {
  assert.throws(() => widgets(ir, 'nope'), /unknown collection/);
});

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
