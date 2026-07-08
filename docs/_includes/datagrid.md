{%- comment -%}
Datagrid — inline AG Grid variants, activated from md + IAL.

Inline, data in the code block (YAML/JSON/CSV per format=""):
  ```yaml
  - name: Lucky
    species: dog
  ```
  {: .datagrid title="Pets" height="300" }

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
.lc-datagrid-title .lc-datagrid-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-datagrid-grid { width: 100%; }
.lc-datagrid-status { padding: 0.7em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #666; font-style: italic; }
.lc-datagrid-err { padding: 0.9em 1em; color: #b00; background: #fff5f5; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; white-space: pre-wrap; }
/* ƒ computed columns — derived, read-only, recomputed live from a formula */
.lc-datagrid-grid .ag-cell.lc-dg-computed { background: #f6f8fa; color: #0a5; font-variant-numeric: tabular-nums; }
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
      html += '</div>';
    }
    html += '<div class="lc-datagrid-status">loading grid…</div>';
    html += '<div class="lc-datagrid-grid ag-theme-alpine" style="height:' + (opts.height || 400) + 'px; display:none;"></div>';
    div.innerHTML = html;
    return div;
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
      detailOf: el.getAttribute(prefix + "master") || el.getAttribute(prefix + "detail-of") || "",
      filterExpr: el.getAttribute(prefix + "filter") || "",
      compute: el.getAttribute(prefix + "compute") || ""
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
    var wrapper = buildDatagridWrapper({ id: id, title: title, format: bindId ? "" : format, height: height });
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

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry
     and the shared helpers aliased above. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.datagrid, pre.datagrid", upgradeDatagridInline);
    window.lcRegisterUpgrader("div.lc-datagrid-src", upgradeDatagridFile);
  }

})();
</script>
