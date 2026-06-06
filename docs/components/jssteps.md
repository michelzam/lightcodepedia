---
---
# 🧪 JsSteps

In-browser BDD step runner powered by MicroPython WASM. Write `@scenario` functions in a fenced Python block — they run live in the page, with access to every component via `self.page`.

Two built-in scenarios run automatically on every suite:
- **"component ids are unique"** — enforces that `self.page.<id>` is unambiguous
- **"component ids are python compatible"** — enforces that every id, after hyphen→underscore substitution, is a valid Python identifier (so `self.page.<name>` can always reach it)

## Live example

The dataset and grid below have ids. The step suite below them tests both.

```json
[
  {"name":"Alice","score":92},
  {"name":"Bob","score":78},
  {"name":"Carol","score":88}
]
```
{: .dataset id="jss-data" }

[Sample grid](#)
{: .datagrid bind="jss-data" id="jss-grid" rows="5" }

```python
@scenario("jss-data dataset is loaded and has 3 rows")
def check_dataset(self):
    ds = Dataset("jss-data")
    assert ds.loaded, "dataset not registered"
    assert ds.count == 3, f"expected 3 rows, got {ds.count}"

@scenario("jss-grid renders all rows")
def check_grid_rows(self):
    grid = self.page.jss_grid
    assert grid.exists,         "jss-grid not found — did you set id=\"jss-grid\"?"
    assert grid.row_count == 3, f"expected 3 rows, got {grid.row_count}"

@scenario("jss-grid headers are name and score")
def check_grid_headers(self):
    headers = self.page.jss_grid.headers
    assert "name"  in headers, f"missing 'name' column, got {headers}"
    assert "score" in headers, f"missing 'score' column, got {headers}"

@scenario("clicking the name header re-sorts")
def check_sort(self):
    grid = self.page.jss_grid
    grid.header("name").click()
    first = grid.rows[0]["name"]
    assert first == "Alice", f"expected Alice first after sort, got {first}"
```
{: .jssteps }

## 🥸 How to write one

````markdown
```python
@scenario("grid has rows")
def check_rows(self):
    grid = self.page.my_grid       # resolves via id="my_grid" on the component
    assert grid.row_count > 0

@scenario("dataset is loaded")
def check_ds(self):
    ds = Dataset("my-data")        # accesses window.lcDatasets directly
    assert ds.loaded
    assert ds.count == 6
```
{: .jssteps }
````

- `self.page.<name>` resolves any component with `id="<name>"` on the page. Underscores in the Python attribute are mapped to hyphens in the id, so `self.page.jss_grid` finds `id="jss-grid"`.
- No id → not accessible. The built-in scenarios will pass (no duplicate/invalid ids), but accessing an unnamed component raises `AttributeError`.
- `Dataset("id")` reaches the data registry directly — no DOM id needed.
- Scenarios run **synchronously** in MicroPython WASM. Async steps are not yet supported.

## 🎛️ The `lc` module (injected preamble)

These classes are available in every `.jssteps` block without any import:

| Class | Key members |
|---|---|
| `Object` | `exists`, `visible`, `text`, `attr(name)`, `has_class(name)`, `q(css)`, `qq(css)`, `click()` |
| `Page` | `self.page.<id>` → component; `feature(n)`, `features()` |
| `Dataset(id)` | `loaded`, `count` |
| `Datagrid(Object)` | `row_count`, `headers`, `rows`, `header(name)` |
| `Chart(Object)` | `bar_count`, `point_count` |
| `FeatureCard(Object)` | `title`, `status`, `run_button` |
| `scenario(label)` | decorator — registers a scenario function |

## Notes

- First run loads the MicroPython WASM binary (~300 KB); subsequent runs reuse the same instance.
- Components need `id="…"` in their IAL to be reachable via `self.page`. The id is propagated to `data-lc-id` on the rendered wrapper.
- Remote datasets (`.dataset` on a link) must have finished fetching before the step runs — place `.jssteps` after the datagrid in the page source.
