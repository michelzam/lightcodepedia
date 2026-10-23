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
| `save="here:site.md"` | — | the file on the host that served this page: 💾 writes it there when the host takes saves, the old copy stamped in `__backup/`; 🕘 Versions lists those copies |
| `comment="true"` | off | 💾 Save… asks for one line, the version's name |
| `replay="1.5"` | `1.5` | seconds per frame in 🎞 Replay |
| `decorations="true"` | off | the preview runs the site's pipeline: components come alive |
| `piano="true"` | off | blocks banded in two shades, the caret's in a third |
| `numbers="true"` | off | line numbers and component icons in a gutter |
| `folded="true"` | off | opens with the editor folded away |
| `layout="rows"` | side by side | preview above the source |

## 🔗 Related components & examples

```
/components/text
/components/agent
/components/dataset
```
{: .related }
