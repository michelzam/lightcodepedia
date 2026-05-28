# 🎠 Carousel
Auto-rotating items — perfect for quotes, testimonials, or rotating tips. Auto-advances every few seconds, and you can click the dots to jump.

## How to use

Pass items as a single string, separated by the `|` (pipe) character:

{% raw %}
```liquid
{% include carousel.md items="First quote here.|Second quote.|Third quote." %}
```
{% endraw %}

## Live example

{% include carousel.md id="demo1" items="💬 Working on this assignment showed me how visual elements make learning clearer.|💬 The progression from visual exploration to executable models supports authentic learning.|💬 Lightcodepedia bridges professional software practices with approachable computing education.|💬 Very relevant and timely submission." %}

## Options

| Parameter | Default | Description |
|---|---|---|
| `items` | required | Items separated by `\|` |
| `id` | `default` | Unique id if you have multiple carousels on one page |
| `delay` | `4000` | Milliseconds between auto-rotations |

## Slower example

{% raw %}
```liquid
{% include carousel.md id="demo2" delay="8000" items="Slow.|Slower.|Slowest." %}
```
{% endraw %}

{% include carousel.md id="demo2" delay="8000" items="🐢 Slow rotation: 8 seconds between items.|🦥 Even slower: lets readers actually read.|⏰ Use delay=8000 for long quotes." %}

{% include backtotop.md %}
