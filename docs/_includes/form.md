{%- comment -%}
Form — key/value object editor rendered as an AG Grid, activated from md + IAL.

Inline, data in the code block (YAML or JSON per format=""):
  ```yaml
  name: Lucky
  species: dog
  adopted: true
  ```
  {: .form title="Lucky" editable="true" }

Master/detail: {: .form bound="grid-id" } renders whichever row the bound
datagrid publishes, and republishes edits back to it.

File-backed (div.lc-form-src emitted by the code include): fetches
data-raw / data-cdn and renders the same form.

Also exports window.lcRenderFormFromJson — the Python bridge for
show.form(obj) in .run blocks.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
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
</style>

<script>
(function () {
  if (window._lcFormReady) return;
  window._lcFormReady = true;

  /* shared helpers from code_chrome.md (parsed earlier — topbar include) */
  var escapeHtml  = window.lcEscapeHtml;
  var prettifyKey = window.lcPrettifyKey;
  var loadAgGrid  = window.lcAgGridReady;
  var parseDatagridText = window.lcParseDataText;

  function buildFormWrapper(opts) {
    var div = document.createElement("div");
    div.className = "lc-form";
    if (opts.id) div.id = "lc-form-" + opts.id;
    if (opts.id) div.setAttribute("data-lc-id", opts.id);
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

    /* publish the live object on the wrapper so Python (Form.field) can read it */
    function _publishFormValue() {
      var w = bodyEl.closest(".lc-form");
      if (w) { try { w.setAttribute("data-lc-value", JSON.stringify(obj)); } catch (e) {} }
    }
    _publishFormValue();

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
          _publishFormValue();
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
    var bound = el.getAttribute("master") || el.getAttribute("bound") || "";
    var editable = el.getAttribute("editable") === "true";
    var id = el.id || ("frm" + (++FORM_ID));

    /* source="file:path" loads one object from a repo file */
    var source = el.getAttribute("source") || "";
    var fileRef = source.indexOf("file:") === 0 ? source.slice(5).trim() : "";
    if (fileRef) {
      var fileFmt = window.lcInferFormat(fileRef, el.getAttribute("format"));
      var fileCdn = window.lcUseCdn();
      var srcs = window.lcFileSrc(fileRef);
      var fwrap = buildFormWrapper({ id: id, title: title || fileRef, format: "", mode: fileCdn ? "cdn" : "live" });
      el.parentNode.replaceChild(fwrap, el);
      var fbody = fwrap.querySelector(".lc-form-body");
      fetch(fileCdn ? srcs.cdn : srcs.raw)
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + fileRef); return r.text(); })
        .then(function (text) { return parseDatagridText(text, fileFmt); })
        .then(function (obj) { renderFormBody(fbody, obj, { editable: editable }); })
        .catch(function (e) { fbody.innerHTML = '<div class="lc-form-err">' + escapeHtml(e.message || String(e)) + '</div>'; });
      return;
    }

    var wrapper = buildFormWrapper({ id: id, title: title || "Form", format: bound ? "" : format });
    if (bound) wrapper.setAttribute("data-bound", bound);
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

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry
     and the shared helpers aliased above. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.form, pre.form", upgradeForm);
    window.lcRegisterUpgrader("div.lc-form-src", upgradeFormFile);
  }

})();
</script>
