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

## @karmicsoft/lc-schema

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
