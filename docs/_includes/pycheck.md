{%- comment -%}
PyCheck — what CPython's doctest and mypy give a learner, for the page's
MicroPython (Michel, 2026-10-26, Python Module 09: "stick with my examples").

MicroPython keeps no docstrings (jump.__doc__ raises) and no annotations, and
has no doctest or mypy. So both are read from the program's TEXT:

  lcPyDocs(src, file)     every def/class with its signature, docstring and
                          >>> examples (line numbers are the file's own)
  lcTypeLint(src, opts)   Dr. mypy (lite): untyped defs (strict), return
                          values, literal arguments — mypy's words and codes
  lcDrMypy(src, opts)     the same as mypy's own report text and exit status
  LC_PY_SHIM              the Python side, installed before each run:
                          import doctest → testmod(verbose=...), __doc__,
                          X.__doc__, help(X), import mypy.api → run([...]),
                          import pycodestyle → StyleGuide().check_files([...])
  lcPep8(src, opts)       🛁 pycodestyle (lite): PEP 8 codes read from the text
  lcPep8Report(src, opts) the same as pycodestyle's path:line:col: CODE lines
  lcPyPrepare(code)       X.__doc__ → _lc_doc(X, "X"), outside strings only

Used by pyrun.md (▶ Run, 🧪 Test, 🩺 Dr. mypy) and mdpad.md (mypy= knob:
⚠ in the gutter of a python fence). Auto-included by docs/_layouts/default.html.
{%- endcomment -%}
<script>
(function () {
  "use strict";
  if (window.lcPyDocs) return;

  /* ── the program's text, read the way doctest and help() read it ───── */
  function cleandoc(lines) {
    /* inspect.cleandoc: the first line loses its indent, the rest lose the
       common one; blank lines at both ends go */
    var rest = lines.slice(1).filter(function (l) { return l.l.trim(); });
    var ind = rest.length ? Math.min.apply(null, rest.map(function (l) { return /^ */.exec(l.l)[0].length; })) : 0;
    var out = lines.map(function (l, k) { return { l: k === 0 ? l.l.replace(/^\s+/, "") : l.l.slice(ind), n: l.n }; });
    while (out.length && !out[0].l.trim()) out.shift();
    while (out.length && !out[out.length - 1].l.trim()) out.pop();
    return out.map(function (l) { return { l: l.l.replace(/\s+$/, ""), n: l.n }; });
  }

  /* a string literal starting the statement at line i: its lines, or null */
  function docAt(lines, i) {
    var t = lines[i].replace(/^\s+/, ""), m = /^[rRuU]?("""|'''|"|')/.exec(t);
    if (!m) return null;
    var q = m[1], body = t.slice(m[0].length);
    if (q.length === 1) {
      var e = body.indexOf(q);
      return e < 0 ? null : { lines: [{ l: body.slice(0, e), n: i + 1 }], end: i };
    }
    var got = [], j = i, s = body;
    for (;;) {
      var k = s.indexOf(q);
      if (k >= 0) { got.push({ l: s.slice(0, k), n: j + 1 }); return { lines: got, end: j }; }
      got.push({ l: s, n: j + 1 });
      if (++j >= lines.length) return { lines: got, end: j - 1 };
      s = lines[j];
    }
  }

  /* >>> examples in a cleaned docstring, doctest's way */
  function examples(doc) {
    var ex = [], k = 0;
    while (k < doc.length) {
      var m = /^(\s*)>>> ?(.*)$/.exec(doc[k].l);
      if (!m) { k++; continue; }
      var ind = m[1].length, src = [m[2]], line = doc[k].n;
      k++;
      while (k < doc.length) {
        var c = /^\s*\.\.\.(?: (.*)|$)/.exec(doc[k].l);
        if (!c) break;
        src.push(c[1] || ""); k++;
      }
      var want = [];
      while (k < doc.length && doc[k].l.trim() && !/^\s*>>>/.test(doc[k].l)) {
        var w = doc[k].l.slice(Math.min(ind, /^ */.exec(doc[k].l)[0].length));
        want.push(w === "<BLANKLINE>" ? "" : w); k++;
      }
      ex.push({ source: src.join("\n"), run: lcPyPrepare(src.join("\n")), want: want.join("\n"), line: line });
    }
    return ex;
  }

  /* split "a: int, b=2, *args" at the commas outside brackets and quotes */
  function topSplit(s) {
    var out = [], depth = 0, cur = "", q = "";
    for (var i = 0; i < s.length; i++) {
      var ch = s[i];
      if (q) { cur += ch; if (ch === "\\") { cur += s[++i] || ""; } else if (ch === q) q = ""; continue; }
      if (ch === "'" || ch === '"') { q = ch; cur += ch; continue; }
      if ("([{".indexOf(ch) >= 0) depth++;
      if (")]}".indexOf(ch) >= 0) depth--;
      if (ch === "," && depth === 0) { out.push(cur.trim()); cur = ""; continue; }
      cur += ch;
    }
    if (cur.trim()) out.push(cur.trim());
    return out;
  }

  function parseHeader(text) {
    /* "def jump(start: int, leap: int) -> int:" → name, params, return */
    var m = /^\s*(?:async\s+)?def\s+(\w+)\s*\(([\s\S]*)\)\s*(?:->\s*([\s\S]*?))?\s*:\s*(#.*)?$/.exec(text);
    if (!m) return null;
    var params = topSplit(m[2].replace(/\s*\n\s*/g, " ")).filter(function (p) { return p !== "/" && p !== "*"; }).map(function (p) {
      var pm = /^(\*{0,2})(\w+)\s*(?::\s*([^=]+?))?\s*(?:=\s*(.+))?$/.exec(p) || [p, "", p, null, null];
      return { name: pm[2], star: pm[1], ann: pm[3] ? pm[3].trim() : null, dflt: pm[4] || null };
    });
    return { name: m[1], params: params, ret: m[3] ? m[3].trim() : null };
  }

  /* which lines sit INSIDE a triple-quoted string, so a "def" or a call
     written in a docstring is no def and no call */
  function inStringMap(lines) {
    var map = [], q = null;
    lines.forEach(function (l) {
      map.push(!!q);
      for (var i = 0; i < l.length; i++) {
        if (q) { if (l[i] === "\\") { i++; continue; } if (l.startsWith(q, i)) { i += 2; q = null; } continue; }
        var ch = l[i];
        if (ch === "#") break;
        if (l.startsWith('"""', i) || l.startsWith("'''", i)) { q = l.substr(i, 3); i += 2; continue; }
        if (ch === "'" || ch === '"') {
          for (i++; i < l.length && l[i] !== ch; i++) if (l[i] === "\\") i++;
        }
      }
    });
    return map;
  }

  function lcPyDocs(src, file) {
    var lines = String(src || "").replace(/\r\n/g, "\n").split("\n");
    var res = { file: file || "main.py", module: null, items: [], docLines: [] };
    var inStr = inStringMap(lines);
    var first = 0;
    while (first < lines.length && (!lines[first].trim() || /^\s*#/.test(lines[first]))) first++;
    if (first < lines.length) {
      var md = docAt(lines, first);
      if (md) {
        for (var ml = first; ml <= md.end; ml++) res.docLines.push(ml);
        var mdoc = cleandoc(md.lines);
        res.module = { doc: mdoc.map(function (l) { return l.l; }).join("\n"), examples: examples(mdoc) };
      }
    }
    var stack = [];
    for (var i = 0; i < lines.length; i++) {
      if (inStr[i]) continue;
      var L = lines[i], hm = /^(\s*)(?:async\s+)?(def|class)\s+(\w+)/.exec(L);
      if (!hm) continue;
      var indent = hm[1].length;
      while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
      var parent = stack.length ? stack[stack.length - 1] : null;
      /* the header may span lines: up to the ':' that closes it */
      var j = i, text = L, depth = 0;
      for (;;) {
        depth = 0;
        text.replace(/(['"])(?:\\.|(?!\1).)*\1/g, "").replace(/[([{]/g, function () { depth++; }).replace(/[)\]}]/g, function () { depth--; });
        if (depth <= 0 && /:\s*(#.*)?$/.test(text)) break;
        if (++j >= lines.length) break;
        text += "\n" + lines[j];
      }
      var decos = [];
      for (var d = i - 1; d >= 0 && /^\s*@/.test(lines[d]); d--) decos.push(lines[d].trim());
      var it = {
        kind: hm[2] === "class" ? "class" : (parent && parent.kind === "class" ? "method" : "function"),
        name: (parent ? parent.qual + "." : "") + hm[3], short: hm[3],
        line: i + 1, header: L, col: indent, decorators: decos, nested: !!(parent && parent.kind !== "class"),
        doc: null, examples: [], end: j, docEnd: j
      };
      if (it.kind === "class") {
        var cm = /class\s+\w+\s*(\(([^)]*)\))?/.exec(text);
        it.bases = cm && cm[2] ? topSplit(cm[2]) : [];
        it.sig = hm[3];
      } else {
        var h = parseHeader(text) || { name: hm[3], params: [], ret: null };
        it.params = h.params; it.ret = h.ret;
        it.sig = hm[3] + "(" + h.params.map(function (p) {
          return p.star + p.name + (p.ann ? ": " + p.ann : "") + (p.dflt ? (p.ann ? " = " : "=") + p.dflt : "");
        }).join(", ") + ")" + (h.ret ? " -> " + h.ret : "");
      }
      /* the body: the lines after the header, deeper than it */
      var b = j + 1;
      while (b < lines.length && (!lines[b].trim() || /^\s*#/.test(lines[b]))) b++;
      if (b < lines.length && /^(\s*)/.exec(lines[b])[1].length > indent) {
        var dd = docAt(lines, b);
        if (dd) {
          it.docEnd = dd.end;
          for (var dl = b; dl <= dd.end; dl++) res.docLines.push(dl);
          var doc = cleandoc(dd.lines);
          it.doc = doc.map(function (l) { return l.l; }).join("\n");
          it.examples = examples(doc);
        }
      }
      var e = j + 1, last = j;
      while (e < lines.length && (!lines[e].trim() || /^(\s*)/.exec(lines[e])[1].length > indent)) {
        if (lines[e].trim()) last = e;
        e++;
      }
      it.bodyEnd = last;
      res.items.push(it);
      stack.push({ indent: indent, qual: it.name, kind: it.kind });
    }
    return res;
  }

  /* X.__doc__ → _lc_doc(X, "X"), in code only — never inside a string or a
     comment, and the line count stays */
  function lcPyPrepare(src) {
    var out = "", i = 0, n = src.length, code = "";
    function flush() {
      out += code.replace(/([A-Za-z_][\w.]*)\.__doc__\b/g, function (all, x) {
        return "_lc_doc(" + x + ", " + JSON.stringify(x) + ")";
      });
      code = "";
    }
    while (i < n) {
      var ch = src[i];
      if (ch === "#") { flush(); var e = src.indexOf("\n", i); if (e < 0) e = n; out += src.slice(i, e); i = e; continue; }
      var m = /^([rRbBuUfF]{0,2})('''|"""|'|")/.exec(src.slice(i, i + 5));
      if (m && (i === 0 || !/[A-Za-z0-9_.]/.test(src[i - 1]))) {
        flush();
        var q = m[2], j = i + m[0].length;
        while (j < n) {
          if (src[j] === "\\") { j += 2; continue; }
          if (src.startsWith(q, j)) { j += q.length; break; }
          if (q.length === 1 && src[j] === "\n") break;
          j++;
        }
        out += src.slice(i, j); i = j; continue;
      }
      code += ch; i++;
    }
    flush();
    return out;
  }

  /* ── Dr. mypy (lite) ────────────────────────────────────────────────
     The checks a beginner meets first, with mypy's own words and codes, so
     what the page says is what PythonAnywhere's mypy says (Module 09 9b):
       strict  no-untyped-def — a def without its hints
       always  return-value / return — a return that contradicts the hint
               arg-type — a literal argument of the wrong type
     Only what can be read for sure from the text is reported: an argument
     or a return that is not a literal is never guessed at. */
  var SIMPLE = { "int": 1, "float": 1, "str": 1, "bool": 1, "None": 1, "complex": 1, "bytes": 1 };
  function litType(x) {
    x = x.trim();
    if (/^(True|False)$/.test(x)) return "bool";
    if (x === "None") return "None";
    if (/^-?\d+$/.test(x.replace(/_/g, ""))) return "int";
    if (/^-?(\d+\.\d*|\.\d+|\d+(\.\d*)?[eE][-+]?\d+)$/.test(x.replace(/_/g, ""))) return "float";
    if (/^[rRuUfF]{0,2}("""|'''|"|')[\s\S]*\1$/.test(x)) return "str";
    if (/^[bB][rR]?("|')[\s\S]*\1$/.test(x)) return "bytes";
    return null;
  }
  function accepts(ann, t) {
    if (!SIMPLE[ann]) return true;          /* Optional, lists, classes: not judged */
    if (ann === t) return true;
    if (ann === "float" && (t === "int" || t === "bool")) return true;
    if (ann === "complex" && (t === "int" || t === "float" || t === "bool")) return true;
    if (ann === "int" && t === "bool") return true;
    return false;
  }
  function stripComment(l) {
    var q = "", out = "";
    for (var i = 0; i < l.length; i++) {
      var ch = l[i];
      if (q) { out += ch; if (ch === "\\") out += l[++i] || ""; else if (ch === q) q = ""; continue; }
      if (ch === "#") break;
      if (ch === "'" || ch === '"') q = ch;
      out += ch;
    }
    return out;
  }

  function lcTypeLint(src, opts) {
    opts = opts || {};
    var strict = !!opts.strict;
    var lines = String(src || "").replace(/\r\n/g, "\n").split("\n");
    var docs = lcPyDocs(src, opts.file);
    var inStr = inStringMap(lines);
    var probs = [];
    function add(line, col, msg, code, sev) { probs.push({ line: line, col: col, severity: sev || "error", msg: msg, code: code || "" }); }
    var funcs = {};                          /* name → its params (calls by name) */
    docs.items.forEach(function (it) {
      if (it.kind === "function" && !it.nested) funcs[it.name] = { params: it.params, name: it.name };
      if (it.kind === "class") {
        var init = docs.items.filter(function (x) { return x.name === it.name + ".__init__"; })[0];
        funcs[it.name] = { params: init ? init.params.slice(1) : [], name: it.name };
      }
    });
    docs.items.forEach(function (it) {
      if (it.kind === "class") return;
      var params = it.params.slice();
      var isStatic = it.decorators.indexOf("@staticmethod") >= 0;
      if (it.kind === "method" && !isStatic && params.length) params.shift();     /* self / cls */
      var annotated = params.filter(function (p) { return p.ann; }).length;
      var body = [];
      for (var b = it.docEnd + 1; b <= it.bodyEnd; b++) body.push(b);
      /* nested defs speak for themselves: their lines leave this body */
      var mine = [], skipTo = -1;
      body.forEach(function (b) {
        if (b <= skipTo || inStr[b]) return;
        var nm = /^(\s*)(?:async\s+)?def\s/.exec(lines[b]);
        if (nm && b > it.end) {
          var inner = docs.items.filter(function (x) { return x.line === b + 1; })[0];
          if (inner) { skipTo = inner.bodyEnd; return; }
        }
        mine.push(b);
      });
      var returns = mine.map(function (b) { return { b: b, m: /^\s*return\b\s*(.*)$/.exec(stripComment(lines[b])) }; }).filter(function (r) { return r.m; });
      var returnsValue = returns.some(function (r) { return r.m[1].trim(); });
      var col = it.col;
      if (strict) {
        if (!annotated && !it.ret) {
          if (!params.length) {
            add(it.line, col, "Function is missing a return type annotation", "no-untyped-def");
            if (!returnsValue) add(it.line, col, 'Use "-> None" if function does not return a value', "", "note");
          } else add(it.line, col, "Function is missing a type annotation", "no-untyped-def");
        } else if (annotated < params.length) {
          add(it.line, col, "Function is missing a type annotation for one or more arguments", "no-untyped-def");
        } else if (!it.ret && !(it.short === "__init__" && params.length)) {
          add(it.line, col, "Function is missing a return type annotation", "no-untyped-def");
          if (!returnsValue) add(it.line, col, 'Use "-> None" if function does not return a value', "", "note");
        }
      }
      /* an unannotated def is not checked by mypy — nor here */
      if (!it.ret && !annotated) return;
      returns.forEach(function (r) {
        var v = r.m[1].trim(), rc = /^(\s*)/.exec(lines[r.b])[1].length;
        if (!it.ret) return;
        if (it.ret === "None") {
          if (v && v !== "None") add(r.b + 1, rc, "No return value expected", "return-value");
          return;
        }
        if (!v) { add(r.b + 1, rc, "Return value expected", "return-value"); return; }
        var t = litType(v);
        if (t && !accepts(it.ret, t)) add(r.b + 1, rc, 'Incompatible return value type (got "' + t + '", expected "' + it.ret + '")', "return-value");
      });
      if (it.ret && it.ret !== "None" && !/^Optional\b|None\b/.test(it.ret) && !returns.length) {
        var raises = mine.some(function (b) { return /^\s*raise\b/.test(lines[b]); });
        var empty = mine.every(function (b) { return !lines[b].trim() || /^\s*(#|pass\s*$|\.\.\.\s*$)/.test(lines[b]); });
        if (!raises && !empty) add(it.line, col, "Missing return statement", "return");
      }
    });
    /* literal arguments against the hints, at every call of a known def */
    var docSet = {};
    docs.docLines.forEach(function (n) { docSet[n] = true; });
    lines.forEach(function (raw, i) {
      if (inStr[i] || docSet[i] || /^\s*(?:async\s+)?(def|class)\s/.test(raw)) return;
      /* no lookbehind: a Safari before 16.4 refuses the whole script for one */
      var l = stripComment(raw), re = /([A-Za-z_]\w*)\s*\(/g, m;
      /* a call spelled inside a string literal is text, not a call */
      var quoted = [], sq = "";
      for (var c = 0; c < l.length; c++) {
        if (sq) { quoted[c] = true; if (l[c] === "\\") quoted[++c] = true; else if (l[c] === sq) sq = ""; continue; }
        if (l[c] === "'" || l[c] === '"') { sq = l[c]; quoted[c] = true; }
      }
      while ((m = re.exec(l))) {
        if (m.index && /[\w.]/.test(l[m.index - 1])) continue;
        var f = funcs[m[1]];
        if (!f || quoted[m.index]) continue;
        m = [m[0], "", m[1]]; m.index = re.lastIndex - m[0].length;
        var start = m.index + m[0].length, depth = 1, k = start, q = "";
        for (; k < l.length && depth; k++) {
          var ch = l[k];
          if (q) { if (ch === "\\") k++; else if (ch === q) q = ""; continue; }
          if (ch === "'" || ch === '"') q = ch;
          else if (ch === "(" || ch === "[" || ch === "{") depth++;
          else if (ch === ")" || ch === "]" || ch === "}") depth--;
        }
        if (depth) continue;
        var args = topSplit(l.slice(start, k - 1));
        var pos = f.params.filter(function (p) { return !p.star; });
        args.forEach(function (a, n) {
          var kw = /^(\w+)\s*=(?!=)\s*([\s\S]+)$/.exec(a), p, val;
          if (kw) { p = pos.filter(function (x) { return x.name === kw[1]; })[0]; val = kw[2]; }
          else if (/^\*/.test(a)) return;
          else { p = pos[n]; val = a; }
          if (!p || !p.ann) return;
          var t = litType(val);
          if (t && !accepts(p.ann, t)) {
            add(i + 1, m.index + m[1].length, 'Argument ' + (kw ? '"' + kw[1] + '"' : (n + 1)) + ' to "' + f.name + '" has incompatible type "' + t + '"; expected "' + p.ann + '"', "arg-type");
          }
        });
      }
    });
    probs.sort(function (a, b) { return a.line - b.line || (a.severity === "note") - (b.severity === "note"); });
    return probs;
  }

  /* mypy's report: path:line: error: words  [code], the source line and a
     caret under --pretty, then the count — and mypy's exit status */
  function lcDrMypy(src, opts) {
    /* a page's proof passes a word: "strict" (or nothing) */
    if (typeof opts === "string") opts = { strict: /strict/.test(opts) };
    opts = opts || {};
    var file = opts.file || "main.py", lines = String(src || "").split("\n");
    var probs = lcTypeLint(src, opts), out = [], errors = 0;
    probs.forEach(function (p) {
      if (p.severity === "error") errors++;
      out.push(file + ":" + p.line + ": " + p.severity + ": " + p.msg + (p.code ? "  [" + p.code + "]" : ""));
      if (opts.pretty && p.severity === "error") {
        var l = lines[p.line - 1] || "", ind = /^\s*/.exec(l)[0].length;
        out.push("    " + l.trim());
        out.push("    " + " ".repeat(Math.max(0, p.col - ind)) + "^");
      }
    });
    out.push(errors ? "Found " + errors + " error" + (errors > 1 ? "s" : "") + " in 1 file (checked 1 source file)"
                    : "Success: no issues found in 1 source file");
    return { out: out.join("\n") + "\n", err: "", status: errors ? 1 : 0, problems: probs };
  }

  /* mypy.api.run([...]) from Python: the flags it understands, on the program
     being run (the runner names it before each run) */
  window.lcDrMypyRun = function (argsJson) {
    var args = [];
    try { args = JSON.parse(String(argsJson)); } catch (e) { }
    var strict = args.indexOf("--strict") >= 0 || args.indexOf("--disallow-untyped-defs") >= 0;
    var r = lcDrMypy(window._lcPySrc || "", { file: window._lcPyFile || "main.py", strict: strict, pretty: args.indexOf("--pretty") >= 0 });
    return JSON.stringify({ out: r.out, err: r.err, status: r.status });
  };

  /* ── 🛁 pycodestyle (lite) — PEP 8 read from the text ───────────────
     Michel, 2026-11-02, Python Module 10: "a new page in the py code
     editor to check pep8, inspired by the slides (pycodestyle)". The deck
     runs pycodestyle.StyleGuide().check_files([__file__]) in PythonAnywhere;
     the page's MicroPython has no pycodestyle, so the codes a learner meets
     first are read from the program's text, in pycodestyle's own words and
     path:line:col format — blank lines (E301-E306), whitespace around
     operators, commas, brackets and parameter equals (E2xx), comments
     (E26x), indentation (E111, E117), statements (E401, E402, E70x),
     comparisons (E711, E712), names (E741), long lines (E501) and trailing
     whitespace (W291, W293, W391). Continuation-line alignment (E12x) is not
     judged. A line carrying "# noqa" is left alone, as pycodestyle does. */
  var PEP8_KEYWORDS = ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class",
    "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import",
    "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"];
  var PEP8_SPACED = ["**=", "//=", ">>=", "<<=", ":=", "->", "==", "!=", "<=", ">=", "+=", "-=", "*=", "/=",
    "%=", "&=", "|=", "^=", "@=", "=", "<", ">"];
  var PEP8_OTHER = ["**", "//", "<<", ">>"];

  /* the text with every string's inside masked ("x"), quotes kept, comments
     cut out and remembered, and the bracket depth where each line starts */
  function pep8Scan(src) {
    var raw = String(src || "").replace(/\r\n?/g, "\n").split("\n");
    var code = [], comment = [], depthAt = [], depth = 0, q = null;
    for (var n = 0; n < raw.length; n++) {
      var l = raw[n], out = "", c = -1;
      depthAt.push(depth);
      for (var i = 0; i < l.length; i++) {
        var ch = l[i];
        if (q) {
          if (ch === "\\") { out += "xx".slice(0, Math.min(2, l.length - i)); i++; continue; }
          if (l.substr(i, q.length) === q) { out += q; i += q.length - 1; q = null; continue; }
          out += "x";
          continue;
        }
        if (ch === "#") { c = i; break; }
        if (ch === '"' || ch === "'") {
          q = l.substr(i, 3) === ch + ch + ch ? ch + ch + ch : ch;
          out += q; i += q.length - 1;
          continue;
        }
        if ("([{".indexOf(ch) >= 0) depth++;
        else if (")]}".indexOf(ch) >= 0) depth = Math.max(0, depth - 1);
        out += ch;
      }
      if (q && q.length === 1 && !/\\$/.test(l)) q = null;   /* a one-quote string ends with its line */
      code.push(out);
      comment.push(c);
    }
    return { raw: raw, code: code, comment: comment, depthAt: depthAt };
  }

  function pep8Indent(l) { var m = /^[ \t]*/.exec(l)[0]; return m.replace(/\t/g, "        ").length; }

  function lcPep8(src, opts) {
    opts = opts || {};
    var maxLen = parseInt(opts.max_line_length, 10) || 79;
    var ignore = (opts.ignore || []).map(String);
    var s = pep8Scan(src), raw = s.raw, code = s.code, probs = [];
    /* a file ends with its newline: the editor's last line is not a blank one */
    var total = raw.length;
    if (total > 1 && raw[total - 1] === "") total--;
    function add(line, col, codeId, text) {
      if (/#\s*noqa\b/i.test(raw[line - 1] || "")) return;
      for (var k = 0; k < ignore.length; k++) if (ignore[k] && codeId.indexOf(ignore[k]) === 0) return;
      probs.push({ line: line, col: col, code: codeId, text: text });
    }
    function chars(l) { return Array.from ? Array.from(l).length : l.length; }

    /* ── physical lines ── */
    for (var n = 0; n < total; n++) {
      var l = raw[n], ln = n + 1;
      var len = chars(l);
      if (len > maxLen) {
        var chunks = l.trim().split(/\s+/);
        if (!(chunks.length === 2 && chunks[0] === "#" && len - chars(chunks[1]) < maxLen - 7))
          add(ln, maxLen + 1, "E501", "line too long (" + len + " > " + maxLen + " characters)");
      }
      var stripped = l.replace(/[ \t\v\f]+$/, "");
      if (stripped !== l) {
        if (!stripped) add(ln, 1, "W293", "blank line contains whitespace");
        else add(ln, chars(stripped) + 1, "W291", "trailing whitespace");
      }
      /* comments */
      var c = s.comment[n];
      if (c >= 0) {
        var text = l.slice(c).replace(/\s+$/, ""), before = l.slice(0, c);
        var sp = text.indexOf(" "), symbol = sp < 0 ? text : text.slice(0, sp), rest = sp < 0 ? "" : text.slice(sp + 1);
        var badPrefix = (symbol === "#" || symbol === "#:") ? "" : (symbol.replace(/^#+/, "").slice(0, 1) || "#");
        if (before.trim()) {
          if (!/  $/.test(before) || /\t/.test(before.slice(-2)))
            add(ln, chars(before.replace(/\s+$/, "")) + 1, "E261", "at least two spaces before inline comment");
          if (badPrefix || /^[ \t]/.test(rest))
            add(ln, chars(before) + 1, "E262", "inline comment should start with '# '");
        } else if (badPrefix && (badPrefix !== "!" || ln > 1)) {
          if (badPrefix !== "#") add(ln, chars(before) + 1, "E265", "block comment should start with '# '");
          else if (rest) add(ln, chars(before) + 1, "E266", "too many leading '#' for block comment");
        }
      }
    }
    if (total > 0 && !raw[total - 1].trim()) {
      var last = total;
      add(last, 1, "W391", "blank line at end of file");
    }

    /* ── logical lines: a statement and its continuation lines ── */
    var logical = [], cur = null;
    for (var m = 0; m < total; m++) {
      var t = code[m];
      if (!cur) {
        if (!t.trim()) {
          /* a blank line, or a comment-only line */
          logical.push({ kind: s.comment[m] >= 0 ? "comment" : "blank", line: m + 1 });
          continue;
        }
        cur = { kind: "code", line: m + 1, end: m + 1, indent: pep8Indent(raw[m]), text: t.trim() };
      } else {
        cur.text += " " + t.trim();
        cur.end = m + 1;
      }
      var nextDepth = m + 1 < s.depthAt.length ? s.depthAt[m + 1] : 0;
      var inString = m + 1 < code.length && code[m + 1] !== undefined && pep8OpenString(code.slice(cur.line - 1, m + 1).join("\n"));
      if (nextDepth === 0 && !/\\$/.test(t) && !inString) { logical.push(cur); cur = null; }
    }
    if (cur) logical.push(cur);

    var prev = null, prevUnindented = "", blankRuns = [0], seenCode = false, seenNonImport = false;
    logical.forEach(function (lg) {
      if (lg.kind === "blank") { blankRuns[blankRuns.length - 1]++; return; }
      if (lg.kind === "comment") { blankRuns.push(0); return; }
      var blankLines = blankRuns[blankRuns.length - 1];
      var blankBefore = Math.max.apply(null, blankRuns);
      blankRuns = [0];
      var t = lg.text, ind = lg.indent, ln = lg.line;
      var top = /^(async\s+def\s|def\s|class\s|@)/.test(t);
      /* blank lines, pycodestyle's blank_lines() */
      if (!prev) {
        if (blankBefore >= 2 && top) { /* no complaint for the first line */ }
      } else if (/^@/.test(prev.text)) {
        if (blankLines) add(ln, ind + 1, "E304", "blank lines found after function decorator (" + blankLines + ")");
      } else if (blankLines > 2 || (ind && blankLines === 2)) {
        add(ln, ind + 1, "E303", "too many blank lines (" + blankLines + ")");
      } else if (top) {
        if (ind) {
          if (!(blankBefore === 1 || prev.indent < ind || /^[uUbBrR]*["']/.test(prev.text))) {
            var nested = false;
            for (var k = ln - 2; k >= 0; k--) {
              if (raw[k].trim() && !/^\s*#/.test(raw[k]) && pep8Indent(raw[k]) < ind) {
                nested = /^\s*(async\s+)?def\s/.test(raw[k]);
                if (nested || pep8Indent(raw[k]) === 0) break;
              }
            }
            if (nested) add(ln, ind + 1, "E306", "expected 1 blank line before a nested definition, found 0");
            else add(ln, ind + 1, "E301", "expected 1 blank line, found 0");
          }
        } else if (blankBefore !== 2) {
          add(ln, 1, "E302", "expected 2 blank lines, found " + blankBefore);
        }
      } else if (!ind && blankBefore !== 2 && /^(def|class)\s/.test(prevUnindented)) {
        add(ln, 1, "E305", "expected 2 blank lines after class or function definition, found " + blankBefore);
      }
      /* indentation */
      if (ind % 4) add(ln, ind + 1, "E111", "indentation is not a multiple of 4");
      else if (prev && /:$/.test(prev.text) && ind > prev.indent + 4) add(ln, ind + 1, "E117", "over-indented");
      /* imports */
      if (/^import\s/.test(t)) {
        var comma = code[ln - 1].indexOf(",");
        if (comma >= 0 && code[ln - 1].slice(0, comma).indexOf(";") < 0) add(ln, comma + 1, "E401", "multiple imports on one line");
      }
      if (!ind) {
        if (/^(import|from)\s/.test(t)) {
          if (seenNonImport) add(ln, 1, "E402", "module level import not at top of file");
        } else if (!/^[uUbBrR]*["']/.test(t) && !/^(try|except|else|finally|with|if|elif)\b/.test(t) &&
                   !/^__\w+__\s*(:[^=]*)?=/.test(t)) {
          seenNonImport = true;
        }
      }
      prev = lg;
      if (!ind) prevUnindented = t;
      seenCode = true;
    });

    /* ── tokens, line by line, on the masked code ── */
    var defLine = false;
    for (var p = 0; p < total; p++) {
      var line = code[p], lnum = p + 1, depth = s.depthAt[p];
      var firstCode = /^\s*/.exec(line)[0].length;
      var startsLogical = depth === 0 && (p === 0 || !/\\$/.test(code[p - 1] || ""));
      if (startsLogical) defLine = /^\s*(async\s+)?def\s/.test(line);
      var annotated = [];   /* per depth: an annotation ':' since the last ',' or opener */
      var headerColon = -1, compound = startsLogical && /^\s*(if|elif|else|for|while|try|except|finally|with|def|class|async)\b/.test(line);
      for (var i = 0; i < line.length; i++) {
        var ch = line[i];
        if (ch === '"' || ch === "'") {
          /* skip a masked string: its quotes and x's */
          var j = i + 1;
          while (j < line.length && line[j] !== ch) j++;
          i = j;
          continue;
        }
        if ("([{".indexOf(ch) >= 0) {
          depth++; annotated[depth] = false;
          if (line[i + 1] === " " && line.slice(i + 1).trim()) add(lnum, i + 2, "E201", "whitespace after '" + ch + "'");
          /* E211: name (  */
          if (ch !== "{" && i > 0 && line[i - 1] === " ") {
            var w = /([A-Za-z_][A-Za-z0-9_]*|[)\]}])\s+$/.exec(line.slice(0, i));
            if (w && PEP8_KEYWORDS.indexOf(w[1]) < 0 && !/\bclass\s+$/.test(line.slice(0, w.index)))
              add(lnum, w.index + w[1].length + 1, "E211", "whitespace before '" + ch + "'");
          }
          continue;
        }
        if (")]}".indexOf(ch) >= 0) {
          if (i > firstCode && line[i - 1] === " ") {
            var k2 = i - 1;
            while (k2 > 0 && line[k2 - 1] === " ") k2--;
            if (k2 > firstCode && line[k2 - 1] !== ",") add(lnum, k2 + 1, "E202", "whitespace before '" + ch + "'");
          }
          depth = Math.max(0, depth - 1);
          continue;
        }
        if (ch === ",") {
          if (depth > 0) annotated[depth] = false;
          if (i > 0 && line[i - 1] === " " && i > firstCode) {
            var k3 = i - 1; while (k3 > 0 && line[k3 - 1] === " ") k3--;
            add(lnum, k3 + 1, "E203", "whitespace before ','");
          }
          var nx = line[i + 1];
          if (nx !== undefined && nx !== " " && nx !== "\t" && ")]".indexOf(nx) < 0) add(lnum, i + 1, "E231", "missing whitespace after ','");
          continue;
        }
        if (ch === ";") {
          var after = line.slice(i + 1).trim();
          if (after) add(lnum, i + 1, "E702", "multiple statements on one line (semicolon)");
          else add(lnum, i + 1, "E703", "statement ends with a semicolon");
          continue;
        }
        /* operators: longest first */
        var op = null;
        for (var o = 0; o < PEP8_SPACED.length; o++) if (line.substr(i, PEP8_SPACED[o].length) === PEP8_SPACED[o]) { op = PEP8_SPACED[o]; break; }
        if (!op) {
          for (var o2 = 0; o2 < PEP8_OTHER.length; o2++) if (line.substr(i, PEP8_OTHER[o2].length) === PEP8_OTHER[o2]) { i += PEP8_OTHER[o2].length - 1; break; }
          if (ch === ":") {
            if (depth > 0) { if (defLine && depth === 1) annotated[depth] = true; continue; }
            if (compound && headerColon < 0) headerColon = i;
            if (i > firstCode && line[i - 1] === " ") {
              var k4 = i - 1; while (k4 > 0 && line[k4 - 1] === " ") k4--;
              add(lnum, k4 + 1, "E203", "whitespace before ':'");
            }
          }
          continue;
        }
        var end = i + op.length, before1 = line[i - 1], after1 = line[end];
        if (op === "=" && depth > 0) {
          if (annotated[depth]) {
            if (before1 !== " ") add(lnum, i + 1, "E252", "missing whitespace around parameter equals");
            if (after1 !== " ") add(lnum, end + 1, "E252", "missing whitespace around parameter equals");
          } else {
            if (before1 === " ") { var k5 = i - 1; while (k5 > 0 && line[k5 - 1] === " ") k5--; add(lnum, k5 + 1, "E251", "unexpected spaces around keyword / parameter equals"); }
            if (after1 === " ") add(lnum, end + 1, "E251", "unexpected spaces around keyword / parameter equals");
          }
          i = end - 1;
          continue;
        }
        if (before1 !== " " && before1 !== "\t") add(lnum, i + 1, "E225", "missing whitespace around operator");
        else if (after1 !== " " && after1 !== "\t" && after1 !== undefined) add(lnum, end + 1, "E225", "missing whitespace around operator");
        else {
          if (line.substr(i - 2, 2) === "  " && i - 2 >= firstCode) { var k6 = i - 1; while (k6 > firstCode && line[k6 - 1] === " ") k6--; add(lnum, k6 + 1, "E221", "multiple spaces before operator"); }
          if (line.substr(end, 2) === "  " && line.slice(end).trim()) add(lnum, end + 1, "E222", "multiple spaces after operator");
        }
        i = end - 1;
      }
      /* a one-line def is E704, which pycodestyle ignores by default */
      if (compound && headerColon >= 0 && line.slice(headerColon + 1).trim() && !/^\s*(async\s+)?def\b/.test(line))
        add(lnum, headerColon + 1, "E701", "multiple statements on one line (colon)");
      /* keywords */
      var kw = /\b(if|elif|while|not|and|or|in|return|assert|del|yield|import|from|is|for|with|except|raise)\(/g, km;
      while ((km = kw.exec(line))) {
        if (km.index > 0 && /[\w.]/.test(line[km.index - 1])) continue;
        add(lnum, km.index + km[1].length + 1, "E275", "missing whitespace after keyword");
      }
      /* comparisons to singletons */
      var cmp = /(\bNone|\bFalse|\bTrue)?\s*([=!]=)\s*(None|False|True)?\b/g, cm;
      while ((cm = cmp.exec(line))) {
        var single = cm[1] || cm[3];
        if (!single || (cm[1] && cm[3])) { if (cm[0].length === 0) cmp.lastIndex++; continue; }
        var opIdx = cm.index + cm[0].indexOf(cm[2]), neg = cm[2] === "!=";
        if (single === "None") add(lnum, opIdx + 1, "E711", "comparison to None should be 'if cond is " + (neg ? "not " : "") + "None:'");
        else {
          var nonzero = (single === "True") !== neg;
          add(lnum, opIdx + 1, "E712", "comparison to " + single + " should be 'if cond is " + (neg ? "not " : "") + single + ":' or 'if " + (nonzero ? "" : "not ") + "cond:'");
        }
      }
      /* ambiguous names */
      var amb = /^\s*(?:for\s+)?([lOI])\s*(=(?!=)|:|\s+in\b)/.exec(line);
      if (amb) add(lnum, line.indexOf(amb[1], /^\s*/.exec(line)[0].length) + 1, "E741", "ambiguous variable name '" + amb[1] + "'");
    }

    probs.sort(function (a, b) { return a.line - b.line || a.col - b.col; });
    return probs;
  }

  /* is a string still open at the end of these masked lines? */
  function pep8OpenString(text) {
    var q = null;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (q) { if (text.substr(i, q.length) === q) { i += q.length - 1; q = null; } continue; }
      if (ch === '"' || ch === "'") { q = text.substr(i, 3) === ch + ch + ch ? ch + ch + ch : ch; i += q.length - 1; }
      if (ch === "\n" && q && q.length === 1) q = null;
    }
    return !!(q && q.length === 3);
  }

  /* pycodestyle's report: path:line:col: CODE text, one per issue */
  function lcPep8Report(src, opts) {
    opts = opts || {};
    var file = opts.file || "main.py";
    var probs = lcPep8(src, opts), counters = {};
    probs.forEach(function (p) { counters[p.code] = (counters[p.code] || 0) + 1; });
    return {
      lines: probs.map(function (p) { return file + ":" + p.line + ":" + p.col + ": " + p.code + " " + p.text; }),
      total: probs.length, counters: counters, problems: probs
    };
  }

  /* pycodestyle.StyleGuide(...).check_files([...]) from Python: the program
     being run, under each path it was given */
  window.lcPep8Run = function (json) {
    var a = {};
    try { a = JSON.parse(String(json)); } catch (e) { }
    var paths = a.paths && a.paths.length ? a.paths : [window._lcPyFile || "main.py"];
    var lines = [], total = 0, counters = {};
    paths.forEach(function (p) {
      var r = lcPep8Report(window._lcPySrc || "", { file: String(p), max_line_length: a.max_line_length, ignore: a.ignore || [] });
      lines = lines.concat(r.lines); total += r.total;
      Object.keys(r.counters).forEach(function (k) { counters[k] = (counters[k] || 0) + r.counters[k]; });
    });
    return JSON.stringify({ lines: lines, total: total, counters: counters });
  };

  /* ── the Python side ──────────────────────────────────────────────── */
  window.LC_PY_SHIM = [
    "import sys",
    "import json as _lc_json",
    "import js as _lc_js",
    "def _lc_docs():",
    "    try:",
    "        return _lc_json.loads(str(_lc_js.window._lcPyDocsJson))",
    "    except Exception:",
    "        return {'file': 'main.py', 'module': None, 'items': []}",
    "def _lc_find(d, dotted, obj):",
    "    for it in d['items']:",
    "        if it['name'] == dotted:",
    "            return it",
    "    n = getattr(obj, '__name__', None)",
    "    if n is None and obj is not None and not isinstance(obj, (int, float, str, bool, list, dict, tuple)):",
    "        n = type(obj).__name__",
    "    last = dotted.split('.')[-1] if dotted else n",
    "    for want in (n, last):",
    "        if not want:",
    "            continue",
    "        for it in d['items']:",
    "            if it['name'] == want:",
    "                return it",
    "        hits = [it for it in d['items'] if it['name'].endswith('.' + want)]",
    "        if len(hits) == 1:",
    "            return hits[0]",
    "    return None",
    "def _lc_doc(obj, dotted=''):",
    "    it = _lc_find(_lc_docs(), dotted, obj)",
    "    if it is not None:",
    "        return it['doc']",
    "    try:",
    "        return obj.__doc__",
    "    except Exception:",
    "        return None",
    "try:",
    "    _lc_help_orig",
    "except NameError:",
    "    _lc_help_orig = help",
    "def help(obj=None):",
    "    d = _lc_docs()",
    "    it = _lc_find(d, '', obj) if obj is not None else None",
    "    if it is None:",
    "        return _lc_help_orig() if obj is None else _lc_help_orig(obj)",
    "    def _ind(text, pre):",
    "        return '\\n'.join((pre + l) if l else pre.rstrip() for l in text.split('\\n'))",
    "    if it['kind'] == 'class':",
    "        print('Help on class ' + it['short'] + ' in module __main__:\\n')",
    "        bases = ', '.join(it.get('bases') or []) or 'builtins.object'",
    "        print('class ' + it['short'] + '(' + bases + ')')",
    "        init = [m for m in d['items'] if m['name'] == it['name'] + '.__init__']",
    "        if init:",
    "            sig = init[0]['sig']",
    "            print(' |  ' + it['short'] + sig[len('__init__'):].replace('(self, ', '(').replace('(self)', '()'))",
    "            print(' |')",
    "        if it['doc']:",
    "            print(_ind(it['doc'], ' |  '))",
    "            print(' |')",
    "        meths = [m for m in d['items'] if m['kind'] == 'method' and m['name'].rsplit('.', 1)[0] == it['name']]",
    "        if meths:",
    "            print(' |  Methods defined here:')",
    "            print(' |')",
    "            for m in sorted(meths, key=lambda m: m['short']):",
    "                print(' |  ' + m['sig'])",
    "                if m['doc']:",
    "                    print(_ind(m['doc'], ' |      '))",
    "                print(' |')",
    "        return",
    "    print('Help on function ' + it['short'] + ' in module __main__:\\n')",
    "    print(it['sig'])",
    "    if it['doc']:",
    "        print(_ind(it['doc'], '    '))",
    "    print()",
    "def _lc_dt_exec(src, ns):",
    "    _lc_js.window._lcMpyCap = ''",
    "    exc = None",
    "    try:",
    "        try:",
    "            code = compile(src, '<doctest>', 'eval')",
    "        except SyntaxError:",
    "            code = None",
    "        if code is None:",
    "            exec(src, ns)",
    "        else:",
    "            v = eval(code, ns)",
    "            if v is not None:",
    "                print(repr(v))",
    "    except Exception as e:",
    "        exc = e",
    "    got = str(_lc_js.window._lcMpyCap)",
    "    _lc_js.window._lcMpyCap = None",
    "    return got, exc",
    "def _lc_dt_exc_line(e):",
    "    m = str(e)",
    "    return type(e).__name__ + (': ' + m if m else '')",
    "def _lc_dt_check(ex, ns):",
    "    got, exc = _lc_dt_exec(ex['run'], ns)",
    "    want = ex['want']",
    "    norm = lambda s: '\\n'.join(l.rstrip() for l in s.rstrip('\\n').split('\\n'))",
    "    if exc is not None:",
    "        line = _lc_dt_exc_line(exc)",
    "        if want.startswith('Traceback (most recent call last)'):",
    "            last = [l for l in want.split('\\n') if l.strip()][-1].strip()",
    "            return last == line or last == type(exc).__name__, got, line",
    "        return False, got, line",
    "    return norm(got) == norm(want), got, None",
    "def _lc_dt_items():",
    "    d = _lc_docs()",
    "    items = []",
    "    if d.get('module') is not None:",
    "        items.append(('__main__', d['module']['examples']))",
    "    for it in d['items']:",
    "        if it['doc'] is not None and not it.get('nested'):",
    "            items.append(('__main__.' + it['name'], it['examples']))",
    "    return d, items",
    "def _lc_dt_rows(base=None):",
    "    d, items = _lc_dt_items()",
    "    g = globals() if base is None else base",
    "    rows = []",
    "    for name, exs in items:",
    "        ns = dict(g)",
    "        for ex in exs:",
    "            ok, got, err = _lc_dt_check(ex, ns)",
    "            rows.append({'line': ex['line'], 'source': ex['source'], 'want': ex['want'], 'got': got.rstrip('\\n'), 'err': err, 'ok': ok})",
    "    return _lc_json.dumps(rows)",
    "def _lc_dt_pad(src):",
    "    ns = dict(globals())",
    "    ns['__name__'] = 'pad'",
    "    ns['input'] = lambda *a: ''",
    "    _lc_js.window._lcMpyCap = ''",
    "    try:",
    "        exec(src, ns)",
    "    except Exception as e:",
    "        return _lc_json.dumps({'error': _lc_dt_exc_line(e)})",
    "    finally:",
    "        _lc_js.window._lcMpyCap = None",
    "    return _lc_dt_rows(ns)",
    "class TestResults:",
    "    def __init__(self, failed, attempted):",
    "        self.failed = failed",
    "        self.attempted = attempted",
    "    def __repr__(self):",
    "        return 'TestResults(failed=' + str(self.failed) + ', attempted=' + str(self.attempted) + ')'",
    "    def __iter__(self):",
    "        return iter((self.failed, self.attempted))",
    "    def __getitem__(self, i):",
    "        return (self.failed, self.attempted)[i]",
    "def _lc_testmod(m=None, name=None, globs=None, verbose=None, report=True, **kw):",
    "    d, items = _lc_dt_items()",
    "    g = globals()",
    "    star = '*' * 70",
    "    def _ind(text):",
    "        return '\\n'.join('    ' + l for l in text.split('\\n'))",
    "    s = lambda n, w: str(n) + ' ' + w + ('' if n == 1 else 's')",
    "    tried = failed = 0",
    "    summary = []",
    "    for name, exs in items:",
    "        ns = dict(g)",
    "        f = 0",
    "        for ex in exs:",
    "            if verbose:",
    "                print('Trying:')",
    "                print(_ind(ex['source']))",
    "                if ex['want']:",
    "                    print('Expecting:')",
    "                    print(_ind(ex['want']))",
    "                else:",
    "                    print('Expecting nothing')",
    "            ok, got, err = _lc_dt_check(ex, ns)",
    "            if ok:",
    "                if verbose:",
    "                    print('ok')",
    "                continue",
    "            f += 1",
    "            print(star)",
    "            print('File \"' + d['file'] + '\", line ' + str(ex['line']) + ', in ' + name)",
    "            print('Failed example:')",
    "            print(_ind(ex['source']))",
    "            if err is not None:",
    "                print('Exception raised:')",
    "                print(_ind('Traceback (most recent call last):\\n  ...\\n' + err))",
    "            else:",
    "                print('Expected:' if ex['want'] else 'Expected nothing')",
    "                if ex['want']:",
    "                    print(_ind(ex['want']))",
    "                print('Got:' if got.strip() else 'Got nothing')",
    "                if got.strip():",
    "                    print(_ind(got.rstrip('\\n')))",
    "        tried += len(exs)",
    "        failed += f",
    "        summary.append((name, len(exs), f))",
    "    if report:",
    "        summary.sort()",
    "        none = [x for x in summary if x[1] == 0]",
    "        good = [x for x in summary if x[1] and not x[2]]",
    "        bad = [x for x in summary if x[2]]",
    "        if verbose:",
    "            if none:",
    "                print(s(len(none), 'item') + ' had no tests:')",
    "                for x in none:",
    "                    print('    ' + x[0])",
    "            if good:",
    "                print(s(len(good), 'item') + ' passed all tests:')",
    "                for x in good:",
    "                    print(' %3d %s in %s' % (x[1], 'test' if x[1] == 1 else 'tests', x[0]))",
    "        if bad:",
    "            print(star)",
    "            print(s(len(bad), 'item') + ' had failures:')",
    "            for x in bad:",
    "                print(' %3d of %3d in %s' % (x[2], x[1], x[0]))",
    "        if verbose:",
    "            print(s(tried, 'test') + ' in ' + s(len(summary), 'item') + '.')",
    "            print(str(tried - failed) + ' passed.')",
    "            if failed:",
    "                print(str(failed) + ' failed.')",
    "        if failed:",
    "            print('***Test Failed*** ' + s(failed, 'failure') + '.')",
    "        elif verbose:",
    "            print('Test passed.')",
    "    return TestResults(failed, tried)",
    "class _LcModule:",
    "    pass",
    "doctest = _LcModule()",
    "doctest.testmod = _lc_testmod",
    "doctest.TestResults = TestResults",
    "sys.modules['doctest'] = doctest",
    "del doctest",
    "def _lc_mypy_run(args):",
    "    r = _lc_json.loads(str(_lc_js.window.lcDrMypyRun(_lc_json.dumps(list(args)))))",
    "    return (r['out'], r['err'], r['status'])",
    "_lc_mypy = _LcModule()",
    "_lc_mypy.api = _LcModule()",
    "_lc_mypy.api.run = _lc_mypy_run",
    "sys.modules['mypy'] = _lc_mypy",
    "sys.modules['mypy.api'] = _lc_mypy.api",
    "class _LcStyleReport:",
    "    def __init__(self, total, counters):",
    "        self.total_errors = total",
    "        self.counters = counters",
    "    def get_count(self, prefix=''):",
    "        return sum([v for k, v in self.counters.items() if k.startswith(prefix)])",
    "class _LcStyleGuide:",
    "    def __init__(self, *args, **kw):",
    "        self._kw = kw",
    "    def check_files(self, paths=None):",
    "        a = {'paths': list(paths or []), 'max_line_length': self._kw.get('max_line_length', 79), 'ignore': list(self._kw.get('ignore', None) or [])}",
    "        r = _lc_json.loads(str(_lc_js.window.lcPep8Run(_lc_json.dumps(a))))",
    "        for line in r['lines']:",
    "            print(line)",
    "        return _LcStyleReport(r['total'], r['counters'])",
    "_lc_pcs = _LcModule()",
    "_lc_pcs.StyleGuide = _LcStyleGuide",
    "sys.modules['pycodestyle'] = _lc_pcs"
  ].join("\n");

  /* before a program runs: its text, its name, its docstrings — and the
     Python names that read them. Returns the code to hand MicroPython. */
  window.lcPyBefore = function (mp, src, file) {
    var docs = lcPyDocs(src, file);
    window._lcPySrc = src;
    window._lcPyFile = file;
    window._lcPyDocsJson = JSON.stringify(docs);
    try { mp.runPython(window.LC_PY_SHIM); } catch (e) { if (window.console) console.warn("[lc pycheck]", e); }
    try {
      mp.runPython("__doc__ = " + JSON.stringify(docs.module ? docs.module.doc : null).replace(/^null$/, "None") +
                   "\n__file__ = " + JSON.stringify(file));
    } catch (e) { }
    return lcPyPrepare(src);
  };

  /* a pad's python fence, doctested on its own (Michel, 2026-10-26: "in the
     mdpad, I prefer not to add a if __main__ … and not to call explicitly
     doctest"): the fence runs in a namespace of its own (__name__ is not
     "__main__", input() answers ""), then every >>> example of its
     docstrings — the rows 🧪 Test shows, or {error} when the fence stops */
  window.lcPyDoctestFence = function (mp, code) {
    var keep = window._lcPyDocsJson;
    try {
      if (!mp._lcPyShim) { mp.runPython(window.LC_PY_SHIM); mp._lcPyShim = true; }
      window._lcPyDocsJson = JSON.stringify(lcPyDocs(code, "pad.py"));
      window._lcDtSrc = lcPyPrepare(code);
      window._lcDtRows = "[]";
      mp.runPython("import js as _lc_js\n_lc_js.window._lcDtRows = _lc_dt_pad(str(_lc_js.window._lcDtSrc))");
      return JSON.parse(String(window._lcDtRows));
    } catch (e) {
      return { error: String((e && e.message) || e).split("\n").filter(Boolean).pop() };
    } finally {
      window._lcPyDocsJson = keep;
    }
  };

  window.lcPyDocs = lcPyDocs;
  window.lcPyPrepare = lcPyPrepare;
  window.lcTypeLint = lcTypeLint;
  window.lcDrMypy = lcDrMypy;
  window.lcPep8 = lcPep8;
  window.lcPep8Report = lcPep8Report;
})();
</script>
