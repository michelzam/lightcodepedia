# 🧩 Diagram

Render a **live** Graphviz class diagram of the component model — built in the
browser from the wrapper classes themselves. There is no static image and no
build step: each class declares its knobs/behaviours via `@component(...)` and
dumps its own node through an inherited `to_dot()` (the single source of truth in
`steps_runtime.md`). The same code produces the committed [Component Model](model)
page at build time.

Attach `{: .diagram }` to a link. Add `scope="ClassName"` to focus on one class
plus its ancestors, association targets and subclasses. No scope → the whole
model.

## 🌍 Whole model

[Component model](#)
{: .diagram }

## 🔬 Scoped to one class

`scope="Chart"` shows `Chart` with everything it touches — its `Block`/`Object`
ancestry (merged UML inheritance) and its `Dataset` / `Bar` associations.

[Chart neighbourhood](#)
{: .diagram scope="Chart" }

## 🎛️ State machines

Components can declare a `states` list and mark methods with `@transition(pre, post)`.
The diagram then draws the state machine — initial state ➡️, transitions labelled
by the method, and `▹ guarded ▹` markers on the methods. `Recorder` goes
`idle → recording → stopped`:

[Recorder state machine](#)
{: .diagram scope="Recorder" }

## 📖 How to read it

- **◻️ / 🧩 icons** label each class; the panels list typed **knobs** (attributes)
  and **behaviours** (methods).
- **`➭ ◻️` / `➭ 🧩` markers** = inheritance from a root base (`Object` / `Block`),
  shown in the title instead of an edge to avoid a heavy fan of obvious lines.
- **Blue arrows** = associations, pointing up to the referenced class, labelled
  at the head (e.g. `bind`, `⦙ bars`).
- **Underscores read as spaces** (`has_class` → `has class`).
- Icons follow the same legend as
  `usecases/module_manager/backend/module_decorator.py` (shown in the diagram).

## 🔬 X-ray lens

Hold **⌥ Option / Alt** and sweep the round lens over **any rendered widget on
any page**: through the disc the widget is stripped to its **inner inspector** —
the component class with the **live value** of every attribute (inherited ones
too, like `id`) and the **current state** in bold. Add **⇧ Shift** to also draw
connectors to the widget's associated objects — a real arrow to a visible target
(e.g. `Form → Datagrid`), or a ghost chip for a hidden one (e.g. a `Dataset`).
Release the key to dismiss.

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `scope="…"` | (whole model) | A **class** name (class + neighbours), a **package** (`ui` / `kore`), or `*` for the whole model |
| `states="…"` | `true` | Set `false`/`off` to hide the state-machine clusters |
