<!-- © 2026 KarmicSoft — LightCode Platform. Proprietary, All Rights Reserved. License: /license -->
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
   */

  /** Parse YAML WITHOUT date/timestamp coercion (CORE schema). */
  function load(text) {
    return window.jsyaml.load(text, { schema: window.jsyaml.CORE_SCHEMA });
  }

  /** Serialize a plain object to block-style YAML, preserving its key order. */
  function dump(obj, opts = {}) {
    return emitMap(obj, 0, opts.order || null) + '\n';
  }

  /** load() → dump(): the round-trip your CI uses to prove non-loss. */
  function roundtrip(text) {
    return dump(load(text));
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
  window.lcYaml = {
    load: load,
    dump: function (obj, order) { return dump(obj, order ? { order: order } : {}); },
    ready: ready,
    roundtrip: roundtrip,
    isLossless: isLossless
  };
})();
</script>
