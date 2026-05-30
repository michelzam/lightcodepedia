# ⚙️ Build your own page

In Tutorial 101 you explored what Lightcodepedia can do. Now let's make it yours.

By the end of this page you'll have your own copy of the site, you'll have edited a page in the browser, and you'll have added a live component — all without touching a terminal.

> Tell learners: "By the end of this page, each of you will have a live website with your name on it."
{: .speaker-note }

---

## 🍴 Make your own copy

Lightcodepedia is a free template. Making your own copy takes about two minutes.

1. Go to [github.com/michelzam/lightcodepedia](https://github.com/michelzam/lightcodepedia)
2. Click **Fork** → **Create a new fork**
3. Keep the default name (or pick your own) and click **Create fork**
4. In your new copy, go to **Settings → Pages**
5. Under *Build and deployment*, choose **GitHub Actions**
6. Go back to the main page of your repo and make any small edit (e.g. click the pencil on `README.md`, add a space, save)

Your site goes live at `https://your-name.github.io/lightcodepedia` within about a minute.

> Walk through the fork live on the projector. The moment the site URL appears in Settings → Pages is always a crowd moment — "it's really live?"
{: .speaker-note }

**Q:** After you fork the repo, where is your new site hosted?

- [ ] On Lightcodepedia's servers — they host all forks automatically.
- [x] On GitHub's free hosting, under your own GitHub account.
- [ ] Nowhere — you still need to buy a hosting plan.
- [ ] On your laptop — you have to run a local server to see it.
{: .quiz }

---

## ✏️ Edit a page in the browser

No need to open a code editor. Every page has a built-in editor — the **✏️** button at the bottom right.

To connect it to your copy of the site you'll need a short access key from GitHub (different from the AI key — this one needs permission to save files).

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) → **Generate new token (classic)**
2. Give it a name, check the **`repo`** box, click **Generate**
3. Copy the key
4. On your forked site, click ✏️ — paste the key and your repo name (`your-name/lightcodepedia`)
5. Click **Connect**

The file tree on the left shows every page. Click one to open it.

> Give learners 5 minutes to connect the editor. The most common stumble: they paste the repo name with a capital letter or extra space. Check for that first if someone can't connect.
{: .speaker-note }

→ [Editor documentation](/components/code)

---

## 🧩 Add your first component

Every component is just a block of content followed by a short tag in curly braces. That tag is what turns a plain text block into something interactive.

Here's the simplest example — a code runner:

````markdown
```python
print("Hello from my page! 🎉")
```
{: .run }
````

The `{: .run }` tag after the code block is the whole secret. Without it: plain code. With it: a live runner.

Open your home page in the editor, find a good spot, and paste that block. Click **Save** — your page rebuilds in about 35 seconds.

> Demo live: paste the block, save, reload the page, click ▶ Run. Then ask a learner to change the message and save again. Two edits in under two minutes — that's the aha moment.
{: .speaker-note }

**Q:** What turns a plain code block into a live interactive component?

- [ ] A special file you need to upload.
- [ ] A setting in the GitHub repo configuration.
- [x] The `{: .tag }` line immediately after the block.
- [ ] Nothing — all code blocks are interactive by default.
{: .quiz }

---

## 🎛️ Every component has options

The tag can carry extra settings. Here are a few:

| What you want | Tag to use |
|---|---|
| A Python runner | `{: .run }` |
| A Python runner with more lines | `{: .run rows="12" }` |
| An AI assistant | `{: .agent }` |
| A data table from a CSV | `{: .datagrid format="csv" }` |
| A bar chart | `{: .chart type="bar" }` |
| A map | `{: .map }` |
| Sliding presentation | `{: .slides }` |

Browse the full library for the complete list:

[Browse all components →](docs/components)
{: .folder cols="3" }

---

## 🚀 Ready to go further?

You have a live site and you can edit it. The next step is making it truly yours — custom address, your own data, your own style.

```
### 🚀 Step 3 — Go further
Custom domain, your own data, and what to do next.

[Go further →](/tutorial103)

### 🧩 Component library
See every component with live examples and documentation.

[Browse →](/components/)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="3" }

{% include backtotop.md %}
