{% include topbar.md title="📻 Radio group" %}

A pick-one selector that reveals different content depending on the choice. Like tabs, but with a different visual style.

## How to use

{% raw %}
```liquid
{% include radio.md file="components/radio_example" %}
```
{% endraw %}

The content file works exactly like tabs — each `### Label` becomes a radio option.

## Live example

{% include radio.md file="components/radio_example" %}

## The content file

`docs/components/radio_example.md`:

```markdown
### Beginner
You're just starting out. Welcome!

### Intermediate
You know the basics. Time to deepen your skills.

### Advanced
You're ready for complex projects.
```

## When to use radio vs tabs

- **Tabs**: feels like switching between equal alternatives (e.g. Python / JS / Ruby)
- **Radio**: feels like answering a question (e.g. What's your level?)

Both work the same way technically.

{% include backtotop.md %}
