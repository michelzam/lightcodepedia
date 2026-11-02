{%- comment -%}
🧩 outside_in.md — a program, read as the page a beginner would use first.
Michel, 2026-11-02: "an alternate tab to the py editor, even open by default,
with the ui … for global variables an input field, in a form called global
… for functions: a form too, with fields for attributes … Globally, I would
generate on the fly a md string using our lc components" — then "go UI tab
in Module 5 first, activable with a knob (outside_in), default=False".

  lcOutsideIn.read(src)          what the program declares at its top level:
                                 the module docstring (the pitch), literal
                                 globals, functions and their parameters,
                                 the input() questions, the calls made
  lcOutsideIn.md(model, rid)     the markdown page: a .form "globals", a
                                 .form "input()", a .form per function with
                                 a 📞 Call .button — our own components, so
                                 the UI is a page a learner could write
  lcOutsideIn.callSource(src, f, values)  the program with only its
                                 definitions kept (line numbers kept), then
                                 the call — what 📞 Call runs
  lcOutsideIn.setGlobal(src, name, value) the program with that global's
                                 literal rewritten — a field edits the code

Phase 1 (2026-11-02): globals, inputs, functions. Loops as grids come with
the stepper's trace (engine Next). Used by pyrun.md's outside_in="true".
{%- endcomment -%}
<script>
(function () {
  "use strict";
  if (window.lcOutsideIn) return;

  var ICON = { int: "🔢", str: "🔤", float: "🧮", bool: "🔘", None: "∅", list: "📋", tuple: "📋", dict: "📒" };

  /* which lines start inside a triple-quoted string */
  function tripleMap(lines) {
    var inside = [], q = null;
    lines.forEach(function (l) {
      inside.push(q);
      var i = 0;
      while (i < l.length) {
        if (q) { var e = l.indexOf(q, i); if (e < 0) break; i = e + 3; q = null; continue; }
        var m = /("""|'''|#|"|')/.exec(l.slice(i));
        if (!m) break;
        var at = i + m.index, t = m[1];
        if (t === "#") break;
        if (t.length === 3) { q = t; i = at + 3; continue; }
        var close = l.indexOf(t, at + 1);
        while (close > 0 && l[close - 1] === "\\") close = l.indexOf(t, close + 1);
        if (close < 0) break;
        i = close + 1;
      }
    });
    return inside;
  }

  /* commas at depth 0, outside strings */
  function splitTop(s) {
    var out = [], depth = 0, cur = "", q = null;
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      if (q) { cur += c; if (c === "\\") { cur += s[++i] || ""; continue; } if (c === q) q = null; continue; }
      if (c === '"' || c === "'") { q = c; cur += c; continue; }
      if ("([{".indexOf(c) >= 0) depth++;
      if (")]}".indexOf(c) >= 0) depth--;
      if (c === "," && depth === 0) { out.push(cur.trim()); cur = ""; continue; }
      cur += c;
    }
    if (cur.trim()) out.push(cur.trim());
    return out;
  }

  /* a Python literal → { ok, v, type } */
  function literal(t) {
    t = String(t || "").trim();
    var m = /^(['"])((?:\\.|(?!\1)[^\\])*)\1$/.exec(t);
    if (m) return { ok: true, type: "str", v: m[2].replace(/\\(.)/g, function (x, c) { return c === "n" ? "\n" : c === "t" ? "\t" : c; }) };
    if (/^-?\d+$/.test(t)) return { ok: true, type: "int", v: parseInt(t, 10) };
    if (/^-?\d*\.\d+(?:e[+-]?\d+)?$|^-?\d+\.\d*$/i.test(t)) return { ok: true, type: "float", v: parseFloat(t) };
    if (t === "True" || t === "False") return { ok: true, type: "bool", v: t === "True" };
    if (t === "None") return { ok: true, type: "None", v: null };
    return { ok: false };
  }
  function baseType(hint) {
    var h = String(hint || "").trim();
    if (!h) return "";
    if (/\|\s*None$/.test(h)) h = h.replace(/\s*\|\s*None$/, "");
    return h.split("[")[0].trim();
  }
  function icon(hint) { var b = baseType(hint); return ICON[b] || (b ? "🏷️" : ""); }

  /* a value from a form field, as Python would write it for this hint */
  function toPy(v, hint) {
    var b = baseType(hint);
    if (b === "int") { var s = String(v == null ? "" : v).trim(); return /^-?\d+$/.test(s) ? { ok: true, py: s } : { ok: false, why: "an int is expected" }; }
    if (b === "float") { var f = String(v == null ? "" : v).trim(); return /^-?(\d+\.?\d*|\.\d+)(e[+-]?\d+)?$/i.test(f) ? { ok: true, py: f } : { ok: false, why: "a float is expected" }; }
    if (b === "bool") { var x = String(v).trim().toLowerCase(); return { ok: true, py: (v === true || x === "true" || x === "1") ? "True" : "False" }; }
    if (v === null || v === undefined) return { ok: true, py: "None" };
    if (b === "str" || typeof v === "string") return { ok: true, py: JSON.stringify(String(v)) };
    return { ok: true, py: String(v) };
  }

  function read(src) {
    var lines = String(src || "").replace(/\r\n?/g, "\n").split("\n"), inT = tripleMap(lines);
    var model = { doc: [], globals: [], defs: [], inputs: [], calls: {} };
    var top = function (i) { return !inT[i] && /^\S/.test(lines[i]) && !/^#/.test(lines[i]); };
    /* the module docstring: the program's elevator pitch */
    var first = 0;
    while (first < lines.length && !lines[first].trim()) first++;
    var dm = first < lines.length ? /^\s*("""|''')(.*)$/.exec(lines[first]) : null;
    if (dm) {
      var q = dm[1], rest = dm[2], j = first;
      if (rest.indexOf(q) >= 0) model.doc.push(rest.slice(0, rest.indexOf(q)).trim());
      else {
        if (rest.trim()) model.doc.push(rest.trim());
        for (j = first + 1; j < lines.length; j++) {
          var k = lines[j].indexOf(q);
          if (k >= 0) { if (lines[j].slice(0, k).trim()) model.doc.push(lines[j].slice(0, k).trim()); break; }
          if (lines[j].trim()) model.doc.push(lines[j].trim());
        }
      }
    }
    function blockEnd(i) { var j = i + 1; while (j < lines.length && !top(j)) j++; return j; }   /* first line after the block */
    for (var i = 0; i < lines.length; i++) {
      if (!top(i)) continue;
      var l = lines[i], m;
      if ((m = /^def\s+([A-Za-z_]\w*)\s*\((.*)\)\s*(?:->\s*(.+?))?\s*:\s*(?:#.*)?$/.exec(l))) {
        var end = blockEnd(i), body = lines.slice(i + 1, end).join("\n");
        var params = splitTop(m[2]).filter(function (p) { return p && p !== "self" && !/^\*/.test(p); }).map(function (p) {
          var pm = /^([A-Za-z_]\w*)\s*(?::\s*([^=]+?))?\s*(?:=\s*(.+))?$/.exec(p) || [];
          var d = pm[3] !== undefined ? literal(pm[3]) : null;
          return { name: pm[1] || p, hint: (pm[2] || "").trim(), dflt: d && d.ok ? d : null, dfltText: pm[3] };
        });
        var doc = "", bl = lines.slice(i + 1, end).filter(function (x) { return x.trim(); })[0] || "";
        var bdm = /^\s*[rRuU]?("""|'''|"|')(.*)$/.exec(bl);
        if (bdm) doc = bdm[2].split(bdm[1])[0].trim() || ((lines.slice(i + 2, end).filter(function (x) { return x.trim(); })[0] || "").trim());
        model.defs.push({ name: m[1], params: params, ret: (m[3] || "").trim(), line: i + 1, doc: doc.replace(/"""|'''/g, "").trim(),
                          asks: /\binput\s*\(/.test(body), prints: /\bprint\s*\(/.test(body) });
        i = end - 1;
        continue;
      }
      if ((m = /^([A-Za-z_]\w*)\s*(?::\s*([^=]+?))?\s*=(?!=)\s*(.+)$/.exec(l))) {
        var raw = m[3].replace(/\s+#[^"']*$/, ""), lit = literal(raw);
        if (lit.ok && m[1] !== "__all__") model.globals.push({ name: m[1], hint: (m[2] || "").trim() || lit.type, value: lit.v, line: i + 1, typed: !!m[2] });
        continue;
      }
      if ((m = /^([A-Za-z_]\w*)\s*\((.*)\)\s*(?:#.*)?$/.exec(l)) && !model.calls[m[1]]) {
        var args = splitTop(m[2]).map(literal);
        if (args.every(function (a) { return a.ok; })) model.calls[m[1]] = args;
      }
    }
    /* every question the program asks, and who asks it */
    var owner = "";
    lines.forEach(function (l, n) {
      if (top(n)) { var dd = /^def\s+([A-Za-z_]\w*)/.exec(l); owner = dd ? dd[1] : ""; }
      if (inT[n]) return;
      var re = /\binput\s*\(\s*(?:(['"])((?:\\.|(?!\1)[^\\])*)\1)?\s*\)/g, im;
      while ((im = re.exec(l))) model.inputs.push({ prompt: im[2] || "", line: n + 1, owner: owner });
    });
    return model;
  }

  function yamlVal(v) { return v === null || v === undefined ? "null" : typeof v === "boolean" ? String(v) : typeof v === "number" ? String(v) : JSON.stringify(String(v)); }
  function yamlKey(k) { return /^[A-Za-z_][\w ]*$/.test(k) ? k : JSON.stringify(k); }
  function attr(s) { return String(s).replace(/"/g, "'"); }
  function fid(rid, name) { return "oi_" + String(rid).replace(/\W/g, "_") + "_" + name; }

  function md(model, rid) {
    var out = [];
    if (model.doc.length) out.push(model.doc.map(function (l) { return "> " + l.replace(/[<>]/g, ""); }).join("  \n"));   /* one line each: a pitch is four lines */
    if (model.globals.length) {
      out.push("```yaml\n" + model.globals.map(function (g) { return g.name + ": " + yamlVal(g.value); }).join("\n") + "\n```\n" +
               '{: .form #' + fid(rid, "globals") + ' title="globals" editable="true" hints="' +
               attr(model.globals.map(function (g) { return g.name + ": " + g.hint; }).join("; ")) + '" }');
    }
    if (model.inputs.length) {
      var seen = {}, rows = [];
      model.inputs.forEach(function (q) {
        var key = q.prompt || "(no question)";
        if (seen[key]) return; seen[key] = 1;
        rows.push(yamlKey(key) + ": " + JSON.stringify("asked in the console" + (q.owner ? ", by " + q.owner + "()" : "") + " — line " + q.line));
      });
      out.push("```yaml\n" + rows.join("\n") + "\n```\n" + '{: .form #' + fid(rid, "inputs") + ' title="input() — what the program asks" }');
    }
    model.defs.forEach(function (f) {
      var call = model.calls[f.name] || [];
      var sig = f.name + "(" + f.params.map(function (p) { return p.name + (p.hint ? ": " + p.hint : "") + (p.dfltText !== undefined ? " = " + p.dfltText : ""); }).join(", ") + ")" + (f.ret ? " -> " + f.ret : "");
      var block = "";
      if (f.params.length) {
        block += "```yaml\n" + f.params.map(function (p, k) {
          var v = call[k] ? call[k].v : p.dflt ? p.dflt.v : (baseType(p.hint) === "int" ? 0 : baseType(p.hint) === "float" ? 0.0 : baseType(p.hint) === "bool" ? false : "");
          return p.name + ": " + yamlVal(v);
        }).join("\n") + "\n```\n" + '{: .form #' + fid(rid, "f_" + f.name) + ' title="' + attr(sig) + '" editable="true" hints="' +
          attr(f.params.map(function (p) { return p.name + ": " + (p.hint || (p.dflt ? p.dflt.type : "")); }).join("; ")) + '" }\n\n';
      } else {
        block += "`" + sig + "`" + (f.doc ? " — " + f.doc : "") + "\n\n";
      }
      if (f.params.length && f.doc) block = "*" + f.doc.replace(/[*_<>]/g, "") + "*\n\n" + block;
      block += "[📞 Call " + f.name + "](#oi-call-" + f.name + ")\n{: .button }";
      out.push(block);
    });
    if (!out.length) out.push("*Nothing to show here yet: no variables, functions or questions at the top of the program. 🐍 Code shows it all.*");
    return out.join("\n\n") + "\n";
  }

  /* the program with only its definitions kept — line numbers unchanged,
     so a traceback still points where the learner looks — then the call */
  function defsOnly(src) {
    var lines = String(src || "").replace(/\r\n?/g, "\n").split("\n"), inT = tripleMap(lines), keep = true, docDone = false;
    return lines.map(function (l, i) {
      if (!inT[i] && /^\S/.test(l) && !/^#/.test(l)) {
        keep = /^(def|class|async\s+def|import|from)\b|^@/.test(l) ||
               (/^[A-Za-z_]\w*\s*(?::[^=]+)?=(?!=)/.test(l) && !/\binput\s*\(/.test(l)) ||
               (!docDone && /^[rRuU]?("""|''')/.test(l));
        docDone = true;
      }
      return keep ? l : "";
    }).join("\n");
  }

  function callSource(src, fname, values) {
    var model = read(src), f = null;
    model.defs.forEach(function (d) { if (d.name === fname) f = d; });
    if (!f) return { ok: false, why: "no function " + fname + " in the program" };
    var args = [];
    for (var k = 0; k < f.params.length; k++) {
      var p = f.params[k], has = values && Object.prototype.hasOwnProperty.call(values, p.name);
      var r = toPy(has ? values[p.name] : (p.dflt ? p.dflt.v : ""), p.hint || (p.dflt ? p.dflt.type : ""));
      if (!r.ok) return { ok: false, why: icon(p.hint) + " " + p.name + ": " + r.why };
      args.push(r.py);
    }
    var call = fname + "(" + args.join(", ") + ")";
    return { ok: true, call: call,
             src: defsOnly(src) + "\nprint(" + JSON.stringify("📞 " + call) + ")\n_lc_r = " + call +
                  "\nif _lc_r is not None:\n    print(\"→\", repr(_lc_r))\n" };
  }

  function setGlobal(src, name, value) {
    var lines = String(src || "").split("\n"), model = read(src), g = null;
    model.globals.forEach(function (x) { if (x.name === name) g = x; });
    if (!g) return { ok: false };
    var r = toPy(value, g.hint);
    if (!r.ok) return { ok: false, why: r.why };
    var l = lines[g.line - 1], m = /^([A-Za-z_]\w*\s*(?::[^=]+?)?\s*=\s*)(.*?)(\s+#.*)?$/.exec(l);
    if (!m) return { ok: false };
    var lit = literal(m[2]);
    var py = r.py;
    if (lit.ok && lit.type === "str" && /^'/.test(m[2].trim()) && py.indexOf("'") < 0) py = "'" + py.slice(1, -1).replace(/\\"/g, '"') + "'";   /* the learner's own quotes */
    lines[g.line - 1] = m[1] + py + (m[3] || "");
    return { ok: true, src: lines.join("\n") };
  }

  window.lcOutsideIn = { read: read, md: md, callSource: callSource, setGlobal: setGlobal, defsOnly: defsOnly, icon: icon, id: fid };
})();
</script>
