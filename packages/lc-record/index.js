/*!
 * @karmicsoft/lc-record — the headless record engine.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * The BRAIN of a record editor, with no DOM and no framework: given a schema
 * (lc-schema IR or a flat field list), a record, and a relation index, it
 * answers what the host should render and how an edit changes the record.
 * Pedia renders the answers as `.record`; another host renders them its way.
 *
 *   schema + record + index
 *        │
 *        ├─ controls()   what to render (field controls, values, options)
 *        ├─ relTitle/relMatch()  relation display + type-ahead
 *        ├─ geoPoints()  which points are mappable
 *        ├─ setValue/addItem/removeItem()  mutations (+ is it structural?)
 *        └─ emit()       the WRITE PATH — full-file re-emit
 *
 * Write strategy is deliberately **full-file re-emit**, not surgical patching:
 * measured on a 44k-file corpus the re-emit drift is ≈1%, and a whole-file
 * write can never interleave a partial edit into a half-parsed file.
 */
import { load, dump, leadingComments } from '@karmicsoft/lc-serialize';

export const ENGINE_VERSION = '0.1';

const isArr = Array.isArray;
const isObj = (v) => v !== null && typeof v === 'object' && !isArr(v);

// ── 1. Schema reconciliation ───────────────────────────────────────────────
// One engine, three shapes of input — so a host can hand us whatever it has:
//   • an lc-schema IR            → { irVersion, collections: [...] }  (+ name)
//   • one IR collection          → { name, fields: [...] }
//   • a flat field list          → [ {name, widget, ...}, ... ]  (what `.record` ships today)
/** Normalize any accepted schema shape to the flat field list the engine uses. */
export function fields(schema, collectionName) {
  if (!schema) return [];
  if (isArr(schema)) return schema;                                   // already flat
  if (isArr(schema.fields)) return schema.fields;                     // one IR collection
  if (isArr(schema.collections)) {                                    // a whole IR
    const c = collectionName
      ? schema.collections.find((x) => x.name === collectionName)
      : schema.collections[0];
    if (!c) throw new Error(`lc-record: collection "${collectionName}" not in this IR`);
    return c.fields || [];
  }
  throw new Error('lc-record: unrecognized schema — pass an lc-schema IR, an IR collection, or a field array');
}

// ── 2. Controls — what the host should render ──────────────────────────────
/**
 * Describe the controls for a record. Pure data: no DOM, no callbacks. Each
 * control carries everything a renderer needs, including the current `value`
 * and, for relations, the resolved `chips` (so a host never re-implements the
 * index lookup). Unknown widgets degrade to a string control rather than
 * vanishing — a field you can't type is worse than a plain input.
 */
export function controls(schema, record, index, collectionName) {
  const list = fields(schema, collectionName), rec = record || {}, idx = index || {};
  return list.map((f) => control(f, rec[f.name], idx));
}

function control(f, value, index) {
  const base = {
    name: f.name,
    label: f.label || f.name,
    widget: f.widget || 'string',
    value: value === undefined ? undefined : value,
    required: f.required !== false,
  };
  if (f.hint) base.hint = f.hint;
  if (f.default !== undefined) base.default = f.default;

  switch (base.widget) {
    case 'select':
      base.multiple = !!f.multiple;
      base.options = f.options || [];
      return base;
    case 'relation': {
      base.collection = f.collection;
      base.multiple = !!f.multiple;
      const slugs = base.multiple ? (isArr(value) ? value : []) : (value == null ? [] : [value]);
      base.chips = slugs.map((s) => ({ slug: s, title: relTitle(index, f.collection, s) }));
      return base;
    }
    case 'object':
      base.fields = (f.fields || []).map((c) => control(c, isObj(value) ? value[c.name] : undefined, index));
      return base;
    case 'objectlist': {
      const items = isArr(value) ? value : [];
      base.itemFields = f.fields || [];
      // one control set PER item, so a host renders N rows without re-deriving
      base.items = items.map((it) => (f.fields || []).map((c) => control(c, isObj(it) ? it[c.name] : undefined, index)));
      return base;
    }
    case 'list':
      base.item = f.item || { name: 'value', widget: 'string' };
      base.items = isArr(value) ? value : [];
      return base;
    default:
      if (!['string', 'text', 'number', 'boolean', 'markdown', 'image', 'file', 'hidden'].includes(base.widget)) {
        base.widget = 'string';          // never drop a field we don't recognise
        base.degraded = true;
      }
      return base;
  }
}

// ── 3. Relations ───────────────────────────────────────────────────────────
/** Display title for a slug in `index[coll]`; falls back to the slug itself. */
export function relTitle(index, coll, slug) {
  const a = (index && index[coll]) || [];
  for (const e of a) if (e && e.slug === slug) return e.title || slug;
  return slug;
}
const norm = (s) => {
  s = String(s == null ? '' : s).toLowerCase().trim();
  return s.normalize ? s.normalize('NFD').replace(/[̀-ͯ]/g, '') : s;
};
/**
 * Type-ahead over the index: prefix matches first, then substring, accent- and
 * case-insensitive, already-picked slugs excluded. Capped (default 8).
 */
export function relMatch(index, coll, query, exclude, limit) {
  const a = (index && index[coll]) || [], n = norm(query), ex = exclude || [];
  if (!n) return [];
  const starts = [], incl = [];
  for (const p of a) {
    if (!p || ex.indexOf(p.slug) !== -1) continue;
    const t = norm(p.title), s = String(p.slug || '');
    if (t.indexOf(n) === 0 || s.indexOf(n) === 0) starts.push(p);
    else if (t.indexOf(n) !== -1 || s.indexOf(n) !== -1) incl.push(p);
  }
  return starts.concat(incl).slice(0, limit || 8);
}

// ── 4. Geo extraction ──────────────────────────────────────────────────────
function collectSlugs(v, out) {
  if (v == null) return;
  if (typeof v === 'string') { out[v] = 1; return; }
  if (isArr(v)) { for (const x of v) collectSlugs(x, out); return; }
  if (isObj(v)) for (const k of Object.keys(v)) collectSlugs(v[k], out);
}
/**
 * Every index entry that has coordinates AND whose slug appears anywhere in the
 * record — at any depth, under any key. The index owns the coordinates, so this
 * works for any record shape (person.addresses, event.location.points…) with no
 * per-record configuration. `lng` and `lon` are both accepted on input; the
 * output is normalized to `{ lat, lon, label }`.
 */
export function geoPoints(record, index) {
  const used = {}; collectSlugs(record, used);
  const pts = [];
  for (const coll of Object.keys(index || {})) {
    for (const e of (index[coll] || [])) {
      const lng = e && (e.lng != null ? e.lng : e.lon);
      if (e && e.lat != null && lng != null && used[e.slug]) {
        pts.push({ lat: e.lat, lon: lng, label: e.title || e.slug });
      }
    }
  }
  return pts;
}

// ── 5. Mutations ───────────────────────────────────────────────────────────
// Every mutation reports whether it was STRUCTURAL (the control set changed —
// the host must rebuild its form) or a value edit (re-render the preview only,
// so a caret is never lost mid-typing). That distinction is the whole reason
// the editor feels stable while typing.
function walk(record, path) {
  const parts = isArr(path) ? path.slice() : String(path).split('.');
  let node = record;
  for (let i = 0; i < parts.length - 1; i++) {
    const k = parts[i], nk = parts[i + 1];
    if (node[k] == null) node[k] = /^\d+$/.test(nk) ? [] : {};
    node = node[k];
  }
  return { node, key: parts[parts.length - 1] };
}
/** Set a value at a dotted path ("title", "daterange.startDay", "addresses.0.role"). */
export function setValue(record, path, value) {
  const rec = record || {}, { node, key } = walk(rec, path);
  node[key] = value;
  return { record: rec, structural: false };
}
/** Append to the list at `path` (creating it when absent). Structural. */
export function addItem(record, path, item) {
  const rec = record || {}, { node, key } = walk(rec, path);
  if (!isArr(node[key])) node[key] = [];
  node[key].push(item);
  return { record: rec, structural: true };
}
/** Remove index `i` from the list at `path`. Structural. */
export function removeItem(record, path, i) {
  const rec = record || {}, { node, key } = walk(rec, path);
  if (isArr(node[key])) node[key].splice(i, 1);
  return { record: rec, structural: true };
}

// ── 6. Round-trip & the write path ─────────────────────────────────────────
/**
 * Parse a file into `{ record, keys, leading }` — `keys` is the record's own
 * key order (emit replays it, so a save is a minimal git diff) and `leading` is
 * the provenance comment block, preserved byte-identically.
 */
export function parse(text) {
  const src = String(text == null ? '' : text);
  const record = load(src) || {};
  return { record, keys: Object.keys(record), leading: leadingComments(src) };
}
/**
 * The WRITE PATH: re-emit the WHOLE file. Not a surgical patch — a full-file
 * write can't interleave a partial edit, and the measured drift is ≈1%.
 * Pass the `keys`/`leading` from parse() to keep order and provenance.
 */
export function emit(record, opts = {}) {
  return dump(record || {}, { order: opts.keys || null, leading: opts.leading || '' });
}
/**
 * Did the edit drop any key that was in the file? Honest, cheap, and the thing
 * a user actually fears. `{ ok, preserved, lost, lostKeys }`.
 */
export function integrity(record, originalKeys) {
  const rec = record || {}, keys = originalKeys || [];
  const lostKeys = keys.filter((k) => !Object.prototype.hasOwnProperty.call(rec, k));
  return { ok: lostKeys.length === 0, preserved: keys.length - lostKeys.length, lost: lostKeys.length, lostKeys };
}
