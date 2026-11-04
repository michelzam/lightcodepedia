# 🔁 Retrospective

The sprint's look back, in four boxes: what the team **keeps**, what it
**improves**, what it **stops**, what it **starts**. One YAML fence, one
card — KISS. A box left empty stays on the card and says so: a retro is
read box by box.

```yaml
sprint: Sprint Zero — the Shelter
keep:
  - Asking Ana before writing a feature
improve:
  - Headlines in three words, not a sentence
stop:
  - Valuing a feature before its impact is written
start:
  - Asking Eve to compare the map before saving it
```
{: .retrospective #shelter_retro }

## Knobs

| knob | meaning |
|---|---|
| `#id` | the card's id — cells and proofs read it (default `retro`) |
| `source="form_id"` | that form becomes this card's **editor**: every keystroke re-renders the card |
| `save="retro.yaml"` | the two-repo contract (same as the persona's): the fence is the seed, the learner's 💾 keeps THEIR retro in their bench |
| `sprint` (field) | the sprint's name, on the card's head |
| `keep`, `improve`, `stop`, `start` (fields) | one line or a list each |

The card registers its data under its id, like the persona: a proof reads
`self.page.shelter_retro.data.keep`, a sentence `{= shelter_retro.start }`.

## The form as editor

Type in a box — the card follows.

```yaml
sprint: Sprint 1
keep: ""
improve: ""
stop: ""
start: ""
```
{: .form #retro_src editable="true" title="✏️ Edit — our retrospective" }

```yaml
sprint: (waiting for the editor)
```
{: .retrospective #my_retro source="retro_src" }

## Proof

```gherkin
Feature: The retrospective card shows its four boxes
  Scenario: The fence becomes a card
    Given the authored retro
    :::python
    self.card: Retrospective = self.page.shelter_retro
    :::
    Then it shows the sprint and every box
    :::python
    assert "Sprint Zero" in self.card.text
    for box in ("Keep", "Improve", "Stop", "Start"):
        assert box in self.card.text, f"no {box} box"
    assert self.card.data.start, "the start box reads empty"
    :::

  Scenario: The editor drives the view
    Given the wired pair
    :::python
    self.editor: Form = self.page.retro_src
    self.view: Retrospective = self.page.my_retro
    :::
    When the team types what to stop
    :::python
    self.editor.set("stop", "Merging without a green proof")
    :::
    Then the card follows
    :::python
    assert "Merging without a green proof" in self.view.text
    :::
```
{: .feature #retro_proof tags="spec" visible="true" status="passing" }
