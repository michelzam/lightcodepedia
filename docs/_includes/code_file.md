{% assign _lang = include.lang | default: "text" %}
{% assign _title = include.title | default: include.src %}
{% assign _id = include.src | replace: "/", "-" | replace: ".", "-" | replace: ":", "-" | append: "-" | append: site.time | date: "%s" %}

<style>
.lc-code { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #fafafa; }
.lc-code-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-code-title .lc-code-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-code pre { margin: 0 !important; padding: 0.9em 1em !important; overflow-x: auto; font-size: 0.85em; line-height: 1.5; background: transparent; }
.lc-code pre code { background: transparent; padding: 0; }
.lc-code .lc-code-err { color: #b00; padding: 0.9em 1em; font-style: italic; }
</style>

<div class="lc-code">
  <div class="lc-code-title">📄 <span>{{ _title }}</span><span class="lc-code-lang">{{ _lang }}</span></div>
  <pre><code id="lc-code-{{ _id }}" class="language-{{ _lang }}">Loading {{ include.src }}…</code></pre>
</div>
<script>
(function(){
  var el = document.getElementById("lc-code-{{ _id }}");
  fetch({{ include.src | jsonify }})
    .then(function(r){ if(!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
    .then(function(t){ el.textContent = t; })
    .catch(function(e){ el.innerHTML = '<span class="lc-code-err">⚠️ could not fetch ' + {{ include.src | jsonify }} + ' — ' + e.message + '</span>'; });
})();
</script>
