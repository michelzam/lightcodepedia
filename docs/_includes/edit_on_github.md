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
#ed-main { flex: 1; display: flex; overflow: hidden; }
#ed-input {
  flex: 1; border: none; border-right: 1px solid #e0e0e0; resize: none;
  font-family: monospace; font-size: 0.88em; padding: 1em; line-height: 1.6;
  outline: none; background: #fdfcfb;
}
#ed-preview { flex: 1; overflow-y: auto; padding: 1em 1.5em; position: relative; }
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
  #ed-preview { display: none; }
}

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
    <span id="ed-filename">No file selected</span>
    <span id="ed-build" style="font-size:0.78em;color:#888;margin-left:0.5em;flex-shrink:0"></span>
    <a href="#" class="lc-btn lc-btn-secondary" id="ed-new-btn" style="font-size:0.82em;padding:0.35em 0.9em;margin-left:auto">+ New</a>
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
      <textarea id="ed-input" placeholder="Select a file from the sidebar, or create a new page…" spellcheck="false"></textarea>
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
        body.innerHTML = marked.parse(src);
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
    var chip   = e.target.closest(".ed-chip");
    var view   = e.target.closest(".ed-view");
    if (fab)   { e.preventDefault(); openDrawer(); return; }
    if (close) { e.preventDefault(); closeDrawer(); return; }
    if (conn)  { e.preventDefault(); connect(); return; }
    if (disc)  { e.preventDefault(); disconnect(); return; }
    if (save)  { e.preventDefault(); saveFile(); return; }
    if (newp)  { e.preventDefault(); newPage(); return; }
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
  });
})();
</script>
{% endif %}
