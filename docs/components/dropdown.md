# ▾ Dropdown

Too many links crowding your page? Tuck them behind a button! **Dropdown is your instrument** ▾ — one click reveals the list, a click anywhere else hides it again. Great for navigation menus or any "pick one of these" moment.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

- [🐍 Run](/components/run)
- [📊 Datagrid](/components/datagrid)
- [📝 Form](/components/form)
- [🧪 Quiz](/components/quiz)
{: .dropdown label="Components ▾" }

```gherkin
Feature: Dropdown reveals its links on demand
  As a reader
  I want a button that unfolds a list of links
  So that navigation stays tidy until I need it

  Scenario: Opening the dropdown reveals its menu
    Given the dropdown above
    :::python
    self.dd = Dropdown._all(".lc-dropdown")[0]
    self.dd.close()
    :::
    When I open it
    :::python
    self.dd.open()
    :::
    Then its menu is shown
    :::python
    assert self.dd.opened
    :::

  Scenario: Closing the dropdown hides its menu
    Given the dropdown above, opened
    :::python
    self.dd = Dropdown._all(".lc-dropdown")[0]
    self.dd.open()
    :::
    When I close it
    :::python
    self.dd.close()
    :::
    Then its menu is hidden
    :::python
    assert not self.dd.opened
    :::
```
{: .feature tags="ui" }

Click the button. Pick a link. Click anywhere else to close.

> Useful when you have 5+ navigation links that shouldn't all crowd the page at once.
{: .speaker-note }

**Q:** The dropdown is open. You click outside the button. What happens?

- [x] The menu closes — a `document` click listener dismisses it.
- [ ] Nothing — click the button again to close.
- [ ] The first link activates automatically.
- [ ] The page scrolls to the top.
{: .quiz }

## 🛠️ How to make one

A bullet list of markdown links with `{: .dropdown label="…" }` on the next line:

```markdown
- [🐍 Run](/components/run)
- [📊 Datagrid](/components/datagrid)
- [📝 Form](/components/form)
{: .dropdown label="Components ▾" }
```

Each `- [label](url)` becomes one menu item.

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `label="…"` | `"Menu"` | Button label |
| `#id` | auto | Optional — auto-assigned if omitted; add one only to reference this dropdown from elsewhere |

## 🏁 Final exam

**Q:** Which of these are TRUE about the dropdown? (Pick all that apply.)

- [x] Each `- [label](url)` bullet becomes one menu item.
- [x] A document-level click listener closes the menu when you click outside.
- [ ] Items must be plain text — markdown links don't work inside bullets.
- [ ] An `#id` is required when there is more than one dropdown.
{: .quiz multi="true" }
