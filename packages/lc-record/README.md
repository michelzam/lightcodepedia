# @karmicsoft/lc-record

**The headless record engine.** Given a schema, a record and a relation index, it
answers *what to render* and *what an edit does* — with **no DOM and no
framework**. Pedia renders the answers as `.record`; your app renders them its
way. Same brain, different skins.

```sh
npm i @karmicsoft/lc-record
```

```js
import { controls, setValue, emit, parse, geoPoints } from '@karmicsoft/lc-record';

const { record, keys, leading } = parse(fileText);       // record + key order + provenance
const ctrls = controls(ir, record, index, 'persons');    // → render these however you like
const { structural } = setValue(record, 'body', 'peintre');
const out = emit(record, { keys, leading });             // the whole file, ready to write
```

## What it gives you

| | |
|---|---|
| `fields(schema, name?)` | **IR reconciliation** — accepts an [lc-schema](https://www.npmjs.com/package/@karmicsoft/lc-schema) IR, one IR collection, or a plain field array |
| `controls(schema, record, index, name?)` | one **control descriptor** per field: value, options, and for relations the **resolved chips** |
| `relTitle` / `relMatch` | relation display + type-ahead (prefix first, accent- and case-insensitive, picked slugs excluded) |
| `geoPoints(record, index)` | every indexed point whose slug appears **anywhere** in the record, at any depth |
| `setValue` / `addItem` / `removeItem` | mutations by dotted path, each reporting whether it was **structural** |
| `parse` / `emit` | round-trip: key order + provenance in, **full file** out |
| `integrity(record, keys)` | did the edit drop a key that was in the file? |

## Three decisions worth knowing

**The write path is a full-file re-emit**, not a surgical patch. On a 44k-file
corpus the re-emit drift measured ≈1%, and a whole-file write can never
interleave a partial edit into a half-parsed file. `emit()` replays the original
key order and the leading provenance comments, so an untouched record saves
**byte-identically** — a no-op diff.

**Mutations tell you if they were structural.** `setValue` is a value edit (the
host keeps its form DOM, so a caret survives typing); `addItem`/`removeItem`
changed the control set, so the form must be rebuilt. That one bit is why an
editor feels stable while you type.

**Unknown widgets degrade, they don't vanish.** A widget the engine doesn't know
comes back as a `string` control flagged `degraded: true`. A field you can't type
into is bad; a field that silently disappears is worse.

## Controls are data

```js
controls([{ name: 'periods', widget: 'relation', collection: 'periods', multiple: true }],
         { periods: ['commune-de-1871'] }, index)
// → [{ name:'periods', widget:'relation', multiple:true, collection:'periods',
//      value:['commune-de-1871'],
//      chips:[{ slug:'commune-de-1871', title:'Commune de 1871' }] }]
```

Nested shapes come back ready to render: an `object` exposes child controls, an
`objectlist` exposes **one control set per item** (so N rows need no re-derivation),
a `list` carries its items plus the item template.

## Geo is generic

The **index owns the coordinates**. Any entry with `lat` + `lng`/`lon` whose slug
appears anywhere in the record is plotted — `person.addresses`, `event.location.points`,
any shape, no per-record configuration. Output is normalized to `{ lat, lon, label }`.

## Scope

This brick decides; it does not draw. No DOM, no CSS, no framework, no network.
Pair it with your own renderer — or with LightCode's `.record`.

MIT © KarmicSoft
