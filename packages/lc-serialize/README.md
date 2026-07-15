# @karmicsoft/lc-serialize

Faithful YAML round-trip for git-backed structured content — a **LightCode** brick.
MIT — © 2026 KarmicSoft (see `LICENSE`).

Reads and writes the **same YAML that lives in git**, losing nothing:

- **key order preserved** (no reordering → minimal git diffs);
- **unquoted dates kept as strings** (`1830-05-29` stays a string — no `js-yaml` timestamp→ISO coercion);
- **block-scalar chomping preserved** (`|` / `|-` / `|+`);
- **null preserved**, nested objects/lists, `[]` for empty arrays;
- **the leading comment block** (migration provenance, e.g. `# source: …`) **survives** round-trip byte-identically.

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

## One-liner corpus check (CLI)

Ships a `bin` — point it at a folder (or a file); exits non-zero on any data loss:

```sh
npx @karmicsoft/lc-serialize lc-serialize-check ./content
#  → "N file(s) checked · 0 data-loss · K byte-drift (advisory)"
#  LC_VERBOSE=1 lists every drifting file
```

`isLossless` is the gate (must be 0). Byte-drift is advisory: a lossless file can
still reformat — the **leading** comment block is preserved, but **inline / mid-file
comments are dropped** and flow style (`{a: 1}` / `[1, 2]`) becomes block. On a
Sveltia-generated corpus with provenance headers, drift ≈ 0.

## CI recipe (round-trip over the whole corpus, in code)

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
  block style** (your migrated corpus largely is) — including its **leading comment
  block** (`# source: …`), which round-trips verbatim. It will differ — while staying
  lossless — for files that carry **inline / mid-file comments** (dropped on parse) or
  **flow style** (`{a: 1}`, `[1, 2]`). Treat byte-drift as an **advisory / drift
  detector**, not a failure.
- Round-trip is **idempotent**: after one `dump`, further round-trips are byte-stable.
