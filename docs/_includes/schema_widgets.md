<!-- © 2026 KarmicSoft — LightCode Platform. Proprietary, All Rights Reserved. License: /license -->
{%- comment -%}
lcSchema — schema → typed widgets. Not a component (registers no upgrader);
exposes window.lcSchema. Renders an editable form for a record from a schema
array; mutations write straight into the record object and call onChange.

  window.lcSchema.buildForm(container, record, schema, index, onChange)
     schema : [{ name, label, widget, ... }]  widgets:
              string · text(rows) · number · boolean · select(options[]) · list ·
              relation(collection, multiple) · object(fields[]) · objectlist(fields[])
     index  : { collection: [{ slug, title, ... }] }  — for relation autocomplete
     onChange(): called after any edit (light) or structural change (rebuild)
     → returns { render, record }

  window.lcSchema.relTitle(index, coll, slug) / .matchRel(index, coll, q, excl)

Domain-agnostic: no field names, collections, or vocab baked in — the schema and
index are supplied by the caller. Lifted from the docs/paris PoC engine.
Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-sch-field { margin-bottom: 0.9em; }
.lc-sch-field > label { display: block; font-weight: 600; margin-bottom: 0.25em; }
.lc-sch-field .lc-sch-hint { font-weight: 400; color: #999; font-size: 0.82em; }
.lc-sch-field input[type=text], .lc-sch-field select, .lc-sch-field textarea { width: 100%; box-sizing: border-box; padding: 0.4em 0.55em; border: 1px solid #ccc; border-radius: 5px; font: inherit; }
.lc-sch-field textarea { resize: vertical; }
.lc-sch-listrow { display: flex; gap: 0.4em; margin-bottom: 0.35em; }
.lc-sch-listrow input { flex: 1; }
.lc-sch-x { border: none; background: #f2f2f2; border-radius: 5px; cursor: pointer; padding: 0 0.6em; font: inherit; }
.lc-sch-add { border: 1px dashed #bbb; background: #fafafa; border-radius: 5px; cursor: pointer; padding: 0.3em 0.7em; font-size: 0.85em; }
.lc-sch-chips { display: flex; flex-wrap: wrap; gap: 0.35em; margin-bottom: 0.4em; }
.lc-sch-chip { background: #eef4ff; border: 1px solid #cfe0ff; border-radius: 14px; padding: 0.15em 0.6em; font-size: 0.85em; }
.lc-sch-chip button { border: none; background: transparent; cursor: pointer; color: #667; margin-left: 0.3em; }
.lc-sch-group { border-left: 3px solid #e3e3e3; padding-left: 0.8em; margin: 0.2em 0; }
.lc-sch-item { border: 1px solid #eee; border-radius: 6px; padding: 0.6em 0.8em; margin-bottom: 0.5em; }
.lc-sch-item-hd { display: flex; justify-content: space-between; align-items: center; font-weight: 600; color: #556; font-size: 0.82em; margin-bottom: 0.4em; }
.lc-sch-suggest { border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 0.2em; overflow: hidden; }
.lc-sch-suggest:empty { display: none; }
.lc-sch-sug { padding: 0.45em 0.6em; cursor: pointer; border-bottom: 1px solid #f0f0f0; }
.lc-sch-sug:last-child { border-bottom: none; }
.lc-sch-sug:hover, .lc-sch-sug:active { background: #eef4ff; }
.lc-sch-sug-empty { padding: 0.45em 0.6em; color: #c0392b; font-size: 0.85em; }
</style>

<script>
(function () {
  if (window.lcSchema) return;
  "use strict";

  function el(t, c) { var e = document.createElement(t); if (c) e.className = c; return e; }
  function txt(s) { return document.createTextNode(s); }
  function isArr(v) { return Object.prototype.toString.call(v) === "[object Array]"; }
  function isObj(v) { return v && typeof v === "object" && !isArr(v); }
  function norm(s) { s = (s || "").toLowerCase().trim(); return s.normalize ? s.normalize("NFD").replace(new RegExp("[\\u0300-\\u036f]", "g"), "") : s; }

  function relTitle(index, coll, slug) { var a = (index && index[coll]) || [], i; for (i = 0; i < a.length; i++) if (a[i].slug === slug) return a[i].title; return slug; }
  function matchRel(index, coll, q, exclude) {
    var a = (index && index[coll]) || [], n = norm(q); exclude = exclude || [];
    if (!n) return [];
    var starts = [], incl = [], i, p, t;
    for (i = 0; i < a.length; i++) {
      p = a[i]; if (exclude.indexOf(p.slug) !== -1) continue;
      t = norm(p.title);
      if (t.indexOf(n) === 0 || p.slug.indexOf(n) === 0) starts.push(p);
      else if (t.indexOf(n) !== -1 || p.slug.indexOf(n) !== -1) incl.push(p);
    }
    return starts.concat(incl).slice(0, 8);
  }

  function buildField(obj, fd, ctx) {
    var wrap = el("div", "lc-sch-field"), lab = el("label");
    lab.appendChild(txt(fd.label || fd.name));
    if (fd.hint) { var h = el("span", "lc-sch-hint"); h.appendChild(txt(" — " + fd.hint)); lab.appendChild(h); }
    wrap.appendChild(lab); wrap.appendChild(ctrlFor(obj, fd, ctx)); return wrap;
  }
  function ctrlFor(obj, fd, ctx) {
    var w = fd.widget;
    if (w === "string") return strCtrl(obj, fd, ctx);
    if (w === "text") return textCtrl(obj, fd, ctx);
    if (w === "number") return numCtrl(obj, fd, ctx);
    if (w === "boolean") return boolCtrl(obj, fd, ctx);
    if (w === "select") return selCtrl(obj, fd, ctx);
    if (w === "list") return listCtrl(obj, fd, ctx);
    if (w === "relation") return relCtrl(obj, fd, ctx);
    if (w === "object") return objCtrl(obj, fd, ctx);
    if (w === "objectlist") return objListCtrl(obj, fd, ctx);
    return txt("(unknown widget: " + w + ")");
  }

  function strCtrl(obj, fd, ctx) {
    var i = el("input"); i.type = "text"; i.value = obj[fd.name] != null ? obj[fd.name] : "";
    i.oninput = function () { obj[fd.name] = i.value; ctx.change(); };
    return i;
  }
  function numCtrl(obj, fd, ctx) {
    var i = el("input"); i.type = "text"; i.setAttribute("inputmode", "numeric");
    i.value = obj[fd.name] == null ? "" : obj[fd.name];
    i.oninput = function () {
      var v = i.value.trim();
      if (v === "") delete obj[fd.name];
      else { var n = Number(v); obj[fd.name] = isNaN(n) ? v : n; }
      ctx.change();
    };
    return i;
  }
  function textCtrl(obj, fd, ctx) {
    var t = el("textarea"); t.rows = fd.rows || 4;
    t.value = obj[fd.name] != null ? obj[fd.name] : "";
    t.oninput = function () { obj[fd.name] = t.value; ctx.change(); };
    return t;
  }
  function boolCtrl(obj, fd, ctx) {
    var c = el("input"); c.type = "checkbox"; c.checked = !!obj[fd.name];
    c.onchange = function () { obj[fd.name] = c.checked; ctx.change(); };
    return c;
  }
  function selCtrl(obj, fd, ctx) {
    var s = el("select"), j, opts = fd.options || [];
    for (j = 0; j < opts.length; j++) {
      var op = el("option"); op.value = opts[j];
      op.textContent = opts[j] === "" ? "—" : opts[j];
      if ((obj[fd.name] || "") === opts[j]) op.selected = true;
      s.appendChild(op);
    }
    s.onchange = function () { if (s.value === "") delete obj[fd.name]; else obj[fd.name] = s.value; ctx.change(); };
    return s;
  }
  function listCtrl(obj, fd, ctx) {
    if (!isArr(obj[fd.name])) obj[fd.name] = [];
    var box = el("div");
    obj[fd.name].forEach(function (val, idx) {
      var row = el("div", "lc-sch-listrow"), i = el("input");
      i.type = "text"; i.value = val;
      i.oninput = function () { obj[fd.name][idx] = i.value; ctx.change(); };
      i.onchange = function () { obj[fd.name][idx] = i.value.trim(); i.value = obj[fd.name][idx]; ctx.change(); };
      var x = el("button", "lc-sch-x"); x.type = "button"; x.appendChild(txt("×"));
      x.onclick = function () { obj[fd.name].splice(idx, 1); ctx.rebuild(); };
      row.appendChild(i); row.appendChild(x); box.appendChild(row);
    });
    var add = el("button", "lc-sch-add"); add.type = "button"; add.appendChild(txt("＋ add"));
    add.onclick = function () { obj[fd.name].push(""); ctx.rebuild(); };
    box.appendChild(add); return box;
  }
  function relChipNode(ctx, coll, slug, onRemove) {
    var c = el("span", "lc-sch-chip"); c.appendChild(txt(relTitle(ctx.index, coll, slug)));
    var b = el("button"); b.type = "button"; b.appendChild(txt("×")); b.onclick = onRemove;
    c.appendChild(b); return c;
  }
  function suggestBox(ctx, coll, exclude, onPick) {
    var box = el("div"), row = el("div", "lc-sch-listrow"), i = el("input");
    i.type = "text"; i.setAttribute("autocomplete", "off"); i.placeholder = "Search “" + coll + "” by name…";
    var add = el("button", "lc-sch-add"); add.type = "button"; add.appendChild(txt("＋"));
    row.appendChild(i); row.appendChild(add); box.appendChild(row);
    var sug = el("div", "lc-sch-suggest"); box.appendChild(sug);
    function draw() {
      var q = i.value, m = matchRel(ctx.index, coll, q, exclude); sug.innerHTML = "";
      if (!q.trim()) return;
      if (!m.length) { var e = el("div", "lc-sch-sug-empty"); e.appendChild(txt("✗ no match “" + q.trim() + "”")); sug.appendChild(e); return; }
      m.forEach(function (p) {
        var d = el("div", "lc-sch-sug"); d.appendChild(txt(p.title));
        d.onmousedown = function (ev) { ev.preventDefault(); onPick(p); };
        sug.appendChild(d);
      });
    }
    i.oninput = draw;
    i.onkeydown = function (e) { if (e.key === "Enter" || e.keyCode === 13) { e.preventDefault(); var m = matchRel(ctx.index, coll, i.value, exclude); if (m.length) onPick(m[0]); } };
    add.onclick = function () { var m = matchRel(ctx.index, coll, i.value, exclude); if (m.length) onPick(m[0]); };
    return box;
  }
  function relCtrl(obj, fd, ctx) {
    var coll = fd.collection, box = el("div");
    if (fd.multiple) {
      if (!isArr(obj[fd.name])) obj[fd.name] = [];
      var chips = el("div", "lc-sch-chips");
      obj[fd.name].forEach(function (slug) {
        chips.appendChild(relChipNode(ctx, coll, slug, function () { var k = obj[fd.name].indexOf(slug); if (k !== -1) obj[fd.name].splice(k, 1); ctx.rebuild(); }));
      });
      box.appendChild(chips);
      box.appendChild(suggestBox(ctx, coll, obj[fd.name], function (p) { if (obj[fd.name].indexOf(p.slug) === -1) obj[fd.name].push(p.slug); ctx.rebuild(); }));
    } else if (obj[fd.name]) {
      var chips2 = el("div", "lc-sch-chips");
      chips2.appendChild(relChipNode(ctx, coll, obj[fd.name], function () { delete obj[fd.name]; ctx.rebuild(); }));
      box.appendChild(chips2);
    } else {
      box.appendChild(suggestBox(ctx, coll, [], function (p) { obj[fd.name] = p.slug; ctx.rebuild(); }));
    }
    return box;
  }
  function objCtrl(obj, fd, ctx) {
    if (!isObj(obj[fd.name])) obj[fd.name] = {};
    var g = el("div", "lc-sch-group"), i, flds = fd.fields || [];
    for (i = 0; i < flds.length; i++) g.appendChild(buildField(obj[fd.name], flds[i], ctx));
    return g;
  }
  function objListCtrl(obj, fd, ctx) {
    if (!isArr(obj[fd.name])) obj[fd.name] = [];
    var box = el("div"), flds = fd.fields || [];
    obj[fd.name].forEach(function (item, idx) {
      if (!isObj(item)) { item = {}; obj[fd.name][idx] = item; }
      var g = el("div", "lc-sch-group lc-sch-item"), hd = el("div", "lc-sch-item-hd");
      hd.appendChild(txt((fd.label || fd.name) + " " + (idx + 1)));
      var x = el("button", "lc-sch-x"); x.type = "button"; x.appendChild(txt("×"));
      x.onclick = function () { obj[fd.name].splice(idx, 1); ctx.rebuild(); };
      hd.appendChild(x); g.appendChild(hd);
      for (var k = 0; k < flds.length; k++) g.appendChild(buildField(item, flds[k], ctx));
      box.appendChild(g);
    });
    var add = el("button", "lc-sch-add"); add.type = "button"; add.appendChild(txt("＋ add " + (fd.label || fd.name || "item")));
    add.onclick = function () { obj[fd.name].push({}); ctx.rebuild(); };
    box.appendChild(add); return box;
  }

  function buildForm(container, record, schema, index, onChange) {
    var ctx = { index: index || {}, onChange: onChange || function () {} };
    ctx.change = function () { ctx.onChange(); };            // value edit — DOM stays
    ctx.rebuild = function () { render(); ctx.onChange(); }; // structural — rebuild form
    function render() {
      container.innerHTML = "";
      for (var i = 0; i < (schema || []).length; i++) container.appendChild(buildField(record, schema[i], ctx));
    }
    render();
    return { render: render, record: record };
  }

  window.lcSchema = { buildForm: buildForm, relTitle: relTitle, matchRel: matchRel };
})();
</script>
