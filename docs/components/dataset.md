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

- The `.dataset` block is **hidden** on the page — it only registers the data.
- `bind="id"` links a view to the dataset by its `id`.
- Multiple `.datagrid` and `.chart` blocks can share the same dataset.
- Click any column header to sort the datagrid.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.dataset` | `id="…"` | any string | Registers data under this key |
| `.datagrid` | `bind="…"` | dataset id | Which dataset to display |
| `.datagrid` | `rows="…"` | number | Rows per page (0 = all) |
| `.chart` | `bind="…"` | dataset id | Which dataset to plot |
| `.chart` | `type="…"` | `bar` · `line` | Chart type |
| `.chart` | `x="…"` | column name | Horizontal axis column |
| `.chart` | `y="…"` | column name | Vertical axis column |
| `.chart` | `title="…"` | string | Label above the chart |
