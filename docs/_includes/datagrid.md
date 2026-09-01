{%- comment -%}
Datagrid — inline AG Grid variants, activated from md + IAL.

Inline, data in the code block (YAML/JSON/CSV per format=""):
  ```yaml
  - name: Lucky
    species: dog
  ```
  {: .datagrid title="Pets" height="300" }

save="dogs.yaml" — the two-repo contract (same as the mdpad's): the
fence is the AUTHOR's seed; the learner's rows persist in their OWN bench
and override the seed on the next visit. Relative = beside the lesson
(the page's folder, full course path); "/my/…" = bench root. 💾 keeps, ↺
restores the seed. ƒ computed columns are stripped on save (derived, the
author's). The author republishes freely — different files, different
repos, one writer each.

File-backed (div.lc-datagrid-src emitted by the code include):
  fetches data-raw / data-cdn and renders the same grid.

Also exports window.lcRenderDatagridFromJson — the Python bridge for
show.grid(rows) in .run blocks.

The dataset-bound table variant (bind="…") lives in dataset.md as
upgradeDatagridBound; the A2 duplicate-name split ends here.

Auto-included by docs/_layouts/default.html (before dataset.md so the
.lc-datagrid cascade keeps its historical order).
{%- endcomment -%}

<style>
.lc-datagrid { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-datagrid-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-datagrid-title .lc-datagrid-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: var(--lc-ink-mute, #616161); letter-spacing: 0.05em; }
.lc-datagrid-edit-hint { float: right; font-size: 0.72em; font-weight: 500;
  color: #475569; background: #eef2f7; border-radius: 99px; padding: 0.1em 0.6em;
  text-transform: none; letter-spacing: 0; }
.lc-datagrid-grid { width: 100%; }
.lc-datagrid-status { padding: 0.7em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #666; font-style: italic; }
/* min-height: this is where an unwired grid comes to rest, and the ⚙️ that
   repairs it is aimed with a thumb — a one-line notice is not a target. */
.lc-datagrid-err { padding: 0.9em 1em; min-height: 44px; box-sizing: border-box; color: #b00; background: #fff5f5; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; white-space: pre-wrap; }
/* ƒ computed columns — derived, read-only, recomputed live from a formula */
.lc-datagrid-grid .ag-cell.lc-dg-computed { background: #f6f8fa; color: #0a5; font-variant-numeric: tabular-nums; }
/* save= — the learner's keep bar under the grid */
.lc-dg-savebar { display: flex; align-items: center; gap: 0.5em; padding: 0.4em 0.9em; border-top: 1px solid #e5e7eb; background: #fafafa; }
.lc-dg-mine { margin-right: auto; font-size: 0.78em; color: #2e7d32; }
.lc-dg-save { font: inherit; font-size: 0.85em; padding: 0.3em 0.9em; border-radius: 6px; border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; margin-left: auto; }
.lc-dg-save:hover:not(:disabled) { background: #0052a3; }
.lc-dg-save:disabled { opacity: 0.45; cursor: default; }
.lc-dg-mine:not([hidden]) ~ .lc-dg-save { margin-left: 0; }
.lc-dg-reset { font: inherit; font-size: 0.85em; padding: 0.3em 0.6em; border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-dg-reset:hover { border-color: #888; color: #222; }
/* 🕘 versions — the shared panel (lcVersions), styled to match the pad's */
.lc-ver-btn { font: inherit; font-size: 0.85em; padding: 0.3em 0.6em; border-radius: 6px;
  border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-ver-btn:hover { border-color: #888; color: #222; }
.lc-ver-panel { border-top: 1px solid #e5e7eb; background: #fafafa; font-size: 0.88em; }
.lc-ver-panel ol { list-style: none; margin: 0; padding: 0; max-height: 200px; overflow: auto; }
.lc-ver-panel li { display: flex; align-items: center; gap: 0.6em; padding: 0.4em 0.9em;
  border-bottom: 1px solid #eee; }
.lc-ver-panel li:last-child { border-bottom: none; }
.lc-ver-panel li.now { background: #eef6ff; }
.lc-ver-panel li.starter { background: #fffbeb; }
.lc-ver-panel li.starter .lc-ver-when { color: #92400e; font-style: italic; }
.lc-ver-when { flex: 1; color: #444; }
.lc-ver-sha { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #94a3b8; font-size: 0.85em; }
.lc-ver-panel button { font: inherit; font-size: 0.85em; padding: 0.2em 0.6em; border-radius: 5px;
  border: 1px solid #cbd5e1; background: #fff; color: #334155; cursor: pointer; }
.lc-ver-panel button:hover { border-color: #0066cc; color: #0066cc; }
.lc-ver-diff { margin: 0; padding: 0.7em 0.9em; background: #fff; border-top: 1px solid #eee;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82em;
  line-height: 1.5; white-space: pre-wrap; overflow: auto; max-height: 240px; }
.lc-ver-diff .add { background: #dcfce7; color: #166534; display: block; }
.lc-ver-diff .del { background: #fee2e2; color: #991b1b; display: block; }
.lc-ver-diff .same { color: #64748b; display: block; }
/* a changed VALUE, not a changed row: red where it was, green where it is */
.lc-datagrid-grid .ag-cell.lc-dg-was { background: #fee2e2; color: #991b1b; font-weight: 600; }
.lc-datagrid-grid .ag-cell.lc-dg-now { background: #dcfce7; color: #166534; font-weight: 600; }
</style>

<script>
(function () {
  if (window._lcDatagridReady) return;
  window._lcDatagridReady = true;

  /* shared helpers from code_chrome.md (parsed earlier — topbar include) */
  var escapeHtml  = window.lcEscapeHtml;
  var prettifyKey = window.lcPrettifyKey;
  var loadAgGrid  = window.lcAgGridReady;
  var parseDatagridText = window.lcParseDataText;

  /* repo-file source: source="file:path/in/repo" → raw/cdn URLs, mirroring the
     old datagrid_file.md include. Shared with form.md via window. */
  var LC_REPO   = {{ site.github.repository_nwo | default: "" | jsonify }};
  var LC_BRANCH = "main";
  var LC_SHA    = {{ site.github.build_revision | default: "main" | jsonify }};
  var LC_CANON  = {{ site.lc_canonical_host | default: "" | jsonify }};
  function lcFileSrc(path) {
    return {
      raw: "https://raw.githubusercontent.com/" + LC_REPO + "/" + LC_BRANCH + "/" + path,
      cdn: "https://cdn.jsdelivr.net/gh/" + LC_REPO + "@" + LC_SHA + "/" + path
    };
  }
  function lcUseCdn() {
    return (LC_CANON && location.hostname === LC_CANON) || location.search.indexOf("cdn=1") >= 0;
  }
  function lcInferFormat(path, given) {
    if (given) return given.toLowerCase();
    if (/\.json$/i.test(path)) return "json";
    if (/\.csv$/i.test(path))  return "csv";
    return "yaml";
  }
  window.lcFileSrc = lcFileSrc;
  window.lcUseCdn = lcUseCdn;
  window.lcInferFormat = lcInferFormat;

  /* "col = expr; col2 = expr2" → [{col, expr}] — a formula per computed column,
     evaluated in declaration order so a column may reference an earlier one. */
  function parseComputeSpecs(str) {
    if (!str) return [];
    return str.split(";").map(function (part) {
      var i = part.indexOf("=");
      if (i < 0) return null;
      var col = part.slice(0, i).trim(), expr = part.slice(i + 1).trim();
      return (col && expr) ? { col: col, expr: expr } : null;
    }).filter(Boolean);
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
    if (opts.id) div.setAttribute("data-lc-id", opts.id);
    var html = "";
    if (opts.title) {
      html += '<div class="lc-datagrid-title">📊 <span>' + escapeHtml(opts.title) + '</span>';
      if (opts.mode) html += '<span class="lc-datagrid-lang" style="font-style:italic; text-transform:none;">' + escapeHtml(opts.mode) + '</span>';
      if (opts.format) html += '<span class="lc-datagrid-lang">' + escapeHtml(opts.format) + '</span>';
      /* AN EDITABLE GRID THAT LOOKS READ-ONLY IS READ-ONLY. Editing needs a
         DOUBLE-click (double-tap on a phone), which nothing on screen said —
         so a reader invited to change a value simply did not (Michel,
         2026-08-20, testing the public taster). The affordance belongs on
         the grid, not in the prose of whichever lesson remembers to add it. */
      if (opts.editable) html += '<span class="lc-datagrid-edit-hint">✏️ double-click a cell</span>';
      html += '</div>';
    }
    html += '<div class="lc-datagrid-status">loading grid…</div>';
    html += '<div class="lc-datagrid-grid ag-theme-alpine" style="height:' + (opts.height || 400) + 'px; display:none;"></div>';
    div.innerHTML = html;
    return div;
  }


  var EMPTY_MSG = "Empty dataset — nothing to show.";

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
    /* An unresolved source= NEVER settles: it names a dataset that will never
       register, so this promise waits forever and the grid sits at "loading
       grid…" — a sliver that is nearly unhittable on a phone, and that reads
       as a stuck page rather than the wiring mistake it is. After a grace
       period (long enough for a .dataset further down the page, or a fetch
       still in flight) fall to the empty state: a solid, tappable target that
       says what is actually wrong. The promise is deliberately left pending —
       a dataset that does arrive late still paints straight over this. */
    var painted = false;
    if (opts.bindId) {
      var grace = window.lcDatagridBindGrace;
      if (grace == null) grace = 4000;
      setTimeout(function () { if (!painted) showError(opts.empty || EMPTY_MSG); }, grace);
    }
    Promise.all([dataPromise, loadAgGrid()]).then(function(results){
      painted = true;
      var data = results[0];
      if (!Array.isArray(data)) {
        showError("Expected an array of objects; got: " + (data === null ? "null" : typeof data));
        return;
      }
      if (data.length === 0) {
        showError(opts.empty || EMPTY_MSG);
        return;
      }
      /* computed columns: seed them so they appear as (read-only) columns; a
         formula fills them once the page runtime is ready, and on every edit. */
      var computeSpecs = parseComputeSpecs(opts.compute);
      var computedSet = {};
      if (computeSpecs.length) {
        computeSpecs.forEach(function (s) { computedSet[s.col] = true; });
        data.forEach(function (row) {
          if (row && typeof row === "object")
            computeSpecs.forEach(function (s) { if (!(s.col in row)) row[s.col] = "…"; });
        });
      }
      var cols = inferColumns(data);
      if (cols.length === 0) {
        showError("No columns inferred — rows must be objects with keys.");
        return;
      }
      if (computeSpecs.length) {
        cols.forEach(function (c) {
          if (computedSet[c.field]) {
            c.editable = false;
            c.cellClass = "lc-dg-computed";
            c.headerName = "ƒ " + c.headerName;
          }
        });
      }
      if (statusEl && statusEl.parentNode) statusEl.remove();
      /* a grace-period empty notice can be standing here — the dataset came
         late, which is the one case that notice must not outlive */
      var staleErr = wrapper.querySelector(".lc-datagrid-err");
      if (staleErr) staleErr.remove();
      gridEl.style.display = "";
      var gridOptions = {
        columnDefs: cols,
        rowData: data,
        defaultColDef: {
          sortable: true, filter: true, resizable: true, flex: 1, minWidth: 80,
          editable: !!opts.editable,
          cellClass: opts.cellClass || null,
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
          // dataset-backed grid: AG mutates the dataset's row objects in
          // place — notify listeners so every bound widget re-renders
          if (opts.bindId && window.lcSetDataset) {
            window.lcSetDataset(opts.bindId, window.lcDatasets[opts.bindId] || data);
          }
          // an input cell changed → the ƒ columns recompute from their formulas
          recompute();
        };
      }
      var api = window.agGrid.createGrid(gridEl, gridOptions);
      window.lcMasterDetail.registerGrid(gridId, api);

      /* Cell editors are DATA, never credentials. The browser pairs a saved
         key with "the text field it saw" — a campus cell got offered (and
         once, stolen as) a password-manager username. Editors are created
         per edit, so mark each one as it takes focus. */
      if (opts.editable) gridEl.addEventListener("focusin", function (e) {
        var t = e.target;
        if (t && t.tagName === "INPUT" && !t.getAttribute("autocomplete")) {
          t.setAttribute("autocomplete", "off");
          t.setAttribute("name", "lc-cell");
          t.setAttribute("data-lpignore", "true");   /* the common managers' opt-outs */
          t.setAttribute("data-1p-ignore", "true");
        }
      });

      /* A DERIVED grid must keep listening. It used to take the dataset once
         (the promise that gave it its first paint) and never hear another
         word — so repairing a dog upstream recomputed the query, and the
         "invisible dogs" grid below went on showing the old answer. A
         derived view that does not follow its source is worse than no view:
         it is a confident wrong number. Skip the echo of our OWN edit (same
         array back again) so an edit never resets scroll or selection. */
      if (opts.bindId && window.lcDatasetListeners) {
        var adopt = function (rows) {
          if (!Array.isArray(rows) || rows === data) return;
          data = rows;
          api.setGridOption("rowData", rows);
          recompute();
        };
        window.lcDatasetListeners[opts.bindId] = window.lcDatasetListeners[opts.bindId] || [];
        window.lcDatasetListeners[opts.bindId].push(adopt);
        /* AG Grid loads asynchronously, so the dataset can move between the
           promise that fed our first paint and this line — the learner's
           saved copy arriving is exactly that case. Adopt whatever is current
           before trusting the stream. */
        if (window.lcDatasets) adopt(window.lcDatasets[opts.bindId]);
      }

      /* Recompute every ƒ column: eval each formula per row with that row's
         fields as locals, in the shared page runtime (so a formula can also
         call a .run silent model). eval, not exec — a bad formula shows ⚠ in
         its own cell, never a frozen grid. */
      function recompute() {
        if (!computeSpecs.length || recompute._busy || !window.lcPageRuntime) return;
        recompute._busy = true;
        try { window._lcDgRows = JSON.stringify(data); }
        catch (e) { recompute._busy = false; return; }
        window._lcDgSpecs = JSON.stringify(computeSpecs);
        window.lcPageRuntime().then(function (mp) {
          try {
            (mp.runPython || mp.run).call(mp,
              "import js, json\n" +
              "_rows = json.loads(str(js.window._lcDgRows))\n" +
              "_specs = json.loads(str(js.window._lcDgSpecs))\n" +
              "def _num(v):\n" +               // AG Grid edits come back as strings; a
              "    if not isinstance(v, str): return v\n" +   // numeric-looking one becomes a number
              "    s = v.strip()\n" +          // just for the formula (input cells are untouched)
              "    try: return int(s) if s.lstrip('+-').isdigit() else float(s)\n" +
              "    except (ValueError, TypeError): return v\n" +
              "for _r in _rows:\n" +
              "    for _k in list(_r.keys()): _r[_k] = _num(_r[_k])\n" +
              "    for _s in _specs:\n" +
              "        try:\n" +
              "            _r[_s['col']] = eval(_s['expr'], globals(), _r)\n" +
              "        except Exception as _e:\n" +
              "            _r[_s['col']] = '\\u26a0 ' + str(_e)\n" +
              "js.window._lcDgOut = json.dumps(_rows)\n");
            var out = JSON.parse(window._lcDgOut);
            data.forEach(function (row, i) {
              var o = out[i]; if (!o) return;
              computeSpecs.forEach(function (s) { row[s.col] = o[s.col]; });
            });
            api.refreshCells({ force: true });
          } catch (e) { if (window.console) console.warn("[lc datagrid compute]", e.message || e); }
          recompute._busy = false;
        }).catch(function () { recompute._busy = false; });
      }
      if (computeSpecs.length) {
        recompute();
        // also recompute when a form/model elsewhere changes (a formula may read
        // a page global); recompute never dispatches the event, so no loop.
        document.addEventListener("lc-model-changed", recompute);
      }

      /* save="my/dogs.yaml" — the two-repo contract, same as the mdpad's:
         the fence is the author's seed, the learner's repaired rows persist
         in their OWN bench and override the seed on the next visit. ƒ columns
         are derived, so they are stripped before saving — a formula is the
         author's standing part, not the learner's data. */
      if (opts.save && window.lcBench) {
        var bar = document.createElement("div");
        bar.className = "lc-dg-savebar";
        var mine = document.createElement("span");
        mine.className = "lc-dg-mine";
        mine.hidden = wrapper.getAttribute("data-lc-mine") !== "1";
        mine.textContent = "✓ yours — saved in your space";
        var reset = document.createElement("button");
        reset.type = "button"; reset.className = "lc-dg-reset";
        reset.textContent = "↺ Start over";
        reset.title = "Bring back the lesson's data — your saved copy stays until you 💾 again";
        var keep = document.createElement("button");
        keep.type = "button"; keep.className = "lc-dg-save";
        keep.textContent = "💾 Save";
        /* 🕘 versions — ONE call, and the whole feature rides on it. Delete
           these four lines and the grid is exactly as it was. */
        /* Rows are not lines: a text diff of YAML is noise to a reader who
           thinks in dogs and campuses. Show the CHANGED rows only, as a
           grid — was/now pairs, plus which fields moved. Identity is the
           first column when its values are unique (a name), position
           otherwise. */
        var rowKey = function (rows) {
          var f = rows.length ? Object.keys(rows[0])[0] : null;
          if (!f) return null;
          var seen = {};
          for (var i = 0; i < rows.length; i++) {
            var v = String(rows[i][f]);
            if (seen[v]) return null;
            seen[v] = 1;
          }
          return f;
        };
        var rowFields = function (a, b) {
          var out = [], k;
          var keys = Object.keys(a || {}).concat(Object.keys(b || {}));
          keys.forEach(function (k2) { if (out.indexOf(k2) < 0) out.push(k2); });
          return out.filter(function (f) {
            return JSON.stringify((a || {})[f]) !== JSON.stringify((b || {})[f]);
          });
        };
        var diffRows = function (older, now) {
          var key = rowKey(now) && rowKey(older) === rowKey(now) ? rowKey(now) : null;
          var out = [];
          var mark = function (sign, fields, row) {
            var r = { "±": sign, "changed": fields.join(", ") };
            Object.keys(row).forEach(function (f) { r[f] = row[f]; });
            return r;
          };
          if (key) {
            var byOld = {}, byNew = {};
            older.forEach(function (r) { byOld[String(r[key])] = r; });
            now.forEach(function (r) { byNew[String(r[key])] = r; });
            now.forEach(function (r) {
              var o2 = byOld[String(r[key])];
              if (!o2) { out.push(mark("+ added", [], r)); return; }
              var f = rowFields(o2, r);
              if (f.length) { out.push(mark("− was", f, o2)); out.push(mark("+ now", f, r)); }
            });
            older.forEach(function (r) {
              if (!byNew[String(r[key])]) out.push(mark("− removed", [], r));
            });
            return out;
          }
          var n = Math.max(older.length, now.length);
          for (var i = 0; i < n; i++) {
            var a = older[i], b = now[i];
            if (a && !b) { out.push(mark("− removed", [], a)); continue; }
            if (!a && b) { out.push(mark("+ added", [], b)); continue; }
            var fs = rowFields(a, b);
            if (fs.length) { out.push(mark("− was", fs, a)); out.push(mark("+ now", fs, b)); }
          }
          return out;
        };

        var vers = window.lcVersions ? window.lcVersions.attach({
          path: opts.save, el: wrapper, anchor: bar,
          current: function () { return serialize(rowsNow()); },
          diff: function (box, olderText) {
            parseDatagridText(olderText, opts.saveFormat).then(function (old) {
              var rows = diffRows(Array.isArray(old) ? old : [], rowsNow());
              if (!rows.length) {
                box.textContent = "Identical to what you have now.";
                return;
              }
              window.lcRenderDatagridFromJson(
                box, JSON.stringify(rows),
                rows.length / 2 + " change" + (rows.length > 2 ? "s" : ""),
                Math.min(60 + rows.length * 42, 260),
                { cellClass: function (pm) {
                    var r = pm.data || {}, f = pm.colDef.field;
                    if (f === "±" || f === "changed") return null;
                    var moved = String(r.changed || "").split(", ");
                    if (moved.indexOf(f) < 0) return null;
                    return String(r["±"]).charAt(0) === "−" ? "lc-dg-was" : "lc-dg-now";
                  } });
            }).catch(function (e) {
              box.textContent = "Could not read that version: " + (e.message || e);
            });
          },
          apply: function (text) {
            parseDatagridText(text, opts.saveFormat).then(function (rows) {
              if (!Array.isArray(rows)) return;
              if (opts.saveApply) opts.saveApply(rows);
              else { data = rows; api.setGridOption("rowData", rows); recompute(); }
            });
          }
        }) : null;
        bar.appendChild(mine); bar.appendChild(reset);
        if (vers) bar.appendChild(vers.button);
        bar.appendChild(keep);
        wrapper.appendChild(bar);
        /* the same stripe every saved block wears (widgets.md) — a repaired
           grid is the learner's file, and until now only a page slot said so */
        var dgFrame = window.lcBenchFrame
          ? window.lcBenchFrame(wrapper, { path: opts.save, id: gridId,
                                           mine: wrapper.getAttribute("data-lc-mine") === "1" })
          : null;
        var refreshKeep = function () {
          var t = window.lcBench.target(wrapper);
          var why = t.gap
            ? "Your bench for “" + t.gap + "” isn’t paired on this device yet — open Setup"
            : (!t.pat || !t.repo ? "Join the course (connect your key) to keep your work" : "");
          keep.disabled = !!why;
          keep.title = why || "Keep these rows in your own space (" +
            (window.lcBench ? window.lcBench.resolve(opts.save, wrapper) : opts.save) + ")";
        };
        refreshKeep();
        /* a saved file HAS a history — offer it from the first paint */
        if (vers && wrapper.getAttribute("data-lc-mine") === "1") vers.reveal();
        /* the grid's rows as the bench would store them: ƒ columns are the
           author's derived parts, never the learner's data */
        var rowsNow = function () {
          /* An AG Grid cell editor holds its value until it is closed —
             typing "Milwaukee" and clicking 💾 without pressing Enter saved
             the OLD value and the learner's last repair was silently lost.
             Close the editor first, every time anything reads the rows. */
          try { api.stopEditing(); } catch (e) {}
          var rows = [];
          api.forEachNode(function (n) {
            var r = Object.assign({}, n.data);
            computeSpecs.forEach(function (s) { delete r[s.col]; });
            rows.push(r);
          });
          return rows;
        };
        var serialize = function (rows) {
          if (opts.saveFormat === "json") return JSON.stringify(rows, null, 2) + "\n";
          if (window.jsyaml && window.jsyaml.dump) return window.jsyaml.dump(rows);
          throw new Error("YAML writer not loaded yet — try again in a moment");
        };
        keep.addEventListener("click", function () {
          refreshKeep();
          if (keep.disabled) return;
          var rows = rowsNow();
          var text;
          try { text = serialize(rows); }
          catch (e) { window.lcxToast && window.lcxToast(String(e.message || e), false); return; }
          keep.disabled = true; keep.textContent = "💾 Saving…";
          /* FIRST save writes the lesson's own rows first — the repair has
             to have a "before" or the very change the lesson is about
             cannot be shown. Never on load, never blocking. */
          var firstKeep = !wrapper._lcBenchSha;
          (firstKeep && opts.saveSeed
            ? opts.saveSeed().then(function (seedRows) {
                return window.lcBench.write(opts.save, serialize(seedRows),
                                            window.lcStarterMsg, null, wrapper);
              }).then(function (sha) { wrapper._lcBenchSha = sha || wrapper._lcBenchSha; })
                .catch(function () {})
            : Promise.resolve()
          ).then(function () {
          return window.lcBench.write(opts.save, text, "✍️ " + (gridId || opts.save), wrapper._lcBenchSha, wrapper)
            .then(function (sha) {
              wrapper._lcBenchSha = sha || wrapper._lcBenchSha;
              wrapper.setAttribute("data-lc-mine", "1");
              mine.hidden = false;
              if (dgFrame) dgFrame.setMine(true);
              if (vers) { vers.reveal(); vers.close(); }
              window.lcxToast && window.lcxToast("Saved to your space ✓", true);
            })
            .catch(function (e) {
              window.lcxToast && window.lcxToast("Save failed: " + (e.message || e), false);
            })
            .finally(function () { keep.textContent = "💾 Save"; refreshKeep(); });
          });
        });
        reset.addEventListener("click", function () {
          if (!opts.saveSeed) return;
          opts.saveSeed().then(function (rows) {
            /* dataset-backed: put the lesson's rows back UPSTREAM, so the
               charts and queries return to the author's story too */
            if (opts.saveApply) opts.saveApply(rows.slice());
            else { api.setGridOption("rowData", rows); recompute(); }
            window.lcxToast && window.lcxToast("Lesson data restored — 💾 to make it yours", true);
          }).catch(function (e) {
            window.lcxToast && window.lcxToast("Could not restore: " + (e.message || e), false);
          });
        });
      }

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
      painted = true;
      showError("Datagrid error: " + (e.message || String(e)));
    });
  }

  function readDatagridOpts(el, prefix) {
    return {
      editable: el.getAttribute(prefix + "editable") === "true",
      detailOf: el.getAttribute(prefix + "master") || el.getAttribute(prefix + "detail-of") || "",
      filterExpr: el.getAttribute(prefix + "filter") || "",
      compute: el.getAttribute(prefix + "compute") || "",
      save: el.getAttribute(prefix + "save") || "",
      /* what this grid says when nothing arrives. The author knows why it
         might be empty ("Nothing arrives here yet.") far better than a
         generic line does — and in a wiring lesson that sentence IS the
         hint. */
      empty: el.getAttribute(prefix + "empty") || ""
    };
  }

  var DG_ID = 0;
  function upgradeDatagridInline(el) {
    if (el.dataset.lcUpgraded) return;
    /* file: sources render via the bound upgrader (dataset.md); skip without
       claiming the element so that upgrader can take it. */
    if ((el.getAttribute("source") || "").indexOf("file:") === 0) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent : "";
    var height = parseInt(el.getAttribute("height"), 10) || 400;
    var format = (el.getAttribute("format") || "yaml").toLowerCase();
    var title = el.getAttribute("title") || "";
    var id = el.id || ("dg" + (++DG_ID));
    var opts = readDatagridOpts(el, "");
    var bindId = el.getAttribute("source") || el.getAttribute("bind") || "";
    var wrapper = buildDatagridWrapper({ id: id, title: title, format: bindId ? "" : format,
                                        height: height, editable: opts.editable });
    if (bindId) wrapper.setAttribute("data-bind", bindId);
    el.parentNode.replaceChild(wrapper, el);
    var dataPromise;
    if (bindId) {
      /* dataset-backed: rows come from the registered dataset (waits if the
         .dataset block hasn't parsed yet); edits notify it via lcSetDataset */
      opts.bindId = bindId;
      dataPromise = new Promise(function (resolve) {
        if (window.lcDatasets && window.lcDatasets[bindId]) { resolve(window.lcDatasets[bindId]); return; }
        window.lcDatasetListeners = window.lcDatasetListeners || {};
        (window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || []).push(resolve);
      });
    } else {
      try { dataPromise = parseDatagridText(raw, format); }
      catch (e) { dataPromise = Promise.reject(new Error(format.toUpperCase() + " parse error: " + e.message)); }
    }
    /* save= — before first paint, prefer the learner's saved copy over the
       fence seed. The seed stays reachable behind ↺, parsed fresh from the
       fence text, so "start over" needs no network and no author round-trip. */
    if (opts.save && window.lcBench) {
      /* the saved file's format follows ITS extension, not the fence's — a
         csv fence still keeps as yaml/json (the two we can write back) */
      opts.saveFormat = /\.json$/i.test(opts.save) ? "json" : "yaml";
      var seedPromise = dataPromise;
      if (bindId) {
        /* DATASET-backed (the real lesson shape: one .dataset feeding a grid,
           a form, three queries and two charts). The learner's saved rows must
           replace the DATASET, not just this grid — otherwise their repair
           shows in the table while every derived view keeps answering from the
           author's broken seed. Publishing it upstream re-derives the whole
           page from their work, which is the entire point. */
        opts.saveSeed = function () {
          return Promise.resolve(opts._seedRows || window.lcDatasets[bindId] || []);
        };
        opts.saveApply = function (rows) {
          if (window.lcSetDataset) window.lcSetDataset(bindId, rows);
        };
        seedPromise.then(function (rows) { opts._seedRows = (rows || []).slice(); });
        window.lcBench.read(opts.save, wrapper).then(function (f) {
          if (!f) return;
          return parseDatagridText(f.text, opts.saveFormat).then(function (rows) {
            if (!Array.isArray(rows)) return;
            wrapper.setAttribute("data-lc-mine", "1");
            wrapper._lcBenchSha = f.sha;
            opts.saveApply(rows);       /* the listener above repaints this grid */
          });
        }).catch(function () {});
      } else {
        opts.saveSeed = function () { return parseDatagridText(raw, format); };
        dataPromise = window.lcBench.read(opts.save, wrapper).then(function (f) {
          if (!f) return seedPromise;
          wrapper.setAttribute("data-lc-mine", "1");
          wrapper._lcBenchSha = f.sha;
          return parseDatagridText(f.text, opts.saveFormat);
        }).catch(function () { return seedPromise; });
      }
    }
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
    var wrapper = buildDatagridWrapper({ id: id, title: title, format: format, height: height,
                                        mode: useCdn ? "cdn" : "live", editable: opts.editable });
    el.parentNode.replaceChild(wrapper, el);
    var dataPromise = fetch(url)
      .then(function(r){ if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + url); return r.text(); })
      .then(function(text){ return parseDatagridText(text, format); });
    renderGridInto(wrapper, dataPromise, id, opts);
  }

  // Called from Python runners: show.grid(rows)
  window.lcRenderDatagridFromJson = function(viewEl, rowsJson, title, height, opts) {
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
    renderGridInto(wrapper, Promise.resolve(rows), rtId, opts || {});
  };

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry
     and the shared helpers aliased above. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.datagrid, pre.datagrid", upgradeDatagridInline);
    window.lcRegisterUpgrader("div.lc-datagrid-src", upgradeDatagridFile);
  }

})();
</script>
