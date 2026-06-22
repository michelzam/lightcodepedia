# 📻 Radio

Got a few options and want the reader to **pick exactly one** before diving in? **Radio is your instrument!** 📻 A row of buttons, one panel at a time — the same content as [📑 Tabs](/components/tabs), but with a "choose one" feel.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
### 🐍 Python
Python is readable, beginner-friendly, and runs in your browser on this site. Great first language.
- Easy to read
- Huge ecosystem
- Works everywhere

### 🦀 Rust
Rust is fast, safe, and beloved by systems programmers. Steeper curve, big payoff.
- Memory-safe without GC
- Blazingly fast
- Loved on Stack Overflow every year since 2016

### 🐹 Go
Go is simple, fast, and built for networked services. Minimal syntax, fast compilation.
- Built-in concurrency
- Fast compile times
- Single binary output
```
{: .radio }

```gherkin
Feature: Radio shows one panel, chosen by a button
  As a reader
  I want to pick which panel I see with a radio button
  So that I compare options one at a time

  Scenario: Picking an option makes it the selected one
    Given the radio above
    :::python
    self.radio = Radio._all(".lc-radio-group")[0]
    self.radio.select(0)
    :::
    When I pick the second option
    :::python
    self.radio.select(1)
    :::
    Then the second option is selected
    :::python
    assert self.radio.active == 1
    :::

  Scenario: Only one option is selected at a time
    Given the radio above with the third option picked
    :::python
    self.radio = Radio._all(".lc-radio-group")[0]
    self.radio.select(2)
    :::
    When I pick the first option
    :::python
    self.radio.select(0)
    :::
    Then the first option is selected
    :::python
    assert self.radio.active == 0
    :::
```
{: .feature tags="ui" }

Click each radio button. The panel swaps instantly.

> Ask yourself: "When would you choose radio over tabs?"
> Good answer: when the options feel like a **choice** (pick one) rather than **categories** (browse any).
{: .speaker-note }

**Q:** How many panels are visible at one time in a radio widget?

- [x] Exactly one — radio buttons are mutually exclusive by design.
- [ ] All of them — radio just adds a selector bar at the top.
- [ ] Up to two — current and previously selected.
- [ ] Zero, until the user clicks something.
{: .quiz }

## 🛠️ How to make one

Same format as [🪗 Accordion](/components/accordion) and [📑 Tabs](/components/tabs) — a plain fenced block with `### ` sections:

````markdown
```
### Option A
Content for A.

### Option B
Content for B.
```
{: .radio }
````

The first section is selected and visible by default.

## 🆚 Tabs vs Radio — when to use which

| | [📑 Tabs](/components/tabs) | 📻 Radio |
|---|---|---|
| Navigation feel | Browse categories | Pick one option |
| Visual | Tab bar | Radio group |
| Best for | Documentation sections | Compare alternatives |

## 🏁 Final exam

**Q:** You have three language options — Python, Rust, Go — and want the learner to consciously **choose** one before reading. Tabs or Radio?

- [ ] Tabs — they're more visual and prominent.
- [x] Radio — the buttons signal "pick one" more clearly than tabs do.
- [ ] Accordion — all three visible means less deciding.
- [ ] Dropdown — maximum suspense.
{: .quiz }
