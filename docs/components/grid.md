{% include topbar.md title="📐 Grid" %}

A free-form layout grid. Each cell can hold any content — text, images, even other components. Use it for dashboards or side-by-side comparisons.

## How to use

{% raw %}
```liquid
{% include grid.md file="components/grid_example" cols="2" %}
```
{% endraw %}

Each `### Heading` in the content file becomes a grid cell.

## Live example (2 columns)

{% include grid.md file="components/grid_example" cols="2" %}

## The content file

`docs/components/grid_example.md`:

```markdown
### Quick links
{% raw %}{% include button.md label="🎬 Demo" href="/demo" %}
{% include button.md label="📚 Read" href="/chapters" style="secondary" %}{% endraw %}

### Live status
A small text block, or any markdown.

### Carousel of tips
{% raw %}{% include carousel.md id="g1" items="Tip A|Tip B|Tip C" %}{% endraw %}

### Stats badges
![Forks](https://img.shields.io/github/forks/michelzam/lightcodepedia)
```

## Options

| Parameter | Default | Description |
|---|---|---|
| `file` | required | Path to content file (no `.md`) |
| `cols` | `auto` | Columns count, or `auto` for responsive |
| `gap` | `18` | Spacing between cells in pixels |
| `headings` | (shown) | Pass `hide` to suppress cell titles |

## Same content without cell headings

{% include grid.md file="components/grid_example" cols="2" headings="hide" %}

## Cards vs Grid — which one?

| | `cards.md` | `grid.md` |
|---|---|---|
| Visual chrome | Bordered card with hover effect | Plain cell, no decoration |
| Best for | Link lists, feature showcases | Dashboards, mixed-content layouts |
| Cell content | Text + optional link | Anything (other includes welcome) |

{% include backtotop.md %}
