{% assign _items = include.items | split: "|" %}
{% assign _gid = include.id | default: "default" %}
{% assign _delay = include.delay | default: 4000 %}

<style>
.lc-carousel { position: relative; padding: 1.2em 2em; min-height: 4em; background: #fafafa; border-left: 4px solid #0066cc; border-radius: 0 6px 6px 0; margin: 1em 0; }
.lc-carousel-item { display: none; font-style: italic; color: #444; line-height: 1.5; }
.lc-carousel-item.active { display: block; animation: lc-fade 0.4s ease; }
@keyframes lc-fade { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: none; } }
.lc-carousel-dots { text-align: center; margin-top: 0.8em; }
.lc-carousel-dots span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ccc; margin: 0 3px; cursor: pointer; transition: background 0.2s; }
.lc-carousel-dots span.active { background: #0066cc; }
</style>

<div class="lc-carousel" id="lc-car-{{ _gid }}">
  {% for item in _items %}
    <div class="lc-carousel-item{% if forloop.first %} active{% endif %}">{{ item | strip }}</div>
  {% endfor %}
  <div class="lc-carousel-dots">
    {% for item in _items %}
      <span class="{% if forloop.first %}active{% endif %}" data-idx="{{ forloop.index0 }}"></span>
    {% endfor %}
  </div>
</div>

<script>
(function() {
  var root = document.getElementById('lc-car-{{ _gid }}');
  var items = root.querySelectorAll('.lc-carousel-item');
  var dots = root.querySelectorAll('.lc-carousel-dots span');
  var i = 0;
  function show(idx) {
    items.forEach(function(x){x.classList.remove('active');});
    dots.forEach(function(x){x.classList.remove('active');});
    items[idx].classList.add('active');
    dots[idx].classList.add('active');
    i = idx;
  }
  dots.forEach(function(d) { d.addEventListener('click', function(){ show(parseInt(d.dataset.idx)); }); });
  setInterval(function(){ show((i+1) % items.length); }, {{ _delay }});
})();
</script>
