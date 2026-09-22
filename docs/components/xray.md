# 🔬 X-ray

X-ray is the platform's inspection mode: switch it on from the ⚙️ pill (or hold
**⌥/Alt** while moving the pointer) and every part of a page reveals what it is.
Each block gets a ghost; the ⚙️ gear on a ghost opens the inline editor — one
dialog for a component's knobs and its content, reachable before any account.

## 📱 On a phone or tablet

Everything works by touch — ⚙️ pill → **🔬 X-ray**, then:

- **one finger** on a part — the lens: what this component is;
- **two fingers** — the **pipelines**: the wiring lights up (grid ← query ←
  dataset), the same view **Shift** gives on a computer.

A toast reminds you of both gestures every time you enter X-ray by touch.
Tap the pill again to leave.

## Keep, honestly

**💾 Keep changes** has two paths, decided by who you are:

- **Connected builder** — the content change is committed to the page's own
  source. The surgery is exact-match-or-abort: unless the original block is
  found exactly once, nothing is written and the ✏️ page editor is suggested
  instead. An inline edit can never corrupt a page.
- **Anonymous learner** — changes live only in this browser, and Keep invites
  you to create an account. Losing work is the incentive.

Knob changes are not committed inline yet — keep those via the ✏️ page editor.

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

Rules carry defaults you answer for, listed under the scores. Every run is
remembered per page on this device, together with the audit's own numbers,
and each card says what changed **since the previous version** of the file:
improvement is the point. Difficulty is not load — a hard target with nothing
around it scores green everywhere but coherence, where it must be validated.
No AI here; a semantic pass on prose is a later, key-gated step.
