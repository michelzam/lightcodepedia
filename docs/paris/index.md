---
title: Éditeur de fiches — démo pour Toni
---

# Paris révolutionnaire — éditeur de fiches (démo pour Toni)

Cette page ne contient **aucun code moteur** : elle **consomme le composant `[.record](/components/record)`**
(le même que la bibliothèque LightCode), nourri par un **schéma** et un **index** en simples blocs `.dataset`
— **en YAML**, comme le corpus. Le moteur reste **agnostique du domaine** ; le vocabulaire parisrev vit ici.

**Rien à installer, aucun compte.** Les 4 composants à valider — dis-nous, pour chacun : *convient / à ajuster / non* :

1. **Formulaire piloté par schéma** — vocabulaire fermé, relations par nom, objets imbriqués, liste d'objets.
2. **Aperçu + WYSIWYG en place** — clique le **nom** ou la **bio** sur la fiche rendue.
3. **Carte** — les adresses géolocalisées de la fiche.
4. **IA in-form** — « 🪄 Suggest » : l'IA propose, tu appliques.

Le **YAML se ré-émet sans perte** (ordre de clés préservé, dates non quotées, `\|`/`\|-`/`\|+`). Le bouton
**💾 Commit** est optionnel (PAT via ✏️) et ne concerne pas l'évaluation. **Deux pistes**, à trancher selon ton
retour : on **ajoute** ces composants à ton CMS, ou on en **remplace**.

## Le schéma (bloc `.dataset`, YAML)

```yaml
- { name: title,         label: Nom affiché,            widget: string, wysiwyg: true }
- { name: gender,        label: Genre,                  widget: select, required: false,
    options: ["", masculin, féminin, non-binaire, inconnu] }
- { name: professions,   label: Professions / activités, widget: list, required: false,
    hint: vocabulaire contrôlé v1.3 }
- { name: nationalities, label: Nationalités,           widget: list, required: false }
- { name: periods,       label: Époques,                widget: relation, collection: periods, multiple: true }
- { name: themes,        label: Thèmes,                 widget: relation, collection: themes,  multiple: true }
- name: addresses
  label: Adresses associées
  widget: objectlist
  required: false
  fields:
    - { name: id,     label: Adresse, widget: relation, collection: addresses }
    - { name: role,   label: Rôle,    widget: string, required: false }
    - { name: period, label: Période, widget: string, required: false }
- { name: body,          label: Biographie,             widget: text, rows: 5, wysiwyg: true }
```
{: .dataset #paris_person_schema format="yaml" }

## L'index de relations (bloc `.dataset`, YAML — entrées avec `lat`/`lng` = cartographiables)

```yaml
periods:
  - { slug: revolution-francaise,  title: Révolution française }
  - { slug: revolutions-de-1848,   title: Révolutions de 1848 }
  - { slug: commune-de-1871,       title: Commune de 1871 }
  - { slug: second-empire,         title: Second Empire }
  - { slug: troisieme-republique,  title: Troisième République }
  - { slug: belle-epoque,          title: Belle Époque }
themes:
  - { slug: paris-feministe, title: Paris féministe }
  - { slug: litterature,     title: Littérature }
addresses:
  - { slug: 24-rue-houdon,          title: 24 rue Houdon,          lat: 48.8836, lng: 2.3376 }
  - { slug: cimetiere-de-levallois, title: Cimetière de Levallois, lat: 48.8975, lng: 2.2836 }
```
{: .dataset #paris_index format="yaml" }

## La fiche (Louise Michel) — édite-la, ou clique le nom / la bio sur l'aperçu

```yaml
id: louise-michel
slug: louise-michel
type: person
title: Louise Michel
sortName: Michel, Louise
gender: féminin
birth:
  date: 1830-05-29
  year: 1830
  place: Vroncourt-la-Côte
death:
  date: 1905-01-09
  year: 1905
  place: Marseille
professions:
  - institutrice
  - anarchiste
nationalities:
  - France
periods:
  - commune-de-1871
  - troisieme-republique
themes:
  - paris-feministe
addresses:
  - { id: 24-rue-houdon, role: résidence, period: 1871 }
  - { id: cimetiere-de-levallois, role: mémoire }
body: |
  Institutrice et militante anarchiste, figure majeure de la Commune de Paris (1871).
  Déportée en Nouvelle-Calédonie, elle y prend le parti des Kanaks.

  Surnommée « la Vierge rouge », elle demeure une icône des mouvements ouvrier et féministe.
workflow:
  draft: false
  aiText: null
  edited: true
  validated: false
  reviewRequested: true
  reviewNote: null
```
{: .record schema="paris_person_schema" index="paris_index" map="true" mapengine="leaflet" ai="true" commit="true" path="docs/paris/sample/louise-michel.yaml" }

---

*Un seul moteur (`.record` = `lcSchema` + `lcYaml`) rend n'importe quelle fiche ; seuls le schéma et
l'index changent. Les champs hors-schéma (`id`, `slug`, `birth`, `death`, `workflow`…) ne sont pas édités
mais **préservés** au round-trip.*
