# ✨ Pitch

The two-sentence product pitch, assembled from its blanks — one emoji
per section. Empty fields render as visible blanks: a pitch under
construction says so.

```yaml
who: shelter coordinators
need: must stop payments that come before a visit
product: Shelter Desk
category: adoption tracker
benefit: no family pays before meeting the dog
alternative: the paper binder
difference: enforces the order of the three steps
```
{: .pitch #demo_pitch persona="ana" }

The `persona` knob names the persona card this pitch serves, and does
two things. It **calculates the who**: the pitch takes it from the
persona (dotted, not bold — nobody typed it), so the two documents
cannot disagree about their audience, and a `who:` in the YAML is
ignored while the knob is set. And it powers a soft check on what IS
typed: when the `need` shares no words with the persona's goal, role or
frustrations, the pitch shows a drift warning. A finding, not an error.

```yaml
name: Ana
role: Shelter coordinator
goal: Every dog goes to a family that met it first
```
{: .persona #ana }

## Knobs

| knob | meaning |
|---|---|
| `#id` | the pitch's id — the impact map references it (default `pitch`) |
| `persona="id"` | the persona this pitch serves: chip, wire, **calculated who**, and a drift check on the need |
| `source="form_id"` | that form becomes the pitch's **editor** — the sentences follow every keystroke |
| `save="file.yaml"` | the learner's own pitch, kept in their bench (same contract as the persona's) |

## The form as editor

```yaml
who: shelter coordinators
need: know where families stop
product: Shelter Desk
category: adoption tracker
benefit: every stalled adoption is visible
alternative: guessing
difference: counts every step
```
{: .form #pitch_form editable="true" title="✏️ Edit — the pitch's source" }

```yaml
product: (waiting for the editor)
```
{: .pitch #live_pitch source="pitch_form" }

## A drifting pitch

The `need` below shares no words with #ana — the warning shows. (Its
`who:` is ignored: the knob calculates that one.)

```yaml
who: astronauts
need: fly to the moon
product: Rocket
category: spacecraft
benefit: gets there
alternative: walking
difference: thrust
```
{: .pitch #drifting persona="ana" }

## Proof

```gherkin
Feature: The pitch assembles and checks itself
  Scenario: The editor drives the sentences
    Given the wired pair
    :::python
    self.editor: Form = self.page.pitch_form
    self.view: Pitch = self.page.live_pitch
    :::
    When the author renames the product
    :::python
    self.editor.set("product", "MoonDesk")
    :::
    Then the sentence follows
    :::python
    assert "MoonDesk" in self.view.text
    :::

  Scenario: A pitch that forgets its persona is warned, not stopped
    Given the two pitches on this page
    :::python
    self.good: Pitch = self.page.demo_pitch
    self.bad: Pitch = self.page.drifting
    :::
    Then only the drifting one carries the warning
    :::python
    assert self.bad.drifting
    assert not self.good.drifting
    :::

  Scenario: The who is calculated, never typed
    Given a pitch that names a persona
    :::python
    self.p: Pitch = self.page.demo_pitch
    :::
    Then it reads the who off that card
    :::python
    assert self.p.data.who == "Shelter coordinator", self.p.data.who
    assert self.p.data.who_calculated
    :::
```
{: .feature #pitch_proof tags="spec" visible="true" status="passing" }
