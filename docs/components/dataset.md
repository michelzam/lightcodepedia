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
{: .dataset #monthly }

[Revenue by month](#)
{: .chart source="monthly" type="bar" x="month" y="revenue" title="Revenue (€)" }

[Costs trend](#)
{: .chart source="monthly" type="line" x="month" y="costs" title="Costs (€)" }

[Full table](#)
{: .datagrid source="monthly" rows="4" }

## Master/detail — dataset → grid → chart

Give the bound grid an **id** and it becomes a master/detail source: clicking
a row publishes it, and a `master` chart renders that row's numeric fields.
One dataset, declared once — the grid is its list view, the chart the detail
view of your selection.

[Pick a month](#)
{: .datagrid source="monthly" rows="6" #monthly_grid }

[Selected month](#)
{: .chart master="monthly_grid" x="month" height="240" }

```gherkin
Feature: One dataset feeds many bound views
  As a lowcoder
  I want to declare data once and bind several grids and charts to it
  So that every view stays in sync without copy-pasting the data

  Scenario: A dataset declared once is shared by every bound view
    Given the #monthly dataset declared once above
    :::python
    self.ds = self.page.monthly
    :::
    When a grid binds to it with source="monthly"
    :::python
    self.grid = self.page.monthly_grid
    :::
    Then the dataset holds all six months
    :::python
    assert self.ds.count == 6, self.ds.count
    :::
    And the bound grid renders every row
    :::python
    assert self.grid.row_count == 6, self.grid.row_count
    :::

  Scenario: Any bound grid row is selectable
    Given the #monthly_grid bound grid above
    :::python
    self.trs = self.page.monthly_grid._qq("tbody tr")
    :::
    When I click its second row
    :::python
    self.trs[1]._el.click()
    :::
    Then that row is the only selected row
    :::python
    assert self.trs[1]._el.classList.contains("lc-dg-selected")
    assert not self.trs[0]._el.classList.contains("lc-dg-selected")
    :::
```
{: .feature tags="data" }

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
{: .dataset #scores }

[Scores](#)
{: .datagrid source="scores" rows="3" }

## Remote / URL source

Apply `{: .dataset }` to a **link** — the href is fetched and parsed as JSON or CSV. The datagrid shows `⏳ Loading…` until data arrives (charts too).

[todos — jsonplaceholder](https://jsonplaceholder.typicode.com/todos?_limit=8)
{: .dataset #todos }

[Todo list](#)
{: .datagrid source="todos" rows="5" }

````markdown
[todos — jsonplaceholder](https://jsonplaceholder.typicode.com/todos?_limit=8)
{: .dataset #todos }

[Todo list](#)
{: .datagrid source="todos" rows="5" }
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
{: .dataset #links }

[Sites](#)
{: .datagrid source="links" }

## 🥸 How to write one

````markdown
```json
[{"x":"A","y":10},{"x":"B","y":20}]
```
{: .dataset #mydata }

[Chart](#)
{: .chart source="mydata" type="bar" x="x" y="y" title="My chart" }

[Table](#)
{: .datagrid source="mydata" rows="10" }
````

- The `.dataset` block is **hidden** — it only registers the data.
- Apply to a **link** (`[Label](https://…)`) to fetch from a URL instead.
- `source="id"` wires a view to the dataset; multiple views can share one dataset.
- Click any **column header** to sort. Sorting persists through pagination.
- Add a **`url` column** to make rows clickable links.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.dataset` | `#id` | snake_case | Registers data under this key |
| `.dataset` | _(applied to a link)_ | `https://…` href | Fetches JSON or CSV from the URL |
| `.datagrid` | `source="…"` | dataset id | Which dataset to display |
| `.datagrid` | `rows="…"` | number | Rows per page (0 = all) |
| `.datagrid` | `url` column | URL string | Hidden column; makes rows clickable links |
| `.chart` | `source="…"` | dataset id | Which dataset to plot |
| `.chart` | `type="…"` | `bar` · `line` | Chart type |
| `.chart` | `x="…"` | column name | Horizontal axis column |
| `.chart` | `y="…"` | column name | Vertical axis column |
| `.chart` | `title="…"` | string | Label above the chart |

## 🔗 Related components & examples

```
/components/datagrid
/components/chart
/components/query
/components/form
```
{: .related }

Browse the [🧩 component gallery](/components/) and [🔬 live examples](/components/examples).

