{%- comment -%}
Rouge syntax-highlight theme.

kramdown/Rouge already tokenises every fenced code block (```python, ```yaml,
```json, ```bash, …) into <span class="k|s|c|nf|…"> server-side — but the site
ships no colour theme, so plain code blocks render monochrome. This stylesheet
just paints those tokens: no JS, no per-language loading, every language at once.

Palette matches the .run editor (GitHub-light) for consistency. Scoped to
.markdown-body so it can't touch editor chrome. The live previews (mdpad / the
editor) render with marked, which emits no Rouge tokens, so this doesn't apply
there — that path would need Prism, which is a separate, JS-based concern.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}
<style>
/* comments */
.markdown-body .highlight :is(.c, .ch, .cm, .cp, .cpf, .c1, .cs) { color: #6e7781; font-style: italic; }
/* keywords / keyword-operators / constants like True·None */
.markdown-body .highlight :is(.k, .kc, .kd, .kn, .kp, .kr, .kt, .ow) { color: #cf222e; }
/* strings */
.markdown-body .highlight :is(.s, .sa, .sb, .sc, .dl, .sd, .s2, .se, .sh, .si, .sx, .sr, .s1, .ss) { color: #0a3069; }
/* numbers */
.markdown-body .highlight :is(.m, .mb, .mf, .mh, .mi, .mo, .il) { color: #0550ae; }
/* functions, classes, builtins, decorators */
.markdown-body .highlight :is(.nf, .nb, .nc, .nd, .bp, .ne, .fm) { color: #8250df; }
/* yaml / json keys, tags, attributes */
.markdown-body .highlight :is(.na, .nt) { color: #0550ae; }
/* operators & punctuation */
.markdown-body .highlight :is(.o, .p) { color: #24292f; }
/* don't paint a red box on tokens the lexer is unsure about */
.markdown-body .highlight .err { color: inherit; background: none; }
</style>
