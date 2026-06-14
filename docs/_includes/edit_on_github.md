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
  display: flex; flex-direction: column; overflow: hidden;
  opacity: 0; visibility: hidden; pointer-events: none;
  transform: scale(0.98) translateY(6px);
  transition: opacity 0.35s ease, visibility 0.35s, transform 0.45s cubic-bezier(0.22,1,0.36,1);
}
#ed-drawer.open {
  opacity: 1; visibility: visible; pointer-events: auto;
  transform: none;
}
#ed-top {
  display: flex; align-items: center; gap: 0.6em; padding: 0.7em 1em;
  border-bottom: 1px solid #e0e0e0; background: #fafafa; flex-shrink: 0;
  min-height: 52px;
}
#ed-filename {
  font-family: monospace; font-size: 0.85em; color: #555;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 220px;
}
/* ── Files dropdown trigger ──────────────────────── */
#ed-files-btn {
  position: relative; display: flex; align-items: center; gap: 0.35em;
  cursor: pointer; padding: 0.25em 0.55em; border-radius: 5px;
  border: 1px solid transparent; flex-shrink: 0;
  transition: border-color 0.12s, background 0.12s;
}
#ed-files-btn:hover { border-color: #d0d0d0; background: #f5f5f5; }
#ed-files-btn.ed-open { border-color: #0066cc; background: #f0f6ff; }
#ed-files-arrow { font-size: 0.65em; color: #aaa; transition: transform 0.15s; flex-shrink: 0; }
#ed-files-btn.ed-open #ed-files-arrow { transform: rotate(180deg); }
#ed-body { display: flex; flex: 1; overflow: hidden; }
/* ── Sidebar as dropdown panel ───────────────────── */
#ed-sidebar {
  position: absolute; top: calc(100% + 2px); left: 0; z-index: 300;
  width: 280px; max-height: 72vh; overflow-y: auto;
  background: #fff; border: 1px solid #d8d8d8; border-radius: 0 6px 6px 6px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.13); padding: 0.8em 0.7em; font-size: 0.85em;
  opacity: 0; visibility: hidden; transform: translateY(-6px);
  transition: opacity 0.15s ease, visibility 0.15s, transform 0.18s ease;
}
#ed-sidebar.ed-open { opacity: 1; visibility: visible; transform: none; }
#ed-main { flex: 1; display: flex; flex-direction: row; overflow: hidden; }
#ed-left { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 200px; }
#ed-input {
  flex: 1; border: none; resize: none;
  font-family: monospace; font-size: 0.88em; padding: 1em; line-height: 1.6;
  outline: none; background: #fdfcfb;
}
#ed-preview { flex: 1; overflow-y: auto; overflow-x: hidden; padding: 1em 1.5em; position: relative; border-right: 1px solid #e0e0e0; box-sizing: border-box; }
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
  #ed-splitter { display: none; }
  #ed-preview { display: none; }
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
#ed-log-pane { display: flex; flex: 1; flex-direction: column; overflow: auto; padding: 0.4em; }
#ed-log-pane.ed-hidden { display: none; }
#ed-diagram-pane { display: flex; flex: 1; flex-direction: column; overflow: auto; padding: 0.6em; }
#ed-diagram-pane.ed-hidden { display: none; }
#ed-diagram-pane .ed-diagram-wrap { overflow: auto; flex: 1; }
#ed-diagram-pane .ed-diagram-wrap svg { max-width: 100%; height: auto; }
#ed-diagram-legend { font-size: 0.76em; color: #9ca3af; padding: 0.3em 0.2em 0.5em; }
#ed-diagram-legend b { color: #6b7280; font-weight: 600; }
/* ── Features tab ─────────────────────────────────────── */
#ed-features-pane { display: flex; flex: 1; flex-direction: column; overflow: hidden; }
#ed-features-pane.ed-hidden { display: none; }
#ed-feat-bar { flex: none; display: flex; align-items: center; gap: 0.7em; padding: 0.45em 0.6em; border-bottom: 1px solid #f0f0f0; }
#ed-feat-bar .lc-btn { font-size: 0.82em; padding: 0.3em 0.85em; }
#ed-feat-bar-note { font-size: 0.78em; color: #9ca3af; }
#ed-feat-grid { flex: 1; min-height: 60px; overflow: auto; }
#ed-feat-grid table { width: 100%; border-collapse: collapse; font-size: 0.86em; }
#ed-feat-grid th, #ed-feat-grid td { text-align: left; padding: 0.4em 0.6em; border-bottom: 1px solid #f0f0f0; }
#ed-feat-grid th { color: #6b7280; font-weight: 600; position: sticky; top: 0; background: #fafafa; }
#ed-feat-grid tr[data-fi] { cursor: pointer; }
#ed-feat-grid tr[data-fi]:hover td { background: #f8f8f8; }
#ed-feat-grid tr.ed-fsel td { background: #e8f2ff; }
.ed-fstatus { display: inline-flex; align-items: center; gap: 0.3em; padding: 0.08em 0.55em; border-radius: 99px; font-size: 0.82em; font-weight: 500; }
.ed-fstatus.passing { background: #dcfce7; color: #15803d; }
.ed-fstatus.failing { background: #fee2e2; color: #b91c1c; }
.ed-fstatus.pending { background: #fef3c7; color: #92400e; }
.ed-fstatus.none    { background: #f1f5f9; color: #64748b; }
#ed-feat-splitter { height: 1px; background: #e5e7eb; flex: none; margin: 0.3em 0; }
#ed-feat-preview { flex: 1; min-height: 80px; overflow: auto; padding: 0.3em 0.6em; }
#ed-feat-preview:empty::before { content: "Select a feature to preview it live — run it, and its status is saved with the page."; color: #bbb; font-size: 0.85em; display: block; padding: 1em; }
.ed-log-item { border-bottom: 1px solid #f0f0f0; padding: 0.45em 0.35em; }
.ed-log-instr { font-size: 0.9em; color: #1f2937; }
.ed-log-meta { font-size: 0.78em; color: #9ca3af; margin-top: 0.15em; }
.ed-log-undo { float: right; font-size: 0.82em; color: #0066cc; text-decoration: none; }
.ed-log-undo:hover { text-decoration: underline; }
/* ── ✨ AI edit dialog ─────────────────────────────────── */
/* floating, non-modal: drag by the header, click elsewhere to re-scope */
#ed-agent-dialog { position: fixed; top: 100px; right: 24px; z-index: 1001; width: min(420px, 92vw); }
#ed-agent-dialog.ed-hidden { display: none; }
#ed-ag-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.28); padding: 0.8em 0.9em; display: flex;
  flex-direction: column; gap: 0.55em; max-height: 78vh; overflow: auto; }
#ed-ag-head { font-weight: 600; display: flex; align-items: center; gap: 0.4em;
  cursor: move; user-select: none; }
#ed-ag-scope { font-weight: 400; font-size: 0.84em; color: #6b7280; flex: 1; }
#ed-ag-x { color: #9ca3af; text-decoration: none; font-size: 1.1em; }
#ed-agent-prompt { resize: vertical; min-height: 3.4em; font: inherit; font-size: 0.92em;
  border: 1px solid #d0d7de; border-radius: 6px; padding: 0.55em; line-height: 1.45; }
#ed-ag-actions { display: flex; align-items: center; gap: 0.8em; }
#ed-agent-status { font-size: 0.84em; color: #777; }
#ed-agent-status.ed-err { color: #b91c1c; }
#ed-ag-plan.ed-hidden { display: none; }
.ed-ag-exp { font-size: 0.9em; color: #1f2937; background: #f1f5ff; border: 1px solid #dbe4ff;
  border-radius: 6px; padding: 0.5em 0.7em; margin: 0 0 0.5em; line-height: 1.45; }
.ed-ag-planhead { font-size: 0.82em; color: #6b7280; margin-bottom: 0.3em; }
.ed-ag-edit { font-family: monospace; font-size: 0.82em; border: 1px solid #eee;
  border-radius: 6px; margin: 0.3em 0; overflow: hidden; }
.ed-ag-del { background: #fef2f2; color: #b91c1c; padding: 0.25em 0.5em; white-space: pre-wrap; }
.ed-ag-add { background: #f0fdf4; color: #166534; padding: 0.25em 0.5em; white-space: pre-wrap; }
.ed-ag-skip { font-size: 0.8em; color: #b45309; margin: 0.3em 0 0; }
.ed-ag-approve { display: flex; gap: 0.6em; margin-top: 0.5em; }

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
  flex-shrink: 0; padding: 0; background: #fafafa;
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
/* .ebf-scroll wraps all scrollable form content; .ebf-actions sits outside it, always visible */
.ebf-scroll { flex: 1; overflow-y: auto; min-height: 0; padding: 0.8em 1em 0.2em; display: flex; flex-direction: column; }
.ebf-meta { flex-shrink: 0; }
.ebf-content-wrap { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.ebf-actions { flex-shrink: 0; padding: 0.4em 1em 0.5em; border-top: 1px solid #e8e8e8; background: #fafafa; }

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
    <!-- Filename acts as dropdown trigger for file browser -->
    <div id="ed-files-btn" title="Browse files">
      <span id="ed-filename">No file selected</span>
      <span id="ed-files-arrow">▼</span>

      <!-- Dropdown panel: connect + file list + history -->
      <div id="ed-sidebar">
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
        <span class="ed-section-label">Pages</span>
        <div id="ed-files" style="color:#bbb">Connect to browse.</div>
        <span class="ed-section-label">History</span>
        <div id="ed-history" style="color:#bbb">Select a file.</div>
      </div><!-- /sidebar dropdown -->
    </div><!-- /files-btn -->

    <span id="ed-build" style="font-size:0.78em;color:#888;margin-left:0.5em;flex-shrink:0"></span>
    <a href="#" class="lc-btn lc-btn-secondary" id="ed-zoom-btn" title="Toggle 50% preview scale" style="font-size:0.82em;padding:0.35em 0.9em;margin-left:auto">50%</a>
    <a href="#" class="lc-btn lc-btn-secondary" id="ed-new-btn" style="font-size:0.82em;padding:0.35em 0.9em">+ New</a>
    <a href="#" class="lc-btn lc-btn-secondary" id="ed-agent-btn" title="Ask AI to change the selected block (✨)" style="font-size:0.82em;padding:0.35em 0.7em">✨</a>
    <a href="#" class="lc-btn" id="ed-save-btn" style="font-size:0.82em;padding:0.35em 0.9em">💾 Save</a>
    <a href="#" id="ed-close-btn" title="Close (Esc)"
       style="font-size:1.3em;color:#888;text-decoration:none;padding:0 0.2em;line-height:1;margin-left:0.2em">✕</a>
  </div>

  <!-- Body: preview + editor only -->
  <div id="ed-body">
    <div id="ed-main">
      <div id="ed-preview"></div>
      <div id="ed-splitter"></div>
      <div id="ed-left">
        <div id="ed-tabs">
          <span class="ed-tab active" data-tab="blocks">⊞ Blocks</span>
          <span class="ed-tab" data-tab="raw">✏️ Raw</span>
          <span class="ed-tab" data-tab="features">🧪 Features</span>
          <span class="ed-tab" data-tab="diagram">🗺️ Diagram</span>
          <span class="ed-tab" data-tab="log">📝 Log</span>
        </div>
        <div id="ed-raw-pane" class="ed-hidden">
          <textarea id="ed-input" placeholder="Select a file to start editing…" spellcheck="false"></textarea>
        </div>
        <div id="ed-features-pane" class="ed-hidden">
          <div id="ed-feat-bar">
            <a href="#" class="lc-btn" id="ed-feat-runall">▶ Run all</a>
            <span id="ed-feat-bar-note">selecting a row scrolls to it; ▶ Run all runs the whole suite</span>
          </div>
          <div id="ed-feat-grid"><p style="color:#bbb;padding:1em">No features on this page. A <code>{: .feature }</code> block appears here.</p></div>
          <div id="ed-feat-splitter"></div>
          <div id="ed-feat-preview"></div>
        </div>
        <div id="ed-diagram-pane" class="ed-hidden">
          <p style="color:#bbb;padding:1em">Load a file to see its class diagram.</p>
        </div>
        <div id="ed-log-pane" class="ed-hidden">
          <div id="ed-log"><p style="color:#bbb;padding:1em">No AI edits yet. Select a block or text, then ✨ to ask for a change.</p></div>
        </div>
        <div id="ed-blocks-pane" class="ed-active">
          <div id="ed-grid"><p style="color:#bbb;padding:1em">Load a file to see its blocks.</p></div>
          <div id="ed-grid-splitter"></div>
          <div id="ed-block-form"></div>
        </div>
      </div>
    </div>
  </div><!-- /body -->

  <!-- ✨ AI edit dialog (scoped to the current selection) -->
  <div id="ed-agent-dialog" class="ed-hidden">
    <div id="ed-ag-card">
      <div id="ed-ag-head">✨ Ask AI <span id="ed-ag-scope"></span><a href="#" id="ed-ag-x" title="Close">✕</a></div>
      <textarea id="ed-agent-prompt" spellcheck="false"
        placeholder="Describe the change to this block — e.g. “remove the ! from the title”, “make the intro one sentence shorter”. The model proposes exact edits you approve before anything changes."></textarea>
      <div id="ed-ag-actions">
        <a href="#" class="lc-btn" id="ed-agent-ask">✨ Plan the change</a>
        <span id="ed-agent-status"></span>
      </div>
      <div id="ed-ag-plan" class="ed-hidden"></div>
    </div>
  </div>
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
  var _pat, _repo, _curFile, _curSha, _dirty = false, _previewTimer = null, _savedContent = null;

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

    // Clear any stale inline styles from previous opens
    var left = document.getElementById("ed-left");
    var prev = document.getElementById("ed-preview");
    if (left) { left.style.transition = ""; left.style.flex = ""; left.style.width = ""; left.style.overflow = ""; }
    if (prev) { prev.style.flex = ""; prev.style.width = ""; }

    d.classList.add("open");
    document.body.style.overflow = "hidden";

    // Blocks tab is always the default view on open
    var rawPane = document.getElementById("ed-raw-pane");
    var blkPane = document.getElementById("ed-blocks-pane");
    document.querySelectorAll(".ed-tab").forEach(function(t){ t.classList.toggle("active", t.dataset.tab === "blocks"); });
    if (rawPane) rawPane.classList.add("ed-hidden");
    if (blkPane) blkPane.classList.add("ed-active");
    var logPane = document.getElementById("ed-log-pane");
    if (logPane) logPane.classList.add("ed-hidden");
    var featPane = document.getElementById("ed-features-pane");
    if (featPane) featPane.classList.add("ed-hidden");
    var diagPane = document.getElementById("ed-diagram-pane");
    if (diagPane) diagPane.classList.add("ed-hidden");
    var agDlg = document.getElementById("ed-agent-dialog");
    if (agDlg) agDlg.classList.add("ed-hidden");
    loadCompModel(); // fetch type→icon map (once)
    buildGrid(); // always build — shows placeholder if no file yet

    if (_pat && _repo) {
      loadFiles();
      if (!_curFile) {
        var pagePath = (document.getElementById("ed-fab") || {}).dataset.pagePath;
        if (pagePath) loadFile("docs/" + pagePath);
      }
    }
  }
  function closeDrawer() {
    if (_dirty && !confirm("Discard unsaved changes to " + (_curFile || "this file") + "?")) return;
    if (_dirty && _savedContent !== null) {
      var inp = document.getElementById("ed-input");
      if (inp) { inp.value = _savedContent; updatePreview(_savedContent); }
      _blocks = []; _selIdx = -1; buildGrid();
    }
    setDirty(false);
    var d = document.getElementById("ed-drawer");
    if (d) d.classList.remove("open");
    setTimeout(function() { document.body.style.overflow = ""; }, 260);
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
    _actionLog = []; renderLog();  // each file gets its own action log
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
      _savedContent = content;
      if (inp) { inp.value = content; updatePreview(content); }
      setDirty(false);
      loadHistory();
      // refresh blocks grid whenever new content loads
      var blkPane = document.getElementById("ed-blocks-pane");
      if (blkPane && blkPane.classList.contains("ed-active")) buildGrid();
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
      var fallback = (_curSha ? "Update " : "Add ") + _curFile.split("/").pop();
      var msg = prompt("Commit message:", logCommitMessage() || fallback);
      if (msg === null) return;
      if (!msg.trim()) msg = fallback;
      var body = { message: msg, content: b64e(inp.value), branch: "main" };
      if (_curSha) body.sha = _curSha;
      gh("PUT", "/contents/" + _curFile, body, function (data) {
        if (!data.content) { toast("Save failed (" + esc(_curFile) + "): " + esc(data.message || JSON.stringify(data)), false); return; }
        _curSha = data.content.sha;
        _savedContent = inp.value;
        toast("Saved · " + data.commit.sha.slice(0, 7) + " ✓", true);
        pushAction("💾", "Saved · " + data.commit.sha.slice(0, 7), null);  // trace (no undo)
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
      if (attempts > 60) {
        clearInterval(timer);
        el.innerHTML = "✅ Saved · <span style='color:#888'>build watch timed out — <a href='https://github.com/" + _repo + "/actions' target='_blank' style='color:#0066cc'>check Actions</a></span>";
        return;
      }
      fetch("https://api.github.com/repos/" + _repo + "/actions/runs?per_page=20", {
        headers: { Authorization: "Bearer " + _pat }
      }).then(function (r) { return r.json(); }).then(function (data) {
        if (!data.workflow_runs) return;
        // Match by commit SHA only — workflow name varies per repo
        var run = data.workflow_runs.find(function (r) {
          return r.head_sha === headSha;
        });
        if (!run) return; /* run not registered yet, keep polling */
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
    timer = setInterval(check, 3000);
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

  /* ── Files dropdown toggle ──────────────────────────── */
  document.addEventListener("click", function(e) {
    var btn = e.target.closest("#ed-files-btn");
    var sb  = document.getElementById("ed-sidebar");
    var fbtn = document.getElementById("ed-files-btn");
    if (btn && sb) {
      // Ignore clicks that landed inside the dropdown panel itself
      if (e.target.closest("#ed-sidebar")) return;
      var nowOpen = sb.classList.toggle("ed-open");
      if (fbtn) fbtn.classList.toggle("ed-open", nowOpen);
    } else if (sb && sb.classList.contains("ed-open")) {
      if (!e.target.closest("#ed-sidebar")) {
        sb.classList.remove("ed-open");
        if (fbtn) fbtn.classList.remove("ed-open");
      }
    }
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
      // Freeze both panes to current pixel widths so flex doesn't interfere
      startLW = left.offsetWidth; startRW = prev.offsetWidth;
      left.style.flex = "none"; left.style.width = startLW + "px";
      prev.style.flex = "none"; prev.style.width = startRW + "px";
      sp.classList.add("ed-dragging");
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      e.preventDefault();
    });
    document.addEventListener("mousemove", function(e) {
      if (!dragging) return;
      var left = document.getElementById("ed-left");
      var prev = document.getElementById("ed-preview");
      var main = document.getElementById("ed-main");
      if (!left || !prev || !main) return;
      var spEl = document.getElementById("ed-splitter");
      var available = main.getBoundingClientRect().width - (spEl ? spEl.offsetWidth : 5);
      var dx = e.clientX - startX;
      // clamp preview, derive editor from remainder so they always sum to available
      var rw = Math.min(available - 150, Math.max(150, startRW + dx));
      var lw = available - rw;
      prev.style.width = rw + "px";
      left.style.width = lw + "px";
    });
    document.addEventListener("mouseup", function() {
      if (!dragging) return;
      dragging = false;
      sp.classList.remove("ed-dragging");
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
      // Store ratio so window resize can recompute pixel widths
      var left = document.getElementById("ed-left");
      var prev = document.getElementById("ed-preview");
      if (left && prev) {
        var total = left.offsetWidth + prev.offsetWidth;
        if (total > 0) _splitRatio = prev.offsetWidth / total;
      }
    });

    window.addEventListener("resize", function() {
      var left = document.getElementById("ed-left");
      var prev = document.getElementById("ed-preview");
      if (!left || !prev || !left.style.width) return; // not yet dragged
      var main = document.getElementById("ed-main");
      if (!main) return;
      var sp2 = document.getElementById("ed-splitter");
      var available = main.offsetWidth - (sp2 ? sp2.offsetWidth : 5);
      var newPrev = Math.max(150, Math.round(available * _splitRatio));
      var newLeft = Math.max(150, available - newPrev);
      prev.style.width = newPrev + "px";
      left.style.width = newLeft + "px";
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
      _gridRatio = gh / (gh + fh); // track ratio to survive resize
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
    "lightnodes","quiz","pytutor","pyrun","slide","slides","folder","cards","transcript","feature","steps","sitemap","dataset","datagrid","chart"];

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

  var _blocks = [], _selIdx = -1, _dragFrom = null, _gridSplitSet = false, _formDirty = false, _gridRatio = 0.5, _splitRatio = 0.5;

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

  /* component model → icon by IAL type (e.g. "datagrid" → "▦") */
  var _compModel = null;
  var _compIcons = {};
  function loadCompModel() {
    if (_compModel) return;
    fetch("{{ "/assets/component-model.json" | relative_url }}")
      .then(function (r) { return r.json(); })
      .then(function (d) {
        _compModel = d.model || {};
        _compIcons = d.icons || {};
        var bp = document.getElementById("ed-blocks-pane");
        if (bp && bp.classList.contains("ed-active")) buildGrid();  // repaint with icons
        var dp = document.getElementById("ed-diagram-pane");
        if (dp && !dp.classList.contains("ed-hidden")) renderDiagram();  // repaint once model lands
      })
      .catch(function () { _compModel = {}; });
  }
  function iconFor(type) {
    if (!type || !_compModel) return "";
    var c = _compModel[compName(type)];
    return (c && c.icon) || "";
  }

  /* ── 🗺️ Diagram tab ───────────────────────────────────────
     A per-page class diagram: the component classes actually used in the file
     being edited, their generalization up to the two roots (Block, Object),
     and the blue association edges among them. Rendered as Graphviz DOT via
     the shared window.lcDotToSvg helper (graphviz.md). */
  function pageClassNames() {
    var inp = document.getElementById("ed-input");
    var seen = {}, out = [];
    if (!inp || !_compModel) return out;
    var raw = parseBlocks(inp.value || ""), blocks = [];
    raw.forEach(function (b) { blocks = blocks.concat(extractSubBlocks(b)); });
    blocks.forEach(function (b) {
      if (!b.type) return;
      var cn = compName(b.type);
      if (_compModel[cn] && !seen[cn]) { seen[cn] = 1; out.push(cn); }
    });
    return out;
  }
  function dotEsc(s) { return String(s).replace(/_/g, " ").replace(/["{}|<>]/g, ""); }
  function nodeLabel(n) {
    var c = _compModel[n] || {}, parts = [(c.icon ? c.icon + " " : "") + dotEsc(n)];
    var attrs = (c.attrs || []).map(function (a) {
      return (_compIcons[a.t] || "•") + (a.list ? "⦙" : "") + " " + dotEsc(a.n) + "\\l";
    }).join("");
    var meths = (c.methods || []).map(function (m) {
      return (m.post ? "▹ " + dotEsc(m.n) + " ▹" : "▸ " + dotEsc(m.n)) + "\\l";
    }).join("");
    if (attrs) parts.push(attrs);
    if (meths) parts.push(meths);
    return "{" + parts.join("|") + "}";
  }
  // resolve an association target to a node in the set, preferring a present
  // subclass (a Chart bind="Dataset" pointed at a Query resolves to Query)
  function resolveTarget(target, nodes, present) {
    if (nodes[target]) return target;
    for (var i = 0; i < present.length; i++) {
      var c = present[i];
      while (c && _compModel[c]) {
        var base = (_compModel[c].bases || [])[0];
        if (base === target) return present[i];
        c = base;
      }
    }
    return null;
  }
  function buildPageDot(present) {
    if (!present.length) return null;
    var nodes = {};
    present.forEach(function (n) { nodes[n] = "page"; });
    // walk each class up to its roots (Block / Object) so generalization shows
    present.forEach(function (n) {
      var c = n;
      while (c && _compModel[c]) {
        var base = (_compModel[c].bases || [])[0];
        if (base && _compModel[base]) { if (!nodes[base]) nodes[base] = "base"; c = base; }
        else break;
      }
    });
    var FONT = 'fontname="Source Sans Pro, sans-serif"', L = [];
    L.push('digraph page_model {');
    L.push('  rankdir=BT; nodesep=0.3; ranksep=0.5;');
    L.push('  graph [splines=ortho, ' + FONT + ', fontsize=10];');
    L.push('  node [' + FONT + ', shape=record, style="filled,rounded", color="gray75", fillcolor=white, fontsize=10, penwidth=0.5];');
    L.push('  edge [' + FONT + ', fontsize=8, penwidth=0.6, arrowsize=0.8];');
    Object.keys(nodes).forEach(function (n) {
      L.push('  ' + n + ' [label="' + nodeLabel(n) + '"' +
        (nodes[n] === "base" ? ', fillcolor="gray95", color="gray80"' : '') + ']');
    });
    // generalization edges (UML hollow triangle) toward Block / Object
    Object.keys(nodes).forEach(function (n) {
      var base = (_compModel[n].bases || [])[0];
      if (base && nodes[base]) L.push('  ' + n + ' -> ' + base +
        ' [arrowhead=onormal, color="gray60", arrowsize=1.0]');
    });
    // association edges (blue), among the present classes
    present.forEach(function (owner) {
      (_compModel[owner].assoc || []).forEach(function (a) {
        var tgt = resolveTarget(a.target, nodes, present);
        if (!tgt) return;
        L.push('  ' + owner + ' -> ' + tgt + ' [color=blue, fontcolor=blue, weight=8,' +
          ' headlabel="' + (a.list ? "⦙ " : "") + dotEsc(a.n) + '", labeldistance=2.2, arrowsize=0.7]');
      });
    });
    L.push('}');
    return L.join("\n");
  }
  function renderDiagram() {
    var pane = document.getElementById("ed-diagram-pane");
    if (!pane) return;
    if (!_compModel) {
      loadCompModel();
      pane.innerHTML = "<p style='color:#bbb;padding:1em'>Loading model…</p>";
      return; // loadCompModel repaints this pane when the model lands
    }
    var present = pageClassNames();
    if (!present.length) {
      pane.innerHTML = "<p style='color:#bbb;padding:1em'>No components on this page yet. " +
        "Add a <code>{: .datagrid }</code>, <code>{: .chart }</code>, … and the classes appear here.</p>";
      return;
    }
    if (!window.lcDotToSvg) {
      pane.innerHTML = "<p style='color:#b00;padding:1em'>Diagram engine unavailable.</p>";
      return;
    }
    var dot = buildPageDot(present);
    pane.innerHTML = "<p style='color:#bbb;padding:0.6em'>Rendering diagram…</p>";
    window.lcDotToSvg(dot).then(function (svg) {
      pane.innerHTML =
        "<div id='ed-diagram-legend'><b>" + present.length + "</b> component class" +
        (present.length === 1 ? "" : "es") + " on this page — " +
        "<span style='color:#3a6'>▸ generalize</span> to <b>Block</b> / <b>Object</b>, " +
        "<span style='color:blue'>→ associations</span> in blue.</div>" +
        "<div class='ed-diagram-wrap'>" + svg + "</div>";
    }).catch(function (e) {
      pane.innerHTML = "<pre style='color:#b00;padding:1em;white-space:pre-wrap'>Diagram error: " +
        escH(String((e && e.message) || e)) + "</pre>";
    });
  }
  /* validate fenced data (json / yaml) in a block's content before applying */
  function checkBlockSyntax(content) {
    var re = /```(json|ya?ml)\s*\r?\n([\s\S]*?)\r?\n```/gi, m, errs = [];
    while ((m = re.exec(content))) {
      var lang = m[1].toLowerCase(), body = m[2];
      if (lang === "json") {
        try { JSON.parse(body); } catch (e) { errs.push("JSON error: " + e.message); }
      } else if (window.jsyaml) {
        try { window.jsyaml.load(body); } catch (e) { errs.push("YAML error: " + (e.message || e)); }
      }
    }
    return errs;
  }

  /* a sub-block's "(component)" placeholder is noise — show its icon instead */
  function subTitleHtml(b) {
    if (b.heading === "(component)") {
      var ic = iconFor(b.type);
      return ic
        ? "<span title='" + escH(compName(b.type)) + "' style='font-size:1.1em'>" + ic + "</span>"
        : "<em style='color:#777'>." + escH(b.type || "") + "</em>";
    }
    return "<em style='color:#777'>" + escH(b.heading) + "</em>";
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
          : b.subBlock ? subTitleHtml(b)
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
      /* keep the selected row in view (centre it in the grid, not the page) */
      var g = document.getElementById("ed-grid"), row = g && g.querySelector("tr.ed-sel");
      if (g && row) {
        var gr = g.getBoundingClientRect(), rr = row.getBoundingClientRect();
        g.scrollTop += (rr.top - gr.top) - (gr.height / 2 - rr.height / 2);
      }
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
      _formDirty = false; // explicit click clears any pending form edit
      _selIdx = parseInt(tr.dataset.idx);
      buildGrid();
      // floating ✨ box open? follow the new selection (prompt is kept)
      var dlg = document.getElementById("ed-agent-dialog");
      if (dlg && !dlg.classList.contains("ed-hidden")) refreshAgentScope();
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
    _gridSplitSet = true; _gridRatio = 0.5;
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
      form.innerHTML = "<div class='ebf-scroll'>"
        + "<p class='ebf-meta' style='color:#888;margin:0 0 0.35em'>"
        + "<span style='color:#bbb;font-size:0.85em'>(fence item — edit via Raw tab)</span></p>"
        + "<div class='ebf-content-wrap'><textarea readonly>" + escH(fcContent) + "</textarea></div>"
        + "</div>";
      return;
    }
    if (b.subBlock) {
      form.innerHTML = "<div class='ebf-scroll'>"
        + "<p class='ebf-meta' style='color:#888;margin:0 0 0.4em'><em>Component block (edit via Raw tab)</em></p>"
        + "<div class='ebf-meta'><label>Type</label><input readonly value='." + escH(b.type||'') + "'></div>"
        + "<div class='ebf-content-wrap'><label>Content</label>"
        + "<textarea readonly>" + escH(b.lines.filter(function(l){ return l.trim() && !/^\{:/.test(l.trim()); }).join("\n").trim()) + "</textarea></div>"
        + "</div>";
      return;
    }
    var knobStr = Object.keys(b.knobs||{}).map(function(k){ return k + '="' + b.knobs[k] + '"'; }).join(" ");
    var content = blockContent(b);
    var featureHint = (b.type === "feature" || b.type === "steps")
      ? "<div id='ebf-feature-hint' style='font-size:0.78em;color:#888;margin:-0.2em 0 0.5em;padding:0.3em 0.6em;background:#f6f8fa;border-radius:4px;border:1px solid #e8e8e8'>"
        + (b.type === "feature"
            ? "Knobs: <code>status=\"passing|failing|pending\"</code> &nbsp; <code>tags=\"smoke,auth\"</code>"
            : "Pair with the preceding <code>.feature</code> block — use <code># Given/When/Then</code> comments to split Python into step chunks")
        + "</div>"
      : "";
    form.innerHTML = "<div class='ebf-scroll'>"
      + "<div class='ebf-meta' style='display:flex;gap:0.6em;flex-wrap:wrap;margin-bottom:0.4em'>"
      + "<div style='flex:3;min-width:100px'><label>Heading</label><input id='ebf-title' value='" + escA(b.heading||"") + "'></div>"
      + "<div style='flex:1;min-width:90px'><label>Type</label><select id='ebf-type'>"
      + "<option value=''>(none)</option>"
      + BLOCK_TYPES.map(function(t){ return "<option value='" + t + "'" + (b.type===t?" selected":"") + ">." + t + "</option>"; }).join("")
      + "</select></div>"
      + "<div style='flex:2;min-width:120px'><label>Knobs</label><input id='ebf-knobs' value='" + escA(knobStr) + "' placeholder='count=\"5\"'></div>"
      + "</div>"
      + featureHint
      + "<div class='ebf-content-wrap'><label>Content</label>"
      + "<textarea id='ebf-content'>" + escH(content) + "</textarea></div>"
      + "</div>"
      + "<div class='ebf-actions'><a href='#' class='lc-btn' id='ebf-apply' style='font-size:0.82em;padding:0.32em 0.9em'>Apply</a></div>";

    /* mark form dirty on any change so hover sync won't clobber edits */
    form.addEventListener("input", function() { _formDirty = true; });

    /* show/hide feature knob hint when type dropdown changes */
    document.getElementById("ebf-type").addEventListener("change", function() {
      var hint = document.getElementById("ebf-feature-hint");
      if (this.value === "feature") {
        if (!hint) {
          var h = document.createElement("div");
          h.id = "ebf-feature-hint";
          h.style.cssText = "font-size:0.78em;color:#888;margin:-0.2em 0 0.5em;padding:0.3em 0.6em;background:#f6f8fa;border-radius:4px;border:1px solid #e8e8e8";
          h.innerHTML = "Knobs: <code>status=\"passing|failing|pending\"</code> &nbsp; <code>tags=\"smoke,auth\"</code> &nbsp;&mdash;&nbsp; embed Python per step with <code>:::python</code>&nbsp;/&nbsp;<code>:::</code>";
          var scroll = form.querySelector(".ebf-scroll");
          var contentWrap = scroll.querySelector(".ebf-content-wrap");
          scroll.insertBefore(h, contentWrap);
        }
      } else {
        if (hint) hint.parentNode.removeChild(hint);
      }
    });

    document.getElementById("ebf-apply").addEventListener("click", function(e) {
      e.preventDefault();
      var cnt     = document.getElementById("ebf-content").value;
      var errs = checkBlockSyntax(cnt);   // check first — don't apply broken data
      if (errs.length) { toast("⚠ " + errs[0] + " — fix before applying.", false); return; }
      var inp = document.getElementById("ed-input");
      var before = inp.value;             // snapshot for undo
      _formDirty = false;
      var title   = document.getElementById("ebf-title").value;
      var type    = document.getElementById("ebf-type").value;
      var knobsIn = document.getElementById("ebf-knobs").value.trim();
      var prefix  = "#".repeat(b.level || 1);
      var newLines = [prefix + " " + title];
      if (cnt.trim()) newLines.push("", cnt.trim());
      if (type) newLines.push("{: ." + type + (knobsIn ? " " + knobsIn : "") + " }");
      b.heading = title; b.type = type || null;
      b.knobs = {}; var kr2 = /(\w+)="([^"]*)"/g, km2;
      while ((km2 = kr2.exec(knobsIn))) b.knobs[km2[1]] = km2[2];
      b.lines = newLines;
      var newText = blocksToText(_blocks);
      inp.value = newText; setDirty(true); updatePreview(newText);
      buildGrid();
      pushAction(iconFor(type) || "✏️", "Edited " + (type ? compName(type) : (title || "block")).slice(0, 40), before);
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
    var log    = document.getElementById("ed-log-pane");
    var feats  = document.getElementById("ed-features-pane");
    var diag   = document.getElementById("ed-diagram-pane");
    blocks.classList.toggle("ed-active", name === "blocks");
    raw.classList.toggle("ed-hidden", name !== "raw");
    if (log) log.classList.toggle("ed-hidden", name !== "log");
    if (feats) feats.classList.toggle("ed-hidden", name !== "features");
    if (diag) diag.classList.toggle("ed-hidden", name !== "diagram");
    if (name === "blocks") buildGrid();
    if (name === "log") renderLog();
    if (name === "features") openFeatures();
    if (name === "diagram") renderDiagram();
  });

  /* ── 🧪 Features tab ─────────────────────────────────────
     Lists the page's .feature blocks; selecting one renders it live
     below. Running it updates its status, which is written back into the
     block's {: .feature status="…" } IAL so a Save persists the real
     result. */
  var _featSelIdx = -1;

  function featureName(b) {
    var lines = b.lines || [];
    for (var i = 0; i < lines.length; i++) {
      var m = lines[i].match(/^\s*Feature:\s*(.+)/i);
      if (m) return m[1].trim();
    }
    return (b.heading && b.heading !== "(component)") ? b.heading : "Feature";
  }

  function featureRows() {
    var out = [];
    (_blocks || []).forEach(function (b, i) {
      // a feature under a heading appears twice in _blocks — the parent and
      // an extracted sub-block. Keep the parent only: blocksToText
      // serialises it (sub-blocks are skipped), so status write-back lands.
      if (b.type === "feature" && !b.subBlock) {
        out.push({ i: i, name: featureName(b),
          status: (b.knobs && b.knobs.status) || "none",
          tags: (b.knobs && b.knobs.tags) || "" });
      }
    });
    return out;
  }

  function buildFeatureGrid() {
    var grid = document.getElementById("ed-feat-grid");
    if (!grid) return;
    var rows = featureRows();
    if (!rows.length) {
      grid.innerHTML = "<p style='color:#bbb;padding:1em'>No features on this page. A <code>{: .feature }</code> block appears here.</p>";
      var pv = document.getElementById("ed-feat-preview"); if (pv) pv.innerHTML = "";
      _featSelIdx = -1;
      return;
    }
    var html = "<table><thead><tr><th>Feature</th><th style='width:92px'>Status</th><th>Tags</th></tr></thead><tbody>";
    rows.forEach(function (r) {
      html += "<tr data-fi='" + r.i + "'" + (r.i === _featSelIdx ? " class='ed-fsel'" : "") + ">"
        + "<td>" + escH(r.name) + "</td>"
        + "<td><span class='ed-fstatus " + escH(r.status) + "'>" + escH(r.status) + "</span></td>"
        + "<td style='color:#888'>" + escH(r.tags) + "</td></tr>";
    });
    grid.innerHTML = html + "</tbody></table>";
  }

  /* render ALL features stacked in the preview. Scanning the root upgrades
     each card AND (via the feature component's lcScanElement hook) inserts
     its own "▶ Run All" suite dashboard when there are 2+ runnable cards —
     so the test suite the .feature page shows appears here too. */
  function renderFeatures() {
    var prev = document.getElementById("ed-feat-preview");
    if (!prev) return;
    var rows = featureRows();
    if (!rows.length) { prev.innerHTML = ""; return; }
    var md = rows.map(function (r) { return (_blocks[r.i].lines || []).join("\n"); }).join("\n\n");
    function doRender() {
      prev.innerHTML = window.marked ? window.marked.parse(normIAL(md)) : "<pre>" + escH(md) + "</pre>";
      if (window.lcApplyIAL) window.lcApplyIAL(prev);
      if (window.lcScanElement) window.lcScanElement(prev);
      wireWriteback(prev, rows);
    }
    if (window.marked) doRender();
    else if (window.lcLoadMarked) window.lcLoadMarked(doRender);
  }

  /* the feature component writes the run status back into #ed-input itself
     (it recognises #ed-feat-preview). Here we only mirror each card's status
     class into the grid badge so the list stays in sync after a run. */
  function wireWriteback(prev, rows) {
    var cards = prev.querySelectorAll(".lc-feature");
    cards.forEach(function (card, k) {
      if (k >= rows.length) return;
      var idx = rows[k].i;
      function refresh() {
        var st = card.classList.contains("lc-feature-passing") ? "passing"
               : card.classList.contains("lc-feature-failing") ? "failing"
               : card.classList.contains("lc-feature-pending") ? "pending" : null;
        if (!st) return;
        var b = _blocks[idx];
        if (b) { b.knobs = b.knobs || {}; b.knobs.status = st; }
        buildFeatureGrid();
      }
      try {
        new MutationObserver(refresh).observe(card, { attributes: true, attributeFilter: ["class"] });
      } catch (e) {}
      refresh();
    });
  }

  /* open the tab: list + render all features so the suite is ready */
  function openFeatures() { buildFeatureGrid(); renderFeatures(); }

  document.addEventListener("click", function (e) {
    var fr = e.target.closest("#ed-feat-grid tr[data-fi]");
    if (fr) {
      var idx = parseInt(fr.getAttribute("data-fi"), 10);
      _featSelIdx = idx; buildFeatureGrid();
      var rows = featureRows(), k = -1;
      for (var j = 0; j < rows.length; j++) { if (rows[j].i === idx) { k = j; break; } }
      var cards = document.querySelectorAll("#ed-feat-preview .lc-feature");
      if (k >= 0 && cards[k]) cards[k].scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }
    if (e.target.closest("#ed-feat-runall")) {
      e.preventDefault();
      var pv = document.getElementById("ed-feat-preview");
      var suiteRun = pv && pv.querySelector(".lc-suite-run");
      if (suiteRun) { suiteRun.click(); return; }      // ≥2 features: drive the suite
      var one = pv && pv.querySelector(".lc-feature .lc-feature-run");
      if (one) one.click();                            // single feature
      return;
    }
  });

  /* ── ✨ AI edit: scoped · previewed · logged ─────────────
     The ✨ button opens a dialog scoped to the current selection (a block
     in the grid, the Raw selection, or the whole page). The model returns
     a small JSON list of exact find/replace edits — the PLAN — which the
     author approves or retries before anything changes. Untouched text
     cannot change; each applied edit is logged, and Save prefills its
     commit message from that log. */
  var _actionLog = [];       // mutating actions (undoable) + saves (traced)
  var _agentPlan = null;     // edits awaiting approval
  var _agentScope = null;    // {label, text} the current ask is focused on

  function agentStatus(msg, err) {
    var s = document.getElementById("ed-agent-status");
    if (!s) return;
    s.textContent = msg || "";
    s.classList.toggle("ed-err", !!err);
  }
  function escPlan(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  /* "datagrid" → "Datagrid", "embed-page" → "EmbedPage" (the component name) */
  function compName(type) {
    return (type || "").split(/[-_]/).map(function (s) {
      return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
    }).join("");
  }

  /* the edit's context: selected block › Raw selection › whole page.
     A parsed block already carries .type (component class) and .knobs
     (its IAL attributes) and its .lines include the heading line. */
  function captureScope() {
    var inp = document.getElementById("ed-input");
    var page = (inp && inp.value) || "";
    if (typeof _selIdx === "number" && _blocks && _blocks[_selIdx]) {
      var b = _blocks[_selIdx];
      var text = (b.lines && b.lines.length) ? b.lines.join("\n").trim() : "";
      if (text && page.indexOf(text) >= 0) {
        var label;
        if (b.preamble) label = "page header";
        else if (b.type) label = compName(b.type) + (b.knobs && b.knobs.id ? " #" + b.knobs.id : "");
        else label = (b.heading || "section").slice(0, 40);
        return { label: label, text: text, type: b.type || null, knobs: b.knobs || {} };
      }
    }
    if (inp && inp.selectionEnd > inp.selectionStart) {
      var sel = page.slice(inp.selectionStart, inp.selectionEnd).trim();
      if (sel) return { label: "selection · " + sel.length + " chars", text: sel, type: null, knobs: {} };
    }
    return { label: "whole page", text: page, type: null, knobs: {} };
  }

  /* tell the model what component it's editing, so the edit stays valid */
  function componentNote(scope) {
    if (!scope.type) return "";
    var knobs = Object.keys(scope.knobs || {}).map(function (k) {
      return k + "=\"" + scope.knobs[k] + "\"";
    }).join(" ");
    return "\n\nThe scoped block is a \"" + compName(scope.type) + "\" component, " +
      "declared with `{: ." + scope.type + (knobs ? " " + knobs : "") + " }`. Preserve that " +
      "IAL line and keep the change compatible with this component — do not remove or " +
      "rename its class or break its attributes unless explicitly asked.";
  }

  function openAgentDialog() {
    var drawer = document.getElementById("ed-drawer");
    if (!drawer || !drawer.classList.contains("open")) return;
    var dlg = document.getElementById("ed-agent-dialog");
    if (!dlg) return;
    _agentScope = captureScope();
    var sc = document.getElementById("ed-ag-scope");
    if (sc) sc.textContent = "· " + _agentScope.label;
    var plan = document.getElementById("ed-ag-plan");
    if (plan) { plan.classList.add("ed-hidden"); plan.innerHTML = ""; }
    _agentPlan = null;
    agentStatus("", false);
    dlg.classList.remove("ed-hidden");
    var p = document.getElementById("ed-agent-prompt");
    if (p) p.focus();
  }
  function closeAgentDialog() {
    var dlg = document.getElementById("ed-agent-dialog");
    if (dlg) dlg.classList.add("ed-hidden");
  }
  /* re-aim the open box at the current selection — keeps the typed prompt,
     drops any stale plan. Scope follows block selection, never focus. */
  function refreshAgentScope() {
    _agentScope = captureScope();
    var sc = document.getElementById("ed-ag-scope");
    if (sc) sc.textContent = "· " + _agentScope.label;
    var plan = document.getElementById("ed-ag-plan");
    if (plan) { plan.classList.add("ed-hidden"); plan.innerHTML = ""; }
    _agentPlan = null;
    agentStatus("", false);
  }

  /* apply find/replace edits locally; untouched text cannot change */
  function applyEdits(text, edits) {
    var next = text, applied = [], skipped = [];
    edits.forEach(function (ed) {
      var f = ed && ed.find, rep = (ed && ed.replace != null) ? ed.replace : "";
      if (!f) return;
      var first = next.indexOf(f);
      if (first < 0) { skipped.push(f); return; }
      if (next.indexOf(f, first + 1) >= 0) { skipped.push(f); return; }
      next = next.slice(0, first) + rep + next.slice(first + f.length);
      applied.push({ find: f, replace: rep });
    });
    return { text: next, applied: applied, skipped: skipped };
  }

  function agentAsk(temp) {
    var promptEl = document.getElementById("ed-agent-prompt");
    var inp = document.getElementById("ed-input");
    var instruction = (promptEl && promptEl.value || "").trim();
    if (!instruction) { agentStatus("Type the change first.", true); return; }
    if (!_pat) { agentStatus("Connect a GitHub token (Setup) first.", true); return; }
    var page = (inp && inp.value) || "";
    if (!page) { agentStatus("Load a file first.", true); return; }
    var scope = _agentScope || captureScope();

    agentStatus(temp ? "✨ Rethinking…" : "✨ Planning…", false);
    fetch("https://models.github.ai/inference/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + _pat, "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "openai/gpt-4o-mini",
        max_tokens: 1500,
        /* non-zero so fuzzy asks vary run-to-run; Retry passes a higher
           value (temperature 0 returns an identical plan every time) */
        temperature: (temp != null ? temp : 0.4),
        messages: [
          { role: "system", content:
            "You edit a Markdown page by returning exact find/replace edits — never " +
            "the whole page. Each \"find\" MUST be a substring copied verbatim, long " +
            "enough to occur exactly once. \"replace\" is what it becomes (\"\" deletes " +
            "it). Make the smallest edits that satisfy the instruction and touch " +
            "nothing else. A leading \"!\" in an accordion title is a meaningful " +
            "eager-render flag.\n" +
            "First READ the existing content. Never add an item that is already " +
            "present, even under a different spelling, name, or coordinates. If the " +
            "requested change is already there, return an empty \"edits\" array and " +
            "say so in the explanation. If the instruction is vague (e.g. \"add a " +
            "park\"), pick ONE concrete option that is NOT already present and name " +
            "your choice in the explanation.\n" +
            "Respond with ONLY a JSON object: {\"explanation\":\"<one sentence naming " +
            "exactly what changed>\",\"edits\":[{\"find\":\"old\",\"replace\":\"new\"}]}" },
          { role: "user", content:
            "Instruction: " + instruction +
            "\n\nApply it within this section:\n```\n" + scope.text + "\n```" +
            componentNote(scope) +
            "\n\nFull page for context:\n```markdown\n" + page + "\n```" }
        ]
      })
    }).then(function (r) {
      return r.json().then(function (data) { return { status: r.status, data: data }; });
    }).then(function (res) {
      if (res.status === 401 || res.status === 403) { agentStatus("Token rejected — fresh PAT?", true); return; }
      if (res.status === 429) { agentStatus("Rate limited — wait a moment.", true); return; }
      if (res.status >= 400) { agentStatus((res.data && res.data.error && res.data.error.message) || ("HTTP " + res.status), true); return; }
      var choice = res.data.choices && res.data.choices[0];
      var txt = choice && choice.message && choice.message.content || "";
      /* accept {explanation, edits} or a bare [edits] array */
      var jm = txt.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
      var parsed; try { parsed = JSON.parse(jm ? jm[0] : txt); } catch (e) { parsed = null; }
      var edits = null, explanation = "";
      if (Array.isArray(parsed)) edits = parsed;
      else if (parsed && Array.isArray(parsed.edits)) { edits = parsed.edits; explanation = parsed.explanation || ""; }
      if (!edits) { agentStatus("Couldn't read a plan — rephrase?", true); return; }
      /* empty edits = deliberate no-op (e.g. "already present") — show why */
      if (!edits.length) { agentStatus(explanation || "Nothing to change — it may already be present.", false); return; }
      var dry = applyEdits(page, edits);   // dry-run to preview what will land
      if (!dry.applied.length) { agentStatus("Couldn't locate the text — name it more exactly.", true); return; }
      _agentPlan = { instruction: instruction, scope: scope.label, explanation: explanation, edits: dry.applied };
      renderPlan(explanation, dry.applied, dry.skipped);
      agentStatus("", false);
    }).catch(function (err) { agentStatus("Network error: " + (err && err.message || err), true); });
  }

  function renderPlan(explanation, applied, skipped) {
    var plan = document.getElementById("ed-ag-plan");
    if (!plan) return;
    var exp = explanation ? "<p class='ed-ag-exp'>" + escPlan(explanation) + "</p>" : "";
    var rows = applied.map(function (e) {
      return "<div class='ed-ag-edit'><div class='ed-ag-del'>− " + escPlan(e.find) + "</div>" +
        "<div class='ed-ag-add'>+ " + escPlan(e.replace || "(deleted)") + "</div></div>";
    }).join("");
    var skip = skipped.length ? "<p class='ed-ag-skip'>" + skipped.length + " edit(s) skipped (not found / ambiguous)</p>" : "";
    plan.innerHTML = exp +
      "<div class='ed-ag-planhead'>Planned change · " + applied.length + " edit(s)</div>" +
      rows + skip +
      "<div class='ed-ag-approve'><a href='#' class='lc-btn' id='ed-ag-approve'>✓ Approve</a>" +
      "<a href='#' class='lc-btn lc-btn-secondary' id='ed-ag-retry'>↻ Retry</a></div>";
    plan.classList.remove("ed-hidden");
  }

  function agentApprove() {
    if (!_agentPlan) return;
    var inp = document.getElementById("ed-input");
    var page = (inp && inp.value) || "";
    var r = applyEdits(page, _agentPlan.edits);
    if (inp) { inp.value = r.text; setDirty(true); updatePreview(r.text); }
    pushAction("✨", _agentPlan.instruction + " (" + _agentPlan.scope + ")", page);
    _agentPlan = null;
    buildGrid();          // block text changed — repaint the grid
    refreshAgentScope();  // re-aim at the edited block; box stays open
    agentStatus("✓ applied — pick another block, or ✕ to close.", false);
    toast("✨ " + r.applied.length + " edit(s) applied.", true);
  }

  /* unified action log: every mutating action records a before-snapshot so
     it can be undone; saves are traced (no undo). Newest first. */
  function pushAction(icon, label, before) {
    _actionLog.push({ icon: icon, label: label, before: before, ts: Date.now() });
    renderLog();
  }

  function renderLog() {
    var box = document.getElementById("ed-log");
    if (!box) return;
    if (!_actionLog.length) {
      box.innerHTML = "<p style='color:#bbb;padding:1em'>No edits yet. Edit a block, or use ✨ to ask for a change — each action is logged here and can be undone.</p>";
      return;
    }
    box.innerHTML = _actionLog.map(function (e, i) { return { e: e, i: i }; }).reverse().map(function (o) {
      var e = o.e;
      var undo = (e.before != null)
        ? "<a href='#' class='ed-log-undo' data-undo='" + o.i + "'>↩ Undo</a>" : "";
      return "<div class='ed-log-item'><div class='ed-log-instr'>" + e.icon + " " + escPlan(e.label) + undo + "</div>" +
        "<div class='ed-log-meta'>" + timeAgo(new Date(e.ts)) + "</div></div>";
    }).join("");
  }

  function undoAction(idx) {
    var entry = _actionLog[idx];
    if (!entry || entry.before == null) return;
    var inp = document.getElementById("ed-input");
    if (inp) { inp.value = entry.before; setDirty(true); updatePreview(entry.before); }
    _actionLog = _actionLog.slice(0, idx);   // this action and any after it are undone
    buildGrid(); renderLog();
    toast("↩ Undone: " + entry.label, true);
  }

  /* commit message prefilled from the edits made since the last save */
  function logCommitMessage() {
    var since = [];
    for (var i = _actionLog.length - 1; i >= 0; i--) {
      if (_actionLog[i].icon === "💾") break;          // stop at the last save
      if (_actionLog[i].before != null) since.unshift(_actionLog[i].label);
    }
    if (!since.length) return "";
    if (since.length === 1) return since[0];
    return "Edits (" + since.length + "): " + since.join("; ");
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("#ed-agent-btn")) { e.preventDefault(); openAgentDialog(); return; }
    if (e.target.closest("#ed-ag-x"))      { e.preventDefault(); closeAgentDialog(); return; }
    if (e.target.closest("#ed-agent-ask")) { e.preventDefault(); agentAsk(); return; }
    if (e.target.closest("#ed-ag-approve")){ e.preventDefault(); agentApprove(); return; }
    var undoEl = e.target.closest(".ed-log-undo");
    if (undoEl) { e.preventDefault(); undoAction(parseInt(undoEl.getAttribute("data-undo"), 10)); return; }
    if (e.target.closest("#ed-ag-retry")) {
      e.preventDefault();
      agentAsk(0.9);   // retry with more variety (temperature 0 returns the same plan)
      return;
    }
  });

  /* drag the floating ✨ box by its header */
  (function () {
    var dlg = null, ox = 0, oy = 0, dragging = false;
    document.addEventListener("mousedown", function (e) {
      if (!e.target.closest("#ed-ag-head") || e.target.closest("#ed-ag-x")) return;
      dlg = document.getElementById("ed-agent-dialog");
      if (!dlg) return;
      var r = dlg.getBoundingClientRect();
      ox = e.clientX - r.left; oy = e.clientY - r.top;
      dlg.style.right = "auto"; dlg.style.left = r.left + "px"; dlg.style.top = r.top + "px";
      dragging = true; e.preventDefault();
    });
    document.addEventListener("mousemove", function (e) {
      if (!dragging || !dlg) return;
      dlg.style.left = Math.max(0, Math.min(window.innerWidth - 80, e.clientX - ox)) + "px";
      dlg.style.top  = Math.max(48, Math.min(window.innerHeight - 40, e.clientY - oy)) + "px";
    });
    document.addEventListener("mouseup", function () { dragging = false; });
  })();

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
        if (_formDirty) return; // don't clobber unsaved form edits
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

  /* ── Window resize: maintain stored grid/form ratio ─── */
  window.addEventListener("resize", function() {
    if (!_gridSplitSet) return;
    var pane = document.getElementById("ed-blocks-pane");
    var grid = document.getElementById("ed-grid");
    var form = document.getElementById("ed-block-form");
    if (!pane || !grid || !form || !form.classList.contains("ed-visible")) return;
    var paneH = pane.offsetHeight;
    if (paneH < 20) return;
    var available = paneH - 5;
    var newGrid = Math.max(60, Math.round(available * _gridRatio));
    var newForm = Math.max(80, available - newGrid);
    grid.style.height = newGrid + "px";
    form.style.height = newForm + "px";
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
    wireGrid(); // wire grid event delegation once, not on every buildGrid()
  });
})();
</script>
{% endif %}
