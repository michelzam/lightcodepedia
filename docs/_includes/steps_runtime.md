{%- comment -%}
Step runtime — the in-browser Python engine for .feature cards and .button
handlers (powered by MicroPython WASM). NOT a standalone widget.

Exposes, as a <script id="lc-steps-preamble"> text blob injected before every
run, the typed component model and scenario runner:

  Object · Block · Datagrid · Chart · Bar · Button · FeatureCard · Dataset
  Page          — typed component resolver: self.page.<id>
  scenario()    — decorator registering a check
  _run_all()    — runs the two built-in checks (unique ids, python-compatible
                  ids) plus every registered scenario; returns JSON and also
                  stashes it on window._lcStepsResult.

Components are reached in a typed way via self.page.<data-lc-id> — there is no
need to construct wrappers from strings.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<!-- Python preamble: injected before every feature/button run -->
<script id="lc-steps-preamble" type="text/plain">
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
    if "lc-button"   in c: return Button(el)
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


class Bar(Object):
    @property
    def value(self):
        v = self.attr("data-value")
        return float(v) if v is not None else 0.0

    @property
    def color(self):
        return self.attr("fill") or "#0066cc"

    @color.setter
    def color(self, v):
        if self._el:
            self._el.setAttribute("fill", v or "#0066cc")


class Chart(Block):
    @property
    def bars(self):
        return [Bar(r._el) for r in self.qq("rect")]

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


class Button(Block):
    @property
    def text(self):
        return str(self._el.textContent or "").strip() if self._el else ""

    @text.setter
    def text(self, v):
        if self._el:
            self._el.textContent = str(v)

    @property
    def color(self):
        return self.attr("data-color") or ""

    @color.setter
    def color(self, v):
        if self._el:
            if v:
                self._el.setAttribute("data-color", v)
            else:
                self._el.removeAttribute("data-color")

    def click(self):
        code = self.attr("data-lc-py") or ""
        if not code:
            if self._el:
                self._el.click()
            return self
        ns = dict(globals())
        ns["button"] = self
        try:
            exec(code + "\non_click(button)\n", ns)
        except Exception as _e:
            if self._el:
                self._el.setAttribute("data-lc-err", str(_e))
        return self

    @property
    def page(self):
        return Page()


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
    js.window._lcStepsResult = result
    return result
</script>
