/**
 * @karmicsoft/lc-patch — minimal-diff writer for git-backed YAML records.
 * © KarmicSoft — LightCode.
 */

export const PATCH_VERSION: string;

/**
 * Original file text + edited object → new text. Every line the edit did not
 * touch is kept byte for byte (quoting, flow lists, number formatting,
 * comments, CRLF, the leading provenance block). Only changed, added or
 * removed entries are re-emitted, with lc-serialize's emitter. Lossless:
 * load(patch(text, edited)) deep-equals `edited`.
 */
export function patch(originalText: string, edited: any, opts?: {}): string;

/** The result of a patch. */
export interface PatchResult {
  /** The new file text. */
  text: string;
  /** Dotted paths that were re-emitted, e.g. "workflow.reviewRequested", "professions[2]", "aka (added)". */
  changed: string[];
  /** True when the structural reader gave up and the text is a full lc-serialize re-emit (still lossless). */
  fallback: boolean;
  /** Why it fell back, when it did. */
  reason: string;
}

/** Same as patch(), with the story of what was re-emitted and whether it fell back. */
export function patchWith(originalText: string, edited: any, opts?: {}): PatchResult;

/** 0-based indexes of the lines of `text` that differ from `original`. */
export function changedLines(original: string, text: string): number[];
