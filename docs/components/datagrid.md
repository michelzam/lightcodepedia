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
- Read-only — no in-cell editing, no export buttons. Ask if you want one.

{% include backtotop.md %}
