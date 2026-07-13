<!-- © 2026 KarmicSoft — LightCode Platform. Proprietary, All Rights Reserved. License: /license -->
{%- comment -%}
lcYaml — lossless YAML round-trip. Not a component (registers no upgrader);
exposes window.lcYaml for the schema-driven editor and anyone else.

  window.lcYaml.ready(cb)      ensure js-yaml is loaded, then call cb
  window.lcYaml.load(text)     parse with CORE_SCHEMA so dates/1830-05-29 stay
                               STRINGS (js-yaml's default would coerce to Date)
  window.lcYaml.dump(obj, ord) emit block YAML; ord = key order array or null to
                               preserve the object's own key order (minimal git
                               diffs). Empty arrays → [], null → null, multi-line
                               strings → block scalar (|-).

Domain-agnostic: no schema, no field names — pure serialization. Lifted from the
docs/paris PoC engine. Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window.lcYaml) return;
  "use strict";

  function rep(s, n) { var o = ""; for (var i = 0; i < n; i++) o += s; return o; }
  function isArr(v) { return Object.prototype.toString.call(v) === "[object Array]"; }
  function isObj(v) { return v && typeof v === "object" && !isArr(v); }

  function quote(s) { return '"' + s.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"'; }
  function scalarStr(s) {
    if (s === "") return '""';
    if (/^\s|\s$/.test(s)) return quote(s);
    if (/:\s/.test(s) || /:$/.test(s)) return quote(s);
    if (/\s#/.test(s)) return quote(s);
    if (/^[>|&*!%@`"'\[\]{}?,]/.test(s)) return quote(s);
    if (/^-(\s|$)/.test(s)) return quote(s);
    if (/^(true|false|null|~|yes|no|on|off)$/i.test(s)) return quote(s);
    if (/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s)) return quote(s);
    return s;
  }
  function scalarInline(v, pad) {
    if (v === null) return "null";
    var t = typeof v;
    if (t === "number" || t === "boolean") return String(v);
    var s = String(v);
    if (s.indexOf("\n") !== -1) {
      // Faithful chomping: pick the indicator from the trailing newline count so
      // the value round-trips exactly — none → |- (strip), one → | (clip),
      // two+ → |+ (keep), with one blank line per extra trailing newline.
      var trail = (s.match(/\n*$/) || [""])[0].length;
      var chomp = trail === 0 ? "|-" : (trail === 1 ? "|" : "|+");
      var lines = s.replace(/\n+$/, "").split("\n"), out = chomp, i;
      for (i = 0; i < lines.length; i++) out += "\n" + (lines[i] === "" ? "" : pad + "  " + lines[i]);
      for (i = 1; i < trail; i++) out += "\n";
      return out;
    }
    return scalarStr(s);
  }
  function orderedKeys(map, order) {
    var keys = [], seen = {}, k, i;
    if (order) for (i = 0; i < order.length; i++) { k = order[i]; if (map.hasOwnProperty(k)) { keys.push(k); seen[k] = 1; } }
    for (k in map) if (map.hasOwnProperty(k) && !seen[k]) keys.push(k);
    return keys;
  }
  function emitMap(map, indent, order) {
    var keys = orderedKeys(map, order), out = [], i;
    for (i = 0; i < keys.length; i++) out.push(emitKV(map, keys[i], indent));
    return out.join("\n");
  }
  function emitKV(map, k, indent) {
    var pad = rep("  ", indent), v = map[k], i;
    if (v === null || v === undefined) return pad + k + ": null";
    if (isArr(v)) {
      if (v.length === 0) return pad + k + ": []";
      var o = pad + k + ":";
      for (i = 0; i < v.length; i++) o += "\n" + emitSeqItem(v[i], indent + 1);
      return o;
    }
    if (isObj(v)) return pad + k + ":\n" + emitMap(v, indent + 1, null);
    return pad + k + ": " + scalarInline(v, pad);
  }
  function emitSeqItem(item, indent) {
    var pad = rep("  ", indent);
    if (isObj(item)) {
      var mt = emitMap(item, indent + 1, null), lead = rep("  ", indent + 1), lines = mt.split("\n");
      lines[0] = pad + "- " + lines[0].substring(lead.length);
      return lines.join("\n");
    }
    if (isArr(item)) return pad + "- []";
    return pad + "- " + scalarInline(item, pad);
  }
  function dump(obj, order) { return emitMap(obj || {}, 0, order || null) + "\n"; }

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
  function load(text) {
    if (!window.jsyaml) throw new Error("js-yaml not loaded — call lcYaml.ready(cb) first");
    return window.jsyaml.load(text, { schema: window.jsyaml.CORE_SCHEMA }) || {};
  }

  window.lcYaml = { dump: dump, load: load, ready: ready };
})();
</script>
