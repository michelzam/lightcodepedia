# 🗂️ Record

A **schema-driven record editor**: a typed form, a live preview you can edit
in place, and a **lossless YAML round-trip** — plus optional in-form AI and a
git commit. One engine renders any record; only the schema changes.

It stands on two libraries — `lcSchema` (schema → widgets) and `lcYaml`
(lossless round-trip) — and reuses `.dataset` for the schema and relation index,
so the engine carries **no domain vocabulary**.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 🛠️ How to make one

Three blocks: a **schema** (`.dataset`), an optional **relation index**
(`.dataset`), and the **record** itself, tagged `{: .record }`.

````markdown
```json
[ {"name":"title","label":"Name","widget":"string","wysiwyg":true},
  {"name":"tags","label":"Tags","widget":"list"},
  {"name":"era","label":"Era","widget":"relation","collection":"eras","multiple":true},
  {"name":"body","label":"Notes","widget":"text","rows":5,"wysiwyg":true} ]
```
{: .dataset #my_schema }

```json
{ "eras": [ {"slug":"belle-epoque","title":"Belle Époque"} ] }
```
{: .dataset #my_index }

```yaml
title: A. de Longpré
tags: [politician]
era: [belle-epoque]
body: président
```
{: .record schema="my_schema" index="my_index" }
````

The form is built from the schema; fields flagged `"wysiwyg": true` are also
editable directly on the rendered preview (click the name or the bio). The YAML
panel re-emits on every edit — **key order preserved, dates kept as strings,
faithful `|`/`|-`/`|+` chomping** — with a key-integrity check.

## 🎛️ Widgets

Set each field's `widget` in the schema:

| Widget | Renders | Notes |
|---|---|---|
| `string` | text input | |
| `text` | textarea | `rows` optional |
| `number` | numeric input | non-numeric reverts |
| `boolean` | checkbox | |
| `select` | dropdown | needs `options: [...]` |
| `list` | add/remove text rows | free strings |
| `relation` | autocomplete chips | needs `collection` (an index key); `multiple: true` for many |
| `object` | nested group | needs `fields: [...]` |
| `objectlist` | repeatable groups | needs `fields: [...]` |

## 🔧 Knobs

| Attribute | What it does |
|---|---|
| `schema="id"` | **Required.** A `.dataset` holding the schema array |
| `index="id"` | A `.dataset` holding the relation index `{ collection: [{slug,title}] }` |
| `ai="true"` | Show the in-form AI panel (Suggest → Apply / Ignore) |
| `endpoint="…"` | Default AI endpoint URL (the learner can override in the panel) |
| `commit="true"` | Show the git-commit panel (PAT from `edit_on_github`) |
| `path="…"` | Default repo path for the commit |
| `#id` | Optional — name the record for X-ray |

**Q:** Where does the parisrev vocabulary (professions, époques) live?

- [ ] Hardcoded in the `.record` engine.
- [x] In the author's `.dataset` schema + index blocks — the engine is domain-agnostic.
- [ ] In a special `parisrev.js` include.
- [ ] It doesn't; relations are typed by hand each time.
{: .quiz }

## 👀 Live example

A full Paris *Personnage* fiche — typed form, in-place preview, lossless YAML,
AI and commit:

[Open the Paris fiche example →](/components/examples/record)

## ⚠️ Limits worth knowing

- **In-place WYSIWYG** covers scalar fields flagged `wysiwyg` (name/bio); rich
  relations are edited in the form.
- **AI** posts `{record, schema}` to your endpoint and expects
  `{suggestions:[{text, field?, value?}]}`; with no endpoint a generic local
  fallback runs (no domain heuristics).
- **Commit** reuses `edit_on_github`'s PAT (`lc_ed_pat`) — editing needs no
  account; only the write does.
- **Map** for a record's geo points is a **separate step** — it will reuse
  `.map` fed by an adapter (the geo-extraction config is still being designed).

## 🔗 Related

```
/components/form
/components/map
/components/dataset
```
{: .related }
