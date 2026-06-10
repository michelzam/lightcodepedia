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
.lc-pyrun-codewrap { position: relative; flex: 1; min-width: 0; }
.lc-pyrun-codewrap .lc-pyrun-code { flex: none; width: 100%; padding-left: 0.6em; }
.lc-pyrun-hl { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 0.9em 1em 0.9em 0.6em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; pointer-events: none; overflow: hidden; background: transparent; color: #111; white-space: pre-wrap; word-wrap: break-word; box-sizing: border-box; }
.lc-pyrun-hl code { font: inherit; background: transparent; padding: 0; color: inherit; display: block; will-change: transform; }
.lc-pyrun-codewrap .lc-pyrun-code { position: relative; background: transparent !important; color: transparent !important; caret-color: #111; }
.lc-pyrun-codewrap .lc-pyrun-code::selection { background: rgba(0, 102, 204, 0.18); color: transparent; }
.lc-pyrun .token.keyword, .lc-pyrun .token.boolean, .lc-pyrun .token.null { color: #cf222e; font-weight: 500; }
.lc-pyrun .token.string, .lc-pyrun .token.triple-quoted-string { color: #0a3069; }
.lc-pyrun .token.number { color: #0550ae; }
.lc-pyrun .token.comment { color: #6e7781; font-style: italic; }
.lc-pyrun .token.function, .lc-pyrun .token.class-name, .lc-pyrun .token.builtin, .lc-pyrun .token.decorator { color: #8250df; }
.lc-pyrun .token.operator, .lc-pyrun .token.punctuation { color: #24292f; }
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

/* tabs (global — also emitted inline by tabs.md include) */
/* accordion */
/* lazy blocks */
/* radio */
/* grid */
/* dropdown */
/* button */
.lc-btn { display: inline-block; padding: 0.5em 1.2em; background: #0066cc; color: white !important; text-decoration: none !important; border-radius: 4px; font-weight: 600; transition: background 0.15s; margin: 0.2em 0.3em 0.2em 0; }
.lc-btn:hover { background: #0052a3; }
.lc-btn-secondary { background: #6c757d; } .lc-btn-secondary:hover { background: #5a6268; }
.lc-btn-success { background: #28a745; } .lc-btn-success:hover { background: #1e7e34; }
.lc-btn-danger { background: #dc3545; } .lc-btn-danger:hover { background: #bd2130; }
.lc-btn-outline { background: transparent; color: #0066cc !important; border: 2px solid #0066cc; padding: calc(0.5em - 2px) calc(1.2em - 2px); }
.lc-btn-outline:hover { background: #0066cc; color: white !important; }
/* scrollable */
/* cards */
/* feature status dots on folder cards */
.lc-card-features { display: flex; gap: 0.35em; align-items: center; margin-top: 0.65em; flex-wrap: wrap; }
.lc-feat-dot { display: inline-flex; align-items: center; gap: 0.2em; font-size: 0.72em; font-weight: 600; padding: 0.1em 0.45em; border-radius: 99px; line-height: 1.6; }
.lc-feat-passing { background: #dcfce7; color: #15803d; }
.lc-feat-failing  { background: #fee2e2; color: #b91c1c; }
.lc-feat-pending  { background: #fef3c7; color: #92400e; }
.lc-feat-none     { background: #f3f4f6; color: #6b7280; }
/* chart */
</style>
<script>
(function(){
  if (window.lcPyrun) return;
  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  // Instance registry — destroy heavy components before live-preview re-render.
  var _lcReg = [];
  function _lcRegister(el, fn) { _lcReg.push({ el: el, fn: fn }); }
  window.lcRegisterCleanup = _lcRegister;
  window.lcDestroyInstancesIn = function(root) {
    _lcReg = _lcReg.filter(function(r) {
      if (r.el === root || root.contains(r.el)) { try { r.fn(); } catch(e) {} return false; }
      return true;
    });
  };

  // Master/detail pub-sub keyed by datagrid id.
  // Order-independent: grids publish on selection; forms subscribe on upgrade.
  window.lcMasterDetail = window.lcMasterDetail || {
    _subs: {},
    _last: {},
    _apis: {},
    subscribe: function(gridId, cb) {
      if (!gridId) return;
      (this._subs[gridId] = this._subs[gridId] || []).push(cb);
      if (gridId in this._last) {
        try { cb(this._last[gridId]); } catch (e) {}
      }
    },
    publish: function(gridId, row) {
      if (!gridId) return;
      this._last[gridId] = row;
      (this._subs[gridId] || []).forEach(function(cb){ try { cb(row); } catch (e) {} });
    },
    registerGrid: function(gridId, api) {
      if (!gridId) return;
      this._apis[gridId] = api;
    },
    refreshGrid: function(gridId) {
      var api = this._apis[gridId];
      if (api) api.refreshCells({ force: true });
    }
  };

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

  var _prismLoading = null;
  function loadPrism() {
    if (window.Prism && window.Prism.languages && window.Prism.languages.python) return Promise.resolve();
    if (_prismLoading) return _prismLoading;
    function injectScript(src) {
      return new Promise(function(resolve){
        var s = document.createElement("script");
        s.src = src;
        s.onload = function(){ resolve(); };
        s.onerror = function(){ resolve(); };
        document.head.appendChild(s);
      });
    }
    _prismLoading = injectScript("https://cdn.jsdelivr.net/npm/prismjs@1/components/prism-core.min.js")
      .then(function(){ return injectScript("https://cdn.jsdelivr.net/npm/prismjs@1/components/prism-python.min.js"); });
    return _prismLoading;
  }
  window.lcLoadPrism = loadPrism;

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

    var hlPre = root.querySelector(".lc-pyrun-hl");
    var hlCode = hlPre ? hlPre.querySelector("code") : null;
    function syncHighlight() {
      if (!hlCode) return;
      var text = codeEl.value;
      hlCode.textContent = text + (text.slice(-1) === "\n" ? " " : "");
      if (window.Prism && window.Prism.languages && window.Prism.languages.python) {
        try { window.Prism.highlightElement(hlCode); } catch (e) {}
      }
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
      var start = codeEl.selectionStart, end = codeEl.selectionEnd;
      var v = codeEl.value;
      codeEl.value = v.substring(0, start) + "    " + v.substring(end);
      codeEl.selectionStart = codeEl.selectionEnd = start + 4;
      updateGutter();
      syncHighlight();
    });

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
        var ok = runUserCode(m);
        status.textContent = ok ? "done" : "error";
        status.style.color = "";
        repaintBound();
        checkExpected(ok);
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
      html += '<div class="lc-pyrun-title">🐍 <span>Python runner</span><span class="lc-pyrun-lang">python</span></div>';
    }
    html += '<div class="lc-pyrun-editor"><div class="lc-pyrun-gutter"><div class="lc-pyrun-gutter-inner"></div></div><div class="lc-pyrun-codewrap"><pre class="lc-pyrun-hl" aria-hidden="true"><code class="language-python"></code></pre><textarea class="lc-pyrun-code" rows="' + rows + '" spellcheck="false"></textarea></div></div>';
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

  var _agGridLoading = null;
  function loadAgGrid() {
    if (window.agGrid && window.agGrid.createGrid) return Promise.resolve();
    if (_agGridLoading) return _agGridLoading;
    var addCss = function(href) {
      var l = document.createElement("link");
      l.rel = "stylesheet";
      l.href = href;
      document.head.appendChild(l);
    };
    addCss("https://cdn.jsdelivr.net/npm/ag-grid-community@31/styles/ag-grid.css");
    addCss("https://cdn.jsdelivr.net/npm/ag-grid-community@31/styles/ag-theme-alpine.css");
    _agGridLoading = new Promise(function(resolve, reject){
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/ag-grid-community@31/dist/ag-grid-community.min.js";
      s.onload = function(){
        if (window.agGrid && window.agGrid.createGrid) resolve();
        else reject(new Error("AG Grid loaded but global missing"));
      };
      s.onerror = function(){ reject(new Error("Failed to load AG Grid from CDN")); };
      document.head.appendChild(s);
    });
    return _agGridLoading;
  }
  window.lcLoadAgGrid = function(cb) { loadAgGrid().then(cb).catch(function(){}); };
  window.lcAgGridReady = loadAgGrid;

  function parseCsv(text) {
    var lines = [], cur = [], field = "", inQuote = false, i = 0;
    while (i < text.length) {
      var c = text.charAt(i);
      if (inQuote) {
        if (c === '"') {
          if (text.charAt(i + 1) === '"') { field += '"'; i += 2; continue; }
          inQuote = false; i++; continue;
        }
        field += c; i++; continue;
      }
      if (c === '"') { inQuote = true; i++; continue; }
      if (c === ",") { cur.push(field); field = ""; i++; continue; }
      if (c === "\n" || c === "\r") {
        cur.push(field); field = "";
        if (!(cur.length === 1 && cur[0] === "")) lines.push(cur);
        cur = [];
        if (c === "\r" && text.charAt(i + 1) === "\n") i++;
        i++; continue;
      }
      field += c; i++;
    }
    if (field !== "" || cur.length > 0) { cur.push(field); lines.push(cur); }
    if (lines.length < 1) return [];
    var headers = lines[0];
    var rows = [];
    for (var r = 1; r < lines.length; r++) {
      var row = {};
      for (var h = 0; h < headers.length; h++) {
        var v = lines[r][h];
        if (v === undefined) v = "";
        if (v !== "" && !isNaN(Number(v)) && /^-?\d+(\.\d+)?$/.test(v)) v = Number(v);
        row[headers[h]] = v;
      }
      rows.push(row);
    }
    return rows;
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function prettifyKey(k) {
    return String(k).replace(/_/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
  }
  window.lcEscapeHtml = escapeHtml;
  window.lcPrettifyKey = prettifyKey;

  function parseDatagridText(raw, format) {
    if (format === "json") return Promise.resolve(JSON.parse(raw));
    if (format === "csv") return Promise.resolve(parseCsv(raw));
    return loadJsYaml().then(function(){
      if (!window.jsyaml) throw new Error("js-yaml failed to load");
      return window.jsyaml.load(raw);
    });
  }
  window.lcParseDataText = parseDatagridText;

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
      rows: parseInt(el.getAttribute("rows"), 10) || 6,
      folded: el.hasAttribute("folded") && el.getAttribute("folded") !== "false",
      expected: el.getAttribute("expected") || ""
    };
    var runner = buildRunner(opts);
    el.parentNode.replaceChild(runner, el);
    attach("lc-pyrun-" + id, opts);
  }

  function runSilent(code) {
    var id = "silent" + (++RUN_ID);
    var view = document.createElement("div");
    view.id = "lc-pyrun-" + id + "-view";
    view.style.display = "none";
    var bound = document.createElement("div");
    bound.id = "lc-pyrun-" + id + "-bound";
    bound.style.display = "none";
    document.body.appendChild(view);
    document.body.appendChild(bound);
    var BOOTSTRAP = BOOTSTRAP_TPL.replace(/__ID__/g, id);
    Promise.all([
      import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs"),
      loadJsYaml()
    ])
      .then(function(results){
        return results[0].loadMicroPython({
          stdout: function(){},
          stderr: function(t){ if (window.console) console.warn("[lc silent stderr]", t); }
        });
      })
      .then(function(mp){
        try { mp.runPython(BOOTSTRAP); } catch (e) { if (window.console) console.warn("[lc silent bootstrap]", e.message || e); }
        try { mp.runPython(code); } catch (e) { if (window.console) console.warn("[lc silent code]", e.message || e); }
      })
      .catch(function(e){ if (window.console) console.warn("[lc silent load]", e.message || e); });
  }

  function safe(fn) {
    return function(el) { try { fn(el); } catch(e) { if (window.console) console.warn("[lc]", e.message || e); } };
  }

  // ── scan registry ──────────────────────────────────────────────────────
  // One registry for every upgrader: a component (here or in its own
  // include) registers selector + upgrade function once, and both the
  // page-level scan and the subtree re-scans walk the same list. Includes
  // that parse after the initial scan are upgraded at registration time.
  var _upgraders = [];
  var _scanned = false;

  function lcRegisterUpgrader(selector, fn) {
    var entry = [selector, safe(fn)];
    _upgraders.push(entry);
    if (_scanned) document.querySelectorAll(selector).forEach(entry[1]);
  }

  function _runUpgraders(root) {
    _upgraders.forEach(function (u) {
      root.querySelectorAll(u[0]).forEach(u[1]);
    });
  }

  lcRegisterUpgrader(".highlighter-rouge.run, pre.run", upgradeRun);
  lcRegisterUpgrader(".highlighter-rouge.repl, pre.repl", upgradeRepl);
  lcRegisterUpgrader(".highlighter-rouge.code, pre.code", upgradeCode);
  lcRegisterUpgrader("p.button", upgradeButton);
  lcRegisterUpgrader("p.folder", upgradeFolder);
  lcRegisterUpgrader("p.lightnodes", upgradeNodes);
  lcRegisterUpgrader("p.deploys", upgradeDeploys);

  function scan() {
    _applyIAL(document);
    _runUpgraders(document);
    _scanned = true;
  }

  // Scoped version of scan() — runs the full upgrade pipeline on a subtree.
  // Used by the live editor preview so the page-level scan() is not needed.
  function scanElement(root) {
    _applyIAL(root);
    _runUpgraders(root);
    if (window.lcUpgradeQuiz)  root.querySelectorAll("ul.quiz, ol.quiz").forEach(window.lcUpgradeQuiz);
    if (window.lcUpgradeAgent) root.querySelectorAll(".highlighter-rouge.agent, pre.agent").forEach(window.lcUpgradeAgent);
  }

  // --- shared helpers for section-based widgets ---
  var _markedQ = null;
  function loadMarked(cb) {
    if (window.marked) { cb(); return; }
    if (_markedQ) { _markedQ.push(cb); return; }
    _markedQ = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/marked@9/marked.min.js";
    s.onload = function() { var q = _markedQ; _markedQ = null; q.forEach(function(f){ try { f(); } catch(e) { if (window.console) console.warn("[lc]", e); } }); };
    document.head.appendChild(s);
  }
  function parseSections(el) {
    var code = el.querySelector("code");
    var raw = code ? code.textContent : el.textContent;
    return raw.split(/\n(?=### )/).map(function(s) {
      var lines = s.split("\n");
      var label = lines[0].replace(/^###\s*/, "").trim();
      var body = lines.slice(1).join("\n").trim();
      return { label: label, body: body };
    }).filter(function(s){ return s.label; });
  }
  function markdownBody(s) {
    /* ensure IAL tags land on their own paragraph so _applyIAL can process them */
    var norm = s.replace(/([^\n])\n(\{:)/g, "$1\n\n$2");
    return window.marked ? marked.parse(norm) : "<pre>" + s + "</pre>";
  }
  window.lcLoadMarked = loadMarked;
  window.lcParseSections = parseSections;
  window.lcMarkdownBody = markdownBody;
  window.lcScanElement = scanElement;
  window.lcApplyIAL   = _applyIAL;
  window.lcRegisterUpgrader = lcRegisterUpgrader;

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
    var style = el.getAttribute("style-variant") || "";
    a.classList.add("lc-btn");
    if (style) a.classList.add("lc-btn-" + style);
    el.classList.remove("button");
  }

  // Run a button's Python on_click(handler) via the shared MicroPython instance.
  function runButtonHandler(btn) {
    var pyCode = btn.getAttribute("data-lc-py") || "";
    if (!pyCode) return;
    var lcId = btn.getAttribute("data-lc-id") || "";
    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    var fullCode = preamble + "\n" + pyCode + "\n"
      + "_btn = _wrap(js.window.document.querySelector(\"[data-lc-id='" + lcId + "']\"))\n"
      + "on_click(_btn)\n";
    if (!window._lcMpReady) {
      window._lcMpReady = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
        .then(function (mjs) { return mjs.loadMicroPython({ stdout: function () {}, stderr: function () {} }); });
    }
    window._lcMpReady.then(function (mp) {
      var runFn = mp.runPython || mp.exec || mp.pyexec || mp.run;
      try { if (runFn) runFn.call(mp, fullCode); } catch (e) { console.error("[lc-button]", e); }
    });
  }

  function extractPageMeta(text) {
    var lines = text.split("\n");
    var i = 0;
    if (lines[0] && lines[0].trim() === "---") {
      i = 1;
      while (i < lines.length && lines[i].trim() !== "---") i++;
      i++;
    }
    var title = null, snippet = "";
    for (; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!title && /^#{1,2}\s/.test(line)) { title = line.replace(/^#+\s+/, ""); continue; }
      if (title && line && !/^[#{`\->|]/.test(line) && !/^\{:/.test(line) && line !== "---" && !/^[\-*+] /.test(line)) {
        snippet = line.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[*_`!]/g, "").trim().substring(0, 140);
        if (snippet.length >= 140) snippet += "…";
        break;
      }
    }
    return { title: title, snippet: snippet };
  }

  function upgradeFolder(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var a = el.querySelector("a");
    if (!a) return;
    var path = a.getAttribute("href").replace(/^\/+|\/+$/g, "");
    var cols = el.getAttribute("cols") || "auto";
    var showPrivate = el.getAttribute("show-private") === "true";
    var colStyle = cols === "auto"
      ? "repeat(auto-fit, minmax(200px, 1fr))"
      : "repeat(" + cols + ", 1fr)";
    var wrap = document.createElement("div");
    wrap.className = "lc-cards";
    wrap.style.gridTemplateColumns = colStyle;
    wrap.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading…</div>";
    el.parentNode.replaceChild(wrap, el);
    if (!_lcSiteRepo) {
      wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ site.github.repository_nwo not set.</div>";
      return;
    }
    var _folderPat = localStorage.getItem('lc_ed_pat') || '';
    var _folderHdrs = _folderPat ? { Authorization: 'Bearer ' + _folderPat, 'X-GitHub-Api-Version': '2022-11-28' } : {};
    function apiFetch(url) {
      return fetch(url, { headers: _folderHdrs }).then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
    }
    apiFetch("https://api.github.com/repos/" + _lcSiteRepo + "/contents/" + path)
      .then(function(files) {
        if (!Array.isArray(files)) throw new Error("Not a directory: " + escapeHtml(path));
        var pages = files.filter(function(f) {
          if (f.type !== "file" || !/\.md$/i.test(f.name) || f.name === "index.md") return false;
          if (!showPrivate && f.name.startsWith("_")) return false;
          return true;
        }).sort(function(a, b) { return a.name.localeCompare(b.name); });
        var subdirs = files.filter(function(f) { return f.type === "dir"; })
          .sort(function(a, b) { return a.name.localeCompare(b.name); });

        // fetch index.md for each subdir; always emit a card (fallback to dir name on any error)
        var subdirFetches = subdirs.map(function(d) {
          var slug   = d.path.replace(/^docs\//, "");
          var pretty = d.name.replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
          var fallback = { title: "📁 " + pretty, snippet: "", url: "/" + slug, isSubdir: true };
          return apiFetch(d.url)
            .then(function(entries) {
              var idx = Array.isArray(entries) && entries.find(function(e) {
                return e.type === "file" && e.name.toLowerCase() === "index.md";
              });
              if (!idx || !idx.download_url) return fallback;
              return fetch(idx.download_url)
                .then(function(r) { return r.ok ? r.text() : null; })
                .then(function(text) {
                  if (!text) return fallback;
                  var meta = extractPageMeta(text);
                  return { title: "📁 " + (meta.title || pretty), snippet: meta.snippet, url: "/" + slug, isSubdir: true };
                })
                .catch(function() { return fallback; });
            })
            .catch(function() { return fallback; });
        });

        var pageFetches = pages.map(function(f) {
          return fetch(f.download_url)
            .then(function(r) { return r.text(); })
            .then(function(text) {
              var meta = extractPageMeta(text);
              var title = meta.title || f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              /* collect .feature status values — skip code fences and inline code */
              var scanText = text
                .replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "")
                .replace(/`[^`\n]+`/g, "``");
              var features = [];
              var fRe = /\{:\s*\.feature\b([^}]*)\}/g, fm;
              while ((fm = fRe.exec(scanText)) !== null) {
                var sm = fm[1].match(/\bstatus="(\w+)"/);
                features.push(sm ? sm[1] : "");
              }
              /* collect internal links for hover ribbons */
              var cleanLinks = text.replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "").replace(/`[^`\n]+`/g, "");
              var pageSlug = f.path.replace(/^docs\//, "").replace(/\.md$/i, "");
              var rawHrefs = [], lRe = /\]\(([^)#\s]+)/g, lm;
              while ((lm = lRe.exec(cleanLinks)) !== null) {
                var h = lm[1]; if (/^https?:|^mailto:/.test(h)) continue; rawHrefs.push({ h: h, base: pageSlug });
              }
              return { title: title, snippet: meta.snippet, url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, ""), features: features, rawHrefs: rawHrefs };
            })
            .catch(function() {
              var title = f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              return { title: title, snippet: "", url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, "") };
            });
        });

        return Promise.all(subdirFetches.concat(pageFetches)).then(function(results) {
          var subdirItems = results.slice(0, subdirs.length).filter(Boolean);
          var pageItems   = results.slice(subdirs.length);
          return pageItems.concat(subdirItems);
        });
      })
      .then(function(items) {
        if (!items || !items.length) {
          wrap.innerHTML = "<div style='padding:1em;color:#888'>No pages found in " + escapeHtml(path) + "</div>";
          return;
        }
        /* resolve internal links between items */
        var urlSet = {};
        items.forEach(function(it) { urlSet[it.url] = it; });
        items.forEach(function(it) {
          it.links = [];
          (it.rawHrefs || []).forEach(function(ref) {
            var resolved;
            if (/^\//.test(ref.h)) {
              resolved = ref.h.replace(/\.md$/i, "");
            } else {
              var parts = ref.base.split("/"); parts.pop();
              ref.h.split("/").forEach(function(p) { if (p === "..") parts.pop(); else if (p && p !== ".") parts.push(p); });
              resolved = "/" + parts.join("/").replace(/\.md$/i, "");
            }
            if (urlSet[resolved] && resolved !== it.url) it.links.push(resolved);
          });
        });

        wrap.innerHTML = items.map(function(item) {
          var style = item.isSubdir ? ' style="background:#f0f2f5"' : '';
          var card = '<div class="lc-card" data-url="' + item.url + '"' + style + '><h3><a href="' + item.url + '">' + escapeHtml(item.title) + '</a></h3>';
          if (item.snippet) card += '<p style="font-size:0.85em;color:#555;margin:0.3em 0 0">' + escapeHtml(item.snippet) + '</p>';
          /* feature status dots */
          if (item.features && item.features.length) {
            var counts = {};
            item.features.forEach(function(s) { counts[s || "none"] = (counts[s || "none"] || 0) + 1; });
            var dots = "";
            if (counts.passing) dots += "<span class='lc-feat-dot lc-feat-passing' title='" + counts.passing + " passing scenario" + (counts.passing > 1 ? "s" : "") + "'>● " + counts.passing + "</span>";
            if (counts.failing)  dots += "<span class='lc-feat-dot lc-feat-failing'  title='" + counts.failing  + " failing scenario"  + (counts.failing  > 1 ? "s" : "") + "'>✗ " + counts.failing  + "</span>";
            if (counts.pending)  dots += "<span class='lc-feat-dot lc-feat-pending'  title='" + counts.pending  + " pending scenario"  + (counts.pending  > 1 ? "s" : "") + "'>◑ " + counts.pending  + "</span>";
            if (counts.none && !counts.passing && !counts.failing && !counts.pending)
              dots += "<span class='lc-feat-dot lc-feat-none' title='" + counts.none + " scenario" + (counts.none > 1 ? "s" : "") + " (no status set)'>● " + counts.none + "</span>";
            if (dots) card += "<div class='lc-card-features'>" + dots + "</div>";
          }
          return card + '</div>';
        }).join("");

        /* hover ribbons — overlay SVG draws bezier arcs between linked cards */
        var ribbonSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        ribbonSvg.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:visible;";
        wrap.style.position = "relative";
        wrap.appendChild(ribbonSvg);

        /* arrowhead marker for ribbons */
        var NS = "http://www.w3.org/2000/svg";
        var defs = document.createElementNS(NS, "defs");
        var mk = document.createElementNS(NS, "marker");
        mk.setAttribute("id", "lc-rib-arr"); mk.setAttribute("markerWidth", "7"); mk.setAttribute("markerHeight", "7");
        mk.setAttribute("refX", "6"); mk.setAttribute("refY", "3"); mk.setAttribute("orient", "auto");
        var mp = document.createElementNS(NS, "path"); mp.setAttribute("d", "M0,0 L0,6 L7,3 z");
        mp.setAttribute("fill", "#0066cc"); mp.setAttribute("opacity", "0.55");
        mk.appendChild(mp); defs.appendChild(mk); ribbonSvg.appendChild(defs);

        function cardCenter(cardEl) {
          var wr = wrap.getBoundingClientRect(), cr = cardEl.getBoundingClientRect();
          return { x: cr.left - wr.left + cr.width / 2, y: cr.top - wr.top + cr.height / 2 };
        }
        function drawRibbons(srcCard, linkedUrls) {
          /* keep defs, clear only paths */
          Array.from(ribbonSvg.childNodes).forEach(function(n) { if (n !== defs) ribbonSvg.removeChild(n); });
          linkedUrls.forEach(function(url) {
            var tgt = wrap.querySelector('[data-url="' + url + '"]');
            if (!tgt) return;
            var s = cardCenter(srcCard), t = cardCenter(tgt);
            var mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2 - Math.abs(t.x - s.x) * 0.25;
            var path = document.createElementNS(NS, "path");
            path.setAttribute("d", "M" + s.x + "," + s.y + " Q" + mx + "," + my + " " + t.x + "," + t.y);
            path.setAttribute("fill", "none");
            path.setAttribute("stroke", "#0066cc");
            path.setAttribute("stroke-width", "1.5");
            path.setAttribute("stroke-dasharray", "4 3");
            path.setAttribute("opacity", "0.45");
            path.setAttribute("marker-end", "url(#lc-rib-arr)");
            ribbonSvg.appendChild(path);
          });
        }

        wrap.querySelectorAll(".lc-card[data-url]").forEach(function(cardEl) {
          var url = cardEl.getAttribute("data-url");
          var item = urlSet[url];
          if (!item || !item.links || !item.links.length) return;
          cardEl.addEventListener("mouseenter", function() { drawRibbons(cardEl, item.links); });
          cardEl.addEventListener("mouseleave", function() { ribbonSvg.innerHTML = ""; });
        });
      })
      .catch(function(e) {
        wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
      });
  }

  function _applyIAL(root) {
    root.querySelectorAll("p").forEach(function(p) {
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
  }

  // ── LightNode network graph (D3 force-directed fork map) ───────────────────
  function loadD3(cb) {
    if (window.d3) { cb(); return; }
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js";
    s.onload = cb;
    s.onerror = function() {
      var st = document.getElementById("lc-nodes-status");
      if (st) st.textContent = "⚠️ Could not load the graph library.";
    };
    document.head.appendChild(s);
  }

  function upgradeNodes(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var OWNER     = el.getAttribute("owner")  || "michelzam";
    var REPO      = el.getAttribute("repo")   || "lightcodepedia";
    var MAX_DEPTH = parseInt(el.getAttribute("depth")  || "3",   10);
    var H         = parseInt(el.getAttribute("height") || "580", 10);

    var wrap = document.createElement("div");
    wrap.id = "lc-nodes-wrap";
    wrap.style.cssText = "position:relative;margin:1.5em 0";
    wrap.innerHTML = [
      '<style>',
      '.lc-node{transition:opacity .15s}',
      '.lc-node:hover{opacity:.85}',
      '.lc-node-label{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;pointer-events:none}',
      '.lc-link{transition:opacity .2s}',
      '</style>',
      '<svg id="lc-nodes-svg" style="width:100%;height:' + H + 'px;border-radius:14px;background:linear-gradient(135deg,#eef2ff 0%,#f0f9ff 100%);display:block"></svg>',
      '<div id="lc-nodes-tooltip" style="display:none;position:absolute;background:rgba(0,0,0,.72);color:#fff;border-radius:6px;padding:5px 10px;font-size:0.78em;pointer-events:none;white-space:nowrap"></div>',
      '<div id="lc-nodes-popup" style="display:none;position:absolute;background:#fff;border:1px solid #ddd;border-radius:12px;padding:16px;box-shadow:0 8px 32px rgba(0,0,0,.15);min-width:220px;z-index:20">',
      '  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">',
      '    <img id="lc-np-avatar" src="" alt="" style="width:42px;height:42px;border-radius:50%;flex-shrink:0">',
      '    <div style="min-width:0">',
      '      <div id="lc-np-login" style="font-weight:700;font-size:0.95em"></div>',
      '      <div id="lc-np-stats" style="font-size:0.78em;color:#888;margin-top:2px"></div>',
      '    </div>',
      '    <button onclick="document.getElementById(\'lc-nodes-popup\').style.display=\'none\'" style="margin-left:auto;background:none;border:none;cursor:pointer;font-size:1.3em;color:#bbb;line-height:1;padding:0;flex-shrink:0">×</button>',
      '  </div>',
      '  <a id="lc-np-site" href="#" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:8px;padding:9px 12px;border:1px solid #0066cc;border-radius:8px;text-decoration:none;color:#0066cc;font-size:0.85em;margin-bottom:8px;font-weight:500">',
      '    <span>🌐</span><span>Visit LightNode</span><span style="margin-left:auto;font-size:0.85em;opacity:.6">↗</span>',
      '  </a>',
      '  <a id="lc-np-profile" href="#" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:8px;padding:9px 12px;border:1px solid #e0e0e0;border-radius:8px;text-decoration:none;color:#444;font-size:0.85em">',
      '    <span>👤</span><span>GitHub profile</span><span style="margin-left:auto;font-size:0.85em;opacity:.6">↗</span>',
      '  </a>',
      '</div>',
      '<div id="lc-nodes-status" style="text-align:center;color:#888;padding:1em;font-size:0.9em">⏳ Loading the LightNode network…</div>'
    ].join("");
    el.parentNode.replaceChild(wrap, el);

    loadD3(function() { runNodes(); });

    function runNodes() {
      var pat  = localStorage.getItem("lc_ed_pat") || "";
      var hdrs = { "X-GitHub-Api-Version": "2022-11-28", Accept: "application/vnd.github+json" };
      if (pat) hdrs["Authorization"] = "Bearer " + pat;

      var statusEl = document.getElementById("lc-nodes-status");
      var popup    = document.getElementById("lc-nodes-popup");

      var GRAPH_TTL = 3600000;
      var GRAPH_KEY = "lc_nodes_graph", GRAPH_TS_KEY = "lc_nodes_ts";

      var COLORS = ["#f5a623", "#0066cc", "#2a9d2a", "#9b59b6", "#e74c3c"];
      function nodeColor(d) { return COLORS[Math.min(d.level, COLORS.length - 1)]; }

      function apiFetch(url) {
        return fetch(url, { headers: hdrs }).then(function (r) {
          var rem = parseInt(r.headers.get("X-RateLimit-Remaining") || "-1", 10);
          if (rem >= 0) localStorage.setItem("lc_rate_remaining", String(rem));
          if (!r.ok) throw new Error("GitHub API " + r.status + (rem >= 0 ? " (" + rem + " calls left)" : ""));
          return r.json();
        });
      }
      function setStatus(msg) { if (statusEl) statusEl.textContent = msg; }
      function clearStatus()  { if (statusEl) statusEl.textContent = ""; }

      document.addEventListener("click", function (e) {
        if (popup && !popup.contains(e.target)) popup.style.display = "none";
      });

      function rootNode() {
        return {
          id: OWNER + "/" + REPO, login: OWNER,
          avatar: "https://github.com/" + OWNER + ".png",
          level: 0, forkCount: 0, stars: 0, pinned: true
        };
      }

      function buildGraph() {
        var nodes = {}, links = [], rootId = OWNER + "/" + REPO;
        nodes[rootId] = rootNode();
        return Promise.all([
          apiFetch("https://api.github.com/users/" + OWNER).catch(function () { return null; }),
          apiFetch("https://api.github.com/repos/" + OWNER + "/" + REPO).catch(function () { return null; })
        ])
        .then(function (results) {
          var ownerUser = results[0], rootRepo = results[1];
          if (ownerUser && ownerUser.avatar_url) nodes[rootId].avatar = ownerUser.avatar_url;
          if (rootRepo) {
            nodes[rootId].forkCount = rootRepo.forks_count || 0;
            nodes[rootId].stars     = rootRepo.stargazers_count || 0;
          }
          var wave = [{ id: rootId, depth: 0 }];
          function processWave(currentWave) {
            if (!currentWave.length) return;
            var nextWave = [];
            setStatus("⏳ Scanning depth " + (currentWave[0].depth + 1) + "… (" + Object.keys(nodes).length + " nodes)");
            var fetches = currentWave
              .filter(function (w) { return w.depth < MAX_DEPTH; })
              .map(function (w) {
                return apiFetch("https://api.github.com/repos/" + w.id + "/forks?per_page=100&sort=newest")
                  .then(function (forks) {
                    if (nodes[w.id]) nodes[w.id].forkCount = forks.length;
                    forks.forEach(function (f) {
                      if (!nodes[f.full_name]) {
                        nodes[f.full_name] = {
                          id: f.full_name, login: f.owner.login, avatar: f.owner.avatar_url,
                          level: w.depth + 1, forkCount: f.forks_count || 0,
                          stars: f.stargazers_count || 0, pinned: false
                        };
                        links.push({ source: w.id, target: f.full_name });
                        if (f.forks_count > 0 && w.depth + 1 < MAX_DEPTH) {
                          nextWave.push({ id: f.full_name, depth: w.depth + 1 });
                        }
                      }
                    });
                  }).catch(function () {});
              });
            return Promise.all(fetches).then(function () { return processWave(nextWave); });
          }
          return processWave(wave);
        })
        .then(function () { return { nodes: Object.values(nodes), links: links }; });
      }

      var _cachedGraph = null, _cachedTs = parseInt(localStorage.getItem(GRAPH_TS_KEY) || "0", 10);
      try { _cachedGraph = JSON.parse(localStorage.getItem(GRAPH_KEY) || "null"); } catch (e) {}
      var _cacheUsable = _cachedGraph && _cachedGraph.nodes && _cachedGraph.nodes.length > 0;

      if (_cacheUsable && (Date.now() - _cachedTs) < GRAPH_TTL) {
        var _ageMin = Math.round((Date.now() - _cachedTs) / 60000);
        render(_cachedGraph.nodes, _cachedGraph.links);
        if (statusEl) { statusEl.textContent = "📦 cached · " + _ageMin + "m ago — refresh after 1h for live data"; statusEl.style.display = "block"; }
      } else {
        buildGraph()
          .then(function (graph) {
            if (!graph.nodes || !graph.nodes.length) graph = { nodes: [rootNode()], links: [] };
            try { localStorage.setItem(GRAPH_KEY, JSON.stringify(graph)); } catch (e) {}
            localStorage.setItem(GRAPH_TS_KEY, String(Date.now()));
            render(graph.nodes, graph.links);
            if (graph.nodes.length <= 1 && statusEl) {
              statusEl.style.display = "block";
              statusEl.textContent = pat
                ? "No forks yet — be the first to fork and grow the network!"
                : "🔑 Log in (top-right) to load the full network — GitHub limits anonymous requests.";
            } else { clearStatus(); }
          })
          .catch(function (e) {
            if (_cacheUsable) {
              render(_cachedGraph.nodes, _cachedGraph.links);
              setStatus("⚠️ Using cached graph — " + e.message);
            } else {
              render([rootNode()], []);
              if (statusEl) { statusEl.style.display = "block"; statusEl.textContent = "⚠️ " + e.message + (pat ? "" : " — log in (top-right) for the full network."); }
            }
          });
      }

      function showPopup(event, d) {
        var box     = wrap.getBoundingClientRect();
        var siteUrl = d.level === 0
          ? "https://lightcodepedia.org"
          : "https://" + d.login + ".github.io/lightcodepedia";
        var px = event.clientX - box.left + 16;
        var py = event.clientY - box.top  - 16;
        if (px + 240 > box.width)  px = event.clientX - box.left - 256;
        if (py + 180 > box.height) py = event.clientY - box.top  - 170;
        popup.style.left = Math.max(4, px) + "px";
        popup.style.top  = Math.max(4, py) + "px";
        var stats = [];
        if (d.stars     > 0) stats.push("⭐ " + d.stars);
        if (d.forkCount > 0) stats.push("🍴 " + d.forkCount);
        if (d.level     > 0) stats.push("depth " + d.level);
        document.getElementById("lc-np-avatar").src        = d.avatar;
        document.getElementById("lc-np-login").textContent = "@" + d.login;
        document.getElementById("lc-np-stats").textContent = stats.join(" · ");
        document.getElementById("lc-np-site").href         = siteUrl;
        document.getElementById("lc-np-profile").href      = "https://github.com/" + d.login;
        popup.style.display = "block";
      }

      function render(nodes, links) {
        var W   = wrap.offsetWidth || 900;
        var svg = d3.select("#lc-nodes-svg").attr("viewBox", "0 0 " + W + " " + H);
        svg.on("click", function () { popup.style.display = "none"; });
        var defs = svg.append("defs");
        nodes.forEach(function (d) {
          defs.append("clipPath").attr("id", "lc-clip-" + d.login)
            .append("circle").attr("r", radius(d));
        });
        function radius(d) { return d.level === 0 ? 36 : Math.max(16, 28 - d.level * 4); }
        var sim = d3.forceSimulation(nodes)
          .force("link", d3.forceLink(links).id(function (d) { return d.id; })
            .distance(function (l) { return 120 + l.source.level * 30; }).strength(0.6))
          .force("charge", d3.forceManyBody().strength(function (d) { return d.level === 0 ? -700 : -300; }))
          .force("center",  d3.forceCenter(W / 2, H / 2))
          .force("collide", d3.forceCollide().radius(function (d) { return radius(d) + 10; }))
          .alphaDecay(0.012);
        var root = nodes.find(function (d) { return d.level === 0; });
        if (root) { root.fx = W / 2; root.fy = H / 2; }
        var link = svg.append("g").selectAll("line").data(links).join("line")
          .attr("class", "lc-link")
          .attr("stroke", function (d) { return nodeColor(d.source); })
          .attr("stroke-width", function (d) { return d.source.level === 0 ? 1.8 : 1.2; })
          .attr("stroke-dasharray", "5 3").attr("opacity", 0.5);
        var node = svg.append("g").selectAll("g").data(nodes).join("g")
          .attr("class", "lc-node").attr("cursor", "pointer")
          .on("click", function (event, d) { event.stopPropagation(); showPopup(event, d); })
          .call(dragBehavior(sim));
        node.append("circle").attr("r", function (d) { return radius(d) + 6; })
          .attr("fill", nodeColor).attr("opacity", 0.1);
        node.append("circle").attr("r", radius).attr("fill", "#fff")
          .attr("stroke", nodeColor).attr("stroke-width", 2.5);
        node.append("image")
          .attr("href",   function (d) { return d.avatar; })
          .attr("x",      function (d) { return -radius(d); })
          .attr("y",      function (d) { return -radius(d); })
          .attr("width",  function (d) { return radius(d) * 2; })
          .attr("height", function (d) { return radius(d) * 2; })
          .attr("clip-path", function (d) { return "url(#lc-clip-" + d.login + ")"; })
          .attr("preserveAspectRatio", "xMidYMid slice");
        node.append("text").attr("class", "lc-node-label")
          .attr("y", function (d) { return radius(d) + 14; }).attr("text-anchor", "middle")
          .attr("font-size", function (d) { return d.level === 0 ? "13px" : Math.max(9, 11 - d.level) + "px"; })
          .attr("fill", "#333").attr("font-weight", function (d) { return d.level === 0 ? "700" : "400"; })
          .text(function (d) { return "@" + d.login; });
        node.filter(function (d) { return d.stars > 0; })
          .append("text").attr("class", "lc-node-label")
          .attr("y", function (d) { return radius(d) + 25; }).attr("text-anchor", "middle")
          .attr("font-size", "9px").attr("fill", "#c47900")
          .text(function (d) { return "⭐ " + d.stars; });
        var tip = d3.select("#lc-nodes-tooltip");
        node
          .on("mouseenter", function (event, d) {
            var parts = ["@" + d.login];
            if (d.stars)     parts.push("⭐ " + d.stars);
            if (d.forkCount) parts.push("🍴 " + d.forkCount);
            tip.style("display", "block").text(parts.join("  "));
          })
          .on("mousemove", function (event) {
            var box = wrap.getBoundingClientRect();
            tip.style("left", (event.clientX - box.left + 14) + "px")
               .style("top",  (event.clientY - box.top  - 32) + "px");
          })
          .on("mouseleave", function () { tip.style("display", "none"); });
        sim.on("tick", function () {
          link.attr("x1", function (d) { return d.source.x; })
              .attr("y1", function (d) { return d.source.y; })
              .attr("x2", function (d) { return d.target.x; })
              .attr("y2", function (d) { return d.target.y; });
          node.attr("transform", function (d) {
            var r = radius(d) + 10;
            d.x = Math.max(r, Math.min(W - r, d.x));
            d.y = Math.max(r, Math.min(H - r, d.y));
            return "translate(" + d.x + "," + d.y + ")";
          });
        });
      }

      function dragBehavior(sim) {
        return d3.drag()
          .on("start", function (event, d) {
            if (!event.active) sim.alphaTarget(0.35).restart();
            d.fx = d.x; d.fy = d.y;
          })
          .on("drag",  function (event, d) { d.fx = event.x; d.fy = event.y; })
          .on("end",   function (event, d) {
            if (!event.active) sim.alphaTarget(0);
            if (!d.pinned) { d.fx = null; d.fy = null; }
          });
      }
    }
  }

  // ── Menu: turn markdown links into a horizontal nav bar ────────────────────
  // The same link format that powers the site's own top bar (see menu.md):
  //   [🎓 Tutorial](/t) [🧩 Components](/c)
  //   {: .menu }
  // ── GitHub deploy/activity list (Actions runs) ─────────────────────────────
  function upgradeDeploys(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var count    = parseInt(el.getAttribute("count") || "8", 10);
    var repoAttr = el.getAttribute("repo") || "";
    var dsId     = el.getAttribute("id") || "deploys";

    /* hide source element like a .dataset block */
    el.style.display = "none";

    /* inject a small control bar right after the hidden element */
    var bar = document.createElement("div");
    bar.className = "lc-deploys-bar";
    bar.innerHTML = [
      '<style>',
      '.lc-deploys-bar{display:flex;align-items:center;gap:8px;font-size:.82em;color:#6b7280;margin:.25em 0}',
      '.lc-deploys-bar strong{color:#374151}',
      '.lc-deploys-bar-sp{margin-left:auto}',
      '.lc-deploys-bar-btn{border:1px solid #d1d5db;background:#fff;border-radius:4px;cursor:pointer;font-size:1em;padding:0 .4em;line-height:1.7;color:#374151}',
      '.lc-deploys-bar-btn:hover{background:#f3f4f6}',
      '</style>',
      '<strong>🚀 Deploys</strong>',
      '<span class="lc-deploys-bar-sp" id="lc-dep-sp-' + dsId + '"></span>',
      '<button class="lc-deploys-bar-btn" id="lc-dep-btn-' + dsId + '" title="Refresh">↻</button>'
    ].join("");
    el.parentNode.insertBefore(bar, el.nextSibling);

    var spEl  = bar.querySelector("#lc-dep-sp-"  + dsId);
    var btnEl = bar.querySelector("#lc-dep-btn-" + dsId);

    var pat = localStorage.getItem("lc_ed_pat") || "";
    if (!pat) {
      spEl.innerHTML = '🔒 <a href="#" style="color:inherit">Sign in</a> to see deployment activity';
      btnEl.style.display = "none"; return;
    }

    var repo = repoAttr || localStorage.getItem("lc_ed_repo") || "";
    if (!repo) {
      var u = null; try { u = JSON.parse(localStorage.getItem("lc_gh_user") || "null"); } catch (e) {}
      if (u && u.login) repo = u.login + "/lightcodepedia";
    }
    if (!repo || repo.indexOf("/") < 0) { spEl.textContent = "⚠️ No repo configured"; return; }

    function timeAgo(iso) {
      var s = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
      if (s < 60) return s + "s ago";
      var m = Math.floor(s / 60); if (m < 60) return m + "m ago";
      var h = Math.floor(m / 60); if (h < 24) return h + "h ago";
      return Math.floor(h / 24) + "d ago";
    }
    function statusIcon(r) {
      if (r.status !== "completed") {
        return r.status === "queued" || r.status === "waiting" || r.status === "pending" ? "⏳" : "🔄";
      }
      switch (r.conclusion) {
        case "success":   return "✅";
        case "failure":
        case "timed_out": return "❌";
        case "cancelled": return "🚫";
        case "skipped":   return "⏭️";
        default:          return "⚪";
      }
    }
    function normalize(runs) {
      return runs.map(function (r) {
        var commit = ((r.display_title || (r.head_commit && r.head_commit.message) || r.name || "Run") + "").split("\n")[0];
        var state  = r.status === "completed" ? (r.conclusion || "done") : r.status.replace(/_/g, " ");
        var author = r.actor && r.actor.login ? "@" + r.actor.login : "";
        return { status: statusIcon(r), commit: commit, workflow: r.name || "", state: state,
                 when: timeAgo(r.created_at), author: author, url: r.html_url || "" };
      });
    }

    var pollTimer = null, polls = 0;
    function fetchRuns() {
      spEl.textContent = "Loading…";
      fetch("https://api.github.com/repos/" + repo + "/actions/runs?per_page=" + count, {
        headers: { Authorization: "Bearer " + pat, "X-GitHub-Api-Version": "2022-11-28", Accept: "application/vnd.github+json" }
      })
      .then(function (r) {
        var rem = parseInt(r.headers.get("X-RateLimit-Remaining") || "-1", 10);
        if (rem >= 0) localStorage.setItem("lc_rate_remaining", String(rem));
        if (!r.ok) throw new Error("GitHub API " + r.status);
        return r.json();
      })
      .then(function (data) {
        var runs = (data.workflow_runs || []).slice(0, count);
        if (!runs.length) {
          if (window.lcSetDataset) window.lcSetDataset(dsId, []);
          spEl.textContent = "No runs yet"; return;
        }
        var rows = normalize(runs);
        if (window.lcSetDataset) window.lcSetDataset(dsId, rows);
        var ongoing = runs.some(function (r) { return r.status !== "completed"; });
        spEl.textContent = ongoing ? "● live" : "updated " + new Date().toLocaleTimeString();
        clearTimeout(pollTimer);
        if (ongoing && polls < 25) { polls++; pollTimer = setTimeout(fetchRuns, 12000); }
        else polls = 0;
      })
      .catch(function (e) {
        spEl.textContent = "⚠️ " + e.message;
        if (window.lcSetDataset) window.lcSetDataset(dsId, []);
      });
    }
    btnEl.addEventListener("click", function () { polls = 0; fetchRuns(); });
    window.addEventListener("pagehide", function () { clearTimeout(pollTimer); });
    fetchRuns();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }

})();
</script>
