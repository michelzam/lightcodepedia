# Changelog — @karmicsoft/lc-* bricks

Versions follow [semver](https://semver.org): **patch** = fix, **minor** =
additive / backward-compatible, **major** = breaking. Every published version
passed CI (both BDD suites + the SSOT drift guard) before release.

## @karmicsoft/lc-serialize

### 0.1.0
- Faithful YAML round-trip: preserved key order, unquoted dates kept as strings,
  `|` / `|-` / `|+` chomping, `null`, and `[]` for empty arrays.
- `isLossless` (the contract) + `isByteIdentical` (advisory) helpers.
- Corpus checker `bin` (`lc-serialize-check`) — CI gate over a whole tree.
- TypeScript types; 17-scenario BDD suite.

## @karmicsoft/lc-schema

### 0.1.0
- Sveltia/Decap `config.yml` → neutral IR (`fromSveltiaConfig`, `widgets`, `collections`).
- Widget mappings: string, text, number, boolean, select, relation, list,
  objectlist, object, markdown, image, file, hidden.
- TypeScript types; 14-scenario BDD suite.
