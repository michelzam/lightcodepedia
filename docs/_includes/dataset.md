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
   rows — the state cell wears a chip, the gutter ⋯ drops the row's verbs,
   legal ones live and the others grey; typed cells; ➕ New under the list. */
.lc-datagrid { position: relative; }
.lc-dg-table td.lc-dg-typed { border-bottom: 1px dashed #9db6d0; }
.lc-dg-table td.lc-dg-typed:focus { outline: 2px solid #0066cc; outline-offset: -2px; background: #fff; }
.lc-dg-table td.lc-dg-state { white-space: nowrap; }
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
/* live tables: the line's mark, always shown — green holds, grey is down (Michel, 2026-10-20) */
.lc-dg-cbtn.lc-dg-live { border: 0; background: transparent; cursor: default; font-size: .8em; }
.lc-dg-cbtn.lc-dg-live.lc-dg-live-on { color: #16a34a; }
.lc-dg-cbtn.lc-dg-live.lc-dg-live-off { color: #9ca3af; }
.lc-dg-cbtn.lc-dg-st-dirty { color: #b45309; border-color: #fcd34d; }
.lc-dg-cbtn.lc-dg-st-saving { color: #0066cc; }
.lc-dg-cbtn.lc-dg-st-saving span { display: inline-block; animation: lc-dg-spin 1s linear infinite; }
.lc-dg-cbtn.lc-dg-st-error { color: #b91c1c; border-color: #fca5a5; background: #fef2f2; }
@keyframes lc-dg-spin { to { transform: rotate(360deg); } }
.lc-datagrid.lc-dg-cornered:not(.lc-dg-titled) .lc-dg-body, .lc-datagrid.lc-dg-cornered:not(.lc-dg-titled) > .lc-dg-scroll,
.lc-datagrid.lc-dg-cornered:not(.lc-dg-titled) > table { margin-top: 2.1em; }
.lc-dg-table td.lc-dg-typed.lc-dg-typing { background: #fff; outline: 2px solid #0066cc; outline-offset: -2px; cursor: text; }
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
.lc-dg-unl textarea.lc-dg-unl-sql { flex: 1 1 100%; font: .8em ui-monospace, SFMono-Regular, Menlo, monospace; border: 1px solid #c7d2e0; border-radius: 6px; padding: .4em; }
.lc-dg-unl code { user-select: all; }
.lc-dg-unl input { font: inherit; padding: .2em .4em; border: 1px solid #cbd5e1; border-radius: 4px; min-width: 12em; }
.lc-dg-unl-me { background: none; border: 0; color: #2563eb; cursor: pointer; font: inherit; padding: 0; text-decoration: underline; }
.lc-dg-unl-note { color: #64748b; }
.lc-dg-struct { color: #b45309 !important; opacity: 1 !important; }
.lc-dg-struct b, .lc-dg-tidy b { font-size: .7em; margin-left: 1px; }
.lc-struct-btn.lc-struct-tidyonly { background: #e2e8f0; color: #334155; }
.lc-struct-btn.lc-struct-idle { background: transparent; color: #94a3b8; padding: .1em .4em; }
.lc-struct-btn.lc-struct-idle:hover { color: #f8fafc; }
.lc-struct-panel .lc-struct-tidy { list-style: none; margin-left: 0; }
.lc-struct-btn { margin-left: auto; border: 0; border-radius: 999px; padding: .15em .7em; font: inherit; font-size: .85em; cursor: pointer; background: #fef3c7; color: #92400e; }
.lc-struct-btn.lc-struct-many { background: #fde68a; }
.lc-struct-panel { position: fixed; z-index: 1000; left: 50%; top: 18%; transform: translateX(-50%); width: min(440px, calc(100vw - 32px)); max-height: 70vh; overflow: auto;
  background: #fff; color: #1e293b; border: 1px solid #cbd5e1; border-radius: 12px; box-shadow: 0 18px 50px rgba(15,23,42,.25); padding: 1em 1.2em; font-size: .95em; }
.lc-struct-panel h4 { margin: 0 0 .6em; }
.lc-struct-panel ol, .lc-struct-panel ul { margin: .2em 0 .8em 1.2em; padding: 0; }
.lc-struct-nudge { color: #92400e; }
.lc-struct-note { color: #475569; font-size: .9em; }
.lc-struct-btns { display: flex; gap: .6em; justify-content: flex-end; }
.lc-struct-btns button { border-radius: 8px; padding: .4em .9em; font: inherit; cursor: pointer; border: 1px solid #cbd5e1; background: #fff; }
.lc-struct-btns .lc-struct-apply { background: #0066cc; border-color: #0066cc; color: #fff; }
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
  /* ONE PICKLIST (Michel, 2026-10-18: "in the form, the picklist for dogs
     is the old style"): the grid's reference cells and the form's use the
     same roomy list — a — to clear, a 🔍 when long, the current one marked */
  window.lcPickMenu = function (anchor, items, onPick, onClose) {
    var open = document.querySelector(".lc-dg-refmenu");
    if (open) { var same = open._lcFor === anchor; open._lcClose(); if (same) return; }
    var esc2 = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var menu = document.createElement("div");
    menu.className = "lc-dg-menu lc-dg-refmenu";
    menu._lcFor = anchor;
    menu.setAttribute("role", "listbox");
    menu.innerHTML = (items.length > 8 ? "<input class='lc-dg-refsearch' type='search' placeholder='🔍 find' aria-label='find'>" : "")
      + "<button type='button' class='lc-dg-verb' data-obj=''><span>—</span></button>"
      + items.map(function (it) {
          return "<button type='button' class='lc-dg-verb" + (it.cur ? " lc-dg-cur" : "") + "' role='option' data-obj='" + esc2(it.v) + "'>"
            + "<span>" + esc2(it.label) + "</span></button>";
        }).join("");
    var rc = anchor.getBoundingClientRect();
    menu.style.minWidth = Math.max(rc.width, 180) + "px";
    menu.style.left = (Math.max(4, Math.min(rc.left, window.innerWidth - Math.max(rc.width, 180) - 8)) + window.scrollX) + "px";
    menu.style.top = (rc.bottom + window.scrollY) + "px";
    var closed = false;
    menu._lcClose = function () {
      if (closed) return; closed = true;
      if (menu.parentNode) menu.parentNode.removeChild(menu);
      document.removeEventListener("click", outside, true);
      if (onClose) onClose();
    };
    var outside = function (e) { if (!menu.contains(e.target)) menu._lcClose(); };
    document.body.appendChild(menu);
    var find = menu.querySelector(".lc-dg-refsearch");
    if (find) {
      find.addEventListener("input", function () {
        var q = find.value.toLowerCase();
        menu.querySelectorAll("button[data-obj]").forEach(function (b) { b.hidden = q && b.textContent.toLowerCase().indexOf(q) < 0; });
      });
      find.focus();
    }
    menu.querySelectorAll("button[data-obj]").forEach(function (b) {
      b.addEventListener("click", function (ev) {
        ev.stopPropagation();
        var v = b.getAttribute("data-obj");
        menu._lcClose();
        onPick(v);
      });
    });
    setTimeout(function () { document.addEventListener("click", outside, true); }, 0);
    return menu;
  };
  /* ONE DOOR for New, an edit and a verb: the page's runtime — or, when the
     class came through a link (lc://), the channel to the page that owns it
     (Michel, 2026-10-20). The grid and the form never knew the difference. */
  window.lcModelOp = function (cls, op, code) {
    var m = (window.lcModels || {})[cls], ops = m && m.remote && (window.lcRemoteOps || {})[m.remote.prefix];
    if (ops) { op.cls = m.remote.cls; ops.send(op); return; }
    if (window.lcPySend) window.lcPySend(code);
  };
  window.lcGridSay = function (cls, msg) {
    /* …and under a grid of its base class (a Sprint in the walks), and under
       a form showing one (Michel, 2026-10-18: "when I click run in the form,
       there is no error message!") */
    var at = [].slice.call(document.querySelectorAll(".lc-datagrid[data-bind], [data-lc-say]")).filter(function (g) {
      var b = g.getAttribute("data-lc-say") || g.getAttribute("data-bind"), m = (window.lcModels || {})[b];
      return b === cls || !!(m && (m.subs || []).indexOf(cls) >= 0);
    });
    at.forEach(function (g) {
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
        if (!U || !U.rpc || !lsGet(U.akey) || ST.frozen(id)) return;   /* a changed structure waits for 🔄 */
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
  /* A STRUCTURE CHANGE FREEZES, THE OWNER RECONCILES (Michel, 2026-10-18,
     after a Sprint(Walk2) typed for two seconds emptied the walk table:
     "data structure changes should freeze the data refresh… and wait for
     the explicit refresh with reconciliation… trace the intermediate
     changes one by one… encourage small changes"). Each database table
     keeps the structure its classes had when it was last read (the base);
     every settled difference since is a step in a log; while the code
     differs from the base the table neither saves nor reads, and the app's
     title says 🔄 N. Back to the base: the freeze lifts by itself. */
  var ST = window.lcStruct = window.lcStruct || { types: {}, seen: {}, log: {}, settle: {} };
  function stColsOf(id) {
    var M = window.lcModels || {}, cols = {}, subs = [];
    (unlCols(id) || []).forEach(function (c) { cols[c.n] = { t: c.t, was: c.was || "" }; });
    Object.keys(M).forEach(function (n) { var m = M[n]; if (m && m.src === id) (m.subs || []).forEach(function (k) { if (subs.indexOf(k) < 0) subs.push(k); }); });
    subs.sort();
    return { cols: cols, subs: subs };
  }
  function stSig(x) {
    return JSON.stringify([Object.keys(x.cols).sort().map(function (k) { return k + ":" + x.cols[k].t + ":" + x.cols[k].was; }), x.subs]);
  }
  function stDiff(a, b) {
    var out = [];
    Object.keys(b.cols).forEach(function (k) {
      var c = b.cols[k], o = a.cols[k];
      if (k === "_sub") { if (!o) out.push("🏷 the rows will say which subclass they are"); return; }
      if (!o && c.was && a.cols[c.was]) out.push("🔁 " + c.was + " → " + k + " (renamed, its data kept)");
      else if (!o) out.push("➕ " + k + " (" + c.t + ")");
      else if (o.t !== c.t) out.push("✏️ " + k + ": " + o.t + " → " + c.t);
    });
    Object.keys(a.cols).forEach(function (k) {
      if (b.cols[k] || k === "_sub") return;
      if (!Object.keys(b.cols).some(function (n) { return b.cols[n].was === k; })) out.push("➖ " + k + " (its column and data stay)");
    });
    b.subs.forEach(function (k) { if (a.subs.indexOf(k) < 0) out.push("➕ class " + k); });
    a.subs.forEach(function (k) { if (b.subs.indexOf(k) < 0) out.push("➖ class " + k + " (its rows stay)"); });
    return out;
  }
  /* TIME TRAVEL COMPARES NOTHING (Michel, 2026-10-18: "in timetravel,
     since the editor is in R/O, that feature should be deactivated… we only
     have 1 current updatable version: the topmost"): while a pad replays an
     old version, no plan, no leftovers, no log — the database is not
     versioned (yet: parked, Michel's Postgres recipe) */
  ST.travelling = function () { return !!document.querySelector(".lc-mdpad[data-lc-replay]"); };
  /* what the table lacks for the code as it stands: the plan 🔄 applies */
  ST.plan = function (id) {
    var r = window.lcRemote[id], U = r && r.unl;
    if (!U || !U.read || !U.tcols || ST.travelling()) return [];
    var cur = stColsOf(id), tc = U.tcols, ty = ST.types[id] || {}, out = [];
    Object.keys(cur.cols).forEach(function (k) {
      var c = cur.cols[k];
      if (tc[k]) { if (ty[k] && ty[k] !== c.t) out.push({ k: "retype", n: k, t: c.t, from: ty[k], say: "✏️ " + k + ": " + ty[k] + " → " + c.t }); return; }
      if (k === "_sub") { out.push({ k: "add", n: k, say: "🏷 a column that says which subclass each row is" }); return; }
      if (c.was && tc[c.was]) out.push({ k: "rename", n: k, from: c.was, say: "🔁 " + c.was + " → " + k + " (its data kept)" });
      else out.push({ k: "add", n: k, t: c.t, say: "➕ " + k + " (" + c.t + ")" });
    });
    return out;
  };
  ST.frozen = function (id) { return ST.plan(id).length > 0; };
  /* 🧹 IN THE SAME PANEL (Michel, 2026-10-18): on the owner's device, the
     columns no class on the page declares and the class names no class
     (nor a was=) answers to — offered unticked, never by themselves */
  ST.tidy = function (id) {
    var r = window.lcRemote[id], U = r && r.unl, out = { orphans: [], stale: [] };
    if (!U || !U.read || !lsGet(U.akey) || ST.travelling()) return out;
    var rows = window.lcDatasets[id] || [], row0 = rows[0] || {}, M = window.lcModels || {}, declared = {};
    (unlCols(id) || []).forEach(function (c) { declared[c.n] = 1; });
    out.orphans = Object.keys(row0).filter(function (k) {
      return k !== "id" && k !== "obj" && k.charAt(0) !== "_" && k !== "⚠️" && !declared[k] && !lcDeclaredAnywhere(k);
    });
    var wases = Object.keys(M).map(function (n) { return M[n] && M[n].was; }).filter(Boolean);
    rows.forEach(function (x) {
      var k = x && x._sub;
      if (k && !M[k] && wases.indexOf(k) < 0 && out.stale.indexOf(k) < 0) out.stale.push(k);
    });
    return out;
  };
  ST.tidyCount = function (id) { var t = ST.tidy(id); return t.orphans.length + t.stale.length; };
  /* the table is as the code says (a read after 🔄, or a first read that
     needed nothing): the types it now has, and a clean log */
  ST.settled = function (id) {
    var cur = stColsOf(id), ty = {};
    Object.keys(cur.cols).forEach(function (k) { ty[k] = cur.cols[k].t; });
    var U = (window.lcRemote[id] || {}).unl;
    if (!ST.types[id] || !ST.plan(id).length) ST.types[id] = ty;
    ST.seen[id] = cur; ST.log[id] = [];
    ST.settle[id] = performance.now();
    document.dispatchEvent(new CustomEvent("lc-struct", { detail: id }));
  };
  ST.check = function () {
    Object.keys(window.lcRemote || {}).forEach(function (id) {
      var r = window.lcRemote[id];
      if (!r || !r.unl || !ST.seen[id]) return;
      var cur = stColsOf(id);
      if (stSig(cur) === stSig(ST.seen[id])) return;
      /* the page's classes still arriving (a pad's after the page's), or an
         old version replayed: no step */
      var quiet = performance.now() - (ST.settle[id] || 0) < 4000 || ST.travelling();
      if (!quiet) stDiff(ST.seen[id], cur).forEach(function (t) { ST.log[id].push(t); });
      ST.seen[id] = cur;
      if (!ST.plan(id).length) ST.log[id] = [];      /* the code and the table agree again */
      document.dispatchEvent(new CustomEvent("lc-struct", { detail: id }));
      if (window.lcSetDataset) window.lcSetDataset(id, window.lcDatasets[id] || []);   /* the grids repaint their state */
    });
  };
  /* the review: what you changed, step by step; what 🔄 does to the table;
     the owner applies, anyone else is told to undo */
  window.lcStructPanel = function (id) {
    var old = document.querySelector(".lc-struct-panel");
    if (old) old.parentNode.removeChild(old);
    var r = window.lcRemote[id], U = r && r.unl, plan = ST.plan(id), log = ST.log[id] || [], tidy = ST.tidy(id);
    var owner = !!(U && lsGet(U.akey));
    var M = window.lcModels || {}, base = Object.keys(M).filter(function (n) { return M[n].src === id && (M[n].subs || []).length; })[0]
      || Object.keys(M).filter(function (n) { return M[n].src === id; })[0] || id;
    var e = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
    var box = document.createElement("div");
    box.className = "lc-struct-panel";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", "the table and your code");
    var leftovers = tidy.orphans.map(function (c) {
        return "<li><label><input type='checkbox' data-drop='" + e(c) + "'> drop the column <code>" + e(c) + "</code>, no class uses it (its data is lost)</label></li>"; })
      .concat(tidy.stale.map(function (k) {
        return "<li><label><input type='checkbox' data-clear='" + e(k) + "'> clear the old class name <code>" + e(k) + "</code> (those rows become " + e(base) + ")</label></li>"; }));
    box.innerHTML = "<h4>" + (plan.length ? "🔄" : "🧹") + " The table <code>" + e(U ? U.tbl : id) + "</code> and your code</h4>"
      + (log.length ? "<p>What you changed, step by step:</p><ol class='lc-struct-log'>" + log.map(function (t) { return "<li>" + e(t) + "</li>"; }).join("") + "</ol>" : "")
      + (plan.length ? "<p>What the table needs now:</p><ul class='lc-struct-plan'>" + plan.map(function (x) { return "<li>" + e(x.say) + "</li>"; }).join("") + "</ul>"
                     : "<p class='lc-struct-agree'>The table has what your code declares. Changed the database itself? Reconcile: the table is checked against the code again, then read.</p>")
      + (log.length > 3 ? "<p class='lc-struct-nudge'>Many steps at once. Small steps, applied one by one, keep the data easy to follow.</p>" : "")
      + (owner && leftovers.length ? "<p>Leftovers, only if you tick them:</p><ul class='lc-struct-tidy'>" + leftovers.join("") + "</ul>" : "")
      + (owner ? (plan.length ? "<p class='lc-struct-note'>Rows wait meanwhile: nothing is saved or read until the table matches.</p>" : "")
               : "<p class='lc-struct-note'>Only the database's owner changes its structure. Undo these changes in your code and your rows save again.</p>")
      + "<div class='lc-struct-btns'>" + (owner ? "<button type='button' class='lc-struct-apply'>" + (plan.length ? "Apply to the table" : "Reconcile with the table") + "</button>" : "")
      + "<button type='button' class='lc-struct-later'>" + (owner ? "Not yet" : "Close") + "</button></div>";
    document.body.appendChild(box);
    var close = function () { if (box.parentNode) box.parentNode.removeChild(box); };
    box.querySelector(".lc-struct-later").addEventListener("click", close);
    var ap = box.querySelector(".lc-struct-apply");
    var ticks = function (a) { return [].slice.call(box.querySelectorAll("input[" + a + "]:checked")).map(function (x) { return x.getAttribute(a); }); };
    var arm = function () {
      if (!ap) return;
      var t = ticks("data-drop").length + ticks("data-clear").length;
      ap.textContent = plan.length || t ? "Apply to the table" : "Reconcile with the table";
    };
    box.querySelectorAll("input[type=checkbox]").forEach(function (x) { x.addEventListener("change", arm); });
    arm();
    if (ap) ap.addEventListener("click", function () {
      var drop = ticks("data-drop"), clear = ticks("data-clear");
      ap.disabled = true; ap.textContent = "Applying…";
      var author = lsGet(U.akey);
      /* the structure first, then the leftovers ticked, then the rows that waited */
      var go = U.rpc("lc_ensure", { token: author, tbl: U.tbl, cols: unlCols(id) || [] }).then(function () {
            (unlCols(id) || []).forEach(function (c) { U.tcols[c.n] = 1; (ST.types[id] = ST.types[id] || {})[c.n] = c.t; });
          });
      go.then(function () { return drop.length ? U.rpc("lc_drop", { token: author, tbl: U.tbl, cols: drop }) : null; })
        .then(function () {
          var rows = (window.lcDatasets[id] || []).filter(function (x) { return x && x.id != null && clear.indexOf(x._sub) >= 0; })
            .map(function (x) { return { id: x.id, _sub: null }; });
          return rows.length ? U.rpc("lc_save", { share: U.share, tbl: U.tbl, ins: [], upd: rows, del: [] }) : null;
        })
        .then(function () { drop.forEach(function (c) { delete U.tcols[c]; }); return r.pull({ ensure: true, keep: true }); })
        .then(function () {
          close();
          if (ST.frozen(id) && window.lcGridSay) window.lcGridSay(base, "⚠️ the table did not take every change: " + ST.plan(id).map(function (x) { return x.n; }).join(", "));
        })
        .catch(function (err) { ap.disabled = false; ap.textContent = "Apply to the table"; if (window.lcGridSay) window.lcGridSay(base, "⚠️ " + err.message); });
    });
    return box;
  };
  /* THE APP'S TITLE SAYS IT (Michel, 2026-10-18: "a button in the app's
     title to reconcile"): 🔄 N over every table its grids show */
  function stPaintHeads() {
    document.querySelectorAll(".lc-mdpad-app").forEach(function (app) {
      var head = app.querySelector(".lc-mdpad-apphead");
      if (!head) return;
      var ids = [];
      app.querySelectorAll(".lc-datagrid[data-bind]").forEach(function (g) {
        var m = (window.lcModels || {})[g.getAttribute("data-bind")], sid = m && m.src;
        if (sid && ids.indexOf(sid) < 0 && window.lcRemote[sid] && window.lcRemote[sid].unl) ids.push(sid);
      });
      var hot = ids.filter(function (sid) { return ST.frozen(sid); });
      var n = hot.reduce(function (a, sid) { return a + ST.plan(sid).length; }, 0);
      var tidyIds = ids.filter(function (sid) { return ST.tidyCount(sid) > 0; });
      var m = tidyIds.reduce(function (a, sid) { return a + ST.tidyCount(sid); }, 0);
      var btn = head.querySelector(".lc-struct-btn");
      /* the owner always has it (Michel, 2026-10-18: "always available,
         including when I changed the db directly") — faint when all agrees */
      var mine = ST.travelling() ? [] : ids.filter(function (sid) { var U2 = window.lcRemote[sid].unl; return U2 && U2.read && lsGet(U2.akey); });
      if (!n && !m && !mine.length) { if (btn) btn.parentNode.removeChild(btn); return; }
      if (!btn) {
        btn = document.createElement("button");
        btn.type = "button"; btn.className = "lc-struct-btn";
        head.appendChild(btn);
        btn.addEventListener("click", function (ev) { ev.stopPropagation(); window.lcStructPanel(btn._lcId); });
      }
      btn._lcId = n ? hot[0] : m ? tidyIds[0] : mine[0];
      btn.classList.toggle("lc-struct-idle", !n && !m);
      var steps = hot.reduce(function (a, sid) { return a + (ST.log[sid] || []).length; }, 0);
      btn.classList.toggle("lc-struct-many", steps > 3);
      btn.classList.toggle("lc-struct-tidyonly", !n);
      btn.textContent = n ? "🔄 " + n + (n > 1 ? " changes" : " change") : m ? "🧹 " + m + " to tidy" : "🔄";
      btn.title = n ? "the code changed a table's structure — review and apply" : m ? "leftovers in a table — review, tick what goes"
        : "the table and the code agree — reconcile anyway (after a change made in the database itself)";
      btn.setAttribute("aria-label", btn.title);
    });
  }
  document.addEventListener("lc-struct", stPaintHeads);
  /* into an old version and back: the corners and the title repaint; coming
     back to the topmost version is not a change of yours */
  document.addEventListener("lc-travel", function () {
    setTimeout(function () {
      Object.keys(window.lcRemote || {}).forEach(function (id) {
        var r = window.lcRemote[id];
        if (!r || !r.unl) return;
        /* the pad redraws the topmost code after this: a quiet moment, no step */
        if (!ST.travelling() && ST.seen[id]) { ST.seen[id] = stColsOf(id); ST.settle[id] = performance.now(); }
        if (window.lcSetDataset && window.lcDatasets[id]) window.lcSetDataset(id, window.lcDatasets[id]);
      });
      stPaintHeads();
    }, 0);
  });
  document.addEventListener("lc-remote-state", stPaintHeads);
  if (!window._lcStructWired) {
    window._lcStructWired = 1;
    var stT = null;
    /* a step is what the code says once typing pauses — not every letter */
    document.addEventListener("lc-model-changed", function () { clearTimeout(stT); stT = setTimeout(ST.check, 1200); });
  }
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
                               unlisted: el.getAttribute("unlisted") || "", title: a ? (a.textContent || "").trim() : id,
                               live: el.getAttribute("live") === "true" };
    /* the line changed its mind (live on, live off): the socket follows —
       on, the tables already read start listening now, not at the next ↻
       (Michel, 2026-10-21: "if I add a live="true", there is no instant
       activation. why?") */
    if (!window.lcDatabases[id].live && window._lcLive && window._lcLive[id]) window._lcLive[id].stop();
    if (window.lcDatabases[id].live) Object.keys(window.lcRemote || {}).forEach(function (dsid) {
      var r = window.lcRemote[dsid], u = r && r.unl;
      if (u && u.db === id && u.share) liveFollow(u, dsid, u.base, u.key, u.share);
    });
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
  /* LIVE TABLES (Michel, 2026-10-20: "live is the table's business, no server
     or client line; live="true" on the database line, default off; the
     trigger always on"). One socket per database line, to the platform's
     realtime door, joined to the topic the setup SQL broadcasts on — "lc-"
     and the unlisted name, the name is the secret. A change arriving names
     its table: every list of that table reads itself again, through the
     same door ↻ uses, so the rows, the counts and the forms follow with no
     second code path. Nothing is applied while a version replays, while a
     structure change waits for 🔄, or while a cell is open: it comes a beat
     later. The socket dropped says so in the grid's corner and under it,
     the broken-wire style; back, every table of the line is read again. */
  window._lcLive = window._lcLive || {};
  function liveFollow(U, dsId, base, key, share) {
    var dbId = U.db, d = window.lcDatabases[dbId];
    if (!dbId || !d || !d.live || !share) return;
    var L = window._lcLive[dbId];
    if (L && (L.share !== share || L.base !== base)) { L.stop(); L = null; }
    if (!L) {
      L = window._lcLive[dbId] = { share: share, base: base, key: key, lists: {}, on: false, ws: null, tries: 0, stopped: false, ref: 0 };
      L.say = function (on) {
        if (L.on === on) return;
        L.on = on;
        Object.keys(L.lists).forEach(function (id) { document.dispatchEvent(new CustomEvent("lc-remote-state", { detail: id })); });
      };
      L.stop = function () {
        L.stopped = true; clearInterval(L.beat); clearTimeout(L.again);
        try { if (L.ws) L.ws.close(); } catch (e) {}
        L.ws = null; L.say(false); delete window._lcLive[dbId];
      };
      L.reread = function (table) {
        Object.keys(L.lists).forEach(function (id) {
          var r = window.lcRemote[id];
          if (!r || !r.unl || (table && r.unl.tbl !== table)) return;
          (function later(n) {
            if (ST.travelling() || ST.frozen(id)) return;            /* the next ↻ or 🔄 reads it */
            var busy = document.querySelector(".lc-datagrid .lc-dg-typing, .lc-form .lc-dg-typing");
            if (busy && n > 0) { setTimeout(function () { later(n - 1); }, 1500); return; }
            r.pull();
          })(20);
        });
      };
      L.open = function () {
        if (L.stopped || L.ws) return;
        var host = base.replace(/^https:/, "wss:").split("/rest/v1")[0];
        var ws;
        try { ws = new WebSocket(host + "/realtime/v1/websocket?apikey=" + encodeURIComponent(key) + "&vsn=1.0.0"); }
        catch (e) { L.again = setTimeout(L.open, 5000); return; }
        L.ws = ws;
        var topic = "realtime:lc-" + share;
        var send = function (t, ev, payload) { try { ws.send(JSON.stringify({ topic: t, event: ev, payload: payload || {}, ref: String(++L.ref) })); } catch (e) {} };
        ws.onopen = function () {
          send(topic, "phx_join", { config: { broadcast: { self: false }, presence: { key: "" }, postgres_changes: [], private: false } });
          clearInterval(L.beat);
          L.beat = setInterval(function () { send("phoenix", "heartbeat", {}); }, 30000);
        };
        ws.onmessage = function (m) {
          var f; try { f = JSON.parse(m.data); } catch (e) { return; }
          if (f.event === "phx_reply" && f.topic === topic) {
            var okJoin = f.payload && f.payload.status === "ok";
            if (okJoin) { var back = L.tries > 0; L.tries = 0; L.say(true); if (back) L.reread(); }
            return;
          }
          if (f.event === "broadcast" && f.topic === topic) {
            var p = f.payload && f.payload.payload;
            if (!p || !p.table) return;
            document.dispatchEvent(new CustomEvent("lc-live", { detail: { db: dbId, table: p.table, op: p.op, id: p.id } }));
            clearTimeout(L.soon);
            L.soon = setTimeout(function () { L.reread(p.table); }, 250);
          }
        };
        ws.onclose = ws.onerror = function () {
          if (L.ws !== ws) return;
          L.ws = null; clearInterval(L.beat); L.say(false);
          if (L.stopped) return;
          L.tries++;
          L.again = setTimeout(L.open, Math.min(30000, 1000 * Math.pow(2, Math.min(L.tries, 5))));
        };
      };
      L.open();
    }
    L.lists[dsId] = 1;
  }
  window.lcLiveOf = function (dsId) {
    var r = window.lcRemote[dsId], U = r && r.unl, L = U && U.db && window._lcLive[U.db];
    return L && L.lists[dsId] ? L : null;
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
  /* a column is never offered for dropping while any class on the page
     declares an attribute of that name (Michel, 2026-10-18: laps declared
     in the pad's Sprint, 🧹 still offered to drop it) */
  function lcDeclaredAnywhere(k) {
    var M = window.lcModels || {};
    return Object.keys(M).some(function (n) { var m = M[n]; var f = m && m.fields && m.fields[k]; return !!(f && !f.computed && !f.src); });
  }
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
  window.lcDeleteOk = function (id, rowId) {
    var m = window._lcDelOk = window._lcDelOk || {};
    (m[id] = m[id] || {})[String(rowId)] = 1;
  };
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
    /* a row leaves the table only when it was deleted (obj.delete(), the
       🗑 verb) — a row that merely vanished from the page (a redraw, a page
       left, a class re-run) is never sent as a deletion (Michel, 2026-10-18:
       "no data at all in the grid") */
    var okDel = (window._lcDelOk || {})[id] || {};
    var del = Object.keys(snap).filter(function (k) { return !seen[k] && okDel[k]; });
    return { ins: ins, upd: upd, del: del, n: ins.length + upd.length + del.length };
  };
  /* 💾 SAVE: the new rows in one insert, each changed row by its id, the
     gone ones by theirs — then the table is read again, its truth (ids,
     defaults) replacing the page's guess */
  window.lcDatasetSave = function (id) {
    var r = window.lcRemote[id];
    if (r && r.unl && ST.frozen(id)) return Promise.reject(new Error("the structure changed — 🔄 applies it first, then the rows save"));
    /* a subclass's row needs _sub (Michel, 2026-10-17: a Sprint made from the
       pad's class came back a Walk) — no name typed letter by letter, so the
       author's save may add it */
    var u0 = r && r.unl, a0 = u0 && lsGet(u0.akey);
    if (a0 && u0.share && u0.tcols && !u0.tcols._sub && !u0._subTried
        && (window.lcDatasets[id] || []).some(function (x) { return x && x._sub; })) {
      u0._subTried = true;
      return u0.rpc("lc_ensure", { token: a0, tbl: u0.tbl, cols: [{ n: "_sub", t: "str" }] })
        .then(function () { u0.tcols._sub = 1; }, function () {})
        .then(function () { return window.lcDatasetSave(id); });
    }
    var ch = window.lcDatasetChanges(id);
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
      /* a file beside the page (data/sales.csv) on a page read from an http
         source — a host serving its files: it resolves against that source,
         not against the site the page is based on (Michel, 2026-10-22) */
      var srcRoot = el.closest ? el.closest("[data-lc-src]") : null, srcBase = srcRoot ? srcRoot.dataset.lcSrc || "" : "";
      if (/^https?:\/\//.test(srcBase) && href && !/^[\w+.-]+:/.test(href) && href.charAt(0) !== "/" && href.charAt(0) !== "#") {
        try { href = new URL(href, srcBase).href; } catch (e) {}
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
                    db: el.getAttribute("data-db") || "", proj: uProj, base: uBase, key: dbKey };
          U.rpc = function (fn, body) {
            return fetch(uBase + "/rpc/" + fn, { method: "POST", cache: "no-store",
                                                 headers: dbHeaders({ "Content-Type": "application/json" }), body: JSON.stringify(body) })
              .then(function (x) {
                return x.text().then(function (t) {
                  var j = null; try { j = JSON.parse(t); } catch (e) {}
                  if (x.ok) return j;
                  if (x.status === 404) { U.setup = "none"; throw new Error("this database has no Lightcode setup yet — 📋 the setup SQL below, pasted once in the project's SQL Editor"); }
                  if (x.status === 401 || x.status === 403) throw new Error("the database refused the key — check apikey=\"…\"");
                  throw new Error(((j && j.message) || ("HTTP " + x.status)).replace(/^lc: /, ""));
                });
              });
          };
          unlPull = function (opts) {
            var r = window.lcRemote[id], author = lsGet(U.akey);
            /* a structure that changed waits for 🔄: no read meanwhile */
            if (U.read && ST.frozen(id) && !(opts && opts.ensure)) return Promise.resolve();
            /* the table's columns change on the first read and when asked
               (↻, 🧹, the pad's save) — never on a save or a re-read */
            /* "first" is per visit, not per drawing: a pad redraws the class
               block on every pause and rebuilds its table's link */
            var seen = window._lcTblSeen = window._lcTblSeen || {};
            if (!U.tcols && seen[id]) U.tcols = seen[id];
            var ensure = author && (!seen[id] || (opts && opts.ensure));
            /* THE SETUP HAS A VERSION (Michel, 2026-10-20: "where to run it? not
               clear"): the author's device asks once per visit; older than the
               engine's, or missing, the grid offers the script to copy */
            var want = window.lcSetupVersion || 2, vk = window._lcSetupSeen = window._lcSetupSeen || {};
            if (author && !vk[uProj]) {
              /* the answer is the project's, kept per project: a pad redraws
                 the class block and rebuilds the table's link, so the record
                 asked is not always the record drawn */
              vk[uProj] = { setup: "" };
              U.rpc("lc_version", {}).then(function (v) {
                vk[uProj].setup = (+v || 0) < want ? "old" : "";
                if (vk[uProj].setup) document.dispatchEvent(new CustomEvent("lc-remote-state", { detail: id }));
              }).catch(function () { vk[uProj].setup = "old"; document.dispatchEvent(new CustomEvent("lc-remote-state", { detail: id })); });
            }
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
                      /* the table now has the code's types too */
                      var ty = {}; (cols || []).forEach(function (c) { ty[c.n] = c.t; });
                      ST.types[id] = ty;
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
              /* 🔄 applied: the rows that waited save now, then the table is read */
              var waiting = opts && opts.keep && window.lcDatasetChanges(id);
              if (waiting && waiting.n && !ST.frozen(id)) {
                return window.lcDatasetSave(id).then(function () { ST.settled(id); });
              }
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
                if (ensure || !ST.seen[id]) ST.settled(id);
                window.lcSetDataset(id, shapeData(rows, el));
                /* same rows, other state (a name now known, a hint gone): the grids repaint */
                document.dispatchEvent(new CustomEvent("lc-remote-state", { detail: id }));
                liveFollow(U, id, uBase, dbKey, sh);
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
        /* AN ADDRESS THAT FOLLOWS A SELECTION (Michel, 2026-10-18, module 06
           page 2: the sky over the shelter picked): {campus_grid.row.lat} in
           the link is the grid's selected row — its first row until a pick —
           written like a Python f-string; a new pick asks again */
        var tplRe = /\{\s*(\w+)\.row\.(\w+)\s*\}/g, tpl = null;
        try { if (/\{\s*\w+\.row\.\w+\s*\}/.test(decodeURI(href))) tpl = decodeURI(href); } catch (e) {}
        var rowOfGrid = function (gidn) {
          var md = window.lcMasterDetail, g = document.querySelector(".lc-datagrid[data-lc-id='" + gidn + "']");
          var r = md && md._last && md._last[gidn];
          if (!r && g) { var rr = (window.lcDatasets || {})[g.getAttribute("data-bind")]; r = Array.isArray(rr) ? rr[0] : null; }
          return r;
        };
        var resolveHref = function () {
          var ok = true;
          var u = tpl.replace(tplRe, function (_, gn, col) {
            var r = rowOfGrid(gn);
            if (!r || r[col] == null || r[col] === "") { ok = false; return ""; }
            return encodeURIComponent(String(r[col]));
          });
          return ok ? u : null;
        };
        window.lcRemote[id] = { href: href, pull: pull, write: !!keyName || el.getAttribute("write") === "true", at: performance.now(),
                                db: isDb ? { base: href.split("?")[0], headers: dbHeaders } : null, snap: {}, unl: unl ? U : null };
        if (tpl && !isDb) {
          var grids = [], m0;
          tplRe.lastIndex = 0;
          while ((m0 = tplRe.exec(tpl))) if (grids.indexOf(m0[1]) < 0) grids.push(m0[1]);
          var askAgain = function () {
            var u = resolveHref();
            if (!u || u === href) return !!u;
            href = u; window.lcRemote[id].href = u; pull(); return true;
          };
          (function first(tries) {
            if (askAgain() || tries > 75) return;
            setTimeout(function () { first(tries + 1); }, 200);
          })(0);
          grids.forEach(function (gn) { if (window.lcMasterDetail) window.lcMasterDetail.subscribe(gn, askAgain); });
        } else pull();
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
    /* dates="time": those columns print as a date and an hour, "Oct 23 12:00 PM" — a time
       written without a zone (a service's local hours) as written, one with a zone on the
       reader's clock (Michel, 2026-10-22: "the time should displayed in local time just like:
       Oct 23 12:00 PM") */
    /* city_time@tz: that column in the zone the row's tz column names (Europe/London) —
       the city's own clock beside the reader's (Michel, 2026-10-22: "both") */
    var dateCols = [], dateZone = {};
    (el.getAttribute("dates") || "").split(",").forEach(function (c) {
      var p = c.trim().split("@"); if (!p[0]) return;
      dateCols.push(p[0].trim()); if (p[1]) dateZone[p[0].trim()] = p[1].trim();
    });
    var dateText = function (v, zone) {
      var s = String(v == null ? "" : v), m = /^(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)(?::\d\d(?:\.\d+)?)?(Z|[+-]\d\d:?\d\d)?$/.exec(s);
      if (!m) return null;
      var mo = +m[2], d = +m[3], h = +m[4], mi = m[5];
      if (m[6]) {
        var t = new Date(s); if (isNaN(t.getTime())) return null;
        if (zone) {
          try {
            var parts = {};
            new Intl.DateTimeFormat("en-US", { timeZone: zone, month: "numeric", day: "numeric", hour: "numeric", minute: "2-digit", hourCycle: "h23" })
              .formatToParts(t).forEach(function (x) { parts[x.type] = x.value; });
            mo = +parts.month; d = +parts.day; h = +parts.hour % 24; mi = parts.minute;
          } catch (e) { return null; }   /* a zone the browser does not know: the raw value shows */
        } else { mo = t.getMonth() + 1; d = t.getDate(); h = t.getHours(); mi = ("0" + t.getMinutes()).slice(-2); }
      }
      var mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][mo - 1];
      return mon + " " + d + " " + ((h % 12) || 12) + ":" + mi + " " + (h < 12 ? "AM" : "PM");
    };
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
    /* THE ROW YOU WERE ON, FOUND AGAIN BY WHAT IT HOLDS (Michel, 2026-10-20:
       "after inserting a line in a datagrid, the newly created line should
       remain the selected one"): a new row is saved, the table is read
       again and its objects are born anew with the table's ids — the old
       identity is gone, the content is not. Its signature: the values,
       without id, obj and the table's own notes. */
    var selSig = null;
    var sigOf = function (r) {
      if (!r) return null;
      var o = {};
      Object.keys(r).sort().forEach(function (k) { if (k !== "obj" && k !== "id" && k.charAt(0) !== "_") o[k] = String(r[k] == null ? "" : r[k]); });
      return JSON.stringify(o);
    };
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
      /* a list read from elsewhere — itself, or behind the query it shows:
         the corner's ↻ reads it again (Michel, 2026-10-18: "keep the style
         defined page 3… when data is R/O, there is no + and it starts from
         right to left") */
      var roRemote = null;
      if (window.lcRemote && !(window.lcRemote[bindId] && window.lcRemote[bindId].db)) {
        if (window.lcRemote[bindId]) roRemote = bindId;
        else {
          var qEl = document.querySelector(".lc-query[data-lc-id='" + bindId + "']");
          ((qEl && qEl.getAttribute("data-bind")) || "").split(",").forEach(function (b) {
            b = b.trim(); if (!roRemote && window.lcRemote[b] && !window.lcRemote[b].db) roRemote = b;
          });
        }
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
      /* a class that came through a link (lc://): ↻ asks its server again (Michel, 2026-10-20) */
      if (!roRemote && mdl0 && mdl0.remote) roRemote = "lc:" + bindId;
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
      /* every class grid wears the gutter (Michel, 2026-10-18: "the grid in page 1 was not upgraded
         to follow the UX decided in page 3" — "Gutter?") — stages or not */
      var gut = !!model;
      /* not lcWhen (topbar.md): that one reads a UTC stamp with its zone; a
         datetime attribute is local, zoneless, and reads as "Oct 20 10:15" —
         its date always, today included: a column where one row says
         "15:35" and the next "Oct 19 10:15" reads as two formats
         (Michel, 2026-10-20, the walk log) */
      window.lcTimeShort = window.lcTimeShort || function (iso) {
        var s = String(iso == null ? "" : iso), m = /^(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)/.exec(s);
        if (!m) return s;
        var mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][+m[2] - 1];
        return mon + " " + (+m[3]) + " " + m[4] + ":" + m[5];
      };
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
          /* the chip alone: the verbs live in the gutter, for every class
             (Michel, 2026-10-18: "we replaced this by the gutter already") */
          return "<td class='lc-dg-state' data-row='" + idx + "'>"
            + "<span class='lc-dg-chip' style='min-width:" + wide + "ch'>" + esc(v) + "</span></td>";
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
        /* a datetime reads as Oct 18 13:15, its date always (Michel, 2026-10-20; time-only today until then) */
        if (f && f.t === "datetime") v = window.lcTimeShort(v);
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
                  var dt = !editable && dateCols.indexOf(c) >= 0 ? dateText(v, dateZone[c] ? row[dateZone[c]] : "") : null;
                  if (dt) return "<td title='" + v + "'>" + dt + "</td>";
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
      /* 🧹 lives in the structure panel now (Michel, 2026-10-18) */
      var tidyN = dbR && dbR.unl ? ST.tidyCount(dbSrc) : 0;
      var st = dbR ? (dbR.state || (dbCh && dbCh.n ? "dirty" : "ok")) : "";
      /* the code changed the table's structure: saving waits for 🔄 */
      var sPlan = dbR && dbR.unl ? ST.plan(dbSrc) : [], frozen = sPlan.length > 0;
      var stTip = { ok: "saved", dirty: (dbCh && dbCh.n) + (frozen ? " change(s) waiting: the structure changed — 🔄 applies it, then they save" : " change(s) to save — saving by itself, or tap"), saving: "saving…",
                    error: "not saved — " + (dbR && dbR.saveErr || "") + " — tap to try again" }[st] || "";
      /* columns the class has and the table not yet: ↻ adds them (author) */
      var pending = [];
      if (dbR && dbR.unl && dbR.unl.tcols && lsGet(dbR.unl.akey)) {
        pending = (unlCols(dbSrc) || []).map(function (c) { return c.n; }).filter(function (n) { return !dbR.unl.tcols[n]; });
      }
      var rfTip = pending.length ? "↻ adds the column" + (pending.length > 1 ? "s " : " ") + pending.join(", ") + " to the table, then reads it" : "read the database again";
      /* the corner, right to left (Michel, 2026-10-17): ＋, the save state
         (always there), ↻ (on hover) — so nothing leaves a hole */
      var liveL = dbR && dbR.unl && window.lcLiveOf ? window.lcLiveOf(dbSrc) : null;
      var liveMark = liveL ? "<span class='lc-dg-cbtn lc-dg-live " + (liveL.on ? "lc-dg-live-on" : "lc-dg-live-off") + "' title='"
        + (liveL.on ? "live — the others&#39; changes arrive by themselves" : "live, but the line is down — the others&#39; changes are not arriving") + "' aria-label='live'>●</span>" : "";
      var corner = liveMark + (dbR && !frozen && tidyN ? "<button class='lc-dg-cbtn lc-dg-tidy' type='button' title='" + esc(tidyN + " leftover(s) to tidy — tap to review") + "' aria-label='review the leftovers'>🧹<b>" + tidyN + "</b></button>" : "")
        + (dbR && frozen ? "<button class='lc-dg-cbtn lc-dg-refresh lc-dg-struct' type='button' title='" + esc("the code changed the table: " + sPlan.length + " step(s) — tap to review and apply") + "' aria-label='review the structure changes'>🔄<b>" + sPlan.length + "</b></button>"
           : dbR ? "<button class='lc-dg-cbtn lc-dg-refresh" + (pending.length ? " lc-dg-pending" : "") + "' type='button' title='" + esc(rfTip) + "' aria-label='" + esc(rfTip) + "'>↻</button>" : "")
        + (dbR ? ""
            + "<button class='lc-dg-cbtn lc-dg-save lc-dg-st-" + st + "' type='button'"
            + (st === "dirty" || st === "error" ? "" : " disabled") + " title='" + esc(stTip) + "' aria-label='" + esc(stTip) + "'>"
            + "<span>" + { ok: "✓", dirty: "●", saving: "⟳", error: "⚠" }[st] + "</span></button>" : "")
        + (!dbR && roRemote ? "<button class='lc-dg-cbtn lc-dg-refresh lc-dg-roreload' type='button' title='read it again — the list lives elsewhere' aria-label='read the list again'>↻</button>" : "")
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
        var setupSt = U.setup || (((window._lcSetupSeen || {})[U.proj] || {}).setup) || "";
        if (setupSt && (U.author || lsGet(U.akey)))
          unlBar += "<span class='lc-dg-unl-setup'>🔧 " + (setupSt === "none" ? "no Lightcode setup in this project yet" : "this project's setup is older than the engine")
            + " — paste it in the project's SQL Editor, Run, then ↻</span>"
            + "<button class='lc-dg-btn lc-dg-unl-setupcopy' type='button' title='the setup SQL, to paste once in the SQL Editor'>📋 Copy the setup SQL</button>";
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
      if (liveL && !liveL.on && !srcErr && !(U && dbR.error)) html += "<p class='lc-dg-say lc-dg-live-say' role='status'>🔌 live, but the line is down — the others&#39; changes are not arriving; ↻ reads the table</p>";
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
          var changing = false;
          var shut = function () {
            td.removeAttribute("contenteditable"); td.classList.remove("lc-dg-typing");
            /* the cell closes with nothing typed (Enter, Escape, a tap away): a
               row born with values (a stamped hour) still has its save to make,
               and the autosave only woke on a change (Michel, 2026-10-21:
               "given the default values, I do have data in that row, the row
               is not saved") — a change renders by itself */
            if (!changing && dbR) setTimeout(function () {
              var ch = window.lcDatasetChanges(dbSrc);
              if (ch && ch.n && !el.querySelector(".lc-dg-typing")) window.lcSetDataset(dbSrc, window.lcDatasets[dbSrc] || []);
            }, 0);
          };
          var commit = function () {
            if (!td.isContentEditable) return;
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            var col = td.getAttribute("data-col"), txt = (td.textContent || "").trim();
            changing = !!row && String(row[col] == null ? "" : row[col]) !== txt;
            shut();
            changing = false;
            if (!row) return;
            if (String(row[col] == null ? "" : row[col]) === txt) return;
            window.lcModelOp(bindId, { t: "set", obj: String(row.obj), col: col, val: txt },
              "_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(col) + "," + JSON.stringify(txt) + ")");
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
            if (open && open._lcFor === cell) { open._lcClose(); return; }
            document.querySelectorAll(".lc-dg-menu").forEach(function (m) { if (m._lcClose) m._lcClose(); else m.remove(); });
            var row = sorted[parseInt(cell.getAttribute("data-row"), 10)];
            if (!row) return;
            var ref = cell.getAttribute("data-ref"), col = cell.getAttribute("data-col");
            var rr = (window.lcDatasets || {})[ref] || [], lab = refLabel(ref);
            var nameOf = function (r) { return String(r[lab] != null && r[lab] !== "" ? r[lab] : r.obj); };
            /* the row a dog is picked for is the selection first (Michel,
               2026-10-18: "that row should be selected first before the
               picklist is open") — the form follows as the list closes */
            var tr = cell.parentNode, key = row.obj != null ? "o:" + row.obj : "i:" + cell.getAttribute("data-row");
            var pub = key !== selKey && lcId && window.lcMasterDetail ? row : null;
            el.querySelectorAll("tbody tr").forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            tr.classList.add("lc-dg-selected");
            selKey = key;
            window.lcPickMenu(cell, rr.map(function (r) { return { v: String(r.obj), label: nameOf(r), cur: String(r.obj) === String(row[col]) }; }),
              function (v) {
                window.lcModelOp(bindId, { t: "set", obj: String(row.obj), col: col, val: v },
                  "_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(col) + "," + JSON.stringify(v) + ")");
              },
              function () { if (pub) window.lcMasterDetail.publish(lcId, pub); });
          });
        });
        el.querySelectorAll("select.lc-dg-pick").forEach(function (sel) {
          sel.addEventListener("change", function () {
            var row = sorted[parseInt(sel.getAttribute("data-row"), 10)];
            if (row) window.lcModelOp(bindId, { t: "set", obj: String(row.obj), col: sel.getAttribute("data-col"), val: sel.value },
              "_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(sel.getAttribute("data-col")) + "," + JSON.stringify(sel.value) + ")");
          });
        });
        /* the ⌄: the row's verbs — a transition is live when the row's state
           is in its pre, grey otherwise (pressing a grey one says what it
           needs); plain verbs always; Delete last, born of Object */
        var closeMenu = function () {
          document.querySelectorAll(".lc-dg-menu").forEach(function (m) {
            m.parentNode.removeChild(m);
            if (m._lcPub && lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, m._lcPub);
          });
        };
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
            /* A TAP IN THE GUTTER SELECTS FIRST (Michel, 2026-10-17) — and the
               form follows at once (2026-10-18: "the form remains on the old
               object"); the menu lives on the page, a repaint leaves it */
            var pub = key !== selKey && lcId && window.lcMasterDetail ? row : null;
            if (pub) { selKey = key; window.lcMasterDetail.publish(lcId, pub); pub = null; }
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
            menu._lcPub = pub;
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
                window.lcModelOp(bindId, { t: "verb", obj: String(row.obj), verb: verb },
                  "_lc_verb(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(verb) + ")");
              });
            });
            setTimeout(function () { document.addEventListener("click", closeMenu, { once: true }); }, 0);
          }
        };
        /* A CLASS WITH NO STATE STILL HAS VERBS (Michel, 2026-10-16) — and
           Delete always: a light ⋯ in the row's gutter opens them (2026-10-17) */
        el.querySelectorAll("td.lc-dg-gut").forEach(function (td) {
          td.addEventListener("click", function (e) { verbsMenu(td, e); });
        });
        /* ➕ New: the class itself, or — when the page declares subclasses —
           a pick of the class and each one; the new row gets selected
           (Michel, 2026-10-16) */
        var nb = el.querySelector(".lc-dg-new");
        var make = function (kind) {
          pendingNew = {};
          (window.lcDatasets[bindId] || []).forEach(function (r) { pendingNew[String(r.obj)] = 1; });
          setTimeout(function () { pendingNew = null; }, 4000);
          window.lcModelOp(bindId, { t: "new", kind: kind && kind !== bindId ? kind : "" },
            "_lc_new(" + JSON.stringify(bindId) + (kind && kind !== bindId ? "," + JSON.stringify(kind) : "") + ")");
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
            /* a default (0, False) is not a value typed: a new Sprint is blank until its first word */
            return !(f && f.state) && k !== "_kind" && k !== "_sub" && r[k] !== "" && r[k] != null && r[k] !== 0 && r[k] !== false;
          });
        });
        clearTimeout(dbR._auto);
        if (!open && !blank && !ST.frozen(dbSrc)) dbR._auto = setTimeout(function () {
          /* a cell opened since (the caret New puts in the first one) waits too */
          var a3 = document.activeElement;
          if (el.querySelector(".lc-dg-typing") || (a3 && a3 !== document.body && el.contains(a3) && a3.isContentEditable)) return;
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
        el.querySelectorAll(".lc-dg-unl-setupcopy").forEach(function (b) {
          b.addEventListener("click", function (e) {
            e.stopPropagation();
            var url = "{{ '/assets/lc_setup.sql' | relative_url }}";
            b.textContent = "⏳";
            fetch(url, { cache: "no-store" }).then(function (r) { return r.ok ? r.text() : Promise.reject(new Error("HTTP " + r.status)); })
              .then(function (sql) {
                return (navigator.clipboard && navigator.clipboard.writeText ? navigator.clipboard.writeText(sql) : Promise.reject(new Error("no clipboard")))
                  .then(function () { b.textContent = "✓ Copied — paste it in the SQL Editor"; },
                        function () {
                          /* the clipboard refused (a frame, a phone): the script sits here, selected — ⌘C */
                          b.textContent = "select all, copy — paste it in the SQL Editor";
                          var ta = b.parentNode.querySelector("textarea.lc-dg-unl-sql");
                          if (!ta) { ta = document.createElement("textarea"); ta.className = "lc-dg-unl-sql"; ta.rows = 6; ta.setAttribute("aria-label", "the setup SQL"); b.parentNode.appendChild(ta); }
                          ta.value = sql; ta.focus(); ta.select();
                        });
              })
              .catch(function (err) { b.textContent = "⚠️ " + err.message; });
          });
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
      var roBtn = el.querySelector(".lc-dg-roreload");
      if (roBtn) roBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        var mm = (window.lcModels || {})[bindId], ops = mm && mm.remote && (window.lcRemoteOps || {})[mm.remote.prefix];
        if (ops) ops.send({ t: "follow" }); else window.lcRemoteReload(roRemote);
      });
      var tidyBtn = el.querySelector(".lc-dg-tidy");
      if (tidyBtn) tidyBtn.addEventListener("click", function (e) { e.stopPropagation(); window.lcStructPanel(dbSrc); });
      if (rf) rf.addEventListener("click", function (e) {
        e.stopPropagation();
        if (ST.frozen(dbSrc)) { window.lcStructPanel(dbSrc); return; }
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
        /* the grid's row exists now: a {= grid.row.x } written before it may read it */
        if (lcId && !el._lcSelSaid) {
          el._lcSelSaid = 1;
          setTimeout(function () { document.dispatchEvent(new CustomEvent("lc-selection", { detail: lcId })); }, 0);
        }
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
              selSig = sigOf(slice[ni]);
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
              selSig = sigOf(r);
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
          /* the same row under a new identity (saved, read back): found by
             its content, it stays selected and the card follows */
          if (!stillThere && selSig) {
            for (var si = 0; si < slice.length; si++) {
              if (sigOf(slice[si]) === selSig && trs[si]) {
                stillThere = true;
                selKey = keyOf(slice[si]) || "i:" + si;
                trs[si].classList.add("lc-dg-selected");
                if (model && lcId && window.lcMasterDetail) {
                  var pj2 = JSON.stringify(slice[si]);
                  if (pj2 !== lastPubJson) { lastPubJson = pj2; window.lcMasterDetail.publish(lcId, slice[si]); }
                }
                break;
              }
            }
          }
          /* the selected row is gone (deleted): the first row takes the
             selection and the bound card follows, never a ghost */
          if (!stillThere) { selKey = null; selSig = null; publishedFirst = false; lastPubJson = null; }
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
