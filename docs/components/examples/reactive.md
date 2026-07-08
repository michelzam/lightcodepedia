---
title: "Reactive cells — formulas in any knob"
---

# 🧮 Reactive cells

The idea we designed, built as a real component: **a knob is a spreadsheet
cell.** It holds a literal — or a `= formula`, a Python *expression* evaluated
live and re-run whenever its inputs change. `visible=` is just another cell.
Everything on this page is plain markdown: a Python model, editable forms, and
`{= … }` cells. No HTML, no script, no engine to wire — `{: .cells }` does it.

## 📊 It's literally a spreadsheet {#sheet}

The model — plain Python. `{: .cells }` runs it once into the page's own cell
namespace; the derived cells below read it:

```python
price = 20
qty   = 3
def subtotal(): return price * qty
def shipping(): return 0 if subtotal() >= 50 else 5   # free over 50 — the "iif"
def total():    return subtotal() + shipping()
def loop():     return loop()                         # a deliberate cycle
```
{: .cells }

The inputs are spreadsheet cells too — an editable form. Click a value and type:

```yaml
price: 20
qty: 3
```
{: .form #inputs editable="true" title="Inputs" }

Subtotal **{= subtotal() }** · Shipping **{= shipping() }** · **Total {= total() }**

Change `price` or `qty` → every `{= … }` recomputes. No `if`, no refresh — the
cells track the model, and free shipping kicks in the moment `subtotal` reaches
50.

## 👁️ `visible` is just a cell {#visibility}

Same mechanism, pointed at a boolean — the cumulative learner-flag case. The
flag is one plain variable:

```python
mixed_up = False   # a learner's misconception — the form below flips it
```
{: .cells }

Toggle it:

```yaml
mixed_up: false
```
{: .form #flag editable="true" title="Learner flag" }

You picked *attribute* — quick recap: **attributes store state, methods *do*
things.** `wanda.blow_bubble()` runs behaviour.
{: visible="= mixed_up" }

Nice — you've got it. `blow_bubble()` is behaviour Wanda performs. 🎉
{: visible="= not mixed_up" }

No `.adaptive`, no container, no branch in the markup — each block is a cell
whose formula reads the same flag. (Cumulative in the real thing: independent
flags, so several blocks can show at once.)

## 🛡️ Why it can't turn into a language {#guardrails}

The formula grammar is **Python expressions only**, because a cell is `eval`'d,
never `exec`'d — and the interpreter enforces the line for free:

- a **comprehension is an expression**, so it's fine: **{= [x for x in range(3)] }** — but a `for:` / `if:` *statement* can't be typed into a cell at all (`eval` rejects it as a syntax error);
- a **cycle** fails **safe** — the recursive `loop()` yields **{= loop() }** as a value, not a frozen page.

So control flow and loops-with-side-effects stay where they belong — a `.run`
Python fence — and knobs stay declarative dataflow. Spreadsheet, not BASIC.

*Shipped form:* the same `= formula` in any real knob (`height="= base*2"`,
`visible="= intro.ready"`), reactive on the platform's `lc-model-changed` event.
Formulas can't reach the platform runtime (an isolated namespace), and the
linter topo-sorts cell dependencies to catch cycles at author time. This page is
the proof that the core evaluates, reacts, isolates, and fails safe — with
nothing but markdown.
