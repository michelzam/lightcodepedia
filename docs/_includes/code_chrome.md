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

.lc-datagrid { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-datagrid-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-datagrid-title .lc-datagrid-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-datagrid-grid { width: 100%; }
.lc-datagrid-status { padding: 0.7em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #666; font-style: italic; }
.lc-datagrid-err { padding: 0.9em 1em; color: #b00; background: #fff5f5; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; white-space: pre-wrap; }

.lc-form { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-form-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-form-title .lc-form-name { color: #222; font-weight: 600; }
.lc-form-title .lc-form-meta { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-form-grid { width: 100%; }
.lc-form-grid .ag-cell.lc-form-label-cell { color: #0066cc; font-weight: 600; background: #fafbfc; }
.lc-form-grid .ag-cell.lc-form-label-cell:hover { background: #fafbfc !important; }
.lc-form-grid .ag-row-hover .lc-form-label-cell { background: #fafbfc !important; }
.lc-form-bool { display: flex; align-items: center; gap: 0.5em; height: 100%; }
.lc-form-bool .lc-form-bool-cb { margin: 0; accent-color: #0066cc; cursor: pointer; }
.lc-form-bool .lc-form-bool-cb:disabled { cursor: default; }
.lc-form-bool .lc-form-bool-t { color: #2a7a2a; font-weight: 600; }
.lc-form-bool .lc-form-bool-f { color: #b00; font-weight: 600; }
.lc-form-null { color: #aaa; font-style: italic; }
.lc-form-num { color: #0a5; }
.lc-form-cellbox { display: flex; align-items: center; height: 100%; overflow: hidden; }
.lc-form-pills { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; line-height: 1.2; padding: 4px 0; }
.lc-form-pill { display: inline-flex; align-items: center; padding: 1px 9px; border-radius: 12px; background: #e7f1fe; color: #1756a9; font-size: 0.82em; border: 1px solid #c5dcf5; white-space: nowrap; line-height: 1.4; }
.lc-form-selectbox { display: inline-flex; align-items: center; gap: 0.4em; padding: 0 8px 0 10px; border: 1px solid #c5dcf5; background: #f5f9ff; border-radius: 4px; color: #1756a9; font-size: 0.88em; line-height: 1.7; max-width: 100%; box-sizing: border-box; }
.lc-form-selectbox-label { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lc-form-selectbox-arrow { color: #6892c4; font-size: 0.85em; }
.lc-form-empty { padding: 0.9em 1em; color: #888; font-style: italic; font-size: 0.9em; }
.lc-form-err { padding: 0.9em 1em; color: #b00; background: #fff5f5; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; white-space: pre-wrap; }
.lc-carousel { position: relative; padding: 1.2em 2em; min-height: 4em; background: #fafafa; border-left: 4px solid #0066cc; border-radius: 0 6px 6px 0; margin: 1em 0; }
.lc-carousel-item { display: none; font-style: italic; color: #444; line-height: 1.5; }
.lc-carousel-item.active { display: block; animation: lc-fade 0.4s ease; }
@keyframes lc-fade { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: none; } }
.lc-carousel-dots { text-align: center; margin-top: 0.8em; }
.lc-carousel-dots span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ccc; margin: 0 3px; cursor: pointer; transition: background 0.2s; }
.lc-carousel-dots span.active { background: #0066cc; }
/* tabs (global — also emitted inline by tabs.md include) */
.lc-tabs { border: 1px solid #ddd; border-radius: 6px; margin: 1em 0; overflow: hidden; }
.lc-tabs .lc-tab-bar { display: flex; background: #f5f5f5; border-bottom: 1px solid #ddd; flex-wrap: wrap; }
.lc-tabs .lc-tab-btn { background: none; border: none; padding: 0.6em 1.2em; cursor: pointer; font-size: 0.95em; color: #555; border-right: 1px solid #ddd; }
.lc-tabs .lc-tab-btn:hover { background: #eaeaea; }
.lc-tabs .lc-tab-btn.active { background: white; color: #0066cc; font-weight: 600; box-shadow: inset 0 -3px 0 #0066cc; }
.lc-tabs .lc-tab-panel { display: none; padding: 1em 1.4em; }
.lc-tabs .lc-tab-panel.active { display: block; }
/* accordion */
.lc-accordion { margin: 1em 0; }
.lc-accordion details { border: 1px solid #ddd; border-radius: 6px; margin: 0.4em 0; overflow: hidden; }
.lc-accordion details summary { padding: 0.7em 1em; background: #f5f5f5; cursor: pointer; font-weight: 600; list-style: none; user-select: none; }
.lc-accordion details summary::-webkit-details-marker { display: none; }
.lc-accordion details[open] > summary { border-bottom: 1px solid #ddd; background: #e8f0fe; color: #0066cc; }
.lc-accordion details .lc-ac-body { padding: 0.8em 1.2em; }
/* radio */
.lc-radio-group { margin: 1em 0; }
.lc-radio-options { margin-bottom: 1em; padding: 0.6em 1em; background: #f5f5f5; border-radius: 6px; display: flex; flex-wrap: wrap; gap: 0.2em 0; }
.lc-radio-options label { margin-right: 1.4em; cursor: pointer; font-weight: 500; }
.lc-radio-options input { margin-right: 0.4em; }
.lc-radio-body { padding: 1em 1.4em; background: white; border: 1px solid #eee; border-left: 3px solid #0066cc; border-radius: 0 6px 6px 0; }
.lc-radio-content { display: none; }
.lc-radio-content.active { display: block; }
/* grid */
.lc-grid { display: grid; gap: 18px; margin: 1em 0; }
.lc-grid .lc-grid-cell { min-width: 0; }
.lc-grid .lc-grid-cell > h3 { margin-top: 0; margin-bottom: 0.6em; font-size: 1em; color: #666; text-transform: uppercase; letter-spacing: 0.05em; }
/* dropdown */
.lc-dropdown { position: relative; display: inline-block; margin: 0.3em 0; }
.lc-dd-toggle { background: #0066cc; color: white; border: none; padding: 0.5em 1em; border-radius: 4px; cursor: pointer; font-size: 0.95em; }
.lc-dd-toggle:hover { background: #0052a3; }
.lc-dd-menu { display: none; position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; border-radius: 4px; min-width: 180px; box-shadow: 0 2px 10px rgba(0,0,0,0.12); z-index: 500; margin-top: 4px; }
.lc-dd-menu.open { display: block; }
.lc-dd-menu a { display: block; padding: 0.6em 1em; color: #333; text-decoration: none; }
.lc-dd-menu a:hover { background: #f5f5f5; color: #0066cc; }
/* button */
.lc-btn { display: inline-block; padding: 0.5em 1.2em; background: #0066cc; color: white !important; text-decoration: none !important; border-radius: 4px; font-weight: 600; transition: background 0.15s; margin: 0.2em 0.3em 0.2em 0; }
.lc-btn:hover { background: #0052a3; }
.lc-btn-secondary { background: #6c757d; } .lc-btn-secondary:hover { background: #5a6268; }
.lc-btn-success { background: #28a745; } .lc-btn-success:hover { background: #1e7e34; }
.lc-btn-danger { background: #dc3545; } .lc-btn-danger:hover { background: #bd2130; }
.lc-btn-outline { background: transparent; color: #0066cc !important; border: 2px solid #0066cc; padding: calc(0.5em - 2px) calc(1.2em - 2px); }
.lc-btn-outline:hover { background: #0066cc; color: white !important; }
/* scrollable */
.lc-scrollable { overflow-y: auto; padding: 1em 1.4em; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; margin: 1em 0; }
/* cards */
.lc-cards { display: grid; gap: 18px; margin: 1em 0; }
.lc-cards .lc-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.2em 1.4em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-cards .lc-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); border-color: #0066cc; }
.lc-cards .lc-card h3 { margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em; color: #222; }
.lc-cards .lc-card p { margin: 0 0 0.6em; color: #555; line-height: 1.45; }
.lc-cards .lc-card p:last-child { margin-bottom: 0; }
.lc-cards .lc-card a { color: #0066cc; text-decoration: none; font-weight: 500; }
.lc-cards .lc-card a:hover { text-decoration: underline; }
@media (max-width: 700px) { .lc-cards { grid-template-columns: repeat(2, 1fr) !important; } }
@media (max-width: 480px) { .lc-cards { grid-template-columns: 1fr !important; } }
/* chart */
.lc-chart { margin: 1em 0; position: relative; }
/* map */
.lc-map { margin: 1em 0; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
</style>
<script>
(function(){
  if (window.lcPyrun) return;
  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

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

  function inferColumns(rows) {
    var seen = {}, cols = [];
    for (var r = 0; r < rows.length; r++) {
      var row = rows[r];
      if (typeof row !== "object" || row === null) continue;
      for (var k in row) {
        if (Object.prototype.hasOwnProperty.call(row, k) && !seen[k]) {
          seen[k] = true;
          cols.push({ field: k, headerName: prettifyKey(k) });
        }
      }
    }
    return cols;
  }

  function buildDatagridWrapper(opts) {
    var div = document.createElement("div");
    div.className = "lc-datagrid";
    if (opts.id) div.id = "lc-datagrid-" + opts.id;
    var html = "";
    if (opts.title) {
      html += '<div class="lc-datagrid-title">📊 <span>' + escapeHtml(opts.title) + '</span>';
      if (opts.mode) html += '<span class="lc-datagrid-lang" style="font-style:italic; text-transform:none;">' + escapeHtml(opts.mode) + '</span>';
      if (opts.format) html += '<span class="lc-datagrid-lang">' + escapeHtml(opts.format) + '</span>';
      html += '</div>';
    }
    html += '<div class="lc-datagrid-status">loading grid…</div>';
    html += '<div class="lc-datagrid-grid ag-theme-alpine" style="height:' + (opts.height || 400) + 'px; display:none;"></div>';
    div.innerHTML = html;
    return div;
  }

  function parseDatagridText(raw, format) {
    if (format === "json") return Promise.resolve(JSON.parse(raw));
    if (format === "csv") return Promise.resolve(parseCsv(raw));
    return loadJsYaml().then(function(){
      if (!window.jsyaml) throw new Error("js-yaml failed to load");
      return window.jsyaml.load(raw);
    });
  }

  function renderGridInto(wrapper, dataPromise, gridId, opts) {
    opts = opts || {};
    var gridEl = wrapper.querySelector(".lc-datagrid-grid");
    var statusEl = wrapper.querySelector(".lc-datagrid-status");
    function showError(msg) {
      if (statusEl && statusEl.parentNode) {
        statusEl.outerHTML = '<div class="lc-datagrid-err">' + escapeHtml(msg) + '</div>';
      }
      gridEl.style.display = "none";
    }
    Promise.all([dataPromise, loadAgGrid()]).then(function(results){
      var data = results[0];
      if (!Array.isArray(data)) {
        showError("Expected an array of objects; got: " + (data === null ? "null" : typeof data));
        return;
      }
      if (data.length === 0) {
        showError("Empty dataset — nothing to show.");
        return;
      }
      var cols = inferColumns(data);
      if (cols.length === 0) {
        showError("No columns inferred — rows must be objects with keys.");
        return;
      }
      if (statusEl && statusEl.parentNode) statusEl.remove();
      gridEl.style.display = "";
      var gridOptions = {
        columnDefs: cols,
        rowData: data,
        defaultColDef: {
          sortable: true, filter: true, resizable: true, flex: 1, minWidth: 80,
          editable: !!opts.editable,
          valueFormatter: function(params){
            if (typeof params.value === "boolean") return params.value ? "True" : "False";
            return params.value;
          }
        },
        animateRows: true,
        rowSelection: "single",
        onSelectionChanged: function(event) {
          var rows = event.api.getSelectedRows();
          window.lcMasterDetail.publish(gridId, rows[0] || null);
        }
      };
      if (opts.editable) {
        gridOptions.onCellValueChanged = function(event) {
          // only republish to bound forms if the edited row is the selected row
          var selected = event.api.getSelectedRows();
          if (selected.length && selected[0] === event.data) {
            window.lcMasterDetail.publish(gridId, event.data);
          }
        };
      }
      var api = window.agGrid.createGrid(gridEl, gridOptions);
      window.lcMasterDetail.registerGrid(gridId, api);

      // grid-to-grid master/detail: detail-of="<master-id>" filter="<local>=<master>"
      if (opts.detailOf && opts.filterExpr) {
        var m = opts.filterExpr.match(/^\s*([\w-]+)\s*=\s*([\w-]+)\s*$/);
        if (m) {
          var localKey = m[1];
          var masterKey = m[2];
          var fullData = data.slice();
          window.lcMasterDetail.subscribe(opts.detailOf, function(masterRow){
            if (!masterRow) {
              api.setGridOption("rowData", fullData);
            } else {
              var filtered = fullData.filter(function(r){
                return r[localKey] === masterRow[masterKey];
              });
              api.setGridOption("rowData", filtered);
            }
          });
        }
      }
    }).catch(function(e){
      showError("Datagrid error: " + (e.message || String(e)));
    });
  }

  function readDatagridOpts(el, prefix) {
    return {
      editable: el.getAttribute(prefix + "editable") === "true",
      detailOf: el.getAttribute(prefix + "detail-of") || "",
      filterExpr: el.getAttribute(prefix + "filter") || ""
    };
  }

  var DG_ID = 0;
  function upgradeDatagrid(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent : "";
    var height = parseInt(el.getAttribute("height"), 10) || 400;
    var format = (el.getAttribute("format") || "yaml").toLowerCase();
    var title = el.getAttribute("title") || "";
    var id = el.id || ("dg" + (++DG_ID));
    var opts = readDatagridOpts(el, "");
    var wrapper = buildDatagridWrapper({ id: id, title: title, format: format, height: height });
    el.parentNode.replaceChild(wrapper, el);
    var dataPromise;
    try { dataPromise = parseDatagridText(raw, format); }
    catch (e) { dataPromise = Promise.reject(new Error(format.toUpperCase() + " parse error: " + e.message)); }
    renderGridInto(wrapper, dataPromise, id, opts);
  }

  function upgradeDatagridFile(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = el.getAttribute("data-raw") || "";
    var cdn = el.getAttribute("data-cdn") || raw;
    var canonical = el.getAttribute("data-canonical") || "";
    var format = (el.getAttribute("data-format") || "yaml").toLowerCase();
    var height = parseInt(el.getAttribute("data-height"), 10) || 400;
    var title = el.getAttribute("data-title") || "";
    var useCdn = (canonical && location.hostname === canonical) || location.search.indexOf("cdn=1") >= 0;
    var url = useCdn ? cdn : raw;
    var id = el.id || ("dg" + (++DG_ID));
    var opts = readDatagridOpts(el, "data-");
    var wrapper = buildDatagridWrapper({ id: id, title: title, format: format, height: height, mode: useCdn ? "cdn" : "live" });
    el.parentNode.replaceChild(wrapper, el);
    var dataPromise = fetch(url)
      .then(function(r){ if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + url); return r.text(); })
      .then(function(text){ return parseDatagridText(text, format); });
    renderGridInto(wrapper, dataPromise, id, opts);
  }

  // Called from Python runners: show.grid(rows)
  window.lcRenderDatagridFromJson = function(viewEl, rowsJson, title, height) {
    var rows;
    try { rows = JSON.parse(rowsJson); }
    catch (e) {
      var err = document.createElement("div");
      err.className = "lc-datagrid-err";
      err.textContent = "show.grid: invalid JSON — " + e.message;
      err.style.gridColumn = "1 / -1";
      viewEl.appendChild(err);
      return;
    }
    var rtId = "rt" + (++DG_ID);
    var wrapper = buildDatagridWrapper({
      id: rtId,
      title: title || null,
      format: "",
      height: height || 300
    });
    wrapper.style.gridColumn = "1 / -1";
    viewEl.appendChild(wrapper);
    renderGridInto(wrapper, Promise.resolve(rows), rtId);
  };

  function buildFormWrapper(opts) {
    var div = document.createElement("div");
    div.className = "lc-form";
    if (opts.id) div.id = "lc-form-" + opts.id;
    var meta = "";
    if (opts.mode) meta = '<span class="lc-form-meta" style="font-style:italic; text-transform:none;">' + escapeHtml(opts.mode) + '</span>';
    else if (opts.format) meta = '<span class="lc-form-meta">' + escapeHtml(opts.format) + '</span>';
    var html = '<div class="lc-form-title">📝 <span class="lc-form-name">' + escapeHtml(opts.title || "Form") + '</span>' + meta + '</div>';
    html += '<div class="lc-form-body"></div>';
    div.innerHTML = html;
    return div;
  }

  function setFormTitle(wrapper, title) {
    var nameEl = wrapper.querySelector(".lc-form-name");
    if (nameEl) nameEl.textContent = title;
  }

  function inferFormTitle(obj) {
    if (!obj || typeof obj !== "object" || Array.isArray(obj)) return "";
    return obj.name || obj.title || obj.label || obj.id || "";
  }

  function typeOfValue(v) {
    if (v === null || v === undefined) return "null";
    if (typeof v === "boolean") return "boolean";
    if (typeof v === "number") return "number";
    if (typeof v === "string") return "string";
    if (Array.isArray(v)) return "array";
    return "object";
  }

  function stringifyObject(o) {
    var label = (o && typeof o === "object" && !Array.isArray(o))
      ? (o.name || o.title || o.label || o.id || "")
      : "";
    if (label) return String(label);
    try {
      var s = JSON.stringify(o);
      if (s && s.length > 60) s = s.substring(0, 57) + "…";
      return s || String(o);
    } catch (e) { return String(o); }
  }

  function makeFormCellRenderer(opts) {
    return function(params) {
      var t = params.data._type;
      var v = params.value;

      if (t === "boolean") {
        var w = document.createElement("div");
        w.className = "lc-form-bool";
        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = !!v;
        cb.disabled = !opts.editable;
        cb.className = "lc-form-bool-cb";
        var lab = document.createElement("span");
        lab.textContent = v ? "True" : "False";
        lab.className = v ? "lc-form-bool-t" : "lc-form-bool-f";
        if (opts.editable) {
          cb.addEventListener("click", function(e){ e.stopPropagation(); });
          cb.addEventListener("change", function(){
            params.node.setDataValue("value", cb.checked);
          });
        }
        w.appendChild(cb);
        w.appendChild(lab);
        return w;
      }

      if (t === "null" || v === null || v === undefined) {
        var ns = document.createElement("span");
        ns.textContent = "—";
        ns.className = "lc-form-null";
        return ns;
      }

      if (t === "array") {
        var aBox = document.createElement("div");
        aBox.className = "lc-form-cellbox";
        var pc = document.createElement("div");
        pc.className = "lc-form-pills";
        if (!v.length) {
          var empty = document.createElement("span");
          empty.className = "lc-form-null";
          empty.textContent = "(empty)";
          pc.appendChild(empty);
        } else {
          v.forEach(function(item){
            var pill = document.createElement("span");
            pill.className = "lc-form-pill";
            var label;
            if (item === null || item === undefined) label = "—";
            else if (typeof item === "object") label = stringifyObject(item);
            else label = String(item);
            pill.textContent = label;
            pc.appendChild(pill);
          });
        }
        aBox.appendChild(pc);
        return aBox;
      }

      if (t === "object") {
        var oBox = document.createElement("div");
        oBox.className = "lc-form-cellbox";
        var sb = document.createElement("span");
        sb.className = "lc-form-selectbox";
        var txt = document.createElement("span");
        txt.className = "lc-form-selectbox-label";
        txt.textContent = stringifyObject(v);
        var arrow = document.createElement("span");
        arrow.className = "lc-form-selectbox-arrow";
        arrow.textContent = "▾";
        sb.appendChild(txt);
        sb.appendChild(arrow);
        sb.title = (function(){ try { return JSON.stringify(v, null, 2); } catch (e) { return String(v); }})();
        oBox.appendChild(sb);
        return oBox;
      }

      if (t === "number") {
        var nSpan = document.createElement("span");
        nSpan.textContent = String(v);
        nSpan.className = "lc-form-num";
        return nSpan;
      }

      return String(v);
    };
  }

  function renderFormBody(bodyEl, obj, opts) {
    opts = opts || {};
    // Tear down any previous AG Grid instance attached here
    if (bodyEl._lcGridApi) {
      try { bodyEl._lcGridApi.destroy(); } catch (e) {}
      bodyEl._lcGridApi = null;
    }
    bodyEl.innerHTML = "";
    if (obj === null || obj === undefined) {
      bodyEl.innerHTML = '<div class="lc-form-empty">(no data)</div>';
      return;
    }
    if (typeof obj !== "object" || Array.isArray(obj)) {
      bodyEl.innerHTML = '<div class="lc-form-err">Expected a single object; got ' + escapeHtml(Array.isArray(obj) ? "array" : typeof obj) + '</div>';
      return;
    }
    var keys = Object.keys(obj);
    if (keys.length === 0) {
      bodyEl.innerHTML = '<div class="lc-form-empty">(empty object)</div>';
      return;
    }

    var rows = keys.map(function(k){
      return { _key: k, label: prettifyKey(k), value: obj[k], _type: typeOfValue(obj[k]) };
    });

    var gridDiv = document.createElement("div");
    gridDiv.className = "lc-form-grid ag-theme-alpine";
    bodyEl.appendChild(gridDiv);

    var cellRenderer = makeFormCellRenderer(opts);

    loadAgGrid().then(function(){
      var columnDefs = [
        {
          field: "label",
          headerName: "",
          pinned: "left",
          editable: false,
          cellClass: "lc-form-label-cell",
          width: 160,
          suppressMovable: true,
          sortable: false,
          filter: false
        },
        {
          field: "value",
          headerName: "",
          flex: 1,
          sortable: false,
          filter: false,
          suppressMovable: true,
          // Only primitives (string/number/null) go through the text editor.
          // Booleans are handled by the renderer's interactive checkbox.
          // Arrays and objects are read-only in v1.
          editable: function(params){
            if (!opts.editable) return false;
            var t = params.data._type;
            return t === "string" || t === "number" || t === "null";
          },
          cellEditor: "agTextCellEditor",
          // Coerce string -> number for number cells (agTextCellEditor always returns string)
          valueParser: function(params) {
            var t = params.data._type;
            if (t === "number") {
              if (params.newValue === "" || params.newValue === null) return null;
              var n = Number(params.newValue);
              if (isNaN(n)) return params.oldValue;
              return n;
            }
            return params.newValue;
          },
          cellRenderer: cellRenderer
        }
      ];

      var gridOptions = {
        columnDefs: columnDefs,
        rowData: rows,
        domLayout: "autoHeight",
        headerHeight: 0,
        singleClickEdit: !!opts.editable,
        stopEditingWhenCellsLoseFocus: true,
        suppressMovableColumns: true,
        suppressCellFocus: !opts.editable,
        animateRows: false,
        defaultColDef: { sortable: false, filter: false, suppressHeaderMenuButton: true, resizable: true },
        getRowHeight: function(params) {
          var t = params.data._type;
          if (t === "array") {
            var n = (params.data.value || []).length;
            if (n <= 4) return null; // default
            if (n <= 10) return 56;
            return 80;
          }
          return null;
        },
        onCellValueChanged: function(event) {
          var k = event.data._key;
          var nv = event.newValue;
          obj[k] = nv;
          // Re-derive type from the new value
          event.data._type = typeOfValue(nv);
          if (opts.onChange) opts.onChange(obj, k, nv);
        }
      };

      bodyEl._lcGridApi = window.agGrid.createGrid(gridDiv, gridOptions);
    }).catch(function(e){
      bodyEl.innerHTML = '<div class="lc-form-err">' + escapeHtml("Could not load AG Grid: " + (e.message || String(e))) + '</div>';
    });
  }

  var FORM_ID = 0;
  function upgradeForm(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent : "";
    var format = (el.getAttribute("format") || "yaml").toLowerCase();
    var title = el.getAttribute("title") || "";
    var bound = el.getAttribute("bound") || "";
    var editable = el.getAttribute("editable") === "true";
    var id = el.id || ("frm" + (++FORM_ID));

    var wrapper = buildFormWrapper({ id: id, title: title || "Form", format: bound ? "" : format });
    el.parentNode.replaceChild(wrapper, el);
    var body = wrapper.querySelector(".lc-form-body");

    if (bound) {
      body.innerHTML = '<div class="lc-form-empty">click a row in <code>#' + escapeHtml(bound) + '</code> to see details</div>';
      window.lcMasterDetail.subscribe(bound, function(row){
        if (!row) {
          renderFormBody(body, null);
          setFormTitle(wrapper, title || "Form");
          return;
        }
        renderFormBody(body, row, {
          editable: editable,
          onChange: function(){ window.lcMasterDetail.refreshGrid(bound); }
        });
        setFormTitle(wrapper, title || inferFormTitle(row) || "Form");
      });
      return;
    }

    if (!raw || !raw.trim()) {
      body.innerHTML = '<div class="lc-form-empty">(no data)</div>';
      return;
    }
    var dataPromise;
    try { dataPromise = parseDatagridText(raw, format); }
    catch (e) { dataPromise = Promise.reject(new Error(format.toUpperCase() + " parse error: " + e.message)); }
    dataPromise.then(function(obj){
      renderFormBody(body, obj, { editable: editable });
      if (!title) setFormTitle(wrapper, inferFormTitle(obj) || "Form");
    }).catch(function(e){
      body.innerHTML = '<div class="lc-form-err">' + escapeHtml(e.message || String(e)) + '</div>';
    });
  }

  function upgradeFormFile(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = el.getAttribute("data-raw") || "";
    var cdn = el.getAttribute("data-cdn") || raw;
    var canonical = el.getAttribute("data-canonical") || "";
    var format = (el.getAttribute("data-format") || "yaml").toLowerCase();
    var title = el.getAttribute("data-title") || "";
    var editable = el.getAttribute("data-editable") === "true";
    var useCdn = (canonical && location.hostname === canonical) || location.search.indexOf("cdn=1") >= 0;
    var url = useCdn ? cdn : raw;
    var id = el.id || ("frm" + (++FORM_ID));
    var wrapper = buildFormWrapper({ id: id, title: title || "Form", mode: useCdn ? "cdn" : "live" });
    el.parentNode.replaceChild(wrapper, el);
    var body = wrapper.querySelector(".lc-form-body");
    body.innerHTML = '<div class="lc-form-empty">loading…</div>';
    fetch(url)
      .then(function(r){ if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + url); return r.text(); })
      .then(function(text){ return parseDatagridText(text, format); })
      .then(function(obj){
        renderFormBody(body, obj, { editable: editable });
        if (!title) setFormTitle(wrapper, inferFormTitle(obj) || "Form");
      })
      .catch(function(e){
        body.innerHTML = '<div class="lc-form-err">' + escapeHtml("Form error: " + (e.message || String(e))) + '</div>';
      });
  }

  // Called from Python runners: show.form(obj)
  window.lcRenderFormFromJson = function(viewEl, objJson, title) {
    var obj;
    try { obj = JSON.parse(objJson); }
    catch (e) {
      var err = document.createElement("div");
      err.className = "lc-form-err";
      err.textContent = "show.form: invalid JSON — " + e.message;
      err.style.gridColumn = "1 / -1";
      viewEl.appendChild(err);
      return;
    }
    var wrapper = buildFormWrapper({
      id: "rt" + (++FORM_ID),
      title: title || inferFormTitle(obj) || "Form"
    });
    wrapper.style.gridColumn = "1 / -1";
    viewEl.appendChild(wrapper);
    renderFormBody(wrapper.querySelector(".lc-form-body"), obj);
  };

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
    document.querySelectorAll(".highlighter-rouge.datagrid, pre.datagrid").forEach(upgradeDatagrid);
    document.querySelectorAll("div.lc-datagrid-src").forEach(upgradeDatagridFile);
    document.querySelectorAll(".highlighter-rouge.form, pre.form").forEach(upgradeForm);
    document.querySelectorAll("div.lc-form-src").forEach(upgradeFormFile);
    document.querySelectorAll("ul.carousel").forEach(upgradeCarousel);
    document.querySelectorAll(".highlighter-rouge.accordion").forEach(upgradeAccordion);
    document.querySelectorAll(".highlighter-rouge.tabs").forEach(upgradeTabsInline);
    document.querySelectorAll("p.tabs").forEach(upgradeTabsFile);
    document.querySelectorAll(".highlighter-rouge.radio").forEach(upgradeRadio);
    document.querySelectorAll(".highlighter-rouge.grid").forEach(upgradeGrid);
    document.querySelectorAll(".highlighter-rouge.scrollable").forEach(upgradeScrollable);
    document.querySelectorAll(".highlighter-rouge.cards").forEach(upgradeCards);
    document.querySelectorAll("ul.dropdown").forEach(upgradeDropdown);
    document.querySelectorAll("p.button").forEach(upgradeButton);
    document.querySelectorAll("p.embed-page").forEach(upgradeEmbedPage);
    document.querySelectorAll("p.embed").forEach(upgradeEmbedExternal);
    document.querySelectorAll("p.video").forEach(upgradeVideo);
    document.querySelectorAll(".highlighter-rouge.chart, pre.chart, p.chart").forEach(upgradeChart);
    document.querySelectorAll(".highlighter-rouge.map").forEach(upgradeMap);
    document.querySelectorAll("p.folder").forEach(upgradeFolder);
  }

  // --- shared helpers for section-based widgets ---
  var _markedQ = null;
  function loadMarked(cb) {
    if (window.marked) { cb(); return; }
    if (_markedQ) { _markedQ.push(cb); return; }
    _markedQ = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/marked@9/marked.min.js";
    s.onload = function() { var q = _markedQ; _markedQ = null; q.forEach(function(f){ f(); }); };
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
    return window.marked ? marked.parse(s) : "<pre>" + s + "</pre>";
  }
  window.lcLoadMarked = loadMarked;

  var _chartJsQ = null;
  function loadChartJs(cb) {
    if (window.Chart) { cb(); return; }
    if (_chartJsQ) { _chartJsQ.push(cb); return; }
    _chartJsQ = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js";
    s.onload = function() { var q = _chartJsQ; _chartJsQ = null; q.forEach(function(f){ f(); }); };
    document.head.appendChild(s);
  }

  var _leafletQ = null;
  function loadLeaflet(cb) {
    if (window.L) { cb(); return; }
    if (_leafletQ) { _leafletQ.push(cb); return; }
    _leafletQ = [cb];
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.min.css";
    document.head.appendChild(link);
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet-src.min.js";
    s.onload = function() { var q = _leafletQ; _leafletQ = null; q.forEach(function(f){ f(); }); };
    document.head.appendChild(s);
  }

  function upgradeChart(el) {
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
    var type = el.getAttribute("type") || "bar";
    var h = parseInt(el.getAttribute("height") || "300", 10);
    var bound = el.getAttribute("bound-to");
    var gid = "lc-chart-" + Math.random().toString(36).slice(2, 7);
    var wrap = document.createElement("div");
    wrap.className = "lc-chart";
    el.parentNode.replaceChild(wrap, el);

    function chartColors(data) {
      var mn = Math.min.apply(null, data), mx = Math.max.apply(null, data), rng = mx - mn || 1;
      return data.map(function(v) {
        var t = (v - mn) / rng;
        return "rgb(" + Math.round(173 - 173*t) + "," + Math.round(216 - 160*t) + "," + Math.round(230 - 91*t) + ")";
      });
    }

    if (bound) {
      var xAttr = el.getAttribute("x") || (lines.length > 0 ? lines[0].split(",")[0].trim() : "");
      var placeholder = document.createElement("div");
      placeholder.style.cssText = "min-height:" + h + "px;display:flex;align-items:center;justify-content:center;color:#aaa;border:2px dashed #e0e0e0;border-radius:8px;font-style:italic;padding:1em;text-align:center";
      placeholder.textContent = "Select a row to visualize";
      wrap.appendChild(placeholder);
      loadChartJs(function() {
        var instance = null;
        window.lcMasterDetail.subscribe(bound, function(row) {
          if (!row) return;
          var title = String(row[xAttr] || "");
          var newLabels = [], newData = [];
          Object.keys(row).forEach(function(k) {
            if (k === xAttr) return;
            var v = parseFloat(row[k]);
            if (!isNaN(v)) { newLabels.push(k); newData.push(v); }
          });
          if (!newLabels.length) return;
          var colors = chartColors(newData);
          if (!instance) {
            placeholder.style.display = "none";
            var canvas = document.createElement("canvas");
            canvas.id = gid;
            wrap.appendChild(canvas);
            instance = new Chart(canvas, {
              type: type,
              data: { labels: newLabels, datasets: [{ label: title, data: newData, backgroundColor: colors, borderColor: colors, borderWidth: 1 }] },
              options: {
                responsive: true,
                plugins: { legend: { display: false }, title: { display: !!title, text: title } },
                scales: type === "pie" || type === "doughnut" ? {} : { y: { beginAtZero: true } }
              }
            });
          } else {
            instance.data.labels = newLabels;
            instance.data.datasets[0].data = newData;
            instance.data.datasets[0].label = title;
            instance.data.datasets[0].backgroundColor = colors;
            instance.data.datasets[0].borderColor = colors;
            if (instance.options.plugins.title) { instance.options.plugins.title.text = title; instance.options.plugins.title.display = !!title; }
            instance.update();
          }
        });
      });
      return;
    }

    // Static CSV mode
    if (lines.length < 2) return;
    var headers = lines[0].split(",").map(function(v){ return v.trim(); });
    var xAttrS = el.getAttribute("x") || headers[0];
    var yAttr = el.getAttribute("y") || headers[1];
    var xIdx = headers.indexOf(xAttrS); if (xIdx < 0) xIdx = 0;
    var yIdx = headers.indexOf(yAttr); if (yIdx < 0) yIdx = 1;
    var rows = lines.slice(1).map(function(l){ return l.split(",").map(function(v){ return v.trim(); }); });
    var labels = rows.map(function(r){ return r[xIdx] || ""; });
    var data = rows.map(function(r){ return parseFloat(r[yIdx]) || 0; });
    var colors = chartColors(data);
    wrap.innerHTML = "<canvas id=\"" + gid + "\"></canvas>";
    loadChartJs(function() {
      new Chart(document.getElementById(gid), {
        type: type,
        data: { labels: labels, datasets: [{ label: yAttr, data: data, backgroundColor: colors, borderColor: colors, borderWidth: 1 }] },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: type === "pie" || type === "doughnut" ? {} : {
            x: { title: { display: true, text: xAttrS } },
            y: { beginAtZero: true, title: { display: true, text: yAttr } }
          }
        }
      });
    });
  }

  function upgradeMap(el) {
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var lat = parseFloat(el.getAttribute("lat") || "48.86");
    var lng = parseFloat(el.getAttribute("lng") || "2.35");
    var zoom = parseInt(el.getAttribute("zoom") || "12", 10);
    var h = el.getAttribute("height") || "350";
    var gid = "lc-map-" + Math.random().toString(36).slice(2, 7);
    var wrap = document.createElement("div");
    wrap.className = "lc-map";
    wrap.id = gid;
    wrap.style.height = h + "px";
    el.parentNode.replaceChild(wrap, el);
    var markers = [];
    var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
    if (lines.length >= 2) {
      var hdrs = lines[0].split(",").map(function(v){ return v.trim(); });
      var nI = hdrs.indexOf("name") >= 0 ? hdrs.indexOf("name") : 0;
      var laI = hdrs.indexOf("lat") >= 0 ? hdrs.indexOf("lat") : 1;
      var lnI = hdrs.indexOf("lng") >= 0 ? hdrs.indexOf("lng") : 2;
      lines.slice(1).forEach(function(l) {
        var c = l.split(",").map(function(v){ return v.trim(); });
        var mLat = parseFloat(c[laI]), mLng = parseFloat(c[lnI]);
        if (!isNaN(mLat) && !isNaN(mLng)) markers.push({ name: c[nI] || "", lat: mLat, lng: mLng });
      });
    }
    loadLeaflet(function() {
      var map = L.map(gid).setView([lat, lng], zoom);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
        maxZoom: 19
      }).addTo(map);
      markers.forEach(function(m) { L.marker([m.lat, m.lng]).addTo(map).bindPopup("<b>" + m.name + "</b>"); });
    });
  }

  function upgradeAccordion(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    loadMarked(function() {
      var wrap = document.createElement("div");
      wrap.className = "lc-accordion";
      sections.forEach(function(s) {
        var d = document.createElement("details");
        d.innerHTML = "<summary>" + s.label + "</summary><div class=\"lc-ac-body\">" + markdownBody(s.body) + "</div>";
        wrap.appendChild(d);
      });
      el.parentNode.replaceChild(wrap, el);
    });
  }

  function upgradeTabsInline(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var gid = el.id || ("lc-ti-" + Math.random().toString(36).slice(2, 7));
    loadMarked(function() {
      var bar = sections.map(function(s, i){
        return "<button class=\"lc-tab-btn" + (i===0?" active":"") + "\" data-tab=\"" + gid + "-" + i + "\">" + s.label + "</button>";
      }).join("");
      var panels = sections.map(function(s, i){
        return "<div id=\"" + gid + "-" + i + "\" class=\"lc-tab-panel" + (i===0?" active":"") + "\">" + markdownBody(s.body) + "</div>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "lc-tabs";
      wrap.innerHTML = "<div class=\"lc-tab-bar\">" + bar + "</div>" + panels;
      wrap.querySelectorAll(".lc-tab-btn").forEach(function(b){
        b.addEventListener("click", function(){
          wrap.querySelectorAll(".lc-tab-btn").forEach(function(x){x.classList.remove("active");});
          wrap.querySelectorAll(".lc-tab-panel").forEach(function(x){x.classList.remove("active");});
          b.classList.add("active");
          document.getElementById(b.dataset.tab).classList.add("active");
        });
      });
      el.parentNode.replaceChild(wrap, el);
    });
  }

  function upgradeTabsFile(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var a = el.querySelector("a");
    if (!a) return;
    var filePath = a.getAttribute("href").replace(/^\/+|\/+$/g, "");
    var gid = el.getAttribute("id") || ("lc-tf-" + Math.random().toString(36).slice(2, 7));
    var placeholder = document.createElement("div");
    placeholder.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading tabs…</div>";
    el.parentNode.replaceChild(placeholder, el);
    if (!_lcSiteRepo) {
      placeholder.innerHTML = "<div class='lc-tabs' style='padding:1em;color:#c00'>⚠️ site.github.repository_nwo not set.</div>";
      return;
    }
    var rawUrl = "https://raw.githubusercontent.com/" + _lcSiteRepo + "/main/docs/" + filePath + ".md";
    fetch(rawUrl)
      .then(function(r) { if (!r.ok) throw new Error("File not found: " + filePath + ".md"); return r.text(); })
      .then(function(text) {
        var lines = text.split("\n");
        var i = 0;
        if (lines[0] && lines[0].trim() === "---") {
          i = 1;
          while (i < lines.length && lines[i].trim() !== "---") i++;
          i++;
        }
        var body = lines.slice(i).join("\n");
        var sections = body.split(/\n(?=### )/).map(function(s) {
          var sl = s.split("\n");
          return { label: sl[0].replace(/^###\s*/, "").trim(), body: sl.slice(1).join("\n").trim() };
        }).filter(function(s) { return s.label; });
        if (!sections.length) {
          placeholder.innerHTML = "<div class='lc-tabs' style='padding:1em;color:#c00'>⚠️ No ### sections found in " + escapeHtml(filePath) + ".md</div>";
          return;
        }
        loadMarked(function() {
          var bar = sections.map(function(s, i) {
            return "<button class=\"lc-tab-btn" + (i===0?" active":"") + "\" data-tab=\"" + gid + "-" + i + "\">" + escapeHtml(s.label) + "</button>";
          }).join("");
          var panels = sections.map(function(s, i) {
            return "<div id=\"" + gid + "-" + i + "\" class=\"lc-tab-panel" + (i===0?" active":"") + "\">" + marked.parse(s.body) + "</div>";
          }).join("");
          var wrap = document.createElement("div");
          wrap.className = "lc-tabs";
          wrap.innerHTML = "<div class=\"lc-tab-bar\">" + bar + "</div>" + panels;
          wrap.querySelectorAll(".lc-tab-btn").forEach(function(b) {
            b.addEventListener("click", function() {
              wrap.querySelectorAll(".lc-tab-btn").forEach(function(x) { x.classList.remove("active"); });
              wrap.querySelectorAll(".lc-tab-panel").forEach(function(x) { x.classList.remove("active"); });
              b.classList.add("active");
              document.getElementById(b.dataset.tab).classList.add("active");
            });
          });
          placeholder.parentNode.replaceChild(wrap, placeholder);
        });
      })
      .catch(function(e) {
        placeholder.innerHTML = "<div class='lc-tabs' style='padding:1em;color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
      });
  }

  function upgradeRadio(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var gid = el.id || ("lc-rg-" + Math.random().toString(36).slice(2, 7));
    loadMarked(function() {
      var radios = sections.map(function(s, i){
        return "<label><input type=\"radio\" name=\"" + gid + "\" data-target=\"" + gid + "-" + i + "\"" + (i===0?" checked":"") + "> " + s.label + "</label>";
      }).join("");
      var panels = sections.map(function(s, i){
        return "<div id=\"" + gid + "-" + i + "\" class=\"lc-radio-content" + (i===0?" active":"") + "\">" + markdownBody(s.body) + "</div>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "lc-radio-group";
      wrap.innerHTML = "<div class=\"lc-radio-options\">" + radios + "</div><div class=\"lc-radio-body\">" + panels + "</div>";
      wrap.querySelectorAll("input[type=radio]").forEach(function(r){
        r.addEventListener("change", function(){
          wrap.querySelectorAll(".lc-radio-content").forEach(function(x){x.classList.remove("active");});
          document.getElementById(r.dataset.target).classList.add("active");
        });
      });
      el.parentNode.replaceChild(wrap, el);
    });
  }

  function upgradeGrid(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var cols = el.getAttribute("cols") || "auto";
    var gap = el.getAttribute("gap") || "18";
    var hideHeadings = el.getAttribute("headings") === "hide";
    var tpl = cols === "auto" ? "repeat(auto-fit,minmax(280px,1fr))" : "repeat(" + cols + ",1fr)";
    loadMarked(function() {
      var cells = sections.map(function(s){
        var h = hideHeadings ? "" : "<h3>" + s.label + "</h3>";
        return "<div class=\"lc-grid-cell\">" + h + markdownBody(s.body) + "</div>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "lc-grid";
      wrap.style.gridTemplateColumns = tpl;
      wrap.style.gap = gap + "px";
      wrap.innerHTML = cells;
      el.parentNode.replaceChild(wrap, el);
    });
  }

  function upgradeScrollable(el) {
    var h = el.getAttribute("height") || "300";
    var code = el.querySelector("code");
    var content = code ? code.innerHTML : el.innerHTML;
    var wrap = document.createElement("div");
    wrap.className = "lc-scrollable";
    wrap.style.maxHeight = h + "px";
    wrap.innerHTML = "<pre style=\"margin:0;white-space:pre-wrap;\">" + content + "</pre>";
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeDropdown(el) {
    var label = el.getAttribute("label") || "Menu";
    var gid = el.id || ("lc-dd-" + Math.random().toString(36).slice(2, 7));
    var links = Array.from(el.querySelectorAll("li a")).map(function(a){
      return "<a href=\"" + a.href + "\">" + a.textContent + "</a>";
    }).join("");
    var wrap = document.createElement("div");
    wrap.className = "lc-dropdown";
    wrap.id = "lc-dd-" + gid;
    wrap.innerHTML = "<button class=\"lc-dd-toggle\">" + label + "</button><div class=\"lc-dd-menu\">" + links + "</div>";
    var btn = wrap.querySelector(".lc-dd-toggle");
    var menu = wrap.querySelector(".lc-dd-menu");
    btn.addEventListener("click", function(e){ e.stopPropagation(); menu.classList.toggle("open"); });
    document.addEventListener("click", function(){ menu.classList.remove("open"); }, { passive: true });
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeButton(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var style = el.getAttribute("style-variant") || "";
    a.classList.add("lc-btn");
    if (style) a.classList.add("lc-btn-" + style);
    el.classList.remove("button");
  }

  function _iframeEl(src, h) {
    var f = document.createElement("iframe");
    f.src = src; f.width = "100%"; f.height = h || "400";
    f.setAttribute("loading", "lazy"); f.setAttribute("allowfullscreen", "");
    f.style.border = "none";
    return f;
  }
  function upgradeEmbedPage(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var h = el.getAttribute("height") || "400";
    var src = a.getAttribute("href");
    if (src && src.indexOf("?") === -1) src += "?embed=true"; else src += "&embed=true";
    el.parentNode.replaceChild(_iframeEl(src, h), el);
  }
  function upgradeEmbedExternal(el) {
    var a = el.querySelector("a");
    if (!a) return;
    el.parentNode.replaceChild(_iframeEl(a.getAttribute("href"), el.getAttribute("height") || "600"), el);
  }
  function upgradeVideo(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var href = a.getAttribute("href");
    var src = href;
    var gdrive = href.match(/^gdrive:(.+)/);
    if (gdrive) src = "https://drive.google.com/file/d/" + gdrive[1] + "/preview";
    var yt = href.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&?]+)/);
    if (yt) src = "https://www.youtube.com/embed/" + yt[1];
    el.parentNode.replaceChild(_iframeEl(src, el.getAttribute("height") || "400"), el);
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
    fetch("https://api.github.com/repos/" + _lcSiteRepo + "/contents/" + path)
      .then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function(files) {
        if (!Array.isArray(files)) throw new Error("Not a directory: " + escapeHtml(path));
        var pages = files.filter(function(f) {
          if (f.type !== "file" || !/\.md$/i.test(f.name) || f.name === "index.md") return false;
          if (!showPrivate && f.name.startsWith("_")) return false;
          return true;
        }).sort(function(a, b) { return a.name.localeCompare(b.name); });
        if (!pages.length) {
          wrap.innerHTML = "<div style='padding:1em;color:#888'>No pages found in " + escapeHtml(path) + "</div>";
          return;
        }
        return Promise.all(pages.map(function(f) {
          return fetch(f.download_url)
            .then(function(r) { return r.text(); })
            .then(function(text) {
              var meta = extractPageMeta(text);
              var title = meta.title || f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              return { title: title, snippet: meta.snippet, url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, "") };
            })
            .catch(function() {
              var title = f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              return { title: title, snippet: "", url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, "") };
            });
        }));
      })
      .then(function(items) {
        if (!items) return;
        wrap.innerHTML = items.map(function(item) {
          var card = '<div class="lc-card"><h3><a href="' + item.url + '">' + escapeHtml(item.title) + '</a></h3>';
          if (item.snippet) card += '<p style="font-size:0.85em;color:#555;margin:0.3em 0 0">' + escapeHtml(item.snippet) + '</p>';
          return card + '</div>';
        }).join("");
      })
      .catch(function(e) {
        wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
      });
  }

  function upgradeCards(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var cols = el.getAttribute("cols") || "auto";
    var gap = el.getAttribute("gap") || "18";
    var colStyle = cols === "auto"
      ? "repeat(auto-fit, minmax(240px, 1fr))"
      : "repeat(" + cols + ", 1fr)";
    var wrap = document.createElement("div");
    wrap.className = "lc-cards";
    wrap.style.gridTemplateColumns = colStyle;
    wrap.style.gap = gap + "px";
    function renderCards() {
      wrap.innerHTML = sections.map(function(s) {
        return "<div class=\"lc-card\"><h3>" + s.label + "</h3>" + markdownBody(s.body) + "</div>";
      }).join("");
    }
    loadMarked(renderCards);
    renderCards();
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeCarousel(el) {
    var items = Array.from(el.querySelectorAll("li")).map(function(li){ return li.innerHTML; });
    if (!items.length) return;
    var delay = parseInt(el.getAttribute("delay") || "4000", 10);
    var gid = el.id || ("lc-car-" + Math.random().toString(36).slice(2, 7));
    var itemsHtml = items.map(function(h, i){
      return '<div class="lc-carousel-item' + (i === 0 ? " active" : "") + '">' + h + '</div>';
    }).join("");
    var dotsHtml = items.map(function(_, i){
      return '<span class="' + (i === 0 ? "active" : "") + '" data-idx="' + i + '"></span>';
    }).join("");
    var wrapper = document.createElement("div");
    wrapper.className = "lc-carousel";
    wrapper.id = gid;
    wrapper.innerHTML = itemsHtml + '<div class="lc-carousel-dots">' + dotsHtml + '</div>';
    el.parentNode.replaceChild(wrapper, el);
    var elItems = wrapper.querySelectorAll(".lc-carousel-item");
    var dots = wrapper.querySelectorAll(".lc-carousel-dots span");
    var idx = 0;
    function show(n) {
      elItems.forEach(function(x){ x.classList.remove("active"); });
      dots.forEach(function(x){ x.classList.remove("active"); });
      elItems[n].classList.add("active");
      dots[n].classList.add("active");
      idx = n;
    }
    dots.forEach(function(d){ d.addEventListener("click", function(){ show(parseInt(d.dataset.idx, 10)); }); });
    setInterval(function(){ show((idx + 1) % elItems.length); }, delay);
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
