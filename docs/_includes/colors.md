{%- comment -%}
Inline colour utilities for content authors.

Markdown has no colour syntax; these classes let an author tint a word with a
kramdown span IAL — no HTML, no CSS to write:

    *danger*{: .red}   **whole phrase**{: .green}   `v2`{: .blue}

The `*…*` / `**…**` is just the IAL carrier (kramdown span IALs must follow an
inline element); the colour classes neutralise the emphasis, so it reads as
plain coloured text. Scoped to .markdown-body so it can't bleed into the editor
or platform chrome. Documented live in /components/text.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}
<style>
/* rendered-markdown surfaces: page content (incl. mdpad / section widgets,
   which nest inside it) plus the editor's live-preview panes */
:is(.markdown-body, #ed-preview, #ed-feat-preview) :is(.red, .green, .blue, .amber, .muted, .hl) {
  font-style: inherit; font-weight: inherit;   /* carrier *…* / **…** ⇒ plain colour */
}
:is(.markdown-body, #ed-preview, #ed-feat-preview) .red   { color: #c0392b; }
:is(.markdown-body, #ed-preview, #ed-feat-preview) .green { color: #2e7d32; }
:is(.markdown-body, #ed-preview, #ed-feat-preview) .blue  { color: #1565c0; }
:is(.markdown-body, #ed-preview, #ed-feat-preview) .amber { color: #b45309; }
:is(.markdown-body, #ed-preview, #ed-feat-preview) .muted { color: #6b7280; }
:is(.markdown-body, #ed-preview, #ed-feat-preview) .hl    { background: #fff3a3; border-radius: 3px; padding: 0 0.22em; }
</style>
