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
| `source="<id>"` | — | Bind to a dataset / query result by id — the chart redraws when that data changes. A name nothing answers to rests on `empty=`; an **empty** name (`source=""`, a knob cleared in the ⚙️) keeps the box, says so, and keeps its gear |
| `master="<grid-id>"` | — | Follow another grid: redraw from the row selected in it (master → detail) |
| `marks="col"` | — | Rows whose value is set become diamonds — a key point, its text on hover |
| `hover="col"` | — | Extra text on every point's hover |
| `labels="col"` | — | The row's short text printed above its point — read without a hover, a note's emoji |
| `top="col"` | — | A band of text above the plot, one cell per column — a stage's title; the cell holds what fits, hover for all of it |
| `bottom="col"` | — | A band under the x labels, one cell per column — the touchpoints. A cell's ` · `-separated items are **chips, one per line** (up to four), so three tools stay legible |
| `color="col"` | — | The row's own colour for its point, a CSS colour — a tone per row |
| `dips="col"` | — | The valley before the summit: when the row's value is above zero the line first dives to minus that value (a red ✗), then climbs to the point — a journey map's negative experiences on the way to a positive one |
| `trail="col"` | — | The row's beats in time order, a string of ✗ ✓ and ? — beads around the point, ✗ below the axis (one deeper for each red in a row), ✓ above, ? on the axis (a question asked), the line threading them; the last run is the point; a row with a trail ignores `dips=` |
| `title="… [col] …"` | — | A title may hold `[col]` placeholders, filled from the first row drawn — a name over a map that follows a master (square brackets: the markdown keeps braces for itself) |
| `hints="y: … \| bars: … \| x: … \| top: … \| bottom: … \| dips: … \| trail: …"` | — | What a hover says about each part of the chart, in the page's words — the grid's `hints=` word and syntax |

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

## 🗺 A journey map: the story above and below the line

A customer journey map draws experiences over time, positive above the axis
and negative below, with the stages named above and the touchpoints below.
The line chart draws that in three bands: `top=` the stage's title, the line
in the middle with `dips=` for the setbacks met before each point, `bottom=`
the touchpoints as chips, and `hints=` so every part explains itself on hover.

```json
[
  {"stage":"1 research","title":"🔍 Researching","mood":1,"setbacks":0,"minutes":20,"touch":"web · dealer","tone":"#86efac"},
  {"stage":"2 finance","title":"💳 Financing","mood":1,"setbacks":2,"runs":"✗?✓✗✓","minutes":45,"touch":"dealer · bank · phone","tone":"#15803d"},
  {"stage":"3 wait","title":"⏳ Waiting","mood":-1,"setbacks":0,"minutes":5,"touch":"email","tone":"#dc2626"},
  {"stage":"4 ride","title":"🚗 First ride","mood":1,"setbacks":0,"minutes":60,"touch":"car","tone":"#86efac"}
]
```
{: .dataset #car_journey }

[Car purchase](#)
{: .chart #car_journey_chart bind="car_journey" type="line" x="stage" y="mood" bars="minutes" dips="setbacks" trail="runs" top="title" bottom="touch" color="tone" height="220" title="🚗 [title] and after" hints="trail: one visit, in order — ✗ it went wrong, ✓ it went well | y: the experience — above the line it went well, below it did not | bars: minutes spent at this stage, on the right scale | x: the stage, in order | top: the stage as the customer names it | bottom: who or what the customer touched here | dips: setbacks met before this stage turned out well" }

Financing carries its beats (`trail="runs"`, ✗?✓✗✓): a refusal, a question
to the bank, an offer, a refusal, the offer that held — a sawtooth before the
point, the question on the axis, where a plain `dips=` would show one dive.
Waiting stays below the axis. The title names the first stage drawn
(`[title]`). Hover any bead, tick, chip or title: it says what it measures.
Every column is addressable — its title above as `<chart>__top__<x>`, its
chips below as `<chart>__chips__<x>` — so a guide's `at:` can walk the map
page by page.

In Python, the map reads itself — the title, the columns, and per column the
beads, the chips and the point's tone:

```gherkin
Feature: A journey map reads itself in Python
  As a page author
  I want to ask the chart what it drew, column by column
  So that a proof speaks the page's words, never a selector

  Scenario: Financing's beats, chips and tone
    Given the car journey map
    :::python
    self.map: Chart = self.page.car_journey_chart
    :::
    Then its title names the first stage
    :::python
    assert self.map.title == "🚗 🔍 Researching and after", self.map.title
    assert self.map.xs == ["1 research", "2 finance", "3 wait", "4 ride"], self.map.xs
    :::
    And financing shows its beats before the point, its chips below, and a dark green point
    :::python
    assert self.map.beads("2 finance") == ["✗", "?", "✓", "✗"], self.map.beads("2 finance")
    assert self.map.chips("2 finance") == ["dealer", "bank", "phone"], self.map.chips("2 finance")
    assert self.map.tone("2 finance") == "#15803d" and self.map.tone("3 wait") == "#dc2626"
    :::
```
{: .feature #car_journey_proof tags="chart" status="pending" }

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
    self.chart: Chart = Chart(Object._all(".lc-chart")[0]._el)
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
{: .feature tags="data" status="passing"}

## 🔗 Related components & examples

```
/components/dataset
/components/datagrid
/components/query
```
{: .related }

Browse the [🧩 component gallery](/components/) and [🔬 live examples](/components/examples).

## 📈 A line that follows a grid, with bars, key points and series

A dataset-bound line can ride the master/detail road a detail grid rides —
`master="grid-id" filter="col=col"` — and carry more than one measure:
`bars="col"` draws a second measure as bars behind the line, `marks="col"`
turns the rows whose value is set into diamonds (hover for the text),
`hover="col"` adds a line to every point's hover, and `series="col"` draws
one line per value: with a master, the selected one in blue, the others grey.

```json
[
  {"who":"ada","day":"2026-09-04","points":0,"saves":1,"mark":"🛠 bench forged","notes":""},
  {"who":"ada","day":"2026-09-06","points":3,"saves":2,"mark":"✍️ first save","notes":"cv.md; dogs.yaml"},
  {"who":"ada","day":"2026-09-10","points":4,"saves":1,"mark":"","notes":"cv.md"},
  {"who":"bo","day":"2026-09-05","points":1,"saves":1,"mark":"✍️ first save","notes":"cv.md"},
  {"who":"bo","day":"2026-09-11","points":2,"saves":3,"mark":"last save","notes":"cv.md; dogs.yaml; notes.md"}
]
```
{: .dataset #days }

```json
[
  {"who":"ada","name":"Ada Lovelace"},
  {"who":"bo","name":"Bo Diddley"}
]
```
{: .dataset #crew }

[Pick a learner](#)
{: .datagrid source="crew" #crew_grid }

[Their days](#)
{: .chart #days_chart bind="days" type="line" x="day" y="points" bars="saves" marks="mark" hover="notes" master="crew_grid" filter="who=who" height="220" title="📈 One learner — points, saves, key points" empty="Pick a learner above." }

[Everyone](#)
{: .chart #crew_chart bind="days" type="line" x="day" y="points" series="who" master="crew_grid" filter="who=who" height="200" title="📈 Everyone — the picked one in blue" }
