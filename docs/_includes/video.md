{% if include.id %}
  {% assign pdf_url = "https://drive.google.com/file/d/" | append: include.id | append: "/preview" %}

  <iframe src="{{ pdf_url }}" width="100%" height="600" style="border:none;"></iframe>
  <p><a href="{{ pdf_url }}" target="_blank">📄 Open PDF in a new tab</a></p>

{% else %}
  <p style="color:red; font-weight:bold;">
    ⚠️ Missing <code>id=</code> parameter.<br>
    Example:
    <code>{% raw %}{% include gdrive_pdf.md id="1AbCdEfGhIjKlMnOpQrStUvWxYz" %}{% endraw %}</code>
  </p>
{% endif %}