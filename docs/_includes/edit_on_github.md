{%- comment -%}
Edit mode lives in the Modes pill (bottom-left) and on ⌥E / Alt-E; the old
✏️ FAB element remains in the DOM (hidden) as the editor's presence marker
and pagePath carrier. Opening shows an in-page editor drawer that
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
.lc-edit-fab { display: none !important; }   /* retired: Edit is in the pill + ⌥E */
.lc-edit-fab-legacy {
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
/* narrow / portrait: the top bar can't hold every control — drop the optional
   ones (build status, 50% zoom, + New) so the ESSENTIALS stay on-screen:
   filename · ✨ Ask · 💾 Save · ✕ Close. Save you can always reach. */
@media (max-width: 600px) {
  #ed-top { gap: 0.35em; padding: 0.55em 0.6em; }
  #ed-filename { max-width: 34vw; }
  #ed-build, #ed-zoom-btn, #ed-new-btn { display: none; }
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
  background: #fff; color: #333; border: 1px solid #d8d8d8; border-radius: 0 6px 6px 6px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.13); padding: 0.8em 0.7em; font-size: 0.85em;
  opacity: 0; visibility: hidden; transform: translateY(-6px);
  transition: opacity 0.15s ease, visibility 0.15s, transform 0.18s ease;
}
#ed-sidebar.ed-open { opacity: 1; visibility: visible; transform: none; }
#ed-main { flex: 1; display: flex; flex-direction: row; overflow: hidden; }
#ed-left { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 200px; }
#ed-input {
  flex: 1; border: none; resize: none;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; padding: 1em; line-height: 1.6;
  outline: none; background: #1e1e2e; color: #cdd6f4;   /* dark workshop — matches the mdpad editor */
  caret-color: #89b4fa;
}
#ed-input::placeholder { color: #6c7086; }
/* line-number gutter for the Raw editor */
#ed-raw-body { display: flex; flex: 1; min-height: 0; overflow: hidden; }
#ed-gutter { flex: none; overflow: hidden; background: #181825; border-right: 1px solid #313244; position: relative; z-index: 1; }
#ed-gutter-inner { padding: 1em 0.55em 1em 0.75em; min-width: 2.4em; text-align: right;
  cursor: default; }
#ed-gutter-inner .ed-gl { display: block; white-space: pre; }
/* the parent gutter is pointer-events:none (numbers must not steal the
   caret) — the fold arrows re-arm themselves, or no real click ever lands */
#ed-gutter-inner .ed-fold-a { cursor: pointer; color: #89b4fa; margin-right: 3px; user-select: none; pointer-events: auto; }
#ed-gutter-inner .ed-fold-a:hover { color: #cdd6f4; }
#ed-gutter-inner {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; line-height: 1.6;
  color: #585b70; white-space: pre; pointer-events: none; user-select: none; will-change: transform; }
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
#ed-raw-pane { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
#ed-raw-pane.ed-hidden { display: none; }
/* the raw source is the "basement workshop" the self-growing house is built from */
#ed-raw-shop {
  flex: none; display: flex; align-items: center; gap: 0.5em;
  padding: 0.42em 0.95em; font-size: 0.76em; letter-spacing: 0.02em;
  background: #181825; color: #6c7086; border-bottom: 1px solid #313244;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; user-select: none;
}
#ed-raw-shop b { color: #cdd6f4; font-weight: 600; }
#ed-raw-shop .ed-shop-grow { margin-left: auto; opacity: 0.7; }
/* ── ✏️ formatting toolbar (inserts markdown; storage stays pure md) ── */
.ed-fmt-bar { flex: none; display: flex; flex-wrap: wrap; align-items: center; gap: 3px;
  padding: 4px 7px; background: #181825; border-bottom: 1px solid #313244; }
.ed-fmt-bar button[data-fmt], .ed-fmt-bar .ed-fmt-col {
  background: #313244; color: #cdd6f4; border: none; border-radius: 4px; cursor: pointer;
  font-size: 0.82em; padding: 3px 9px; font-family: inherit; line-height: 1.5; }
.ed-fmt-bar button[data-fmt]:hover { background: #45475a; }
.ed-fmt-bar .ed-fmt-sep { width: 1px; align-self: stretch; background: #313244; margin: 0 2px; }
.ed-fmt-bar .ed-fmt-col { padding: 2px 4px; }
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
/* ── lint chip + findings panel ───────────────────────── */
#ed-lint { font-size: 0.8em; font-weight: 600; padding: 2px 9px; border-radius: 11px;
  cursor: pointer; user-select: none; flex-shrink: 0; margin-left: 0.4em;
  background: #eef7ee; color: #1e7a2e; border: 1px solid #cde8cd; }
#ed-lint.warn { background: #fff7e6; color: #915f00; border-color: #ffd98a; }
#ed-lint.err  { background: #fef2f2; color: #b91c1c; border-color: #fecaca; }
#ed-lint-panel { display: none; position: absolute; top: 44px; left: 220px; z-index: 60;
  background: #fff; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.18);
  max-width: 560px; max-height: 45vh; overflow: auto; font-size: 0.8em; padding: 4px 0; }
#ed-lint-panel.open { display: block; }
.ed-lint-item { padding: 4px 12px; cursor: pointer; display: flex; gap: 8px; align-items: baseline; white-space: nowrap; }
.ed-lint-item:hover { background: #f0f6ff; }
.ed-lint-item .ln { color: #888; font-family: monospace; flex-shrink: 0; min-width: 3.5em; }
.ed-lint-item .msg { overflow: hidden; text-overflow: ellipsis; }
.ed-lint-empty { padding: 6px 12px; color: #1e7a2e; }

/* ── Features tab ─────────────────────────────────────── */
#ed-features-pane { display: flex; flex: 1; flex-direction: column; overflow: hidden; }
#ed-features-pane.ed-hidden { display: none; }
#ed-feat-bar { flex: none; display: flex; align-items: center; gap: 0.7em; padding: 0.45em 0.6em; border-bottom: 1px solid #f0f0f0; }
#ed-feat-bar .button { font-size: 0.82em; padding: 0.3em 0.85em; }
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
/* the Content field is the same dark "workshop" surface as the Raw tab —
   scoped to .ebf-content-wrap so heading / type / knob fields stay light */
#ed-block-form .ebf-content-wrap textarea,
#ed-block-form .ebf-content-wrap textarea[readonly] {
  background: #1e1e2e; color: #cdd6f4; caret-color: #89b4fa;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
#ed-block-form .ebf-content-wrap textarea::placeholder { color: #6c7086; }
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
            <a href="#" class="button" id="ed-connect-btn" style="font-size:0.82em;padding:0.35em 0.9em">Connect</a>
            <a href="#" class="button button-danger" id="ed-disconnect-btn" style="font-size:0.82em;padding:0.35em 0.9em;display:none">Disconnect</a>
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
    <span id="ed-lint" title="Draft checks — syntax, knobs, ids, references">✓</span>
    <div id="ed-lint-panel"></div>
    <a href="#" class="button button-secondary" id="ed-zoom-btn" title="Toggle 50% preview scale" style="font-size:0.82em;padding:0.35em 0.9em;margin-left:auto">50%</a>
    <a href="#" class="button button-secondary" id="ed-new-btn" style="font-size:0.82em;padding:0.35em 0.9em">+ New</a>
    <a href="#" class="button button-secondary" id="ed-agent-btn" title="Ask AI to change the selected block (✨)" style="font-size:0.82em;padding:0.35em 0.7em">✨</a>
    <a href="#" class="button" id="ed-save-btn" style="font-size:0.82em;padding:0.35em 0.9em">💾 Save</a>
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
          <div id="ed-raw-shop">🔧 <b>basement workshop</b> · the source the self-growing house is built from<span class="ed-shop-grow">🌱→🏠</span></div>
          <div id="ed-raw-body">
            <div id="ed-gutter"><div id="ed-gutter-inner">1</div></div>
            <textarea id="ed-input" placeholder="Select a file to start editing…" spellcheck="false" wrap="off"></textarea>
          </div>
        </div>
        <div id="ed-features-pane" class="ed-hidden">
          <div id="ed-feat-bar">
            <a href="#" class="button" id="ed-feat-runall">▶ Run all</a>
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
        <a href="#" class="button" id="ed-agent-ask">✨ Plan the change</a>
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
   title="Edit this page (⌥⇧E)"
   aria-keyshortcuts="Alt+Shift+E"
   aria-label="Edit this page">
  <span class="lc-edit-fab-icon" aria-hidden="true">✏️</span>
  <span class="lc-edit-fab-label">Edit page</span>
</a>

<script>
(function () {
  var LS_PAT = "lc_ed_pat", LS_REPO = "lc_ed_repo";
  var _pat, _repo, _curFile, _curSha, _dirty = false, _previewTimer = null, _savedContent = null, _savedSinceOpen = false;
  var _runnerEdit = false;   // editing a runner-rendered source (gh:repo/path), not a docs/ page

  /* On the runtime (/run.html) the page itself is only the runner stub — what
     the author actually edits is the RENDERED source the runner stamped on its
     root (gh:repo/path). When such a render is present, the SAME rich editor
     targets that repo+file: course material, a bench, any runner render. The
     vault/Library is read-only (data-lc-readonly) → never a target.

     Scoped to #lc-run — the STANDALONE runner only. Component pages and /paris
     embed demo renders (.lc-run WITHOUT an id, see runner.md), and a loose
     `.lc-run[...]` selector matched those too: opening the editor there
     retargeted it at the demo's repo, and connecting overwrote the repo the
     author had just verified — i.e. "the file picker is broken and I can't
     sign in". An embedded demo must never hijack the page's own editor. */
  /* Null means "this page is not a runner render". A READ-ONLY render is still
     a render — conflating the two made the editor fall through to the page
     underneath and open docs/run.md, the runtime's own source, while the
     learner thought they were editing the library page in front of them. The
     readonly flag is carried, not swallowed. */
  function runnerTarget() {
    var r = document.querySelector("#lc-run[data-lc-src-repo][data-lc-src-path]");
    if (!r) return null;
    var repo = r.dataset.lcSrcRepo, path = r.dataset.lcSrcPath;
    if (!repo || !path) return null;             // a same-origin render carries no repo
    return { repo: repo, path: path, readonly: !!r.dataset.lcReadonly };
  }

  /* A read-only source has nothing to open and nothing to save. Say which file
     it is and why, rather than quietly editing something else. */
  function lockReadOnly(rt) {
    _runnerEdit = true;
    _curFile = null;
    var fn = document.getElementById("ed-filename");
    if (fn) fn.textContent = "🔒 " + rt.path;
    var save = document.getElementById("ed-save-btn");
    if (save) { save.style.display = "none"; }
    var inp = document.getElementById("ed-input");
    if (inp) { inp.value = ""; inp.readOnly = true; }
    var files = document.getElementById("ed-files");
    if (files) files.innerHTML = "<span style='color:#bbb'>Read-only source — nothing to edit here.</span>";
    setStatus("🔒 " + rt.repo + " is read-only for you — this page is the Library. "
            + "Edit it in the lab, then publish.", false);
  }

  function setDirty(on) {
    _dirty = on;
    if (window._edLintSoon) window._edLintSoon();   // draft checks track every change
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
    /* the frame contract is the last gate: whatever door was used, an
       embedding page that said editable=0 gets no editor */
    if (window.lcFrame && window.lcFrame.editable === false) return;
    var d = document.getElementById("ed-drawer");
    if (!d) return;

    // Clear any stale inline styles from previous opens
    var left = document.getElementById("ed-left");
    var prev = document.getElementById("ed-preview");
    if (left) { left.style.transition = ""; left.style.flex = ""; left.style.width = ""; left.style.overflow = ""; }
    if (prev) { prev.style.flex = ""; prev.style.width = ""; }

    d.classList.add("open");
    document.body.classList.add("ed-drawer-open"); // lets the score FAB (and others) hide behind the editor
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
    attachFmtToolbar(document.getElementById("ed-input")); // format-by-click on the Raw editor
    initRawGutter(); // line-number gutter for the Raw editor
    buildGrid(); // always build — shows placeholder if no file yet

    var rt = runnerTarget();
    if (rt && rt.readonly) { lockReadOnly(rt); }
    else if (_pat && (rt || _repo)) {
      if (rt) {
        /* target the RENDERED repo+file, not the connected repo or docs/run.md.
           In-memory only — /run.html edits nothing but renders, so overriding
           _repo here can't leak into a normal page edit. */
        _repo = rt.repo; _runnerEdit = true;
        loadFiles();
        loadFile(rt.path);                       // the gh path as-is — no docs/ prefix
      } else {
        _runnerEdit = false;
        loadFiles();
        if (!_curFile) {
          var fabEl = document.getElementById("ed-fab");
          var pagePath = fabEl && fabEl.dataset ? fabEl.dataset.pagePath : "";
          if (pagePath) loadFile("docs/" + pagePath);
        }
      }
    } else {
      /* never fail silently: say WHY there's no file instead of the
         ambiguous "No file selected" */
      var fnEl0 = document.getElementById("ed-filename");
      if (fnEl0) fnEl0.textContent = "Not connected — open ⚙️ Connect";
      var setup0 = document.getElementById("ed-setup");
      if (setup0) setup0.open = true;
      /* the Connect pane lives in the filename dropdown — actually open it,
         a tick later so the drawer-opening click can't immediately close it */
      setTimeout(openFilePanel, 0);
    }
  }
  /* the page you RETURN to shows what you saved (Michel, 2026-08-24):
     Pages takes minutes to rebuild, so re-render main from the draft
     client-side — the same road the live preview walks. (X-ray edits feel
     instant for the same reason: they patch the live DOM directly.) */
  function renderIntoPage(src) {
    var main = document.querySelector("main.markdown-body");
    if (!main || !window.marked) return;
    try {
      if (window.lcDestroyInstancesIn) window.lcDestroyInstancesIn(main);
      main.innerHTML = (window.lcInlineIAL || function (h) { return h; })(marked.parse(normIAL(src)));
      if (window.lcApplyIAL)    window.lcApplyIAL(main);
      if (window.lcScanElement) window.lcScanElement(main);
      if (window.lcSlidesRebuild) window.lcSlidesRebuild();
    } catch (e) { console.warn("[lc-edit] page refresh failed", e); }
  }
  function closeDrawer() {
    if (_dirty && !confirm("Discard unsaved changes to " + (_curFile || "this file") + "?")) return;
    if (_dirty && _savedContent !== null) {
      var inp = document.getElementById("ed-input");
      if (inp) { inp.value = _savedContent; if (inp._hist) inp._hist.reset(); updatePreview(_savedContent); }
      _blocks = []; _selIdx = -1; buildGrid();
    }
    if (_savedSinceOpen && _savedContent !== null) {
      var fab2 = document.getElementById("ed-fab");
      var pp = fab2 && fab2.dataset ? fab2.dataset.pagePath : "";
      if (pp && _curFile === "docs/" + pp) renderIntoPage(_savedContent);
      _savedSinceOpen = false;
    }
    setDirty(false);
    closeFilePanel();   /* it lives on <body> now — it would outlive the drawer */
    var d = document.getElementById("ed-drawer");
    if (d) d.classList.remove("open");
    document.body.classList.remove("ed-drawer-open");
    setTimeout(function() { document.body.style.overflow = ""; }, 260);
  }

  /* A course page inside a teacher's frame is the LESSON's file, not the
     learner's — the editor opened on it empty and useless (Michel,
     2026-08-18, Canvas as student). One predicate, asked by every edit
     door: the pill item, the pencil, both hotkeys. The learner's own
     bench pages (topbar bench-mode) stay fully editable — that path
     works and must keep working — and an explicit ?editable=1 wins, as
     explicit always does. Returns the reason, or "" when editing is open. */
  window.lcEditLocked = function () {
    if (window.lcFrame && window.lcFrame.editable === false) return "editing is off in this frame";
    if (document.documentElement.classList.contains("lc-editable")) return "";
    var framed = window.lcFrame && (window.lcFrame.crumb || window.lcFrame.focus);
    var ghSrc = /#src=gh(:|%3[Aa])/.test(location.hash || "");
    var bench = !!document.querySelector("#lc-topbar.lc-bench-mode");
    return (framed && ghSrc && !bench)
      ? "this page is the course's — your own pages (🎒 bench) are yours to edit"
      : "";
  };
  function syncEditDoors() {
    var lk = window.lcEditLocked();
    var fab = document.getElementById("ed-fab");
    if (fab) { fab.classList.toggle("ed-locked", !!lk); if (lk) fab.title = lk; }
    var pill = document.getElementById("lc-bl-edit-btn");
    if (pill) { pill.disabled = !!lk; pill.title = lk || "⌥E"; }
  }
  addEventListener("hashchange", function () {
    syncEditDoors();
    setTimeout(syncEditDoors, 1600);   /* bench-mode is stamped after the render */
  });
  document.addEventListener("lc-mode-changed", syncEditDoors);
  setTimeout(syncEditDoors, 1600);
  /* bench-mode lands whenever the render finishes — watch the stamp itself,
     so a slow bench never leaves its own door wrongly locked */
  (function () {
    var tb = document.getElementById("lc-topbar");
    if (tb && window.MutationObserver)
      new MutationObserver(syncEditDoors).observe(tb, { attributes: true, attributeFilter: ["class"] });
  })();

  /* edit is an exclusive page mode: entering it exits present/reel/x-ray and
     vice versa; closeDrawer's own unsaved-changes confirm acts as the veto */
  /* ⌥E / Alt-E toggles edit mode — layout-independent, ignored while typing */
  document.addEventListener("keydown", function (e) {
    if (!e.altKey || e.code !== "KeyE" || e.ctrlKey || e.metaKey) return;
    /* an embedding page said editable=0 — the hotkey honours it like the
       pill and the drawer itself (Canvas vault iframe, 2026-07-30) */
    if (window.lcEditLocked()) return;
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    e.preventDefault();
    if (window.lcMode) window.lcMode.set("edit");
  });

  if (window.lcMode) window.lcMode.register("edit", {
    enter: openDrawer,
    exit: closeDrawer,
    isActive: function () {
      var d = document.getElementById("ed-drawer");
      return !!(d && d.classList.contains("open"));
    }
  });

  /* A stored key that GitHub no longer accepts (expired, revoked, rescoped) is
     the worst state to be in silently: the file list errors and the filename
     shows ⚠️, so the picker "looks broken" — and because ⚙️ Connect is a
     COLLAPSED <details>, and we only auto-expand it when no key is stored, the
     way back in is invisible. When a load fails, surface the sign-in. */
  function promptReconnect(why) {
    var setup = document.getElementById("ed-setup");
    if (setup) setup.open = true;
    openFilePanel();
    setStatus(why || "GitHub refused this key — reconnect below.", false);
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
        el.innerHTML = "<span style='color:#dc3545;font-size:0.85em'>" + esc(data.message || "Error") + "</span>";
        promptReconnect("GitHub refused this key for " + esc(_repo) + " (" + esc(data.message || "error") + ") — reconnect below.");
        return;
      }
      var rows = data.tree.filter(function (f) {
        var name = f.path.split("/").pop();
        // include underscore modules (e.g. _dog.md) — they're editable content too,
        // but skip Jekyll/system files that aren't meant to be hand-edited here
        if (name === "_config.yml" || name === "_build_trigger.md") return false;
        if (f.type !== "blob" || !name.endsWith(".md")) return false;
        // runner-edit browses the rendered repo's WHOLE md tree (course material
        // and benches live outside docs/); a normal page edit stays under docs/.
        return _runnerEdit ? true : f.path.startsWith("docs/");
      }).sort(function (a, b) { return a.path.localeCompare(b.path); })
      .map(function (f) {
        var rel = _runnerEdit ? f.path : f.path.replace(/^docs\//, "");
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
          onRowClicked: function (e) { loadFile(e.data.path); closeFilePanel(); }
        });
      }
      /* Picking another file must never depend on a CDN. AG Grid is a nicety
         here — a few hundred filenames are a list, not a data grid — but when
         jsdelivr is blocked (corporate net, a content blocker, an offline
         iPad) its onload never fired and the panel sat at "Loading…" forever,
         indistinguishable from broken. So: use the grid when it is actually
         there, otherwise render a plain list that always works. */
      function buildPlainList(why) {
        el.innerHTML = "";
        if (why) {
          var note = document.createElement("div");
          note.style.cssText = "color:#92400e;background:#fffbeb;border:1px solid #fcd34d;border-radius:5px;padding:.3em .5em;margin-bottom:.4em;font-size:.82em";
          note.textContent = why;
          el.appendChild(note);
        }
        var list = document.createElement("div");
        list.style.cssText = "max-height:320px;overflow:auto";
        rows.forEach(function (r) {
          var a = document.createElement("a");
          a.href = "#"; a.className = "ed-chip"; a.dataset.path = r.path; a.textContent = r.file;
          if (r.path === _curFile) a.classList.add("active");
          list.appendChild(a);            // the delegated .ed-chip handler loads it
        });
        el.appendChild(list);
      }
      if (window.agGrid && window.agGrid.createGrid) { buildGrid(); return; }
      /* give the shared loader a bounded chance, then fall back — a hang is
         worse than a plain list */
      var settled = false, giveUp = setTimeout(function () {
        if (settled || (window.agGrid && window.agGrid.createGrid)) return;
        settled = true;
        buildPlainList("Couldn't load the file browser — showing a simple list.");
      }, 4000);
      function grid() { if (settled) return; settled = true; clearTimeout(giveUp); buildGrid(); }
      if (window.lcLoadAgGrid) { window.lcLoadAgGrid(grid); return; }
      function addCss(h) { var l=document.createElement("link"); l.rel="stylesheet"; l.href=h; document.head.appendChild(l); }
      addCss("https://cdn.jsdelivr.net/npm/ag-grid-community@31/styles/ag-grid.css");
      addCss("https://cdn.jsdelivr.net/npm/ag-grid-community@31/styles/ag-theme-alpine.css");
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/ag-grid-community@31/dist/ag-grid-community.min.js";
      s.onload = grid;
      s.onerror = function () {
        if (settled) return; settled = true; clearTimeout(giveUp);
        buildPlainList("Couldn't load the file browser — showing a simple list.");
      };
      document.head.appendChild(s);
    }).catch(function () {
      if (el) el.innerHTML = "<span style='color:#dc3545;font-size:0.85em'>Network error</span>";
      promptReconnect("Couldn't reach GitHub with this key — check the connection, or reconnect below.");
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
      if (!data.content) {
        toast("Load failed: " + esc(data.message || ""), false);
        /* the toast fades — leave the reason where the filename goes */
        _curFile = null;
        var fnErr = document.getElementById("ed-filename");
        if (fnErr) fnErr.textContent = "⚠️ " + path + " — " + (data.message || data.error || "load failed");
        return;
      }
      _curSha = data.sha;
      var content = b64d(data.content.replace(/\n/g, ""));
      _savedContent = content;
      if (inp) { inp.value = content; if (inp._hist) inp._hist.reset(); updatePreview(content); }
      /* FOLDED BY DEFAULT (Michel, 2026-08-23): a page arrives as its
         outline — every fenced block one marker line wearing its icon and
         knobs — so the Raw tab reads modular; unfold what you touch. Only
         the LOAD folds: AI edits and typing never re-collapse the file. */
      if (window._lcEdFold) window._lcEdFold.foldAll();
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
      var lintErrs = (_lintFindings || []).filter(function (f) { return f.sev === "error"; });
      if (lintErrs.length && !confirm("⚠️ " + lintErrs.length + " reference/id error" +
          (lintErrs.length === 1 ? "" : "s") + " in the draft (see the ✖ chip). Save anyway?")) return;
      /* LAST GATE: a fold marker in the outgoing content means folded lines
         lost their source (a bug, not a state) — refuse rather than commit
         a page with its fences amputated (Michel, 2026-08-24). */
      if (/\u2060/.test(inp.value)) {
        toast("⚠️ folded blocks lost their content — press ▾ unfold, reload the file, then save", false);
        return;
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
        _savedSinceOpen = true;   // closing the drawer refreshes the page from this
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
        /* A file outside the Pages tree (courses/, hubs/…) declares itself on
           the preview via the data-lc-src contract the runner's render root
           already carries — so folder-aware components (embed) resolve
           against ITS folder, not docs/. docs/ files stay unstamped: their
           embeds keep the site-root meaning, exactly as before. */
        if (_curFile && !/^docs(\/|$)/.test(_curFile)) {
          body.setAttribute("data-lc-src-path", _curFile);
          if (_repo) body.setAttribute("data-lc-src-repo", _repo);
        }
        body.innerHTML = (window.lcInlineIAL || function (h) { return h; })(marked.parse(normIAL(src)));
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
          /* A green build needs no forensics: show the status, keep the builder
             here. Only a FAILURE earns a way out to the CI logs — otherwise we
             invite everyone to go read YAML for no reason. */
          el.innerHTML = ok ? "✅ Built"
            : "❌ " + esc(run.conclusion) + " · <a href='" + run.html_url +
              "' target='_blank' rel='noopener' style='color:#0066cc'>see why</a>";
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
        /* stamp it: an unstamped pairing is refused by lcBench (a bench from
           another class must never be inherited) — this one is the author's */
        try { localStorage.setItem("lc_ed_session", window.lcAuthorPair || "lc:author"); } catch (e) {}
        setStatus("✓ " + d.full_name + (d.fork ? " (fork)" : ""), true);
        var setup = document.getElementById("ed-setup");
        if (setup) setup.open = false;
        toggleConnected(true);
        /* Only the STANDALONE runtime retargets the repo just verified (there the
           page has no file of its own). runnerTarget() is scoped to #lc-run, so a
           page merely hosting a runner demo can no longer hijack the sign-in. */
        var rt = runnerTarget();
        if (rt && rt.readonly) { lockReadOnly(rt); }
        else if (rt) { _repo = rt.repo; _runnerEdit = true; loadFiles(); loadFile(rt.path); }
        else {
          _runnerEdit = false;
          loadFiles();
          var fab = document.getElementById("ed-fab");
          if (fab && fab.dataset.pagePath) loadFile("docs/" + fab.dataset.pagePath);
        }
      } else {
        setStatus("Failed: " + esc(d.message || "unknown error"), false);
      }
    });
  }

  function disconnect() {
    localStorage.removeItem(LS_PAT); localStorage.removeItem(LS_REPO);
    try { localStorage.removeItem("lc_ed_session"); } catch (e) {}
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
    if (fab)   { e.preventDefault(); if (window.lcEditLocked()) return;
                 if (window.lcMode) window.lcMode.set("edit"); else openDrawer(); return; }
    if (close) { e.preventDefault(); if (window.lcMode) window.lcMode.set("read"); else closeDrawer(); return; }
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
    if (chip)  { e.preventDefault(); loadFile(chip.dataset.path); closeFilePanel(); return; }
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
    // Undo/redo in a code editor with its own history (native undo is wiped by
    // the toolbar/Blocks programmatic edits, so we drive our own stack).
    if ((e.metaKey || e.ctrlKey) && /^[zy]$/i.test(e.key)) {
      var ae = document.activeElement;
      if (ae && ae._hist) {
        e.preventDefault();
        if (/y/i.test(e.key) || e.shiftKey) ae._hist.redo(); else ae._hist.undo();
      }
    }
    /* Shift+Alt+E (⌥⇧E on Mac) opens the editor from anywhere it's available.
       e.code is used so Option+E's dead-key behaviour on Mac doesn't matter. */
    if (!e.ctrlKey && !e.metaKey && e.altKey && e.shiftKey && e.code === "KeyE") {
      var fab = document.getElementById("ed-fab");
      var dr = document.getElementById("ed-drawer");
      if (fab && getComputedStyle(fab).display !== "none" && dr && !dr.classList.contains("open")) {
        e.preventDefault(); openDrawer();
      }
    }
  });

  /* show the shortcut in the FAB tooltip, platform-appropriately */
  (function () {
    var fab = document.getElementById("ed-fab");
    if (!fab) return;
    var isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || "");
    fab.title = "Edit this page (" + (isMac ? "⌥⇧E" : "Alt+Shift+E") + ")";
  })();

  /* ── Files dropdown toggle ──────────────────────────── */
  /* Authored inside the filename button, the panel was at the mercy of every
     ancestor between it and the viewport: `top:100%` resolved against <body>
     (menu below the fold), and WebKit clips a fixed descendant of the drawer's
     `overflow:hidden` anyway — so on iPad the arrow flipped and nothing showed.
     Portal it to <body> on first open: no transformed ancestor, no clipping
     box, nothing left to resolve against but the viewport. Every open path
     goes through openFilePanel so none of them can skip the anchoring. */
  function anchorFilePanel() {
    var sb = document.getElementById("ed-sidebar"),
        fbtn = document.getElementById("ed-files-btn");
    if (!sb || !fbtn || !sb.classList.contains("ed-open")) return;
    var r = fbtn.getBoundingClientRect();
    sb.style.position = "fixed";
    sb.style.zIndex = "10000";
    sb.style.top = Math.round(r.bottom + 2) + "px";
    sb.style.left = Math.round(Math.min(r.left, Math.max(8, innerWidth - 300))) + "px";
    sb.style.maxHeight = Math.round(innerHeight - r.bottom - 16) + "px";
  }
  function openFilePanel() {
    var sb = document.getElementById("ed-sidebar"),
        fbtn = document.getElementById("ed-files-btn");
    if (!sb) return;
    if (sb.parentNode !== document.body) document.body.appendChild(sb);
    sb.classList.add("ed-open");
    if (fbtn) fbtn.classList.add("ed-open");
    anchorFilePanel();
  }
  function closeFilePanel() {
    var sb = document.getElementById("ed-sidebar"),
        fbtn = document.getElementById("ed-files-btn");
    if (sb) sb.classList.remove("ed-open");
    if (fbtn) fbtn.classList.remove("ed-open");
  }
  window.addEventListener("resize", anchorFilePanel);
  window.addEventListener("orientationchange", function () { setTimeout(anchorFilePanel, 250); });

  document.addEventListener("click", function(e) {
    var sb = document.getElementById("ed-sidebar");
    if (!sb) return;
    /* the panel now lives on <body>, so a click inside it never looks like a
       click on the button — check it first and leave the panel alone */
    if (e.target.closest("#ed-sidebar")) return;
    if (e.target.closest("#ed-files-btn")) {
      if (sb.classList.contains("ed-open")) closeFilePanel(); else openFilePanel();
    } else if (sb.classList.contains("ed-open")) {
      closeFilePanel();
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
            lines: chunk.slice().concat([line]), type: im[1], knobs: kn,
            subBlock: true, _parentType: block.type });
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
  /* author-defined model classes, parsed from the draft's python blocks:
     class Pet(Object): with Attr/State fields and @transition methods. The
     draft is the truth here (no runtime needed) — the picture matches what's
     in the editor, saved or not. */
  function pageUserClasses() {
    var inp = document.getElementById("ed-input");
    var out = {};
    if (!inp) return out;
    var fence = /```python\r?\n([\s\S]*?)\r?\n```/g, m;
    while ((m = fence.exec(inp.value || ""))) {
      var lines = m[1].split(/\r?\n/), icon = "", cur = null, pendTrans = false;
      lines.forEach(function (ln) {
        var mi = ln.match(/^@component\(.*icon\s*=\s*["']([^"']+)["']/);
        if (mi) { icon = mi[1]; return; }
        var mc = ln.match(/^class\s+(\w+)\s*\(\s*(\w+)\s*\)\s*:/);
        if (mc) {
          cur = { icon: icon, base: mc[2], fields: [], meths: [], assoc: [] };
          out[mc[1]] = cur; icon = ""; pendTrans = false; return;
        }
        if (!cur) return;
        if (/^\S/.test(ln)) { cur = null; return; }          // dedent → class body ended
        var mf = ln.match(/^\s+(\w+)\s*=\s*(Attr|State)\(\s*(?:["'](\w+)["']|(\w+))?/);
        if (mf) {
          var t = mf[3] || mf[4] || "str", isState = mf[2] === "State";
          cur.fields.push({ n: mf[1], t: t, state: isState });
          if (!isState && !/^(str|int|float|bool)$/.test(t)) cur.assoc.push({ n: mf[1], target: t });
          return;
        }
        if (/^\s+@transition\(/.test(ln)) { pendTrans = true; return; }
        var md = ln.match(/^\s+def\s+(\w+)\s*\(/);
        if (md) {
          if (md[1].charAt(0) !== "_") cur.meths.push({ n: md[1], trans: pendTrans });
          pendTrans = false;
        }
      });
    }
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
  function userLabel(n, u, users, nodes) {
    var parts = [(u.icon ? u.icon + " " : "") + dotEsc(n)];
    var attrs = u.fields.map(function (f) {
      // DRY: a reference drawn as an association edge is not repeated as an
      // attribute row (the row survives only when the target isn't drawn)
      var isRef = !/^(str|int|float|bool)$/.test(f.t) && !f.state;
      if (isRef && nodes && nodes[f.t]) return "";
      var ic = f.state ? "🎛️"
        : (_compIcons[f.t] || (users[f.t] || {}).icon || (_compModel[f.t] || {}).icon || "📦");
      return ic + " " + dotEsc(f.n) + "\\l";
    }).join("");
    var meths = u.meths.map(function (m) {
      return (m.trans ? "▹ " + dotEsc(m.n) + " ▹" : "▸ " + dotEsc(m.n)) + "\\l";
    }).join("");
    if (attrs) parts.push(attrs);
    if (meths) parts.push(meths);
    return "{" + parts.join("|") + "}";
  }
  function buildPageDot(present, users) {
    users = users || {};
    var userNames = Object.keys(users);
    if (!present.length && !userNames.length) return null;
    var nodes = {};
    present.forEach(function (n) { nodes[n] = "page"; });
    userNames.forEach(function (n) { if (!nodes[n]) nodes[n] = "user"; });
    // authored classes generalize to each other or into the component model
    userNames.forEach(function (n) {
      var b = users[n].base;
      if (b && !nodes[b] && !users[b] && _compModel[b]) nodes[b] = "base";
    });
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
    // classes are square records — rounded corners are reserved for states
    L.push('  node [' + FONT + ', shape=record, style=filled, color="gray75", fillcolor=white, fontsize=10, penwidth=0.5];');
    L.push('  edge [' + FONT + ', fontsize=8, penwidth=0.6, arrowsize=0.8];');
    Object.keys(nodes).forEach(function (n) {
      var lbl = nodes[n] === "user" ? userLabel(n, users[n], users, nodes) : nodeLabel(n);
      L.push('  ' + n + ' [label="' + lbl + '"' +
        (nodes[n] === "base" ? ', fillcolor="gray95", color="gray80"' : '') + ']');
    });
    // generalization edges (UML hollow triangle) toward Block / Object
    Object.keys(nodes).forEach(function (n) {
      var base = nodes[n] === "user" ? users[n].base : (_compModel[n].bases || [])[0];
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
    // authored references (bestie = Attr("Pet")) — blue, possibly reflexive
    userNames.forEach(function (owner) {
      users[owner].assoc.forEach(function (a) {
        if (!nodes[a.target]) return;
        L.push('  ' + owner + ' -> ' + a.target + ' [color=blue, fontcolor=blue, weight=8,' +
          ' headlabel="' + dotEsc(a.n) + '", labeldistance=2.2, arrowsize=0.7]');
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
    var users = pageUserClasses();
    var nUsers = Object.keys(users).length;
    if (!present.length && !nUsers) {
      pane.innerHTML = "<p style='color:#bbb;padding:1em'>No components on this page yet. " +
        "Add a <code>{: .datagrid }</code>, <code>{: .chart }</code>, … and the classes appear here.</p>";
      return;
    }
    if (!window.lcDotToSvg) {
      pane.innerHTML = "<p style='color:#b00;padding:1em'>Diagram engine unavailable.</p>";
      return;
    }
    var dot = buildPageDot(present, users);
    pane.innerHTML = "<p style='color:#bbb;padding:0.6em'>Rendering diagram…</p>";
    window.lcDotToSvg(dot).then(function (svg) {
      pane.innerHTML =
        "<div id='ed-diagram-legend'><b>" + present.length + "</b> component class" +
        (present.length === 1 ? "" : "es") +
        (nUsers ? " + <b>" + nUsers + "</b> authored model" + (nUsers === 1 ? "" : "s") : "") +
        " on this page — " +
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
      inp.value = newText; if (inp._hist) inp._hist.reset(); setDirty(true); updatePreview(newText);
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

  /* ── ✏️ formatting toolbar ────────────────────────────────
     Inserts plain markdown at the cursor/selection so an author can format by
     clicking instead of typing syntax — the stored file stays pure markdown.
     Reused on the Raw editor and the block Content field. */
  var FMT_BTNS =
    '<button type="button" data-fmt="undo" title="Undo (⌘Z)">&#8630;</button>' +
    '<button type="button" data-fmt="redo" title="Redo (⌘⇧Z)">&#8631;</button>' +
    '<span class="ed-fmt-sep"></span>' +
    '<button type="button" data-fmt="bold" title="Bold"><b>B</b></button>' +
    '<button type="button" data-fmt="italic" title="Italic"><i>I</i></button>' +
    '<button type="button" data-fmt="code" title="Inline code">&lt;&gt;</button>' +
    '<span class="ed-fmt-sep"></span>' +
    '<button type="button" data-fmt="h2" title="Heading">H</button>' +
    '<button type="button" data-fmt="list" title="Bullet list">&#8226;</button>' +
    '<button type="button" data-fmt="link" title="Link">&#128279;</button>' +
    '<span class="ed-fmt-sep"></span>' +
    '<select class="ed-fmt-col" title="Colour"><option value="">&#127912;</option>' +
      '<option value="red">red</option><option value="green">green</option>' +
      '<option value="blue">blue</option><option value="amber">amber</option>' +
      '<option value="hl">highlight</option></select>';

  function applyFmt(ta, kind, arg) {
    if (ta._hist) ta._hist.flush();   // capture the pre-format state so undo can revert it
    var s = ta.selectionStart, e = ta.selectionEnd, v = ta.value, sel = v.slice(s, e);
    function set(val, ns, ne) { ta.value = val; ta.selectionStart = ns; ta.selectionEnd = ne; }
    function wrap(mark) {
      var t = sel || "text";
      set(v.slice(0, s) + mark + t + mark + v.slice(e), s + mark.length, s + mark.length + t.length);
    }
    function prefix(p) {
      var ls = v.lastIndexOf("\n", s - 1) + 1, le = v.indexOf("\n", e); if (le < 0) le = v.length;
      var blk = v.slice(ls, le).split("\n").map(function (l) { return p + l; }).join("\n");
      set(v.slice(0, ls) + blk + v.slice(le), ls, ls + blk.length);
    }
    if (kind === "bold") wrap("**");
    else if (kind === "italic") wrap("*");
    else if (kind === "code") wrap("`");
    else if (kind === "h2") prefix("## ");
    else if (kind === "list") prefix("- ");
    else if (kind === "link") {
      var lt = sel || "text", li = "[" + lt + "](url)";
      set(v.slice(0, s) + li + v.slice(e), s + li.length - 4, s + li.length - 1);
    } else if (kind === "colour") {
      var ct = sel || "text", ci = "*" + ct + "*{: ." + (arg || "red") + "}";
      set(v.slice(0, s) + ci + v.slice(e), s + 1, s + 1 + ct.length);
    }
    ta.dispatchEvent(new Event("input", { bubbles: true }));
    ta.focus();
  }

  /* ── undo/redo history for a code editor ──────────────────
     The format toolbar (and the Blocks grid) set ta.value directly, which wipes
     the browser's native undo — so each editor textarea keeps its own snapshot
     stack. Typing runs coalesce (debounced); format actions flush first. */
  function edHist(ta) {
    if (ta._hist) return ta._hist;
    var undo = [{ v: ta.value, s: ta.selectionStart || 0, e: ta.selectionEnd || 0 }];
    var redo = [], timer = null, applying = false, MAX = 200;
    function snap() {
      timer = null;
      var top = undo[undo.length - 1];
      if (top && top.v === ta.value) return;
      undo.push({ v: ta.value, s: ta.selectionStart, e: ta.selectionEnd });
      if (undo.length > MAX) undo.shift();
      redo.length = 0;
    }
    function restore(st) {
      applying = true;
      ta.value = st.v;
      try { ta.selectionStart = st.s; ta.selectionEnd = st.e; } catch (_) {}
      ta.dispatchEvent(new Event("input", { bubbles: true }));  // preview + dirty
      applying = false; ta.focus();
    }
    ta.addEventListener("input", function () {
      if (applying) return;
      clearTimeout(timer); timer = setTimeout(snap, 220);
    });
    ta._hist = {
      flush: function () { clearTimeout(timer); snap(); },
      reset: function () { clearTimeout(timer); timer = null;
        undo = [{ v: ta.value, s: 0, e: 0 }]; redo = []; },
      undo: function () {
        clearTimeout(timer); snap();
        if (undo.length < 2) return;
        redo.push(undo.pop());
        restore(undo[undo.length - 1]);
      },
      redo: function () {
        clearTimeout(timer);
        if (!redo.length) return;
        var st = redo.pop(); undo.push(st); restore(st);
      }
    };
    return ta._hist;
  }

  function attachFmtToolbar(ta) {
    if (!ta || ta.dataset.fmtBar) return;
    ta.dataset.fmtBar = "1";
    edHist(ta);   // give this editor an undo/redo stack
    var bar = document.createElement("div");
    bar.className = "ed-fmt-bar";
    bar.innerHTML = FMT_BTNS;
    /* the Raw textarea sits in a flex row (gutter | textarea); put the toolbar
       in the column above that row, not inside it */
    var anchor = ta.closest("#ed-raw-body") || ta;
    anchor.parentNode.insertBefore(bar, anchor);
    // keep the textarea's focus + selection when a format button is clicked
    bar.addEventListener("mousedown", function (ev) { if (ev.target.closest("button[data-fmt]")) ev.preventDefault(); });
    bar.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-fmt]"); if (!b) return;
      ev.preventDefault();
      var f = b.getAttribute("data-fmt");
      if (f === "undo") { if (ta._hist) ta._hist.undo(); return; }
      if (f === "redo") { if (ta._hist) ta._hist.redo(); return; }
      applyFmt(ta, f);
    });
    var col = bar.querySelector(".ed-fmt-col");
    if (col) col.addEventListener("change", function () {
      if (col.value) { applyFmt(ta, "colour", col.value); col.value = ""; }
    });
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
      + "<div class='ebf-actions'><a href='#' class='button' id='ebf-apply' style='font-size:0.82em;padding:0.32em 0.9em'>Apply</a></div>";

    attachFmtToolbar(document.getElementById("ebf-content"));   // format-by-click on the Content field

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
      inp.value = newText; if (inp._hist) inp._hist.reset(); setDirty(true); updatePreview(newText);
      buildGrid();
      pushAction(iconFor(type) || "✏️", "Edited " + (type ? compName(type) : (title || "block")).slice(0, 40), before);
    });
  }

  /* Line-number gutter for the Raw editor: numbers track the content (typing,
     file loads, AI edits, format inserts) and follow the textarea's scroll. */
  function initRawGutter() {
    var input = document.getElementById("ed-input");
    var inner = document.getElementById("ed-gutter-inner");
    if (!input || !inner) return;
    /* ONCE, forever. Re-opening the drawer used to re-run this, rebinding
       the value property to a FRESH (empty) fold map while the display
       still held the old session's markers — the "full" value then WAS the
       folded text, and one save committed markers to git, content gone
       (Michel, 2026-08-24, classroom3). One closure per page lifetime. */
    if (input._lcGutterWired) return;
    input._lcGutterWired = true;
    var desc = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value");

    /* ── Folding (Michel, 2026-08-23: "fold/unfold blocks") ─────────────
       A fold swaps a fenced block's lines for ONE marker line in the
       DISPLAY only. The value property stays virtual-full: every reader —
       save, blocks grid, features, preview, diff — always sees the whole
       source, so a folded file can never be committed folded. Clicking a
       marker line (or typing into it) unfolds it in place. */
    var folds = {}, foldSeq = 0;
    /* the marker's machine half is INVISIBLE (Michel, 2026-08-23: "not even
       clear what ⟢f19⟣ means"): the fold id rides as zero-width characters —
       U+2060 sentinels around a binary of U+200B (0) / U+200C (1) — so the
       reader sees only icon · type · preview · count. The virtual value
       substitutes the whole line back, so the invisibles can never be saved. */
    var MARK = /\u2060([\u200B\u200C]+)\u2060/;
    function encId(id) {
      var b = Number(id).toString(2), out = "\u2060";
      for (var i = 0; i < b.length; i++) out += b[i] === "1" ? "\u200C" : "\u200B";
      return out + "\u2060";
    }
    function decId(bits) {
      var n = 0;
      for (var i = 0; i < bits.length; i++) n = n * 2 + (bits.charAt(i) === "\u200C" ? 1 : 0);
      return String(n);
    }
    function markId(line) {
      var m = line.match(MARK);
      return m ? decId(m[1]) : null;
    }
    function dv() { return desc.get.call(input); }                 /* display */
    function fullOf(v) {
      /* recursive: a folded outer fence may hold inner markers */
      for (var guard = 0; guard < 12; guard++) {
        if (!Object.keys(folds).length) return v;
        var changed = false;
        v = v.split("\n").map(function (line) {
          var id = markId(line);
          if (id != null && folds[id] != null) { changed = true; return folds[id]; }
          return line;
        }).join("\n");
        if (!changed) break;
      }
      return v;
    }
    function setDisplay(v) { desc.set.call(input, v); refresh(); }
    function regionAt(lines, i) {
      /* the fold region opened by line i, or null. IAL lines ride along. */
      var m = lines[i].match(/^(`{3,}|~{3,})/);
      if (!m || MARK.test(lines[i])) return null;
      var tick = m[1].charAt(0), len = m[1].length, j = i + 1;
      while (j < lines.length) {
        var c = lines[j].match(/^(`{3,}|~{3,})\s*$/);
        if (c && c[1].charAt(0) === tick && c[1].length >= len) break;
        j++;
      }
      if (j >= lines.length) return null;
      while (j + 1 < lines.length && /^\{:/.test(lines[j + 1])) j++;
      return j;
    }
    function foldLabel(region) {
      /* icon + type FIRST, like the block's visible cue; then #id and key
         knobs when it has them, else the first words of the first content
         line as a preview; the line count trails (Michel, 2026-08-23) */
      var ial = "";
      for (var k = region.length - 1; k >= 0 && /^\{:/.test(region[k]); k--) {
        if (/^\{:\s*\./.test(region[k])) { ial = region[k]; break; }
      }
      var preview = "";
      for (var c = 1; c < region.length - 1; c++) {
        var t = region[c].trim();
        if (t && !/^[`~]/.test(t) && !/^\{:/.test(t)) { preview = t.slice(0, 34); break; }
      }
      if (ial) {
        var type = (ial.match(/\.([\w-]+)/) || [])[1] || "";
        var bid = (ial.match(/#([\w-]+)/) || [])[1] || "";
        var knobs = [], kr = /(\w+)="([^"]*)"/g, km;
        while ((km = kr.exec(ial)) && knobs.length < 2)
          knobs.push(km[1] + '="' + km[2] + '"');
        var icon = iconFor(type);
        var cue = bid ? " #" + bid + (knobs.length ? " " + knobs.join(" ") : "")
                      : knobs.length ? " " + knobs.join(" ")
                      : preview ? " · " + preview : "";
        return ((icon ? icon + " " : "") + "." + type + cue).slice(0, 72);
      }
      var lang = region[0].replace(/^[`~]+/, "").trim();
      return ((lang || "…") + (preview ? " · " + preview : "")).slice(0, 60);
    }
    function foldRegion(lines, i, j) {
      var region = lines.slice(i, j + 1);
      var id = ++foldSeq;
      folds[id] = region.join("\n");
      return "▸ " + foldLabel(region) + " · " + region.length + " lines" + encId(id);
    }
    function foldAll() {
      var lines = dv().split("\n"), out = [], i = 0;
      while (i < lines.length) {
        var j = regionAt(lines, i);
        if (j == null || j - i + 1 < 3) { out.push(lines[i]); i++; continue; }
        out.push(foldRegion(lines, i, j));
        i = j + 1;
      }
      setDisplay(out.join("\n"));
    }
    function foldAt(i) {
      var lines = dv().split("\n");
      var j = regionAt(lines, i);
      if (j == null) return;
      var marker = foldRegion(lines, i, j);
      lines.splice(i, j - i + 1, marker);
      setDisplay(lines.join("\n"));
    }
    function unfoldOne(id) {
      var lines = dv().split("\n");
      for (var i = 0; i < lines.length; i++) {
        if (markId(lines[i]) === String(id) && folds[id] != null) {
          lines[i] = folds[id];
          delete folds[id];
          setDisplay(lines.join("\n"));
          return;
        }
      }
    }
    function unfoldAll() { setDisplay(fullOf(dv())); folds = {}; refresh(); }
    function caretFold() {
      var v = dv(), pos = input.selectionStart || 0;
      var start = v.lastIndexOf("\n", pos - 1) + 1;
      var end = v.indexOf("\n", pos); if (end < 0) end = v.length;
      return markId(v.slice(start, end));
    }
    input.addEventListener("click", function () {
      var id = caretFold(); if (id != null) unfoldOne(id);
    });
    input.addEventListener("beforeinput", function (e) {
      /* an edit must never land ON a marker — unfold it and let them retry */
      var id = caretFold();
      if (id != null) { e.preventDefault(); unfoldOne(id); }
    });
    window._lcEdFold = { foldAll: foldAll, unfoldAll: unfoldAll,
                         count: function () { return Object.keys(folds).length; } };

    function render() {
      /* numbers are SOURCE numbers: a fold marker wears its region's first
         line and the next visible line resumes after the hidden ones —
         and every fence line wears its own ▾/▸ (Michel, 2026-08-23) */
      var lines = dv().split("\n"), h = "", src = 1;
      for (var i = 0; i < lines.length; i++) {
        var fid = markId(lines[i]);
        var arrow = "";
        if (fid != null && folds[fid] != null) {
          arrow = "<span class='ed-fold-a' data-unfold='" + fid + "' title='unfold'>▸</span>";
          h += "<div class='ed-gl'>" + arrow + src + "</div>";
          src += folds[fid].split("\n").length;
        } else {
          if (regionAt(lines, i) != null) {
            arrow = "<span class='ed-fold-a' data-foldline='" + i + "' title='fold this block'>▾</span>";
          }
          h += "<div class='ed-gl'>" + arrow + src + "</div>";
          src += 1;
        }
      }
      inner.innerHTML = h;
    }
    inner.addEventListener("click", function (e) {
      var a = e.target.closest(".ed-fold-a");
      if (!a) return;
      if (a.hasAttribute("data-unfold")) unfoldOne(a.getAttribute("data-unfold"));
      else foldAt(parseInt(a.getAttribute("data-foldline"), 10));
    });
    function sync() { inner.style.transform = "translateY(" + (-input.scrollTop) + "px)"; }
    function refresh() { render(); sync(); }
    input.addEventListener("input", refresh);
    input.addEventListener("scroll", sync);
    /* programmatic writes (loadFile, AI edits, feature status) bypass the
       'input' event — intercept the value property once: reads are always
       the FULL source (folds substituted back), writes reset the folds */
    try {
      Object.defineProperty(input, "value", {
        configurable: true,
        get: function () { return fullOf(desc.get.call(this)); },
        set: function (v) { folds = {}; desc.set.call(this, v); refresh(); }
      });
    } catch (e) {}
    window._lcEdGutterRefresh = refresh;
    /* the workshop bar grows the two fold buttons */
    var shop = document.getElementById("ed-raw-shop");
    if (shop && !shop.querySelector(".ed-fold-btn")) {
      var bf = document.createElement("button");
      bf.className = "ed-fold-btn"; bf.textContent = "▸ fold blocks"; bf.title = "collapse every fenced block to one line (display only — saves always carry the full source)";
      var bu = document.createElement("button");
      bu.className = "ed-fold-btn"; bu.textContent = "▾ unfold"; bu.title = "restore every folded block";
      [bf, bu].forEach(function (b) {
        b.style.cssText = "margin-left:8px;font:inherit;font-size:0.85em;background:#313244;color:#cdd6f4;border:none;border-radius:5px;padding:1px 9px;cursor:pointer";
      });
      bf.addEventListener("click", foldAll);
      bu.addEventListener("click", unfoldAll);
      var grow = shop.querySelector(".ed-shop-grow");
      shop.insertBefore(bf, grow); shop.insertBefore(bu, grow);
    }
    refresh();
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
    if (name === "raw" && window._lcEdGutterRefresh) window._lcEdGutterRefresh();
    if (name === "blocks") buildGrid();
    if (name === "log") renderLog();
    if (name === "features") openFeatures();
    if (name === "diagram") renderDiagram();
  });

  /* ── ✓ draft linter (Tier 1) ──────────────────────────────
     Checks the draft as you type: python fences compile (via the shared
     MicroPython, no execution), yaml fences parse, IAL knobs match the
     component model, component ids are unique and python-istic, and
     reference knobs (bind / bound-to / target / …) plus avatar `at: "#id"`
     cues resolve to ids/anchors that exist in the draft. Severities:
     error = broken reference / duplicate id (would fail at runtime),
     warn = syntax, info = suspicious knob. Advisory: save asks, never blocks. */
  var _lintFindings = [], _lintTimer = null, _lintSeq = 0;
  var LINT_REF_KNOBS = { "bind": 1, "bound-to": 1, "target": 1, "master": 1, "bound": 1 };

  function edLoadYaml(cb) {
    if (window.jsyaml) return cb(window.jsyaml);
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js";
    s.onload = function () { cb(window.jsyaml); };
    s.onerror = function () { cb(null); };
    document.head.appendChild(s);
  }

  var LINT_LIVE_CONTAINERS = { blocks: 1, block: 1, accordion: 1, tabs: 1,
                               cards: 1, grid: 1, radio: 1, carousel: 1 };

  function lintParse(text) {
    /* fences can nest; a lang-less fence whose trailing IAL marks it as a
       section container (.blocks/.accordion/…) holds LIVE blocks — anything
       else fenced is display-only text and must not contribute ids, refs or
       code to the checks. */
    var lines = text.split("\n");
    var fences = [], stack = [], owner = [];
    lines.forEach(function (ln, i) {
      var f = ln.match(/^(`{3,})(\w*)\s*$/);
      if (f) {
        var top = stack[stack.length - 1];
        if (top && f[1].length >= top.ticks && !f[2]) {
          top.end = i; fences.push(stack.pop());
        } else {
          stack.push({ ticks: f[1].length, lang: (f[2] || "").toLowerCase(),
                       start: i, end: -1, parent: top || null, live: false });
        }
        owner[i] = stack[stack.length - 1] || null;
        return;
      }
      owner[i] = stack[stack.length - 1] || null;
    });
    while (stack.length) { var u = stack.pop(); u.end = lines.length; fences.push(u); }
    /* liveness: the first IAL right after a lang-less fence names its container */
    fences.forEach(function (f) {
      if (f.lang) return;
      for (var j = f.end + 1; j <= f.end + 2 && j < lines.length; j++) {
        var m = (lines[j] || "").match(/^\{:(.+)\}\s*$/);
        if (m) {
          lintIal(m[1], j).classes.forEach(function (c) { if (LINT_LIVE_CONTAINERS[c]) f.live = true; });
          break;
        }
        if ((lines[j] || "").trim()) break;
      }
    });
    function chainLive(f) {
      while (f) {
        if (f.lang || !f.live) return false;   // code fences never host IALs
        f = f.parent;
      }
      return true;
    }
    var ials = [], ids = {};
    lines.forEach(function (ln, i) {
      if (!chainLive(owner[i])) return;        // display-only region
      var m = ln.match(/^\{:(.+)\}\s*$/);
      if (m) ials.push(lintIal(m[1], i));
      var h = ln.match(/\{#([A-Za-z_][\w-]*)\}/);
      if (h && ids[h[1]] === undefined) ids[h[1]] = i;
    });
    ials.forEach(function (a) {
      if (a.id && ids[a.id] === undefined) ids[a.id] = a.line;
    });
    fences.forEach(function (f) {
      f.body = lines.slice(f.start + 1, f.end).join("\n");
      f.checked = (f.parent === null) || chainLive(f.parent);   // code checks apply to live code only
    });
    /* authored classes are identifiers too (Michel, 2026-08-23): a grid
       binds a CLASS the python above declares — bind="Student",
       of="Student" — and that must not read as a broken reference */
    fences.forEach(function (f) {
      if (f.lang !== "python") return;
      f.body.split("\n").forEach(function (ln, j) {
        var cm = ln.match(/^class\s+([A-Za-z_]\w*)\s*[(:]/);
        if (cm && ids[cm[1]] === undefined) ids[cm[1]] = f.start + 1 + j;
      });
    });
    return { lines: lines, fences: fences, ials: ials, ids: ids };
  }

  function lintIal(inner, line) {
    var classes = [], id = null, knobs = {}, m;
    var reC = /(?:^|\s)\.([\w-]+)/g, reI = /(?:^|\s)#([\w-]+)/g, reK = /([\w-]+)="([^"]*)"/g;
    while ((m = reC.exec(inner))) classes.push(m[1]);
    while ((m = reI.exec(inner))) id = m[1];
    while ((m = reK.exec(inner))) knobs[m[1]] = m[2];
    return { line: line, classes: classes, id: id, knobs: knobs };
  }

  function lintDraft(text, done) {
    var P = lintParse(text), F = [];
    function add(sev, line, msg) { F.push({ sev: sev, line: line, msg: msg }); }

    /* ids: duplicates + python-istic (component ids only) */
    var seen = {};
    P.ials.forEach(function (a) {
      if (!a.id) return;
      if (seen[a.id] !== undefined) add("error", a.line, "duplicate id #" + a.id + " (first at line " + (seen[a.id] + 1) + ")");
      else seen[a.id] = a.line;
      if (!/^[A-Za-z_]\w*$/.test(a.id)) add("warn", a.line, "id #" + a.id + " is not a python identifier");
    });

    /* references: knob → an id that exists in the draft */
    P.ials.forEach(function (a) {
      Object.keys(a.knobs).forEach(function (k) {
        if (LINT_REF_KNOBS[k] && a.knobs[k] && P.ids[a.knobs[k]] === undefined) {
          add("warn", a.line, k + '="' + a.knobs[k] + '" — no such id in this draft (ok if it\'s created at runtime)');
        }
      });
    });

    /* avatar cues: at: "#id" must resolve (heading anchors count) */
    P.fences.forEach(function (f) {
      if (f.lang !== "yaml" || !f.checked) return;
      f.body.split("\n").forEach(function (ln, j) {
        var m = ln.match(/^\s*(?:-\s+)?at:\s*["']#([A-Za-z_][\w-]*)["']/);
        if (m && P.ids[m[1]] === undefined) {
          add("warn", f.start + 1 + j + 1, 'at: "#' + m[1] + '" — no such id/anchor in this draft (ok if generated at runtime)');
        }
      });
    });

    /* knobs vs the component model (conservative: only exact type matches) */
    if (_compModel) P.ials.forEach(function (a) {
      var cls = null;
      for (var i = 0; i < a.classes.length && !cls; i++) {
        var cn = compName(a.classes[i]);
        if (_compModel[cn]) cls = _compModel[cn];
      }
      if (!cls) return;
      (cls.attrs || []).forEach(function (at) {
        var v = a.knobs[at.n];
        if (v === undefined) return;
        if ((at.t === "int" || at.t === "float") && v !== "" && isNaN(Number(v))) {
          add("info", a.line, at.n + '="' + v + '" — expected a ' + at.t);
        }
        if (at.t === "bool" && !/^(true|false|1|0|yes|no|on|off)$/i.test(v)) {
          add("info", a.line, at.n + '="' + v + '" — expected true/false');
        }
      });
    });

    /* yaml fences parse */
    var yamls = P.fences.filter(function (f) { return f.lang === "yaml" && f.checked && f.body.trim(); });
    /* python fences compile (module-level; gherkin :::python steps as functions) */
    var pys = [];
    P.fences.forEach(function (f) {
      if (!f.checked) return;
      if (f.lang === "python" && f.body.trim()) pys.push({ line: f.start + 1, src: f.body });
      if (f.lang === "gherkin") {
        var rel = 0, inPy = false, buf = [], at0 = 0;
        f.body.split("\n").forEach(function (ln, j) {
          if (/^\s*:::python\s*$/.test(ln)) { inPy = true; buf = []; at0 = j; return; }
          if (/^\s*:::\s*$/.test(ln)) {
            if (inPy && buf.length) pys.push({ line: f.start + 1 + at0 + 1,
              src: "def _lint(self):\n" + buf.map(function (l) { return "    " + l; }).join("\n") });
            inPy = false; return;
          }
          if (inPy) buf.push(ln);
        });
      }
    });

    var seq = ++_lintSeq, pending = 1;
    function finish() { if (--pending === 0 && seq === _lintSeq) done(F.sort(function (x, y) { return x.line - y.line; })); }

    if (yamls.length) {
      pending++;
      edLoadYaml(function (jsyaml) {
        if (jsyaml) yamls.forEach(function (f) {
          try { jsyaml.load(f.body); }
          catch (e) {
            var l = (e.mark && typeof e.mark.line === "number") ? f.start + 1 + e.mark.line + 1 : f.start + 1;
            add("warn", l, "yaml: " + String(e.reason || e.message || e).slice(0, 90));
          }
        });
        finish();
      });
    }
    if (pys.length && window._lcMpReady) {
      pending++;
      window._lcMpReady.then(function (mp) {
        try {
          var run = mp.runPython || mp.exec || mp.pyexec || mp.run;
          window._edLintSrcs = pys.map(function (p) { return p.src; });
          run.call(mp,
            "import js, json\n" +
            "_out = []\n" +
            "for _i in range(int(js.window._edLintSrcs.length)):\n" +
            "    try:\n" +
            "        compile(str(js.window._edLintSrcs[_i]), '<lint>', 'exec')\n" +
            "    except Exception as _e:\n" +
            "        _out.append([_i, str(_e)])\n" +
            "js.window._edLintPy = json.dumps(_out)\n");
          JSON.parse(window._edLintPy || "[]").forEach(function (r) {
            add("warn", pys[r[0]].line, "python: " + String(r[1]).slice(0, 90));
          });
        } catch (e) { /* runtime unavailable → skip python checks */ }
        finish();
      }).catch(finish);
    }
    finish();
  }

  function renderLint() {
    var chip = document.getElementById("ed-lint");
    var panel = document.getElementById("ed-lint-panel");
    if (!chip || !panel) return;
    var errs = _lintFindings.filter(function (f) { return f.sev === "error"; }).length;
    var warns = _lintFindings.filter(function (f) { return f.sev !== "error"; }).length;
    chip.className = errs ? "err" : (warns ? "warn" : "");
    chip.textContent = errs ? "✖ " + errs + (warns ? " +" + warns : "")
                     : (warns ? "⚠ " + warns : "✓");
    var ICONS = { error: "✖", warn: "⚠", info: "ℹ" };
    panel.innerHTML = _lintFindings.length
      ? _lintFindings.map(function (f) {
          return "<div class='ed-lint-item' data-line='" + f.line + "'>" +
            "<span>" + ICONS[f.sev] + "</span><span class='ln'>" + (f.line + 1) + "</span>" +
            "<span class='msg'>" + escH(f.msg) + "</span></div>";
        }).join("")
      : "<div class='ed-lint-empty'>✓ no findings — ids, references, knobs and syntax look good</div>";
  }

  window._edLintSoon = function () {
    clearTimeout(_lintTimer);
    _lintTimer = setTimeout(function () {
      var inp = document.getElementById("ed-input");
      if (!inp || !inp.value) { _lintFindings = []; renderLint(); return; }
      lintDraft(inp.value, function (f) { _lintFindings = f; renderLint(); });
    }, 900);
  };

  document.addEventListener("click", function (e) {
    var chip = e.target.closest("#ed-lint");
    var panel = document.getElementById("ed-lint-panel");
    if (chip && panel) { panel.classList.toggle("open"); return; }
    var item = e.target.closest(".ed-lint-item");
    if (item) {
      var ln = parseInt(item.getAttribute("data-line"), 10);
      var tab = document.querySelector('.ed-tab[data-tab="raw"]');
      if (tab) tab.click();
      var ta = document.getElementById("ed-input");
      if (ta) {
        var pos = 0, ls = ta.value.split("\n");
        for (var i = 0; i < ln && i < ls.length; i++) pos += ls[i].length + 1;
        ta.focus();
        ta.setSelectionRange(pos, pos + (ls[ln] || "").length);
        var lh = parseFloat(getComputedStyle(ta).lineHeight) || 18;
        ta.scrollTop = Math.max(0, ln * lh - ta.clientHeight / 2);
      }
      return;
    }
    if (panel && panel.classList.contains("open") && !e.target.closest("#ed-lint-panel")) {
      panel.classList.remove("open");
    }
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
      // a sole-feature section yields a parent typed "feature" (plus a dup
      // sub-block); a feature sharing a section with other components yields
      // only a sub-block. Take feature parents, and feature sub-blocks whose
      // parent isn't itself a feature, so co-located specs still list here.
      if (b.type === "feature" && !(b.subBlock && b._parentType === "feature")) {
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
      prev.innerHTML = window.marked ? (window.lcInlineIAL || function (h) { return h; })(window.marked.parse(normIAL(md))) : "<pre>" + escH(md) + "</pre>";
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

  /* The vocabulary hint: a Lightcode page is built from COMPONENTS declared with
     an IAL line, not raw HTML/code fences. When the ask is unscoped ("add a
     block"), tell the model which components exist (snake_case IAL classes from
     the component model) so it proposes a real one, not a generic ``` fence. */
  function componentCatalog() {
    if (!_compModel) return "";
    var SKIP = { Object: 1, Block: 1, Blocks: 1, Page: 1, Dataset: 1, Query: 1, Bar: 1 };
    var names = Object.keys(_compModel)
      .filter(function (k) { return !SKIP[k]; })
      .map(function (k) { return k.replace(/([a-z0-9])([A-Z])/g, "$1_$2").toLowerCase(); })
      .sort();
    if (!names.length) return "";
    return "\n\nThis is a Lightcode page: interactive blocks are COMPONENTS, each " +
      "declared with an IAL line under a paragraph or heading — e.g.\n" +
      "`[my quiz](#)`\n`{: .quiz }`  or  `{: .chart source=\"data\" }`.\n" +
      "Available components (use the exact snake_case class): " + names.join(", ") + ".\n" +
      "When the instruction asks to add a block, component, widget or interactive " +
      "element, prefer a real component with its `{: .name }` IAL over a plain " +
      "markdown code fence; pick the most fitting one and name your choice.";
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
    /* the page composes from {: .embed } fragments living in OTHER files —
       fold them in so "make a quiz from this page" sees what the reader
       sees, not just the reference lines (lcEmbedRefs = the same SSOT the
       embed widget and the tutor's knowledge use) */
    var _fragDir = (_curFile || "").split("/").slice(0, -1).join("/");
    var _fragRefs = window.lcEmbedRefs ? window.lcEmbedRefs(page, _fragDir) : [];
    Promise.all(_fragRefs.map(function (fp) {
      return fetch("https://api.github.com/repos/" + _repo + "/contents/" + fp,
        { headers: { Authorization: "Bearer " + _pat, Accept: "application/vnd.github.v3.raw" } })
        .then(function (r) { return r.ok ? r.text() : ""; })
        .then(function (t) { return t ? "\n\n--- Embedded fragment: " + fp + " ---\n" + t.slice(0, 4000) : ""; })
        .catch(function () { return ""; });
    })).then(function (frags) {
    var fragNote = frags.join("");
    return fetch("https://models.github.ai/inference/chat/completions", {
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
            (scope.type ? "" : componentCatalog()) +
            "\n\nFull page for context:\n```markdown\n" + page + "\n```" +
            (fragNote ? "\n\nContent of fragments the page embeds ({: .embed }) — part of the page as the reader sees it:" + fragNote : "") }
        ]
      })
    });
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
      "<div class='ed-ag-approve'><a href='#' class='button' id='ed-ag-approve'>✓ Approve</a>" +
      "<a href='#' class='button button-secondary' id='ed-ag-retry'>↻ Retry</a></div>";
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
    var SITE_REPO = "{{ site.github.repository_nwo | default: '' }}";
    /* one credential per device, borrowed everywhere (T10): if the platform
       knows the builder (topbar sign-in shares this PAT) but the repo entry
       is gone, it is this very site's repo — never ask twice */
    if (_pat && !_repo) {
      _repo = SITE_REPO;
      if (_repo) {
        localStorage.setItem(LS_REPO, _repo);
        try { localStorage.setItem("lc_ed_session", window.lcAuthorPair || "lc:author"); } catch (e) {}
      } else _repo = null;
    }
    /* A PAGE OF THIS SITE BELONGS TO THIS SITE'S REPO. lc_ed_repo is ONE
       browser-wide pairing and the last bench to connect wins it — so after
       any bench or ship work, opening the editor on a plain pedia page
       connected it to the BENCH, which does not contain that page: an empty
       editor and no way to edit your own site (Michel, 2026-08-19,
       lightcodepedia.org/events). A runner render still targets what it
       rendered (rt.repo, below), and the pairing itself is left untouched —
       the bench keeps it. */
    if (SITE_REPO && _repo && _repo !== SITE_REPO && !runnerTarget()) _repo = SITE_REPO;
    var patEl = document.getElementById("ed-pat");
    var repoEl = document.getElementById("ed-repo");
    if (patEl && _pat)   patEl.value  = _pat;
    if (repoEl && _repo) repoEl.value = _repo;
    /* the node knows its own repo at build time — never make the builder
       type (or wrongly guess) it: prefill lab/pedia/fork alike */
    else if (repoEl) repoEl.value = "{{ site.github.repository_nwo | default: '' }}";
    if (_pat && _repo) {
      setStatus("✓ " + _repo, true);
      toggleConnected(true);
    }
    wireGrid(); // wire grid event delegation once, not on every buildGrid()
  });
})();
</script>
{% endif %}
