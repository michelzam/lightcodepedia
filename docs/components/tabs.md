{% include topbar.md title="📑 Tabs" %}

Show alternative content panels — only one visible at a time.

## How to use

In your `.md` page, write one line:

{% raw %}
```liquid
{% include tabs.md file="components/tabs_example" %}
```
{% endraw %}

Then create a content file. Each `### Heading` becomes a tab label, and the text below it becomes the panel body.

## Live example

{% include tabs.md file="components/tabs_example" %}

## The content file

The example above reads `docs/components/tabs_example.md`, which looks like this:

```markdown
### 🐍 Python
Python is a great first language.
- Easy to read
- Huge community

### 🎬 Demo
Click below to try the demo app.

### 📚 Resources
- [Official docs](https://docs.python.org)
- [Cheat sheet](https://pythoncheatsheet.org)
```

That's it. Add a `### NewTab` section in the file → a new tab appears.

{% include backtotop.md %}
