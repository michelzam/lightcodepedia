# 📁 Folder

Auto-generate a card grid from all `.md` files in a folder — no manual list to maintain. Subfolders that have an `index.md` also appear as cards.

**The rule:** one link, one IAL tag. The component fetches the folder from GitHub and renders each page as a card.

## Syntax

```markdown
[Browse →](docs/components)
{: .folder cols="3" }
```

## Options

| Attribute | Default | Description |
|-----------|---------|-------------|
| `cols` | `auto` | Fixed number of columns. `auto` = responsive grid. |
| `show-private` | `false` | Include files whose names start with `_`. |
| `sort` | `name` | Initial order: `name` or `recent` (git dates, lazy). |
| `open` | | `runner`: scan a repo path *outside* `docs/` (unrendered material like `courses/`) via the API with your key — every card opens in the runner. |
| `path` | the link href | Folder to scan. Accepts a knob-cell: `path="= get_var('COURSE_PATH', 'courses')"` resolves the node's variable (see [Cells](/components/cells)). |

## Notes

- `index.md` is excluded from the file list (it's the listing page itself).
- **Subfolders** that contain an `index.md` are shown as 📁 cards at the top of the grid.
- Titles come from the first `# Heading` in the file (emoji included). Falls back to a prettified filename.
- Cards show a short text snippet from the first paragraph after the title.
- Links use the Jekyll URL convention: `docs/components/cards.md` → `/components/cards`.
- Uses the GitHub Contents API — works on public repos; uses your stored PAT if available.

## Example — components folder

The `docs/components` folder contains many `.md` files **and** a subfolder `examples/` with its own `index.md`. Both appear as cards:

[Browse →](docs/components)
{: .folder cols="3" }

```gherkin
Feature: A directory that presents itself
  As an author
  I want a folder to become a grid of cards on its own
  So that adding a page is the only thing I ever have to do

  Scenario: Every page in the folder gets a card
    Given a folder holding several pages and a subfolder with an index
    When the page renders
    Then each page is a card, and the subfolder is a card too
    And no card was written by hand

  Scenario: The cards carry what the pages declare
    Given pages that declare features and quizzes
    When the cards are built
    Then each card shows that page's tags and its feature status
    And the tags become filters above the grid

  Scenario: A bare folder means "where I am"
    Given a folder tag with no path
    When the page renders
    Then it lists the folder the current page lives in
```
{: .feature tags="ui,lifecycle" status="pending" }

---

## Example — play folder

[Browse →](docs/play)
{: .folder cols="4" }

## 🧠 Quick check

**Q:** A folder turns a directory into a grid of cards automatically. How many cards must you write by hand?

- [x] Zero. It reads the folder and builds them for you.
- [ ] One per page, lovingly handcrafted at midnight.
- [ ] Depends how much coffee you've had.
- [ ] All of them, in raw HTML, like an animal.
{: .quiz }
