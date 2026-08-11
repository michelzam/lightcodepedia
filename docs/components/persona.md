# 👤 Persona

An empathy-map card for the person your product serves. One YAML fence,
one card: identity, goal, frustrations, a real quote, and the four
empathy sections. All fields optional — the card renders what you give it.

```yaml
name: Maria
role: Shelter coordinator
photo: ""
goal: Every dog goes to a family that met it first
frustrations:
  - Families pay before they visit
  - Nobody knows where applicants stop
quote: We are driving to their house this afternoon to explain.
says:
  - Did they meet the dog?
thinks:
  - The app got lucky once
does:
  - Checks the week's numbers every Tuesday
feels:
  - Responsible for every adoption
```
{: .persona #maria }

## Knobs

| knob | meaning |
|---|---|
| `#id` | the card's id — other components reference it (default `persona`) |
| `source="form_id"` | that form becomes this card's **editor**: every keystroke re-renders the card, and the x-ray pipes the wire |
| `save="file.yaml"` | the two-repo contract (same as the datagrid's): the fence is the seed, the learner's 💾 keeps THEIR card in their bench and it wins on the next visit — from any page naming the same file |
| `photo` (field) | image URL for the portrait slot; empty shows a placeholder |

The card registers its data under its id, so cells, agents, proofs and
the x-ray see it like any dataset. The photo slot is deliberately a plain
URL — an AI-generated portrait based on the empathy map plugs in later
without a new knob.

## The form as editor

Edit a field below — the card follows, live. Sweep the x-ray with ⇧ to
see the pipe.

```yaml
name: Sam
role: Volunteer
goal: Answer families without guessing
```
{: .form #sam_src editable="true" title="✏️ Edit — the persona's source" }

With `save=` alongside, the card also offers 💾 — read/write, because
there is something to type in.

```yaml
role: (waiting for the editor)
```
{: .persona #sam source="sam_src" save="persona_demo.yaml" }

## Read-only: the recap card

`save=` **with** `source=` is read/write — the editor types, 💾 keeps.
`save=` **alone** is a read-only view of what the learner saved
elsewhere: no editor, so no save button, and a note saying where the
document gets built.

```yaml
role: Shelter coordinator
```
{: .persona #recap save="never_saved_demo.yaml" }

## Proof

```gherkin
Feature: The persona card renders its person
  Scenario: The fence becomes a card
    Given the authored card
    :::python
    self.card: Persona = self.page.maria
    :::
    Then it shows her name and her goal
    :::python
    assert "Maria" in self.card.text
    assert "met it first" in self.card.text
    :::

  Scenario: The editor drives the view
    Given the wired pair
    :::python
    self.editor: Form = self.page.sam_src
    self.view: Persona = self.page.sam
    :::
    When the author renames the persona
    :::python
    self.editor.set("name", "Samantha")
    :::
    Then the card follows
    :::python
    assert "Samantha" in self.view.text
    :::
```
{: .feature #persona_proof tags="persona" visible="true" status="passing" }
