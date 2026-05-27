{% assign _file = include.file | append: ".md" %}
{% assign _page = site.pages | where: "path", _file | first %}
{% assign _gid = include.file | replace: "/", "-" | replace: ".", "-" %}
{% assign _nl = "
" %}

{% if _page == nil %}
<div style="background:#fee;color:#900;padding:1em;border:1px solid #c00;border-radius:6px;margin:1em 0">
⚠️ <strong>radio.md:</strong> content file not found at <code>{{ _file }}</code>.
</div>
{% else %}

{% assign _raw = _page.content %}
{% if _raw contains "### " %}
  {% assign _sections = _raw | split: "### " %}
  {% assign _mode = "md" %}
{% else %}
  {% assign _sections = _raw | split: "<h3" %}
  {% assign _mode = "html" %}
{% endif %}

<style>
.lc-radio-group { margin: 1em 0; }
.lc-radio-options { margin-bottom: 1em; padding: 0.6em 1em; background: #f5f5f5; border-radius: 6px; }
.lc-radio-options label { margin-right: 1.4em; cursor: pointer; font-weight: 500; }
.lc-radio-options input { margin-right: 0.4em; }
.lc-radio-body { padding: 1em 1.4em; background: white; border: 1px solid #eee; border-left: 3px solid #0066cc; border-radius: 0 6px 6px 0; }
.lc-radio-content { display: none; }
.lc-radio-content.active { display: block; }
</style>

<div class="lc-radio-group" id="lc-rg-{{ _gid }}">
  <div class="lc-radio-options">
    {% for s in _sections offset:1 %}
      {% if _mode == "md" %}
        {% assign _title = s | split: _nl | first | strip %}
      {% else %}
        {% assign _title = s | split: ">" | slice: 1 | first | split: "<" | first | strip %}
      {% endif %}
      <label><input type="radio" name="lc-rg-{{ _gid }}" data-target="lc-rc-{{ _gid }}-{{ forloop.index0 }}"{% if forloop.first %} checked{% endif %}> {{ _title }}</label>
    {% endfor %}
  </div>
  <div class="lc-radio-body">
    {% for s in _sections offset:1 %}
      {% if _mode == "md" %}
        {% assign _title = s | split: _nl | first %}
        {% assign _body = s | remove_first: _title %}
        {% assign _html = _body | markdownify %}
      {% else %}
        {% assign _html = "<h3" | append: s %}
      {% endif %}
<div id="lc-rc-{{ _gid }}-{{ forloop.index0 }}" class="lc-radio-content{% if forloop.first %} active{% endif %}">
{{ _html }}
</div>
    {% endfor %}
  </div>
</div>

<script>
(function() {
  var root = document.getElementById('lc-rg-{{ _gid }}');
  root.querySelectorAll('input[type=radio]').forEach(function(r) {
    r.addEventListener('change', function() {
      root.querySelectorAll('.lc-radio-content').forEach(function(x){ x.classList.remove('active'); });
      document.getElementById(r.dataset.target).classList.add('active');
    });
  });
})();
</script>

{% endif %}
