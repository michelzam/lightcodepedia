# 📊 Datagrid

Interactive tables powered by **AG Grid Community** (~300 KB JS + ~30 KB CSS, loaded from jsDelivr on first sighting, cached after). Sort, filter, resize — all in the browser, no Python needed.

## Tiniest grid — `{: .datagrid }` on a YAML fence

Drop `{: .datagrid }` on the line right after a YAML fenced block. The page upgrades it into a live grid.

{% raw %}
````markdown
```yaml
- name: Lucky
  age: 3
  breed: Beagle
- name: Wanda
  age: 5
  breed: Poodle
- name: Max
  age: 2
  breed: Husky
```
{: .datagrid }
````
{% endraw %}

Renders to:

```yaml
- name: Lucky
  age: 3
  breed: Beagle
- name: Wanda
  age: 5
  breed: Poodle
- name: Max
  age: 2
  breed: Husky
```
{: .datagrid }

Click a column header to sort. Hover the **☰** icon to filter. Drag the right edge of a header to resize.

## Knobs

| Attribute | Description |
|---|---|
| `id="..."` | Required if you have multiple grids on the same page |
| `title="..."` | Optional title bar above the grid |
| `height="400"` | Grid height in pixels (default 400) |
| `format="yaml"` | `yaml` (default), `json`, or `csv` |

## JSON format

```json
[
  {"city": "Tokyo", "country": "Japan", "population": 37400068},
  {"city": "Delhi", "country": "India", "population": 28514000},
  {"city": "Shanghai", "country": "China", "population": 25582000},
  {"city": "São Paulo", "country": "Brazil", "population": 21650000},
  {"city": "Mexico City", "country": "Mexico", "population": 21581000}
]
```
{: .datagrid format="json" title="World's largest cities" height="250" }

## CSV format

Numbers are auto-coerced. Empty cells stay empty.

```csv
name,age,breed,adopted
Lucky,3,Beagle,true
Wanda,5,Poodle,true
Max,2,Husky,false
Bella,4,Labrador,true
Charlie,1,Pug,false
```
{: .datagrid format="csv" title="Shelter dogs" height="250" }

## When to use this vs a markdown table

| Markdown table | `{: .datagrid }` |
|---|---|
| Static, small, no interaction | Sortable, filterable, virtualized |
| Renders in any markdown viewer | Needs JS |
| 5 lines of code | 300+ KB on first sighting (cached after) |

Use markdown tables for ≤10 rows you just want to display. Use a datagrid when students need to **explore** the data — sort by a column, filter to a subset, scroll through hundreds of rows.

## Limitations of v1

- Data must be an **array of objects** (keys become columns).
- All data loads at once; no server-side pagination. Works smoothly up to ~10k rows in-browser.
- Column types inferred by AG Grid from the values; no explicit per-column overrides yet.
- Read-only — no in-cell editing, no export buttons. Ask if you want one.

{% include backtotop.md %}
