{%- comment -%}
Dataset / Datagrid — data binding primitives.

.dataset  — hidden block that parses + registers data
.datagrid — sortable paginated table bound to a dataset
(.chart — bound and inline variants — lives in chart.md)

Usage:
  ```json
  [{"month":"Jan","sales":100},{"month":"Feb","sales":150}]
  ```
  {: .dataset #sales }

  [Sales Table](#)
  {: .datagrid bind="sales" rows="5" }

Formats: JSON (default) or CSV are auto-detected; add format="yaml" to parse a
YAML block. Arrays register as rows; a plain object (e.g. a schema/index) is
registered as-is, so components like .record can read structured config.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* ── dataset (invisible) ───────────────────────────── */
.highlighter-rouge.dataset, .dataset { display: none !important; }

/* ── datagrid ──────────────────────────────────────── */
.lc-datagrid { margin: 1em 0; font-size: 0.88em; overflow-x: auto; }
/* a titled grid: the form's bar at the form's size (the grid's text is 0.88em) */
.lc-datagrid .lc-dg-titlebar { font-size: 0.966em; }
.lc-datagrid .lc-dg-titlebar .lc-datagrid-name { color: #222; font-weight: 600; }
.lc-dg-table { width: 100%; border-collapse: collapse; }
.lc-dg-table th, .lc-dg-table td { padding: 0.4em 0.75em; border: 1px solid #e5e7eb; text-align: left; white-space: nowrap; }
.lc-dg-table th { background: #f9fafb; font-weight: 600; color: #374151; cursor: pointer; user-select: none; }
.lc-dg-table th.lc-th-hint { text-decoration: underline dotted #9ca3af; text-underline-offset: 3px; cursor: help; }
.lc-dg-table th:hover { background: #f3f4f6; }
/* an editable cell has to LOOK editable — a dotted underline and a caret,
   so a reader sees where the page invites them to type */
.lc-dg-table td.lc-dg-edit { cursor: text; background: #fcfdff;
  border-bottom: 1px dashed #9db6d0; }
.lc-dg-table td.lc-dg-edit:focus { outline: 2px solid #0066cc; outline-offset: -2px;
  background: #fff; }
.lc-dg-table tr:nth-child(even) td { background: #fafafa; }
.lc-dg-table td { color: #111827; user-select: text; }
.lc-dg-scroll { overflow: auto; }
.lc-dg-scroll .lc-dg-table thead th { position: sticky; top: 0; z-index: 1; }
.lc-dg-pages { display: flex; align-items: center; gap: 0.5em; margin-top: 0.5em; font-size: 0.82em; color: #6b7280; }
.lc-dg-pages button { background: none; border: 1px solid #d1d5db; border-radius: 4px; padding: 0.15em 0.55em; cursor: pointer; color: #374151; }
.lc-dg-pages button:hover { background: #f3f4f6; }
.lc-dg-table tbody tr { cursor: pointer; }
.lc-dg-table tr.lc-dg-selected td { background: #e8f0fe !important; }
/* A CLASS IS A DATASET (Michel, 2026-10-15): a grid on a class dresses the
   rows — the state cell wears a ⌄ that drops the row's verbs, legal ones
   live and the others grey; typed cells; ➕ New under the list. */
.lc-datagrid { position: relative; }
.lc-dg-table td.lc-dg-typed { border-bottom: 1px dashed #9db6d0; }
.lc-dg-table td.lc-dg-typed:focus { outline: 2px solid #0066cc; outline-offset: -2px; background: #fff; }
.lc-dg-table td.lc-dg-state { cursor: pointer; white-space: nowrap; }
/* the chip and the ⌄ sit on the row's own text line: an inline chip (its
   padding never lifts the line), the ⌄ nudged up to the x-height — a block
   chip rode high and a floated ⌄ sank (Michel, 2026-10-16) */
.lc-dg-chip { display: inline-block; vertical-align: baseline; background: #eef2ff; color: #3730a3; border-radius: 1em; padding: 0 .6em; line-height: 1.45; }
/* every stage's chip as wide as the longest stage: the ⌄ line up in one column (Michel, 2026-10-16) */
.lc-dg-state .lc-dg-chip { box-sizing: content-box; }
.lc-dg-caret { display: inline-block; margin-left: .45em; color: #6b7280; position: relative; top: -.22em; line-height: 1; }
.lc-dg-state .lc-dg-chip { text-align: center; }
.lc-dg-table th { position: relative; }
/* the grip SHOWS (Michel, 2026-10-16: "why can't the columns be resized?" —
   an invisible 7 px strip, and a click beside it sorted instead): a thin bar
   on every header's right edge, blue under the pointer, 10 px to grab */
.lc-dg-grip { position: absolute; top: 15%; right: 0; width: 10px; height: 70%; cursor: col-resize; z-index: 2; touch-action: none;
  background: linear-gradient(90deg, transparent 4px, #cbd5e1 4px, #cbd5e1 6px, transparent 6px); }
.lc-dg-grip:hover, .lc-dg-grip:active { background: linear-gradient(90deg, transparent 3px, #0066cc 3px, #0066cc 7px, transparent 7px); }
/* ⋯ THE GUTTER (Michel, 2026-10-17: "when there is no state, a gutter with
   a simple discrete/light but intuitive way to open the method picklist") */
.lc-dg-table th.lc-dg-gut, .lc-dg-table td.lc-dg-gut { width: 1.7em; min-width: 1.7em; padding: 0 .15em; text-align: center; }
.lc-dg-table td.lc-dg-gut .lc-dg-rowmenu { border: 0; background: none; cursor: pointer; font: inherit; font-size: 1.05em; line-height: 1;
  padding: .15em .3em; border-radius: 6px; color: #94a3b8; opacity: .45; transition: opacity .12s; }
.lc-dg-table tr:hover td.lc-dg-gut .lc-dg-rowmenu, .lc-dg-table tr.lc-dg-selected td.lc-dg-gut .lc-dg-rowmenu,
.lc-dg-table td.lc-dg-gut .lc-dg-rowmenu:focus-visible { opacity: 1; color: #0066cc; }
.lc-dg-table td.lc-dg-gut .lc-dg-rowmenu:hover { background: #eff6ff; }
.lc-dg-table td.lc-dg-gut .lc-dg-rowmenu.lc-dg-kindmark { opacity: 1; color: inherit; }
/* THE CORNER (Michel, 2026-10-17: "a delicate refresh spiral arrow on top
   right, better visible on hovering, a similar more stable one for save, and
   a + round little button"): + always, ↻ on hover, the save state always */
.lc-datagrid { position: relative; }
.lc-dg-corner { position: absolute; top: .3em; right: .4em; z-index: 2; display: flex; gap: .3em; align-items: center; }
.lc-dg-cbtn { width: 1.65em; height: 1.65em; border-radius: 50%; border: 1px solid #c7d2e0; background: #fff; color: #475569;
  font: inherit; font-size: .9em; line-height: 1; padding: 0; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; }
.lc-dg-cbtn:hover, .lc-dg-cbtn:focus-visible { border-color: #0066cc; color: #0066cc; background: #eff6ff; }
.lc-dg-cbtn.lc-dg-new { background: #0066cc; border-color: #0066cc; color: #fff; font-size: 1em; }
.lc-dg-cbtn.lc-dg-new:hover { background: #0052a3; color: #fff; }
.lc-dg-cbtn.lc-dg-refresh { opacity: 0; transition: opacity .15s; }
.lc-datagrid:hover .lc-dg-cbtn.lc-dg-refresh, .lc-dg-cbtn.lc-dg-refresh:focus-visible { opacity: 1; }
@media (hover: none) { .lc-dg-cbtn.lc-dg-refresh { opacity: .6; } }
.lc-dg-cbtn.lc-dg-save[disabled] { cursor: default; }
.lc-dg-cbtn.lc-dg-refresh.lc-dg-pending { opacity: 1; position: relative; color: #0066cc; border-color: #93c5fd; }
.lc-dg-cbtn.lc-dg-refresh.lc-dg-pending::after { content: ""; position: absolute; top: -2px; right: -2px; width: 7px; height: 7px; border-radius: 50%; background: #f59e0b; }
.lc-dg-cbtn.lc-dg-st-ok { color: #16a34a; border-color: #bbf7d0; }
.lc-dg-cbtn.lc-dg-st-dirty { color: #b45309; border-color: #fcd34d; }
.lc-dg-cbtn.lc-dg-st-saving { color: #0066cc; }
.lc-dg-cbtn.lc-dg-st-saving span { display: inline-block; animation: lc-dg-spin 1s linear infinite; }
.lc-dg-cbtn.lc-dg-st-error { color: #b91c1c; border-color: #fca5a5; background: #fef2f2; }
@keyframes lc-dg-spin { to { transform: rotate(360deg); } }
.lc-datagrid.lc-dg-cornered:not(.lc-dg-titled) .lc-dg-body, .lc-datagrid.lc-dg-cornered:not(.lc-dg-titled) > .lc-dg-scroll,
.lc-datagrid.lc-dg-cornered:not(.lc-dg-titled) > table { margin-top: 2.1em; }
.lc-dg-table td.lc-dg-typed.lc-dg-typing { background: #fff; outline: 2px solid #0066cc; outline-offset: -2px; cursor: text; }
.lc-dg-state:hover .lc-dg-caret { color: #0066cc; }
.lc-dg-table td.lc-dg-refcell { cursor: pointer; white-space: nowrap; position: relative; padding-right: 1.6em; }
.lc-dg-table td.lc-dg-refcell .lc-dg-caret { position: absolute; right: .55em; top: 50%; transform: translateY(-62%); margin: 0; }
.lc-dg-table td.lc-dg-refcell:hover .lc-dg-caret { color: #0066cc; }
.lc-dg-refmenu { max-height: 16em; overflow-y: auto; }
.lc-dg-refmenu .lc-dg-cur { background: #eff6ff; font-weight: 600; }
.lc-dg-refsearch { display: block; width: calc(100% - .8em); margin: .3em .4em; font: inherit; padding: .25em .45em; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
.lc-dg-pick { font: inherit; font-size: .95em; border: 1px solid #d1d5db; border-radius: 4px; background: #fff; padding: .1em .3em; }
.lc-dg-menu { position: absolute; z-index: 1000; background: #fff; border: 1px solid #d1d5db; border-radius: 8px; box-shadow: 0 6px 18px rgba(0,0,0,.14); padding: .25em; min-width: 11em; }
.lc-dg-verb { display: flex; justify-content: space-between; gap: 1em; width: 100%; text-align: left; background: none; border: 0; padding: .4em .7em; cursor: pointer; font: inherit; color: #111827; border-radius: 5px; }
.lc-dg-verb:hover { background: #f3f4f6; }
.lc-dg-verb small { color: #6b7280; }
.lc-dg-verb.lc-dg-off { color: #9ca3af; }
.lc-dg-verb.lc-dg-off small { color: #c4c7cc; }
.lc-dg-verb.lc-dg-danger { color: #b91c1c; border-top: 1px solid #eee; border-radius: 0 0 5px 5px; }
.lc-dg-btn { font: inherit; font-size: .85em; font-weight: 500; padding: .35em 1em; border-radius: 6px; border: 1px solid #0066cc; background: #fff; color: #0066cc; cursor: pointer; }
.lc-dg-btn:hover:not(:disabled) { background: #eff6ff; }
.lc-dg-btn:disabled { opacity: .45; cursor: default; }
.lc-dg-reload { float: right; font: inherit; font-size: 1em; line-height: 1; padding: .1em .45em; border-radius: 6px;
  border: 1px solid #cbd5e1; background: #fff; color: #0066cc; cursor: pointer; }
.lc-dg-reload:hover { background: #eff6ff; border-color: #0066cc; }
.lc-ds-key { display: flex; flex-wrap: wrap; gap: .5em; align-items: center; margin: .6em 0; padding: .55em .8em;
  border: 1px dashed #93c5fd; border-radius: 8px; background: #f8fbff; font-size: .9em; color: #1e3a8a; }
.lc-ds-key input { flex: 1 1 16em; font: inherit; padding: .3em .5em; border: 1px solid #cbd5e1; border-radius: 6px; }
.lc-ds-key button { font: inherit; font-weight: 500; padding: .3em 1em; border-radius: 6px; border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; }
.lc-dg-unl { display: flex; flex-wrap: wrap; align-items: center; gap: .4em .6em; margin-top: .4em; font-size: .9em; }
.lc-dg-unl code { user-select: all; }
.lc-dg-unl input { font: inherit; padding: .2em .4em; border: 1px solid #cbd5e1; border-radius: 4px; min-width: 12em; }
.lc-dg-unl-me { background: none; border: 0; color: #2563eb; cursor: pointer; font: inherit; padding: 0; text-decoration: underline; }
.lc-dg-unl-note { color: #64748b; }
.lc-dg-say { margin-top: .4em; padding: .35em .7em; border-radius: 6px; background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; font-size: .9em; }

/* ── button ─────────────────────────────────────────── */
.lc-button { display: inline-block; background: #0066cc; color: #fff; border: none; border-radius: 6px; padding: 0.4em 1.1em; font-size: 0.88em; font-weight: 500; cursor: pointer; margin: 0.5em 0; }
.lc-button:hover { background: #0052a3; }
.lc-button[data-color="muted"]   { background: #9ca3af; }
.lc-button[data-color="danger"]  { background: #ef4444; }
.lc-button[data-color="success"] { background: #22c55e; }
.lc-dbx { font-size: 0.85em; color: #6b7280; border: 1px dashed #d1d5db; border-radius: 8px; padding: 6px 10px; margin: 6px 0 10px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.lc-dbx input { flex: 1 1 220px; font-family: monospace; font-size: 0.95em; padding: 4px 6px; border: 1px solid #cbd5e1; border-radius: 6px; }
.lc-dbx button { font-size: 0.9em; padding: 3px 10px; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; cursor: pointer; }
.lc-dbx .lc-dbx-ok { color: #166534; }
.lc-dbx .lc-dbx-err { color: #b91c1c; }
</style>

<script>
(function () {

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  window.lcDatasets = window.lcDatasets || {};
  window.lcDatasetListeners = window.lcDatasetListeners || {};

  /* ── async dataset registration ─────────────────── */
  if (!window.lcSetDataset) {
    window.lcSetDataset = function (id, data) {
      window.lcDatasets[id] = data;
      /* A LISTENER DIES WITH ITS PART. A pad re-renders its preview on every
         pause in typing; each new grid, chart or class added a listener and
         the replaced ones kept repainting off-screen — one more per pause, the
         freeze growing with it (Michel, 2026-10-16: "typing is slow"). A
         listener tagged with its element (_lcEl) is dropped once that element
         has left the page. */
      var L = window.lcDatasetListeners[id] || [];
      var live = L.filter(function (fn) {
        var e = fn._lcEl;
        if (!e) return true;
        if (e.isConnected) { fn._lcSeen = 1; return true; }
        return !fn._lcSeen;
      });
      if (live.length !== L.length) window.lcDatasetListeners[id] = live;
      live.forEach(function (fn) { try { fn(data); } catch (e) {} });
    };
  }
  /* what a class's grid says when a verb or an edit is refused: one line
     under every grid bound to that class, gone after a few seconds */
  window.lcGridSay = function (cls, msg) {
    document.querySelectorAll(".lc-datagrid[data-bind='" + cls + "']").forEach(function (g) {
      var s = g.querySelector(".lc-dg-say");
      if (!s) { s = document.createElement("div"); s.className = "lc-dg-say"; g.appendChild(s); }
      s.textContent = msg;
      clearTimeout(s._t);
      s._t = setTimeout(function () { if (s.parentNode) s.parentNode.removeChild(s); }, 4500);
    });
  };

  /* ONE MORE ROW (Michel, 2026-10-16: "an API where data is read but also
     written"). dataset.append(row) from Python lands here: the row shows at
     once; a list read from a sheet that takes writes (a key: link) also gets
     it POSTed — a simple request, so no preflight — then is read back, the
     sheet's truth replacing the guess. */
  window.lcRemote = window.lcRemote || {};
  window.lcIsDb = function (id) { var r = window.lcRemote[id]; return !!(r && r.db); };
  /* COLUMNS REACH THE TABLE WHEN IT IS SAFE (Michel, 2026-10-17, register P5):
     on load and on save already; and when the author saves the pad — never
     while typing, or "name" would leave n, na, nam behind */
  if (!window._lcEnsureOnSave) {
    window._lcEnsureOnSave = 1;
    document.addEventListener("lc-saved", function () {
      Object.keys(window.lcRemote).forEach(function (id) {
        var r = window.lcRemote[id], U = r && r.unl;
        if (!U || !U.rpc || !lsGet(U.akey)) return;
        window.lcRemoteReload(id, { ensure: true });
      });
    });
  }
  /* A LIST THAT LIVES ELSEWHERE IS READ AGAIN (Michel, 2026-10-16: "how to
     refresh the grid after a change made directly in the sheet?"): coming
     back to the page — from the sheet's tab — re-reads every such list once
     (not more often than every 5 s); its grid's ↻ re-reads it on demand;
     refresh="30" on the dataset re-reads it every 30 s. */
  window.lcRemoteReload = function (id, opts) {
    var r = window.lcRemote[id];
    if (!r) return false;
    r.at = performance.now();
    r.pull(opts);
    return true;
  };
  if (!window._lcRemoteVis) {
    window._lcRemoteVis = 1;
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState !== "visible") return;
      Object.keys(window.lcRemote).forEach(function (id) {
        var r = window.lcRemote[id];
        if (r && performance.now() - (r.at || 0) > 5000) window.lcRemoteReload(id);
      });
    });
  }
  /* a row as the table would hold it: no page-only fields, keys in order */
  function dbRow(r) {
    var o = {};
    Object.keys(r || {}).sort().forEach(function (k) { if (k !== "obj" && (k.charAt(0) !== "_" || k === "_sub") && k !== "⚠️") o[k] = r[k]; });
    return o;
  }
  /* empty is empty: the table's null and the page's "" are the same blank */
  function dbSame(r) {
    var o = dbRow(r);
    /* a text column holding an id ("2") and the page's 2 are the same value */
    for (var k in o) o[k] = (o[k] === null || o[k] === undefined) ? "" : (typeof o[k] === "number" ? String(o[k]) : o[k]);
    return o;
  }
  function dbKeyOf(r) { return JSON.stringify(dbSame(r)); }
  /* ONE .database, ANY SOURCE (Michel, 2026-10-17, register P3): the link's
     scheme says the kind — [the shelter](supabase://shelter)
     {: .database #shelter unlisted="…" } — and the page holds no key: the
     address and public key come from a databases.yml in the course folder
     (or above it), name → {url, key}, read once per folder. A model on it
     ({: .model source="shelter" }) gets a table per class; a lone dataset
     may name its table itself: [walks](supabase://shelter/walk). */
  window.lcDatabases = window.lcDatabases || {};
  /* the attribute that names a class's objects: its first text attribute */
  function refLabel(cls) {
    var m = (window.lcModels || {})[cls];
    if (!m) return "obj";
    var n = (m.order || Object.keys(m.fields || {})).filter(function (k) {
      var f = m.fields[k]; return f && f.t === "str" && !f.hidden && !f.state;
    })[0];
    return n || "obj";
  }
  window.lcRefLabel = refLabel;
  var _dbYml = {};
  function ghText(repo, path) {
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    var h = { Accept: "application/vnd.github.v3.raw" };
    if (pat) h.Authorization = "Bearer " + pat;
    return fetch("https://api.github.com/repos/" + repo + "/contents/" + path, { headers: h })
      .then(function (r) { return r.ok ? r.text() : null; }, function () { return null; });
  }
  function yamlOf(text) {
    return new Promise(function (res) {
      if (!text || !window.lcYaml) return res(null);
      window.lcYaml.ready(function () { try { res(window.lcYaml.load(text)); } catch (e) { res(null); } });
    });
  }
  function dbConf(name, el) {
    var roots = [el.closest("[data-lc-src-path]"), document.querySelector(".lc-run[data-lc-src-path]")];
    var tries = [];
    roots.forEach(function (r) {
      if (!r) return;
      var repo = r.getAttribute("data-lc-src-repo") || _lcSiteRepo;
      var parts = (r.getAttribute("data-lc-src-path") || "").split("/");
      parts.pop();
      for (;;) {
        var p = (parts.length ? parts.join("/") + "/" : "") + "databases.yml";
        if (!tries.some(function (t) { return t.repo === repo && t.path === p; })) tries.push({ repo: repo, path: p });
        if (!parts.length) break;
        parts.pop();
      }
    });
    return (function next(i) {
      if (i >= tries.length) return Promise.reject(new Error("no databases.yml names \"" + name + "\" — add it to the course folder"));
      var k = tries[i].repo + ":" + tries[i].path;
      var got = _dbYml[k] || (_dbYml[k] = ghText(tries[i].repo, tries[i].path).then(yamlOf));
      return got.then(function (y) {
        var c = y && y[name];
        if (!c) return next(i + 1);
        if (!c.url || !/^(https:\/\/|\/)/.test(c.url)) throw new Error("databases.yml: \"" + name + "\" has no https (or /proxy) url");
        return { url: String(c.url).replace(/\/+$/, ""), key: c.key || "" };
      });
    })(0);
  }
  function upgradeDatabase(el) {
    if (el.dataset.lcDbDone) return; el.dataset.lcDbDone = "1";
    var id = el.id || el.getAttribute("id");
    var a = el.querySelector("a[href]");
    var m = /^(\w+):\/\/([\w-]+)/.exec(a ? a.getAttribute("href") || "" : "");
    if (!id) return;
    el.classList.add("lc-database");
    el.hidden = true;
    window.lcDatabases[id] = { el: el, kind: m ? m[1] : "", name: m ? m[2] : "",
                               unlisted: el.getAttribute("unlisted") || "", title: a ? (a.textContent || "").trim() : id };
    /* THE LINE CHANGED, ITS TABLES FOLLOW (Michel, 2026-10-17: "did that,
       but the grid is dirty with the key!"): a pad redraws only the block
       that changed — the class's tables were read with the old line. Each
       table of this database whose name differs is read again with the new. */
    var nm = el.getAttribute("unlisted") || "true";
    document.querySelectorAll("p.lc-db-table[data-db='" + id + "']").forEach(function (p) {
      if ((p.getAttribute("unlisted") || "true") === nm) return;
      var pa = p.querySelector("a");
      if (pa) pa.setAttribute("href", "db://" + id + "/" + p.getAttribute("data-tbl"));
      p.removeAttribute("unlisted");
      delete p.dataset.lcDsDone;
      upgradeDataset(p);
    });
    document.dispatchEvent(new CustomEvent("lc-database", { detail: id }));
  }
  /* a class's table on a database: a hidden dataset beside the model, named
     <database>_<table>, read and written like any table of that database */
  window.lcDatabaseTable = function (dbId, table, near) {
    var dsid = dbId + "_" + table;
    var ex = document.getElementById(dsid);
    if (ex && ex.isConnected) return dsid;
    /* ONE LINK PER TABLE PER VISIT (Michel, 2026-10-17: "rows are twice!"):
       a pad redraws the class block on every pause; a rebuilt link sent a
       walk still being saved a second, a third time. The same link is put
       back where the class now stands, its save in flight and all. */
    var keep = (window._lcDbTableEls = window._lcDbTableEls || {})[dsid];
    if (keep) {
      if (near && near.parentNode) near.parentNode.insertBefore(keep, near.nextSibling); else document.body.appendChild(keep);
      return dsid;
    }
    var p = document.createElement("p");
    p.className = "dataset lc-db-table"; p.id = dsid; p.hidden = true;
    p.setAttribute("data-db", dbId); p.setAttribute("data-tbl", table);
    var a = document.createElement("a");
    a.setAttribute("href", "db://" + dbId + "/" + table);
    a.textContent = table;
    p.appendChild(a);
    if (near && near.parentNode) near.parentNode.insertBefore(p, near.nextSibling); else document.body.appendChild(p);
    window._lcDbTableEls[dsid] = p;
    upgradeDataset(p);
    return dsid;
  };
  function dbWhen(dbId, tries) {
    return new Promise(function (res, rej) {
      (function look(n) {
        var d = window.lcDatabases[dbId];
        if (d) return res(d);
        if (n <= 0) return rej(new Error("no database #" + dbId + " on this page"));
        setTimeout(function () { look(n - 1); }, 100);
      })(tries);
    });
  }

  /* AN UNLISTED TABLE — the device's two secrets: the author key (makes
     tables) and each list's unlisted name (reads and writes it) */
  function lsGet(k) { try { return localStorage.getItem(k) || ""; } catch (e) { return ""; } }
  function lsSet(k, v) { try { if (v) localStorage.setItem(k, v); else localStorage.removeItem(k); } catch (e) {} }
  /* the columns a list's class declares, in its order, for the table it
     makes: str, int, float, bool (a state is a str) — the columns the table
     brought are not the class's to make */
  function unlCols(id) {
    var M = window.lcModels || {}, out = null;
    Object.keys(M).forEach(function (n) {
      var m = M[n];
      if (!m || m.src !== id) return;
      out = out || [];
      (m.order || Object.keys(m.fields || {})).forEach(function (f) {
        var d = (m.fields || {})[f];
        if (!d || d.src || d.computed || f === "id" || f.charAt(0) === "_" || !/^[a-z][a-z0-9_]{0,40}$/.test(f)) return;
        if (!out.some(function (c) { return c.n === f; })) {
          var col = { n: f, t: d.state ? "str" : (d.t || "str") };
          if (d.was) col.was = d.was;
          out.push(col);
        }
      });
      /* a class with subclasses keeps, per row, which one it is */
      if ((m.subs || []).length && !out.some(function (c) { return c.n === "_sub"; })) out.push({ n: "_sub", t: "str" });
    });
    return out;
  }
  /* the class may not be read yet when the list is: wait for it a little */
  function unlColsSoon(id, tries) {
    return new Promise(function (res) {
      (function look(n) {
        var c = unlCols(id);
        if ((c && c.length) || n <= 0) return res(c);   /* a class not yet run has no attributes to send */
        setTimeout(function () { look(n - 1); }, 250);
      })(tries);
    });
  }
  /* what changed since the table was read: new rows (no id yet), changed
     rows, rows that are gone */
  window.lcDatasetChanges = function (id) {
    var r = window.lcRemote[id], arr = window.lcDatasets[id];
    if (!r || !r.db || !Array.isArray(arr)) return null;
    var snap = r.snap || {}, seen = {}, ins = [], upd = [];
    /* only the columns the table has: an attribute still being typed is not
       a change to send (it reaches the table with ↻ or 🧹) */
    var keep = r.unl && r.unl.tcols && Object.keys(r.unl.tcols).length ? r.unl.tcols : null;
    var cut = function (o) { if (!keep) return o; var x = {}; for (var k in o) if (keep[k]) x[k] = o[k]; return x; };
    var keyOf = function (row) { return JSON.stringify(dbSame(cut(dbRow(row)))); };
    arr.forEach(function (row) {
      if (row["⚠️"]) return;
      if (row.id == null || row.id === "") {
        /* new — no id yet: the table gives one */
        var c = cut(dbRow(row)); delete c.id; ins.push(c); return;
      }
      /* a row with an id came from the table: never inserted again, even
         when this page's picture of the table is not read yet (Michel,
         2026-10-17: "rows are twice!" — a fresh link's empty picture made
         every row look new) */
      if (!(String(row.id) in snap)) return;
      seen[String(row.id)] = 1;
      if (snap[String(row.id)] !== keyOf(row)) upd.push(cut(dbRow(row)));
    });
    var del = Object.keys(snap).filter(function (k) { return !seen[k]; });
    return { ins: ins, upd: upd, del: del, n: ins.length + upd.length + del.length };
  };
  /* 💾 SAVE: the new rows in one insert, each changed row by its id, the
     gone ones by theirs — then the table is read again, its truth (ids,
     defaults) replacing the page's guess */
  window.lcDatasetSave = function (id) {
    var r = window.lcRemote[id], ch = window.lcDatasetChanges(id);
    if (!r || !ch) return Promise.resolve(null);
    /* a blank cell is the table's null (Michel, 2026-10-17: a new Sprint with
       its speed still blank sent "" to a number column — refused, and the
       Walk saved with it failed too) */
    var blank = function (row) { var o = {}; for (var k in row) o[k] = row[k] === "" ? null : row[k]; return o; };
    ch = { n: ch.n, ins: ch.ins.map(blank), upd: ch.upd.map(blank), del: ch.del };
    if (r.unl) {
      var u = r.unl, author = lsGet(u.akey);
      if (!u.share) return Promise.reject(new Error("paste the list's unlisted name first"));
      /* a save never changes the table's columns (Michel, 2026-10-17: typing
         "speed" left s, sp, spe… behind): ↻, 🧹 and the pad's save do */
      return u.rpc("lc_save", { share: u.share, tbl: u.tbl, ins: ch.ins, upd: ch.upd, del: ch.del.map(Number) })
        .then(function () { r.pull(); return ch; });
    }
    var H = r.db.headers({ "Content-Type": "application/json", Prefer: "return=minimal" });
    var ok = function (x) { if (!x.ok) return x.text().then(function (t) { throw new Error("HTTP " + x.status + " " + t.slice(0, 160)); }); return x; };
    var calls = [];
    if (ch.ins.length) calls.push(fetch(r.db.base, { method: "POST", headers: H, body: JSON.stringify(ch.ins) }).then(ok));
    ch.upd.forEach(function (row) {
      var body = {}; for (var k in row) if (k !== "id") body[k] = row[k];
      calls.push(fetch(r.db.base + "?id=eq." + encodeURIComponent(row.id), { method: "PATCH", headers: H, body: JSON.stringify(body) }).then(ok));
    });
    if (ch.del.length) calls.push(fetch(r.db.base + "?id=in.(" + ch.del.map(encodeURIComponent).join(",") + ")", { method: "DELETE", headers: H }).then(ok));
    return Promise.all(calls).then(function () { r.pull(); return ch; });
  };
  window.lcDatasetAppend = function (id, rowJson) {
    var row = typeof rowJson === "string" ? JSON.parse(rowJson) : rowJson;
    var arr = Array.isArray(window.lcDatasets[id]) ? window.lcDatasets[id].filter(function (r) { return !r["⚠️"]; }) : [];
    arr.push(row);
    window.lcSetDataset(id, arr);
    var r = window.lcRemote[id];
    if (!r || !r.write) return;
    fetch(r.href, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" },
                    body: JSON.stringify({ append: row }) })
      .then(function () { setTimeout(r.pull, 1200); })
      .catch(function (e) {
        if (window.lcGridSay) window.lcGridSay(id, "⚠️ the sheet did not take the row: " + e.message);
      });
  };
  /* A LINK THAT IS A KEY. [the walk sheet](key:walk_sheet) — the address of a
     sheet that takes writes is a key: it lives on the device, never in the
     page or the repo (the keys-in-browser ruling). Missing, the page asks
     for it once, in a small field under where the list would be. */
  function linkKey(name) { try { return localStorage.getItem("lc_link_" + name) || ""; } catch (e) { return ""; } }
  function askLink(el, id, name, label) {
    var box = document.createElement("div");
    box.className = "lc-ds-key";
    box.setAttribute("data-lc-key", name);
    box.innerHTML = "<span>🔑 " + (label || name).replace(/</g, "&lt;") + " — paste its link (kept on this device only)</span>"
      + "<input type='url' placeholder='https://…' aria-label='the link of " + (label || name).replace(/'/g, "") + "'>"
      + "<button type='button'>Connect</button>";
    el.parentNode.insertBefore(box, el.nextSibling);
    var inp = box.querySelector("input"), go = box.querySelector("button");
    var done = function () {
      var v = (inp.value || "").trim();
      if (!/^https:\/\//.test(v)) { inp.focus(); return; }
      try { localStorage.setItem("lc_link_" + name, v); } catch (e) {}
      box.parentNode.removeChild(box);
      delete el.dataset.lcDsDone;
      upgradeDataset(el);
    };
    go.addEventListener("click", done);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); done(); } });
    window.lcSetDataset(id, []);
  }

  /* ── CSV parser ─────────────────────────────────── */
  function parseCSV(text) {
    var lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return [];
    var headers = splitCSVRow(lines[0]);
    return lines.slice(1).filter(function (l) { return l.trim(); }).map(function (l) {
      var vals = splitCSVRow(l);
      var row = {};
      headers.forEach(function (h, i) {
        var v = vals[i] !== undefined ? vals[i] : "";
        row[h] = v !== "" && !isNaN(v) ? +v : v;
      });
      return row;
    });
  }
  function splitCSVRow(line) {
    var out = [], cur = "", inQ = false;
    for (var i = 0; i < line.length; i++) {
      var ch = line[i];
      if (ch === '"') { inQ = !inQ; }
      else if (ch === ',' && !inQ) { out.push(cur.trim()); cur = ""; }
      else cur += ch;
    }
    out.push(cur.trim());
    return out;
  }

  /* extract a nested array (path="a.b") and turn an object-of-equal-length-
     arrays (e.g. Open-Meteo's daily/hourly) into rows — so live APIs that nest
     or columnarise their data still bind to grids and charts. */
  function shapeData(data, el) {
    var path = el.getAttribute("path");
    if (path) {
      path.split(".").forEach(function (k) {
        if (data && typeof data === "object" && data[k] != null) data = data[k];
      });
    }
    if (data && !Array.isArray(data) && typeof data === "object") {
      var keys = Object.keys(data);
      if (keys.length && keys.every(function (k) { return Array.isArray(data[k]); })) {
        var n = data[keys[0]].length;
        if (keys.every(function (k) { return data[k].length === n; })) {
          var rows = [];
          for (var i = 0; i < n; i++) {
            var row = {};
            keys.forEach(function (k) { row[k] = data[k][i]; });
            rows.push(row);
          }
          return rows;
        }
      }
    }
    if (Array.isArray(data)) return data;
    if (data && typeof data === "object") return data;   // a plain object (e.g. a schema index) is kept as-is, not wrapped
    return [data];
  }

  /* parse inline/remote text as JSON, YAML (format="yaml"), or CSV, then register */
  function setFromText(text, fmt, el, id) {
    if ((fmt === "yaml" || fmt === "yml") && window.lcYaml) {
      window.lcYaml.ready(function () {
        var data; try { data = window.lcYaml.load(text); } catch (e) { data = [{ "⚠️": "YAML: " + e.message }]; }
        window.lcSetDataset(id, shapeData(data, el));
      });
      return;
    }
    var data;
    try { data = JSON.parse(text); } catch (e) { data = parseCSV(text); }
    window.lcSetDataset(id, shapeData(data, el));
  }

  /* ── .dataset upgrade ───────────────────────────── */
  function upgradeDataset(el) {
    if (el.dataset.lcDsDone) return; el.dataset.lcDsDone = "1";
    /* of="SomeModel": the rows are ADOPTED by a model class — same fence,
       one grammar (Michel, 2026-08-22: "KISS that"). The model machinery
       owns the hydration; retry briefly if its include has not parsed yet. */
    if (el.getAttribute("of")) {
      (function adopt(tries) {
        if (window.lcAdoptRows) { delete el.dataset.lcRowsDone; window.lcAdoptRows(el); return; }
        if (tries < 50) setTimeout(function () { adopt(tries + 1); }, 200);
      })(0);
      return;
    }
    var id = el.id || el.getAttribute("id");
    if (!id) return;

    /* remote variant: apply {: .dataset #x } to a link → fetch its href */
    var link = el.querySelector("a[href]");
    if (link) {
      var href = link.getAttribute("href");
      /* forgiving: authors often write the URL as the visible link text
         with a dummy "#" href — use the text when it looks like a URL */
      if (!/^(https?:\/\/|\/)/.test(href) && /^https?:\/\//.test((link.textContent || "").trim())) {
        href = link.textContent.trim();
      }
      /* a table of a .database (db://<database>/<table>, made for a model's
         class) or a lone dataset naming its database (supabase://<name>/<table>):
         the address and key arrive from databases.yml, then the link is a
         table like any other */
      var dbm = /^db:\/\/([\w-]+)\/([\w-]+)$/.exec(href), sbm = /^supabase:\/\/([\w-]+)\/([\w-]+)$/.exec(href);
      if (dbm || sbm) {
        (dbm ? dbWhen(dbm[1], 50) : Promise.resolve({ kind: "supabase", name: sbm[1], unlisted: el.getAttribute("unlisted") || "" }))
          .then(function (d) {
            if (d.kind !== "supabase") throw new Error("a " + (d.kind || "?") + ":// database holds no tables here yet");
            return dbConf(d.name, el).then(function (c) {
              link.setAttribute("href", c.url + "/rest/v1/" + (dbm ? dbm[2] : sbm[2]));
              if (c.key) el.setAttribute("apikey", c.key);
              el.setAttribute("unlisted", d.unlisted || "true");
              if (dbm) el.setAttribute("data-db", dbm[1]);
              delete el.dataset.lcDsDone;
              upgradeDataset(el);
            });
          })
          .catch(function (e) { window.lcSetDataset(id, [{ "⚠️": e.message }]); });
        return;
      }
      var keyName = (/^key:([A-Za-z_][\w-]*)$/.exec(href) || [])[1] || "";
      if (keyName) {
        href = linkKey(keyName);
        if (!href) { askLink(el, id, keyName, (link.textContent || "").trim()); return; }
      }
      /* A GOOGLE SHEET'S OWN LINK READS AS ROWS (Michel, 2026-10-16: the grid
         stayed empty on a …/edit?usp=sharing link — that address sends the
         editor's web page, which a page may not read). Its CSV door does,
         for a sheet shared "anyone with the link can view"; #gid= keeps the tab. */
      var gsh = /^https:\/\/docs\.google\.com\/spreadsheets\/d\/([\w-]+)/.exec(href);
      if (gsh && !/\/gviz\/|\/export|output=csv|\/pub/.test(href)) {
        var gid = (/[#&?]gid=(\d+)/.exec(href) || [])[1];
        href = "https://docs.google.com/spreadsheets/d/" + gsh[1] + "/gviz/tq?tqx=out:csv" + (gid ? "&gid=" + gid : "");
      }
      /* sheet="Sheet1" — WHICH TAB (Michel, 2026-10-16: "why don't you use the
         Sheet1 name anywhere?"): a sheet with no tab named sends its first
         one; sheet= names it, for the CSV door and for the sheet's script
         (both read ?sheet=, the script writes there too) */
      var tab = el.getAttribute("sheet");
      if (tab && /^https:\/\//.test(href) && !/[?&]sheet=/.test(href))
        href += (href.indexOf("?") < 0 ? "?" : "&") + "sheet=" + encodeURIComponent(tab);
      if (/^(https?:\/\/|\/)/.test(href)) {
        var fmt = (el.getAttribute("format") || "").toLowerCase();
        if (!fmt && /\.ya?ml($|\?)/i.test(href)) fmt = "yaml";
        var tick = 0;
        /* A DATABASE TABLE (Michel, 2026-10-17: "I create the db myself, the
           class reads it, students add objects, then save and refresh"):
           a Supabase table's address, …supabase.co/rest/v1/<table>, with the
           project's public key in apikey="…" — read here, written by
           💾 Save (lcDatasetSave), only what changed since this read */
        var dbKey = el.getAttribute("apikey") || "";
        var isDb = /\.supabase\.co\/rest\/v1\/[\w-]+/.test(href);
        var dbHeaders = function (extra) {
          var h = { Accept: "application/json" };
          if (dbKey) { h.apikey = dbKey; if (/^eyJ/.test(dbKey)) h.Authorization = "Bearer " + dbKey; }
          for (var k in (extra || {})) h[k] = extra[k];
          return h;
        };
        /* AN UNLISTED TABLE (Michel, 2026-10-17: "my class creates the table
           if not exists, even with a token in my browser, while others read
           or write just by sharing a special unlisted name"): unlisted="true".
           The tables sit in the database's private schema, no rule opens
           them; four functions are the only door (the setup SQL, pasted once).
           The author's device holds the author key: its class makes the table
           and adds the columns it gains, and the table's unlisted name shows
           under the grid, to share. Everyone else pastes that name once. Both
           stay on the device, never in the page. */
        var unl = isDb && !!el.getAttribute("unlisted");
        /* unlisted="<name>": the name is in the page, everyone reads and writes
           with it, nothing to paste (Michel, 2026-10-17); "true": pasted once */
        var unlFixed = unl && el.getAttribute("unlisted") !== "true" ? el.getAttribute("unlisted") : "";
        var unlPull = null;
        if (unl) {
          var uProj = (/^https:\/\/([\w-]+)\./.exec(href) || [])[1] || "";
          var uTbl = (/\/rest\/v1\/([\w-]+)/.exec(href) || [])[1] || "";
          var uBase = href.split("/rest/v1/")[0] + "/rest/v1";
          var U = { tbl: uTbl, akey: "lc_author_" + uProj, skey: "lc_unlisted_" + uProj + "_" + uTbl,
                    share: "", author: false, need: false, newKey: "", fixed: unlFixed, hint: "",
                    db: el.getAttribute("data-db") || "" };
          U.rpc = function (fn, body) {
            return fetch(uBase + "/rpc/" + fn, { method: "POST", cache: "no-store",
                                                 headers: dbHeaders({ "Content-Type": "application/json" }), body: JSON.stringify(body) })
              .then(function (x) {
                return x.text().then(function (t) {
                  var j = null; try { j = JSON.parse(t); } catch (e) {}
                  if (x.ok) return j;
                  if (x.status === 404) throw new Error("this database has no Lightcode setup yet — run the setup SQL once");
                  if (x.status === 401 || x.status === 403) throw new Error("the database refused the key — check apikey=\"…\"");
                  throw new Error(((j && j.message) || ("HTTP " + x.status)).replace(/^lc: /, ""));
                });
              });
          };
          unlPull = function (opts) {
            var r = window.lcRemote[id], author = lsGet(U.akey);
            /* the table's columns change on the first read and when asked
               (↻, 🧹, the pad's save) — never on a save or a re-read */
            /* "first" is per visit, not per drawing: a pad redraws the class
               block on every pause and rebuilds its table's link */
            var seen = window._lcTblSeen = window._lcTblSeen || {};
            if (!U.tcols && seen[id]) U.tcols = seen[id];
            var ensure = author && (!seen[id] || (opts && opts.ensure));
            var step = ensure
              ? unlColsSoon(id, 40).then(function (cols) {
                  /* a database set up before _sub refuses it: the rest of the class still goes in */
                  return U.rpc("lc_ensure", { token: author, tbl: U.tbl, cols: cols || [] })
                    .catch(function (e) {
                      if (!/"_sub"/.test(e.message || "")) throw e;
                      cols = (cols || []).filter(function (c) { return c.n !== "_sub"; });
                      return U.rpc("lc_ensure", { token: author, tbl: U.tbl, cols: cols });
                    })
                    .then(function (sh) {
                      U.tcols = { id: 1 };
                      (cols || []).forEach(function (c) { U.tcols[c.n] = 1; });
                      seen[id] = U.tcols;
                      U.author = true;
                      /* the page's name is not the database's: the author is told the right one */
                      U.hint = sh && sh !== U.fixed ? sh : "";
                      if (sh && !U.fixed) lsSet(U.skey, sh);
                      return sh;
                    });
                })
              : Promise.resolve(U.fixed || lsGet(U.skey) || U.share);
            if (author && !ensure) U.author = true;
            return step.then(function (sh) {
              U.share = sh || "";
              U.need = !sh && !U.fixed;
              if (!sh) { r.snap = {}; r.error = ""; window.lcSetDataset(id, []); return; }
              return U.rpc("lc_read", { share: sh, tbl: U.tbl }).then(function (rows) {
                rows = Array.isArray(rows) ? rows : [];
                var snap = {};
                U.read = true;
                U.tcols = U.tcols || {};
                seen[id] = U.tcols;
                rows.forEach(function (x) { if (x) Object.keys(x).forEach(function (k) { U.tcols[k] = 1; }); });
                var keep = Object.keys(U.tcols).length ? U.tcols : null;
                rows.forEach(function (x) {
                  if (!x || x.id == null) return;
                  var o = dbRow(x), y = {};
                  for (var k in o) if (!keep || keep[k]) y[k] = o[k];
                  snap[String(x.id)] = JSON.stringify(dbSame(y));
                });
                r.snap = snap; r.error = "";
                window.lcSetDataset(id, shapeData(rows, el));
                /* same rows, other state (a name now known, a hint gone): the grids repaint */
                document.dispatchEvent(new CustomEvent("lc-remote-state", { detail: id }));
              });
            }).catch(function (e) {
              if (/no list by that name/.test(e.message || "")) U.need = true;
              fail(e);
            });
          };
        }
        var pull = function (opts) {
          if (unlPull) return unlPull(opts);
          /* cache-bust so a just-landed file (results, fleet) is seen now,
             not from the 60s API/Pages cache — this is the whole point of
             refresh= (a counter, since Date is engine-blocked); a database
             reads every column it is not told to filter, so no _t there */
          (isDb ? fetch(href + (href.indexOf("?") < 0 ? "?select=*&order=id" : ""), { cache: "no-store", headers: dbHeaders() })
                : fetch(href + (href.indexOf("?") < 0 ? "?" : "&") + "_t=" + (tick++), { cache: "no-store" }))
            .then(function (r) {
              /* 404 is not a fault — it means this node carries no such data.
                 The fleet board and the backlog are lab-only instruments the
                 gate never publishes, so on pedia they are simply absent, and
                 the page already promises "an empty board". Showing ⚠️ HTTP 404
                 turned a by-design absence into what looks like a broken site.
                 Every other status stays an error, because those ARE faults. */
              if (r.status === 404 && !isDb) { window.lcSetDataset(id, []); return null; }
              if (!r.ok) {
                if (isDb && (r.status === 401 || r.status === 403)) throw new Error("the table refused the key (HTTP " + r.status + ") — check apikey=\"…\" and the table's read rule");
                if (isDb && r.status === 404) throw new Error("no such table (HTTP 404) — check the name after /rest/v1/");
                throw new Error("HTTP " + r.status);
              }
              return r.text();
            })
            .then(function (text) {
              if (text === null) return;
              /* a web page is not rows: say so, instead of an empty table */
              if (/^\s*<(!doctype|html|head|body)/i.test(text))
                throw new Error("this link sends a web page, not rows — use the sheet's data link");
              if (isDb) {
                /* what the table held when read: 💾 Save sends the difference */
                var rows0 = []; try { rows0 = JSON.parse(text); } catch (e) {}
                var snap = {};
                (Array.isArray(rows0) ? rows0 : []).forEach(function (r) { if (r && r.id != null) snap[String(r.id)] = dbKeyOf(r); });
                window.lcRemote[id].snap = snap;
              }
              setFromText(text, fmt, el, id);
            })
            .catch(fail);
        };
        var fail = function (e) {
              var cur = window.lcDatasets[id];
              /* Chrome says "Failed to fetch", Safari "Load failed", Firefox
                 "NetworkError…": the same refusal, said one way */
              var refused = e instanceof TypeError || /failed to fetch|load failed|networkerror/i.test(e.message || "");
              var why = refused
                ? (isDb ? "the database cannot be reached — check its address (…supabase.co/rest/v1/<table>)"
                        : "this link cannot be read from a page (not shared, or not a data link)")
                : e.message;
              if (isDb && window.lcRemote[id]) window.lcRemote[id].error = why;
              if (!cur || !cur.length) window.lcSetDataset(id, [{ "⚠️": why }]);
              else if (unl) window.lcSetDataset(id, cur);   /* the grid says why, under the rows */
        };
        window.lcRemote[id] = { href: href, pull: pull, write: !!keyName || el.getAttribute("write") === "true", at: performance.now(),
                                db: isDb ? { base: href.split("?")[0], headers: dbHeaders } : null, snap: {}, unl: unl ? U : null };
        pull();
        /* refresh="30" → live mode: re-pull every N seconds. Republishing to
           the bus repaints every bound grid/stat/chart with no page reload —
           the generic auto-refresh, not a dashboard special-case. */
        var every = parseInt(el.getAttribute("refresh") || "0", 10);
        if (every > 0) setInterval(pull, Math.max(10, every) * 1000);
        return;
      }
      /* RELATIVE LINK — a pile that LIVES IN A FILE (Michel, 2026-10-03:
         "why is there a yaml if we use the dogs yaml file?"). The fence was
         a second truth for the same rows, so a dataset can now be declared
         by its file alone: [dogs](../module_00/dogs.yaml) + {: .dataset #dogs }.
         The learner's bench copy wins when there is one; otherwise the
         lesson's own copy, read from the course repo beside the page. */
      if (href && href !== "#") {
        var rfmt = (el.getAttribute("format") || "").toLowerCase();
        if (window.lcInferFormat) rfmt = window.lcInferFormat(href, rfmt);
        var fromSource = function () {
          var srcEl = el.closest ? el.closest("[data-lc-src-path]") : null;
          if (!srcEl) srcEl = document.querySelector(".lc-run[data-lc-src-path]");
          var srcPath = srcEl ? (srcEl.getAttribute("data-lc-src-path") || "") : "";
          var dir = srcPath.indexOf("/") >= 0 ? srcPath.replace(/\/[^\/]*$/, "") : "";
          var parts = [];
          (dir ? dir + "/" + href : href).split("/").forEach(function (p) {
            if (!p || p === ".") return;
            if (p === "..") parts.pop(); else parts.push(p);
          });
          var repo = (srcEl && srcEl.getAttribute("data-lc-src-repo")) || _lcSiteRepo;
          var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
          var h = { Accept: "application/vnd.github.v3.raw" };
          if (pat) h.Authorization = "Bearer " + pat;
          return fetch("https://api.github.com/repos/" + repo + "/contents/" + parts.join("/"), { headers: h })
            .then(function (r) {
              if (r.status === 404) return null;
              if (!r.ok) throw new Error("HTTP " + r.status);
              return r.text();
            });
        };
        var bench = window.lcBench
          ? window.lcBench.read(href, el).then(function (f) { return f ? f.text : null; })
          : Promise.resolve(null);
        bench.catch(function () { return null; })
          .then(function (text) {
            if (text !== null) { el.setAttribute("data-lc-mine", "1"); return text; }
            return fromSource();
          })
          .then(function (text) {
            if (text === null) { window.lcSetDataset(id, []); return; }
            setFromText(text, rfmt, el, id);
          })
          .catch(function (e) { if (!window.lcDatasets[id]) window.lcSetDataset(id, [{ "⚠️": e.message }]); });
        return;
      }
    }

    /* Databricks variant: the fence is SQL, dbx="<warehouse id>" names the
       warehouse. The statement goes through a same-origin proxy (host=,
       default /dbx) that forwards the browser's OWN token and stores nothing
       — the key lives on this device like every other key here, and no
       server ever holds it (Michel, 2026-09-26: "the perfect match with
       the CFO's need to not share strategic data with anyone else"). */
    if (el.getAttribute("dbx")) { dbxDataset(el, id); return; }
    /* A SQL FENCE ON A .database (Michel, 2026-10-17, register P3): the fence
       holds the statement, source="warehouse" says where it runs, the
       database's scheme says how — databricks://<name>/<warehouse id>; its
       proxy root comes from databases.yml (url: /dbx by default) */
    if (el.getAttribute("source")) {
      dbWhen(el.getAttribute("source"), 50).then(function (d) {
        var m = /^databricks:\/\/[\w.-]+\/([\w-]+)/.exec((d.el.querySelector("a[href]") || { getAttribute: function () { return ""; } }).getAttribute("href") || "");
        if (d.kind !== "databricks" || !m) throw new Error("a SQL fence runs on a databricks://<name>/<warehouse> database — #" + el.getAttribute("source") + " is " + (d.kind || "?") + "://");
        return dbConf(d.name, el).catch(function () { return { url: "/dbx" }; }).then(function (c) {
          el.setAttribute("dbx", m[1]);
          el.setAttribute("host", c.url || "/dbx");
          dbxDataset(el, id);
        });
      }).catch(function (e) { window.lcSetDataset(id, [{ "⚠️": e.message }]); });
      return;
    }

    /* inline code block variant */
    var code = el.querySelector("code") || el;
    var seed = code.textContent.trim();
    var fmt = (el.getAttribute("format") || window.lcFenceFormat(el) || "").toLowerCase();

    /* save="…" — the same contract every other component with a save= knob
       already follows: the fence is the AUTHOR'S seed, the learner's file is
       the truth. A dataset could not read a bench until now, so a lesson had
       no way to feed today's screen from the file the reader repaired
       yesterday — and "watch your own fix land somewhere new" is the whole
       reason the second lesson is worth sitting through.
       Seed FIRST, then replace: a bench read is a network round trip and a
       page that starts blank teaches nothing while it waits. lcSetDataset
       notifies every listener, so the swap re-derives each bound view. */
    var savePath = el.getAttribute("save") || "";
    if (savePath && window.lcBench) {
      setFromText(seed, fmt, el, id);
      window.lcBench.read(savePath, el).then(function (f) {
        if (!f) return;
        el.setAttribute("data-lc-mine", "1");
        setFromText(f.text, window.lcInferFormat
          ? window.lcInferFormat(savePath, fmt) : fmt, el, id);
      }).catch(function () {});
      return;
    }
    setFromText(seed, fmt, el, id);
  }

  /* ── Databricks: a SQL statement on a warehouse, with this device's token ── */
  var DBX_KEY = "lc_key_dbx";
  function dbxToken() { try { return localStorage.getItem(DBX_KEY) || ""; } catch (e) { return ""; } }
  function dbxKeep(v) { try { if (v) localStorage.setItem(DBX_KEY, v); else localStorage.removeItem(DBX_KEY); } catch (e) {} }
  var DBX_NUM = /^(INT|LONG|SHORT|BYTE|FLOAT|DOUBLE|DECIMAL)/i;
  function dbxDataset(el, id) {
    var code = el.querySelector("code") || el;
    var sql = code.textContent.trim();
    var wh = el.getAttribute("dbx");
    var host = (el.getAttribute("host") || "/dbx").replace(/\/$/, "");
    var every = parseInt(el.getAttribute("refresh") || "0", 10);
    /* the fence is invisible, as every dataset is; the bar beside it is
       where the token is pasted once and where the run reports */
    var bar = document.createElement("div");
    bar.className = "lc-dbx"; bar.setAttribute("data-lc-dbx", id);
    bar.innerHTML = '<span class="lc-dbx-status"></span>' +
      '<input type="password" class="lc-dbx-token" placeholder="Databricks token — stays in this browser" aria-label="Databricks token" hidden>' +
      '<button type="button" class="lc-dbx-save" hidden>Save</button>' +
      '<button type="button" class="lc-dbx-change">🔑 token</button>';
    el.parentNode.insertBefore(bar, el.nextSibling);
    var status = bar.querySelector(".lc-dbx-status"), input = bar.querySelector(".lc-dbx-token"),
        save = bar.querySelector(".lc-dbx-save"), change = bar.querySelector(".lc-dbx-change");
    function say(t, cls) { status.textContent = t; status.className = "lc-dbx-status" + (cls ? " " + cls : ""); }
    function ask(open) { input.hidden = save.hidden = !open; if (open) input.focus(); }
    change.addEventListener("click", function () { ask(input.hidden); });
    save.addEventListener("click", function () { dbxKeep(input.value.trim()); input.value = ""; ask(false); run(); });
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") save.click(); });
    function headers(tok) { return { Authorization: "Bearer " + tok, "Content-Type": "application/json", Accept: "application/json" }; }
    function asJson(r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); }
    function run() {
      var tok = dbxToken();
      if (!tok) { window.lcSetDataset(id, []); say("🔑 paste your Databricks token to run this query", "lc-dbx-err"); ask(true); return; }
      say("⏳ running on warehouse " + wh + "…");
      var H = headers(tok);
      fetch(host + "/api/2.0/sql/statements", { method: "POST", headers: H, cache: "no-store",
        body: JSON.stringify({ warehouse_id: wh, statement: sql, wait_timeout: "30s", disposition: "INLINE", format: "JSON_ARRAY" }) })
        .then(asJson)
        .then(function step(d) {
          if (!d.ok) throw new Error(d.status === 401 || d.status === 403 ? "token refused — paste a fresh one" : ("HTTP " + d.status + (d.j && d.j.message ? " — " + d.j.message : "")));
          var st = d.j.status && d.j.status.state;
          if (st === "PENDING" || st === "RUNNING")
            return new Promise(function (res) { setTimeout(res, 1000); })
              .then(function () { return fetch(host + "/api/2.0/sql/statements/" + d.j.statement_id, { headers: H, cache: "no-store" }); })
              .then(asJson).then(step);
          if (st !== "SUCCEEDED") throw new Error((d.j.status && d.j.status.error && d.j.status.error.message) || ("statement " + (st || "failed")));
          var cols = ((d.j.manifest || {}).schema || {}).columns || [];
          var rows = [];
          var take = function (arr) {
            (arr || []).forEach(function (a) {
              var o = {};
              cols.forEach(function (c, i) {
                var v = a[i];
                o[c.name] = (v !== null && v !== undefined && DBX_NUM.test(c.type_name || "") && v !== "" && !isNaN(v)) ? Number(v) : v;
              });
              rows.push(o);
            });
          };
          take((d.j.result || {}).data_array);
          /* a large result comes in chunks — follow them to the end */
          var more = function (link) {
            if (!link) return rows;
            return fetch(host + link, { headers: H, cache: "no-store" }).then(asJson).then(function (c) {
              if (!c.ok) throw new Error("HTTP " + c.status + " on a result chunk");
              take(c.j.data_array); return more(c.j.next_chunk_internal_link);
            });
          };
          return more((d.j.result || {}).next_chunk_internal_link);
        })
        .then(function (rows) { window.lcSetDataset(id, rows); say("✓ " + rows.length + " row" + (rows.length === 1 ? "" : "s") + " from warehouse " + wh, "lc-dbx-ok"); })
        .catch(function (e) { window.lcSetDataset(id, [{ "⚠️": e.message }]); say("⚠️ " + e.message, "lc-dbx-err"); });
    }
    run();
    if (every > 0) setInterval(run, Math.max(10, every) * 1000);
  }

  /* ── .datagrid upgrade ──────────────────────────── */
  function upgradeDatagridBound(el) {
    if (el.dataset.lcDgDone || el.dataset.lcUpgraded) return;
    var bindId = el.getAttribute("source") || el.getAttribute("bind");
    if (!bindId) return; /* skip old-style code-block datagrids */
    /* source="file:path" loads a repo file (read format now — el is replaced below) */
    var fileRef = bindId.indexOf("file:") === 0 ? bindId.slice(5).trim() : "";
    var fileFmt = fileRef && window.lcInferFormat ? window.lcInferFormat(fileRef, el.getAttribute("format")) : "yaml";
    el.dataset.lcDgDone = "1";
    var perPage = parseInt(el.getAttribute("rows") || "0", 10) || 0;
    /* height="…" — a SCROLLING table with a sticky header, never pages: a
       roster of a class is read in one glance, not in pages of eight with
       the last one half empty (Michel, 2026-09-04). height wins over rows. */
    var height = parseInt(el.getAttribute("height") || "0", 10) || 0;
    if (height) perPage = 0;
    /* hints="col: explanation | col2: ..." → header tooltips. Read from the
       declaration HERE — below, el is reassigned to the fresh wrapper and
       the original attributes are gone with the replaced element. */
    var hints = {};
    (el.getAttribute("hints") || "").split("|").forEach(function (h) {
      var i = h.indexOf(":");
      if (i > 0) hints[h.slice(0, i).trim()] = h.slice(i + 1).trim();
    });

    /* empty="…" — what to say when the dataset is legitimately empty. The
       default reads like a fault, which is wrong for a grid that is simply
       waiting on a choice made elsewhere (pick a course → see its pages). */
    var emptyMsg = el.getAttribute("empty") || "";
    /* EDITABLE WAS SILENTLY IGNORED HERE. A grid bound to a dataset is
       rendered by this light table, not by the AG path in datagrid.md — so
       `editable="true"` looked like a knob and did nothing at all: "the grid
       looks r/o", and on iPhone "double tap did not work" while tutorial-01
       (an AG grid) was fine (Michel, 2026-08-20).

       Editing lands here instead of borrowing AG, and it is BETTER on the
       device this course is read on: a contenteditable cell takes ONE tap,
       where AG needs a double-click that phones barely deliver. */
    var editable = el.getAttribute("editable") === "true";
    /* a grid on a CLASS edits by default — a double click (or a second tap
       on the selected row) opens a cell; editable="false" says otherwise
       (Michel, 2026-10-16) */
    var editSaid = el.getAttribute("editable") || "";
    var pendingNew = null, typeNew = null;   /* the objects before ➕ New: the one that is not among them gets selected */
    var lcId = el.getAttribute("id") || "";
    var masterId = el.getAttribute("master") || el.getAttribute("detail-of") || "";
    var filterExpr = el.getAttribute("filter") || "";
    /* sort="<column>": the order the table opens in — a roster by name
       (Canvas writes "Last, First", so that is by last name), a work
       table by module (Michel, 2026-09-11). A header click still re-sorts. */
    var sortAttr = el.getAttribute("sort") || null;
    /* columns="topic, title": the table SHOWS these, in this order, and still
       PUBLISHES the whole row — a narrow list on the left of a bound card that
       reads every field (Michel, 2026-10-04, the stories example). */
    var shownCols = (el.getAttribute("columns") || "").split(",")
      .map(function (c) { return c.trim(); }).filter(Boolean);
    /* A TITLE BAR LIKE THE FORM'S (Michel, 2026-10-10: "the grid's header
       should be as big as the Form one"): ▦ and the words of the link that
       declared it — [The dogs](#) — or title="…". The table goes under it. */
    var link = el.querySelector ? el.querySelector("a") : null;
    var gridTitle = el.getAttribute("title") || (link ? (link.textContent || "").trim() : "");
    var wrap = document.createElement("div");
    wrap.className = "lc-datagrid";
    wrap.setAttribute("data-bind", bindId);
    if (lcId) wrap.setAttribute("data-lc-id", lcId);
    el.parentNode.replaceChild(wrap, el);
    el = wrap;
    var bodyEl = el;
    if (gridTitle) {
      var bar = document.createElement("div");
      bar.className = "lc-datagrid-title lc-dg-titlebar";
      bar.appendChild(document.createTextNode("▦ "));
      var tn = document.createElement("span");
      tn.className = "lc-datagrid-name";
      tn.textContent = gridTitle;
      bar.appendChild(tn);
      bodyEl = document.createElement("div");
      bodyEl.className = "lc-dg-body";
      el.appendChild(bar);
      el.appendChild(bodyEl);
      el.classList.add("lc-dg-titled");
    }

    var sortCol = sortAttr, sortAsc = true, page = 0;
    var colW = {};   /* a column's width the reader dragged, kept across repaints */

    /* grid-to-grid master/detail, the light-table half: the AG road had
       master= + filter="local=masterKey" and this road silently ignored
       both, so on a runner page the detail grid showed everything and a
       click upstream changed nothing (Michel, 2026-08-21). Same contract,
       same attributes — one selection bus for both roads. */
    var masterRow = null, lastData = null, publishedFirst = false;
    var lastPubJson = null;   /* the selected row as last re-published after a repaint */
    var selKey = null;   /* the selected row's identity (obj name, else its index) */
    var touched = null;  /* the row a button just wrote — next() walks on from it */
    var filterKeys = null;
    if (masterId && filterExpr) {
      var fm = filterExpr.match(/^\s*([\w-]+)\s*=\s*([\w-]+)\s*$/);
      if (fm) filterKeys = { local: fm[1], master: fm[2] };
    }
    if (filterKeys && window.lcMasterDetail) {
      window.lcMasterDetail.subscribe(masterId, function (row) {
        masterRow = row;
        /* the master moved: this grid's own detail (a bound form) must not
           keep showing a row that just got filtered away */
        publishedFirst = false;
        if (lastData) render(lastData);
      });
    }

    var onRemoteState = function (e) {
      if (!el.isConnected) { document.removeEventListener("lc-remote-state", onRemoteState); return; }
      var m = (window.lcModels || {})[bindId];
      if (lastData && e.detail === (m ? m.src : bindId)) render(lastData);
    };
    document.addEventListener("lc-remote-state", onRemoteState);

    var refWatch = {};
    function watchRefs(m) {
      if (!m) return;
      Object.keys(m.fields || {}).forEach(function (k) {
        var r = m.fields[k] && m.fields[k].ref;
        if (!r || refWatch[r]) return;
        refWatch[r] = 1;
        var L = window.lcDatasetListeners = window.lcDatasetListeners || {};
        var fn = function () { if (lastData) render(lastData); };
        fn._lcEl = el;
        (L[r] = L[r] || []).push(fn);
      });
    }

    function render(data) {
      lastData = data;
      watchRefs((window.lcModels || {})[bindId]);
      /* the class's own icon and words on the grid's title (Michel, 2026-10-17:
         "replacing the grid generic emoji") */
      var cdoc = window.lcDocOf && (window.lcModels || {})[bindId] ? window.lcDocOf(bindId) : null;
      var tbar = el.querySelector(".lc-dg-titlebar");
      if (tbar && tbar.firstChild && tbar.firstChild.nodeType === 3) {
        tbar.firstChild.nodeValue = (cdoc && cdoc.icon ? cdoc.icon : "▦") + " ";
        if (cdoc && cdoc.text) tbar.title = cdoc.text; else tbar.removeAttribute("title");
      }
      /* a list read from elsewhere: a ↻ in the title bar reads it again */
      if (window.lcRemote && window.lcRemote[bindId] && !window.lcRemote[bindId].db && el.querySelector(".lc-dg-titlebar") && !el.querySelector(".lc-dg-reload")) {
        var rb = document.createElement("button");
        rb.type = "button"; rb.className = "lc-dg-reload"; rb.textContent = "↻";
        rb.title = "read it again — the list lives elsewhere";
        rb.setAttribute("aria-label", "read the list again");
        rb.addEventListener("click", function (e) { e.stopPropagation(); window.lcRemoteReload(bindId); });
        el.querySelector(".lc-dg-titlebar").appendChild(rb);
      }
      if (data && filterKeys && masterRow) {
        data = data.filter(function (r) {
          return r[filterKeys.local] === masterRow[filterKeys.master];
        });
      }
      /* AN EMPTY CLASS STILL HAS ITS COLUMNS (Michel, 2026-10-17: "read the
         empty grid with the class, let students add new objects"): a grid on
         a class whose list is empty shows the class's fields as headers and
         ➕ New, never "No data" */
      /* a class whose list failed to load: the list's own words, not a row */
      var mdl0 = (window.lcModels || {})[bindId];
      var srcErr = mdl0 && mdl0.src && (window.lcDatasets[mdl0.src] || [])[0] && window.lcDatasets[mdl0.src][0]["⚠️"];
      if (srcErr) data = [];
      var emptyModel = (!data || !data.length) && (window.lcModels || {})[bindId];
      if ((!data || !data.length) && !emptyModel) {
        if (selKey && lcId && window.lcMasterDetail) { selKey = null; window.lcMasterDetail.publish(lcId, null); }
        /* empty for a moment (a class publishes before its rows arrive):
           when rows come, the first one is selected AND announced again —
           the card said "(no data)" over a lit row (Michel, 2026-10-16) */
        publishedFirst = false; lastPubJson = null;
        bodyEl.innerHTML = emptyMsg
          ? "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>" + emptyMsg + "</p>"
          : "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em'>⚠ No data: <code>" + bindId + "</code></p>";
        return;
      }
      if (emptyModel) {
        data = [];
        if (selKey && lcId && window.lcMasterDetail) { selKey = null; window.lcMasterDetail.publish(lcId, null); }
        publishedFirst = false; lastPubJson = null;
      }
      var allCols = data.length ? Object.keys(data[0])
        : (emptyModel.order || Object.keys(emptyModel.fields)).filter(function (c) { return !emptyModel.fields[c] || !emptyModel.fields[c].hidden; });
      var urlCol  = allCols.indexOf("url") >= 0 ? "url" : null;
      /* a grid on a CLASS (a class is a dataset): the model says which cell
         is the state, which are typed, which are locked; obj is the object's
         name, the grid's own business, never a column */
      var model = (window.lcModels || {})[bindId] || null;
      var cols    = allCols.filter(function (c) { return c !== "url" && !(model && (c === "obj" || c.charAt(0) === "_" || !model.fields[c] || model.fields[c].hidden)); });
      /* a class's columns in the class's order, whatever order the rows
         bring them in — a database hands them back alphabetically (Michel,
         2026-10-17: Dog, Hour, Walker for dog, walker, hour) */
      if (model && model.order) {
        var ord = model.order;
        cols.sort(function (a, b) {
          var i = ord.indexOf(a), j = ord.indexOf(b);
          return (i < 0 ? 1e6 : i) - (j < 0 ? 1e6 : j);
        });
      }
      if (shownCols.length) cols = shownCols.filter(function (c) { return allCols.indexOf(c) >= 0; });
      function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/'/g, "&#39;"); }
      function dressedCell(row, c, idx) { return dressedCell0(row, c, idx); }
      /* the gutter: ⋯ for a class with no state; a subclass's row wears its
         class's icon there (Michel, 2026-10-17) — a tap still opens its verbs */
      var gut = !!(model && (!model.state || (model.subs || []).length));
      var gutTd = function (idx) {
        var r = sorted[idx] || {}, kd = r._kind && window.lcDocOf ? window.lcDocOf(r._kind) : null;
        var mark = kd && kd.icon ? kd.icon : "⋯", tip = (r._kind ? "a " + r._kind + " — " : "") + "what this one can do";
        return "<td class='lc-dg-gut' data-row='" + idx + "'><button type='button' class='lc-dg-rowmenu" + (kd && kd.icon ? " lc-dg-kindmark" : "") + "'"
          + " title='" + esc(tip) + "' aria-label='" + esc(tip) + "'>" + esc(mark) + "</button></td>";
      };
      function dressedCell0(row, c, idx) {
        var v = row[c] !== undefined && row[c] !== null ? row[c] : "";
        var f = model.fields[c];
        if (f && f.state) {
          var wide = (f.enum || []).reduce(function (m, s) { return Math.max(m, String(s).length); }, String(v).length);
          return "<td class='lc-dg-state' data-row='" + idx + "' title='what this one can do'>"
            + "<span class='lc-dg-chip' style='min-width:" + wide + "ch'>" + esc(v) + "</span><span class='lc-dg-caret'>⌄</span></td>";
        }
        /* a tap on a row SELECTS it; cells open for typing only when the
           grid says editable="true" — the detail form is where one edits
           (Michel, 2026-10-16) */
        /* A REFERENCE (Michel, 2026-10-17: "a picklist in the grid"): the
           cell names the referenced object by its first text attribute and
           picks among the referenced class's objects */
        if (f && f.ref) {
          var rr = (window.lcDatasets || {})[f.ref] || [], lab = refLabel(f.ref);
          var nameOf = function (r) { return r ? String(r[lab] != null && r[lab] !== "" ? r[lab] : r.obj) : ""; };
          var curR = rr.filter(function (r) { return String(r.obj) === String(v); })[0];
          var shown = curR ? nameOf(curR) : "";   /* plain, like any other cell; the icon is the column's */
          if (f.ro || editSaid === "false") return "<td>" + esc(shown) + "</td>";
          /* a rich pick, like AG Grid's (Michel, 2026-10-17: "the picklist is
             a bit narrow"): the value and its icon, a ▾, a roomy list */
          return "<td class='lc-dg-refcell' data-col='" + c + "' data-row='" + idx + "' data-ref='" + esc(f.ref) + "' title='pick a " + esc(f.ref) + "'>"
            + "<span class='lc-dg-refval'>" + esc(shown) + "</span><span class='lc-dg-caret'>⌄</span></td>";
        }
        if (!f || f.ro || editSaid === "false") return "<td>" + esc(v) + "</td>";
        if (f.enum)
          return "<td><select class='lc-dg-pick' data-col='" + c + "' data-row='" + idx + "'>"
            + [""].concat(f.enum).map(function (o) { return "<option" + (String(o) === String(v) ? " selected" : "") + ">" + esc(o) + "</option>"; }).join("")
            + "</select></td>";
        return "<td class='lc-dg-typed' title='double click to edit' data-col='" + c + "' data-row='" + idx + "'"
          + " inputmode='" + (f.t === "int" || f.t === "float" ? "decimal" : "text") + "'>" + esc(v) + "</td>";
      }

      var sorted = data.slice();
      if (sortCol !== null) {
        sorted.sort(function (a, b) {
          var va = a[sortCol], vb = b[sortCol];
          /* words compare as a reader would: "abeera" before "DWLERS" */
          var diff = (typeof va === "string" && typeof vb === "string")
            ? va.localeCompare(vb, undefined, { sensitivity: "base" })
            : (va > vb ? 1 : va < vb ? -1 : 0);
          return sortAsc ? diff : -diff;
        });
      }
      var total = sorted.length, pp = perPage || total || 1;
      var pages = Math.max(1, Math.ceil(total / pp));
      /* an empty list made 0 / 0 a page number that stuck, and no row ever
         showed again — the page is always a number, the first one at worst */
      page = Math.min(page || 0, pages - 1);
      var slice = sorted.slice(page * pp, (page + 1) * pp);

      var html = (height ? "<div class='lc-dg-scroll' style='max-height:" + height + "px'>" : "")
        + "<table class='lc-dg-table'><thead><tr>"
        + (gut ? "<th class='lc-dg-gut' aria-label='actions'></th>" : "")
        + cols.map(function (c) {
            var arrow = sortCol === c ? (sortAsc ? " ↑" : " ↓") : "";
            var hint = hints[c] ? " title='" + hints[c].replace(/'/g, "&#39;") + "' class='lc-th-hint'" : "";
            var label = window.lcPrettifyKey ? window.lcPrettifyKey(c) : c;
            /* a reference's column wears its class's icon (its docstring) */
            var rf = model && model.fields[c] && model.fields[c].ref;
            var rdoc = rf && window.lcDocOf ? window.lcDocOf(rf) : null;
            if (rdoc && rdoc.icon) label = rdoc.icon + " " + label;
            var cw = colW[c] ? " style='width:" + colW[c] + "px;min-width:" + colW[c] + "px'" : "";
            return "<th data-col='" + c + "'" + hint + cw + ">" + label + arrow + "<span class='lc-dg-grip' title='drag to resize'></span></th>";
          }).join("") + "</tr></thead><tbody>"
        + slice.map(function (row) {
            var urlVal = urlCol ? (row[urlCol] || "") : "";
            var trAttrs = urlVal ? " data-url='" + urlVal.replace(/'/g, "&#39;") + "' style='cursor:pointer'" : "";
            return "<tr" + trAttrs + ">"
              + (gut ? gutTd(sorted.indexOf(row)) : "")
              + cols.map(function (c) {
                  if (model) return dressedCell(row, c, sorted.indexOf(row));
                  var v = row[c] !== undefined ? row[c] : "";
                  /* a UTC stamp prints on the reader's clock, UTC on hover;
                     an editable cell keeps the raw value it will write back */
                  var w = !editable && window.lcWhen ? window.lcWhen(v) : null;
                  if (w) return "<td title='" + w.utc + "'>" + w.text + "</td>";
                  if (!editable) return "<td>" + v + "</td>";
                  /* the row is found again by its position in the CURRENT
                     sort, so an edit after sorting still lands on the row
                     the reader is looking at */
                  return "<td contenteditable='true' class='lc-dg-edit'" +
                         " data-col='" + c + "' data-row='" + sorted.indexOf(row) + "'" +
                         " inputmode='" + (typeof row[c] === "number" ? "decimal" : "text") +
                         "'>" + v + "</td>";
                }).join("") + "</tr>";
          }).join("") + "</tbody></table>" + (height ? "</div>" : "");

      /* a list kept in a database: 💾 Save sends what changed, ↻ reads it again */
      var dbSrc = model ? model.src : bindId;
      var dbR = window.lcRemote && window.lcRemote[dbSrc] && window.lcRemote[dbSrc].db ? window.lcRemote[dbSrc] : null;
      var dbCh = dbR && window.lcDatasetChanges ? window.lcDatasetChanges(dbSrc) : null;
      /* 🧹 on the author's device: the table's columns no attribute declares,
         and the class names no class (nor a was=) answers to any more */
      var orphans = [], stale = [];
      if (dbR && dbR.unl && model && lsGet(dbR.unl.akey)) {
        var row0 = (window.lcDatasets[dbSrc] || [])[0] || {};
        /* every class on the table declares its columns — a subclass's
           own (Sprint's speed) is no leftover of the base class */
        var declared = {};
        (unlCols(dbSrc) || []).forEach(function (c) { declared[c.n] = 1; });
        orphans = Object.keys(row0).filter(function (k) {
          return k !== "id" && k !== "obj" && k.charAt(0) !== "_" && k !== "⚠️" && !declared[k];
        });
        var known = [bindId].concat(model.subs || []), wases = (model.subs || []).map(function (k) { var m2 = (window.lcModels || {})[k]; return m2 && m2.was; });
        (window.lcDatasets[dbSrc] || []).forEach(function (r) {
          var k = r && r._sub;
          if (k && known.indexOf(k) < 0 && wases.indexOf(k) < 0 && stale.indexOf(k) < 0) stale.push(k);
        });
      }
      var st = dbR ? (dbR.state || (dbCh && dbCh.n ? "dirty" : "ok")) : "";
      var stTip = { ok: "saved", dirty: (dbCh && dbCh.n) + " change(s) to save — saving by itself, or tap", saving: "saving…",
                    error: "not saved — " + (dbR && dbR.saveErr || "") + " — tap to try again" }[st] || "";
      /* columns the class has and the table not yet: ↻ adds them (author) */
      var pending = [];
      if (dbR && dbR.unl && dbR.unl.tcols && lsGet(dbR.unl.akey)) {
        pending = (unlCols(dbSrc) || []).map(function (c) { return c.n; }).filter(function (n) { return !dbR.unl.tcols[n]; });
      }
      var rfTip = pending.length ? "↻ adds the column" + (pending.length > 1 ? "s " : " ") + pending.join(", ") + " to the table, then reads it" : "read the database again";
      /* the corner, right to left (Michel, 2026-10-17): ＋, the save state
         (always there), ↻ (on hover) — so nothing leaves a hole */
      var corner = (orphans.length || stale.length ? "<button class='lc-dg-cbtn lc-dg-tidy' type='button' title='" + esc(
              [orphans.length ? "drop the columns no attribute uses: " + orphans.join(", ") : "",
               stale.length ? "clear the class names no class answers to: " + stale.join(", ") : ""].filter(Boolean).join(" · ")) + "' aria-label='tidy the table'>🧹</button>" : "")
        + (dbR ? "<button class='lc-dg-cbtn lc-dg-refresh" + (pending.length ? " lc-dg-pending" : "") + "' type='button' title='" + esc(rfTip) + "' aria-label='" + esc(rfTip) + "'>↻</button>"
            + "<button class='lc-dg-cbtn lc-dg-save lc-dg-st-" + st + "' type='button'"
            + (st === "dirty" || st === "error" ? "" : " disabled") + " title='" + esc(stTip) + "' aria-label='" + esc(stTip) + "'>"
            + "<span>" + { ok: "✓", dirty: "●", saving: "⟳", error: "⚠" }[st] + "</span></button>" : "")
        + (model ? "<button class='lc-dg-cbtn lc-dg-new' type='button' title='a new " + esc(bindId) + "' aria-label='a new " + esc(bindId) + "'>＋</button>" : "");
      el.classList.toggle("lc-dg-cornered", !!corner);
      var dbBtns = "";
      /* an unlisted table: the name to paste, or — on the author's device —
         the name to share */
      var U = dbR && dbR.unl;
      if (U && !U.share) dbBtns = dbBtns.replace("lc-dg-save' type='button'", "lc-dg-save' type='button' disabled");
      var unlBar = "";
      if (U) {
        unlBar = "<div class='lc-dg-unl'>";
        /* compact (Michel, 2026-10-17: "too many keys still there!!!"): the
           author sees the name to share on one line; a new author key shows
           once and leaves when copied; a newcomer sees one field — the
           author's field takes its place, never sits beside it */
        if (U.hint && U.db)
          unlBar += "<span>✍️ put <code class='lc-dg-unl-show'>unlisted=\"" + esc(U.hint) + "\"</code> on the <b>" + esc(U.db) + "</b> database line</span>"
            + "<button class='lc-dg-btn lc-dg-unl-copy' type='button' data-copy='unlisted=\"" + esc(U.hint) + "\"'>📋 Copy</button>";
        else if (U.share && U.author && !U.fixed)
          unlBar += "<span>🔗 <code class='lc-dg-unl-show' title='the unlisted name — share it with the class'>" + esc(U.share) + "</code></span>"
            + "<button class='lc-dg-btn lc-dg-unl-copy' type='button' data-copy='" + esc(U.share) + "' title='copy the name, to share it with the class'>📋 Copy</button>";
        if (U.newKey)
          unlBar += "<span class='lc-dg-unl-key'>🔑 your author key, shown once — keep it: <code>" + esc(U.newKey) + "</code></span>"
            + "<button class='lc-dg-btn lc-dg-unl-copy lc-dg-unl-keycopy' type='button' data-copy='" + esc(U.newKey) + "'>📋 Copy</button>";
        if (U.need)
          unlBar += "<span class='lc-dg-unl-ask'><input class='lc-dg-unl-name' type='text' autocomplete='off' spellcheck='false' placeholder='🔗 the list&#39;s name' aria-label='the list&#39;s unlisted name'>"
            + "<button class='lc-dg-btn lc-dg-unl-ok' type='button'>OK</button></span>"
            + "<span class='lc-dg-unl-auth' hidden><input class='lc-dg-unl-akey' type='password' autocomplete='off' placeholder='🔑 author key — empty makes one' aria-label='author key'>"
            + "<button class='lc-dg-btn lc-dg-unl-claim' type='button'>OK</button></span>"
            + "<button class='lc-dg-unl-me' type='button'>✍️ I'm the author</button>";
        unlBar = unlBar === "<div class='lc-dg-unl'>" ? "" : unlBar + "</div>";   /* nothing to say, no bar */
      }
      if (srcErr) html += "<p class='lc-dg-say' role='status'>⚠️ " + esc(srcErr) + "</p>";
      else if (U && dbR.error) html += "<p class='lc-dg-say' role='status'>⚠️ " + esc(dbR.error) + "</p>";
      /* why ⚠ — said under the grid, not in a tooltip a finger never sees */
      else if (st === "error" && dbR.saveErr) html += "<p class='lc-dg-say' role='status'>⚠️ not saved: " + esc(dbR.saveErr) + "</p>";
      if (corner) html = "<div class='lc-dg-corner'>" + corner + "</div>" + html;
      html += unlBar;
      if (pages > 1) {
        html += "<div class='lc-dg-pages'>";
        if (page > 0)         html += "<button data-pg='" + (page - 1) + "'>←</button>";
        html += "<span>Page " + (page + 1) + " / " + pages + "</span>";
        if (page < pages - 1) html += "<button data-pg='" + (page + 1) + "'>→</button>";
        html += "</div>";
      }

      /* THE SCROLL SURVIVES A REPUBLISH. Picking a seat binds its card,
         the card republishes the class, and this table is rebuilt from
         the new rows: the selection was kept (below), the scroll was not —
         the box came back at the top and the picked row sat out of view
         (Michel, 2026-09-15, the desk's roster). Keep where the reader was. */
      var scrollBox = bodyEl.querySelector(".lc-dg-scroll");
      var keepTop = scrollBox ? scrollBox.scrollTop : 0;
      bodyEl.innerHTML = html;
      if (keepTop) { var nb = bodyEl.querySelector(".lc-dg-scroll"); if (nb) nb.scrollTop = keepTop; }
      if (editable) {
        el.querySelectorAll("td.lc-dg-edit").forEach(function (td) {
          /* commit on blur and on Enter — never on every keystroke, or the
             chart would redraw under the finger mid-number */
          var commit = function () {
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            if (!row) return;
            var col = td.getAttribute("data-col");
            var was = row[col];
            var txt = (td.textContent || "").trim();
            /* a column that held numbers keeps holding numbers: a chart
               cannot plot "120 " and a blank must stay blank, not 0 */
            var val = txt;
            if (typeof was === "number" || (was === "" && txt !== "" && !isNaN(Number(txt))))
              val = txt === "" ? "" : Number(txt);
            if (val === was) return;
            row[col] = val;
            if (window.lcSetDataset)
              window.lcSetDataset(bindId, window.lcDatasets[bindId] || data);
          };
          td.addEventListener("blur", commit);
          td.addEventListener("keydown", function (e) {
            if (e.key === "Enter") { e.preventDefault(); td.blur(); }
          });
        });
      }
      if (model) {
        var py = function (code) { if (window.lcPySend) window.lcPySend(code); };
        var objOf = function (td) { var r = sorted[parseInt(td.getAttribute("data-row"), 10)]; return r ? String(r.obj) : ""; };
        /* a typed cell: the value goes through the object — type, enum and
           lock apply there, and a refused value says why under the grid */
        /* a tap SELECTS the row; a double click — or a second tap on the
           row already selected, which a phone can deliver — opens the cell,
           its text selected so typing replaces it; Enter or leaving commits,
           Escape gives up (Michel, 2026-10-16) */
        el.querySelectorAll("td.lc-dg-typed").forEach(function (td) {
          var was = "";
          var open = function () {
            if (td.isContentEditable) return;
            was = td.textContent;
            td.setAttribute("contenteditable", "true");
            td.classList.add("lc-dg-typing");
            td.focus();
            try {
              var r = document.createRange(); r.selectNodeContents(td);
              var sl = window.getSelection(); sl.removeAllRanges(); sl.addRange(r);
            } catch (e) {}
          };
          var shut = function () { td.removeAttribute("contenteditable"); td.classList.remove("lc-dg-typing"); };
          var commit = function () {
            if (!td.isContentEditable) return;
            shut();
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            if (!row) return;
            var col = td.getAttribute("data-col"), txt = (td.textContent || "").trim();
            if (String(row[col] == null ? "" : row[col]) === txt) return;
            py("_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(col) + "," + JSON.stringify(txt) + ")");
          };
          td.addEventListener("click", function () {
            var tr = td.parentNode;
            if (tr && tr.classList.contains("lc-dg-selected")) open();
          });
          td.addEventListener("dblclick", open);
          td.addEventListener("blur", commit);
          td.addEventListener("keydown", function (e) {
            if (!td.isContentEditable) return;
            typeNew = null;   /* typing has begun: no repaint re-opens a fresh cell over it */
            if (e.key === "Enter") { e.preventDefault(); td.blur(); }
            else if (e.key === "Escape") { e.preventDefault(); td.textContent = was; shut(); }
          });
        });
        /* a click in a typed cell or a picklist still selects its row — the
           bound card follows the row being edited (a swallowed click left
           the first row selected, classroom 4's roster, 2026-10-16) */
        el.querySelectorAll("td.lc-dg-refcell").forEach(function (cell) {
          cell.addEventListener("click", function (e) {
            e.stopPropagation();
            var open = document.querySelector(".lc-dg-refmenu");
            document.querySelectorAll(".lc-dg-menu").forEach(function (m) { m.remove(); });
            if (open && open._lcFor === cell) return;
            var row = sorted[parseInt(cell.getAttribute("data-row"), 10)];
            if (!row) return;
            var ref = cell.getAttribute("data-ref"), col = cell.getAttribute("data-col");
            var rr = (window.lcDatasets || {})[ref] || [], lab = refLabel(ref);
            var rd = window.lcDocOf ? window.lcDocOf(ref) : null, ic = rd && rd.icon ? rd.icon + " " : "";
            var nameOf = function (r) { return String(r[lab] != null && r[lab] !== "" ? r[lab] : r.obj); };
            var menu = document.createElement("div");
            menu.className = "lc-dg-menu lc-dg-refmenu";
            menu._lcFor = cell;
            menu.setAttribute("role", "listbox");
            menu.innerHTML = (rr.length > 8 ? "<input class='lc-dg-refsearch' type='search' placeholder='🔍 find' aria-label='find'>" : "")
              + "<button type='button' class='lc-dg-verb' data-obj=''><span>—</span></button>"
              + rr.map(function (r) {
                  return "<button type='button' class='lc-dg-verb" + (String(r.obj) === String(row[col]) ? " lc-dg-cur" : "") + "' role='option' data-obj='" + esc(r.obj) + "'>"
                    + "<span>" + esc(nameOf(r)) + "</span></button>";
                }).join("");
            var rc = cell.getBoundingClientRect();
            menu.style.minWidth = Math.max(rc.width, 180) + "px";
            menu.style.left = (Math.max(4, Math.min(rc.left, window.innerWidth - Math.max(rc.width, 180) - 8)) + window.scrollX) + "px";
            menu.style.top = (rc.bottom + window.scrollY) + "px";
            document.body.appendChild(menu);
            var find = menu.querySelector(".lc-dg-refsearch");
            if (find) {
              find.addEventListener("click", function (ev) { ev.stopPropagation(); });
              find.addEventListener("input", function () {
                var q = find.value.toLowerCase();
                menu.querySelectorAll("button[data-obj]").forEach(function (b) { b.hidden = q && b.textContent.toLowerCase().indexOf(q) < 0; });
              });
              find.focus();
            }
            menu.querySelectorAll("button[data-obj]").forEach(function (b) {
              b.addEventListener("click", function (ev) {
                ev.stopPropagation();
                menu.remove();
                py("_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(col) + "," + JSON.stringify(b.getAttribute("data-obj")) + ")");
              });
            });
            setTimeout(function () { document.addEventListener("click", function () { menu.remove(); }, { once: true }); }, 0);
          });
        });
        el.querySelectorAll("select.lc-dg-pick").forEach(function (sel) {
          sel.addEventListener("change", function () {
            var row = sorted[parseInt(sel.getAttribute("data-row"), 10)];
            if (row) py("_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(sel.getAttribute("data-col")) + "," + JSON.stringify(sel.value) + ")");
          });
        });
        /* the ⌄: the row's verbs — a transition is live when the row's state
           is in its pre, grey otherwise (pressing a grey one says what it
           needs); plain verbs always; Delete last, born of Object */
        var closeMenu = function () { document.querySelectorAll(".lc-dg-menu").forEach(function (m) { m.parentNode.removeChild(m); }); };
        var verbsMenu = function (td, e) {
          {
            e.stopPropagation();
            var open = document.querySelector(".lc-dg-menu");
            closeMenu();
            if (open && open._lcFor === td) return;
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            if (!row) return;
            /* the row is marked as selected too (no publish: a follower's
               republish would repaint the table and take the menu with it) */
            var tr = td.parentNode;
            var key = row.obj != null ? "o:" + row.obj : "i:" + parseInt(td.getAttribute("data-row"), 10);
            /* A TAP IN THE GUTTER SELECTS FIRST (Michel, 2026-10-17): the row
               becomes the selection — a bound form follows — then its verbs
               open, on the row as redrawn */
            if (!e._lcReopen && key !== selKey && lcId && window.lcMasterDetail) {
              el.querySelectorAll("tbody tr").forEach(function (x) { x.classList.remove("lc-dg-selected"); });
              tr.classList.add("lc-dg-selected");
              selKey = key;
              window.lcMasterDetail.publish(lcId, row);
              setTimeout(function () { if (el._lcOpenVerbs) el._lcOpenVerbs(key); }, 150);
              return;
            }
            el.querySelectorAll("tbody tr").forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            tr.classList.add("lc-dg-selected");
            selKey = key;
            /* a subclass's row wears its own verbs */
            var rm = (row._kind && (window.lcModels || {})[row._kind]) || model;
            var cur = String(row[rm.state] == null ? "" : row[rm.state]);
            var items = [];
            Object.keys(rm.transitions).forEach(function (n) {
              var tr = rm.transitions[n], ok = !tr.pre.length || tr.pre.indexOf(cur) >= 0;
              items.push({ n: n, ok: ok, hint: ok ? ("→ " + (tr.post || cur)) : ("needs " + tr.pre.join(" / ")) });
            });
            rm.verbs.forEach(function (n) { items.push({ n: n, ok: true, hint: "" }); });
            items.push({ n: "delete", ok: true, hint: "", label: "🗑 Delete", danger: true });
            var menu = document.createElement("div");
            menu.className = "lc-dg-menu";
            menu._lcFor = td;
            menu.innerHTML = items.map(function (it) {
              var dd = !it.label && window.lcDocOf ? window.lcDocOf(row._kind || bindId, it.n) : null;
              var label = it.label || ((dd && dd.icon ? dd.icon + " " : "") + (window.lcPrettifyKey ? window.lcPrettifyKey(it.n) : it.n));
              return "<button type='button' class='lc-dg-verb" + (it.ok ? "" : " lc-dg-off") + (it.danger ? " lc-dg-danger" : "")
                + "' data-verb='" + it.n + "' data-ok='" + (it.ok ? 1 : 0) + "' title='" + esc((dd && dd.text) || it.hint) + "'>"
                + "<span>" + esc(label) + "</span>" + (it.hint ? "<small>" + esc(it.hint) + "</small>" : "") + "</button>";
            }).join("");
            /* on the body, fixed: a scrolling grid clipped the last row's
               menu under its frame (Michel, 2026-10-16) */
            var r = td.getBoundingClientRect();
            menu.style.left = (Math.max(4, Math.min(r.left, window.innerWidth - 200)) + window.scrollX) + "px";
            menu.style.top = (r.bottom + window.scrollY) + "px";
            document.body.appendChild(menu);
            var box = el.querySelector(".lc-dg-scroll");
            if (box) box.addEventListener("scroll", closeMenu, { once: true, passive: true });
            menu.querySelectorAll("button[data-verb]").forEach(function (b) {
              b.addEventListener("click", function (ev) {
                ev.stopPropagation();
                var verb = b.getAttribute("data-verb");
                if (b.getAttribute("data-ok") !== "1") { closeMenu(); window.lcGridSay(bindId, "⛔ " + verb + " " + b.getAttribute("title")); return; }
                if (verb === "delete") {
                  /* the row as the reader sees it (Michel, 2026-10-17: "Delete
                     dog_1?" — an internal name, and not even the walk's own):
                     the class's icon and name, then its first values, a
                     reference by its name */
                  var kind = row._kind || bindId, kdoc = window.lcDocOf ? window.lcDocOf(kind) : null;
                  var seen = cols.filter(function (c) { return c !== model.state; }).map(function (c) {
                    var f = model.fields[c], v = row[c];
                    if (f && f.ref && v != null && v !== "") {
                      var rr = ((window.lcDatasets || {})[f.ref] || []).filter(function (x) { return String(x.obj) === String(v); })[0];
                      var lab = refLabel(f.ref);
                      v = rr ? (rr[lab] != null && rr[lab] !== "" ? rr[lab] : "") : "";
                    }
                    return v == null ? "" : String(v);
                  }).filter(Boolean).slice(0, 3);
                  if (!window.confirm("Delete this " + (kdoc && kdoc.icon ? kdoc.icon + " " : "") + kind + (seen.length ? ": " + seen.join(" · ") : "") + "?")) return;
                }
                closeMenu();
                py("_lc_verb(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(verb) + ")");
              });
            });
            setTimeout(function () { document.addEventListener("click", closeMenu, { once: true }); }, 0);
          }
        };
        el.querySelectorAll("td.lc-dg-state").forEach(function (td) {
          td.addEventListener("click", function (e) { verbsMenu(td, e); });
        });
        /* A CLASS WITH NO STATE STILL HAS VERBS (Michel, 2026-10-16) — and
           Delete always: a light ⋯ in the row's gutter opens them (2026-10-17) */
        el.querySelectorAll("td.lc-dg-gut").forEach(function (td) {
          td.addEventListener("click", function (e) { verbsMenu(td, e); });
        });
        el._lcOpenVerbs = function (key) {
          var tds = el.querySelectorAll("td.lc-dg-gut");
          for (var i = 0; i < tds.length; i++) {
            var ix = parseInt(tds[i].getAttribute("data-row"), 10), r = sorted[ix];
            if (r && (r.obj != null ? "o:" + r.obj : "i:" + ix) === key) {
              verbsMenu(tds[i], { _lcReopen: true, stopPropagation: function () {} });
              return;
            }
          }
        };
        /* ➕ New: the class itself, or — when the page declares subclasses —
           a pick of the class and each one; the new row gets selected
           (Michel, 2026-10-16) */
        var nb = el.querySelector(".lc-dg-new");
        var make = function (kind) {
          pendingNew = {};
          (window.lcDatasets[bindId] || []).forEach(function (r) { pendingNew[String(r.obj)] = 1; });
          setTimeout(function () { pendingNew = null; }, 4000);
          py("_lc_new(" + JSON.stringify(bindId) + (kind && kind !== bindId ? "," + JSON.stringify(kind) : "") + ")");
        };
        if (nb) nb.addEventListener("click", function (e) {
          e.stopPropagation();
          var subs = model.subs || [];
          var open = document.querySelector(".lc-dg-menu");
          closeMenu();
          if (!subs.length) { make(bindId); return; }
          if (open && open._lcFor === nb) return;
          var menu = document.createElement("div");
          menu.className = "lc-dg-menu lc-dg-kinds";
          menu._lcFor = nb;
          menu.innerHTML = [bindId].concat(subs).map(function (k) {
            var kd = window.lcDocOf ? window.lcDocOf(k) : null;   /* each class wears its docstring's icon */
            return "<button type='button' class='lc-dg-verb' data-kind='" + esc(k) + "'><span>" + esc((kd && kd.icon ? kd.icon + " " : "") + k) + "</span></button>";
          }).join("");
          var r = nb.getBoundingClientRect();
          menu.style.left = (Math.max(4, Math.min(r.left, window.innerWidth - 200)) + window.scrollX) + "px";
          menu.style.top = (r.bottom + window.scrollY) + "px";
          document.body.appendChild(menu);
          menu.querySelectorAll("button[data-kind]").forEach(function (b) {
            b.addEventListener("click", function (ev) { ev.stopPropagation(); closeMenu(); make(b.getAttribute("data-kind")); });
          });
          setTimeout(function () { document.addEventListener("click", closeMenu, { once: true }); }, 0);
        });
      }
      /* COLUMNS RESIZE (Michel, 2026-10-16): drag the right edge of a header */
      var sv = el.querySelector(".lc-dg-save"), rf = el.querySelector(".lc-dg-refresh");
      /* ONE PRESS SAVES (Michel, 2026-10-17: "when I'm in a new line and
         click on save, it only gets the focus away"): the press itself left
         the open cell, its commit redrew the grid, and the click landed on
         a button that was gone. The save now starts on the press, before
         the focus moves; a keyboard's click still works, never twice. */
      var saveNow = function (typing) {
        if (!dbR || dbR.state === "saving") return;
        clearTimeout(dbR._auto);
        dbR.state = "saving"; dbR.saveErr = "";
        if (sv) { sv.disabled = true; sv.className = sv.className.replace(/lc-dg-st-\w+/, "lc-dg-st-saving"); sv.innerHTML = "<span>⟳</span>"; }
        if (window.lcDid && lcId) window.lcDid.mark(lcId, "save");   /* grid.saved — a proof reads it */
        /* a cell still open is committed first, and its value given a beat to
           reach the object — a click on 💾 right after typing saved the blank */
        if (typing) typing.blur();
        new Promise(function (res) { setTimeout(res, typing ? 400 : 0); }).then(function () {
          return window.lcDatasetSave(dbSrc);
        }).then(function () {
          dbR.state = "";                       /* the table is read again: the grid repaints ✓ */
        }).catch(function (err) {
          dbR.state = "error"; dbR.saveErr = err.message;
          window.lcSetDataset(dbSrc, window.lcDatasets[dbSrc] || []);
        });
      };
      var doSave = function (e) {
        e.stopPropagation();
        /* the click that ends a press already saving is that same press */
        if (e.type === "click" && sv._lcPressed) { sv._lcPressed = false; return; }
        if (e.type === "pointerdown") { e.preventDefault(); sv._lcPressed = true; }
        if (sv.disabled) return;
        var act = document.activeElement;
        saveNow(el.querySelector(".lc-dg-typing")
          || (act && act !== document.body && el.contains(act) && act.isContentEditable ? act : null));
      };
      /* AUTOSAVE (Michel, 2026-10-17: "autosave should work as soon as it
         looks reasonable"): a closed cell's change, a deletion, a new object
         once it holds a value — a beat after the grid settles, never while a
         cell is open; an empty new row waits for its first value */
      if (dbR && st === "dirty" && dbCh) {
        var act2 = document.activeElement;
        var open = el.querySelector(".lc-dg-typing") || (act2 && act2 !== document.body && el.contains(act2) && act2.isContentEditable);
        var blank = dbCh.ins.some(function (r) {
          return !Object.keys(r).some(function (k) {
            var f = model && model.fields[k];
            return !(f && f.state) && k !== "_kind" && r[k] !== "" && r[k] != null;
          });
        });
        clearTimeout(dbR._auto);
        if (!open && !blank) dbR._auto = setTimeout(function () {
          var c = window.lcDatasetChanges(dbSrc);
          if (c && c.n && dbR.state !== "saving") saveNow(null);
        }, 700);
      }
      if (sv) { sv.addEventListener("pointerdown", doSave); sv.addEventListener("click", doSave); }
      if (U) {
        var uOk = el.querySelector(".lc-dg-unl-ok"), uName = el.querySelector(".lc-dg-unl-name");
        var take = function () {
          var v = (uName.value || "").trim();
          if (!v) return;
          lsSet(U.skey, v); U.need = false;
          window.lcRemoteReload(dbSrc);
        };
        if (uOk) uOk.addEventListener("click", function (e) { e.stopPropagation(); take(); });
        if (uName) uName.addEventListener("keydown", function (e) { e.stopPropagation(); if (e.key === "Enter") take(); });
        var uMe = el.querySelector(".lc-dg-unl-me"), uAuth = el.querySelector(".lc-dg-unl-auth");
        var uAsk = el.querySelector(".lc-dg-unl-ask");
        if (uMe) uMe.addEventListener("click", function (e) {
          e.stopPropagation();
          var author = uAuth.hidden;
          uAuth.hidden = !author; uAsk.hidden = author;
          uMe.textContent = author ? "🔗 I have the list's name" : "✍️ I'm the author";
        });
        var uClaim = el.querySelector(".lc-dg-unl-claim"), uKey = el.querySelector(".lc-dg-unl-akey");
        if (uKey) uKey.addEventListener("keydown", function (e) { e.stopPropagation(); });
        if (uClaim) uClaim.addEventListener("click", function (e) {
          e.stopPropagation();
          var k = (uKey.value || "").trim(), made = !k;
          if (made) {
            var b = new Uint8Array(18); window.crypto.getRandomValues(b);
            k = "lca_" + Array.prototype.map.call(b, function (x) { return ("0" + x.toString(16)).slice(-2); }).join("");
          }
          U.rpc("lc_claim", { token: k }).then(function (ok) {
            if (!ok) throw new Error("this database already has an author — paste that author key");
            lsSet(U.akey, k);
            if (made) U.newKey = k;
            window.lcRemoteReload(dbSrc, { ensure: true });   /* the new author's class makes its table */
          }).catch(function (err) { if (window.lcGridSay) window.lcGridSay(bindId, "⚠️ " + err.message); });
        });
        el.querySelectorAll(".lc-dg-unl-copy").forEach(function (b) {
          b.addEventListener("click", function (e) {
            e.stopPropagation();
            var v = b.getAttribute("data-copy");
            var done = function () {
              b.textContent = "✓ Copied";
              /* the author key, once copied, leaves the screen */
              if (b.classList.contains("lc-dg-unl-keycopy")) setTimeout(function () {
                U.newKey = "";
                var k = el.querySelector(".lc-dg-unl-key");
                if (k) k.remove();
                b.remove();
              }, 900);
            };
            var pick = function () {
              var c = b.previousElementSibling && b.previousElementSibling.querySelector("code");
              if (c) { var rg = document.createRange(); rg.selectNodeContents(c); var sl = window.getSelection(); sl.removeAllRanges(); sl.addRange(rg); }
              b.textContent = "⌘C to copy";
            };
            if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(done, pick);
            else pick();
          });
        });
      }
      var tidyBtn = el.querySelector(".lc-dg-tidy");
      if (tidyBtn) tidyBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        var U2 = dbR.unl;
        var say = [orphans.length ? "drop the column" + (orphans.length > 1 ? "s " : " ") + orphans.join(", ") + " (their data is lost)" : "",
                   stale.length ? "clear the class name" + (stale.length > 1 ? "s " : " ") + stale.join(", ") + " (those rows become " + bindId + ")" : ""].filter(Boolean).join(" and ");
        if (!window.confirm("In the table " + U2.tbl + ": " + say + "?")) return;
        var clearRows = (window.lcDatasets[dbSrc] || []).filter(function (r) { return r && r.id != null && stale.indexOf(r._sub) >= 0; })
          .map(function (r) { return { id: r.id, _sub: null }; });
        (orphans.length ? U2.rpc("lc_drop", { token: lsGet(U2.akey), tbl: U2.tbl, cols: orphans }) : Promise.resolve(0))
          .then(function () { return clearRows.length ? U2.rpc("lc_save", { share: U2.share, tbl: U2.tbl, ins: [], upd: clearRows, del: [] }) : null; })
          .then(function () { window.lcRemoteReload(dbSrc, { ensure: true }); })
          .catch(function (err) { if (window.lcGridSay) window.lcGridSay(bindId, "⚠️ " + err.message); });
      });
      if (rf) rf.addEventListener("click", function (e) {
        e.stopPropagation();
        var ch = window.lcDatasetChanges(dbSrc);
        if (ch && ch.n && !window.confirm(ch.n + " change(s) not saved — read the database again and lose them?")) return;
        window.lcRemoteReload(dbSrc, { ensure: true });
      });
      el.querySelectorAll("th[data-col] .lc-dg-grip").forEach(function (g) {
        g.addEventListener("click", function (e) { e.stopPropagation(); });
        g.addEventListener("pointerdown", function (e) {
          e.preventDefault(); e.stopPropagation();
          var th = g.parentNode, c = th.getAttribute("data-col"), x0 = e.clientX, w0 = th.getBoundingClientRect().width;
          try { g.setPointerCapture(e.pointerId); } catch (x) {}
          var move = function (ev) {
            var w = Math.max(40, Math.round(w0 + ev.clientX - x0));
            colW[c] = w; th.style.width = w + "px"; th.style.minWidth = w + "px";
          };
          var up = function () { g.removeEventListener("pointermove", move); g.removeEventListener("pointerup", up); g.removeEventListener("pointercancel", up); };
          g.addEventListener("pointermove", move);
          g.addEventListener("pointerup", up);
          g.addEventListener("pointercancel", up);
        });
      });
      el.querySelectorAll("th[data-col]").forEach(function (th) {
        th.addEventListener("click", function () {
          var col = th.getAttribute("data-col");
          sortAsc = sortCol === col ? !sortAsc : true;
          sortCol = col; page = 0; render(window.lcDatasets[bindId] || data);
        });
      });
      el.querySelectorAll("[data-pg]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          /* A NEW PAGE SELECTS ITS FIRST ROW, AND SAYS SO (Michel, 2026-10-10:
             "when the grid goes to the next page and the first line gets
             selected, any detail form should follow"): the selection is
             dropped and the first-row rule below picks and publishes again. */
          page = +btn.getAttribute("data-pg");
          selKey = null; publishedFirst = false;
          render(window.lcDatasets[bindId] || data);
        });
      });
      if (urlCol) {
        el.querySelectorAll("tr[data-url]").forEach(function (tr) {
          var u = tr.getAttribute("data-url");
          if (u) tr.addEventListener("click", function () { window.open(u, "_blank", "noopener"); });
        });
      } else {
        /* every bound grid: clicking a row selects it (visual highlight). If the
           grid has an id it also publishes, so bound-to charts and bound forms
           can hang off it (dataset → grid → detail). */
        var trs = el.querySelectorAll("tbody tr");
        function keyOf(r) { return r && r.obj != null ? "o:" + r.obj : null; }
        trs.forEach(function (tr, i) {
          tr.addEventListener("click", function () {
            trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            tr.classList.add("lc-dg-selected");
            selKey = keyOf(slice[i]) || "i:" + i;
            if (lcId) window.lcMasterDetail.publish(lcId, slice[i] || null);
          });
        });
        /* THE GUIDE'S HANDS. A grid bound to a dataset is drawn by this
           light table, not by AG — so the select verb, which only knew the
           AG api, moved nothing here: on 410 module_01 Doc said "there is
           our winner: one row" over a table where nothing was ever picked
           (Michel, 2026-08-30, reading the quiz that claimed otherwise).
           Selection belongs to whoever draws the rows, so this table hands
           the verb its own door instead of letting anyone guess from
           outside. Same effect as a finger, minus a link row's navigation. */
        el._lcSelectRow = function (text) {
          var t = String(text == null ? "" : text).toLowerCase();
          for (var i = 0; i < trs.length; i++) {
            if (trs[i].textContent.toLowerCase().indexOf(t) < 0) continue;
            trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            trs[i].classList.add("lc-dg-selected");
            selKey = keyOf(slice[i]) || "i:" + i;
            if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, slice[i] || null);
            try { trs[i].scrollIntoView({ block: "nearest" }); } catch (e) {}
            return trs[i];
          }
          return null;
        };
        /* A BUTTON'S HANDS (Michel, 2026-10-09, Module 05: "currentline.met
           = today's weekday, and select the next line"). current() is the
           selected row; set() writes one field into the DATASET this table
           shows — through a query, to the base row with the same values —
           and republishes it, so the query re-runs, this table repaints and
           every cell recounts, all in the same tick; next() selects the row
           after the one just written, or the row that slid into its place
           when the write took it out of the answer. */
        function curIndex() {
          if (!selKey) return 0;
          if (selKey.indexOf("i:") === 0) return parseInt(selKey.slice(2), 10) || 0;
          for (var i = 0; i < slice.length; i++) if (keyOf(slice[i]) === selKey) return i;
          return 0;
        }
        function sameRow(a, b) {
          if (!a || !b) return false;
          for (var k in a) if (Object.prototype.hasOwnProperty.call(b, k) && String(b[k]) !== String(a[k])) return false;
          return true;
        }
        function pick(i) {
          trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
          if (trs[i]) trs[i].classList.add("lc-dg-selected");
          selKey = keyOf(slice[i]) || "i:" + i;
          if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, slice[i] || null);
          return slice[i] || null;
        }
        el._lcRow = {
          current: function () { return slice[curIndex()] || null; },
          set: function (field, value) {
            var cur = slice[curIndex()];
            if (!cur) return false;
            var baseId = bindId, target = cur;
            var q = document.querySelector(".lc-query[data-lc-id='" + bindId + "']");
            if (q) {
              baseId = (q.getAttribute("data-bind") || "").split(",")[0].trim();
              target = null;
              (window.lcDatasets[baseId] || []).forEach(function (b) { if (!target && sameRow(cur, b)) target = b; });
            }
            if (!target || !window.lcDatasets[baseId]) return false;
            touched = {};
            for (var k in cur) touched[k] = cur[k];
            touched[field] = value;
            target[field] = value;
            window.lcSetDataset(baseId, window.lcDatasets[baseId]);
            return true;
          },
          next: function () {
            var k = curIndex();
            if (touched) {
              var j = -1;
              for (var i = 0; i < slice.length && j < 0; i++) if (sameRow(touched, slice[i])) j = i;
              k = j >= 0 ? j + 1 : k;
              touched = null;
            } else k = k + 1;
            if (k >= slice.length) return null;
            return pick(k);
          }
        };
        /* ➕ New just made one: it is the row nobody had before — select it,
           show it, and the bound card follows */
        if (pendingNew) {
          for (var ni = 0; ni < slice.length; ni++) {
            if (slice[ni].obj != null && !pendingNew[String(slice[ni].obj)]) {
              pendingNew = null;
              selKey = keyOf(slice[ni]);
              lastPubJson = JSON.stringify(slice[ni]);
              publishedFirst = true;
              trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
              if (trs[ni]) { trs[ni].classList.add("lc-dg-selected"); try { trs[ni].scrollIntoView({ block: "nearest" }); } catch (e) {} }
              if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, slice[ni]);
              typeNew = { key: selKey, until: Date.now() + 1500 };
              break;
            }
          }
        }
        /* ➕ New leaves the caret in the new row's first cell, ready to type
           (Michel, 2026-10-16) — again after the repaints that follow it */
        if (typeNew && Date.now() < typeNew.until) {
          for (var ti = 0; ti < slice.length; ti++) {
            if (keyOf(slice[ti]) !== typeNew.key || !trs[ti]) continue;
            var first = trs[ti].querySelector("td.lc-dg-typed");
            if (first && !first.isContentEditable) first.dispatchEvent(new MouseEvent("dblclick", { bubbles: true }));
            break;
          }
        } else typeNew = null;
        /* the selection survives a republish: a model's verb repaints the
           whole table, and the row you were on must stay lit (Michel,
           2026-08-22: "the datagrid does not show the selected row") */
        if (selKey) {
          var stillThere = false;
          slice.forEach(function (r, i) {
            if ((keyOf(r) || "i:" + i) === selKey && trs[i]) {
              stillThere = true;
              trs[i].classList.add("lc-dg-selected");
              /* a verb moved the object and the table repainted: the bound
                 form must show the row as it is now, not as it was clicked.
                 Only when the row CHANGED — a follower that republishes the
                 class on every selection (classroom 4's inspector) would
                 otherwise chase this repaint forever (2026-10-16). */
              if (model && lcId && window.lcMasterDetail) {
                var pj = JSON.stringify(r);
                if (pj !== lastPubJson) { lastPubJson = pj; window.lcMasterDetail.publish(lcId, r); }
              }
            }
          });
          /* the selected row is gone (deleted): the first row takes the
             selection and the bound card follows, never a ghost */
          if (!stillThere) { selKey = null; publishedFirst = false; lastPubJson = null; }
        }
        /* a master with data selects its first row at once, like the AG
           road — a bound form should never sit empty waiting for a click */
        if (!publishedFirst && slice.length) {
          publishedFirst = true;
          if (!selKey) {
            selKey = keyOf(slice[0]) || "i:0";
            if (trs[0]) trs[0].classList.add("lc-dg-selected");
          }
          var firstRow = slice[curIndex()] || slice[0];   /* the lit row, which is not always the first */
          lastPubJson = JSON.stringify(firstRow);
          if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, firstRow);
        }
        /* never a grid with rows and nothing lit (Michel, 2026-10-16: "a
           line should always be selected, after a refresh, on opening") */
        if (slice.length && !el.querySelector("tbody tr.lc-dg-selected") && trs[curIndex()])
          trs[curIndex()].classList.add("lc-dg-selected");
      }
    }

    /* repo-file source: fetch once and render (no dataset listener) */
    if (fileRef) {
      bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
      var useCdn = window.lcUseCdn ? window.lcUseCdn() : false;
      var srcs = window.lcFileSrc(fileRef);
      fetch(useCdn ? srcs.cdn : srcs.raw)
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + fileRef); return r.text(); })
        .then(function (text) { return window.lcParseDataText(text, fileFmt); })
        .then(function (data) { render(Array.isArray(data) ? data : [data]); })
        .catch(function (e) { bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em'>⚠ " + e.message + "</p>"; });
      return;
    }

    /* register as persistent listener so auto-refresh re-renders */
    window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || [];
    render._lcEl = el;
    window.lcDatasetListeners[bindId].push(render);

    if (window.lcDatasets[bindId]) render(window.lcDatasets[bindId]);
    else {
      bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
      /* a source that is merely slow arrives inside the grace; one that will
         never arrive — a name that matches nothing, a query still waiting
         for ITS source — stops pretending to load and says what the author
         wrote for the case. Same knob as the datagrid and the chart. A late
         arrival still renders straight over this through the listener. */
      var grace = window.lcDatagridBindGrace;
      if (grace == null) grace = 4000;
      setTimeout(function () {
        if (window.lcDatasets[bindId] === undefined)
          bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>"
            + (emptyMsg || "Nothing arrives here yet.") + "</p>";
      }, grace);
    }
  }

  /* NOTE: .button upgrade (incl. optional Python on_click handler) lives in
     pyrun.md's upgradeButton — it owns p.button. Keeping the .lc-button CSS
     above; no upgrader here. */

  /* ── boot ─────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry.
     Datasets register before grids so data is available when grids read
     it; the .chart variants live in chart.md. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".database", upgradeDatabase);
    window.lcRegisterUpgrader(".dataset", upgradeDataset);
    window.lcRegisterUpgrader(".datagrid", upgradeDatagridBound);
  }

})();
</script>
