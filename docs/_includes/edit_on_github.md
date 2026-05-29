{%- comment -%}
Footer link that opens the current page's source file in GitHub's web editor.

Auto-included by docs/_layouts/default.html on every page. Skipped for:
  - the 404 page (no real source)
  - pages without a page.path (auto-generated)
  - pages with `no_edit: true` in front matter (opt-out)
  - embed mode (?embed=true)

The site source lives under `docs/`, so we prepend `docs/` to page.path
to construct the repo-relative file URL.
{%- endcomment -%}

{% if page.path and page.permalink != "/404.html" and page.no_edit != true %}
<style>
.lc-edit-footer { max-width: 980px; margin: 3em auto 2em; padding: 1em 1.2rem 0; border-top: 1px solid #eee; text-align: center; font-size: 0.85em; color: #888; box-sizing: border-box; }
.lc-edit-footer a { display: inline-flex; align-items: center; gap: 0.4em; text-decoration: none; color: #0066cc; padding: 0.4em 0.9em; border: 1px solid #d0e3f5; border-radius: 6px; background: white; transition: background 0.15s, border-color 0.15s, box-shadow 0.15s; }
.lc-edit-footer a:hover { background: #f5f9ff; border-color: #0066cc; box-shadow: 0 2px 6px rgba(0, 102, 204, 0.08); }
.lc-edit-footer .lc-edit-icon { font-size: 1.1em; line-height: 1; }
.lc-embed-mode .lc-edit-footer { display: none !important; }
</style>
<footer class="lc-edit-footer">
  <a href="https://github.com/{{ site.github.repository_nwo }}/edit/main/docs/{{ page.path }}" target="_blank" rel="noopener">
    <span class="lc-edit-icon">✏️</span><span>Edit this page on GitHub</span>
  </a>
</footer>
{% endif %}
