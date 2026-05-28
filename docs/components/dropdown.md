# 📋 Dropdown menu
A button that reveals a vertical list of links when clicked.

## How to use

Pass items as `Label:url` pairs, separated by `|`:

{% raw %}
```liquid
{% include dropdown.md label="Resources" id="res" items="🐍 Python:../python|📚 Chapters:../chapters|🎬 Demo:../demo" %}
```
{% endraw %}

## Live example

{% include dropdown.md label="Resources" id="res" items="🐍 Python:../python|📚 Chapters:../chapters|🎬 Demo:../demo|🎈 Play:../play" %}

## Options

| Parameter | Default | Description |
|---|---|---|
| `label` | `Menu` | The button text |
| `id` | `dd` | Unique id if multiple dropdowns on one page |
| `items` | required | `Label:url` pairs separated by `\|` |

## Two dropdowns on one page

{% include dropdown.md label="Learn" id="learn" items="🐍 Python:../python|📚 Chapters:../chapters" %}
{% include dropdown.md label="Play" id="play" items="🎈 Play:../play|🎡 Examples:../examples|🎬 Demo:../demo" %}

⚠️ **Heads up:** URLs containing `:` (like `https://...`) don't work as values — use relative paths to internal pages. If you need external links, use a regular markdown link below the dropdown.

{% include backtotop.md %}
