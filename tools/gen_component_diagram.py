"""
Generate the build-time component diagram for docs/components/model.md.

Single source of truth = the Python wrapper classes in
docs/_includes/steps_runtime.md. Each class declares its model via
@component(...) and dumps its own DOT via an inherited to_dot() method; the
preamble's module-level to_dot(scope, gaps) assembles the whole graph.

This script just execs that preamble (with a stubbed `js` module so it runs
under CPython) and calls to_dot() — the very same code path the live .diagram
component uses in the browser. No logic is duplicated here.

Run from repo root:
  python tools/gen_component_diagram.py

Reads:   docs/_includes/steps_runtime.md   (the SSOT)
         docs/components/*.md              (to compute the gap report)
Writes:  docs/components/model.md
"""

import glob
import os
import re
import sys
import types

PREAMBLE = "docs/_includes/steps_runtime.md"
OUT = "docs/components/model.md"

# component pages that are not addressable gallery widgets
NON_WIDGET = {"index", "sitemap", "deploys", "model", "diagram"}


def load_runtime():
    """Exec the steps-runtime preamble under CPython and return its namespace."""
    raw = open(PREAMBLE).read()
    m = re.search(
        r'<script id="lc-steps-preamble" type="text/plain">(.*?)</script>',
        raw, re.S)
    if not m:
        raise SystemExit("preamble script block not found in " + PREAMBLE)

    # Stub the MicroPython-only `js` module so the preamble imports cleanly.
    js = types.ModuleType("js")
    js.window = types.SimpleNamespace()
    sys.modules["js"] = js

    ns = {}
    exec(m.group(1), ns)
    return ns


def gap_components(model):
    """Gallery widgets that have no typed wrapper class → fall back to Block."""
    out = []
    for path in sorted(glob.glob("docs/components/*.md")):
        stem = os.path.basename(path)[:-3]
        if stem.startswith("_") or stem in NON_WIDGET:
            continue
        cls = "".join(p.capitalize() for p in re.split(r"[_-]", stem))
        if cls not in model:
            out.append(cls)
    return out


def page(diagram):
    return f"""\
---
title: Component Model
---

# Component Model

The typed **coder-side Python API** available in every `.feature` step and
`.button` handler. Reach any named component via `self.page.<id>` — the resolver
returns the matching wrapper below.

This diagram is generated from the wrapper classes themselves (the single source
of truth in `docs/_includes/steps_runtime.md`): each class declares its knobs and
behaviours via `@component(...)` and dumps its own node through an inherited
`to_dot()`. The same code renders **live** through the [`.diagram`](diagram)
component.

```dot
{diagram}
```

Regenerate with `python tools/gen_component_diagram.py`.
"""


if __name__ == "__main__":
    ns = load_runtime()
    model = ns["_MODEL"]
    to_dot = ns["to_dot"]
    gaps = gap_components(model)
    diagram = to_dot(None, gaps=gaps)
    with open(OUT, "w") as f:
        f.write(page(diagram))
    print(f"Wrote {OUT}  ({len(model)} classes, {len(gaps)} gap components)")
    if gaps:
        print("  gap:", ", ".join(gaps))
