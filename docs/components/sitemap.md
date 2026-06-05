# 🗺️ Sitemap

Force-directed graph of pages in a directory. Nodes are pages; edges are internal Markdown links between them. Node size reflects link degree; colour reflects feature status.

## Components graph

[Browse](/docs/components)
{: .sitemap path="docs/components" height="460" }

## 🥸 How to write one

Put a link to the directory you want to map, then apply `{: .sitemap }`:

```markdown
[Browse](/docs/components)
{: .sitemap path="docs/components" height="460" }
```

- **Drag** any node to rearrange; the simulation continues from there.
- **Hover** a node for its title, snippet, and feature status pills.
- **Click** a node to navigate to that page.
- Nodes tinted **green / red / amber** have passing / failing / pending features.
- Edge lines appear between pages that link to each other in their Markdown source.

## 🎛️ Knobs

| Attribute | Default | What it does |
|---|---|---|
| `path="…"` | _(required)_ | GitHub repo path of the directory to scan |
| `height="…"` | `420` | SVG canvas height in px |
