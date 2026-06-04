{%- comment -%}
Floating ✏️ FAB (bottom-right). Clicking opens an in-page editor drawer that
reads/writes the current page via GitHub Contents API. PAT + repo stored in
localStorage. Falls back gracefully: if no PAT, shows the connect form first.

Keyboard: Esc closes the drawer. Cmd/Ctrl+S saves.

Auto-included by docs/_layouts/default.html. Skipped for:
  - the 404 page
  - pages without page.path
  - pages with no_edit: true in front matter
  - embed mode (?embed=true)
{%- endcomment -%}

{% if page.path and page.permalink != "/404.html" and page.no_edit != true %}
<style>
/* ── FAB ───────────────────────────────────────────────── */
.lc-edit-fab {
  position: fixed; bottom: 1.2em; right: 1.2em;
  height: 44px; min-width: 44px; padding: 0 14px;
  border-radius: 22px; background: white; color: #0066cc;
  border: 1px solid #d0e3f5; display: inline-flex; align-items: center;
  gap: 0; text-decoration: none; font-size: 0.88em; font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08); z-index: 997; overflow: hidden;
  white-space: nowrap; cursor: pointer;
  transition: gap 0.18s, padding 0.18s, background 0.15s, border-color 0.15s, box-shadow 0.15s, transform 0.15s;
}
.lc-edit-fab .lc-edit-fab-icon { font-size: 1.2em; line-height: 1; }
.lc-edit-fab .lc-edit-fab-label { max-width: 0; opacity: 0; overflow: hidden;
  transition: max-width 0.22s ease, opacity 0.18s ease 0.04s; }
@media (hover: hover) and (pointer: fine) {
  .lc-edit-fab:hover { background: #f5f9ff; border-color: #0066cc;
    box-shadow: 0 4px 14px rgba(0,102,204,0.18); transform: translateY(-1px); gap: 0.45em; padding-right: 16px; }
  .lc-edit-fab:hover .lc-edit-fab-label { max-width: 200px; opacity: 1; }
}
.lc-edit-fab:focus-visible { outline: 2px solid #0066cc; outline-offset: 2px; }
.lc-embed-mode .lc-edit-fab { display: none !important; }
@media (max-width: 700px) { .lc-edit-fab { bottom: 0.8em; right: 0.8em; } }

/* ── Drawer ────────────────────────────────────────────── */
#ed-drawer {
  position: fixed; top: 48px; right: 0; bottom: 0; left: 0; background: #fff; z-index: 999;
  display: none; flex-direction: column; overflow: hidden;
}
#ed-drawer.open { display: flex; }
#ed-top {
  display: flex; align-items: center; gap: 0.6em; padding: 0.7em 1em;
  border-bottom: 1px solid #e0e0e0; background: #fafafa; flex-shrink: 0;
  min-height: 52px;
}
#ed-filename {
  flex: 1; font-family: monospace; font-size: 0.85em; color: #666;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
#ed-body { display: flex; flex: 1; overflow: hidden; }
#ed-sidebar {
  width: 210px; flex-shrink: 0; overflow-y: auto;
  border-right: 1px solid #e0e0e0; padding: 0.8em 0.7em; font-size: 0.85em;
}
#ed-main { flex: 1; display: flex; flex-direction: row; overflow: hidden; }
#ed-left { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 200px; }
#ed-input {
  flex: 1; border: none; resize: none;
  font-family: monospace; font-size: 0.88em; padding: 1em; line-height: 1.6;
  outline: none; background: #fdfcfb;
}
#ed-preview { flex: 1; overflow-y: auto; padding: 1em 1.5em; position: relative; border-left: 1px solid #e0e0e0; }
/* 50% zoom mode: render content at 200% width then scale to fit */
#ed-preview.lc-zoom { overflow-x: hidden; }
#ed-preview.lc-zoom > div:not(.ed-pbar) { width: 200%; zoom: 0.5; transform-origin: top left; }
/* Live-preview progress bar */
.ed-pbar {
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: #0066cc; transform-origin: left;
  transform: scaleX(0); opacity: 0;
  transition: transform 0.35s ease, opacity 0.15s;
  pointer-events: none;
}
.ed-pbar.wait { opacity: 1; transform: scaleX(0.3); transition: transform 2s ease, opacity 0.1s; }
.ed-pbar.go   { opacity: 1; transform: scaleX(0.8); transition: transform 0.25s ease; }
.ed-pbar.done { opacity: 0; transform: scaleX(1);   transition: transform 0.1s ease, opacity 0.3s 0.05s; }
@media (max-width: 700px) {
  #ed-sidebar { display: none; }
  #ed-splitter { display: none; }
  #ed-preview { display: none; }
}

/* ── Sidebar toggle ─────────────────────────────────── */
#ed-sidebar-toggle {
  flex-shrink: 0; background: none; border: 1px solid #e0e0e0;
  border-radius: 4px; cursor: pointer; color: #888; font-size: 0.85em;
  padding: 0.2em 0.5em; line-height: 1; transition: background 0.1s;
}
#ed-sidebar-toggle:hover { background: #f0f0f0; color: #333; }
#ed-sidebar {
  transition: width 0.2s ease, padding 0.2s ease, opacity 0.15s ease, border 0.2s ease;
}
#ed-sidebar.ed-collapsed {
  width: 0 !important; padding: 0 !important; opacity: 0;
  overflow: hidden; border-right: none;
}

/* ── Splitter ───────────────────────────────────────── */
#ed-splitter {
  width: 5px; flex-shrink: 0; cursor: col-resize;
  background: #e8e8e8; position: relative; z-index: 1;
  transition: background 0.15s;
}
#ed-splitter:hover, #ed-splitter.ed-dragging { background: #0066cc; }

/* ── Editor tabs ────────────────────────────────────── */
#ed-tabs {
  display: flex; border-bottom: 1px solid #e0e0e0;
  background: #f5f5f5; flex-shrink: 0; padding: 0 0.5em;
}
.ed-tab {
  padding: 0.45em 1em; cursor: pointer; font-size: 0.83em;
  border-bottom: 2px solid transparent; color: #777; user-select: none;
  transition: color 0.1s, border-color 0.1s;
}
.ed-tab.active { color: #0066cc; border-bottom-color: #0066cc; font-weight: 600; }
.ed-tab:hover:not(.active) { color: #333; }
#ed-raw-pane { display: flex; flex: 1; overflow: hidden; }
#ed-raw-pane.ed-hidden { display: none; }
#ed-blocks-pane { display: none; flex: 1; flex-direction: column; overflow: hidden; }
#ed-blocks-pane.ed-active { display: flex; }

/* ── Grid/form splitter ─────────────────────────────── */
#ed-grid-splitter {
  height: 5px; flex-shrink: 0; cursor: row-resize;
  background: #e8e8e8; display: none;
  transition: background 0.15s;
}
#ed-grid-splitter:hover, #ed-grid-splitter.ed-dragging { background: #0066cc; }
#ed-grid-splitter.ed-vis { display: block; }

/* ── Blocks grid ────────────────────────────────────── */
#ed-grid {
  flex: 1; overflow-y: auto; min-height: 0; font-size: 0.84em;
}
#ed-grid table { width: 100%; border-collapse: collapse; table-layout: fixed; }
#ed-grid th {
  position: sticky; top: 0; background: #f8f8f8; z-index: 1;
  font-size: 0.78em; font-weight: 600; color: #999; text-transform: uppercase;
  letter-spacing: 0.05em; padding: 0.4em 0.7em;
  border-bottom: 1px solid #e0e0e0; text-align: left; white-space: nowrap;
}
#ed-grid td { padding: 0.32em 0.7em; border-bottom: 1px solid #f0f0f0; vertical-align: middle; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#ed-grid tr.ed-sel td { background: #e8f2ff; }
#ed-grid tr[data-idx]:hover:not(.ed-sel) td { background: #f8f8f8; cursor: pointer; }
#ed-grid tr.ed-drag-over td { border-top: 2px solid #0066cc; }
.ed-drag-handle { cursor: grab; color: #ccc; font-size: 1.1em; }
.ed-drag-handle:active { cursor: grabbing; }
.ed-block-type {
  display: inline-block; padding: 0.1em 0.45em; border-radius: 3px;
  background: #eef3ff; color: #0052cc; font-size: 0.88em; font-family: monospace;
}

/* ── Block edit form ────────────────────────────────── */
#ed-block-form {
  flex-shrink: 0; padding: 0.8em 1em; background: #fafafa;
  border-top: 2px solid #0066cc; font-size: 0.84em;
  display: none; overflow: hidden; height: 180px; /* fallback until initGridSplit runs */
}
#ed-block-form.ed-visible { display: flex; flex-direction: column; }
#ed-block-form label { display: block; color: #666; font-size: 0.82em; margin: 0 0 0.18em; flex-shrink: 0; }
#ed-block-form input, #ed-block-form select, #ed-block-form textarea {
  width: 100%; box-sizing: border-box; padding: 0.3em 0.5em;
  border: 1px solid #ddd; border-radius: 4px; font-size: 0.9em;
  font-family: inherit; margin-bottom: 0.55em; background: #fff;
}
#ed-block-form textarea { font-family: monospace; resize: none; flex: 1; min-height: 0; margin-bottom: 0; }
#ed-block-form textarea[readonly] { background: #f6f8fa; color: #444; }
#ed-block-form select { cursor: pointer; }
.ebf-meta { flex-shrink: 0; }
.ebf-content-wrap { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.ebf-actions { flex-shrink: 0; padding-top: 0.5em; }

/* ── Preview highlight pulse ─────────────────────────── */
@keyframes ed-hl-pulse {
  0%   { outline: 3px solid rgba(0,102,204,0.7); outline-offset: 3px; }
  60%  { outline: 3px solid rgba(0,102,204,0.4); outline-offset: 3px; }
  100% { outline: none; outline-offset: 0; }
}
.ed-hl-pulse { animation: ed-hl-pulse 1.6s ease-out forwards; }

/* ── Sidebar pieces ────────────────────────────────────── */
.ed-section-label {
  font-size: 0.75em; color: #999; font-weight: 600; letter-spacing: 0.06em;
  text-transform: uppercase; margin: 0.9em 0 0.4em; display: block;
}
.ed-folder { font-size: 0.78em; color: #888; font-weight: 600; margin: 0.7em 0 0.15em; padding-left: 0.1em; }
.ed-chip {
  display: block; padding: 0.28em 0.6em; margin: 0.18em 0;
  border: 1px solid #e0e0e0; border-radius: 5px; cursor: pointer;
  color: #333; text-decoration: none; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
  transition: border-color 0.1s, background 0.1s;
}
.ed-chip:hover { border-color: #0066cc; background: #f0f6ff; color: #0066cc; }
.ed-chip.active { border-color: #0066cc; background: #e8f2ff; color: #004fa0; font-weight: 500; }

/* ── Connect panel ─────────────────────────────────────── */
#ed-setup { margin-bottom: 0.6em; }
#ed-setup summary {
  cursor: pointer; color: #0066cc; font-weight: 500; padding: 0.2em 0;
  list-style: none; display: flex; align-items: center; gap: 0.3em;
}
#ed-setup summary::-webkit-details-marker { display: none; }
#ed-setup label { display: block; color: #555; margin: 0.5em 0 0.2em; }
#ed-setup input {
  width: 100%; font-family: monospace; font-size: 0.9em;
  padding: 0.3em 0.5em; border: 1px solid #ddd; border-radius: 4px;
  box-sizing: border-box; margin-bottom: 0.1em;
}
#ed-status { font-size: 0.8em; margin-top: 0.4em; min-height: 1.2em; }

/* ── History entries ───────────────────────────────────── */
.ed-commit { margin: 0.3em 0; padding: 0.3em 0; border-bottom: 1px solid #f0f0f0; }
.ed-commit-msg { font-weight: 500; color: #333; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ed-commit-meta { font-size: 0.82em; color: #999; margin-top: 0.1em; }
.ed-diff-add { background: #e6ffed; display: block; }
.ed-diff-del { background: #ffeef0; display: block; }
.ed-diff-ctx { color: #bbb; display: block; }

/* ── Toast ─────────────────────────────────────────────── */
#ed-toast {
  position: fixed; top: 1em; left: 50%; transform: translateX(-50%);
  padding: 0.55em 1.1em; border-radius: 6px; font-size: 0.88em; font-weight: 500;
  z-index: 9999; display: none; box-shadow: 0 3px 10px rgba(0,0,0,0.15);
  pointer-events: none;
}
</style>

<!-- Toast -->
<div id="ed-toast"></div>

<!-- Editor drawer -->
<div id="ed-drawer" role="dialog" aria-label="Page editor">

  <!-- Top bar -->
  <div id="ed-top">
    <button id="ed-sidebar-toggle" title="Toggle sidebar">◀</button>
    <span id="ed-filename">No file selected</span>
    <span id="ed-build" style="font-size:0.78em;color:#888;margin-left:0.5em;flex-shrink:0"></span>
    <a href="#" class="lc-btn lc-btn-secondary" id="ed-zoom-btn" title="Toggle 50% preview scale" style="font-size:0.82em;padding:0.35em 0.9em;margin-left:auto">50%</a>
    <a href="#" class="lc-btn lc-btn-secondary" id="ed-new-btn" style="font-size:0.82em;padding:0.35em 0.9em">+ New</a>
    <a href="#" class="lc-btn" id="ed-save-btn" style="font-size:0.82em;padding:0.35em 0.9em">💾 Save</a>
    <a href="#" id="ed-close-btn" title="Close (Esc)"
       style="font-size:1.3em;color:#888;text-decoration:none;padding:0 0.2em;line-height:1;margin-left:0.2em">✕</a>
  </div>

  <!-- Body -->
  <div id="ed-body">

    <!-- Sidebar -->
    <div id="ed-sidebar">

      <!-- Connection -->
      <details id="ed-setup">
        <summary>⚙️ Connect</summary>
        <label>Personal access token
          <input id="ed-pat" type="password" placeholder="ghp_…" autocomplete="current-password">
        </label>
        <label>Repository
          <input id="ed-repo" type="text" placeholder="owner/repo-name" autocomplete="off">
        </label>
        <div style="margin-top:0.6em;display:flex;gap:0.4em;flex-wrap:wrap">
          <a href="#" class="lc-btn" id="ed-connect-btn" style="font-size:0.82em;padding:0.35em 0.9em">Connect</a>
          <a href="#" class="lc-btn lc-btn-danger" id="ed-disconnect-btn" style="font-size:0.82em;padding:0.35em 0.9em;display:none">Disconnect</a>
        </div>
        <div id="ed-status"></div>
      </details>

      <!-- File list -->
      <span class="ed-section-label">Pages</span>
      <div id="ed-files" style="color:#bbb">Connect to browse.</div>

      <!-- History -->
      <span class="ed-section-label">History</span>
      <div id="ed-history" style="color:#bbb">Select a file.</div>

      <!-- Build status moved to topbar -->

    </div><!-- /sidebar -->

    <!-- Editor + Preview -->
    <div id="ed-main">
      <!-- Left: tabs + raw OR blocks pane -->
      <div id="ed-left">
        <div id="ed-tabs">
          <span class="ed-tab active" data-tab="raw">✏️ Raw</span>
          <span class="ed-tab" data-tab="blocks">⊞ Blocks</span>
        </div>
        <div id="ed-raw-pane">
          <textarea id="ed-input" placeholder="Select a file from the sidebar, or create a new page…" spellcheck="false"></textarea>
        </div>
        <div id="ed-blocks-pane">
          <div id="ed-grid"><p style="color:#bbb;padding:1em">Load a file to see its blocks.</p></div>
          <div id="ed-grid-splitter"></div>
          <div id="ed-block-form"></div>
        </div>
      </div>
      <!-- Splitter + Preview always visible on right -->
      <div id="ed-splitter"></div>
      <div id="ed-preview"></div>
    </div>

  </div><!-- /body -->
</div><!-- /drawer -->

<!-- FAB -->
<a class="lc-edit-fab" id="ed-fab"
   href="#"
   data-page-path="{{ page.path }}"
   title="Edit this page"
   aria-label="Edit this page">
  <span class="lc-edit-fab-icon" aria-hidden="true">✏️</span>
  <span class="lc-edit-fab-label">Edit page</span>
</a>

<script>
(function () {
  var LS_PAT = "lc_ed_pat", LS_REPO = "lc_ed_repo";
  var _pat, _repo, _curFile, _curSha, _dirty = false, _previewTimer = null;

  function setDirty(on) {
    _dirty = on;
    var fnEl = document.getElementById("ed-filename");
    if (!fnEl) return;
    fnEl.textContent = on ? (_curFile || "New file") + " (unsaved)" : (_curFile || "No file selected");
  }

  /* ── GitHub API ──────────────────────────────────────── */
  function gh(method, path, body, cb) {
    var opts = {
      method: method,
      headers: {
        Authorization: "Bearer " + _pat,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    };
    if (body) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(body); }
    fetch("https://api.github.com/repos/" + _repo + path, opts)
      .then(function (r) { return r.json(); })
      .then(cb)
      .catch(function (e) { cb({ error: e.message }); });
  }
  function b64e(s) { return btoa(unescape(encodeURIComponent(s))); }
  function b64d(s) { try { return decodeURIComponent(escape(atob(s))); } catch (_) { return atob(s); } }
  function esc(s) { return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* ── Toast / Status ──────────────────────────────────── */
  function toast(msg, ok) {
    var el = document.getElementById("ed-toast");
    if (!el) return;
    el.textContent = msg;
    el.style.background = ok ? "#28a745" : "#dc3545";
    el.style.color = "#fff";
    el.style.display = "block";
    clearTimeout(el._t);
    el._t = setTimeout(function () { el.style.display = "none"; }, 3000);
  }
  function setStatus(msg, ok) {
    var el = document.getElementById("ed-status");
    if (!el) return;
    el.textContent = msg;
    el.style.color = ok === true ? "#28a745" : ok === false ? "#dc3545" : "#888";
  }

  /* ── Drawer open / close ─────────────────────────────── */
  function openDrawer() {
    var d = document.getElementById("ed-drawer");
    if (!d) return;
    d.classList.add("open");
    document.body.style.overflow = "hidden";
    if (_pat && _repo) {
      /* load file list every open so it stays fresh */
      loadFiles();
      /* auto-load current page on first open */
      if (!_curFile) {
        var pagePath = (document.getElementById("ed-fab") || {}).dataset.pagePath;
        if (pagePath) loadFile("docs/" + pagePath);
      }
    }
  }
  function closeDrawer() {
    if (_dirty && !confirm("Discard unsaved changes to " + (_curFile || "this file") + "?")) return;
    setDirty(false);
    var d = document.getElementById("ed-drawer");
    if (d) d.classList.remove("open");
    document.body.style.overflow = "";
  }

  /* ── File list — AG Grid (recursive via Git Trees API) ─ */
  var _edAgApi = null;
  function loadFiles() {
    var el = document.getElementById("ed-files");
    if (!el) return;
    if (!_edAgApi) el.innerHTML = "<span style='color:#bbb'>Loading…</span>";
    fetch("https://api.github.com/repos/" + _repo + "/git/trees/HEAD?recursive=1", {
      headers: { Authorization: "Bearer " + _pat, Accept: "application/vnd.github+json" }
    }).then(function (r) { return r.json(); }).then(function (data) {
      if (!data.tree) {
        el.innerHTML = "<span style='color:#dc3545;font-size:0.85em'>" + esc(data.message || "Error") + "</span>"; return;
      }
      var rows = data.tree.filter(function (f) {
        var name = f.path.split("/").pop();
        // include underscore modules (e.g. _dog.md) — they're editable content too,
        // but skip Jekyll/system files that aren't meant to be hand-edited here
        if (name === "_config.yml" || name === "_build_trigger.md") return false;
        return f.type === "blob" && f.path.startsWith("docs/") && name.endsWith(".md");
      }).sort(function (a, b) { return a.path.localeCompare(b.path); })
      .map(function (f) {
        var rel = f.path.replace(/^docs\//, "");
        return { path: f.path, file: rel };
      });
      function buildGrid() {
        if (_edAgApi) {
          _edAgApi.setGridOption("rowData", rows);
          _edAgApi.redrawRows();
          return;
        }
        el.innerHTML = "";
        var wrap = document.createElement("div");
        wrap.className = "ag-theme-alpine";
        wrap.style.cssText = "height:320px;width:100%;font-size:0.82em";
        el.appendChild(wrap);
        _edAgApi = agGrid.createGrid(wrap, {
          columnDefs: [{ field: "file", headerName: "📄 File", flex: 1 }],
          rowData: rows,
          rowHeight: 26,
          headerHeight: 28,
          defaultColDef: { sortable: true, filter: true, resizable: false },
          getRowStyle: function (p) {
            return p.data.path === _curFile
              ? { background: "#e8f2ff", color: "#004fa0", fontWeight: "600" } : {};
          },
          onRowClicked: function (e) { loadFile(e.data.path); }
        });
      }
      if (window.agGrid && window.agGrid.createGrid) { buildGrid(); return; }
      if (window.lcLoadAgGrid) { window.lcLoadAgGrid(buildGrid); return; }
      /* standalone fallback */
      function addCss(h) { var l=document.createElement("link"); l.rel="stylesheet"; l.href=h; document.head.appendChild(l); }
      addCss("https://cdn.jsdelivr.net/npm/ag-grid-community@31/styles/ag-grid.css");
      addCss("https://cdn.jsdelivr.net/npm/ag-grid-community@31/styles/ag-theme-alpine.css");
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/ag-grid-community@31/dist/ag-grid-community.min.js";
      s.onload = buildGrid;
      document.head.appendChild(s);
    }).catch(function () {
      if (el) el.innerHTML = "<span style='color:#dc3545;font-size:0.85em'>Network error</span>";
    });
  }

  /* ── Open a file ─────────────────────────────────────── */
  function loadFile(path) {
    if (_dirty && !confirm("Discard unsaved changes to " + (_curFile || "this file") + "?")) return;
    _curFile = path; _curSha = null;
    setDirty(false);
    var inp = document.getElementById("ed-input");
    if (inp) inp.value = "Loading…";
    document.querySelectorAll(".ed-chip").forEach(function (c) {
      c.classList.toggle("active", c.dataset.path === path);
    });
    gh("GET", "/contents/" + path, null, function (data) {
      if (!data.content) { toast("Load failed: " + esc(data.message || ""), false); return; }
      _curSha = data.sha;
      var content = b64d(data.content.replace(/\n/g, ""));
      if (inp) { inp.value = content; updatePreview(content); }
      setDirty(false);
      loadHistory();
    });
  }

  /* ── Save ────────────────────────────────────────────── */
  function saveFile() {
    if (!_curFile) { toast("No file selected.", false); return; }
    if (!_pat || !_repo) { toast("Not connected.", false); return; }
    var inp = document.getElementById("ed-input");
    if (!inp) return;
    /* verify write access before bothering the user with a prompt */
    fetch("https://api.github.com/repos/" + _repo, {
      headers: { Authorization: "Bearer " + _pat }
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (!d.full_name) { toast("Repo not found: " + esc(_repo), false); return; }
      if (d.permissions && !d.permissions.push) {
        toast("No write access to " + esc(d.full_name) + " — use your fork.", false); return;
      }
      var msg = prompt("Commit message:", (_curSha ? "Update " : "Add ") + _curFile.split("/").pop());
      if (msg === null) return;
      if (!msg.trim()) msg = (_curSha ? "Update " : "Add ") + _curFile.split("/").pop();
      var body = { message: msg, content: b64e(inp.value), branch: "main" };
      if (_curSha) body.sha = _curSha;
      gh("PUT", "/contents/" + _curFile, body, function (data) {
        if (!data.content) { toast("Save failed (" + esc(_curFile) + "): " + esc(data.message || JSON.stringify(data)), false); return; }
        _curSha = data.content.sha;
        toast("Saved · " + data.commit.sha.slice(0, 7) + " ✓", true);
        setDirty(false);
        loadFiles();
        loadHistory();
        watchBuild(data.commit.sha);
      });
    });
  }

  /* ── New page ────────────────────────────────────────── */
  function newPage() {
    var name = prompt("New page filename (e.g. my-topic.md):");
    if (!name) return;
    if (!name.endsWith(".md")) name += ".md";
    _curFile = "docs/" + name; _curSha = null;
    var title = name.replace(/\.md$/, "").replace(/[-_]/g, " ")
      .replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    var content = "# " + title + "\n\n**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.\n\n";
    var inp = document.getElementById("ed-input");
    if (inp) { inp.value = content; updatePreview(content); }
    setDirty(true);
    var eh = document.getElementById("ed-history");
    if (eh) eh.innerHTML = "<span style='color:#bbb'>Save to start tracking history.</span>";
  }

  /* ── Live preview ────────────────────────────────────── */
  // Ensure a blank line before every {: ... } IAL line so that marked.parse()
  // renders it as its own <p> (kramdown handles this natively; marked does not).
  // Code fence interiors are left untouched.
  function normIAL(src) {
    var lines = src.split('\n'), out = [], inFence = false, fenceChar = '', fenceLen = 0;
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i], t = line.trim();
      if (!inFence && (t.slice(0, 3) === '```' || t.slice(0, 3) === '~~~')) {
        inFence = true; fenceChar = t[0]; fenceLen = 0;
        while (fenceLen < t.length && t[fenceLen] === fenceChar) fenceLen++;
      } else if (inFence) {
        var cnt = 0;
        while (cnt < t.length && t[cnt] === fenceChar) cnt++;
        if (cnt >= fenceLen && t.slice(cnt).trim() === '') inFence = false;
      }
      if (!inFence && t.slice(0, 2) === '{:' && i > 0 && out.length && out[out.length - 1].trim() !== '') {
        out.push('');
      }
      out.push(line);
    }
    return out.join('\n');
  }

  function previewBar(out, state) {
    var bar = out.querySelector(".ed-pbar");
    if (!bar) {
      bar = document.createElement("div");
      out.insertBefore(bar, out.firstChild);
    }
    bar.className = "ed-pbar" + (state ? " " + state : "");
  }

  function updatePreview(text) {
    var out = document.getElementById("ed-preview");
    if (!out) return;
    var src = text !== undefined ? text
      : ((document.getElementById("ed-input") || {}).value || "");

    clearTimeout(_previewTimer);
    previewBar(out, "wait"); // immediate signal: heard the keystroke

    _previewTimer = setTimeout(function() {
      function doRender() {
        if (window.lcDestroyInstancesIn) window.lcDestroyInstancesIn(out);
        out.innerHTML = "";
        // Progress bar at "go" (will advance to "done" after render)
        var bar = document.createElement("div");
        bar.className = "ed-pbar go";
        out.appendChild(bar);
        // Render markdown into a child container
        var body = document.createElement("div");
        body.innerHTML = marked.parse(normIAL(src));
        out.appendChild(body);
        // Apply IAL markers then run the full component upgrade pipeline
        if (window.lcApplyIAL)    window.lcApplyIAL(body);
        if (window.lcScanElement) window.lcScanElement(body);
        // Advance bar to "done" on the next paint
        requestAnimationFrame(function() { bar.className = "ed-pbar done"; });
      }
      if (window.marked) { doRender(); return; }
      if (window.lcLoadMarked) { window.lcLoadMarked(doRender); return; }
      /* standalone fallback */
      if (window._edMQ) { window._edMQ.push(doRender); return; }
      window._edMQ = [doRender];
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/marked@9/marked.min.js";
      s.onload = function() { var q = window._edMQ; window._edMQ = null; q.forEach(function(f) { f(); }); };
      document.head.appendChild(s);
    }, text !== undefined ? 0 : 400);
  }

  /* ── Commit history ──────────────────────────────────── */
  function loadHistory() {
    var el = document.getElementById("ed-history");
    if (!el || !_curFile) return;
    el.innerHTML = "<span style='color:#bbb'>Loading…</span>";
    fetch("https://api.github.com/repos/" + _repo + "/commits?path=" + encodeURIComponent(_curFile) + "&per_page=8", {
      headers: { Authorization: "Bearer " + _pat }
    }).then(function (r) { return r.json(); }).then(function (commits) {
      if (!Array.isArray(commits) || !commits.length) {
        el.innerHTML = "<span style='color:#bbb'>No commits yet.</span>"; return;
      }
      el.innerHTML = commits.map(function (c) {
        var rel = timeAgo(new Date(c.commit.author.date));
        return "<div class='ed-commit'>"
          + "<div class='ed-commit-msg'>" + esc(c.commit.message.split("\n")[0]) + "</div>"
          + "<div class='ed-commit-meta'>" + rel + " · "
          + "<a href='#' class='ed-view' data-sha='" + c.sha + "' style='color:#0066cc'>diff</a></div>"
          + "</div>";
      }).join("");
    });
  }

  function timeAgo(d) {
    var s = Math.round((Date.now() - d) / 1000);
    if (s < 60) return s + "s ago";
    if (s < 3600) return Math.round(s / 60) + "m ago";
    if (s < 86400) return Math.round(s / 3600) + "h ago";
    return Math.round(s / 86400) + "d ago";
  }

  /* ── Diff against a historical commit ───────────────── */
  function viewDiff(sha) {
    var el = document.getElementById("ed-history");
    gh("GET", "/contents/" + _curFile + "?ref=" + sha, null, function (data) {
      if (!data.content) return;
      var older = b64d(data.content.replace(/\n/g, "")).split("\n");
      var inp = document.getElementById("ed-input");
      var newer = inp ? inp.value.split("\n") : [];
      var lines = [], max = Math.max(older.length, newer.length);
      for (var i = 0; i < max; i++) {
        var o = i < older.length ? older[i] : undefined;
        var n = i < newer.length ? newer[i] : undefined;
        if (o === undefined)  lines.push("<span class='ed-diff-add'>+ " + esc(n) + "</span>");
        else if (n === undefined) lines.push("<span class='ed-diff-del'>- " + esc(o) + "</span>");
        else if (o !== n) {
          lines.push("<span class='ed-diff-del'>- " + esc(o) + "</span>");
          lines.push("<span class='ed-diff-add'>+ " + esc(n) + "</span>");
        } else {
          lines.push("<span class='ed-diff-ctx'>  " + esc(o) + "</span>");
        }
      }
      el.insertAdjacentHTML("afterbegin",
        "<pre style='font-size:0.75em;overflow-x:auto;white-space:pre-wrap;margin:0 0 0.5em;padding:0.5em;background:#fafafa;border-radius:4px'>"
        + lines.join("") + "</pre><hr style='border:none;border-top:1px solid #eee;margin:0.4em 0'>");
    });
  }

  /* ── GitHub Actions build watcher ───────────────────── */
  function watchBuild(headSha) {
    var el = document.getElementById("ed-build");
    if (!el) return;
    el.innerHTML = "<span style='color:#888'>⏳ Queuing…</span>";
    var attempts = 0, timer = null;
    function check() {
      attempts++;
      if (attempts > 36) {
        clearInterval(timer);
        el.innerHTML = "<span style='color:#888'>⚠️ Timed out — <a href='https://github.com/" + _repo + "/actions' target='_blank' style='color:#0066cc'>check Actions</a></span>";
        return;
      }
      fetch("https://api.github.com/repos/" + _repo + "/actions/runs?per_page=20", {
        headers: { Authorization: "Bearer " + _pat }
      }).then(function (r) { return r.json(); }).then(function (data) {
        if (!data.workflow_runs) return;
        var run = data.workflow_runs.find(function (r) {
          return r.head_sha === headSha && r.name === "pages build and deployment";
        });
        if (!run) return; /* not registered yet */
        if (run.status === "completed") {
          clearInterval(timer);
          var ok = run.conclusion === "success";
          el.innerHTML = (ok ? "✅ Built · " : "❌ " + esc(run.conclusion) + " · ")
            + "<a href='" + run.html_url + "' target='_blank' style='color:#0066cc'>view run</a>";
        } else {
          var icon = run.status === "in_progress" ? "🔄" : "⏳";
          el.innerHTML = "<span style='color:#888'>" + icon + " " + esc(run.status) + "…</span>";
        }
      });
    }
    check();
    timer = setInterval(check, 5000);
  }

  /* ── Connect / Disconnect ────────────────────────────── */
  function connect() {
    var patEl = document.getElementById("ed-pat");
    var repoEl = document.getElementById("ed-repo");
    if (!patEl || !repoEl) return;
    _pat = patEl.value.trim(); _repo = repoEl.value.trim();
    if (!_pat || !_repo) { setStatus("Enter both fields.", false); return; }
    setStatus("Verifying…", null);
    fetch("https://api.github.com/repos/" + _repo, {
      headers: { Authorization: "Bearer " + _pat }
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (d.full_name) {
        if (d.permissions && !d.permissions.push) {
          setStatus("❌ Read-only: your PAT has no write access to " + esc(d.full_name) + ". Connect to your fork instead.", false);
          return;
        }
        localStorage.setItem(LS_PAT, _pat); localStorage.setItem(LS_REPO, _repo);
        setStatus("✓ " + d.full_name + (d.fork ? " (fork)" : ""), true);
        var setup = document.getElementById("ed-setup");
        if (setup) setup.open = false;
        toggleConnected(true);
        loadFiles();
        var fab = document.getElementById("ed-fab");
        if (fab && fab.dataset.pagePath) loadFile("docs/" + fab.dataset.pagePath);
      } else {
        setStatus("Failed: " + esc(d.message || "unknown error"), false);
      }
    });
  }

  function disconnect() {
    localStorage.removeItem(LS_PAT); localStorage.removeItem(LS_REPO);
    _pat = _repo = _curFile = _curSha = null;
    setStatus("Disconnected.", false);
    toggleConnected(false);
    var el;
    el = document.getElementById("ed-files"); if (el) el.innerHTML = "<span style='color:#bbb'>Connect to browse.</span>";
    el = document.getElementById("ed-history"); if (el) el.innerHTML = "<span style='color:#bbb'>Select a file.</span>";
    el = document.getElementById("ed-build"); if (el) el.textContent = "";
    setDirty(false);
    el = document.getElementById("ed-input"); if (el) el.value = "";
    el = document.getElementById("ed-preview"); if (el) el.innerHTML = "";
  }

  function toggleConnected(on) {
    var c = document.getElementById("ed-connect-btn");
    var d = document.getElementById("ed-disconnect-btn");
    if (c) c.style.display = on ? "none" : "";
    if (d) d.style.display = on ? "" : "none";
  }

  /* ── Event delegation ────────────────────────────────── */
  document.addEventListener("click", function (e) {
    var ct = e.target.closest || function(sel){ return null; };
    var fab    = e.target.closest("#ed-fab");
    var close  = e.target.closest("#ed-close-btn");
    var conn   = e.target.closest("#ed-connect-btn");
    var disc   = e.target.closest("#ed-disconnect-btn");
    var save   = e.target.closest("#ed-save-btn");
    var newp   = e.target.closest("#ed-new-btn");
    var zoom   = e.target.closest("#ed-zoom-btn");
    var chip   = e.target.closest(".ed-chip");
    var view   = e.target.closest(".ed-view");
    if (fab)   { e.preventDefault(); openDrawer(); return; }
    if (close) { e.preventDefault(); closeDrawer(); return; }
    if (conn)  { e.preventDefault(); connect(); return; }
    if (disc)  { e.preventDefault(); disconnect(); return; }
    if (save)  { e.preventDefault(); saveFile(); return; }
    if (newp)  { e.preventDefault(); newPage(); return; }
    if (zoom)  {
      e.preventDefault();
      var prev = document.getElementById("ed-preview");
      if (prev) { var on = prev.classList.toggle("lc-zoom"); zoom.textContent = on ? "100%" : "50%"; }
      return;
    }
    if (chip)  { e.preventDefault(); loadFile(chip.dataset.path); return; }
    if (view)  { e.preventDefault(); viewDiff(view.dataset.sha); return; }
  });
  document.addEventListener("input", function (e) {
    if (e.target.id === "ed-input") { setDirty(true); updatePreview(); }
  });
  window.addEventListener("beforeunload", function (e) {
    var d = document.getElementById("ed-drawer");
    if (_dirty && d && d.classList.contains("open")) { e.preventDefault(); e.returnValue = ""; }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeDrawer();
    if ((e.metaKey || e.ctrlKey) && e.key === "s") {
      var d = document.getElementById("ed-drawer");
      if (d && d.classList.contains("open")) { e.preventDefault(); saveFile(); }
    }
  });

  /* ── Sidebar toggle ─────────────────────────────────── */
  document.addEventListener("click", function(e) {
    var btn = e.target.closest("#ed-sidebar-toggle");
    if (!btn) return;
    var sb = document.getElementById("ed-sidebar");
    var open = sb.classList.toggle("ed-collapsed");
    btn.textContent = open ? "▶" : "◀";
  });

  /* ── Splitter drag (left ↔ preview) ─────────────────── */
  (function() {
    var sp = document.getElementById("ed-splitter");
    if (!sp) return;
    var dragging = false, startX = 0, startLW = 0, startRW = 0;
    sp.addEventListener("mousedown", function(e) {
      var left = document.getElementById("ed-left");
      var prev = document.getElementById("ed-preview");
      if (!left || !prev) return;
      dragging = true; startX = e.clientX;
      startLW = left.offsetWidth; startRW = prev.offsetWidth;
      sp.classList.add("ed-dragging");
      document.body.style.cursor = "col-resize";
      e.preventDefault();
    });
    document.addEventListener("mousemove", function(e) {
      if (!dragging) return;
      var left = document.getElementById("ed-left");
      var prev = document.getElementById("ed-preview");
      if (!left || !prev) return;
      var dx = e.clientX - startX;
      var lw = Math.max(150, startLW + dx);
      var rw = Math.max(150, startRW - dx);
      left.style.flex = "none"; left.style.width = lw + "px";
      prev.style.flex = "none"; prev.style.width = rw + "px";
    });
    document.addEventListener("mouseup", function() {
      if (!dragging) return;
      dragging = false;
      sp.classList.remove("ed-dragging");
      document.body.style.cursor = "";
    });
  })();

  /* ── Grid/form splitter drag (grid ↕ form) ──────────── */
  (function() {
    var sp = document.getElementById("ed-grid-splitter");
    if (!sp) return;
    var dragging = false, startY = 0, startGH = 0, startFH = 0;
    sp.addEventListener("mousedown", function(e) {
      var grid = document.getElementById("ed-grid");
      var form = document.getElementById("ed-block-form");
      if (!grid || !form) return;
      _gridSplitSet = true; // user has manually positioned, don't auto-init anymore
      dragging = true; startY = e.clientY;
      startGH = grid.offsetHeight; startFH = form.offsetHeight;
      sp.classList.add("ed-dragging");
      document.body.style.cursor = "row-resize";
      e.preventDefault();
    });
    document.addEventListener("mousemove", function(e) {
      if (!dragging) return;
      var grid = document.getElementById("ed-grid");
      var form = document.getElementById("ed-block-form");
      if (!grid || !form) return;
      var dy = e.clientY - startY;
      var gh = Math.max(60, startGH + dy);
      var fh = Math.max(60, startFH - dy);
      grid.style.flex = "none"; grid.style.height = gh + "px";
      form.style.height = fh + "px";
    });
    document.addEventListener("mouseup", function() {
      if (!dragging) return;
      dragging = false;
      sp.classList.remove("ed-dragging");
      document.body.style.cursor = "";
    });
  })();

  /* ── Blocks tab ──────────────────────────────────────── */
  var BLOCK_TYPES = ["block","blocks","carousel","menu","video","deploys","recorder",
    "lightnodes","quiz","pytutor","pyrun","slide","slides","folder","cards","transcript"];

  function escH(s) { return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
  function escA(s) { return (s||"").replace(/"/g,"&quot;"); }

  function parseBlocks(text) {
    var lines = text.split("\n"), blocks = [], pre = [], cur = null;
    var inFence = false, fenceChar = '', fenceLen = 0;
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i], t = line.trim();
      var fm = t.match(/^(`{3,}|~{3,})/);
      if (fm) {
        if (!inFence) {
          inFence = true; fenceChar = fm[1][0]; fenceLen = fm[1].length;
        } else {
          var cntF = 0;
          while (cntF < t.length && t[cntF] === fenceChar) cntF++;
          if (cntF >= fenceLen && t.slice(cntF).trim() === '') inFence = false;
        }
      }
      if (!inFence) {
        var hm = t.match(/^(#{1,6})\s+(.*)/);
        if (hm) {
          if (cur) blocks.push(cur);
          else if (pre.length) blocks.push({ preamble: true, lines: pre.slice(), level: 0, heading: "(preamble)", type: null, knobs: {} });
          pre = [];
          cur = { level: hm[1].length, heading: hm[2], lines: [line], type: null, knobs: {} };
          continue;
        }
      }
      if (cur) {
        cur.lines.push(line);
        if (!inFence) {
          var im = t.match(/^\{:\s*\.(\S+)\s*(.*?)\s*\}/);
          if (im) {
            cur.type = im[1]; cur.knobs = {};
            var kr = /(\w+)="([^"]*)"/g, km;
            while ((km = kr.exec(im[2]))) cur.knobs[km[1]] = km[2];
          }
        }
      } else { pre.push(line); }
    }
    if (cur) blocks.push(cur);
    else if (pre.length) blocks.push({ preamble: true, lines: pre, level: 0, heading: "(preamble)", type: null, knobs: {} });
    return blocks;
  }

  /* Split heading blocks that contain component paragraphs (paragraph + {: .type })
     into sub-block entries for display. Sub-blocks have subBlock:true and are
     skipped in blocksToText (their content is already in the parent's lines). */
  function extractSubBlocks(block) {
    if (block.preamble) return [block];
    var rest = block.lines.slice(1);
    var inF = false, fC = '', fL = 0;
    var chunk = [], subs = [];
    for (var i = 0; i < rest.length; i++) {
      var line = rest[i], t = line.trim();
      var fm = t.match(/^(`{3,}|~{3,})/);
      if (fm) {
        if (!inF) { inF = true; fC = fm[1][0]; fL = fm[1].length; }
        else { var c=0; while(c<t.length&&t[c]===fC)c++; if(c>=fL&&t.slice(c).trim()==='') inF=false; }
      }
      var im = !inF && t.match(/^\{:\s*\.(\S+)\s*(.*?)\s*\}/);
      if (im) {
        var content = chunk.filter(function(l){ return l.trim() && !/^\{:/.test(l.trim()); });
        if (content.length > 0) {
          var title = content[0].replace(/^\[([^\]]+)\].*/, '$1')
            .replace(/^[#*_`>[\]()]+/, '').trim().slice(0, 60) || '(component)';
          var kn = {}, kr2 = /(\w+)="([^"]*)"/g, km2;
          while ((km2 = kr2.exec(im[2]))) kn[km2[1]] = km2[2];
          subs.push({ level: block.level + 1, heading: title,
            lines: chunk.slice().concat([line]), type: im[1], knobs: kn, subBlock: true });
        }
        chunk = [];
      } else {
        chunk.push(line);
      }
    }
    if (subs.length > 0) {
      // IAL(s) belong to sub-components, not the section heading.
      // Mark parent so the grid hides the misleading type badge,
      // but keep block.type/block.lines intact so Apply can reconstruct correctly.
      block.hasSubComponents = true;
    }
    return subs.length > 0 ? [block].concat(subs) : [block];
  }

  function blocksToText(blocks) {
    return blocks.filter(function(b){ return !b.subBlock; })
      .map(function(b) { return b.lines.join("\n"); }).join("\n");
  }

  function blockContent(b) {
    if (b.preamble) return b.lines.join("\n");
    var ls = b.lines.slice(1);
    // Strip trailing blank lines, then trailing IAL, then trailing blank lines again
    // so that {: .foo }\n\n (blank before next heading) doesn't prevent IAL removal
    while (ls.length && ls[ls.length - 1].trim() === '') ls.pop();
    if (ls.length && /^\{:.*\}/.test(ls[ls.length - 1].trim())) ls.pop();
    while (ls.length && ls[ls.length - 1].trim() === '') ls.pop();
    return ls.join("\n").trim();
  }

  var _blocks = [], _selIdx = -1, _dragFrom = null, _gridSplitSet = false;

  /* Expand component sub-blocks: parse headings inside their first code fence
     and insert them as fenceChild display rows (display-only, no text reconstruction).
     Only runs for subBlock entries — parent heading rows are already excluded via
     hasSubComponents — so there is no duplication. Each fenceChild stores its
     own section lines so the form can show its content read-only. */
  function expandFenceHeadings(blocks) {
    var result = [];
    blocks.forEach(function(b) {
      result.push(b);
      if (!b.type || !b.subBlock) return; // only for component sub-block rows
      var inF = false, fC = '', fL = 0, fLines = [];
      for (var i = 0; i < b.lines.length; i++) {
        var t = b.lines[i].trim();
        var fm = t.match(/^(`{3,}|~{3,})/);
        if (fm) {
          if (!inF) { inF = true; fC = fm[1][0]; fL = fm[1].length; fLines = []; }
          else { var c=0; while(c<t.length&&t[c]===fC)c++; if(c>=fL&&t.slice(c).trim()==='') { inF=false; break; } }
        } else if (inF) { fLines.push(b.lines[i]); } // preserve original spacing
      }
      // Split fence content into per-heading sections
      var sections = [], cur = null;
      fLines.forEach(function(line) {
        var hm = line.trim().match(/^(#{1,6})\s+(.*)/);
        if (hm) {
          if (cur) sections.push(cur);
          cur = { heading: hm[2], lines: [line] };
        } else if (cur) {
          cur.lines.push(line);
        }
      });
      if (cur) sections.push(cur);
      sections.forEach(function(sec) {
        // Trim trailing blank lines from section content
        var ls = sec.lines.slice(1); // skip the heading line itself
        while (ls.length && ls[ls.length-1].trim() === '') ls.pop();
        result.push({ level: b.level + 1, heading: sec.heading, lines: ls,
          type: null, knobs: {}, subBlock: true, fenceChild: true });
      });
    });
    return result;
  }

  /* Scroll preview to and pulse-highlight the heading corresponding to block. */
  function highlightInPreview(block) {
    var prev = document.getElementById("ed-preview");
    if (!prev || !block || block.preamble) return;
    prev.querySelectorAll(".ed-hl-pulse").forEach(function(el){ el.classList.remove("ed-hl-pulse"); });
    var want = (block.heading || '').replace(/\s+/g, ' ').trim().slice(0, 40).toLowerCase();
    if (!want) return;
    var target = null;
    // Search headings + accordion/dt labels
    prev.querySelectorAll("h1,h2,h3,h4,h5,h6,summary,dt").forEach(function(h) {
      if (target) return;
      var t = h.textContent.replace(/\s+/g, ' ').trim().slice(0, 40).toLowerCase();
      if (t === want || (want.length > 4 && t.indexOf(want.slice(0, 20)) !== -1)) target = h;
    });
    // For sub-blocks with type: also try the component container itself
    if (!target && block.subBlock && block.type) {
      target = prev.querySelector('.' + block.type);
    }
    if (target) {
      void target.offsetWidth;
      target.classList.add("ed-hl-pulse");
      target.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  function buildGrid() {
    var inp = document.getElementById("ed-input");
    if (!inp) return;
    var raw = parseBlocks(inp.value);
    _blocks = [];
    raw.forEach(function(b){ _blocks = _blocks.concat(extractSubBlocks(b)); });
    _blocks = expandFenceHeadings(_blocks);
    var minLv = 9;
    _blocks.forEach(function(b){ if (!b.preamble && b.level < minLv) minLv = b.level; });
    if (minLv === 9) minLv = 1;

    var html = "<table><thead><tr>"
      + "<th style='width:18px'></th>"
      + "<th>Title</th>"
      + "<th style='width:110px'>Type</th>"
      + "<th>Knobs</th>"
      + "</tr></thead><tbody>";

    _blocks.forEach(function(b, i) {
      var indent = b.preamble ? 0 : (b.level - minLv) * 14;
      var titleHtml = b.preamble
        ? "<em style='color:#bbb'>preamble</em>"
        : (b.fenceChild ? "<span style='color:#aaa'>– " + escH(b.heading) + "</span>"
          : b.subBlock ? "<em style='color:#777'>" + escH(b.heading) + "</em>"
          : escH(b.heading));
      var typeHtml = (b.type && !b.hasSubComponents) ? "<span class='ed-block-type'>." + escH(b.type) + "</span>" : "";
      var knobHtml = Object.keys(b.knobs||{}).map(function(k){
        return "<span style='font-size:0.82em;color:#999'>" + escH(k) + "=<em>" + escH(b.knobs[k]) + "</em></span>";
      }).join(" ");
      var sel = i === _selIdx ? " ed-sel" : "";
      var draggable = b.subBlock ? "false" : "true";
      var handle = b.subBlock ? "<td style='color:#eee'>⠿</td>" : "<td class='ed-drag-handle'>⠿</td>";
      html += "<tr data-idx='" + i + "' draggable='" + draggable + "' class='" + sel + "'>"
        + handle
        + "<td style='padding-left:" + (8 + indent) + "px'>" + titleHtml + "</td>"
        + "<td>" + typeHtml + "</td>"
        + "<td>" + knobHtml + "</td>"
        + "</tr>";
    });
    html += "</tbody></table>";
    document.getElementById("ed-grid").innerHTML = html;

    if (_selIdx >= 0 && _selIdx < _blocks.length) {
      showBlockForm(_selIdx);
      highlightInPreview(_blocks[_selIdx]);
    }
  }

  /* wireGrid is called ONCE at init — uses event delegation on the persistent
     #ed-grid container. Calling it on every buildGrid() would accumulate
     duplicate listeners on each click (memory leak + slowdown). */
  function wireGrid() {
    var grid = document.getElementById("ed-grid");
    if (!grid) return;

    grid.addEventListener("click", function(e) {
      var tr = e.target.closest("tr[data-idx]");
      if (!tr) return;
      _selIdx = parseInt(tr.dataset.idx);
      buildGrid();
    });

    grid.addEventListener("dragstart", function(e) {
      var tr = e.target.closest("tr[data-idx]");
      if (!tr) return;
      var idx = parseInt(tr.dataset.idx);
      if (_blocks[idx] && _blocks[idx].subBlock) { e.preventDefault(); return; }
      _dragFrom = idx;
      tr.style.opacity = "0.45";
      e.dataTransfer.effectAllowed = "move";
    });
    grid.addEventListener("dragend", function(e) {
      var tr = e.target.closest("tr[data-idx]");
      if (tr) tr.style.opacity = "";
      grid.querySelectorAll(".ed-drag-over").forEach(function(r){ r.classList.remove("ed-drag-over"); });
      _dragFrom = null;
    });
    grid.addEventListener("dragover", function(e) {
      e.preventDefault();
      grid.querySelectorAll(".ed-drag-over").forEach(function(r){ r.classList.remove("ed-drag-over"); });
      var tr = e.target.closest("tr[data-idx]");
      if (tr) tr.classList.add("ed-drag-over");
    });
    grid.addEventListener("drop", function(e) {
      e.preventDefault();
      var tr = e.target.closest("tr[data-idx]");
      if (!tr || _dragFrom === null) return;
      var to = parseInt(tr.dataset.idx);
      if (_dragFrom === to) return;
      if (_blocks[to] && _blocks[to].subBlock) return;
      var moved = _blocks.splice(_dragFrom, 1)[0];
      _blocks.splice(to > _dragFrom ? to - 1 : to, 0, moved);
      _selIdx = to > _dragFrom ? to - 1 : to;
      var inp = document.getElementById("ed-input");
      var newText = blocksToText(_blocks);
      inp.value = newText; setDirty(true); updatePreview(newText);
      buildGrid();
    });
  }

  function initGridSplit() {
    if (_gridSplitSet) return;
    var pane = document.getElementById("ed-blocks-pane");
    var grid = document.getElementById("ed-grid");
    var form = document.getElementById("ed-block-form");
    if (!pane || !grid || !form) return;
    if (pane.offsetHeight < 10) {
      requestAnimationFrame(function() { initGridSplit(); });
      return;
    }
    _gridSplitSet = true;
    var half = Math.floor((pane.offsetHeight - 5) / 2);
    grid.style.flex = "none"; grid.style.height = half + "px";
    form.style.height = half + "px";
  }

  function showBlockForm(idx) {
    var b = _blocks[idx];
    var form = document.getElementById("ed-block-form");
    var sp   = document.getElementById("ed-grid-splitter");
    form.classList.add("ed-visible");
    if (sp) sp.classList.add("ed-vis");
    initGridSplit();

    if (b.fenceChild) {
      var hPrefix = "#".repeat(Math.min(b.level || 3, 6));
      var fcContent = hPrefix + " " + b.heading
        + ((b.lines && b.lines.length) ? "\n" + b.lines.join("\n").trim() : "");
      form.innerHTML = "<p class='ebf-meta' style='color:#888;margin:0 0 0.35em'>"
        + "<span style='color:#bbb;font-size:0.85em'>(fence item — edit via Raw tab)</span></p>"
        + "<div class='ebf-content-wrap'><textarea readonly>" + escH(fcContent) + "</textarea></div>";
      return;
    }
    if (b.subBlock) {
      form.innerHTML = "<p class='ebf-meta' style='color:#888;margin:0 0 0.4em'><em>Component block (edit via Raw tab)</em></p>"
        + "<div class='ebf-meta'><label>Type</label><input readonly value='." + escH(b.type||'') + "'></div>"
        + "<div class='ebf-content-wrap'><label>Content</label>"
        + "<textarea readonly>" + escH(b.lines.filter(function(l){ return l.trim() && !/^\{:/.test(l.trim()); }).join("\n").trim()) + "</textarea></div>";
      return;
    }
    var knobStr = Object.keys(b.knobs||{}).map(function(k){ return k + '="' + b.knobs[k] + '"'; }).join(" ");
    var content = blockContent(b);
    form.innerHTML = "<div class='ebf-meta' style='display:flex;gap:0.6em;flex-wrap:wrap;margin-bottom:0.4em'>"
      + "<div style='flex:3;min-width:100px'><label>Heading</label><input id='ebf-title' value='" + escA(b.heading||"") + "'></div>"
      + "<div style='flex:1;min-width:90px'><label>Type</label><select id='ebf-type'>"
      + "<option value=''>(none)</option>"
      + BLOCK_TYPES.map(function(t){ return "<option value='" + t + "'" + (b.type===t?" selected":"") + ">." + t + "</option>"; }).join("")
      + "</select></div>"
      + "<div style='flex:2;min-width:120px'><label>Knobs</label><input id='ebf-knobs' value='" + escA(knobStr) + "' placeholder='count=\"5\"'></div>"
      + "</div>"
      + "<div class='ebf-content-wrap'><label>Content</label>"
      + "<textarea id='ebf-content'>" + escH(content) + "</textarea></div>"
      + "<div class='ebf-actions'><a href='#' class='lc-btn' id='ebf-apply' style='font-size:0.82em;padding:0.32em 0.9em'>Apply</a></div>";

    document.getElementById("ebf-apply").addEventListener("click", function(e) {
      e.preventDefault();
      var title   = document.getElementById("ebf-title").value;
      var type    = document.getElementById("ebf-type").value;
      var knobsIn = document.getElementById("ebf-knobs").value.trim();
      var cnt     = document.getElementById("ebf-content").value;
      var prefix  = "#".repeat(b.level || 1);
      var newLines = [prefix + " " + title];
      if (cnt.trim()) newLines.push("", cnt.trim());
      if (type) newLines.push("{: ." + type + (knobsIn ? " " + knobsIn : "") + " }");
      b.heading = title; b.type = type || null;
      b.knobs = {}; var kr2 = /(\w+)="([^"]*)"/g, km2;
      while ((km2 = kr2.exec(knobsIn))) b.knobs[km2[1]] = km2[2];
      b.lines = newLines;
      var inp = document.getElementById("ed-input");
      var newText = blocksToText(_blocks);
      inp.value = newText; setDirty(true); updatePreview(newText);
      buildGrid();
    });
  }

  /* Tab switching */
  document.addEventListener("click", function(e) {
    var tab = e.target.closest(".ed-tab");
    if (!tab) return;
    var name = tab.dataset.tab;
    document.querySelectorAll(".ed-tab").forEach(function(t){ t.classList.toggle("active", t.dataset.tab === name); });
    var raw    = document.getElementById("ed-raw-pane");
    var blocks = document.getElementById("ed-blocks-pane");
    if (name === "blocks") {
      raw.classList.add("ed-hidden"); blocks.classList.add("ed-active");
      buildGrid();
    } else {
      raw.classList.remove("ed-hidden"); blocks.classList.remove("ed-active");
    }
  });

  /* ── Raw editor cursor → preview highlight ──────────── */
  (function() {
    var _cursorTimer = null;
    function onRawCursor() {
      clearTimeout(_cursorTimer);
      _cursorTimer = setTimeout(function() {
        var inp = document.getElementById("ed-input");
        if (!inp || !_blocks.length) return;
        var pos = inp.selectionStart;
        var before = inp.value.substring(0, pos).split("\n").length - 1;
        var cumul = 0;
        for (var i = 0; i < _blocks.length; i++) {
          if (_blocks[i].subBlock) continue;
          var blen = _blocks[i].lines.length;
          if (before >= cumul && before < cumul + blen) {
            highlightInPreview(_blocks[i]); break;
          }
          cumul += blen;
        }
      }, 250);
    }
    document.addEventListener("click",  function(e){ if (e.target.id === "ed-input") onRawCursor(); });
    document.addEventListener("keyup",  function(e){ if (e.target.id === "ed-input") onRawCursor(); });
  })();

  /* ── Preview hover → editor highlight ──────────────── */
  (function() {
    var _prevHoverTimer = null;
    document.addEventListener("mousemove", function(e) {
      var prev = document.getElementById("ed-preview");
      if (!prev || !prev.contains(e.target)) return;
      clearTimeout(_prevHoverTimer);
      _prevHoverTimer = setTimeout(function() {
        if (!_blocks.length) return;
        var node = e.target, matchIdx = -1, done = false;
        while (node && node !== prev && !done) {
          var tag = (node.tagName || "").toLowerCase();
          if (/^h[1-6]$/.test(tag) || tag === "summary" || tag === "dt") {
            var want = node.textContent.replace(/\s+/g, ' ').trim().slice(0, 40).toLowerCase();
            for (var i = 0; i < _blocks.length && !done; i++) {
              var bh = (_blocks[i].heading || '').replace(/\s+/g, ' ').trim().slice(0, 40).toLowerCase();
              if (bh && want && (bh === want || (bh.length > 4 && want.indexOf(bh.slice(0, 20)) !== -1))) {
                matchIdx = i; done = true;
              }
            }
          }
          if (!done && node.classList) {
            for (var ci = 0; ci < BLOCK_TYPES.length && !done; ci++) {
              if (node.classList.contains(BLOCK_TYPES[ci])) {
                for (var i = 0; i < _blocks.length && !done; i++) {
                  if (_blocks[i].type === BLOCK_TYPES[ci]) { matchIdx = i; done = true; }
                }
              }
            }
          }
          node = node.parentElement;
        }
        if (matchIdx < 0) return;
        // Sync Blocks grid if that tab is active
        var blocksPane = document.getElementById("ed-blocks-pane");
        if (blocksPane && blocksPane.classList.contains("ed-active")) {
          if (_selIdx !== matchIdx) {
            _selIdx = matchIdx; buildGrid();
            var tr = document.querySelector("#ed-grid tr.ed-sel");
            if (tr) tr.scrollIntoView({ block: "nearest" });
          }
          return;
        }
        // Sync Raw tab: scroll to approximate position without stealing focus
        var inp = document.getElementById("ed-input");
        if (!inp || document.activeElement === inp) return;
        var cumul = 0;
        for (var i = 0; i < matchIdx; i++) {
          if (!_blocks[i].subBlock) cumul += _blocks[i].lines.length;
        }
        var totalLines = Math.max(1, inp.value.split("\n").length);
        inp.scrollTop = (cumul / totalLines) * inp.scrollHeight;
      }, 300);
    });
  })();

  /* ── Restore session from localStorage ───────────────── */
  document.addEventListener("DOMContentLoaded", function () {
    _pat  = localStorage.getItem(LS_PAT);
    _repo = localStorage.getItem(LS_REPO);
    var patEl = document.getElementById("ed-pat");
    var repoEl = document.getElementById("ed-repo");
    if (patEl && _pat)   patEl.value  = _pat;
    if (repoEl && _repo) repoEl.value = _repo;
    if (_pat && _repo) {
      setStatus("✓ " + _repo, true);
      toggleConnected(true);
    }
    wireGrid(); // wire grid event delegation once, not on every buildGrid()
  });
})();
</script>
{% endif %}
