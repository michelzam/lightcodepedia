{% assign _id = include.id | default: "default" %}
{% assign _code = include.code | default: "print('Hello from MicroPython!')" %}
{% assign _rows = include.rows | default: 6 %}
{% assign _init = include.init | default: "" %}
{% assign _bound = include.bound | default: "" %}

<div class="lc-pyrun" id="lc-pyrun-{{ _id }}">
  {% if _bound != "" %}<div class="lc-pyrun-bound" id="lc-pyrun-{{ _id }}-bound"></div>{% endif %}
  {% if include.folded %}<details class="lc-pyrun-fold"><summary>🐍 Edit &amp; run Python</summary>{% else %}<div class="lc-pyrun-title">🐍 <span>MicroPython runner</span><span class="lc-pyrun-lang">python</span></div>{% endif %}
  <div class="lc-pyrun-editor"><div class="lc-pyrun-gutter"><div class="lc-pyrun-gutter-inner"></div></div><textarea class="lc-pyrun-code" rows="{{ _rows }}" spellcheck="false">{{ _code | escape }}</textarea></div>
  <div class="lc-pyrun-bar">
    <button class="lc-pyrun-run">▶ Run</button>
    <button class="lc-pyrun-test">🧪 Test</button>
    <button class="lc-pyrun-clear">Clear</button>
    <span class="lc-pyrun-status"></span>
  </div>
  <pre class="lc-pyrun-out lc-empty">click ▶ Run to execute</pre>
  <div class="lc-pyrun-view" id="lc-pyrun-{{ _id }}-view"></div>
  <div class="lc-pyrun-tests" id="lc-pyrun-{{ _id }}-tests"></div>
  {% if include.folded %}</details>{% endif %}
</div>

<script>
(function(){
  var opts = {
    id: "{{ _id }}",
    init: {{ _init | jsonify }},
    bound: {{ _bound | jsonify }}
  };
  function attachNow() { window.lcPyrun.attach("lc-pyrun-{{ _id }}", opts); }
  if (window.lcPyrun) attachNow();
  else (window.lcPyrunQueue = window.lcPyrunQueue || []).push(attachNow);
})();
</script>
