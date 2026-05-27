{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _nl = "
" %}
{% assign _sections = _page.content | split: "### " %}

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
      {% assign _title = s | split: _nl | first | strip %}
      <button class="lc-tab-btn{% if forloop.first %} active{% endif %}" data-tab="lc-panel-{{ _gid }}-{{ forloop.index0 }}">{{ _title }}</button>
    {% endfor %}
  </div>
  {% for s in _sections offset:1 %}
    {% assign _title = s | split: _nl | first %}
    {% assign _body = s | remove_first: _title %}
<div id="lc-panel-{{ _gid }}-{{ forloop.index0 }}" class="lc-tab-panel{% if forloop.first %} active{% endif %}" markdown="1">
{{ _body }}
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
