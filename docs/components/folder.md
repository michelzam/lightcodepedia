# 📁 Folder

Auto-generate a card grid from all `.md` files in a given folder — no manual list to maintain.

**The rule:** one link, one IAL tag. The component fetches the folder from GitHub and renders each page as a card.

## Syntax

```markdown
[Browse →](docs/components)
{: .folder cols="3" }
```

### Result — components folder

[Browse →](docs/components)
{: .folder cols="3" }

---

## Options

| Attribute | Default | Description |
|-----------|---------|-------------|
| `cols` | `auto` | Fixed number of columns. `auto` = responsive grid. |

## Notes

- `index.md` is excluded automatically (it's the listing page itself).
- Titles are derived from the filename: `getting-started.md` → **Getting Started**.
- Links use the Jekyll URL convention: `docs/components/cards.md` → `/components/cards`.
- Uses the GitHub Contents API — works on public repos without authentication.

## Example — play folder

[Browse →](docs/play)
{: .folder cols="4" }

{% include backtotop.md %}
