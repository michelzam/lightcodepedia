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
digraph component_model {
  rankdir=BT; nodesep=0.35; ranksep=0.6;
  graph [splines=ortho, fontname="Monaco,monospace", fontsize=11];
  node [shape=record, style="filled,rounded", fillcolor="gray97", color="gray75", fontname="Monaco,monospace", fontsize=11, penwidth=0.5];
  edge [penwidth=0.4, arrowsize=0.8, fontsize=8];
  Object [label="{🪵 Object|🔤 id\l|}"]
  Block [label="{🧩 Block|🔘 exists\l🔘 visible\l🔤 text\l|⏵ click\l⏵ has_class\l}"]
  Page [label="{📄 Page|🔤 id\l|⏵ feature\l⏵ features\l}"]
  Dataset [label="{🗃️ Dataset|🔘 loaded\l🔢 count\l|}"]
  Bar [label="{▮ Bar|🔢 value\l🔤 color\l|}"]
  Datagrid [label="{▦ Datagrid|🔢 row_count\l🔤⦙ headers\l📦⦙ rows\l|⏵ header\l}"]
  Datagrid -> Dataset [constraint=false, arrowhead=open, color=steelblue, fontcolor=steelblue, xlabel="bind"]
  Chart [label="{📈 Chart|🔤 type\l🔤 x\l🔤 y\l🔢 bar_count\l🔢 point_count\l|}"]
  Chart -> Dataset [constraint=false, arrowhead=open, color=steelblue, fontcolor=steelblue, xlabel="bind"]
  Chart -> Bar [constraint=false, arrowhead=open, color=steelblue, fontcolor=steelblue, xlabel="⦙ bars"]
  Feature [label="{🦄 Feature|🔤 title\l🔤 status\l|⏵ run\l}"]
  Button [label="{🖱️ Button|🔤 text\l🔤 color\l|⚡ on_click\l}"]
  Button -> Page [constraint=false, arrowhead=open, color=steelblue, fontcolor=steelblue, xlabel="page"]
  Accordion [label="{🪗 Accordion||⏵ open\l⏵ close\l⏵ sections\l}"]
  Agent [label="{🤖 Agent|🔡 system\l🔤 model\l🔢 temperature\l🔢 max_tokens\l🔤 intro\l🔤 placeholder\l|⏵ ask\l}"]
  Cards [label="{🃏 Cards|🔤 cols\l🔢 gap\l|}"]
  Carousel [label="{🎠 Carousel|🔢 delay\l|⏵ next\l⏵ prev\l⏵ goto\l}"]
  Code [label="{📄 Code|🔤 path\l🔤 src\l🔤 lang\l🔤 title\l🔤 repo\l🔤 branch\l|}"]
  Dropdown [label="{🔽 Dropdown|🔤 label\l|⏵ open\l⏵ close\l}"]
  EmbedPage [label="{🖼️ EmbedPage|🔢 height\l|}"]
  Folder [label="{📁 Folder|🔤 cols\l🔘 show_private\l|}"]
  Form [label="{📝 Form|🔤 title\l🔤 format\l🔘 editable\l|⏵ submit\l}"]
  Form -> Datagrid [constraint=false, arrowhead=open, color=steelblue, fontcolor=steelblue, xlabel="bound"]
  Grid [label="{▤ Grid|🔤 cols\l🔢 gap\l🔤 headings\l|}"]
  Map [label="{🗺️ Map|🔢 lat\l🔢 lng\l🔢 zoom\l🔢 height\l|⏵ pan_to\l⏵ set_zoom\l}"]
  Menu [label="{🍔 Menu||⏵ items\l}"]
  Pytutor [label="{🔬 Pytutor|🔢 height\l🔤 bound_to\l|}"]
  Qr [label="{🔳 Qr|🔢 size\l|}"]
  Quiz [label="{❓ Quiz|🎛️ state\l🔘 multi\l🔘 graded\l|▹ check ▹\l}"]
  subgraph cluster_states_Quiz {
    label="🎛️ Quiz states"; fontsize=10;
    style="rounded,filled"; fillcolor="white"; color="gray85";
    node [shape=box, style="rounded,filled", fillcolor="gray95", color="gray", fontsize=10, penwidth=0.3]
    st_Quiz_pending [label="➡️ pending"]
    st_Quiz_graded [label="graded"]
  }
  st_Quiz_pending -> st_Quiz_graded [xlabel="check", arrowhead=open, color="gray45", fontcolor="gray45", penwidth=0.3, constraint=false]
  st_Quiz_pending -> Quiz [style=dashed, arrowhead=none, color="gray70", constraint=false]
  Radio [label="{📻 Radio|🔤 selected\l|⏵ select\l}"]
  Recorder [label="{🎥 Recorder|🎛️ state\l🔤 pip\l🔢 size\l🔢 zoom\l🔢 fps\l|▹ start ▹\l▹ stop ▹\l}"]
  subgraph cluster_states_Recorder {
    label="🎛️ Recorder states"; fontsize=10;
    style="rounded,filled"; fillcolor="white"; color="gray85";
    node [shape=box, style="rounded,filled", fillcolor="gray95", color="gray", fontsize=10, penwidth=0.3]
    st_Recorder_idle [label="➡️ idle"]
    st_Recorder_recording [label="recording"]
    st_Recorder_stopped [label="stopped"]
  }
  st_Recorder_idle -> st_Recorder_recording [xlabel="start", arrowhead=open, color="gray45", fontcolor="gray45", penwidth=0.3, constraint=false]
  st_Recorder_recording -> st_Recorder_stopped [xlabel="stop", arrowhead=open, color="gray45", fontcolor="gray45", penwidth=0.3, constraint=false]
  st_Recorder_idle -> Recorder [style=dashed, arrowhead=none, color="gray70", constraint=false]
  Run [label="{🐍 Run|🔢 rows\l🔘 folded\l🔘 silent\l🔡 init\l🔤 bound\l🔤 expected\l|⏵ run\l}"]
  Scrollable [label="{📜 Scrollable|🔢 height\l|}"]
  Slides [label="{🎞️ Slides|🔢 current\l|⏵ next\l⏵ prev\l⏵ goto\l}"]
  Tabs [label="{📑 Tabs|🔢 active\l|⏵ select\l}"]
  Text [label="{🔤 Text||}"]
  __legend [label="{Legend|🔤 str\l🔡 long str\l🔢 int / float\l🔘 bool\l📅 date\l🕗 datetime\l🔒 password\l📦⦙ list of [type]\l📦 object ref\l⚡ event or code\l|⏵ method\l▹ guarded method (preconditions)\lmethod ▹ sets a state\l🎛️ state\l|🎛️ state machine\l➡️ initial state\l|➭  inherits from\l =  default value\l}", fillcolor="gray98", color="gray80", fontcolor="#505050"]
  edge [arrowhead=empty, arrowsize=0.9, color=black, penwidth=0.5];
  __j_Object [shape=point, width=0.06, color="gray50", style=filled, fillcolor="gray50"]
  Block -> __j_Object [dir=none, arrowhead=none]
  Page -> __j_Object [dir=none, arrowhead=none]
  Dataset -> __j_Object [dir=none, arrowhead=none]
  Bar -> __j_Object [dir=none, arrowhead=none]
  __j_Object -> Object
  __j_Block [shape=point, width=0.06, color="gray50", style=filled, fillcolor="gray50"]
  Datagrid -> __j_Block [dir=none, arrowhead=none]
  Chart -> __j_Block [dir=none, arrowhead=none]
  Feature -> __j_Block [dir=none, arrowhead=none]
  Button -> __j_Block [dir=none, arrowhead=none]
  Accordion -> __j_Block [dir=none, arrowhead=none]
  Agent -> __j_Block [dir=none, arrowhead=none]
  Cards -> __j_Block [dir=none, arrowhead=none]
  Carousel -> __j_Block [dir=none, arrowhead=none]
  Code -> __j_Block [dir=none, arrowhead=none]
  Dropdown -> __j_Block [dir=none, arrowhead=none]
  EmbedPage -> __j_Block [dir=none, arrowhead=none]
  Folder -> __j_Block [dir=none, arrowhead=none]
  Form -> __j_Block [dir=none, arrowhead=none]
  Grid -> __j_Block [dir=none, arrowhead=none]
  Map -> __j_Block [dir=none, arrowhead=none]
  Menu -> __j_Block [dir=none, arrowhead=none]
  Pytutor -> __j_Block [dir=none, arrowhead=none]
  Qr -> __j_Block [dir=none, arrowhead=none]
  Quiz -> __j_Block [dir=none, arrowhead=none]
  Radio -> __j_Block [dir=none, arrowhead=none]
  Recorder -> __j_Block [dir=none, arrowhead=none]
  Run -> __j_Block [dir=none, arrowhead=none]
  Scrollable -> __j_Block [dir=none, arrowhead=none]
  Slides -> __j_Block [dir=none, arrowhead=none]
  Tabs -> __j_Block [dir=none, arrowhead=none]
  Text -> __j_Block [dir=none, arrowhead=none]
  __j_Block -> Block
}
```

Regenerate with `python tools/gen_component_diagram.py`.
