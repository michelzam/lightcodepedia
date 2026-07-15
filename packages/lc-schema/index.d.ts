/**
 * @karmicsoft/lc-schema — schema → neutral IR → widget definitions.
 * © KarmicSoft — LightCode.
 */

export const IR_VERSION: string;

export interface IROption { label: string; value: unknown; }

export interface IRField {
  name: string;
  label: string;
  /** string | text | number | boolean | select | relation | list | objectlist | object | markdown | image | file | hidden */
  widget: string;
  required?: boolean;
  hint?: string;
  default?: unknown;
  /** select / relation */
  multiple?: boolean;
  /** select */
  options?: IROption[];
  /** relation */
  collection?: string;
  valueField?: string;
  displayField?: string;
  searchFields?: string[];
  /** object / objectlist */
  fields?: IRField[];
  /** list of scalars */
  item?: IRField;
}

export interface IRCollection {
  name: string;
  label: string;
  folder?: string;
  extension?: string;
  identifier?: string;
  slug?: string;
  fields: IRField[];
}

export interface IR {
  irVersion: string;
  source: string;
  collections: IRCollection[];
}

/** Compile a Sveltia/Decap config.yml (string or parsed object) into the neutral IR. */
export function fromSveltiaConfig(config: string | object): IR;

/**
 * Compile runtime Zod object schemas (Astro content collections) into the same IR.
 * `schemas` is a map `{ name: zObject | { schema } }` or an array `[{ name, schema }]`.
 * Version-tolerant (Zod 3 & 4). A collection whose root is wrapped in
 * `z.preprocess(...)` / effects / default is unwrapped to the `z.object` before
 * reading fields; a non-object root (or a function-form `image()` schema) throws
 * a clear error rather than compiling to zero fields.
 *
 * Widgets & relations come from `.describe()` directives, pipe-separated:
 *   `.describe('relation:periods')`  — a relation (a `z.array` of it → multiple)
 *   `.describe('markdown' | 'image' | 'text')` — rich-text / media widgets
 *   `.describe('label:Époque | text')` — an inline display label + a widget
 *
 * Display labels resolve by precedence: `opts.labels` (i18n, per active locale) →
 * a `label:` directive → the prettified field name (`startDay` → "Start Day").
 * `opts.labels` is keyed `{ collectionName: { fieldName: 'Label' } }`.
 */
export function fromZod(
  schemas: Record<string, any> | Array<{ name: string; schema?: any }>,
  opts?: { labels?: Record<string, Record<string, string>> }
): IR;

/** The flat field list for one collection (throws if the collection is unknown). */
export function widgets(ir: IR, collectionName: string): IRField[];

/** All collection names in the IR. */
export function collections(ir: IR): string[];
