# 🚀 Deploys

Invisible data source that fetches your **GitHub Actions runs** and registers them as a live `.dataset`. Pair it with a `.datagrid` to get a sortable, auto-refreshing deployment table where every row is a clickable link to that run on GitHub.

Requires a GitHub Personal Access Token saved via the **Sign in** button (top-right).

## Live example

[deploys-data](#)
{: .deploys count="8" }

[Latest runs](#)
{: .datagrid bind="deploys" rows="8" }

## 🥸 How to write one

```markdown
[deploys-data](#)
{: .deploys count="8" }

[Latest runs](#)
{: .datagrid bind="deploys" rows="8" }
```

- The `.deploys` element is **hidden** — it only fetches data and registers it under the dataset key `deploys`.
- A compact `🚀 Deploys · [status] · ↻` bar appears just above the table.
- While a run is still in progress the bar shows **● live** and the data **auto-refreshes every 12 s**.
- Each table row opens the GitHub Actions run in a new tab.

## Status icons

| Icon | Meaning |
|------|---------|
| ✅ | Success |
| ❌ | Failed / timed out |
| 🚫 | Cancelled |
| ⏭️ | Skipped |
| 🔄 | In progress |
| ⏳ | Queued / waiting |

## 🎛️ Knobs

| Block | Attribute | Default | What it does |
|---|---|---|---|
| `.deploys` | `count="…"` | `8` | Runs to fetch |
| `.deploys` | `repo="…"` | _(auto)_ | `owner/repo` override; defaults to signed-in user's fork |
| `.deploys` | `id="…"` | `deploys` | Dataset key — change when placing multiple deploys blocks on one page |
| `.datagrid` | `bind="…"` | _(required)_ | Must match the `.deploys` id |
| `.datagrid` | `rows="…"` | `0` (all) | Rows per page |

## Notes

- Uses the GitHub Actions API (`/repos/{owner}/{repo}/actions/runs`). Requires **Actions enabled** on the repo.
- Each refresh counts against your hourly GitHub rate limit; remaining calls appear in your avatar menu.
- For a GitHub Pages site the relevant workflow is **pages-build-deployment**.

## 🧠 Quick check

**Q:** Your deploy is taking a minute. What's the most likely culprit?

- [x] GitHub Pages is rebuilding the site — give it a moment, it's doing its best.
- [ ] The hamster powering the server unionised.
- [ ] You deployed on a Friday. Everyone knows the rules.
- [ ] The bytes got lost and are asking for directions.
{: .quiz }
