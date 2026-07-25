# lc-schema 0.1.3 — nested labels, decided: dotted paths on one flat map

Your Phase 1 landed clean, Toni — **socle pinned, CI gate on 44,881 files, 24 `relation:`
tags verified, `fr.json` ready**. That's the green light we needed. Your open question on
nested labels is now decided and shipped.

```sh
npm update @karmicsoft/lc-schema     # → 0.1.3   (lc-serialize stays 0.1.1)
```

## 1. Nested labels — the rule

**One flat map per collection, keyed by dotted path.** You address the structure; you
never mirror it. No nested label objects, no per-item indices.

```js
const ir = fromZod(astro, { labels: { periods: {
  title: 'Titre',                    // top-level field
  daterange: 'Période',              // the CONTAINER keeps its own key
  'daterange.startDay': 'Jour de début',   // a field INSIDE that object
  'addresses.role': 'Rôle',          // objectlist child — NO index
  'tags.value': 'Étiquette',         // the item of a scalar list
} } });
```

Three consequences worth stating plainly:

- **The container keeps its own key.** `daterange` labels the object field itself;
  `daterange.startDay` labels the field inside it. They coexist on the same map.
- **Objectlist children skip the index.** `addresses.role` labels that field in
  **every** item — there is no `addresses.0.role`, and there never will be. One key,
  N items; adding a 12th address needs no new translation.
- **Fallback is unchanged.** Anything unlisted auto-labels from the field name
  (`startDay` → "Start Day"). Partial translation is fine — translate what matters.

Depth is not limited: `a.b.c` works wherever the structure goes.

## 2. It applies to **both** readers

`fromSveltiaConfig` takes the same second argument now — same map, same rules:

```js
const ir = fromSveltiaConfig(cfg, { labels: { places: { 'addresses.role': 'Rôle' } } });
```

There it acts as an **i18n overlay that wins over the config's own `label:`** — so you
translate per locale without forking `config.yml`. Called with one argument it behaves
exactly as 0.1.2; a scenario guards that, so your existing call sites are untouched.

## 3. Astro: mark relations **inline**, never through a wrapper

Filing this where you'll trip over it (README + HANDOVER): a generic helper around
`reference()` —

```ts
const rel = (c) => reference(c).describe(`relation:${c}`);   // ✗ don't
```

— makes Astro's content types **circular** and inference collapses (your 231 errors).
The supported pattern is inline, at each use site:

```ts
periods: reference('periods').describe('relation:periods'),   // ✓
```

One repetition per field, inference intact. It's the only shape we test.

## 4. Verification

`node test.mjs` — **35 scenarios, 0 failed**, including the new block:

- a nested child resolves by dotted path, container keeps its own key
- an objectlist child resolves without an index (labels every item)
- a scalar list item resolves as `<list>.value`
- unlisted children fall back to the auto-label (nested **and** objectlist siblings)
- `fromSveltiaConfig` without `opts` still honours the config label — **no behaviour
  change for existing callers**

## Next from us

**lc-record** — the headless engine you're waiting on (IR + record + index → field
controls, relations, geo extraction, round-trip, mutations), write path = **full-file
re-emit**, per your ≈1% drift measurement. Pedia will render it as `.record`; you render
it your way. `lc-map` / `lc-suggest` follow as host-wired islands.
