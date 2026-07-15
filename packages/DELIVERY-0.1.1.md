# LightCode socle — delivered (v0.1.1)

**`@karmicsoft/lc-serialize` + `@karmicsoft/lc-schema` are on npm.** Both are
**standalone and usable now** — no editor required.

```sh
npm install @karmicsoft/lc-serialize @karmicsoft/lc-schema
# already installed? → npm update  (to reach 0.1.1)
```

## What's in 0.1.1 — the two things from your corpus run

**1. Leading comments preserved.** Your `# source: xwiki-export…` provenance
headers now survive the round-trip **byte-identically** — so your byte-drift drops
from ~77% to ~1%, which means **full-file re-emit is the safe write strategy**.
Nothing to configure; it's automatic in `roundtrip` / `isByteIdentical`.

**2. `fromZod` — Zod canonical (your choice).** Compile your Astro content
collections straight to the neutral IR:

```js
import { fromZod, widgets, collections } from '@karmicsoft/lc-schema';
import { collections as astroCollections } from './src/content.config.ts';

const ir = fromZod(astroCollections);   // same neutral IR as fromSveltiaConfig
collections(ir);                         // ["persons", "events", ...]
widgets(ir, 'persons');                  // the field list an editor renders
```

Version-tolerant (verified on **Zod 3.25 and 4.4**). **Two caveats:**
- Astro's `reference('periods')` doesn't expose its target collection at runtime →
  tag those fields **`.describe('relation:periods')`** (a `z.array` of that is a
  *multiple* relation).
- A **function-form schema** (`({ image }) => z.object(...)`) must be **resolved**
  before you pass it in.

## The rest of the socle (already yours)

- **Corpus CI gate:** `npx @karmicsoft/lc-serialize lc-serialize-check ./content`
  — exits non-zero on any **data** loss (`isLossless`). Byte-drift is advisory.
- **`fromSveltiaConfig`** still works — both readers emit the **same IR**, so your
  canonical-source choice stays reversible.

## License

Both infra bricks are now **MIT** (© 2026 KarmicSoft) — no license friction for
adoption. (The higher bricks — `lc-editor` / `lc-record` / `lc-suggest` /
`lc-roles` — keep the LightCode Platform License.)

## Where this leaves you

Your **socle + corpus-CI gate is fully unblocked** — install/update and go. The
**editor** (`lc-record`) is the next milestone and is **not needed** to use any of
the above; it's built and reviewed as its own step.

## One thing back, when you can

Does `fromZod` produce the right IR against your **real** `content.config.ts`
(especially relations and refinements)? If a field comes out wrong, send it and
we'll adjust the reader.

---
*Versions: `@karmicsoft/lc-serialize@0.1.1`, `@karmicsoft/lc-schema@0.1.1`. Full
API in each package's `README.md`; integration contract in `HANDOVER.md`.*
