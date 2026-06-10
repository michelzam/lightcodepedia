{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _h = include.height | default: 300 %}

{% if _page == nil %}
<div style="background:#fee;color:#900;padding:1em;border:1px solid #c00;border-radius:6px;margin:1em 0">
⚠️ <strong>scrollable.md:</strong> content file not found at <code>{{ _file }}</code>.
</div>
{% else %}

<style>
.lc-scroll-{{ _gid }} { max-height: {{ _h }}px; overflow-y: auto; padding: 1em 1.4em; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; margin: 1em 0; }
</style>

<div class="lc-scroll-{{ _gid }}">
{{ _page.content | markdownify }}
</div>

{% endif %}
