# lc-map 0.1.0 + lc-suggest 0.1.0 — the two islands

The pair that sits on top of `lc-record`, Toni. Both headless, both host-wired:
they decide, you draw.

```sh
npm i @karmicsoft/lc-map @karmicsoft/lc-suggest
```

## lc-map — where to look

No map library, no DOM. It takes points and answers the viewport question.

```js
import { view } from '@karmicsoft/lc-map';
import { geoPoints } from '@karmicsoft/lc-record';

const { markers, center, zoom, bounds, empty } = view(geoPoints(record, index), { width: 640, height: 400 });
if (!empty) map.jumpTo({ center: [center.lon, center.lat], zoom });
```

`geoPoints()` from lc-record is already the input shape — that pipe is the whole
wiring. Three decisions you'll care about:

- **Junk is dropped, not plotted.** A point without finite, in-range coordinates
  would otherwise land off the coast of Africa and read as a data bug.
- **Centre is the box centre, not the average** — one outlier can't drag the view.
- **A single point has no box**, so it gets `pointZoom` (default 14) instead of a
  meaningless fit. `maxZoom` still wins.

Zoom is standard Web-Mercator tile math (256px tiles), so the number means the
same thing to MapLibre and to Leaflet — that's what makes the renderer swappable.

## lc-suggest — it suggests, you decide

It proposes edits and **never performs one**. Nothing mutates until you call
`apply()` with something a human accepted.

```js
import { suggest, payload, normalize, apply } from '@karmicsoft/lc-suggest';

const local  = suggest(schema, record, index);                        // no endpoint needed
const remote = normalize(await post(url, payload(schema, record)));   // identical shape
const { record: next, structural } = apply(record, accepted);
```

**The key move: a suggestion is DATA, never a closure.**

```js
{ id: 'relate:periods:commune-de-1871', kind: 'relate', field: 'periods',
  value: ['commune-de-1871'],
  text: 'The text mentions “Commune de 1871” → link it under “Époques”',
  reason: 'title found in the record’s text, not yet linked' }
```

Your current in-page version carries an `apply: function` closure — which can't
cross a network boundary, so local and remote suggestions need different
handling. Normalizing both to `{field, value}` means **one Apply button serves
both paths**, and a suggestion can be logged, queued or reviewed like any record.

Two local generators, both domain-agnostic:

- **`stub`** — an empty required or prose field offers a placeholder (this is
  your existing fallback, generalized past `wysiwyg` to required fields too).
  Relations and containers are never stubbed.
- **`relate`** — the record's own text names something in the index that isn't
  linked yet → offer the link. Accent- and case-insensitive; a multiple relation
  **keeps what's already linked**; an existing link is never re-proposed. This is
  the one that earns its keep on a real corpus.

Remote endpoints are treated as untrusted: `normalize()` accepts
`{suggestions:[…]}` or a bare array, drops items with no applicable edit, and a
junk answer degrades to `[]` — it never throws into your render loop.

## Verification

- **lc-map — 14 scenarios, 0 failed**: normalization and dropped junk, bounds,
  box-centre vs average, zoom-out on a wider spread, viewport size effects,
  single-point and empty behaviour.
- **lc-suggest — 21 scenarios, 0 failed**: generating never mutates, suggestions
  survive a JSON round-trip, stub rules, relate (accents, existing links,
  single vs multiple), endpoint contract + junk degradation, apply semantics.

Both publish through the same CD, which now derives its package list from the
workspace list — so these two went out without anyone editing the pipeline.

## Where this leaves the socle

```
lc-serialize  0.1.1   lossless YAML round-trip
lc-schema     0.1.3   schema → IR (+ nested dotted labels)
lc-record     0.1.0   the headless brain: controls, relations, geo, mutations, re-emit
lc-map        0.1.0   where to look
lc-suggest    0.1.0   what to propose (never what to do)
```

Five bricks, no DOM in any of them, MIT. Pedia renders them one way; you render
them yours.
