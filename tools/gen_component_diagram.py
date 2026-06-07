"""
Generate a Mermaid classDiagram for docs/components/model.md.

Run from repo root:
  python tools/gen_component_diagram.py

Reads:   docs/_includes/steps_runtime.md  (Python preamble via AST)
Writes:  docs/components/model.md
"""

import ast
import re
import textwrap

# ── type icons (matches module_decorator.py) ──────────────────────────────────
ICON = {
    "str":      "🔤",
    "int":      "🔢",
    "float":    "🔢",
    "bool":     "🔘",
    "list":     "⦙",
    "ref":      "🔗",   # object reference / association
    "event":    "⚡️",
}
SETTABLE = "✏️"
METHOD   = "⏵"

# ── hand-annotated type map (preamble has no annotations) ────────────────────
# format: class → {prop_name: (type_key, settable)}
# Props listed in source-code order (preserved via ordered dict).
TYPE_MAP = {
    "Object":      {},
    "Block":       {
        "exists":    ("bool",  False),
        "visible":   ("bool",  False),
        "text":      ("str",   False),
    },
    "Dataset":     {
        "loaded":    ("bool",  False),
        "count":     ("int",   False),
    },
    "Bar":         {
        "value":     ("float", False),
        "color":     ("str",   True),
    },
    "Datagrid":    {
        "row_count": ("int",   False),
        "headers":   ("list",  False),
        "rows":      ("list",  False),
    },
    "Chart":       {
        "bars":      ("list",  False),   # drawn as association
        "bind":      ("ref",   False),   # drawn as association
        "type":      ("str",   False),
        "x":         ("str",   False),
        "y":         ("str",   False),
        "bar_count": ("int",   False),
        "point_count":("int",  False),
    },
    "FeatureCard": {
        "title":      ("str",  False),
        "status":     ("str",  False),
        "run_button": ("ref",  False),   # drawn as association
    },
    "Button":      {
        "text":      ("str",   True),
        "color":     ("str",   True),
        "page":      ("ref",   False),   # drawn as association
    },
    "Page":        {},
}

# properties rendered as association arrows instead of inline members
ASSOC = {
    "Chart":       [("bind",       "Dataset", "bind"),
                    ("bars",       "Bar",     "⦙ bars")],
    "FeatureCard": [("run_button", "Block",   "run_button")],
    "Button":      [("page",       "Page",    "page")],
}

# class emoji icons (distinct from type icons)
CLASS_ICON = {
    "Object":      "🧱",
    "Block":       "🧩",
    "Dataset":     "🗃️",
    "Bar":         "▮",
    "Datagrid":    "▦",
    "Chart":       "📈",
    "FeatureCard": "🦄",
    "Button":      "🖱️",
    "Page":        "📄",
}


def parse_preamble(path="docs/_includes/steps_runtime.md"):
    raw = open(path).read()
    m = re.search(r'<script id="lc-steps-preamble" type="text/plain">(.*?)</script>',
                  raw, re.S)
    if not m:
        raise SystemExit("preamble not found")
    return ast.parse(m.group(1))


def collect_classes(tree):
    """Return list of (name, bases, props_ordered, settable_set, methods) for public classes."""
    out = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if node.name.startswith("_"):
            continue                             # skip private helpers (_Ctx etc.)
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        props_ordered, settable, methods = [], set(), []
        seen_props = set()
        for b in node.body:
            if not isinstance(b, ast.FunctionDef):
                continue
            is_prop   = any(isinstance(d, ast.Name) and d.id == "property"
                            for d in b.decorator_list)
            is_setter = any(isinstance(d, ast.Attribute) and d.attr == "setter"
                            for d in b.decorator_list)
            if is_prop or is_setter:
                if b.name not in seen_props:
                    props_ordered.append(b.name)
                    seen_props.add(b.name)
                if is_setter:
                    settable.add(b.name)
            elif not b.name.startswith("_"):
                if b.name not in methods:        # skip duplicates (overloads)
                    methods.append(b.name)
        out.append((node.name, bases, props_ordered, settable, methods))
    return out


def member_line(prop, type_key, is_settable, assoc_set):
    """Return indented member line or None if rendered as association."""
    if prop in assoc_set:
        return None
    icon = ICON.get(type_key, "📦")
    prefix = SETTABLE if is_settable else ""
    return f"    {prefix}{icon} {prop}"


def render_diagram(classes):
    lines = ["classDiagram", "  direction TB", ""]

    for name, bases, props, settable, methods in classes:
        label = f"{CLASS_ICON.get(name, '')} {name}".strip()
        lines.append(f'  class {name}["{label}"] {{')

        assoc_set = {a[0] for a in ASSOC.get(name, [])}
        tmap = TYPE_MAP.get(name, {})

        for prop in props:                       # source-code order preserved
            if prop in assoc_set:
                continue
            type_key, _ = tmap.get(prop, ("ref", False))
            is_set = prop in settable
            icon = ICON.get(type_key, "📦")
            pfx  = SETTABLE if is_set else ""
            lines.append(f"    {pfx}{icon} {prop}")

        for m in methods:
            if m not in ("__bool__", "__eq__", "__init__"):
                lines.append(f"    {METHOD} {m}()")

        lines.append("  }")
        lines.append("")

    # ── inheritance ───────────────────────────────────────────────────────────
    lines.append("  %% inheritance (parent above child)")
    for name, bases, *_ in classes:
        for base in bases:
            lines.append(f"  {base} <|-- {name}")
    lines.append("")

    # ── associations ──────────────────────────────────────────────────────────
    lines.append("  %% associations")
    for src, assocs in ASSOC.items():
        for prop, target, label in assocs:
            lines.append(f"  {src} --> {target} : {label}")

    return "\n".join(lines)


def render_page(diagram_src):
    legend_rows = [
        ("🔤", "`str`"),
        ("🔢", "`int` / `float`"),
        ("🔘", "`bool`"),
        ("⦙",  "`list`"),
        ("🔗", "object reference"),
        ("✏️", "settable (has setter)"),
        ("⚡️", "event handler"),
        ("⏵", "method"),
    ]
    legend = "\n".join(
        f"| {icon} | {desc} |"
        for icon, desc in legend_rows
    )

    return f"""\
---
title: Component Model
---

# Component Model

The **coder-side Python API** available in every `.feature` step and `.button` handler.
Reach any component via `self.page.<data-lc-id>` — the page resolver returns a typed wrapper.

```mermaid
{diagram_src}
```

## Icon legend

| Icon | Meaning |
|------|---------|
{legend}

All classes live in the steps runtime (`docs/_includes/steps_runtime.md`).
Regenerate this page with `python tools/gen_component_diagram.py`.
"""


if __name__ == "__main__":
    tree = parse_preamble()
    classes = collect_classes(tree)
    diagram = render_diagram(classes)
    page = render_page(diagram)
    out = "docs/components/model.md"
    with open(out, "w") as f:
        f.write(page)
    print(f"Wrote {out}")
    print()
    print("--- Mermaid source ---")
    print(diagram)
