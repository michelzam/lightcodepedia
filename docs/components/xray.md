# 🔬 X-ray

X-ray is the platform's inspection mode: switch it on from the ⚙️ pill (or hold
**⌥/Alt** while moving the pointer) and every part of a page reveals what it is.
Each block gets a ghost; the ⚙️ gear on a ghost opens the inline editor — one
dialog for a component's knobs and its content, reachable before any account.

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
    self.gears = Object._all("#lcx-gear")
    self.dialogs = Object._all("#lcx-edit")
    self.keeps = Object._all("#lcx-keep")
    :::
    When the engine has loaded
    Then the ghost gear, the dialog and its Keep button exist exactly once
    :::python
    assert len(self.gears) == 1, len(self.gears)
    assert len(self.dialogs) == 1, len(self.dialogs)
    assert len(self.keeps) == 1, len(self.keeps)
    :::
```
{: .feature visible="true" #xray_keep_feature tags="ui" status="passing" }

The commit path itself is proven by the UX suite (`tests/features/xray.feature`):
a stubbed repository receives the block's new content — exactly once, or not at all.
