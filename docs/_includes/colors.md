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
.markdown-body .red, .markdown-body .green, .markdown-body .blue,
.markdown-body .amber, .markdown-body .muted, .markdown-body .hl {
  font-style: inherit; font-weight: inherit;   /* carrier *…* / **…** ⇒ plain colour */
}
.markdown-body .red   { color: #c0392b; }
.markdown-body .green { color: #2e7d32; }
.markdown-body .blue  { color: #1565c0; }
.markdown-body .amber { color: #b45309; }
.markdown-body .muted { color: #6b7280; }
.markdown-body .hl    { background: #fff3a3; border-radius: 3px; padding: 0 0.22em; }
</style>
