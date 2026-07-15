# lc-schema 0.1.2 — your two `fromZod` findings, fixed

Thanks for the real-corpus run, Toni — **44,879 files, 0 data-loss, 1.7% byte-drift**
is exactly the profile we expected, and it confirms **full-file re-emit** as the safe
write strategy. MIT + Zod-canonical both noted. Your `fromZod` bug report was spot-on;
it's fixed.

```sh
npm update @karmicsoft/lc-schema     # → 0.1.2   (lc-serialize stays 0.1.1)
```

## 1. The silent-zero-fields bug — fixed (both your suggestions shipped)

You found `fromZod` compiling a collection to **zero fields, silently**, when its root
was `z.preprocess(stripNull, z.object({…}))` — your Sveltia-null guard. Root cause: we
unwrapped `optional`/`default`/`effects` **per field** but not at the **collection root**,
so a root-level wrapper hid the object. Both of your fixes are in 0.1.2:

- **(a) Unwrap the root.** We now run the same peel — `optional · nullable · default ·
  preprocess/effects · pipe` — at the collection root before reading fields. Your
  `z.preprocess(stripNull, z.object(...))` collections now compile to their real fields.
  Verified on **Zod 3** (where a root preprocess is a `ZodEffects`) **and Zod 4** (where
  it's a `ZodPipe`) — so it works whichever major you land on.
- **(b) Fail loud, never silent-empty.** A root that *isn't* an object (a bare
  `z.string()`, a stray union, or a function-form `({ image }) => z.object(...)`) now
  **throws a clear error naming the collection**, instead of handing you an empty form.

## 2. Display labels / i18n — the channel you asked for

You're right that `.describe()` is already spent on `relation:` / widget hints, and that
auto-labels come out English-from-the-name (`StartDay`, `AiText`). New in 0.1.2, labels
resolve by **precedence** — pick whichever layer fits, mix freely:

**1. `opts.labels` — the i18n channel (recommended).** A map keyed
`{ collection: { field: 'Label' } }`, passed at compile time. Load it **per active
locale**, so translations live in your locale files, **not** in the schema:

```js
import fr from './i18n/fr.json';   // { periods: { startDay: 'Jour de début', … } }
const ir = fromZod(collections, { labels: fr });
```

**2. `label:` inside `.describe()` — a default baked next to the widget.** It coexists
with the widget hint; the label runs up to the next `|`:

```js
name: z.string().describe('label:Époque | text'),   // label + widget, together
```

**3. Prettified field name — the fallback, now nicer.** With neither of the above, the
name is prettified and **camelCase is split**: `startDay` → **"Start Day"**,
`aiText` → **"Ai Text"**. So even with zero config the ugly run-on labels are gone.

> Precedence: **`opts.labels`** → **`label:` directive** → **prettified name**.
> Keep i18n in `opts.labels` (per locale), keep a sensible default in `label:`, and lean
> on the prettified fallback for everything you haven't touched yet.

## 3. Nothing else changed

`fromSveltiaConfig` is untouched and still emits the **same IR** — your canonical-source
choice stays reversible. `lc-serialize` stays **0.1.1**. This release is **additive and
backward-compatible**: existing `fromZod(schemas)` calls keep working; `opts.labels` and
the root-unwrap are pure additions.

Non-regression: **lc-serialize 21 BDD · lc-schema 26 BDD** (6 new — root-preprocess
unwrap on v3 **and** v4, throw-on-bad-root, throw-on-function-schema, label precedence)
+ the SSOT drift guard. All green in CI before publish.

## One thing back, when you can

Run `fromZod` on all **12** collections again after `npm update`. If any field still
comes out wrong (a relation not detected, a nested object flattened, a widget mis-typed),
send that one field's Zod line and we'll adjust the reader — same loop as before.

---
*`@karmicsoft/lc-schema@0.1.2`, `@karmicsoft/lc-serialize@0.1.1`. Full API in each
package's `README.md`; changelog in `packages/CHANGELOG.md`.*
