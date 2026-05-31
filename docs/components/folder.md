---
title: Folder
---
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

---

## Example — play folder

[Browse →](docs/play)
{: .folder cols="4" }
