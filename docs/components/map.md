# 🗺️ Map

An interactive Leaflet map with optional markers. CSV in a fenced block — one row per pin. Pan, zoom, click markers for popups.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
name,lat,lng
Parc des Buttes-Chaumont,48.8787,2.3828
Jardin du Luxembourg,48.8462,2.3372
Bois de Vincennes,48.8333,2.4333
Parc de la Villette,48.8938,2.3928
Parc Monceau,48.8793,2.3093
Parc de Bercy,48.8369,2.3832
```
{: .map lat="48.86" lng="2.35" zoom="12" height="380" }

Click a marker to see the park name. Scroll to zoom. Drag to pan.

> This is the Paris dog-walking map from `tutorial101.yaml` — same dataset, now interactive in the browser.
> Ask: "Which park is closest to the centre of Paris?"
{: .speaker-note }

**Q:** You click a marker. What appears?

- [ ] Nothing — markers are decorative dots.
- [x] A popup with the name from the CSV `name` column.
- [ ] The marker bounces but no popup appears.
- [ ] The page navigates to a new URL.
{: .quiz }

## 🛠️ How to make one

CSV with `name,lat,lng` columns, `{: .map }` IAL — plus `lat=`, `lng=`, `zoom=` to set the initial view:

````markdown
```
name,lat,lng
Eiffel Tower,48.8584,2.2945
Notre-Dame,48.8530,2.3499
```
{: .map lat="48.855" lng="2.32" zoom="14" }
````

The fenced block rows become map markers. An empty fenced block (no rows after the header) gives you a clean map with no pins.

**Q:** You want a map centred on New York (lat 40.71, lng -74.01) with no markers. What do you write in the fenced block?

- [ ] Leave the block completely empty — no header row needed.
- [x] Just the header row `name,lat,lng` with no data rows — markers are optional.
- [ ] Write `none` as the only row.
- [ ] You cannot render a map without at least one marker.
{: .quiz }

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `lat="N"` | `48.86` | Initial map centre latitude |
| `lng="N"` | `2.35` | Initial map centre longitude |
| `zoom="N"` | `12` | Initial zoom level (1 = world, 18 = street) |
| `height="N"` | `350` | Map height in pixels |

**Street-level zoom on the Eiffel Tower:**

```
name,lat,lng
Eiffel Tower,48.8584,2.2945
```
{: .map lat="48.8584" lng="2.2945" zoom="16" height="300" }

**Q:** You set `zoom="3"`. What does the map show?

- [ ] An error — zoom must be between 10 and 18.
- [ ] A street-level view of the default lat/lng.
- [x] A continent-scale view — zoom 3 is very zoomed out.
- [ ] The zoom attribute is ignored — it always starts at 12.
{: .quiz }

## 🌐 Tiles and attribution

The map uses OpenStreetMap tiles, free to use with the required attribution shown at bottom-right. The © OpenStreetMap contributors notice is added automatically.

**Q:** Which of these are TRUE about the map widget? (Pick all that apply.)

- [x] Tiles come from OpenStreetMap — free, no API key needed.
- [x] Attribution is added automatically and cannot be removed.
- [x] An empty CSV (header row only) renders a clean map with no markers.
- [ ] You must supply at least one marker or the widget throws an error.
- [x] `zoom=` controls the initial view; the user can zoom interactively.
{: .quiz multi="true" }

## 🏁 Final exam

**Q:** You want to embed a map of London (lat 51.51, lng -0.13) at zoom 13, with two pubs marked. Which IAL?

- [ ] `{: .map center="51.51,-0.13" zoom="13" }`
- [x] `{: .map lat="51.51" lng="-0.13" zoom="13" }`
- [ ] `{: .map location="London" zoom="13" }` — name-based geocoding.
- [ ] `{: .leaflet lat="51.51" lng="-0.13" zoom="13" }`
{: .quiz }

