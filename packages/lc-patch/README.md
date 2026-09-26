# @karmicsoft/lc-patch

**Minimal-diff writer for git-backed YAML records.** A LightCode brick.

`lc-serialize` reads and writes a whole file in its canonical style, which is
the right contract for a round-trip and the wrong one for a reviewer who reads
contributions as diffs: edit one field and, in about 1.7 % of a real corpus,
an unrelated value somewhere else gets re-quoted (`'l''opéra'` → `"l'opéra"`).

`lc-patch` keeps every line the edit did not touch, byte for byte — quoting,
flow lists, number formatting, comments, CRLF, the leading provenance block —
and re-emits only the entries that changed, with lc-serialize's own emitter.
It imports lc-serialize; it copies nothing from it.

```sh
npm i @karmicsoft/lc-patch      # depends on @karmicsoft/lc-serialize ^0.1.1
```

```js
import { load } from '@karmicsoft/lc-serialize';
import { patch, patchWith } from '@karmicsoft/lc-patch';

const text = await fs.readFile('fiches/persons/louise-michel.yaml', 'utf8');
const record = load(text);
record.addresses[0].period = 1871;

const out = patch(text, record);          // one line differs from `text`
// or, with the story:
const { text: out2, changed, fallback } = patchWith(text, record);
// changed → ['addresses[0].period'], fallback → false
```

## Contract

- `load(patch(text, edited))` deep-equals `edited`. Always.
- An untouched record is written back byte-identical.
- Only changed, added or removed entries move. Changed entries are re-emitted
  in lc-serialize style; added keys land at the end of their mapping; removed
  keys take only their own lines.
- List items are compared by position. A changed item is re-emitted; a mapping
  item (`- id: …`) is patched field by field, so one changed field is one
  changed line.
- If the structural reader meets a YAML shape it does not know (flow mappings
  as documents, complex keys…), the result is lc-serialize's full re-emit —
  still lossless, only less minimal — and `patchWith()` reports
  `fallback: true` with the reason. The brick is never wrong, only sometimes
  less minimal.

## What the reader understands

Block mappings and block sequences, at any depth; a sequence at its key's own
indent or one deeper; inline scalars with continuation lines; block scalars
(`|`, `|-`, `|+`, `>`); flow lists on one line; comments and blank lines
(they ride with the entry above them); CRLF files.

## Proof

`npm test` runs the acceptance scenarios agreed with a partner — an untouched
record written back byte-identical, one edited field is one changed line, a
provenance comment kept, wiki-style `[[links]]` untouched by an edit
elsewhere, every edit lossless — against seven real records whose SHA-256
must match their baseline first, plus nine scenarios of the brick's own. The
real records are the partner's content: they live with the lab's suite, never
in the npm package; without them the suite skips those scenarios by name.

## Scope

One document, one mapping at the root. The brick does not merge concurrent
edits, does not validate against a schema (that is `lc-schema`'s job), and
does not write files. It answers one question: *given this file and this
edited object, what is the smallest text that loads to the object?*

MIT © 2026 KarmicSoft — [lightcodepedia.org](https://lightcodepedia.org)
