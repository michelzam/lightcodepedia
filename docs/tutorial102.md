# ⚙️ Tutorial 102 — Compose (Low-code)

Fork the repo. Open the editor. Add a component with one line. Done.

**This page is the tutorial.** Click 📽️ to enter slide mode.

## 🍴 Fork the repo

1. Go to [github.com/michelzam/lightcodepedia](https://github.com/michelzam/lightcodepedia)
2. Click **Fork → Create a new fork**
3. Keep the default name and click **Create fork**

Your personal copy of Lightcodepedia is now live at `https://<you>.github.io/lightcodepedia`.

> Demo: fork live, show the forked repo URL. Ask: "what just happened?" — a full website was copied in 10 seconds.
{: .speaker-note }

**Q:** After forking, your new site is hosted…

- [ ] On your laptop — you need to run a local server
- [ ] On Lightcodepedia's servers
- [x] On GitHub Pages under your own GitHub account
- [ ] Nowhere yet — you need to click Deploy first
{: .quiz }

## ✏️ Open the editor

1. Go to your forked site
2. Click the **✏️** button (bottom-right)
3. Generate a GitHub PAT with **`repo` scope**: [github.com/settings/tokens](https://github.com/settings/tokens)
4. Paste the PAT and your repo name (`you/lightcodepedia`)
5. Click **Connect**

The file tree loads. Click any `.md` file to edit it.

> Live demo: connect the editor, open `index.md`, change one word, save. Reload — change is live.
{: .speaker-note }

## 🧩 Add your first component

Every component is a fenced code block followed by a `{: .class }` IAL tag.

Open any page in the editor and add:

````markdown
```python
print("My first component! 🎉")
```
{: .run }
````

Save. Wait ~35 s for the build. Reload — your Python runner is live.

**Q:** What does the `{: .run }` tag do?

- [ ] It runs the code on the server when the page loads
- [x] It tells the LightCode JavaScript to upgrade the code block into an interactive runner
- [ ] It's a CSS class that changes the font color
- [ ] Nothing — it's ignored by Jekyll
{: .quiz }

## 🎛️ Knobs to turn

Most components accept extra attributes in the IAL:

```markdown
{: .run rows="10" id="my-editor" }
{: .agent bound="my-editor" }
{: .datagrid format="csv" height="300" }
{: .chart type="bar" x="name" }
```

[Browse all components →](/components/)

## 📚 What's next?

You can edit pages. Ready to deploy your own?

```
### 🚀 Step 3 — Deploy (Dev)
Configure your LightNode, set a custom domain, and ship it.

[Deploy →](/tutorial103)

### 🧩 Components
Browse the full component library.

[Browse →](/components/)

### 🏠 Back to start
Return to the home page.

[Home →](/)
```
{: .cards cols="3" }

{% include backtotop.md %}
