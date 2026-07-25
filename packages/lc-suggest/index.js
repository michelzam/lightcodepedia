/*!
 * @karmicsoft/lc-suggest — headless suggestion engine.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * "It suggests, you decide." This brick proposes edits to a record and never
 * performs one: nothing here mutates anything until a host calls apply() with
 * a suggestion a human accepted.
 *
 * A suggestion is DATA, never a closure — `{ id, kind, text, field, value }`.
 * That is the whole design: the same shape survives a JSON round-trip, so a
 * local generator and a remote AI endpoint are indistinguishable to the host,
 * and one Apply button handles both.
 *
 *   suggest(schema, record, index)      → local, domain-agnostic proposals
 *   payload(schema, record)             → the body to POST to an AI endpoint
 *   normalize(remote)                   → coerce ANY endpoint answer to our shape
 *   apply(record, suggestion)           → the accepted edit (via lc-record)
 */
import { fields, relMatch, setValue } from '@karmicsoft/lc-record';

export const SUGGEST_VERSION = '0.1';

const isArr = Array.isArray;
const isEmpty = (v) => v == null || (typeof v === 'string' && !v.trim()) || (isArr(v) && !v.length);
const norm = (s) => {
  s = String(s == null ? '' : s).toLowerCase();
  return s.normalize ? s.normalize('NFD').replace(/[̀-ͯ]/g, '') : s;
};
const PROSE = ['markdown', 'text', 'string'];

/** Collect the record's free text, so generators can read what the author wrote. */
function prose(record, list) {
  const out = [];
  for (const f of list) {
    const v = record[f.name];
    if (typeof v === 'string' && PROSE.includes(f.widget || 'string')) out.push(v);
  }
  return out.join('\n');
}

/**
 * Local, domain-agnostic proposals — the fallback when no AI endpoint is set,
 * and a useful floor even when one is.
 *
 *  • `stub`    a required or prose field is empty → offer a placeholder to fill
 *  • `relate`  the record's text names something in the index that isn't linked
 *              yet → offer the link (this is the one that earns its keep)
 *
 * opts: { kinds:['stub','relate'], limit=8 }
 */
export function suggest(schema, record, index, opts = {}) {
  const list = fields(schema, opts.collection), rec = record || {}, idx = index || {};
  const kinds = opts.kinds || ['stub', 'relate'];
  const out = [];

  if (kinds.includes('stub')) {
    for (const f of list) {
      const v = rec[f.name], w = f.widget || 'string';
      if (!isEmpty(v)) continue;
      if (!(f.required !== false || w === 'markdown' || w === 'text')) continue;
      if (['relation', 'object', 'objectlist', 'list', 'hidden'].includes(w)) continue;
      const label = f.label || f.name;
      out.push({
        id: 'stub:' + f.name, kind: 'stub', field: f.name,
        value: 'TODO: ' + label + '.',
        text: '“' + label + '” is empty → insert a stub to fill in',
        reason: 'empty ' + (f.required !== false ? 'required field' : 'prose field'),
      });
    }
  }

  if (kinds.includes('relate')) {
    const text = prose(rec, list);
    if (text.trim()) {
      for (const f of list) {
        if ((f.widget || '') !== 'relation' || !f.collection) continue;
        const already = f.multiple ? (isArr(rec[f.name]) ? rec[f.name] : []) : (rec[f.name] == null ? [] : [rec[f.name]]);
        for (const e of (idx[f.collection] || [])) {
          if (!e || !e.title || already.indexOf(e.slug) !== -1) continue;
          if (norm(text).indexOf(norm(e.title)) === -1) continue;
          out.push({
            id: 'relate:' + f.name + ':' + e.slug, kind: 'relate', field: f.name,
            value: f.multiple ? already.concat([e.slug]) : e.slug,
            text: 'The text mentions “' + e.title + '” → link it under “' + (f.label || f.name) + '”',
            reason: 'title found in the record’s text, not yet linked',
          });
        }
      }
    }
  }

  return out.slice(0, opts.limit == null ? 8 : opts.limit);
}

/** Type-ahead over the index for a relation field — the manual counterpart of `relate`. */
export function candidates(index, collection, query, exclude, limit) {
  return relMatch(index, collection, query, exclude, limit);
}

/** The request body for a remote AI endpoint — one contract, so hosts agree. */
export function payload(schema, record, opts = {}) {
  return { record: record || {}, schema: fields(schema, opts.collection), suggestVersion: SUGGEST_VERSION };
}

/**
 * Coerce whatever an endpoint returned into our suggestion shape. Endpoints are
 * third-party and drift; a bad answer must degrade to "no suggestions", never
 * throw into the host's render loop. Items with no applicable edit are dropped.
 */
export function normalize(remote) {
  const list = isArr(remote) ? remote : (remote && isArr(remote.suggestions) ? remote.suggestions : []);
  return list.reduce((out, s, i) => {
    if (!s || typeof s !== 'object') return out;
    const field = s.field || s.name;
    if (!field || s.value === undefined) return out;      // nothing we could apply
    out.push({
      id: s.id || 'remote:' + field + ':' + i,
      kind: s.kind || 'remote',
      field,
      value: s.value,
      text: s.text || s.label || ('Set “' + field + '”'),
      reason: s.reason || 'from the AI endpoint',
    });
    return out;
  }, []);
}

/**
 * Apply an ACCEPTED suggestion. Returns lc-record's `{ record, structural }`,
 * so the host knows whether to rebuild its form. Nothing else in this module
 * touches the record.
 */
export function apply(record, suggestion) {
  if (!suggestion || !suggestion.field) return { record: record || {}, structural: false };
  return setValue(record, suggestion.field, suggestion.value);
}
