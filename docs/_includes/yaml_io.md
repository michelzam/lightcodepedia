<!-- Generated from @karmicsoft/lc-serialize — MIT, © 2026 KarmicSoft. DO NOT EDIT (run: node packages/gen-includes.mjs). -->
{%- comment -%}
lcYaml — GENERATED from packages/lc-serialize/index.js (the SSOT). DO NOT EDIT BY
HAND; run `node packages/gen-includes.mjs` to regenerate. The canonical YAML
round-trip lives once, in @karmicsoft/lc-serialize; this exposes it to the
browser as window.lcYaml (load / dump(obj, order) / ready + roundtrip / isLossless).
Not a component (registers no upgrader). Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window.lcYaml) return;
  "use strict";

  var _q = null;
  function ready(cb) {
    if (window.jsyaml) { cb(); return; }
    if (_q) { _q.push(cb); return; }
    _q = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js";
    s.onload = function () { var q = _q; _q = null; q.forEach(function (f) { f(); }); };
    s.onerror = function () { _q = null; if (window.console) console.warn("[lcYaml] js-yaml CDN failed"); };
    document.head.appendChild(s);
  }

  /* ─── canonical body, generated from @karmicsoft/lc-serialize ──────────── */
  /*!
   * @karmicsoft/lc-serialize — faithful YAML round-trip for git-backed content.
   * © KarmicSoft — LightCode. See LICENSE.
   *
   * Reads/writes the SAME YAML that lives in git, losing nothing:
   *  - key order preserved (no reordering → minimal git diffs)
   *  - unquoted dates kept as strings (no timestamp coercion: 1830-05-29 stays a string)
   *  - block-scalar chomping preserved (| / |- / |+)
   *  - null preserved, nested objects/lists, [] for empty arrays
   *  - the leading comment block (migration provenance) survives round-trip
   *  - Markdown with a YAML header (0.2.0): the header is read and written as
   *    above, the text after the closing fence is the record's `body`
   */

  /** Parse YAML WITHOUT date/timestamp coercion (CORE schema). */
  function loadYaml(text) {
    return window.jsyaml.load(text, { schema: window.jsyaml.CORE_SCHEMA });
  }

  /**
   * Read a record: plain YAML, or Markdown with a YAML header (0.2.0) — the
   * header's keys, then `body`: the text after the closing fence. A header that
   * carries a `body:` key of its own is refused: the text has one home.
   */
  function load(text) {
    const fm = splitFrontMatter(text);
    if (!fm) return loadYaml(text);
    let data = loadYaml(fm.header);
    if (data === null || data === undefined) data = {};          // a header of comments only
    if (!isObj(data)) throw new Error('lc-serialize: the header of a Markdown file must be a mapping');
    if (Object.prototype.hasOwnProperty.call(data, 'body'))
      throw new Error('lc-serialize: a Markdown file keeps its text after the header, never in a body: key');
    return { ...data, body: fm.body };
  }

  /**
   * A Markdown file with a YAML header: the first line is exactly `---`, and a
   * later line is exactly `---`. Returns { header, body } — the header's lines
   * (with their newline), the text after the fence without the one blank line
   * that follows the fence and without its final newline — or null for any
   * other text (plain YAML, even one that opens with a lone `---` marker).
   * CRLF line ends read as LF; a write-back is LF (byte drift, not loss).
   */
  function splitFrontMatter(text) {
    const lines = String(text).replace(/\r\n/g, '\n').split('\n');   // a Windows checkout (CRLF) reads the same
    if (lines[0] !== '---') return null;
    let j = 1;
    while (j < lines.length && lines[j] !== '---') j++;
    if (j >= lines.length) return null;
    const header = j > 1 ? lines.slice(1, j).join('\n') + '\n' : '';
    let body = lines.slice(j + 1).join('\n');
    if (body[0] === '\n') body = body.slice(1);                     // the blank line after the fence
    if (body.slice(-1) === '\n') body = body.slice(0, -1);          // the final newline
    return { header, body };
  }

  /** 'md' for Markdown with a YAML header, 'yaml' otherwise. */
  function formatOf(text) { return splitFrontMatter(text) ? 'md' : 'yaml'; }

  /**
   * The leading contiguous block of comment (`# …`) and blank lines before the
   * first data line, verbatim (with its trailing newline) — e.g. a migration
   * provenance header. Empty string when the file starts with data.
   */
  function leadingComments(text) {
    const lines = String(text).split('\n');
    let i = 0;
    for (; i < lines.length; i++) {
      const t = lines[i].trim();
      if (t === '' || t[0] === '#') continue;
      break;
    }
    return i === 0 ? '' : lines.slice(0, i).join('\n') + '\n';
  }

  /**
   * Serialize a plain object to block-style YAML, preserving its key order.
   * `opts.order` — explicit key order. `opts.leading` — a comment block to
   * re-emit above the data (from leadingComments()). Callers without source text
   * just call dump(obj) — behaviour is unchanged.
   */
  function dump(obj, opts = {}) {
    if (opts.format === 'md') return dumpMd(obj || {}, opts);
    const body = emitMap(obj || {}, 0, opts.order || null) + '\n';
    return opts.leading ? opts.leading + body : body;
  }

  /* `opts.format: 'md'` (0.2.0): the record without `body` as the header,
     `body` after the fence and one blank line, a final newline. */
  function dumpMd(rec, opts) {
    const text = rec.body === undefined || rec.body === null ? '' : rec.body;
    if (typeof text !== 'string') throw new Error('lc-serialize: body must be a string in a Markdown file');
    const head = {};
    for (const k of Object.keys(rec)) if (k !== 'body') head[k] = rec[k];
    const order = opts.order ? opts.order.filter((k) => k !== 'body') : null;
    let header = Object.keys(head).length ? emitMap(head, 0, order) + '\n' : '';
    if (opts.leading) header = opts.leading + header;
    return '---\n' + header + '---\n' + (text !== '' ? '\n' + text + '\n' : '');
  }

  /**
   * load() → dump(): the round-trip the corpus CI uses to prove non-loss.
   * Comment-aware — the leading provenance block survives byte-identically.
   */
  function roundtrip(text) {
    const fm = splitFrontMatter(text);
    if (fm) return dump(load(text), { format: 'md', leading: leadingComments(fm.header) });
    return dump(load(text), { leading: leadingComments(text) });
  }

  /** Byte-identical check. Holds for canonical block-style YAML (see README § scope). */
  function isByteIdentical(text) {
    return roundtrip(text) === text;
  }

  /** Semantic non-loss: the parsed data survives a round-trip (order-independent). */
  function isLossless(text) {
    return deepEqual(load(text), load(roundtrip(text)));
  }

  // ── emitter ──────────────────────────────────────────────────────────────
  const pad = (n) => '  '.repeat(n);
  const isArr = Array.isArray;
  const isObj = (v) => v && typeof v === 'object' && !isArr(v);

  function quote(s) { return '"' + s.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"'; }
  function scalarStr(s) {
    if (s === '') return '""';
    if (/^\s|\s$/.test(s)) return quote(s);
    if (/:\s/.test(s) || /:$/.test(s)) return quote(s);
    if (/\s#/.test(s)) return quote(s);
    if (/^[>|&*!%@`"'\[\]{}?,]/.test(s)) return quote(s);
    if (/^-(\s|$)/.test(s)) return quote(s);
    if (/^(true|false|null|~|yes|no|on|off)$/i.test(s)) return quote(s);
    if (/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s)) return quote(s);
    return s;
  }
  function scalarInline(v, p) {
    if (v === null || v === undefined) return 'null';
    const t = typeof v;
    if (t === 'number' || t === 'boolean') return String(v);
    const s = String(v);
    if (s.indexOf('\n') !== -1) {
      const trail = (/(\n*)$/.exec(s)[1] || '').length;         // trailing newlines
      const chomp = trail === 0 ? '-' : (trail === 1 ? '' : '+'); // faithful chomping
      const lines = s.replace(/\n+$/, '').split('\n');
      let out = '|' + chomp;
      for (const ln of lines) out += '\n' + (ln === '' ? '' : p + '  ' + ln);
      for (let i = 0; i < trail - 1; i++) out += '\n';
      return out;
    }
    return scalarStr(s);
  }
  function orderedKeys(map, order) {
    const keys = [], seen = new Set();
    if (order) for (const k of order) if (Object.prototype.hasOwnProperty.call(map, k)) { keys.push(k); seen.add(k); }
    for (const k of Object.keys(map)) if (!seen.has(k)) keys.push(k);
    return keys;
  }
  function emitMap(map, indent, order) {
    return orderedKeys(map, order).map((k) => emitKV(map, k, indent)).join('\n');
  }
  function emitKV(map, k, indent) {
    const p = pad(indent), v = map[k];
    if (v === null || v === undefined) return p + k + ': null';
    if (isArr(v)) {
      if (v.length === 0) return p + k + ': []';
      let o = p + k + ':';
      for (const it of v) o += '\n' + emitSeqItem(it, indent + 1);
      return o;
    }
    if (isObj(v)) return p + k + ':\n' + emitMap(v, indent + 1, null);
    return p + k + ': ' + scalarInline(v, p);
  }
  function emitSeqItem(item, indent) {
    const p = pad(indent);
    if (isObj(item)) {
      const mt = emitMap(item, indent + 1, null), lead = pad(indent + 1), lines = mt.split('\n');
      lines[0] = p + '- ' + lines[0].slice(lead.length);
      return lines.join('\n');
    }
    if (isArr(item)) return p + '- []';
    return p + '- ' + scalarInline(item, p);
  }
  function deepEqual(a, b) { return JSON.stringify(sortDeep(a)) === JSON.stringify(sortDeep(b)); }
  function sortDeep(v) {
    if (isArr(v)) return v.map(sortDeep);
    if (isObj(v)) { const o = {}; for (const k of Object.keys(v).sort()) o[k] = sortDeep(v[k]); return o; }
    return v;
  }

  // dump(obj, order) shim keeps the site's call sites (lcYaml.dump(rec, null)),
  // adapting to the package's dump(obj, { order }).
  // load is the plain YAML reader: the site's record editor writes back what it
  // read with dump(rec, null), so a Markdown-with-header file must keep failing
  // to open here instead of being saved over as YAML (lc-serialize 0.2.0 reads
  // that format for the npm bricks only).
  window.lcYaml = {
    load: loadYaml,
    dump: function (obj, order) { return dump(obj, order ? { order: order } : {}); },
    ready: ready,
    roundtrip: roundtrip,
    isLossless: isLossless
  };
})();
</script>
