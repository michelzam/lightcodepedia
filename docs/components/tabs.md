# 📑 Tabs

Show alternative content panels — only one tab visible at a time. Each `### Heading` in a content file becomes a tab label; everything below it becomes the panel body.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

{% include tabs.md file="components/_tabs_example" %}

Click any tab. The active tab is highlighted in blue; the others hide. That's the whole widget.

> Ask: "When would you use tabs vs a bullet list?"
> Good answers: comparing alternatives side-by-side, hiding advanced content until needed,
> showing the same thing in multiple languages.
{: .speaker-note }

**Q:** A learner clicks the second tab. What happens to the first tab's content?

- [ ] It stays visible below — tabs stack vertically on click.
- [x] It hides — only one panel is visible at a time.
- [ ] It collapses to just its heading.
- [ ] It slides into a drawer on the right. Very smooth.
{: .quiz }

## 🛠️ How to make one

Two files. That's all.

**Step 1** — add one line to your page:

{% raw %}
```liquid
{% include tabs.md file="components/my_tabs" %}
```
{% endraw %}

**Step 2** — create `docs/components/my_tabs.md`. Each `### Heading` becomes a tab; the content below it becomes the panel body:

```markdown
### 🐍 Python
Python is a great first language.
- Easy to read
- Huge community

### 🎬 Demo
Click here to try the demo.

### 📚 Resources
- [Official docs](https://docs.python.org)
```

Add another `### Section` → a new tab appears. Remove one → it's gone.

**Q:** You want to add a fourth tab called "🧪 Exercises". What do you do?

- [ ] Add `tab4="🧪 Exercises"` to the `{% raw %}{% include %}{% endraw %}` line.
- [ ] Edit `_includes/tabs.md` directly.
- [x] Add `### 🧪 Exercises` (and its body) to your content file.
- [ ] Create a new `tabs4.md` include. One include per tab.
{: .quiz }

## ✏️ Try it live — edit and see

Edit the tab content below. The preview updates instantly on every keystroke. Each `### Heading` becomes a tab; the text below it is the panel body (full markdown supported).

<div id="tabs-pg" style="display:flex;gap:0.75em;margin:1em 0;align-items:flex-start;">
<textarea id="tabs-input" spellcheck="false" style="flex:1;min-width:0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:0.85em;line-height:1.5;padding:0.8em;border:1px solid #d0d0d0;border-radius:6px;resize:vertical;min-height:260px;background:#1e1e2e;color:#cdd6f4;">### 🐍 Python
Python is a great **first language** for learners.
- Easy to read
- Huge community
- Works everywhere

### 🎬 Demo
Click below to try the demo app.

[🎬 Open Demo](../demo)

### 📚 Resources
- [Official Python docs](https://docs.python.org)
- [Cheat sheet](https://pythoncheatsheet.org)
</textarea>
<div id="tabs-preview" style="flex:1;min-width:0;"></div>
</div>

<script>
(function(){
  var _uid = 0;
  function buildTabs(text, container) {
    var sections = text.split(/\n(?=### )/);
    var tabs = sections.map(function(s){
      var lines = s.split('\n');
      var label = lines[0].replace(/^###\s*/, '').trim();
      var body = lines.slice(1).join('\n').trim();
      return { label: label, body: body };
    }).filter(function(t){ return t.label; });
    if (!tabs.length) { container.innerHTML = '<p style="color:#888;font-style:italic;">Add a <code>### Tab name</code> heading to create a tab.</p>'; return; }
    var id = 'lc-tp-' + (++_uid);
    var bar = tabs.map(function(t, i){
      return '<button class="lc-tab-btn' + (i===0?' active':'') + '" data-tab="' + id + '-' + i + '">' + t.label + '</button>';
    }).join('');
    var panels = tabs.map(function(t, i){
      return '<div id="' + id + '-' + i + '" class="lc-tab-panel' + (i===0?' active':'') + '">' + (window.marked ? marked.parse(t.body) : t.body) + '</div>';
    }).join('');
    container.innerHTML = '<div class="lc-tabs"><div class="lc-tab-bar">' + bar + '</div>' + panels + '</div>';
    container.querySelectorAll('.lc-tab-btn').forEach(function(b){
      b.addEventListener('click', function(){
        container.querySelectorAll('.lc-tab-btn').forEach(function(x){x.classList.remove('active');});
        container.querySelectorAll('.lc-tab-panel').forEach(function(x){x.classList.remove('active');});
        b.classList.add('active');
        document.getElementById(b.dataset.tab).classList.add('active');
      });
    });
  }
  function init(){
    var inp = document.getElementById('tabs-input');
    var out = document.getElementById('tabs-preview');
    if (!inp || !out) return;
    function render(){ buildTabs(inp.value, out); }
    if (window.marked) { render(); inp.addEventListener('input', render); return; }
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/marked@9/marked.min.js';
    s.onload = function(){ render(); inp.addEventListener('input', render); };
    document.head.appendChild(s);
  }
  var el = document.getElementById('tabs-pg');
  if (el) {
    var obs = new IntersectionObserver(function(e){ if(e[0].isIntersecting){ init(); obs.disconnect(); }},{threshold:0.1});
    obs.observe(el);
  }
})();
</script>

Try adding a `### ⚡ New Tab` section. Try putting a `**bold**` word or a `- bullet list` inside a panel body.

> Live demo: ask learners to add a tab called "❓ Questions" with a bullet list of their questions.
> The instant preview makes the two-file structure click — they see the rendered result
> before ever touching the include line.
{: .speaker-note }

## 🔧 Options

The `{% raw %}{% include %}{% endraw %}` line accepts a few optional parameters:

| Parameter | Default | What it does |
|---|---|---|
| `file="…"` | required | Path to the content file, without `.md` |
| `id="…"` | `"default"` | Required when more than one tabs widget lives on a page |

## ⚠️ Limits worth knowing

- **Panels are static.** Content is rendered at build time by Jekyll — no live components (runners, datagrids) inside tab panels yet.
- **One active tab at a time.** No multi-open accordion mode.
- **Two-file requirement.** The content must live in a separate `.md` file — you can't write tab content inline in the same page. This is the main ergonomic cost of the current include approach.

## 🏁 Final exam — boss level

**Q:** You add `### ⚡ Speed` to the content file but the new tab doesn't appear on the page after you save. What's missing?

- [ ] You need to add `tab5="⚡ Speed"` to the include line.
- [ ] The content file requires a front-matter `tabs: true` flag.
- [x] A Jekyll rebuild — the include processes the file at build time, not in the browser.
- [ ] The `### ` must be at column 1 with exactly one space after the hashes.

  > Jekyll processes everything at build time. Save → wait for build → reload. No hot-reload yet.
{: .quiz }

**Q:** You want two separate tabs widgets on the same page. What do you add to each include?

- [ ] Nothing — tabs widgets are automatically namespaced by file path.
- [x] A distinct `id="…"` on each include line.
- [ ] A `namespace="…"` parameter.
- [ ] You can't — one tabs widget per page is the hard limit.
{: .quiz }

{% include backtotop.md %}
