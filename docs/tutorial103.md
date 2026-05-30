# 🚀 Go further

You have a live site. You've edited pages in the browser. Now let's make it truly yours.

This page covers three things: giving your site its own address, bringing in your own data, and connecting with the wider Lightcodepedia community.

---

## 🌐 Give your site a real address

Right now your site lives at `your-name.github.io/lightcodepedia`. You can give it any address you own — like `myclass.example.com`.

**What you need:** a domain name (costs about €10/year from any registrar — Namecheap, OVH, Infomaniak, etc.)

**Three steps once you have one:**

1. In your GitHub repo → **Settings → Pages → Custom domain** → type your domain → **Save**
2. At your domain registrar, add a `CNAME` record pointing to `your-name.github.io`
3. Wait a few minutes, tick **Enforce HTTPS**, done.

Your site is now at your own address, with a free security certificate that renews automatically.

> Show a live example: lightcodepedia.org is exactly this setup — a GitHub repo, a custom domain, free hosting.
{: .speaker-note }

---

## 📁 Organise your pages

Your site is just a folder of text files. Every file becomes a page. The home page is `index.md`. Every other file (`about.md`, `python.md`, `myclass.md`) becomes a page at `/about`, `/python`, `/myclass`.

The **✏️ editor** shows all your files on the left. You can:
- **Create** a new page with the **+ New** button
- **Edit** any page by clicking it in the file tree
- **Delete** a file by removing its content and saving (or directly in GitHub)

Page titles come from the first `# Heading` in the file. That's also what the [folder component](/components/folder) uses when it auto-generates card grids from a folder.

---

## 📊 Bring in your own data

There are three levels. Pick the one that fits your situation.

```
### 📄 Simple lists
Keep data in the page itself — as a table, a YAML block, or a CSV fenced block. Good for things that rarely change.

[Datagrid →](/components/datagrid)

### 📊 Shared spreadsheet
Publish a Google Sheet as a CSV and embed it. Your collaborators edit the sheet; the page reflects it automatically.

[Chart →](/components/chart)

### 🗄️ Live database
Connect to a Supabase (free tier) table via its REST API. Good for real-time dashboards and collaborative tools.

[Agent →](/components/agent)
```
{: .cards cols="3" }

---

## 🤖 Add an AI assistant trained on your content

Every page can have an AI assistant that knows exactly what you want it to know — because you write its instructions.

````markdown
```yaml
system: |
  You are a teaching assistant for my Python course.
  Only answer questions about the topics covered in this course.
  If a student asks something off-topic, gently redirect them.
model: openai/gpt-4o-mini
```
{: .agent }
````

The `system:` field is where you define the assistant's personality, knowledge and limits. Short and specific works better than long and vague.

→ [Agent documentation](/components/agent)

---

## 🎓 Teach a whole course

A course is just a collection of pages. Here's a simple structure that works well:

```
docs/
├── index.md          ← overview and navigation
├── week01.md         ← week 1 content + exercises
├── week02.md
├── ...
└── pages/
    ├── quiz01.md     ← reusable tab content, quiz banks, etc.
    └── data01.md
```

Use the [folder component](/components/folder) on your index page to auto-generate a card grid from the folder — no manual list to maintain.

Use [slide mode](/components/slides) (`📽️` button) on any page to turn it into a presentation.

Use the [AI agent](/components/agent) on each topic page, with a system prompt focused on that week's content.

> This is how lightcodepedia.org itself is built. The components docs are just pages in a `components/` folder with a folder card on the index.
{: .speaker-note }

---

## 🌍 Join the network

Lightcodepedia is a community. Each site is a **LightNode** — an independent, forkable piece of a larger network.

- **Share your LightNode** — add it to the network map on [lightcodepedia.org](/nodes)
- **Contribute a component** — open an issue or a pull request on [github.com/michelzam/lightcodepedia](https://github.com/michelzam/lightcodepedia)
- **Learn with Ari** — the AI assistant on [/ari](/ari) knows the whole platform

---

## ✅ You've completed the tutorial

You can explore, build, and ship. Everything else is in the component docs.

```
### 🧩 Component library
See every component with live examples and documentation.

[Browse →](/components/)

### 🤖 Learn with Ari
Ask your AI guide anything about Lightcodepedia.

[Chat →](/ari)

### ⚙️ Setup reference
Quick-reference for GitHub Pages, domains and the editor.

[Setup →](/setup)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="4" }

{% include backtotop.md %}
