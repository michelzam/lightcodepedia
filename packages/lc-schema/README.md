# @karmicsoft/lc-schema

Schema → **neutral IR** → widget definitions — a small **schema compiler** and a
**LightCode** brick. MIT — © 2026 KarmicSoft (see `LICENSE`).

## Why (the SSOT strategy)

Keep **one canonical schema** and generate the rest, instead of hand-maintaining
several descriptions of the same model (which drift). `lc-schema` is the compiler:

```
  CANONICAL SOURCE ─(reader)→ neutral IR ─(consumers/emitters)→ { lc widgets · JSON Schema · config.yml · … }
     (your choice)            (LightCode)
```

The **IR decouples the choice of canonical source**: switching Zod ↔ config.yml
later changes only the *reader*; consumers (the editor) are unaffected — **reversible,
no lock-in**.

## Install

```sh
npm install @karmicsoft/lc-schema
```

## API

```js
import { fromSveltiaConfig, fromZod, widgets, collections } from '@karmicsoft/lc-schema';

// from a Sveltia/Decap config.yml:
const ir = fromSveltiaConfig(readFileSync('public/admin/config.yml', 'utf8'));

// …or from your runtime Zod schemas (Astro content collections):
import { collections as astro } from './src/content.config.ts';
const ir2 = fromZod(astro);           // { persons: {schema}, events: {schema} } or { persons: z.object(...) }

collections(ir);            // ["persons", "events", ...]
widgets(ir, 'persons');     // flat widget list the lc-editor renders
```

`fromZod` is **version-tolerant** (Zod 3 & 4). Astro's `reference('periods')`
doesn't expose its target collection at runtime, so mark relations with
`.describe('relation:periods')` (a `z.array` of that is a *multiple* relation);
`.describe('markdown' | 'image' | 'text')` pick those widgets. A schema that is a
**function** (`({ image }) => z.object(...)`) must be resolved before passing it in.

### Neutral IR shape

```
{ irVersion, source, collections: [
  { name, label, folder, extension, identifier, fields: [ Field ] }
]}
Field = { name, label, widget, required, hint?, default?,
          options?      // select: [{label, value}]
          collection?, multiple?, valueField?, displayField?  // relation
          item?         // list of scalars
          fields?       // object / objectlist
        }
```

Supported widgets: `string · text · number · boolean · select · relation · list ·
objectlist · object · markdown · image · file · hidden`.

## SSOT — canonical source, your call (reversible)

- **v0.1 reader: Sveltia/Decap `config.yml`** (already in your repo).
- **Recommended canonical: your Zod `content.config.ts`** — it is your build authority
  and the richest (`reference()`, refinements, `nullSafe`, `dateStr`); `config.yml` is a
  *subset*. With a Zod reader (roadmap), `config.yml` becomes **generated** and the
  duplication disappears.
- **If you keep `config.yml` canonical:** add a CI check that it stays consistent with
  the Zod (which carries semantics `config.yml` can't).

Either way, consumers read the **IR**, so the decision is reversible.
