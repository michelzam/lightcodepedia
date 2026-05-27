{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _cols = include.cols | default: "auto" %}
{% assign _gap = include.gap | default: 18 %}
{% assign _nl = "
" %}

{% if _page == nil %}
<div style="background:#fee;color:#900;padding:1em;border:1px solid #c00;border-radius:6px;margin:1em 0">
⚠️ <strong>cards.md:</strong> content file not found at <code>{{ _file }}</code>.
</div>
{% else %}

{% assign _raw = _page.content %}
{% if _raw contains "### " %}
  {% assign _sections = _raw | split: "### " %}
  {% assign _mode = "md" %}
{% else %}
  {% assign _sections = _raw | split: "<h3" %}
  {% assign _mode = "html" %}
{% endif %}

<style>
.lc-cards { display: grid; gap: {{ _gap }}px; margin: 1em 0; }
.lc-cards .lc-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.2em 1.4em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-cards .lc-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); border-color: #0066cc; }
.lc-cards .lc-card h3 { margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em; color: #222; }
.lc-cards .lc-card p { margin: 0 0 0.6em; color: #555; line-height: 1.45; }
.lc-cards .lc-card p:last-child { margin-bottom: 0; }
.lc-cards .lc-card a { color: #0066cc; text-decoration: none; font-weight: 500; }
.lc-cards .lc-card a:hover { text-decoration: underline; }
@media (max-width: 700px) {
  .lc-cards .lc-card { padding: 0.9em 1em; }
  .lc-cards .lc-card h3 { font-size: 1em; margin-bottom: 0.3em; }
  .lc-cards .lc-card p:first-of-type {
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 0.4em;
  }
}
</style>

<div class="lc-cards" style="grid-template-columns: {% if _cols == 'auto' %}repeat(auto-fit, minmax(240px, 1fr)){% else %}repeat({{ _cols }}, 1fr){% endif %};">
  {% for s in _sections offset:1 %}
    {% if _mode == "md" %}
      {% assign _title = s | split: _nl | first | strip %}
      {% assign _body = s | remove_first: _title %}
      {% assign _body_html = _body | markdownify %}
    {% else %}
      {% assign _title = s | split: ">" | slice: 1 | first | split: "<" | first | strip %}
      {% assign _body_html = s | split: "</h3>" | last %}
    {% endif %}
<div class="lc-card">
<h3>{{ _title }}</h3>
{{ _body_html }}
</div>
  {% endfor %}
</div>

{% endif %}
