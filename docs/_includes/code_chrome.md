<style>
.lc-code { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #fafafa; }
.lc-code-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-code-title .lc-code-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-code > .highlighter-rouge, .lc-code > pre { margin: 0 !important; border-radius: 0 !important; background: transparent !important; }
.lc-code .highlight { background: transparent !important; }
.lc-code .highlight pre, .lc-code > pre { padding: 0.9em 1em !important; margin: 0 !important; overflow-x: auto; font-size: 0.85em; line-height: 1.5; background: transparent !important; }

.lc-pyrun { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-pyrun-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrun-title .lc-pyrun-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-pyrun textarea { display: block; width: 100%; box-sizing: border-box; border: none; outline: none; padding: 0.9em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; resize: vertical; background: #fafafa; color: #111; }
.lc-pyrun-editor { display: flex; background: #fafafa; align-items: stretch; }
.lc-pyrun-editor .lc-pyrun-code { flex: 1; min-width: 0; padding-left: 0.6em; }
.lc-pyrun-gutter { position: relative; overflow: hidden; background: #f3f4f6; border-right: 1px solid #e8e8e8; user-select: none; min-width: 2.5em; }
.lc-pyrun-gutter-inner { padding: 0.9em 0.5em 0.9em 0.6em; color: #aaa; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; text-align: right; white-space: pre; pointer-events: none; will-change: transform; }
.lc-pyrun-bar { display: flex; align-items: center; gap: 0.6em; padding: 0.5em 0.9em; background: #f3f4f6; border-top: 1px solid #e0e0e0; }
.lc-pyrun-bar button { background: #0066cc; color: white; border: none; border-radius: 4px; padding: 0.35em 0.9em; cursor: pointer; font-size: 0.85em; font-weight: 500; }
.lc-pyrun-bar button:hover:not(:disabled) { background: #0052a3; }
.lc-pyrun-bar button:disabled { background: #888; cursor: progress; }
.lc-pyrun-bar .lc-pyrun-clear { background: #e5e5e5; color: #333; }
.lc-pyrun-bar .lc-pyrun-clear:hover:not(:disabled) { background: #d0d0d0; }
.lc-pyrun-bar .lc-pyrun-test { background: #4a8a3d; }
.lc-pyrun-bar .lc-pyrun-test:hover:not(:disabled) { background: #3d7330; }
.lc-pyrun-bar .lc-pyrun-status { margin-left: auto; font-size: 0.78em; color: #666; }
.lc-pyrun-out { margin: 0; padding: 0.9em 1em; background: #1e1e1e; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; min-height: 2em; max-height: 300px; overflow-y: auto; }
.lc-pyrun-out.lc-empty { color: #888; font-style: italic; }
.lc-pyrun-out .lc-err { color: #ff6b6b; }
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
.lc-pyrun-tests .lc-pyrun-test-empty { color: #888; font-style: italic; }

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
</style>
<script>
(function(){
  if (window.lcPyrun) return;

  // Parse a Python source string and extract simple doctests:
  //   >>> expr
  //   expected_repr
  // Only single-line expected output, only inside triple-quoted docstrings.
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
    "show = _Showable('lc-pyrun-__ID__-view')",
    "class Object:",
    "    def __init__(self, **kw):",
    "        for k, v in kw.items():",
    "            setattr(self, k, v)",
    "    def __repr__(self):",
    "        attrs = ', '.join(k + '=' + repr(v) for k, v in self.__dict__.items())",
    "        return 'Object(' + attrs + ')'",
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

  function loadJsYaml() {
    if (window.jsyaml) return Promise.resolve();
    return new Promise(function(resolve){
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js";
      s.onload = function(){ resolve(); };
      s.onerror = function(){ resolve(); };
      document.head.appendChild(s);
    });
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

    function updateGutter() {
      if (!gutterInner) return;
      var n = (codeEl.value.match(/\n/g) || []).length + 1;
      var s = "";
      for (var i = 1; i <= n; i++) s += (i > 1 ? "\n" : "") + i;
      gutterInner.textContent = s;
    }
    function syncGutter() {
      if (!gutterInner) return;
      gutterInner.style.transform = "translateY(" + (-codeEl.scrollTop) + "px)";
    }
    if (gutterInner) {
      updateGutter();
      codeEl.addEventListener("input", updateGutter);
      codeEl.addEventListener("scroll", syncGutter);
    }

    function loadMp() {
      if (mp) return Promise.resolve(mp);
      if (loading) return loading;
      runBtn.disabled = true;
      if (testBtn) testBtn.disabled = true;
      status.textContent = "loading runtime…";
      loading = Promise.all([
        import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs"),
        loadJsYaml()
      ])
        .then(function(results){
          return results[0].loadMicroPython({
            stdout: function(t){ buf += t; },
            stderr: function(t){ buf += t; }
          });
        })
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

    function runUserCode(m) {
      buf = "";
      view.innerHTML = "";
      try {
        m.runPython(codeEl.value);
        setOut(buf || "(no print output)", false);
        return true;
      } catch (e) {
        setOut(buf + (buf ? "\n" : "") + (e.message || String(e)), true);
        return false;
      }
    }

    runBtn.addEventListener("click", function(){
      loadMp().then(function(m){
        clearTests();
        status.textContent = "running…";
        var ok = runUserCode(m);
        status.textContent = ok ? "done" : "error";
        repaintBound();
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
            return "_doctest(" + JSON.stringify(t.expr) + ", " + JSON.stringify(t.expected) + ", " + t.lineno + ")";
          }).join("\n");
          var finish = "_summary.textContent = str(_pass) + ' passed, ' + str(_fail) + ' failed'";
          try {
            m.runPython(driver + "\n" + calls + "\n" + finish);
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
      html += '<div class="lc-pyrun-title">🐍 <span>MicroPython runner</span><span class="lc-pyrun-lang">python</span></div>';
    }
    html += '<div class="lc-pyrun-editor"><div class="lc-pyrun-gutter"><div class="lc-pyrun-gutter-inner"></div></div><textarea class="lc-pyrun-code" rows="' + rows + '" spellcheck="false"></textarea></div>';
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
      '<div class="lc-pyrepl-input-row"><span class="lc-pyrepl-marker">&gt;&gt;&gt;</span><input class="lc-pyrepl-input" type="text" spellcheck="false" autocapitalize="off" autocorrect="off" autocomplete="off" /></div>';
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
      loading = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
        .then(function(mod){
          return mod.loadMicroPython({
            stdout: function(t){ buf += t; },
            stderr: function(t){ buf += t; }
          });
        })
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
      if (!line) {
        append(">>> \n", "lc-pyrepl-prompt-line");
        return;
      }
      history.push(line);
      historyIdx = history.length;
      loadMp().then(function(m){
        append(">>> " + line + "\n", "lc-pyrepl-prompt-line");
        buf = "";
        try {
          m.runPython("_repl_eval(" + JSON.stringify(line) + ")");
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

  function upgradeCode(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var title = el.getAttribute("title") || "";
    var m = el.className.match(/language-([\w+-]+)/);
    var lang = m ? m[1] : "text";
    var wrap = document.createElement("div");
    wrap.className = "lc-code";
    if (title) {
      var bar = document.createElement("div");
      bar.className = "lc-code-title";
      bar.appendChild(document.createTextNode("📄 "));
      var t = document.createElement("span");
      t.textContent = title;
      bar.appendChild(t);
      var lg = document.createElement("span");
      lg.className = "lc-code-lang";
      lg.textContent = lang;
      bar.appendChild(lg);
      wrap.appendChild(bar);
    }
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);
  }

  var RUN_ID = 0;
  function upgradeRun(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent.replace(/\n+$/, "") : "";
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
      rows: parseInt(el.getAttribute("rows"), 10) || 6,
      folded: el.hasAttribute("folded") && el.getAttribute("folded") !== "false"
    };
    var runner = buildRunner(opts);
    el.parentNode.replaceChild(runner, el);
    attach("lc-pyrun-" + id, opts);
  }

  function scan() {
    document.querySelectorAll("p").forEach(function(p){
      var t = (p.textContent || "").trim();
      var m = t.match(/^\{:\s*(.+?)\s*\}$/);
      if (!m) return;
      var prev = p.previousElementSibling;
      if (!prev) return;
      var body = m[1];
      var c, classRe = /\.([\w-]+)/g;
      while ((c = classRe.exec(body)) !== null) prev.classList.add(c[1]);
      var idM = body.match(/#([\w-]+)/);
      if (idM) prev.id = idM[1];
      var kv, kvRe = /([\w-]+)="([^"]*)"/g;
      while ((kv = kvRe.exec(body)) !== null) prev.setAttribute(kv[1], kv[2]);
      p.parentNode.removeChild(p);
    });
    document.querySelectorAll(".highlighter-rouge.run, pre.run").forEach(upgradeRun);
    document.querySelectorAll(".highlighter-rouge.repl, pre.repl").forEach(upgradeRepl);
    document.querySelectorAll(".highlighter-rouge.code, pre.code").forEach(upgradeCode);
  }

  window.lcPyrun = { attach: attach };
  if (window.lcPyrunQueue) {
    window.lcPyrunQueue.forEach(function(fn){ try { fn(); } catch (e) {} });
    window.lcPyrunQueue = null;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
})();
</script>
