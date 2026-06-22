# 📝 Form

Display a single object's attributes as a labeled two-column view. Pair it with a [📊 Datagrid](/components/datagrid) to drill into a selected row — click a row, the form fills. Works standalone too.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 Try it now

Here's a form showing one dog's full profile.

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
  phone: "555-0142"
notes: null
```
{: .form }

Notice how different types render differently: numbers in green, booleans as checkboxes, lists as pills, nested dicts as a labeled button (hover it for the full JSON), and `null` as an italic dash.

> Ask yourself: "What happens when you hover the Vet button?"
> Walk through each type rendering. The type-awareness is the point.
{: .speaker-note }

**Q:** Which value type renders as interactive pills?

- [ ] Strings — they're the most common.
- [x] Lists (arrays) — shown as compact pill tags.
- [ ] Booleans — click to toggle, so pills make sense.
- [ ] Nulls — empty pills for empty values.
{: .quiz }

## 🛠️ How to make one

Write a YAML block describing **one object** (not a list), then put `{: .form }` on the very next line:

````markdown
```yaml
name: Lucky
age: 3
breed: Beagle
```
{: .form }
````

Keys become the left-column labels (auto-prettified: `weight_kg` → **Weight Kg**). The title bar auto-picks the object's `name`, `title`, `label`, or `id` field — override with `title="…"`.

## 🔧 Knobs

| Attribute | What it does |
|---|---|
| `#id` | Optional — auto-assigned if omitted; add one only to reference this form from elsewhere |
| `title="…"` | Title bar — overrides the auto-inferred name/title/label/id |
| `format="yaml"` | `yaml` (default) or `json` |
| `bound="<grid-id>"` | Link to a datagrid — form fills when a row is selected |
| `editable="true"` | Make primitive fields editable — see below |

**Q:** You put two forms on a page and only one shows up. What did you forget?

- [ ] A `format="yaml"` on the second one.
- [ ] An `#id` on each form — otherwise only one shows.
- [x] Nothing — each form auto-gets a unique id and renders independently.
- [ ] To feed the page. It gets cranky when hungry.
{: .quiz }

## ✏️ Editable form — `editable="true"`

Add `editable="true"` and primitive fields become inputs. Click a string or number cell to edit. Booleans toggle via their checkbox with no extra step. Changes are **in-memory only** — refresh discards them.

```yaml
name: Lucky
age: 3
breed: Beagle
weight_kg: 11.2
adopted: true
```
{: .form editable="true" #edit_form_demo }

Numbers stay numeric — the editor rejects non-numeric input by reverting to the previous value. Lists and nested dicts stay read-only for now.

## 🔗 Linked to a datagrid — master/detail

An empty `{: .form bound="<id>" }` waits for a row to be clicked in the named datagrid, then fills itself with that row's data. The grid is the list view; the form is the detail view.

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
{: .datagrid #dogs height="200" }

```yaml
```
{: .form bound="dogs" }

Click a dog in the grid above — the form fills. Click another dog — the form updates. Click the same row again to deselect.

> Key selling point: order doesn't matter. The form can sit above the grid in the source
> and it still works — subscription is by id.
{: .speaker-note }

**Q:** You put the form above the datagrid in the markdown source. Does the binding still work?

- [ ] No — the form subscribes at render time, so it must come after the grid.
- [x] Yes — the form subscribes by id. Source order doesn't matter.
- [ ] Only if you add `order="after"` to the form's IAL.
- [ ] Depends on the browser. Safari is always the exception.
{: .quiz }

## ✏️🔗 Edit a grid row through the form

Combine `editable="true"` AND `bound="<id>"`: edits in the form flow back to the grid row immediately.

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
{: .datagrid #edit_md_dogs height="180" }

```yaml
```
{: .form bound="edit_md_dogs" editable="true" #edit_form_bound }

Click a dog, change a field in the form — the grid cell updates in place. If the grid is also `editable="true"`, double-clicking a grid cell repaints the form too.

## 📂 Loading from a repo file

`{% raw %}{% include form_file.md path="…" %}{% endraw %}` fetches a JSON or YAML file from the repo and renders it as a form — always showing the current file content.

{% raw %}
```liquid
{% include form_file.md path="data/lucky.json" %}
```
{% endraw %}

Renders to:

{% include form_file.md path="data/lucky.json" %}

### File-loader knobs

| Attribute | What it does |
|---|---|
| `path="…"` | Repo-relative path — format auto-inferred from `.json`/`.yaml`/`.yml` |
| `format="…"` | Override the inferred format |
| `title="…"` | Title bar — defaults to the path |
| `src="https://…"` | External URL escape hatch |
| `repo="org/repo"` `branch="…"` | Override repo + branch (defaults: current site, `main`) |

## 🐍 From a Python runner — `show.form()`

Every runner exposes a `show.form(obj)` helper alongside `show()` and `show.grid()`.

```python
class Dog:
    def __init__(self, name, age, breed, adopted):
        self.name = name
        self.age = age
        self.breed = breed
        self.adopted = adopted

lucky = Dog("Lucky", 3, "Beagle", True)
show.form(lucky)

show.form({
    "city": "Tokyo",
    "country": "Japan",
    "population": 37400068
}, title="Tokyo")
```
{: .run #show_form_demo rows="14" }

```python
show.form(obj, title=None)
```

- `obj` — a dict, or any object with `__dict__`. Other types are wrapped as `{'value': str(obj)}`.
- `title` — optional; defaults to `obj.name` / `obj.title` / `obj.label` / `obj.id` if present.

## ⚠️ Limits worth knowing

- **Single record only.** For lists, use `.datagrid`. They pair naturally: grid as overview, form as detail.
- **Lists and dicts are read-only** in v1. Editing a pill list or a nested dict needs richer UI — deferred.
- **Edits are in-memory.** Refresh discards them. No persistence layer yet.
- **No validation hooks.** Numbers reject non-numeric input; strings accept anything. Ask if you want `pattern=` / `min=` / `required=`.

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the form widget? (Pick all that apply.)

- [x] `bound="grid-id"` links the form to a datagrid by id.
- [x] Source order doesn't matter — a form above the grid still binds.
- [ ] `null` values render as empty strings.
- [x] `editable="true"` + `bound=` makes edits flow back to the grid row.
- [ ] Multiple forms can't bind to the same datagrid.
{: .quiz multi="true" }

**Q:** A student double-clicks a number cell in an editable form, types `"banana"`, and presses Enter. What happens?

- [ ] The cell turns red and shows a validation error.
- [x] The editor rejects the input and reverts to the previous number.
- [ ] `"banana"` is saved as a string — form doesn't care about types.
- [ ] The whole grid refreshes. Banana clears the cache.
{: .quiz }

[^ial]: **IAL (Inline Attribute List)** — kramdown's `{: .class key="value" }` syntax, placed on its own line right after a block, attaches HTML attributes to that block. See [✍️ Text](/components/text).
