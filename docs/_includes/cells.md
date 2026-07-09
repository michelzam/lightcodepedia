{%- comment -%}
Cells — reactive spreadsheet cells: a knob (or a run of prose) is a cell.

  {= expr }               an inline cell anywhere in prose — replaced by the
                          value of the Python *expression* `expr`, recomputed
                          whenever the page's data changes.

  {: visible="= expr" }   any block shows only while `bool(expr)` is true —
                          `visible` is just another cell.

There is no component to declare. Cells evaluate in the page's own Python
runtime — the same instance a hidden `{: .run silent="true" }` block seeds with
its model (constants, helper functions). Each editable {: .form } is a scope
keyed by its id, so a formula can say `inputs.price` (explicit) or just `price`
(bare sugar, when that field name is unique on the page) — flat when safe,
scoped when needed. Every form edit (and every silent model run) fires
`lc-model-changed`; the cells recompute.

Cells are eval'd, never exec'd: a statement can't be typed into one, and a
cyclic formula fails *safe* (a value like "⚠ maximum recursion…", never a
frozen page).

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

  function run(m, code) { (m.runPython || m.exec || m.run).call(m, code); }
  var cells = [], vis = [], wired = false;

  /* Walk text for {= expr } and replace each with a live <span>. Code fences,
     scripts and styles are left untouched. */
  function collect() {
    var root = document.querySelector("main") || document.body;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var hits = [], n;
    while ((n = walker.nextNode())) if (n.nodeValue.indexOf("{=") >= 0) hits.push(n);
    hits.forEach(function (t) {
      if (t.parentNode && t.parentNode.closest &&
          t.parentNode.closest("pre, code, script, style")) return;
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
    return cells.length + vis.length;
  }

  /* Every editable form publishes its object as JSON on its wrapper. Each form
     is a scope keyed by its id — `inputs.price` — and any field that lives in
     exactly one form is also exposed bare — `price` — as unambiguous sugar.
     A field name shared by two forms is dropped from the bare set, so the
     scoped form (`inputs.price` vs `shipping.price`) is the only way to reach
     it: flat when safe, scoped when needed. */
  function readInputs() {
    var scopes = {}, counts = {}, vals = {};
    document.querySelectorAll(".lc-form[data-lc-value]").forEach(function (f) {
      var id = f.getAttribute("data-lc-id") || "";
      var o;
      try { o = JSON.parse(f.getAttribute("data-lc-value")); } catch (e) { return; }
      if (!o || typeof o !== "object") return;
      if (id) scopes[id] = o;
      for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) {
        counts[k] = (counts[k] || 0) + 1;
        vals[k] = o[k];
      }
    });
    var bare = {};
    for (var k in counts) if (counts[k] === 1) bare[k] = vals[k];
    return { scopes: scopes, bare: bare };
  }

  function evalAll(m) {
    var inp = readInputs();
    window._lcCellScopes = JSON.stringify(inp.scopes);
    window._lcCellBare = JSON.stringify(inp.bare);
    var exprs = cells.map(function (c) { return c.getAttribute("data-expr"); })
      .concat(vis.map(function (v) { return "bool(" + v.expr + ")"; }));
    window._lcCellExprs = JSON.stringify(exprs);
    run(m,
      "import js, json\n" +
      "class _Scope:\n" +                       // recursive: flat form scopes AND nested store nodes
      "    def __init__(self, d):\n" +
      "        for _k, _v in (d.items() if isinstance(d, dict) else []):\n" +
      "            setattr(self, _k, _Scope(_v) if isinstance(_v, dict) else _v)\n" +
      "    def __getattr__(self, _n):\n" +        // unset structural field -> empty, never ⚠
      "        if _n.startswith('_'): raise AttributeError(_n)\n" +
      "        return ''\n" +
      "try:\n" +                                 // site-wide persisted state (Store)
      "    _st = json.loads(str(js.window.lcStore.tree()))\n" +
      "except Exception:\n" +
      "    _st = {}\n" +
      "for _sk, _sv in _st.items():\n" +
      "    globals()[_sk] = _Scope(_sv) if isinstance(_sv, dict) else _sv\n" +
      "_sc = json.loads(str(js.window._lcCellScopes))\n" +   // this page's form scopes
      "for _sid in _sc: globals()[_sid] = _Scope(_sc[_sid])\n" +
      "_bare = json.loads(str(js.window._lcCellBare))\n" +
      "for _k in _bare: globals()[_k] = _bare[_k]\n" +
      "_out = []\n" +
      "for _e in json.loads(str(js.window._lcCellExprs)):\n" +
      "    try:\n" +
      "        _out.append(str(eval(_e)))\n" +
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

  function start() {
    if (wired) return;
    if (!collect()) return;               // no cells on this page — nothing to do
    if (!window.lcPageRuntime) return;    // pyrun provides the shared runtime
    wired = true;
    window.lcPageRuntime().then(function (m) {
      // Listen first, then paint: if a `.run silent` model seeds the runtime
      // after this eval, its lc-model-changed still triggers a recompute.
      document.addEventListener("lc-model-changed", function () { evalAll(m); });
      evalAll(m);
    });
  }

  if (document.readyState !== "loading") start();
  else document.addEventListener("DOMContentLoaded", start);
})();
</script>
