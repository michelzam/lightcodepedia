# 🎏 Event flow

A page's story as an event-storming sequence: colored sticky notes, read
left to right. The key of each line is the color; the value is the words.

```yaml
- actor: The family
- command: Name a dog
- event: A dog is named
- policy: The meet card opens when a dog is named
- command: Book the visit
- event: A visit is on the calendar
- reader: The coordinator sees how far they got
```
{: .event_flow #demo_flow legend="true" }

## The grammar

Six kinds, each with the sticky-note color the technique made standard:

| kind | color | meaning |
|---|---|---|
| `actor` | 🟨 yellow | a person |
| `command` | 🟦 blue | what they do |
| `event` | 🟧 orange | what became true because of it |
| `policy` | 🟪 purple | the rule that reacts to an event |
| `reader` | 🟩 green | what the screen shows next |
| `external` | 🩷 pink | a system outside the page |

An unknown kind renders grey rather than failing — a draft is allowed to
be a draft.

## Knobs

| knob | meaning |
|---|---|
| `#id` | the flow's id (default `event_flow`) |
| `legend="true"` | show the color legend under the sequence |

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
    Then all seven notes are there, in grammar order
    :::python
    assert self.flow.count == 7, self.flow.count
    kinds = self.flow.kinds()
    assert kinds[0] == "actor"
    assert kinds.index("event") > kinds.index("command"), \
        "an event follows the command that caused it"
    assert kinds.index("policy") > kinds.index("event"), \
        "a policy reacts to an event"
    :::
```
{: .feature #event_flow_proof tags="event_flow" visible="true" status="passing" }
