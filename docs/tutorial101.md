# 🌱 Tutorial 101 — Explore (No-code)

No account, no install, no code. Just click and learn.

**This page is the tutorial.** Click 📽️ to enter slide mode.

## 👀 What is Lightcodepedia?

A network of interactive learning pages hosted on GitHub — each one a **LightNode**.

Every page is built from **components**: Python runners, quizzes, charts, AI agents, maps and more.
You use them by reading, clicking and asking questions. No setup required.

> Point to any component on this page and say: "this is a LightCode component — it runs in your browser, not on a server."
{: .speaker-note }

**Q:** What do you need to start using Lightcodepedia?

- [ ] A paid GitHub account
- [ ] Python installed on your computer
- [x] Just a browser — everything runs client-side
- [ ] A university login and a VPN
{: .quiz }

## 🐍 Run your first Python

Click ▶ Run below.

```python
name = "Lightcoder"
print(f"Hello, {name}! 🌱")
```
{: .run }

You just executed Python in your browser — no install, no server, no waiting.

> Ask: "where did this code run?" Answer: in the browser, via WebAssembly (Pyodide). Zero servers.
{: .speaker-note }

**Q:** Where does the Python code actually execute?

- [ ] On a cloud VM Lightcodepedia rents for you
- [x] In your browser via WebAssembly (Pyodide)
- [ ] On GitHub's servers
- [ ] It doesn't — it's simulated output
{: .quiz }

## 🤖 Ask the AI

Paste your GitHub PAT below and ask the agent anything.

```yaml
system: You are a friendly guide for first-time Lightcode learners. Keep answers short and encouraging.
intro: "Ask me anything about Lightcodepedia — or about learning to code!"
placeholder: "What is a LightNode?"
```
{: .agent id="intro-agent" }

No server receives your PAT. It goes directly from your browser to GitHub's API.

## 📚 What's next?

You've explored. Ready to build?

```
### ⚙️ Step 2 — Compose (Low-code)
Fork the repo and start editing pages with the built-in browser editor.

[Compose →](/tutorial102)

### 🏠 Back to start
Return to the home page.

[Home →](/)
```
{: .cards cols="2" }

{% include backtotop.md %}
