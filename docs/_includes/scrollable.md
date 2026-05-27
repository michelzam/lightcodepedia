{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _h = include.height | default: 300 %}

<style>
.lc-scroll-{{ _gid }} { max-height: {{ _h }}px; overflow-y: auto; padding: 1em 1.4em; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; margin: 1em 0; }
</style>

<div class="lc-scroll-{{ _gid }}" markdown="1">
{{ _page.content }}
</div>
