# 📊 Chart

Turn a CSV fenced block into a bar, line, or pie chart. No config files — data and options live right in the page.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
Dog,Speed
Husky,5
Shiny,3
Blaze,4
Misty,2
Rocket,6
Whisper,3
```
{: .chart type="bar" x="Dog" y="Speed" height="280" }

The bar color is a blue gradient — darker = faster. Edit the numbers and reload to see the chart update.

> This data comes straight from `tutorial101.yaml` → `charts.yaml`. Same dogs, same speeds.
> Ask yourself: "Which dog would you take for a sprint?"
{: .speaker-note }

**Q:** You change `Rocket`'s speed from 6 to 1. What changes in the chart?

- [x] Rocket's bar becomes the shortest and lightest blue.
- [ ] The chart crashes — it expects values in ascending order.
- [ ] Nothing — the chart is static HTML.
- [ ] Rocket disappears from the legend.
{: .quiz }

## 🛠️ How to make one

CSV in a fenced block, `{: .chart }` IAL on the next line:

````markdown
```
Dog,Speed
Husky,5
Shiny,3
```
{: .chart type="bar" x="Dog" y="Speed" }
````

First row = column headers. `x=` picks the label column, `y=` picks the value column.

**Q:** Your CSV has columns `Month`, `Sales`, `Profit`. You write `{: .chart x="Month" y="Profit" }`. What's on the X axis?

- [ ] Sales — it's the second column.
- [x] Month — `x=` maps to the label axis.
- [ ] Profit — it's the column with the highest values.
- [ ] The chart refuses to render because there are three columns.
{: .quiz }

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `type="bar"` | `bar` | Chart type: `bar`, `line`, `pie`, `doughnut` |
| `x="col"` | first column | Column to use as labels |
| `y="col"` | second column | Column to use as values |
| `height="N"` | `300` | Canvas height in pixels |
| `source="<id>"` | — | Bind to a dataset / query result by id — the chart redraws when that data changes |
| `master="<grid-id>"` | — | Follow another grid: redraw from the row selected in it (master → detail) |

**Line chart — same data:**

```
Dog,Speed
Husky,5
Shiny,3
Blaze,4
Misty,2
Rocket,6
Whisper,3
```
{: .chart type="line" x="Dog" y="Speed" height="240" }

**Pie chart:**

```
Type,Count
Labrador,12
Husky,8
Poodle,5
Other,15
```
{: .chart type="pie" x="Type" y="Count" height="260" }

**Q:** Which of these are TRUE about the chart widget? (Pick all that apply.)

- [x] The first row of the fenced block is always the header row.
- [x] `type="line"` and `type="bar"` both use the same CSV format.
- [ ] You must provide a `color=` attribute — there is no default palette.
- [x] `x=` and `y=` match column names from the header row.
{: .quiz multi="true" }

## 🏁 Final exam

**Q:** You want a doughnut chart of dog breed popularity. Which is correct?

- [ ] `{: .chart doughnut x="Breed" y="Count" }`
- [ ] `{: .chart kind="doughnut" }`
- [x] `{: .chart type="doughnut" x="Breed" y="Count" }`
- [ ] Doughnut is not supported — use `pie` and add a `hole=` attribute.
{: .quiz }

```gherkin
Feature: A data block becomes a chart
  As a lowcoder
  I want a fenced CSV block to render as a chart
  So that I can visualize data without config files or a server

  Scenario: The first block renders a bar chart canvas
    Given the bar chart at the top of this page
    :::python
    self.chart = Chart(Object._all(".lc-chart")[0]._el)
    :::
    When it has finished rendering
    Then it is a visible bar chart
    :::python
    assert self.chart.visible
    assert self.chart.type == "bar", self.chart.type
    :::
    And it drew a canvas to paint on
    :::python
    assert self.chart._q("canvas")._el is not None
    :::
```
{: .feature tags="data" }

## 🔗 Related components & examples

```
/components/dataset
/components/datagrid
/components/query
```
{: .related }

Browse the [🧩 component gallery](/components/) and [🔬 live examples](/components/examples).
