/**
 * @karmicsoft/lc-serialize — faithful YAML round-trip for git-backed content.
 * © KarmicSoft — LightCode.
 */

/**
 * Read a record with the CORE schema so unquoted dates stay strings. Plain YAML,
 * or (0.2.0) Markdown with a YAML header: the header's keys, then `body` — the
 * text after the closing fence. Throws on a header that has its own `body:` key.
 */
export function load(text: string): any;

/** A Markdown file with a YAML header → { header, body }; null for any other text (0.2.0). */
export function splitFrontMatter(text: string): { header: string; body: string } | null;

/** 'md' for Markdown with a YAML header, 'yaml' otherwise (0.2.0). */
export function formatOf(text: string): 'md' | 'yaml';

/** The leading comment/blank block before the first data line, verbatim (or ""). */
export function leadingComments(text: string): string;

/**
 * Serialize a value to block-style YAML, preserving the object's own key order
 * (minimal git diffs). `order` = explicit key order; `leading` = a comment block
 * (from leadingComments) to re-emit above the data. dump(obj) alone is unchanged.
 * `format: 'md'` (0.2.0): the record without `body` as the header, `body` after it.
 */
export function dump(obj: any, opts?: { order?: string[]; leading?: string; format?: 'yaml' | 'md' }): string;

/** load() → dump(): the round-trip a corpus CI uses to prove non-loss. */
export function roundtrip(text: string): string;

/** True when roundtrip(text) === text. Holds for canonical block-style YAML. */
export function isByteIdentical(text: string): boolean;

/** True when the parsed data survives a round-trip (order-independent). The contract. */
export function isLossless(text: string): boolean;
