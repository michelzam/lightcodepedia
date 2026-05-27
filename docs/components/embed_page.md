{% include topbar.md %}

# 🪟 Embed page (internal)

Embed another page from this same site inside an iframe. Perfect for **safely nesting components** — each iframe is its own document, so there are no ID collisions, no shared CSS, no double JavaScript.

When called this way, the embedded page automatically hides its topbar and back-to-top button (clean look).

## How to use

{% raw %}
```liquid
{% include embed_page.md page="/components/tabs" height="500" %}
```
{% endraw %}

## Live example — tabs page embedded

{% include embed_page.md page="/components/tabs" height="600" %}

## Why use this instead of nesting?

When you put tabs inside radio inside accordion using the direct `{% raw %}{% include %}{% endraw %}` approach, several things can break:

- Same JavaScript runs twice → click events fire twice
- IDs collide → wrong panel shows on click
- CSS bleeds between components

With `embed_page.md`, each nested page is **fully isolated**:

| Issue | Direct nesting | `embed_page` |
|---|---|---|
| ID collisions | ❌ Possible | ✅ Impossible (different docs) |
| Double-firing JS | ❌ Possible | ✅ Impossible |
| Style bleed | ❌ Possible | ✅ Impossible |
| Footprint | Lighter | Heavier (extra iframe) |
| Scrolling | Page-level | Inside iframe |

## Options

| Parameter | Default | Description |
|---|---|---|
| `page` | required | Internal URL path (start with `/`) |
| `height` | `400` | iframe height in pixels |

## Live example — radio page embedded

{% include embed_page.md page="/components/radio" height="500" %}

## How it works

The include adds `?embed=true` to the URL. The `topbar.md` and `backtotop.md` includes detect this query parameter and hide themselves. The iframe shows only the page's main content.

{% include backtotop.md %}
