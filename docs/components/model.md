---
title: Component Model
---

# Component Model

The **coder-side Python API** available in every `.feature` step and `.button` handler.
Reach any component via `self.page.<data-lc-id>` — the page resolver returns a typed wrapper.

```mermaid
classDiagram
  direction TB

  class Object["🧱 Object"] {
    ⏵ all()
    ⏵ q()
    ⏵ qq()
    ⏵ attr()
    ⏵ click()
  }

  class Block["🧩 Block"] {
    🔘 exists
    🔘 visible
    🔤 text
    ⏵ has_class()
  }

  class Dataset["🗃️ Dataset"] {
    🔘 loaded
    🔢 count
  }

  class Datagrid["▦ Datagrid"] {
    🔢 row_count
    ⦙ headers
    ⦙ rows
    ⏵ header()
  }

  class Bar["▮ Bar"] {
    🔢 value
    ✏️🔤 color
  }

  class Chart["📈 Chart"] {
    🔤 type
    🔤 x
    🔤 y
    🔢 bar_count
    🔢 point_count
  }

  class FeatureCard["🦄 FeatureCard"] {
    🔤 title
    🔤 status
    ⏵ nth()
  }

  class Button["🖱️ Button"] {
    ✏️🔤 text
    ✏️🔤 color
    ⏵ click()
  }

  class Page["📄 Page"] {
    ⏵ feature()
    ⏵ features()
  }

  %% inheritance (parent above child)
  Object <|-- Block
  Block <|-- Datagrid
  Object <|-- Bar
  Block <|-- Chart
  Block <|-- FeatureCard
  Block <|-- Button

  %% associations
  Chart --> Dataset : bind
  Chart --> Bar : ⦙ bars
  FeatureCard --> Block : run_button
  Button --> Page : page
```

## Icon legend

| Icon | Meaning |
|------|---------|
| 🔤 | `str` |
| 🔢 | `int` / `float` |
| 🔘 | `bool` |
| ⦙ | `list` |
| 🔗 | object reference |
| ✏️ | settable (has setter) |
| ⚡️ | event handler |
| ⏵ | method |

All classes live in the steps runtime (`docs/_includes/steps_runtime.md`).
Regenerate this page with `python tools/gen_component_diagram.py`.
