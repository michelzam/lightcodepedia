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
  graph [penwidth=0.1, splines=ortho, fontsize=10, fontname="Source Sans Pro, sans-serif"];
  node [fontname="Source Sans Pro, sans-serif", penwidth=0.5, shape=record, style=filled, color=lightgray, fillcolor=white, fontsize=10];
  edge [fontname="Source Sans Pro, sans-serif", penwidth=0.2, arrowhead=vee, arrowsize=0.8];
  subgraph cluster_pkg_kore {
    label="⚙️ kore"; labeljust=l; fontsize=10; fontcolor="gray40";
    style=filled; fillcolor="gray98"; color="gray85"; margin=16; penwidth=0.3;
    Object [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">◻️ Object</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">id</TD></TR></TABLE>>]
    Page [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📄 Page ➭ ◻️</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">id</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">feature</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">features</TD></TR></TABLE>>]
    Dataset [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🗃️ Dataset ➭ ◻️</TD></TR><HR/><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">loaded</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">count</TD></TR></TABLE>>]
    Bar [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">▮ Bar ➭ ◻️</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">value</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">color</TD></TR></TABLE>>]
  }
  subgraph cluster_pkg_ui {
    label="🎨 ui"; labeljust=l; fontsize=10; fontcolor="gray40";
    style=filled; fillcolor="gray98"; color="gray85"; margin=16; penwidth=0.3;
    Block [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🧩 Block ➭ ◻️</TD></TR><HR/><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">exists</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">visible</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">text</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">click</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">has class</TD></TR></TABLE>>]
    Datagrid [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">▦ Datagrid ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">row count</TD></TR><TR><TD ALIGN="CENTER">🔤⦙</TD><TD ALIGN="LEFT">headers</TD></TR><TR><TD ALIGN="CENTER">📦⦙</TD><TD ALIGN="LEFT">rows</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">header</TD></TR></TABLE>>]
    Chart [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📈 Chart ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">type</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">x</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">y</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">bar count</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">point count</TD></TR></TABLE>>]
    Feature [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🦄 Feature ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">title</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">status</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">run</TD></TR></TABLE>>]
    Button [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🖱️ Button ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">text</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">color</TD></TR><HR/><TR><TD ALIGN="CENTER">⚡</TD><TD ALIGN="LEFT">on click</TD></TR></TABLE>>]
    Accordion [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🪗 Accordion ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">open</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">close</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">sections</TD></TR></TABLE>>]
    Agent [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🤖 Agent ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔡</TD><TD ALIGN="LEFT">system</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">model</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">temperature</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">max tokens</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">intro</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">placeholder</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">ask</TD></TR></TABLE>>]
    Cards [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🃏 Cards ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">cols</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">gap</TD></TR></TABLE>>]
    Carousel [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🎠 Carousel ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">delay</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">next</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">prev</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">goto</TD></TR></TABLE>>]
    Code [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📄 Code ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">path</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">src</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">lang</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">title</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">repo</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">branch</TD></TR></TABLE>>]
    Dropdown [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🔽 Dropdown ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">label</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">open</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">close</TD></TR></TABLE>>]
    EmbedPage [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🖼️ EmbedPage ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">height</TD></TR></TABLE>>]
    Folder [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📁 Folder ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">cols</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">show private</TD></TR></TABLE>>]
    Form [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📝 Form ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">title</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">format</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">editable</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">submit</TD></TR></TABLE>>]
    Grid [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">▤ Grid ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">cols</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">gap</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">headings</TD></TR></TABLE>>]
    Map [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🗺️ Map ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">lat</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">lng</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">zoom</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">height</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">pan to</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">set zoom</TD></TR></TABLE>>]
    Menu [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🍔 Menu ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">items</TD></TR></TABLE>>]
    Pytutor [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🔬 Pytutor ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">height</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">bound to</TD></TR></TABLE>>]
    Qr [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🔳 Qr ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">size</TD></TR></TABLE>>]
    Quiz [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">❓ Quiz ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🎛️</TD><TD ALIGN="LEFT">state</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">multi</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">graded</TD></TR><HR/><TR><TD ALIGN="CENTER">▹</TD><TD ALIGN="LEFT">check ▹</TD></TR></TABLE>>]
    Radio [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📻 Radio ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">selected</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">select</TD></TR></TABLE>>]
    Recorder [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🎥 Recorder ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🎛️</TD><TD ALIGN="LEFT">state</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">pip</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">size</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">zoom</TD></TR><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">fps</TD></TR><HR/><TR><TD ALIGN="CENTER">▹</TD><TD ALIGN="LEFT">start ▹</TD></TR><TR><TD ALIGN="CENTER">▹</TD><TD ALIGN="LEFT">stop ▹</TD></TR></TABLE>>]
    Run [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🐍 Run ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">rows</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">folded</TD></TR><TR><TD ALIGN="CENTER">🔘</TD><TD ALIGN="LEFT">silent</TD></TR><TR><TD ALIGN="CENTER">🔡</TD><TD ALIGN="LEFT">init</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">bound</TD></TR><TR><TD ALIGN="CENTER">🔤</TD><TD ALIGN="LEFT">expected</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">run</TD></TR></TABLE>>]
    Scrollable [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📜 Scrollable ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">height</TD></TR></TABLE>>]
    Slides [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🎞️ Slides ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">current</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">next</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">prev</TD></TR><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">goto</TD></TR></TABLE>>]
    Tabs [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">📑 Tabs ➭ 🧩</TD></TR><HR/><TR><TD ALIGN="CENTER">🔢</TD><TD ALIGN="LEFT">active</TD></TR><HR/><TR><TD ALIGN="CENTER">▸</TD><TD ALIGN="LEFT">select</TD></TR></TABLE>>]
    Text [shape=plain, label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="white"><TR><TD COLSPAN="2" ALIGN="LEFT">🔤 Text ➭ 🧩</TD></TR></TABLE>>]
  }
  Datagrid -> Dataset [color=blue, fontcolor=blue, weight=8, labeldistance=2, headlabel="bind", fontsize=8]
  Chart -> Dataset [color=blue, fontcolor=blue, weight=8, labeldistance=2, headlabel="bind", fontsize=8]
  Chart -> Bar [color=blue, fontcolor=blue, weight=8, labeldistance=2, headlabel="⦙ bars", fontsize=8]
  Button -> Page [color=blue, fontcolor=blue, weight=8, labeldistance=2, headlabel="page", fontsize=8]
  Form -> Datagrid [color=blue, fontcolor=blue, weight=8, labeldistance=2, headlabel="bound", fontsize=8]
  subgraph cluster_states_Quiz {
    label="❓ states 🎛️"; fontsize=10;
    style="filled,rounded"; fillcolor="gray94"; color="gray85"; margin=12; nodesep=0.9;
    node [fontname="Source Sans Pro, sans-serif", shape=record, style="filled,rounded", fillcolor="white", color="gray", fontsize=10, penwidth=0.3]
    edge [style=solid, arrowhead=vee, penwidth=0.2, arrowsize=0.7, fontsize=8]
    st_Quiz_pending [label="➡️ pending"]
    st_Quiz_graded [label="graded"]
  }
  st_Quiz_pending -> st_Quiz_graded [xlabel="check", fontsize=8, color="gray45", fontcolor="gray45", minlen=2, constraint=false]
  st_Quiz_pending -> Quiz [style=dashed, arrowhead=none, color="gray70"]
  subgraph cluster_states_Recorder {
    label="🎥 states 🎛️"; fontsize=10;
    style="filled,rounded"; fillcolor="gray94"; color="gray85"; margin=12; nodesep=0.9;
    node [fontname="Source Sans Pro, sans-serif", shape=record, style="filled,rounded", fillcolor="white", color="gray", fontsize=10, penwidth=0.3]
    edge [style=solid, arrowhead=vee, penwidth=0.2, arrowsize=0.7, fontsize=8]
    st_Recorder_idle [label="➡️ idle"]
    st_Recorder_recording [label="recording"]
    st_Recorder_stopped [label="stopped"]
  }
  st_Recorder_idle -> st_Recorder_recording [xlabel="start", fontsize=8, color="gray45", fontcolor="gray45", minlen=2, constraint=false]
  st_Recorder_recording -> st_Recorder_stopped [xlabel="stop", fontsize=8, color="gray45", fontcolor="gray45", minlen=2, constraint=false]
  st_Recorder_idle -> Recorder [style=dashed, arrowhead=none, color="gray70"]
  subgraph cluster_legend {
    style=invis;
    __legend [shape=plain, fontcolor="#505050", label=<<TABLE BORDER="1" COLOR="lightgray" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1" BGCOLOR="gray98"><TR><TD ALIGN="CENTER">Legend</TD></TR><HR/><TR><TD ALIGN="LEFT">🔤 str or 🔡 long str</TD></TR><TR><TD ALIGN="LEFT">🔢 int or float</TD></TR><TR><TD ALIGN="LEFT">🔘 bool</TD></TR><TR><TD ALIGN="LEFT">🕗 datetime</TD></TR><TR><TD ALIGN="LEFT">🔒 password</TD></TR><TR><TD ALIGN="LEFT">🔤 ⦙ list of 🔤</TD></TR><TR><TD ALIGN="LEFT">◻️ Object from kore</TD></TR><TR><TD ALIGN="LEFT">📦 any</TD></TR><TR><TD ALIGN="LEFT">🐟 custom type Fish</TD></TR><TR><TD ALIGN="LEFT"> /  derived</TD></TR><TR><TD ALIGN="LEFT"> _  private</TD></TR><TR><TD ALIGN="LEFT"> =  default value</TD></TR><TR><TD ALIGN="LEFT">⤴️ reflexive reference</TD></TR><TR><TD ALIGN="LEFT">↩️ ⦙ reflexive collection</TD></TR><TR><TD ALIGN="LEFT"> ♢ composite or owned</TD></TR><HR/><TR><TD ALIGN="LEFT">⚡️ event or code</TD></TR><TR><TD ALIGN="LEFT"> ▸ method</TD></TR><TR><TD ALIGN="LEFT"> ▹ conditionnal method</TD></TR><TR><TD ALIGN="LEFT"> ▹ with transition ▹</TD></TR><HR/><TR><TD ALIGN="LEFT">🎛️ state machine</TD></TR><TR><TD ALIGN="LEFT">➡️ initial state</TD></TR><HR/><TR><TD ALIGN="LEFT"> ➭  inherits from</TD></TR><HR/><TR><TD ALIGN="LEFT">🛄 imported py</TD></TR></TABLE>>]
  }
}
```

Regenerate with `python tools/gen_component_diagram.py`.
