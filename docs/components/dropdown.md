# ▾ Dropdown

A button that reveals a list of links on click. Closes when you click anywhere else. Good for navigation menus or any "pick one of these links" pattern.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

- [🐍 Run](/components/run)
- [📊 Datagrid](/components/datagrid)
- [📝 Form](/components/form)
- [🧪 Quiz](/components/quiz)
{: .dropdown label="Components ▾" }

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
| `id="…"` | auto | Required when more than one dropdown lives on the same page |

## 🏁 Final exam

**Q:** Which of these are TRUE about the dropdown? (Pick all that apply.)

- [x] Each `- [label](url)` bullet becomes one menu item.
- [x] A document-level click listener closes the menu when you click outside.
- [ ] Items must be plain text — markdown links don't work inside bullets.
- [x] `id=` is required when more than one dropdown lives on the page.
{: .quiz multi="true" }

{% include backtotop.md %}
