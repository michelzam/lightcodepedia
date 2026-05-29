{%- comment -%}
Render a form from a single-object YAML/JSON file in the repo.

Preferred:   {% include form_file.md path="data/dog.json" %}
With knobs:  {% include form_file.md path="data/dog.yaml" title="Lucky" %}
Escape hatch:{% include form_file.md src="https://..." format="json" %}

Format auto-inferred from path extension (.json → json, .yaml/.yml → yaml).
CSV not supported — forms are single-record. Use {% include datagrid_file.md %}
for tabular files.

Mode decided at runtime (mirrors datagrid_file.md):
  - live  (raw.githubusercontent.com)  → default
  - cdn   (jsDelivr @ build SHA)       → ?cdn=1 or canonical host
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
{% if include.path contains ".json" %}{% assign _format_default = "json" %}{% endif %}
{% assign _format = include.format | default: _format_default %}

<div class="lc-form-src"
     data-raw="{{ _raw }}"
     data-cdn="{{ _cdn }}"
     data-canonical="{{ _canonical }}"
     data-format="{{ _format }}"
     data-editable="{{ include.editable | default: 'false' }}"
     data-title="{{ _label }}"></div>
