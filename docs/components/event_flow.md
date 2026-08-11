# 🎏 Event flow

A page's story as an event-storming sequence. The key of each line is
the note's color; the value is the words. Each person heads their own
beats, and a beat begins with the command that person gives.

```yaml
- user: The family
- ui: dog_grid — the list of dogs
- command: Name a dog
- event: A dog is named
- ui: meet — the second card
- rule: Opens only once a dog is named
- command: Pick an afternoon
- event: A visit is on the calendar
- user: The coordinator
- ui: week — this week's reservations
- command: Count who is still waiting
```
{: .event_flow #demo_flow legend="true" }

## The grammar

Seven kinds, each with the sticky-note color the technique made standard
— named in plain words, not in jargon:

| kind | note | meaning | event storming calls it |
|---|---|---|---|
| `user` | 👤 🍦 cream | a person | actor |
| `ui` | 🖥️ 🟩 green | the screen they act on | read model |
| `data` | 📦 🟨 yellow | what the beat is about | aggregate |
| `command` | 🗣️ 🟦 blue | what they ask for | command |
| `rule` | 📏 🟪 purple | what governs it | policy |
| `event` | ⚡ 🟧 orange | what became true because of it | domain event |
| `external` | 🌐 🩷 pink | a system outside the page | external system |

Every name in the last column parses too (plus `view`, `reader`,
`screen`, `entity`), so a page written in either vocabulary renders.

The glyph comes from the kind — an author writes the sentence and never
types the icon. It is there because a colour alone is not the grammar:
printed in grey, or read aloud, 🟦 and 🟪 are the same note.

An unknown kind renders grey rather than failing — a draft is allowed to
be a draft.

## The beat

One line is one beat, and every beat has the same shape:

    🖥️ ui | 📦 data → 🗣️ command → [📏 rule →] ⚡ event

A beat **opens** on the `ui` — where the person sits to decide, named
after the component it is (`ask`, `dog_grid`, `week`) — and **closes**
on its `event`. A rule never makes a person act; it only governs what
they asked for. Beats of one person share a grid, so commands line up
under commands. A user with a single beat is written on one line, not
two.

## The workshop wall

The default is the flow above: marked words, read as a sentence.
`notes="sticky"` brings back the cardboard of a real event-storming
wall, for a page that wants the workshop rather than the sentence:

```yaml
- user: The coordinator
- ui: The follow-up list
- command: Call the next family
- event: The call is recorded
```
{: .event_flow #sticky_flow notes="sticky" }

## Knobs

| knob | meaning |
|---|---|
| `#id` | the flow's id (default `event_flow`) |
| `legend="true"` | show the color legend under the sequence |
| `notes="sticky"` | the workshop wall — cardboard notes instead of the default marked words |

The flow registers its steps under its id, so `{= demo_flow.count }`
counts them and a proof reads the sequence. The YAML is authored today;
the shape is chosen so a later version can *generate* the sequence from
the page's own wiring — gates are policies, button handlers are
commands.

## Proof

```gherkin
Feature: The flow tells the story in color
  Scenario: Every step renders in its kind's color
    Given the demo flow
    :::python
    self.flow = self.page.demo_flow
    :::
    Then every note is there, in the beat's order
    :::python
    assert self.flow.count == 11, self.flow.count
    kinds: list[str] = self.flow.kinds()
    assert kinds[0] == "user", "a story starts with a person"
    assert kinds.index("ui") < kinds.index("command"), \
        "a beat opens on the screen the person acts on"
    assert kinds.index("event") > kinds.index("command"), \
        "an event follows the command that asked for it"
    assert kinds.index("rule") > kinds.index("ui"), \
        "a rule governs what a person asked for, it never issues it"
    :::
```
{: .feature #event_flow_proof tags="event_flow" visible="true" status="passing" }
