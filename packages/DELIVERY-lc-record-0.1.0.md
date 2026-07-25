# lc-record 0.1.0 — the headless engine you were waiting for

Here it is, Toni: the record **brain**, extracted and published. No DOM, no
framework, no network. It answers *what to render* and *what an edit does*;
you render it your way, pedia renders it as `.record`. Same brain, two skins.

```sh
npm i @karmicsoft/lc-record       # 0.1.0 — depends on lc-serialize ^0.1.1
```

```js
import { parse, controls, setValue, emit, geoPoints, integrity } from '@karmicsoft/lc-record';

const { record, keys, leading } = parse(fileText);      // record + key ORDER + provenance
const ctrls = controls(ir, record, index, 'persons');   // → render however you like
const { structural } = setValue(record, 'body', 'peintre');
const out = emit(record, { keys, leading });            // the WHOLE file, ready to write
```

## 1. The IR is reconciled — in-flight, as decided

`fields()` (and everything built on it) accepts **whichever shape you have**:

- an **lc-schema IR** — `fromZod(...)` / `fromSveltiaConfig(...)`, with a collection name
- a **single IR collection** — `{ name, fields }`
- a **flat field array** — what pedia's `.record` ships today

So adopting lc-schema's IR costs you nothing at the call site, and an unknown
collection **throws** instead of quietly compiling to an empty form.

## 2. Controls are data

```js
controls([{ name:'periods', widget:'relation', collection:'periods', multiple:true }],
         { periods:['commune-de-1871'] }, index)
// → [{ name:'periods', widget:'relation', multiple:true, value:['commune-de-1871'],
//      chips:[{ slug:'commune-de-1871', title:'Commune de 1871' }] }]
```

Relations arrive with their **chips already resolved** — no host re-does the
index lookup. Nested shapes come back ready: an `object` exposes child controls,
an **`objectlist` exposes one control set per item** (N rows, no re-derivation),
a `list` carries items + template. An unrecognized widget **degrades** to a
string control flagged `degraded: true` — a field you can't type is bad, one
that silently vanishes is worse.

## 3. Write path — full-file re-emit, per your ≈1%

`emit()` re-emits the **whole file**: it replays the original key order and the
leading provenance block, so an untouched record saves **byte-identically** (a
no-op diff — there's a scenario asserting exactly that). Your 1.7% byte-drift
measurement is what settled this: a surgical patch can interleave a partial edit
into a half-parsed file; a full write cannot.

`integrity(record, keys)` answers the thing users actually fear — *did I lose a
key?* — and **names** the lost keys, not just a count.

## 4. Mutations say whether the form must be rebuilt

Every mutation returns `{ record, structural }`:

- `setValue(rec, 'daterange.startDay', 1871)` → **value edit**, keep the form DOM
  (this is why a caret survives typing). Dotted paths create missing parents; a
  numeric segment creates an **array**, not an object.
- `addItem` / `removeItem` → **structural**, the control set changed, rebuild.

That single bit is the difference between an editor that feels stable and one
that fights you.

## 5. Geo stays generic

`geoPoints(record, index)` plots every indexed entry with `lat` + `lng`/`lon`
whose slug appears **anywhere** in the record, at any depth — `person.addresses`,
`event.location.points`, any shape, zero per-record config. `lng` and `lon` are
both accepted on input; output is normalized to `{ lat, lon, label }`.

## 6. Verification

`node test.mjs` — **35 scenarios, 0 failed**, covering: IR reconciliation (all
three shapes + both failure modes), controls incl. nested/objectlist/degraded,
relation display + type-ahead (accents, ranking, exclusions), geo at depth,
mutations incl. structural flags and array creation, round-trip incl. the
byte-identical no-op save, and integrity.

CD is now driven by the workspace list, so this brick — and `lc-map` /
`lc-suggest` after it — publish without anyone editing the pipeline.

## Next

**lc-map** and **lc-suggest** as host-wired islands. `geoPoints()` above is
already the contract lc-map will consume, so that one is mostly wiring.
