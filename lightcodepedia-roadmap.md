# lightcodepedia — what remains to add (and why I need it anyway)

Framing: the parisrev encyclopedia is not a special project requiring a special stack.
It's the first **real corpus** that forces capabilities I'd add to lightcodepedia regardless.
Everything below is a reusable platform component — parisrev is just the proving ground.

---

## Already running (no work needed)

| Capability | Where | Notes |
|---|---|---|
| Build + deploy | GitHub Pages / Jekyll + Actions | Free, zero-config, zero VPS |
| In-page CMS | `docs/_includes/edit_on_github.md` | Blocks + raw editor, PAT auth, GitHub API save, build watcher, history. No separate admin app |
| Map | `docs/components/map.md` | Leaflet + OSM, no API key, CSV markers + popups, `lat/lng/zoom/height`. Already Paris |
| Data-by-API | `datagrid_file.md` + `*_file` family | Pulls `.csv/.json/.yaml` from `raw.githubusercontent` (live) or jsDelivr CDN @ build SHA; `filter`, `detail_of`, `src=` escape hatch. Corpus can live in its own repo |
| Structured tables | datagrid (AG Grid) | Sorting, filtering, detail views |
| Other content blocks | cards, charts, carousel, quiz, slides, tabs, accordion, agent, code | Useful for fiche pages and indexes |

So the CMS, the host, the map, and decoupled data already exist. What's missing is the
encyclopedia-specific glue — and each piece is generally useful.

---

## What remains to add

| # | Capability | What to build | Also useful beyond parisrev |
|---|---|---|---|
| 1 | **Structured-field schema + CI** | A front-matter/data convention for entities (person, event, address…) + a CI validation check + cross-reference integrity scan | Any structured lightcodepedia corpus; catches broken refs platform-wide |
| 2 | **Map from external data** | A `map_file` component (analogous to `datagrid_file`): markers sourced from a data file/API, click-through to the fiche page | Any data-driven map, not just parisrev |
| 3 | **Faceted browse at scale** | Index pages that filter a large external dataset by field (theme / period / arrondissement) — building on datagrid filtering + data-by-API | Any large catalog/index on the platform |
| 4 | **Static full-text search** | Pagefind (or lunr) over the built site | Every lightcodepedia site benefits; zero runtime |
| 5 | **Itinerary / route on the map** | Ordered stops + drawn pedestrian route. Either pre-stored GeoJSON authored once, or an OSRM/GraphHopper call | A reusable "tour/route" map mode — guided tutorials, trails, any sequence-of-places |
| 6 | **Walk/tour content type** | A page convention (ordered stops + map + narration) authorable in the in-page editor | Generic "itinerary" component; pairs with #5 |
| 7 | **(Later) On-demand generation** | The Claude pipeline (parse query → candidate pool → narrate → route). Single provider: Haiku for parse, Claude for narration. Could ride the existing `agent` component | An AI-backed generator over any corpus — reuses your agent block |

Items **1–4** are the encyclopedia foundation and are broadly useful today.
**5–6** are the one genuinely new area (routing/itineraries) — also a clean reusable component.
**7** is deferrable and shared with any stack.

---

## Suggested order

1. **Schema + CI (#1)** and **static search (#4)** — platform hygiene, small, immediately useful.
2. **`map_file` (#2)** + **faceted browse (#3)** — turns a corpus-in-a-repo into a browsable, mapped encyclopedia. This is the vertical slice: one arrondissement, end-to-end, on lightcodepedia.
3. **Itinerary/route (#5)** + **walk content type (#6)** — the headline feature, pre-baked first (no runtime).
4. **On-demand generation (#7)** — only once there's real traffic to justify it.

The corpus itself lives in its own repo and is edited through the same in-page editor pointed at it — no new CMS, no new host, no new bill. Each step lands a component the platform keeps.
