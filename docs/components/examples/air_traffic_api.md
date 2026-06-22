# ✈️ Live air traffic (API)

Military aircraft **in the air right now, worldwide**, pulled live from the free [adsb.lol](https://adsb.lol) API (a community network of ADS-B receivers) — no key. The global military feed is busy around the clock, so there's almost always something flying (a small geographic radius over one city often isn't). `path="ac"` lifts the aircraft array out of the response; a query renames a few of the ~30 raw fields.

[adsb.lol — military aircraft aloft](https://api.adsb.lol/v2/mil)
{: .dataset #flights path="ac" }

```sql
SELECT flight AS callsign, t AS type, r AS registration, alt_baro AS altitude_ft, gs AS speed_kts
FROM flights ORDER BY altitude_ft DESC
```
{: .query source="flights" #aloft }

[Aircraft aloft — sorted by altitude](#)
{: .datagrid source="aloft" rows="20" }

## How it works

- `{: .dataset #flights path="ac" }` on a link fetches the API and extracts the `ac` array — one object per aircraft.
- `{: .query source="flights" }` selects and renames a few of the raw fields.
- The grid binds with `source="aloft"`, sorted by altitude.

> Live data from a free community API: the list reflects real flights and varies minute to minute. The service can rate-limit or, occasionally, be unreachable from the browser (CORS) — if the grid shows *No data*, that's the upstream, not the wiring.
{: .speaker-note }
