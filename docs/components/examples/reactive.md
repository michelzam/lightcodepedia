---
title: "Reactive cells — formulas in any knob"
---

# 🧮 Reactive cells (prototype)

A working sketch of the idea we designed: **a knob is a spreadsheet cell.** It
holds a literal — or a `= formula`, a Python *expression* evaluated live in the
page's own namespace and re‑run whenever its inputs change. `visible=` is just
another cell. This page carries its **own tiny engine** (nothing global is
touched) so it's a safe, isolated prototype.

## 📊 It's literally a spreadsheet {#sheet}

The model — plain Python, the page's namespace:

```python
price = 20
qty   = 3
def subtotal(): return price * qty
def shipping(): return 0 if subtotal() >= 50 else 5   # free over 50 — the "iif"
def total():    return subtotal() + shipping()
def loop():     return loop()                         # a deliberate cycle
```
{: #cell-model }

<div class="cell-controls">
  <label>price <input type="range" min="0" max="40" value="20" data-set="price" data-out="price-out"><b id="price-out">20</b></label>
  <label>qty <input type="number" min="1" max="9" value="3" data-set="qty"></label>
</div>

Subtotal **{= subtotal() }** · Shipping **{= shipping() }** · **Total {= total() }**

Drag `price` or change `qty` → every `{= … }` recomputes. No `if`, no refresh —
the cells track the model. (Free shipping kicks in the moment `total` crosses 50.)

## 👁️ `visible` is just a cell {#visibility}

Same mechanism, pointed at a boolean — the cumulative learner‑flag case. Pick one:

<div class="cell-controls">
  <button data-set="mixed_up" data-val="true">🤔 I think it's an attribute</button>
  <button data-set="mixed_up" data-val="false">✅ It's a method</button>
</div>

You picked *attribute* — quick recap: **attributes store state, methods *do* things.** `wanda.blow_bubble()` runs behaviour.
{: visible="= mixed_up" }

Nice — you've got it. `blow_bubble()` is behaviour Wanda performs. 🎉
{: visible="= not mixed_up" }

No `.adaptive`, no container, no branch in the markup — each block is a cell
whose formula reads the same flag. (Cumulative in the real thing: independent
flags, so several blocks can show at once.)

## 🛡️ Why it can't turn into a language {#guardrails}

The formula grammar is **Python expressions only**, because a cell is `eval`'d,
never `exec`'d — and the interpreter enforces the line for free:

- a **comprehension is an expression**, so it's fine: **{= [x for x in range(3)] }** — but a `for:` / `if:` *statement* can't be typed into a cell at all (`eval` rejects it as a syntax error);
- a **cycle** fails **safe** — the recursive `loop()` yields **{= loop() }** as a value, not a frozen page.

So control flow and loops‑with‑side‑effects stay where they belong — a `.run`
Python fence — and knobs stay declarative dataflow. Spreadsheet, not BASIC.

*Shipped form:* the same `= formula` in any real knob (`height="= base*2"`,
`visible="= intro.ready"`), reactive on the platform's `lc-model-changed` event,
with the linter topo‑sorting cell dependencies to catch cycles at author time.
This page is the isolated proof that the core evaluates, reacts, isolates, and
fails safe.

<style>
.cell-controls { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; margin: 10px 0 4px; padding: 10px 14px; background: #f6f8fa; border: 1px solid #e2e8f0; border-radius: 10px; }
.cell-controls label { display: inline-flex; align-items: center; gap: 8px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.9em; }
.cell-controls button { font: inherit; font-size: 0.9em; padding: 5px 12px; border: 1px solid #cbd5e1; border-radius: 8px; background: #fff; cursor: pointer; }
.cell-controls button:hover { border-color: #0066cc; }
.lc-cell { font-weight: 700; color: #0066cc; font-variant-numeric: tabular-nums; }
.lc-cell.err { color: #b91c1c; font-weight: 600; }
[visible^="="] { display: none; }
[visible^="="] { border-left: 3px solid #cde8cd; background: #fffdf5; padding: 6px 12px; border-radius: 6px; }
</style>

<script>
(function () {
  var NS = "_LCCELLNS";
  function mp() {
    if (!window._lcMpReady) {
      window._lcMpReady = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
        .then(function (m) { return m.loadMicroPython({ stdout: function(){}, stderr: function(){} }); });
    }
    return window._lcMpReady;
  }
  function run(m, c) { (m.runPython || m.exec || m.run).call(m, c); }
  function pylit(v) {
    return typeof v === "boolean" ? (v ? "True" : "False")
         : typeof v === "number" ? String(v) : JSON.stringify(String(v));
  }
  var cells = [], vis = [];
  function collect() {
    var root = document.querySelector("main") || document.body;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var hits = [], n;
    while ((n = walker.nextNode())) if (n.nodeValue.indexOf("{=") >= 0) hits.push(n);
    hits.forEach(function (t) {
      if (t.parentNode && t.parentNode.closest && t.parentNode.closest("#cell-model, script, pre, code, style")) return;
      var s = t.nodeValue, re = /\{=\s*([\s\S]*?)\s*\}/g, m, last = 0, frag = document.createDocumentFragment(), any = false;
      while ((m = re.exec(s))) {
        any = true;
        if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
        var sp = document.createElement("span");
        sp.className = "lc-cell"; sp.setAttribute("data-expr", m[1]); sp.textContent = "…";
        frag.appendChild(sp); cells.push(sp); last = re.lastIndex;
      }
      if (!any) return;
      if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
      t.parentNode.replaceChild(frag, t);
    });
    var els = document.querySelectorAll("[visible]");
    for (var i = 0; i < els.length; i++) {
      var v = (els[i].getAttribute("visible") || "").trim();
      if (v.charAt(0) === "=") vis.push({ el: els[i], expr: v.slice(1) });
    }
  }
  function evalAll(m) {
    var exprs = cells.map(function (c) { return c.getAttribute("data-expr"); })
      .concat(vis.map(function (v) { return "bool(" + v.expr + ")"; }));
    window._lcExprs = exprs;
    run(m,
      "import js, json\n_o=[]\n" +
      "for _i in range(int(js.window._lcExprs.length)):\n" +
      " try:\n  _o.append(str(eval(str(js.window._lcExprs[_i]), " + NS + ")))\n" +
      " except Exception as _e:\n  _o.append('\\u26a0 '+str(_e))\n" +
      "js.window._lcCellOut=json.dumps(_o)\n");
    var out = []; try { out = JSON.parse(window._lcCellOut); } catch (e) { return; }
    cells.forEach(function (c, i) {
      c.textContent = out[i];
      c.classList.toggle("err", (out[i] || "").charAt(0) === "⚠");
    });
    vis.forEach(function (v, i) { v.el.style.display = (out[cells.length + i] === "True") ? "" : "none"; });
  }
  function init() {
    collect();
    var modelEl = document.getElementById("cell-model");
    var codeEl = modelEl ? (modelEl.querySelector("code") || modelEl) : null;
    window._lcCellModelSrc = codeEl ? codeEl.textContent : "";
    mp().then(function (m) {
      run(m, "import js\n" + NS + " = {}\ntry:\n exec(str(js.window._lcCellModelSrc), " + NS + ")\nexcept Exception as _e:\n js.window.console.error('[cell-model] '+str(_e))\n");
      var ctrls = document.querySelectorAll("[data-set]");
      for (var i = 0; i < ctrls.length; i++) (function (ctrl) {
        var name = ctrl.getAttribute("data-set");
        var ev = (ctrl.type === "range" || ctrl.type === "number") ? "input" : "click";
        ctrl.addEventListener(ev, function () {
          var val;
          if (ctrl.type === "checkbox") val = ctrl.checked;
          else if (ctrl.type === "range" || ctrl.type === "number") val = Number(ctrl.value);
          else if (ctrl.hasAttribute("data-val")) {
            var dv = ctrl.getAttribute("data-val");
            val = dv === "true" ? true : dv === "false" ? false : dv;
          } else val = ctrl.value;
          run(m, NS + "[" + JSON.stringify(name) + "] = " + pylit(val));
          if (ctrl.hasAttribute("data-out")) {
            var o = document.getElementById(ctrl.getAttribute("data-out"));
            if (o) o.textContent = val;
          }
          evalAll(m);
        });
      })(ctrls[i]);
      evalAll(m);
    });
  }
  if (document.readyState !== "loading") init();
  else document.addEventListener("DOMContentLoaded", init);
})();
</script>
