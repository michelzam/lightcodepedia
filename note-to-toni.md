# Note to Toni — Incremental optimization of Rev 2

Hi Toni,

Michel pointed me at your Rev 2 architecture doc and asked me to pressure-test his "make the migration incremental" intuition against it. I did the analysis; he just steered. Here's what came out — **at constant stack**. I'm not touching your choices (YAML-in-git, Zod/JSON-Schema, Sveltia, Meilisearch, Astro, the Node guide service, Claude). I'm only changing the **sequencing**.

## The core finding

Your 13–19 week estimate (§9) blends two clocks that don't share a unit:

1. **Engineering-build time** — schemas, migration script, frontend, search index. Compressible with the AI-assisted codegen you already assume in §11.
2. **Editorial review throughput** — the "long tail of manual correction" across 18,000 fiches (§8). This is *not* developer time, but §9 prices it as if it were.

That's why your own "two developers → ~2.5 months" barely helps: a second dev can't review fiches faster. Your real launch date is gated by review, not by build.

## Rev 2 as written vs. the incremental version — same components, different order

| Dimension | Rev 2 as planned | Incremental |
|---|---|---|
| First public page live | Week 13–19 (after full review, §8) | **~Week 1** (one arrondissement, end-to-end) |
| Launch model | Big-bang, whole corpus at once | **Progressive, arrondissement by arrondissement** |
| Data-quality risk (your §8 #1 risk) | Surfaces ~week 10, deep in the project | **Surfaces day 5**, on the first slice |
| Search at launch | Meilisearch VPS (EUR 10–30/mo, §5.2) | **Pagefind** (static, EUR 0); Meilisearch added only when faceting/geo demands it |
| Walking guide at launch | On-demand runtime: Node service + quota + cache + per-IP caps + split-model routing (§5.3) | **Pre-baked editorial walks only** (zero runtime, zero marginal cost) — the §5.3 runtime deferred to post-launch |
| Guide AI routing | Mistral/Groq for parse + Claude for narration, behind a provider abstraction (§5.3) | **Single provider**: Claude Haiku (`claude-haiku-4-5`, $1/$5 per 1M) for parse + Claude for narration. Drop the abstraction |
| Launch infra cost | EUR 20–60/mo (§5.2) | **~EUR 0–10/mo** |
| Always-on runtime at launch | Meilisearch + Node service | **None** (static site) |
| Features shipped | All | **All** — nothing cut, the heavy pieces just arrive *after* launch instead of gating it |

## Revised timeline (your stack)

| When | Work | On launch path? |
|---|---|---|
| **W1** | Vertical slice: one arrondissement end-to-end — schemas + migration script + BAN geocoding + Astro render + Pagefind search → deployed | ✅ |
| **W2–3** | Harden the migration script on the real (messy) data the slice exposes; CI integrity scan; stand up Sveltia | ✅ |
| **W4–5** | Faceted index pages + map island; add Meilisearch only if needed | ✅ |
| **W6–7** | Pre-baked walking guides as editorial content — the headline feature, no runtime | ✅ |
| **W3–8 (parallel)** | Migration + arrondissement-by-arrondissement review, launching progressively | runs alongside |
| **Post-launch** | On-demand guide runtime, quota/cache, save-time AI hooks — funded by real traffic | ❌ deferred |

Net: engineering-build drops to **~6–8 weeks**, decoupled from review throughput, with the first arrondissement live in roughly a week instead of after three to five months.

## How I can help you directly — no intermediary needed

Since you already run Claude Code: point a session at your repo and I can build this with you, autonomously, in-session:

- generate the Zod/JSON schemas and the CI integrity scan (your §11 list — these are squarely in scope);
- write the XWiki export + migration script (`ruamel.yaml`) and **iterate it against your real XWiki data** until the long tail is mechanically handled — the part §11 says needs a human, I can do the loop and surface only the genuine semantic edge cases;
- stand up the BAN geocoding pipeline, the Astro Content Collections + page templates, the Sveltia `config.yml`, and the Pagefind index;
- and deliver the **one-arrondissement vertical slice as a deployable PoC in a single session** — so you can see the real data, the real timeline, and the real simplifications before committing to the full plan.

That last point is the whole argument: a slice generated in an afternoon will tell you more about your true delays and risks than any estimate. Start a session on your repo, ask for the slice, and we'll have something live to look at.

Best,
**Claude Code**
