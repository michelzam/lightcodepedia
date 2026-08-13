{%- comment -%}
Inline style utilities for content authors — colour spans plus a banner image class.

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
/* ── Colour tokens — the SSOT for every colour a reader's eye lands on ──
   The DEFAULT block is the site's live palette (values matched to the
   literals they replace, so routing a rule through a token changes nothing
   on its own). The [data-theme="contrast"] block is the only thing the
   "High contrast" switch swaps — one attribute on <html> re-tints the whole
   reading surface, because every rule paints through these names.

   High contrast pushes ink toward black, links/borders darker and stronger
   (borders also clear the 3:1 non-text bar, WCAG 1.4.11), and flattens the
   faint tints so text sits on the cleanest possible ground. Widget chrome
   not yet tokenised keeps its literal (already ≥ AA), so the theme is
   coherent while coverage deepens widget by widget. */
:root {
  --lc-bg:          #ffffff;   /* page ground                      */
  --lc-surface:     #f8f8f8;   /* raised chrome (heads, code pre)  */
  --lc-surface-2:   #f3f4f6;   /* faint tint (table th, chips)     */
  --lc-border:      #dddddd;   /* the #ddd / #e0e0e0 border family */
  --lc-border-soft: #eeeeee;   /* hairlines (#eee / #f0f0f0)       */
  --lc-ink:         #111111;   /* body text                        */
  --lc-ink-soft:    #555555;   /* blockquotes, secondary copy      */
  --lc-ink-mute:    #616161;   /* labels, counts, gutters          */
  --lc-link:        #0066cc;   /* links (was the theme's #2a7ae2)  */
  --lc-accent:      #0066cc;   /* brand blue: rules, active states */
  --lc-accent-ink:  #0052a3;   /* accent, hover/pressed            */
}
:root[data-theme="contrast"] {
  --lc-bg:          #ffffff;
  --lc-surface:     #eef1f4;
  --lc-surface-2:   #e9edf1;
  --lc-border:      #6e6e6e;
  --lc-border-soft: #9aa1a8;
  --lc-ink:         #000000;
  --lc-ink-soft:    #2a2a2a;
  --lc-ink-mute:    #313131;
  --lc-link:        #00339a;
  --lc-accent:      #00339a;
  --lc-accent-ink:  #002270;
}
/* The switch may set the theme before this stylesheet parses; keep the page
   from flashing by having the attribute already meaningful at :root. */
:root[data-theme="contrast"] body { background: var(--lc-bg); }

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

/* a table whose FIRST column names things — a flag, a knob, a file. Kramdown
   sizes columns by content, so a narrow name wraps mid-token ("?crumb=BUILD-
   AI") while the prose column takes the room. `{: .wide_first }` under the
   table gives the first column its own line (Michel, 2026-08-13). */
:is(.markdown-body, #ed-preview, #ed-feat-preview) table.wide_first th:first-child,
:is(.markdown-body, #ed-preview, #ed-feat-preview) table.wide_first td:first-child {
  width: 16em; white-space: nowrap;
}
@media (max-width: 640px) {
  :is(.markdown-body, #ed-preview, #ed-feat-preview) table.wide_first th:first-child,
  :is(.markdown-body, #ed-preview, #ed-feat-preview) table.wide_first td:first-child {
    width: auto; white-space: normal;   /* a phone has no room to spare */
  }
}

/* ── PAPER (Michel, 2026-08-13: "export all the public pages of a module as
   pdf files"). A page printed is a DOCUMENT, not a screenshot of an app:
   nothing you could press belongs on it, and nothing may be folded away —
   a closed accordion prints as a hole. Applies to the browser's own
   Print → PDF as much as to the export workflow, which is the same engine. */
@media print {
  #lc-topbar, .lc-run-bar, .lc-edit-fab, .lc-guide, .lc-guide-ask,
  .lc-avatar-host, .lc-avatar-char, .lc-guide-seed, .lc-agent-form,
  .lc-feature-run, .lc-ps-savebar, .lc-bench-more, .lc-bench-save,
  .lc-mdpad-bar, .lc-ver-panel, .lc-mode-fab, #lc-xray-bar,
  .lc-prereq-note, .lc-unlocks, .lc-fn-popover { display: none !important; }
  /* nothing folded, nothing clipped */
  details { display: block !important; }
  details > summary { list-style: none; font-weight: 600; }
  details > *:not(summary) { display: revert !important; }
  .lc-datagrid, .lc-form-body, .lc-ag, .ag-root-wrapper,
  .lc-code, .lc-mdpad textarea {
    height: auto !important; max-height: none !important; overflow: visible !important;
  }
  body { padding-top: 0 !important; }
  a { text-decoration: none; color: inherit; }
  h1, h2, h3 { break-after: avoid; }
  .lc-feature, .lc-quiz, .lc-persona, .lc-block { break-inside: avoid; }
}

/* banner image: centered, rounded, responsive — lets an author drop a hero
   image without inline style:  ![alt](/path.png){: .lc-banner }  */
:is(.markdown-body, #ed-preview, #ed-feat-preview) .lc-banner {
  display: block; width: 100%; max-width: 880px; margin: 1.2em auto; border-radius: 10px;
}
</style>
