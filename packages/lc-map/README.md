# @karmicsoft/lc-map

**Headless map view model.** The math a map island needs — bounds, centre, zoom —
with **no map library and no DOM**. Hand the answer to MapLibre, Leaflet, or
whatever you like: swapping the renderer changes nothing here.

```sh
npm i @karmicsoft/lc-map
```

```js
import { view } from '@karmicsoft/lc-map';
import { geoPoints } from '@karmicsoft/lc-record';

const { markers, center, zoom, bounds, empty } = view(geoPoints(record, index), { width: 640, height: 400 });
if (!empty) map.jumpTo({ center: [center.lon, center.lat], zoom });
```

| | |
|---|---|
| `markers(points)` | normalize to `{lat, lon, label}` — `lng`/`lon` both accepted |
| `bounds(points)` | tightest box, or `null` |
| `center(points)` | box centre, or `null` |
| `view(points, opts)` | everything at once: `{markers, bounds, center, zoom, empty}` |

**Three decisions.** Junk is **dropped, not plotted** — a point without finite,
in-range coordinates would otherwise land off the coast of Africa. The centre is
the **box centre, not the average**, so one outlier can't drag the view. A
**single point has no box**, so it gets `pointZoom` (default 14) instead of a
meaningless fit.

Zoom is standard Web-Mercator tile math (256px tiles), so the number means the
same thing to MapLibre and Leaflet.

MIT © KarmicSoft
