# 📝 Form

Display a single object's attributes as a labeled card. Read-only in v1. Bind it to a [📊 Datagrid](/components/datagrid) by id and it auto-populates with the selected row (master/detail).

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

Type-aware formatting: booleans as **✓ true** / **✗ false**, numbers in green, `null` as italic em-dash, nested objects and lists pretty-printed as JSON.

The title bar auto-picks `name` (then `title`, then `label`, then `id`) from the object — override with `title="..."`.

## Knobs

| Attribute | Description |
|---|---|
| `id="..."` | Required if you have multiple forms on the same page |
| `title="..."` | Title bar (overrides the auto-inferred `name`/`title`/`label`/`id`) |
| `format="yaml"` | `yaml` (default) or `json` |
| `bound="<grid-id>"` | Master/detail — see below |

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

- **Read-only.** Editing is on the wishlist — would land as `editable="true"`, with type-inferred inputs and two-way binding back to the underlying object.
- **Single record only.** For lists, use `.datagrid`. The widgets pair naturally — datagrid as overview, form as detail.
- **Nested objects / arrays** are pretty-printed as JSON. Recursive subform rendering is doable later if you want it.

{% include backtotop.md %}
