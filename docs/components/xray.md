# 🔬 X-ray

X-ray is the platform's inspection mode: switch it on from the ⚙️ pill (or hold
**⌥/Alt** while moving the pointer) and every part of a page reveals what it is.
Each block gets a ghost; the ⚙️ gear on a ghost opens the inline editor — one
dialog for a component's knobs and its content, reachable before any account.

## 📌 It stays for the screenshot

On a computer, letting go of ⌥ no longer puts the reveal away: the lens or
the pipes stay **pinned** until you click or tap anywhere, press **Esc**, or
sweep again with ⌥. A screenshot chord is keys, not a click, so the pipes
hold still for it.

## 📱 On a phone or tablet

Everything works by touch — ⚙️ pill → **🔬 X-ray**, then:

- **one finger** on a part — the lens: what this component is;
- **two fingers** — the **pipelines**: the wiring lights up (grid ← query ←
  dataset), the same view **Shift** gives on a computer.

A toast reminds you of both gestures every time you enter X-ray by touch.
Tap the pill again to leave.

## 🧮 Names are wires too

A part can name another without any knob. Each one gets its own pipe:

- a **cell** `{= order.price * 2 }` *reads* every part its formula names: a
  form, a pad, a check, a dataset or a query;
- an **avatar** *points* at every part its scripts walk to (`at:`), such as
  the app it shows or the check it runs.

The pipes show from either end. Shift on the app shows the avatar and the
cells that lean on it.

## 🎬 Scripted: the loupe, then the pipes

A guide can show the x-ray the way a hand would, in two beats. `do: xray,
with: lens` is the **loupe**: the ghost of one part under the ring, no pipes.
`do: xray, with: 6` is the **pipes**: the part's wiring, back to reading
after six seconds. While the guide performs, its own pointers stay out of
the scene — otherwise every `at:` of its script would come along.

```yaml
- { city: Porto,  sales: 12 }
- { city: Lisbon, sales: 9 }
```
{: .dataset #xray_sales format="yaml" }

[Sales](#)
{: .datagrid source="xray_sales" #xray_sales_grid height="120" }

[▶ Doc, the loupe, then the pipes](#)
{: .avatar_trigger target="xray_doc" }

```yaml
bot: doc
script:
  - { at: xray_sales_grid, do: xray, with: lens, say: "The loupe: one part, what it is. No wires yet." }
  - { at: xray_sales_grid, do: xray, with: 6, say: "Now its pipes: the grid reads the sales. Six seconds, then back to reading." }
```
{: .avatar #xray_doc dock="true" size="100" }

```gherkin
Feature: The loupe, then the pipes
  As a guide showing a page's insides
  I want the x-ray in two beats, one part alone and then its wiring
  So that a learner sees what a thing is before seeing what feeds it

  Scenario: The lens draws one ghost and no pipes
    Given the sales grid above
    :::python
    import js
    self.grid: Datagrid = self.page.xray_sales_grid
    :::
    When the guide asks for the loupe on it
    :::python
    assert js.window.lcVerbs.act("xray", self.grid._el, "lens", None), "the xray verb refused the lens"
    :::
    Then one ghost shows, and the pipes do not
    :::python
    scene = js.document.getElementById("lcx-scene")
    assert scene is not None and scene.style.display != "none", "no scene for the lens"
    svg = scene.querySelector(".lcx-svg")
    assert svg is not None and svg.style.display == "none", "the lens drew pipes"
    js.window.lcMode.set("read")
    :::
```
{: .feature visible="true" #xray_lens_feature tags="ui" status="pending" }

## Keep, honestly

**💾 Keep changes** has two paths, decided by who you are:

- **Connected builder** — the content change is committed to the page's own
  source. The surgery is exact-match-or-abort: unless the original block is
  found exactly once, nothing is written and the ✏️ page editor is suggested
  instead. An inline edit can never corrupt a page.
- **Anonymous learner** — changes live only in this browser, and Keep invites
  you to create an account. Losing work is the incentive.

Knob changes are not committed inline yet — keep those via the ✏️ page editor.

- **Inside a bench slot** (`{: .embed save="…" }`), the frame's own gear and
  the gear on any plain line inside it edit the learner's **whole file**, as
  it is now, and 💾 Save writes it back whole: no anchor to find, so a file
  that already left the lesson's starter, or a cell name typed by mistake,
  can always be edited again. A component inside the slot (a grid, a chart)
  keeps its own fence and its own exact-match save.

```gherkin
Feature: X-ray inline editing keeps changes honestly
  As a connected builder
  I want Keep to commit my inline edits to the page's own source
  So that nothing I keep is lost — and learners get invited instead

  Scenario: The editing machinery is wired on this very page
    Given the x-ray chrome of the page I am reading
    :::python
    self.gears: list = Object._all("#lcx-gear")
    self.dialogs: list = Object._all("#lcx-edit")
    self.keeps: list = Object._all("#lcx-keep")
    :::
    When the engine has loaded
    Then the ghost gear, the dialog and its Keep button exist exactly once
    :::python
    assert len(self.gears) == 1, len(self.gears)
    assert len(self.dialogs) == 1, len(self.dialogs)
    assert len(self.keeps) == 1, len(self.keeps)
    :::
```
{: .feature visible="true" #xray_keep_feature tags="ui,lifecycle" status="passing" }

The commit path itself is proven by the UX suite (`tests/features/xray.feature`):
a stubbed repository receives the block's new content — exactly once, or not at all.

## 🧠 Cognitive load check — the ♿ Audit tab's second button

Beside **♿ Audit this page**, **🧠 Check load** reads the page as rendered
and scores four things, deterministically, each expanding into its factors
with one row per component (click a row: the part is outlined):

- **🎯 coherence** — validations on the page (quizzes and proofs), proofs
  tagged with a skill, a prerequisite declared. A page that cannot tell what
  was learned scores here.
- **🧩 load** — per section, one reel screen: distinct component kinds shown
  at once, and the largest cluster of blocks bound together (bindings,
  masters, cells) that must be understood as one. Element interactivity,
  not a count of words.
- **⚙️ friction** — interactive parts (forms, agents, runners, grids) that no
  validation and no binding ever reads: work with no path to a target.
- **🎬 seduction** — media nothing points at: engaging, target-less.

Rules carry defaults you answer for, listed under the scores. Every run,
with the audit's own numbers, is written **beside the page** in
`__<page>_audit.yaml`, one row per version, committed with your key — a
dunder file, never published, never rendered. The grid under the scores
reads it back: header tooltips say what each column means, the version
names its commit on hover, and each number turns green when it improved
or red when it regressed against the run before. Improvement is the point. Difficulty is not load — a hard target with nothing
around it scores green everywhere but coherence, where it must be validated.
No AI here; a semantic pass on prose is a later, key-gated step.
