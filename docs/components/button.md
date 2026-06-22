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

  Scenario: The variant buttons render with their labels
    Given the buttons above
    :::python
    self.btns = [Button(b._el) for b in Object._all(".button")]
    self.labels = [b.text for b in self.btns]
    :::
    When they have rendered
    Then the primary button is present
    :::python
    assert any("Get started" in t for t in self.labels), self.labels
    :::
    And the danger variant renders the Delete button
    :::python
    self.danger = None
    for b in self.btns:
        if b._el.classList.contains("button-danger"):
            self.danger = b
    assert self.danger is not None, [b._el.getAttribute("class") for b in self.btns]
    assert "Delete" in self.danger.text, self.danger.text
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

## 🏁 Final exam

**Q:** Which markdown produces a green button linking to `/submit`?

- [ ] `[Submit](/submit){: .button-success }` — variant class only.
- [x] `[Submit](/submit){: .button .button-success }` — base class + variant.
- [ ] `[Submit](/submit){: .btn .btn-success }` — Bootstrap-style classes.
- [ ] Only the old `{% raw %}{% include button.md %}{% endraw %}` form produces colored buttons.
{: .quiz }
