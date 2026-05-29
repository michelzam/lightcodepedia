# 📝 Form

Display (and optionally edit) a single object's attributes. Rendered as a 2-column AG Grid under the hood — same look and feel as [📊 Datagrid](/components/datagrid), with a pinned label column on the left and a value column on the right. Bind it to a datagrid by id and it auto-populates with the selected row (master/detail).

## The data contract

Across `.form`, `.datagrid`, `show.form()`, and `show.grid()`, the universal data shape is:

- **`.form`** consumes **one object** — a dict, a YAML mapping, a JSON object, a Python class instance (via `__dict__`).
- **`.datagrid`** consumes **a list of those objects**.

YAML / JSON / Python dicts / Python class instances all flatten to the same thing — a dict with string keys. The widgets don't care which source you used.

## Tiniest form — `{: .form }` on a YAML fence

Drop `{: .form }` on the line right after a YAML/JSON block describing **one** object.

{% raw %}
````markdown
```yaml
name: Lucky
age: 3
breed: Beagle
weight_kg: 11.2
adopted: true
favorite_toys:
  - squeaky bone
  - tennis ball
vet:
  name: Dr. Patel
  phone: 555-0142
notes: null
```
{: .form }
````
{% endraw %}

Renders to:

```yaml
name: Lucky
age: 3
breed: Beagle
weight_kg: 11.2
adopted: true
favorite_toys:
  - squeaky bone
  - tennis ball
vet:
  name: Dr. Patel
  phone: 555-0142
notes: null
```
{: .form }

Type-aware formatting: booleans as **✓ True** / **✗ False** (Python-style), numbers in green, `null` as italic em-dash, nested objects and lists pretty-printed as JSON. Attribute labels are auto-prettified — `weight_kg` becomes **Weight Kg**, `favorite_toys` becomes **Favorite Toys**.

The title bar auto-picks `name` (then `title`, then `label`, then `id`) from the object — override with `title="..."`.

## Knobs

| Attribute | Description |
|---|---|
| `id="..."` | Required if you have multiple forms on the same page |
| `title="..."` | Title bar (overrides the auto-inferred `name`/`title`/`label`/`id`) |
| `format="yaml"` | `yaml` (default) or `json` |
| `bound="<grid-id>"` | Master/detail — see below |
| `editable="true"` | Each primitive field becomes an input — see below |

## Editable form — `editable="true"`

Single-click any value cell to edit. AG Grid picks the right editor based on the value's type — `agTextCellEditor` for strings, `agNumberCellEditor` for numbers, `agCheckboxCellEditor` for booleans. Edits update the underlying object **in memory** — refresh discards them.

```yaml
name: Lucky
age: 3
breed: Beagle
weight_kg: 11.2
adopted: true
```
{: .form editable="true" id="edit-form-demo" }

Numbers stay numeric (so the back-end value is `3`, not `"3"`). Booleans use AG Grid's checkbox editor — single-click the cell, click the checkbox to toggle, click away to commit. Nested objects and arrays stay read-only — those need richer editors, deferred.

### Combined with `bound=` — edit a row via the form

When `editable="true"` AND `bound="<grid-id>"`, edits flow back to the grid: the row repaints with the new value.

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
{: .datagrid id="edit-md-dogs" height="180" }

```yaml
```
{: .form bound="edit-md-dogs" editable="true" }

Click a dog, edit any field in the form — the grid updates in place. Conversely, if the grid is also editable (`editable="true"` on the datagrid), double-click a cell and watch the form repaint with the new value.

## Master/detail — `bound="<grid-id>"`

The killer feature: an empty `.form` on the same page as a `.datagrid` auto-fills with the selected row.

{% raw %}
````markdown
```yaml
- name: Lucky
  age: 3
  breed: Beagle
  weight_kg: 11.2
  adopted: true
- name: Wanda
  age: 5
  breed: Poodle
  weight_kg: 7.8
  adopted: true
- name: Max
  age: 2
  breed: Husky
  weight_kg: 24.5
  adopted: false
```
{: .datagrid id="dogs" height="220" }

```yaml
```
{: .form bound="dogs" }
````
{% endraw %}

Renders to:

```yaml
- name: Lucky
  age: 3
  breed: Beagle
  weight_kg: 11.2
  adopted: true
- name: Wanda
  age: 5
  breed: Poodle
  weight_kg: 7.8
  adopted: true
- name: Max
  age: 2
  breed: Husky
  weight_kg: 24.5
  adopted: false
```
{: .datagrid id="dogs" height="220" }

```yaml
```
{: .form bound="dogs" }

Click a row in the grid — the form below repaints. The title bar updates to the row's `name`.

**Mechanics:** the grid publishes its selected row on a tiny pub/sub keyed by id (`window.lcMasterDetail`). Forms subscribe by id at upgrade time. Order on the page doesn't matter (you can put the form first), and multiple forms can bind to the same grid.

A second form bound to the same grid, just to demonstrate independence:

```yaml
```
{: .form bound="dogs" title="(same selection, different form)" }

## Loading from a repo file — `{% raw %}{% include form_file.md path="..." %}{% endraw %}`

Same raw / jsDelivr pattern as the datagrid file loader.

{% raw %}
```liquid
{% include form_file.md path="data/lucky.json" %}
```
{% endraw %}

Renders to:

{% include form_file.md path="data/lucky.json" %}

### Knobs (file form)

| Attribute | Description |
|---|---|
| `path="..."` | Repo-relative path. Format auto-inferred from `.json`/`.yaml`/`.yml` |
| `format="..."` | Override the inferred format |
| `title="..."` | Title bar — defaults to the path |
| `src="https://..."` | Escape hatch for an external URL |
| `repo="org/repo"` `branch="..."` | Override repo + branch (default: current site, `main`) |

## From inside a Python runner — `show.form(obj)`

Like `show.grid()`, but for a single record.

```python
class Dog:
    def __init__(self, name, age, breed, adopted):
        self.name = name
        self.age = age
        self.breed = breed
        self.adopted = adopted

lucky = Dog("Lucky", 3, "Beagle", True)
show.form(lucky)

# from a dict
show.form({
    "city": "Tokyo",
    "country": "Japan",
    "population": 37400068
}, title="Tokyo")
```
{: .run id="show-form-demo" rows="14" }

### `show.form` signature

```python
show.form(obj, title=None)
```

- `obj` — a dict, or any object with `__dict__`. Other types are wrapped as `{'value': str(obj)}`.
- `title` — optional title bar. Defaults to `obj.name` / `obj.title` / `obj.label` / `obj.id` if present, otherwise "Form".

## Limitations of v1

- **Single record only.** For lists, use `.datagrid`. The widgets pair naturally — datagrid as overview, form as detail.
- **Nested objects / arrays** are pretty-printed as JSON and stay read-only in editable mode. Recursive subform rendering is doable later.
- **Edits are in-memory only.** Refresh discards them. No persistence layer yet.
- **No validation hooks yet.** A number input accepts any number; a text input accepts any string. Ask if you want `pattern=` / `min=` / `required=`.

{% include backtotop.md %}
