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

compute="photo = 'https://…?id=' + str(pic)" — ƒ fields the card derives from
the row it shows (same spelling as the grid's ƒ columns, "col = expr; …"),
evaluated in the page runtime. The row it reads stays as it is: the table a
card follows never grows a column it was not asked for.

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
.lc-form-title .lc-form-meta { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: var(--lc-ink-mute, #616161); letter-spacing: 0.05em; }
.lc-form-grid { width: 100%; position: relative; }
/* a form is a narrow thing — often beside a datagrid: half the theme's padding */
.lc-form-grid.ag-theme-alpine { --ag-cell-horizontal-padding: 12px; }
.lc-form-grip { position: absolute; top: 0; bottom: 0; width: 7px; cursor: col-resize; z-index: 3; touch-action: none; }
.lc-form-grip:hover, .lc-form-grip.lc-form-grip-on { background: linear-gradient(90deg, transparent 2px, #0066cc 2px, #0066cc 4px, transparent 4px); }
.lc-form-grid .ag-cell.lc-form-label-cell { color: #0066cc; font-weight: 600; background: #fafbfc; }
/* a required value left blank: marked, never refused on sight */
.lc-form-grid .ag-cell.lc-form-missing { background: #fff7ed; box-shadow: inset 3px 0 #f59e0b; }
.lc-form-grid .ag-cell.lc-form-label-cell:hover { background: #fafbfc !important; }
.lc-form-grid .ag-row-hover .lc-form-label-cell { background: #fafbfc !important; }
.lc-form-bool { display: flex; align-items: center; gap: 0.5em; height: 100%; }
.lc-form-refpick { display: flex; align-items: center; height: 100%; cursor: pointer; gap: .4em; }
.lc-form-refpick .lc-form-refval { flex: 1; }
.lc-form-refpick .lc-form-refcaret { color: var(--lc-ink-mute, #616161); }
.lc-form-refpick:hover .lc-form-refcaret, .lc-form-refpick:focus-visible .lc-form-refcaret { color: #0066cc; }
.lc-form-bool .lc-form-bool-cb { margin: 0; accent-color: #0066cc; cursor: pointer; }
.lc-form-bool .lc-form-bool-cb:disabled { cursor: default; }
.lc-form-bool .lc-form-bool-t { color: #2a7a2a; font-weight: 600; }
.lc-form-bool .lc-form-bool-f { color: #b00; font-weight: 600; }
.lc-form-null { color: #aaa; font-style: italic; }
.lc-form-num { color: #087a40; }
.lc-form-cellbox { display: flex; align-items: center; height: 100%; overflow: hidden; }
.lc-form-grid .ag-cell-wrap-text { line-height: 1.5; padding-top: 6px; padding-bottom: 6px; word-break: normal; }
.lc-form-pills { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; line-height: 1.2; padding: 4px 0; }
.lc-form-pill { display: inline-flex; align-items: center; padding: 1px 9px; border-radius: 12px; background: #e7f1fe; color: #1756a9; font-size: 0.82em; border: 1px solid #c5dcf5; white-space: nowrap; line-height: 1.4; }
.lc-form-selectbox { display: inline-flex; align-items: center; gap: 0.4em; padding: 0 8px 0 10px; border: 1px solid #c5dcf5; background: #f5f9ff; border-radius: 4px; color: #1756a9; font-size: 0.88em; line-height: 1.7; max-width: 100%; box-sizing: border-box; }
.lc-form-selectbox-label { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lc-form-selectbox-arrow { color: #6892c4; font-size: 0.85em; }
.lc-form-empty { padding: 0.9em 1em; color: var(--lc-ink-mute, #616161); font-style: italic; font-size: 0.9em; }
.lc-form-err { padding: 0.9em 1em; color: #b00; background: #fff5f5; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; white-space: pre-wrap; }
.lc-form-verbs { display: flex; flex-wrap: wrap; gap: .4em; padding: .5em .75em .6em; border-top: 1px solid #eee; }
/* the verbs wear the page's action blue — Save, ▶ Run, ➕ New — one family
   of buttons (Michel, 2026-10-16: "elegant and homogeneous"); a verb the
   stage forbids is a quiet grey */
.lc-form-verb { font: inherit; font-size: .85em; font-weight: 500; padding: .35em 1em; border-radius: 6px; border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; }
.lc-form-verb:hover { background: #0052a3; border-color: #0052a3; }
.lc-form-verb.lc-form-verb-off { border-color: #e5e7eb; background: #f3f4f6; color: #9ca3af; cursor: default; }
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

  /* the width a label needs, in the label cell's own font (bold, the grid's size) */
  var _measure = null;
  function textWidth(text, el) {
    _measure = _measure || document.createElement("canvas").getContext("2d");
    var cs = getComputedStyle(el);
    _measure.font = "600 " + (cs.fontSize || "14px") + " " + (cs.fontFamily || "sans-serif");
    return _measure.measureText(String(text || "")).width;
  }

  /* THE GRIP: the form has no header row, so AG Grid's own resize handle never
     shows. A thin bar on the line between label and value drags it; once
     dragged, the learner's width holds, row after row — otherwise the column
     re-fits when the form changes width (a pad's preview, a phone turned). */
  function wireLabelGrip(gridDiv, api, keep) {
    var grip = document.createElement("div");
    grip.className = "lc-form-grip";
    grip.title = "Drag to resize the labels";
    gridDiv.appendChild(grip);
    /* the learner's width outlives the row: a card that follows a datagrid
       repaints on every click, and the line stays where they dragged it */
    var mine = !!keep._lcLabelW;
    if (mine) api.setColumnWidths([{ key: "label", newWidth: keep._lcLabelW }]);
    function width() { var c = api.getColumn("label"); return c ? c.getActualWidth() : 0; }
    function place() { grip.style.left = (width() - 3) + "px"; }
    /* the canvas guess sized the first paint; the rendered cells have the
       last word — AG Grid fits the column to them, the cap still holds */
    function refit() {
      if (mine) return;
      api.autoSizeColumns(["label"], true);
      var cap = Math.max(60, gridDiv.clientWidth * 0.5);
      if (width() > cap) api.setColumnWidths([{ key: "label", newWidth: cap }]);
      place();
    }
    api.addEventListener("columnResized", place);
    api.addEventListener("firstDataRendered", refit);
    api.addEventListener("rowDataUpdated", refit);
    setTimeout(refit, 0);              /* the first render may already be done */
    grip.addEventListener("pointerdown", function (ev) {
      ev.preventDefault();
      var x0 = ev.clientX, w0 = width();
      grip.setPointerCapture(ev.pointerId);
      grip.classList.add("lc-form-grip-on");
      function move(e) {
        var max = Math.max(60, gridDiv.clientWidth - 40);
        keep._lcLabelW = Math.max(40, Math.min(max, w0 + e.clientX - x0));
        api.setColumnWidths([{ key: "label", newWidth: keep._lcLabelW }]);
        mine = true;
      }
      function up() {
        grip.classList.remove("lc-form-grip-on");
        grip.removeEventListener("pointermove", move);
        grip.removeEventListener("pointerup", up);
        grip.removeEventListener("pointercancel", up);
      }
      grip.addEventListener("pointermove", move);
      grip.addEventListener("pointerup", up);
      grip.addEventListener("pointercancel", up);
    });
    if (window.ResizeObserver) {
      var lastW = gridDiv.clientWidth;
      new ResizeObserver(function () {
        if (mine || !gridDiv.isConnected || gridDiv.clientWidth === lastW) return;
        lastW = gridDiv.clientWidth;
        refit();
      }).observe(gridDiv);
    }
  }

  function buildFormWrapper(opts) {
    var div = document.createElement("div");
    div.className = "lc-form";
    if (opts.id) div.id = "lc-form-" + opts.id;
    if (opts.id) div.setAttribute("data-lc-id", opts.id);
    var meta = "";
    if (opts.mode) meta = '<span class="lc-form-meta" style="font-style:italic; text-transform:none;">' + escapeHtml(opts.mode) + '</span>';
    else if (opts.format) meta = '<span class="lc-form-meta">' + escapeHtml(opts.format) + '</span>';
    var html = '<div class="lc-form-title">☷ <span class="lc-form-name">' + escapeHtml(opts.title || "Form") + '</span>' + meta + '</div>';
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

  /* a URL that IS a picture: an image extension, or an image-ish field name
     (photo/image/pic/avatar) — URL APIs like placedog carry no extension */
  function isImageValue(key, v) {
    return typeof v === "string" && /^https?:\/\//i.test(v) &&
      (/\.(png|jpe?g|gif|webp|svg|avif)([?#]|$)/i.test(v) ||
       /photo|image|pic|avatar/i.test(key || ""));
  }

  function makeFormCellRenderer(opts) {
    return function(params) {
      var t = params.data._type;
      var v = params.value;

      /* photo: an image URL shows the picture itself, not the string —
         a detail view earns its name (Adoption Day, 2026-07-31) */
      if (isImageValue(params.data._key, v)) {
        var im = document.createElement("img");
        im.src = v;
        im.alt = params.data._key || "photo";
        im.style.maxHeight = "96px";
        im.style.maxWidth = "100%";
        im.style.borderRadius = "6px";
        im.style.margin = "4px 0";
        return im;
      }

      /* gauge: a numeric field named in sliders="…" renders as a range input */
      var slid = opts.sliders && opts.sliders[params.data._key];
      if (slid) {
        var sw = document.createElement("div");
        sw.className = "lc-form-bool";
        var rng = document.createElement("input");
        rng.type = "range";
        rng.min = slid.min; rng.max = slid.max; rng.step = slid.step;
        rng.value = (v === null || v === undefined || isNaN(Number(v))) ? slid.min : v;
        rng.setAttribute("aria-label", String(params.data._key || "value"));
        rng.disabled = !opts.editable;
        rng.style.flex = "1";
        var rl = document.createElement("span");
        rl.className = "lc-form-num";
        rl.textContent = rng.value;
        if (opts.editable) {
          // keep the grid from hijacking the drag (row-select / cell focus)
          rng.addEventListener("mousedown", function (e) { e.stopPropagation(); });
          rng.addEventListener("touchstart", function (e) { e.stopPropagation(); }, { passive: true });
          rng.addEventListener("click", function (e) { e.stopPropagation(); });
          // update the label live while dragging, but only COMMIT on release —
          // committing on every input re-renders the cell and breaks the drag
          rng.addEventListener("input", function () { rl.textContent = rng.value; });
          rng.addEventListener("change", function () { params.node.setDataValue("value", Number(rng.value)); });
        }
        sw.appendChild(rng);
        sw.appendChild(rl);
        return sw;
      }

      /* a reference (a walk's dog): the value, a ⌄, the grid's own picklist
         (Michel, 2026-10-18: "in the form, the picklist for dogs is the old style") */
      var rp = opts.refs && opts.refs[params.data._key];
      if (rp && opts.editable && window.lcPickMenu) {
        var rw = document.createElement("div");
        rw.className = "lc-form-refpick";
        rw.setAttribute("role", "button");
        rw.setAttribute("tabindex", "0");
        rw.setAttribute("aria-label", "pick " + String(params.data._key || "value"));
        rw.innerHTML = "<span class='lc-form-refval'></span><span class='lc-form-refcaret'>⌄</span>";
        rw.firstChild.textContent = v == null ? "" : String(v);
        var openPick = function (e) {
          e.stopPropagation();
          window.lcPickMenu(rw, rp.map(function (n) { return { v: n, label: n, cur: n === String(v) }; }),
            function (n) { params.node.setDataValue("value", n); });
        };
        rw.addEventListener("mousedown", function (e) { e.stopPropagation(); });
        rw.addEventListener("click", openPick);
        rw.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openPick(e); } });
        return rw;
      }

      /* pick list: a field named in options="field=a|b|c" renders as a dropdown */
      var picks = opts.options && opts.options[params.data._key];
      if (picks) {
        var pw = document.createElement("div");
        pw.className = "lc-form-bool";
        var sel = document.createElement("select");
        sel.className = "lc-form-select";
        sel.setAttribute("aria-label", String(params.data._key || "value"));
        sel.disabled = !opts.editable;
        sel.style.flex = "1";
        if (picks.indexOf(String(v)) < 0) {
          var ph = document.createElement("option");
          ph.value = ""; ph.textContent = (v == null || v === "") ? "— pick —" : String(v);
          sel.appendChild(ph);
        }
        picks.forEach(function (o) {
          var op = document.createElement("option");
          op.value = o; op.textContent = o;
          if (String(v) === o) op.selected = true;
          sel.appendChild(op);
        });
        if (opts.editable) {
          sel.addEventListener("mousedown", function (e) { e.stopPropagation(); });
          sel.addEventListener("click", function (e) { e.stopPropagation(); });
          sel.addEventListener("change", function () { params.node.setDataValue("value", sel.value); });
        }
        pw.appendChild(sel);
        return pw;
      }

      if (t === "boolean") {
        var w = document.createElement("div");
        w.className = "lc-form-bool";
        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.checked = !!v;
        cb.disabled = !opts.editable;
        cb.className = "lc-form-bool-cb";
        cb.setAttribute("aria-label", String(params.data._key || "value"));
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

      /* a state reads as a chip, as in the grid */
      if (opts.chips && opts.chips.indexOf(params.data._key) >= 0) {
        var ch = document.createElement("span");
        ch.className = "lc-dg-chip";
        ch.textContent = (v == null ? "" : String(v));
        return ch;
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
        arrow.setAttribute("aria-hidden", "true");   /* decoration: the label names the field */
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

  // Fence-embedded per-field config: a field whose value is a config object —
  // {value, min, max, step} for a slider, or {value, options: [...]} for a
  // pick-list — declares its own widget, so no sliders=/options= attribute is
  // needed and the field + its range live together once. Pull the scalar into
  // obj[k] and fold the config into the slider/option maps. Runs before
  // store-over-seed so the config survives a persisted scalar. The attributes
  // stay a fallback and win for fields not declared in the fence.
  var _CFG_KEYS = { value: 1, min: 1, max: 1, step: 1, options: 1 };
  function extractFieldConfig(obj, opts) {
    opts.sliders = opts.sliders || {};
    opts.options = opts.options || {};
    Object.keys(obj).forEach(function (k) {
      var v = obj[k];
      if (!v || typeof v !== "object" || Array.isArray(v)) return;
      var ks = Object.keys(v);
      if (!ks.length || !ks.every(function (kk) { return _CFG_KEYS[kk]; })) return;  // a real object, leave it
      if (Array.isArray(v.options)) opts.options[k] = v.options.map(String);
      if (("min" in v) || ("max" in v) || ("step" in v)) {
        opts.sliders[k] = {
          min:  v.min  != null ? parseFloat(v.min)  : 0,
          max:  v.max  != null ? parseFloat(v.max)  : 100,
          step: v.step != null ? parseFloat(v.step) : 1
        };
      }
      obj[k] = ("value" in v) ? v.value
             : opts.sliders[k] ? opts.sliders[k].min
             : opts.options[k] ? opts.options[k][0]
             : "";
    });
  }

  /* the object's verbs under its card: a transition is live when the
     object's state is in its pre, grey (and says what it needs) otherwise */
  function renderVerbs(bodyEl, model, row, cls, objName) {
    var old = bodyEl.parentNode.querySelector(".lc-form-verbs");
    if (old) old.parentNode.removeChild(old);
    var cur = String(row[model.state] == null ? "" : row[model.state]);
    var bar = document.createElement("div");
    bar.className = "lc-form-verbs";
    var items = [];
    Object.keys(model.transitions).forEach(function (n) {
      var t = model.transitions[n], ok = !t.pre.length || t.pre.indexOf(cur) >= 0;
      items.push({ n: n, ok: ok, hint: ok ? "→ " + (t.post || cur) : "needs " + t.pre.join(" / ") });
    });
    model.verbs.forEach(function (n) { items.push({ n: n, ok: true, hint: "" }); });
    items.forEach(function (it) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "lc-form-verb" + (it.ok ? "" : " lc-form-verb-off");
      var dd = window.lcDocOf ? window.lcDocOf(cls, it.n) : null;   /* its docstring's icon and words */
      b.textContent = (dd && dd.icon ? dd.icon + " " : "") + prettifyKey(it.n);
      b.title = (dd && dd.text) || it.hint;
      b.addEventListener("click", function () {
        if (!it.ok) { if (window.lcGridSay) window.lcGridSay(cls, "⛔ " + it.n + " " + it.hint); return; }
        if (window.lcModelOp) window.lcModelOp(cls, { t: "verb", obj: String(objName), verb: it.n },
          "_lc_verb(" + JSON.stringify(cls) + "," + JSON.stringify(objName) + "," + JSON.stringify(it.n) + ")");
      });
      bar.appendChild(b);
    });
    bodyEl.parentNode.appendChild(bar);
    bodyEl.parentNode.setAttribute("data-lc-say", cls);   /* a verb's refusal or error is said here too */
  }

  /* what the card's grid was built for: the same fields under the same
     rules reuse it, only the values change */
  function formSig(obj, opts) {
    var o = opts || {};
    return JSON.stringify([Object.keys(obj), !!o.editable, o.locked || [], o.chips || [],
      o.options ? Object.keys(o.options) : [], o.sliders ? Object.keys(o.sliders) : [], o.refs || {}, o.required || []]);
  }
  /* a required attribute wears ✱ on its label, and its blank value is marked
     (Michel, 2026-10-24: "go required") */
  function labelOf(k, opts) { return prettifyKey(k) + ((opts && opts.required || []).indexOf(k) >= 0 ? " ✱" : ""); }
  function renderFormBody(bodyEl, obj, opts) {
    opts = opts || {};
    /* A NEW ROW, THE SAME CARD (Michel, 2026-10-16: "changing lines in the
       grid is too slow — it rebuilds the form?"): it did, a whole grid per
       click. The same fields under the same rules now keep the grid and only
       swap its values; the handlers read the current object. */
    if (bodyEl._lcGridApi && obj && typeof obj === "object" && !Array.isArray(obj) && !opts.persist
        && bodyEl._lcSig === formSig(obj, opts) && bodyEl.querySelector(".lc-form-grid")) {
      bodyEl._lcCur = { obj: obj, opts: opts };
      var api0 = bodyEl._lcGridApi, rows0 = Object.keys(obj).map(function (k) {
        return { _key: k, label: labelOf(k, opts), value: obj[k], _type: typeOfValue(obj[k]) };
      });
      if (api0.setGridOption) api0.setGridOption("rowData", rows0); else api0.setRowData(rows0);
      var w0 = bodyEl.closest(".lc-form");
      if (w0) { try { w0.setAttribute("data-lc-value", JSON.stringify(obj)); } catch (e) {} }
      return;
    }
    bodyEl._lcCur = { obj: obj, opts: opts };
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
    extractFieldConfig(obj, opts);   // fence-declared slider/option config → maps (before store override)
    /* Store-over-seed: a persisted field the learner has set overrides its
       design-time default; unset fields keep the seed. */
    if (opts.persist && opts.formId && window.lcStore) {
      Object.keys(obj).forEach(function (k) {
        var sv = window.lcStore.get(opts.persist + "." + opts.formId + "." + k);
        if (sv !== undefined) obj[k] = sv;
      });
    }
    var keys = Object.keys(obj);
    if (keys.length === 0) {
      bodyEl.innerHTML = '<div class="lc-form-empty">(empty object)</div>';
      return;
    }

    var rows = keys.map(function(k){
      return { _key: k, label: labelOf(k, opts), value: obj[k], _type: typeOfValue(obj[k]) };
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
    function labelWidth() {
      var longest = rows.reduce(function (m, r) { return Math.max(m, textWidth(r.label, gridDiv)); }, 0);
      var cap = Math.max(60, (gridDiv.clientWidth || 600) * 0.5);
      return Math.round(Math.min(cap, longest + 22));   /* the cell's own padding, both sides */
    }

    loadAgGrid().then(function(){
      var columnDefs = [
        {
          /* THE LABEL COLUMN FITS ITS LABELS (Michel, 2026-10-10: a form
             beside a datagrid showed labels only — a fixed 160px left the
             values 39). Sized to the longest label, never more than half of
             the form, and the learner drags the grip to move the line. */
          field: "label",
          colId: "label",
          headerName: "",
          editable: false,
          cellClass: "lc-form-label-cell",
          width: labelWidth(),
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
            if (opts.locked && opts.locked.indexOf(params.data._key) >= 0) return false;
            if (opts.sliders && opts.sliders[params.data._key]) return false; // slider handles it
            if (opts.options && opts.options[params.data._key]) return false; // dropdown handles it
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
          cellRenderer: cellRenderer,
          cellClassRules: { "lc-form-missing": function (p) {
            var o = (bodyEl._lcCur || {}).opts || {};
            return (o.required || []).indexOf(p.data._key) >= 0 && (p.value == null || String(p.value).trim() === "");
          } },
          /* a long value is a paragraph, not a peephole: wrap and let the
             row grow (Michel, 2026-08-21: "it should appear as a long
             text in the form: multiple lines") */
          wrapText: true,
          autoHeight: true
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

        onCellValueChanged: function(event) {
          var cur = bodyEl._lcCur || {}, obj = cur.obj || {}, opts = cur.opts || {};   /* the row shown NOW */
          var k = event.data._key;
          var nv = event.newValue;
          obj[k] = nv;
          // Re-derive type from the new value
          event.data._type = typeOfValue(nv);
          var wv = bodyEl.closest(".lc-form");
          if (wv) { try { wv.setAttribute("data-lc-value", JSON.stringify(obj)); } catch (e) {} }
          // persist the learner's edit to the browser Store (also fires the bus)
          if (opts.persist && opts.formId && window.lcStore) {
            window.lcStore.set(opts.persist + "." + opts.formId + "." + k, nv);
          }
          // A form is a live data source: announce the edit on the platform's
          // reactive bus so {= …} cells (and diagrams) recompute.
          try { document.dispatchEvent(new CustomEvent("lc-model-changed", { detail: { source: "form" } })); } catch (e) {}
          if (opts.onChange) opts.onChange(obj, k, nv);
        }
      };

      var api = bodyEl._lcGridApi = window.agGrid.createGrid(gridDiv, gridOptions);
      bodyEl._lcSig = formSig(obj, opts);
      wireLabelGrip(gridDiv, api, bodyEl);
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
    var format = (el.getAttribute("format") || (window.lcFenceFormat && window.lcFenceFormat(el)) || "yaml").toLowerCase();
    /* THE LINK NAMES THE CARD (Michel, 2026-10-11: "the form's title is Lucky.
       Why not 'The dog' as in the link?") — [The dog](#) titles the form the
       way [The dogs](#) titles the grid; the row's name only when nothing does */
    var link = !codeNode && el.querySelector ? el.querySelector("a") : null;
    var title = el.getAttribute("title") || (link ? (link.textContent || "").trim() : "");
    var bound = el.getAttribute("master") || el.getAttribute("bound") || "";
    var editable = el.getAttribute("editable") === "true";
    var editableSaid = el.getAttribute("editable");   /* a class-bound card edits unless told "false" */
    /* compute="photo = '…' + str(pic)" — the grid's formula engine on ONE
       row (datagrid.md, lcComputeRows), run on a COPY: the card derives,
       the row it follows is never written (Michel, 2026-10-06: the photo
       belongs on the card, not on the table). */
    var compute = el.getAttribute("compute") || "";
    function derive(obj) {
      if (!compute || !obj || typeof obj !== "object" || Array.isArray(obj) || !window.lcComputeRows)
        return Promise.resolve(obj);
      return window.lcComputeRows([Object.assign({}, obj)], compute)
        .then(function (rows) { return rows[0]; }, function () { return obj; });
    }
    var id = el.id || ("_frm" + (++FORM_ID));
    /* persist="true" -> keyed by this page's slug; persist="scope" -> a stable
       top segment (e.g. build_ai). Learner edits save to the Store under
       <scope>.<id>.<field>; seeds hydrate only where the Store is unset. */
    var persist = el.getAttribute("persist") || "";
    var persistScope = persist === "true"
      ? ((location.pathname.replace(/\/+$/, "").split("/").pop() || "index").replace(/\.html$/, ""))
      : persist;
    /* sliders="x,y" renders those numeric fields as range gauges (min/max/step) */
    var _smin = parseFloat(el.getAttribute("min")); if (isNaN(_smin)) _smin = 0;
    var _smax = parseFloat(el.getAttribute("max")); if (isNaN(_smax)) _smax = 100;
    var _sstep = parseFloat(el.getAttribute("step")); if (isNaN(_sstep)) _sstep = 1;
    // sliders="x,y" (shared min/max/step) or per-field "lat:43.05:43.09:0.005,lon:…"
    var slidersMap = {};
    (el.getAttribute("sliders") || "").split(",").forEach(function (f) {
      var p = f.trim().split(":"); var name = p[0].trim(); if (!name) return;
      slidersMap[name] = {
        min:  p.length > 1 ? parseFloat(p[1]) : _smin,
        max:  p.length > 2 ? parseFloat(p[2]) : _smax,
        step: p.length > 3 ? parseFloat(p[3]) : _sstep
      };
    });
    /* options="field=a|b|c; field2=x|y" renders those fields as pick-list dropdowns */
    var optionsMap = {};
    (el.getAttribute("options") || "").split(";").forEach(function (part) {
      var eq = part.indexOf("=");
      if (eq < 0) return;
      var f = part.slice(0, eq).trim();
      var os = part.slice(eq + 1).split("|").map(function (s) { return s.trim(); }).filter(Boolean);
      if (f && os.length) optionsMap[f] = os;
    });

    /* source="file:path" loads one object from a repo file */
    var source = el.getAttribute("source") || "";
    var fileRef = source.indexOf("file:") === 0 ? source.slice(5).trim() : "";
    if (fileRef) {
      var fileFmt = window.lcInferFormat(fileRef, el.getAttribute("format"));
      var fileCdn = window.lcUseCdn();
      var srcs = window.lcFileSrc(fileRef);
      var fwrap = buildFormWrapper({ id: id, title: title || fileRef, format: "", mode: fileCdn ? "cdn" : "live" });
      if (window.lcCarryCellKnobs) window.lcCarryCellKnobs(el, fwrap);
      el.parentNode.replaceChild(fwrap, el);
      var fbody = fwrap.querySelector(".lc-form-body");
      fetch(fileCdn ? srcs.cdn : srcs.raw)
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + fileRef); return r.text(); })
        .then(function (text) { return parseDatagridText(text, fileFmt); })
        .then(derive)
        .then(function (obj) { renderFormBody(fbody, obj, { editable: editable, persist: persistScope, formId: id, sliders: slidersMap, options: optionsMap }); })
        .catch(function (e) { fbody.innerHTML = '<div class="lc-form-err">' + escapeHtml(e.message || String(e)) + '</div>'; });
      return;
    }

    var wrapper = buildFormWrapper({ id: id, title: title || "Form", format: bound ? "" : format });
    if (bound) wrapper.setAttribute("data-bound", bound);
    if (window.lcCarryCellKnobs) window.lcCarryCellKnobs(el, wrapper);
    el.parentNode.replaceChild(wrapper, el);
    var body = wrapper.querySelector(".lc-form-body");

    if (bound) {
      body.innerHTML = '<div class="lc-form-empty">click a row in <code>#' + escapeHtml(bound) + '</code> to see details</div>';
      var turn = 0;   /* a derive still in flight never paints over a later click */
      window.lcMasterDetail.subscribe(bound, function(row){
        var mine = ++turn;
        var objName = row && row.obj != null ? String(row.obj) : "";
        if (!row) {
          renderFormBody(body, null);
          setFormTitle(wrapper, title || "Form");
          return;
        }
        /* the master is a grid on a CLASS (a class is a dataset): the row is
           an object — its verbs come as buttons under the card, live or grey
           by its state, and an edit goes through the object, not the row */
        var gridEl = document.querySelector(".lc-datagrid[data-lc-id='" + bound + "']");
        var cls = gridEl ? gridEl.getAttribute("data-bind") : "";
        var model = cls && row.obj != null ? (window.lcModels || {})[cls] : null;
        /* a subclass's object shows its own fields' rules and verbs */
        if (model && row._kind && (window.lcModels || {})[row._kind]) { cls = row._kind; model = window.lcModels[cls]; }
        var locked = [], chips = [], picks = {}, refs = {}, refNames = {}, required = [];
        if (model) {
          /* the object's card: the state LAST, as a chip, beside its verbs;
             locked and state fields read-only; enum fields pick lists; the
             rest editable through the object unless editable="false" */
          var copy = {};
          Object.keys(row).forEach(function (k) { if (k !== "obj" && k.charAt(0) !== "_" && k !== model.state && !(model.fields[k] && model.fields[k].hidden)) copy[k] = row[k]; });
          if (model.state && model.state in row) copy[model.state] = row[model.state];
          row = copy;
          Object.keys(model.fields).forEach(function (k) {
            var f = model.fields[k];
            if (f.ro || f.state) locked.push(k);
            if (f.req) required.push(k);
            /* a read-only datetime shows as the grid does: Oct 18 13:15 */
            if (f.t === "datetime" && f.ro && k in row && window.lcTimeShort) row[k] = window.lcTimeShort(row[k]);
            if (f.enum && !f.ro && !f.state) picks[k] = f.enum.map(String);
            /* a reference picks among its class's objects, by their names */
            if (f.ref) {
              var rr = (window.lcDatasets || {})[f.ref] || [], lab = window.lcRefLabel ? window.lcRefLabel(f.ref) : "obj";
              var nm = function (r) { return String(r[lab] != null && r[lab] !== "" ? r[lab] : r.obj); };
              refs[k] = {};
              rr.forEach(function (r) { refs[k][nm(r)] = String(r.obj); });
              var cur = rr.filter(function (r) { return String(r.obj) === String(row[k]); })[0];
              if (k in row) row[k] = cur ? nm(cur) : "";
              if (!f.ro) { picks[k] = [""].concat(Object.keys(refs[k])); refNames[k] = Object.keys(refs[k]); }
            }
          });
          if (model.state) chips.push(model.state);
        }
        /* no compute= → paint NOW, in the click's own tick: a check that
           clicks a row and reads the card at once found the previous row
           behind a promise (the Dataset page's card, red since 2026-10-08) */
        var paint = function (shown) {
          if (mine !== turn) return;
          renderFormBody(body, shown, {
            editable: model ? editableSaid !== "false" : editable,
            locked: locked, chips: chips, options: model ? picks : undefined, required: required,
            refs: model ? refNames : undefined,
            /* an edit lands on the master's own row (the shown object may be
               the derived copy), then the grid repaints */
            onChange: function(o, k, v){
              if (model && refs[k]) v = refs[k][v] || "";   /* a dog's name → the dog */
              if (model) { if (window.lcModelOp) window.lcModelOp(cls, { t: "set", obj: String(objName), col: k, val: v },
                "_lc_set(" + JSON.stringify(cls) + "," + JSON.stringify(String(objName)) + "," + JSON.stringify(k) + "," + JSON.stringify(v) + ")"); return; }
              if (shown !== row && k) row[k] = v;
              window.lcMasterDetail.refreshGrid(bound);
            }
          });
          setFormTitle(wrapper, title || inferFormTitle(shown) || "Form");
          if (model) renderVerbs(body, model, shown, cls, objName);
        };
        if (compute) derive(row).then(paint); else paint(row);
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
    dataPromise.then(derive).then(function(obj){
      renderFormBody(body, obj, { editable: editable, persist: persistScope, formId: id, sliders: slidersMap, options: optionsMap });
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
    var id = el.id || ("_frm" + (++FORM_ID));
    var wrapper = buildFormWrapper({ id: id, title: title || "Form", mode: useCdn ? "cdn" : "live" });
    if (window.lcCarryCellKnobs) window.lcCarryCellKnobs(el, wrapper);
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

  // Programmatic edit: set one field of a rendered form BY THE SAME PATH a
  // human edit takes (grid setDataValue → onCellValueChanged → model +
  // data-lc-value + lc-model-changed bus + persist). Used by .demo's ▶ Replay
  // to genuinely re-perform a recorded session. Returns true if applied.
  window.lcFormSet = function (formId, key, value) {
    var w = document.querySelector('.lc-form[data-lc-id="' + String(formId).replace(/"/g, '\\"') + '"]');
    var body = w && w.querySelector(".lc-form-body");
    var api = body && body._lcGridApi;
    if (!api) return false;
    var done = false;
    try {
      api.forEachNode(function (node) {
        if (!done && node.data && node.data._key === key) { node.setDataValue("value", value); done = true; }
      });
    } catch (e) { return false; }
    /* AG GRID DELIVERS onCellValueChanged A TICK LATER, so a caller that acts
       and then looks saw the old value and a gate that had not moved. That is
       what stopped a .feature from having a real When: the step set a field,
       the next step read the page, and nothing had changed yet (Michel,
       2026-08-06 — "the when step should change something the then would
       test"). Publish the same edit synchronously here. The grid's own handler
       repeats it with an identical object a moment later, which is harmless,
       and cells listen to lc-model-changed synchronously, so a gate has moved
       by the time this returns. */
    if (done) {
      try {
        var cur = JSON.parse(w.getAttribute("data-lc-value") || "{}");
        cur[key] = value;
        w.setAttribute("data-lc-value", JSON.stringify(cur));
        document.dispatchEvent(new CustomEvent("lc-model-changed",
                                               { detail: { source: "form" } }));
      } catch (e) {}
    }
    return done;
  };

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
    /* a link paragraph too — [The dog](#) + {: .form master="dog_grid" }: a
       card that follows a table has no words of its own, so it needs no
       fence (Michel, 2026-10-03: "keep simple things simple — the chart
       needs none, why would the form"). Same spelling as a chart or a grid. */
    window.lcRegisterUpgrader(".highlighter-rouge.form, pre.form, p.form", upgradeForm);
    window.lcRegisterUpgrader("div.lc-form-src", upgradeFormFile);
  }

})();
</script>
