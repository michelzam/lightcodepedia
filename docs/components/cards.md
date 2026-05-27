{% include topbar.md title="🃏 Cards" %}

A row or grid of content cards — each with a title, description, and optional link. Responsive: auto-stacks on mobile.

## How to use

{% raw %}
```liquid
{% include cards.md file="components/cards_example" cols="3" %}
```
{% endraw %}

Each `### Title` in the content file becomes one card.

## Live example (3 columns)

{% include cards.md file="components/cards_example" cols="3" %}

## The content file

`docs/components/cards_example.md`:

```markdown
### 🎬 Demo
Try the live LightCode demo right in your browser.
[Open demo →](/demo)

### 📚 Chapters
Read the course materials covering low-code fundamentals.
[Start reading →](/chapters)

### 🤖 Ari
Chat with your AI pair lightcoder.
[Chat with Ari →](/ari)
```

## Options

| Parameter | Default | Description |
|---|---|---|
| `file` | required | Path to content file (no `.md`) |
| `cols` | `auto` | Number of columns, or `auto` for responsive |
| `gap` | `18` | Spacing between cards in pixels |

## Same content, auto-responsive

{% include cards.md file="components/cards_example" cols="auto" %}

(Resize the window — cards rearrange automatically.)

{% include backtotop.md %}
