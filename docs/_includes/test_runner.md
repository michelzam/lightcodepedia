{%- comment -%}
Test runner — in-app buttons to dispatch the UX Tests workflow without leaving
the LC app (no terminal, no GitHub web UI). Activated by IAL {: .test_runner }
on a link paragraph (see docs/nodes.md, "UX test results").

Author-only: the control renders only for a connected builder (a PAT in
localStorage), so anonymous visitors — and the public pedia site — never see
it. "Run all" dispatches the whole suite; "Run failing" reads the red scenarios
from the last published ux-results.json and runs only those (behave -n) — a fast
turnaround when you're chasing a few reds. Mirrors the Publish gate in topbar.md.
{%- endcomment -%}
<style>
.lc-ci-runner { display: flex; align-items: center; gap: 0.5em; flex-wrap: wrap; margin: 0.6em 0; }
.lc-ci-btn { font-size: 0.85em; font-weight: 600; padding: 0.35em 0.8em; border-radius: 8px;
  border: 1px solid #d0e3f5; background: #fff; color: #0066cc; cursor: pointer; }
.lc-ci-btn:hover:not(:disabled) { background: #f0f6ff; }
.lc-ci-btn:disabled { color: #9ca3af; border-color: #e5e7eb; cursor: default; }
.lc-ci-status { font-size: 0.82em; color: #6b7280; }
</style>
<script>
(function () {
  if (window._lcTestRunnerReady) return;
  window._lcTestRunnerReady = true;

  var REPO = {{ site.github.repository_nwo | default: "" | jsonify }};

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    /* author-only: no PAT (or no repo) → this control does not exist */
    if (!pat || !REPO) { if (el.parentNode) el.parentNode.removeChild(el); return; }

    var wrap = document.createElement("div");
    wrap.className = "lc-ci-runner";
    wrap.innerHTML =
      '<button type="button" class="lc-ci-btn" data-a="all">🧪 Run all</button>' +
      '<button type="button" class="lc-ci-btn" data-a="failing" disabled>🧪 Run failing…</button>' +
      '<span class="lc-ci-status"></span>';
    el.parentNode.replaceChild(wrap, el);
    var status  = wrap.querySelector(".lc-ci-status");
    var failBtn = wrap.querySelector('[data-a="failing"]');
    var failNames = [];

    /* which scenarios were red last run — so "Run failing" runs only those */
    fetch(window.lcHref ? window.lcHref("/assets/ux-results.json") : "/assets/ux-results.json")
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (rows) {
        failNames = (rows || [])
          .filter(function (x) { return String(x.status || "").indexOf("❌") >= 0; })
          .map(function (x) { return String(x.scenario || ""); })
          .filter(Boolean);
        if (failNames.length) { failBtn.disabled = false; failBtn.textContent = "🧪 Run failing (" + failNames.length + ")"; }
        else failBtn.textContent = "✓ none failing";
      })
      .catch(function () { failBtn.textContent = "🧪 Run failing"; });

    function dispatch(inputs, label) {
      status.textContent = "🚀 launching…";
      var body = { ref: "main" }; if (inputs) body.inputs = inputs;
      fetch("https://api.github.com/repos/" + REPO + "/actions/workflows/ux-tests.yml/dispatches", {
        method: "POST",
        headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "Content-Type": "application/json" },
        body: JSON.stringify(body)
      }).then(function (r) {
        status.textContent = (r.status === 204) ? "✔ " + label + " running — watch 🚀 Deploys above"
          : (r.status === 403 || r.status === 404) ? "❌ PAT lacks Actions read/write on this repo"
          : "❌ HTTP " + r.status;
      }).catch(function () { status.textContent = "❌ network error — try again"; })
        .then(function () { setTimeout(function () { status.textContent = ""; }, 9000); });
    }

    /* behave -n is a regex — escape each name to a literal, join as alternation */
    function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

    wrap.addEventListener("click", function (e) {
      var b = e.target.closest(".lc-ci-btn"); if (!b || b.disabled) return;
      if (b.getAttribute("data-a") === "all") {
        if (window.confirm("Run the full UX suite against the live site?")) dispatch(null, "full suite");
      } else if (failNames.length) {
        dispatch({ scenarios: failNames.map(esc).join("|") }, failNames.length + " failing");
      }
    });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.test_runner", upgrade);
})();
</script>
