{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _nl = "
" %}
{% assign _sections = _page.content | split: "### " %}

{% for s in _sections offset:1 %}
  {% assign _title = s | split: _nl | first | strip %}
  {% assign _body = s | remove_first: _title %}
<details>
<summary>{{ _title }}</summary>

{{ _body | markdownify }}

</details>
{% endfor %}
