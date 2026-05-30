# 🚀 Tutorial 103 — Deploy (Dev)

Configure `_config.yml`, set a custom domain, automate with Actions. Your LightNode, your rules.

**This page is the tutorial.** Click 📽️ to enter slide mode.

## 🗂️ Key files

```
lightcodepedia/
├── docs/
│   ├── _config.yml        ← site title, theme, plugins
│   ├── _includes/
│   │   ├── code_chrome.md ← all component JS/CSS
│   │   └── edit_on_github.md ← in-browser editor
│   ├── _layouts/
│   │   └── default.html   ← page shell (nav, footer)
│   ├── index.md           ← home page
│   └── components/        ← component docs
└── .github/
    └── workflows/         ← CI/CD (Pages deploy)
```
{: .run rows="14" readonly="true" }

> Walk through the file tree live — "there's no server config because there is no server."
{: .speaker-note }

## ⚙️ `_config.yml` essentials

```yaml
title: My LightNode
description: A learning hub for my students
lc_canonical_host: mysite.example.com
```

Change `title` and `description` — they appear in the browser tab and `<meta>` tags.
Set `lc_canonical_host` to your custom domain (used by the CDN cache buster).

**Q:** Where does `lc_canonical_host` appear in the running site?

- [ ] It's displayed in the page footer automatically
- [x] It's embedded in the page JavaScript for CDN cache busting
- [ ] It sets the GitHub Pages URL
- [ ] It's a Jekyll plugin configuration key
{: .quiz }

## 🌐 Custom domain

1. In your repo: **Settings → Pages → Custom domain** → enter `yourdomain.com`
2. At your DNS registrar, add a `CNAME` record: `www → <you>.github.io`
3. Check **Enforce HTTPS** once the cert provisions (~5 min)

GitHub Pages handles SSL automatically — free, auto-renewing Let's Encrypt certificate.

## 🤖 GitHub Actions

Every push to `main` triggers `.github/workflows/` — Jekyll builds and deploys to Pages in ~35 s.

You can add your own workflow steps: linting, link checking, data syncing from a Google Sheet, etc.

```yaml
# .github/workflows/my-custom-step.yml
on: [push]
jobs:
  sync-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/sync_data.py
```

## 🔗 Advanced: data sources

| Tier | Tool | Best for |
|------|------|----------|
| Simple | YAML in `_data/` | Static lists, config |
| Collaborative | Google Sheets CSV embed | Shared editable tables |
| Real-time | Supabase REST | Live dashboards |

## 📚 You've completed the tutorial!

```
### 🧩 Components
Browse the full interactive widget library.

[Browse →](/components/)

### 🤖 Learn with Ari
Ask your AI pair-coder anything about LightCode.

[Chat →](/ari)

### 🏠 Home
Back to the Lightcodepedia home.

[Home →](/)
```
{: .cards cols="3" }

{% include backtotop.md %}
