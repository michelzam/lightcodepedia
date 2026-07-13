# @karmicsoft/lc-serialize

Faithful YAML round-trip for git-backed structured content — a **LightCode** brick.
© KarmicSoft (see `LICENSE`).

Reads and writes the **same YAML that lives in git**, losing nothing:

- **key order preserved** (no reordering → minimal git diffs);
- **unquoted dates kept as strings** (`1830-05-29` stays a string — no `js-yaml` timestamp→ISO coercion);
- **block-scalar chomping preserved** (`|` / `|-` / `|+`);
- **null preserved**, nested objects/lists, `[]` for empty arrays.

## Install

```sh
npm install @karmicsoft/lc-serialize
```

## API

```js
import { load, dump, roundtrip, isByteIdentical, isLossless } from '@karmicsoft/lc-serialize';

const obj  = load(yamlText);      // parse (dates stay strings)
const yaml = dump(obj);           // serialize (block style, key order preserved)
const yaml2 = roundtrip(yamlText); // load()→dump()
isByteIdentical(yamlText);        // roundtrip === source ?
isLossless(yamlText);             // parsed data survives round-trip (order-independent)
```

`dump(obj, { order })` — pass an explicit key order if you want a canonical order
instead of the object's own order. Omit it to preserve the source order.

## CI recipe (round-trip over the whole corpus)

```js
import { isLossless, isByteIdentical } from '@karmicsoft/lc-serialize';
import { readFileSync } from 'node:fs';
import { globSync } from 'glob';

let loss = 0, drift = 0;
for (const f of globSync('content/**/*.yaml')) {
  const src = readFileSync(f, 'utf8');
  if (!isLossless(src))       { loss++;  console.error('LOSS  ', f); }   // ← must be 0 (fail CI)
  else if (!isByteIdentical(src)) { drift++; console.warn ('drift ', f); } // ← advisory
}
process.exit(loss ? 1 : 0);
```

### Scope of the guarantee

- **`isLossless` is the contract** — no data lost. Assert this in CI; it must be 0.
- **`isByteIdentical`** additionally holds when the source is already in **canonical
  block style** (your migrated corpus largely is). It will differ — while staying
  lossless — for files that carry **YAML comments** (`# …`, dropped on parse) or
  **flow style** (`{a: 1}`, `[1, 2]`). Treat byte-drift as an **advisory / drift
  detector**, not a failure.
- Round-trip is **idempotent**: after one `dump`, further round-trips are byte-stable.
