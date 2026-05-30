{%- comment -%}
Floating ✏️ pencil button (bottom-right) that opens the current page's
source file in GitHub's web editor. On hover the button expands to
reveal an "Edit on GitHub" label.

Auto-included by docs/_layouts/default.html on every page. Skipped for:
  - the 404 page
  - pages without a page.path (auto-generated)
  - pages with `no_edit: true` in front matter
  - embed mode (?embed=true), which already hides the topbar

The site source lives under `docs/`, so we prepend `docs/` to page.path
to construct the repo-relative file URL.
{%- endcomment -%}

{% if page.path and page.permalink != "/404.html" and page.no_edit != true %}
<style>
.lc-edit-fab {
  position: fixed;
  bottom: 1.2em;
  right: 1.2em;
  height: 44px;
  min-width: 44px;
  padding: 0 14px 0 14px;
  border-radius: 22px;
  background: white;
  color: #0066cc;
  border: 1px solid #d0e3f5;
  display: inline-flex;
  align-items: center;
  gap: 0;
  text-decoration: none;
  font-size: 0.88em;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: gap 0.18s ease, padding 0.18s ease, background 0.15s, border-color 0.15s, box-shadow 0.15s, transform 0.15s;
  z-index: 999;
  overflow: hidden;
  white-space: nowrap;
}
.lc-edit-fab .lc-edit-fab-icon { font-size: 1.2em; line-height: 1; }
.lc-edit-fab .lc-edit-fab-label { max-width: 0; opacity: 0; transition: max-width 0.22s ease, opacity 0.18s ease 0.04s; overflow: hidden; }
@media (hover: hover) and (pointer: fine) {
  .lc-edit-fab:hover { background: #f5f9ff; border-color: #0066cc; box-shadow: 0 4px 14px rgba(0, 102, 204, 0.18); transform: translateY(-1px); gap: 0.45em; padding-right: 16px; }
  .lc-edit-fab:hover .lc-edit-fab-label { max-width: 200px; opacity: 1; }
}
.lc-edit-fab.lc-fab-expanded { background: #f5f9ff; border-color: #0066cc; box-shadow: 0 4px 14px rgba(0, 102, 204, 0.18); transform: translateY(-1px); gap: 0.45em; padding-right: 16px; }
.lc-edit-fab.lc-fab-expanded .lc-edit-fab-label { max-width: 200px; opacity: 1; }
.lc-edit-fab:focus-visible { outline: 2px solid #0066cc; outline-offset: 2px; }
.lc-embed-mode .lc-edit-fab { display: none !important; }
@media (max-width: 700px) {
  .lc-edit-fab { bottom: 0.8em; right: 0.8em; }
}
</style>
<a class="lc-edit-fab"
   href="https://github.com/{{ site.github.repository_nwo }}/edit/main/docs/{{ page.path }}"
   target="_blank"
   rel="noopener"
   title="Edit this page on GitHub"
   aria-label="Edit this page on GitHub">
  <span class="lc-edit-fab-icon" aria-hidden="true">✏️</span><span class="lc-edit-fab-label">Edit on GitHub</span>
</a>
<script>
(function(){
  var fab = document.querySelector('.lc-edit-fab');
  if (!fab) return;
  if (!window.matchMedia('(hover: none)').matches) return;
  var collapseTimer = null;
  function collapse(){ fab.classList.remove('lc-fab-expanded'); }
  fab.addEventListener('click', function(e){
    if (!fab.classList.contains('lc-fab-expanded')) {
      e.preventDefault();
      fab.classList.add('lc-fab-expanded');
      clearTimeout(collapseTimer);
      collapseTimer = setTimeout(collapse, 3000);
    } else {
      clearTimeout(collapseTimer);
      setTimeout(collapse, 0);
    }
  });
  document.addEventListener('click', function(e){
    if (!fab.contains(e.target)) collapse();
  });
})();
</script>
{% endif %}
