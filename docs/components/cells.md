# 🔢 Cells

Reactive spreadsheet cells in prose: `{= expr }` anywhere in a paragraph is
replaced by the value of the Python *expression*, and recomputes whenever the
page's data changes (form edits, model runs, store writes).🧪

## Syntax

```markdown
The total is {= price * quantity } €.
```

Any knob can be a cell too — the convention is a leading `=`:

```markdown
{: .block visible="= score > 3" }
```

```gherkin
Feature: Values that follow the page's data
  As an author
  I want to drop a live expression into a sentence or a knob
  So that my prose stays true when the learner changes something

  Scenario: A cell recomputes when its data changes
    Given a paragraph holding a cell over a form's field
    When the learner edits that field
    Then the sentence shows the new value, with no reload

  Scenario: A knob written as a cell drives visibility
    Given a block whose visible knob is an expression over the score
    When the score crosses the threshold
    Then the block appears, and disappears again when it drops back
```
{: .feature tags="data,code" status="pending" }

## Node variables — `get_var`

A node (this site's repository) can carry **variables** — generic per-node
configuration, set once in the repo under
**Settings → Secrets and variables → Variables**. The engine fetches them
with the connected author key, so they resolve only for who is connected to
**their own** node; visitors simply see the default:

```markdown
Welcome to {= get_var('CLASS_NAME', 'Customize your own class!') }.
```

The same form works in knobs, so a component can point at whatever the node
configures:

```markdown
[courses](#)
{: .folder path="= get_var('COURSE_PATH', 'courses')" open="runner" }
```

| Rule | Behaviour |
|------|-----------|
| Variable set on the connected repo | its value renders (and recomputes on arrival) |
| Not set, or nobody connected | the default renders — `🌱 To be defined` unless you pass your own |
| Never | an error. Unset is a normal, gentle state. |

**The honest boundary:** node variables are *configuration*, not secrets —
they resolve for the connected owner, and content privacy still comes from
repository privacy alone. Use them on owner-facing pages; visitor-facing
pages keep literal values.

## Notes

- Cells are eval'd, never exec'd — statements can't be typed into one, and a
  cyclic formula fails safe.
- Form fields join the namespace by id (`inputs.price`) or bare (`price`)
  when unique; the store's nodes (including `node.*`) join as scopes.
