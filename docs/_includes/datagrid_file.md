{%- comment -%}
Render a datagrid from a YAML/JSON/CSV file in the repo.

Preferred:   {% include datagrid_file.md path="data/dogs.csv" %}
With knobs:  {% include datagrid_file.md path="data/dogs.yaml" title="Shelter dogs" height="500" %}
Escape hatch:{% include datagrid_file.md src="https://..." format="json" %}

Format auto-inferred from path extension (.csv → csv, .json → json, else yaml).
Override with format="..." if needed.

Mode decided at runtime (mirrors code_file.md):
  - live  (raw.githubusercontent.com)  → default; ~1s freshness after push
  - cdn   (jsDelivr @ build SHA)       → when location has ?cdn=1
                                         OR hostname matches site.lc_canonical_host
{%- endcomment -%}

{% assign _repo = include.repo | default: site.github.repository_nwo %}
{% assign _branch = include.branch | default: "main" %}
{% assign _sha = site.github.build_revision | default: _branch %}
{% assign _canonical = site.lc_canonical_host | default: "" %}

{% if include.src %}
  {% assign _raw = include.src %}
  {% assign _cdn = include.src %}
  {% assign _label = include.title | default: include.src %}
{% else %}
  {% capture _raw %}https://raw.githubusercontent.com/{{ _repo }}/{{ _branch }}/{{ include.path }}{% endcapture %}
  {% capture _cdn %}https://cdn.jsdelivr.net/gh/{{ _repo }}@{{ _sha }}/{{ include.path }}{% endcapture %}
  {% assign _label = include.title | default: include.path %}
{% endif %}

{% assign _format_default = "yaml" %}
{% if include.path contains ".csv" %}{% assign _format_default = "csv" %}{% endif %}
{% if include.path contains ".json" %}{% assign _format_default = "json" %}{% endif %}
{% assign _format = include.format | default: _format_default %}
{% assign _height = include.height | default: 400 %}

{% assign _detail_of = include.detail_of | default: "" %}

<div class="lc-datagrid-src"
     data-raw="{{ _raw }}"
     data-cdn="{{ _cdn }}"
     data-canonical="{{ _canonical }}"
     data-format="{{ _format }}"
     data-height="{{ _height }}"
     data-editable="{{ include.editable | default: 'false' }}"
     data-detail-of="{{ _detail_of }}"
     data-filter="{{ include.filter | default: '' }}"
     data-title="{{ _label }}"></div>
