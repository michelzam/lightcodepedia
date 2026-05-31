{% if include.name %}
  {%- assign subpath = include.path | default: "" | strip -%}
  {%- if subpath != "" and subpath | slice: -1, 1 != "/" -%}
    {%- assign subpath = subpath | append: "/" -%}
  {%- endif -%}

  {%- comment -%} PDFs live in the repo's /pdfs (outside the Jekyll source) and are
  served via jsDelivr so they stay out of the Pages build artifact. {%- endcomment -%}
  {%- assign _docrepo = site.github.repository_nwo | default: "michelzam/lightcodepedia" -%}
  {%- assign pdf_url = "https://cdn.jsdelivr.net/gh/" | append: _docrepo | append: "@main/pdfs/" | append: subpath | append: include.name | append: ".pdf" -%}

  <iframe src="{{ pdf_url }}" width="100%" height="600" style="border:none;"></iframe>
  <p><a href="{{ pdf_url }}" target="_blank">📄 Open {{ include.name }}.pdf in a new tab</a></p>

{% else %}
  <p style="color:red; font-weight:bold;">
    ⚠️ Missing <code>name=</code> parameter.<br>
    Example:
    <code>{% raw %}{% include doc.md name="guide" path="subdir" %}{% endraw %}</code>
  </p>
{% endif %}
