<details>
<summary>{{ include.title | default: "Click to expand" }}</summary>

{% if include.gdrive_id %}
{% include gdrive_pdf.md id=include.gdrive_id %}
{% elsif include.content %}
{{ include.content | markdownify }}
{% endif %}

</details>
