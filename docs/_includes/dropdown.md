{% assign _gid = include.id | default: "dd" %}
{% assign _items = include.items | split: "|" %}

<style>
.lc-dropdown { position: relative; display: inline-block; margin: 0.3em 0; }
.lc-dd-toggle { background: #0066cc; color: white; border: none; padding: 0.5em 1em; border-radius: 4px; cursor: pointer; font-size: 0.95em; }
.lc-dd-toggle:hover { background: #0052a3; }
.lc-dd-menu { display: none; position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; border-radius: 4px; min-width: 180px; box-shadow: 0 2px 10px rgba(0,0,0,0.12); z-index: 500; margin-top: 4px; }
.lc-dd-menu.open { display: block; }
.lc-dd-menu a { display: block; padding: 0.6em 1em; color: #333; text-decoration: none; }
.lc-dd-menu a:hover { background: #f5f5f5; color: #0066cc; }
</style>

<div class="lc-dropdown" id="lc-dd-{{ _gid }}">
  <button class="lc-dd-toggle">{{ include.label | default: "Menu" }} ▾</button>
  <div class="lc-dd-menu">
    {% for item in _items %}
      {% assign _parts = item | split: ":" %}
      <a href="{{ _parts[1] | strip }}">{{ _parts[0] | strip }}</a>
    {% endfor %}
  </div>
</div>

<script>
(function() {
  var root = document.getElementById('lc-dd-{{ _gid }}');
  var btn = root.querySelector('.lc-dd-toggle');
  var menu = root.querySelector('.lc-dd-menu');
  btn.addEventListener('click', function(e){ e.stopPropagation(); menu.classList.toggle('open'); });
  document.addEventListener('click', function(){ menu.classList.remove('open'); });
})();
</script>
