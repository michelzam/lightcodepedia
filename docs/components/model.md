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

  subgraph cluster_runtime {
    label   = "🔧 runtime"
    style   = "filled"
    fillcolor = "aliceblue"
    color   = "grey75"
    margin  = 20
    penwidth = 0.3

    Object [label = "{🪵 Object|🔤 id\l|}"]
    Block [label = "{🧩 Block|🔘 exists\l🔘 visible\l🔤 text\l|⏵ click\l⏵ has_class\l}"]
    Dataset [label = "{🗃️ Dataset|🔘 loaded\l🔢 count\l|}"]
    Page [label = "{📄 Page||⏵ feature\l⏵ features\l}"]
    Bar [label = "{▮ Bar|🔢 value\l🔤 color\l|}"]
    Datagrid [label = "{▦ Datagrid|🔢 row_count\l🔤⦙ headers\l📦⦙ rows\l|⏵ header\l}"]
    Chart [label = "{📈 Chart|🔤 type\l🔤 x\l🔤 y\l🔢 bar_count\l🔢 point_count\l|}"]
    FeatureCard [label = "{🦄 FeatureCard|🔤 title\l🔤 status\l📦 run_button\l|⏵ nth\l}"]
    Button [label = "{🖱️ Button|🔤 text\l🔤 color\l|⏵ click\l}"]
  }

  subgraph cluster_builder {
    label     = ""
    style     = invis
    builder_gap [label = "{🏗️ builder — no typed wrapper yet|Accordion · Agent · Cards · Carousel · Code\lDropdown · EmbedPage · Folder · Form · Grid\lMap · Menu · Pytutor · Qr · Quiz\lRadio · Recorder · Run · Scrollable · Slides\lTabs · Text\l}",
                 shape = record, style = "filled, dashed, rounded",
                 fillcolor = "lightyellow", color = "gray60",
                 fontsize = 10]
  }

  subgraph cluster_legend {
    label   = ""
    style   = invis
    legend [label = "{Legend|🔤 str\l🔡 long str\l🔢 int / float\l🔘 bool\l📅 date\l🕗 datetime\l🔒 password\l📦⦙ list of [type]\l📦 object ref\l⚡ event or code\l|⏵ method\l|➭  inherits from\l| =  default value\l  /  derived\l}",
            shape = record, style = "filled, rounded",
            fillcolor = "gray98", color = "gray80",
            fontcolor = "#505050"]
  }

  // inheritance
  Block -> Object  [color = black, penwidth = 0.3, arrowhead = normal]
  Dataset -> Object  [color = black, penwidth = 0.3, arrowhead = normal]
  Page -> Object  [color = black, penwidth = 0.3, arrowhead = normal]
  Bar -> Object  [color = black, penwidth = 0.3, arrowhead = normal]
  Datagrid -> Block  [color = black, penwidth = 0.3, arrowhead = normal]
  Chart -> Block  [color = black, penwidth = 0.3, arrowhead = normal]
  FeatureCard -> Block  [color = black, penwidth = 0.3, arrowhead = normal]
  Button -> Block  [color = black, penwidth = 0.3, arrowhead = normal]

  // builder gap → Block (generic fallback, one summary edge)
  builder_gap -> Block  [style = dashed, color = "gray60", arrowhead = open,   constraint = false,   xlabel = "uses Block", fontsize = 8, fontcolor = "gray50"]

  // associations
  Datagrid -> Dataset  [dir = forward, arrowhead = open, constraint = false,   color = "steelblue", fontcolor = "steelblue",   xlabel = "bind", fontsize = 8]
  Chart -> Dataset  [dir = forward, arrowhead = open, constraint = false,   color = "steelblue", fontcolor = "steelblue",   xlabel = "bind", fontsize = 8]
  Chart -> Bar  [dir = forward, arrowhead = open, constraint = false,   color = "steelblue", fontcolor = "steelblue",   xlabel = "⦙ bars", fontsize = 8]
  Button -> Page  [dir = forward, arrowhead = open, constraint = false,   color = "steelblue", fontcolor = "steelblue",   xlabel = "page", fontsize = 8]
}
```

Regenerate with `python tools/gen_component_diagram.py`.
