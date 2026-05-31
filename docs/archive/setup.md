# ⚙️ Setup

Everything you need to run your own LightNode — from zero to live in under 10 minutes.

## 1️⃣ Fork the repo

1. Go to [github.com/michelzam/lightcodepedia](https://github.com/michelzam/lightcodepedia)
2. Click **Fork → Create a new fork**. Keep the default name or pick your own.
3. On your fork, go to **Settings → Pages**.
4. Under *Build and deployment*, select **Source: GitHub Actions**.
5. Push any small change to `main` to trigger the first build.

Your site is live at `https://<your-username>.github.io/lightcodepedia` (or a custom domain if you add a `CNAME`).

## 2️⃣ Edit pages in the browser

Click the **✏️** button (bottom-right of any page) to open the built-in editor.

1. Generate a GitHub PAT with **`repo` scope** (classic) — [github.com/settings/tokens](https://github.com/settings/tokens)
2. Enter your PAT and repo name (`owner/repo`) in the editor connection form.
3. Browse, edit and save. Each save commits directly to `main` and triggers a new Pages build (~35 s).

[Learn more about the editor →](/components/code)

## 3️⃣ Add interactive components

Drop a fenced block + IAL tag onto any page:

````markdown
```python
print("Hello, world!")
```
{: .run }
````

[Browse all components →](/components/)

## 🤖 Enable the AI agent

Paste a GitHub PAT (no scopes needed) into any agent panel and start chatting. Your PAT stays in your browser — never on our servers.

[Agent documentation →](/components/agent)

## 🚚 Legacy Streamlit deployment

For the older Streamlit-based LightNode, see the [full deploy guide →](/archive/deploy).

## 🔗 Useful links

- [GitHub Pages docs](https://docs.github.com/en/pages)
- [Jekyll docs](https://jekyllrb.com/docs/)
- [Lightcodepedia repo](https://github.com/michelzam/lightcodepedia)
