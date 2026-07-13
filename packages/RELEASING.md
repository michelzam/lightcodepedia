# Releasing the bricks — continuous delivery

Shipping a new version is **one small edit + a merge**. CI does the rest.

## To ship a version
1. Make your change in `packages/lc-serialize` or `packages/lc-schema`.
2. Bump that package's version in its `package.json` — the semver rule:
   - **patch** (`0.1.0 → 0.1.1`) — a bug fix, no behaviour change for callers.
   - **minor** (`0.1.0 → 0.2.0`) — something added, old code still works.
   - **major** (`0.1.0 → 1.0.0`) — a breaking change (removed/renamed API).
   Shortcut from `packages/`: `npm version patch --workspace lc-serialize` (edits
   the file for you).
3. Update `CHANGELOG.md` under that package.
4. Merge to `main`.

That's it. The **Publish LC bricks** workflow then:
- runs both BDD suites **and** the SSOT drift guard (`npm test`),
- publishes **only** the packages whose version isn't on npm yet (so re-runs are safe),
- tags the release (`lc-serialize-v0.1.1`).

If a version is unchanged, it's skipped — nothing republishes.

## One-time setup (Michel)
Add an npm **automation token** for the `@karmicsoft` org as a repo secret named
**`NPM_TOKEN`** (Settings → Secrets and variables → Actions → New secret). The
workflow uses it to publish. Nothing else to configure.

- Provenance (`--provenance`) signs each release from the workflow — keep it on for
  a public repo; if the repo is ever private, drop that flag in the workflow.

## Why this keeps Toni safe
Every published version passed the corpus-grade tests before it existed, and semver
tells him what a bump means — so `npm update` is a **no-regression** operation, exactly
the integration contract (HANDOVER §5).

## Manual publish (fallback, if ever needed)
From `packages/`, after `npm login`: `npm run publish-all`.
