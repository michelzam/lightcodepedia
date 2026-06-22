# 🌤️ Live weather (API)

A 7-day forecast pulled **live** from the free [Open-Meteo](https://open-meteo.com) API — no key, no server, no copy-paste. The `.dataset` fetches the URL; `path="daily"` digs into the nested response and the parallel arrays are zipped into one row per day.

[Open-Meteo — Paris, 7 days](https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone=auto&forecast_days=7)
{: .dataset #weather path="daily" }

[Forecast](#)
{: .datagrid source="weather" }

[Daily max temperature](#)
{: .chart source="weather" type="line" x="time" y="temperature_2m_max" title="Max °C" }

[Rain](#)
{: .chart source="weather" type="bar" x="time" y="precipitation_sum" title="Precipitation (mm)" }

## How it works

- `{: .dataset #weather path="daily" }` on a link fetches the API and walks into the `daily` object.
- That object is **columnar** (`time: [...]`, `temperature_2m_max: [...]`) — the dataset zips equal-length arrays into one row per day automatically.
- A grid and two charts bind to `weather` with `source=`, exactly like a local dataset.

````markdown
[Open-Meteo — Paris](https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&daily=temperature_2m_max,temperature_2m_min&timezone=auto)
{: .dataset #weather path="daily" }

[Forecast](#)
{: .datagrid source="weather" }
````

> Live data — the numbers change with the real forecast, and the API is a public service that can rate-limit or change shape.
{: .speaker-note }
