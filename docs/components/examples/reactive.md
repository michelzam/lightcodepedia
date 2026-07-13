# 🧮 Reactive cells

A knob is a spreadsheet cell: it holds a literal — or a `= formula`, a Python
*expression* evaluated live and re-run whenever its inputs change. There's
**nothing new to declare** — just `{= … }` in prose and `visible="= …"` on any
block. Formulas read your editable **form** fields by name and run in the
page's own Python runtime, so a cell is as simple as `{= price * qty }`.

## 📊 A cell is just an expression {#sheet}

An editable form is a grid of cells — click a value and type:

```yaml
price: 20
qty: 3
```
{: .form #inputs editable="true" title="Inputs" }

Now read them straight, no wiring — Subtotal **{= price * qty }** · with free
shipping over 50, **Total {= price * qty + (0 if price * qty >= 50 else 5) }**.

Change `price` or `qty` → every `{= … }` recomputes. No `if` in the markup, no
refresh — the cells track the form.

**Name the source when you like.** Each form is a scope keyed by its id, so the
explicit way to say the same subtotal is **{= inputs.price * inputs.qty }**. Bare
`price` is just sugar that works because no *other* form has a `price`; when two
forms would collide, the scope (`inputs.price` vs `shipping.price`) is how you
say which — flat when safe, scoped when needed. It's the same `id.field` you use
from Python (`Page().inputs.data.price`), one scope model for the whole page.

## 👁️ `visible` is just a cell {#visibility}

Point the same mechanism at a boolean and it decides whether a block shows.
Here the flag is one form field — flip it:

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

## 🧠 Name your formulas — a hidden `.run` model {#model}

Repeated logic belongs in one place, and there's **no special block for it** —
a plain, hidden `{: .run silent="true" }` runs on load into the page's runtime
and defines the model:

```python
def subtotal(): return price * qty
def shipping(): return 0 if subtotal() >= 50 else 5   # free over 50 — the "iif"
def total():    return subtotal() + shipping()
def loop():     return loop()                         # a deliberate cycle
```
{: .run silent="true" }

*(That block renders nothing — `silent="true"` means "run on load, show no UI".
It's the same `.run` you already know, used as the page's model.)*

Now the cells just call the model, and still react to the form above —
Subtotal **{= subtotal() }** · Shipping **{= shipping() }** · **Total {= total() }**.

## 🛡️ Why it can't turn into a language {#guardrails}

The formula grammar is **Python expressions only**, because a cell is `eval`'d,
never `exec`'d — and the interpreter enforces the line for free:

- a **comprehension is an expression**, so it's fine: **{= [x for x in range(3)] }** — but a `for:` / `if:` *statement* can't be typed into a cell at all (`eval` rejects it as a syntax error);
- a **cycle** fails **safe** — the recursive `loop()` yields **{= loop() }** as a value, not a frozen page.

So control flow and loops-with-side-effects stay where they belong — a `.run`
Python fence — and knobs stay declarative dataflow. Spreadsheet, not BASIC.

*Shipped form:* the same `= formula` in any real knob (`height="= base*2"`,
`visible="= intro.ready"`), reactive on the platform's `lc-model-changed` event,
with the linter topo-sorting cell dependencies to catch cycles at author time.
Model in a hidden `.run`, inputs in a `.form`, results in `{= … }` cells — three
things you already have, wired by dataflow.

## 🗂️ Structural state — one address everywhere {#state}

A value has one address, `node.component.field`, and it means the same thing in
a `{= }` cell, in Python, and in browser storage (the **Store** — localStorage,
per-browser). Design-time seeds (inline/file) are defaults; only what the learner
*sets* reaches the Store, so a nickname captured once personalizes every page.

**Try it live** — type a name, then **reload the page**: it sticks (this browser only).

```yaml
nickname: ""
```
{: .form #whoami persist="build_ai" editable="true" title="You" }

Hello **{= whoami.nickname or 'stranger' }** — nice to meet you 🐾

The acceptance feature below proves the *same* Store from Python — press ▶:

```gherkin
Feature: Structural state — one address in cells, Python and storage
  As an author
  I want node.component.field to resolve the same everywhere and persist per-browser
  So that a learner's answers personalize the whole credential with no server

  Scenario: An absolute path reads the same value on every surface
    Given a clean store
    :::python
    Store.reset()
    :::
    When the welcome node captures a nickname
    :::python
    Store.set("welcome.profile.nickname", "Rex")
    :::
    Then the Store, the injected name and Page() all agree
    :::python
    assert Store.get("welcome.profile.nickname") == "Rex"
    assert welcome.profile.nickname == "Rex"
    assert Page().welcome.profile.nickname == "Rex"
    :::

  Scenario: Seeds don't pollute the Store; only edits persist, and survive a reload
    Given a clean store
    :::python
    Store.reset()
    assert Store.get("build_ai.profile.nickname") == ""
    :::
    When the learner sets a value
    :::python
    Store.set("build_ai.profile.nickname", "Rex")
    :::
    Then it survives a runtime reload — browser-instance, localStorage
    :::python
    assert build_ai.profile.nickname == "Rex"
    self.page._reload_runtime()
    assert Store.get("build_ai.profile.nickname") == "Rex"
    :::

  Scenario: An unset field is empty, and a conditional reads the store
    Given a dog-builder profile
    :::python
    Store.reset()
    Store.set("build_ai.profile.building_for", "dogs")
    :::
    Then unset fields are blank and a visible= flag evaluates
    :::python
    assert build_ai.profile.nickname == ""
    assert eval_cell("build_ai.profile.building_for == 'dogs'") is True
    :::
```
{: .feature tags="state,learn" }

*(Next: the `.form persist="build_ai"` knob writes these edits for you, and
`{= welcome.profile.nickname }` reads them inline — the widget wiring on top of
this Store.)*
