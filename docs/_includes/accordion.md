{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _nl = "
" %}

{% if _page == nil %}
<div style="background:#fee;color:#900;padding:1em;border:1px solid #c00;border-radius:6px;margin:1em 0">
⚠️ <strong>accordion.md:</strong> content file not found at <code>{{ _file }}</code>.
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

{% for s in _sections offset:1 %}
  {% if _mode == "md" %}
    {% assign _title = s | split: _nl | first | strip %}
    {% assign _body = s | remove_first: _title %}
    {% assign _html = _body | markdownify %}
  {% else %}
    {% assign _title = s | split: ">" | slice: 1 | first | split: "<" | first | strip %}
    {% assign _body = s | split: "</h3>" | last %}
    {% assign _html = _body %}
  {% endif %}
<details>
<summary>{{ _title }}</summary>

{{ _html }}

</details>
{% endfor %}

{% endif %}
