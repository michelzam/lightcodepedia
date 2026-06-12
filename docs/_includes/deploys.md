{%- comment -%}
Deploys — GitHub Actions run list for this repository (the live
deploy log). Activated by IAL: {: .deploys }.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window._lcDeploysReady) return;
  window._lcDeploysReady = true;

  // ── GitHub deploy/activity list (Actions runs) ─────────────────────────────
  function upgradeDeploys(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var count    = parseInt(el.getAttribute("count") || "8", 10);
    var repoAttr = el.getAttribute("repo") || "";
    var dsId     = el.getAttribute("id") || "deploys";

    /* hide source element like a .dataset block */
    el.style.display = "none";

    /* inject a small control bar right after the hidden element */
    var bar = document.createElement("div");
    bar.className = "lc-deploys-bar";
    /* the bar IS the publisher of dsId — modelcheck resolves bind=
       declarations against it even while signed-out (no data published) */
    bar.setAttribute("data-lc-id", dsId);
    bar.innerHTML = [
      '<style>',
      '.lc-deploys-bar{display:flex;align-items:center;gap:8px;font-size:.82em;color:#6b7280;margin:.25em 0}',
      '.lc-deploys-bar strong{color:#374151}',
      '.lc-deploys-bar-sp{margin-left:auto}',
      '.lc-deploys-bar-btn{border:1px solid #d1d5db;background:#fff;border-radius:4px;cursor:pointer;font-size:1em;padding:0 .4em;line-height:1.7;color:#374151}',
      '.lc-deploys-bar-btn:hover{background:#f3f4f6}',
      '</style>',
      '<strong>🚀 Deploys</strong>',
      '<span class="lc-deploys-bar-sp" id="lc-dep-sp-' + dsId + '"></span>',
      '<button class="lc-deploys-bar-btn" id="lc-dep-btn-' + dsId + '" title="Refresh">↻</button>'
    ].join("");
    el.parentNode.insertBefore(bar, el.nextSibling);

    var spEl  = bar.querySelector("#lc-dep-sp-"  + dsId);
    var btnEl = bar.querySelector("#lc-dep-btn-" + dsId);

    var pat = localStorage.getItem("lc_ed_pat") || "";
    if (!pat) {
      spEl.innerHTML = '🔒 <a href="#" style="color:inherit">Sign in</a> to see deployment activity';
      btnEl.style.display = "none"; return;
    }

    var repo = repoAttr || localStorage.getItem("lc_ed_repo") || "";
    if (!repo) {
      var u = null; try { u = JSON.parse(localStorage.getItem("lc_gh_user") || "null"); } catch (e) {}
      if (u && u.login) repo = u.login + "/lightcodepedia";
    }
    if (!repo || repo.indexOf("/") < 0) { spEl.textContent = "⚠️ No repo configured"; return; }

    function timeAgo(iso) {
      var s = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
      if (s < 60) return s + "s ago";
      var m = Math.floor(s / 60); if (m < 60) return m + "m ago";
      var h = Math.floor(m / 60); if (h < 24) return h + "h ago";
      return Math.floor(h / 24) + "d ago";
    }
    function statusIcon(r) {
      if (r.status !== "completed") {
        return r.status === "queued" || r.status === "waiting" || r.status === "pending" ? "⏳" : "🔄";
      }
      switch (r.conclusion) {
        case "success":   return "✅";
        case "failure":
        case "timed_out": return "❌";
        case "cancelled": return "🚫";
        case "skipped":   return "⏭️";
        default:          return "⚪";
      }
    }
    function normalize(runs) {
      return runs.map(function (r) {
        var commit = ((r.display_title || (r.head_commit && r.head_commit.message) || r.name || "Run") + "").split("\n")[0];
        var state  = r.status === "completed" ? (r.conclusion || "done") : r.status.replace(/_/g, " ");
        var author = r.actor && r.actor.login ? "@" + r.actor.login : "";
        return { status: statusIcon(r), commit: commit, workflow: r.name || "", state: state,
                 when: timeAgo(r.created_at), author: author, url: r.html_url || "" };
      });
    }

    var pollTimer = null, polls = 0;
    function fetchRuns() {
      spEl.textContent = "Loading…";
      fetch("https://api.github.com/repos/" + repo + "/actions/runs?per_page=" + count, {
        headers: { Authorization: "Bearer " + pat, "X-GitHub-Api-Version": "2022-11-28", Accept: "application/vnd.github+json" }
      })
      .then(function (r) {
        var rem = parseInt(r.headers.get("X-RateLimit-Remaining") || "-1", 10);
        if (rem >= 0) localStorage.setItem("lc_rate_remaining", String(rem));
        if (!r.ok) throw new Error("GitHub API " + r.status);
        return r.json();
      })
      .then(function (data) {
        var runs = (data.workflow_runs || []).slice(0, count);
        if (!runs.length) {
          if (window.lcSetDataset) window.lcSetDataset(dsId, []);
          spEl.textContent = "No runs yet"; return;
        }
        var rows = normalize(runs);
        if (window.lcSetDataset) window.lcSetDataset(dsId, rows);
        var ongoing = runs.some(function (r) { return r.status !== "completed"; });
        spEl.textContent = ongoing ? "● live" : "updated " + new Date().toLocaleTimeString();
        clearTimeout(pollTimer);
        if (ongoing && polls < 25) { polls++; pollTimer = setTimeout(fetchRuns, 12000); }
        else polls = 0;
      })
      .catch(function (e) {
        spEl.textContent = "⚠️ " + e.message;
        if (window.lcSetDataset) window.lcSetDataset(dsId, []);
      });
    }
    btnEl.addEventListener("click", function () { polls = 0; fetchRuns(); });
    window.addEventListener("pagehide", function () { clearTimeout(pollTimer); });
    fetchRuns();
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.deploys", upgradeDeploys);
  }

})();
</script>
