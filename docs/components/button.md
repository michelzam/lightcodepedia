# 🔘 Button

A styled call-to-action link. Write a normal markdown link, add `{: .button }` inline after the closing bracket, and it renders as a button. Four color variants; works anywhere a link works.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

[🚀 Get started](/components/run){: .button }
[Learn more](/components/text){: .button kind="secondary" }
[✓ Done](/components/quiz){: .button kind="success" }
[✗ Delete](#){: .button kind="danger" }
[Outline](#){: .button kind="outline" }

```gherkin
Feature: A link becomes a styled button
  As a lowcoder
  I want a markdown link tagged .button to render as a call-to-action
  So that I get buttons and color variants with no HTML or CSS

  Scenario: Every demo button renders with its label
    Given the buttons above
    :::python
    self.labels = [Button(b._el).text for b in Object._all(".button")]
    :::
    When they have rendered
    Then each labelled call-to-action is present
    :::python
    for want in ["Get started", "Learn more", "Done", "Delete", "Outline"]:
        assert any(want in t for t in self.labels), (want, self.labels)
    :::
```
{: .feature tags="ui" status="passing" }

## 🛠️ How to make one

Add `{: .button }` **immediately** after the closing `]` of any markdown link — no space, no newline:

```markdown
[🚀 Get started](/components/run){: .button }
```

This is kramdown's **inline IAL** — it attaches the class directly to the `<a>` element.

**Q:** You write `[Go](#) {: .button }` with a space before `{:`. Does the button render?

- [ ] Yes — kramdown is flexible about spaces before inline IAL.
- [x] No — the inline IAL must immediately follow the `]` with no space at all.
- [ ] It attaches to the paragraph instead.
- [ ] It becomes an outline button — the space triggers a fallback style.
{: .quiz }

## 🎨 Variants

| You write | Result |
|---|---|
| `{: .button }` | Blue (primary) |
| `{: .button kind="secondary" }` | Grey |
| `{: .button kind="success" }` | Green |
| `{: .button kind="danger" }` | Red |
| `{: .button kind="outline" }` | Transparent with blue border |

The variant is a single knob, `kind`, with values `secondary`, `success`, `danger`, or `outline`. Omit it for the blue primary.


## Events

[🗓️ Event: ON](#)
{: .button #event_btn }
```python
def on_click(button):
    if "ON" in button.text:
        button.text = "OFF"
    else:
        button.text = "ON"
```
{: .onclick }

> The handler needs an `#id` (here `#event_btn`): a click resolves the button by id to run its Python. Without one, the click can't find its handler.

```gherkin
Feature: A button runs Python on click
  As a lowcoder
  I want a :::python::: handler attached to a .button
  So that clicking it changes the page with no JavaScript

  Scenario: Clicking the event button toggles ON and OFF
    Given the #event_btn button and its on_click handler
    :::python
    self.eb = self.page.event_btn
    self.before = self.eb.text
    :::
    When its handler runs
    :::python
    self.eb.click()
    :::
    Then the label flips between ON and OFF
    :::python
    assert ("ON" in self.before) != ("ON" in self.eb.text), (self.before, self.eb.text)
    :::
```
{: .feature tags="events" status="passing" }

## 🏁 Final exam

**Q:** Which markdown produces a green button linking to `/submit`?

- [x] `[Submit](/submit){: .button kind="success" }` — base class + the `kind` knob.
- [ ] `[Submit](/submit){: .button success }` — `success` isn't a value without `kind=`.
- [ ] `[Submit](/submit){: .button .success }` — `success` as a bare class does nothing.
- [ ] `[Submit](/submit){: .btn kind="success" }` — wrong base class.
{: .quiz }
