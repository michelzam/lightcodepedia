{% assign _id = include.id | default: "default" %}
{% assign _code = include.code | default: "print('Hello from MicroPython!')" %}
{% assign _rows = include.rows | default: 6 %}

<style>
.lc-pyrun { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-pyrun-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrun-title .lc-pyrun-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-pyrun textarea { display: block; width: 100%; box-sizing: border-box; border: none; outline: none; padding: 0.9em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; resize: vertical; background: #fafafa; color: #111; }
.lc-pyrun-bar { display: flex; align-items: center; gap: 0.6em; padding: 0.5em 0.9em; background: #f3f4f6; border-top: 1px solid #e0e0e0; }
.lc-pyrun-bar button { background: #0066cc; color: white; border: none; border-radius: 4px; padding: 0.35em 0.9em; cursor: pointer; font-size: 0.85em; font-weight: 500; }
.lc-pyrun-bar button:hover:not(:disabled) { background: #0052a3; }
.lc-pyrun-bar button:disabled { background: #888; cursor: progress; }
.lc-pyrun-bar .lc-pyrun-clear { background: #e5e5e5; color: #333; }
.lc-pyrun-bar .lc-pyrun-clear:hover:not(:disabled) { background: #d0d0d0; }
.lc-pyrun-bar .lc-pyrun-status { margin-left: auto; font-size: 0.78em; color: #666; }
.lc-pyrun-out { margin: 0; padding: 0.9em 1em; background: #1e1e1e; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; min-height: 2em; max-height: 300px; overflow-y: auto; }
.lc-pyrun-out.lc-empty { color: #888; font-style: italic; }
.lc-pyrun-out .lc-err { color: #ff6b6b; }
.lc-pyrun-view { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; padding: 0.9em 1em; background: #fafbfc; border-top: 1px solid #e0e0e0; }
.lc-pyrun-view:empty { display: none; }
.lc-pyrun-view .lc-rt-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8em 1em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-pyrun-view .lc-rt-card:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0,0,0,0.06); border-color: #0066cc; }
.lc-pyrun-view .lc-rt-card h3 { margin: 0 0 0.4em; font-size: 1em; color: #222; }
.lc-pyrun-view .lc-rt-card .lc-rt-row { margin: 0.15em 0; font-size: 0.88em; color: #444; }
.lc-pyrun-view .lc-rt-card .lc-rt-row b { color: #0066cc; margin-right: 0.4em; }
.lc-pyrun-view .lc-rt-card .lc-rt-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; color: #333; word-break: break-word; }
</style>

<div class="lc-pyrun" id="lc-pyrun-{{ _id }}">
  <div class="lc-pyrun-title">🐍 <span>MicroPython runner</span><span class="lc-pyrun-lang">python</span></div>
  <textarea class="lc-pyrun-code" rows="{{ _rows }}" spellcheck="false">{{ _code | escape }}</textarea>
  <div class="lc-pyrun-bar">
    <button class="lc-pyrun-run">▶ Run</button>
    <button class="lc-pyrun-clear">Clear</button>
    <span class="lc-pyrun-status"></span>
  </div>
  <pre class="lc-pyrun-out lc-empty">click ▶ Run to execute</pre>
  <div class="lc-pyrun-view" id="lc-pyrun-{{ _id }}-view"></div>
</div>

<script>
(function(){
  var ID = "{{ _id }}";
  var root = document.getElementById("lc-pyrun-" + ID);
  var codeEl = root.querySelector(".lc-pyrun-code");
  var runBtn = root.querySelector(".lc-pyrun-run");
  var clearBtn = root.querySelector(".lc-pyrun-clear");
  var status = root.querySelector(".lc-pyrun-status");
  var out = root.querySelector(".lc-pyrun-out");
  var view = root.querySelector(".lc-pyrun-view");
  var buf = "";
  var mp = null;
  var loading = null;

  var BOOTSTRAP = [
    "from js import document",
    "class _Showable:",
    "    def __init__(self, view_id):",
    "        self._view = document.getElementById(view_id)",
    "    def _esc(self, s):",
    "        return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')",
    "    def _card(self, title, rows_html):",
    "        c = document.createElement('div')",
    "        c.className = 'lc-rt-card'",
    "        c.innerHTML = '<h3>' + self._esc(title) + '</h3>' + rows_html",
    "        self._view.appendChild(c)",
    "    def _rows_from_pairs(self, pairs):",
    "        out = ''",
    "        for k, v in pairs:",
    "            out += '<div class=\"lc-rt-row\"><b>' + self._esc(k) + '</b><span class=\"lc-rt-val\">' + self._esc(v) + '</span></div>'",
    "        return out",
    "    def __call__(self, obj, title=None):",
    "        if isinstance(obj, dict):",
    "            t = title or obj.get('name') or obj.get('title') or 'dict'",
    "            self._card(t, self._rows_from_pairs(obj.items()))",
    "        elif isinstance(obj, (list, tuple)):",
    "            for i, item in enumerate(obj):",
    "                self(item, title=title and (title + '[' + str(i) + ']'))",
    "        else:",
    "            try:",
    "                d = obj.__dict__",
    "                if d:",
    "                    t = title or getattr(obj, 'name', None) or type(obj).__name__",
    "                    self._card(t, self._rows_from_pairs(d.items()))",
    "                    return",
    "            except (AttributeError, TypeError):",
    "                pass",
    "            self._card(title or type(obj).__name__, '<div class=\"lc-rt-val\">' + self._esc(obj) + '</div>')",
    "    def clear(self):",
    "        self._view.innerHTML = ''",
    "show = _Showable('lc-pyrun-' + '" + ID + "' + '-view')"
  ].join("\n");

  function setOut(text, isErr) {
    out.classList.remove("lc-empty");
    out.textContent = "";
    if (isErr) {
      var span = document.createElement("span");
      span.className = "lc-err";
      span.textContent = text;
      out.appendChild(span);
    } else {
      out.textContent = text;
    }
  }

  function loadMp() {
    if (mp) return Promise.resolve(mp);
    if (loading) return loading;
    runBtn.disabled = true;
    status.textContent = "loading runtime…";
    loading = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
      .then(function(mod){
        return mod.loadMicroPython({
          stdout: function(t){ buf += t; },
          stderr: function(t){ buf += t; }
        });
      })
      .then(function(instance){
        mp = instance;
        try { mp.runPython(BOOTSTRAP); } catch (e) { /* show() unavailable, user still has print */ }
        runBtn.disabled = false;
        status.textContent = "ready";
        return mp;
      })
      .catch(function(e){
        runBtn.disabled = false;
        status.textContent = "";
        loading = null;
        throw e;
      });
    return loading;
  }

  runBtn.addEventListener("click", function(){
    loadMp().then(function(m){
      buf = "";
      view.innerHTML = "";
      status.textContent = "running…";
      try {
        m.runPython(codeEl.value);
        setOut(buf || "(no print output)", false);
        status.textContent = "done";
      } catch (e) {
        setOut(buf + (buf ? "\n" : "") + (e.message || String(e)), true);
        status.textContent = "error";
      }
    }).catch(function(e){
      setOut("Failed to load MicroPython: " + (e.message || String(e)), true);
    });
  });

  clearBtn.addEventListener("click", function(){
    out.textContent = "click ▶ Run to execute";
    out.classList.add("lc-empty");
    view.innerHTML = "";
    status.textContent = mp ? "ready" : "";
  });
})();
</script>
