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

const isArr = Array.isArray;
function firstOf(a) { return isArr(a) ? a[0] : a; }
function asArray(a) { return isArr(a) ? a : (a == null ? [] : [a]); }
function prettify(s) { return String(s || '').replace(/[-_]/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase()); }
