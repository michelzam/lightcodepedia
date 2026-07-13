/**
 * @karmicsoft/lc-serialize — faithful YAML round-trip for git-backed content.
 * © KarmicSoft — LightCode.
 */

/** Parse YAML with the CORE schema so unquoted dates stay strings (no timestamp coercion). */
export function load(text: string): any;

/**
 * Serialize a value to block-style YAML, preserving the object's own key order
 * (minimal git diffs). Pass `{ order }` for an explicit canonical key order.
 */
export function dump(obj: any, opts?: { order?: string[] }): string;

/** load() → dump(): the round-trip a corpus CI uses to prove non-loss. */
export function roundtrip(text: string): string;

/** True when roundtrip(text) === text. Holds for canonical block-style YAML. */
export function isByteIdentical(text: string): boolean;

/** True when the parsed data survives a round-trip (order-independent). The contract. */
export function isLossless(text: string): boolean;
