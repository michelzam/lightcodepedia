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

## Databricks — a SQL statement on a warehouse

Apply `{: .dataset }` to a **SQL fence** with `dbx="<warehouse id>"`. The
statement runs on that warehouse through a same-origin proxy (`host=`, default
`/dbx`) that forwards **this browser's own token** and stores nothing. The
token is pasted once, in the bar under the fence, and lives on this device
like every other key here. Rows land on the bus like any dataset: grids,
charts, queries and proofs read them without knowing where they came from.

````markdown
```sql
SELECT region, SUM(arr_kusd) AS arr_kusd FROM finance.accounts GROUP BY region
```
{: .dataset #arr dbx="0123456789abcdef" }

[ARR by region](#)
{: .datagrid source="arr" #arr_grid height="200" }
````

The proxy is one block in the host's reverse proxy, no secret in it:

```nginx
location /dbx/ {
  proxy_pass https://<workspace>.cloud.databricks.com/;
  proxy_set_header Authorization $http_authorization;
}
```

Numeric columns arrive as numbers, results in chunks are followed to the
end, `refresh="60"` re-runs the statement every minute, and a refused token
says so in the bar instead of failing silently.

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
    self.ds: Dataset = self.page.monthly
    :::
    When a grid binds to it with source="monthly"
    :::python
    self.grid: Datagrid = self.page.monthly_grid
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
    self.trs: list = self.page.monthly_grid._qq("tbody tr")
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
{: .feature tags="data" status="passing"}

## Timestamps read on your clock

A cell holding a UTC stamp (`2026-09-09T01:43:04Z`) prints in the reader's local time; hover it for the UTC. A stamp with a zone offset (`2026-09-11T11:56:32.000-05:00`, the way GitHub dates an invitation) prints the same way, and the hover shows its UTC. The data keeps what it was given — only the printing changes, in grids and in the read-only fields of a card.

```json
[
  {"who":"zara","joined":"2026-09-04T18:05:49Z"},
  {"who":"ada","joined":"2026-09-09T01:43:04Z"},
  {"who":"Mike","joined":"2026-09-10T14:32:45Z"},
  {"who":"wassim","joined":"2026-09-11T11:56:32.000-05:00"}
]
```
{: .dataset #joins }

[Who joined when — opened in name order](#)
{: .datagrid source="joins" #joins_grid sort="who" }

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

## A list that writes back — a sheet, by its key

A link can also **take** rows. Write `key:<name>` instead of an address:
the real address of a sheet that takes writes is a key, so it lives on
the device, never in the page. The first time, the page asks for it in a
small field and keeps it. In Python, `append` adds one row: the row shows
at once, is sent to the sheet, and the sheet is read back.

````markdown
[the walk sheet](key:walk_sheet)
{: .dataset #walks }

[🐾 I walked a dog](#)
{: .button }
```python
button.page.walks.append({"dog": "Biscuit", "walker": "Ada", "at": weekday() + " " + clock()})
```
{: .onclick }
````

The sheet itself is any service that answers a GET with the rows (JSON
or CSV) and takes a POST of `{"append": {…}}`, a Google Sheet with a
small Apps Script web app for instance. Module 06's *Who Walked Whom*
uses one. `clock()` gives the time as a person writes it (`16:05`),
the way `weekday()` gives the day.

A list read from elsewhere is read again when the reader comes back to the
page (from the sheet's tab, say), on its grid's **↻**, and every N seconds
with `refresh="N"` on the dataset. A Google Sheet's own link
(`…/spreadsheets/d/<id>/edit…`) reads as rows when the sheet is shared
"anyone with the link can view"; writing still goes through its script.

A sentence can also read the **first** row of any list, not only count
them: **{= todos.first.title }** is the first todo above
(`{= todos.first.title }`).

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

## A few columns shown, the whole row published

`columns="topic, title"` on a bound grid shows those columns, in that order,
and nothing else — the row it publishes on a click is still the whole row.
So a narrow list can sit beside a card that reads every field.

```json
[
  {"topic":"Chipmaking","title":"India brings five new plants into production","summary":"Twelve projects approved, five producing.","quote":"We can jump ahead."},
  {"topic":"Diabetes","title":"Lilly wins approval for one dose each week","summary":"A weekly insulin shot.","quote":"Fewer injections."}
]
```
{: .dataset #stories_few }

[Two columns, click one](#)
{: .datagrid source="stories_few" #few_grid columns="topic, title" }

[The whole story](#)
{: .form master="few_grid" #few_card }

```gherkin
Feature: A grid shows a few columns and publishes the whole row
  As an author
  I want a narrow list beside a card that reads every field
  So that the list stays scannable and the detail stays complete

  Scenario: Only the named columns are drawn
    Given the grid with columns="topic, title"
    :::python
    self.grid: Datagrid = self.page.few_grid
    :::
    Then it draws two headers, in the order named
    :::python
    heads = [h._el.textContent.strip() for h in self.grid._qq("thead th")]
    assert heads == ["Topic", "Title"], heads
    :::

  Scenario: The published row keeps the hidden fields
    Given the grid and its bound card
    :::python
    self.trs: list = self.page.few_grid._qq("tbody tr")
    :::
    When I click the second row
    :::python
    self.trs[1]._el.click()
    :::
    Then the card holds the summary the grid never drew
    :::python
    card: Form = self.page.few_card
    assert card.data.summary == "A weekly insulin shot.", card.data.summary
    :::
```
{: .feature #columns_proof tags="data" visible="true" status="passing" }

## 🧥 A class as source — the list, dressed

A class **is** a dataset: its name is a dataset id. Say `source="<dataset>"`
on the class and the list's rows become its objects, the list's columns its
fields, nothing redeclared. The class adds what a list cannot say: a
**state**, and the **verbs** that move it.

```csv
family,dog,stage,since
Nguyen,Biscuit,asked,Tue
Diallo,Scout,met,Tue
Alvarez,Scout,home,Sat
```
{: .dataset #calls }

```python
class Family(Object, source="calls"):
    stage = State("asked", "met", "home")

    @transition("asked", "met")
    def meet(self):
        self.since = weekday()

    @transition("met", "home")
    def adopt(self):
        self.since = weekday()


class Foster(Family):
    until = Attr(str)

    def give_back(self):
        self.since = weekday()
```
{: .model }

[the families](#)
{: .datagrid source="Family" #family_grid }

[the family](#)
{: .form master="family_grid" #family_card }

Three things to see: the `stage` cell wears a **⌄** — click it, the verbs
this stage allows are live, the others grey and say what they need; a tap
on a row selects it (a row is always selected), and a **double click** on
another cell — or a second tap on the selected row — opens it for typing,
the old value selected, the edit going through the object
(`editable="false"` closes them); **➕ New** and **🗑 Delete** are there
without a line of yours, every object is born with them. A class with
subclasses on the page — `Foster(Family)` here — makes ➕ New a pick: a
Family or a Foster, and the new row is selected. A Foster's ⌄ carries its
own verb, *give back*, and its card its own field, *until*. `State("asked", "met", "home")` lists the stages in
order, `@transition("asked", "met")` goes from one to the other: no
brackets needed for one state. Click a row: the form shows the object, its state as a chip beside
the same verbs as buttons, the rest editable through the object. And the
class *is* the list: a cell counts **{= Family.count }** families, the
same **{= calls.count }** rows.

```gherkin
Feature: A class wears a dataset
  As a page author
  I want a class over my list, with a state and verbs, without redeclaring its columns
  So that a grid on the class refuses what the stage forbids and counts what the list counts

  Scenario: The rows are the objects, the columns their fields
    Given the dressed list
    :::python
    self.fam: Dataset = self.page.Family
    self.calls: Dataset = self.page.calls
    :::
    Then the class counts what the list counts
    :::python
    assert self.fam.count == self.calls.count == 3, (self.fam.count, self.calls.count)
    :::
    And a row is an object with the list's columns and the class's state
    :::python
    self.nguyen: Family = self.fam.row(family="Nguyen")
    assert self.nguyen.dog == "Biscuit" and self.nguyen.stage == "asked"
    :::

  Scenario: What the stage forbids is refused, in code as in the grid
    Given a fresh family, nobody met it yet
    :::python
    self.fam: Family = Family.new()
    self.fam.family = "Proof"
    assert self.fam.stage == "asked"
    :::
    When the dog is sent home too early
    :::python
    self.refused: str = ""
    try:
        self.fam.adopt()
    except PreconditionError as e:
        self.refused = str(e)
    :::
    Then the verb is refused and names the missing stage
    :::python
    assert "met" in self.refused, self.refused
    :::
    And after meeting, the list itself moved
    :::python
    self.fam.meet()
    assert self.page.calls.row(family="Proof")["stage"] == "met", "the class moved, the list did not"
    self.fam.delete()
    :::

  Scenario: Born verbs — the list grows and shrinks
    Given the families as they are
    :::python
    self.n: int = self.page.Family.count
    :::
    When one is added, then removed
    :::python
    self.fresh: Family = Family.new()
    assert self.page.calls.count == self.n + 1 and self.fresh.stage == "asked"
    self.fresh.delete()
    :::
    Then the count is back
    :::python
    assert self.page.Family.count == self.n == self.page.calls.count
    :::
```
{: .feature #class_source_proof visible="true" status="pending" tags="model" }

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
- A **relative** link (`[dogs](../module_00/dogs.yaml)`) names a file beside the page: the reader's own bench copy when they saved one, the page's repository copy otherwise — a pile declared by its file, no rows retyped.
- `source="id"` wires a view to the dataset; multiple views can share one dataset.
- `class X(Object, source="id")` makes the dataset a class: a grid on `X` dresses the same rows (see above).
- Click any **column header** to sort. Sorting persists through pagination.
- Add a **`url` column** to make rows clickable links.

## 🎛️ Knobs

| Block | Attribute | Values | What it does |
|---|---|---|---|
| `.dataset` | `#id` | snake_case | Registers data under this key |
| `.dataset` | _(applied to a link)_ | `https://…` href | Fetches JSON or CSV from the URL |
| `.dataset` | `dbx="…"` + `host="…"` | warehouse id, proxy root (default `/dbx`) | The fence is a SQL statement run on a Databricks warehouse with this device's token — see above |
| `.dataset` | `refresh="…"` | seconds (≥10) | Live mode: re-fetch on a timer (cache-busted); every bound grid/stat/chart repaints itself — no page reload |
| `.model` | `class X(Object, source="…")` | dataset id | The dataset's rows become X's objects, its columns X's fields; X adds a `State` and verbs — and X is a dataset id itself |
| `.datagrid` | `source="…"` | dataset id, or a class | Which dataset to display; a class dresses its rows: the state cell's ⌄ drops the row's verbs, typed cells, ➕ New |
| `.datagrid` | `rows="…"` | number | Rows per page (0 = all) |
| `.datagrid` | `columns="…"` | `a, b, c` | Draw only these columns, in this order; the published row is still whole (bound grids) |
| `.datagrid` | `height="…"` | px | A scrolling table with a sticky header instead of pages — wins over `rows` |
| `.datagrid` | `url` column | URL string | Hidden column; makes rows clickable links |
| `.datagrid` | UTC stamp cells | `…T…Z` strings | Print in the reader's local time, UTC on hover (data unchanged) |
| `.datagrid` | `sort="…"` | column name | The order the table opens in, ascending, words compared case-insensitively; a header click still re-sorts |
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


## 🧠 Quick check

**Q:** A `.dataset` block renders nothing on the page. Where did your data go?

- [x] Registered in memory under its `#id` — invisible isn't gone; grids and charts read it.
- [ ] It evaporated. Data is a gas at room temperature.
- [ ] Hiding behind the chart. It's shy around strangers.
- [ ] You forgot to feed it. Hungry datasets sulk and hide.
{: .quiz }

## Reading rows in a check

`count` says how many; `values("field")` says what is in them — so a
proof can assert on content, not just size. Missing values read as `""`.

```csv
family,dog,met
Nguyen,Biscuit,
Alvarez,Scout,Wed
Kaur,Scout,
```
{: .dataset #visits }

```sql
SELECT family, met FROM visits WHERE met = ''
```
{: .query bind="visits" #waiting }

[Still waiting](#)
{: .datagrid source="waiting" rows="5" title="Waiting for a visit" }

```gherkin
Feature: A check can read the rows, not just count them
  Scenario: The filtered pile holds only families still waiting
    Given the question and its answer
    :::python
    self.all: Dataset = self.page.visits
    self.waiting: Query = self.page.waiting
    :::
    Then nobody who already met a dog is in the answer
    :::python
    assert self.all.count == 3, self.all.count
    assert self.waiting.count == 2, self.waiting.count
    mets: list[str] = self.waiting.values("met")
    names: list[str] = self.waiting.values("family")
    bad: list[str] = [n for n, m in zip(names, mets) if m]
    assert not bad, "already met: " + str(bad)
    assert "Nguyen" in names, names
    :::
```
{: .feature #values_proof tags="data" visible="true" status="passing" }

[^dataset]: **dataset** — a pile of rows registered under an `#id`. It
    renders nothing; the faces that name it do.

[^query]: **query** — a question asked of a pile in SQL. Its answer is a
    pile of its own, re-asked whenever an input changes.
