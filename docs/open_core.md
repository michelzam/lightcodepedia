---
sitemap: false
---

# ⚖️ Licensing — open core

LightCode is **open core**: the engine bricks are MIT, the platform around them
is licensed. Two layers, two licences, no ambiguity.

## The open layer — MIT

Published on npm under `@karmicsoft`, © 2026 KarmicSoft, **MIT**. Permissive:
use them anywhere, commercially, fork them if we ever stop maintaining them.
Each package ships its own `LICENSE` and declares it in `package.json`.

| Brick | Role |
|---|---|
| `@karmicsoft/lc-serialize` | Faithful YAML round-trip (key order, dates-as-strings, block scalars, null) |
| `@karmicsoft/lc-schema` | Schema → neutral IR → widget descriptors |
| `@karmicsoft/lc-record` | Headless record engine: fields, controls, relations, edits, emit |
| `@karmicsoft/lc-map` | Headless map view model (projection, zoom, markers) |
| `@karmicsoft/lc-suggest` | Suggestions as data — candidates, payload, apply |

They are **headless**: data in, data out, no DOM, no framework, no network.
That is what makes them safe to open — and useful to anyone building their own
UI on top.

## The closed layer — LightCode Platform License

The platform itself — the runtime includes, the page editor, the components,
the classroom, benches, roles, publishing gates — stays under the
[LightCode Platform License](/license) (educational and partner use; commercial
deployment by agreement).

## Why open core

- Partners and integrators can build on the bricks without asking anyone.
- The bricks get real external use, so their APIs get honest pressure.
- The value we sell is the platform experience, not the parsers underneath.

The line is **movable, by choice**: any layer can be opened later if opening it
serves adoption more than holding it does. MIT is the default we reach for when
that happens.

Commercial licensing, on-premise deployment, partnership:
[sales@karmicsoft.com](mailto:sales@karmicsoft.com).
