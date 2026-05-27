{% include topbar.md %}

# 🔘 Button

A styled link that looks like a clickable button.

## How to use

{% raw %}
```liquid
{% include button.md label="🎬 Watch Demo" href="../demo" %}
```
{% endraw %}

## Live example

{% include button.md label="🎬 Watch Demo" href="../demo" %}

## Styles

Pass an optional `style=` parameter for different colors:

{% include button.md label="Primary (default)" href="#" %}
{% include button.md label="Secondary" href="#" style="secondary" %}
{% include button.md label="Success" href="#" style="success" %}
{% include button.md label="Danger" href="#" style="danger" %}
{% include button.md label="Outline" href="#" style="outline" %}

The code for the row above:

{% raw %}
```liquid
{% include button.md label="Primary (default)" href="#" %}
{% include button.md label="Secondary" href="#" style="secondary" %}
{% include button.md label="Success" href="#" style="success" %}
{% include button.md label="Danger" href="#" style="danger" %}
{% include button.md label="Outline" href="#" style="outline" %}
```
{% endraw %}

## Options

| Parameter | Default | Description |
|---|---|---|
| `label` | required | Button text |
| `href` | required | Where the button links to |
| `style` | (primary) | `secondary`, `success`, `danger`, or `outline` |

{% include backtotop.md %}
