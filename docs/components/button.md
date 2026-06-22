# 🔘 Button

A styled call-to-action link. Write a normal markdown link, add `{: .button }` inline after the closing bracket, and it renders as a button. Four color variants; works anywhere a link works.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

[🚀 Get started](/components/run){: .button }
[Learn more](/components/text){: .button .button-secondary }
[✓ Done](/components/quiz){: .button .button-success }
[✗ Delete](#){: .button .button-danger }
[Outline](#){: .button .button-outline }

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
| `{: .button .button-secondary }` | Grey |
| `{: .button .button-success }` | Green |
| `{: .button .button-danger }` | Red |
| `{: .button .button-outline }` | Transparent with blue border |


## Events

[🗓️ Event: ON](#)
{: .button }
```python
def on_click(button):
    if button.text == "ON" 
        button.text = "OFF"
    else:
        button.text = "ON"
```
{: .onclick }

## 🏁 Final exam

**Q:** Which markdown produces a green button linking to `/submit`?

- [ ] `[Submit](/submit){: .button-success }` — variant class only.
- [x] `[Submit](/submit){: .button .button-success }` — base class + variant.
- [ ] `[Submit](/submit){: .btn .btn-success }` — Bootstrap-style classes.
- [ ] Only the old `{% raw %}{% include button.md %}{% endraw %}` form produces colored buttons.
{: .quiz }
