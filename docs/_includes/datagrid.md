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
          // dataset-backed grid: AG mutates the dataset's row objects in
          // place — notify listeners so every bound widget re-renders
          if (opts.bindId && window.lcSetDataset) {
            window.lcSetDataset(opts.bindId, window.lcDatasets[opts.bindId] || data);
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
      detailOf: el.getAttribute(prefix + "master") || el.getAttribute(prefix + "detail-of") || "",
      filterExpr: el.getAttribute(prefix + "filter") || ""
    };
  }

  var DG_ID = 0;
  function upgradeDatagridInline(el) {
    if (el.dataset.lcUpgraded) return;
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
