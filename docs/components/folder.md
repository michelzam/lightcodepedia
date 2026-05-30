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
| `show-private` | `false` | Include files whose names start with `_`. |

## Notes

- `index.md` is excluded automatically (it's the listing page itself).
- Titles come from the first `# Heading` in the file (emoji included). Falls back to prettified filename.
- Cards show a short text snippet from the first paragraph after the title.
- Links use the Jekyll URL convention: `docs/components/cards.md` → `/components/cards`.
- Uses the GitHub Contents API + raw file fetches — works on public repos without authentication.

## Example — play folder

[Browse →](docs/play)
{: .folder cols="4" }

{% include backtotop.md %}
