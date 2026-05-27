{% include topbar.md title="📜 Scrollable pane" %}

Wrap a content file in a fixed-height container with its own scrollbar. Great for long lists you don't want to dominate the page.

## How to use

{% raw %}
```liquid
{% include scrollable.md file="components/scrollable_example" height="220" %}
```
{% endraw %}

## Live example (height = 220px)

{% include scrollable.md file="components/scrollable_example" height="220" %}

## Options

| Parameter | Default | Description |
|---|---|---|
| `file` | required | Path to the content file (no `.md` extension) |
| `height` | `300` | Max height in pixels |

## Same content, taller pane (height = 500px)

{% include scrollable.md file="components/scrollable_example" height="500" %}

{% include backtotop.md %}
