---
---
# 🧭 Menu

Turn a set of markdown links into a clean horizontal **navigation bar**. It's the same mechanism that powers this site's own top bar.

## Try it

[🏠 Home](/) [🎓 Tutorial](/tutorial101) [🧩 Components](/components/) [🚀 Start](/start)
{: .menu }

```gherkin
Feature: A link list becomes a navigation bar
  As a lowcoder
  I want a row of markdown links rendered as a nav bar
  So that I get site navigation without writing any HTML

  Scenario: The bar lists one item per link
    Given the navigation bar above (Home, Tutorial, Components, Start)
    :::python
    self.labels = None
    for m in Object._all(".lc-menu"):
        labels = Menu(m._el).items()
        if len(labels) >= 4 and any("Home" in x for x in labels):
            self.labels = labels
    :::
    When it has rendered
    Then it carries one item per link
    :::python
    assert self.labels is not None, [Menu(m._el).items() for m in Object._all(".lc-menu")]
    assert len(self.labels) == 4, self.labels
    :::
```
{: .feature tags="ui" status="passing" }

## How to add one

Write your links on one line (each link is `[emoji Label](url)`), then add `{: .menu }` on the next line:

```markdown
[🏠 Home](/) [🎓 Tutorial](/tutorial101) [🧩 Components](/components/)
{: .menu }
```

The first emoji/word of each link becomes its icon; the rest is the label. A bulleted list works too:

```markdown
- [🏠 Home](/)
- [🎓 Tutorial](/tutorial101)
- [🧩 Components](/components/)
{: .menu }
```

## This site's top bar

The top bar you see on every page is exactly this — driven by **`docs/menu.md`**. Edit that file to change the site's top menu:

```markdown
[🎓 Tutorial](/tutorial101) [🎭 Examples](/components/examples) [🧩 Components](/components/)
```

So the `.menu` component lets you build that same kind of nav anywhere in your own pages.

## Notes

- Links open in the same tab by default; add `{:target="_blank"}` to a link for a new tab.
- Pure markdown — no HTML needed. The bar is responsive and wraps on small screens.
