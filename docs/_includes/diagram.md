{%- comment -%}
Live component-model diagram.

Attach `{: .diagram }` to a link/paragraph to render a Graphviz class diagram of
the component model, generated IN THE BROWSER from the wrapper classes' own
to_dot() methods (the single source of truth in steps_runtime.md). Optional
`scope="ClassName"` narrows to that class plus its ancestors, association targets
and subclasses; `scope="A,B"` unions several closures — the way to include a
manager class nothing associates INTO. No scope → the whole model.

Pipeline: MicroPython runs the preamble + to_dot(scope) → DOT string →
@viz-js/viz (vendored) renders it to inline SVG.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  /* One engine, two roads. A Jekyll page carries its .diagram blocks at load;
     a runner render (courses in Canvas, every gh: page) adds them AFTER the
     script ran, and an accordion's body arrives later still. So the engine
     is an UPGRADER: each block renders when it appears, the model is defined
     once per runtime, and every drawn diagram redraws when an author model
     lands (the .model block dispatches lc-model-changed). Found 2026-09-04:
     the 410 concepts page drew nothing — the link just sat there. */
  (function () {
    var VIZ_URL = "{{ "/assets/js/viz-global.js" | relative_url }}";
    var rendered = [];
    var ready = null;     /* {viz, mp, run} once both engines are up and the model is defined */

    function engines() {
      if (ready) return ready;
      var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
      if (!preamble) return (ready = Promise.reject(new Error("no steps preamble on this page")));
      var vizPromise = window._lcVizReady || (window._lcVizReady = new Promise(function (res, rej) {
        if (window.Viz) { window.Viz.instance().then(res).catch(rej); return; }
        var s = document.createElement("script");
        s.src = VIZ_URL;
        s.onload = function () { window.Viz.instance().then(res).catch(rej); };
        s.onerror = function () { rej(new Error("failed to load " + VIZ_URL)); };
        document.head.appendChild(s);
      }));
      var mpPromise = window._lcMpReady || (window._lcMpReady =
        window.lcMpy ? window.lcMpy() :
        import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
          .then(function (m) { return m.loadMicroPython({ stdout: function () {}, stderr: function () {} }); }));
      ready = Promise.all([vizPromise, mpPromise]).then(function (both) {
        var mp = both[1], run = mp.runPython || mp.exec || mp.pyexec || mp.run;
        // Define the model once; each diagram just calls to_dot(scope). The
        // registries survive re-runs, so an author model already in this
        // runtime is kept, not wiped.
        run.call(mp, preamble);
        return { viz: both[0], mp: mp, run: run };
      });
      return ready;
    }

    function renderOne(e, div, arg, sm) {
      e.run.call(e.mp, "import js\njs.window._lcDiagramDot = to_dot(" + arg
                       + ", statemachines=" + sm + ")\n");
      div.innerHTML = e.viz.renderString(window._lcDiagramDot || "digraph{}", { format: "svg" });
    }

    function upgradeDiagram(el) {
      if (el.dataset.lcDiagramDone) return;
      el.dataset.lcDiagramDone = "1";
      var scope = (el.getAttribute("scope") || "").replace(/[^A-Za-z0-9_*,]/g, "");
      var arg = (scope && scope !== "*") ? ('"' + scope + '"') : "None";
      // states="false"/"off"/"no" hides the state-machine clusters (knob)
      var st = (el.getAttribute("states") || "").toLowerCase();
      var sm = (st === "false" || st === "off" || st === "no" || st === "0") ? "False" : "True";
      var div = document.createElement("div");
      div.className = "lc-dot-diagram lc-diagram";
      div.style.cssText = "overflow:auto;line-height:1";
      if (el.id) div.id = el.id;
      el.parentNode.replaceChild(div, el);
      engines().then(function (e) {
        renderOne(e, div, arg, sm);
        rendered.push({ div: div, arg: arg, sm: sm });
      }).catch(function (err) {
        console.error("[lc-diagram]", err);
        var pre = document.createElement("pre");
        pre.style.cssText = "color:red;font-size:0.8em";
        pre.textContent = "[diagram] " + err;
        if (div.parentNode) div.parentNode.replaceChild(pre, div);
      });
    }

    // author classes land in the shared runtime once a .model or .inspector
    // block has run — redraw so the page's diagrams tell the whole story
    document.addEventListener("lc-model-changed", function () {
      if (!ready) return;
      ready.then(function (e) {
        rendered.forEach(function (r) {
          try { renderOne(e, r.div, r.arg, r.sm); } catch (err) { console.error("[lc-diagram]", err); }
        });
      }).catch(function () {});
    });

    if (window.lcRegisterUpgrader) {
      window.lcRegisterUpgrader(".diagram", upgradeDiagram);
    } else {
      document.querySelectorAll(".diagram").forEach(upgradeDiagram);
    }
  })();
</script>
