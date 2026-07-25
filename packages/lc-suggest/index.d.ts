/** Brick contract version, also sent in payload(). */
export declare const SUGGEST_VERSION: string;

/** A suggestion is DATA, never a closure — the same shape survives a JSON round-trip. */
export interface Suggestion {
  id: string;
  kind: 'stub' | 'relate' | 'remote' | string;
  /** the field this would set */
  field: string;
  /** the value it would set (for a multiple relation: the WHOLE new list) */
  value: unknown;
  /** human-facing one-liner */
  text: string;
  /** why it was proposed */
  reason?: string;
}

/** Local, domain-agnostic proposals. Never mutates the record. */
export declare function suggest(
  schema: any, record: Record<string, any>, index?: Record<string, any[]>,
  opts?: { kinds?: string[]; limit?: number; collection?: string }
): Suggestion[];

/** Type-ahead over the index for a relation field — the manual counterpart of `relate`. */
export declare function candidates(
  index: Record<string, any[]>, collection: string, query: string, exclude?: string[], limit?: number
): Array<{ slug: string; title?: string }>;

/** The agreed request body for a remote AI endpoint. */
export declare function payload(schema: any, record: Record<string, any>, opts?: { collection?: string }):
  { record: Record<string, any>; schema: any[]; suggestVersion: string };

/** Coerce ANY endpoint answer to Suggestion[]; junk degrades to [] and never throws. */
export declare function normalize(remote: unknown): Suggestion[];

/** Apply an ACCEPTED suggestion. Returns lc-record's `{record, structural}`. */
export declare function apply(record: Record<string, any>, suggestion: Suggestion | null):
  { record: Record<string, any>; structural: boolean };
