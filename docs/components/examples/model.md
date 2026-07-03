---
title: "Live Models — declarative classes, auto-generated widgets"
---

# 🧬 Live Models — classes that build their own widget

Declare a Python class with **typed, constrained fields** and **state-gated
behaviours** — the platform renders the widget for you: sliders from `min/max`,
dropdowns from `enum`, locked fields from `ro`, state chips and gated buttons
from `@transition`. One declaration, many projections: widget, validation,
diagram, x-ray.

## 🐕 Meet Lucky — a model with a mood {#lucky_demo}

```python
@component(icon="🐕")
class Dog(Object):
    mood      = State("hungry", ["hungry", "fed"])
    colour    = Attr(str, "Golden", enum=["Golden", "Black", "Brown", "White"])
    weight_kg = Attr(float, 30, min=20, max=60, step=0.5, unit="kg", hint="Healthy range 20–60 kg")
    last_said = Attr(str, "…", ro=True, hint="Only bark() can change it")
    adopted   = Attr(bool, False, ro=True, hint="Locked — only a behaviour flips it")

    @transition(pre=["hungry"], post="fed")
    def eat(self):
        self.weight_kg += 1

    @transition(pre=["fed"])
    def bark(self):
        self.last_said = "Woof!"
        self.adopted = True

    def run(self):
        self.weight_kg -= 1
        if self.weight_kg < 30:
            self.mood = "hungry"


lucky = Dog()
```
{: .inspector #lucky_widget }

Try it: drag the **weight** slider past 60 (it clamps), pick a **colour**
(only the declared ones exist), and follow the machine — `bark()` stays locked
until `eat()` moves the mood to **fed**. The `adopted` checkbox can't be
clicked at all: *state is never set, it's reached*.

## 🍖 The same object, from anywhere {#shared_runtime}

The widget and page code share one Python runtime — this button calls the
**same** `lucky`, and the widget follows:

[🍖 Feed Lucky](#)
{: .button #feed_btn }

```python
def on_click(button):
    lucky.eat()
```
{: .onclick }

Click it twice: the second call raises `PreconditionError` — `eat()` needs
`hungry`, and Lucky is already `fed`. The gate is a property of the **model**,
not of any particular button.

## 🐾 Inheritance & references — a Pet with a bestie {#pet_demo}

Classes inherit fields, states and behaviours; a field typed with **another
Model class** becomes a **picklist of live instances** — subclasses included,
so a Dog's bestie can be a Fish:

```python
@component(icon="🐾")
class Pet(Object):
    mood   = State("bored", ["bored", "happy"])
    bestie = Attr("Pet", None, hint="Best friend — any Pet will do")

    @transition(pre=["bored"], post="happy")
    def play(self): pass

@component(icon="🐕")
class Dog(Pet):
    weight_kg = Attr(float, 30, min=20, max=60, unit="kg")

@component(icon="🐠")
class Fish(Pet):
    bubbles = Attr(int, 0, min=0, max=99)

rex   = Dog()
wanda = Fish()
```
{: .inspector #pet_widget }

Open **rex**'s `bestie` picklist: it offers `wanda` — a Fish *is a* Pet, so the
cross-species friendship type-checks. In code, `rex.bestie = wanda` works too,
while `rex.bestie = some_rock` raises `ValueError: bestie expects a Pet`. Note
`Attr("Pet")` — the class names *itself* as a string (it doesn't exist yet on
that line), the classic forward reference.

And the declarations draw their own picture — **Pet is an Object** (the ➭ ◻️
marker), Dog and Fish generalize to Pet, `bestie` loops back as a reflexive
association, and the mood statechart hangs below:

[class diagram](#)
{: .diagram scope="Pet" }

## ⚙️ How it works {#how_it_works}

| Declaration | The widget renders |
|---|---|
| `Attr(float, 30, min=20, max=60, step=0.5, unit="kg")` | a slider — values clamp to the range |
| `Attr(str, "Golden", enum=[…])` | a dropdown — other values raise `ValueError` |
| `Attr(bool, False)` | a checkbox |
| `Attr(str, "", secret=True)` | a password field |
| `ro=True` | a locked value 🔒 — outside writes raise; the object's **own behaviours** simply assign it |
| `hint="…"` | a tooltip on the row |
| `State("hungry", ["hungry", "fed"])` | the chips row — current state highlighted |
| `Attr("Pet")` | a **picklist** of live, type-compatible instances (subclasses count); wrong types raise |
| `@transition(pre=["hungry"], post="fed")` | a gated button — disabled outside `pre`, moves the state to `post` |
| `def run(self): …` | **every public method is a button** — no decorator needed; `_underscore` methods stay internal |

- **Everything is an Object** — your classes inherit `Object` directly, the
  same root every component descends from, so they join the
  [component model](/components/model) diagram: fields, guarded methods ▹ and
  the statechart, drawn automatically. The editor's 🗺️ Diagram tab reads them
  straight from the page source.
- **Validation lives in the model.** The widget, the REPL and buttons all go
  through the same setters — clamping, enum checks and preconditions apply
  everywhere, with teachable error messages.
- **No `@component`? Still works.** A plain `class Cat(Object)` self-registers
  on first use; the decorator just adds the icon.

## 🧪 Behavior checks {#behavior_checks}

The model's promises, verified live — press ▶ to run them in this very page's
Python runtime (the CD suite runs them on every deploy too):

```gherkin
Feature: Live models validate, gate and reference
  As a page author
  I want declared fields and transitions enforced everywhere
  So that widgets, buttons and code cannot break the model

  Scenario: Fields clamp, enums reject, read-only locks
    Given a fresh dog model
    :::python
    @component(icon="🐶")
    class FDog(Object):
        mood      = State("hungry", ["hungry", "fed"])
        colour    = Attr(str, "Golden", enum=["Golden", "Black"])
        weight_kg = Attr(float, 30, min=20, max=60)
        adopted   = Attr(bool, False, ro=True)

        @transition(pre=["hungry"], post="fed")
        def eat(dog):
            dog.weight_kg += 1

        @transition(pre=["fed"])
        def bark(dog):
            dog.adopted = True
    self.dog = FDog()
    assert self.dog.mood == "hungry" and self.dog.weight_kg == 30
    :::
    When I push the weight past its max
    :::python
    self.dog.weight_kg = 999
    :::
    Then it clamps to the declared range
    :::python
    assert self.dog.weight_kg == 60, self.dog.weight_kg
    :::
    Then a colour outside the enum is refused
    :::python
    try:
        self.dog.colour = "Pink"
        assert False, "enum should reject Pink"
    except ValueError as e:
        assert "one of" in str(e)
    :::
    Then adopted cannot be assigned directly
    :::python
    try:
        self.dog.adopted = True
        assert False, "ro should reject a direct write"
    except AttributeError as e:
        assert "behaviour" in str(e)
    :::

  Scenario: Behaviours gate on state and apply their post-state
    Given the dog is still hungry
    :::python
    assert self.dog.mood == "hungry"
    :::
    When it eats
    :::python
    self.dog.eat()
    :::
    Then it is fed — and refuses to eat again
    :::python
    assert self.dog.mood == "fed"
    try:
        self.dog.eat()
        assert False, "the gate should refuse a second meal"
    except PreconditionError as e:
        assert "needs hungry" in str(e)
    :::
    Then its own behaviour may write what outsiders cannot
    :::python
    self.dog.bark()
    assert self.dog.adopted is True
    :::

  Scenario: References type-check and survive a runtime refresh
    Given a pet family with a bestie reference
    :::python
    @component(icon="🐾")
    class FPet(Object):
        bestie = Attr("FPet", None)

    @component(icon="🐟")
    class FFish(FPet):
        pass
    self.rex = FPet()
    self.fish = FFish()
    :::
    When the runtime preamble re-runs, as any button click makes it do
    :::python
    self.page._reload_runtime()
    :::
    Then a subclass instance is still accepted as bestie
    :::python
    self.rex.bestie = self.fish
    assert self.rex.bestie is self.fish
    :::
    Then a non-pet is still refused
    :::python
    class FRock(Object):
        pass
    try:
        self.rex.bestie = FRock()
        assert False, "a rock is no bestie"
    except ValueError as e:
        assert "expects a FPet" in str(e)
    :::
```
{: .feature tags="model,learn" }

**Q:** `lucky.adopted = True` raises an error, yet after `bark()` the box is
ticked. Why?

- [ ] `adopted` is broken — a bug in the widget.

  > No — the model rejected a *direct* write. That's `ro=True` doing its job.

- [x] `adopted` is read-only state: only a **behaviour** may change it.

  > Exactly — inside `bark()` the object assigns its own field; from outside,
  > the same assignment raises. Outcomes are *reached* through the object's
  > own methods, never imposed from outside.

- [ ] Booleans can't be assigned in Python.

  > They can — but this one is declared `ro=True`, so the model refuses.
{: .quiz #ro_quiz }
