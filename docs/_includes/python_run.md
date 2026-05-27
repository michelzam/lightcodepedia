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
</style>

<div class="lc-pyrun" id="lc-pyrun-{{ _id }}">
  <div class="lc-pyrun-title">🐍 <span>MicroPython runner</span><span class="lc-pyrun-lang">python</span></div>
  <textarea class="lc-pyrun-code" rows="{{ _rows }}" spellcheck="false">{{ _code | escape }}</textarea>
  <div class="lc-pyrun-bar">
    <button class="lc-pyrun-run">▶ Run</button>
    <button class="lc-pyrun-clear">Clear output</button>
    <span class="lc-pyrun-status"></span>
  </div>
  <pre class="lc-pyrun-out lc-empty">click ▶ Run to execute</pre>
</div>

<script>
(function(){
  var root = document.getElementById("lc-pyrun-{{ _id }}");
  var codeEl = root.querySelector(".lc-pyrun-code");
  var runBtn = root.querySelector(".lc-pyrun-run");
  var clearBtn = root.querySelector(".lc-pyrun-clear");
  var status = root.querySelector(".lc-pyrun-status");
  var out = root.querySelector(".lc-pyrun-out");
  var buf = "";
  var mp = null;
  var loading = null;

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
      status.textContent = "running…";
      try {
        m.runPython(codeEl.value);
        setOut(buf || "(no output)", false);
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
    status.textContent = mp ? "ready" : "";
  });
})();
</script>
