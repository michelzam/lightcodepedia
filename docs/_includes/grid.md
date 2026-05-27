{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _cols = include.cols | default: "auto" %}
{% assign _gap = include.gap | default: 18 %}
{% assign _nl = "
" %}

{% if _page == nil %}
<div style="background:#fee;color:#900;padding:1em;border:1px solid #c00;border-radius:6px;margin:1em 0">
⚠️ <strong>grid.md:</strong> content file not found at <code>{{ _file }}</code>.
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
.lc-grid { display: grid; gap: {{ _gap }}px; margin: 1em 0; }
.lc-grid .lc-grid-cell { min-width: 0; }
.lc-grid .lc-grid-cell > h3 { margin-top: 0; margin-bottom: 0.6em; font-size: 1em; color: #666; text-transform: uppercase; letter-spacing: 0.05em; }
</style>

<div class="lc-grid" style="grid-template-columns: {% if _cols == 'auto' %}repeat(auto-fit, minmax(280px, 1fr)){% else %}repeat({{ _cols }}, 1fr){% endif %};">
  {% for s in _sections offset:1 %}
    {% if _mode == "md" %}
      {% assign _title = s | split: _nl | first | strip %}
      {% assign _body = s | remove_first: _title %}
      {% assign _body_html = _body | markdownify %}
    {% else %}
      {% assign _title = s | split: ">" | slice: 1 | first | split: "<" | first | strip %}
      {% assign _body_html = s | split: "</h3>" | last %}
    {% endif %}
<div class="lc-grid-cell">
{% if include.headings != "hide" %}<h3>{{ _title }}</h3>{% endif %}
{{ _body_html }}
</div>
  {% endfor %}
</div>

{% endif %}
