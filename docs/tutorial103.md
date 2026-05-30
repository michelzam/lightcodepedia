# 🚀 Go further

You have a live site with your own blocks. Now let's make it truly yours.

- [x] Give it its own address
- [x] Organise your pages
- [x] Bring in your own data — three levels
- [x] Add an AI assistant with its own personality
- [x] Turn any page into a slide presentation
- [x] Connect with the Lightcodepedia community

---

## 🌐 This is a custom address block

Right now your site is at `your-name.github.io/lightcodepedia`. You can give it any address you own.

**What you need:** a domain name — about €10/year from any registrar (OVH, Namecheap, Infomaniak…).

**Three steps:**

1. In your GitHub repo → **Settings → Pages → Custom domain** → enter your domain → **Save**
2. At your registrar, add a `CNAME` record pointing to `your-name.github.io`
3. Tick **Enforce HTTPS** once the certificate appears (a few minutes)

Done. Your site now has its own address, with a free security certificate that renews itself automatically.

_The site you're on right now — `lightcodepedia.org` — is exactly this setup: a GitHub repo, a free custom domain, zero servers._

---

## 📁 This is a pages block

Your site is a folder of text files. Each file is a page.

```
docs/
├── index.md         ← home
├── about.md         ← /about
├── myclass.md       ← /myclass
└── pages/
    ├── week01.md    ← tab content, quiz banks, reusable blocks
    └── week02.md
```

The **✏️ editor** shows all your files. Use **+ New** to create a page. The file name becomes the URL (`myclass.md` → `/myclass`). The first `# Heading` in the file becomes the page title everywhere it appears — in navigation, in card grids, in search.

Use the folder block to auto-generate a card grid from any folder — no manual list to maintain:

```markdown
[Browse →](docs/components)
{: .folder cols="3" }
```

_[Folder documentation →](/components/folder)_

---

## 📊 This is a data block — three levels

Pick the level that fits your situation.

```
### 📄 Level 1 — Data in the page
Write your data directly in the page as a CSV or table. Good for things that rarely change.

[Datagrid →](/components/datagrid)

### 📊 Level 2 — Shared spreadsheet
Publish a Google Sheet as a CSV. Your colleagues edit the sheet; the page reflects it instantly — no rebuild needed.

[Chart →](/components/chart)

### 🗄️ Level 3 — Live database
Connect to a Supabase table (free tier). Good for real-time dashboards and multi-user tools.

[Agent →](/components/agent)
```
{: .cards cols="3" }

---

## 🤖 This is an AI block — with its own personality

Every page can have its own AI assistant, trained on whatever you want it to know — because you write its instructions.

````markdown
```yaml
system: |
  You are a teaching assistant for a Python course for beginners.
  You only answer questions about the topics in this course.
  Keep answers short. When someone seems stuck, ask what they tried first.
  If a question is off-topic, gently redirect: "That's outside this course — try asking on Stack Overflow."
model: openai/gpt-4o-mini
intro: "Ask me anything about Python — I'm here to help!"
```
{: .agent }
````

Short and specific instructions work better than long ones. The `system:` field is a creative writing exercise: write the assistant you wish you had.

_[Agent documentation →](/components/agent)_

---

## 📽️ This page is already a slide presentation

Click the **📽️** button at the bottom left of any page. Every `## Section` becomes a slide. Click → to advance.

Each page on this site doubles as a slide deck — nothing to configure, no extra files, no export. The same page works as a reading document and as a presentation.

Speaker notes appear only in presenter view:

```markdown
> This is a speaker note — only you see it during a presentation.
{: .speaker-note }
```

_[Slides documentation →](/components/slides)_

---

## 🌍 This is a community block

Lightcodepedia is not a product — it's a network. Each site is a **LightNode**: independent, forkable, owned by its educator.

- **Add your LightNode to the map** — [lightcodepedia.org/nodes](/nodes)
- **Suggest a new component** — open an issue on [github.com/michelzam/lightcodepedia](https://github.com/michelzam/lightcodepedia)
- **Ask Ari anything** — the AI guide at [/ari](/ari) knows the whole platform

---

## 🧩 Quick check

**Q:** You have a data table that three colleagues update every week. What's the best approach?

- [ ] Edit the page by hand each time and save.
- [x] Connect the table to a shared Google Sheet — colleagues update the sheet, the page reflects it.
- [ ] Email the data to Lightcodepedia support and ask them to update the page.
- [ ] Use Level 3 — a live database — it's always better.
{: .quiz }

**Q:** You want the same AI assistant on every page of your course, but with the same personality each time. What do you do?

- [ ] Copy-paste the agent block on every page.
- [x] Copy-paste it — but write the `system:` prompt once and reuse it verbatim. (Reusable pages are a planned feature.)
- [ ] Buy a higher-tier plan to unlock global assistant configuration.
- [ ] It's not possible — each assistant is completely independent.
{: .quiz }

---

## ✅ You've completed the tutorial

You can explore, build, customise and ship. Everything else is in the component docs.

```
### 🧩 Component library
Every block, with live examples and full documentation.

[Browse →](/components/)

### 🤖 Learn with Ari
Ask your AI guide anything about Lightcodepedia.

[Chat →](/ari)

### ⚙️ Setup reference
Quick-reference for forking, domains and the editor.

[Setup →](/setup)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="4" }

{% include backtotop.md %}
