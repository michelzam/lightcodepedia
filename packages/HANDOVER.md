# LightCode bricks — socle handover (for Toni & his Claude Code)

© KarmicSoft — LightCode. Two packages, ready to integrate: **`@karmicsoft/lc-serialize`**
and **`@karmicsoft/lc-schema`**. This is the *socle* your parcours (§5.1) starts from.

---

## 1. What you're getting

| Package | Role | Status |
|---|---|---|
| `@karmicsoft/lc-serialize` | Faithful YAML round-trip (key order, dates-as-strings, `\|`/`\|-`/`\|+`, null) | **verified** (byte-identical on canonical block YAML) |
| `@karmicsoft/lc-schema` | Schema → neutral IR → widgets (schema compiler) | v0.1 (Sveltia `config.yml` reader) |

Each ships its **`LICENSE`** and an **example** (`example.yaml`, `example.config.yml`), and
declares the license in `package.json` — as you asked. Full API in each package's `README.md`.

## 2. How to install

Final form (once published): `npm install @karmicsoft/lc-serialize @karmicsoft/lc-schema`.

Until they're on npm, two interim routes that **respect the immutable-runtime contract**
(you don't vendor or edit the source):

- **tarball**: `npm pack` in each package dir → `npm i ./karmicsoft-lc-serialize-0.1.0.tgz`;
- **git**: publish each package to its own repo/tag and `npm i git+https://…#v0.1.0`.

Pin the version either way. Michel does the `npm publish` to `@karmicsoft`; nothing to build on your side.

## 3. Integrate (your parcours, unchanged)

1. **Socle** — install both, pinned. Derive your lc schema from your `config.yml`:
   ```js
   import { fromSveltiaConfig, widgets } from '@karmicsoft/lc-schema';
   const ir = fromSveltiaConfig(readFileSync('poc/public/admin/config.yml', 'utf8'));
   ```
2. **Corpus safety net (CI)** — round-trip all ~56 000 files. Assert **`isLossless`** (must be 0
   failures); treat byte-drift as advisory (see `lc-serialize/README.md` § Scope). Recipe is in that README.
3. **Visible bricks** — `lc-map` + `lc-suggest` as islands on fiches (next deliverables).
4. **Editor pilot** — `lc-editor` on a trial route for one type, to compare with Sveltia.

## 4. SSOT — one schema, your call (reversible)

You currently maintain **two** descriptions of the same model: `config.yml` (Sveltia) **and**
`content.config.ts` (Zod). The first is a **subset** of the second → hand-maintained, they **drift**
(a field added to Zod but not to `config.yml` = an incomplete form or a bypassed check).

`lc-schema` fixes this by being a compiler: **one canonical source → neutral IR → generated projections**.

- **Recommended: Zod canonical** (your build authority, the richest) → `config.yml` becomes **generated**, duplication gone.
- **Or keep `config.yml` canonical** → add a **CI consistency check** against the Zod (which carries what `config.yml` can't).

v0.1 ships the **`config.yml` reader** so you can start today; the choice is **reversible** (only the reader changes). Tell us which canonical you want.

## 5. Integration contract (accepted)

- `@karmicsoft/lc-*` = **immutable runtime**: no vendoring, no editing `node_modules`, no regenerating its source.
- **Your zone** = schema / index / endpoints (+ keys). Change your schema **whenever you want, independently** — the bricks follow it.
- **Semver** + your CI round-trip gate ⇒ **successive deploys without regression**: every `npm update` is validated automatically before merge.

## 6. Contributor auth — avoiding GitHub accounts (your open §6 point)

Writing to git from a browser needs **one** credential, so avoiding a GitHub account per
contributor has exactly two solution families: a **shared service identity behind app-level auth**
(a gateway), or **local editing** (no remote write). The paths:

| Path | The contributor… | Infra | Notes |
|---|---|---|---|
| GitHub OAuth (Sveltia today) | needs a GitHub account | none | the accepted compromise |
| **Commit gateway** (magic-link email + **one service identity / GitHub App**) | signs in by **email**, never sees GitHub | small serverless | **the target** — attributes the human via commit co-author |
| Decap-style git-gateway | invited by email | gateway service | Decap supports it; **verify Sveltia support** |
| Sveltia `local_backend` (File System Access API) | edits a **local clone**, someone pushes | none | zero-account, good for **on-site** editing, not remote/mobile |
| Proposal queue | fills a form, **no git** | small serverless | contributor writes nothing to git; an editor merges — fits draft→review→published |

**Recommendation.** The future no-account path is the **commit gateway**: email magic-link → a single
**GitHub App** identity (`contents:write` on the one repo, least-privilege, rotated) that commits on the
contributor's behalf, **enforcing "one writer per fiche"** (serialized/locked per file) and routing via
PR or direct commit per your branch policy. Deployable on **Cloudflare Workers / your QNAP** — near
zero-infra, sovereign if self-hosted. This is our **`lc-roles` (+ a thin `lc-gateway`)** brick, and it
serves Sveltia *and* `lc-editor` *and* the LightCode teaching platform (same email contributors).

**For now (Phase 1, zero new infra):** keep GitHub-account OAuth (accepted) **or** `local_backend` for
on-site editing. We build the gateway when you approach "replacement" — it's already a §6 switch criterion.

Security note: the service token is the sensitive asset → GitHub App least-privilege + rotation, the
endpoint is **auth-gated** (never an open write endpoint), writes serialized per fiche.

## 7. To settle later (not now)

When `lc-editor` starts committing: agree on the **commit-message format** and the **branch circuit**
(PR vs direct), consistent with Sveltia — the **"one writer per fiche"** rule.

---

## For your Claude Code — checklist

- [ ] `npm i @karmicsoft/lc-serialize @karmicsoft/lc-schema` (pinned). **Do not** edit `node_modules` / vendor / regenerate them.
- [ ] Build the IR: `fromSveltiaConfig(config.yml)` → cache it at build.
- [ ] Add a CI job: round-trip every `content/**/*.yaml` with `isLossless` (fail on any loss); log byte-drift as advisory.
- [ ] Generate the relations/coords **index** from `content/` at build (centroids, event-places, slugs).
- [ ] Mount `lc-map` / `lc-suggest` as islands on fiche pages once delivered.
- [ ] Keep your edits to **schema / index / endpoints** only; update bricks via `npm update`.
- [ ] Report back: chosen **canonical schema** (Zod recommended) and CI results on the 56k corpus.
