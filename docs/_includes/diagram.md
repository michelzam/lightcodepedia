{%- comment -%}
Live component-model diagram.

Attach `{: .diagram }` to a link/paragraph to render a Graphviz class diagram of
the component model, generated IN THE BROWSER from the wrapper classes' own
to_dot() methods (the single source of truth in steps_runtime.md). Optional
`scope="ClassName"` narrows to that class plus its ancestors, association targets
and subclasses. No scope → the whole model.

Pipeline: MicroPython runs the preamble + to_dot(scope) → DOT string →
@viz-js/viz renders it to inline SVG.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  const nodes = document.querySelectorAll(".diagram");
  if (nodes.length) {
    const preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    if (preamble) {
      try {
        const [vizMod, mp] = await Promise.all([
          import("https://cdn.jsdelivr.net/npm/@viz-js/viz@3/dist/viz.js"),
          (window._lcMpReady || (window._lcMpReady =
            import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
              .then(function (m) { return m.loadMicroPython({ stdout: function () {}, stderr: function () {} }); })))
        ]);
        const viz = await (vizMod.instance || vizMod.default.instance || vizMod.default)();
        const run = mp.runPython || mp.exec || mp.pyexec || mp.run;

        // Define the model once; each diagram just calls to_dot(scope).
        run.call(mp, preamble);

        nodes.forEach(function (el) {
          var scope = (el.getAttribute("scope") || "").replace(/[^A-Za-z0-9_]/g, "");
          var arg = scope ? ('"' + scope + '"') : "None";
          try {
            run.call(mp, "import js\njs.window._lcDiagramDot = to_dot(" + arg + ")\n");
            var svg = viz.renderString(window._lcDiagramDot || "digraph{}");
            var div = document.createElement("div");
            div.className = "lc-dot-diagram lc-diagram";
            div.style.cssText = "overflow:auto;line-height:1";
            div.innerHTML = svg;
            el.parentNode.replaceChild(div, el);
          } catch (e) {
            console.error("[lc-diagram]", e);
            var pre = document.createElement("pre");
            pre.style.cssText = "color:red;font-size:0.8em";
            pre.textContent = "[diagram] " + e;
            el.parentNode.replaceChild(pre, el);
          }
        });
      } catch (e) {
        console.error("[lc-diagram] init", e);
      }
    }
  }
</script>
