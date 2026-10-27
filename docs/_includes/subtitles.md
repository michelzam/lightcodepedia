{%- comment -%}
💬 subtitles.md — the run block's subtitles: what each part of the program
IS, said for a twelve-year-old. A small Python tokenizer tags every token
with a kind (a parameter, a default value, a type hint, a loop variable, a
call, a named argument…) and a one-line subtitle; pyrun.md paints them as
an overlay the reader hovers or taps. Michel, 2026-10-27: "tooltips in that
.run component to explicit what code parts are (variable, type, positional
or named param, default value, conditionals, etc), based on an on/off
option to add subtitles".
{%- endcomment -%}
<script>
(function () {
  if (window.lcSubtitles) return;
  var KW = {
    "def": "def — defines a function: a named recipe you can call later",
    "class": "class — defines a kind of object: its data and its functions (methods)",
    "return": "return — the function gives this value back and stops",
    "for": "for — repeats the block once for each item",
    "in": "in — the list (or string, or range) to go through",
    "while": "while — repeats the block as long as the condition is true",
    "if": "if — runs the block only when the condition is true",
    "elif": "elif — otherwise, if this other condition is true",
    "else": "else — otherwise",
    "import": "import — brings in a module (a toolbox) by name",
    "from": "from — the module the names come from",
    "as": "as — gives it a shorter name here",
    "True": "True — yes, a boolean value", "False": "False — no, a boolean value",
    "None": "None — no value at all",
    "and": "and — both must be true", "or": "or — one of them is enough", "not": "not — the opposite",
    "is": "is — the very same object?", "lambda": "lambda — a tiny function with no name",
    "with": "with — opens something and closes it for you at the end",
    "pass": "pass — do nothing (a placeholder)", "break": "break — leaves the loop now",
    "continue": "continue — skips to the next item", "try": "try — attempt this; errors go to except",
    "except": "except — what to do if that failed", "finally": "finally — runs in every case",
    "raise": "raise — signals an error", "yield": "yield — hands out one value and pauses",
    "global": "global — the variable outside the function", "del": "del — removes it",
    "assert": "assert — must be true, or the program stops here"
  };
  var BUILTIN = { print: "print — writes to the output", len: "len — how many items", range: "range — the numbers from 0 up to (not including) this one",
    str: "str — text", int: "int — a whole number", float: "float — a number with a decimal point", list: "list — an ordered collection, in [ ]",
    dict: "dict — pairs of key: value, in { }", tuple: "tuple — a fixed group of values, in ( )", bool: "bool — True or False",
    input: "input — asks the reader and waits for the answer", type: "type — what kind of value this is", isinstance: "isinstance — is it of this kind?",
    sorted: "sorted — a sorted copy", max: "max — the biggest", min: "min — the smallest", sum: "sum — adds them up", abs: "abs — without the sign",
    round: "round — to the nearest", enumerate: "enumerate — each item with its number", zip: "zip — pairs items from two lists",
    show: "show — draws the value as a card below", play: "play — plays a note, or a list of notes" };
  var OPS = { "=": "= assigns: the value on the right goes into the name on the left", "==": "== compares: are they equal?",
    "!=": "!= compares: are they different?", "<": "< less than", ">": "> greater than", "<=": "<= less or equal", ">=": ">= greater or equal",
    "+": "+ adds (or joins text and lists)", "-": "- subtracts", "*": "* multiplies (or repeats)", "/": "/ divides", "//": "// divides, whole part only",
    "%": "% the remainder", "**": "** to the power of", "+=": "+= adds to the variable", "-=": "-= subtracts from the variable",
    "->": "-> the return type hint: what the function gives back", ":": ": the block starts on the next line (indented)",
    ".": ". reaches inside: an attribute or a method", ",": ", separates items", "(": "( opens the parentheses", ")": ") closes them",
    "[": "[ a list, or an index: which item", "]": "]", "{": "{ a dict (key: value pairs) or a set", "}": "}", "@": "@ a decorator: wraps the function below" };
  var SUB = {
    fname: "the function's name — call it with ( )", cname: "the class's name — a new kind of object", parent: "the parent class: this one inherits its data and methods",
    param: "a parameter — a name for the value you pass in", param_default: "a parameter with a default value — used when you pass nothing for it",
    default: "the default value", hint: "a type hint — what kind of value is expected", rhint: "the return type hint — what the function gives back",
    loopvar: "the loop variable — takes each item in turn", assign: "a variable — a name for a value, set here", var: "a variable — a name for a value",
    call: "a function call — runs the function with these arguments", method: "a method call — asks the object to do something",
    attr: "an attribute — data kept inside the object", self: "self — the object itself, from inside its own class",
    pos: "a positional argument — passed in order", named: "a named argument — passed by name", kwname: "the argument's name",
    string: "a string — text, between quotes", fstring: "an f-string — the {…} parts are filled in with values",
    docstring: "a docstring — what the function does, and its >>> examples (🧪 Test runs them)",
    doctest: "a doctest example — the call after >>>, the expected result on the next line",
    number: "a number", comment: "a comment — a note for people, ignored by Python", decorator: "a decorator — changes the function below it",
    dunder: "a special method — Python calls it for you (here __init__ builds the object)", module: "a module — a toolbox of functions", slice: "a slice [start:stop:step] — a piece of the list; [::-1] is backwards"
  };
  var TOK = /(#.*)|("""[\s\S]*?"""|'''[\s\S]*?''')|([rbuf]{0,2}"(?:\\.|[^"\\\n])*"|[rbuf]{0,2}'(?:\\.|[^'\\\n])*')|(\d+\.?\d*(?:e[+-]?\d+)?)|([A-Za-z_][A-Za-z_0-9]*)|(->|\*\*|\/\/|==|!=|<=|>=|\+=|-=|\*=|\/=|[-+*\/%<>=:.,()\[\]{}@])|(\n)|(\s+)|(.)/g;
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function tokens(code) {
    var out = [], m;
    TOK.lastIndex = 0;
    while ((m = TOK.exec(code))) {
      var t = m[0];
      out.push({ t: t, k: m[1] ? "comment" : m[2] ? "tstring" : m[3] ? "string" : m[4] ? "number" : m[5] ? "name" : m[6] ? "op" : m[7] ? "nl" : m[8] ? "ws" : "other" });
    }
    return out;
  }
  /* one pass with a little memory: where we are in a def line, a for line, a call */
  function tag(toks) {
    var ctx = { def: 0, cls: false, forv: false, calls: [], stmtStart: true, afterDot: false, indentDoc: -1, prevSig: null, hintNext: false, paren: 0, defParen: -1 };
    function sig(i) { for (var j = i - 1; j >= 0; j--) if (toks[j].k !== "ws") return toks[j]; return null; }
    function nxt(i) { for (var j = i + 1; j < toks.length; j++) if (toks[j].k !== "ws") return toks[j]; return null; }
    /* a parameter's default may sit behind its type hint: name: int = 1 */
    function defaultFollows(i) {
      var depth = 0;
      for (var j = i + 1; j < toks.length; j++) {
        var t = toks[j];
        if (t.k === "ws") continue;
        if (t.k === "nl") return false;
        if (t.t === "[" || t.t === "(") { depth++; continue; }
        if (t.t === "]" || t.t === ")") { if (depth === 0) return false; depth--; continue; }
        if (depth) continue;
        if (t.t === "=") return true;
        if (t.t === ",") return false;
      }
      return false;
    }
    var lineStart = true, blockDoc = false;
    for (var i = 0; i < toks.length; i++) {
      var tk = toks[i], p = sig(i), n = nxt(i), s = null;
      if (tk.k === "nl") { lineStart = true; ctx.forv = false; if (ctx.paren === 0) { ctx.def = 0; ctx.defParen = -1; ctx.cls = false; } continue; }
      if (tk.k === "ws") continue;
      var atStart = lineStart; lineStart = false;
      if (tk.k === "comment") s = SUB.comment;
      else if (tk.k === "tstring") {
        s = (atStart && (blockDoc || p === null || (p.t === ":" ) || p.k === "nl")) ? SUB.docstring : SUB.string;
        if (s === SUB.docstring && /^\s*>>>/m.test(tk.t)) s = SUB.docstring;
      }
      else if (tk.k === "string") s = /^[rbu]*f/i.test(tk.t) ? SUB.fstring : SUB.string;
      else if (tk.k === "number") s = (p && p.t === "=" && ctx.defParen >= 0) ? SUB.default : (ctx.calls.length && !(p && p.t === "=")) ? SUB.pos : SUB.number;
      else if (tk.k === "op") {
        if (tk.t === "(") { ctx.paren++; if (p && p.k === "name" && (ctx.def === 2)) { ctx.defParen = ctx.paren; ctx.def = 3; } else if (p && p.k === "name") ctx.calls.push(ctx.paren); else if (ctx.cls) ctx.cls = "parent"; }
        if (tk.t === ")") { if (ctx.calls.length && ctx.calls[ctx.calls.length - 1] === ctx.paren) ctx.calls.pop(); if (ctx.defParen === ctx.paren) ctx.defParen = -1; ctx.paren--; }
        if (tk.t === "[" && n && (n.t === ":" || (nxt(i + 1) && nxt(i + 1).t === ":"))) s = SUB.slice;
        else if (tk.t === ":" && ctx.defParen >= 0) { s = "the type hint follows"; ctx.hintNext = true; }
        else if (tk.t === "=" && ctx.calls.length && p && p.k === "name") s = "= gives the named argument its value";
        else if (tk.t === "=" && ctx.defParen >= 0) s = "= the default value follows";
        else if (tk.t === "->") { s = OPS["->"]; ctx.hintNext = "r"; }
        else s = OPS[tk.t] || null;
        if (tk.t === "@" && atStart) s = SUB.decorator;
        ctx.afterDot = tk.t === ".";
        if (tk.t !== ".") { /* keep */ }
      }
      else if (tk.k === "name") {
        var w = tk.t;
        if (ctx.hintNext) { s = ctx.hintNext === "r" ? SUB.rhint : SUB.hint; if (!(n && (n.t === "." || n.t === "["))) ctx.hintNext = false; }
        else if (KW[w]) { s = KW[w]; if (w === "def") ctx.def = 1; if (w === "class") ctx.cls = true; if (w === "for") ctx.forv = true; if (w === "in") ctx.forv = false; if (w === "import" || w === "from") ctx.imp = true; }
        else if (ctx.def === 1) { s = /^__\w+__$/.test(w) ? SUB.dunder : SUB.fname; ctx.def = 2; }
        else if (ctx.cls === true && p && p.t === "class") s = SUB.cname;
        else if (ctx.cls === "parent") s = SUB.parent;
        else if (ctx.defParen >= 0 && ctx.paren === ctx.defParen) { s = w === "self" ? SUB.self : defaultFollows(i) ? SUB.param_default : SUB.param; }
        else if (ctx.forv) s = SUB.loopvar;
        else if (ctx.afterDot) s = (n && n.t === "(") ? SUB.method : SUB.attr;
        else if (w === "self") s = SUB.self;
        else if (n && n.t === "(") s = BUILTIN[w] ? BUILTIN[w] + " (a built-in call)" : SUB.call;
        else if (ctx.calls.length && n && n.t === "=") s = SUB.kwname;
        else if (ctx.calls.length) s = (BUILTIN[w] || SUB.pos);
        else if (atStart && n && (n.t === "=" || n.t === ":" || n.t === "+=" || n.t === "-=")) s = SUB.assign;
        else if (ctx.imp) s = SUB.module;
        else s = BUILTIN[w] || SUB.var;
        ctx.afterDot = false;
      }
      if (tk.k !== "op") ctx.afterDot = false;
      if (tk.k === "nl") ctx.imp = false;
      tk.s = s;
      if (atStart) ctx.imp = false;
    }
    return toks;
  }
  /* THE COLOURS STAY UNDER THE CAPTIONS (Michel, 2026-10-27: "when the
     captions are on, the syntax should remain colored; bold for python
     keywords") — the same palette as the editor's, keywords bold */
  function colour(tk) {
    if (tk.k === "comment") return "lc-sub-comment";
    if (tk.k === "string" || tk.k === "tstring") return "lc-sub-string";
    if (tk.k === "number") return "lc-sub-number";
    if (tk.k === "op") return /^[.,:;()\[\]{}]$/.test(tk.t) ? "lc-sub-punct" : "lc-sub-op";
    if (tk.k === "name") {
      if (KW[tk.t]) return "lc-sub-kw";
      if (tk.s === SUB.fname || tk.s === SUB.cname || tk.s === SUB.dunder || tk.s === SUB.decorator) return "lc-sub-def";
      if (BUILTIN[tk.t] && (tk.s || "").indexOf(BUILTIN[tk.t]) === 0) return "lc-sub-builtin";
      if (tk.s === SUB.call || tk.s === SUB.method) return "lc-sub-call";
      if (/^[A-Z]/.test(tk.t)) return "lc-sub-type";
    }
    return "";
  }
  /* one <span class="lc-sub-line"> per line, its indent kept, a ▾ on a line
     that opens a block (def, class, for, if…) so the captioned program folds
     (Michel, 2026-10-27: "make the code foldable in caption_on mode") */
  function html(code) {
    var lines = [], cur = [];
    tag(tokens(code)).forEach(function (tk) {
      if (tk.k === "nl") { lines.push(cur.join("")); cur = []; return; }
      if (!tk.s || tk.k === "ws") { cur.push(esc(tk.t)); return; }
      var cls = colour(tk);
      /* a docstring spans lines: one span per line, so the lines stay in step with the program */
      tk.t.split("\n").forEach(function (piece, k) {
        if (k) { lines.push(cur.join("")); cur = []; }
        cur.push('<span class="lc-sub' + (cls ? " " + cls : "") + '" data-sub="' + esc(tk.s) + '" title="' + esc(tk.s) + '">' + esc(piece) + "</span>");
      });
    });
    lines.push(cur.join(""));
    var raw = code.split("\n"), out = [];
    function indentOf(l) { var m = /^[ \t]*/.exec(l); return m ? m[0].replace(/\t/g, "    ").length : 0; }
    for (var i = 0; i < lines.length; i++) {
      var text = raw[i] || "", ind = indentOf(text), opens = false;
      if (/:\s*(#.*)?$/.test(text) && text.trim()) {
        for (var j = i + 1; j < raw.length; j++) { if (!raw[j].trim()) continue; opens = indentOf(raw[j]) > ind; break; }
      }
      out.push('<span class="lc-sub-line" data-l="' + i + '" data-indent="' + ind + '"' + (text.trim() ? "" : ' data-blank="1"') + (opens ? ' data-opens="1"' : "") + ">" + lines[i] + "</span>");
    }
    return out.join("");          /* the lines are blocks: a newline between them was a line too (seen 2026-10-27) */
  }
  /* fold or unfold the block a line opens: the lines below it that are
     indented deeper. The sign lives in the gutter (Michel, 2026-10-27) */
  function fold(line) {
    if (!line || !line.classList.contains("lc-sub-line")) return false;
    var open = line.getAttribute("data-folded") !== "1", ind = parseInt(line.getAttribute("data-indent") || "0", 10);
    if (open) line.setAttribute("data-folded", "1"); else line.removeAttribute("data-folded");
    var el = line.nextElementSibling, n = 0;
    while (el && el.classList.contains("lc-sub-line")) {
      var blank = el.getAttribute("data-blank") === "1", deeper = parseInt(el.getAttribute("data-indent") || "0", 10) > ind;
      if (!blank && !deeper) break;
      el.classList.toggle("lc-sub-hidden", open); n++;
      el = el.nextElementSibling;
    }
    return n;
  }
  window.lcSubtitles = { html: html, fold: fold, tokens: function (c) { return tag(tokens(c)); } };
})();
</script>
