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
| `id="..."` | Required if you have multiple grids on the same page (also required to bind a form or a detail grid) |
| `title="..."` | Optional title bar above the grid |
| `height="400"` | Grid height in pixels (default 400) |
| `format="yaml"` | `yaml` (default), `json`, or `csv` |
| `editable="true"` | Cells editable on double-click — see below |
| `detail-of="<id>"` | Filter this grid by selection in another grid — see below |
| `filter="<local>=<master>"` | Required with `detail-of`. Filter rule: row in this grid matches the master row's field. |

Headers are auto-prettified — `weight_kg` becomes **Weight Kg**. Booleans render as **True** / **False** (Python style).

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

## Loading from a repo file — `{% raw %}{% include datagrid_file.md path="..." %}{% endraw %}`

Same pattern as `code_file.md`: live raw URL by default for fast feedback, jsDelivr CDN when published on the canonical host or with `?cdn=1`. Format auto-inferred from the extension.

{% raw %}
```liquid
{% include datagrid_file.md path="data/cities.json" title="World's largest cities" height="350" %}
```
{% endraw %}

Renders to:

{% include datagrid_file.md path="data/cities.json" title="World's largest cities" height="350" %}

The mode (`live` / `cdn`) is shown in italics in the title bar — so you can see which copy you're looking at.

### Knobs (file form)

| Attribute | Description |
|---|---|
| `path="..."` | Repo-relative path. Format auto-inferred from `.csv`/`.json`/`.yaml` extension |
| `format="..."` | Override the inferred format (rare) |
| `title="..."` | Title bar — defaults to the path |
| `height="..."` | Pixel height — default 400 |
| `src="https://..."` | Escape hatch for an external URL (skips repo/branch logic) |
| `repo="org/repo"` `branch="..."` | Override repo + branch (default: current site, `main`) |

A CSV example from the repo:

{% include datagrid_file.md path="data/dogs.csv" title="Shelter dogs" height="300" %}

## Editable cells — `editable="true"`

Double-click a cell to edit. Enter commits, Esc cancels. Edits update the underlying row in memory; any [📝 Form](/components/form) bound to this grid via `bound=` repaints with the new value.

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

Numbers stay numeric (sorting is correct), booleans stay boolean. Changes are local to the browser session — refresh discards them.

## Grid-to-grid master/detail — `detail-of=` + `filter=`

A detail grid filters its rows by the row currently selected in a master grid. The relationship is **cities ➜ dogs**: click a city, see only the dogs in that city.

{% raw %}
````markdown
```json
[
  {"city": "Tokyo", "country": "Japan", "population": 37400068},
  {"city": "Delhi", "country": "India", "population": 28514000},
  {"city": "Shanghai", "country": "China", "population": 25582000}
]
```
{: .datagrid id="md-cities" format="json" height="180" }

```json
[
  {"name": "Hachi", "breed": "Akita", "city": "Tokyo"},
  {"name": "Sakura", "breed": "Shiba Inu", "city": "Tokyo"},
  {"name": "Raj", "breed": "Pariah", "city": "Delhi"}
]
```
{: .datagrid id="md-dogs" format="json" detail-of="md-cities" filter="city=city" height="200" }
````
{% endraw %}

Renders to:

```json
[
  {"city": "Tokyo", "country": "Japan", "population": 37400068},
  {"city": "Delhi", "country": "India", "population": 28514000},
  {"city": "Shanghai", "country": "China", "population": 25582000},
  {"city": "São Paulo", "country": "Brazil", "population": 21650000},
  {"city": "Mexico City", "country": "Mexico", "population": 21581000}
]
```
{: .datagrid id="md-cities" format="json" height="180" }

```json
[
  {"name": "Hachi", "breed": "Akita", "age": 4, "city": "Tokyo"},
  {"name": "Sakura", "breed": "Shiba Inu", "age": 2, "city": "Tokyo"},
  {"name": "Raj", "breed": "Pariah", "age": 3, "city": "Delhi"},
  {"name": "Priya", "breed": "Mudhol Hound", "age": 5, "city": "Delhi"},
  {"name": "Bo", "breed": "Chow Chow", "age": 6, "city": "Shanghai"},
  {"name": "Mei", "breed": "Pekingese", "age": 1, "city": "Shanghai"},
  {"name": "Tito", "breed": "Mutt", "age": 4, "city": "São Paulo"},
  {"name": "Coco", "breed": "Xolo", "age": 3, "city": "Mexico City"},
  {"name": "Diego", "breed": "Chihuahua", "age": 5, "city": "Mexico City"}
]
```
{: .datagrid id="md-dogs" format="json" detail-of="md-cities" filter="city=city" height="240" }

Click a city above. The dogs grid below filters to that city's dogs. Deselect (click again) and the full list returns.

**The filter syntax:** `filter="<local-field>=<master-field>"`. So `filter="city=city"` means "show rows where this grid's `city` column equals the selected master row's `city` column." If you have a `city_id` foreign key linking to a master with an `id` column, you'd write `filter="city_id=id"`.

You can chain forms onto this too — bind a form to `md-dogs` and you get a three-level master/detail/detail view.

## From inside a Python runner — `show.grid(rows)`

Every runner exposes a `show.grid(rows)` helper alongside `show()`. Pass a list of dicts (or objects with `__dict__`) and a full-width datagrid appears in the cards area below the output.

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
- name: Bella
  age: 4
  breed: Labrador
  weight_kg: 28.0
- name: Charlie
  age: 1
  breed: Pug
  weight_kg: 8.3
""")

show.grid(dogs, title="My dogs", height=260)
print(f"Showed {len(dogs)} dogs in the grid.")
```
{: .run id="show-grid-demo" rows="18" }

Works with custom classes too — `show.grid` reads `__dict__`:

```python
class Pet:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

pets = [
    Pet("Lucky", 3, "Beagle"),
    Pet("Wanda", 5, "Poodle"),
    Pet("Max", 2, "Husky"),
]
show.grid(pets, title="Pets (from objects)")
```
{: .run id="show-grid-objects" rows="13" }

### `show.grid` signature

```python
show.grid(rows, title=None, height=300)
```

- `rows` — iterable of dicts. Non-dict items are auto-converted via `__dict__`; failing that, wrapped as `{'value': str(r)}`.
- `title` — optional title bar above the grid.
- `height` — pixel height of the grid (default 300).

## Limitations of v1

- Data must be an **array of objects** (keys become columns).
- All data loads at once; no server-side pagination. Works smoothly up to ~10k rows in-browser.
- Column types inferred by AG Grid from the values; no explicit per-column overrides yet.
- Editable mode is in-memory only — refresh discards changes. No persistence layer yet.
- No CSV/Excel export buttons yet. Ask if you want them.

{% include backtotop.md %}
