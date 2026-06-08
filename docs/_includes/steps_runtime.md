{%- comment -%}
Step runtime — the in-browser Python engine for .feature cards, .button handlers
and the live .diagram component (powered by MicroPython WASM). NOT a widget.

Injected as <script id="lc-steps-preamble"> before every run. It exposes:

  • a typed component model — Object (the js bridge, all helpers are _protected)
    and one wrapper class per gallery component. Each class is declared with
    @component(icon, attrs, assoc, events, methods): a SINGLE source of truth
    used both for runtime access (self.page.<id>.<knob>) and for diagrams.
  • Page         — typed resolver: self.page.<data-lc-id>
  • scenario()   — decorator registering a check
  • _run_all()   — runs built-in checks + scenarios, returns JSON
  • to_dot(scope=None, gaps=None) — emits a Graphviz DOT class diagram of the
    model. No scope → the whole model. Used by the .diagram component AND by
    tools/gen_component_diagram.py.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<!-- Python preamble: injected before every feature/button/diagram run -->
<script id="lc-steps-preamble" type="text/plain">
import js
import json

# ════════════════════════ model metadata (single source) ═════════════════════
# Type → icon. Mirrors usecases/module_manager/backend/module_decorator.py.
ICON = {
    "str": "🔤", "long": "🔡", "int": "🔢", "float": "🔢", "bool": "🔘",
    "date": "📅", "datetime": "🕗", "password": "🔒",
    "ref": "📦", "event": "⚡", "method": "▸", "list": "⦙",
    "guard": "▹", "trans": "▹", "fsm": "🎛️", "init": "➡️",
}

_MODEL = {}        # class name → spec dict
_CLASSES = {}      # class name → class object (for per-class to_dot dispatch)
_TRANSITIONS = {}  # function object → (precondition states, postcondition state)

# Bases shown as a "➭ <icon>" marker in the class title instead of a drawn edge.
# Object and Block are notorious roots — almost everything descends from them,
# so arrows to them are obvious noise. The marker keeps the fact without the
# heavy fan of lines (as in the original ModuleDecorator's ➭ ◻️ convention).
_DOT_ROOT_BASES = {"Object", "Block"}


def transition(pre=(), post=None):
    """Decorate a method as a state transition.

    @transition(["pending", "placed"], "paid")
    def pay(self): ...

    `pre` lists the states the method may be called from (guard); `post` is the
    single state it moves the object to. Read back by @component for the diagram.
    """
    def deco(fn):
        _TRANSITIONS[fn] = (list(pre), post)
        return fn
    return deco


def _prop(attr, typ, default, settable):
    """Build a property that reads (and optionally writes) a data-* attribute."""
    def fget(self):
        v = self._attr(attr)
        if v is None:
            return default
        if typ == "int":
            try:
                return int(v)
            except Exception:
                return default
        if typ == "float":
            try:
                return float(v)
            except Exception:
                return default
        if typ == "bool":
            return str(v).lower() in ("true", "1", "yes")
        return v
    if settable:
        def fset(self, val):
            if self._el is not None:
                if val is None:
                    self._el.removeAttribute(attr)
                else:
                    self._el.setAttribute(attr, str(val))
        return property(fget, fset)
    return property(fget)


def component(icon="", attrs=(), assoc=(), events=(), methods=(), states=()):
    """Class decorator: generate data-* knob properties and register the spec.

    `states` is the ordered list of the class's state-machine states (first =
    initial). Methods decorated with @transition contribute guards/transitions,
    resolved here into each method's spec (pre / post).
    """
    def deco(cls):
        for a in attrs:
            if a.get("data"):
                cname = a["n"]
                aname = a.get("attr", "data-" + cname)
                setattr(cls, cname,
                        _prop(aname, a.get("t", "str"), a.get("d"), a.get("set", False)))
        meth_specs = []
        for m in methods:
            fn = getattr(cls, m, None)
            pre, post = _TRANSITIONS.get(fn, ([], None))
            meth_specs.append({"n": m, "pre": list(pre), "post": post})
        spec = {
            "icon": icon,
            "bases": [b.__name__ for b in cls.__bases__],
            "attrs": [dict(a) for a in attrs],
            "assoc": [dict(a) for a in assoc],
            "events": list(events),
            "methods": meth_specs,
            "states": list(states),
        }
        cls._spec = spec          # SSOT lives on the class itself
        _MODEL[cls.__name__] = spec
        _CLASSES[cls.__name__] = cls
        return cls
    return deco


# ════════════════════════ Object — the js bridge ═════════════════════════════
# Every DOM helper is _protected (leading underscore) → never shown in diagrams.

@component(icon="◻️", attrs=[{"n": "id", "t": "str"}])
class Object:
    def __init__(self, el=None):
        self._el = el

    @classmethod
    def _all(cls, css):
        nl = js.window.document.querySelectorAll(css)
        return [cls(nl.item(i)) for i in range(int(nl.length))]

    def _q(self, css):
        el = self._el.querySelector(css) if self._el else None
        return Object(el)

    def _qq(self, css):
        if not self._el:
            return []
        nl = self._el.querySelectorAll(css)
        return [Object(nl.item(i)) for i in range(int(nl.length))]

    def _attr(self, name):
        if not self._el:
            return None
        v = self._el.getAttribute(name)
        return str(v) if v is not None else None

    def _tap(self, css):
        if self._el is not None:
            sub = self._el.querySelector(css)
            if sub is not None:
                sub.click()
        return self

    @property
    def id(self):
        return self._attr("data-lc-id") or ""

    @property
    def state(self):
        """Current state-machine state (data-state); defaults to the initial."""
        v = self._attr("data-state")
        if v:
            return v
        sts = type(self)._spec.get("states", []) if hasattr(type(self), "_spec") else []
        return sts[0] if sts else ""

    @property
    def states(self):
        """The declared list of states for this class (first = initial)."""
        return list(type(self)._spec.get("states", [])) if hasattr(type(self), "_spec") else []

    # ── per-class diagram contribution (SSOT = cls._spec, set by @component) ──
    @classmethod
    def _dot_node(cls):
        # Plain record label (like the original ModuleDecorator): {title|attrs|meths}
        sp = cls._spec
        title = ((sp["icon"] + " ") if sp["icon"] else "") + cls.__name__
        for b in sp["bases"]:                          # ➭ <icon> for root bases
            if b in _DOT_ROOT_BASES:
                title += " ➭ " + (_MODEL.get(b, {}).get("icon") or "◻️")
        rows = ""
        if sp.get("states"):                       # stateful → show current state
            rows += ICON["fsm"] + " state\\l"
        for a in sp["attrs"]:
            rows += _attr_icon(a) + " " + _disp(a["n"]) + "\\l"
        meth = ""
        for e in sp["events"]:
            meth += ICON["event"] + " " + _disp(e) + "\\l"
        for m in sp["methods"]:
            lead = ICON["guard"] if m["pre"] else ICON["method"]   # ▹ guarded / ▸ plain
            line = lead + " " + _disp(m["n"])
            if m["post"]:
                line += " " + ICON["trans"]                         # trailing ▹ = transition
            meth += line + "\\l"
        comps = [_dot_esc(title)]                   # only non-empty compartments
        if rows:
            comps.append(rows)
        if meth:
            comps.append(meth)
        return "  " + cls.__name__ + ' [label="{' + "|".join(comps) + '}"]'

    @classmethod
    def _dot_states(cls):
        """Emit this class's state-machine cluster + transition edges (if any)."""
        sp = cls._spec
        states = sp.get("states", [])
        if not states:
            return []
        cn = cls.__name__
        def sid(s):
            return "st_" + cn + "_" + s
        # label = class icon + "states" + 🎛️ (no class name — the icon and the
        # dashed tie already identify the owning class)
        ico = (sp["icon"] + " ") if sp["icon"] else ""
        L = ["  subgraph cluster_states_" + cn + " {",
             '    label="' + ico + "states " + ICON["fsm"] + '"; fontsize=10;',
             '    style="filled,rounded"; fillcolor="gray94"; color="gray85";'
             ' margin=12; nodesep=0.9;',
             '    node [fontname="Source Sans Pro, sans-serif", shape=record,'
             ' style="filled,rounded", fillcolor="white", color="gray",'
             ' fontsize=10, penwidth=0.3]',
             '    edge [style=solid, arrowhead=vee, penwidth=0.2,'
             ' arrowsize=0.7, fontsize=8]']
        for i, s in enumerate(states):
            name = _disp(s)
            lbl = (ICON["init"] + " " + name) if i == 0 else name
            L.append("    " + sid(s) + ' [label="' + lbl + '"]')
        L.append("  }")
        for m in sp["methods"]:
            if m["post"] and m["post"] in states:
                froms = [p for p in m["pre"] if p in states] or [states[0]]
                for p in froms:
                    L.append("  " + sid(p) + " -> " + sid(m["post"])
                             + ' [xlabel="' + _disp(m["n"]) + '", fontsize=8,'
                             + ' color="gray45", fontcolor="gray45",'
                             + ' minlen=2, constraint=false]')
        # tie the cluster below its class (dashed, no arrow); constraint keeps it
        # directly under the class node rather than floating off to the side.
        L.append("  " + sid(states[0]) + " -> " + cn
                 + ' [style=dashed, arrowhead=none, color="gray70"]')
        return L

    @classmethod
    def _dot_assoc(cls, sel=None):
        """Association edges — with rankdir=BT a plain owner->target edge points
        UP to the referenced class; open blue head, role as a headlabel there."""
        lines = []
        for a in cls._spec["assoc"]:
            if sel is None or a["target"] in sel:
                lbl = ("⦙ " if a.get("list") else "") + _disp(a["n"])
                # weight pulls the referenced class nearer; head inherits vee
                lines.append("  " + cls.__name__ + " -> " + a["target"]
                             + ' [color=blue, fontcolor=blue, weight=8,'
                             + ' labeldistance=2, headlabel="' + lbl
                             + '", fontsize=8]')
        return lines

    @classmethod
    def to_dot(cls, sel=None):
        """Dump THIS class's contribution: node + associations + state machine."""
        return "\n".join([cls._dot_node()] + cls._dot_assoc(sel)
                         + cls._dot_states())


# ════════════════════════ Block — base of visible components ═════════════════

@component(icon="🧩",
           attrs=[{"n": "exists", "t": "bool"},
                  {"n": "visible", "t": "bool"},
                  {"n": "text", "t": "str"}],
           methods=["click", "has_class"])
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

    def click(self):
        if self._el:
            self._el.click()
        return self


# ════════════════════════ data + leaf wrappers ══════════════════════════════

@component(icon="🗃️", attrs=[{"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"}])
class Dataset(Object):
    def __init__(self, id):
        self._el = None
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


@component(icon="▮", attrs=[{"n": "value", "t": "float"}, {"n": "color", "t": "str"}])
class Bar(Object):
    @property
    def value(self):
        v = self._attr("data-value")
        return float(v) if v is not None else 0.0

    @property
    def color(self):
        return self._attr("fill") or "#0066cc"

    @color.setter
    def color(self, v):
        if self._el:
            self._el.setAttribute("fill", v or "#0066cc")


@component(icon="▦",
           attrs=[{"n": "row_count", "t": "int"},
                  {"n": "headers", "t": "str", "list": True},
                  {"n": "rows", "t": "ref", "list": True}],
           assoc=[{"n": "bind", "target": "Dataset"}],
           methods=["header"])
class Datagrid(Block):
    @property
    def bind(self):
        return Dataset(self._attr("data-bind") or "")

    @property
    def row_count(self):
        return len(self._qq("tbody tr"))

    @property
    def headers(self):
        return [th.text.rstrip(" ↑↓") for th in self._qq("th")]

    @property
    def rows(self):
        cols = self.headers
        out = []
        for tr in self._qq("tbody tr"):
            cells = tr._qq("td")
            out.append({cols[i]: cells[i].text if i < len(cells) else ""
                        for i in range(len(cols))})
        return out

    def header(self, name):
        for th in self._qq("th"):
            if th.text.rstrip(" ↑↓") == name:
                return th
        return Block(None)


@component(icon="📈",
           attrs=[{"n": "type", "t": "str", "data": True, "d": "bar"},
                  {"n": "x", "t": "str", "data": True, "d": ""},
                  {"n": "y", "t": "str", "data": True, "d": ""},
                  {"n": "bar_count", "t": "int"},
                  {"n": "point_count", "t": "int"}],
           assoc=[{"n": "bind", "target": "Dataset"},
                  {"n": "bars", "target": "Bar", "list": True}])
class Chart(Block):
    @property
    def bars(self):
        return [Bar(r._el) for r in self._qq("rect")]

    @property
    def bind(self):
        return Dataset(self._attr("data-bind") or "")

    @property
    def bar_count(self):
        return len(self._qq("rect"))

    @property
    def point_count(self):
        return len(self._qq("circle"))


@component(icon="🦄",
           attrs=[{"n": "title", "t": "str"}, {"n": "status", "t": "str"}],
           methods=["run"])
class Feature(Block):
    @classmethod
    def nth(cls, n=0):
        nl = js.window.document.querySelectorAll(".lc-feature")
        return cls(nl.item(n) if n < int(nl.length) else None)

    @property
    def title(self):
        return self._q(".lc-feature-title").text

    @property
    def status(self):
        v = self._attr("data-status")
        return str(v) if v else "none"

    def run(self):
        """Trigger the card's ▶ Run button."""
        return self._tap(".lc-feature-run-btn")


@component(icon="🖱️",
           attrs=[{"n": "text", "t": "str"}, {"n": "color", "t": "str"}],
           assoc=[{"n": "page", "target": "Page"}],
           events=["on_click"])
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
        return self._attr("data-color") or ""

    @color.setter
    def color(self, v):
        if self._el:
            if v:
                self._el.setAttribute("data-color", v)
            else:
                self._el.removeAttribute("data-color")

    @property
    def page(self):
        return Page()

    def click(self):
        code = self._attr("data-lc-py") or ""
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


# ════════════════════════ gallery component wrappers ═════════════════════════
# Knobs are typed properties (data-* backed); behaviours are methods.

@component(icon="🎠", attrs=[{"n": "delay", "t": "int", "data": True, "d": 4000}],
           methods=["next", "prev", "goto"])
class Carousel(Block):
    def next(self):
        return self._tap(".lc-next, [data-lc-next]")

    def prev(self):
        return self._tap(".lc-prev, [data-lc-prev]")

    def goto(self, n):
        if self._el is not None:
            dots = self._el.querySelectorAll(".lc-dot, [data-go]")
            if dots is not None and int(dots.length) > n:
                dots.item(n).click()
        return self


@component(icon="🃏",
           attrs=[{"n": "cols", "t": "str", "data": True, "d": "auto"},
                  {"n": "gap", "t": "int", "data": True, "d": 18}])
class Cards(Block):
    pass


@component(icon="🔽", attrs=[{"n": "label", "t": "str", "data": True, "d": "Menu"}],
           methods=["open", "close"])
class Dropdown(Block):
    def open(self):
        if self._el is not None:
            self._el.classList.add("open")
        return self

    def close(self):
        if self._el is not None:
            self._el.classList.remove("open")
        return self


@component(icon="📁",
           attrs=[{"n": "cols", "t": "str", "data": True, "d": "auto"},
                  {"n": "show_private", "t": "bool", "data": True,
                   "attr": "data-show-private"}])
class Folder(Block):
    pass


@component(icon="▤",
           attrs=[{"n": "cols", "t": "str", "data": True, "d": "auto"},
                  {"n": "gap", "t": "int", "data": True, "d": 18},
                  {"n": "headings", "t": "str", "data": True, "d": "show"}])
class Grid(Block):
    pass


@component(icon="🗺️",
           attrs=[{"n": "lat", "t": "float", "data": True, "d": 48.86},
                  {"n": "lng", "t": "float", "data": True, "d": 2.35},
                  {"n": "zoom", "t": "int", "data": True, "d": 12},
                  {"n": "height", "t": "int", "data": True, "d": 350}],
           methods=["pan_to", "set_zoom"])
class Map(Block):
    def pan_to(self, lat, lng):
        if self._el is not None:
            self._el.setAttribute("data-lat", str(lat))
            self._el.setAttribute("data-lng", str(lng))
        return self

    def set_zoom(self, z):
        if self._el is not None:
            self._el.setAttribute("data-zoom", str(z))
        return self


@component(icon="🍔", methods=["items"])
class Menu(Block):
    def items(self):
        return [o.text for o in self._qq("a, li")]


@component(icon="📻", attrs=[{"n": "selected", "t": "str"}], methods=["select"])
class Radio(Block):
    @property
    def selected(self):
        c = self._q("input:checked")
        return c.text if c else ""

    def select(self, n):
        if self._el is not None:
            ins = self._el.querySelectorAll("input")
            if ins is not None and int(ins.length) > n:
                ins.item(n).click()
        return self


@component(icon="❓",
           attrs=[{"n": "multi", "t": "bool", "data": True, "d": False},
                  {"n": "graded", "t": "bool"}],
           methods=["check"],
           states=["pending", "graded"])
class Quiz(Block):
    @property
    def graded(self):
        return self.has_class("graded")

    @transition(["pending"], "graded")
    def check(self):
        return self._tap(".lc-quiz-check, [data-lc-check]")


@component(icon="📑", attrs=[{"n": "active", "t": "int"}], methods=["select"])
class Tabs(Block):
    @property
    def active(self):
        if self._el is None:
            return 0
        tabs = self._el.querySelectorAll(".lc-tab")
        for i in range(int(tabs.length)):
            if tabs.item(i).classList.contains("active"):
                return i
        return 0

    def select(self, n):
        if self._el is not None:
            tabs = self._el.querySelectorAll(".lc-tab")
            if tabs is not None and int(tabs.length) > n:
                tabs.item(n).click()
        return self


@component(icon="📝",
           attrs=[{"n": "title", "t": "str", "data": True, "d": ""},
                  {"n": "format", "t": "str", "data": True, "d": "yaml"},
                  {"n": "editable", "t": "bool", "data": True, "d": False}],
           assoc=[{"n": "bound", "target": "Datagrid"}],
           methods=["submit"])
class Form(Block):
    @property
    def bound(self):
        gid = self._attr("data-bound") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
        return _wrap(el)

    def submit(self):
        return self._tap("button[type=submit], .lc-form-submit")


@component(icon="🎞️", attrs=[{"n": "current", "t": "int"}],
           methods=["next", "prev", "goto"])
class Slides(Block):
    @property
    def current(self):
        v = self._attr("data-current")
        return int(v) if v is not None else 0

    def next(self):
        return self._tap(".lc-slide-next, [data-lc-next]")

    def prev(self):
        return self._tap(".lc-slide-prev, [data-lc-prev]")

    def goto(self, n):
        if self._el is not None:
            self._el.setAttribute("data-current", str(n))
        return self


@component(icon="📜", attrs=[{"n": "height", "t": "int", "data": True, "d": 300}])
class Scrollable(Block):
    pass


@component(icon="📄",
           attrs=[{"n": "path", "t": "str", "data": True, "d": ""},
                  {"n": "src", "t": "str", "data": True, "d": ""},
                  {"n": "lang", "t": "str", "data": True, "d": "text"},
                  {"n": "title", "t": "str", "data": True, "d": ""},
                  {"n": "repo", "t": "str", "data": True, "d": ""},
                  {"n": "branch", "t": "str", "data": True, "d": "main"}])
class Code(Block):
    pass


@component(icon="🤖",
           attrs=[{"n": "system", "t": "long", "data": True, "d": ""},
                  {"n": "model", "t": "str", "data": True, "d": "openai/gpt-4o-mini"},
                  {"n": "temperature", "t": "float", "data": True, "d": 0.7},
                  {"n": "max_tokens", "t": "int", "data": True, "d": 500,
                   "attr": "data-max-tokens"},
                  {"n": "intro", "t": "str", "data": True, "d": ""},
                  {"n": "placeholder", "t": "str", "data": True, "d": "Ask anything..."}],
           methods=["ask"])
class Agent(Block):
    def ask(self, prompt):
        if self._el is not None:
            box = self._el.querySelector("textarea, input")
            if box is not None:
                box.value = str(prompt)
            self._tap(".lc-agent-send, button")
        return self


@component(icon="🎥",
           attrs=[{"n": "pip", "t": "str", "data": True, "d": "bottom-right"},
                  {"n": "size", "t": "int", "data": True, "d": 240},
                  {"n": "zoom", "t": "float", "data": True, "d": 1.35},
                  {"n": "fps", "t": "int", "data": True, "d": 25}],
           methods=["start", "stop"],
           states=["idle", "recording", "stopped"])
class Recorder(Block):
    @transition(["idle"], "recording")
    def start(self):
        return self._tap(".lc-rec-start, [data-lc-start]")

    @transition(["recording"], "stopped")
    def stop(self):
        return self._tap(".lc-rec-stop, [data-lc-stop]")


@component(icon="🔳", attrs=[{"n": "size", "t": "int", "data": True, "d": 180}])
class Qr(Block):
    pass


@component(icon="🔤")
class Text(Block):
    pass


@component(icon="🐍",
           attrs=[{"n": "rows", "t": "int", "data": True, "d": 6},
                  {"n": "folded", "t": "bool", "data": True, "d": False},
                  {"n": "silent", "t": "bool", "data": True, "d": False},
                  {"n": "init", "t": "long", "data": True, "d": ""},
                  {"n": "bound", "t": "str", "data": True, "d": ""},
                  {"n": "expected", "t": "str", "data": True, "d": ""}],
           methods=["run"])
class Run(Block):
    def run(self):
        return self._tap(".lc-run-btn, [data-lc-run]")


@component(icon="🔬",
           attrs=[{"n": "height", "t": "int", "data": True, "d": 400},
                  {"n": "bound_to", "t": "str", "data": True, "d": "",
                   "attr": "data-bound-to"}])
class Pytutor(Block):
    pass


@component(icon="🖼️", attrs=[{"n": "height", "t": "int", "data": True, "d": 400}])
class EmbedPage(Block):
    pass


@component(icon="🪗", methods=["open", "close", "sections"])
class Accordion(Block):
    def sections(self):
        return [s.text for s in self._qq("summary, .lc-acc-head")]

    def open(self, n=0):
        if self._el is not None:
            ds = self._el.querySelectorAll("details")
            if ds is not None and int(ds.length) > n:
                ds.item(n).open = True
        return self

    def close(self, n=0):
        if self._el is not None:
            ds = self._el.querySelectorAll("details")
            if ds is not None and int(ds.length) > n:
                ds.item(n).open = False
        return self


# ════════════════════════ resolver ══════════════════════════════════════════

_WRAP = [
    ("lc-datagrid", Datagrid), ("lc-chart", Chart), ("lc-feature", Feature),
    ("lc-button", Button), ("lc-carousel", Carousel), ("lc-cards", Cards),
    ("lc-dropdown", Dropdown), ("lc-folder", Folder), ("lc-grid", Grid),
    ("lc-map", Map), ("lc-menu", Menu), ("lc-radio", Radio), ("lc-quiz", Quiz),
    ("lc-tabs", Tabs), ("lc-form", Form), ("lc-slides", Slides),
    ("lc-scroll", Scrollable), ("lc-code", Code), ("lc-agent", Agent),
    ("lc-recorder", Recorder), ("lc-qr", Qr), ("lc-pyrun", Run),
    ("lc-pytutor", Pytutor), ("lc-embed", EmbedPage), ("lc-accordion", Accordion),
]


def _wrap(el):
    if not el:
        return Block(None)
    c = str(el.getAttribute("class") or "")
    for token, cls in _WRAP:
        if token in c:
            return cls(el)
    return Block(el)


def _lcx_str(v):
    """Short display string for a live attribute value (used by the x-ray lens)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    s = str(v)
    return s if len(s) <= 40 else s[:40] + "…"


def _lcx_target_id(tgt):
    """data-lc-id (or dataset id) of a resolved association target, else ""."""
    if tgt is None:
        return ""
    sid = getattr(tgt, "_id", None)   # id-backed wrappers (Dataset)
    if isinstance(sid, str) and sid:
        return sid
    el = getattr(tgt, "_el", None)
    if el is None:
        return ""
    if isinstance(el, str):
        return el
    try:
        return el.getAttribute("data-lc-id") or ""
    except Exception:
        return ""


def _lcx_dump(obj):
    """Live values (own + inherited), current state, and resolved association
    links (role → target id) for a wrapped object — shared by the lens calls."""
    cn = type(obj).__name__
    cur, seen, vals, roles, seen_role = cn, set(), {}, [], set()
    while cur and cur in _MODEL and cur not in seen:      # walk the base chain
        seen.add(cur)
        for a in _MODEL[cur]["attrs"]:
            if a["n"] not in vals:
                try:
                    vals[a["n"]] = _lcx_str(getattr(obj, a["n"]))
                except Exception:
                    vals[a["n"]] = ""
        for a in _MODEL[cur]["assoc"]:
            if a["n"] not in seen_role:
                seen_role.add(a["n"])
                roles.append((a["n"], a["target"], a.get("list", False)))
        bs = _MODEL[cur]["bases"]
        cur = bs[0] if bs else None
    links = []
    for role, target, is_list in roles:
        try:
            tid = _lcx_target_id(getattr(obj, role))
        except Exception:
            tid = ""
        if tid:
            links.append({"role": role, "target": target, "id": tid, "list": is_list})
    sp = _MODEL.get(cn, {})
    return {"cls": cn, "vals": vals, "links": links,
            "state": (obj.state if sp.get("states") else "")}


def lcx_inspect():
    """Inspect the element marked [data-lcx-target] (the hovered widget)."""
    el = js.window.document.querySelector("[data-lcx-target]")
    if not el:
        return "{}"
    return json.dumps(_lcx_dump(_wrap(el)))


def lcx_target(cls_name, idv):
    """Inspect a connected object by class + id — element-backed (a widget on
    the page) or id-backed (a hidden Dataset). Lets the lens show the full
    inspector of associated objects, even invisible ones."""
    cls = _CLASSES.get(cls_name)
    if cls is None:
        return "{}"
    el = js.window.document.querySelector("[data-lc-id='" + idv + "']")
    obj = None
    if el is not None:
        w = _wrap(el)
        if type(w).__name__ == cls_name:
            obj = w
    if obj is None:
        try:
            obj = cls(idv)            # id-backed (e.g. Dataset(id))
        except Exception:
            obj = _wrap(el) if el is not None else None
    if obj is None:
        return "{}"
    return json.dumps(_lcx_dump(obj))


@component(icon="📄", attrs=[{"n": "id", "t": "str"}], methods=["feature", "features"])
class Page(Object):
    @property
    def id(self):
        path = str(js.window.location.pathname or "")
        name = path.rsplit("/", 1)[-1] or "index"
        if name.endswith(".html"):
            name = name[:-5]
        return name or "index"

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
        return Feature.nth(n)

    def features(self):
        return Feature._all(".lc-feature")


# ════════════════════════ runner infrastructure ═════════════════════════════

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
    els = Object._all("[data-lc-id]")
    ids = [el._attr("data-lc-id") for el in els]
    seen, dupes = set(), set()
    for i in ids:
        (dupes if i in seen else seen).add(i)
    assert not dupes, "duplicate component ids: " + str(dupes)

def _builtin_python_ids(ctx):
    import re as _re
    _id_re = _re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    els = Object._all("[data-lc-id]")
    bad = [el._attr("data-lc-id") for el in els
           if not _id_re.match(el._attr("data-lc-id") or "")]
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
            out.append({"status": "fail", "label": lbl,
                        "error": type(e).__name__ + ": " + str(e)})
    result = json.dumps(out)
    js.window._lcStepsResult = result
    return result


# ════════════════════════ to_dot — the diagram generator ═════════════════════
# Single generator, shared by the live .diagram component and the build script.

_DOT_ORDER = ["Object", "Block", "Page", "Dataset", "Bar",
              "Datagrid", "Chart", "Feature", "Button"]


def _dot_esc(s):
    s = str(s)
    for a, b in (("\\", "\\\\"), ('"', '\\"'), ("{", "\\{"), ("}", "\\}"),
                 ("|", "\\|"), ("<", "\\<"), (">", "\\>")):
        s = s.replace(a, b)
    return s


def _disp(name):
    # display convention: underscores read as spaces (has_class → has class)
    return _dot_esc(str(name).replace("_", " "))


def _attr_icon(a):
    ico = ICON.get(a.get("t", "ref"), "📦")
    if a.get("list"):
        ico = ico + ICON["list"]
    return ico


def _dot_legend():
    # Reproduces the original ModuleDecorator legend verbatim (record label).
    types_ = ("🔤 str or 🔡 long str\\l🔢 int or float\\l🔘 bool\\l🕗 datetime\\l"
              "🔒 password\\l🔤 ⦙ list of 🔤\\l◻️ Object from kore\\l📦 any\\l"
              "🐟 custom type Fish\\l /  derived\\l _  private\\l"
              " =  default value\\l⤴️ reflexive reference\\l"
              "↩️ ⦙ reflexive collection\\l ♢ composite or owned\\l")
    behav = ("⚡️ event or code\\l ▸ method\\l ▹ conditionnal method\\l"
             " ▹ with transition ▹\\l")
    state = "🎛️ state machine\\l➡️ initial state\\l"
    inher = " ➭  inherits from\\l"
    imp = "🛄 imported py\\l"
    return ('"{Legend|' + types_ + "|" + behav + "|" + state + "|"
            + inher + "|" + imp + '}"')


def _scope_set(scope):
    # "*"/"all"/empty → whole model.
    if not scope or scope in ("*", "all"):
        return set(_MODEL.keys())
    # a package name (e.g. "ui"/"kore") → that package's classes + their
    # ancestors (so inheritance arrows resolve to a visible base).
    if scope not in _MODEL and scope in {_pkg_of(n) for n in _MODEL}:
        sel = set()
        for n in _MODEL:
            if _pkg_of(n) == scope:
                sel.add(n)
                stack = list(_MODEL[n]["bases"])
                while stack:
                    b = stack.pop()
                    if b in _MODEL and b not in sel:
                        sel.add(b)
                        stack += _MODEL[b]["bases"]
        return sel
    # a class name → the class + ancestors + association targets + subclasses.
    if scope not in _MODEL:
        return set(_MODEL.keys())
    sel, stack = set(), [scope]
    while stack:
        n = stack.pop()
        if n in sel or n not in _MODEL:
            continue
        sel.add(n)
        for b in _MODEL[n]["bases"]:
            if b in _MODEL:
                stack.append(b)
        for a in _MODEL[n]["assoc"]:
            if a["target"] in _MODEL:
                stack.append(a["target"])
    for m in _MODEL:
        if scope in _MODEL[m]["bases"]:
            sel.add(m)
    return sel


def _dot_order(sel):
    out = [n for n in _DOT_ORDER if n in sel]
    out += sorted(n for n in sel if n not in _DOT_ORDER)
    return out


# ── packages (scopes) ────────────────────────────────────────────────────────
# Default package == intended docs folder: the Block subtree is the UI kit;
# Object and its non-Block descendants (Dataset, Bar, Page) are the kore. Both
# build (CPython) and live (MicroPython) run this same code, so clusters match.
# A build step may later override this from the actual docs/<folder>/ layout.
_PKG_ICON = {"ui": "🎨", "kore": "⚙️"}


def _pkg_of(name):
    stack, seen = [name], set()
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        if n == "Block":
            return "ui"
        stack += _MODEL.get(n, {}).get("bases", [])
    return "kore"


def to_dot(scope=None, gaps=None, packages=None, statemachines=True):
    # Assembler: wraps the graph, groups class nodes into package clusters, then
    # adds the cross-class concerns (associations, inheritance, legend, gaps).
    # statemachines=False hides the state-machine clusters (a display knob).
    # `packages` optionally overrides the default _pkg_of mapping (e.g. from the
    # docs folder layout, supplied by the build step).
    sel = set(_MODEL.keys()) if not scope else _scope_set(scope)
    # Graph/node/edge defaults mirror ModuleDecorator.get_diagram exactly:
    # square filled records, sans-serif @12, hairline edges.
    L = ["digraph component_model {",
         "  rankdir=BT; nodesep=0.25;",
         '  graph [penwidth=0.1, splines=ortho, fontsize=10,'
         ' fontname="Source Sans Pro, sans-serif"];',
         '  node [fontname="Source Sans Pro, sans-serif", penwidth=0.3, shape=record,'
         ' style=filled, color=lightgray, fillcolor=white, fontsize=10];',
         '  edge [fontname="Source Sans Pro, sans-serif", penwidth=0.2,'
         ' arrowhead=vee, arrowsize=0.8];']

    # class nodes, grouped into package (scope) clusters
    pkg_of = (lambda n: packages.get(n, "kore")) if packages else _pkg_of
    groups = {}
    for n in _dot_order(sel):
        groups.setdefault(pkg_of(n), []).append(n)
    for p in sorted(groups):
        icon = _PKG_ICON.get(p, "📦")
        L.append("  subgraph cluster_pkg_" + p + " {")
        L.append('    label="' + _dot_esc(icon + " " + p) + '"; labeljust=l;'
                 ' fontsize=10; fontcolor="gray40";')
        L.append('    style=filled; fillcolor="gray98"; color="gray85";'
                 ' margin=16; penwidth=0.3;')
        for n in groups[p]:
            L.append("  " + _CLASSES[n]._dot_node())
        L.append("  }")

    # associations + state machines (kept at top level, may cross clusters)
    for n in _dot_order(sel):
        L += _CLASSES[n]._dot_assoc(sel)
        if statemachines:
            L += _CLASSES[n]._dot_states()

    # inheritance — direct child→base edges (no junction merging); let dot route
    # them as orthogonal stairs. constraint=true keeps parents above children.
    for n in _dot_order(sel):
        for b in _MODEL[n]["bases"]:
            if b in sel and b not in _DOT_ROOT_BASES:   # Object → ➭ marker, no edge
                L.append("  " + n + " -> " + b
                         + " [arrowhead=empty, color=black, penwidth=0.3,"
                         + " constraint=true]")

    # legend (invisible cluster, like the reference)
    L.append("  subgraph cluster_legend {")
    L.append("    style=invis;")
    L.append('    __legend [label=' + _dot_legend() +
             ', style="filled", fillcolor="gray98", color="gray80",'
             ' fontcolor="#505050", fontsize=10]')
    L.append("  }")

    # gap report (build-time only — needs the docs listing)
    if gaps and not scope:
        ROW = 4
        parts = [" · ".join(_dot_esc(g) for g in gaps[i:i + ROW])
                 for i in range(0, len(gaps), ROW)]
        body = "\\l".join(parts) + "\\l"
        L.append('  __gap [label="{🏗️ builder — no typed wrapper yet|' + body +
                 '}", style="filled,dashed", fillcolor="lightyellow",'
                 ' color="gray60", fontsize=10]')
        L.append('  __gap -> Block [style=dashed, arrowhead=open, color="gray60",'
                 ' constraint=false]')

    L.append("}")
    return "\n".join(L)
</script>
