# 🗺️ Sitemap

Force-directed graph of pages in a directory. Nodes are pages; edges are directed internal Markdown links. Node size reflects total degree; colour reflects feature status; emoji from the page title appears inside each circle. Pages that are heavily linked-to float upward; pages that link to many others sink — giving a natural hierarchy.

## 📍 Where it looks

`path` defaults to **`"."`** — the folder the page itself lives in. On a
course page that is almost always what you want, so the shortest map is
just `{: .sitemap }`. Point it elsewhere with `path="courses/x"`, or up a
level with `path=".."`.

## 🌳 What the arrows mean

The map draws three different relations, and tells them apart on purpose:

| Arrow | Relation | Where it comes from |
|---|---|---|
| solid, darker | **contains** | the folder structure itself — an `index.md` owns the pages beside it and the indexes of its subfolders. Nothing to declare: the tree draws itself from the paths. |
| solid, thin | **links to** | an ordinary markdown link between two scanned pages |
| dashed, lighter | **must come first** | a link inside a `{: .prerequisite }` block |

Containment is the skeleton, so those edges also pull tighter in the
layout — folders settle into clusters. A prerequisite is a constraint
*across* the tree rather than part of its shape, so it hangs back as a
dashed overlay instead of distorting the map.

## Components graph

[Browse](/docs/components)
{: .sitemap path="docs/components" height="460" }

```gherkin
Feature: A directory becomes a force-directed sitemap
  As a lowcoder
  I want pages and their links drawn as a graph
  So that I can see a folder's structure at a glance

  Scenario: The block upgrades into a sitemap graph
    Given the sitemap above
    :::python
    self.sm = Object._all(".lc-sitemap")[0]
    :::
    When the page has upgraded it
    Then it is a visible sitemap
    :::python
    assert self.sm.visible
    :::
```
{: .feature tags="lifecycle" status="passing" }

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

## 🧠 Quick check

**Q:** In the sitemap graph, heavily linked-to pages float upward. Why?

- [x] More incoming links = more "gravity" pulling them up — a natural hierarchy.
- [ ] They are full of helium.
- [ ] They paid for premium placement.
- [ ] The graph likes them better. Graphs have favourites.
{: .quiz }
