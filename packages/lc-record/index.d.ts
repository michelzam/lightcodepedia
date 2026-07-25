/** Engine contract version, for host compatibility checks. */
export declare const ENGINE_VERSION: string;

/** A field as the engine consumes it (an lc-schema IR field, or your own). */
export interface Field {
  name: string;
  label?: string;
  widget?: string;
  required?: boolean;
  hint?: string;
  default?: unknown;
  options?: Array<{ label: string; value: unknown }>;
  collection?: string;
  multiple?: boolean;
  fields?: Field[];
  item?: Field;
  [k: string]: unknown;
}

/** An entry in the relation index; `lat` + (`lng` | `lon`) make it mappable. */
export interface IndexEntry { slug: string; title?: string; lat?: number; lng?: number; lon?: number; }
export type RelationIndex = Record<string, IndexEntry[]>;

/** What the host should render for one field. Pure data — no DOM, no callbacks. */
export interface Control {
  name: string;
  label: string;
  widget: string;
  value?: unknown;
  required: boolean;
  hint?: string;
  default?: unknown;
  options?: Array<{ label: string; value: unknown }>;
  collection?: string;
  multiple?: boolean;
  /** relation: the resolved chips, so a host never re-does the index lookup */
  chips?: Array<{ slug: string; title: string }>;
  /** object: child controls */
  fields?: Control[];
  /** objectlist: one control set PER item; list: the raw items */
  items?: Control[][] | unknown[];
  /** objectlist: the field template behind each item */
  itemFields?: Field[];
  /** list: the item template */
  item?: Field;
  /** set when an unrecognized widget was degraded to a string control */
  degraded?: boolean;
}

/** Any accepted schema shape: an lc-schema IR, one IR collection, or a field list. */
export type SchemaInput = Field[] | { fields: Field[] } | { collections: Array<{ name: string; fields: Field[] }> };

/** Normalize any accepted schema shape to the flat field list. Throws on an unknown collection or shape. */
export declare function fields(schema: SchemaInput, collectionName?: string): Field[];

/** Describe the controls for a record — the host renders them however it likes. */
export declare function controls(
  schema: SchemaInput, record: Record<string, any>, index?: RelationIndex, collectionName?: string
): Control[];

/** Display title for a slug; falls back to the slug itself. */
export declare function relTitle(index: RelationIndex, coll: string, slug: string): string;
/** Type-ahead: prefix matches first, then substring; accent/case-insensitive; excludes picked slugs. */
export declare function relMatch(
  index: RelationIndex, coll: string, query: string, exclude?: string[], limit?: number
): IndexEntry[];

/** Every indexed point whose slug appears anywhere in the record, at any depth. */
export declare function geoPoints(record: Record<string, any>, index: RelationIndex): Array<{ lat: number; lon: number; label: string }>;

/** A mutation result: `structural` means the control set changed — rebuild the form. */
export interface MutationResult { record: Record<string, any>; structural: boolean; }
/** Set a value at a dotted path ("daterange.startDay", "addresses.0.role"). Value edit. */
export declare function setValue(record: Record<string, any>, path: string | string[], value: unknown): MutationResult;
/** Append to the list at `path` (creating it when absent). Structural. */
export declare function addItem(record: Record<string, any>, path: string | string[], item: unknown): MutationResult;
/** Remove index `i` from the list at `path`. Structural. */
export declare function removeItem(record: Record<string, any>, path: string | string[], i: number): MutationResult;

/** Parse a file into the record, its key order, and its provenance comment block. */
export declare function parse(text: string): { record: Record<string, any>; keys: string[]; leading: string };
/** The WRITE PATH: re-emit the WHOLE file (not a surgical patch). */
export declare function emit(record: Record<string, any>, opts?: { keys?: string[] | null; leading?: string }): string;
/** Did the edit drop a key that was in the file? */
export declare function integrity(record: Record<string, any>, originalKeys: string[]): {
  ok: boolean; preserved: number; lost: number; lostKeys: string[];
};
