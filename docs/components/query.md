---
---
# 🔎 Query

A **query** is a dataset computed by SQL over *other* datasets. Because a `{: .query }` **is** a dataset — it publishes its result under its id — any grid, chart, or stat binds to it exactly like a hand-written `{: .dataset }`. They can't tell the difference: a query is a dataset that computes itself. The SQL runs in your browser (no server), and it re-runs whenever an input changes.

## 👀 See it in action

A plain dataset of dogs:

```csv
breed,weight_kg,cuteness
Beagle,12,8
Poodle,20,7
Beagle,14,9
Corgi,11,10
Poodle,22,6
Corgi,10,9
```
{: .dataset #dogs }

A query that aggregates it — grouped, counted, averaged, sorted:

```sql
SELECT breed, COUNT(*) AS n, AVG(cuteness) AS cuteness
FROM dogs GROUP BY breed ORDER BY cuteness DESC
```
{: .query bind="dogs" #by_breed }

[By breed](#)
{: .datagrid bind="by_breed" }

[Cuteness by breed](#)
{: .chart bind="by_breed" type="bar" x="breed" y="cuteness" }

The grid and chart above bind to `by_breed` — a *query result*, not a raw dataset — and neither needed any special wiring. **Shift-X-ray** the chart and you'll see the whole flow light up: `chart → by_breed (Query) → dogs (Dataset)`.

## 🛠️ How to make one

Put SQL in a fenced block, name the input dataset(s) with `bind=`, and give the result an `id`:

````markdown
```sql
SELECT region, SUM(amount) AS total FROM sales GROUP BY region
```
{: .query bind="sales" #by_region }
````

- `bind="a,b"` — input dataset id(s); reference them as tables by id in the SQL (`FROM a JOIN b …`).
- `id="…"` — the result is published under this id, so `{: .chart bind="…" }` and friends just work.
- **Reactive**: edit an upstream `editable` grid and the query — and everything downstream — re-runs live.

SQL runs via [AlaSQL](https://github.com/AlaSQL/alasql) in the browser. It's permissive, learner-friendly SQL (`SELECT`/`JOIN`/`GROUP BY`/window functions) — not a strict ANSI reference.

## ✏️ Live SQL editor

Add `editable="true"` and the block becomes a **SQL editor** wired to the same data. Edit the query, press **▶ Run**, and everything bound to its result moves — a live SQL playground, no server:

```sql
SELECT breed, MAX(cuteness) AS top FROM dogs GROUP BY breed ORDER BY top DESC
```
{: .query bind="dogs" #live_q editable="true" }

[Result](#)
{: .datagrid bind="live_q" }

Try changing `MAX` to `MIN`, or `cuteness` to `weight_kg`, and Run — the grid updates. The result is still a dataset, so a chart could bind to `live_q` just the same.

**Q:** A `{: .chart bind="by_breed" }` is pointed at a query result. What does the chart need to know about the query?

- [x] Nothing — a query is a dataset, so the chart binds to it the same way.
- [ ] It must use `{: .chart query="…" }` instead of `bind`.
- [ ] The query has to run first and be saved to a file.
- [ ] Charts can't read query results, only raw datasets.
{: .quiz }
