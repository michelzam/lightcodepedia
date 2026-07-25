/*!
 * BDD non-regression suite for @karmicsoft/lc-map.  Run: node test.mjs
 */
import { MAP_VERSION, markers, bounds, center, view } from './index.js';
import assert from 'node:assert';

let scen = 0, fail = 0;
function feature(n) { console.log('\nFeature: ' + n); }
function scenario(n, fn) { scen++; try { fn(); console.log('  ✓ ' + n); } catch (e) { fail++; console.log('  ✗ ' + n + '\n      ' + (e.message || e)); } }
const ok = assert.ok, eq = assert.strictEqual, deep = assert.deepStrictEqual;

const PARIS = { lat: 48.8566, lon: 2.3522, label: 'Paris' };
const LYON = { lat: 45.7640, lng: 4.8357, label: 'Lyon' };     // note: lng

feature('Points are normalized, and junk is dropped rather than plotted');
scenario('lng and lon both work; output is always lon', () => {
  const m = markers([PARIS, LYON]);
  eq(m.length, 2); eq(m[1].lon, 4.8357); eq(m[1].label, 'Lyon');
});
scenario('a point without finite coordinates is DROPPED, not placed at (0,0)', () => {
  eq(markers([{ label: 'nowhere' }, { lat: 'x', lon: 2 }, null, PARIS]).length, 1);
});
scenario('out-of-range coordinates are refused', () => {
  eq(markers([{ lat: 99, lon: 0 }, { lat: 0, lon: 999 }]).length, 0);
});
scenario('a label falls back to title, then slug, then empty', () => {
  eq(markers([{ lat: 1, lon: 1, title: 'T' }])[0].label, 'T');
  eq(markers([{ lat: 1, lon: 1, slug: 's' }])[0].label, 's');
  eq(markers([{ lat: 1, lon: 1 }])[0].label, '');
});

feature('Bounds and centre describe where to look');
scenario('bounds is the tightest box over every point', () => {
  deep(bounds([PARIS, LYON]), { north: 48.8566, south: 45.764, east: 4.8357, west: 2.3522 });
});
scenario('centre is the box centre, so one outlier cannot drag the view', () => {
  const c = center([{ lat: 0, lon: 0 }, { lat: 10, lon: 10 }, { lat: 10, lon: 10 }]);
  eq(c.lat, 5); eq(c.lon, 5);          // an average would have said 6.67
});
scenario('no points → no bounds, no centre (the host shows its empty state)', () => {
  eq(bounds([]), null); eq(center([]), null); eq(bounds(null), null);
});

feature('view() is the whole model in one call');
{
  const v = view([PARIS, LYON], { width: 640, height: 400 });
  scenario('it carries markers, bounds, centre and a zoom', () => {
    eq(v.empty, false); eq(v.markers.length, 2); ok(v.bounds && v.center);
    ok(Number.isInteger(v.zoom) && v.zoom >= 0 && v.zoom <= 18);
  });
  scenario('a wider spread zooms further OUT than a tight one', () => {
    const tight = view([PARIS, { lat: 48.86, lon: 2.36 }]);
    ok(tight.zoom > v.zoom);
  });
  scenario('a bigger viewport fits the same box at a HIGHER zoom', () => {
    ok(view([PARIS, LYON], { width: 1600, height: 1200 }).zoom >= v.zoom);
  });
  scenario('a single point gets pointZoom — a box with no size implies no zoom', () => {
    eq(view([PARIS]).zoom, 14);
    eq(view([PARIS], { pointZoom: 11 }).zoom, 11);
  });
  scenario('maxZoom is respected even for a single point', () => {
    eq(view([PARIS], { pointZoom: 18, maxZoom: 12 }).zoom, 12);
  });
  scenario('an empty set is explicitly empty, never a fake centre', () => {
    const e = view([]);
    eq(e.empty, true); eq(e.center, null); eq(e.zoom, null); deep(e.markers, []);
  });
}

feature('The brick announces its version');
scenario('MAP_VERSION is exposed', () => ok(/^\d+\.\d+$/.test(MAP_VERSION)));

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
