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

## Two postures — read and workbench

- **Read** (default): the listing you see everywhere — underscore-prefixed
  files (`_menu.md`, fragments, `_trash/`…) stay hidden, and there are no
  writing affordances at all.
- **Workbench** (🔬 **X-ray mode**, on a runner render, with a connected
  key that can **push to this repo** — never under `editable=0`): the shelf
  turns writable. Pedagogical access is not ownership: X-raying someone
  else's material gives the lens, never the tools. In the workbench,
  **➕ New** appears, **every** file shows (underscore ones included), each
  card keeps its full read-mode preview and decorations and gains an
  **appended row**: the real **file name** and a **⚙️** menu:
  - **✏️ Rename** — same folder, new name;
  - **📦 Move to…** — type the destination folder;
  - **🗑 Trash** — moves the file to a `_trash/` subfolder with a
    `_deleted_<timestamp>` suffix. Recoverable, never destructive.

  Subfolder cards get the same **⚙️** (a folder is its files: rename, move
  and trash walk every file beneath it, `_trash` keeps the inner structure)
  plus a **census**: `📄 public/total` files, sub-sub-folders included —
  the weight of every branch at a glance. The menu's first entry, **🔬
  Open**, jumps to the file (or the folder's `index.md`) straight in X-ray,
  and **Move to…** autocompletes from the repo's own folders. One boundary
  holds everywhere: gears change **slots** — the folder's generated cards
  are derivatives, so the text-edit ghost never lands on them.

  The shelf re-lists live when X-ray opens or closes, and X-ray survives a
  refresh (`?xray=1` rides in the URL, like reel's `?reel=1`). A new
  **folder** is always born as its `index.md` with a bare `{: .folder }`
  inside — every node lists its own children from day one.

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
