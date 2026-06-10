{%- comment -%}
PyTutor — pythontutor.com step-visualiser iframe, activated from md + IAL:
a Python code block + {: .pytutor height="400" bound-to="run-id" }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window._lcPytutorReady) return;
  window._lcPytutorReady = true;

  function upgradePyTutor(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var code = el.querySelector("code");
    var initialCode = (code ? code.textContent : el.textContent).trim();
    if (!initialCode) return;
    var h       = el.getAttribute("height") || "400";
    var boundTo = el.getAttribute("bound-to");

    function buildUrl(codeStr) {
      return "https://pythontutor.com/iframe-embed.html#code="
        + encodeURIComponent(codeStr)
        + "&py=3&origin=opt-frontend.js&cumulative=false&heapPrimitives=newin&textReferences=false";
    }

    function makeFrame(src) {
      var f = document.createElement("iframe");
      f.src = src; f.width = "100%"; f.height = h + "px";
      f.style.border = "none"; f.setAttribute("loading", "lazy");
      return f;
    }

    var f = makeFrame(buildUrl(initialCode));
    el.parentNode.replaceChild(f, el);

    if (boundTo) {
      var runEl = document.getElementById("lc-pyrun-" + boundTo);
      if (runEl) {
        var ta = runEl.querySelector(".lc-pyrun-code");
        if (ta) {
          var _pytTimer = null;
          ta.addEventListener("input", function() {
            clearTimeout(_pytTimer);
            _pytTimer = setTimeout(function() {
              // Replace the element entirely — setting src on a hash-based URL
              // doesn't trigger an iframe reload in any browser.
              var newF = makeFrame(buildUrl(ta.value));
              f.parentNode.replaceChild(newF, f);
              f = newF;
            }, 600);
          });
        }
      }
    }
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.pytutor, pre.pytutor", upgradePyTutor);
  }

})();
</script>
