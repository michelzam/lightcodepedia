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
/* lazy blocks */
.lc-lazy-block { border: 1px solid #ddd; border-radius: 6px; margin: 0.5em 0; overflow: hidden; }
.lc-lazy-block > summary { padding: 0.65em 1em; background: #f5f5f5; cursor: pointer; font-weight: 600; list-style: none; user-select: none; }
.lc-lazy-block > summary::-webkit-details-marker { display: none; }
.lc-lazy-block[open] > summary { background: #e8f0fe; color: #0066cc; border-bottom: 1px solid #ddd; }
.lc-lazy-block .lc-lazy-content { padding: 0.3em 0 0; }
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
/* blocks */
.lc-blocks { display: grid; gap: 18px; margin: 1em 0; }
.lc-block { border: 1px solid #ddd; border-radius: 8px; padding: 1.5em 2em; background: #fff; overflow: hidden; }
.lc-block > h3:first-child { margin-top: 0; margin-bottom: 0.6em; font-size: 1.1em; color: #222; display: flex; align-items: center; gap: 0.4em; }
.lc-block img { max-width: 100%; border-radius: 4px; display: block; margin: 0.6em auto; }
.lc-block p:last-child, .lc-block ul:last-child { margin-bottom: 0; }
.lc-help { cursor: help; font-style: normal; font-size: 0.9em; opacity: 0.6; transition: opacity 0.15s; }
.lc-help:hover { opacity: 1; }
/* embed */
.lc-embed { margin: 0.5em 0; }
@media (max-width: 600px) { .lc-blocks { grid-template-columns: 1fr !important; } }
/* chart */
.lc-chart { margin: 1em 0; position: relative; }
/* map */
.lc-map { margin: 1em 0; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
/* qr */
.lc-qr { display: inline-block; text-align: center; margin: 1em 0; padding: 1em 1.2em; background: #fff; border: 1px solid #ddd; border-radius: 8px; }
.lc-qr canvas, .lc-qr img { display: block; }
.lc-qr-label { font-size: 0.85em; color: #555; margin-top: 0.6em; }
</style>
<script>
(function(){
  if (window.lcPyrun) return;
  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  // Instance registry — destroy heavy components before live-preview re-render.
  var _lcReg = [];
  function _lcRegister(el, fn) { _lcReg.push({ el: el, fn: fn }); }
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

  function safe(fn) {
    return function(el) { try { fn(el); } catch(e) { if (window.console) console.warn("[lc]", e.message || e); } };
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
    document.querySelectorAll(".highlighter-rouge.run, pre.run").forEach(safe(upgradeRun));
    document.querySelectorAll(".highlighter-rouge.repl, pre.repl").forEach(safe(upgradeRepl));
    document.querySelectorAll(".highlighter-rouge.code, pre.code").forEach(safe(upgradeCode));
    document.querySelectorAll(".highlighter-rouge.datagrid, pre.datagrid").forEach(safe(upgradeDatagrid));
    document.querySelectorAll("div.lc-datagrid-src").forEach(safe(upgradeDatagridFile));
    document.querySelectorAll(".highlighter-rouge.form, pre.form").forEach(safe(upgradeForm));
    document.querySelectorAll("div.lc-form-src").forEach(safe(upgradeFormFile));
    document.querySelectorAll("ul.carousel").forEach(safe(upgradeCarousel));
    document.querySelectorAll(".highlighter-rouge.accordion, pre.accordion").forEach(safe(upgradeAccordion));
    document.querySelectorAll(".highlighter-rouge.tabs, pre.tabs").forEach(safe(upgradeTabsInline));
    document.querySelectorAll("p.tabs").forEach(safe(upgradeTabsFile));
    document.querySelectorAll(".highlighter-rouge.radio, pre.radio").forEach(safe(upgradeRadio));
    document.querySelectorAll(".highlighter-rouge.grid, pre.grid").forEach(safe(upgradeGrid));
    document.querySelectorAll(".highlighter-rouge.scrollable, pre.scrollable").forEach(safe(upgradeScrollable));
    document.querySelectorAll(".highlighter-rouge.cards, pre.cards").forEach(safe(upgradeCards));
    document.querySelectorAll(".highlighter-rouge.block, .highlighter-rouge.blocks, pre.block, pre.blocks").forEach(safe(upgradeBlock));
    document.querySelectorAll("ul.dropdown").forEach(safe(upgradeDropdown));
    document.querySelectorAll("p.button").forEach(safe(upgradeButton));
    document.querySelectorAll("p.embed-page").forEach(safe(upgradeEmbedPage));
    document.querySelectorAll("p.embed").forEach(safe(upgradeEmbedExternal));
    document.querySelectorAll("p.video").forEach(safe(upgradeVideo));
    document.querySelectorAll(".highlighter-rouge.chart, pre.chart, p.chart").forEach(safe(upgradeChart));
    document.querySelectorAll(".highlighter-rouge.map, pre.map").forEach(safe(upgradeMap));
    document.querySelectorAll(".highlighter-rouge.qr, pre.qr").forEach(safe(upgradeQr));
    document.querySelectorAll(".highlighter-rouge.pytutor, pre.pytutor").forEach(safe(upgradePyTutor));
    document.querySelectorAll("p.folder").forEach(safe(upgradeFolder));
    document.querySelectorAll("p.recorder").forEach(safe(upgradeRecorder));
    document.querySelectorAll("p.lightnodes").forEach(safe(upgradeNodes));
  }

  // Scoped version of scan() — runs the full upgrade pipeline on a subtree.
  // Used by the live editor preview so the page-level scan() is not needed.
  function scanElement(root) {
    _applyIAL(root);
    root.querySelectorAll(".highlighter-rouge.run, pre.run").forEach(safe(upgradeRun));
    root.querySelectorAll(".highlighter-rouge.repl, pre.repl").forEach(safe(upgradeRepl));
    root.querySelectorAll(".highlighter-rouge.code, pre.code").forEach(safe(upgradeCode));
    root.querySelectorAll(".highlighter-rouge.datagrid, pre.datagrid").forEach(safe(upgradeDatagrid));
    root.querySelectorAll("div.lc-datagrid-src").forEach(safe(upgradeDatagridFile));
    root.querySelectorAll(".highlighter-rouge.form, pre.form").forEach(safe(upgradeForm));
    root.querySelectorAll("div.lc-form-src").forEach(safe(upgradeFormFile));
    root.querySelectorAll("ul.carousel").forEach(safe(upgradeCarousel));
    if (window.lcUpgradeQuiz)  root.querySelectorAll("ul.quiz, ol.quiz").forEach(window.lcUpgradeQuiz);
    if (window.lcUpgradeAgent) root.querySelectorAll(".highlighter-rouge.agent, pre.agent").forEach(window.lcUpgradeAgent);
    root.querySelectorAll(".highlighter-rouge.accordion, pre.accordion").forEach(safe(upgradeAccordion));
    root.querySelectorAll(".highlighter-rouge.tabs, pre.tabs").forEach(safe(upgradeTabsInline));
    root.querySelectorAll("p.tabs").forEach(safe(upgradeTabsFile));
    root.querySelectorAll(".highlighter-rouge.radio, pre.radio").forEach(safe(upgradeRadio));
    root.querySelectorAll(".highlighter-rouge.grid, pre.grid").forEach(safe(upgradeGrid));
    root.querySelectorAll(".highlighter-rouge.scrollable, pre.scrollable").forEach(safe(upgradeScrollable));
    root.querySelectorAll(".highlighter-rouge.cards, pre.cards").forEach(safe(upgradeCards));
    root.querySelectorAll(".highlighter-rouge.block, .highlighter-rouge.blocks, pre.block, pre.blocks").forEach(safe(upgradeBlock));
    root.querySelectorAll("ul.dropdown").forEach(safe(upgradeDropdown));
    root.querySelectorAll("p.button").forEach(safe(upgradeButton));
    root.querySelectorAll("p.embed-page").forEach(safe(upgradeEmbedPage));
    root.querySelectorAll("p.embed").forEach(safe(upgradeEmbedExternal));
    root.querySelectorAll("p.video").forEach(safe(upgradeVideo));
    root.querySelectorAll(".highlighter-rouge.chart, pre.chart, p.chart").forEach(safe(upgradeChart));
    root.querySelectorAll(".highlighter-rouge.map, pre.map").forEach(safe(upgradeMap));
    root.querySelectorAll(".highlighter-rouge.qr, pre.qr").forEach(safe(upgradeQr));
    root.querySelectorAll(".highlighter-rouge.pytutor, pre.pytutor").forEach(safe(upgradePyTutor));
    root.querySelectorAll("p.folder").forEach(safe(upgradeFolder));
    root.querySelectorAll("p.recorder").forEach(safe(upgradeRecorder));
    root.querySelectorAll("p.lightnodes").forEach(safe(upgradeNodes));
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
    return window.marked ? marked.parse(s) : "<pre>" + s + "</pre>";
  }
  window.lcLoadMarked = loadMarked;
  window.lcScanElement = scanElement;
  window.lcApplyIAL   = _applyIAL;

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

  var _maplibreQ = null;
  function loadMapLibre(cb) {
    if (window.maplibregl) { cb(); return; }
    if (_maplibreQ) { _maplibreQ.push(cb); return; }
    _maplibreQ = [cb];
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/npm/maplibre-gl@4/dist/maplibre-gl.css";
    document.head.appendChild(link);
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/maplibre-gl@4/dist/maplibre-gl.js";
    s.onload = function() { var q = _maplibreQ; _maplibreQ = null; q.forEach(function(f){ f(); }); };
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
        _lcRegister(wrap, function() { if (instance) { try { instance.destroy(); } catch(e) {} instance = null; } });
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
      var ch = new Chart(document.getElementById(gid), {
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
      _lcRegister(wrap, function() { try { ch.destroy(); } catch(e) {} });
    });
  }

  function upgradeMap(el) {
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var zoom = parseInt(el.getAttribute("zoom") || "12", 10);
    var h = el.getAttribute("height") || "350";
    var gid = "lc-map-" + Math.random().toString(36).slice(2, 7);
    var wrap = document.createElement("div");
    wrap.className = "lc-map";
    wrap.id = gid;
    wrap.style.height = h + "px";
    el.parentNode.replaceChild(wrap, el);
    var markers = [];
    try {
      var parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        parsed.forEach(function(item) {
          var mlat = parseFloat(item.lat), mlon = parseFloat(item.lon != null ? item.lon : item.lng);
          if (!isNaN(mlat) && !isNaN(mlon)) markers.push({ lat: mlat, lon: mlon, label: item.label || item.name || "" });
        });
      }
    } catch(e) {
      var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
      if (lines.length >= 2) {
        var hdrs = lines[0].split(",").map(function(v){ return v.trim(); });
        var nI = ["label","name"].reduce(function(a, k){ return hdrs.indexOf(k) >= 0 ? hdrs.indexOf(k) : a; }, 0);
        var laI = hdrs.indexOf("lat") >= 0 ? hdrs.indexOf("lat") : 1;
        var lnI = ["lon","lng"].reduce(function(a, k){ return hdrs.indexOf(k) >= 0 ? hdrs.indexOf(k) : a; }, 2);
        lines.slice(1).forEach(function(l) {
          var c = l.split(",").map(function(v){ return v.trim(); });
          var mlat = parseFloat(c[laI]), mlon = parseFloat(c[lnI]);
          if (!isNaN(mlat) && !isNaN(mlon)) markers.push({ lat: mlat, lon: mlon, label: c[nI] || "" });
        });
      }
    }
    var centerLat = markers.length ? markers.reduce(function(s,m){ return s+m.lat; }, 0)/markers.length : parseFloat(el.getAttribute("lat") || "48.86");
    var centerLon = markers.length ? markers.reduce(function(s,m){ return s+m.lon; }, 0)/markers.length : parseFloat(el.getAttribute("lon") || "2.35");
    loadMapLibre(function() {
      var map = new maplibregl.Map({
        container: gid,
        style: "https://tiles.openfreemap.org/styles/positron",
        center: [centerLon, centerLat],
        zoom: zoom,
        pitch: parseFloat(el.getAttribute("pitch") || "0"),
        bearing: parseFloat(el.getAttribute("bearing") || "0"),
        maxPitch: 85
      });
      map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");
      _lcRegister(wrap, function() { try { map.remove(); } catch(e) {} });

      // Shift+drag to pivot in 3D (bearing + pitch), like deck.gl / Streamlit.
      // Horizontal → rotate (bearing); vertical → tilt (pitch).
      var canvas = map.getCanvas();
      var pivot = null;
      canvas.addEventListener("mousedown", function(e) {
        if (!e.shiftKey || e.button !== 0) return;
        pivot = { x: e.clientX, y: e.clientY, bearing: map.getBearing(), pitch: map.getPitch() };
        map.dragPan.disable();
        canvas.style.cursor = "move";
        e.preventDefault();
        e.stopPropagation();
      });
      window.addEventListener("mousemove", function(e) {
        if (!pivot) return;
        map.setBearing(pivot.bearing - (e.clientX - pivot.x) * 0.5);
        map.setPitch(Math.max(0, Math.min(85, pivot.pitch + (e.clientY - pivot.y) * 0.5)));
      });
      window.addEventListener("mouseup", function() {
        if (!pivot) return;
        pivot = null;
        map.dragPan.enable();
        canvas.style.cursor = "";
      });

      markers.forEach(function(m) {
        var dot = document.createElement("div");
        dot.style.cssText = "width:13px;height:13px;background:#e05454;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.35);cursor:pointer";
        new maplibregl.Marker({ element: dot })
          .setLngLat([m.lon, m.lat])
          .setPopup(new maplibregl.Popup({ offset: 12 }).setText(m.label))
          .addTo(map);
      });

      // Hint overlay
      var hint = document.createElement("div");
      hint.textContent = "⇧ Shift + drag to tilt / rotate";
      hint.style.cssText = "position:absolute;bottom:8px;left:8px;background:rgba(255,255,255,0.85);color:#555;font-size:0.72em;padding:3px 8px;border-radius:4px;pointer-events:none;z-index:2";
      wrap.style.position = "relative";
      wrap.appendChild(hint);
    });
  }

  var _qrcodeQ = null;
  function loadQRCode(cb) {
    if (window.QRCode) { cb(); return; }
    if (_qrcodeQ) { _qrcodeQ.push(cb); return; }
    _qrcodeQ = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/gh/davidshimjs/qrcodejs/qrcode.min.js";
    s.onload = function() { var q = _qrcodeQ; _qrcodeQ = null; q.forEach(function(f){ f(); }); };
    document.head.appendChild(s);
  }

  function upgradeQr(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
    var text = lines[0] || "";
    var label = lines.length > 1 ? lines.slice(1).join(" ").trim() : "";
    var size = parseInt(el.getAttribute("size") || "180", 10);
    if (!text) return;
    var wrap = document.createElement("div");
    wrap.className = "lc-qr";
    var qrDiv = document.createElement("div");
    wrap.appendChild(qrDiv);
    if (label) {
      var cap = document.createElement("div");
      cap.className = "lc-qr-label";
      cap.textContent = label;
      wrap.appendChild(cap);
    }
    el.parentNode.replaceChild(wrap, el);
    loadQRCode(function() {
      new QRCode(qrDiv, { text: text, width: size, height: size, correctLevel: QRCode.CorrectLevel.M });
    });
  }

  function upgradeAccordion(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var wrap = document.createElement("div");
    wrap.className = "lc-accordion";
    sections.forEach(function(s) {
      var d = document.createElement("details");
      var sum = document.createElement("summary");
      sum.textContent = s.label;
      var body = document.createElement("div");
      body.className = "lc-ac-body";
      d.appendChild(sum);
      d.appendChild(body);
      d.addEventListener("toggle", function() {
        if (!d.open || body.dataset.lcReady) return;
        body.dataset.lcReady = "1";
        loadMarked(function() {
          body.innerHTML = markdownBody(s.body);
          _applyIAL(body);
          body.querySelectorAll("p.video").forEach(safe(upgradeVideo));
          body.querySelectorAll("p.embed").forEach(safe(upgradeEmbedExternal));
          body.querySelectorAll("ul.carousel").forEach(safe(upgradeCarousel));
          if (window.lcUpgradeQuiz) body.querySelectorAll("ul.quiz, ol.quiz").forEach(window.lcUpgradeQuiz);
        });
      });
      wrap.appendChild(d);
    });
    el.parentNode.replaceChild(wrap, el);
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
    var href = a.getAttribute("href");
    // External URLs → iframe
    if (/^https?:\/\//i.test(href)) {
      el.parentNode.replaceChild(_iframeEl(href, el.getAttribute("height") || "600"), el);
      return;
    }
    // Local module → fetch the raw markdown source and render it inline.
    // [Lucky](/_dog) → docs/_dog.md fetched from raw.githubusercontent.
    var container = document.createElement("div");
    container.className = "lc-embed";
    container.innerHTML = "<div style='color:#aaa;font-style:italic;padding:0.5em 0'>⏳ Loading…</div>";
    el.parentNode.replaceChild(container, el);
    var rel = href.replace(/^\/+|\/+$/g, "");
    if (!/\.md$/i.test(rel)) rel += ".md";
    var srcUrl = _lcSiteRepo
      ? "https://raw.githubusercontent.com/" + _lcSiteRepo + "/HEAD/docs/" + rel
      : "/" + rel;
    fetch(srcUrl)
      .then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
      .then(function(text) {
        // strip optional YAML front matter
        if (text.indexOf("---") === 0) {
          var end = text.indexOf("\n---", 3);
          if (end >= 0) { var nl = text.indexOf("\n", end + 1); text = nl >= 0 ? text.slice(nl + 1) : ""; }
        }
        loadMarked(function() { container.innerHTML = marked.parse(text.trim()); });
      })
      .catch(function(err) {
        container.innerHTML = "<div style='color:#c00'>⚠️ Could not load " + escapeHtml(href) + ": " + escapeHtml(err.message) + "</div>";
      });
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
              return { title: title, snippet: meta.snippet, url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, "") };
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
        wrap.innerHTML = items.map(function(item) {
          var style = item.isSubdir ? ' style="background:#f0f2f5"' : '';
          var card = '<div class="lc-card"' + style + '><h3><a href="' + item.url + '">' + escapeHtml(item.title) + '</a></h3>';
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
    el.parentNode.replaceChild(wrap, el);
    loadMarked(function() {
      wrap.innerHTML = sections.map(function(s) {
        return "<div class=\"lc-card\"><h3>" + s.label + "</h3>" + markdownBody(s.body) + "</div>";
      }).join("");
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

  function _renderAndScanBlock(wrap, sections) {
    wrap.innerHTML = sections.map(function(s) {
      var html = '<div class="lc-block">';
      if (s.label) {
        var helpMatch = s.label.match(/^(.*?)\s*\[([^\]]+)\]\s*$/);
        var title = helpMatch ? helpMatch[1].trim() : s.label;
        var help = helpMatch ? helpMatch[2] : null;
        html += '<h3>' + title;
        if (help) html += ' <span class="lc-help" title="' + escapeHtml(help) + '">ℹ️</span>';
        html += '</h3>';
      }
      html += markdownBody(s.body);
      return html + '</div>';
    }).join("");
    _applyIAL(wrap);
    wrap.querySelectorAll("p.video").forEach(safe(upgradeVideo));
    wrap.querySelectorAll("p.button").forEach(safe(upgradeButton));
    wrap.querySelectorAll("p.embed-page").forEach(safe(upgradeEmbedPage));
    wrap.querySelectorAll("p.embed").forEach(safe(upgradeEmbedExternal));
    if (window.lcUpgradeQuiz) wrap.querySelectorAll("ul.quiz, ol.quiz").forEach(window.lcUpgradeQuiz);
    wrap.querySelectorAll(".highlighter-rouge.run, pre.run").forEach(safe(upgradeRun));
    wrap.querySelectorAll(".highlighter-rouge.datagrid, pre.datagrid").forEach(safe(upgradeDatagrid));
    wrap.querySelectorAll(".highlighter-rouge.form, pre.form").forEach(safe(upgradeForm));
    wrap.querySelectorAll(".highlighter-rouge.chart, pre.chart, p.chart").forEach(safe(upgradeChart));
    wrap.querySelectorAll(".highlighter-rouge.map, pre.map").forEach(safe(upgradeMap));
    wrap.querySelectorAll(".highlighter-rouge.pytutor, pre.pytutor").forEach(safe(upgradePyTutor));
  }

  function upgradeBlock(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var lazy = el.classList.contains("lazy");
    var cols = el.getAttribute("cols") || "1";
    var colStyle = cols === "1" ? "1fr" : "repeat(" + cols + ", 1fr)";
    var sections = parseSections(el);
    if (!sections.length) {
      var code = el.querySelector("code");
      var raw = (code ? code.textContent : el.textContent).trim();
      sections = [{ label: "", body: raw }];
    }

    if (lazy) {
      var titles = sections.filter(function(s){ return s.label; }).map(function(s){
        var m = s.label.match(/^(.*?)\s*\[([^\]]+)\]\s*$/);
        return m ? m[1].trim() : s.label;
      });
      var summaryText = titles.length ? titles.join(" · ") : "Section";
      var details = document.createElement("details");
      details.className = "lc-lazy-block";
      var sumEl = document.createElement("summary");
      sumEl.textContent = summaryText;
      var content = document.createElement("div");
      content.className = "lc-lazy-content";
      details.appendChild(sumEl);
      details.appendChild(content);
      el.parentNode.replaceChild(details, el);
      details.addEventListener("toggle", function() {
        if (!details.open || details.dataset.lcReady) return;
        details.dataset.lcReady = "1";
        var wrap = document.createElement("div");
        wrap.className = "lc-blocks";
        wrap.style.gridTemplateColumns = colStyle;
        content.appendChild(wrap);
        loadMarked(function() { _renderAndScanBlock(wrap, sections); });
      });
      return;
    }

    var wrap = document.createElement("div");
    wrap.className = "lc-blocks";
    wrap.style.gridTemplateColumns = colStyle;
    el.parentNode.replaceChild(wrap, el);
    loadMarked(function() { _renderAndScanBlock(wrap, sections); });
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

  // ── Screen + face recorder ────────────────────────────────────────────────
  function upgradeRecorder(el, hooks) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    hooks = hooks || {};
    var pipAttr = el.getAttribute("pip") || "bottom-right";
    var pipSize = parseInt(el.getAttribute("size") || "240", 10);
    var camZoom = parseFloat(el.getAttribute("zoom") || "1.35");
    var fps     = parseInt(el.getAttribute("fps")  || "25",  10);

    var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
                (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    var canScreen = !isIOS && !!navigator.mediaDevices && !!navigator.mediaDevices.getDisplayMedia;
    // macOS desktop: rely on the native Presenter Overlay for the face (it composites
    // the camera into the screen capture in higher quality and avoids a second camera
    // consumer that destabilises Safari). So we don't open our own camera there.
    var isMac = !isIOS && /Mac/.test(navigator.platform || navigator.userAgent || "");

    // Safari 16+ reports video/webm as supported (VP9 playback) but produces
    // poor/inconsistent recordings — prefer mp4 there. Chrome/Firefox use webm.
    var isSafari = /safari/i.test(navigator.userAgent) && !/chrome|chromium|crios|android/i.test(navigator.userAgent);
    var candidates = isSafari
      ? ["video/mp4;codecs=avc1","video/mp4;codecs=h264","video/mp4","video/webm"]
      : ["video/webm;codecs=vp9","video/webm","video/mp4"];
    var mimeType = candidates.find(function(t){ return MediaRecorder.isTypeSupported(t); }) || "";
    if (!mimeType && isSafari) mimeType = "video/mp4";
    var ext = mimeType.includes("mp4") ? "mp4" : "webm";

    /* ── Widget (in-page launcher) ── */
    var wrap = document.createElement("div");
    wrap.className = "lc-recorder";
    wrap.innerHTML = [
      '<style>',
      '.lc-recorder{border:1px solid #ddd;border-radius:10px;overflow:hidden;max-width:480px;font-family:inherit}',
      '.lc-rec-head{background:#1e1e2e;color:#cdd6f4;display:flex;align-items:center;gap:10px;padding:10px 14px;font-size:.9em;font-weight:600}',
      '.lc-rec-dot{width:10px;height:10px;border-radius:50%;background:#555;flex-shrink:0}',
      '.lc-rec-dot.live{background:#f33;animation:lcBlink 1s infinite}',
      '@keyframes lcBlink{0%,100%{opacity:1}50%{opacity:.2}}',
      '.lc-rec-body{padding:14px 16px;background:#fafafa}',
      '.lc-rec-opts{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}',
      '.lc-rec-opt{font-size:.82em;padding:4px 10px;border:1px solid #ccc;border-radius:20px;cursor:pointer;background:#fff;color:#333;user-select:none}',
      '.lc-rec-opt.on{background:#0066cc;color:#fff;border-color:#0066cc}',
      '.lc-rec-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}',
      '.lc-rec-btn{padding:.45em 1.2em;border:none;border-radius:6px;cursor:pointer;font-size:.9em;font-weight:600}',
      '.lc-rec-btn.start{background:#0066cc;color:#fff}.lc-rec-btn.start:hover{background:#0052a3}',
      '.lc-rec-btn.stop{background:#c00;color:#fff}.lc-rec-btn.stop:hover{background:#a00}',
      '.lc-rec-btn.again{background:#eee;color:#333}.lc-rec-btn.again:hover{background:#ddd}',
      '.lc-rec-status{font-size:.82em;color:#888;margin-top:8px;min-height:1.2em}',
      '.lc-rec-status.ok{color:#1a7a1a}.lc-rec-status.err{color:#c00}',
      '.lc-rec-ios{font-size:.84em;line-height:1.6;color:#444;background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:10px 12px;margin-top:4px}',
      '.lc-rec-ios ol{margin:6px 0 0 16px;padding:0}',
      '.lc-rec-ios li{margin-bottom:2px}',
      /* HUD styles */
      '.lc-rec-hud{position:fixed;z-index:2147483647;background:transparent;padding:0;display:flex;flex-direction:column;align-items:center;gap:6px;user-select:none;touch-action:none;cursor:grab}',
      '.lc-rec-hud:active{cursor:grabbing}',
      '.lc-rec-hud-pip{width:96px;height:96px;border-radius:50%;overflow:hidden;border:3px solid rgba(255,255,255,.9);flex-shrink:0;background:#111;position:relative;box-shadow:0 6px 24px rgba(0,0,0,.45)}',
      '.lc-rec-hud-pip video{width:100%;height:100%;object-fit:cover;display:block;transform:scaleX(-1)}',
      '.lc-rec-hud-pip .lc-cam-off{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2em}',
      '.lc-rec-hud-timer{color:#fff;font-size:.85em;font-variant-numeric:tabular-nums;font-weight:700;letter-spacing:.04em;min-height:1.2em;background:rgba(15,15,25,.78);padding:2px 10px;border-radius:12px}',
      '.lc-rec-hud-stop{background:#c00;color:#fff;border:none;border-radius:14px;padding:5px 14px;cursor:pointer;font-size:.85em;font-weight:600;box-shadow:0 3px 12px rgba(0,0,0,.4)}',
      '.lc-rec-hud-stop:hover{background:#a00}',
      '.lc-rec-hud-ios{font-size:.72em;color:#fff;text-align:center;max-width:140px;line-height:1.4;background:rgba(15,15,25,.78);padding:6px 10px;border-radius:10px}',
      '.lc-rec-hud-timer-btn{font-size:.75em;color:#fff;background:rgba(15,15,25,.78);border:1px solid #777;border-radius:12px;padding:3px 10px;cursor:pointer}',
      '.lc-rec-hud-timer-btn.running{color:#f88;border-color:#f88}',
      '.lc-rec-hud-pip canvas{position:absolute;inset:0;width:100%;height:100%;display:none;transform:scaleX(-1)}',
      '.lc-rec-hud-ctrls{display:flex;gap:6px;align-items:center}',
      '.lc-rec-hud-pause{background:#333;color:#fff;border:none;border-radius:14px;padding:5px 12px;cursor:pointer;font-size:.85em;font-weight:600;box-shadow:0 3px 12px rgba(0,0,0,.4)}',
      '.lc-rec-hud-pause:hover{background:#222}',
      '.lc-rec-hud-pause.paused{background:#1a7a1a}.lc-rec-hud-pause.paused:hover{background:#156315}',
      /* Review + launcher modals */
      '.lc-rec-ov{position:fixed;inset:0;z-index:2147483646;background:rgba(10,10,20,.62);display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(3px)}',
      '.lc-rec-panel{background:#fff;border-radius:14px;box-shadow:0 20px 60px rgba(0,0,0,.4);max-width:560px;width:100%;max-height:90vh;overflow:auto;position:relative}',
      '.lc-rec-panel-close{position:absolute;top:8px;right:10px;background:none;border:none;font-size:1.3em;color:#888;cursor:pointer;line-height:1;z-index:2}',
      '.lc-rec-panel-close:hover{color:#333}',
      '.lc-rec-review-vid{width:100%;display:block;background:#000;border-radius:14px 14px 0 0;max-height:60vh}',
      '.lc-rec-review-body{padding:14px 18px 18px}',
      '.lc-rec-review-meta{font-size:.82em;color:#888;margin-bottom:12px}',
      '.lc-rec-review-acts{display:flex;gap:8px;flex-wrap:wrap}',
      '.lc-rec-review-acts button{padding:.5em 1.1em;border:none;border-radius:7px;cursor:pointer;font-size:.9em;font-weight:600}',
      '.lc-rb-save{background:#0066cc;color:#fff}.lc-rb-save:hover{background:#0052a3}',
      '.lc-rb-again{background:#eee;color:#333}.lc-rb-again:hover{background:#ddd}',
      '.lc-rb-discard{background:#fff;color:#c00;border:1px solid #f0caca!important}.lc-rb-discard:hover{background:#fff5f5}',
      '</style>',
      '<div class="lc-rec-head"><span class="lc-rec-dot" id="lc-rd"></span><span>🎬 Screen Recorder</span></div>',
      '<div class="lc-rec-body">',
      '  <div class="lc-rec-opts" id="lc-ropts">',
      isMac ? '' : '    <span class="lc-rec-opt on"  id="lc-ropt-cam">📷 Camera</span>',
      '    <span class="lc-rec-opt on"  id="lc-ropt-mic">🎤 Mic</span>',
      canScreen ? '<span class="lc-rec-opt off" id="lc-ropt-snd">🔊 Screen audio</span>' : '',
      isMac ? '' : '<span class="lc-rec-opt" id="lc-ropt-bg">🖼 BG: Off</span>',
      '  </div>',
      '  <div class="lc-rec-actions">',
      canScreen
        ? '<button class="lc-rec-btn start" id="lc-rbtn">▶ Start recording</button>'
        : '<button class="lc-rec-btn start" id="lc-rbtn">📱 Show camera</button>',
      '  </div>',
      isMac ? [
        '<div class="lc-rec-ios" style="background:#eef4ff;border-color:#cdddff;color:#234">',
        '<strong>💡 Add your face with Presenter Overlay</strong>',
        '<div>Once you press Start, a green 🟢 <strong>camera/screen icon</strong> appears in the macOS menu bar (top-right). Click it → <strong>Presenter Overlay → Small</strong>. macOS composites your camera into the recording in higher quality than any in-page overlay. <em>(The menu only shows while we hold the camera — i.e. during recording.)</em></div>',
        '</div>'
      ].join("") : '',
      isIOS ? [
        '<div class="lc-rec-ios">',
        '<strong>📱 iPhone screen recording</strong>',
        '<ol>',
        '<li>Tap <strong>Show camera</strong> above — your face appears floating</li>',
        '<li>Open Control Center (swipe from top-right)</li>',
        '<li>Long-press <strong>⏺ Screen Recording</strong> → enable Microphone</li>',
        '<li>Tap ⏺ to start — record your demo</li>',
        '<li>Tap the red status bar to stop</li>',
        '</ol>',
        '<em>Video saves to your Photos app.</em>',
        '</div>'
      ].join("") : '',
      '  <div class="lc-rec-status" id="lc-rstat"></div>',
      '</div>'
    ].join("");
    el.parentNode.replaceChild(wrap, el);

    var btnEl   = wrap.querySelector("#lc-rbtn");
    var statEl  = wrap.querySelector("#lc-rstat");
    var dotEl   = wrap.querySelector("#lc-rd");
    var optCam  = wrap.querySelector("#lc-ropt-cam");
    var optMic  = wrap.querySelector("#lc-ropt-mic");
    var optSnd  = wrap.querySelector("#lc-ropt-snd");

    // On macOS we don't run our own camera — the native Presenter Overlay owns it.
    var useCam = !isMac, useMic = true, useSnd = false;
    var bgMode = "none";
    var optBg  = wrap.querySelector("#lc-ropt-bg");
    var bgCycle  = ["none","blur","dark","blue","green","white"];
    var bgLabels = { none: "🖼 BG: Off", blur: "🌫 BG: Blur", dark: "⬛ BG: Dark", blue: "🔵 BG: Blue", green: "🟢 BG: Green", white: "⬜ BG: White" };
    if (optCam) optCam.addEventListener("click", function(){ useCam = !useCam; optCam.classList.toggle("on", useCam); refreshHUD(); });
    optMic.addEventListener("click", function(){ useMic = !useMic; optMic.classList.toggle("on", useMic); });
    if (optSnd) optSnd.addEventListener("click", function(){ useSnd = !useSnd; optSnd.classList.toggle("on", useSnd); });
    if (optBg) optBg.addEventListener("click", function() {
      bgMode = bgCycle[(bgCycle.indexOf(bgMode) + 1) % bgCycle.length];
      optBg.textContent = bgLabels[bgMode];
      optBg.classList.toggle("on", bgMode !== "none");
      if (hud) refreshHUDCam();
    });

    function setStatus(msg, cls) { statEl.className = "lc-rec-status " + (cls||""); statEl.textContent = msg; }
    function fmtTime(ms) {
      var s = Math.floor(ms/1000), m = Math.floor(s/60);
      return String(m).padStart(2,"0") + ":" + String(s%60).padStart(2,"0");
    }

    /* ── Floating HUD ── */
    var hud = null, hudCamVid = null, hudTimer = null, hudStop = null, hudPause = null;
    var hudIosTimer = null, hudIosBtn = null;
    var isPaused = false, pausedAccum = 0, pauseStart = 0;
    var bgCanvas = null, bgCtx = null, bgHidVid = null, bgSegmenter = null, bgAnimId = null, bgActive = false;

    function hudInitialPos() {
      var margin = 20;
      var w = 116; // approx hud width
      if (pipAttr === "bottom-right") return { right: margin + "px", bottom: margin + "px" };
      if (pipAttr === "bottom-left")  return { left:  margin + "px", bottom: margin + "px" };
      if (pipAttr === "top-right")    return { right: margin + "px", top:    margin + "px" };
      return { left: margin + "px", top: margin + "px" };
    }

    function createHUD() {
      if (hud) return;
      hud = document.createElement("div");
      hud.className = "lc-rec-hud";
      var pos = hudInitialPos();
      Object.keys(pos).forEach(function(k){ hud.style[k] = pos[k]; });

      // On macOS the face comes from the native Presenter Overlay, so we show only
      // the floating controls (timer + pause + stop) — no camera pip, no segmentation.
      if (!isMac) {
        var pipWrap = document.createElement("div");
        pipWrap.className = "lc-rec-hud-pip";
        pipWrap.style.width = pipSize + "px";
        pipWrap.style.height = pipSize + "px";
        hudCamVid = document.createElement("video");
        hudCamVid.autoplay = true; hudCamVid.muted = true; hudCamVid.playsInline = true;
        // Zoom into the face (mirrored) so it fills the circle rather than showing the whole torso.
        hudCamVid.style.transform = "scaleX(-1) scale(" + camZoom + ")";
        var camOffEl = document.createElement("div");
        camOffEl.className = "lc-cam-off"; camOffEl.textContent = "📷";
        pipWrap.appendChild(hudCamVid);
        pipWrap.appendChild(camOffEl);
        bgCanvas = document.createElement("canvas");
        // Backing store rendered well above the CSS circle size so the composited
        // face stays as crisp as the rest of the (often retina/4K) screen capture.
        var bgScale = Math.min(3, Math.max(2, window.devicePixelRatio || 1));
        bgCanvas.width = Math.round(pipSize * bgScale);
        bgCanvas.height = Math.round(pipSize * bgScale);
        bgCtx = bgCanvas.getContext("2d");
        pipWrap.appendChild(bgCanvas);
        bgHidVid = document.createElement("video");
        bgHidVid.autoplay = true; bgHidVid.muted = true; bgHidVid.playsInline = true;
        bgHidVid.style.cssText = "position:absolute;width:1px;height:1px;opacity:0;pointer-events:none";
        document.body.appendChild(bgHidVid);
        hud.appendChild(pipWrap);
      } else {
        // small label so the floating control reads as "recording" without a face
        var macTag = document.createElement("div");
        macTag.className = "lc-rec-hud-timer";
        macTag.style.cssText = "background:rgba(15,15,25,.78);color:#fff";
        macTag.textContent = "🎬 Recording";
        hud.appendChild(macTag);
      }

      hudTimer = document.createElement("div");
      hudTimer.className = "lc-rec-hud-timer";
      hud.appendChild(hudTimer);

      if (isIOS) {
        var iosNote = document.createElement("div");
        iosNote.className = "lc-rec-hud-ios";
        iosNote.textContent = "Start Screen Recording from Control Center";
        hud.appendChild(iosNote);
        hudIosBtn = document.createElement("button");
        hudIosBtn.className = "lc-rec-hud-timer-btn";
        hudIosBtn.textContent = "⏱ Start timer";
        hud.appendChild(hudIosBtn);
        var iosRunning = false, iosStart = 0, iosInterval = null;
        hudIosBtn.addEventListener("click", function(e) {
          e.stopPropagation();
          if (!iosRunning) {
            iosRunning = true; iosStart = Date.now();
            hudIosBtn.className = "lc-rec-hud-timer-btn running";
            hudIosBtn.textContent = "⏹ Stop timer";
            iosInterval = setInterval(function(){ hudTimer.textContent = fmtTime(Date.now()-iosStart); }, 500);
          } else {
            iosRunning = false;
            clearInterval(iosInterval);
            hudIosBtn.className = "lc-rec-hud-timer-btn";
            hudIosBtn.textContent = "⏱ Start timer";
          }
        });
      } else {
        var ctrls = document.createElement("div");
        ctrls.className = "lc-rec-hud-ctrls";
        hudPause = document.createElement("button");
        hudPause.className = "lc-rec-hud-pause";
        hudPause.textContent = "⏸";
        hudPause.title = "Pause";
        hudPause.addEventListener("click", function(e) { e.stopPropagation(); togglePause(); });
        hudPause.style.display = "none";
        hudStop = document.createElement("button");
        hudStop.className = "lc-rec-hud-stop";
        hudStop.textContent = "⏹ Stop";
        hudStop.addEventListener("click", function(e) {
          e.stopPropagation();
          if (recorder && (recorder.state === "recording" || recorder.state === "paused")) recorder.stop();
        });
        hudStop.style.display = "none";
        ctrls.appendChild(hudPause);
        ctrls.appendChild(hudStop);
        hud.appendChild(ctrls);
      }

      makeDraggable(hud);
      document.body.appendChild(hud);
      refreshHUDCam();
    }

    function destroyHUD() {
      stopBg();
      if (hud) { hud.parentNode && hud.parentNode.removeChild(hud); hud = null; hudCamVid = null; hudTimer = null; hudStop = null; }
      if (bgHidVid) { bgHidVid.parentNode && bgHidVid.parentNode.removeChild(bgHidVid); bgHidVid = null; }
      bgCanvas = null; bgCtx = null;
    }

    function refreshHUDCam() {
      if (!hud || isMac || !hudCamVid) return;
      var pipWrap = hud.querySelector(".lc-rec-hud-pip");
      var offEl   = hud.querySelector(".lc-cam-off");
      var showBg  = bgMode !== "none" && useCam && !!camStream;
      if (bgCanvas) bgCanvas.style.display = showBg ? "block" : "none";
      if (useCam && camStream) {
        hudCamVid.srcObject = showBg ? null : camStream;
        hudCamVid.style.display = showBg ? "none" : "block";
        offEl.style.display = "none";
        pipWrap.style.border = "3px solid rgba(255,255,255,.85)";
        if (showBg) startBg(); else stopBg();
      } else {
        hudCamVid.srcObject = null;
        hudCamVid.style.display = "block";
        offEl.style.display = "flex";
        pipWrap.style.border = "3px solid rgba(255,255,255,.3)";
        stopBg();
      }
    }

    function refreshHUD() {
      if (hud) refreshHUDCam();
    }

    function togglePause() {
      if (!recorder) return;
      if (recorder.state === "recording") {
        recorder.pause();
        isPaused = true; pauseStart = Date.now();
        if (hudPause) { hudPause.className = "lc-rec-hud-pause paused"; hudPause.textContent = "▶"; hudPause.title = "Resume"; }
        dotEl.classList.remove("live");
        setStatus("⏸ Paused — resume from the floating panel.");
      } else if (recorder.state === "paused") {
        recorder.resume();
        isPaused = false; pausedAccum += Date.now() - pauseStart;
        if (hudPause) { hudPause.className = "lc-rec-hud-pause"; hudPause.textContent = "⏸"; hudPause.title = "Pause"; }
        dotEl.classList.add("live");
        setStatus("● Recording — stop via the floating panel.");
      }
    }

    /* ── Review before save ── */
    function showReview(blob) {
      var url = URL.createObjectURL(blob);
      var ts  = new Date().toISOString().slice(0,19).replace(/:/g,"-");
      var fname = "recording-" + ts + "." + ext;
      var mb = (blob.size / 1048576).toFixed(1);
      var ov = document.createElement("div");
      ov.className = "lc-rec-ov";
      ov.innerHTML = [
        '<div class="lc-rec-panel">',
        '  <button class="lc-rec-panel-close" title="Discard">✕</button>',
        '  <video class="lc-rec-review-vid" controls autoplay playsinline></video>',
        '  <div class="lc-rec-review-body">',
        '    <div class="lc-rec-review-meta">' + fname + ' · ' + mb + ' MB</div>',
        '    <div class="lc-rec-review-acts">',
        '      <button class="lc-rb-save">⬇ Save</button>',
        '      <button class="lc-rb-again">↻ Re-record</button>',
        '      <button class="lc-rb-discard">🗑 Discard</button>',
        '    </div>',
        '  </div>',
        '</div>'
      ].join("");
      document.body.appendChild(ov);
      ov.querySelector("video").src = url;
      function close() { URL.revokeObjectURL(url); ov.parentNode && ov.parentNode.removeChild(ov); }
      ov.querySelector(".lc-rb-save").addEventListener("click", function() {
        var a = document.createElement("a");
        a.href = url; a.download = fname; a.click();
        setStatus("✅ Saved as " + fname, "ok");
        close();
      });
      ov.querySelector(".lc-rb-again").addEventListener("click", function() {
        close();
        startRecording();
      });
      var discard = function() { setStatus("Recording discarded.", ""); close(); };
      ov.querySelector(".lc-rb-discard").addEventListener("click", discard);
      ov.querySelector(".lc-rec-panel-close").addEventListener("click", discard);
      ov.addEventListener("click", function(e) { if (e.target === ov) discard(); });
    }

    /* ── Virtual background (MediaPipe Selfie Segmentation) ── */
    function loadMediaPipe(cb) {
      if (window.SelfieSegmentation) { cb(); return; }
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation@0.1/selfie_segmentation.js";
      s.crossOrigin = "anonymous";
      s.onload  = function() { window.SelfieSegmentation ? cb() : setStatus("⚠️ BG model unavailable","err"); };
      s.onerror = function() { setStatus("⚠️ BG model failed to load","err"); };
      document.head.appendChild(s);
    }

    function startBg() {
      if (!bgCanvas || !bgHidVid || !camStream) return;
      bgActive = true;
      bgHidVid.srcObject = camStream;
      if (bgSegmenter) { bgLoop(); return; }
      setStatus("Loading background model…");
      loadMediaPipe(function() {
        bgSegmenter = new SelfieSegmentation({ locateFile: function(f) {
          return "https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation@0.1/" + f;
        }});
        bgSegmenter.setOptions({ modelSelection: 1 });
        bgSegmenter.onResults(onSegResults);
        bgSegmenter.initialize().then(function() { setStatus(""); bgLoop(); });
      });
    }

    function stopBg() {
      bgActive = false;
      if (bgAnimId) { cancelAnimationFrame(bgAnimId); bgAnimId = null; }
      if (bgHidVid) bgHidVid.srcObject = null;
    }

    function bgLoop() {
      if (!bgActive) return;
      bgAnimId = requestAnimationFrame(function() {
        if (!bgActive || bgMode === "none" || !bgSegmenter) return;
        if (bgHidVid && bgHidVid.readyState >= 2) {
          bgSegmenter.send({ image: bgHidVid }).then(bgLoop).catch(bgLoop);
        } else {
          bgLoop();
        }
      });
    }

    function onSegResults(results) {
      if (!bgCtx || !bgCanvas || bgMode === "none") return;
      var w = bgCanvas.width, h = bgCanvas.height;
      bgCtx.clearRect(0, 0, w, h);
      var iw = bgHidVid.videoWidth  || w;
      var ih = bgHidVid.videoHeight || h;
      // "cover" scale × user zoom so the face fills the circle, then re-centre.
      var scale = Math.max(w / iw, h / ih) * camZoom;
      var sw = iw * scale, sh = ih * scale;
      var dx = (w - sw) / 2, dy = (h - sh) / 2;
      // Feather amount scales with the (hi-res) canvas so the contour stays soft
      // regardless of circle size — this hides the jagged segmentation edge.
      var feather = Math.max(2, Math.round(w * 0.018));

      // Person pixels, then keep only what the (blurred → soft-edged) mask covers.
      bgCtx.save();
      bgCtx.drawImage(results.image, dx, dy, sw, sh);
      bgCtx.globalCompositeOperation = "destination-in";
      bgCtx.filter = "blur(" + feather + "px)";
      bgCtx.drawImage(results.segmentationMask, dx, dy, sw, sh);
      bgCtx.filter = "none";
      bgCtx.restore();

      // Background painted behind the person.
      bgCtx.save();
      bgCtx.globalCompositeOperation = "destination-over";
      if (bgMode === "blur") {
        bgCtx.filter = "blur(18px)";
        bgCtx.drawImage(results.image, dx, dy, sw, sh);
        bgCtx.filter = "none";
        bgCtx.fillStyle = "#111";
        bgCtx.fillRect(0, 0, w, h);
      } else {
        var bgColors = { dark: "#1a1a2e", blue: "#0d3b66", green: "#1a472a", white: "#f5f5f5" };
        bgCtx.fillStyle = bgColors[bgMode] || "#111";
        bgCtx.fillRect(0, 0, w, h);
      }
      bgCtx.restore();
    }

    /* ── Drag ── */
    function makeDraggable(el) {
      var startX, startY, startL, startT, startR, startB;
      function getPos(e) {
        return e.touches ? { x: e.touches[0].clientX, y: e.touches[0].clientY }
                         : { x: e.clientX,            y: e.clientY };
      }
      function onStart(e) {
        if (e.target.tagName === "BUTTON") return;
        var p = getPos(e);
        startX = p.x; startY = p.y;
        var r = el.getBoundingClientRect();
        startL = r.left; startT = r.top;
        el.style.right = el.style.bottom = "auto";
        el.style.left = startL + "px"; el.style.top = startT + "px";
        document.addEventListener("mousemove", onMove);
        document.addEventListener("touchmove", onMove, { passive: false });
        document.addEventListener("mouseup",   onEnd);
        document.addEventListener("touchend",  onEnd);
      }
      function onMove(e) {
        if (e.cancelable) e.preventDefault();
        var p = getPos(e);
        var nx = startL + p.x - startX;
        var ny = startT + p.y - startY;
        nx = Math.max(0, Math.min(window.innerWidth  - el.offsetWidth,  nx));
        ny = Math.max(0, Math.min(window.innerHeight - el.offsetHeight, ny));
        el.style.left = nx + "px"; el.style.top = ny + "px";
      }
      function onEnd() {
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("touchmove", onMove);
        document.removeEventListener("mouseup",   onEnd);
        document.removeEventListener("touchend",  onEnd);
      }
      el.addEventListener("mousedown",  onStart);
      el.addEventListener("touchstart", onStart, { passive: true });
    }

    /* ── Camera stream ── */
    var camStream = null;
    function initCam(cb) {
      if (!useCam) { if (cb) cb(); return; }
      navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 1280 } }, audio: false })
        .then(function(s) {
          camStream = s;
          refreshHUDCam();
          if (cb) cb();
        })
        .catch(function() {
          useCam = false; optCam.classList.remove("on");
          if (cb) cb();
        });
    }

    /* ── Button ── */
    btnEl.addEventListener("click", function() {
      if (recorder && recorder.state === "recording") { recorder.stop(); return; }
      if (isIOS) {
        // iOS: show HUD with camera pip, user does native screen recording
        initCam(function() {
          createHUD();
          btnEl.textContent = "✅ Camera active";
          btnEl.disabled = true;
          setStatus("Your camera is floating. Follow the steps above.", "ok");
          if (hooks.onStart) hooks.onStart();
        });
        return;
      }
      startRecording();
    });

    /* ── Desktop recording ── */
    var recorder = null, chunks = [], timerInterval = null;

    function startRecording() {
      btnEl.disabled = true;
      setStatus("Requesting screen share…");
      // getDisplayMedia MUST be called synchronously from the user gesture —
      // any preceding async call (e.g. getUserMedia) breaks the gesture chain in Safari.
      navigator.mediaDevices.getDisplayMedia({
            // Cap at ~1080p: Safari's MediaRecorder is unstable encoding 4K and tends
            // to die after a few seconds. Share a single window for crisp code text.
            video: { frameRate: fps, width: { max: 1920 }, height: { max: 1080 } },
            audio: useSnd
          })
          .then(function(screenStream) {
            createHUD();
            setStatus("Setting up…");
            // The camera is ONLY used for the HUD pip / as the Presenter Overlay
            // source — it never joins the recording stream. So acquire it in the
            // BACKGROUND: a camera prompt or denial must never block Start, or the
            // Stop/Pause buttons would never appear. (On macOS we hold it so macOS
            // offers Presenter Overlay, but we don't draw our own circle.)
            var wantCam = useCam || isMac;
            if (wantCam) {
              navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 1280 } }, audio: false })
                .then(function(s) { camStream = s; if (!isMac) refreshHUDCam(); })
                .catch(function() { if (!isMac) { useCam = false; if (optCam) optCam.classList.remove("on"); refreshHUDCam(); } });
            }

            // Only the mic must be ready before we start — its audio track joins the
            // recording. (MediaRecorder ignores tracks added after .start().)
            var micPromise = useMic
              ? navigator.mediaDevices.getUserMedia({ audio: true, video: false })
                  .then(function(m) { return m; })
                  .catch(function() { return null; })
              : Promise.resolve(null);

            micPromise.then(function(micStream) {
              if (micStream) micStream.getAudioTracks().forEach(function(t){ screenStream.addTrack(t); });
              launch(screenStream);
            });

            function launch(stream) {
              chunks = [];
              var vs = stream.getVideoTracks()[0].getSettings() || {};
              var W = vs.width || 1920, H = vs.height || 1080;
              var recOpts = {};
              // Safari ignores videoBitsPerSecond — omit it and let the native encoder decide.
              // Other browsers get a generous target scaled to screen resolution.
              if (!isSafari) {
                recOpts.videoBitsPerSecond = Math.min(40000000, Math.max(8000000, Math.round(W * H * fps * 0.25)));
              }
              if (mimeType) recOpts.mimeType = mimeType;
              recorder = new MediaRecorder(stream, recOpts);
              chunks = [];
              recorder.ondataavailable = function(e){ if (e.data.size) chunks.push(e.data); };
              recorder.onstop = function() {
                clearInterval(timerInterval);
                stream.getTracks().forEach(function(t){ t.stop(); });
                if (camStream) { camStream.getTracks().forEach(function(t){ t.stop(); }); camStream = null; }
                destroyHUD();
                dotEl.classList.remove("live");
                isPaused = false; pausedAccum = 0;
                btnEl.disabled = false; btnEl.className = "lc-rec-btn again"; btnEl.textContent = "▶ Record again";
                [optCam, optMic, optSnd].filter(Boolean).forEach(function(o){ o.style.pointerEvents = ""; o.style.opacity = ""; });
                if (hooks.onStop) hooks.onStop();
                var blob = new Blob(chunks, { type: mimeType || "video/webm" });
                if (!blob.size) { setStatus("Nothing was recorded.", "err"); return; }
                setStatus("Review your recording…");
                showReview(blob);
              };
              // If the user stops sharing via the browser's own "Stop sharing" bar
              stream.getVideoTracks()[0].addEventListener("ended", function() {
                if (recorder && recorder.state === "recording") recorder.stop();
              });
              recorder.start(1000);
              var startTs = Date.now();
              isPaused = false; pausedAccum = 0;
              dotEl.classList.add("live");
              if (hudStop)  hudStop.style.display  = "";
              if (hudPause) hudPause.style.display = "";
              btnEl.disabled = false; btnEl.className = "lc-rec-btn stop"; btnEl.textContent = "⏹ Stop";
              timerInterval = setInterval(function(){
                if (!hudTimer) return;
                var elapsed = Date.now() - startTs - pausedAccum - (isPaused ? Date.now() - pauseStart : 0);
                hudTimer.textContent = fmtTime(elapsed);
              }, 500);
              setStatus("● Recording — stop via the floating panel.");
              [optCam, optMic, optSnd].filter(Boolean).forEach(function(o){ o.style.pointerEvents = "none"; o.style.opacity = ".5"; });
              if (hooks.onStart) hooks.onStart();
            }
          })
          .catch(function(e) {
            destroyHUD();
            btnEl.disabled = false;
            setStatus("❌ " + (e.name === "NotAllowedError" ? "Screen share was cancelled." : e.message), "err");
          });
    }
  }

  // Global launcher — open the recorder from anywhere (e.g. the topbar) without
  // needing a .recorder tag on the page. Builds a placeholder, upgrades it inside
  // a modal, and closes the modal chrome once recording starts so it isn't captured.
  window.lcOpenRecorder = function(opts) {
    opts = opts || {};
    if (document.getElementById("lc-rec-launcher")) return;
    var ov = document.createElement("div");
    ov.id = "lc-rec-launcher";
    ov.className = "lc-rec-ov";
    var panel = document.createElement("div");
    panel.className = "lc-rec-panel";
    panel.style.maxWidth = "480px";
    panel.style.background = "transparent";
    panel.style.boxShadow = "none";
    var close = document.createElement("button");
    close.className = "lc-rec-panel-close";
    close.title = "Close"; close.textContent = "✕"; close.style.color = "#fff";
    var p = document.createElement("p");
    p.className = "recorder";
    ["pip","size","zoom","fps"].forEach(function(k){ if (opts[k] != null) p.setAttribute(k, opts[k]); });
    panel.appendChild(close);
    panel.appendChild(p);
    ov.appendChild(panel);
    document.body.appendChild(ov);
    function closeLauncher() { ov.parentNode && ov.parentNode.removeChild(ov); }
    close.addEventListener("click", closeLauncher);
    ov.addEventListener("click", function(e){ if (e.target === ov) closeLauncher(); });
    upgradeRecorder(p, { onStart: closeLauncher });
  };

  window.lcPyrun = { attach: attach };
  if (window.lcPyrunQueue) {
    window.lcPyrunQueue.forEach(function(fn){ try { fn(); } catch (e) {} });
    window.lcPyrunQueue = null;
  }

  function upgradePyTutor(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var code = el.querySelector("code");
    var initialCode = (code ? code.textContent : el.textContent).trim();
    if (!initialCode) return;
    var h       = el.getAttribute("height") || "400";
    var boundTo = el.getAttribute("bound-to");

    function buildUrl(codeStr) {
      return "https://pythontutor.com/iframe-embed.html#code="
        + encodeURIComponent(codeStr)
        + "&py=3&origin=opt-frontend.js&cumulative=false&heapPrimitives=newin&textReferences=false";
    }

    function makeFrame(src) {
      var f = document.createElement("iframe");
      f.src = src; f.width = "100%"; f.height = h + "px";
      f.style.border = "none"; f.setAttribute("loading", "lazy");
      return f;
    }

    var f = makeFrame(buildUrl(initialCode));
    el.parentNode.replaceChild(f, el);

    if (boundTo) {
      var runEl = document.getElementById("lc-pyrun-" + boundTo);
      if (runEl) {
        var ta = runEl.querySelector(".lc-pyrun-code");
        if (ta) {
          var _pytTimer = null;
          ta.addEventListener("input", function() {
            clearTimeout(_pytTimer);
            _pytTimer = setTimeout(function() {
              // Replace the element entirely — setting src on a hash-based URL
              // doesn't trigger an iframe reload in any browser.
              var newF = makeFrame(buildUrl(ta.value));
              f.parentNode.replaceChild(newF, f);
              f = newF;
            }, 600);
          });
        }
      }
    }
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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
})();
</script>
