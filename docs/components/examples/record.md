---
title: "Record editor — Paris fiche"
---

# 🗂️ Record editor — a Paris révolutionnaire fiche

A schema-driven [`.record`](/components/record) editor over real *Personnage* and
*Événement* fiches. Everything is **markdown + data** — the schema and the
relation index are plain `.dataset` blocks (here in **YAML**), so the engine
stays domain-agnostic; the parisrev vocab lives here, in the example.

Edit on the left (typed widgets, relation autocomplete), or click the **name**
and **bio** on the rendered card to edit in place. The **YAML** re-emits
losslessly — key order kept, dates as strings, faithful `|`/`|-`/`|+` blocks.
Try **🪄 Suggest** for the in-form AI, and open **💾 Commit** to write back.

## The schema (a YAML `.dataset`)

```yaml
- { name: title,         label: Nom affiché,  widget: string, wysiwyg: true }
- { name: gender,        label: Genre,        widget: select, options: ["", masculin, féminin, non-binaire, inconnu] }
- { name: professions,   label: Professions,  widget: list,   hint: vocabulaire contrôlé v1.3 }
- { name: nationalities, label: Nationalités, widget: list }
- { name: periods,       label: Époques,      widget: relation, collection: periods,   multiple: true }
- { name: themes,        label: Thèmes,       widget: relation, collection: themes,    multiple: true }
- { name: addresses,     label: Adresses,     widget: relation, collection: addresses, multiple: true }
- { name: body,          label: Bio,          widget: text, rows: 5, wysiwyg: true }
```
{: .dataset #paris_person_schema format="yaml" }

## The relation index (a YAML `.dataset`)

```yaml
periods:
  - { slug: revolution-francaise,  title: Révolution française }
  - { slug: revolutions-de-1848,   title: Révolutions de 1848 }
  - { slug: commune-de-1871,       title: Commune de 1871 }
  - { slug: second-empire,         title: Second Empire }
  - { slug: troisieme-republique,  title: Troisième République }
  - { slug: belle-epoque,          title: Belle Époque }
  - { slug: entre-deux-guerres,    title: Entre-deux-guerres }
persons:
  - { slug: albert-camus,         title: Albert Camus }
  - { slug: robert-desnos,        title: Robert Desnos }
  - { slug: paul-eluard,          title: Paul Éluard }
  - { slug: jules-supervielle,    title: Jules Supervielle }
  - { slug: roger-martin-du-gard, title: Roger Martin du Gard }
themes:
  - { slug: litterature,     title: Littérature }
  - { slug: arts-plastiques, title: Arts plastiques }
  - { slug: femmes-artistes, title: Femmes artistes }
  - { slug: montmartre,      title: Montmartre }
addresses:
  - { slug: 5-rue-sebastien-bottin,  title: 5 rue Sébastien-Bottin,  lat: 48.8557, lng: 2.3268 }
  - { slug: 12-rue-cortot,           title: 12 rue Cortot,           lat: 48.8869, lng: 2.3410 }
  - { slug: place-charles-de-gaulle, title: Place Charles-de-Gaulle, lat: 48.8738, lng: 2.2950 }
  - { slug: 24-rue-houdon,           title: 24 rue Houdon,           lat: 48.8836, lng: 2.3376 }
```
{: .dataset #paris_index format="yaml" }

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

## Same engine, a second type — an *Événement*

The **identical** `.record` engine over an *Événement* schema — reusing the same
`#paris_index`. This one exercises the nested widgets: `object` (datation),
`objectlist` (points), `number` (years), `boolean` (flags). Fields not in the
schema (`districts`, `bibliography`, `workflow`) are still **preserved** in the
YAML round-trip — check the integrity line.

```yaml
- { name: title, label: Titre, widget: string, wysiwyg: true }
- name: daterange
  label: Datation
  widget: object
  fields:
    - { name: startYear, label: Année de début, widget: number }
    - { name: endYear,   label: Année de fin,   widget: number }
    - { name: precision, label: Précision,      widget: select, options: [exact, month, year, circa, unknown] }
- name: location
  label: Localisation
  widget: object
  fields:
    - { name: ordered,     label: Itinéraire ordonné, widget: boolean }
    - { name: approximate, label: Approximatif,       widget: boolean }
    - name: points
      label: Point
      widget: objectlist
      fields:
        - { name: street,  label: Adresse,         widget: relation, collection: addresses }
        - { name: note,    label: Nom du lieu,     widget: string }
        - { name: primary, label: Point principal, widget: boolean }
- { name: epochs, label: Époques,     widget: relation, collection: periods, multiple: true }
- { name: themes, label: Thèmes,      widget: relation, collection: themes,  multiple: true }
- { name: people, label: Personnages, widget: relation, collection: persons, multiple: true }
- { name: body,   label: Corps,       widget: text, rows: 4, wysiwyg: true }
```
{: .dataset #paris_event_schema format="yaml" }

```yaml
id: 4eme-siege-de-la-maison-d-edition-gallimard
slug: 4eme-siege-de-la-maison-d-edition-gallimard
type: event
title: 4ème siège de la maison d'édition Gallimard
daterange:
  startYear: 1930
  endYear: 1945
  precision: year
location:
  ordered: false
  approximate: false
  points:
    - street: 5-rue-sebastien-bottin
      primary: true
      note: Siège de la maison d'édition Gallimard
epochs:
  - entre-deux-guerres
themes:
  - litterature
districts:
  - 7
people:
  - albert-camus
  - robert-desnos
  - paul-eluard
bibliography:
  - id: dictionnaire-historique-des-rues-de-paris-hillairet-jacques
    page: t2 p 584
externalLinks: []
body: ""
workflow:
  draft: false
  aiText: null
  edited: false
  validated: false
  reviewRequested: true
  reviewNote: Migré de l'export XWiki 2026-04-05 — à vérifier.
```
{: .record schema="paris_event_schema" index="paris_index" map="true" mapengine="leaflet" ai="true" }

```
/components/record
/components/form
/components/map
```
{: .related }
