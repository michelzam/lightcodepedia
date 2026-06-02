---
---
# 🚀 Deployment activity

Show your repository's latest **GitHub Actions runs** — the same list you'd see on GitHub's *Actions* tab — right inside a page, in pure markdown. Each row shows the commit, the workflow, and its delivery status: ✅ done, 🟡 running, ❌ failed.

It only appears when you're **signed in** (it uses your saved GitHub token). Signed-out visitors see a polite "sign in" note instead — nothing is exposed.

## Try it

Your latest deployments.
{: .deploys }

## How to add one

Write any paragraph and add `{: .deploys }` on the next line:

```markdown
Your latest deployments.
{: .deploys }
```

The paragraph is replaced by the activity list. While a run is still in progress, the list **auto-refreshes** until it finishes.

## Options

| Attribute | Default | What it does |
|-----------|---------|--------------|
| `count` | `8` | How many recent runs to show |
| `repo` | *your repo* | `owner/name` to read from. Defaults to your connected repo (`lc_ed_repo`), or `your-login/lightcodepedia`. |

```markdown
Latest 5 runs for a specific repo.
{: .deploys count="5" repo="octocat/Hello-World" }
```

## Status icons

| Icon | Meaning |
|------|---------|
| ✅ | Completed — success |
| ❌ | Completed — failed / timed out |
| 🚫 | Cancelled |
| ⏭️ | Skipped |
| 🟡 | In progress (spinning) |
| ⏳ | Queued / waiting |

## Notes

- Uses the GitHub Actions API (`/repos/{owner}/{repo}/actions/runs`). Requires **Actions enabled** on the repo (GitHub Pages deployments count).
- Each refresh costs one API call against your hourly GitHub rate limit; the remaining count is tracked in your avatar menu.
- For a GitHub Pages site, the relevant workflow is **pages-build-deployment** — that's your "is my site live yet?" status.
