# @karmicsoft/lc-suggest

**It suggests, you decide.** A headless suggestion engine that proposes edits to
a record and **never performs one** — nothing mutates until a host calls
`apply()` with a suggestion a human accepted.

```sh
npm i @karmicsoft/lc-suggest
```

```js
import { suggest, payload, normalize, apply } from '@karmicsoft/lc-suggest';

const local = suggest(schema, record, index);            // no endpoint needed
const remote = normalize(await post(url, payload(schema, record)));   // same shape
const { record: next, structural } = apply(record, accepted);          // only on accept
```

## A suggestion is data, never a closure

```js
{ id: 'relate:periods:commune-de-1871', kind: 'relate', field: 'periods',
  value: ['commune-de-1871'],
  text: 'The text mentions “Commune de 1871” → link it under “Époques”',
  reason: 'title found in the record’s text, not yet linked' }
```

That's the whole design: the shape survives a JSON round-trip, so a **local
generator and a remote AI endpoint are indistinguishable to the host** — one
Apply button handles both.

## Local generators (domain-agnostic)

- **`stub`** — an empty required or prose field → offer a placeholder to fill in.
  Relations and containers are never stubbed.
- **`relate`** — the record's own text names something in the index that isn't
  linked yet → offer the link. Accent- and case-insensitive; a multiple relation
  keeps what's already there; an existing link is never re-proposed.

Pick with `suggest(schema, record, index, { kinds: ['relate'], limit: 5 })`.

## Remote endpoints are untrusted

`payload()` is the agreed request body; `normalize()` coerces **any** answer to
`Suggestion[]`. A junk response degrades to `[]` — it never throws into the
host's render loop, and items with no applicable edit are dropped.

MIT © KarmicSoft
