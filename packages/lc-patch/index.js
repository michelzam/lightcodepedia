/*!
 * @karmicsoft/lc-patch — minimal-diff writer for git-backed YAML records.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * lc-serialize re-emits a WHOLE file in its canonical style. That is the right
 * contract for a round-trip, and the wrong one for a reviewer who reads
 * contributions as diffs: editing one field re-quotes an unrelated value
 * ('l''opéra' → "l'opéra") somewhere else in the file. This brick keeps every
 * line the edit did not touch, byte for byte — quoting, flow lists, number
 * formatting, comments, CRLF — and re-emits only the entries that changed,
 * with lc-serialize's own emitter. Nothing is parsed twice, nothing is copied:
 * lc-serialize reads and writes, lc-patch decides which lines to keep.
 *
 * Contract: load(patch(text, edited)) deep-equals `edited`. If the structural
 * reader cannot guarantee that (a YAML shape it does not know), the result
 * is the full re-emit lc-serialize would have produced — never wrong, only
 * less minimal — and `patchWith()` says so.
 */
import { load, dump, leadingComments } from '@karmicsoft/lc-serialize';

export const PATCH_VERSION = '0.1.0';

/** Minimal-diff write: original text + edited object → new text. */
export function patch(originalText, edited, opts = {}) {
  return patchWith(originalText, edited, opts).text;
}

/**
 * Same, with the story: which paths were re-emitted, whether the brick had
 * to fall back to a full re-emit, and why.
 */
export function patchWith(originalText, edited, opts = {}) {
  const src = String(originalText == null ? '' : originalText);
  const crlf = src.indexOf('\r\n') !== -1;
  const text = crlf ? src.replace(/\r\n/g, '\n') : src;
  const leading = leadingComments(text);
  const rest = text.slice(leading.length);
  const changed = [];
  let orig = null, out = '', fallback = false, reason = '';
  try {
    orig = load(text);
    if (!isObj(orig)) throw new Error('the original is not a mapping document');
    if (!isObj(edited)) throw new Error('the edited value is not a mapping');
    const lines = rest.split('\n');
    if (lines.length && lines[lines.length - 1] === '') lines.pop();   // final newline
    const body = patchMap(lines, 0, lines.length, 0, orig, edited, '', changed);
    out = leading + body.join('\n') + '\n';
    if (!deepEqual(load(out), edited)) throw new Error('the patched text does not load back to the edited object');
  } catch (e) {
    fallback = true;
    reason = e && e.message ? e.message : String(e);
    changed.length = 0;
    changed.push('* (full re-emit)');
    out = dump(edited, { leading, order: isObj(orig) ? Object.keys(orig) : null });
  }
  if (crlf) out = out.replace(/\n/g, '\r\n');
  return { text: out, changed, fallback, reason };
}

/** The lines of `text` that would differ from `original` (0-based, in `text`). */
export function changedLines(original, text) {
  const a = String(original).split('\n'), b = String(text).split('\n');
  const out = [];
  for (let i = 0; i < Math.max(a.length, b.length); i++) if (a[i] !== b[i]) out.push(i);
  return out;
}

// ── structural reader: where each entry lives ────────────────────────────
const isArr = Array.isArray;
const isObj = (v) => v && typeof v === 'object' && !isArr(v);
const hasOwn = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
const pad = (n) => ' '.repeat(n);
const indentOf = (l) => /^( *)/.exec(l)[1].length;
const isFiller = (l) => { const t = l.trim(); return t === '' || t[0] === '#'; };
const isDash = (l) => /^ *-( |$)/.test(l);

/* A block mapping at indent `n` inside lines[from, to). Each entry spans from
   its key line to the line before the next key at `n` (filler lines — blank
   or comment — ride with the entry before them). */
function scanMap(lines, from, to, n) {
  const entries = [];
  let i = from;
  while (i < to) {
    const l = lines[i];
    if (isFiller(l)) {
      if (entries.length) entries[entries.length - 1].end = i + 1;
      else entries.push({ key: null, start: i, end: i + 1, inline: undefined });   // filler before the first key
      i++; continue;
    }
    if (indentOf(l) !== n) throw new Error('unexpected indent at line ' + (i + 1));
    if (isDash(l)) throw new Error('a sequence where a mapping was expected, line ' + (i + 1));
    const m = /^ *("(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^\s#][^:]*?):(?: (.*)|$)/.exec(l);
    if (!m) throw new Error('not a key at line ' + (i + 1));
    const key = unquoteKey(m[1]);
    const inline = m[2];                       // undefined → nested block or null
    let j = i + 1;
    while (j < to) {
      const lj = lines[j];
      if (isFiller(lj)) { j++; continue; }
      const ij = indentOf(lj);
      if (ij < n) break;
      if (ij === n) {
        // a sequence may sit at the key's own indent: `key:` then `- item`
        if (inline === undefined && isDash(lj)) { j++; continue; }
        break;
      }
      j++;
    }
    entries.push({ key, start: i, end: j, inline });
    i = j;
  }
  return entries;
}

function unquoteKey(k) {
  if (k[0] === '"') return JSON.parse(k);
  if (k[0] === "'") return k.slice(1, -1).replace(/''/g, "'");
  return k;
}

/* The nested block under a `key:` line: its first content line, its indent,
   its kind, and where its content ends (trailing filler excluded). */
function nestedOf(lines, e) {
  let f = e.start + 1;
  while (f < e.end && isFiller(lines[f])) f++;
  if (f >= e.end) return null;                 // `key:` alone → null value
  let t = e.end;
  while (t > f && isFiller(lines[t - 1])) t--;
  return { from: f, to: t, indent: indentOf(lines[f]), kind: isDash(lines[f]) ? 'seq' : 'map' };
}

/* Items of a block sequence at indent `m` inside lines[from, to). */
function scanSeq(lines, from, to, m) {
  const items = [];
  let i = from;
  while (i < to) {
    const l = lines[i];
    if (isFiller(l)) { if (items.length) items[items.length - 1].end = i + 1; i++; continue; }
    if (indentOf(l) !== m || !isDash(l)) throw new Error('not a sequence item at line ' + (i + 1));
    let j = i + 1;
    while (j < to) {
      const lj = lines[j];
      if (isFiller(lj)) { j++; continue; }
      if (indentOf(lj) <= m) break;
      j++;
    }
    items.push({ start: i, end: j });
    i = j;
  }
  return items;
}

// ── the patch: keep, recurse, or re-emit ─────────────────────────────────
function patchMap(lines, from, to, n, orig, edited, path, changed) {
  const entries = scanMap(lines, from, to, n);
  const out = [], seen = new Set();
  for (const e of entries) {
    if (e.key === null) { out.push(...lines.slice(e.start, e.end)); continue; }
    if (seen.has(e.key)) throw new Error('duplicate key ' + e.key);
    seen.add(e.key);
    const ov = hasOwn(orig, e.key) ? orig[e.key] : undefined;
    if (!hasOwn(edited, e.key)) { changed.push(path + e.key + ' (removed)'); continue; }
    const nv = edited[e.key];
    if (deepEqual(ov, nv)) { out.push(...lines.slice(e.start, e.end)); continue; }
    const nested = e.inline === undefined ? nestedOf(lines, e) : null;
    if (nested && nested.kind === 'map' && isObj(ov) && isObj(nv)) {
      out.push(...lines.slice(e.start, nested.from));
      out.push(...patchMap(lines, nested.from, nested.to, nested.indent, ov, nv, path + e.key + '.', changed));
      out.push(...lines.slice(nested.to, e.end));
      continue;
    }
    if (nested && nested.kind === 'seq' && isArr(ov) && isArr(nv) && nv.length) {
      out.push(...lines.slice(e.start, nested.from));
      out.push(...patchSeq(lines, nested.from, nested.to, nested.indent, ov, nv, path + e.key, changed));
      out.push(...lines.slice(nested.to, e.end));
      continue;
    }
    changed.push(path + e.key);
    out.push(...emitEntry(e.key, nv, n));
  }
  for (const k of Object.keys(edited)) {
    if (seen.has(k)) continue;
    changed.push(path + k + ' (added)');
    out.push(...emitEntry(k, edited[k], n));
  }
  return out;
}

function patchSeq(lines, from, to, m, ov, nv, path, changed) {
  const items = scanSeq(lines, from, to, m);
  const out = [];
  const count = Math.max(ov.length, nv.length, items.length);
  for (let i = 0; i < count; i++) {
    const at = path + '[' + i + ']';
    if (i >= nv.length) { changed.push(at + ' (removed)'); continue; }
    if (i >= ov.length || i >= items.length) { changed.push(at + ' (added)'); out.push(...emitItem(nv[i], m)); continue; }
    const it = items[i];
    if (deepEqual(ov[i], nv[i])) { out.push(...lines.slice(it.start, it.end)); continue; }
    if (isObj(ov[i]) && isObj(nv[i]) && /^ *- \S/.test(lines[it.start]) && !/^ *- [|>]/.test(lines[it.start])) {
      // a mapping item: its first key rides the dash line — patch it as a
      // mapping at indent m+2 through a virtual copy, then put the dash back
      const virt = lines.slice(it.start, it.end);
      virt[0] = virt[0].replace(/^( *)- /, '$1  ');
      const sub = patchMap(virt, 0, virt.length, m + 2, ov[i], nv[i], at + '.', changed);
      if (!sub.length || indentOf(sub[0]) !== m + 2) throw new Error('could not put the dash back at ' + at);
      sub[0] = pad(m) + '- ' + sub[0].slice(m + 2);
      out.push(...sub);
      continue;
    }
    changed.push(at);
    out.push(...emitItem(nv[i], m));
  }
  return out;
}

// ── re-emit through lc-serialize, re-indented to where the entry lives ───
function emitEntry(key, value, n) {
  const t = dump({ [key]: value });
  const ls = t.split('\n');
  if (ls[ls.length - 1] === '') ls.pop();
  return ls.map((l) => (l === '' ? '' : pad(n) + l));
}

function emitItem(value, m) {
  const t = dump({ k: [value] });
  const ls = t.split('\n');
  ls.shift();                                   // 'k:'
  if (ls[ls.length - 1] === '') ls.pop();
  return ls.map((l) => (l === '' ? '' : pad(m) + l.slice(2)));   // dump puts items at indent 2
}

function deepEqual(a, b) { return JSON.stringify(sortDeep(a)) === JSON.stringify(sortDeep(b)); }
function sortDeep(v) {
  if (isArr(v)) return v.map(sortDeep);
  if (isObj(v)) { const o = {}; for (const k of Object.keys(v).sort()) o[k] = sortDeep(v[k]); return o; }
  return v === undefined ? null : v;
}
