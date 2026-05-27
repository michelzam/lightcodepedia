{% include topbar.md %}

# 🧩 Component Gallery

Welcome, lowcoder! This page lists every interactive component you can use in your `.md` pages.

**The rule of the game:** you only write markdown and `{% raw %}{% include ... %}{% endraw %}` calls. No HTML, no CSS, no JavaScript. The components live in `_includes/` and you never need to open that folder.

## Available components

{% include cards.md file="components/index_cards" cols="3" %}

## How each one works

Two kinds of components:

1. **Inline-config** (carousel, dropdown, button) — you pass everything as parameters on the include line. Best for short content.
2. **File-config** (tabs, radio, accordion, scrollable, cards, grid) — content lives in a separate `.md` file under `docs/components/`. Best for rich content with formatting.

Click any card above to see how to use each component.

{% include backtotop.md %}
