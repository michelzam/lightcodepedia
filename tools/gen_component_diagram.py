"""
Generate a Graphviz DOT class diagram for docs/components/model.md.

Follows the same conventions as
  usecases/module_manager/backend/module_decorator.py :
  • rankdir = BT  (children at bottom, parents at top)
  • splines = ortho  (stair-step edges)
  • record nodes  (icon | attrs | methods sections)
  • inheritance:   child -> parent  [penwidth=0.3, arrowhead=normal]
  • association:   owner -> target  [constraint=false, dir=forward,
                                    headlabel="…", fontcolor=blue]
  • gap classes:   owner -> Block   [style=dashed, arrowhead=open]
  • legend & packages as cluster subgraphs

Run from repo root:
  python tools/gen_component_diagram.py

Reads:   docs/_includes/steps_runtime.md  (Python preamble via AST)
         docs/components/*.md              (builder-side gap report)
Writes:  docs/components/model.md
"""

import ast
import os
import re
import glob

# ─────────────────────────────── type icons ───────────────────────────────────
# Strictly mirrors the legend in module_decorator.py
ICON = {
    "str":      "🔤",
    "long_str": "🔡",
    "int":      "🔢",
    "float":    "🔢",
    "bool":     "🔘",
    "date":     "📅",
    "datetime": "🕗",
    "password": "🔒",
    "list":     "⦙",   # combined as  <elem-icon>⦙  e.g. 🔤⦙
    "ref":      "📦",
    "event":    "⚡",
    "method":   "⏵",
}

# ─────────────────────────── class-level emoji ────────────────────────────────
CLASS_ICON = {
    "Object":      "🪵",
    "Block":       "🧩",
    "Dataset":     "🗃️",
    "Bar":         "▮",
    "Datagrid":    "▦",
    "Chart":       "📈",
    "FeatureCard": "🦄",
    "Button":      "🖱️",
    "Page":        "📄",
}

# ─────────── per-property annotations (preamble has no type hints) ────────────
# class → { prop: type_spec }
# type_spec: plain type key -or- ("elem", "list") for typed collections
TYPE_MAP = {
    "Object":      {"id": "str"},
    "Block":       {"exists": "bool", "visible": "bool", "text": "str"},
    "Dataset":     {"loaded": "bool", "count": "int"},
    "Bar":         {"value": "float", "color": "str"},
    "Datagrid":    {"row_count": "int",
                    "headers":   ("str",  "list"),   # list[str]  → 🔤⦙
                    "rows":      ("ref",  "list")},  # list[dict] → 📦⦙
    "Chart":       {"type": "str", "x": "str", "y": "str",
                    "bar_count": "int", "point_count": "int"},
    "FeatureCard": {"title": "str", "status": "str"},
    "Button":      {"text": "str", "color": "str"},
    "Page":        {},
}

# members hidden from the diagram (internal API, not needed by the builder)
HIDDEN = {
    "Object": {"all", "q", "qq", "attr"},
}

# association edges: owner → target (constraint=false, do not affect rank)
# (prop, target, role_label)
ASSOC = {
    "Datagrid":    [("bind", "Dataset", "bind")],
    "Chart":       [("bind", "Dataset", "bind"),
                    ("bars", "Bar",     "⦙ bars")],
    "Button":      [("page", "Page",    "page")],
    # run_button omitted: FeatureCard→Block is noise (already inherits Block)
}

# display order of runtime classes (parents before children)
RUNTIME_ORDER = ["Object", "Block", "Dataset", "Page",
                 "Bar", "Datagrid", "Chart", "FeatureCard", "Button"]

# builder widgets that already have a typed wrapper (skip in gap report)
WRAPPED = {"chart", "dataset", "datagrid", "feature", "button", "block"}

# component pages that are not gallery widgets
NON_WIDGET = {"index", "sitemap", "deploys", "model"}


# ─────────────────────────── helpers ─────────────────────────────────────────

def icon_for(spec):
    """spec = type key str | ("elem_key", "list")  → combined icon string."""
    if isinstance(spec, tuple):
        elem, _ = spec
        return ICON.get(elem, "📦") + ICON["list"]
    return ICON.get(spec, "📦")


def esc(s):
    """Escape for Graphviz record label content."""
    return s.replace("\\", "\\\\").replace('"', '\\"') \
            .replace("{", "\\{").replace("}", "\\}") \
            .replace("<", "\\<").replace(">", "\\>")


def parse_preamble(path="docs/_includes/steps_runtime.md"):
    raw = open(path).read()
    m = re.search(
        r'<script id="lc-steps-preamble" type="text/plain">(.*?)</script>',
        raw, re.S)
    if not m:
        raise SystemExit("preamble script block not found in " + path)
    return ast.parse(m.group(1))


def collect_classes(tree):
    """Return OrderedDict name → {bases, props (ordered), methods (ordered)}."""
    out = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name.startswith("_"):
            continue
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        props, methods, seen_p, seen_m = [], [], set(), set()
        for b in node.body:
            if not isinstance(b, ast.FunctionDef):
                continue
            is_prop   = any(isinstance(d, ast.Name) and d.id == "property"
                            for d in b.decorator_list)
            is_setter = any(isinstance(d, ast.Attribute) and d.attr == "setter"
                            for d in b.decorator_list)
            if is_prop or is_setter:
                if b.name not in seen_p:
                    props.append(b.name)
                    seen_p.add(b.name)
            elif not b.name.startswith("_") and b.name not in seen_m:
                methods.append(b.name)
                seen_m.add(b.name)
        out[node.name] = {"bases": bases, "props": props, "methods": methods}
    return out


def record_label(name, info):
    """Build the Graphviz record label string for a class node."""
    icon  = CLASS_ICON.get(name, "")
    tmap  = TYPE_MAP.get(name, {})
    hidden = HIDDEN.get(name, set())
    assoc_props = {a[0] for a in ASSOC.get(name, [])}

    attrs_parts   = []
    methods_parts = []

    for prop in info["props"]:
        if prop in hidden or prop in assoc_props:
            continue
        ico = icon_for(tmap.get(prop, "ref"))
        attrs_parts.append(f"{esc(ico)} {esc(prop)}\\l")

    for m in info["methods"]:
        if m in hidden:
            continue
        methods_parts.append(f"{esc(ICON['method'])} {esc(m)}\\l")

    title   = f"{esc(icon)} {esc(name)}"
    attrs   = "".join(attrs_parts)
    methods = "".join(methods_parts)

    # Graphviz record: {title | attrs | methods}
    return f'"{{{title}|{attrs}|{methods}}}"'


def gap_components():
    """Builder widgets with no typed wrapper → fall back to Block."""
    out = []
    for path in sorted(glob.glob("docs/components/*.md")):
        stem = os.path.basename(path)[:-3]
        if stem.startswith("_") or stem in WRAPPED or stem in NON_WIDGET:
            continue
        cls = "".join(p.capitalize() for p in re.split(r"[_-]", stem))
        out.append(cls)
    return out


# ─────────────────────────── DOT rendering ───────────────────────────────────

GRAPH_HEADER = """\
digraph component_model {
  rankdir = BT
  nodesep = 0.35
  ranksep = 0.6
  graph [
    splines = ortho
    fontsize = 11
    fontname = "Monaco, monospace"
    penwidth = 0.1
  ]
  node [
    fontname = "Monaco, monospace"
    penwidth  = 0.5
    shape     = record
    style     = "filled, rounded"
    fillcolor = "gray97"
    color     = "gray75"
    fontsize  = 11
  ]
  edge [
    penwidth  = 0.3
    arrowsize = 0.5
    fontsize  = 8
  ]
"""

LEGEND_LABEL = (
    '"{Legend'
    '|🔤 str\\l🔡 long str\\l🔢 int / float\\l🔘 bool\\l'
    '📅 date\\l🕗 datetime\\l🔒 password\\l'
    '📦⦙ list of [type]\\l📦 object ref\\l'
    '⚡ event or code\\l'
    '|⏵ method\\l'
    '|➭  inherits from\\l'
    '| =  default value\\l  /  derived\\l}"'
)


def render(classes):
    L = [GRAPH_HEADER]

    # ── package: runtime ──────────────────────────────────────────────────────
    L.append('  subgraph cluster_runtime {')
    L.append('    label   = "🔧 runtime"')
    L.append('    style   = "filled"')
    L.append('    fillcolor = "aliceblue"')
    L.append('    color   = "grey75"')
    L.append('    margin  = 20')
    L.append('    penwidth = 0.3')
    L.append('')
    for name in RUNTIME_ORDER:
        if name in classes:
            lbl = record_label(name, classes[name])
            L.append(f'    {name} [label = {lbl}]')
    L.append('  }')
    L.append('')

    # ── package: builder gap (single summary node, 5 per row) ────────────────
    gaps = gap_components()
    ROW = 5
    # Escape names first, THEN join with \l (do NOT pass \l through esc() again)
    row_parts = [" · ".join(esc(g) for g in gaps[i:i+ROW])
                 for i in range(0, len(gaps), ROW)]
    rows_content = "\\l".join(row_parts) + "\\l"
    gap_label = f'"{{🏗️ builder — no typed wrapper yet|{rows_content}}}"'
    L.append('  subgraph cluster_builder {')
    L.append('    label     = ""')
    L.append('    style     = invis')
    L.append(f'    builder_gap [label = {gap_label},')
    L.append('                 shape = record, style = "filled, dashed, rounded",')
    L.append('                 fillcolor = "lightyellow", color = "gray60",')
    L.append('                 fontsize = 10]')
    L.append('  }')
    L.append('')

    # ── package: legend ───────────────────────────────────────────────────────
    L.append('  subgraph cluster_legend {')
    L.append('    label   = ""')
    L.append('    style   = invis')
    L.append(f'    legend [label = {LEGEND_LABEL},')
    L.append('            shape = record, style = "filled, rounded",')
    L.append('            fillcolor = "gray98", color = "gray80",')
    L.append('            fontcolor = "#505050"]')
    L.append('  }')
    L.append('')

    # ── inheritance (child -> parent, rankdir=BT puts parent above) ───────────
    L.append('  // inheritance')
    for name in RUNTIME_ORDER:
        for base in classes.get(name, {}).get("bases", []):
            L.append(
                f'  {name} -> {base}'
                '  [color = black, penwidth = 0.3, arrowhead = normal]'
            )
    L.append('')

    # ── builder summary → Block (one dashed edge) ─────────────────────────────
    L.append('  // builder gap → Block (generic fallback, one summary edge)')
    L.append(
        '  builder_gap -> Block'
        '  [style = dashed, color = "gray60", arrowhead = open,'
        '   constraint = false,'
        '   xlabel = "uses Block", fontsize = 8, fontcolor = "gray50"]'
    )
    L.append('')

    # ── associations (owner -> target, constraint=false) ─────────────────────
    # Use xlabel (external label) — headlabel is not supported with splines=ortho
    L.append('  // associations')
    for src, items in ASSOC.items():
        for prop, target, label in items:
            L.append(
                f'  {src} -> {target}'
                f'  [dir = forward, arrowhead = open, constraint = false,'
                f'   color = "steelblue", fontcolor = "steelblue",'
                f'   xlabel = "{esc(label)}", fontsize = 8]'
            )

    L.append('}')
    return "\n".join(L)


def page(diagram):
    return f"""\
---
title: Component Model
---

# Component Model

The **coder-side Python API** available in every `.feature` step and `.button` handler.
Reach any named component via `self.page.<id>` — the resolver returns a typed wrapper.

- **runtime** — typed wrapper classes, introspected from `steps_runtime.md`.
- **builder (no typed wrapper yet)** — gallery widgets that fall back to the generic `Block`
  (dashed arrows). This is the live gap report.

```dot
{diagram}
```

Regenerate with `python tools/gen_component_diagram.py`.
"""


if __name__ == "__main__":
    classes = collect_classes(parse_preamble())
    diagram = render(classes)
    with open("docs/components/model.md", "w") as f:
        f.write(page(diagram))
    print("Wrote docs/components/model.md")
    print()
    print(diagram)
