{% if include.name %}
<iframe src="https://www.light-code.org/?module={{include.name}}" 
  width="100%" height="1600" loading="lazy" 
  allowfullscreen="allowfullscreen" style="border:none;">
</iframe>
{% else %}
<p style="color:red; font-weight:bold;">
  ⚠️ Missing <code>name=</code> parameter in include call.
  Example: <code>{% raw %}{% include example.md name="hello" %}{% endraw %}</code>
</p>
{% endif %}
