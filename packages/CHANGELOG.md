# Changelog — @karmicsoft/lc-* bricks

Versions follow [semver](https://semver.org): **patch** = fix, **minor** =
additive / backward-compatible, **major** = breaking. Every published version
passed CI (both BDD suites + the SSOT drift guard) before release.

## @karmicsoft/lc-serialize

### 0.1.1
- **Leading comment block preserved** through round-trip: a migration provenance
  header (`# source: …` / blank lines before the first data line) survives
  byte-identically. New `leadingComments(text)` + `dump(obj, { leading })`;
  `roundtrip`/`isByteIdentical` are now comment-aware. `dump(obj)` is unchanged.
  (On a corpus with provenance headers this drops byte-drift dramatically.)
- **Relicensed MIT** (© 2026 KarmicSoft).

### 0.1.0
- Faithful YAML round-trip: preserved key order, unquoted dates kept as strings,
  `|` / `|-` / `|+` chomping, `null`, and `[]` for empty arrays.
- `isLossless` (the contract) + `isByteIdentical` (advisory) helpers.
- Corpus checker `bin` (`lc-serialize-check`) — CI gate over a whole tree.
- TypeScript types; 17-scenario BDD suite.

## @karmicsoft/lc-record

### 0.1.0
- **First release — the headless record engine.** Schema + record + relation
  index → field controls, relation display/type-ahead, geo extraction,
  mutations, round-trip. No DOM, no framework: pedia renders the answers as
  `.record`, another host renders them its way.
- **IR reconciled in-flight.** Accepts an lc-schema IR, a single IR collection,
  or a flat field array; an unknown collection throws instead of compiling to an
  empty form.
- **Write path = full-file re-emit.** `emit()` replays key order + the leading
  provenance block, so an untouched record saves byte-identically. Chosen over
  surgical patching on the ≈1% measured drift.
- **Mutations report `structural`** — value edits keep the host's form DOM (the
  caret survives typing); add/remove rebuild it.
- 35 BDD scenarios, 0 failed.

## @karmicsoft/lc-schema

### 0.1.3
- **Nested display labels — dotted paths on the same flat map.** `opts.labels`
  keys now address the structure instead of mirroring it: `'daterange.startDay'`
  labels a field inside an object, the container keeps its own key (`daterange`),
  and an **objectlist child skips the index** (`'addresses.role'` labels that
  field in *every* item). A scalar list item is `'<list>.value'`. Anything
  unlisted falls back to the auto-label, as before.
- **`fromSveltiaConfig(config, { labels })`** takes the same map — an i18n
  overlay that wins over the config's own `label:`, so translations live per
  locale instead of forking `config.yml`. Additive: called with one argument it
  behaves exactly as 0.1.2 (guarded by a scenario).
- **Astro doc warning.** A generic wrapper around `reference()` makes content
  types circular and collapses inference (231 errors at an integrator's). The
  supported pattern is inline: `reference('periods').describe('relation:periods')`.

### 0.1.2
- **`fromZod` unwraps a wrapped collection root.** A collection whose root is
  `z.preprocess(fn, z.object(...))` / effects / `.default()` (the Sveltia-null
  pattern) now compiles to its **fields** instead of **zero fields silently**.
  Verified on Zod 3 (`ZodEffects`) and Zod 4 (`ZodPipe`).
- **Fails loud on a bad root.** A non-object root (a bare `z.string()`, etc.) or a
  function-form `image()` schema now **throws** a clear, actionable error instead
  of producing an empty form.
- **Display-label / i18n channel.** `fromZod(schemas, { labels })` takes a map
  keyed `{ collection: { field: 'Label' } }` (load per locale). Precedence:
  `opts.labels` → a `.describe('label:…')` directive → the prettified field name.
- **Prettified fallback splits camelCase** too: `startDay` → "Start Day".
- Additive and backward-compatible; `fromSveltiaConfig` unchanged.

### 0.1.1
- **`fromZod(schemas)`** — compile runtime Zod object schemas (Astro content
  collections) into the same neutral IR. Version-tolerant (Zod 3 & 4). Relations
  via `.describe('relation:coll')`; `markdown`/`image`/`text` via `.describe(...)`.
  `fromSveltiaConfig` still works — both readers emit the same IR.
- **Relicensed MIT** (© 2026 KarmicSoft).

### 0.1.0
- Sveltia/Decap `config.yml` → neutral IR (`fromSveltiaConfig`, `widgets`, `collections`).
- Widget mappings: string, text, number, boolean, select, relation, list,
  objectlist, object, markdown, image, file, hidden.
- TypeScript types; 14-scenario BDD suite.
