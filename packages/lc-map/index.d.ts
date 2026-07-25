/** Brick contract version. */
export declare const MAP_VERSION: string;

export interface Point { lat: number; lon?: number; lng?: number; label?: string; title?: string; slug?: string; }
export interface Marker { lat: number; lon: number; label: string; }
export interface Bounds { north: number; south: number; east: number; west: number; }

/** Normalize to `{lat, lon, label}`; points without finite, in-range coordinates are dropped. */
export declare function markers(points: Point[]): Marker[];
/** Tightest box over every point, or null when there is nothing to show. */
export declare function bounds(points: Point[]): Bounds | null;
/** Centre of the bounding box (not the average — one outlier cannot drag the view). */
export declare function center(points: Point[]): { lat: number; lon: number } | null;

export interface View {
  markers: Marker[];
  bounds: Bounds | null;
  center: { lat: number; lon: number } | null;
  /** Web-Mercator zoom fitting the box in the viewport; null when empty. */
  zoom: number | null;
  empty: boolean;
}
/** The whole view model in one call. opts: {width=640,height=400,padding=24,maxZoom=18,pointZoom=14}. */
export declare function view(points: Point[], opts?: {
  width?: number; height?: number; padding?: number; maxZoom?: number; pointZoom?: number;
}): View;
