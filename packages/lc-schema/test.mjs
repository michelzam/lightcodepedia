import { fromSveltiaConfig, widgets, collections } from './index.js';
import { readFileSync } from 'node:fs';
import assert from 'node:assert';

const ir = fromSveltiaConfig(readFileSync(new URL('./example.config.yml', import.meta.url), 'utf8'));
let pass = 0;
const ok = (n, c) => { assert.ok(c, n); console.log('  ✓ ' + n); pass++; };

ok('collections detected', collections(ir).includes('persons'));
const w = widgets(ir, 'persons');
const by = (n) => w.find((f) => f.name === n);

ok('string widget', by('title').widget === 'string');
ok('select carries options', by('gender').widget === 'select' && by('gender').options.some((o) => o.value === 'féminin'));
ok('list of scalars → list', by('professions').widget === 'list' && by('professions').item.widget === 'string');
ok('relation multiple', by('periods').widget === 'relation' && by('periods').multiple === true && by('periods').collection === 'periods');
ok('list of objects → objectlist with nested relation', by('addresses').widget === 'objectlist' &&
   by('addresses').fields.find((f) => f.name === 'id').widget === 'relation');
ok('markdown widget', by('body').widget === 'markdown');

console.log(`\n${pass} checks passed.`);
