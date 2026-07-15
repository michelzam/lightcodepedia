/*!
 * gen-includes — SSOT bridge. The canonical YAML round-trip lives ONCE, in
 * @karmicsoft/lc-serialize (packages/lc-serialize/index.js). The Jekyll site
 * can't import ESM+bare-specifier at runtime (no build step), so this script
 * GENERATES the browser include docs/_includes/yaml_io.md from that single
 * source — same algorithm, wrapped as window.lcYaml. Packages stay immutable
 * (HANDOVER §5); the include is a generated artifact, never hand-edited.
 *
 *   node packages/gen-includes.mjs         # regenerate
 *   node packages/gen-includes.mjs --check # fail if the include has drifted
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'packages/lc-serialize/index.js');
const OUT = join(ROOT, 'docs/_includes/yaml_io.md');

function build() {
  // Take the canonical module and neutralize its module system for the browser:
  //  - drop the `import yaml from 'js-yaml'` (browser uses window.jsyaml)
  //  - drop `export` so the functions are local to the IIFE
  //  - resolve the one yaml.* call against window.jsyaml
  const body = readFileSync(SRC, 'utf8')
    .replace(/^import\s+yaml\s+from\s+['"]js-yaml['"];?\s*$/m, '')
    .replace(/^export\s+/gm, '')
    .replace(/yaml\.load\(text,\s*\{\s*schema:\s*yaml\.CORE_SCHEMA\s*\}\)/g,
             'window.jsyaml.load(text, { schema: window.jsyaml.CORE_SCHEMA })')
    .trim();

  const indented = body.split('\n').map((l) => (l ? '  ' + l : l)).join('\n');

  return `<!-- Generated from @karmicsoft/lc-serialize — MIT, © 2026 KarmicSoft. DO NOT EDIT (run: node packages/gen-includes.mjs). -->
{%- comment -%}
lcYaml — GENERATED from packages/lc-serialize/index.js (the SSOT). DO NOT EDIT BY
HAND; run \`node packages/gen-includes.mjs\` to regenerate. The canonical YAML
round-trip lives once, in @karmicsoft/lc-serialize; this exposes it to the
browser as window.lcYaml (load / dump(obj, order) / ready + roundtrip / isLossless).
Not a component (registers no upgrader). Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window.lcYaml) return;
  "use strict";

  var _q = null;
  function ready(cb) {
    if (window.jsyaml) { cb(); return; }
    if (_q) { _q.push(cb); return; }
    _q = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js";
    s.onload = function () { var q = _q; _q = null; q.forEach(function (f) { f(); }); };
    s.onerror = function () { _q = null; if (window.console) console.warn("[lcYaml] js-yaml CDN failed"); };
    document.head.appendChild(s);
  }

  /* ─── canonical body, generated from @karmicsoft/lc-serialize ──────────── */
${indented}

  // dump(obj, order) shim keeps the site's call sites (lcYaml.dump(rec, null)),
  // adapting to the package's dump(obj, { order }).
  window.lcYaml = {
    load: load,
    dump: function (obj, order) { return dump(obj, order ? { order: order } : {}); },
    ready: ready,
    roundtrip: roundtrip,
    isLossless: isLossless
  };
})();
</script>
`;
}

const generated = build();
if (process.argv.includes('--check')) {
  const current = readFileSync(OUT, 'utf8');
  if (current !== generated) {
    console.error('DRIFT: docs/_includes/yaml_io.md is out of sync with packages/lc-serialize.\nRun: node packages/gen-includes.mjs');
    process.exit(1);
  }
  console.log('OK: yaml_io.md is in sync with lc-serialize.');
} else {
  writeFileSync(OUT, generated);
  console.log('Wrote docs/_includes/yaml_io.md from packages/lc-serialize/index.js');
}
