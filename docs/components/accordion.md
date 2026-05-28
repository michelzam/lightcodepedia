# 🪗 Accordion
Multiple collapsible sections stacked together. Each can open/close independently.

## How to use

{% raw %}
```liquid
{% include accordion.md file="components/accordion_example" %}
```
{% endraw %}

Same content-file convention as tabs and radio: split by `### Label`.

## Live example

{% include accordion.md file="components/accordion_example" %}

## The content file

`docs/components/accordion_example.md`:

```markdown
### What is LightCode?
A no-code/low-code platform for learning to build apps.

### Who can use it?
Anyone — no programming experience needed.

### How much does it cost?
Free. Hosted on GitHub and Streamlit Cloud.
```

## When to use accordion vs collapsible vs tabs

- **`collapsible`**: one section, one toggle (e.g. EU funding details)
- **`accordion`**: many sections, each independent (e.g. FAQ)
- **`tabs`** / **`radio`**: many sections, only one visible at a time

{% include backtotop.md %}
