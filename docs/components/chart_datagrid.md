# 📊 Chart + Datagrid

A chart that updates live when you select a row in a datagrid — the same master/detail pattern as datagrid+form, but visualized.

**Try it:** click any language row below.

```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
JavaScript,62,95,68,8
Java,35,70,75,-5
TypeScript,44,55,78,25
Rust,20,15,82,40
Go,22,22,77,20
Swift,18,28,73,10
Kotlin,16,22,72,18
```
{: .datagrid #lang-grid format="csv" title="Programming languages" height="240" }

```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
JavaScript,62,95,68,8
Java,35,70,75,-5
TypeScript,44,55,78,25
Rust,20,15,82,40
Go,22,22,77,20
Swift,18,28,73,10
Kotlin,16,22,72,18
```
{: .chart type="bar" bound-to="lang-grid" x="language" height="280" }

_Columns: **popularity** = % devs using it · **demand** = job market index · **pay\_index** = relative salary · **growth** = YoY % change_

---

## How it works

The datagrid gets an `id`. The chart declares `bound-to` pointing at that id. On row selection, the chart re-renders with that row's numeric values as bars.

````markdown
```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
...
```
{: .datagrid #lang-grid format="csv" title="Languages" height="240" }

```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
...
```
{: .chart type="bar" bound-to="lang-grid" x="language" }
````

Keep the same data in both blocks — `bound-to` overrides the chart's static rendering and updates the bars on every row click. The data rows are needed so Jekyll produces a proper code block (without them, it may render as plain text).

## Options

| Attribute | Role |
|-----------|------|
| `bound-to="<id>"` | Subscribe to row selections from datagrid with that id |
| `x="<column>"` | Which column is the label (skipped as a bar value) |
| `type="bar\|line\|pie\|doughnut"` | Chart type (default: `bar`) |
| `height="280"` | Canvas height in px |

## Pie variant

Same data, different chart type — just change `type`:

```csv
language,popularity,demand,pay_index,growth
Python,58,80,72,15
JavaScript,62,95,68,8
Java,35,70,75,-5
TypeScript,44,55,78,25
Rust,20,15,82,40
Go,22,22,77,20
Swift,18,28,73,10
Kotlin,16,22,72,18
```
{: .chart type="doughnut" bound-to="lang-grid" x="language" height="260" }

{% include backtotop.md %}
