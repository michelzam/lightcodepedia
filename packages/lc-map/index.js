/*!
 * @karmicsoft/lc-map — headless map view model.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * The MATH a map island needs, with no map library and no DOM: given points,
 * it answers where to look — bounds, centre, zoom. The host hands that to
 * MapLibre, Leaflet, or anything else. Swapping the renderer changes nothing
 * here; that is the point of an island being host-wired.
 *
 *   points → bounds() → view() → { center, zoom, bounds, markers }
 *
 * Feed it `geoPoints(record, index)` from @karmicsoft/lc-record, or any
 * `{ lat, lon|lng, label }` list of your own.
 */
export const MAP_VERSION = '0.1';

const isNum = (v) => typeof v === 'number' && isFinite(v);

/**
 * Accept the shapes that occur in the wild and normalize to `{ lat, lon, label }`.
 * `lng` and `lon` both work; anything without finite coordinates is dropped
 * rather than plotted at (0,0) — a marker off the coast of Africa is a bug
 * report waiting to happen.
 */
export function markers(points) {
  return (points || []).reduce((out, p) => {
    if (!p) return out;
    const lat = Number(p.lat), lon = Number(p.lon != null ? p.lon : p.lng);
    if (isNum(lat) && isNum(lon) && lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180) {
      out.push({ lat, lon, label: p.label || p.title || p.slug || '' });
    }
    return out;
  }, []);
}

/** The tightest box containing every point, or null when there is nothing to show. */
export function bounds(points) {
  const m = markers(points);
  if (!m.length) return null;
  let north = m[0].lat, south = m[0].lat, east = m[0].lon, west = m[0].lon;
  for (const p of m) {
    if (p.lat > north) north = p.lat;
    if (p.lat < south) south = p.lat;
    if (p.lon > east) east = p.lon;
    if (p.lon < west) west = p.lon;
  }
  return { north, south, east, west };
}

/** Centre of the bounding box (not the average — one outlier shouldn't drag the view). */
export function center(points) {
  const b = bounds(points);
  return b ? { lat: (b.north + b.south) / 2, lon: (b.east + b.west) / 2 } : null;
}

/**
 * Zoom that fits `b` in a `width`×`height` viewport — standard Web-Mercator
 * tile math (256px tiles), which is what every slippy map uses, so the number
 * is meaningful to MapLibre and Leaflet alike.
 */
function zoomFor(b, width, height, padding, maxZoom) {
  const w = Math.max(1, width - padding * 2), h = Math.max(1, height - padding * 2);
  const latRad = (d) => {
    const s = Math.sin((d * Math.PI) / 180);
    return Math.log((1 + s) / (1 - s)) / 2;
  };
  const latFrac = Math.abs(latRad(b.north) - latRad(b.south)) / (2 * Math.PI);
  let lonSpan = b.east - b.west;
  if (lonSpan < 0) lonSpan += 360;                       // box crossing the antimeridian
  const lonFrac = lonSpan / 360;
  const zoom = (px, frac) => (frac <= 0 ? maxZoom : Math.log2(px / 256 / frac));
  return Math.max(0, Math.min(maxZoom, Math.floor(Math.min(zoom(h, latFrac), zoom(w, lonFrac)))));
}

/**
 * The whole view model in one call:
 *   `{ markers, bounds, center, zoom, empty }`
 * A single point can't imply a zoom (its box has no size), so it gets
 * `opts.pointZoom` (default 14) — close enough to read a street.
 *
 * opts: { width=640, height=400, padding=24, maxZoom=18, pointZoom=14 }
 */
export function view(points, opts = {}) {
  const m = markers(points);
  const o = {
    width: opts.width || 640, height: opts.height || 400,
    padding: opts.padding == null ? 24 : opts.padding,
    maxZoom: opts.maxZoom == null ? 18 : opts.maxZoom,
    pointZoom: opts.pointZoom == null ? 14 : opts.pointZoom,
  };
  if (!m.length) return { markers: [], bounds: null, center: null, zoom: null, empty: true };
  const b = bounds(m), c = center(m);
  const single = b.north === b.south && b.east === b.west;
  return {
    markers: m,
    bounds: b,
    center: c,
    zoom: single ? Math.min(o.pointZoom, o.maxZoom) : zoomFor(b, o.width, o.height, o.padding, o.maxZoom),
    empty: false,
  };
}
