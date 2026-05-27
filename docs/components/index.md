{% include topbar.md %}

# 🧩 Component Gallery

Welcome, c-dev! This page lists every interactive component you can use in your `.md` pages.

**The rule of the game:** you only write markdown and `{% raw %}{% include ... %}{% endraw %}` calls. No HTML, no CSS, no JavaScript. The components live in `_includes/` and you never need to open that folder.

## Available components

- [📑 Tabs](tabs) — alternative content panels
- [🎠 Carousel](carousel) — auto-rotating quotes/items
- [📋 Dropdown menu](dropdown) — click-to-reveal link list
- [🔘 Button](button) — styled link button
- [📻 Radio group](radio) — pick-one with reveal
- [🪗 Accordion](accordion) — multiple collapsibles from one file
- [📜 Scrollable pane](scrollable) — fixed-height scrolling container
- [🪟 Embed page](embed_page) — embed another page in an iframe (safe nesting)

## How each one works

Two kinds of components:

1. **Inline-config** (carousel, dropdown, button) — you pass everything as parameters on the include line. Best for short content.
2. **File-config** (tabs, radio, accordion, scrollable) — content lives in a separate `.md` file under `docs/components/`. Best for rich content with formatting.

Click any component above to see how to use it.

{% include backtotop.md %}
