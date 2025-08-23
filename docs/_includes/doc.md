{% if include.name %}
  {%- assign subpath = include.path | default: "" | strip -%}
  {%- if subpath != "" and subpath | slice: -1, 1 != "/" -%}
    {%- assign subpath = subpath | append: "/" -%}
  {%- endif -%}

  {%- assign pdf_url = "/pdfs/" | append: subpath | append: include.name | append: ".pdf" -%}

  <iframe src="{{ pdf_url }}" width="100%" height="600" style="border:none;"></iframe>
  <p><a href="{{ pdf_url }}" target="_blank">📄 Open {{ include.name }}.pdf in a new tab</a></p>

{% else %}
  <p style="color:red; font-weight:bold;">
    ⚠️ Missing <code>name=</code> parameter.<br>
    Example:
    <code>{% raw %}{% include doc.md name="guide" path="subdir" %}{% endraw %}</code>
  </p>
{% endif %}
