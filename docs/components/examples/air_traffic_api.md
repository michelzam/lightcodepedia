# ✈️ Live air traffic (API)

Aircraft currently in the sky near Paris, pulled **live** from the free [adsb.lol](https://adsb.lol) API (a community network of ADS-B receivers) — no key. `path="ac"` lifts the aircraft array out of the response; a query renames a handful of the ~30 raw fields into readable columns.

[adsb.lol — within 25 nm of Paris](https://api.adsb.lol/v2/lat/48.85/lon/2.35/dist/25)
{: .dataset #flights path="ac" }

```sql
SELECT flight AS callsign, t AS type, alt_baro AS altitude_ft, gs AS speed_kts, track AS heading
FROM flights WHERE flight <> '' ORDER BY altitude_ft DESC
```
{: .query source="flights" #nearby }

[Aircraft overhead](#)
{: .datagrid source="nearby" rows="20" }

## How it works

- `{: .dataset #flights path="ac" }` on a link fetches the API and extracts the `ac` array — one object per aircraft.
- `{: .query source="flights" }` selects and renames a few columns and drops aircraft with no callsign.
- The grid binds with `source="nearby"`, sorted by altitude.

> Live data: how many planes appear depends on real traffic — quiet hours may show only a handful, busy ones dozens. adsb.lol is a free community API and can rate-limit.
{: .speaker-note }
