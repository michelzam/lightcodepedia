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
  rankdir=BT; nodesep=0.25;
  graph [penwidth=0.1, splines=ortho, fontsize=12, fontname="Helvetica,Arial,sans-serif"];
  node [fontname="Helvetica,Arial,sans-serif", penwidth=0.5, shape=record, style=filled, color=lightgray, fillcolor=white, fontsize=12, margin="0.18,0.05"];
  edge [fontname="Helvetica,Arial,sans-serif", penwidth=0.2];
  subgraph cluster_pkg_kore {
    label="⚙️ kore"; labeljust=l; fontsize=12; fontcolor="gray40";
    style=filled; fillcolor="gray98"; color="gray85"; margin=16; penwidth=0.3;
    Object [label="{🪵 Object|🔤 id\l|}"]
    Page [label="{📄 Page|🔤 id\l|⏵ feature\l⏵ features\l}"]
    Dataset [label="{🗃️ Dataset|🔘 loaded\l🔢 count\l|}"]
    Bar [label="{▮ Bar|🔢 value\l🔤 color\l|}"]
  }
  subgraph cluster_pkg_ui {
    label="🎨 ui"; labeljust=l; fontsize=12; fontcolor="gray40";
    style=filled; fillcolor="gray98"; color="gray85"; margin=16; penwidth=0.3;
    Block [label="{🧩 Block|🔘 exists\l🔘 visible\l🔤 text\l|⏵ click\l⏵ has_class\l}"]
    Datagrid [label="{▦ Datagrid|🔢 row_count\l🔤⦙ headers\l📦⦙ rows\l|⏵ header\l}"]
    Chart [label="{📈 Chart|🔤 type\l🔤 x\l🔤 y\l🔢 bar_count\l🔢 point_count\l|}"]
    Feature [label="{🦄 Feature|🔤 title\l🔤 status\l|⏵ run\l}"]
    Button [label="{🖱️ Button|🔤 text\l🔤 color\l|⚡ on_click\l}"]
    Accordion [label="{🪗 Accordion||⏵ open\l⏵ close\l⏵ sections\l}"]
    Agent [label="{🤖 Agent|🔡 system\l🔤 model\l🔢 temperature\l🔢 max_tokens\l🔤 intro\l🔤 placeholder\l|⏵ ask\l}"]
    Cards [label="{🃏 Cards|🔤 cols\l🔢 gap\l|}"]
    Carousel [label="{🎠 Carousel|🔢 delay\l|⏵ next\l⏵ prev\l⏵ goto\l}"]
    Code [label="{📄 Code|🔤 path\l🔤 src\l🔤 lang\l🔤 title\l🔤 repo\l🔤 branch\l|}"]
    Dropdown [label="{🔽 Dropdown|🔤 label\l|⏵ open\l⏵ close\l}"]
    EmbedPage [label="{🖼️ EmbedPage|🔢 height\l|}"]
    Folder [label="{📁 Folder|🔤 cols\l🔘 show_private\l|}"]
    Form [label="{📝 Form|🔤 title\l🔤 format\l🔘 editable\l|⏵ submit\l}"]
    Grid [label="{▤ Grid|🔤 cols\l🔢 gap\l🔤 headings\l|}"]
    Map [label="{🗺️ Map|🔢 lat\l🔢 lng\l🔢 zoom\l🔢 height\l|⏵ pan_to\l⏵ set_zoom\l}"]
    Menu [label="{🍔 Menu||⏵ items\l}"]
    Pytutor [label="{🔬 Pytutor|🔢 height\l🔤 bound_to\l|}"]
    Qr [label="{🔳 Qr|🔢 size\l|}"]
    Quiz [label="{❓ Quiz|🎛️ state\l🔘 multi\l🔘 graded\l|▹ check ▹\l}"]
    Radio [label="{📻 Radio|🔤 selected\l|⏵ select\l}"]
    Recorder [label="{🎥 Recorder|🎛️ state\l🔤 pip\l🔢 size\l🔢 zoom\l🔢 fps\l|▹ start ▹\l▹ stop ▹\l}"]
    Run [label="{🐍 Run|🔢 rows\l🔘 folded\l🔘 silent\l🔡 init\l🔤 bound\l🔤 expected\l|⏵ run\l}"]
    Scrollable [label="{📜 Scrollable|🔢 height\l|}"]
    Slides [label="{🎞️ Slides|🔢 current\l|⏵ next\l⏵ prev\l⏵ goto\l}"]
    Tabs [label="{📑 Tabs|🔢 active\l|⏵ select\l}"]
    Text [label="{🔤 Text||}"]
  }
  Datagrid -> Dataset [arrowhead=open, color=blue, fontcolor=blue, labeldistance=2, headlabel="bind", fontsize=8]
  Chart -> Dataset [arrowhead=open, color=blue, fontcolor=blue, labeldistance=2, headlabel="bind", fontsize=8]
  Chart -> Bar [arrowhead=open, color=blue, fontcolor=blue, labeldistance=2, headlabel="⦙ bars", fontsize=8]
  Button -> Page [arrowhead=open, color=blue, fontcolor=blue, labeldistance=2, headlabel="page", fontsize=8]
  Form -> Datagrid [arrowhead=open, color=blue, fontcolor=blue, labeldistance=2, headlabel="bound", fontsize=8]
  subgraph cluster_states_Quiz {
    label="🎛️ Quiz states"; fontsize=10;
    style="filled,rounded"; fillcolor="white"; color="gray85"; margin=12;
    node [fontname="Helvetica,Arial,sans-serif", shape=record, style="filled,rounded", fillcolor="gray95", color="gray", fontsize=12, penwidth=0.3]
    edge [style=solid, arrowhead=open, penwidth=0.2, arrowsize=0.5, fontsize=10]
    st_Quiz_pending [label="➡️ pending"]
    st_Quiz_graded [label="graded"]
  }
  st_Quiz_pending -> st_Quiz_graded [xlabel="check", color="gray45", fontcolor="gray45", constraint=false]
  st_Quiz_pending -> Quiz [style=dashed, arrowhead=none, color="gray70", constraint=false]
  subgraph cluster_states_Recorder {
    label="🎛️ Recorder states"; fontsize=10;
    style="filled,rounded"; fillcolor="white"; color="gray85"; margin=12;
    node [fontname="Helvetica,Arial,sans-serif", shape=record, style="filled,rounded", fillcolor="gray95", color="gray", fontsize=12, penwidth=0.3]
    edge [style=solid, arrowhead=open, penwidth=0.2, arrowsize=0.5, fontsize=10]
    st_Recorder_idle [label="➡️ idle"]
    st_Recorder_recording [label="recording"]
    st_Recorder_stopped [label="stopped"]
  }
  st_Recorder_idle -> st_Recorder_recording [xlabel="start", color="gray45", fontcolor="gray45", constraint=false]
  st_Recorder_recording -> st_Recorder_stopped [xlabel="stop", color="gray45", fontcolor="gray45", constraint=false]
  st_Recorder_idle -> Recorder [style=dashed, arrowhead=none, color="gray70", constraint=false]
  Block -> Object [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Page -> Object [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Dataset -> Object [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Bar -> Object [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Datagrid -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Chart -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Feature -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Button -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Accordion -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Agent -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Cards -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Carousel -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Code -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Dropdown -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  EmbedPage -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Folder -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Form -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Grid -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Map -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Menu -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Pytutor -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Qr -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Quiz -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Radio -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Recorder -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Run -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Scrollable -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Slides -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Tabs -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  Text -> Block [arrowhead=empty, color=black, penwidth=0.3, constraint=true]
  subgraph cluster_legend {
    style=invis;
    __legend [label="{Legend|🔤 str\l🔡 long str\l🔢 int / float\l🔘 bool\l📅 date\l🕗 datetime\l🔒 password\l📦⦙ list of [type]\l📦 object ref\l⚡ event or code\l|⏵ method\l▹ guarded method (preconditions)\lmethod ▹ sets a state\l🎛️ state\l|🎛️ state machine\l➡️ initial state\l|➭  inherits from\l =  default value\l}", style="filled", fillcolor="gray98", color="gray80", fontcolor="#505050", fontsize=10]
  }
}
```

Regenerate with `python tools/gen_component_diagram.py`.
