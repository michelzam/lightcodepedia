# lc-schema 0.1.2 — tes deux retours sur `fromZod`, corrigés

Merci pour le passage sur ton vrai corpus, Toni — **44 879 fichiers, 0 perte de
données, 1,7 % de dérive binaire** : c'est exactement le profil qu'on attendait, et ça
confirme la **réémission du fichier entier** comme stratégie d'écriture sûre. Ton rapport
de bug sur `fromZod` était juste ; c'est réglé.

```sh
npm update @karmicsoft/lc-schema     # → 0.1.2  (lc-serialize reste en 0.1.1)
```

## 1. Le bug des « zéro champ en silence » — corrigé (tes deux suggestions livrées)

Tu as trouvé que `fromZod` compilait une collection en **zéro champ, en silence**, quand
sa racine était `z.preprocess(stripNull, z.object({…}))` — ton garde-fou anti-null de
Sveltia. Cause racine : on dépliait `optional`/`default`/`effects` **par champ**, mais pas
à la **racine de la collection**. Tes deux corrections sont en place :

- **(a) Déplier la racine** — on applique maintenant le même dépliage
  `optional · nullable · default · preprocess/effects · pipe` **à la racine** de la
  collection avant de lire les champs. Tes collections `z.preprocess(stripNull, z.object(...))`
  compilent désormais leurs vrais champs. Vérifié sur **Zod 3** (où une racine `preprocess`
  est un `ZodEffects`) **et Zod 4** (où c'est un `ZodPipe`) — donc ça marche quelle que
  soit la version majeure.
- **(b) Échouer bruyamment** — une racine qui **n'est pas** un objet (un simple
  `z.string()`, ou une forme-fonction `({ image }) => z.object(...)`) **lève désormais une
  erreur claire nommant la collection**, au lieu de te rendre un formulaire vide.

## 2. Libellés d'affichage / i18n — le canal que tu demandais

`.describe()` est déjà pris par les indices `relation:` / widget, donc les libellés ont
leur propre canal. Ils se résolvent **par ordre de priorité** — à mélanger librement :

**1. `opts.labels` — le canal i18n (recommandé).** Une table clée
`{ collection: { champ: 'Libellé' } }`, chargée **par langue active**, pour que les
traductions restent **hors** du schéma :

```js
import fr from './i18n/fr.json';   // { periods: { startDay: 'Jour de début' } }
const ir = fromZod(collections, { labels: fr });
```

**2. `label:` dans `.describe()` — un défaut posé à côté du widget** (le libellé court
jusqu'au prochain `|`) :

```js
name: z.string().describe('label:Époque | text'),
```

**3. Le nom de champ « embelli » — le repli, désormais plus propre.** Il découpe le
camelCase : `startDay` → **« Start Day »**, `aiText` → **« Ai Text »**. Donc même sans
rien configurer, fini les libellés collés.

> Priorité : **`opts.labels`** → **directive `label:`** → **nom embelli**.
> Garde l'i18n dans `opts.labels` (par langue), un défaut raisonnable dans `label:`, et
> laisse le repli embelli gérer tout ce que tu n'as pas encore touché.

## 3. Rien d'autre n'a changé

`fromSveltiaConfig` est intact et émet toujours **le même IR** — ton choix de source
canonique reste réversible. `lc-serialize` reste en **0.1.1**. Cette version est
**additive et rétrocompatible** : tes appels `fromZod(schemas)` existants continuent de
marcher ; `opts.labels` et le dépliage de racine sont de purs ajouts.

Non-régression : **lc-serialize 21 scénarios BDD · lc-schema 26 scénarios BDD** (6
nouveaux — dépliage de racine `preprocess` sur v3 **et** v4, erreur sur racine non-objet,
erreur sur schéma-fonction, priorité des libellés) + le garde-fou anti-dérive SSOT. Tout
au vert en CI avant publication.

## Une chose en retour, quand tu peux

Repasse `fromZod` sur tes **12** collections après le `npm update`. Si un champ sort
encore faux (relation non détectée, objet imbriqué aplati, widget mal typé), envoie la
ligne Zod de ce champ-là et on ajuste le lecteur — même boucle qu'avant.

---
*`@karmicsoft/lc-schema@0.1.2`, `@karmicsoft/lc-serialize@0.1.1`. API complète dans le
`README.md` de chaque paquet ; changelog dans `packages/CHANGELOG.md`.*
