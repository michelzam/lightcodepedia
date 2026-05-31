# 📊 Datagrid

Sort, filter, and scroll through data — no Python, no server, no setup. Drop a YAML, JSON, or CSV block on the page and get a fully interactive table.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 Try it now

Click a column header to sort. Hover the **☰** icon to filter. Drag a column border to resize.

```yaml
- name: Lucky
  age: 3
  breed: Beagle
  adopted: true
- name: Wanda
  age: 5
  breed: Poodle
  adopted: true
- name: Max
  age: 2
  breed: Husky
  adopted: false
- name: Bella
  age: 4
  breed: Labrador
  adopted: true
```
{: .datagrid title="Shelter dogs" }

That's a live grid. Sort by age, filter to `adopted = true`, resize the breed column.

> Ask students to predict the sort order before clicking. Then: "what's the youngest dog?"
> The filter question — "show me only the adopted dogs" — always lands well.
{: .speaker-note }

**Q:** You want to see only the Poodles in the grid. Which control do you use?

- [ ] Click the column header twice to filter.
- [ ] Add `filter="true"` to the IAL[^ial].
- [x] Hover the **☰** icon on the Breed column header and type "Poodle".
- [ ] You can't filter — this is just a static HTML table with CSS tricks.
{: .quiz }

## 🛠️ How to make one

Write a YAML list of objects, then put `{: .datagrid }` on the very next line:

````markdown
```yaml
- name: Lucky
  age: 3
  breed: Beagle
- name: Wanda
  age: 5
  breed: Poodle
```
{: .datagrid }
````

Each object becomes a row; its keys become the column headers. Header labels are auto-prettified — `weight_kg` becomes **Weight Kg**.

## 🔧 Knobs

| Attribute | What it does |
|---|---|
| `id="…"` | Required when you have more than one grid on the same page |
| `title="…"` | Title bar shown above the grid |
| `height="400"` | Grid height in pixels (default 400) |
| `format="yaml"` | `yaml` (default), `json`, or `csv` |
| `editable="true"` | Double-click a cell to edit in place — see below |
| `detail-of="<id>"` | Filter this grid by the selected row in another grid — see below |
| `filter="<local>=<master>"` | Required with `detail-of`: which field to match |

**Q:** You have two grids on the same page and they're interfering with each other. What's missing?

- [ ] `format="yaml"` on both.
- [ ] A blank line between the two YAML blocks.
- [x] `id="…"` on each grid — required when more than one lives on a page.
- [ ] They can't coexist. One grid per page — site policy.
{: .quiz }

## 📋 Other data formats

The grid accepts JSON and CSV too — just tell it which with `format=`.

**JSON:**

```json
[
  {"city": "Tokyo",      "country": "Japan",  "population": 37400068},
  {"city": "Delhi",      "country": "India",  "population": 28514000},
  {"city": "Shanghai",   "country": "China",  "population": 25582000},
  {"city": "São Paulo",  "country": "Brazil", "population": 21650000},
  {"city": "Mexico City","country": "Mexico", "population": 21581000}
]
```
{: .datagrid format="json" title="World's largest cities" height="230" }

**CSV:** numbers are auto-coerced to numeric; empty cells stay empty.

```csv
name,age,breed,adopted
Lucky,3,Beagle,true
Wanda,5,Poodle,true
Max,2,Husky,false
Bella,4,Labrador,true
Charlie,1,Pug,false
```
{: .datagrid format="csv" title="Shelter dogs (CSV)" height="230" }

## ✏️ Editable cells

Add `editable="true"` and double-click any primitive cell to edit. Numbers stay numeric; booleans stay boolean. Changes are **in-memory only** — refresh discards them.

```yaml
- name: Lucky
  age: 3
  breed: Beagle
  adopted: true
- name: Wanda
  age: 5
  breed: Poodle
  adopted: true
- name: Max
  age: 2
  breed: Husky
  adopted: false
```
{: .datagrid id="editable-dogs" editable="true" height="200" }

When a [📝 Form](/components/form) is bound to this grid (`bound="editable-dogs"`), edits here repaint the form automatically.

## 🔗 Master/detail — two grids linked

`detail-of="<master-id>"` + `filter="<local-field>=<master-field>"` makes a detail grid that filters its rows by the row selected in the master. Click a city below — the dogs grid follows.

```json
[
  {"city": "Tokyo",   "country": "Japan",  "population": 37400068},
  {"city": "Delhi",   "country": "India",  "population": 28514000},
  {"city": "Shanghai","country": "China",  "population": 25582000},
  {"city": "São Paulo","country":"Brazil", "population": 21650000},
  {"city": "Mexico City","country":"Mexico","population": 21581000}
]
```
{: .datagrid id="md-cities" format="json" height="200" }

```json
[
  {"name":"Hachi",  "breed":"Akita",         "age":4,"city":"Tokyo"},
  {"name":"Sakura", "breed":"Shiba Inu",      "age":2,"city":"Tokyo"},
  {"name":"Raj",    "breed":"Pariah",         "age":3,"city":"Delhi"},
  {"name":"Priya",  "breed":"Mudhol Hound",   "age":5,"city":"Delhi"},
  {"name":"Bo",     "breed":"Chow Chow",      "age":6,"city":"Shanghai"},
  {"name":"Mei",    "breed":"Pekingese",      "age":1,"city":"Shanghai"},
  {"name":"Tito",   "breed":"Mutt",           "age":4,"city":"São Paulo"},
  {"name":"Coco",   "breed":"Xolo",           "age":3,"city":"Mexico City"},
  {"name":"Diego",  "breed":"Chihuahua",      "age":5,"city":"Mexico City"}
]
```
{: .datagrid id="md-dogs" format="json" detail-of="md-cities" filter="city=city" height="240" }

Deselect a city row (click again) and the full dog list returns.

**Filter syntax:** `filter="<local>=<master>"` — `filter="city=city"` means "show rows where *this* grid's `city` equals the *selected* row's `city`." Foreign key pattern: `filter="city_id=id"`.

> Walk through the filter rule carefully — the left side is always the detail grid's column, the right side is the master's column.
{: .speaker-note }

**Q:** You want a dogs grid to filter by the selected row of a cities grid with `id="cities"`. What attribute do you add to the dogs grid's IAL?

- [ ] `parent="cities"`
- [ ] `linked="cities"`
- [x] `detail-of="cities"` plus `filter="city=city"`
- [ ] `filter="cities"` — one attribute covers everything
{: .quiz }

## 📂 Loading from a repo file

Use `{% raw %}{% include datagrid_file.md path="…" %}{% endraw %}` to load a file that lives in the repo. The grid always shows the current content — no copy-paste needed when the file changes.

{% raw %}
```liquid
{% include datagrid_file.md path="data/cities.json" title="World cities" height="300" %}
```
{% endraw %}

Renders to:

{% include datagrid_file.md path="data/cities.json" title="World cities" height="300" %}

The *(live)* or *(cdn)* tag in the title bar shows which source the data came from.

### File-loader knobs

| Attribute | What it does |
|---|---|
| `path="…"` | Repo-relative path — format auto-inferred from `.csv`/`.json`/`.yaml` extension |
| `format="…"` | Override the inferred format |
| `title="…"` | Title bar — defaults to the path |
| `height="…"` | Pixel height — default 400 |
| `src="https://…"` | External URL escape hatch (bypasses repo/branch logic) |
| `repo="org/repo"` `branch="…"` | Override repo + branch (defaults: current site, `main`) |

## 🐍 From a Python runner — `show.grid()`

Every runner exposes a `show.grid(rows)` helper. Pass a list of dicts or objects and get a full datagrid below the output.

```python
dogs = yaml.load("""
- name: Lucky
  age: 3
  breed: Beagle
  weight_kg: 11.2
- name: Wanda
  age: 5
  breed: Poodle
  weight_kg: 7.8
- name: Max
  age: 2
  breed: Husky
  weight_kg: 24.5
""")
show.grid(dogs, title="Dogs from Python", height=220)
print(f"{len(dogs)} rows rendered.")
```
{: .run id="show-grid-demo" rows="16" }

## ⚠️ Limits worth knowing

- **Array of objects only.** Each item must be a dict (or have `__dict__`). A flat list of scalars won't work as columns.
- **All data loads at once.** Smooth up to ~10k rows in-browser; beyond that you'd want server-side pagination.
- **Edits are in-memory.** Refresh discards them. No persistence layer yet.
- **No column-type overrides.** Types are inferred from values by AG Grid[^ag-grid] — useful 95% of the time, but you can't yet force a column to be "date" or "currency".

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the datagrid? (Pick all that apply.)

- [x] YAML, JSON, and CSV are all supported with `format=`.
- [x] Editable changes are in-memory — refresh discards them.
- [ ] `detail-of=` works without a `filter=` attribute.
- [x] `show.grid(rows)` inside a Python runner renders a datagrid below the output.
- [ ] The grid supports server-side pagination by default.
{: .quiz multi="true" }

**Q:** It's demo day. Your grid has 5000 rows and your boss is watching. Will the datagrid handle it?

- [x] Yes — AG Grid virtualizes rows, so only visible ones hit the DOM. 5k is nothing.
- [ ] No — the 500-row hard limit kicks in and truncates silently.
- [ ] Maybe — depends on the browser's karma.
- [ ] Define "handle". It'll load. It'll also melt the laptop.
{: .quiz }

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class key="value" }` syntax, placed on its own line right after a block, attaches HTML attributes to that block. Every component on this site is activated this way.

[^ag-grid]: **AG Grid** — a high-performance open-source grid library (~300 KB JS + CSS) that powers the datagrid and form widgets. Loaded once from jsDelivr[^jsdelivr] and cached.

[^jsdelivr]: **jsDelivr** — a free, fast CDN (content-delivery network) that serves open-source npm packages from edge nodes worldwide. Used here for AG Grid and other JS libraries.
