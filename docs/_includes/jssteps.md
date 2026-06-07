{%- comment -%}
.jssteps — in-browser BDD step runner powered by MicroPython WASM.

Each fenced ```python block becomes a test suite.
Decorate functions with @scenario("label") to register scenarios.
Two built-in scenarios always run first: "component ids are unique" and
"component ids are python compatible" (ids must be valid Python identifiers — no hyphens).
Components are accessed through self.page.<data-lc-id>.

Usage:
  ```python
  @scenario("grid has rows")
  def check_grid(self):
      assert self.page.my_grid.row_count > 0
  ```
  {: .jssteps }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<!-- Python preamble: lc module injected before every .jssteps block -->
<script id="lc-jss-preamble" type="text/plain">
import js
import json

# ── Object — DOM bridge (raw element access, no visible-state assumptions) ────

class Object:
    def __init__(self, el):
        self._el = el

    @classmethod
    def all(cls, css):
        nl = js.window.document.querySelectorAll(css)
        return [cls(nl.item(i)) for i in range(int(nl.length))]

    def q(self, css):
        el = self._el.querySelector(css) if self._el else None
        return Object(el)

    def qq(self, css):
        if not self._el:
            return []
        nl = self._el.querySelectorAll(css)
        return [Object(nl.item(i)) for i in range(int(nl.length))]

    def attr(self, name):
        if not self._el:
            return None
        v = self._el.getAttribute(name)
        return str(v) if v is not None else None

    def click(self):
        if self._el:
            self._el.click()
        return self


# ── Block — base class for all visible components ─────────────────────────────

class Block(Object):
    def __bool__(self):
        return self._el is not None

    @property
    def exists(self):
        return self._el is not None

    @property
    def visible(self):
        if not self._el:
            return False
        cs = js.window.getComputedStyle(self._el)
        return str(cs.display) != "none" and str(cs.visibility) != "hidden"

    @property
    def text(self):
        return str(self._el.textContent or "").strip() if self._el else ""

    def has_class(self, name):
        return bool(self._el and self._el.classList.contains(name))


# ── component wrappers ───────────────────────────────────────────────────────

def _wrap(el):
    if not el:
        return Block(None)
    c = str(el.getAttribute("class") or "")
    if "lc-datagrid" in c: return Datagrid(el)
    if "lc-chart"    in c: return Chart(el)
    if "lc-feature"  in c: return FeatureCard(el)
    return Block(el)


class Dataset:
    def __init__(self, id):
        self._id = id

    def __bool__(self):
        return self.loaded

    def __eq__(self, other):
        if isinstance(other, Dataset):
            return self._id == other._id
        return NotImplemented

    @property
    def loaded(self):
        ds = getattr(js.window, "lcDatasets", None)
        return ds is not None and getattr(ds, self._id, None) is not None

    @property
    def count(self):
        ds = getattr(js.window, "lcDatasets", None)
        if not ds:
            return 0
        arr = getattr(ds, self._id, None)
        return int(arr.length) if arr else 0


class Datagrid(Block):
    @property
    def row_count(self):
        return len(self.qq("tbody tr"))

    @property
    def headers(self):
        return [th.text.rstrip(" ↑↓") for th in self.qq("th")]

    @property
    def rows(self):
        cols = self.headers
        out = []
        for tr in self.qq("tbody tr"):
            cells = tr.qq("td")
            out.append({cols[i]: cells[i].text if i < len(cells) else "" for i in range(len(cols))})
        return out

    def header(self, name):
        for th in self.qq("th"):
            if th.text.rstrip(" ↑↓") == name:
                return th
        return Block(None)


class Chart(Block):
    @property
    def bind(self):
        return Dataset(self.attr("data-bind") or "")

    @property
    def type(self):
        return self.attr("data-type") or "bar"

    @property
    def x(self):
        return self.attr("data-x") or ""

    @property
    def y(self):
        return self.attr("data-y") or ""

    @property
    def bar_count(self):
        return len(self.qq("rect"))

    @property
    def point_count(self):
        return len(self.qq("circle"))


class FeatureCard(Block):
    @classmethod
    def nth(cls, n=0):
        nl = js.window.document.querySelectorAll(".lc-feature")
        return cls(nl.item(n) if n < int(nl.length) else None)

    @property
    def title(self):
        return self.q(".lc-feature-title").text

    @property
    def status(self):
        v = self.attr("data-status")
        return str(v) if v else "none"

    @property
    def run_button(self):
        return self.q(".lc-feature-run-btn")


# ── Page — dynamic component resolver ────────────────────────────────────────

class Page:
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        el = js.window.document.querySelector("[data-lc-id='" + name + "']")
        if el:
            return _wrap(el)
        ds = getattr(js.window, "lcDatasets", None)
        if ds and getattr(ds, name, None) is not None:
            return Dataset(name)
        raise AttributeError("no component with id='" + name + "' on this page")

    def feature(self, n=0):
        return FeatureCard.nth(n)

    def features(self):
        return FeatureCard.all(".lc-feature")


# ── runner infrastructure ────────────────────────────────────────────────────

class _Ctx:
    def __init__(self):
        self.page = Page()

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self.page, name)

_scenarios = []

def scenario(label):
    def decorator(fn):
        _scenarios.append((label, fn))
        return fn
    return decorator

def _builtin_unique_ids(ctx):
    els = Object.all("[data-lc-id]")
    ids = [el.attr("data-lc-id") for el in els]
    seen, dupes = set(), set()
    for i in ids:
        (dupes if i in seen else seen).add(i)
    assert not dupes, "duplicate component ids: " + str(dupes)

def _builtin_python_ids(ctx):
    import re as _re
    _id_re = _re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    els = Object.all("[data-lc-id]")
    bad = [el.attr("data-lc-id") for el in els
           if not _id_re.match(el.attr("data-lc-id") or "")]
    assert not bad, "ids must be valid Python identifiers: " + str(bad)

def _run_all():
    ctx = _Ctx()
    all_s = [
        ("component ids are unique", _builtin_unique_ids),
        ("component ids are python compatible", _builtin_python_ids),
    ] + _scenarios
    out = []
    for lbl, fn in all_s:
        try:
            fn(ctx)
            out.append({"status": "pass", "label": lbl, "error": ""})
        except Exception as e:
            out.append({"status": "fail", "label": lbl, "error": type(e).__name__ + ": " + str(e)})
    result = json.dumps(out)
    js.window._lcJssResult = result
    return result
</script>

<style>
.lc-jssteps { border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; margin: 1em 0; font-family: inherit; }
.lc-jss-head { display: flex; align-items: center; gap: 8px; padding: 8px 14px; background: #f6f8fa; border-bottom: 1px solid #e5e7eb; font-size: .88em; }
.lc-jss-title { font-weight: 600; color: #374151; }
.lc-jss-run { margin-left: auto; border: 1px solid #d1d5db; background: #fff; border-radius: 6px; padding: 3px 12px; cursor: pointer; font-size: .82em; color: #374151; }
.lc-jss-run:hover { background: #f3f4f6; }
.lc-jss-run:disabled { opacity: .5; cursor: default; }
.lc-jss-body { padding: 6px 0; min-height: 2em; }
.lc-jss-row { display: flex; align-items: flex-start; gap: 8px; padding: 3px 14px; font-size: .85em; line-height: 1.5; }
.lc-jss-pass { color: #166534; }
.lc-jss-fail { color: #991b1b; }
.lc-jss-detail { font-size: .82em; color: #6b7280; font-family: ui-monospace,monospace; white-space: pre-wrap; padding: 2px 0 2px 22px; }
.lc-jss-summary { padding: 5px 14px 4px; font-size: .8em; color: #6b7280; border-top: 1px solid #f3f4f6; margin-top: 4px; }
</style>

<script>
(function () {

  var _mpPromise = null;

  function loadMP() {
    if (_mpPromise) return _mpPromise;
    _mpPromise = (window._lcMpReady ||
      import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
        .then(function (mjs) { return mjs.loadMicroPython({ stdout: function () {}, stderr: function () {} }); }));
    window._lcMpReady = _mpPromise;
    return _mpPromise;
  }

  function upgradeJssteps(el) {
    if (el.dataset.lcJsDone) return;
    el.dataset.lcJsDone = "1";

    var code = el.querySelector("code");
    if (!code) return;
    var userCode = code.textContent;

    var wrap = document.createElement("div");
    wrap.className = "lc-jssteps";

    var body = document.createElement("div");
    body.className = "lc-jss-body";

    wrap.innerHTML = '<div class="lc-jss-head">'
      + '<span class="lc-jss-title">🧪 Step tests</span>'
      + '<button class="lc-jss-run">▶ Run</button>'
      + '</div>';
    wrap.appendChild(body);
    el.parentNode.replaceChild(wrap, el);

    wrap.querySelector(".lc-jss-run").addEventListener("click", function () {
      var btn = this;
      btn.disabled = true; btn.textContent = "⏳ Loading…";
      body.innerHTML = "";

      loadMP().then(function (mp) {
        btn.textContent = "⏳ Running…";

        // Detect the correct run method — API differs across MicroPython WASM versions
        var runFn = mp.runPython || mp.exec || mp.pyexec || mp.run;
        if (!runFn) {
          var fns = [];
          try { fns = Object.getOwnPropertyNames(mp).filter(function(k){ return typeof mp[k] === "function"; }); } catch(e2) {}
          body.innerHTML = "<div class='lc-jss-row lc-jss-fail'>⚠️ mp has no runPython. Available: " + (fns.join(", ") || "(none — mp is: " + String(mp) + ")") + "</div>";
          btn.disabled = false; btn.textContent = "▶ Run"; return;
        }

        window._lcJssResult = null;
        var preamble = document.getElementById("lc-jss-preamble").textContent;
        var fullCode = preamble + "\n" + userCode + "\n_run_all()";
        var jsonStr;
        try {
          jsonStr = runFn.call(mp, fullCode);
        } catch (e) {
          body.innerHTML = "<div class='lc-jss-row lc-jss-fail'>⚠️ " + String(e.message || e) + "</div>";
          btn.disabled = false; btn.textContent = "▶ Run"; return;
        }
        // Some MicroPython WASM methods don't return the expression value;
        // _run_all() also stores the result in window._lcJssResult as a fallback.
        if (jsonStr == null) jsonStr = window._lcJssResult;
        var results;
        try { results = JSON.parse(jsonStr); } catch(e3) {}
        if (!Array.isArray(results)) {
          body.innerHTML = "<div class='lc-jss-row lc-jss-fail'>⚠️ unexpected output: " + String(jsonStr).slice(0, 200) + "</div>";
          btn.disabled = false; btn.textContent = "▶ Run"; return;
        }
        var passed = 0;
        results.forEach(function (r) {
          if (r.status === "pass") passed++;
          var row = document.createElement("div");
          row.className = "lc-jss-row " + (r.status === "pass" ? "lc-jss-pass" : "lc-jss-fail");
          row.textContent = (r.status === "pass" ? "✅ " : "❌ ") + r.label;
          if (r.error) {
            var det = document.createElement("div");
            det.className = "lc-jss-detail";
            det.textContent = r.error;
            row.appendChild(det);
          }
          body.appendChild(row);
        });
        var summ = document.createElement("div");
        summ.className = "lc-jss-summary";
        summ.textContent = passed + " / " + results.length + " passed";
        body.appendChild(summ);
        btn.disabled = false; btn.textContent = "▶ Run";
      }).catch(function (e) {
        body.innerHTML = "<div class='lc-jss-row lc-jss-fail'>⚠️ MicroPython failed to load: " + String(e.message || e) + "</div>";
        btn.disabled = false; btn.textContent = "▶ Run";
      });
    });
  }

  function init(root) {
    (root || document).querySelectorAll(".highlighter-rouge.jssteps, p.jssteps").forEach(upgradeJssteps);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { init(); });
  else init();

  var _os = window.lcScanElement;
  window.lcScanElement = function (root) {
    if (_os) _os(root);
    (root || document).querySelectorAll(".highlighter-rouge.jssteps, p.jssteps").forEach(upgradeJssteps);
  };

})();
</script>
