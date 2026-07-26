# Le socle est complet — 5 briques, toutes publiées

Salut Toni,

Ta Phase 1 est arrivée nickel : **socle épinglé, garde CI sur 44 881 fichiers,
24 tags `relation:` vérifiés, `fr.json` prêt**. C'était le feu vert qu'on
attendait — voici tout ce qui suit, publié et testé.

```sh
npm i @karmicsoft/lc-record @karmicsoft/lc-map @karmicsoft/lc-suggest
npm update @karmicsoft/lc-schema     # → 0.1.3
```

| Brique | Version | Rôle |
|---|---|---|
| `lc-serialize` | 0.1.1 | round-trip YAML sans perte *(inchangée)* |
| `lc-schema` | **0.1.3** | schéma → IR **+ libellés imbriqués** |
| `lc-record` | **0.1.0** | **le cerveau headless** — c'est le jalon que tu attendais |
| `lc-map` | **0.1.0** | où regarder (bounds, centre, zoom) |
| `lc-suggest` | **0.1.0** | ce qu'on propose — jamais ce qu'on fait |

Zéro DOM dans les cinq. MIT. Pedia les rend à sa façon, toi à la tienne.

---

## 1. Libellés imbriqués — ta question, tranchée

**Une seule map plate par collection, clés en chemin pointé.** On adresse la
structure, on ne la recopie pas.

```js
labels: { periods: {
  title: 'Titre',
  daterange: 'Période',                 // le conteneur garde sa propre clé
  'daterange.startDay': 'Jour de début',// un champ DANS cet objet
  'addresses.role': 'Rôle',             // enfant d'objectlist — SANS index
  'tags.value': 'Étiquette',            // l'item d'une liste scalaire
} }
```

Trois conséquences :

- **le conteneur garde sa clé** — `daterange` et `daterange.startDay` coexistent ;
- **l'enfant d'objectlist saute l'index** — `addresses.role` libelle ce champ dans
  **chaque** item. Il n'y a pas de `addresses.0.role`, et il n'y en aura jamais :
  ajouter une 12ᵉ adresse ne demande aucune traduction de plus ;
- **le repli ne change pas** — non listé = libellé auto (`startDay` → « Start Day »).
  Traduire partiellement est parfaitement valable.

La profondeur n'est pas limitée (`a.b.c`). Et **les deux lecteurs** la prennent :
`fromSveltiaConfig(cfg, { labels })` existe maintenant, où elle agit comme une
**surcouche i18n qui l'emporte sur le `label:` du config** — tu traduis par locale
sans forker `config.yml`. Appelée à un seul argument, elle se comporte exactement
comme en 0.1.2 (un scénario le garantit).

## 2. Astro : marque les relations **en ligne**, jamais via un wrapper

C'est dans le README et le HANDOVER maintenant, là où tu tomberas dessus :

```ts
const rel = (c) => reference(c).describe(`relation:${c}`);   // ✗ non
periods: reference('periods').describe('relation:periods'),  // ✓ oui
```

Un helper générique autour de `reference()` rend les types de contenu Astro
**circulaires** et l'inférence s'effondre — c'est l'origine de tes 231 erreurs.
Une répétition par champ, et l'inférence reste intacte. C'est la seule forme
qu'on teste.

## 3. `lc-record` — le cerveau, extrait

Pas de DOM, pas de framework, pas de réseau. Il répond *quoi afficher* et *ce que
fait une modification* ; l'hôte dessine.

```js
const { record, keys, leading } = parse(fileText);      // record + ORDRE des clés + provenance
const ctrls = controls(ir, record, index, 'persons');   // → à rendre comme tu veux
const { structural } = setValue(record, 'body', 'peintre');
const out = emit(record, { keys, leading });            // le fichier ENTIER, prêt à écrire
```

- **L'IR est réconcilié à la volée** : IR lc-schema, une collection d'IR, ou un
  tableau de champs plat — tout passe. Une collection inconnue **lève une erreur**
  au lieu de produire un formulaire vide.
- **Les contrôles sont des données** : les relations arrivent avec leurs **chips
  déjà résolues** (aucun hôte ne refait le lookup) ; un `objectlist` expose **un
  jeu de contrôles par item** ; un widget inconnu **dégrade** en `string` marqué
  `degraded: true` — un champ qu'on ne peut pas saisir, c'est ennuyeux ; un champ
  qui disparaît en silence, c'est pire.
- **Écriture = réémission du fichier entier**, d'après ton ≈1 % : `emit()` rejoue
  l'ordre des clés et le bloc de provenance, donc un enregistrement non modifié se
  sauve **à l'octet près** (un diff nul — un scénario l'affirme).
- **Les mutations disent si c'est structurel** : `setValue` = édition de valeur
  (l'hôte garde son DOM, donc le curseur survit à la frappe) ; `addItem`/`removeItem`
  = structurel, il faut reconstruire. Ce bit-là, c'est toute la différence entre un
  éditeur stable et un éditeur qui se bat contre toi.
- **`integrity(record, keys)`** répond à la vraie peur — *ai-je perdu une clé ?* —
  et **nomme** les clés perdues, pas juste un compte.

## 4. Les deux îlots

**`lc-map`** — la géométrie de la vue, sans bibliothèque de carte :

```js
const { markers, center, zoom, empty } = view(geoPoints(record, index), { width: 640, height: 400 });
```

`geoPoints()` de `lc-record` est déjà la forme d'entrée : le câblage est un seul
tuyau. Les points sans coordonnées finies sont **écartés, pas tracés** (sinon ils
atterrissent au large de l'Afrique) ; le centre est celui de la **boîte**, pas la
moyenne (un point isolé ne tire pas la vue) ; un point unique n'a pas de boîte,
donc il reçoit `pointZoom`. Le zoom est du Web-Mercator standard : le même nombre
veut dire la même chose pour MapLibre et pour Leaflet.

**`lc-suggest`** — « il propose, tu décides ». Rien ne bouge tant que tu n'appelles
pas `apply()` sur une suggestion acceptée par un humain.

**Le point clé : une suggestion est une DONNÉE, jamais une closure.**

```js
{ id: 'relate:periods:commune-de-1871', kind: 'relate', field: 'periods',
  value: ['commune-de-1871'],
  text: 'Le texte mentionne « Commune de 1871 » → la lier sous « Époques »' }
```

Ta version en page porte un `apply: function`, qui ne peut pas traverser le
réseau — local et distant demandent donc deux traitements. En normalisant les deux
vers `{field, value}`, **un seul bouton Appliquer sert les deux chemins**, et une
suggestion se journalise ou se relit comme n'importe quelle donnée.

Deux générateurs locaux, agnostiques du domaine : **`stub`** (champ requis ou
prose vide → un texte à remplir ; ton repli actuel, généralisé aux champs requis)
et **`relate`** (le texte du record nomme une entrée de l'index pas encore liée →
propose le lien ; insensible aux accents et à la casse, conserve les liens
existants, ne re-propose jamais). Les endpoints distants sont traités comme non
fiables : `normalize()` accepte `{suggestions:[…]}` ou un tableau nu, jette ce qui
n'est pas applicable, et une réponse aberrante dégrade en `[]` — jamais une
exception dans ta boucle de rendu.

> ⚠️ **`relate` est du neuf, pas de l'extrait.** C'est le seul endroit où on est
> allés au-delà d'un portage littéral. Désactivable :
> `suggest(schema, record, index, { kinds: ['stub'] })`. Dis-nous si tu préfères
> qu'on le retire.

## 5. Vérification

Tout est passé en CI avant publication :

```
lc-serialize  21 scénarios, 0 échec
lc-schema     35 scénarios, 0 échec
lc-record     35 scénarios, 0 échec
lc-map        14 scénarios, 0 échec
lc-suggest    21 scénarios, 0 échec
+ la garde anti-dérive SSOT
```

Les cinq briques sont publiées avec **provenance signée** (Sigstore) depuis
GitHub Actions.

> Détail utile : une toute première publication d'un paquet *scoped* met ~5 min à
> apparaître dans `npm view` (latence de CDN sur le packument) alors que
> `registry.npmjs.org/@karmicsoft%2flc-map/0.1.0` répond déjà. Si ton install
> tombe sur un 404 juste après une annonce, c'est ça — retente une minute plus tard.

## 6. À toi de jouer

- `controls()` remplace ta construction de formulaire — même IR, ton rendu.
- `emit()` + `integrity()` remplacent ton chemin d'écriture : fichier entier,
  ordre des clés conservé, provenance intacte.
- `view(geoPoints(...))` câble la carte sans toucher au moteur.
- `payload()`/`normalize()` fixent le contrat de ton endpoint IA quand tu en
  brancheras un.

Dis-nous ce qui coince sur ton corpus — les retours de la 0.1.2 ont directement
produit deux correctifs, c'est la boucle qui marche le mieux.

À bientôt,
**KarmicSoft — LightCode**
