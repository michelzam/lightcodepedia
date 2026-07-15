/*!
 * @karmicsoft/lc-schema — schema → neutral IR → widget definitions.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * SSOT strategy: keep ONE canonical schema and generate the rest. This is a
 * small "schema compiler": a reader turns your canonical source into a neutral
 * IR; the lc-* editor (and other back-ends) consume the IR. Swapping the
 * canonical source later changes only the reader — consumers are unaffected.
 *
 * v0.1 ships the Sveltia/Decap `config.yml` reader (config is already in your
 * repo). A Zod reader + projections (config.yml, JSON Schema) can be added
 * without touching consumers — see README § SSOT.
 */
import yaml from 'js-yaml';

export const IR_VERSION = '0.1';

// Sveltia/Decap widget → neutral IR widget.
const WIDGET = {
  string: 'string', text: 'text', number: 'number', boolean: 'boolean',
  select: 'select', relation: 'relation', list: 'list', object: 'object',
  markdown: 'markdown', image: 'image', file: 'file', hidden: 'hidden',
  datetime: 'string', code: 'text',
};

/** Parse a Sveltia/Decap config.yml (string or object) into the neutral IR. */
export function fromSveltiaConfig(config) {
  const cfg = typeof config === 'string' ? yaml.load(config, { schema: yaml.CORE_SCHEMA }) : config;
  if (!cfg || !Array.isArray(cfg.collections)) throw new Error('lc-schema: not a Sveltia/Decap config (missing collections[])');
  return { irVersion: IR_VERSION, source: 'sveltia', collections: cfg.collections.map(mapCollection) };
}

function mapCollection(c) {
  return {
    name: c.name,
    label: c.label || c.name,
    folder: c.folder,
    extension: c.extension || 'yaml',
    identifier: c.identifier_field || 'title',
    slug: c.slug,
    fields: (c.fields || []).map(mapField),
  };
}

function mapField(f) {
  let w = WIDGET[f.widget] || 'string';
  const out = { name: f.name, label: f.label || prettify(f.name), widget: w };
  out.required = f.required !== false;
  if (f.hint) out.hint = f.hint;
  if (f.default !== undefined) out.default = f.default;

  if (w === 'select') {
    out.multiple = !!f.multiple;
    out.options = (f.options || []).map((o) =>
      (o && typeof o === 'object') ? { label: o.label ?? String(o.value), value: o.value }
                                   : { label: String(o), value: o });
  } else if (w === 'relation') {
    out.collection = f.collection;
    out.multiple = !!f.multiple;
    out.valueField = f.value_field || '{{slug}}';
    out.displayField = firstOf(f.display_fields) || firstOf(f.search_fields) || 'title';
    out.searchFields = asArray(f.search_fields);
  } else if (w === 'list') {
    if (Array.isArray(f.fields)) { out.widget = 'objectlist'; out.fields = f.fields.map(mapField); }
    else out.item = f.field ? mapField(f.field) : { name: 'value', widget: 'string' };
  } else if (w === 'object') {
    out.fields = (f.fields || []).map(mapField);
  }
  return out;
}

/** Flat widget list for the editor, for one collection. */
export function widgets(ir, collectionName) {
  const c = ir.collections.find((c) => c.name === collectionName);
  if (!c) throw new Error(`lc-schema: unknown collection "${collectionName}"`);
  return c.fields;
}

/** All collection names in the IR. */
export function collections(ir) { return ir.collections.map((c) => c.name); }

// ── Zod reader ─────────────────────────────────────────────────────────────
// Compile runtime Zod schemas (Astro's content collections) into the SAME IR.
// Version-tolerant: keys off constructor.name (stable across Zod 3 and 4) with
// forgiving accessors for the internals that moved between majors.
//
//   import { fromZod } from '@karmicsoft/lc-schema';
//   import { collections as astro } from './src/content.config.ts';
//   const ir = fromZod(astro);            // { persons: {schema}, events: {schema} } or { persons: z.object(...) }
//
// Relations: Astro's reference('periods') doesn't expose its target at runtime,
// so mark it with .describe('relation:periods') (single) — a z.array of that is
// a multiple relation. .describe('markdown'|'image'|'text') pick those widgets.

/** Compile a map (or array) of Zod object schemas into the neutral IR. */
export function fromZod(schemas, opts = {}) {
  const labels = opts.labels || {};
  const entries = isArr(schemas)
    ? schemas.map((c) => [c.name, c.schema || c])
    : Object.keys(schemas).map((n) => [n, schemas[n]]);
  return {
    irVersion: IR_VERSION,
    source: 'zod',
    collections: entries.map(([name, raw]) => ({
      name,
      label: labels[name] || prettify(name),
      fields: zShapeFields(raw),
    })),
  };
}

function zCtor(s) { return (s && s.constructor && s.constructor.name) || ''; }
function zDesc(s) { return (s && (s.description || (s._def && s._def.description))) || ''; }

function zResolveObject(raw) {
  let o = raw && raw.schema !== undefined ? raw.schema : raw;   // Astro collection → its .schema
  if (typeof o === 'function') throw new Error('lc-schema.fromZod: a schema is a function (uses image()) — call it / pass the resolved z.object');
  return o;
}
function zShapeFields(raw) {
  const o = zResolveObject(raw);
  if (!o || !o._def) return [];
  let sh = o.shape !== undefined ? o.shape : o._def.shape;
  if (typeof sh === 'function') sh = sh();
  return sh ? Object.keys(sh).map((n) => zField(n, sh[n])) : [];
}

// Peel Optional / Nullable / Default / Effects|Pipe, tracking required + default.
function zUnwrap(schema) {
  let s = schema, required = true, def;
  for (let i = 0; i < 16 && s && s._def; i++) {
    const k = zCtor(s);
    if (k === 'ZodOptional' || k === 'ZodNullable') { required = false; s = s._def.innerType; }
    else if (k === 'ZodDefault' || k === 'ZodPrefault') { const dv = s._def.defaultValue; def = typeof dv === 'function' ? dv() : dv; required = false; s = s._def.innerType; }
    else if (k === 'ZodEffects') { s = s._def.schema; }
    else if (k === 'ZodPipe' || k === 'ZodPipeline') { s = s._def.out || s._def.in; }
    else break;
  }
  return { base: s, required, def, desc: zDesc(schema) || zDesc(s) };
}
function zEnumOptions(s) {
  const v = (s && s.options) || (s._def && (s._def.values || (s._def.entries && Object.values(s._def.entries)))) || [];
  return isArr(v) ? v : Object.values(v);
}
function zArrayElement(s) { return s._def && (s._def.element || s._def.type); }

function zField(name, schema) {
  const u = zUnwrap(schema), s = u.base, kind = zCtor(s), desc = u.desc;
  const out = { name, label: prettify(name), widget: 'string', required: u.required };
  if (u.def !== undefined) out.default = u.def;

  // description conventions win
  const rel = /relation:([A-Za-z0-9_-]+)/.exec(desc);
  if (rel) { out.widget = 'relation'; out.collection = rel[1]; if (kind === 'ZodArray') out.multiple = true; return out; }
  const d = desc.toLowerCase();
  if (/\bmarkdown\b/.test(d)) { out.widget = 'markdown'; return out; }
  if (/\bimage\b/.test(d)) { out.widget = 'image'; return out; }
  if (/\btext\b/.test(d)) { out.widget = 'text'; return out; }

  if (kind === 'ZodString' || kind === 'ZodLiteral' || kind === 'ZodDate') out.widget = 'string';
  else if (kind === 'ZodNumber' || kind === 'ZodBigInt') out.widget = 'number';
  else if (kind === 'ZodBoolean') out.widget = 'boolean';
  else if (kind === 'ZodEnum' || kind === 'ZodNativeEnum') { out.widget = 'select'; out.options = zEnumOptions(s).map((v) => ({ label: String(v), value: v })); }
  else if (kind === 'ZodObject') { out.widget = 'object'; out.fields = zShapeFields(s); }
  else if (kind === 'ZodArray') {
    const elem = zArrayElement(s), eu = zUnwrap(elem), erel = /relation:([A-Za-z0-9_-]+)/.exec(eu.desc);
    if (erel) { out.widget = 'relation'; out.collection = erel[1]; out.multiple = true; }
    else if (zCtor(eu.base) === 'ZodObject') { out.widget = 'objectlist'; out.fields = zShapeFields(eu.base); }
    else { out.widget = 'list'; out.item = zField('value', elem); out.multiple = true; }
  }
  return out;
}

const isArr = Array.isArray;
function firstOf(a) { return isArr(a) ? a[0] : a; }
function asArray(a) { return isArr(a) ? a : (a == null ? [] : [a]); }
function prettify(s) { return String(s || '').replace(/[-_]/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase()); }
