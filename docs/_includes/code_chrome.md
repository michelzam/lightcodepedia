<script>
(function(){
  if (window._lcCoreReady) return;
  window._lcCoreReady = true;
  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  /* ── Base path (project Pages) ──────────────────────────────────────
     pedia lives at a domain root; the lab and every fork live under
     /<repo>/ on github.io, where root-absolute URLs in content
     ("/assets/lab.jpg", "/_dog") silently 404. lcBase is "" at a root
     and "/<repo>" under a project path; lcHref() resolves one path;
     lcRebase() heals media and links in a subtree. */
  var _lcRepoName = {{ site.github.repository_name | default: "" | jsonify }};
  /* private repo? unpublished (_-prefixed) nodes 404 on raw for anonymous
     visitors here, so components skip fetching them and invite a PAT instead. */
  window.lcRepoPrivate = {{ site.github.private | default: false | jsonify }};
  var _lcSeg = "/" + _lcRepoName + "/";
  window.lcBase = (_lcRepoName &&
    (location.pathname === _lcSeg.slice(0, -1) || location.pathname.indexOf(_lcSeg) === 0))
    ? _lcSeg.slice(0, -1) : "";
  window.lcHref = function (p) {
    return (window.lcBase && p && p.charAt(0) === "/" && p.indexOf("//") !== 0 &&
            p.indexOf(window.lcBase + "/") !== 0) ? window.lcBase + p : p;
  };
  window.lcRebase = function (root) {
    if (!window.lcBase) return;
    (root || document).querySelectorAll(
      'img[src^="/"], video[src^="/"], audio[src^="/"], source[src^="/"]'
    ).forEach(function (el) {
      var v = el.getAttribute("src"), w = window.lcHref(v);
      if (w !== v) el.setAttribute("src", w);
    });
    (root || document).querySelectorAll('a[href^="/"]').forEach(function (el) {
      var v = el.getAttribute("href"), w = window.lcHref(v);
      if (w !== v) el.setAttribute("href", w);
    });
  };
  document.addEventListener("DOMContentLoaded", function () { window.lcRebase(document); });

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

  // Stash each id'd source block's markup BEFORE it is upgraded, so a later
  // inline editor (X-ray edit) can read its knobs/content and re-render it.
  var _srcSnap = {};
  function _snapshotSources(root) {
    root.querySelectorAll("[id]").forEach(function (el) {
      if (el.id && _srcSnap[el.id] === undefined && !el.dataset.lcUpgraded) _srcSnap[el.id] = el.outerHTML;
    });
  }
  window.lcSourceOf = function (id) { return _srcSnap[id]; };
  window.lcSnapshotSources = _snapshotSources;   // runner: snapshot RT fences pre-upgrade
  window.lcSetSourceOf = function (id, html) { _srcSnap[id] = html; };   // xray: refresh after a kept edit

  /* ── kramdown footnotes for the client pipeline ─────────────────────
     marked has no footnote syntax, so [^x] refs and [^x]: defs stay raw in
     any client render (runner, previews). Transform the markdown to the same
     DOM kramdown emits (<sup id="fnref:x"><a class="footnote">, div.footnotes)
     so the page CSS and tips keep working. Fenced code is shielded — a doc
     SHOWING footnote syntax must not have its examples eaten. Call with
     marked loaded (note bodies render through marked.parseInline). */
  window.lcClientFootnotes = function (md) {
    if (md.indexOf("[^") < 0) return md;
    var fences = [];
    md = md.replace(/(`{3,})[^\n]*\n[\s\S]*?\1|`[^`\n]+`/g, function (m) {
      fences.push(m); return " LCFN" + (fences.length - 1) + " ";
    });
    var defs = {}, order = [];
    md = md.replace(/^\[\^([^\]\s]+)\]:[ \t]?(.*(?:\n[ \t]+.*)*)/gm, function (_, id, body) {
      defs[id] = body.replace(/\n[ \t]+/g, " ").trim(); return "";
    });
    function replaceRefs(text) {
      return text.replace(/\[\^([^\]\s]+)\]/g, function (m, id) {
        if (!(id in defs)) return m;                     // undefined ref: leave raw
        if (order.indexOf(id) < 0) order.push(id);
        var n = order.indexOf(id) + 1;
        return '<sup id="fnref:' + id + '"><a href="#fn:' + id + '" class="footnote">' + n + "</a></sup>";
      });
    }
    md = replaceRefs(md);
    if (order.length) {
      var inline = (window.marked && window.marked.parseInline)
        ? function (s) { try { return window.marked.parseInline(s); } catch (e) { return s; } }
        : function (s) { return s; };
      /* a def body may itself reference a footnote (kramdown allows it) —
         replace inside bodies too; order grows as nested defs are pulled in */
      var items = [];
      for (var i = 0; i < order.length; i++) {
        var id = order[i];
        items.push('<li id="fn:' + id + '"><p>' + inline(replaceRefs(defs[id])) +
                   ' <a href="#fnref:' + id + '" class="reversefootnote">&#8617;</a></p></li>');
      }
      md += '\n\n<div class="footnotes"><ol>' + items.join("") + "</ol></div>\n";
    }
    return md.replace(/ LCFN(\d+) /g, function (_, i) { return fences[+i]; });
  };

  /* Includes render inside <main class="markdown-body">. Reel mode turns
     that element into an iOS touch-scroller, and position:fixed descendants
     of such a scroller scroll WITH the content on Safari (the "bottom bar
     rides up" bug). Floating chrome therefore must live directly on <body> —
     re-home it once, before the first upgrade pass. */
  var _CHROME = ['.lc-slides-fab', '#lc-bl-popup', '.lc-reel-bar', '.lc-slides-nav',
                 '.lc-slides-share-overlay', '#ed-fab', '#ed-drawer', '#ed-sidebar'];
  function _rehomeChrome() {
    _CHROME.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        if (el.parentNode && el.parentNode !== document.body) document.body.appendChild(el);
      });
    });
  }

  function scan() {
    _rehomeChrome();
    _applyIAL(document);
    _snapshotSources(document);
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
    // Component-injected media/links carry root-absolute paths ("/assets/…")
    // that 404 under a project base (/lightcodelab, forks). Page-level lcRebase
    // ran at DOMContentLoaded, before this subtree existed — heal it now, at the
    // one place every component's HTML lands. Idempotent; a no-op at a domain root.
    if (window.lcRebase) window.lcRebase(root);
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

  // ── exclusive page-mode manager ──────────────────────────────────────────
  // ONE way of experiencing the page at a time: read (default) · present ·
  // reel · xray · edit. Engines register {enter, exit, isActive}; every entry
  // point (pill, FABs, URLs) routes through set(), which exits the current
  // mode first — conflicting combinations (reel while editing…) become
  // structurally impossible. An exit may veto (e.g. unsaved edit confirm):
  // if the old mode is still active after exit(), the switch is aborted.
  var _lcModes = {};
  window.lcMode = {
    register: function (name, api) { _lcModes[name] = api || {}; },
    current: function () {
      for (var k in _lcModes) {
        try { if (_lcModes[k].isActive && _lcModes[k].isActive()) return k; } catch (e) {}
      }
      return "read";
    },
    set: function (name) {
      var cur = window.lcMode.current();
      if (name === cur) name = "read";              // re-selecting the active mode exits it
      if (cur !== "read" && _lcModes[cur]) {
        try { _lcModes[cur].exit(); } catch (e) {}
        try { if (_lcModes[cur].isActive && _lcModes[cur].isActive()) return false; } catch (e) {}
      }
      if (name !== "read" && _lcModes[name]) { try { _lcModes[name].enter(); } catch (e) {} }
      try { document.dispatchEvent(new CustomEvent("lc-mode-changed", { detail: { mode: window.lcMode.current() } })); } catch (e) {}
      return true;
    }
  };

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
<script>
/* ── Node variables ────────────────────────────────────────────────────
   Generic per-node configuration: the connected repo's Actions VARIABLES
   (Settings → Secrets and variables → Variables), fetched once with the
   author key. They resolve only for who is connected to THEIR node —
   visitors get the gentle defaults. Cells read them via get_var(NAME,
   default); knobs via the "= get_var('NAME','default')" form. Values land
   in the store under node.* (reactive: cells recompute on arrival). */
(function () {
  if (window.lcNodeVars) return;
  var p = null;
  window.lcNodeVars = function () {
    if (p) return p;
    var pat = "", repo = "";
    try { pat = localStorage.getItem("lc_ed_pat") || ""; repo = localStorage.getItem("lc_ed_repo") || ""; } catch (e) {}
    if (!pat || !repo) { window._lcNodeVars = {}; return (p = Promise.resolve({})); }
    p = fetch("https://api.github.com/repos/" + repo + "/actions/variables?per_page=100",
        { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }, cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        var m = {};
        ((d && d.variables) || []).forEach(function (v) { m[v.name] = v.value; });
        window._lcNodeVars = m;
        if (window.lcStore && window.lcStore.set) { try { window.lcStore.set("node", m); } catch (e) {} }
        return m;
      })
      .catch(function () { window._lcNodeVars = {}; return {}; });
    return p;
  };
  /* knob-cell: "= get_var('NAME', 'default')" → the resolved value.
     Anything else passes through untouched. */
  window.lcResolveKnob = function (val) {
    var m = /^=\s*get_var\(\s*['"]([^'"]+)['"]\s*(?:,\s*['"]([^'"]*)['"]\s*)?\)\s*$/.exec((val || "").trim());
    if (!m) return Promise.resolve(val);
    return window.lcNodeVars().then(function (vars) {
      if (vars && vars[m[1]] !== undefined && vars[m[1]] !== "") return vars[m[1]];
      return m[2] !== undefined ? m[2] : "";
    });
  };
})();
</script>
<script>
/* Private-tool IALs (HQ engines like the classroom): on builds that don't
   carry the engine, their trigger paragraphs HIDE instead of rendering dead
   links — pages stay byte-identical across nodes, no Liquid in content. */
(function () {
  function sweep() {
    document.querySelectorAll("p.classroom_console, p.classroom_actions").forEach(function (el) {
      if (!el.dataset.lcUpgraded) el.style.display = "none";
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { setTimeout(sweep, 400); });
  else setTimeout(sweep, 400);
})();
</script>
