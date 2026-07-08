{%- comment -%}
Cells — reactive spreadsheet cells for any page, activated from md + IAL.

A knob is a spreadsheet cell: it holds a literal, or a `= formula` — a Python
*expression* (never a statement: cells are eval'd, not exec'd) evaluated live
and re-run whenever its inputs change.

  python block + {: .cells }   the shared model — plain Python defs/consts,
                               exec'd once into an isolated page namespace.
                               Several blocks compose into the same namespace.

  {= expr }                    an inline cell anywhere in prose — replaced by
                               the value of `expr`, recomputed on every change.

  {: visible="= expr" }        any block shows only while `bool(expr)` is true —
                               `visible` is just another cell.

Inputs come from the page's editable forms: every {: .form } publishes its
object as JSON, and its keys are injected as variables in the cell namespace.
Editing a form fires `lc-model-changed`; the cells recompute. Nothing global is
touched — formulas can't reach the platform runtime, and a cyclic formula fails
*safe* (a value like "⚠ maximum recursion…", never a frozen page).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-cell { font-weight: 700; color: #0066cc; font-variant-numeric: tabular-nums; }
.lc-cell.lc-cell-err { color: #b91c1c; font-weight: 600; }
/* hidden until a cell decides — the .lc-vis-show class (set by JS) wins */
[visible^="="] { display: none; border-left: 3px solid #cde8cd; background: #fffdf5; padding: 6px 12px; border-radius: 6px; margin: 8px 0; }
[visible^="="].lc-vis-show { display: block !important; }
</style>

<script>
(function () {
  if (window._lcCellsReady) return;
  window._lcCellsReady = true;

  var NS = "_LC_CELL_NS";
  var mpReady = null;
  function mp() {
    if (!mpReady) {
      mpReady = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
        .then(function (m) { return m.loadMicroPython({ stdout: function () {}, stderr: function () {} }); });
    }
    return mpReady;
  }
  function run(m, code) { (m.runPython || m.exec || m.run).call(m, code); }

  var cells = [], vis = [], booted = false;

  /* Walk text for {= expr } and replace each with a live <span>. Code, the
     model listings and this page's script/style are left untouched. */
  function collect() {
    var root = document.querySelector("main") || document.body;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var hits = [], n;
    while ((n = walker.nextNode())) if (n.nodeValue.indexOf("{=") >= 0) hits.push(n);
    hits.forEach(function (t) {
      if (t.parentNode && t.parentNode.closest &&
          t.parentNode.closest("pre, code, script, style, .lc-cells-model")) return;
      var s = t.nodeValue, re = /\{=\s*([\s\S]*?)\s*\}/g, m, last = 0,
          frag = document.createDocumentFragment(), any = false;
      while ((m = re.exec(s))) {
        any = true;
        if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
        var sp = document.createElement("span");
        sp.className = "lc-cell";
        sp.setAttribute("data-expr", m[1]);
        sp.textContent = "…";
        frag.appendChild(sp); cells.push(sp); last = re.lastIndex;
      }
      if (!any) return;
      if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
      t.parentNode.replaceChild(frag, t);
    });
    document.querySelectorAll("[visible]").forEach(function (el) {
      var v = (el.getAttribute("visible") || "").trim();
      if (v.charAt(0) === "=") vis.push({ el: el, expr: v.slice(1) });
    });
  }

  /* Every editable form publishes its object as JSON on the wrapper — merge
     them all so their keys become variables the formulas can read. */
  function readInputs() {
    var merged = {};
    document.querySelectorAll(".lc-form[data-lc-value]").forEach(function (f) {
      try {
        var o = JSON.parse(f.getAttribute("data-lc-value"));
        for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) merged[k] = o[k];
      } catch (e) {}
    });
    return merged;
  }

  function evalAll(m) {
    window._lcCellInputs = JSON.stringify(readInputs());
    var exprs = cells.map(function (c) { return c.getAttribute("data-expr"); })
      .concat(vis.map(function (v) { return "bool(" + v.expr + ")"; }));
    window._lcCellExprs = JSON.stringify(exprs);
    run(m,
      "import js, json\n" +
      NS + ".update(json.loads(str(js.window._lcCellInputs)))\n" +
      "_ex = json.loads(str(js.window._lcCellExprs))\n" +
      "_out = []\n" +
      "for _e in _ex:\n" +
      "    try:\n" +
      "        _out.append(str(eval(_e, " + NS + ")))\n" +
      "    except Exception as _err:\n" +
      "        _out.append('\\u26a0 ' + str(_err))\n" +
      "js.window._lcCellOut = json.dumps(_out)\n");
    var out;
    try { out = JSON.parse(window._lcCellOut); } catch (e) { return; }
    cells.forEach(function (c, i) {
      c.textContent = out[i];
      c.classList.toggle("lc-cell-err", (out[i] || "").charAt(0) === "⚠");
    });
    vis.forEach(function (v, i) {
      v.el.classList.toggle("lc-vis-show", out[cells.length + i] === "True");
    });
  }

  function init() {
    if (booted) return;
    booted = true;
    var models = document.querySelectorAll(".highlighter-rouge.cells, pre.cells");
    models.forEach(function (el) { el.classList.add("lc-cells-model"); });
    collect();
    mp().then(function (m) {
      run(m, "import js\n" + NS + " = {}");
      models.forEach(function (el) {
        var codeEl = el.querySelector("code") || el;
        window._lcCellModel = codeEl.textContent || "";
        run(m, "try:\n exec(str(js.window._lcCellModel), " + NS +
               ")\nexcept Exception as _e:\n js.window.console.error('[cells model] ' + str(_e))\n");
      });
      evalAll(m);
      document.addEventListener("lc-model-changed", function () { evalAll(m); });
    });
  }

  /* The first {: .cells } model block on the page ignites the engine, which
     then discovers every cell, form and model block in one pass. */
  function upgradeModel(el) {
    if (el.dataset.lcCellsSeen) return;
    el.dataset.lcCellsSeen = "1";
    init();
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.cells, pre.cells", upgradeModel);
  }
})();
</script>
