{%- comment -%}
Fetch and display a code file from GitHub.

Preferred:   {% include code_file.md path="modules/dog_ui.yaml" lang="yaml" %}
Escape hatch:{% include code_file.md src="https://..." lang="yaml" %}

Repo/branch default to site.github.repository_nwo / "main" — forks work
automatically (each fork's page fetches from its own repo).

Mode is decided at runtime:
  - live  (raw.githubusercontent.com)  → default; ~1s freshness after push
  - cdn   (jsDelivr @ build SHA)       → when location has ?cdn=1
                                         OR hostname matches site.lc_canonical_host
{%- endcomment -%}

{% assign _lang = include.lang | default: "text" %}
{% assign _repo = include.repo | default: site.github.repository_nwo %}
{% assign _branch = include.branch | default: "main" %}
{% assign _sha = site.github.build_revision | default: _branch %}
{% assign _canonical = site.lc_canonical_host | default: "" %}

{% if include.src %}
  {% assign _raw = include.src %}
  {% assign _cdn = include.src %}
  {% assign _label = include.title | default: include.src %}
{% else %}
  {% capture _raw %}https://raw.githubusercontent.com/{{ _repo }}/{{ _branch }}/{{ include.path }}{% endcapture %}
  {% capture _cdn %}https://cdn.jsdelivr.net/gh/{{ _repo }}@{{ _sha }}/{{ include.path }}{% endcapture %}
  {% assign _label = include.title | default: include.path %}
{% endif %}

{% assign _id = _label | replace: "/", "-" | replace: ".", "-" | replace: ":", "-" %}

<style>
.lc-code { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #fafafa; }
.lc-code-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-code-title .lc-code-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-code-title .lc-code-mode { font-size: 0.7em; color: #aaa; font-style: italic; }
.lc-code pre { margin: 0 !important; padding: 0.9em 1em !important; overflow-x: auto; font-size: 0.85em; line-height: 1.5; background: transparent; }
.lc-code pre code { background: transparent; padding: 0; }
.lc-code .lc-code-err { color: #b00; padding: 0.9em 1em; font-style: italic; }
</style>

<div class="lc-code">
  <div class="lc-code-title">📄 <span>{{ _label }}</span><span class="lc-code-mode" id="lc-code-mode-{{ _id }}"></span><span class="lc-code-lang">{{ _lang }}</span></div>
  <pre><code id="lc-code-{{ _id }}" class="language-{{ _lang }}">Loading {{ _label }}…</code></pre>
</div>
<script>
(function(){
  var raw = {{ _raw | jsonify }};
  var cdn = {{ _cdn | jsonify }};
  var canonical = {{ _canonical | jsonify }};
  var useCdn = (canonical && location.hostname === canonical) || location.search.indexOf("cdn=1") >= 0;
  var url = useCdn ? cdn : raw;
  var el = document.getElementById("lc-code-{{ _id }}");
  var modeEl = document.getElementById("lc-code-mode-{{ _id }}");
  if (modeEl) modeEl.textContent = useCdn ? "cdn" : "live";
  fetch(url)
    .then(function(r){ if(!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
    .then(function(t){ el.textContent = t; })
    .catch(function(e){ el.innerHTML = '<span class="lc-code-err">⚠️ could not fetch ' + url + ' — ' + e.message + '</span>'; });
})();
</script>
