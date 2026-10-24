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
import re
try:
    from collections import OrderedDict as _ODict   # a row's columns keep the list's order
except ImportError:
    _ODict = dict


class datetime:
    """The standard name, on the device's clock (MicroPython ships no datetime,
    the browser knows the local time). Enough of the real one for a page:
    now(), the fields, isoformat(), strftime(), ordering (no __format__:
    MicroPython gives an f-string no format spec on objects).
    A datetime attribute — Attr(datetime, datetime.now) — reads and writes
    its table column as ISO text (Michel, 2026-10-19)."""
    _MON = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    _DAY = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        self.year, self.month, self.day = int(year), int(month), int(day)
        self.hour, self.minute, self.second = int(hour), int(minute), int(second)

    @classmethod
    def now(cls):
        d = js.Date.new()
        return cls(d.getFullYear(), d.getMonth() + 1, d.getDate(), d.getHours(), d.getMinutes(), d.getSeconds())

    @classmethod
    def fromisoformat(cls, s):
        s = str(s).strip().replace("T", " ")
        d, _, t = s.partition(" ")
        y, m, dd = d.split("-")
        parts = (t.split("+")[0].split("Z")[0].split(".")[0].split(":") + ["0", "0", "0"])[:3] if t else ["0", "0", "0"]
        return cls(y, m, dd, parts[0], parts[1], parts[2])

    def _tuple(self):
        return (self.year, self.month, self.day, self.hour, self.minute, self.second)

    def weekday(self):
        y, m, d = self.year, self.month, self.day      # Zeller, Monday = 0
        if m < 3:
            m += 12
            y -= 1
        return (d + (13 * (m + 1)) // 5 + y + y // 4 - y // 100 + y // 400 + 5) % 7

    def date(self):
        return datetime(self.year, self.month, self.day)

    def isoformat(self):
        return "%04d-%02d-%02dT%02d:%02d:%02d" % self._tuple()

    def strftime(self, fmt):
        h12 = self.hour % 12 or 12
        tab = {"Y": "%04d" % self.year, "m": "%02d" % self.month, "d": "%02d" % self.day,
               "H": "%02d" % self.hour, "M": "%02d" % self.minute, "S": "%02d" % self.second,
               "y": "%02d" % (self.year % 100), "I": "%02d" % h12, "p": "AM" if self.hour < 12 else "PM",
               "b": self._MON[self.month - 1], "a": self._DAY[self.weekday()], "%": "%"}
        out, i = "", 0
        while i < len(fmt):
            c = fmt[i]
            if c == "%" and i + 1 < len(fmt):
                out += tab.get(fmt[i + 1], "%" + fmt[i + 1])
                i += 2
            else:
                out += c
                i += 1
        return out

    def __str__(self):
        return "%04d-%02d-%02d %02d:%02d:%02d" % self._tuple()

    def __repr__(self):
        return "datetime(%d, %d, %d, %d, %d, %d)" % self._tuple()

    def __eq__(self, o):
        return _lc_isdt(o) and self._tuple() == o._tuple()

    def __lt__(self, o):
        return self._tuple() < o._tuple()

    def __le__(self, o):
        return self._tuple() <= o._tuple()

    def __gt__(self, o):
        return self._tuple() > o._tuple()

    def __ge__(self, o):
        return self._tuple() >= o._tuple()

    def __hash__(self):
        return hash(self._tuple())


def _lc_isdt(v):
    """A datetime by its shape: the preamble runs again before every feature
    or button, so an object born earlier holds an instance of an earlier
    class of the same name — isinstance would say no."""
    return hasattr(v, "isoformat") and hasattr(v, "year")

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
try:
    _LC_DECL          # model blocks: block id → the class names it declared
except NameError:
    _LC_DECL = {}
    _LC_SRC = {}          # model blocks: block id → the fence's text (declaration order)
try:
    _LC_SOURCED       # a class is a dataset: source dataset id → the class wearing it
except NameError:
    _LC_SOURCED = {}

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

    One state needs no list: @transition("asked", "met") (Michel, 2026-10-16).
    `pre` lists the states the method may be called from (guard); `post` is the
    single state it moves the object to. Read back by @component for the diagram.
    On Model classes the method is also wrapped: calling it outside `pre` raises
    PreconditionError, and `post` is applied on success. `state` names which
    State field the transition drives (default: the class's first State field).
    """
    def deco(fn):
        _T_ORD[0] += 1
        _TRANSITIONS[fn] = ([pre] if isinstance(pre, str) else list(pre), post, state, _T_ORD[0])
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
    secret (render as password), required (never blank). Values live
    per-instance; writes validate.
    """
    _count = [0]

    def __init__(self, typ=str, default=None, min=None, max=None, step=None,
                 enum=None, ro=False, unit="", hint="", secret=False, hidden=False, was=None,
                 required=False):
        Attr._count[0] += 1
        self._ord = Attr._count[0]
        self.t = typ if isinstance(typ, str) else getattr(typ, "__name__", "str")
        # a non-builtin type names a Model class → a typed reference. Use the
        # string form for forward/self references: bestie = Attr("Pet")
        self.ref = self.t not in ("int", "float", "bool", "str", "datetime")
        # Attr() with no default reads as "the empty one of its type" — a
        # blank string, a zero, a False — so name = Attr() is legal shorthand
        # (Michel, 2026-08-22). Refs keep None: an empty reference is real.
        # A DEFAULT MAY BE A FUNCTION — Attr(datetime, datetime.now): called
        # when the object is born (➕ New, Walk(...)), never when a row is read
        # back, the result coerced like any typed-in value (Michel, 2026-10-19:
        # standard Python, construction only, the attribute's type decides).
        if default is None and not self.ref:
            default = {"str": "", "int": 0, "float": 0.0, "bool": False}.get(self.t)
        self.d = default
        self.min = min
        self.max = max
        self.step = step
        self.enum = list(enum) if enum else None
        self.ro = bool(ro)
        self.unit = unit
        self.hint = hint
        self.secret = bool(secret)
        # hidden=True: kept by the class and its table, shown by no grid or
        # form (Michel, 2026-10-17: "it should not appear anymore in the grid")
        self.hidden = bool(hidden)
        # was="old": the attribute's former name — its table column is renamed,
        # its data kept (Michel, 2026-10-17, register P5)
        self.was = was
        # required=True: never blank (Michel, 2026-10-24: "default should be
        # False (tolerant); only an explicit value would check"). A write of a
        # blank is refused, Walk(...) without it is refused; a row read back
        # blank is kept as it is and waits on the page, never saved blank; the
        # table refuses blanks once every row has one (lc_ensure, setup v3)
        self.required = bool(required)
        self.is_state = False
        self.n = None

    def _default(self):
        """The value a newborn gets: the default itself, or what the default
        function returns, through the attribute's type."""
        d = self.d
        if callable(d):
            d = d()
            try:
                d = self._coerce(d)
            except Exception:
                pass
        return d

    @staticmethod
    def _blank(v):
        return v is None or (isinstance(v, str) and not v.strip())

    def _coerce(self, v):
        v = self._coerce0(v)
        if self.required and Attr._blank(v):
            raise ValueError(str(self.n) + " is required")
        return v

    def _coerce0(self, v):
        if self.ref:
            # accept an instance, a bound global name, or None ("" from the widget)
            if v is None or v == "":
                return None
            if isinstance(v, str):
                v = globals().get(v)
            if v is None or not _lc_isa(v, self.t):
                raise ValueError(str(self.n) + " expects a " + self.t)
            return v
        if self.t == "datetime":
            if v is None or v == "":
                return None
            if _lc_isdt(v):
                return v
            try:
                return datetime.fromisoformat(v)
            except Exception:
                raise ValueError(str(self.n) + " expects a datetime")
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
        # a function default is shown by its name (= datetime.now), a datetime as text
        dv = self.d
        if callable(dv):
            dv = getattr(dv, "__name__", "…")
            if dv == "now":
                dv = "datetime.now"
        elif _lc_isdt(dv):
            dv = str(dv)
        d = {"n": self.n, "t": t, "d": dv,
             "ro": self.ro, "unit": self.unit, "hint": self.hint, "secret": self.secret,
             "field": True, "state": self.is_state}
        if self.required:
            d["req"] = True
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

    def __init__(self, initial, *more, **kw):
        # State("asked", "met", "home") — the stages in order, no list needed
        # (Michel, 2026-10-16); State([...]) and State(initial, [...]) still hold
        states, hint = kw.get("states"), kw.get("hint", "")
        if more and isinstance(more[0], (list, tuple)):
            states = list(more[0])
        elif more:
            states = [initial] + [m for m in more if isinstance(m, str)]
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


class _AgentResponse:
    """One answer of an agent, in the areas the page shows."""
    def __init__(self, r):
        g = (lambda k: str(getattr(r, k, "") or "")) if r is not None else (lambda k: "")
        self.text, self.direction, self.question, self.example = g("text"), g("direction"), g("question"), g("example")

    def __str__(self):
        return self.text


def _lc_did(part, verb):
    """What the learner did with a part, counted by the page (lcDid)."""
    d = getattr(js.window, "lcDid", None)
    pid = part._attr("data-lc-id") if part._el is not None else None
    if d is None or not pid:
        return 0
    return int(d.count(str(pid), verb))


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
                # a class may write its own property for a knob (an agent's
                # system is live configuration, not only a data-* echo)
                if cname in (getattr(cls, "_lc_keep", ()) or ()):
                    continue
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
            for n in _lc_verbs(cls):
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
    def __init__(self, el=None, **kw):
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
                self._v[f.n] = f._default()
            self._lc_elid = None
            self._js = None          # the list's own row, when the class wears a dataset
            if kw:
                fmap = getattr(cls, "_lc_fmap", None) or {}
                for k, v in kw.items():
                    f = fmap.get(k)
                    if f is None:
                        raise TypeError(cls.__name__ + " has no attribute " + k)
                    self._v[k] = f._coerce(v)
                # a required attribute is a required argument, as in any Python call
                missing = [f.n for f in cls._lc_fields if getattr(f, "required", False) and Attr._blank(self._v.get(f.n))]
                if missing:
                    raise TypeError(cls.__name__ + "() needs " + ", ".join(missing))
            _LC_NEW.append(self)
            _LC_OBJS.append(self)
            # THE CONSTRUCTOR WITH KEYWORDS IS ➕ NEW (Michel, 2026-10-19: a walk
            # made in a method "with the implicit intention to make it
            # persistent"): Walk(dog=rex, walker="Ana") takes the row, the
            # defaults fill the rest, a database class saves by itself. A bare
            # Walk() is the engine's own path for rows read back.
            if kw:
                cls._lc_born(self)

    # ── born verbs: every object can be made and unmade; a class that wears a
    # dataset adds and removes the row itself (Michel, 2026-10-16: "Delete being
    # a generic implicit method, inherited from Object") ──
    @classmethod
    def new(cls):
        """A fresh one, named, on the bus — a sourced class adds a row to its list."""
        return cls._lc_born(cls())

    @classmethod
    def _lc_born(cls, inst):
        if not getattr(cls, "_lc_fields", None):
            return inst
        cls._lc_seq = getattr(cls, "_lc_seq", 0) + 1
        nm = cls.__name__.lower() + "_" + str(cls._lc_seq)
        src = getattr(cls, "_lc_source", None)
        if src:
            arr = getattr(js.window.lcDatasets, src, None)
            if arr is not None:
                row = js.window.JSON.parse("{}")
                for f in cls._lc_fields:
                    if f.n == "id" and getattr(f, "src", False):
                        # the database gives the id on 💾 Save; a 0 here made a
                        # new family look like an old one (Michel, 2026-10-17)
                        inst._v["id"] = None
                        setattr(row, "id", None)
                        continue
                    v = inst._v.get(f.n, f.d)
                    setattr(row, f.n, "" if f.ref else _lc_cell(f, v))
                _lc_row_mark(row, nm)
                arr.push(row)
                inst._js = row
        globals()[nm] = inst
        _lc_push_obj(inst)
        return inst

    def delete(self):
        """Gone: from the page, the bus and its list."""
        # only a delete asked for leaves the table — never a row that merely
        # vanished from the page (Michel, 2026-10-18: an empty grid after
        # navigating away and back)
        src, rid = getattr(type(self), "_lc_source", None), getattr(self, "_v", {}).get("id")
        ok = getattr(js.window, "lcDeleteOk", None)
        if src and rid is not None and ok is not None:
            ok(src, str(rid))
        _lc_forget(self)
        _lc_publish_class(type(self))

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
            # a part born from a row (a crew's member): its attributes are the row's columns
            row = getattr(self, "_row", None)
            if not row:
                return None
            v = row.get((name[5:] if name.startswith("data-") else name).replace("-", "_"))
            return None if v is None or v == "" else str(v)
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

    def confetti(self):
        """Celebrate from wherever this object is shown. A widget bursts on
        its own element; a MODEL instance bursts on the inspector card that
        displays it (Michel, 2026-09-07: "Congrats! and confettis" when the
        cup is guessed right) — page Python, no js in the page."""
        burst = getattr(js.window, "lcConfetti", None)
        if not burst:
            return self
        el = getattr(self, "_el", None)
        if el is None:
            for elid, pairs in _LC_INSPECT.items():
                if any(inst is self for _, inst in pairs):
                    host = js.window.document.querySelector("[data-lc-inspector='" + elid + "']")
                    # the card REDRAWS right after the verb returns, and a
                    # redraw wipes anything appended inside it — the burst
                    # lands on the card's parent, which survives
                    el = host.parentElement if host is not None else None
                    if el is not None:
                        break
        burst(el if el is not None else js.window.document.body)
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
           methods=["click", "has_class", "confetti"])
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

    def confetti(self):
        """Celebrate from this component — a burst the page chose to earn.
        Put it after the asserts of a final step: it only ever fires when
        everything above it survived."""
        if self._el is not None and getattr(js.window, "lcConfetti", None):
            js.window.lcConfetti(self._el)
        return self


# Author-defined domain classes inherit Object directly — everything is an
# Object. The field machinery (Attr/State storage, registries, _set) lives on
# Object itself; `Model` remains as a compatibility alias.
Model = Object


# ════════════════════════ data + leaf wrappers ══════════════════════════════

# THE KNOBS A LINE CAN WEAR ride the registry (Michel, 2026-10-20: "offer the right
# knobs in the right components"): data=True and attr=<the knob> — the pad's Ctrl+Space,
# the x-ray and tools/component_model.py read this one list; the include that reads
# the attribute stays the behaviour's home.
@component(icon="🛢️", attrs=[{"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"},
                             {"n": "format", "t": "str", "data": True, "attr": "format", "d": 'csv'}, {"n": "path", "t": "str", "data": True, "attr": "path"}, {"n": "refresh", "t": "int", "data": True, "attr": "refresh"}, {"n": "unlisted", "t": "str", "data": True, "attr": "unlisted"}, {"n": "sheet", "t": "str", "data": True, "attr": "sheet"}, {"n": "write", "t": "bool", "data": True, "attr": "write"}])
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

    def row(self, **kw):
        """The first row whose fields match: the object itself when the dataset
        is a class (a class is a dataset), a dict when it is a list —
        self.page.Family.row(family="Nguyen").adopt(),
        self.page.reservations.row(family="Nguyen")["stage"]."""
        ds = getattr(js.window, "lcDatasets", None)
        arr = getattr(ds, self._id, None) if ds else None
        n = int(arr.length) if arr else 0
        for i in range(n):
            r = arr[i]
            if all(str(getattr(r, k, "") if getattr(r, k, None) is not None else "") == str(v)
                   for k, v in kw.items()):
                cls = _CLASSES.get(self._id)
                nm = getattr(r, "obj", None)
                if cls is not None and nm:
                    inst = globals().get(str(nm))
                    if inst is not None:
                        return inst
                return json.loads(str(js.window.JSON.stringify(r)))
        raise AssertionError("no row in " + self.id + " with " +
                             ", ".join(k + "=" + str(v) for k, v in kw.items()))

    def save(self):
        """Send what changed since the list was read — new, changed, gone —
        to the database it lives in; then read it again (💾 Save)."""
        fn = getattr(js.window, "lcDatasetSave", None)
        if fn is not None:
            fn(self._id)

    def reload(self):
        """Read the list again from where it lives (↻)."""
        fn = getattr(js.window, "lcRemoteReload", None)
        if fn is not None:
            fn(self._id)

    def append(self, row):
        """One more row: on the page at once, and — when the list lives in a
        sheet that takes writes — in the sheet too, then read back
        (Michel, 2026-10-16: "an API where data is read but also written")."""
        fn = getattr(js.window, "lcDatasetAppend", None)
        if fn is None:
            raise RuntimeError("this page cannot add rows")
        fn(self._id, json.dumps(row))

    def values(self, field):
        """Every row's value for one field, in order, as strings.

        COUNTING IS NOT ENOUGH. A check could say "nine rows" but not
        "and none of them already went home" — so the first proof a
        learner writes about their own list had nothing to assert on
        (module 05, 2026-08-11). A missing field reads as "", so a
        blank cell and an absent column look the same to a reader,
        which is what a reader means by empty."""
        ds = getattr(js.window, "lcDatasets", None)
        arr = getattr(ds, self._id, None) if ds else None
        if not arr:
            return []
        out = []
        for i in range(int(arr.length)):
            v = getattr(arr[i], field, None)
            out.append("" if v is None else str(v))
        return out


@component(icon="🔎",
           attrs=[{"n": "query", "t": "str"}, {"n": "editable", "t": "bool"},
                  {"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"}],
           assoc=[{"n": "source", "target": "Dataset"}],
           methods=["run"])
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

    def run(self, sql=None):
        """Run SQL in this query — exactly what the reader does by typing in
        the editor and pressing Run. Omit sql to re-run what is there.

        Lets a check rehearse the learner's own move: rewrite the query the
        other way and show that one question, said twice, gives one answer
        (Michel, 2026-09-19). The result is published before this returns,
        so the next step can read it."""
        if self._el is None:
            raise AttributeError("no query #" + str(self._id) + " on this page")
        try:
            fn = self._el._lcRun
        except AttributeError:
            fn = None
        if fn is None:
            raise AttributeError("this query cannot be run from here")
        return str(fn(sql) if sql is not None else fn())


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
                  {"n": "rows", "t": "ref", "list": True},
                  {"n": "title", "t": "str", "data": True, "attr": "title"}, {"n": "height", "t": "int", "data": True, "attr": "height", "d": 400}, {"n": "format", "t": "str", "data": True, "attr": "format", "d": 'yaml'}, {"n": "editable", "t": "bool", "data": True, "attr": "editable"}, {"n": "filter", "t": "str", "data": True, "attr": "filter"}, {"n": "save", "t": "str", "data": True, "attr": "save"}, {"n": "empty", "t": "str", "data": True, "attr": "empty"}, {"n": "hints", "t": "str", "data": True, "attr": "hints"}, {"n": "sort", "t": "str", "data": True, "attr": "sort"}, {"n": "columns", "t": "str", "data": True, "attr": "columns"}, {"n": "dates", "t": "str", "data": True, "attr": "dates"}, {"n": "autocomplete", "t": "bool", "data": True, "attr": "autocomplete"}],
           assoc=[{"n": "source", "target": "Dataset"}, {"n": "master", "target": "Datagrid"}],
           methods=["header", "select", "next"])
class Datagrid(Block):
    # THE SELECTED ROW, READ AND WRITTEN (Michel, 2026-10-09, Module 05:
    # "currentline.met = today's weekday, and select the next line — KISS").
    # `grid.row.met = weekday()` writes into the DATASET the grid shows
    # (through its query, to the base row), so the query re-runs, the grid
    # repaints and every count recounts; `grid.next()` selects the row after
    # the one just written — or the one that slid into its place when the
    # write took it out of the query's answer.
    @property
    def row(self):
        return _Row(self)

    @property
    def saved(self):
        """How many times the learner pressed 💾 Save on this grid (this device)."""
        return _lc_did(self, "save")

    def next(self):
        # True when it moved, False on the last row — so a loop can stop by
        # itself: `while grid.next() and grid.row.met: pass` (Michel,
        # 2026-10-13, Module 05's first loop: skip the families already met)
        door = getattr(self._el, "_lcRow", None) if self._el is not None else None
        if door is None:
            raise AssertionError("#" + str(self.id) + " has no rows to walk yet")
        moved = door.next()
        return moved is not None and bool(moved)

    @property
    def source(self):
        b = self._attr("data-bind") or ""
        # bind="Student" names a CLASS: the source is the model block that
        # declared it — the x-ray pipes grid → model (Michel, 2026-08-24)
        for mid in _LC_DECL:
            if b in _LC_DECL[mid]:
                el = js.window.document.querySelector(
                    ".lc-model[data-lc-id='" + mid + "']")
                if el is not None:
                    return Model(el)
        return Dataset(b)

    def _api(self):
        # AG-backed grids register their api under their id — the honest
        # source inside a synchronous step run, where the DOM's rows only
        # repaint after the run ends.
        md = getattr(js.window, "lcMasterDetail", None)
        if md is None:
            return None
        try:
            return getattr(md._apis, self.id, None)
        except Exception:
            return None

    def _waiting_for(self):
        # the query this grid is bound to, if it is still waiting for one of
        # its own sources — see query.md: it publishes nothing until then
        b = self._attr("data-bind") or ""
        if not b:
            return ""
        q = js.window.document.querySelector(".lc-query[data-lc-id='" + b + "']")
        return (q.getAttribute("data-waiting") or "") if q is not None else ""

    @property
    def row_count(self):
        # a grid whose query is still waiting has NO count yet: 0 would pass
        # a proof early, and a half-computed join failed one for the wrong
        # reason ("12 dog(s) still invisible", Michel 2026-09-16). Name the
        # wait, so the reader runs again once the page has finished loading.
        w = self._waiting_for()
        if w:
            raise AssertionError((self._attr("data-lc-id") or "this grid")
                                 + " is still waiting for " + w
                                 + " - the page has not finished loading; run again")
        # three renderers back a datagrid: the AG api (code-block grids —
        # its row model updates synchronously, the painted rows do not),
        # the custom HTML table (source-bound grids), and painted AG rows
        # as the last resort.
        api = self._api()
        if api is not None:
            try:
                return int(api.getDisplayedRowCount())
            except Exception:
                pass
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

    def select(self, n=1):
        """Select row n (1-based) — what a reader's click does: master-bound
        forms and detail grids receive the row, inside the same step."""
        api = self._api()
        if api is not None:
            node = api.getDisplayedRowAtIndex(n - 1)
            if node is not None:
                node.setSelected(True, True)
                # AG batches its selection event to a later tick — after a
                # synchronous step run has already ended. Publish the row
                # now; the batched event re-publishes the same row, harmless.
                md = getattr(js.window, "lcMasterDetail", None)
                if md is not None:
                    md.publish(self.id, node.data)
                return self
        rows = self._qq("tbody tr") or self._qq(".ag-row")
        if rows and 1 <= n <= len(rows):
            rows[n - 1]._el.click()
        return self


@component(icon="📈",
           attrs=[{"n": "type", "t": "str", "data": True, "d": "bar"},
                  {"n": "x", "t": "str", "data": True, "d": ""},
                  {"n": "y", "t": "str", "data": True, "d": ""},
                  {"n": "bar_count", "t": "int"},
                  {"n": "point_count", "t": "int"},
                  {"n": "height", "t": "int", "data": True, "attr": "height", "d": 300}, {"n": "bars", "t": "str", "data": True, "attr": "bars"}, {"n": "series", "t": "str", "data": True, "attr": "series"}, {"n": "empty", "t": "str", "data": True, "attr": "empty"}],
           assoc=[{"n": "source", "target": "Dataset"},
                  {"n": "master", "target": "Datagrid"},
                  {"n": "bind", "target": "Datagrid"},
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
        """Rects when the chart drew SVG (a bound chart), otherwise the count
        the inline canvas recorded. A chart that is visibly drawing bars must
        never report zero — that turns a page's own proof into a liar."""
        rects = len(self._qq("rect"))
        if rects:
            return rects
        try:
            return int(self._attr("data-lc-bars") or 0)
        except Exception:
            return 0

    @property
    def point_count(self):
        return len(self._qq("circle"))


@component(icon="🦄",
           attrs=[{"n": "title", "t": "str"}, {"n": "status", "t": "str"},
                  {"n": "tags", "t": "str", "data": True, "attr": "tags"}, {"n": "visible", "t": "bool", "data": True, "attr": "visible"}, {"n": "celebration", "t": "bool", "data": True, "attr": "celebration"}, {"n": "pace", "t": "str", "data": True, "attr": "pace"}, {"n": "saves", "t": "str", "data": True, "attr": "saves"}, {"n": "src", "t": "str", "data": True, "attr": "src"}],
           assoc=[{"n": "flow", "target": "EventFlow"}, {"n": "grades", "target": "Mdpad"}],
           methods=["run"])
class Feature(Block):
    _lc_keep = ("tags",)
    @property
    def flow(self):
        """The event flow this feature checks (flow= knob) — Given is the
        setup, When the command, Then the event; the pipe says which story."""
        fid = self._attr("data-flow") or ""
        el = js.window.document.querySelector("[data-lc-id='" + fid + "']")
        return EventFlow(el) if el is not None else None

    @classmethod
    def nth(cls, n=0):
        nl = js.window.document.querySelectorAll(".lc-feature")
        return cls(nl.item(n) if n < int(nl.length) else None)

    @property
    def title(self):
        return str(self._attr("data-title") or "")

    @property
    def status(self):
        v = self._attr("data-status")
        return str(v) if v else "none"

    @property
    def wanted(self):
        """A request from the problem space: steps written, none implemented."""
        return self.status == "wanted"

    @property
    def tags(self):
        return [str(o._el.getAttribute("data-tag") or "") for o in self._qq(".lc-feature-tag")]

    @property
    def text(self):
        """The feature as written — Gherkin only, no step bodies."""
        return str(self._attr("data-gherkin") or "")

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
        # A BARE BODY RUNS AT MODULE SCOPE, `button` in hand — the same
        # contract the JS side runs on a real click, so a proof cannot pass
        # on semantics no reader ever gets. What the lines set, the page
        # reads: `message = …` in a button feeds `{= message }` beside it.
        g = globals()
        g["button"] = self
        try:
            if "def on_click" in code:
                exec(code + "\non_click(button)\n", g)
            else:
                exec(code, g)
        except Exception as _e:
            if self._el:
                self._el.setAttribute("data-lc-err", str(_e))
        try:
            js.window.document.dispatchEvent(js.CustomEvent.new("lc-model-changed"))
        except Exception:
            pass
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
                   "attr": "data-show-private"},
                  {"n": "view", "t": "str", "data": True, "attr": "view"}, {"n": "path", "t": "str", "data": True, "attr": "path"}, {"n": "parent", "t": "bool", "data": True, "attr": "parent"}, {"n": "open", "t": "str", "data": True, "attr": "open"}, {"n": "sort", "t": "str", "data": True, "attr": "sort"}, {"n": "title", "t": "str", "data": True, "attr": "title"}])
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
                  {"n": "height", "t": "int", "data": True, "d": 350},
                  {"n": "tiles", "t": "str", "data": True, "attr": "tiles", "d": 'positron'}, {"n": "bindicon", "t": "str", "data": True, "attr": "bindicon"}, {"n": "bearing", "t": "float", "data": True, "attr": "bearing"}, {"n": "pitch", "t": "float", "data": True, "attr": "pitch"}, {"n": "fit", "t": "bool", "data": True, "attr": "fit"}, {"n": "radius", "t": "float", "data": True, "attr": "radius"}],
           assoc=[{"n": "source", "target": "Dataset"}, {"n": "bind", "target": "Datagrid"}],
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
    def passed(self):
        """Did the learner get it right? READ ONLY, on purpose: a proof may
        ask a quiz how it went, and may never answer it (doctrine 5)."""
        return self._attr("data-passed") == "1"

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


class _Row(object):
    """The datagrid's selected row: grid.row.family reads a field,
    grid.row.met = "Fri" writes it into the dataset behind the grid."""
    def __init__(self, grid):
        object.__setattr__(self, "_grid", grid)

    def _door(self):
        g = self._grid
        door = getattr(g._el, "_lcRow", None) if g._el is not None else None
        if door is None:
            raise AssertionError("#" + str(g.id) + " has no rows yet")
        return door

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        cur = self._door().current()
        d = json.loads(str(js.JSON.stringify(cur))) if cur else {}
        return d.get(name)

    def __setattr__(self, name, value):
        if not self._door().set(name, value):
            raise AssertionError("#" + str(self._grid.id) + ": no selected row to write " + name + " into")


def weekday():
    """Today's weekday as the course's data writes it: Mon, Tue … Sun."""
    return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][int(js.Date.new().getDay())]


def clock():
    """The time now, as a person writes it: "16:05"."""
    d = js.Date.new()
    h, m = int(d.getHours()), int(d.getMinutes())
    return ("0" if h < 10 else "") + str(h) + ":" + ("0" if m < 10 else "") + str(m)


class _Attrs(object):
    """Attribute view over a dict — form.data.url returns that field's value
    (or None). Used by Form.data so handlers read self.page.<form>.data.<field>."""
    def __init__(self, d):
        self._d = d or {}

    def __getattr__(self, name):
        return self._d.get(name)


@component(icon="☷",
           attrs=[{"n": "title", "t": "str", "data": True, "d": ""},
                  {"n": "format", "t": "str", "data": True, "d": "yaml"},
                  {"n": "editable", "t": "bool", "data": True, "d": False},
                  {"n": "compute", "t": "str", "data": True, "attr": "compute"}, {"n": "persist", "t": "str", "data": True, "attr": "persist"}, {"n": "sliders", "t": "bool", "data": True, "attr": "sliders"}, {"n": "options", "t": "str", "data": True, "attr": "options"}, {"n": "min", "t": "float", "data": True, "attr": "min"}, {"n": "max", "t": "float", "data": True, "attr": "max"}, {"n": "step", "t": "float", "data": True, "attr": "step"}],
           assoc=[{"n": "master", "target": "Datagrid"}, {"n": "source", "target": "Dataset"}],
           methods=["submit", "set"])
class Form(Block):
    def __setattr__(self, name, value):
        """`page.ask.name = "Ada"` types the field, like a person would.

        Reading was already pythonistic (`.data.name`); writing needed
        `.set("name", …)`, and Michel wrote the natural line in a scenario
        (2026-09-01) — it set a dead attribute on the wrapper and the form
        never moved. A name that IS one of this form's fields now goes
        through the same edit path a keystroke takes; anything else stays a
        plain attribute, so the wrapper's own internals are untouched.
        """
        if not name.startswith("_"):
            try:
                if name in self.data._d:
                    self.set(name, value)
                    return
            except Exception:
                pass
        object.__setattr__(self, name, value)

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

    def set(self, field, value):
        """Type one field, the way a person does.

        A SCENARIO HAS TO BE ABLE TO ACT. Every When in this course read
        "when the page has settled", which changes nothing, so Given/When/Then
        collapsed into three ways of saying Then (Michel, 2026-08-06). This
        goes through the grid's own edit path — setDataValue, then
        onCellValueChanged, the model, data-lc-value and the lc-model-changed
        bus — so every cell watching this form recomputes exactly as it would
        for a human keystroke. Returns True when the field was found.
        """
        fn = getattr(js.window, "lcFormSet", None)
        if fn is None:
            return False
        # self.id, not self._id — a Form is an element wrapper (Object keeps
        # _el); only Dataset and its kin carry a bare _id string
        return bool(fn(self.id, field, value))

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
                  {"n": "branch", "t": "str", "data": True, "d": "main"},
                  {"n": "bound", "t": "str", "data": True, "d": ""},
                  {"n": "placeholder", "t": "str", "data": True, "d": ""}])
class Code(Block):
    @property
    def text(self):
        """The card's lines."""
        v = self._attr("data-lc-value")
        if not v:
            return ""
        return str(js.JSON.parse(v).text or "")

    @text.setter
    def text(self, v):
        """Write the card's lines — an event's way to show code (an agent's
        on_response: code.text = agent.response.example). The card repaints;
        its ⬇ Add, if bound, offers the new lines."""
        f = getattr(self._el, "_lcSetText", None) if self._el is not None else None
        if f is not None:
            f(str(v))


@component(icon="🤖",
           attrs=[{"n": "system", "t": "long", "data": True, "d": ""},
                  {"n": "model", "t": "str", "data": True, "d": "openai/gpt-4o-mini"},
                  {"n": "temperature", "t": "float", "data": True, "d": 0.7},
                  {"n": "max_tokens", "t": "int", "data": True, "d": 500,
                   "attr": "data-max-tokens"},
                  {"n": "intro", "t": "str", "data": True, "d": ""},
                  {"n": "placeholder", "t": "str", "data": True, "d": "Ask anything..."},
                  {"n": "bot", "t": "str", "data": True, "attr": "bot"}, {"n": "name", "t": "str", "data": True, "attr": "name"}, {"n": "rows", "t": "int", "data": True, "attr": "rows", "d": 3},
                  {"n": "replies", "t": "list"},
                  {"n": "last", "t": "str"},
                  {"n": "asked", "t": "int"}],
           assoc=[{"n": "bound", "target": "Mdpad"}, {"n": "target", "target": "Feature"}],
           events=["on_response"],
           methods=["ask", "clear"])
class Agent(Block):
    """A page agent (.agent) — a part a proof, a guide or another agent can
    act on: read or rewrite its brain (system), ask it, read what it said."""
    _lc_keep = ("system",)

    @property
    def bound(self):
        """The pad it reads (bound=) — the x-ray draws the pipe."""
        return _lc_ref(self, "data-lc-bound")

    @property
    def target(self):
        """The check it aims at (target=)."""
        return _lc_ref(self, "data-lc-target")

    @property
    def asked(self):
        """How many questions the learner asked this agent, on this page."""
        return _lc_did(self, "ask")

    @property
    def response(self):
        """The last answer, cut in its areas: .text (all of it), .direction,
        .question, .example (the lines it offers, a catalogue part expanded).
        What an on_response handler reads."""
        r = getattr(self._el, "_lcResponse", None) if self._el is not None else None
        return _AgentResponse(r)

    @property
    def todos(self):
        """The "# TODO" lines of the editor this agent is bound to, in source
        order — what the tutor scans when asked (todos="true")."""
        label = self._q(".lc-agent-bound")
        m = re.search(r"#([\w-]+)", str(label._el.textContent or "")) if label._el is not None else None
        if not m:
            return []
        ta = js.window.document.querySelector("#lc-pyrun-" + m.group(1) + " .lc-pyrun-code")
        if ta is None:   # a pad: the builder's checklist (- [ ] lines)
            ta = js.window.document.querySelector('.lc-mdpad[data-lc-id="' + m.group(1) + '"] .lc-mdpad-in')
        if ta is None:
            return []
        out = []
        for line in str(ta.value).split("\n"):
            mm = re.match(r"^\s*#\s*[Tt][Oo][Dd][Oo][:\s-]*(.*)$", line)   # MicroPython re: no flags, no \b
            if mm is None:
                mm = re.match(r"^\s*-\s\[ \]\s*(.*)$", line)
            if mm:
                out.append(mm.group(1).strip())
        return out

    @property
    def system(self):
        cfg = getattr(self._el, "_lcCfg", None) if self._el is not None else None
        v = getattr(cfg, "system", None) if cfg is not None else None
        return str(v) if v is not None else str(self._attr("data-system") or "")

    @system.setter
    def system(self, v):
        """Rewrite the instructions the NEXT ask runs under — the assignment
        move: disturb the agent, change its brain, prove the change."""
        if self._el is None:
            return
        cfg = getattr(self._el, "_lcCfg", None)
        if cfg is not None:
            cfg.system = str(v)
        self._el.setAttribute("data-system", str(v))

    @property
    def last(self):
        r = self.replies
        return r[-1] if r else ""

    def clear(self):
        """Forget this sitting's exchanges, so the next verdict is read alone."""
        for sel in (".lc-agent-log-entry", ".lc-agent-msg-bot", ".lc-agent-msg-user"):
            for o in self._qq(sel):
                o._el.remove()
        return self

    @property
    def replies(self):
        """Every answer the agent has given this sitting — the panel shows
        one exchange, the ledger keeps them all, so a rubric can read
        verdict lines out of the whole conversation."""
        out = [m.text for m in self._qq(".lc-agent-log-entry")]
        return out if out else [m.text for m in self._qq(".lc-agent-msg-bot")]

    def _bound_text(self, prompt):
        """What the panel would send: the bound document under review, read
        from the page as it stands, then the request. The expression is the
        panel's own ({= dict(dog=ask.dog, …) }), evaluated over every part
        that publishes its data — forms, documents, feature cards."""
        expr = self._attr("data-bound-expr") or ""
        if not expr:
            return str(prompt)
        ns = {}
        nodes = js.window.document.querySelectorAll("[data-lc-id][data-lc-value]")
        for i in range(int(nodes.length)):
            n = nodes.item(i)
            try:
                ns[str(n.getAttribute("data-lc-id"))] = _Attrs(json.loads(str(n.getAttribute("data-lc-value"))))
            except Exception:
                pass
        cards = js.window.document.querySelectorAll(".lc-feature[data-lc-id]")
        for i in range(int(cards.length)):
            c = cards.item(i)
            cid = str(c.getAttribute("data-lc-id"))
            if cid not in ns:
                ns[cid] = _Attrs({"status": str(c.getAttribute("data-status") or ""),
                                  "title": str(c.getAttribute("data-title") or ""),
                                  "text": str(c.getAttribute("data-gherkin") or "")})
        try:
            v = eval(expr, {"dict": dict, "str": str, "len": len, "int": int, "float": float, "list": list}, ns)
        except Exception as e:
            return str(prompt)
        return "The document under review:\n\n```\n" + str(v) + "\n```\n\nThe request:\n\n" + str(prompt)

    def ask(self, prompt, wait=True):
        """Send a message, as a person would — and, by default, WAIT for the
        answer, so the next line of the scenario can read `last`. The panel
        hands the runtime the exact request it would send; a synchronous
        call carries it and the reply is filed in the panel's own box and
        ledger. wait=False only presses Ask (the prompt box is named: the
        first input in the panel is the key field, not the question)."""
        if self._el is None:
            return self
        api = getattr(self._el, "_lcAgent", None) if wait else None
        req = api.request(self._bound_text(prompt)) if api is not None else None
        if req is not None:
            xhr = js.XMLHttpRequest.new()
            xhr.open("POST", str(req.url), False)
            xhr.setRequestHeader("Authorization", "Bearer " + str(req.token))
            xhr.setRequestHeader("Content-Type", "application/json")
            xhr.send(str(req.body))
            status = int(xhr.status)
            if status < 200 or status >= 300:
                raise AssertionError("the agent's engine answered " + str(status) + " — ask it by hand once, then run again")
            data = json.loads(str(xhr.responseText))
            try:
                text = data["choices"][0]["message"]["content"]
            except Exception:
                raise AssertionError("the agent's engine sent no answer text")
            api.record(str(prompt), str(text))
            return self
        box = self._el.querySelector(".lc-agent-prompt")
        if box is None:
            box = self._el.querySelector("textarea")
        if box is not None:
            box.value = str(prompt)
        self._tap(".lc-agent-send")
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
           attrs=[{"n": "size", "t": "int", "data": True, "attr": "size", "d": 180},
                  {"n": "playing", "t": "bool"},
                  {"n": "speech", "t": "str"},
                  {"n": "dock", "t": "bool", "data": True, "attr": "dock"}, {"n": "autoplay", "t": "bool", "data": True, "attr": "autoplay"}, {"n": "story", "t": "str", "data": True, "attr": "story"}, {"n": "pick", "t": "str", "data": True, "attr": "pick"}, {"n": "src", "t": "str", "data": True, "attr": "src"}],
           assoc=[{"n": "points", "target": "Block", "list": True}],
           methods=["play", "stop", "video"],
           states=["idle", "speaking"])
class Avatar(Block):
    _lc_keep = ("size",)
    def _reg(self):
        regs = getattr(js.window, "_lcAvatars", None)
        aid = self.id
        return getattr(regs, aid, None) if regs is not None and aid else None

    @property
    def playing(self):
        av = self._reg()
        return bool(av.playing) if av is not None else False

    @property
    def points(self):
        """Every part its scripts walk to (at:) — the app it shows, the
        check it runs: the x-ray draws one pipe each."""
        av = self._reg()
        if av is None:
            return []
        scripts = [getattr(av, "script", None), getattr(av, "_tourScript", None)]
        st = getattr(av, "stories", None)
        if st:
            for k in js.window.Object.keys(st):
                scripts.append(getattr(st, k, None))
        out, seen = [], set()
        for sc in scripts:
            if not sc:
                continue
            for i in range(int(sc.length or 0)):
                at = str(getattr(sc[i], "at", "") or "")
                el = js.window.lcAvatarResolve(at) if at else None
                w = _wrap(el) if el else None
                if w is None or type(w) is Block or not w.id or w.id in seen:
                    continue
                seen.add(w.id)
                out.append(w)
        return out

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


@component(icon="✍️", attrs=[{"n": "rows", "t": "int", "data": True},
                             {"n": "save", "t": "str", "data": True, "attr": "save"}, {"n": "comment", "t": "bool", "data": True, "attr": "comment"}, {"n": "replay", "t": "float", "data": True, "attr": "replay", "d": 1.5}, {"n": "decorations", "t": "bool", "data": True, "attr": "decorations"}, {"n": "piano", "t": "bool", "data": True, "attr": "piano"}, {"n": "numbers", "t": "bool", "data": True, "attr": "numbers"}, {"n": "folded", "t": "bool", "data": True, "attr": "folded"}, {"n": "layout", "t": "str", "data": True, "attr": "layout", "d": 'cols'}, {"n": "demo", "t": "str", "data": True, "attr": "demo"},
                             {"n": "rendered", "t": "str"},
                             {"n": "source", "t": "str"},
                             {"n": "titles", "t": "list"},
                             {"n": "sections", "t": "list"},
                             {"n": "bolds", "t": "list"},
                             {"n": "italics", "t": "list"},
                             {"n": "bullets", "t": "list"},
                             {"n": "numbered", "t": "list"},
                             {"n": "links", "t": "list"},
                             {"n": "images", "t": "int"},
                             {"n": "components", "t": "list"},
                             {"n": "versions", "t": "list"},
                             {"n": "replayed", "t": "int"}])
class Mdpad(Block):
    _lc_keep = ("folded", "numbers", "replay")
    # The preview half IS the document being made — every property reads it,
    # so a rubric feature can grade what the learner typed without any js.
    def _preview_texts(self, css):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        if o is None:
            return []
        nl = o.querySelectorAll(css)
        return [str(nl.item(i).textContent or "").strip()
                for i in range(int(nl.length))]

    @property
    def versions(self):
        """The names of the versions the learner kept, newest first — what
        each 💾 said it did. The lesson's starter is not one of them."""
        h = getattr(self._el, "_lcHist", None) if self._el is not None else None
        if h is None:
            return []
        return [str(h[i]) for i in range(int(h.length))]

    @property
    def replayed(self):
        """How many times the film of this pad was played (🎞 / Watch it grow)."""
        return _lc_did(self, "replay")

    @property
    def rendered(self):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        return str(o.textContent or "").strip() if o is not None else ""

    @property
    def source(self):
        """What the learner actually typed — for criteria about HOW the
        markdown is written, not just what it renders to."""
        ta = self._el.querySelector(".lc-mdpad-in") if self._el is not None else None
        return str(ta.value) if ta is not None else ""

    @source.setter
    def source(self, text):
        """Write the pad as a person would: one render, now — the preview,
        its model and its wires follow (pad.broken says which hang)."""
        f = getattr(self._el, "_lcApply", None) if self._el is not None else None
        if f is not None:
            f(str(text))

    def painted(self, kind):
        """The source's painted tokens of one kind, in order — 'cls' for the
        decorations' classes ('.pitch'), 'id', 'key', 'val', 'fence', 'h',
        'link', 'ial' (whole decoration lines)."""
        k = self._el.querySelector(".lc-mdpad-piano") if self._el is not None else None
        if k is None:
            return []
        nl = k.querySelectorAll(".md-" + str(kind))
        return [str(nl.item(i).textContent or "") for i in range(int(nl.length))]

    @property
    def broken(self):
        """The wires to nothing in the preview, as the pad draws them:
        ['source «pets»'] — a renamed or deleted id shows here at once."""
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        if o is None:
            return []
        nl = o.querySelectorAll("[data-lc-broken]")
        out = []
        for i in range(int(nl.length)):
            for part in str(nl.item(i).getAttribute("data-lc-broken") or "").split(", "):
                if part:
                    out.append(part)
        return out

    @property
    def caret(self):
        """Where the caret is in the source, as a character offset."""
        ta = self._el.querySelector(".lc-mdpad-in") if self._el is not None else None
        return int(ta.selectionStart) if ta is not None else 0

    @caret.setter
    def caret(self, pos):
        """Move the caret the way a person would — the pad then shows the
        caret's block on both sides (pad.focus, pad.focused, pad.keys)."""
        f = getattr(self._el, "_lcCaret", None) if self._el is not None else None
        if f is not None:
            f(int(pos))

    @property
    def focus(self):
        """The block the caret is in, counted as the preview counts them;
        None on a blank line."""
        v = self._attr("data-lc-focus")
        return int(v) if v not in (None, "") else None

    @property
    def focused(self):
        """The preview element wearing the pulse, or None."""
        o = self._el.querySelector(".lc-mdpad-out .lc-mdpad-focus") if self._el is not None else None
        return _wrap(o) if o is not None else None

    @property
    def keys(self):
        """The piano: one class string per block ('k0' / 'k1', the caret's
        block with ' now'), in source order. Empty without piano= or numbers=."""
        nl = self._el.querySelectorAll(".lc-mdpad-piano > div") if self._el is not None else None
        out = []
        if nl is not None:
            for i in range(int(nl.length)):
                c = str(nl.item(i).className or "")
                if not c.startswith("ln"):
                    out.append(c)
        return out

    # ── ✎ fold: the editor tucks away, the preview takes the whole width ──
    @property
    def folded(self):
        """True while the editor is folded away and the preview alone shows."""
        return self._attr("data-lc-folded") == "1"

    def fold(self):
        f = getattr(self._el, "_lcFold", None) if self._el is not None else None
        if f is not None:
            f(True)

    def unfold(self):
        f = getattr(self._el, "_lcFold", None) if self._el is not None else None
        if f is not None:
            f(False)

    # ── 🎞 replay: the saved versions as frames, read-only ──
    def replay(self):
        """Press 🎞 — the frames load (a promise the page resolves), the
        pane turns into a diff pane and the slider appears."""
        r = getattr(self._el, "_lcReplay", None) if self._el is not None else None
        return r.start() if r is not None else None

    def stop(self):
        r = getattr(self._el, "_lcReplay", None) if self._el is not None else None
        if r is not None:
            r.stop()

    @property
    def replaying(self):
        return self._attr("data-lc-replay") == "1"

    @property
    def frames(self):
        v = self._attr("data-lc-frames")
        return int(v) if v else 0

    @property
    def frame(self):
        """The frame shown, counted from zero (the starter); None when not replaying."""
        v = self._attr("data-lc-frame")
        return int(v) if v not in (None, "") else None

    @frame.setter
    def frame(self, n):
        r = getattr(self._el, "_lcReplay", None) if self._el is not None else None
        if r is not None:
            r.go(int(n))

    @property
    def diff(self):
        """The diff pane, one (sign, line) per row: '+' came, '-' went, ' ' stayed."""
        nl = self._el.querySelectorAll(".lc-mdpad-diff .ln") if self._el is not None else None
        out = []
        if nl is not None:
            for i in range(int(nl.length)):
                sp = nl.item(i); c = str(sp.className or ""); t = str(sp.textContent or "")
                out.append(("+" if " add" in c else "-" if " del" in c else " ", t))
        return out

    @property
    def numbers(self):
        """The line numbers the gutter shows, in order."""
        nl = self._el.querySelectorAll(".lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln") if self._el is not None else None
        return [int(nl.item(i).getAttribute("data-n")) for i in range(int(nl.length))] if nl is not None else []

    @property
    def titles(self):
        """The # lines — a page opens with exactly one."""
        return self._preview_texts("h1")

    @property
    def sections(self):
        """The ## lines — the document's real structure."""
        return self._preview_texts("h2")

    @property
    def bolds(self):
        return self._preview_texts("strong, b")

    @property
    def italics(self):
        return self._preview_texts("em, i")

    @property
    def bullets(self):
        """Unordered list items — the • kind."""
        return self._preview_texts("ul li")

    @property
    def numbered(self):
        """Ordered list items — the 1. 2. 3. kind, where rank matters."""
        return self._preview_texts("ol li")

    @property
    def links(self):
        return self._preview_texts("a")

    @property
    def images(self):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        return int(o.querySelectorAll("img").length) if o is not None else 0

    @property
    def components(self):
        """The live components in the preview (decorations="true"), by kind:
        ['cards', 'pitch'] — a fence the learner decorated came alive."""
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        if o is None:
            return []
        kinds = []
        # A plain link-button is the one part whose class carries no lc-
        # prefix ({: .button }); a learner's first decoration must count.
        for token, cls in _WRAP:
            name = cls.__name__.lower()
            if (token.startswith("lc-") or token == "button") and name not in kinds \
                    and o.querySelector("." + token) is not None:
                kinds.append(name)
        return sorted(kinds)


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


def _lc_doc_data(obj):
    """The problem-space documents register their data as a dataset under
    their own id — hand back that JS object so a proof asserts on fields
    (self.page.<id>.data.name), not markup."""
    ds = getattr(js.window, "lcDatasets", None)
    eid = obj._attr("data-lc-id") or ""
    return getattr(ds, eid, None) if (ds and eid) else None


def _lc_ref(obj, attr):
    gid = obj._attr(attr) or ""
    el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
    return _wrap(el)


@component(icon="👤",
           assoc=[{"n": "source", "target": "Form"}])
class Persona(Block):
    """Empathy-map card (.persona) — who the product serves."""
    @property
    def data(self):
        return _lc_doc_data(self)

    @property
    def source(self):
        return _lc_ref(self, "data-bind")


@component(icon="✨",
           assoc=[{"n": "source", "target": "Form"},
                  {"n": "persona", "target": "Persona"}])
class Pitch(Block):
    """Assembled two-sentence pitch (.pitch) — why the product exists."""
    @property
    def data(self):
        return _lc_doc_data(self)

    @property
    def source(self):
        return _lc_ref(self, "data-bind")

    @property
    def persona(self):
        return _lc_ref(self, "data-persona")

    @property
    def drifting(self):
        """True while the who/need stopped echoing the persona this pitch
        reads — the soft warning a proof can assert on."""
        w = self._el.querySelector(".lc-pitch-warn") if self._el is not None else None
        return bool(w is not None and w.hasAttribute("hidden") is False)


@component(icon="🎯",
           assoc=[{"n": "pitch", "target": "Pitch"}])
class ImpactMap(Block):
    """Impact map (.impact_map) — goal → who → how → what."""
    @property
    def pitch(self):
        return _lc_ref(self, "data-pitch")

    @property
    def features(self):
        """The features its leaves name, in map order — the link from the
        problem space to the solution. A leaf whose card is missing wraps
        None, so .exists says so."""
        out = []
        for o in self._qq(".lc-imap-what a[data-feature]"):
            fid = str(o._el.getAttribute("data-feature") or "")
            el = js.window.document.querySelector(".lc-feature[data-lc-id='" + fid + "']")
            out.append(Feature(el))
        return out


@component(icon="🎏", attrs=[{"n": "count", "t": "int"}],
           assoc=[{"n": "map", "target": "ImpactMap"}])
class EventFlow(Block):
    """Event-storming sequence (.event_flow) — the page's story as
    colored notes. One beat, under the user who gives it:
    ui|data → command → [rule] → event."""
    @property
    def count(self):
        return len(self._qq(".lc-ef-step"))

    def kinds(self):
        """The sequence of note kinds, in order — so a proof can assert
        the grammar (a command before its event, a rule that governs a
        command rather than issuing one)."""
        return [str(o._el.getAttribute("data-kind") or "") for o in self._qq(".lc-ef-step")]

    @property
    def map(self):
        """The impact map this story tells (map= knob) — each beat serves
        an impact; the pipe says which map."""
        mid = self._attr("data-map") or ""
        el = js.window.document.querySelector("[data-lc-id='" + mid + "']")
        return ImpactMap(el) if el is not None else None

    def elements(self):
        """The flow's cast — every ‘— ref’ tail, collected: #blocks, classes,
        Class.commands, Class[states]. The meta level checks each one against
        the page's own artifacts."""
        return [{"kind": str(o._el.getAttribute("data-el-kind") or ""),
                 "ref": str(o._el.getAttribute("data-el-ref") or "")}
                for o in self._qq(".lc-ef-el")]


@component(icon="🗄️", attrs=[{"n": "unlisted", "t": "str", "data": True, "attr": "unlisted"}, {"n": "live", "t": "bool", "data": True, "attr": "live"}])
class Database(Block):
    """The database line (.database): a link whose scheme says the kind, an
    unlisted name that opens its tables, live="true" to hear their changes."""
    pass


@component(icon="📡", attrs=[{"n": "exports", "t": "str", "data": True, "attr": "exports"}], assoc=[{"n": "model", "target": "Model"}, {"n": "pages", "target": "Dataset"}])
class Server(Block):
    """The server line (.server): serves a model at lc://<name>, and the
    pages a dataset lists (pages=, rows of path and file); what it knows
    hangs under its id — traffic, clients, contract, pages."""
    pass


@component(icon="🧑‍🤝‍🧑",
           attrs=[{"n": "stages", "t": "str", "data": True, "attr": "stages"},
                  {"n": "tries", "t": "int", "data": True, "attr": "tries", "d": 2},
                  {"n": "budget", "t": "int", "data": True, "attr": "budget", "d": 6},
                  {"n": "fallback", "t": "str", "data": True, "attr": "fallback"},
                  {"n": "text", "t": "str", "data": True, "attr": "text", "d": "message"},
                  {"n": "pace", "t": "float", "data": True, "attr": "pace", "d": 0.5}],
           assoc=[{"n": "members", "target": "Agent", "list": True}, {"n": "inbox", "target": "Dataset"}],
           methods=["run"])
class Crew(Agent):
    """A crew (.crew) is an agent made of agents (Michel, 2026-10-24: "the
    crew should inherit from agent"): its members are agents, their
    attributes the columns of a dataset (members=), run over an inbox with clear bounds — tries= per message,
    budget= AI asks in all, fallback= for what stays open. It has an agent's
    desk and key; its provider, model, temperature and max_tokens are its
    members' defaults. It writes <id>.sorted and <id>.log, nothing else."""
    @property
    def asked(self):
        """The AI asks this crew made, in its last run."""
        return self.asks

    @property
    def replies(self):
        """What its members said, step by step, in its last run."""
        return [str(v) for v in self.log.values("out")]

    @property
    def last(self):
        r = self.replies
        return r[-1] if r else ""

    def ask(self, prompt, wait=True):
        raise AssertionError("a crew works its inbox, not one question — put the message in the inbox, then run()")

    @property
    def members(self):
        """Its members: a list of agents (Michel, 2026-10-24: "Crew's members
        is a list of agents") — the composite: a crew is an agent made of
        agents, so a member may one day be a crew itself (the tree)."""
        ds = getattr(js.window, "lcDatasets", None)
        arr = getattr(ds, self._attr("members") or "members", None) if ds else None
        rows = json.loads(str(js.JSON.stringify(arr))) if arr else []
        return [_lc_agent_of(r) for r in rows if isinstance(r, dict)]


    @property
    def sorted(self):
        return Dataset(str(self.id) + ".sorted")

    @property
    def log(self):
        return Dataset(str(self.id) + ".log")

    @property
    def asks(self):
        return int(self._attr("data-asks") or 0)

    @property
    def tokens(self):
        return int(self._attr("data-tokens") or 0)

    @property
    def done(self):
        return self._attr("data-state") == "done"

    def run(self):
        """Press ▶ Run, as a person would; the crew works on, the page repaints."""
        self._tap(".lc-crew-run")
        return self


def _lc_agent_of(row):
    """An agent whose attribute values come from a row — data-driven: a crew's
    members are agents, their name, system, model… the columns of a csv."""
    a = Agent(None)
    a._row = row
    return a


@component(icon="🗺", attrs=[{"n": "scope", "t": "str", "data": True, "attr": "scope"}, {"n": "states", "t": "bool", "data": True, "attr": "states", "d": True}])
class Diagram(Block):
    """The model, drawn (.diagram): scope= a class, a package or *; states=
    off hides the state machines."""
    pass


@component(icon="🏛️",
           attrs=[{"n": "classes", "t": "str"}],
           assoc=[{"n": "source", "target": "Database"}])
class Model(Block):
    """The page's declarations (.model) — classes and singletons, invisible
    on the page like a dataset: structure, not ink. Widgets point at it
    with source=, the x-ray docks it (Michel, 2026-08-24)."""
    @property
    def classes(self):
        return " ".join(_LC_DECL.get(self.id) or [])


@component(icon="🧬",
           attrs=[{"n": "cards", "t": "int"}, {"n": "follows", "t": "str"}],
           assoc=[{"n": "grid", "target": "Datagrid"},
                  {"n": "source", "target": "Model"}],
           methods=["bind"])
class Inspector(Block):
    """Model widget (.inspector) — live cards over the objects its fence
    builds; follow= makes it a claimed grid's detail form. It POINTS at the
    model block as its source — the declarations stay the SSOT, the widget
    only shows them, and the x-ray pipes the flow."""
    @property
    def cards(self):
        return len(self._qq("[data-card]"))

    @property
    def follows(self):
        return str(self._attr("data-bound-to") or "")

    @property
    def grid(self):
        gid = self._attr("data-bound-to") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']")
        return Datagrid(el) if el is not None else None

    @property
    def source(self):
        mid = self._attr("data-bind") or ""
        el = js.window.document.querySelector(".lc-model[data-lc-id='" + mid + "']")
        return Model(el) if el is not None else None


def _lc_named(expr):
    """The parts a formula names by id — a component on the page, or a
    dataset registered under that name. `form.field` names the form only."""
    out, seen, i, n = [], set(), 0, len(expr)
    ds = getattr(js.window, "lcDatasets", None)
    while i < n:
        ch = expr[i]
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (expr[j].isalpha() or expr[j].isdigit() or expr[j] == "_"):
                j += 1
            tok, after_dot = expr[i:j], i > 0 and expr[i - 1] == "."
            i = j
            if after_dot or tok in seen:
                continue
            seen.add(tok)
            el = js.window.document.querySelector("[data-lc-id='" + tok + "']")
            if el is not None:
                w = _wrap(el)
                if type(w) is not Block:
                    out.append(w)
            elif ds is not None and getattr(ds, tok, None) is not None:
                out.append(Dataset(tok))
        elif ch in "'\"":                      # a string literal names nothing
            j = expr.find(ch, i + 1)
            i = n if j < 0 else j + 1
        else:
            i += 1
    return out


@component(icon="🧮",
           attrs=[{"n": "formula", "t": "str"}, {"n": "value", "t": "str"}],
           assoc=[{"n": "reads", "target": "Block", "list": True}])
class Cell(Block):
    """An inline cell {= expr } — its formula, its value, and every part
    the formula reads (the x-ray draws one pipe each)."""
    @property
    def formula(self):
        return self._attr("data-expr") or ""

    @property
    def value(self):
        return self.text

    @property
    def reads(self):
        return _lc_named(self.formula)


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
    ("lc-persona", Persona), ("lc-pitch", Pitch), ("lc-imap", ImpactMap),
    ("lc-event-flow", EventFlow), ("lc-inspector", Inspector),
    ("lc-model", Model), ("lc-cell", Cell),
    ("lc-database", Database), ("lc-server", Server), ("lc-crew", Crew),
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
            v = getattr(obj, role)
        except Exception:
            v = None
        if is_list and isinstance(v, (list, tuple)):
            for it in v:                       # one pipe per item, its live class
                tid = _lcx_target_id(it)
                if tid:
                    links.append({"role": role, "target": type(it).__name__,
                                  "id": tid, "list": True})
            continue
        tid = _lcx_target_id(v)
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
    if cls_name == "Class":
        # the target IS a class — Class is a component type (inheriting
        # Object); its panel shows the declaration, docked like any other
        # page-invisible source (Michel, 2026-08-23)
        sp = _MODEL.get(idv)
        if not sp:
            return "{}"
        vals = {"name": idv,
                "attrs": " ".join(a["n"] for a in sp.get("attrs", [])),
                "states": " → ".join(sp.get("states", [])),
                "methods": " ".join(m["n"] for m in sp.get("methods", []))}
        return json.dumps({"cls": "Class", "vals": vals, "events": {},
                           "links": [], "state": ""})
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


# every block a run reads by name — the data a proof stands on is whatever
# its steps touched, walked upstream to the block that saves it (feature.md)
_LC_TOUCHED = []


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
        _LC_TOUCHED.append(name)
        # a server or a remote model imported with a link: self.page.demo.traffic, self.page.m.Tally
        if name in _LC_REMOTE:
            return _LC_REMOTE[name]
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
        # AN #id IS THE AUTHOR'S NAME FOR A THING, component or not. Only
        # upgraded components carry data-lc-id, so a plain `{: .block #tally }`
        # — a list, a paragraph — was unreachable from a check even though the
        # author had named it (2026-08-06, writing module 02 page 3: the three
        # counted lines are prose, and the check has to read them). Last
        # resort, so nothing above changes meaning.
        plain = js.window.document.getElementById(name)
        if plain:
            return Block(plain)
        raise AttributeError("no component or #id='" + name + "' on this page")

    def feature(self, n=0):
        return Feature.nth(n)

    def features(self):
        return Feature._all(".lc-feature")


def this_year():
    """The year on the reader's own clock — so a story can ask for a date
    from the future without any js in the page. 0 when the clock is
    unreadable, which no honest year ever is."""
    try:
        s = str(js.window.Date())
    except Exception:
        return 0
    for w in s.replace(",", " ").split():
        if len(w) == 4 and w.isdigit():
            return int(w)
    return 0


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
            d["v"] = _lc_cell(f, v)
        fields.append(d)
    # the state axis is special — it carries the state, so it closes the card
    fields = ([f for f in fields if not f.get("state")]
              + [f for f in fields if f.get("state")])
    meths = []
    tmeta = cls._lc_tmeta or {}

    def _doc1(n):
        # the verb's own first docstring line rides to the button as its
        # tooltip — "Reads X. Writes Y." — so what a press touches is said
        # where it is pressed, and can never drift from the spec (Michel,
        # 2026-09-04: "tooltips … to explicit if it's read or write")
        try:
            d = getattr(getattr(cls, n), "__doc__", "") or ""
        except Exception:
            d = ""
        return str(d).strip().split("\n")[0].strip()

    for n in sorted(tmeta, key=lambda k: tmeta[k][3]):
        pre, post, sfn, _o = tmeta[n]
        cur = obj._v.get(sfn) if sfn else None
        meths.append({"n": n, "pre": pre, "post": post, "doc": _doc1(n),
                      "enabled": (not pre) or (cur in pre)})
    for n in _lc_verbs(cls):
        if n not in tmeta:
            meths.append({"n": n, "pre": [], "post": None, "doc": _doc1(n),
                          "enabled": True})
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


def _lc_props(cls):
    """The class's computed columns: the @property methods its source (and
    its bases') declares, in the order written — never the engine's own
    properties (id, state, text…), which no page wrote."""
    fn = getattr(js.window, "lcPropsOf", None)
    if fn is None:
        return []
    arr = fn(cls.__name__)
    out = []
    for i in range(int(arr.length)):
        n = str(arr[i])
        try:
            if isinstance(getattr(cls, n), property):
                out.append(n)
        except Exception:
            pass
    return out


def _lc_prop_value(o, n):
    try:
        v = getattr(o, n)
    except Exception:
        return ""
    if v is None or isinstance(v, (int, float, str, bool)):
        return v
    return _lc_name_of(v) or str(v)


def _lc_rows_of(cls):
    """The class's collection as rows — NAMED instances only, so a feature's
    throwaway objects never pollute the roster. One column per Attr (state
    fields included), plus obj = the instance's bound name."""
    rows = []
    for o in _LC_OBJS:
        if isinstance(o, cls):
            nm = _lc_name_of(o)
            if not nm:
                continue
            row = _ODict()
            row["obj"] = nm
            fields = cls._lc_fields
            if type(o) is not cls:
                row["_kind"] = type(o).__name__   # a subclass rides in its parent's list,
                fields = getattr(type(o), "_lc_fields", None) or fields   # with its own fields too
            for f in fields:
                v = o._v.get(f.n)
                row[f.n] = (_lc_name_of(v) or "?") if f.ref and v is not None else _lc_cell(f, v)
            for n in _lc_props(type(o)):
                if n not in row:
                    row[n] = _lc_prop_value(o, n)
            rows.append(row)
    return rows


def _lc_publish_class(cls):
    """SSOT projection: the dataset bus carries the class's live collection
    under the class name, so every dataset consumer — grids, charts, forms —
    works on models with zero column declarations (Michel, 2026-08-22).
    A class that WEARS a dataset (source=) writes its objects back into the
    list's own rows first, so the list and the class are one set of rows
    and every consumer of either recounts (Michel, 2026-10-15)."""
    fn = getattr(js.window, "lcSetDataset", None)
    if fn is None or not getattr(cls, "_lc_fields", None):
        return
    src = getattr(cls, "_lc_source", None)
    if src:
        arr = getattr(js.window.lcDatasets, src, None)
        if arr is not None:
            db = _lc_isdb(src)
            for o in _LC_OBJS:
                if isinstance(o, cls) and getattr(o, "_js", None) is not None:
                    for f in cls._lc_fields:
                        v = o._v.get(f.n, f.d)
                        if f.n == "id" and db:
                            # the table gives the id; a new object has none — never a
                            # default (Michel, 2026-10-17: a new Sprint got id 0, read
                            # as saved, never sent, gone on refresh)
                            setattr(o._js, "id", o._v.get("id"))
                            continue
                        if f.ref and db:
                            # the table keeps the id; an id not yet resolved stays as read
                            if v is not None and hasattr(v, "_v"):
                                val = v._v.get("id")
                            else:
                                val = (getattr(o, "_lc_raw", None) or {}).get(f.n)
                            setattr(o._js, f.n, "" if val is None else val)
                            continue
                        setattr(o._js, f.n, (_lc_name_of(v) or "") if f.ref and v is not None else _lc_cell(f, v))
                    if db:
                        # which subclass this row is; the base class writes none — but a
                        # name no class answers to stays as read, for the author's 🧹
                        base = _LC_SOURCED.get(src, "")
                        if type(o).__name__ != base:
                            setattr(o._js, "_sub", type(o).__name__)
                        else:
                            cur = getattr(o._js, "_sub", None)
                            known = [c.__name__ for c in _lc_subs(type(o))] + [getattr(c, "was", None) for c in _lc_subs(type(o))]
                            if not cur or str(cur) in known:
                                setattr(o._js, "_sub", "")
            # the bus listener that adopts rows must not re-adopt our own write
            js.window._lcModelWriting = 1
            try:
                fn(src, arr)
            finally:
                js.window._lcModelWriting = 0
    _lc_model_spec_push(cls)
    rows = _lc_rows_of(cls)
    if rows or src:
        fn(cls.__name__, js.window.JSON.parse(json.dumps(rows)))
    # a subclass's object lives in its parent's list: the parent's grid recounts
    owner = globals().get(_LC_SOURCED.get(src, "")) if src else None
    if isinstance(owner, type) and owner is not cls and issubclass(cls, owner):
        _lc_publish_class(owner)


def _lc_subs(cls):
    """The page's subclasses of cls, harvested — ➕ New offers each one
    (Michel, 2026-10-16)."""
    out = []
    for k, v in list(globals().items()):
        if k.startswith("_") or not isinstance(v, type) or v is cls:
            continue
        try:
            if not issubclass(v, cls):
                continue
        except Exception:
            continue
        if getattr(v, "_lc_harvested_for", None) is not v:
            component(icon="📦")(v)
        out.append(v)
    out.sort(key=lambda c: c.__name__)
    return out


def _lc_model_spec_push(cls, subs=True):
    """What a grid needs to dress a class's rows: the fields with their type
    and lock, the state axis and its transitions, the plain verbs, and the
    subclasses ➕ New may make."""
    if getattr(js.window, "lcModels", None) is None:
        js.window.lcModels = js.window.JSON.parse("{}")
    kids = _lc_subs(cls) if subs else []
    for k in kids:
        _lc_model_spec_push(k, False)
    statef = getattr(cls, "_lc_statef", None)
    tmeta = getattr(cls, "_lc_tmeta", {}) or {}
    fields = {}
    fmap0 = set(f.n for f in cls._lc_fields)
    for f in cls._lc_fields:
        dbid = f.n == "id" and bool(getattr(f, "src", False))   # the table's own id: kept, never shown
        fields[f.n] = {"t": f.t, "enum": f.enum, "ro": f.ro or dbid, "state": f.is_state,
                       "src": bool(getattr(f, "src", False)), "hidden": dbid or bool(getattr(f, "hidden", False)),
                       "ref": f.t if f.ref else None, "was": getattr(f, "was", None),
                       "req": bool(getattr(f, "required", False))}
    # A COMPUTED COLUMN (Michel, 2026-10-17: "add an example of a computed
    # column — @property?"): each property is a read-only column, worked out
    # from the object, never stored
    # — and one with a setter is edited through it (Michel, 2026-10-17:
    # "go setter"): the setter writes the real attributes, those are saved
    props = _lc_props(cls)
    for n in props:
        if n not in fields:
            hs = getattr(js.window, "lcHasSetter", None)
            ro = not (hs is not None and bool(hs(cls.__name__, n)))
            bs = getattr(js.window, "lcBadSetter", None)
            bad = str(bs(cls.__name__, n) or "") if (ro and bs is not None) else ""
            if bad and (cls.__name__, n, bad) not in _LC_SETTER_SAID:
                # @who.setter over def setwho: who stays read-only — said once, plainly
                _LC_SETTER_SAID.append((cls.__name__, n, bad))
                _lc_say(cls.__name__, "⚠️ " + n + " stays read-only: its setter is named " + bad
                        + " — under @" + n + ".setter write def " + n + "(self, value):")
            fields[n] = {"t": "str", "enum": None, "ro": ro, "state": False, "src": False,
                         "hidden": False, "ref": None, "was": None, "computed": True}
    trans = {}
    for n in sorted(tmeta, key=lambda k: tmeta[k][3]):
        pre, post, sfn, _o = tmeta[n]
        trans[n] = {"pre": list(pre), "post": post}
    verbs = [n for n in _lc_verbs(cls) if n not in tmeta]
    spec = {"fields": fields, "state": statef.n if statef else None,
            "states": list(statef.enum) if statef else [], "transitions": trans,
            "verbs": verbs, "src": getattr(cls, "_lc_source", None) or "",
            "was": getattr(cls, "was", None) if isinstance(getattr(cls, "was", None), str) else None,
            "subs": [k.__name__ for k in kids], "order": [f.n for f in cls._lc_fields] + [n for n in props if n not in fmap0]}
    setattr(js.window.lcModels, cls.__name__, js.window.JSON.parse(json.dumps(spec)))


# ── a class is a dataset (Michel, 2026-10-15) ────────────────────────────────
# class Family(Object, source="reservations"): the list's rows become Family
# objects, its columns Family's fields, nothing redeclared; the class adds the
# state and the verbs. The runner rewrites the class line (MicroPython takes no
# keyword there) and calls _lc_source_bind after the body.

def _lc_row_mark(row, nm=None):
    """The object's name on its js row — a non-enumerable property, so no
    grid ever shows it as a column."""
    if nm is None:
        v = getattr(row, "_lcObj", None)
        return str(v) if v else ""
    js.window.Object.defineProperty(row, "_lcObj",
        js.window.JSON.parse(json.dumps({"value": nm, "configurable": True})))
    return nm


def _lc_source_fields(cls, row0, src):
    """Columns the class does not declare become its fields, typed by the
    first row — the source brings what it knows. Declared fields keep their
    column's place; the list's order is the class's order. A column whose
    name starts with "_" is the source's own note (a database's stamp): it
    never becomes a field."""
    keys = js.window.Object.keys(row0)
    order = [str(keys[i]) for i in range(int(keys.length))]
    fmap = cls._lc_fmap
    for c in order:
        if c == "obj" or c == "⚠️" or c in fmap or c.startswith("_"):
            continue
        v = getattr(row0, c, None)
        t = "bool" if isinstance(v, bool) else ("int" if isinstance(v, int)
            else "float" if isinstance(v, float) else "str")
        f = Attr(t, None, hint="a column of " + src)
        f.n = c
        f.src = True
        setattr(cls, c, _lc_field_prop(f))
        cls._lc_fields.append(f)
        fmap[c] = f
        d = f._spec_dict()
        d["src"] = True
        cls._spec["attrs"].append(d)
    # a database hands its columns back alphabetically: there the class's
    # own order wins, the table's extra columns after (Michel, 2026-10-17)
    isdb = getattr(js.window, "lcIsDb", None)
    if isdb is not None and bool(isdb(src)):
        cls._lc_fields = ([f for f in cls._lc_fields if not getattr(f, "src", False)]
                          + [fmap[c] for c in order if c in fmap and getattr(fmap[c], "src", False)])
        # a column no attribute declares (a deleted or renamed one) is kept by
        # the table and shown by no grid (register P5); 🧹 offers to drop it
        for f in cls._lc_fields:
            if getattr(f, "src", False) and f.n != "id":
                f.hidden = True
        return
    cls._lc_fields = ([fmap[c] for c in order if c in fmap]
                      + [f for f in cls._lc_fields if f.n not in order])


def _lc_forget(o):
    cls = type(o)
    while o in _LC_OBJS:
        _LC_OBJS.remove(o)
    g = globals()
    for k in list(g):
        if g[k] is o and not k.startswith("_"):
            del g[k]
    for elid, pairs in list(_LC_INSPECT.items()):
        _LC_INSPECT[elid] = [(n, i) for n, i in pairs if i is not o]
    row = getattr(o, "_js", None)
    src = getattr(cls, "_lc_source", None)
    if row is not None and src:
        arr = getattr(js.window.lcDatasets, src, None)
        nm = _lc_row_mark(row)
        if arr is not None and nm:
            for i in range(int(arr.length)):
                if _lc_row_mark(arr[i]) == nm:
                    arr.splice(i, 1)
                    break
        o._js = None


def _lc_forget_class(name):
    """A class whose block left the page (renamed, deleted, retyped): gone
    from the registries, the globals, the bus and the diagrams — a renamed
    Company left a ghost per keystroke (Michel, 2026-10-16)."""
    cls = globals().get(name)
    for reg in (_MODEL, _CLASSES):
        if name in reg:
            del reg[name]
    if isinstance(cls, type):
        for o in list(_LC_OBJS):
            if type(o) is cls:
                _lc_forget(o)
        for src in list(_LC_SOURCED):
            if _LC_SOURCED[src] == name:
                del _LC_SOURCED[src]
        if globals().get(name) is cls:
            del globals()[name]
    for k in list(_LC_DECL):
        _LC_DECL[k] = [n for n in _LC_DECL[k] if n != name]
    w = js.window
    if getattr(w, "lcModels", None) is not None and getattr(w.lcModels, name, None) is not None:
        js.Reflect.deleteProperty(w.lcModels, name)
    if getattr(w.lcDatasets, name, None) is not None:
        js.Reflect.deleteProperty(w.lcDatasets, name)


def _lc_source_bind(cls_name, src):
    cls = globals().get(cls_name)
    if not isinstance(cls, type):
        raise NameError(cls_name + " is not a class on this page")
    if getattr(cls, "_lc_harvested_for", None) is not cls:
        component(icon="📦")(cls)
    cls._lc_source = src
    cls._lc_seq = getattr(cls, "_lc_seq", 0)
    _LC_SOURCED[src] = cls_name
    # the class says what it is before its rows arrive: a table that waits
    # for the class's attributes (to make its columns) must not wait for rows
    _lc_model_spec_push(cls)
    _lc_source_sync(src)


def _lc_isdb(src):
    fn = getattr(js.window, "lcIsDb", None)
    return fn is not None and bool(fn(src))


def _lc_ref_by_id(tname, v):
    """A REFERENCE ON A DATABASE (Michel, 2026-10-17: a walk's dog, picked
    from the shelter's dogs): the table keeps the dog's id; the object holds
    the dog itself."""
    rc = globals().get(tname)
    if not isinstance(rc, type) or v is None or v == "":
        return None
    for o in _LC_OBJS:
        if isinstance(o, rc) and str(o._v.get("id")) == str(v):
            return o
    return None


_LC_RESYNC = [False]


def _lc_source_sync(src):
    """The list moved (arrived, a bare edit, a new row): wrap the rows that
    have no object yet, refresh the ones that do, forget the ones that went.
    A raw cell wins over the type here — the bare list has no manners."""
    cls_name = _LC_SOURCED.get(src)
    cls = globals().get(cls_name) if cls_name else None
    if cls is None:
        return
    arr = getattr(js.window.lcDatasets, src, None)
    if arr is None:
        return
    n = int(arr.length)
    if n:
        _lc_source_fields(cls, arr[0], src)
    db = _lc_isdb(src)
    g = globals()
    kept = []
    # a table read again hands back new rows: the same id keeps its object —
    # its name, and the grid's selection (Michel, 2026-10-18: after run() the
    # grid went back to the first walk)
    by_id = {}
    if db:
        for o in _LC_OBJS:
            oid = o._v.get("id") if isinstance(o, cls) else None
            if oid is not None and str(oid) != "":
                by_id[str(oid)] = o
    for i in range(n):
        row = arr[i]
        if getattr(row, "⚠️", None) is not None:
            continue          # a list that failed to load says why; it is not an object
        nm = _lc_row_mark(row)
        inst = g.get(nm) if nm else None
        if inst is None and db:
            rid = getattr(row, "id", None)
            old = by_id.get(str(rid)) if rid is not None else None
            onm = _lc_name_of(old) if old is not None else ""
            if onm:
                inst, nm = old, onm
                _lc_row_mark(row, nm)
        # a row's _sub names its subclass (empty for the base class) — or a former name (was = "Run")
        k = cls
        kn = getattr(row, "_sub", None) if db else None
        if kn:
            kn = str(kn)
            k2 = g.get(kn)
            if not (isinstance(k2, type) and issubclass(k2, cls)):
                k2 = None
                for sc in _lc_subs(cls):
                    if getattr(sc, "was", None) == kn:
                        k2 = sc
            if k2 is not None:
                k = k2
        if inst is None or type(inst) is not k:
            inst = k()
            cls._lc_seq += 1
            nm = cls_name.lower() + "_" + str(cls._lc_seq)
            _lc_row_mark(row, nm)
            g[nm] = inst
        inst._js = row
        # a subclass's row reads its own attributes too (a Sprint's laps) — on
        # top of the base class's, which hold the table's id
        # …and what the subclass declares wins over a column the base only
        # read from the table, typed by guess (Michel, 2026-10-18: laps read as
        # text from rows where it was empty — run() added 1 to a str)
        fl = list(cls._lc_fields)
        for f in (getattr(k, "_lc_fields", None) or []):
            at = [i for i, b in enumerate(fl) if b.n == f.n]
            if not at:
                fl.append(f)
            elif getattr(fl[at[0]], "src", False) and not getattr(f, "src", False):
                fl[at[0]] = f
        for f in fl:
            v = getattr(row, f.n, None)
            if v is None:
                continue
            if f.ref and db:
                # the table holds the id; an id whose object is not read yet waits
                ref = _lc_ref_by_id(f.t, v)
                inst._v[f.n] = ref
                raw = getattr(inst, "_lc_raw", None)
                if raw is None:
                    raw = inst._lc_raw = {}
                raw[f.n] = None if ref is not None else v
                continue
            if v == "" and f.t in ("int", "float", "bool"):
                # a blank number is the attribute's default, never "" (Michel,
                # 2026-10-18: laps read "" from a column made while it was str)
                inst._v[f.n] = f.d
                continue
            try:
                inst._v[f.n] = f._coerce(v)
            except Exception:
                inst._v[f.n] = v
        kept.append(inst)
    for o in list(_LC_OBJS):
        if isinstance(o, cls) and getattr(o, "_js", None) is not None and not any(o is k for k in kept):
            _lc_forget(o)
    _lc_publish_class(cls)
    # the classes that point here find their objects now (dogs read after walks)
    if not _LC_RESYNC[0]:
        _LC_RESYNC[0] = True
        try:
            for s2, cn in list(_LC_SOURCED.items()):
                c2 = globals().get(cn)
                if s2 != src and isinstance(c2, type) and any(f.ref and f.t == cls_name for f in c2._lc_fields):
                    _lc_source_sync(s2)
        finally:
            _LC_RESYNC[0] = False


_LC_SETTER_SAID = []


def _lc_say(cls_name, msg):
    fn = getattr(js.window, "lcGridSay", None)
    if fn is not None:
        fn(cls_name, msg)


def _lc_verb(cls_name, nm, verb):
    """A verb pressed on a row — the object acts, the gate decides, the grid is told."""
    inst = globals().get(nm)
    if inst is None:
        return _lc_say(cls_name, "⚠️ " + nm + " is gone")
    try:
        getattr(inst, verb)()
    except PreconditionError as e:
        _lc_say(cls_name, "⛔ " + str(e))
    except Exception as e:
        _lc_say(cls_name, "⚠️ " + verb + "(): " + str(e))


def _lc_set(cls_name, nm, field, value):
    """A cell edited on a class-bound grid goes through the object: the type,
    the enum and the lock apply, and a refused value says why."""
    inst = globals().get(nm)
    if inst is None:
        return _lc_say(cls_name, "⚠️ " + nm + " is gone")
    raw = getattr(inst, "_lc_raw", None)
    if raw:
        raw.pop(field, None)        # a picked reference replaces the id read
    try:
        setattr(inst, field, value)
    except Exception as e:
        _lc_say(cls_name, "⛔ " + str(e))
        _lc_publish_class(type(inst))


def _lc_new(cls_name, kind=None):
    """➕ New under a class's grid: the class itself, or one of its subclasses."""
    cls = globals().get(cls_name)
    if not isinstance(cls, type):
        return
    k = globals().get(kind) if kind else cls
    if isinstance(k, type) and issubclass(k, cls):
        k.new()


def _lc_publish_all():
    seen = []
    for o in _LC_OBJS:
        c = type(o)
        if c not in seen:
            seen.append(c)
            _lc_publish_class(c)


def _lc_rows_load(cls_name, rows_json):
    """Bottom-up meets the contract: values-only rows adopted by the class.
    The header is VALIDATED against the Attrs, never declared again — a
    column the class does not know is an error naming the class."""
    cls = globals().get(cls_name)
    if not isinstance(cls, type):
        raise NameError(cls_name + " is not a model on this page")
    rows = json.loads(rows_json)
    fmap = getattr(cls, "_lc_fmap", None) or {}
    for r in rows:
        bad = [k for k in r if k not in fmap]
        if bad:
            raise ValueError(cls_name + " has no field named " + ", ".join(bad))
    g = globals()
    for i, r in enumerate(rows):
        inst = cls()
        for k, v in r.items():
            f = fmap[k]
            if f.ro or f.is_state:
                inst._set(k, v)
            else:
                setattr(inst, k, v)
        nm = str(r.get("name") or r.get("login") or "").lower()
        safe = ""
        for ch in nm:   # MicroPython: no str.isalnum
            safe += ch if ("a" <= ch <= "z" or "0" <= ch <= "9") else "_"
        g[safe or (cls_name.lower() + str(i + 1))] = inst
    _lc_publish_all()


def _lc_decl_order(cls):
    """The names a class's own block declares with def, in the order written —
    read from the fence's text (MicroPython keeps no line numbers)."""
    name = cls.__name__
    for mid in _LC_SRC:
        src = _LC_SRC[mid]
        lines = src.split("\n")
        at = None
        out = []
        for ln in lines:
            if ln.startswith("class "):
                if at is not None:
                    break
                head = ln[6:].split("(")[0].split(":")[0].strip()
                if head == name:
                    at = True
                continue
            if at and ln.lstrip().startswith("def "):
                out.append(ln.lstrip()[4:].split("(")[0].strip())
        if at:
            return out
    return []


def _lc_verbs(cls):
    """The buttons under a card, base class first, each class's own verbs in
    the order they were written (Michel, 2026-10-19: "from base class to the
    closest one, so Start before Run"). Transitions are the state's and are
    listed by the state; what is left is sorted, so nothing is lost."""
    pub = getattr(cls, "_lc_pub", {}) or {}
    tmeta = getattr(cls, "_lc_tmeta", {}) or {}
    chain = []
    k = cls
    while isinstance(k, type) and k.__name__ != "Object":
        chain.append(k)
        k = k.__bases__[0] if k.__bases__ else None
    out = []
    for k in reversed(chain):
        for n in _lc_decl_order(k):
            if n in pub and n not in tmeta and n not in out:
                out.append(n)
    for n in sorted(pub):
        if n not in tmeta and n not in out:
            out.append(n)
    return out


def _lc_cell(f, v):
    """What a row's cell holds for a value: a datetime travels as ISO text."""
    if f.t == "datetime":
        return v.isoformat() if _lc_isdt(v) else ("" if v is None else v)
    return v


# ════════════════════════ export / import across pages ════════════════════
# The server page exports classes and functions at lc://<name>; a client
# page imports them with a link. Here: what the CLIENT's Python sees (m.Tally
# is the rows as a dataset, m.hello(...) a call whose answer lands in the
# dataset m.hello) and what the SERVER runs on a call (Michel, 2026-10-20).
try:
    _LC_REMOTE        # the preamble runs again before every button: keep the imports
except NameError:
    _LC_REMOTE = {}


class _RemoteCall:
    def __init__(self, prefix, fn):
        self._p, self._f = prefix, fn

    def __call__(self, *args):
        ops = getattr(js.window.lcRemoteOps, self._p, None)
        if ops is None:
            raise RuntimeError("nobody serves " + self._p + " yet")
        ops.call(self._f, js.JSON.parse(json.dumps(list(args))))
        return None     # the answer arrives as one row: m.<fn>.first.result


class _RemoteModel:
    """What a link-shaped model gives the page's Python: m.<Class> as a
    dataset (count, values…), m.<function>(…) as a call."""
    def __init__(self, prefix, name):
        self._prefix, self._name, self._classes, self._funcs = prefix, name, [], []

    def __getattr__(self, k):
        if k.startswith("_"):
            raise AttributeError(k)
        if k in self._classes:
            return Dataset(self._prefix + "." + k)
        if k in self._funcs:
            return _RemoteCall(self._prefix, k)
        ds = getattr(js.window, "lcDatasets", None)
        if ds is not None and getattr(ds, self._prefix + "." + k, None) is not None:
            return Dataset(self._prefix + "." + k)
        raise AttributeError("lc://" + self._name + " exports no " + k)


class _ServerObject:
    """What a .server gives the page's Python: demo.traffic, demo.clients,
    demo.contract — born with it, as delete() is born with an Object."""
    def __init__(self, sid, name):
        self._sid, self._name = sid, name

    def __getattr__(self, k):
        if k.startswith("_"):
            raise AttributeError(k)
        if k in ("traffic", "clients", "contract", "pages"):
            return Dataset(self._sid + "." + k)
        raise AttributeError("a server has traffic, clients, contract and pages — not " + k)


def _lc_server_bind(sid, name):
    r = _LC_REMOTE.get(sid)
    if r is None or not isinstance(r, _ServerObject):
        r = _LC_REMOTE[sid] = _ServerObject(sid, name)
    globals()[sid] = r


def _lc_remote_bind(prefix, name, classes_json, funcs_json):
    r = _LC_REMOTE.get(prefix)
    if r is None:
        r = _LC_REMOTE[prefix] = _RemoteModel(prefix, name)
    r._classes = json.loads(classes_json)
    r._funcs = json.loads(funcs_json)
    globals()[prefix] = r


def _lc_export_call(name, cid, fn, args_json):
    """The server runs an exported function for a client and answers."""
    f = globals().get(fn)
    try:
        if not callable(f) or isinstance(f, type) or fn.startswith("_"):
            raise NameError("lc://" + name + " exports no function " + fn)
        res = f(*json.loads(args_json))
        if not (res is None or isinstance(res, (str, int, float, bool))):
            res = str(res)
        js.window.lcExportAnswer(name, cid, True, res)
    except Exception as e:
        js.window.lcExportAnswer(name, cid, False, str(e))


def _lc_crew_rule(cid, fn, text):
    """A crew's rules member: the page's own function answers a stage, or None."""
    f = globals().get(fn)
    try:
        if not callable(f) or isinstance(f, type) or fn.startswith("_"):
            raise NameError("no function " + fn + " on this page")
        res = f(text)
        js.window.lcCrewAnswer(cid, True, "" if res is None else str(res))
    except Exception as e:
        js.window.lcCrewAnswer(cid, False, str(e))


def _lc_push_obj(obj):
    elid = getattr(obj, "_lc_elid", None)
    if elid:
        _lc_inspect_push(elid)
    _lc_publish_class(type(obj))


def _lc_inspect_bind(elid, insts):
    pairs = []
    for inst in insts:
        inst._lc_elid = elid
        pairs.append((_lc_name_of(inst) or "obj" + str(len(pairs) + 1), inst))
    _LC_INSPECT[elid] = pairs
    # the widget POINTS at its class — data-source feeds the x-ray's
    # Inspector → Class pipe, and the class roster lets the lens resolve
    # a Class target that has no DOM element (Michel, 2026-08-23)
    el = js.window.document.querySelector("[data-lc-inspector='" + elid + "']")
    if el is not None and pairs:
        el.setAttribute("data-source", type(pairs[0][1]).__name__)
    try:
        js.window._lcxClasses = ",".join(list(_CLASSES.keys()))
    except Exception:
        pass
    _lc_inspect_push(elid)
    _lc_publish_all()


def _lc_inspect_bind_new(elid):
    """Bind every Model instance created by the block that just ran. A block
    that declared classes but built nothing shows one live SPECIMEN of each
    new class instead of an empty card — "the story, as classes" must show
    the classes (Michel, 2026-08-23: the widget built nothing forever)."""
    insts = list(_LC_NEW)
    _LC_NEW[:] = []
    if not insts:
        snap = globals().get("_LC_CLS_SNAP") or set()
        for n in _CLASSES:
            if n not in snap and getattr(_CLASSES[n], "_lc_fields", None):
                insts.append(_CLASSES[n]())
        _LC_NEW[:] = []
    _lc_inspect_bind(elid, insts)


def _lc_inspect_bind_decl(elid, mid):
    """Bind an inspector to a MODEL BLOCK's declarations (source= knob): one
    live specimen per class the block declared. The code lives in the model
    block — the page's own structure — and the widget only points at it
    (Michel, 2026-08-24: 'the inspector should just use that block as source')."""
    insts = []
    for n in _LC_DECL.get(mid) or []:
        cls = _CLASSES.get(n)
        if cls is not None and getattr(cls, "_lc_fields", None):
            insts.append(cls())
    _LC_NEW[:] = []
    _lc_inspect_bind(elid, insts)


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

    def __getattr__(self, name):
        """The page is a class of its own: whatever a model block declares —
        classes, singletons like `gh` or `canvas` — reads as self.<name> in
        a feature step (Michel, 2026-08-24). Explicit self.x = … still wins:
        __getattr__ only fires when the instance has no such attribute."""
        if name.startswith("_"):
            raise AttributeError(name)
        g = globals()
        if name in g:
            return g[name]
        raise AttributeError(name)

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
    while _LC_TOUCHED:          # MicroPython: no slice deletion
        _LC_TOUCHED.pop()
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
    js.window._lcStepsTouched = json.dumps(_LC_TOUCHED)
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
    # "Canvas,GH" → the union of each name's closure. Managers with no
    # inbound association need naming, or the picture omits them (Michel,
    # 2026-08-23: "surprised the class diagram is missing GH and Canvas").
    if "," in scope:
        out = set()
        for part in scope.split(","):
            part = part.strip()
            if part:
                out |= _scope_set(part)
        return out
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
    # A name the model does not (yet) define selects nothing — never the whole
    # framework: the author's model may still sit in a closed fold further down
    # (Michel, 2026-10-09, 410 Module 07). The diagram waits for it.
    if scope not in _MODEL:
        return set()
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
/* the console under the cards — the editor's own, so a verb that prints
   shows it, prompt and all (Michel, 2026-10-12: "I see nothing when I
   click on come … I would expect a console") */
.lc-ins-console { border-radius: 8px; margin: -0.4em 0 1em; }
/* a MODEL block is invisible on the page — like a dataset: structure, not
   ink. The widgets that use it show it; the x-ray docks it (2026-08-24).
   The pre-upgrade selectors too, so the code never flashes before hiding. */
.lc-model, .highlighter-rouge.model, pre.model { display: none; }
/* a server line its host runs follows the host as a model, and still shows where it runs */
.lc-server[data-lc-hosted] { display: block; }
</style>

<script>
(function () {
  if (window._lcInspectorReady) return;
  window._lcInspectorReady = true;

  var INS_N = 0;

  function mpReady() {
    if (!window._lcMpReady) {
      window._lcMpReady = window.lcMpy ? window.lcMpy()
        : import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
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

  /* verb tooltips come from the docstring's FIRST LINE. MicroPython keeps no
     docstrings at runtime, so the inspector reads them off the model block's
     own source (the pre-upgrade snapshot) — the page text stays the single
     source of "what does this verb read and write" (Michel, 2026-09-04). */
  function verbDocs(sourceId) {
    var out = {};
    if (!sourceId || !window.lcSourceOf) return out;
    var html = window.lcSourceOf(sourceId);
    if (!html) return out;
    var box = document.createElement("div"); box.innerHTML = html;
    var lines = (box.textContent || "").split("\n"), cls = null;
    lines.forEach(function (line, i) {
      var mc = line.match(/^\s*class\s+(\w+)/); if (mc) { cls = mc[1]; return; }
      var md = line.match(/^\s+def\s+(\w+)\s*\(/);
      if (!md || !cls) return;
      for (var j = i + 1; j < lines.length && j <= i + 3; j++) {
        var l = lines[j].trim();
        if (!l) continue;
        var mq = l.match(/^[rRuU]?("""|''')\s*(.*)$/);
        if (mq) {
          var first = mq[2];
          for (var k = j + 1; !first.trim() && k < lines.length; k++) first = lines[k];
          out[cls + "." + md[1]] = first.replace(/("""|''').*$/, "").trim();
        }
        break;
      }
    });
    return out;
  }

  /* the Python side pushes a fresh schema here after every change */
  window._lcInspectorRender = function (elid, payload) {
    var host = document.querySelector("[data-lc-inspector='" + elid + "']");
    if (!host) return;
    /* while a verb's frames play, the cards wait for the last one — a card
       showing the finish while the console still shows the start reads as
       a bug (the race, 2026-10-19) */
    if (host._lcHold) { host._lcPending = payload; return; }
    var d;
    try { d = JSON.parse(payload); } catch (e) { return; }
    /* source="…" points at a model block; without it the fence IS the model */
    var docs = verbDocs(host.getAttribute("data-bind") || elid);
    /* a readonly widget is a MONITOR: every field renders disabled — the
       identity belongs to the roster, not the reader. Verbs stay live. */
    var allRo = host.hasAttribute("data-lc-ro");
    var h = "";
    (d.cards || []).forEach(function (c) {
      h += "<div class='lc-ins-card' data-card='" + esc(c.name) + "'>";
      h += "<div class='lc-ins-head'>" + esc(c.icon) + " " + esc(c.name)
        + "<span class='lc-ins-cls'>: " + esc(c.cls) + "</span></div>";
      if (c.doc) h += "<div class='lc-ins-doc'>" + esc(c.doc) + "</div>";
      /* labels speak the diagram's dialect: Capitalized, type-emoji prefixed */
      function cap(n) { n = String(n).replace(/_/g, " "); return n.charAt(0).toUpperCase() + n.slice(1); }
      /* names="code": the names as the class writes them — `distance`,
         `come()` — so a card reads like the code it stands for (Michel,
         2026-10-12: "non capitalized to keep it closer to the code") */
      var codeNames = host.getAttribute("data-lc-names") === "code";
      function label(n) { return codeNames ? String(n) : cap(n); }
      function tmoji(f) {
        if (f.ref) return "📦";
        if (f.secret) return "🔒";
        return { str: "🔤", int: "🔢", float: "🔢", bool: "🔘" }[f.t] || "🔤";
      }
      (c.fields || []).forEach(function (f) {
        if (f.state) return;
        var unit = f.unit ? " <span class='lc-ins-unit'>(" + esc(f.unit) + ")</span>" : "";
        h += "<div class='lc-ins-row'" + (f.hint ? " title='" + esc(f.hint) + "'" : "") + ">"
          + "<label>" + tmoji(f) + " " + esc(label(f.n)) + unit + "</label><div class='lc-ins-ctl'>";
        var dis = (f.ro || allRo) ? " disabled" : "";
        if (f.ref) {
          /* typed reference → picklist of live, type-compatible instances */
          h += "<select data-f='" + esc(f.n) + "' data-t='str'" + dis + "><option value=''>None</option>";
          (f.options || []).forEach(function (o) {
            h += "<option" + (o === f.v ? " selected" : "") + ">" + esc(o) + "</option>";
          });
          h += "</select><span class='lc-ins-ro'>:" + esc(f.ref) + "</span>";
        } else if (f.t === "bool") {
          h += "<input type='checkbox' data-f='" + esc(f.n) + "' data-t='bool'" + (f.v ? " checked" : "") + dis + ">"
            + (f.ro ? "<span class='lc-ins-ro'>🔒</span>" : "");
        } else if (f.ro || allRo) {
          var w = window.lcWhen ? window.lcWhen(f.v) : null;      /* a stamp, on the reader's clock */
          h += "<span class='lc-ins-ro'" + (w ? " title='" + esc(w.utc) + "'" : "") + ">"
            + esc(w ? w.text : f.v) + (f.ro ? " 🔒" : "") + "</span>";
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
      (c.fields || []).forEach(function (f) {          /* the state axis closes the card */
        if (!f.state) return;
        h += "<div class='lc-ins-chips'><span class='lc-ins-axis'>🎛️ " + esc(label(f.n)) + "</span>";
        (f.enum || []).forEach(function (s) {
          h += "<span class='lc-ins-chip" + (s === f.v ? " active" : "") + "'>" + esc(String(s).replace(/_/g, " ")) + "</span>";
        });
        h += "</div>";
      });
      if ((c.methods || []).length) {
        h += "<div class='lc-ins-meths'>";
        c.methods.forEach(function (m) {
          /* the verb, not the mechanics: no end-state on the button — the
             destination lives in the tooltip (Michel, 2026-08-22; his
             original Lightcode drew them exactly so) */
          var gate = m.enabled ? (m.post ? "→ " + m.post : "") : "needs: " + (m.pre || []).join(" / ");
          var doc = m.doc || docs[c.cls + "." + m.n] || "";
          var tip = doc ? (doc + (gate ? " · " + gate : "")) : gate;
          h += "<button data-m='" + esc(m.n) + "'" + (m.enabled ? "" : " disabled")
            + (tip ? " title='" + esc(tip) + "'" : "") + ">" + esc(codeNames ? m.n + "()" : cap(m.n)) + "</button>";
        });
        h += "</div>";
      }
      h += "</div>";
    });
    if (d.error) h += "<div class='lc-ins-err'>⚠️ " + esc(d.error) + "</div>";
    host.innerHTML = h;
  };

  /* run code with stdout routed to this widget's console; `echo` is the
     line the learner would have typed — `>>> lucky.come()` — so the card
     teaches the call it stands for */
  function runIn(host, mp, code, echo) {
    var buf = "", fr = window.lcFrames;
    window._lcMpyOut = function (t) { buf += t; };
    /* a verb may animate (time.sleep + os.system('clear')): the frames
       play in this console, like the editor's (pyrun.md, FRAMES) */
    if (fr && window.LC_FRAMES_ON) { try { runPy(mp, window.LC_FRAMES_ON); } catch (e) {} }
    if (host) host._lcHold = true;
    /* a verb's confetti waits for its last frame too (Michel, 2026-10-19:
       "Confetti should only appear at the end of the race") — the burst
       is queued while the verb runs and fired on release */
    var realBurst = window.lcConfetti, bursts = [];
    if (realBurst) window.lcConfetti = function (el) { bursts.push(el); };
    var released = false;
    function release() {
      if (!host || released) return;
      released = true;
      host._lcHold = false;
      var p = host._lcPending;
      host._lcPending = null;
      if (p) window._lcInspectorRender(host.getAttribute("data-lc-inspector"), p);
      if (realBurst) bursts.forEach(function (el) { try { realBurst(el); } catch (e) {} });
    }
    try { runPy(mp, code); } catch (e) { release(); throw e; } finally {
      if (realBurst) window.lcConfetti = realBurst;
      if (fr && window.LC_FRAMES_OFF) { try { runPy(mp, window.LC_FRAMES_OFF); } catch (e) {} }
      window._lcMpyOut = null;
    }
    var con = host && host._lcCon;
    if (!con || (!buf && !echo)) { release(); return; }
    if (con.classList.contains("lc-empty")) { con.textContent = ""; con.classList.remove("lc-empty"); }
    var before = con.textContent + (echo ? ">>> " + echo + "\n" : "");
    if (fr && fr.has(buf)) {
      fr.play(con, buf, function (scr) { con.textContent = scr; con.scrollTop = con.scrollHeight; }, before, release);
      return;
    }
    release();
    con._lcPlay = null;
    con.textContent = before + buf;
    con.scrollTop = con.scrollHeight;
  }
  function pySend(code, host, echo) {
    mpReady().then(function (mp) {
      try { runIn(host, mp, code, echo); } catch (e) { console.error("[lc-inspector]", e); }
    });
  }

  /* {: .dataset of="Learner" } — the bottom-up on-ramp meeting the contract:
     a values-only csv/yaml fence, hydrated into instances by the class,
     header validated against the Attrs, never declared twice. */
  function upgradeRows(el) {
    if (el.dataset.lcRowsDone) return;
    el.dataset.lcRowsDone = "1";
    var of = el.getAttribute("of") || "";
    var raw = (el.querySelector("code") || el).textContent;
    var host = document.createElement("div");
    host.className = "lc-rows-seed";
    if (el.id) host.setAttribute("data-lc-id", el.id);
    host.innerHTML = "<span style='font-size:.8em;color:#888'>🌱 seeding…</span>";
    el.parentNode.replaceChild(host, el);
    if (!of) { host.innerHTML = "<span style='font-size:.8em;color:#b00'>⚠ rows needs of=\"SomeModel\"</span>"; return; }
    /* the IAL eats the fence's language class, so sniff the content:
       a first line of comma-separated bare words is csv; [ or { is json;
       anything else goes to yaml. format= overrides the sniff. */
    var fmt = el.getAttribute("format") || "";
    if (!fmt) {
      var head = (raw.trim().split("\n")[0] || "");
      fmt = /^[\[{]/.test(raw.trim()) ? "json"
          : (head.indexOf(",") > 0 && head.indexOf(":") < 0) ? "csv" : "";
    }
    window.lcParseDataText(raw, fmt).then(function (data) {
      if (!Array.isArray(data)) { host.innerHTML = "<span style='font-size:.8em;color:#b00'>⚠ rows must be a list</span>"; return; }
    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
      var tries = 0;
      (function attempt() {
        mpReady().then(function (mp) {
          try {
            runPy(mp, preamble + "\n_lc_rows_load(" + JSON.stringify(of) + "," + JSON.stringify(JSON.stringify(data)) + ")");
            host.innerHTML = "<span style='font-size:.8em;color:#3a7'>🌱 " + data.length + " " + esc(of) + " row(s) adopted</span>";
          } catch (e) {
            /* the class's own fence may still be on its way through mpReady */
            if (++tries < 25 && /NameError/.test(String(e))) { setTimeout(attempt, 400); return; }
            host.innerHTML = "<span style='font-size:.8em;color:#b00'>⚠ " + esc(String(e.message || e).slice(-260)) + "</span>";
          }
        });
      })();
    }, function (e) { host.innerHTML = "<span style='font-size:.8em;color:#b00'>⚠ " + esc(String(e.message || e)) + "</span>"; });
  }

  function upgradeInspector(el) {
    if (el.dataset.lcInsDone) return;
    el.dataset.lcInsDone = "1";
    var code = (el.querySelector("code") || el).textContent;
    var elid = el.id || ("_insp" + (++INS_N));
    var bind = el.getAttribute("bind") || "";
    var follow = el.getAttribute("follow") || "";
    var host = document.createElement("div");
    host.className = "lc-inspector";
    host.id = elid;
    host.setAttribute("data-lc-id", elid);
    host.setAttribute("data-lc-inspector", elid);
    /* follow= is a master/detail bond — data-bound-to is the attribute the
       x-ray already reads, so the inspector ⇄ grid pipe comes for free */
    if (follow) host.setAttribute("data-bound-to", follow);
    /* readonly="true": a MONITOR — identity fields come from the roster
       (Canvas owns them), so nothing here is typable; verbs stay live
       (Michel, 2026-08-24: the join wizard must not let name/email move) */
    if (el.getAttribute("readonly") === "true") host.setAttribute("data-lc-ro", "1");
    if (el.getAttribute("names") === "code") host.setAttribute("data-lc-names", "code");
    host.innerHTML = "<div class='lc-ins-loading'>⏳ Building the model widget…</div>";
    el.parentNode.replaceChild(host, el);
    var con = document.createElement("pre");
    con.className = "lc-pyrun-out lc-ins-console lc-empty";
    con.setAttribute("data-lc-console", elid);
    con.setAttribute("aria-live", "polite");
    con.textContent = "Press a button — what it prints lands here.";
    host.parentNode.insertBefore(con, host.nextSibling);
    if (el.getAttribute("readonly") === "true") con.hidden = true;   /* a monitor prints nothing */
    host._lcCon = con;

    /* widget edits → Python setters (validation lives there) */
    host.addEventListener("change", function (ev) {
      var t = ev.target, f = t.getAttribute && t.getAttribute("data-f");
      if (!f) return;
      var card = t.closest("[data-card]"); if (!card) return;
      var v = t.type === "checkbox" ? t.checked : (t.getAttribute("data-t") === "num" ? Number(t.value) : t.value);
      var shown = typeof v === "string" ? JSON.stringify(v) : (v === true ? "True" : v === false ? "False" : String(v));
      pySend("_lc_inspect_set(" + JSON.stringify(elid) + "," + JSON.stringify(card.getAttribute("data-card"))
        + "," + JSON.stringify(f) + "," + JSON.stringify(JSON.stringify(v)) + ")",
        host, card.getAttribute("data-card") + "." + f + " = " + shown);
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
        + "," + JSON.stringify(b.getAttribute("data-m")) + ")",
        host, card.getAttribute("data-card") + "." + b.getAttribute("data-m") + "()");
    });

    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    /* source="<model-id>": the code lives in a MODEL BLOCK — the page's own
       structure — and this widget only points at it: wait for that block to
       run, then show one specimen per class it declared (Michel, 2026-08-24). */
    var source = el.getAttribute("source") || "";
    if (source) {
      host.setAttribute("data-bind", source);   // the x-ray's source pipe
      mpReady().then(function () {
        var tries = 0;
        (function waitM() {
          if ((window._lcModelReady || {})[source]) {
            /* bind= alongside source=: the model is the WHEN, the names are
               the WHAT — cards for its live singletons, not specimens */
            pySend(bind
              ? "_lc_inspect_bind_names(" + JSON.stringify(elid) + "," + JSON.stringify(bind) + ")"
              : "_lc_inspect_bind_decl(" + JSON.stringify(elid) + "," + JSON.stringify(source) + ")");
          } else if (++tries < 150) setTimeout(waitM, 120);
          else host.innerHTML = "<div class='lc-ins-err'>⚠️ model block #" + esc(source) + " never ran</div>";
        })();
      }).catch(function () {
        host.innerHTML = "<div class='lc-ins-err'>⚠️ Python runtime failed to load</div>";
      });
      return;
    }
    /* follow="<grid-id>": the inspector waits for the CLAIMED grid's
       selection and binds that row's instance — the detail form is the
       object itself, verbs and all (Michel, 2026-08-22: one SSOT). */
    var tail = follow ? "\n"
      : bind
      ? "\n_lc_inspect_bind_names(" + JSON.stringify(elid) + ", " + JSON.stringify(bind) + ")\n"
      : "\n_lc_inspect_bind_new(" + JSON.stringify(elid) + ")\n";
    mpReady().then(function (mp) {
      try {
        runIn(host, mp, preamble + "\n_LC_NEW[:] = []\n_LC_CLS_SNAP = set(_CLASSES)\n" + code + tail);
        if (follow) {
          host.innerHTML = "<div class='lc-ins-loading'>👉 click a row to open its object</div>";
          if (window.lcMasterDetail) window.lcMasterDetail.subscribe(follow, function (row) {
            if (!row || !row.obj) return;
            pySend("_lc_inspect_bind_names(" + JSON.stringify(elid) + "," + JSON.stringify(String(row.obj)) + ")");
          });
        }
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

  /* ── the MODEL block: the page's classes as a first-class structural
     element. {: .model #id } on a python fence — the code STAYS VISIBLE
     (it IS the declaration), runs once in the shared interpreter, and
     records what it declared so inspectors can point at it with source=
     and the Blocks tab shows it as a key piece (Michel, 2026-08-24). */
  /* DOCSTRING ICONS (Michel, 2026-10-17, register P4): a one-line docstring
     that starts with an emoji gives a class or a method its icon, the rest
     its description — """🔔 Remind the walker.""". The menus, the form's
     buttons and the grid's title wear them. MicroPython drops docstrings, so
     they are read here, from the text, before it runs. */
  var DOCS = window.lcDocs = window.lcDocs || {};
  var EMOJI = /^((?:\p{Extended_Pictographic}|\p{Emoji_Presentation})(?:\uFE0F|\u200D(?:\p{Extended_Pictographic}|\p{Emoji_Presentation})|[\u{1F3FB}-\u{1F3FF}])*)\s*([\s\S]*)$/u;
  function docSplit(t) {
    t = String(t).trim();   /* """ 💰 Buys time""" — a space before the emoji is fine (Michel, 2026-10-17) */
    var m = EMOJI.exec(t);
    return m ? { icon: m[1], text: m[2].trim() } : { icon: "", text: t.trim() };
  }
  function readDocs(code) {
    var lines = code.split("\n"), cur = null;
    var docAfter = function (i) {
      for (var k = i + 1; k < lines.length; k++) {
        if (!lines[k].trim()) continue;
        var m = /^\s*(?:\"\"\"|''')(.*?)(?:\"\"\"|''')\s*$/.exec(lines[k]);
        return m ? m[1] : null;
      }
      return null;
    };
    lines.forEach(function (ln, i) {
      var c = /^class\s+(\w+)\s*(?:\(([^)]*)\))?\s*:/.exec(ln);
      if (c) {
        cur = c[1];
        var d = docAfter(i), sp = d == null ? { icon: "", text: "" } : docSplit(d);
        DOCS[cur] = { icon: sp.icon, text: sp.text, base: ((c[2] || "").split(",")[0] || "").trim(), m: {}, props: [] };
        return;
      }
      var f = /^\s+def\s+(\w+)\s*\(/.exec(ln);
      if (f && cur) {
        var d2 = docAfter(i); if (d2 != null) DOCS[cur].m[f[1]] = docSplit(d2);
        /* @property on the line above: a computed column, in the order written */
        for (var b = i - 1; b >= 0 && /^\s*@/.test(lines[b]); b--) {
          if (/^\s*@property\s*$/.test(lines[b]) && DOCS[cur].props.indexOf(f[1]) < 0) DOCS[cur].props.push(f[1]);
          /* @who.setter: the column is typed in, through the setter */
          /* …and only when its def keeps the property's name: @who.setter over
             def setwho makes a second property, who stays read-only (Michel,
             2026-10-18) — that slip is kept, to be said in plain words */
          var st = /^\s*@(\w+)\.setter\s*$/.exec(lines[b]);
          if (st && st[1] === f[1]) (DOCS[cur].setters = DOCS[cur].setters || {})[st[1]] = 1;
          else if (st) (DOCS[cur].badSetters = DOCS[cur].badSetters || {})[st[1]] = f[1];
        }
      }
    });
  }
  /* the @property names a class (and its bases) declare, as written */
  window.lcPropsOf = function (cls) {
    var out = [], d = DOCS[cls], n = 0;
    var chain = [];
    while (d && n++ < 8) { chain.unshift(d); d = DOCS[d.base]; }
    chain.forEach(function (x) { (x.props || []).forEach(function (p) { if (out.indexOf(p) < 0) out.push(p); }); });
    return out;
  };
  /* does a property of the class (or a base) have a setter — MicroPython's
     property does not say, the source does */
  /* a setter written under another name: what it was called, or "" */
  window.lcBadSetter = function (cls, prop) {
    var d = DOCS[cls], n = 0;
    while (d && n++ < 8) { if (d.badSetters && d.badSetters[prop]) return d.badSetters[prop]; d = DOCS[d.base]; }
    return "";
  };
  window.lcHasSetter = function (cls, prop) {
    var d = DOCS[cls], n = 0;
    while (d && n++ < 8) { if (d.setters && d.setters[prop]) return true; d = DOCS[d.base]; }
    return false;
  };
  /* a class's doc, or a method's — found up the class's bases */
  window.lcDocOf = function (cls, method) {
    var d = DOCS[cls], n = 0;
    while (d && n++ < 8) {
      if (!method) return d;
      if (d.m[method]) return d.m[method];
      d = DOCS[d.base];
    }
    return null;
  };

  function upgradeModel(el) {
    if (el.dataset.lcModelDone) return;
    el.dataset.lcModelDone = "1";
    /* THE REMOTE MODEL IS A LINK (Michel, 2026-10-20): [the demo](lc://demo)
       {: .model #m } imports the classes and functions another running page
       exports — no Python on this side */
    var lnk = el.tagName !== "PRE" && el.querySelector("a[href^='lc://']");
    if (lnk) { importModel(el, lnk.getAttribute("href")); return; }
    var code = (el.querySelector("code") || el).textContent;
    var mid = el.id || ("_model" + (++INS_N));
    el.setAttribute("data-lc-id", mid);
    el.classList.add("lc-model");
    /* A CLASS IS A DATASET (Michel, 2026-10-15): class Family(Object,
       source="reservations") — MicroPython takes no keyword on a class line,
       so the runner lifts it: the class is declared plain, then bound to its
       list; the list's later moves (arrival, a bare edit) re-sync the objects. */
    var sourced = [];
    code = code.replace(/^([ \t]*)class\s+(\w+)\s*\(([^)]*?),\s*source\s*=\s*(["'])([^"']+)\4\s*\)\s*:/mg,
      function (_, ind, name, bases, q, src) { sourced.push([name, src]); return ind + "class " + name + "(" + bases + "):"; });
    /* A MODEL ON A DATABASE (Michel, 2026-10-17, register P3):
       {: .model source="shelter" } — each class of Object is its table
       (Walk ↔ walk, FosterFamily ↔ foster_family); source= names the table
       only when it is named otherwise. No dataset to declare. */
    /* ONE WORD, source= (Michel, 2026-10-17, register P6: "more polymorphic,
       while reducing the cognitive load"): a .database → a table per class;
       a list → the model's one class wears it (several: the page says which
       question to answer); a class's own source= always wins */
    var mSrc = el.getAttribute("source") || "";
    var mEl = mSrc ? document.getElementById(mSrc) : null;
    var isDbSrc = !!mSrc && (!!(window.lcDatabases || {})[mSrc] || !!(mEl && /(^|\s)(lc-)?database(\s|$)/.test(mEl.className)));
    var dbAttr = isDbSrc ? mSrc : "";
    var srcWarn = "";
    if (mSrc && !isDbSrc) {
      var plain = [];
      code.replace(/^class\s+(\w+)\s*\(\s*Object\s*\)\s*:/mg, function (_, name) {
        if (!sourced.some(function (p) { return p[0] === name; })) plain.push(name);
        return _;
      });
      if (plain.length === 1) sourced.push([plain[0], mSrc]);
      else if (plain.length > 1) srcWarn = "source=\"" + mSrc + "\" is one list — which class wears it? Put source= on that class.";
    }
    if (dbAttr && window.lcDatabaseTable) {
      sourced = sourced.map(function (p) {
        return document.getElementById(p[1]) ? p : [p[0], window.lcDatabaseTable(dbAttr, p[1], el)];
      });
      code.replace(/^class\s+(\w+)\s*\(\s*Object\s*\)\s*:/mg, function (_, name) {
        if (!sourced.some(function (p) { return p[0] === name; })) {
          var table = name.replace(/([a-z0-9])([A-Z])/g, "$1_$2").toLowerCase();
          sourced.push([name, window.lcDatabaseTable(dbAttr, table, el)]);
        }
        return _;
      });
    }
    var bind = sourced.map(function (p) { return "\n_lc_source_bind(" + JSON.stringify(p[0]) + ", " + JSON.stringify(p[1]) + ")"; }).join("");
    sourced.forEach(function (p) {
      var L = window.lcDatasetListeners = window.lcDatasetListeners || {};
      var sync = function () {
        if (window._lcModelWriting) return;   /* our own write-back, not a move */
        pySend("_lc_source_sync(" + JSON.stringify(p[1]) + ")");
      };
      sync._lcEl = el;                        /* gone with its block (dataset.md) */
      (L[p[1]] = L[p[1]] || []).push(sync);
    });
    readDocs(code);
    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    /* THE SAME CLASSES ARE NOT RE-RUN. A pad re-renders on every pause in
       typing; re-running the runtime and the classes each time froze the
       typing (Michel, 2026-10-16). When every class this block declares was
       last declared by this very text, the classes stand: only the lists are
       re-bound (their rows were re-read) and the page republished. */
    var names = [], nm, reCls = /^[ \t]*class\s+(\w+)/mg;
    while ((nm = reCls.exec(code))) names.push(nm[1]);
    var by = window._lcClassBy = window._lcClassBy || {};
    var same = names.length && names.every(function (n) { return by[n] === code; });
    el.setAttribute("data-lc-classes", names.join(" "));
    if (sourced.length) el.setAttribute("data-bind", sourced[0][1]);   /* the x-ray's source pipe */
    /* the classes of a block that has left the page — and that no block on
       the page declares any more — are forgotten before this one runs */
    var blocks = window._lcModelEls = (window._lcModelEls || []).filter(function (b) { return b.el !== el; });
    var gone = [];
    blocks = blocks.filter(function (b) {
      if (b.el.isConnected) return true;
      b.names.forEach(function (n) { if (gone.indexOf(n) < 0) gone.push(n); });
      return false;
    });
    blocks.push({ el: el, names: names });
    window._lcModelEls = blocks;
    gone = gone.filter(function (n) {
      return names.indexOf(n) < 0 && !blocks.some(function (b) { return b.el.isConnected && b.names.indexOf(n) >= 0; });
    });
    var purge = gone.length ? gone.map(function (n) { delete by[n]; return "_lc_forget_class(" + JSON.stringify(n) + ")\n"; }).join("") : "";
    mpReady().then(function (mp) {
      if (same) {
        try {
          runPy(mp, purge + "_LC_DECL[" + JSON.stringify(mid) + "] = " + JSON.stringify(names) + "\n_LC_SRC[" + JSON.stringify(mid) + "] = " + JSON.stringify(code) + bind + "\n_lc_publish_all()\n");
          (window._lcModelReady = window._lcModelReady || {})[mid] = 1;
          document.dispatchEvent(new CustomEvent("lc-model-changed"));
          if (window.lcWarn) window.lcWarn(el, srcWarn);
          el._lcModelNames = names; el._lcModelCode = code;    /* a .server reads them */
          return;
        } catch (e) { names.forEach(function (n) { delete by[n]; }); }
      }
      /* THE RUNTIME LOADS ONCE PER INTERPRETER (Michel, 2026-10-16: "a
         syntax error in the editor blocks the page"): each class edit in a
         pad re-ran the whole engine before the class — 0.7–1 s frozen per
         pause. Its registries survive anyway; the class runs alone after
         the first time. */
      var pre = window._lcModelPreIn === mp ? "" : preamble;
      try {
        if (purge) runPy(mp, purge);
        /* the fence's text is known BEFORE its classes run: the first publish
           already orders the verbs as written */
        runPy(mp, pre + "\n_LC_SNAP_M = set(_CLASSES)\n_LC_SRC[" + JSON.stringify(mid) + "] = " + JSON.stringify(code) + "\n" + code + bind +
          "\n_LC_DECL[" + JSON.stringify(mid) + "] = [n for n in _CLASSES if n not in _LC_SNAP_M]\n" +
          "_LC_NEW[:] = []\n_lc_publish_all()\n");
        window._lcModelPreIn = mp;
        (window._lcModelReady = window._lcModelReady || {})[mid] = 1;
        names.forEach(function (n) { by[n] = code; });
        document.dispatchEvent(new CustomEvent("lc-model-changed"));
        if (window.lcWarn) window.lcWarn(el, srcWarn);
        el._lcModelNames = names; el._lcModelCode = code;      /* a .server reads them */
      } catch (e) {
        names.forEach(function (n) { delete by[n]; });
        console.error("[lc-model]", e);
        /* a class that does not run says so beside itself, on ITS line —
           not only in the console (Michel, 2026-10-16) */
        if (pre) window._lcModelPreIn = null;
        if (window.lcWarn) window.lcWarn(el, window.lcPyError ? window.lcPyError(e, pre ? pre.split("\n").length + 1 : 2) : String(e));
      }
    }).catch(function (e) { console.error("[lc-model]", e); });
  }

  /* ── SERVER / CLIENT: two running pages, one browser (Michel, 2026-10-20;
     hq/architecture/distributed.md, "The simplest example"). Inside a page an
     id is free for its neighbours; reaching OTHER pages is an explicit
     intent, a line of its own: [the demo](lc://demo) {: .server #demo
     model="tally_model" }. The server joins a channel of that name and
     serves the model's classes and functions — spec and rows on follow and
     on every change; new, set, verb and a function call through the same
     door its own grid uses. Its id is a dataset: one row per request, the
     monitor is a grid on it. A client imports with the same link on a
     .model: its grids, forms and buttons never know where the object lives.
     One server per name: a newcomer claims, the holder says taken, the
     newcomer stands by. One loop, one queue, in order. Transport today: the
     browser's own channel (same site, same browser). */
  function lcChan(name) { return new BroadcastChannel("lc://" + name); }
  function upgradeServer(el) {
    if (el.dataset.lcServerDone) return;
    el.dataset.lcServerDone = "1";
    var lnk = el.querySelector("a[href^='lc://']"), m = lnk && /^lc:\/\/([\w.-]+)$/.exec(lnk.getAttribute("href") || "");
    if (!m) { if (window.lcWarn) window.lcWarn(el, "a server is a link: [the demo](lc://<name>) {: .server #id model=\"<model id>\" }"); return; }
    var sid = el.id || ("_server" + (++INS_N));
    el.setAttribute("data-lc-id", sid); el.classList.add("lc-server");
    /* THE HOST ALREADY RUNS IT (Michel, 2026-10-22: "how come on site.md I
       see 6 grids? They are NOT in the source"). A page a host serves names
       the servers that host runs; this line is one of them, so it stands by
       — no second server in the tab, no lc:// link a browser cannot open —
       and says where it runs. The page shows as it is written, and its
       books read the host: the line follows lc://here/<name> under its own
       id, so site.pages, site.Visit, site.contract hold the host's rows
       (Michel, 2026-10-22, "That's all?" → "go"). */
    var hostRuns = document.querySelector('meta[name="lc-host-serves"]');
    if (hostRuns && ("," + hostRuns.getAttribute("content") + ",").indexOf("," + m[1] + ",") >= 0) {
      el.setAttribute("data-lc-hosted", "1");
      el.textContent = "📡 lc://" + m[1] + " — served by this host";
      el.title = (lnk.textContent || m[1]) + ": runs on the host this page came from, not in this tab";
      importModel(el, "lc://here/" + m[1]);
      return;
    }
    var want = el.getAttribute("model") || "";
    var modelOf = function () {
      if (want) return document.querySelector(".lc-model[data-lc-id='" + want + "']");
      var all = [].slice.call(document.querySelectorAll(".lc-model")).filter(function (e) { return !e.hasAttribute("data-lc-remote") && e.isConnected; });
      return all[0] || null;
    };
    /* born with the server, like delete() with an Object: demo.traffic,
       demo.clients, demo.contract (Michel, 2026-10-20: "the traffic dataset
       remains implicit and this bugs me") */
    ["traffic", "clients", "contract", "pages"].forEach(function (k) { window.lcSetDataset(sid + "." + k, []); });
    /* THE SIMPLEST SERVER SERVES PAGES (Michel, 2026-10-22): pages="<dataset id>"
       names rows of path and file; with it, no model is needed — the server
       stands with an empty contract and answers paths. */
    var pagesId = el.getAttribute("pages") || "";
    var tries = 0;
    (function wait() {
      /* pages= and no model=: a server of pages only — it never borrows the
         page's first model (Michel, 2026-10-22: the annex repeated the site's
         rows and contract), and it stands at once */
      if (pagesId && !want) { serveModel(el, m[1], sid, function () { return null; }, pagesId); return; }
      var me = modelOf();
      if (me && me._lcModelNames) { serveModel(el, m[1], sid, modelOf, pagesId); return; }
      if (++tries > 60) {
        if (pagesId) { serveModel(el, m[1], sid, function () { return null; }, pagesId); return; }
        if (window.lcWarn) window.lcWarn(el, "no model to serve" + (want ? ": #" + want : "") + " — a .model on this page, ready");
        return;
      }
      if (!want && !me && pagesId && tries > 4) { serveModel(el, m[1], sid, function () { return null; }, pagesId); return; }
      setTimeout(wait, 250);
    })();
  }
  /* THE PAGES A SERVER SERVES (Michel, 2026-10-22): rows of path and file,
     like today's site — a path is a page, or a folder whose index.md answers
     the folder itself; a file is a repo path to the markdown (served as the
     site serves it, or through the runner when the server runs there), or
     another server (lc://<name>), which is asked in turn. */
  function pageRows(pagesId) {
    return ((window.lcDatasets || {})[pagesId] || []).filter(function (r) { return r && !r["⚠️"] && r.path != null; });
  }
  function resolvePage(rows, path) {
    var p = "/" + String(path || "").replace(/^\/+/, "");
    var best = null, bestLen = -1;
    rows.forEach(function (r) {
      var rp = ("/" + String(r.path || "").replace(/^\/+/, "")).replace(/\/+$/, ""), f = String(r.file || "").trim();   /* the root row reads "" */
      var folder = /\/$/.test(f) || /^lc:\/\/[\w.-]+$/.test(f);
      if (!folder && p.replace(/\/+$/, "") === rp) { if (rp.length > bestLen) { best = { file: f, rest: "" }; bestLen = rp.length; } return; }
      if (folder && (p === rp || p === rp + "/" || p.indexOf(rp + "/") === 0 || rp === "")) {
        var rest = rp === "" ? p.slice(1) : p.slice(rp.length + 1);
        if (rp.length >= bestLen) { best = { file: f, rest: rest }; bestLen = rp.length; }
      }
    });
    if (!best) return null;
    if (/^lc:\/\//.test(best.file)) return { via: best.file.replace(/^lc:\/\//, ""), path: "/" + best.rest };
    var f = best.file;
    if (/\/$/.test(f)) f += (best.rest === "" || /\/$/.test(best.rest)) ? best.rest + "index.md" : best.rest + (/\.md$/i.test(best.rest) ? "" : ".md");
    return { file: f };
  }
  function pageUrl(file) {
    /* the file as the browser reaches it: the runner's door when the server
       page runs there (a private repo), else the site's own path */
    var run = document.querySelector(".lc-run[data-lc-src-repo]");
    if (run && run.getAttribute("data-lc-src-repo")) return "/run.html#src=gh:" + run.getAttribute("data-lc-src-repo") + "/" + file;
    return "/" + file.replace(/^docs\//, "").replace(/\.md$/i, "");
  }
  function serveModel(el, name, sid, modelOf, pagesId) {
    /* ONE SERVER PER NAME PER PAGE (Michel, 2026-10-20: "each bump adds 8"):
       a pad or the editor re-renders its blocks, and every render had opened
       one more channel on the same name — a verb then ran once per stale
       listener. The newest render takes the name; the old one closes. */
    var exportsOf = function () { return String(el.getAttribute("exports") || "").split(",").map(function (x) { return x.trim(); }).filter(Boolean); };
    var reg = window._lcExports = window._lcExports || {};
    if (reg[name]) { try { reg[name].ch.close(); } catch (e) {} document.removeEventListener("lc-model-changed", reg[name].onChange); }
    var ch = lcChan(name), me = "srv-" + Math.random().toString(36).slice(2, 7);
    el._lcExport = ch;
    el.setAttribute("data-lc-export", name);
    var said = (reg[name] && reg[name].said) || 0, seen = (reg[name] && reg[name].seen) || {}, standby = false;
    var hhmm = function () { var d = new Date(), p = function (n) { return (n < 10 ? "0" : "") + n; }; return p(d.getHours()) + ":" + p(d.getMinutes()) + ":" + p(d.getSeconds()); };
    function client(from) {
      /* demo.clients: who follows, since when, last seen, how many requests */
      if (!from) return;
      var rows = (window.lcDatasets[sid + ".clients"] || []).filter(function (r) { return r && !r["⚠️"]; }).slice();
      var hit = rows.filter(function (r) { return r.id === from; })[0];
      if (!hit) { hit = { id: from, since: hhmm(), seen: hhmm(), requests: 0 }; rows.push(hit); }
      hit = Object.assign({}, hit, { seen: hhmm(), requests: (hit.requests || 0) + 1 });
      window.lcSetDataset(sid + ".clients", rows.map(function (r) { return r.id === from ? hit : r; }));
    }
    function traffic(what, from) {
      /* demo.traffic: one row per request — follow once per client, then its
         verbs, edits, New and calls; the heartbeat (ping) never; the last 50 rows stay */
      var rows = (window.lcDatasets[sid + ".traffic"] || []).filter(function (r) { return r && !r["⚠️"]; });
      rows.push({ n: ++said, at: hhmm(), from: from || "", what: what });
      reg[name] && (reg[name].said = said);
      window.lcSetDataset(sid + ".traffic", rows.slice(-50));
      client(from);
    }
    function funcsOf(code) {
      var f = [];
      String(code || "").replace(/^def\s+([A-Za-z]\w*)\s*\(([^)]*)\)/mg, function (_, n, args) { f.push({ n: n, sig: n + "(" + args.trim() + ")" }); return _; });
      return f;
    }
    function contractOf(classes, funcs) {
      /* demo.contract: what is served — name · kind · signature · doc — the
         interface without the implementation; the client mirrors it as m.contract */
      var rows = [], doc = function (c, v) { var d = window.lcDocOf ? window.lcDocOf(c, v) : null; return (d && d.text) || ""; };
      Object.keys(classes).forEach(function (c) {
        var m = classes[c], fields = (m.order || Object.keys(m.fields || {})).filter(function (k) { return m.fields[k] && !m.fields[k].hidden; });
        rows.push({ name: c, kind: "class", signature: c + "(" + fields.join(", ") + ")", doc: doc(c) });
        Object.keys(m.transitions || {}).forEach(function (v) { rows.push({ name: c + "." + v, kind: "verb", signature: c + "." + v + "()  " + (m.transitions[v].pre || []).join("/") + " → " + (m.transitions[v].post || ""), doc: doc(c, v) }); });
        (m.verbs || []).forEach(function (v) { rows.push({ name: c + "." + v, kind: "verb", signature: c + "." + v + "()", doc: doc(c, v) }); });
      });
      funcs.forEach(function (f) { rows.push({ name: f.n, kind: "function", signature: f.sig, doc: "" }); });
      return rows;
    }
    function spec() {
      var mEl = modelOf(), names = (mEl && mEl._lcModelNames) || [], classes = {}, rows = {};
      names.forEach(function (n) {
        if ((window.lcModels || {})[n]) { classes[n] = window.lcModels[n]; rows[n] = (window.lcDatasets || {})[n] || []; }
      });
      var funcs = funcsOf(mEl && mEl._lcModelCode), contract = contractOf(classes, funcs);
      /* exports="totals,cities": datasets and query results handed out by name, as on a host */
      var datasets = {};
      exportsOf().forEach(function (k) {
        var r = (window.lcDatasets || {})[k]; datasets[k] = Array.isArray(r) ? r : [];
        contract.push({ name: k, kind: "dataset", signature: k + "(" + Object.keys(datasets[k][0] || {}).join(", ") + ")", doc: "" });
      });
      window.lcSetDataset(sid + ".contract", contract);
      var pages = pagesId ? pageRows(pagesId) : [];
      var mine = JSON.stringify(pages);
      if (JSON.stringify((window.lcDatasets || {})[sid + ".pages"] || []) !== mine) window.lcSetDataset(sid + ".pages", JSON.parse(mine));
      return { t: "spec", name: name, classes: classes, funcs: funcs.map(function (f) { return f.n; }), contract: contract, rows: rows, pages: pages, datasets: datasets };
    }
    function servePage(d, from) {
      /* a client asks a path; the answer names the file and where the
         browser reaches it — or says what is not served. A file that is
         another server is asked in turn, the answer relayed as is. */
      traffic("page " + d.path, from);
      var hit = pagesId ? resolvePage(pageRows(pagesId), d.path) : null;
      var answer = function (ok, msg) { try { ch.postMessage(Object.assign({ t: ok ? "served" : "refused", id: d.id, path: d.path }, msg)); } catch (e) {} };
      if (!hit) { answer(false, { result: "lc://" + name + " serves no page " + d.path }); return; }
      if (!hit.via) { answer(true, { file: hit.file, url: pageUrl(hit.file) }); return; }
      var up = lcChan(hit.via), id = me + "#page#" + Math.random().toString(36).slice(2, 7), done = false;
      var quiet = setTimeout(function () { if (done) return; done = true; try { up.close(); } catch (e) {} answer(false, { result: "lc://" + hit.via + " answers nothing for " + hit.path }); }, 1500);
      up.onmessage = function (ev) {
        var r = ev.data || {};
        if (r.id !== id || done) return;
        done = true; clearTimeout(quiet); try { up.close(); } catch (e) {}
        answer(r.t === "served", r.t === "served" ? { file: r.file, url: r.url, via: hit.via } : { result: r.result });
      };
      try { up.postMessage({ t: "page", path: hit.path, id: id, from: me }); } catch (e) {}
    }
    var soon = null, last = "";
    function push(force) {
      if (standby) return;
      clearTimeout(soon);
      soon = setTimeout(function () {
        var s = spec(), j = JSON.stringify(s);
        if (force || j !== last) { last = j; try { ch.postMessage(s); } catch (e) {} }
      }, 40);
    }
    var L = window.lcDatasetListeners = window.lcDatasetListeners || {};
    var hook = function () { push(); }; hook._lcEl = el;
    (modelOf() && modelOf()._lcModelNames || []).forEach(function (n) { (L[n] = L[n] || []).push(hook); });
    if (pagesId) (L[pagesId] = L[pagesId] || []).push(hook);     /* a page added to the list is served at once */
    exportsOf().forEach(function (k) { (L[k] = L[k] || []).push(hook); });   /* an exported list that moves is sent again */
    var onChange = function () {
      /* the model re-rendered (a pad): its new classes get the hook too */
      (modelOf() && modelOf()._lcModelNames || []).forEach(function (n) { if ((L[n] || []).indexOf(hook) < 0) (L[n] = L[n] || []).push(hook); });
      push();
    };
    document.addEventListener("lc-model-changed", onChange);
    reg[name] = { ch: ch, onChange: onChange, el: el, said: said, seen: seen, me: me };
    function standDown() {
      standby = true;
      el.setAttribute("data-lc-standby", "1");
      if (reg[name] && reg[name].ch === ch) delete reg[name];
      document.removeEventListener("lc-model-changed", onChange);
      try { ch.close(); } catch (e) {}
      window.lcSetDataset(sid + ".traffic", [{ n: 0, at: hhmm(), from: "", what: "stands by — lc://" + name + " is served by another page" }]);
      if (window.lcWarn) window.lcWarn(el, "lc://" + name + " is served by another page — this one stands by");
    }
    ch.onmessage = function (ev) {
      if (standby) return;
      if (reg[name] && reg[name].ch !== ch) { try { ch.close(); } catch (e) {} return; }   /* replaced */
      var d = ev.data || {}, from = d.from || "";
      if (d.t === "claim") { try { ch.postMessage({ t: "taken", to: from, name: name }); } catch (e) {} return; }
      if (d.t === "taken" && d.to === me) { standDown(); return; }
      if (d.t === "ping") { try { ch.postMessage({ t: "pong", name: name }); } catch (e) {} return; }
      if (d.t === "follow") { if (!seen[from]) { seen[from] = 1; traffic("follow", from); } push(true); return; }
      if (d.t === "page") { servePage(d, from); return; }
      if (d.t === "verb") { traffic(d.cls + "." + d.obj + "." + d.verb + "()", from);
        pySend("_lc_verb(" + JSON.stringify(d.cls) + "," + JSON.stringify(d.obj) + "," + JSON.stringify(d.verb) + ")"); return; }
      if (d.t === "new") { traffic("new " + (d.kind || d.cls), from);
        pySend("_lc_new(" + JSON.stringify(d.cls) + (d.kind && d.kind !== d.cls ? "," + JSON.stringify(d.kind) : "") + ")"); return; }
      if (d.t === "set") { traffic(d.cls + "." + d.obj + "." + d.col + " = " + JSON.stringify(d.val), from);
        pySend("_lc_set(" + JSON.stringify(d.cls) + "," + JSON.stringify(d.obj) + "," + JSON.stringify(d.col) + "," + JSON.stringify(d.val) + ")"); return; }
      if (d.t === "call") { traffic(d.fn + "(" + (d.args || []).map(function (a) { return JSON.stringify(a); }).join(", ") + ")", from);
        pySend("_lc_export_call(" + JSON.stringify(name) + "," + JSON.stringify(d.id) + "," + JSON.stringify(d.fn) + "," + JSON.stringify(JSON.stringify(d.args || [])) + ")"); return; }
    };
    /* the claim: a holder answers taken within the moment; else the name is ours */
    try { ch.postMessage({ t: "claim", from: me }); } catch (e) {}
    setTimeout(function () { if (!standby) push(true); }, 300);
    mpReady().then(function (mp) {
      var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
      var pre = window._lcModelPreIn === mp ? "" : preamble + "\n";
      runPy(mp, pre + "_lc_server_bind(" + JSON.stringify(sid) + "," + JSON.stringify(name) + ")");
      window._lcModelPreIn = mp;
    }).catch(function () {});
  }
  /* python answers a call through here: done with the result, or refused with the words */
  window.lcExportAnswer = function (name, id, ok, result) {
    var el = document.querySelector("[data-lc-export='" + name + "']");
    if (el && el._lcExport) el._lcExport.postMessage({ t: ok ? "done" : "refused", id: id, result: result });
  };
  /* THE CARRIER IS PICKED FROM THE ADDRESS (Michel, 2026-10-22, the host's run
     mode): lc://<name> is the browser's own channel, same device, as above;
     lc://<host:port>/<name> is a host on the network serving the page, and
     "here" is the origin this page was served from. Same messages, same
     answers — one request per message, the spec on a stream — so a client
     page never knows which carrier it rides. */
  function lcNetChan(where, name) {
    var base = (where === "here" ? location.origin : (/^https?:\/\//.test(where) ? where : location.protocol + "//" + where)) + "/lc/" + name;
    var self = { onmessage: null, closed: false }, es = null, origin = base.replace(/\/lc\/[\w.-]+$/, "");
    var deliver = function (d) {
      /* a page the host serves lives on the host: its path resolves there, not
         against the site the served page is based on (Michel, 2026-10-23: the
         annex card opened the site's /annex, a 404) */
      if (d && d.t === "served" && typeof d.url === "string" && d.url.charAt(0) === "/") d.url = origin + d.url;
      if (!self.closed && self.onmessage && d) self.onmessage({ data: d });
    };
    function listen() {
      try { es = new EventSource(base + "/events"); } catch (e) { es = null; return; }
      es.onmessage = function (ev) { try { deliver(JSON.parse(ev.data)); } catch (e) {} };
      es.onerror = function () {};   /* a host away answers nothing: the client says so by itself */
    }
    self.postMessage = function (msg) {
      if (self.closed) return;
      if (msg.t === "follow" && !es) listen();
      /* a request the network drops (a connection closed under it — Safari)
         is sent once more before silence means nobody (Michel, 2026-10-22) */
      var send = function () { return fetch(base, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(msg) }); };
      send().catch(function () { return send(); })
        .then(function (r) { return r.json(); }).then(deliver).catch(function () {});
    };
    self.close = function () { self.closed = true; if (es) { try { es.close(); } catch (e) {} es = null; } };
    return self;
  }
  function importModel(el, href) {
    var m = /^lc:\/\/(?:([\w.-]+(?::\d+)?)\/)?([\w.-]+)$/.exec(href);
    if (!m) { if (window.lcWarn) window.lcWarn(el, "a remote model is a link: lc://<name>, or lc://<host:port>/<name> for a host on the network"); return; }
    var name = m[2], prefix = el.id || "m", ch = m[1] ? lcNetChan(m[1], name) : lcChan(name), me = "";
    /* the tab's id survives a reload: the same tab reads as the same client
       (Michel, 2026-10-20: "why a refresh on a tab would create a new entry") */
    try { me = sessionStorage.getItem("lc_tab") || ""; if (!me) { me = "tab-" + Math.random().toString(36).slice(2, 7); sessionStorage.setItem("lc_tab", me); } }
    catch (e) { me = "tab-" + Math.random().toString(36).slice(2, 7); }
    el.setAttribute("data-lc-id", prefix); el.setAttribute("data-lc-remote", name); el.classList.add("lc-model");
    var known = [], quiet = null, lastSpec = "", gone = false, tick = null;
    /* ONE IMPORT PER NAME ON A PAGE (Michel, 2026-10-22, Safari: "nobody
       serves lc://site" three seconds after load, rows from the host on
       screen). A pad redraws its preview and every redraw imported again,
       each with its own stream to the host; Safari keeps six connections
       per host, so the heartbeat waited behind the streams and missed its
       moment. The newest import of a prefix takes it; the one before closes
       at once and says nothing more. */
    var live = window._lcImports = window._lcImports || {};
    if (live[prefix]) live[prefix]();
    var stop = function () { gone = true; clearTimeout(quiet); if (tick) clearInterval(tick); try { ch.close(); } catch (e) {} };
    live[prefix] = stop;
    /* the network's answer takes a round trip, the tab's a moment */
    var patience = m[1] ? 3000 : 1500;
    function nobody() {
      /* a line the page re-rendered away (a pad redraws its preview) is not
         the page's import any more: it says nothing over the live one's grids
         (Michel, 2026-10-22: "nobody serves lc://site" under rows from the host) */
      if (gone || !el.isConnected) return;
      el.setAttribute("data-lc-nobody", "1");
      document.querySelectorAll(".lc-datagrid[data-bind^='" + prefix + ".']").forEach(function (g) {
        if (window.lcGridSay) window.lcGridSay(g.getAttribute("data-bind"), "🔌 nobody serves lc://" + name + " — open its server page");
      });
    }
    ch.onmessage = function (ev) {
      if (gone) return;
      var d = ev.data || {};
      if (d.t === "pong" && d.name === name) { clearTimeout(quiet); el.removeAttribute("data-lc-nobody"); return; }
      if (d.t === "spec" && d.name === name) {
        clearTimeout(quiet); el.removeAttribute("data-lc-nobody");
        var j = JSON.stringify(d); if (j === lastSpec) return; lastSpec = j;
        window.lcModels = window.lcModels || {};
        (window.lcRemoteSpec = window.lcRemoteSpec || {})[prefix] = { classes: Object.keys(d.classes), funcs: d.funcs || [] };
        window.lcSetDataset(prefix + ".contract", d.contract || []);     /* m.contract — what was imported */
        window.lcSetDataset(prefix + ".pages", d.pages || []);           /* m.pages — what the server serves as pages */
        /* m.<name> — what the server exports by name: a dataset, a query's result (Michel, 2026-10-22) */
        Object.keys(d.datasets || {}).forEach(function (k) { window.lcSetDataset(prefix + "." + k, d.datasets[k] || []); });
        Object.keys(d.classes).forEach(function (n) {
          var s = d.classes[n]; s.remote = { name: name, cls: n, prefix: prefix };
          window.lcModels[prefix + "." + n] = s;
          if (known.indexOf(n) < 0) known.push(n);
          window.lcSetDataset(prefix + "." + n, d.rows[n] || []);
        });
        mpReady().then(function (mp) {
          /* a client page may run no Python of its own yet: the runtime goes in first, once */
          var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
          var pre = window._lcModelPreIn === mp ? "" : preamble + "\n";
          runPy(mp, pre + "_lc_remote_bind(" + JSON.stringify(prefix) + "," + JSON.stringify(name) + "," +
            JSON.stringify(JSON.stringify(Object.keys(d.classes))) + "," + JSON.stringify(JSON.stringify(d.funcs || [])) + ")");
          window._lcModelPreIn = mp;
        }).catch(function (e) { console.error("[lc-model import]", e); });
        document.dispatchEvent(new CustomEvent("lc-model-changed"));
        return;
      }
      if ((d.t === "served" || d.t === "refused") && typeof d.id === "string" && d.id.indexOf(me + "#page#") === 0) {
        /* a page's answer: where the browser reaches it, or why not — one row
           anyone can read (m.page), and the promise the asker holds */
        var ok = d.t === "served";
        window.lcSetDataset(prefix + ".page", [{ path: d.path || "", file: ok ? (d.file || "") : "", url: ok ? (d.url || "") : "", via: d.via || "", error: ok ? "" : (d.result || "") }]);
        var w = asked[d.id]; delete asked[d.id];
        if (w) { clearTimeout(w.quiet); ok ? w.ok(d) : w.no(new Error(d.result || "not served")); }
        return;
      }
      if ((d.t === "done" || d.t === "refused") && typeof d.id === "string" && d.id.indexOf(me + "#") === 0) {
        var fn = d.id.slice(me.length + 1);
        /* a function's answer is one row anyone can read: a grid, a cell, a proof */
        window.lcSetDataset(prefix + "." + fn, [{ result: d.t === "done" ? d.result : "", error: d.t === "refused" ? d.result : "" }]);
      }
    };
    function follow() {
      try { ch.postMessage({ t: "follow", from: me }); } catch (e) {}
      clearTimeout(quiet); quiet = setTimeout(nobody, patience);
    }
    function ping() {
      /* the heartbeat: a server that left answers nothing; one that is there says pong, no spec */
      try { ch.postMessage({ t: "ping", from: me }); } catch (e) {}
      clearTimeout(quiet); quiet = setTimeout(nobody, patience);
    }
    window.lcRemoteOps = window.lcRemoteOps || {};
    var asked = {};
    window.lcRemoteOps[prefix] = {
      send: function (msg) { msg.from = me; try { ch.postMessage(msg); } catch (e) {} },
      call: function (fn, args) { var id = me + "#" + fn; this.send({ t: "call", fn: fn, args: args, id: id }); return id; },
      page: function (path) {
        /* ask the server for a path: a promise of {file, url} — refused, or
           nobody answering within the moment, rejects with the words */
        var self = this, id = me + "#page#" + Math.random().toString(36).slice(2, 7);
        return new Promise(function (ok, no) {
          asked[id] = { ok: ok, no: no, quiet: setTimeout(function () { delete asked[id]; no(new Error("nobody serves lc://" + name + " — open its server page")); }, 2500) };
          self.send({ t: "page", path: path, id: id });
        });
      }
    };
    follow();
    /* a server that leaves says no goodbye: ask again now and then; silence says it */
    tick = setInterval(function () { if (gone) return; if (!el.isConnected) { live[prefix] && live[prefix] === stop && delete live[prefix]; stop(); return; } if (el.hasAttribute("data-lc-nobody")) follow(); else ping(); }, 4000);
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.inspector, pre.inspector", upgradeInspector);
    window.lcRegisterUpgrader(".highlighter-rouge.model, pre.model, p.model", upgradeModel);
    window.lcRegisterUpgrader("p.server", upgradeServer);
    window.lcAdoptRows = upgradeRows;   /* dataset.md delegates of= here — one grammar */
    window.lcPySend = pySend;           /* console bridges hand verdicts to page python */
  }
})();
</script>
