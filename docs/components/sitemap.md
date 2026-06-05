# 🗺️ Sitemap

Force-directed graph of pages in a directory. Nodes are pages; edges are directed internal Markdown links. Node size reflects total degree; colour reflects feature status; emoji from the page title appears inside each circle. Pages that are heavily linked-to float upward; pages that link to many others sink — giving a natural hierarchy.

## Components graph

[Browse](/docs/components)
{: .sitemap path="docs/components" height="460" }

## 🥸 How to write one

Put a link to the directory you want to map, then apply `{: .sitemap }`:

```markdown
[Browse](/docs/components)
{: .sitemap path="docs/components" height="460" }
```

- **Drag** any node to rearrange; the simulation resumes from there.
- **Hover** a node for its title, snippet, and feature status pills.
- **Click** a node to navigate to that page.
- Nodes tinted **green / red / amber** have passing / failing / pending features.
- The first **emoji** in a page's H1 title appears inside its circle.
- **Directed arrows** show which page links to which.
- **Gravity**: pages referenced by others float up; pages that reference many others sink.

## 🎛️ Knobs

| Attribute | Default | What it does |
|---|---|---|
| `path="…"` | _(required)_ | GitHub repo path of the directory to scan |
| `height="…"` | `420` | SVG canvas height in px |
