<script>
(function(){
  if (window._lcCoreReady) return;
  window._lcCoreReady = true;
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
  window.lcLoadJsYaml = loadJsYaml;

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
  // Inline kramdown span-IAL the live (marked) renderers can't do: turn
  // "<em>word</em>{: .red}" into "<em class=\"red\">word</em>" so colour classes
  // (and any inline class) work in mdpad / the editor / section widgets, matching
  // what kramdown emits server-side. Literal IAL inside `code spans` is untouched.
  function inlineIAL(html) {
    // [^<] for the carrier's content so the match can't span across other tags
    // (a lazy .*? would stretch from an earlier <em> to a later </em>{: .x})
    return String(html).replace(
      /<(em|strong|code|a)\b([^>]*)>([^<]*)<\/\1>\s*\{:\s*([^}]*?)\s*\}/g,
      function (m, tag, attrs, inner, ial) {
        var cls = (ial.match(/\.[-\w]+/g) || []).map(function (c) { return c.slice(1); });
        if (!cls.length) return m;
        if (/\bclass\s*=\s*"/.test(attrs)) {
          attrs = attrs.replace(/class\s*=\s*"([^"]*)"/, function (mm, ex) { return 'class="' + ex + " " + cls.join(" ") + '"'; });
        } else {
          attrs += ' class="' + cls.join(" ") + '"';
        }
        return "<" + tag + attrs + ">" + inner + "</" + tag + ">";
      }
    );
  }
  function markdownBody(s) {
    /* ensure IAL tags land on their own paragraph so _applyIAL can process them */
    var norm = s.replace(/([^\n])\n(\{:)/g, "$1\n\n$2");
    return window.marked ? inlineIAL(marked.parse(norm)) : "<pre>" + s + "</pre>";
  }
  window.lcLoadMarked = loadMarked;
  window.lcInlineIAL = inlineIAL;
  window.lcParseSections = parseSections;
  window.lcMarkdownBody = markdownBody;
  window.lcScanElement = scanElement;
  window.lcApplyIAL   = _applyIAL;
  window.lcRegisterUpgrader = lcRegisterUpgrader;

  function _applyIAL(root) {
    root.querySelectorAll("p").forEach(function(p) {
      var t = (p.textContent || "").trim();
      var m = t.match(/^\{:\s*(.+?)\s*\}$/);
      if (!m) return;
      var prev = p.previousElementSibling;
      if (!prev) return;
      var body = m[1];
      var kv, kvRe = /([\w-]+)="([^"]*)"/g;
      while ((kv = kvRe.exec(body)) !== null) prev.setAttribute(kv[1], kv[2]);
      /* .class and #id shorthands are read from the declaration minus the
         key="value" pairs, so dots/hashes inside attribute values (href="#x",
         title="v1.2") cannot leak in as bogus classes or ids */
      var rest = body.replace(/([\w-]+)="([^"]*)"/g, " ");
      var c, classRe = /\.([\w-]+)/g;
      while ((c = classRe.exec(rest)) !== null) prev.classList.add(c[1]);
      var idM = rest.match(/#([\w-]+)/);
      if (idM) prev.id = idM[1];
      p.parentNode.removeChild(p);
    });
  }

  // The same link format that powers the site's own top bar (see menu.md):
  //   [🎓 Tutorial](/t) [🧩 Components](/c)
  //   {: .menu }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }

})();
</script>
