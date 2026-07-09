<!-- © 2026 KarmicSoft — LightCode Platform. Proprietary, All Rights Reserved. License: /license -->
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

# Inspector-widget registries survive preamble re-runs (buttons re-run it on
# every click): bound instances and the new-instance capture list must persist.
try:
    _LC_INSPECT
except NameError:
    _LC_INSPECT = {}
try:
    _LC_NEW
except NameError:
    _LC_NEW = []
try:
    _LC_OBJS
except NameError:
    _LC_OBJS = []

# ════════════════════════ model metadata (single source) ═════════════════════
# Type → icon. Mirrors usecases/module_manager/backend/module_decorator.py.
ICON = {
    "str": "🔤", "long": "🔡", "int": "🔢", "float": "🔢", "bool": "🔘",
    "date": "📅", "datetime": "🕗", "password": "🔒",
    "ref": "📦", "event": "⚡", "method": "▸", "list": "⦙",
    "guard": "▹", "trans": "▹", "fsm": "🎛️", "init": "➡️",
}

# The registries persist across preamble re-runs (every button click re-runs
# the preamble): builtins re-register identically on each run, but author
# classes defined by page blocks register only once — wiping the dicts would
# drop them from diagrams, the x-ray and reference type-checks.
try:
    _MODEL
except NameError:
    _MODEL = {}        # class name → spec dict
    _CLASSES = {}      # class name → class object (for per-class to_dot dispatch)
    _TRANSITIONS = {}  # function object → (pre states, post state, axis, order)

# Bases shown as a "➭ <icon>" marker in the class title instead of a drawn edge.
# Object and Block are notorious roots — almost everything descends from them,
# so arrows to them are obvious noise. The marker keeps the fact without the
# heavy fan of lines (as in the original ModuleDecorator's ➭ ◻️ convention).
_DOT_ROOT_BASES = {"Object", "Block"}


_T_ORD = [0]   # declaration counter — keeps method buttons in source order


def transition(pre=(), post=None, state=None):
    """Decorate a method as a state transition.

    @transition(["pending", "placed"], "paid")
    def pay(self): ...

    `pre` lists the states the method may be called from (guard); `post` is the
    single state it moves the object to. Read back by @component for the diagram.
    On Model classes the method is also wrapped: calling it outside `pre` raises
    PreconditionError, and `post` is applied on success. `state` names which
    State field the transition drives (default: the class's first State field).
    """
    def deco(fn):
        _T_ORD[0] += 1
        _TRANSITIONS[fn] = (list(pre), post, state, _T_ORD[0])
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


# ════════════════════════ declarative fields (Attr / State) ══════════════════
# Author-defined domain classes declare their fields pydantic-style — one line
# carries type, default, constraints and UI metadata. @component harvests them
# into the same _MODEL spec the diagrams, x-ray and inspector widget consume.

class PreconditionError(Exception):
    pass


class Attr:
    """A declarative field: Attr(float, 30, min=20, max=60, unit="kg", ...).

    Knobs: min/max/step (numbers), enum (choices), ro (read-only from outside —
    only a behaviour may change it, via self._set), unit, hint (tooltip),
    secret (render as password). Values live per-instance; writes validate.
    """
    _count = [0]

    def __init__(self, typ=str, default=None, min=None, max=None, step=None,
                 enum=None, ro=False, unit="", hint="", secret=False):
        Attr._count[0] += 1
        self._ord = Attr._count[0]
        self.t = typ if isinstance(typ, str) else getattr(typ, "__name__", "str")
        # a non-builtin type names a Model class → a typed reference. Use the
        # string form for forward/self references: bestie = Attr("Pet")
        self.ref = self.t not in ("int", "float", "bool", "str")
        self.d = default
        self.min = min
        self.max = max
        self.step = step
        self.enum = list(enum) if enum else None
        self.ro = bool(ro)
        self.unit = unit
        self.hint = hint
        self.secret = bool(secret)
        self.is_state = False
        self.n = None

    def _coerce(self, v):
        if self.ref:
            # accept an instance, a bound global name, or None ("" from the widget)
            if v is None or v == "":
                return None
            if isinstance(v, str):
                v = globals().get(v)
            if v is None or not _lc_isa(v, self.t):
                raise ValueError(str(self.n) + " expects a " + self.t)
            return v
        try:
            if self.t == "int":
                v = int(v)
            elif self.t == "float":
                v = float(v)
            elif self.t == "bool":
                v = v if isinstance(v, bool) else str(v).lower() in ("true", "1", "yes", "on")
            elif self.t == "str":
                v = "" if v is None else str(v)
        except Exception:
            raise ValueError(str(self.n) + " expects " + self.t)
        if self.t in ("int", "float"):
            if self.min is not None and v < self.min:
                v = self.min
            if self.max is not None and v > self.max:
                v = self.max
        if self.enum is not None and v not in self.enum:
            raise ValueError(str(self.n) + " must be one of: " + ", ".join(str(x) for x in self.enum))
        return v

    def _spec_dict(self):
        t = "password" if self.secret else ("fsm" if self.is_state else self.t)
        d = {"n": self.n, "t": t, "d": self.d,
             "ro": self.ro, "unit": self.unit, "hint": self.hint, "secret": self.secret,
             "field": True, "state": self.is_state}
        if self.ref:
            d["ref"] = self.t
        if self.min is not None:
            d["min"] = self.min
        if self.max is not None:
            d["max"] = self.max
        if self.step is not None:
            d["step"] = self.step
        if self.enum is not None:
            d["enum"] = list(self.enum)
        return d


class State(Attr):
    """A state-machine axis: State(["hungry", "fed"]) — the first state is the
    initial one. Read-only — only behaviours move it. The first State field is
    the class's canonical state. (Legacy two-arg form still accepted.)"""

    def __init__(self, initial, states=None, hint=""):
        if states is None and isinstance(initial, (list, tuple)):
            states = list(initial)
            initial = states[0]
        Attr.__init__(self, "str", initial, enum=list(states), ro=True, hint=hint)
        self.is_state = True


def _lc_isa(obj, cls_name):
    """Class-name chain check. Walks the instance's own class chain (always
    true to the object, whatever the registry state), then falls back to the
    _MODEL bases — name-based on both paths, so it survives preamble re-runs
    where isinstance would compare stale class objects."""
    k = type(obj)
    seen = set()
    while k is not None and k.__name__ not in seen:
        if k.__name__ == cls_name:
            return True
        seen.add(k.__name__)
        bs = getattr(k, "__bases__", None)
        k = bs[0] if bs else None
    n = type(obj).__name__
    seen = set()
    while n and n not in seen:
        if n == cls_name:
            return True
        seen.add(n)
        bs = _MODEL.get(n, {}).get("bases") or []
        n = bs[0] if bs else None
    return False


def _lc_name_of(inst):
    """The bound global name of an instance (how learners know it)."""
    g = globals()
    for k in g:
        if g[k] is inst and not k.startswith("_"):
            return k
    return ""


def _lc_field_prop(f):
    def fget(self):
        return self._v.get(f.n, f.d)

    def fset(self, val):
        # ro guards the outside world; inside the object's OWN behaviour
        # (@transition methods bracket themselves) plain assignment works.
        if f.ro and not getattr(self, "_lc_active", 0):
            raise AttributeError(f.n + " is read-only — only a behaviour can change it")
        self._v[f.n] = f._coerce(val)
        _lc_push_obj(self)
    return property(fget, fset)


def _lc_bracket(fn):
    """Mark the instance as running its own behaviour for the duration of a
    plain public method — ro/State fields accept assignment from inside,
    exactly as they do inside @transition behaviours."""
    def w(self, *a, **k):
        self._lc_active = getattr(self, "_lc_active", 0) + 1
        try:
            return fn(self, *a, **k)
        finally:
            self._lc_active -= 1
            _lc_push_obj(self)
    return w


def _lc_guard(name, fn, pre, post, sfn):
    """Wrap a transition method: gate on the State field, apply post — and
    mark the instance as running its own behaviour, so ro fields accept
    plain assignment from inside (the lock only faces the outside world)."""
    def w(self, *a, **k):
        if sfn and pre:
            f = type(self)._lc_fmap.get(sfn)
            cur = self._v.get(sfn, f.d if f else None)
            if cur not in pre:
                raise PreconditionError(name + "() needs " + "/".join(pre)
                                        + " — " + sfn + " is " + str(cur))
        self._lc_active = getattr(self, "_lc_active", 0) + 1
        try:
            r = fn(self, *a, **k)
        finally:
            self._lc_active -= 1
        if sfn and post:
            self._v[sfn] = post
        _lc_push_obj(self)
        return r
    return w


def _lc_harvest(cls):
    """Collect Attr fields + transition metadata from a class body; replace the
    fields with validating properties; gate transition methods (Model only)."""
    if getattr(cls, "_lc_harvested_for", None) is cls:
        return cls._lc_fields, cls._lc_statef
    own = []
    for n in dir(cls):
        if n.startswith("_"):
            continue          # fields are public; skips harvest bookkeeping too
        try:
            v = getattr(cls, n)
        except Exception:
            continue
        if isinstance(v, Attr) and v.n in (None, n):
            v.n = n
            own.append(v)
    own.sort(key=lambda f: f._ord)
    fields = list(getattr(cls, "_lc_fields", []) or []) + own
    statef = None
    for f in fields:
        if f.is_state:
            statef = f
            break
    tmeta = dict(getattr(cls, "_lc_tmeta", {}) or {})
    own_t = {}   # transitions declared in THIS class body — inherited ones are
                 # already wrapped, so they no longer match the registry
    for n in dir(cls):
        try:
            fn = getattr(cls, n)
        except Exception:
            continue
        if not callable(fn):
            continue          # only functions can carry @transition metadata
        m = _TRANSITIONS.get(fn)
        if m:
            tmeta[n] = (list(m[0]), m[1], m[2] or (statef.n if statef else None), m[3])
            own_t[n] = tmeta[n]
    # public plain methods (no underscore) are part of the author surface —
    # they become widget buttons. The framework surface (anything Object
    # itself carries) and transition methods are excluded; inherited author
    # methods arrive via the parent's _lc_pub.
    _root = globals().get("Object")
    pub = {}
    if _root is not None and cls is not _root:
        pub = dict(getattr(cls, "_lc_pub", {}) or {})
        for n in dir(cls):
            if n.startswith("_") or n in tmeta or hasattr(_root, n):
                continue
            try:
                fn = getattr(cls, n)
            except Exception:
                continue
            if callable(fn) and not isinstance(fn, type):
                pub[n] = True
    for f in own:
        setattr(cls, f.n, _lc_field_prop(f))
    if fields:
        # ALL of the class's own methods are behaviours — public (buttons),
        # _helpers, and __init__ (constructors set initial state). Inherited
        # methods were wrapped by their declaring class; the framework surface
        # (whatever is literally Object's) is excluded by identity.
        base = cls.__bases__[0] if cls.__bases__ else None
        for n in dir(cls):
            if n in tmeta or (n.startswith("__") and n != "__init__"):
                continue
            try:
                fn = getattr(cls, n)
            except Exception:
                continue
            if not callable(fn) or isinstance(fn, type) or type(fn).__name__ == "bound_method":
                continue
            if base is not None and getattr(base, n, None) is fn:
                continue                      # inherited — wrapped where declared
            if _root is not None and getattr(_root, n, None) is fn:
                continue                      # framework surface
            setattr(cls, n, _lc_bracket(fn))
    if statef is not None:
        for n in tmeta:
            fn = getattr(cls, n, None)
            if fn is not None and _TRANSITIONS.get(fn) is not None:   # not yet wrapped
                pre, post, sfn, _o = tmeta[n]
                setattr(cls, n, _lc_guard(n, fn, pre, post, sfn))
    cls._lc_fields = fields
    cls._lc_own = own          # DRY: specs/diagrams show only own declarations
    cls._lc_own_t = own_t
    cls._lc_pub = pub
    cls._lc_fmap = {f.n: f for f in fields}
    cls._lc_statef = statef
    cls._lc_tmeta = tmeta
    cls._lc_harvested_for = cls
    return fields, statef


def component(icon="", attrs=(), assoc=(), events=(), methods=(), states=()):
    """Class decorator: generate data-* knob properties and register the spec.

    `states` is the ordered list of the class's state-machine states (first =
    initial). Methods decorated with @transition contribute guards/transitions,
    resolved here into each method's spec (pre / post).
    """
    def deco(cls):
        fields, statef = _lc_harvest(cls)   # declarative Attr/State fields (may be none)
        for a in attrs:
            if a.get("data"):
                cname = a["n"]
                aname = a.get("attr", "data-" + cname)
                setattr(cls, cname,
                        _prop(aname, a.get("t", "str"), a.get("d"), a.get("set", False)))
        meth_specs = []
        for m in methods:
            fn = getattr(cls, m, None)
            meta = _TRANSITIONS.get(fn) or (getattr(cls, "_lc_tmeta", {}) or {}).get(m)
            pre, post = (meta[0], meta[1]) if meta else ([], None)
            meth_specs.append({"n": m, "pre": list(pre), "post": post})
        # transition-decorated methods declared HERE join the spec even when
        # not listed (inherited ones stay on the base class's node — DRY)
        own_t = getattr(cls, "_lc_own_t", {}) or {}
        listed = set(methods)
        for n in sorted(own_t, key=lambda k: own_t[k][3]):
            if n not in listed:
                meth_specs.append({"n": n, "pre": list(own_t[n][0]), "post": own_t[n][1]})
                listed.add(n)
        if fields:   # author models: own public plain methods join the node
            base = cls.__bases__[0] if cls.__bases__ else None
            for n in sorted(getattr(cls, "_lc_pub", {}) or {}):
                if n not in listed and not (base is not None and hasattr(base, n)):
                    meth_specs.append({"n": n, "pre": [], "post": None})
        spec = {
            "icon": icon,
            "bases": [b.__name__ for b in cls.__bases__],
            "attrs": [dict(a) for a in attrs]
                     + [f._spec_dict() for f in getattr(cls, "_lc_own", [])],
            "assoc": [dict(a) for a in assoc]
                     + [{"n": f.n, "target": f.t}
                        for f in getattr(cls, "_lc_own", []) if f.ref],
            "events": list(events),
            "methods": meth_specs,
            "states": list(states) or (list(statef.enum)
                      if statef is not None and statef in getattr(cls, "_lc_own", [])
                      else []),
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
        # Everything is an Object — including author-defined domain classes,
        # which declare Attr/State fields. Undecorated subclasses self-register
        # on first use; classes with fields get per-instance storage and join
        # the live-instance registry (reference picklists, inspector cards).
        cls = type(self)
        if getattr(cls, "_lc_harvested_for", None) is not cls:
            component(icon="📦")(cls)
        if cls._lc_fields:
            self._v = {}
            for f in cls._lc_fields:
                self._v[f.n] = f.d
            self._lc_elid = None
            _LC_NEW.append(self)
            _LC_OBJS.append(self)

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

    def _set(self, name, value):
        """Protected write: behaviours use it to change ro fields (validated)."""
        f = (getattr(type(self), "_lc_fmap", None) or {}).get(name)
        self._v[name] = f._coerce(value) if f is not None else value
        _lc_push_obj(self)
        return self

    def _reload_runtime(self):
        """Re-run the steps preamble in place — exactly what a button click
        does. Object is the js bridge, so author code (feature steps) calls
        this instead of touching js/DOM directly."""
        el = js.window.document.getElementById("lc-steps-preamble")
        if el is not None:
            exec(str(el.textContent), globals())
        return self

    @property
    def id(self):
        return self._attr("data-lc-id") or ""

    @property
    def text(self):
        # every wrapped element exposes its text — _q/_qq return Objects, so
        # sub-elements (a th, a td, a title span) need this on the base, not
        # just on Block. Block keeps declaring it for the diagram.
        return str(self._el.textContent or "").strip() if self._el else ""

    @property
    def visible(self):
        # like text: any wrapped element can report visibility. Block keeps
        # declaring it for the diagram.
        if not self._el:
            return False
        cs = js.window.getComputedStyle(self._el)
        return str(cs.display) != "none" and str(cs.visibility) != "hidden"

    def _event_src(self, name):
        """Live source of a declared event handler (for the x-ray inspector).
        Default: none. Wrappers that carry handler code override this."""
        return ""

    @property
    def state(self):
        """Current state: the first State field (models), else data-state."""
        sf = getattr(type(self), "_lc_statef", None)
        if sf is not None:
            return self._v.get(sf.n, sf.d)
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
    def _dot_node(cls, sel=None):
        # Plain record label (like the original ModuleDecorator): {title|attrs|meths}
        sp = cls._spec
        title = ((sp["icon"] + " ") if sp["icon"] else "") + cls.__name__
        for b in sp["bases"]:                          # ➭ <icon> for root bases
            if b in _DOT_ROOT_BASES:
                title += " ➭ " + (_MODEL.get(b, {}).get("icon") or "◻️")
        rows = ""
        if sp.get("states") and not any(a.get("state") for a in sp["attrs"]):
            rows += ICON["fsm"] + " state\\l"
        for a in sp["attrs"]:
            # DRY: a reference drawn as an association edge is not repeated as
            # an attribute row — the row only appears when the target class is
            # outside the diagram, so the reference is never silently lost.
            if a.get("ref") and (sel is None or a["ref"] in sel):
                continue
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
        # label = class icon + the State FIELD's name (mood) + 🎛️ — falls
        # back to "states" for legacy states= classes with no named field.
        # (no class name — the icon and the dashed tie identify the owner)
        ico = (sp["icon"] + " ") if sp["icon"] else ""
        sfn = None
        for a in sp["attrs"]:
            if a.get("state"):
                sfn = a["n"]
                break
        L = ["  subgraph cluster_states_" + cn + " {",
             '    label="' + ico + _disp(sfn or "states") + " " + ICON["fsm"] + '"; fontsize=10;',
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
        return "\n".join([cls._dot_node(sel)] + cls._dot_assoc(sel)
                         + cls._dot_states())


# ════════════════════════ Block — base of visible components ═════════════════

@component(icon="🧩",
           attrs=[{"n": "exists", "t": "bool"},
                  {"n": "visible", "t": "bool"},
                  {"n": "text", "t": "str"}],
           assoc=[{"n": "page", "target": "Page"}],
           methods=["click", "has_class"])
class Block(Object):
    def __bool__(self):
        return self._el is not None

    @property
    def page(self):
        """Every visible component can reach its page — and through it any
        other component by id (self.page.<data-lc-id>)."""
        return Page()

    @property
    def exists(self):
        return self._el is not None

    def has_class(self, name):
        return bool(self._el and self._el.classList.contains(name))

    def click(self):
        if self._el:
            self._el.click()
        return self


# Author-defined domain classes inherit Object directly — everything is an
# Object. The field machinery (Attr/State storage, registries, _set) lives on
# Object itself; `Model` remains as a compatibility alias.
Model = Object


# ════════════════════════ data + leaf wrappers ══════════════════════════════

@component(icon="🛢️", attrs=[{"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"}])
class Dataset(Object):
    def __init__(self, id):
        self._el = None
        self._id = id

    @property
    def id(self):
        return self._id or ""

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


@component(icon="🔎",
           attrs=[{"n": "query", "t": "str"}, {"n": "editable", "t": "bool"},
                  {"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"}],
           assoc=[{"n": "source", "target": "Dataset"}])
class Query(Dataset):
    """A dataset computed by SQL over other datasets — it IS a Dataset (it
    publishes its result under its id), so consumers can't tell it apart.
    With editable, the SQL comes from a live editor instead of the source."""
    def __init__(self, ref=None):
        self._el = None
        if ref is not None and hasattr(ref, "getAttribute"):   # X-ray wraps by element
            self._el = ref
            self._id = ref.getAttribute("data-lc-id") or ""
        else:                                                  # resolver builds by id
            self._id = ref or ""

    @property
    def query(self):
        return str(self._el.getAttribute("data-query") or "") if self._el is not None else ""

    @property
    def editable(self):
        return self._el is not None and self._el.getAttribute("data-editable") == "true"

    @property
    def source(self):
        sid = self._el.getAttribute("data-bind") if self._el is not None else None
        return Dataset((str(sid).split(",")[0] if sid else ""))


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
           assoc=[{"n": "source", "target": "Dataset"}],
           methods=["header"])
class Datagrid(Block):
    @property
    def source(self):
        return Dataset(self._attr("data-bind") or "")

    @property
    def row_count(self):
        # two renderers back a datagrid: the custom HTML table (.lc-dg-table →
        # tbody tr, used by source-bound grids) and AG Grid (.ag-row in the body
        # viewport, used by code-block grids). Count whichever this grid uses.
        n = len(self._qq("tbody tr"))
        if n:
            return n
        ag = self._qq(".ag-center-cols-container .ag-row")
        return len(ag) if ag else len(self._qq(".ag-row"))

    @property
    def headers(self):
        ths = [th.text.rstrip(" ↑↓") for th in self._qq("th")]
        if ths:
            return ths
        return [h.text for h in self._qq(".ag-header-cell-text")]

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
           assoc=[{"n": "source", "target": "Dataset"},
                  {"n": "master", "target": "Datagrid"},
                  {"n": "bars", "target": "Bar", "list": True}])
class Chart(Block):
    @property
    def bars(self):
        return [Bar(r._el) for r in self._qq("rect")]

    @property
    def source(self):
        return Dataset(self._attr("data-bind") or "")

    @property
    def master(self):
        gid = self._attr("data-bound-to") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']")
        return Datagrid(el)

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
           attrs=[{"n": "text", "t": "str"},
                  {"n": "kind", "t": "str", "data": True, "d": "", "attr": "kind"},
                  {"n": "color", "t": "str"}],
           events=["on_click"], methods=["click"])
class Button(Block):
    @property
    def kind(self):
        # link-button variant knob: secondary | success | danger | outline
        return self._attr("kind") or ""

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

    def _event_src(self, name):
        # on_click carries its Python body in data-lc-py (see click()).
        return self._attr("data-lc-py") or "" if name == "on_click" else ""

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

@component(icon="🎠", attrs=[{"n": "delay", "t": "int", "data": True, "d": 4000},
                            {"n": "current", "t": "int"}],
           methods=["next", "prev", "goto"])
class Carousel(Block):
    @property
    def current(self):
        items = self._qq(".lc-carousel-item")
        for i in range(len(items)):
            if items[i]._el.classList.contains("active"):
                return i
        return 0

    def _dots(self):
        return self._el.querySelectorAll(".lc-carousel-dots span") if self._el else None

    def goto(self, n):
        d = self._dots()
        if d is not None and int(d.length) > n:
            d.item(n).click()
        return self

    def next(self):
        items = self._qq(".lc-carousel-item")
        return self.goto((self.current + 1) % len(items)) if items else self

    def prev(self):
        items = self._qq(".lc-carousel-item")
        return self.goto((self.current - 1) % len(items)) if items else self


@component(icon="🃏",
           attrs=[{"n": "cols", "t": "str", "data": True, "d": "auto"},
                  {"n": "gap", "t": "int", "data": True, "d": 18}])
class Cards(Block):
    pass


@component(icon="🔽", attrs=[{"n": "label", "t": "str", "data": True, "d": "Menu"}],
           methods=["open", "close"])
class Dropdown(Block):
    def _menu(self):
        return self._el.querySelector(".lc-dd-menu") if self._el else None

    @property
    def opened(self):
        m = self._menu()
        return bool(m and m.classList.contains("open"))

    def open(self):
        m = self._menu()
        if m is not None:
            m.classList.add("open")
        return self

    def close(self):
        m = self._menu()
        if m is not None:
            m.classList.remove("open")
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


@component(icon="📻", attrs=[{"n": "selected", "t": "str"}, {"n": "active", "t": "int"}], methods=["select"])
class Radio(Block):
    @property
    def selected(self):
        c = self._el.querySelector("input:checked") if self._el else None
        if not c:
            return ""
        lbl = c.parentElement
        return (lbl.textContent or "").strip() if lbl else ""

    @property
    def active(self):
        if self._el is None:
            return 0
        ins = self._el.querySelectorAll("input")
        for i in range(int(ins.length)):
            if ins.item(i).checked:
                return i
        return 0

    def select(self, n):
        if self._el is not None:
            ins = self._el.querySelectorAll("input")
            if ins is not None and int(ins.length) > n:
                ins.item(n).click()
        return self


@component(icon="❓",
           attrs=[{"n": "multi", "t": "bool", "data": True, "d": False},
                  {"n": "graded", "t": "bool"}],
           methods=["pick", "check"],
           states=["pending", "graded"])
class Quiz(Block):
    @property
    def graded(self):
        # a quiz is graded once any option has been revealed as ✓ or ✗
        return any(o._el.classList.contains("lc-quiz-correct") or
                   o._el.classList.contains("lc-quiz-wrong")
                   for o in self._qq("li"))

    def pick(self, n):
        opts = self._qq("li")
        if n < len(opts):
            opts[n]._el.click()
        return self

    @transition(["pending"], "graded")
    def check(self):
        return self._tap(".lc-quiz-check, [data-lc-check]")


@component(icon="📚",
           attrs=[{"n": "title", "t": "str", "data": True, "d": ""},
                  {"n": "goal", "t": "str", "data": True, "d": ""},
                  {"n": "use_case", "t": "str", "data": True, "d": ""},
                  {"n": "key_concepts", "t": "list"},
                  {"n": "karma", "t": "int", "data": True, "d": 0}],
           assoc=[{"n": "prerequisites", "target": "KnowledgeNode", "list": True},
                  {"n": "next", "target": "KnowledgeNode", "list": True},
                  {"n": "quiz", "target": "Quiz", "list": True}],
           methods=["discover", "design", "specify", "master"],
           states=["locked", "discovering", "designing", "specifying", "mastered"])
class KnowledgeNode(Object):
    """A single learning topic, modelled as a stateful object.

    Encapsulates one BUILD-AI module: its from-the-future goal, the use-case
    slice it teaches, its key concepts and quiz, the karma it grants, and its
    place in the graph (prerequisites ←→ next). Its state machine *is* the
    teaching method — the three Aristotelian unities, walked in order:
    locked → discovering (place) → designing (action) → specifying (time) →
    mastered.
    """

    @transition(["locked"], "discovering")
    def discover(self):
        """Unity of place — meet the running thing as a user."""
        return self

    @transition(["discovering"], "designing")
    def design(self):
        """Unity of action — open the synchronised screen / model / code."""
        return self

    @transition(["designing"], "specifying")
    def specify(self):
        """Unity of time — reveal the specs that were there all along."""
        return self

    @transition(["specifying"], "mastered")
    def master(self):
        """Quiz passed, karma granted — the verified topic becomes a block."""
        return self


@component(icon="📑", attrs=[{"n": "active", "t": "int"}], methods=["select"])
class Tabs(Block):
    @property
    def active(self):
        if self._el is None:
            return 0
        tabs = self._el.querySelectorAll(".lc-tab-btn")
        for i in range(int(tabs.length)):
            if tabs.item(i).classList.contains("active"):
                return i
        return 0

    def select(self, n):
        if self._el is not None:
            tabs = self._el.querySelectorAll(".lc-tab-btn")
            if tabs is not None and int(tabs.length) > n:
                tabs.item(n).click()
        return self


class _Attrs(object):
    """Attribute view over a dict — form.data.url returns that field's value
    (or None). Used by Form.data so handlers read self.page.<form>.data.<field>."""
    def __init__(self, d):
        self._d = d or {}

    def __getattr__(self, name):
        return self._d.get(name)


@component(icon="📝",
           attrs=[{"n": "title", "t": "str", "data": True, "d": ""},
                  {"n": "format", "t": "str", "data": True, "d": "yaml"},
                  {"n": "editable", "t": "bool", "data": True, "d": False}],
           assoc=[{"n": "master", "target": "Datagrid"}],
           methods=["submit"])
class Form(Block):
    @property
    def master(self):
        gid = self._attr("data-bound") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
        return _wrap(el)

    @property
    def data(self):
        """Live field values as attributes: self.page.<form>.data.<field>.
        The form republishes its object to data-lc-value on every edit."""
        import json
        raw = self._attr("data-lc-value") or "{}"
        try:
            d = json.loads(raw)
        except Exception:
            d = {}
        return _Attrs(d)

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
                  {"n": "master", "t": "str", "data": True, "d": "",
                   "attr": "data-bound-to"}])
class Pytutor(Block):
    pass


@component(icon="🖼️", attrs=[{"n": "height", "t": "int", "data": True, "d": 400}],
           methods=["load", "image"])
class EmbedPage(Block):
    def load(self, url):
        """Point the embedded iframe at a new URL (e.g. from a button on_click)."""
        if self._el is not None:
            self._el.src = url

    def image(self, url):
        """Show a single image, auto-fitted (object-fit: contain) inside the frame.
        A bare iframe pointed at an image shows the browser's raw image document,
        which the page can't style — so we wrap it in a tiny centred srcdoc."""
        if self._el is None:
            return
        doc = ("<!doctype html><meta charset=utf-8>"
               "<style>html,body{margin:0;height:100%;background:#fff}"
               "body{display:flex;align-items:center;justify-content:center}"
               "img{max-width:100%;max-height:100%;object-fit:contain;display:block}"
               "</style><img src='" + url + "'>")
        self._el.srcdoc = doc


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


@component(icon="🧊",
           attrs=[{"n": "height", "t": "int", "data": True, "d": 440,
                   "attr": "height"},
                  {"n": "loaded", "t": "bool"},
                  {"n": "last_log", "t": "str"}],
           methods=["bark", "run", "wag_tail", "swim", "blow_bubble"])
class Scene3d(Block):
    @property
    def loaded(self):
        return bool(self._el is not None
                    and self._el.querySelector("canvas") is not None)

    @property
    def last_log(self):
        if self._el is None:
            return ""
        nl = self._el.querySelectorAll(".lc-s3d-console div")
        n = int(nl.length)
        return str(nl.item(n - 1).textContent or "").strip() if n else ""

    def _method_btn(self, name):
        if self._el is not None:
            nl = self._el.querySelectorAll(".lc-s3d-methods button")
            for i in range(int(nl.length)):
                b = nl.item(i)
                if str(b.textContent or "").strip() == name + "()":
                    return Block(b)
        return Block(None)

    def bark(self):
        return self._method_btn("bark").click()

    def run(self):
        return self._method_btn("run").click()

    def wag_tail(self):
        return self._method_btn("wag_tail").click()

    def swim(self):
        return self._method_btn("swim").click()

    def blow_bubble(self):
        return self._method_btn("blow_bubble").click()


@component(icon="🗣️",
           attrs=[{"n": "size", "t": "int"},
                  {"n": "playing", "t": "bool"},
                  {"n": "speech", "t": "str"}],
           methods=["play", "stop", "video"],
           states=["idle", "speaking"])
class Avatar(Block):
    def _reg(self):
        regs = getattr(js.window, "_lcAvatars", None)
        aid = self.id
        return getattr(regs, aid, None) if regs is not None and aid else None

    @property
    def playing(self):
        av = self._reg()
        return bool(av.playing) if av is not None else False

    @property
    def speech(self):
        b = self._el.querySelector(".lc-avatar-speech") if self._el is not None else None
        return str(b.textContent or "").strip() if b is not None else ""

    @property
    def size(self):
        c = self._el.querySelector(".lc-avatar-char") if self._el is not None else None
        if c is None:
            return 0
        try:
            return int(str(c.style.width).replace("px", "") or 0)
        except Exception:
            return 0

    @transition(["idle"], "speaking")
    def play(self):
        if not self.playing:
            self._tap(".lc-avatar-char")
        return self

    @transition(["speaking"], "idle")
    def stop(self):
        if self.playing:
            self._tap(".lc-avatar-char")
        return self

    def video(self, url):
        """Set a runtime video source (direct .mp4/.webm URL or a YouTube link)
        for this avatar — e.g. from a button on_click, so the URL never lives in
        the repo. A script line with `video: true` then plays this source with
        its cues; YouTube links play through the embed, file URLs keep alpha."""
        fn = getattr(js.window, "lcAvatarSetVideo", None)
        if fn is not None and self.id:
            fn(self.id, str(url or ""))
        return self


@component(icon="🧱")
class Blocks(Block):
    """Card-sections widget (.block / .blocks) — layout container."""
    pass


@component(icon="⌨️")
class Repl(Block):
    """Interactive Python REPL (.repl)."""
    pass


@component(icon="🎬", attrs=[{"n": "height", "t": "int", "data": True, "d": 400}])
class Video(Block):
    """Embedded video iframe (.video)."""
    pass


@component(icon="📊",
           attrs=[{"n": "samples", "t": "int"}, {"n": "heap_mb", "t": "float"},
                  {"n": "dom_nodes", "t": "int"}])
class Vitals(Block):
    @property
    def samples(self):
        return int(self._attr("data-samples") or 0)

    @property
    def heap_mb(self):
        v = self._attr("data-heap")
        return float(v) if v else None

    @property
    def dom_nodes(self):
        return int(self._attr("data-dom") or 0)


@component(icon="✍️", attrs=[{"n": "rows", "t": "int", "data": True}])
class Mdpad(Block):
    @property
    def rendered(self):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        return str(o.textContent or "").strip() if o is not None else ""


@component(icon="🏷️", attrs=[{"n": "value", "t": "str"}])
class Stat(Block):
    @property
    def value(self):
        return self.text


@component(icon="🧪",
           attrs=[{"n": "checked", "t": "int"}, {"n": "broken", "t": "int"},
                  {"n": "ok", "t": "bool"}])
class ModelCheck(Block):
    @property
    def checked(self):
        return int(self._attr("data-checked") or 0)

    @property
    def broken(self):
        return int(self._attr("data-broken") or 0)

    @property
    def ok(self):
        return self._attr("data-checked") is not None and self.broken == 0


@component(icon="▶️",
           attrs=[{"n": "playing", "t": "bool"}, {"n": "label", "t": "str"}],
           assoc=[{"n": "target", "target": "Avatar"}])
class AvatarTrigger(Block):
    @property
    def playing(self):
        return self.has_class("playing")

    @property
    def label(self):
        return self.text

    @property
    def target(self):
        gid = self._attr("data-avt-target") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
        return _wrap(el)


# ════════════════════════ resolver ══════════════════════════════════════════

_WRAP = [
    ("lc-query", Query),
    ("lc-datagrid", Datagrid), ("lc-chart", Chart), ("lc-feature", Feature),
    ("lc-button", Button), ("button", Button), ("lc-carousel", Carousel),
    ("lc-cards", Cards), ("lc-dropdown", Dropdown), ("lc-folder", Folder),
    ("lc-grid", Grid), ("lc-map", Map), ("lc-menu", Menu),
    ("lc-radio-group", Radio), ("lc-quiz", Quiz), ("lc-tabs", Tabs),
    ("lc-form", Form), ("lc-slides", Slides), ("lc-scrollable", Scrollable),
    ("lc-code", Code), ("lc-agent", Agent), ("lc-recorder", Recorder),
    ("lc-qr", Qr), ("lc-pyrun", Run), ("lc-pyrepl", Repl),
    ("lc-pytutor", Pytutor), ("lc-embed-page", EmbedPage),
    ("lc-embed", EmbedPage), ("lc-video", Video), ("lc-accordion", Accordion),
    ("lc-blocks", Blocks),
    ("lc-scene3d", Scene3d), ("lc-avatar-host", Avatar),
    ("lc-vitals", Vitals), ("lc-modelcheck", ModelCheck), ("lc-stat", Stat), ("lc-mdpad", Mdpad),
    ("lc-avatar-trigger", AvatarTrigger),
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
    cur, seen, vals, roles, seen_role, evts = cn, set(), {}, [], set(), {}
    while cur and cur in _MODEL and cur not in seen:      # walk the base chain
        seen.add(cur)
        for a in _MODEL[cur]["attrs"]:
            if a["n"] not in vals:
                try:
                    vals[a["n"]] = _lcx_str(getattr(obj, a["n"]))
                except Exception:
                    vals[a["n"]] = ""
        for e in _MODEL[cur]["events"]:                   # live handler source
            if e not in evts:
                try:
                    evts[e] = obj._event_src(e)
                except Exception:
                    evts[e] = ""
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
    return {"cls": cn, "vals": vals, "events": evts, "links": links,
            "state": (obj.state if (sp.get("states")
                      or getattr(type(obj), "_lc_statef", None) is not None) else "")}


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
        # cross-page persisted state: Page().<node>.<component>.<field>
        st = _store_tree()
        if name in st and isinstance(st[name], dict):
            return _StoreScope(st[name])
        raise AttributeError("no component with id='" + name + "' on this page")

    def feature(self, n=0):
        return Feature.nth(n)

    def features(self):
        return Feature._all(".lc-feature")


# ════════════════════════ inspector widget bridge ════════════════════════════
# A {: .inspector } block binds Model instances to a DOM card. Python owns the
# truth: every field write / transition pushes a fresh schema to the JS
# renderer, so widget, REPL and buttons all stay in sync.

def _lc_inspect_schema(obj):
    cls = type(obj)
    sp = getattr(cls, "_spec", None) or {}
    fields = []
    for f in cls._lc_fields:
        d = f._spec_dict()
        v = obj._v.get(f.n, f.d)
        if f.ref:
            # value = the referenced instance's name; options = every live,
            # type-compatible instance (subclasses included — polymorphism)
            d["v"] = _lc_name_of(v) if v is not None else ""
            d["options"] = [_lc_name_of(o) for o in _LC_OBJS
                            if o is not obj and _lc_isa(o, f.t) and _lc_name_of(o)]
        else:
            d["v"] = v
        fields.append(d)
    meths = []
    tmeta = cls._lc_tmeta or {}
    for n in sorted(tmeta, key=lambda k: tmeta[k][3]):
        pre, post, sfn, _o = tmeta[n]
        cur = obj._v.get(sfn) if sfn else None
        meths.append({"n": n, "pre": pre, "post": post,
                      "enabled": (not pre) or (cur in pre)})
    for n in sorted(getattr(cls, "_lc_pub", {}) or {}):
        if n not in tmeta:
            meths.append({"n": n, "pre": [], "post": None, "enabled": True})
    return {"cls": cls.__name__, "icon": sp.get("icon", ""),
            "doc": str(getattr(cls, "__doc__", "") or ""),
            "fields": fields, "methods": meths}


def _lc_inspect_push(elid, err=""):
    pairs = _LC_INSPECT.get(elid) or []
    cards = []
    for name, inst in pairs:
        d = _lc_inspect_schema(inst)
        d["name"] = name
        cards.append(d)
    fn = getattr(js.window, "_lcInspectorRender", None)
    if fn is not None:
        fn(elid, json.dumps({"cards": cards, "error": err}))


def _lc_push_obj(obj):
    elid = getattr(obj, "_lc_elid", None)
    if elid:
        _lc_inspect_push(elid)


def _lc_inspect_bind(elid, insts):
    pairs = []
    for inst in insts:
        inst._lc_elid = elid
        pairs.append((_lc_name_of(inst) or "obj" + str(len(pairs) + 1), inst))
    _LC_INSPECT[elid] = pairs
    _lc_inspect_push(elid)


def _lc_inspect_bind_new(elid):
    """Bind every Model instance created by the block that just ran."""
    _lc_inspect_bind(elid, list(_LC_NEW))
    _LC_NEW[:] = []


def _lc_inspect_bind_names(elid, names):
    g = globals()
    want = [n.strip() for n in str(names).split(",")]
    _lc_inspect_bind(elid, [g[n] for n in want if n in g])
    _LC_NEW[:] = []


def _lc_inspect_set(elid, name, field, vjson):
    err = ""
    for nm, inst in (_LC_INSPECT.get(elid) or []):
        if nm == name:
            try:
                setattr(inst, field, json.loads(vjson))
            except Exception as e:
                err = str(e)
    _lc_inspect_push(elid, err)


def _lc_inspect_call(elid, name, meth):
    err = ""
    for nm, inst in (_LC_INSPECT.get(elid) or []):
        if nm == name:
            try:
                getattr(inst, meth)()
            except Exception as e:
                err = str(e)
    _lc_inspect_push(elid, err)


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

def _in_editor(el):
    # the page editor renders a live preview of the page, so every component
    # exists twice (real page + #ed-drawer preview). Its copies must not count
    # toward page-level id checks, or features run in the editor falsely fail.
    e = getattr(el, "_el", None)
    try:
        return bool(e) and bool(e.closest("#ed-drawer"))
    except Exception:
        return False

def _builtin_unique_ids(ctx):
    els = [el for el in Object._all("[data-lc-id]") if not _in_editor(el)]
    ids = [el._attr("data-lc-id") for el in els]
    seen, dupes = set(), set()
    for i in ids:
        (dupes if i in seen else seen).add(i)
    assert not dupes, "duplicate component ids: " + str(dupes)

def _builtin_python_ids(ctx):
    import re as _re
    _id_re = _re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    els = [el for el in Object._all("[data-lc-id]") if not _in_editor(el)]
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
    t = a.get("t", "ref")
    # a custom type shows the referenced class's own icon (🐟 for a Fish ref)
    ico = ICON.get(t) or _MODEL.get(t, {}).get("icon") or "📦"
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
            L.append("  " + _CLASSES[n]._dot_node(sel))
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


# ════════════════════════ structural Store (browser-instance) ════════════════
# Learner state lives in this browser (window.lcStore -> localStorage), keyed by
# the structural path node.component.field. Files/inline are design-time seeds;
# only learner edits reach the Store. Reads are Store-over-seed, and an unset
# path is empty — never an error. The same path works in cells, Python and
# storage. The whole tree is injected as nested namespaces so build_ai.profile
# .nickname resolves as plain attribute access (and Page().build_ai... too).

class _StoreScope:
    def __init__(self, d):
        for _k, _v in (d.items() if isinstance(d, dict) else []):
            setattr(self, _k, _StoreScope(_v) if isinstance(_v, dict) else _v)
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return ""                       # unset structural field -> empty

def _store_tree():
    try:
        raw = js.window.lcStore.tree()
        return json.loads(str(raw)) if raw else {}
    except Exception:
        return {}

class _Store:
    def get(self, path, default=""):
        node = _store_tree()
        for seg in str(path).split("."):
            if isinstance(node, dict) and seg in node:
                node = node[seg]
            else:
                return default
        return node
    def set(self, path, value):
        try:
            js.window.lcStore.set(path, value)
        except Exception:
            pass
        _inject_store()                 # refresh the bare namespaces after a write
    def reset(self):
        try:
            js.window.lcStore.reset()
        except Exception:
            pass
        _inject_store()
    def tree(self):
        return _store_tree()

Store = _Store()

def eval_cell(expr):
    """Evaluate a {= cell } expression in the page's namespace (store + defs)."""
    return eval(str(expr), globals())

_STORE_KEYS = set()
def _inject_store():
    global _STORE_KEYS
    _g = globals()
    tree = _store_tree()
    for _k in list(_STORE_KEYS):        # drop namespaces no longer in the store
        if _k not in tree and _k in _g:
            del _g[_k]
    _STORE_KEYS = set()
    for _k, _v in tree.items():
        _g[_k] = _StoreScope(_v) if isinstance(_v, dict) else _v
        _STORE_KEYS.add(_k)

_inject_store()
</script>

<style>
/* ── .inspector — auto-widget generated from a Model class ─────────────── */
.lc-inspector { margin: 1em 0; display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.92em; }
.lc-ins-card { flex: 1 1 260px; max-width: 420px; border: 1px solid #d8dee6; border-radius: 10px; padding: 12px 14px; background: #fff; }
.lc-ins-head { font-weight: 600; margin-bottom: 8px; color: #1e293b; }
.lc-ins-head .lc-ins-cls { color: #64748b; font-weight: 400; }
.lc-ins-doc { font-size: 0.85em; color: #64748b; margin: -4px 0 8px; }
.lc-ins-chips { display: flex; align-items: center; flex-wrap: wrap; gap: 5px; margin: 6px 0 10px; }
.lc-ins-chips .lc-ins-axis { font-family: monospace; font-size: 0.85em; color: #64748b; margin-right: 2px; }
.lc-ins-chip { font-family: monospace; font-size: 0.82em; padding: 2px 9px; border-radius: 999px; background: #e5e7eb; color: #6b7280; }
.lc-ins-chip.active { background: #dc2626; color: #fff; font-weight: 600; box-shadow: 0 0 0 2px rgba(220,38,38,0.18); }
.lc-ins-row { display: flex; align-items: center; gap: 8px; padding: 3px 0; }
.lc-ins-row > label { flex: 0 0 40%; font-family: monospace; font-size: 0.88em; color: #334155; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lc-ins-row > label .lc-ins-unit { color: #94a3b8; }
.lc-ins-ctl { flex: 1; display: flex; align-items: center; gap: 6px; min-width: 0; }
.lc-ins-ctl input[type=range] { flex: 1; min-width: 0; }
.lc-ins-ctl input[type=text], .lc-ins-ctl input[type=password], .lc-ins-ctl input[type=number], .lc-ins-ctl select {
  flex: 1; min-width: 0; font: inherit; font-size: 0.88em; padding: 2px 6px; border: 1px solid #cbd5e1; border-radius: 5px; }
.lc-ins-ctl output { font-family: monospace; font-size: 0.85em; color: #0066cc; min-width: 3.5em; text-align: right; }
.lc-ins-ro { font-family: monospace; font-size: 0.88em; color: #64748b; }
.lc-ins-meths { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.lc-ins-meths button { font-family: monospace; font-size: 0.86em; padding: 4px 12px; border: none; border-radius: 6px;
  cursor: pointer; background: #0066cc; color: #fff; }
.lc-ins-meths button:hover:not(:disabled) { background: #0052a3; }
.lc-ins-meths button:disabled { background: #cbd5e1; color: #eef2f7; cursor: not-allowed; }
.lc-ins-meths button .lc-ins-post { opacity: 0.75; font-size: 0.9em; }
.lc-ins-err { flex-basis: 100%; font-family: monospace; font-size: 0.85em; color: #b91c1c; background: #fef2f2;
  border: 1px solid #fecaca; border-radius: 6px; padding: 5px 10px; }
.lc-ins-loading { color: #94a3b8; font-size: 0.9em; padding: 8px 0; }
</style>

<script>
(function () {
  if (window._lcInspectorReady) return;
  window._lcInspectorReady = true;

  var INS_N = 0;

  function mpReady() {
    if (!window._lcMpReady) {
      window._lcMpReady = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
        .then(function (mjs) { return mjs.loadMicroPython({ stdout: function () {}, stderr: function () {} }); });
    }
    return window._lcMpReady;
  }
  function runPy(mp, code) {
    var fn = mp.runPython || mp.exec || mp.pyexec || mp.run;
    if (fn) fn.call(mp, code);
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* the Python side pushes a fresh schema here after every change */
  window._lcInspectorRender = function (elid, payload) {
    var host = document.querySelector("[data-lc-inspector='" + elid + "']");
    if (!host) return;
    var d;
    try { d = JSON.parse(payload); } catch (e) { return; }
    var h = "";
    (d.cards || []).forEach(function (c) {
      h += "<div class='lc-ins-card' data-card='" + esc(c.name) + "'>";
      h += "<div class='lc-ins-head'>" + esc(c.icon) + " " + esc(c.name)
        + " <span class='lc-ins-cls'>· " + esc(c.cls) + "</span></div>";
      if (c.doc) h += "<div class='lc-ins-doc'>" + esc(c.doc) + "</div>";
      (c.fields || []).forEach(function (f) {          /* state axes → chip rows */
        if (!f.state) return;
        h += "<div class='lc-ins-chips'><span class='lc-ins-axis'>" + esc(f.n) + "</span>";
        (f.enum || []).forEach(function (s) {
          h += "<span class='lc-ins-chip" + (s === f.v ? " active" : "") + "'>" + esc(s) + "</span>";
        });
        h += "</div>";
      });
      (c.fields || []).forEach(function (f) {
        if (f.state) return;
        var unit = f.unit ? " <span class='lc-ins-unit'>(" + esc(f.unit) + ")</span>" : "";
        h += "<div class='lc-ins-row'" + (f.hint ? " title='" + esc(f.hint) + "'" : "") + ">"
          + "<label>" + esc(f.n).replace(/_/g, " ") + unit + "</label><div class='lc-ins-ctl'>";
        var dis = f.ro ? " disabled" : "";
        if (f.ref) {
          /* typed reference → picklist of live, type-compatible instances */
          h += "<select data-f='" + esc(f.n) + "' data-t='str'" + dis + "><option value=''>—</option>";
          (f.options || []).forEach(function (o) {
            h += "<option" + (o === f.v ? " selected" : "") + ">" + esc(o) + "</option>";
          });
          h += "</select><span class='lc-ins-ro'>:" + esc(f.ref) + "</span>";
        } else if (f.t === "bool") {
          h += "<input type='checkbox' data-f='" + esc(f.n) + "' data-t='bool'" + (f.v ? " checked" : "") + dis + ">"
            + (f.ro ? "<span class='lc-ins-ro'>🔒</span>" : "");
        } else if (f.ro) {
          h += "<span class='lc-ins-ro'>" + esc(f.v) + " 🔒</span>";
        } else if (f.enum) {
          h += "<select data-f='" + esc(f.n) + "' data-t='str'>";
          f.enum.forEach(function (o) {
            h += "<option" + (o === f.v ? " selected" : "") + ">" + esc(o) + "</option>";
          });
          h += "</select>";
        } else if ((f.t === "int" || f.t === "float") && f.min != null && f.max != null) {
          var step = f.step != null ? f.step : (f.t === "int" ? 1 : (f.max - f.min) / 100);
          h += "<input type='range' data-f='" + esc(f.n) + "' data-t='num' min='" + f.min
            + "' max='" + f.max + "' step='" + step + "' value='" + f.v + "'>"
            + "<output>" + esc(f.v) + "</output>";
        } else if (f.t === "int" || f.t === "float") {
          h += "<input type='number' data-f='" + esc(f.n) + "' data-t='num' value='" + esc(f.v) + "'>";
        } else {
          h += "<input type='" + (f.secret ? "password" : "text") + "' data-f='" + esc(f.n)
            + "' data-t='str' value='" + esc(f.v) + "'>";
        }
        h += "</div></div>";
      });
      if ((c.methods || []).length) {
        h += "<div class='lc-ins-meths'>";
        c.methods.forEach(function (m) {
          var tip = m.enabled ? (m.post ? "→ " + m.post : "") : "needs: " + (m.pre || []).join(" / ");
          h += "<button data-m='" + esc(m.n) + "'" + (m.enabled ? "" : " disabled")
            + (tip ? " title='" + esc(tip) + "'" : "") + ">" + esc(m.n) + "()"
            + (m.post ? " <span class='lc-ins-post'>▸ " + esc(m.post) + "</span>" : "") + "</button>";
        });
        h += "</div>";
      }
      h += "</div>";
    });
    if (d.error) h += "<div class='lc-ins-err'>⚠️ " + esc(d.error) + "</div>";
    host.innerHTML = h;
  };

  function pySend(code) { mpReady().then(function (mp) { try { runPy(mp, code); } catch (e) { console.error("[lc-inspector]", e); } }); }

  function upgradeInspector(el) {
    if (el.dataset.lcInsDone) return;
    el.dataset.lcInsDone = "1";
    var code = (el.querySelector("code") || el).textContent;
    var elid = el.id || ("insp" + (++INS_N));
    var bind = el.getAttribute("bind") || "";
    var host = document.createElement("div");
    host.className = "lc-inspector";
    host.id = elid;
    host.setAttribute("data-lc-id", elid);
    host.setAttribute("data-lc-inspector", elid);
    host.innerHTML = "<div class='lc-ins-loading'>⏳ Building the model widget…</div>";
    el.parentNode.replaceChild(host, el);

    /* widget edits → Python setters (validation lives there) */
    host.addEventListener("change", function (ev) {
      var t = ev.target, f = t.getAttribute && t.getAttribute("data-f");
      if (!f) return;
      var card = t.closest("[data-card]"); if (!card) return;
      var v = t.type === "checkbox" ? t.checked : (t.getAttribute("data-t") === "num" ? Number(t.value) : t.value);
      pySend("_lc_inspect_set(" + JSON.stringify(elid) + "," + JSON.stringify(card.getAttribute("data-card"))
        + "," + JSON.stringify(f) + "," + JSON.stringify(JSON.stringify(v)) + ")");
    });
    host.addEventListener("input", function (ev) {   /* live slider label */
      var t = ev.target;
      if (t.type === "range" && t.nextElementSibling) t.nextElementSibling.textContent = t.value;
    });
    host.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-m]");
      if (!b || b.disabled) return;
      var card = b.closest("[data-card]"); if (!card) return;
      pySend("_lc_inspect_call(" + JSON.stringify(elid) + "," + JSON.stringify(card.getAttribute("data-card"))
        + "," + JSON.stringify(b.getAttribute("data-m")) + ")");
    });

    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    var tail = bind
      ? "\n_lc_inspect_bind_names(" + JSON.stringify(elid) + ", " + JSON.stringify(bind) + ")\n"
      : "\n_lc_inspect_bind_new(" + JSON.stringify(elid) + ")\n";
    mpReady().then(function (mp) {
      try {
        runPy(mp, preamble + "\n_LC_NEW[:] = []\n" + code + tail);
        /* page diagrams redraw so freshly-declared classes join the picture */
        document.dispatchEvent(new CustomEvent("lc-model-changed"));
      }
      catch (e) {
        host.innerHTML = "<div class='lc-ins-err'>⚠️ " + esc(e.message || e) + "</div>";
        console.error("[lc-inspector]", e);
      }
    }).catch(function (e) {
      host.innerHTML = "<div class='lc-ins-err'>⚠️ Python runtime failed to load</div>";
      console.error("[lc-inspector]", e);
    });
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.inspector, pre.inspector", upgradeInspector);
  }
})();
</script>
