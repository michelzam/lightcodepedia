{%- comment -%}
PyRun — the in-browser Python family, activated from md + IAL.

  python code block + {: .run }     editor with ▶ Run, doctests, show.grid/form
  python code block + {: .repl }    interactive REPL
  {: .run silent="true" }           executes on load, renders nothing
  link + {: .button }               styled button; an adjacent {: .onclick }
                                    Python block becomes its click handler

MicroPython (lazy-loaded, ~300 KB) runs the editor; buttons run on the
shared page instance against the steps-runtime preamble. CPython's
f'{x = }' is rewritten before the code reaches it (desugarFstrings). Exposes
window.lcPyrun.attach for Liquid-rendered python_run.md blocks and
flushes their lcPyrunQueue.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-pyrun { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-pyrun-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrun-title .lc-pyrun-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: var(--lc-ink-mute, #616161); letter-spacing: 0.05em; }
.lc-pyrun textarea { display: block; width: 100%; box-sizing: border-box; border: none; outline: none; padding: 0.9em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; resize: vertical; background: #fafafa; color: #111; }
.lc-pyrun-editor { display: flex; background: #fafafa; align-items: stretch; }
.lc-pyrun-codewrap { position: relative; flex: 1; min-width: 0; }
.lc-pyrun-codewrap .lc-pyrun-code { flex: none; width: 100%; padding-left: 0.6em; }
.lc-pyrun-hl { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 0.9em 1em 0.9em 0.6em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; pointer-events: none; overflow: hidden; background: transparent; color: #111; white-space: pre-wrap; word-wrap: break-word; box-sizing: border-box; }
.lc-pyrun-hl code { font: inherit; background: transparent; padding: 0; color: inherit; display: block; will-change: transform; }
.lc-pyrun-codewrap .lc-pyrun-code { position: relative; background: transparent !important; color: transparent !important; caret-color: #111; }
.lc-pyrun-codewrap .lc-pyrun-code::selection { background: rgba(0, 102, 204, 0.18); color: transparent; }
.lc-pyrun .token.keyword, .lc-pyrun .token.boolean, .lc-pyrun .token.null { color: #cf222e; font-weight: 500; }
.lc-pyrun .token.string, .lc-pyrun .token.triple-quoted-string { color: #0a3069; }
.lc-pyrun .token.number { color: #0550ae; }
.lc-pyrun .token.comment { color: #59636e; font-style: italic; }
.lc-pyrun .token.function, .lc-pyrun .token.class-name, .lc-pyrun .token.builtin, .lc-pyrun .token.decorator { color: #8250df; }
.lc-pyrun .token.operator, .lc-pyrun .token.punctuation { color: #24292f; }
/* CODE DOES NOT WRAP (Michel, 2026-10-06/07). An overlay editor can only
   disagree with its caret where a line wraps, so a long line scrolls
   sideways instead; the overlay follows scrollLeft. By CSS alone: the
   first cut (wrap="off" + overflow:auto as well) left the editor
   read-only on the iPhone (WebKit), and this is the smallest piece.
   The gutter still measures rows through a mirror that copies the
   editor's white-space: true either way, one number per line. */
.lc-pyrun-code, .lc-pyrun-hl { white-space: pre; word-wrap: normal; overflow-wrap: normal; }
.lc-pyrun-mirror { position: absolute; top: 0; left: 0; visibility: hidden; pointer-events: none; box-sizing: border-box; margin: 0; }
.lc-pyrun-mirror div { min-height: 1.5em; }
.lc-pyrun-gutter { position: relative; overflow: hidden; background: #f3f4f6; border-right: 1px solid #e8e8e8; user-select: none; min-width: 2.5em; }
.lc-pyrun-gutter-inner { padding: 0.9em 0.5em 0.9em 0.6em; color: var(--lc-ink-mute, #616161); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; text-align: right; white-space: pre; pointer-events: none; will-change: transform; }
.lc-pyrun-bar { display: flex; align-items: center; gap: 0.6em; padding: 0.5em 0.9em; background: #f3f4f6; border-top: 1px solid #e0e0e0; }
.lc-pyrun-bar button { background: #0066cc; color: white; border: none; border-radius: 4px; padding: 0.35em 0.9em; cursor: pointer; font-size: 0.85em; font-weight: 500; }
.lc-pyrun-bar button:hover:not(:disabled) { background: #0052a3; }
.lc-pyrun-bar button:disabled { background: #888; cursor: progress; }
.lc-pyrun-bar .lc-pyrun-clear { background: #e5e5e5; color: #333; }
.lc-pyrun-bar .lc-pyrun-clear:hover:not(:disabled) { background: #d0d0d0; }
.lc-pyrun-bar .lc-pyrun-test { background: #3d7330; }
.lc-pyrun-bar .lc-pyrun-test:hover:not(:disabled) { background: #33641f; }
.lc-pyrun-bar .lc-pyrun-status { margin-left: auto; font-size: 0.78em; color: #666; }
.lc-pyrun-out { margin: 0; padding: 0.9em 1em; background: #1e1e1e; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; min-height: 2em; max-height: 300px; overflow-y: auto; }
.lc-pyrun-out.lc-empty { color: #888; font-style: italic; }
.lc-pyrun-out .lc-err { color: #ff6b6b; }
/* the question, and the line the reader answers on — a terminal's own look:
   the caret sits where the prompt ends, and Enter sends it */
.lc-pyrun-ask { display: inline; }
.lc-pyrun-ask-box { background: transparent; border: 0; border-bottom: 1px solid #4d4d4d;
  color: #9cdcfe; font: inherit; outline: none; min-width: 8em; padding: 0 0.15em; caret-color: #9cdcfe; }
.lc-pyrun-ask-box:focus { border-bottom-color: #9cdcfe; }
.lc-pyrun-view { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; padding: 0.9em 1em; background: #fafbfc; border-top: 1px solid #e0e0e0; }
.lc-pyrun-view:empty { display: none; }
.lc-pyrun-view .lc-rt-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8em 1em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-pyrun-view .lc-rt-card:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0,0,0,0.06); border-color: #0066cc; }
.lc-pyrun-view .lc-rt-card h3 { margin: 0 0 0.4em; font-size: 1em; color: #222; }
.lc-pyrun-view .lc-rt-card .lc-rt-row { margin: 0.15em 0; font-size: 0.88em; color: #444; }
.lc-pyrun-view .lc-rt-card .lc-rt-row b { color: #0066cc; margin-right: 0.4em; }
.lc-pyrun-view .lc-rt-card .lc-rt-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; color: #333; word-break: break-word; }
.lc-pyrun-bound { padding: 0.9em 1em; background: #fafbfc; border-bottom: 1px solid #d0d0d0; }
.lc-pyrun-bound:empty { display: none; }
.lc-pyrun-bound .lc-rt-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8em 1em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-pyrun-bound .lc-rt-card h3 { margin: 0 0 0.4em; font-size: 1em; color: #222; }
.lc-pyrun-bound .lc-rt-card .lc-rt-row { margin: 0.15em 0; font-size: 0.88em; color: #444; }
.lc-pyrun-bound .lc-rt-card .lc-rt-row b { color: #0066cc; margin-right: 0.4em; }
.lc-pyrun-bound .lc-rt-card .lc-rt-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; color: #333; word-break: break-word; }
.lc-pyrun-fold > summary { padding: 0.45em 0.9em; cursor: pointer; background: #f3f4f6; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; user-select: none; list-style: none; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrun-fold > summary::-webkit-details-marker { display: none; }
.lc-pyrun-fold > summary::before { content: "▶"; font-size: 0.7em; transition: transform 0.15s; color: #888; }
.lc-pyrun-fold[open] > summary::before { transform: rotate(90deg); }
.lc-pyrun-fold > summary:hover { background: #e8e9eb; }
.lc-pyrun-fold[open] > summary { border-bottom: 1px solid #d0d0d0; }
.lc-pyrun-tests { background: #fafbfc; border-top: 1px solid #e0e0e0; }
.lc-pyrun-tests:empty { display: none; }
.lc-pyrun-tests .lc-pyrun-test-summary { padding: 0.5em 0.9em; font-weight: 600; background: #f3f4f6; border-bottom: 1px solid #d0d0d0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #333; }
.lc-pyrun-tests .lc-pyrun-test-row { padding: 0.4em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; border-bottom: 1px solid #f0f0f0; white-space: pre-wrap; }
.lc-pyrun-tests .lc-pyrun-test-row:last-child { border-bottom: none; }
.lc-pyrun-tests .lc-pyrun-test-pass { color: #2a7a2a; }
.lc-pyrun-tests .lc-pyrun-test-fail { color: #b00; background: #fff5f5; }
.lc-pyrun-tests .lc-pyrun-test-empty { color: var(--lc-ink-mute, #616161); font-style: italic; }

.lc-pyrepl { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #1e1e1e; }
.lc-pyrepl-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrepl-title .lc-pyrepl-reset { margin-left: auto; background: #e5e5e5; color: #333; border: none; border-radius: 4px; padding: 0.15em 0.55em; cursor: pointer; font-size: 0.95em; line-height: 1; }
.lc-pyrepl-title .lc-pyrepl-reset:hover { background: #d0d0d0; }
.lc-pyrepl-title .lc-pyrepl-status { font-size: 0.78em; color: #888; font-style: italic; margin-left: 0.5em; }
.lc-pyrepl-transcript { margin: 0; padding: 0.9em 1em; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; min-height: 4em; max-height: 320px; overflow-y: auto; }
.lc-pyrepl-transcript:empty::before { content: "type a Python expression below and press Enter"; color: #888; font-style: italic; }
.lc-pyrepl-transcript .lc-pyrepl-prompt-line { color: #6aa84f; }
.lc-pyrepl-transcript .lc-pyrepl-err { color: #ff6b6b; }
.lc-pyrepl-input-row { display: flex; align-items: center; gap: 0.5em; padding: 0.5em 1em; background: #1e1e1e; border-top: 1px solid #333; }
.lc-pyrepl-marker { color: #6aa84f; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; font-weight: bold; user-select: none; }
.lc-pyrepl-input { flex: 1; min-width: 0; background: transparent; border: none; outline: none; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; padding: 0; }
.lc-pyrepl-input:disabled { color: #666; }

.button { display: inline-block; padding: 0.5em 1.2em; background: #0066cc; color: white !important; text-decoration: none !important; border-radius: 4px; font-weight: 600; transition: background 0.15s; margin: 0.2em 0.3em 0.2em 0; }
/* safety net: if {: .button } is written on its own line it becomes a block IAL
   on the wrapping <p>, leaving the inner link the site colour (low contrast);
   force the inner link readable so the button works either way */
.button a { color: #fff !important; }
.button:hover { background: #0052a3; }
.button[kind="secondary"], .button-secondary { background: #6c757d; } .button[kind="secondary"]:hover, .button-secondary:hover { background: #5a6268; }
.button[kind="success"], .button-success { background: #28a745; } .button[kind="success"]:hover, .button-success:hover { background: #1e7e34; }
.button[kind="danger"], .button-danger { background: #dc3545; } .button[kind="danger"]:hover, .button-danger:hover { background: #bd2130; }
.button[kind="outline"], .button-outline { background: transparent; color: #0066cc !important; border: 2px solid #0066cc; padding: calc(0.5em - 2px) calc(1.2em - 2px); }
.button[kind="outline"]:hover, .button-outline:hover { background: #0066cc; color: white !important; }
</style>

<script>
(function () {
  if (window._lcPyrunReady) return;
  window._lcPyrunReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  /* shared loaders from code_chrome.md (parsed earlier — topbar include) */
  var loadPrism  = window.lcLoadPrism;
  var loadJsYaml = window.lcLoadJsYaml;

  function parseDoctests(source) {
    var tests = [];
    var lines = source.split("\n");
    var inDoc = false, quote = "", pending = null;
    for (var i = 0; i < lines.length; i++) {
      var L = lines[i];
      if (!inDoc) {
        var dm = L.match(/("""|''')/);
        if (dm) {
          quote = dm[1];
          var after = L.substring(L.indexOf(quote) + 3);
          // Skip single-line docstrings like """one-liner"""
          if (after.indexOf(quote) >= 0) continue;
          inDoc = true;
        }
        continue;
      }
      // Inside a docstring
      if (L.indexOf(quote) >= 0) {
        if (pending) { tests.push(pending); pending = null; }
        inDoc = false;
        continue;
      }
      var em = L.match(/^\s*>>>\s*(.*)$/);
      if (em) {
        if (pending) { tests.push(pending); }
        pending = { expr: em[1], expected: "", lineno: i + 1 };
        continue;
      }
      if (pending) {
        var t = L.replace(/^\s+/, "").replace(/\s+$/, "");
        if (t === "" || /^\s*>>>/.test(L)) {
          tests.push(pending);
          pending = null;
          if (em) { pending = { expr: em[1], expected: "", lineno: i + 1 }; }
        } else if (pending.expected === "") {
          pending.expected = t;
        }
      }
    }
    if (pending) tests.push(pending);
    return tests;
  }

  /* ONE MicroPython per page. The wasm build is a singleton: a second
     loadMicroPython silently kills the first (every later call throws
     "NULL object"). Features, editors, cells, buttons, diagrams and the
     x-ray all share THIS interpreter; stdout/stderr route through a
     swappable hook — runPython is synchronous, so a consumer sets the
     hook, runs, and clears it, atomically. */
  function lcMpy() {
    if (window._lcMpyP) return window._lcMpyP;
    window._lcMpyP = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
      .then(function (mjs) {
        return mjs.loadMicroPython({
          /* THE BUILD HANDS US LINES, NOT BYTES: with a function hook,
             MicroPython calls stdout once per line WITHOUT its newline — so
             two prints arrived as "ab", and `expected="0\n1\n2"`, which this
             component's own docs teach, could never match (found while
             building input(), 2026-09-02). Put the newline back, unless a
             build ever hands one over. */
          stdout: function (t) { if (window._lcMpyOut) window._lcMpyOut(/\n$/.test(t) ? t : t + "\n"); },
          stderr: function (t) {
            var line = /\n$/.test(t) ? t : t + "\n";
            if (window._lcMpyOut) window._lcMpyOut(line);
            else if (window.console) console.warn("[lc mpy stderr]", t);
          }
        });
      });
    return window._lcMpyP;
  }
  window.lcMpy = lcMpy;

  var BOOTSTRAP_TPL = [
    "from js import document",
    "class _Showable:",
    "    def __init__(self, view_id):",
    "        self._view = document.getElementById(view_id)",
    "    def _esc(self, s):",
    "        return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')",
    "    def _card(self, title, rows_html):",
    "        c = document.createElement('div')",
    "        c.className = 'lc-rt-card'",
    "        c.innerHTML = '<h3>' + self._esc(title) + '</h3>' + rows_html",
    "        self._view.appendChild(c)",
    "    def _rows_from_pairs(self, pairs):",
    "        out = ''",
    "        for k, v in pairs:",
    "            out += '<div class=\"lc-rt-row\"><b>' + self._esc(k) + '</b><span class=\"lc-rt-val\">' + self._esc(v) + '</span></div>'",
    "        return out",
    "    def __call__(self, obj, title=None):",
    "        if isinstance(obj, dict):",
    "            t = title or obj.get('name') or obj.get('title') or 'dict'",
    "            self._card(t, self._rows_from_pairs(obj.items()))",
    "        elif isinstance(obj, (list, tuple)):",
    "            for i, item in enumerate(obj):",
    "                self(item, title=title and (title + '[' + str(i) + ']'))",
    "        else:",
    "            try:",
    "                d = obj.__dict__",
    "                if d:",
    "                    t = title or getattr(obj, 'name', None) or type(obj).__name__",
    "                    self._card(t, self._rows_from_pairs(d.items()))",
    "                    return",
    "            except (AttributeError, TypeError):",
    "                pass",
    "            self._card(title or type(obj).__name__, '<div class=\"lc-rt-val\">' + self._esc(obj) + '</div>')",
    "    def clear(self):",
    "        self._view.innerHTML = ''",
    "    def grid(self, rows, title=None, height=300):",
    "        import json as _json",
    "        from js import lcRenderDatagridFromJson",
    "        normalized = []",
    "        for r in rows:",
    "            if isinstance(r, dict):",
    "                normalized.append(r)",
    "            else:",
    "                try:",
    "                    normalized.append(r.__dict__)",
    "                except (AttributeError, TypeError):",
    "                    normalized.append({'value': str(r)})",
    "        lcRenderDatagridFromJson(self._view, _json.dumps(normalized), title or '', int(height))",
    "    def form(self, obj, title=None):",
    "        import json as _json",
    "        from js import lcRenderFormFromJson",
    "        if isinstance(obj, dict):",
    "            d = obj",
    "        else:",
    "            try:",
    "                d = obj.__dict__",
    "            except (AttributeError, TypeError):",
    "                d = {'value': str(obj)}",
    "        lcRenderFormFromJson(self._view, _json.dumps(d), title or '')",
    "show = _Showable('lc-pyrun-__ID__-view')",
    "class Object:",
    "    def __init__(self, **kw):",
    "        for k, v in kw.items():",
    "            setattr(self, k, v)",
    "    def __repr__(self):",
    "        attrs = ', '.join(k + '=' + repr(v) for k, v in self.__dict__.items())",
    "        return 'Object(' + attrs + ')'",
    /* input() WITHOUT A CONSOLE. MicroPython runs on the page's own thread,
       so a real input() would wait for a stdin the browser does not have and
       freeze the tab (measured, 2026-09-01). Instead the call is ANSWERED
       FROM A QUEUE and, when the queue runs dry, it stops the pass and says
       which question is unanswered; the driver asks the reader and runs the
       script again from the top with one more answer in hand. The queue is
       keyed by CALL ORDER, so a loop needs nothing special — five questions
       in a while are just calls 1..5 (Michel asked exactly this, 2026-09-02).
       Each answer remembers its prompt: if a re-run asks something else at
       that position, the program changed its mind and the driver drops the
       answers from there on. */
    "import js",
    "import json as _lc_json",
    "class _LcNeedInput(Exception):",
    "    pass",
    "_lc_answers = []",
    "_lc_ask_i = 0",
    "def _lc_load_answers():",
    "    global _lc_answers, _lc_ask_i",
    "    _lc_ask_i = 0",
    "    try:",
    "        _lc_answers = _lc_json.loads(str(js.window._lcInputAnswers or '[]'))",
    "    except Exception:",
    "        _lc_answers = []",
    "def input(prompt=''):",
    "    global _lc_ask_i",
    "    p = str(prompt)",
    "    i = _lc_ask_i",
    "    _lc_ask_i = i + 1",
    "    if i < len(_lc_answers) and _lc_answers[i][0] == p:",
    "        v = _lc_answers[i][1]",
    "        print(p + v)",   /* the transcript a terminal would show */
    "        return v",
    "    js.window._lcInputWant = _lc_json.dumps([i, p])",
    "    raise _LcNeedInput(p)",
    "_BOUND_ID = 'lc-pyrun-__ID__-bound'",
    "def _render_bound(name):",
    "    g = globals()",
    "    if name not in g:",
    "        return",
    "    obj = g[name]",
    "    container = document.getElementById(_BOUND_ID)",
    "    if container is None:",
    "        return",
    "    container.innerHTML = ''",
    "    c = document.createElement('div')",
    "    c.className = 'lc-rt-card'",
    "    d = getattr(obj, '__dict__', None) or {}",
    "    rows = ''",
    "    for k, v in d.items():",
    "        rows += '<div class=\"lc-rt-row\"><b>' + str(k) + '</b><span class=\"lc-rt-val\">' + str(v) + '</span></div>'",
    "    c.innerHTML = '<h3>' + name + '</h3>' + rows",
    "    container.appendChild(c)",
    "try:",
    "    import json as _json",
    "    from js import jsyaml as _jsyaml, JSON as _JSON",
    "    class _Yaml:",
    "        def load(self, s):",
    "            return _json.loads(_JSON.stringify(_jsyaml.load(s)))",
    "    yaml = _Yaml()",
    "    yaml.safe_load = yaml.load",
    "except Exception:",
    "    pass"
  ].join("\n");


  /* MICROPYTHON HAS NO f'{x = }' (Michel, 2026-10-07: his starters print
     f'{secret = }'). CPython 3.8 reads {expr = } as the text "expr = "
     followed by repr(expr) — or format(expr, spec) when a :spec follows.
     The runner rewrites it that way before the code reaches MicroPython,
     inside f-strings only, same line count, so a traceback still points
     where the learner looks. Comparisons ({a == b}), keyword arguments
     ({f(a=1)}) and doubled-brace escapes are left alone. */
  function desugarFstrings(src) {
    var out = "", i = 0, n = src.length;
    while (i < n) {
      var ch = src[i];
      if (ch === "#") { var e = src.indexOf("\n", i); if (e < 0) e = n; out += src.slice(i, e); i = e; continue; }
      var m = /^([rRbBuUfF]{0,2})('''|"""|'|")/.exec(src.slice(i, i + 5));
      if (m && (i === 0 || !/[A-Za-z0-9_.]/.test(src[i - 1]))) {
        var prefix = m[1], q = m[2], isF = /[fF]/.test(prefix);
        var j = i + prefix.length + q.length, body = "";
        while (j < n) {
          if (src[j] === "\\") { body += src.slice(j, j + 2); j += 2; continue; }
          if (src.startsWith(q, j)) break;
          if (q.length === 1 && src[j] === "\n") break;
          body += src[j]; j++;
        }
        var closed = src.startsWith(q, j);
        out += prefix + q + (isF ? desugarFBody(body) : body) + (closed ? q : "");
        i = j + (closed ? q.length : 0);
        continue;
      }
      out += ch; i++;
    }
    return out;
  }
  function desugarFBody(body) {
    return body.replace(/\{\{/g, "\u0001").replace(/\}\}/g, "\u0002")
      .replace(/\{([^{}]*)\}/g, function (all, inner) {
        var m = /^(\s*)(.*?[^=!<>])(\s*=\s*)(![rsa])?(:[^{}]*)?$/.exec(inner);
        if (!m) return all;
        var expr = m[2], conv = m[4] || (m[5] ? "" : "!r"), spec = m[5] || "";
        return m[1] + expr + m[3] + "{" + expr + conv + spec + "}";
      })
      .replace(/\u0001/g, "{" + "{").replace(/\u0002/g, "}" + "}");   /* no literal doubled braces: Liquid eats them */
  }

  /* text into an element WITHOUT replacing its node — Chromium closes the
     open typing (undo) group whenever a node is removed from the page */
  function setText(el, s) {
    var c = el.firstChild;
    if (c && c.nodeType === 3 && !c.nextSibling) { if (c.data !== s) c.data = s; }
    else el.textContent = s;
  }

  /* EVERY WRITE INTO THE EDITOR KEEPS UNDO (Michel, 2026-10-07: "undo does
     NOT work"). Assigning .value wipes the browser's undo stack; typing
     through insertText does not — so Tab, the tutor's piece, anything that
     edits the program goes through here: ⌘Z takes it back, like typing.
     Falls back to setRangeText where insertText is refused (old Firefox). */
  function editRange(ta, start, end, text) {
    var want = ta.value.slice(0, start) + text + ta.value.slice(end), ok = false;
    try {
      ta.focus();
      ta.setSelectionRange(start, end);
      ok = document.execCommand("insertText", false, text) && ta.value === want;
    } catch (e) { ok = false; }
    if (!ok) {
      ta.setRangeText(text, start, end, "end");
      try { ta.dispatchEvent(new Event("input", { bubbles: true })); } catch (e) {}
    }
    return ta.value === want;
  }

  function attach(rootId, opts) {
    opts = opts || {};
    var ID = opts.id || rootId.replace(/^lc-pyrun-/, "");
    var BOUND = opts.bound || "";
    var INIT = opts.init || "";
    var root = document.getElementById(rootId);
    if (!root || root.dataset.lcAttached) return;
    root.dataset.lcAttached = "1";
    var codeEl = root.querySelector(".lc-pyrun-code");
    var gutterInner = root.querySelector(".lc-pyrun-gutter-inner");
    var runBtn = root.querySelector(".lc-pyrun-run");
    var clearBtn = root.querySelector(".lc-pyrun-clear");
    var testBtn = root.querySelector(".lc-pyrun-test");
    var status = root.querySelector(".lc-pyrun-status");
    var out = root.querySelector(".lc-pyrun-out");
    var view = root.querySelector(".lc-pyrun-view");
    var testsEl = root.querySelector(".lc-pyrun-tests");
    if (!codeEl || !runBtn) return;
    var buf = "";
    var mp = null;
    var loading = null;
    var BOOTSTRAP = BOOTSTRAP_TPL.replace(/__ID__/g, ID);

    function repaintBound() {
      if (!BOUND || !mp) return;
      try { mp.runPython("_render_bound(" + JSON.stringify(BOUND) + ")"); } catch (e) { }
    }

    function setOut(text, isErr) {
      out.classList.remove("lc-empty");
      out.textContent = "";
      if (isErr) {
        var span = document.createElement("span");
        span.className = "lc-err";
        span.textContent = text;
        out.appendChild(span);
      } else {
        out.textContent = text;
      }
    }

    function clearTests() {
      if (testsEl) testsEl.innerHTML = "";
    }

    /* One number per line, however many rows the line wraps into: a mirror
       with the editor's font, padding and width lays each line out as a
       block, its height says how many rows it took, and the gutter pads the
       number with that many blank rows. */
    var mirror = null;
    function rowsPerLine(lines) {
      var wrapEl = codeEl.parentNode;
      if (!wrapEl || !wrapEl.classList || !wrapEl.classList.contains("lc-pyrun-codewrap")) return null;
      if (!mirror) { mirror = document.createElement("div"); mirror.className = "lc-pyrun-mirror"; mirror.setAttribute("aria-hidden", "true"); wrapEl.appendChild(mirror); }
      var cs = getComputedStyle(codeEl);
      ["fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "tabSize",
       "whiteSpace", "wordWrap", "overflowWrap",
       "paddingTop", "paddingRight", "paddingBottom", "paddingLeft"].forEach(function (k) { mirror.style[k] = cs[k]; });
      mirror.style.width = codeEl.clientWidth + "px";    /* minus a scrollbar, as the text is laid out */
      var lh = parseFloat(cs.lineHeight);
      if (!(lh > 0)) lh = parseFloat(cs.fontSize) * 1.5;
      var kids = mirror.children;
      while (kids.length > lines.length) mirror.removeChild(mirror.lastChild);
      while (kids.length < lines.length) { var d = document.createElement("div"); d.appendChild(document.createTextNode("")); mirror.appendChild(d); }
      lines.forEach(function (ln, i) { setText(kids[i], ln || " "); });
      var out = [];
      for (var i = 0; i < kids.length; i++) out.push(Math.max(1, Math.round(kids[i].offsetHeight / lh)));
      return out;
    }
    /* THE EDITOR FITS ITS PROGRAM (Michel, 2026-10-07, Safari: "the cursor
       stays trapped in the first 7 lines"): without rows= the box grows
       with the lines and never scrolls inside — the page scrolls, as it
       does for any text. rows= pins the height, scrolling as before. */
    var FIT = !opts.rows, MIN_ROWS = parseInt(codeEl.getAttribute("rows"), 10) || 6;
    function fitRows() {
      if (!FIT) return;
      var n = Math.max(MIN_ROWS, codeEl.value.split("\n").length + 1);
      if (codeEl.rows !== n) codeEl.rows = n;
    }
    function updateGutter() {
      if (!gutterInner) return;
      fitRows();
      var lines = codeEl.value.split("\n");
      var rows = codeEl.clientWidth ? rowsPerLine(lines) : null;
      var s = "";
      for (var i = 0; i < lines.length; i++) {
        s += (i ? "\n" : "") + (i + 1);
        var extra = rows ? rows[i] - 1 : 0;
        for (var k = 0; k < extra; k++) s += "\n";
      }
      setText(gutterInner, s);   /* no node swap: typing stays one undo step */
    }
    function syncGutter() {
      if (!gutterInner) return;
      gutterInner.style.transform = "translateY(" + (-codeEl.scrollTop) + "px)";
    }
    if (gutterInner) {
      updateGutter();
      codeEl.addEventListener("input", updateGutter);
      codeEl.addEventListener("scroll", syncGutter);
      /* a narrower editor wraps more: the rows are measured again */
      if (window.ResizeObserver) new ResizeObserver(function () { updateGutter(); }).observe(codeEl);
      else window.addEventListener("resize", updateGutter);
    }

    var hlPre = root.querySelector(".lc-pyrun-hl");
    var hlCode = hlPre ? hlPre.querySelector("code") : null;
    /* THE OVERLAY IS PATCHED, NOT REBUILT, WHILE TYPING (2026-10-07): a
       rebuilt overlay removes nodes, and Chromium then closes the typing
       group — ⌘Z took one character at a time. A keystroke changes one
       text node in place (colours catch up on a pause); only a change
       that crosses tokens rebuilds, as the recolour does. */
    var hlText = null, hlTimer = null;
    function hlPatch(next) {
      if (hlText == null || !hlCode.firstChild) return false;
      var prev = hlText, a = 0, pb = prev.length, nb = next.length;
      while (a < pb && a < nb && prev[a] === next[a]) a++;
      while (pb > a && nb > a && prev[pb - 1] === next[nb - 1]) { pb--; nb--; }
      var walker = document.createTreeWalker(hlCode, NodeFilter.SHOW_TEXT), node, pos = 0, last = null;
      while ((node = walker.nextNode())) {
        var len = node.data.length;
        if (a >= pos && pb <= pos + len && (a < pos + len || pb > a)) {
          node.data = node.data.slice(0, a - pos) + next.slice(a, nb) + node.data.slice(pb - pos);
          return true;
        }
        if (a < pos + len) return false;   /* the change crosses tokens */
        pos += len; last = node;
      }
      if (last && a === pos && pb === pos) {   /* typed at the very end */
        last.data += next.slice(a, nb);
        return true;
      }
      return false;
    }
    function recolour() {
      hlTimer = null;
      if (!hlCode || hlText == null) return;
      if (window.Prism && window.Prism.languages && window.Prism.languages.python) {
        hlCode.textContent = hlText;
        try { window.Prism.highlightElement(hlCode); } catch (e) {}
      }
    }
    function syncHighlight() {
      if (!hlCode) return;
      var text = codeEl.value, shown = text + (text.slice(-1) === "\n" ? " " : "");
      if (!hlPatch(shown)) setText(hlCode, shown);
      hlText = shown;
      clearTimeout(hlTimer);
      hlTimer = setTimeout(recolour, 250);
      syncHlScroll();
    }
    function syncHlScroll() {
      if (!hlCode) return;
      hlCode.style.transform = "translate(" + (-codeEl.scrollLeft) + "px, " + (-codeEl.scrollTop) + "px)";
    }
    if (hlCode) {
      syncHighlight();
      loadPrism().then(syncHighlight);
      codeEl.addEventListener("input", syncHighlight);
      codeEl.addEventListener("scroll", syncHlScroll);
    }

    codeEl.addEventListener("keydown", function(e){
      if (e.key !== "Tab") return;
      e.preventDefault();
      editRange(codeEl, codeEl.selectionStart, codeEl.selectionEnd, "    ");
      updateGutter();
      syncHighlight();
    });

    function loadMp() {
      if (mp) return Promise.resolve(mp);
      if (loading) return loading;
      runBtn.disabled = true;
      if (testBtn) testBtn.disabled = true;
      status.textContent = "loading runtime…";
      loading = Promise.all([lcMpy(), loadJsYaml()])
        .then(function(results){ return results[0]; })
        .then(function(instance){
          mp = instance;
          try { mp.runPython(BOOTSTRAP); } catch (e) { }
          if (INIT) {
            try { mp.runPython(INIT); } catch (e) { }
          }
          repaintBound();
          runBtn.disabled = false;
          if (testBtn) testBtn.disabled = false;
          status.textContent = "ready";
          return mp;
        })
        .catch(function(e){
          runBtn.disabled = false;
          if (testBtn) testBtn.disabled = false;
          status.textContent = "";
          loading = null;
          throw e;
        });
      return loading;
    }

    /* ── input(), by ask-and-replay ─────────────────────────────────────
       One pass runs to the first unanswered question and stops there; the
       reader answers in the console; the script runs AGAIN from the top with
       that answer in the queue. n questions cost n+1 passes, and the reader
       sees only the last one — the transcript, prompts and answers included,
       exactly as a terminal shows it.

       A loop needs nothing special: the queue is keyed by call order.
       What it cannot survive is a program that asks a DIFFERENT question at
       the same position on a re-run (a random or timed path) — the prompts
       are recorded with the answers, and a mismatch drops the tail. And a
       program that asks without end would replay for ever, so the ceiling
       below stops it with a sentence instead of a hang. */
    var MAX_ASKS = 25;
    var answers = [];              /* [[prompt, value], …] — this press only */

    function askInConsole(prompt) {
      return new Promise(function (resolve) {
        out.classList.remove("lc-empty");
        out.textContent = buf;                       /* what printed so far */
        var line = document.createElement("span");
        line.className = "lc-pyrun-ask";
        line.textContent = prompt;
        var box = document.createElement("input");
        box.type = "text";
        box.className = "lc-pyrun-ask-box";
        box.setAttribute("aria-label", prompt || "input");
        line.appendChild(box);
        out.appendChild(line);
        box.focus();
        box.addEventListener("keydown", function (e) {
          if (e.key === "Enter") { e.preventDefault(); resolve(box.value); }
          else if (e.key === "Escape") { e.preventDefault(); resolve(null); }
        });
      });
    }

    /* the whole press: passes, questions, and the verdict */
    function runAsking(m) {
      answers = [];
      var pass = 0;
      function once() {
        window._lcInputAnswers = JSON.stringify(answers);
        window._lcInputWant = "";
        var ok = runUserCode(m);
        var want = window._lcInputWant;
        if (!want) return Promise.resolve(ok);       /* finished, green or red */
        if (++pass > MAX_ASKS) {
          setOut(buf + "\n… this program asks more questions than a page can "
               + "hold (" + MAX_ASKS + "). A conversation that long belongs in a "
               + "terminal, or in a REPL block.", true);
          return Promise.resolve(false);
        }
        var asked;
        try { asked = JSON.parse(want); } catch (e) { return Promise.resolve(ok); }
        answers.length = asked[0];                   /* the tail is stale */
        return askInConsole(asked[1]).then(function (value) {
          if (value === null) {                      /* Escape — leave it be */
            setOut(buf + "\n(cancelled — nothing was asked twice)", false);
            return false;
          }
          answers.push([asked[1], value]);
          return once();
        });
      }
      return once();
    }

    function runUserCode(m) {
      buf = "";
      view.innerHTML = "";
      /* shared interpreter: point `show` (and print) at THIS editor for
         the duration of the run — runPython is synchronous */
      window._lcMpyOut = function (t) { buf += t; };
      try { m.runPython(BOOTSTRAP); } catch (e) { }
      try { m.runPython("_lc_load_answers()"); } catch (e) { }
      try {
        m.runPython(desugarFstrings(codeEl.value));
        setOut(buf || "(no print output)", false);
        return true;
      } catch (e) {
        /* an unanswered input() is not an error the reader should read: the
           driver is about to ask the question and run this again */
        if (window._lcInputWant) return false;
        setOut(buf + (buf ? "\n" : "") + (e.message || String(e)), true);
        return false;
      } finally {
        window._lcMpyOut = null;
      }
    }

    var EXPECTED = (opts.expected || "").replace(/\r\n/g, "\n");
    if (EXPECTED) root.dataset.lcQuizId = "run-" + ID;

    function checkExpected(ok) {
      if (!EXPECTED) return;
      var actual = (buf || "").replace(/\r\n/g, "\n").replace(/\n+$/, "");
      var want = EXPECTED.replace(/\n+$/, "");
      var match = ok && actual === want;
      status.textContent = match ? "✓ output matches" : "✗ expected: " + want;
      status.style.color = match ? "#2e7d32" : "#c62828";
      if (window.lcQuizScore && window.lcQuizScore.update) {
        window.lcQuizScore.update("run-" + ID, match);
      }
    }

    runBtn.addEventListener("click", function(){
      loadMp().then(function(m){
        clearTests();
        status.textContent = "running…";
        status.style.color = "";
        return runAsking(m).then(function (ok) {
          status.textContent = ok ? "done" : "error";
          status.style.color = "";
          repaintBound();
          checkExpected(ok);
        });
      }).catch(function(e){
        setOut("Failed to load MicroPython: " + (e.message || String(e)), true);
      });
    });

    if (testBtn) {
      testBtn.addEventListener("click", function(){
        loadMp().then(function(m){
          status.textContent = "running…";
          var ok = runUserCode(m);
          if (!ok) {
            status.textContent = "error in code";
            return;
          }
          var tests = parseDoctests(codeEl.value);
          clearTests();
          if (tests.length === 0) {
            var empty = document.createElement("div");
            empty.className = "lc-pyrun-test-row lc-pyrun-test-empty";
            empty.textContent = "No doctests found. Add >>> lines inside a triple-quoted docstring.";
            testsEl.appendChild(empty);
            status.textContent = "no tests";
            repaintBound();
            return;
          }
          var driver = [
            "from js import document",
            "_tests_el = document.getElementById('lc-pyrun-" + ID + "-tests')",
            "_tests_el.innerHTML = ''",
            "_summary = document.createElement('div')",
            "_summary.className = 'lc-pyrun-test-summary'",
            "_summary.textContent = 'running…'",
            "_tests_el.appendChild(_summary)",
            "_pass = 0",
            "_fail = 0",
            "def _doctest(expr, expected, lineno):",
            "    global _pass, _fail",
            "    try:",
            "        v = eval(expr)",
            "        actual = '' if v is None else repr(v)",
            "        err = None",
            "    except Exception as e:",
            "        actual = ''",
            "        err = type(e).__name__ + ': ' + str(e)",
            "    passed = err is None and actual == expected",
            "    row = document.createElement('div')",
            "    row.className = 'lc-pyrun-test-row ' + ('lc-pyrun-test-pass' if passed else 'lc-pyrun-test-fail')",
            "    icon = '✅' if passed else '❌'",
            "    if passed:",
            "        _pass += 1",
            "        row.textContent = icon + ' line ' + str(lineno) + '  ' + expr",
            "    else:",
            "        _fail += 1",
            "        if err:",
            "            row.textContent = icon + ' line ' + str(lineno) + '  ' + expr + '  →  raised ' + err",
            "        else:",
            "            row.textContent = icon + ' line ' + str(lineno) + '  ' + expr + '  →  got ' + (actual or '(no value)') + ', expected ' + expected",
            "    _tests_el.appendChild(row)"
          ].join("\n");
          var calls = tests.map(function(t){
            return "_doctest(" + JSON.stringify(desugarFstrings(t.expr)) + ", " + JSON.stringify(t.expected) + ", " + t.lineno + ")";
          }).join("\n");
          var finish = "_summary.textContent = str(_pass) + ' passed, ' + str(_fail) + ' failed'";
          try {
            window._lcMpyOut = function (t) { buf += t; };
            try { m.runPython(BOOTSTRAP); } catch (e2) { }
            try {
            m.runPython(driver + "\n" + calls + "\n" + finish);
            } finally { window._lcMpyOut = null; }
            status.textContent = "tests done";
          } catch (e) {
            var row = document.createElement("div");
            row.className = "lc-pyrun-test-row lc-pyrun-test-fail";
            row.textContent = "Test runner error: " + (e.message || String(e));
            testsEl.appendChild(row);
            status.textContent = "test error";
          }
          repaintBound();
        }).catch(function(e){
          setOut("Failed to load MicroPython: " + (e.message || String(e)), true);
        });
      });
    }

    clearBtn.addEventListener("click", function(){
      out.textContent = "click ▶ Run to execute";
      out.classList.add("lc-empty");
      view.innerHTML = "";
      clearTests();
      status.textContent = mp ? "ready" : "";
    });

    if (BOUND) {
      loadMp().catch(function(){ });
    }
  }

  function buildRunner(opts) {
    var id = opts.id;
    var bound = opts.bound || "";
    var folded = opts.folded;
    var rows = opts.rows || 6;
    var div = document.createElement("div");
    div.className = "lc-pyrun";
    div.id = "lc-pyrun-" + id;
    var html = "";
    if (bound) html += '<div class="lc-pyrun-bound" id="lc-pyrun-' + id + '-bound"></div>';
    if (folded) {
      html += '<details class="lc-pyrun-fold"><summary>🐍 Edit &amp; run Python</summary>';
    } else {
      html += '<div class="lc-pyrun-title">🐍 <span>Python runner</span><span class="lc-pyrun-lang">python</span></div>';
    }
    html += '<div class="lc-pyrun-editor"><div class="lc-pyrun-gutter"><div class="lc-pyrun-gutter-inner"></div></div><div class="lc-pyrun-codewrap"><pre class="lc-pyrun-hl" aria-hidden="true" tabindex="-1"><code class="language-python"></code></pre><textarea class="lc-pyrun-code" rows="' + rows + '" spellcheck="false" aria-label="Python editor"></textarea></div></div>';
    html += '<div class="lc-pyrun-bar"><button class="lc-pyrun-run">▶ Run</button><button class="lc-pyrun-test">🧪 Test</button><button class="lc-pyrun-clear">Clear</button><span class="lc-pyrun-status"></span></div>';
    html += '<pre class="lc-pyrun-out lc-empty">click ▶ Run to execute</pre>';
    html += '<div class="lc-pyrun-view" id="lc-pyrun-' + id + '-view"></div>';
    html += '<div class="lc-pyrun-tests" id="lc-pyrun-' + id + '-tests"></div>';
    if (folded) html += '</details>';
    div.innerHTML = html;
    div.querySelector(".lc-pyrun-code").value = opts.code || "";
    return div;
  }

  var REPL_BOOTSTRAP = [
    "def _repl_eval(line):",
    "    try:",
    "        _code = compile(line, '<repl>', 'eval')",
    "        _val = eval(_code)",
    "        if _val is not None:",
    "            print(repr(_val))",
    "    except SyntaxError:",
    "        try:",
    "            exec(compile(line, '<repl>', 'exec'))",
    "        except BaseException as e:",
    "            print(repr(e))",
    "    except BaseException as e:",
    "        print(repr(e))"
  ].join("\n");

  function buildRepl(opts) {
    var id = opts.id;
    var div = document.createElement("div");
    div.className = "lc-pyrepl";
    div.id = "lc-pyrepl-" + id;
    div.innerHTML =
      '<div class="lc-pyrepl-title">🐍 <span>Python REPL</span><button class="lc-pyrepl-reset" title="reset runtime — clears state">↻</button><span class="lc-pyrepl-status"></span></div>' +
      '<pre class="lc-pyrepl-transcript"></pre>' +
      '<div class="lc-pyrepl-input-row"><span class="lc-pyrepl-marker">&gt;&gt;&gt;</span><input class="lc-pyrepl-input" type="text" spellcheck="false" autocapitalize="off" autocorrect="off" autocomplete="off" aria-label="Python console input" /></div>';
    return div;
  }

  function attachRepl(rootId, opts) {
    opts = opts || {};
    var root = document.getElementById(rootId);
    if (!root || root.dataset.lcAttached) return;
    root.dataset.lcAttached = "1";
    var transcript = root.querySelector(".lc-pyrepl-transcript");
    var input = root.querySelector(".lc-pyrepl-input");
    var status = root.querySelector(".lc-pyrepl-status");
    var resetBtn = root.querySelector(".lc-pyrepl-reset");
    var INIT = opts.init || "";
    var buf = "";
    var mp = null;
    var loading = null;
    var history = [];
    var historyIdx = -1;

    function append(text, cls) {
      if (cls) {
        var span = document.createElement("span");
        span.className = cls;
        span.textContent = text;
        transcript.appendChild(span);
      } else {
        transcript.appendChild(document.createTextNode(text));
      }
      transcript.scrollTop = transcript.scrollHeight;
    }

    function loadMp() {
      if (mp) return Promise.resolve(mp);
      if (loading) return loading;
      input.disabled = true;
      status.textContent = "loading runtime…";
      loading = lcMpy()
        .then(function(instance){
          mp = instance;
          try { mp.runPython(REPL_BOOTSTRAP); } catch (e) { }
          if (INIT) {
            try { mp.runPython(INIT); } catch (e) { }
          }
          input.disabled = false;
          input.focus();
          status.textContent = "";
          return mp;
        })
        .catch(function(e){
          input.disabled = false;
          status.textContent = "load failed";
          loading = null;
          throw e;
        });
      return loading;
    }

    function submit(line) {
      window._lcMpyOut = null;
      if (!line) {
        append(">>> \n", "lc-pyrepl-prompt-line");
        return;
      }
      history.push(line);
      historyIdx = history.length;
      loadMp().then(function(m){
        append(">>> " + line + "\n", "lc-pyrepl-prompt-line");
        buf = "";
        window._lcMpyOut = function (t) { buf += t; };
        try { m.runPython(REPL_BOOTSTRAP); } catch (e0) { }
        try {
          m.runPython("_repl_eval(" + JSON.stringify(desugarFstrings(line)) + ")");
          if (buf) {
            if (buf.charAt(buf.length - 1) !== "\n") buf += "\n";
            var isErr = /^(SyntaxError|NameError|TypeError|ValueError|ZeroDivisionError|IndexError|KeyError|AttributeError|ImportError|RuntimeError|Exception)/.test(buf);
            append(buf, isErr ? "lc-pyrepl-err" : null);
          }
        } catch (e) {
          var msg = e.message || String(e);
          append(msg + "\n", "lc-pyrepl-err");
          append("(runtime crashed — state lost, reloading on next command)\n", "lc-pyrepl-err");
          mp = null;
          window._lcMpyOut = null;
          loading = null;
        }
      }).catch(function(e){
        append("Failed to load MicroPython: " + (e.message || String(e)) + "\n", "lc-pyrepl-err");
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function(){
        mp = null;
        loading = null;
        history = [];
        historyIdx = -1;
        transcript.innerHTML = "";
        append("(runtime reset — state cleared)\n", "lc-pyrepl-err");
        input.focus();
      });
    }

    input.addEventListener("keydown", function(e){
      if (e.key === "Enter") {
        e.preventDefault();
        var line = input.value;
        input.value = "";
        submit(line);
      } else if (e.key === "ArrowUp") {
        if (history.length === 0) return;
        e.preventDefault();
        historyIdx = Math.max(0, historyIdx - 1);
        input.value = history[historyIdx] || "";
      } else if (e.key === "ArrowDown") {
        if (history.length === 0) return;
        e.preventDefault();
        historyIdx = Math.min(history.length, historyIdx + 1);
        input.value = history[historyIdx] || "";
      }
    });

    // Focus input when the transcript area is clicked
    root.addEventListener("click", function(e){
      if (e.target !== input) input.focus();
    });
  }

  var REPL_ID = 0;
  function upgradeRepl(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent.replace(/\n+$/, "") : "";
    var id = el.id || ("repl" + (++REPL_ID));
    var opts = {
      id: id,
      init: el.getAttribute("init") || raw || ""
    };
    var widget = buildRepl(opts);
    el.parentNode.replaceChild(widget, el);
    attachRepl("lc-pyrepl-" + id, opts);
  }


  var RUN_ID = 0;
  function upgradeRun(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent.replace(/\n+$/, "") : "";
    var silent = el.hasAttribute("silent") && el.getAttribute("silent") !== "false";
    if (silent) {
      el.parentNode.removeChild(el);
      runSilent(raw);
      return;
    }
    var code = raw;
    var initFromCode = "";
    var sepRe = /^#\s*-{3,}\s*$\n?/m;
    var sepMatch = raw.match(sepRe);
    if (sepMatch) {
      initFromCode = raw.substring(0, sepMatch.index).replace(/\n+$/, "");
      code = raw.substring(sepMatch.index + sepMatch[0].length);
    }
    var id = el.id || ("r" + (++RUN_ID));
    var opts = {
      id: id,
      code: code,
      bound: el.getAttribute("bound") || "",
      init: el.getAttribute("init") || initFromCode || "",
      rows: parseInt(el.getAttribute("rows"), 10) || 0,   /* 0: the editor fits its program */
      folded: el.hasAttribute("folded") && el.getAttribute("folded") !== "false",
      expected: el.getAttribute("expected") || ""
    };
    var runner = buildRunner(opts);
    el.parentNode.replaceChild(runner, el);
    attach("lc-pyrun-" + id, opts);
  }

  /* The shared page runtime: one persistent MicroPython instance that silent
     setup code seeds and reactive {= cells } read. It's separate from the
     button/preamble instance (window._lcMpReady) — this one holds page data
     and model defs, so a `.run silent` block is the page's model, and its
     names stay live for the cells. Exported so cells.md evaluates in it. */
  function pageRuntime() {
    if (window._lcPageRuntime) return window._lcPageRuntime;
    var view = document.createElement("div");
    view.id = "lc-pyrun-page-view"; view.style.display = "none";
    var bound = document.createElement("div");
    bound.id = "lc-pyrun-page-bound"; bound.style.display = "none";
    document.body.appendChild(view);
    document.body.appendChild(bound);
    window._lcPageRuntime = Promise.all([lcMpy(), loadJsYaml()])
      .then(function(results){ return results[0]; })
      .then(function(mp){
        try { mp.runPython(BOOTSTRAP_TPL.replace(/__ID__/g, "page")); }
        catch (e) { if (window.console) console.warn("[lc page-rt bootstrap]", e.message || e); }
        return mp;
      });
    return window._lcPageRuntime;
  }
  window.lcPageRuntime = pageRuntime;

  function runSilent(code) {
    pageRuntime()
      .then(function(mp){
        try { mp.runPython(desugarFstrings(code)); } catch (e) { if (window.console) console.warn("[lc silent code]", e.message || e); }
        /* the page model just changed — cells and diagrams recompute */
        try { document.dispatchEvent(new CustomEvent("lc-model-changed", { detail: { source: "run-silent" } })); } catch (e) {}
      })
      .catch(function(e){ if (window.console) console.warn("[lc silent load]", e.message || e); });
  }

  // Export the runner for Liquid-rendered python_run.md blocks, then flush
  // any attach calls they queued while this file was still parsing.
  window.lcPyrun = { attach: attach, edit: editRange };
  if (window.lcPyrunQueue) {
    window.lcPyrunQueue.forEach(function(fn){ try { fn(); } catch (e) {} });
    window.lcPyrunQueue = null;
  }


  function upgradeButton(el) {
    var a = el.querySelector("a");
    if (!a) return;

    // Optional Python click handler: a code block tagged {: .onclick }
    // immediately following the button paragraph.
    var handlerCode = "";
    var sib = el.nextElementSibling;
    while (sib && !sib.textContent.trim()) sib = sib.nextElementSibling;
    if (sib && sib.classList.contains("onclick") && sib.querySelector("code")) {
      handlerCode = sib.querySelector("code").textContent;
      sib.parentNode.removeChild(sib);
    }

    if (handlerCode) {
      // Interactive button: replace the link with a real <button> so the
      // Python step layer (self.page.<id>.click()) and real clicks both run it.
      var lcId = el.getAttribute("data-lc-id") || el.getAttribute("id") || "";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lc-button";
      btn.textContent = (a.textContent || el.textContent || "").trim();
      if (lcId) btn.setAttribute("data-lc-id", lcId);
      btn.setAttribute("data-lc-py", handlerCode);
      btn.addEventListener("click", function () { runButtonHandler(btn); });
      el.parentNode.replaceChild(btn, el);
      return;
    }

    // Plain styled-link button (existing behaviour).
    /* the component page documents `kind=` — the code only read the older
       style-variant, so every kind="outline" silently rendered default
       (module 05's 🏠 button, 2026-08-18). Both spellings work; kind wins. */
    var style = el.getAttribute("kind") || el.getAttribute("style-variant") || "";
    a.classList.add("button");
    if (style) a.classList.add("button-" + style);
    el.classList.remove("button");
  }

  /* A handler fence may be JUST the body — ideally one line, `button` in
     scope. The def line is the ENGINE's (Michel, 2026-08-11: beginners see
     only the if); it is added here for execution, and the lens shows it
     dimmed and locked. A full `def on_click…` still works unchanged. */
  window.lcWrapHandler = function (code) {
    if (/^\s*def\s+on_click\s*\(/m.test(code)) return code;
    return "def on_click(button):\n" + String(code).split("\n")
      .map(function (l) { return "    " + l; }).join("\n");
  };

  // Run a button's Python on_click(handler) via the shared MicroPython instance.
  function runButtonHandler(btn) {
    var pyCode = btn.getAttribute("data-lc-py") || "";
    if (!pyCode) return;
    var lcId = btn.getAttribute("data-lc-id") || "";
    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    /* A BARE BODY IS THE PAGE'S OWN LINES, not a function's. Wrapped in a
       def, every name a beginner assigns died with the click — Michel wrote
       `message = …` in a button and `{= message }` beside it stayed empty
       (2026-09-01). A bare fence now runs at module scope with `button`
       bound, so what the lines set, the page can read. An explicit
       `def on_click(…)` keeps Python's own rules: its locals stay local. */
    var bare = !/^\s*def\s+on_click\s*\(/m.test(pyCode);
    var fullCode = preamble + "\n"
      + "button = _wrap(js.window.document.querySelector(\"[data-lc-id='" + lcId + "']\"))\n"
      + (bare ? pyCode + "\n" : pyCode + "\non_click(button)\n");
    if (!window._lcMpReady) window._lcMpReady = lcMpy();
    window._lcMpReady.then(function (mp) {
      var runFn = mp.runPython || mp.exec || mp.pyexec || mp.run;
      try { if (runFn) runFn.call(mp, fullCode); } catch (e) { console.error("[lc-button]", e); }
      /* a click changed the page's data, exactly as a form edit does — so the
         page's cells recompute on the same bus, and never a second later */
      try { document.dispatchEvent(new CustomEvent("lc-model-changed",
                                   { detail: { source: "button" } })); } catch (e) {}
    });
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  /* the inline form — [x](y){: .button kind="…" } — tags the <a> itself,
     so the paragraph upgrader above never sees it; map the knob here too */
  function upgradeButtonLink(a) {
    var k = a.getAttribute("kind") || a.getAttribute("style-variant") || "";
    if (k) a.classList.add("button-" + k);
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.run, pre.run", upgradeRun);
    window.lcRegisterUpgrader(".highlighter-rouge.repl, pre.repl", upgradeRepl);
    window.lcRegisterUpgrader("p.button", upgradeButton);
    window.lcRegisterUpgrader("a.button[kind], a.button[style-variant]", upgradeButtonLink);
  }

})();
</script>
