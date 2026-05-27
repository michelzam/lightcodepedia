{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _nl = "
" %}

{% if _page == nil %}
<div style="background:#fee;color:#900;padding:1em;border:1px solid #c00;border-radius:6px;margin:1em 0">
⚠️ <strong>tabs.md:</strong> content file not found at <code>{{ _file }}</code>.
Make sure the file exists and pass the path without <code>.md</code>, e.g. <code>file="components/my_tabs"</code>.
</div>
{% else %}

{% assign _raw = _page.content %}
{% comment %} Detect raw markdown vs already-rendered HTML and split accordingly. {% endcomment %}
{% if _raw contains "### " %}
  {% assign _sections = _raw | split: "### " %}
  {% assign _mode = "md" %}
{% else %}
  {% assign _sections = _raw | split: "<h3" %}
  {% assign _mode = "html" %}
{% endif %}

<style>
.lc-tabs { border: 1px solid #ddd; border-radius: 6px; margin: 1em 0; overflow: hidden; }
.lc-tabs .lc-tab-bar { display: flex; background: #f5f5f5; border-bottom: 1px solid #ddd; }
.lc-tabs .lc-tab-btn { background: none; border: none; padding: 0.6em 1.2em; cursor: pointer; font-size: 0.95em; color: #555; border-right: 1px solid #ddd; }
.lc-tabs .lc-tab-btn:hover { background: #eaeaea; }
.lc-tabs .lc-tab-btn.active { background: white; color: #0066cc; font-weight: 600; box-shadow: inset 0 -3px 0 #0066cc; }
.lc-tabs .lc-tab-panel { display: none; padding: 1em 1.4em; }
.lc-tabs .lc-tab-panel.active { display: block; }
</style>

<div class="lc-tabs" id="lc-tabs-{{ _gid }}">
  <div class="lc-tab-bar">
    {% for s in _sections offset:1 %}
      {% if _mode == "md" %}
        {% assign _title = s | split: _nl | first | strip %}
      {% else %}
        {% assign _after_gt = s | split: ">" | shift %}
        {% assign _title = s | split: ">" | slice: 1 | first | split: "<" | first | strip %}
      {% endif %}
      <button class="lc-tab-btn{% if forloop.first %} active{% endif %}" data-tab="lc-panel-{{ _gid }}-{{ forloop.index0 }}">{{ _title }}</button>
    {% endfor %}
  </div>
  {% for s in _sections offset:1 %}
    {% if _mode == "md" %}
      {% assign _title = s | split: _nl | first %}
      {% assign _body = s | remove_first: _title %}
      {% assign _html = _body | markdownify %}
    {% else %}
      {% assign _html = "<h3" | append: s %}
    {% endif %}
<div id="lc-panel-{{ _gid }}-{{ forloop.index0 }}" class="lc-tab-panel{% if forloop.first %} active{% endif %}">
{{ _html }}
</div>
  {% endfor %}
</div>

<script>
(function() {
  var root = document.getElementById('lc-tabs-{{ _gid }}');
  root.querySelectorAll('.lc-tab-btn').forEach(function(b) {
    b.addEventListener('click', function() {
      root.querySelectorAll('.lc-tab-btn').forEach(function(x) { x.classList.remove('active'); });
      root.querySelectorAll('.lc-tab-panel').forEach(function(x) { x.classList.remove('active'); });
      b.classList.add('active');
      document.getElementById(b.dataset.tab).classList.add('active');
    });
  });
})();
</script>

{% endif %}
