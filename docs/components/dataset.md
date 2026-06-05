# 📊 Dataset

Invisible data block that `.datagrid` and `.chart` bind to. Declare data once, reuse across multiple views.

## JSON example

```json
[
  {"month":"Jan","revenue":4200,"costs":2800},
  {"month":"Feb","revenue":5100,"costs":3100},
  {"month":"Mar","revenue":4800,"costs":2950},
  {"month":"Apr","revenue":6300,"costs":3400},
  {"month":"May","revenue":5900,"costs":3200},
  {"month":"Jun","revenue":7100,"costs":3800}
]
```
{: .dataset id="monthly" }

[Revenue by month](#)
{: .chart bind="monthly" type="bar" x="month" y="revenue" title="Revenue (€)" }

[Costs trend](#)
{: .chart bind="monthly" type="line" x="month" y="costs" title="Costs (€)" }

[Full table](#)
{: .datagrid bind="monthly" rows="4" }

## CSV example

```csv
name,score,attempts
Alice,92,3
Bob,78,5
Carol,88,2
Dave,65,7
Eve,95,1
Frank,71,4
```
{: .dataset id="scores" }

[Scores](#)
{: .datagrid bind="scores" rows="3" }

## Remote / URL source

Apply `{: .dataset }` to a **link** — the href is fetched and parsed as JSON or CSV. The datagrid shows `⏳ Loading…` until data arrives (charts too).

[https://jsonplaceholder.typicode.com/todos?_limit=8](#)
{: .dataset id="todos" }

[Todo list](#)
{: .datagrid bind="todos" rows="5" }

````markdown
[https://jsonplaceholder.typicode.com/todos?_limit=8](#)
{: .dataset id="todos" }

[Todo list](#)
{: .datagrid bind="todos" rows="5" }
````

## Clickable rows

Add a `url` field to any row — the column is **hidden** and the whole row becomes a clickable link (opens in a new tab).

```json
[
  {"name":"Google","type":"Search","url":"https://google.com"},
  {"name":"GitHub","type":"Code","url":"https://github.com"},
  {"name":"MDN","type":"Docs","url":"https://developer.mozilla.org"}
]
```
{: .dataset id="links" }

[Sites](#)
{: .datagrid bind="links" }

## 🥸 How to write one

````markdown
```json
[{"x":"A","y":10},{"x":"B","y":20}]
```
{: .dataset id="mydata" }

[Chart](#)
{: .chart bind="mydata" type="bar" x="x" y="y" title="My chart" }

[Table](#)
{: .datagrid bind="mydata" rows="10" }
````

- The `.dataset` block is **hidden** — it only registers the data.
- Apply to a **link** (`[Label](https://…)`) to fetch from a URL instead.
- `bind="id"` wires a view to the dataset; multiple views can share one dataset.
- Click any **column header** to sort. Sorting persists through pagination.
- Add a **`url` column** to make rows clickable links.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.dataset` | `id="…"` | any string | Registers data under this key |
| `.dataset` | _(applied to a link)_ | `https://…` href | Fetches JSON or CSV from the URL |
| `.datagrid` | `bind="…"` | dataset id | Which dataset to display |
| `.datagrid` | `rows="…"` | number | Rows per page (0 = all) |
| `.datagrid` | `url` column | URL string | Hidden column; makes rows clickable links |
| `.chart` | `bind="…"` | dataset id | Which dataset to plot |
| `.chart` | `type="…"` | `bar` · `line` | Chart type |
| `.chart` | `x="…"` | column name | Horizontal axis column |
| `.chart` | `y="…"` | column name | Vertical axis column |
| `.chart` | `title="…"` | string | Label above the chart |
