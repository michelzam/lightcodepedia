/**
 * @karmicsoft/lc-serialize — faithful YAML round-trip for git-backed content.
 * © KarmicSoft — LightCode.
 */

/** Parse YAML with the CORE schema so unquoted dates stay strings (no timestamp coercion). */
export function load(text: string): any;

/** The leading comment/blank block before the first data line, verbatim (or ""). */
export function leadingComments(text: string): string;

/**
 * Serialize a value to block-style YAML, preserving the object's own key order
 * (minimal git diffs). `order` = explicit key order; `leading` = a comment block
 * (from leadingComments) to re-emit above the data. dump(obj) alone is unchanged.
 */
export function dump(obj: any, opts?: { order?: string[]; leading?: string }): string;

/** load() → dump(): the round-trip a corpus CI uses to prove non-loss. */
export function roundtrip(text: string): string;

/** True when roundtrip(text) === text. Holds for canonical block-style YAML. */
export function isByteIdentical(text: string): boolean;

/** True when the parsed data survives a round-trip (order-independent). The contract. */
export function isLossless(text: string): boolean;
