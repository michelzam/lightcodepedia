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

    /* public repo → the runs API works without auth; a PAT (when the ✏️
       editor is connected) just raises the rate limit. Never gate on sign-in. */
    var pat = localStorage.getItem("lc_ed_pat") || "";

    /* repo: attribute → this very site → editor setting → user guess.
       This is the node's OWN deploy log, and GitHub Pages exposes its repo
       to Jekyll — so lab, pedia and every fork self-resolve. Guesses come
       last: they once shadowed the lab with pedia's runs. */
    var repo = repoAttr || "{{ site.github.repository_nwo | default: '' }}";
    if (!repo) repo = localStorage.getItem("lc_ed_repo") || "";
    if (!repo) {
      var u = null; try { u = JSON.parse(localStorage.getItem("lc_gh_user") || "null"); } catch (e) {}
      if (u && u.login) repo = u.login + "/lightcodepedia";
    }
    repo = repo.trim().replace(/^https?:\/\/github\.com\//, "").replace(/\.git$/, "").replace(/^\/+|\/+$/g, "");
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
    /* Requests with Authorization / custom headers need a CORS preflight, and
       some networks (mobile relays, middleboxes) silently kill the OPTIONS —
       WebKit then reports only "Load failed". The repo is public, so on any
       network-level failure retry as a BARE simple GET: no headers at all →
       no preflight → nothing to kill. Auth only raises the rate limit. */
    function ghFetch(url) {
      var H = { "X-GitHub-Api-Version": "2022-11-28", Accept: "application/vnd.github+json" };
      if (pat) H.Authorization = "Bearer " + pat;
      return fetch(url, { headers: H }).catch(function () { return fetch(url); });
    }
    function fetchRuns() {
      spEl.textContent = "Loading…";
      ghFetch("https://api.github.com/repos/" + repo + "/actions/runs?per_page=" + count + "&exclude_pull_requests=true")
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
        /* frugal: keep live-polling only while the bar is actually visible
           (inside an open accordion section); shut sections keep the first
           numbers and refresh on demand via the button */
        if (ongoing && polls < 25 && bar.offsetParent !== null) {
          polls++; pollTimer = setTimeout(fetchRuns, 12000);
        }
        else polls = 0;
      })
      .catch(function (e) {
        /* HTTP errors carry a status; anything else was a network failure
           that survived even the bare no-preflight retry */
        spEl.textContent = /403/.test(e.message)
          ? "⚠️ rate-limited — try again in a few minutes"
          : /GitHub API/.test(e.message)
            ? "⚠️ " + e.message
            : "⚠️ network error — tap ↻ to retry";
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
