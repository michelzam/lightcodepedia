# ✍️ Pad

The pad is where a learner **builds**: Markdown on one side, the living
page on the other, updated as they type. Seed it with a fence; what they
write is theirs. Markdown itself — headings, lists, tables, footnotes —
is on the [✍️ Text](text) page, with its own playground.

## 👀 See it in action

````markdown
## 🐾 My first page

A **sentence** with *style*, and a list:

- one thing
- another

```csv
name,age
Rex,3
Luna,5
```
{: .dataset #pets }

[the pets](#)
{: .datagrid source="pets" }
````
{: .mdpad #pad_demo rows="14" decorations="true" }

Change a name, add a row to the list: the grid follows. With
`decorations="true"` the preview is the site's own pipeline — a dataset,
a grid, a chart, a class come alive as they would on a published page.

```gherkin
Feature: The pad renders what is typed
  As a learner
  I want to see my page as I write it
  So that syntax is never the blocker

  Scenario: The seed renders, and a component in it is alive
    Given the pad above
    :::python
    self.pad: Mdpad = self.page.pad_demo
    :::
    When I read its preview
    :::python
    self.rows: int = self.page.pets.count
    :::
    Then the dataset in it has its rows
    :::python
    assert self.rows == 2, f"{self.rows} rows, the seed holds 2"
    :::
```
{: .feature #pad_proof visible="true" status="pending" tags="pad" }

## 🧰 What a pad does

- **Yours, in your bench.** `save="cv.md"` makes the fence the author's
  seed and the learner's copy a file in their own repo: 💾 commits it, ↺
  restores the seed, and the author republishes the lesson forever without
  touching anyone's work. `save="/my/…"` for files that outlive one lesson.
- **A diary of versions.** `comment="true"` asks one line at 💾 — *what
  did you just do?* — and 🕘 Versions lists them; any row shows that
  version, read-only.
- **Time travel.** 🎞 Replay plays the saved versions forward (▶) and
  backward (◀ Moonwalk): added lines unfold, removed ones fold, the
  changed component pulses in the preview, and the version's own words
  float as a caption. `replay="1.5"` sets the pace.
- **The source, painted.** A fence and its body muted, a decoration on
  its own band — class, `#id` and knobs in their colours — line numbers
  and a component icon in the gutter (`numbers="true"`), blocks banded
  like a piano (`piano="true"`).
- **Errors in the gutter.** A fence that never closes, a decoration
  without its `}`, a Python fence that does not compile: ⚠ on the line, one
  sentence under the pad.
- **Type hints, checked.** `mypy="true"` lets Dr. mypy (lite) read every
  Python fence too — a `def` without its hints, a `return` or a literal
  argument against them — ⚠ on the line in mypy's own words, as the
  [🐍 runner](run)'s 🩺 Dr. mypy says them. `"loose"` forgives a missing
  hint and checks only the ones written.

````markdown
## 🐶 A typed pet

```python
class Pet:
    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}!"
```
````
{: .mdpad #typed_pad mypy="true" numbers="true" rows="10" }

  `greet` gives back a `str` and does not say so: line 8 wears the ⚠.
  Type `-> str` before its colon and the ⚠ goes.
- **Examples, run as you write.** `doctest="true"`: every Python fence
  runs its own `>>>` examples — no `if __name__ == "__main__":`, no
  `doctest.testmod()` — and a failing one wears ⚠ on its `>>>` line:
  *got 0, expected 2*. A fence runs again only when its own text changes.

````markdown
## 🦘 jump

```python
def jump(start: int, leap: int) -> int:
    """
    Makes an absolute jump from start.

    >>> jump(2, 3)
    5
    >>> jump(1, -1)
    2
    """
    return start + leap
```
````
{: .mdpad #doctest_pad doctest="true" mypy="true" numbers="true" rows="14" }

  Line 10 wears the ⚠: `jump(1, -1)` gives `0`. Fix the example (or the
  code) and the gutter clears.
- **Keys and the phone.** ⌘↑/↓ jumps between blocks, ⌥ moves one, ⇥ folds
  the editor away so the preview takes the whole width (✎ brings it back);
  `folded="true"` opens that way. `?` on the pad lists the keys of this
  computer.
- **Invisible parts, shown.** A dataset or a class has no face; with the
  caret in it, a ghost line in the preview says where it sits.
- **Wires that break are drawn broken.** A `source=` or `master=` to an id
  the page no longer has: dashed frame, one chip, and the pad says so.
- **A builder beside it.** An [`.agent`](agent) bound to a pad proposes
  the lines a red proof needs; ⬇ Add puts them in, ▶ runs again.

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `rows="N"` | `12` | editor height in text rows |
| `save="cv.md"` | — | the learner's copy, beside the lesson in their bench; `/my/…` at the bench root |
| `save="here:site.md"` | — | the file on the host that served this page: 💾 writes it there when the host takes saves (`--edit`), the old copy stamped in `__backup/`; 🕘 Versions lists those copies. On a read-only host no 💾 is offered — the bar says “read-only” — and the gear offers nothing on the page |
| `comment="true"` | off | 💾 Save… asks for one line, the version's name |
| `replay="1.5"` | `1.5` | seconds per frame in 🎞 Replay |
| `decorations="true"` | off | the preview runs the site's pipeline: components come alive |
| `piano="true"` | off | blocks banded in two shades, the caret's in a third |
| `numbers="true"` | off | line numbers and component icons in a gutter |
| `doctest="true"` | off | each Python fence runs its own `>>>` examples as you write; a failing one is marked ⚠ on its line |
| `mypy="true"` | off | Dr. mypy (lite) reads the Python fences: missing hints and wrong types, ⚠ on the line (`"loose"`: written hints only) |
| `folded="true"` | off | opens with the editor folded away |
| `layout="below"` | `beside`, side by side | preview above the source |
| `layout="behind"` | `beside`, side by side | one face at a time: the result in front, ✎ brings the source |

## 🔗 Related components & examples

```
/components/text
/components/agent
/components/dataset
```
{: .related }
