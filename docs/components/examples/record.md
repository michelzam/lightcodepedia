---
title: "Record editor — Paris fiche"
---

# 🗂️ Record editor — a Paris révolutionnaire fiche

A schema-driven [`.record`](/components/record) editor over a real *Personnage*
fiche. Everything is **markdown + data** — the schema and the relation index are
plain `.dataset` blocks, so the engine stays domain-agnostic; the parisrev vocab
lives here, in the example.

Edit on the left (typed widgets, relation autocomplete), or click the **name**
and **bio** on the rendered card to edit in place. The **YAML** re-emits
losslessly — key order kept, dates as strings, faithful `|`/`|-`/`|+` blocks.
Try **🪄 Suggest** for the in-form AI, and open **💾 Commit** to write back (needs
a PAT via the ✏️ editor — editing itself needs no account).

## The schema (a `.dataset`)

```json
[
  { "name": "title", "label": "Nom affiché", "widget": "string", "wysiwyg": true },
  { "name": "gender", "label": "Genre", "widget": "select", "options": ["", "masculin", "féminin", "non-binaire", "inconnu"] },
  { "name": "professions", "label": "Professions / activités", "widget": "list", "hint": "vocabulaire contrôlé v1.3" },
  { "name": "nationalities", "label": "Nationalités", "widget": "list" },
  { "name": "periods", "label": "Époques", "widget": "relation", "collection": "periods", "multiple": true },
  { "name": "themes", "label": "Thèmes", "widget": "relation", "collection": "themes", "multiple": true },
  { "name": "addresses", "label": "Adresses", "widget": "relation", "collection": "addresses", "multiple": true },
  { "name": "body", "label": "Bio", "widget": "text", "rows": 5, "wysiwyg": true }
]
```
{: .dataset #paris_person_schema }

## The relation index (a `.dataset`)

```json
{
  "periods": [
    { "slug": "revolution-francaise", "title": "Révolution française" },
    { "slug": "revolutions-de-1848", "title": "Révolutions de 1848" },
    { "slug": "commune-de-1871", "title": "Commune de 1871" },
    { "slug": "second-empire", "title": "Second Empire" },
    { "slug": "troisieme-republique", "title": "Troisième République" },
    { "slug": "belle-epoque", "title": "Belle Époque" }
  ],
  "themes": [
    { "slug": "litterature", "title": "Littérature" },
    { "slug": "arts-plastiques", "title": "Arts plastiques" },
    { "slug": "femmes-artistes", "title": "Femmes artistes" },
    { "slug": "montmartre", "title": "Montmartre" }
  ],
  "addresses": [
    { "slug": "5-rue-sebastien-bottin", "title": "5 rue Sébastien-Bottin", "lat": 48.8557, "lng": 2.3268 },
    { "slug": "12-rue-cortot", "title": "12 rue Cortot", "lat": 48.8869, "lng": 2.3410 },
    { "slug": "place-charles-de-gaulle", "title": "Place Charles-de-Gaulle", "lat": 48.8738, "lng": 2.2950 },
    { "slug": "24-rue-houdon", "title": "24 rue Houdon", "lat": 48.8836, "lng": 2.3376 }
  ]
}
```
{: .dataset #paris_index }

## The fiche

```yaml
id: a-de-longpre
slug: a-de-longpre
type: person
title: A. de Longpré
sortName: Longpré, A. de
professions:
  - homme politique
nationalities:
  - France
periods:
  - revolutions-de-1848
themes: []
addresses:
  - 12-rue-cortot
  - 24-rue-houdon
bibliography: []
externalLinks: []
body: président
workflow:
  draft: false
  aiText: null
  edited: true
  validated: true
  reviewRequested: false
  reviewNote: Enrichi par IA (suggestions §7.2), revu et accepté.
entityType: person
gender: masculin
qualificatifs:
  - républicain
```
{: .record schema="paris_person_schema" index="paris_index" map="true" mapengine="leaflet" ai="true" commit="true" path="docs/paris/sample/a-de-longpre.yaml" }

*Add a type by adding a schema — no engine code. The same `.record` renders any
schema; only the `.dataset` blocks change.*

```
/components/record
/components/form
/components/map
```
{: .related }
