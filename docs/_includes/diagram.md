{%- comment -%}
Live component-model diagram.

Attach `{: .diagram }` to a link/paragraph to render a Graphviz class diagram of
the component model, generated IN THE BROWSER from the wrapper classes' own
to_dot() methods (the single source of truth in steps_runtime.md). Optional
`scope="ClassName"` narrows to that class plus its ancestors, association targets
and subclasses. No scope → the whole model.

Pipeline: MicroPython runs the preamble + to_dot(scope) → DOT string →
@viz-js/viz (vendored) renders it to inline SVG.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  (async function () {
    var VIZ_URL = "{{ "/assets/js/viz-global.js" | relative_url }}";
    var nodes = document.querySelectorAll(".diagram");
    if (!nodes.length) return;
    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    if (!preamble) return;
    try {
      // Load viz (via global script tag) and MicroPython in parallel.
      var vizPromise = window._lcVizReady || (window._lcVizReady = new Promise(function (res, rej) {
        if (window.Viz) { window.Viz.instance().then(res).catch(rej); return; }
        var s = document.createElement("script");
        s.src = VIZ_URL;
        s.onload = function () { window.Viz.instance().then(res).catch(rej); };
        s.onerror = function () { rej(new Error("failed to load " + VIZ_URL)); };
        document.head.appendChild(s);
      }));
      var mpPromise = window._lcMpReady || (window._lcMpReady =
        import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
          .then(function (m) { return m.loadMicroPython({ stdout: function () {}, stderr: function () {} }); }));

      var viz = await vizPromise;
      var mp  = await mpPromise;
      var run = mp.runPython || mp.exec || mp.pyexec || mp.run;

      // Define the model once; each diagram just calls to_dot(scope).
      run.call(mp, preamble);

      var rendered = [];
      function renderOne(div, arg, sm) {
        run.call(mp, "import js\njs.window._lcDiagramDot = to_dot(" + arg
                     + ", statemachines=" + sm + ")\n");
        div.innerHTML = viz.renderString(window._lcDiagramDot || "digraph{}", { format: "svg" });
      }
      nodes.forEach(function (el) {
        var scope = (el.getAttribute("scope") || "").replace(/[^A-Za-z0-9_*]/g, "");
        var arg = (scope && scope !== "*") ? ('"' + scope + '"') : "None";
        // states="false"/"off"/"no" hides the state-machine clusters (knob)
        var st = (el.getAttribute("states") || "").toLowerCase();
        var sm = (st === "false" || st === "off" || st === "no" || st === "0")
                 ? "False" : "True";
        try {
          var div = document.createElement("div");
          div.className = "lc-dot-diagram lc-diagram";
          div.style.cssText = "overflow:auto;line-height:1";
          el.parentNode.replaceChild(div, el);
          renderOne(div, arg, sm);
          rendered.push({ div: div, arg: arg, sm: sm });
        } catch (e) {
          console.error("[lc-diagram]", e);
          var pre = document.createElement("pre");
          pre.style.cssText = "color:red;font-size:0.8em";
          pre.textContent = "[diagram] " + e;
          el.parentNode.replaceChild(pre, el);
        }
      });
      // author classes land in the shared runtime once an .inspector block has
      // run — redraw so the page's diagrams tell the whole story
      document.addEventListener("lc-model-changed", function () {
        rendered.forEach(function (r) {
          try { renderOne(r.div, r.arg, r.sm); } catch (e) { console.error("[lc-diagram]", e); }
        });
      });
    } catch (e) {
      console.error("[lc-diagram] init", e);
    }
  })();
</script>
