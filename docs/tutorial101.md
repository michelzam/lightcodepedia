# 👋 Welcome to Lightcodepedia

You're looking at a page made of blocks. Some blocks have text. Some have code you can run. Some let you chat with an AI. Some show data as charts or maps.

All of them work right here in your browser — nothing to install, nothing to sign up for.

This page will walk you through what you can do. Just read, click, and explore.

> Tell learners: "Don't just read — everything on this page is live. Click buttons, type questions, select rows. That's the point."
{: .speaker-note }

---

## ▶️ Try running code

See that button below? Click ▶ **Run**.

```python
print("Hello! 👋")
print("I'm running right inside your browser.")
```
{: .run }

That's a **code runner**. Real code, real output — no install, no account, no waiting.

You can also edit the code and run it again. Try changing the message.

> Let learners change the text and re-run. They'll realise they're writing code without knowing it.
{: .speaker-note }

→ Want to add a code runner to your own page? [See the documentation.](/components/run)

---

## 💬 Ask a question

Below is an **AI assistant**. It knows about Lightcodepedia and can answer questions about coding, learning, or anything else.

Type a question and click **Ask**.

```yaml
system: |
  You are a friendly guide for first-time Lightcodepedia visitors.
  Keep answers short (2–3 sentences), warm, and jargon-free.
  If asked about code, give a tiny example. Never mention "PAT", "API keys" or technical setup.
intro: "Ask me anything — about this page, about coding, about anything!"
placeholder: "What is Lightcodepedia?"
```
{: .agent id="welcome-agent" }

The first time you use this, it will ask for a free access key — a short code you get from GitHub in about a minute. The key goes directly from your browser to GitHub's AI service. This site never sees it.

→ Learn more about the AI assistant: [Agent documentation.](/components/agent)

> Walk through getting the access key live. Route A (classic token, no scopes) takes under 60 seconds. Do it with them — one stumble here loses half the class.
{: .speaker-note }

---

## 📊 Explore data

Click any row in the table below — the chart updates to show that row's values.

```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
JavaScript,62,95,68,8
Java,35,70,75,-5
TypeScript,44,55,78,25
Rust,20,15,82,40
Go,22,22,77,20
```
{: .datagrid #tut-grid format="csv" title="Programming languages" height="220" }

```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
JavaScript,62,95,68,8
Java,35,70,75,-5
TypeScript,44,55,78,25
Rust,20,15,82,40
Go,22,22,77,20
```
{: .chart type="bar" bound-to="tut-grid" x="language" height="240" }

This is a **data table** linked to a **chart**. Select a row — the chart redraws instantly.

→ [Datagrid documentation](/components/datagrid) · [Chart documentation](/components/chart)

> Ask: "Which language has the highest demand? Which has the best pay index?" Let them click to find out — that's the whole point of interactive data.
{: .speaker-note }

---

## 🗺️ See it on a map

Data doesn't have to be rows and columns. Here it is on a map.

```json
[
  { "lat": 48.85, "lon": 2.35, "label": "Paris — France 🇫🇷" },
  { "lat": 50.85, "lon": 4.35, "label": "Brussels — Belgium 🇧🇪" },
  { "lat": 52.37, "lon": 4.90, "label": "Amsterdam — Netherlands 🇳🇱" },
  { "lat": 52.52, "lon": 13.40, "label": "Berlin — Germany 🇩🇪" },
  { "lat": 41.90, "lon": 12.50, "label": "Rome — Italy 🇮🇹" }
]
```
{: .map height="280" zoom="4" }

→ [Map documentation](/components/map)

---

## 🧩 Everything is a block

Every interactive element you've seen on this page is a **component** — a block of content with a small tag that brings it to life.

Browse the full component library to see what else is possible:

[Browse →](docs/components)
{: .folder cols="3" }

---

## ✅ Check what you've learned

Now that you've seen everything — here's a quick check.

**Q:** You clicked ▶ Run and saw output appear. Where did the code actually run?

- [ ] On Lightcodepedia's servers — it was sent over the internet.
- [x] In your own browser — no server was involved.
- [ ] On GitHub's computers.
- [ ] It was pre-recorded — the output was already stored in the page.
{: .quiz }

**Q:** You selected a row in the data table and the chart changed. What caused that?

- [ ] The page reloaded in the background.
- [ ] The server recalculated the chart.
- [x] The chart is linked to the table — it updates automatically when you select a row.
- [ ] Pure magic. Accept it.
{: .quiz }

---

## 🚀 Ready to build?

You've seen what Lightcodepedia can do. Now let's make your own page.

```
### ⚙️ Step 2 — Build your own page
Learn to make a copy of this site and add your own components in minutes.

[Start building →](/tutorial102)

### 🧩 Component library
See every component with live examples and documentation.

[Browse →](/components/)

### 🏠 Back to home
[Home →](/)
```
{: .cards cols="3" }

{% include backtotop.md %}
