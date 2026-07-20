{%- comment -%}
Course join — the dedicated STUDENT wizard (distinct from /start, which is the
builder/LightNode journey). Activated by IAL on a link paragraph:

  [join](#)
  {: .course_join vault="uwm-build-ai/uwm-build-ai-vault" entry="courses/micro_build_ai/index.md" }

Three steps: ① GitHub account → ② course key (classic, repo scope — deep link
pre-fills scope + an org-named note) → ③ access check (tries the actual course
entry with the student's key; green = enrolled + key right → 📖 Open button).
The check is live truth against the API, never cached. Done steps reopen via
"change" (cockpit rule). Shares the app's identity storage (lc_ed_pat).
{%- endcomment -%}
<style>
.lc-join { margin: 1em 0; }
.lc-join .lcj-step { border: 1px solid #ddd; border-radius: 10px; margin-bottom: 0.9em; overflow: hidden; }
.lc-join .lcj-step.on { border-color: #0066cc; box-shadow: 0 0 0 3px #e8f0fe; }
.lc-join .lcj-step.ok { border-color: #2a9d2a; }
.lc-join .lcj-step.off { opacity: 0.5; }
.lc-join .lcj-step.off .lcj-body { display: none; }
.lc-join .lcj-step.ok .lcj-body { display: none; }
.lc-join .lcj-head { display: flex; align-items: center; gap: 10px; padding: 0.7em 1em; background: #fafafa; font-weight: 600; }
.lc-join .lcj-step.on .lcj-head { background: #e8f0fe; }
.lc-join .lcj-step.ok .lcj-head { background: #f0faf0; }
.lc-join .lcj-num { width: 26px; height: 26px; border-radius: 50%; background: #e5e7eb; display: inline-flex; align-items: center; justify-content: center; font-size: 0.85em; flex: none; }
.lc-join .lcj-step.on .lcj-num { background: #0066cc; color: #fff; }
.lc-join .lcj-step.ok .lcj-num { background: #2a9d2a; color: #fff; }
.lc-join .lcj-change { margin-left: auto; font-size: 0.8em; color: #0066cc; cursor: pointer; font-weight: 500; }
.lc-join .lcj-body { padding: 1em; }
.lc-join .lcj-btn { display: inline-block; padding: 0.45em 1em; border-radius: 8px; border: 1px solid #0066cc; background: #0066cc; color: #fff; font-weight: 600; cursor: pointer; text-decoration: none; font-size: 0.92em; }
.lc-join .lcj-btn.alt { background: #fff; color: #0066cc; border-color: #d0e3f5; }
.lc-join .lcj-btn:disabled { opacity: 0.5; cursor: default; }
.lc-join .lcj-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-top: 0.7em; }
.lc-join .lcj-key { flex: 1; min-width: 220px; padding: 0.45em 0.7em; border: 1px solid #ccc; border-radius: 8px; font-family: monospace; }
.lc-join .lcj-msg { margin-top: 0.6em; font-size: 0.9em; }
.lc-join .lcj-msg.ok { color: #2a7d2a; }
.lc-join .lcj-msg.err { color: #b3261e; }
</style>
<script>
(function () {
  if (window._lcCourseJoinReady) return;
  window._lcCourseJoinReady = true;

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return; el.dataset.lcUpgraded = "1";
    var vault = el.getAttribute("vault") || "";
    var entry = el.getAttribute("entry") || "";
    if (!vault || !entry) return;
    var org = vault.split("/")[0];
    var keyNote = encodeURIComponent("Lightcode course key — " + org);
    var keyUrl = "https://github.com/settings/tokens/new?scopes=repo&description=" + keyNote;
    var openUrl = (window.lcHref ? window.lcHref("/run.html") : "/run.html") + "#src=gh:" + vault + "/" + entry;

    var wrap = document.createElement("div");
    wrap.className = "lc-join";
    wrap.innerHTML =
      '<div class="lcj-step" data-n="1"><div class="lcj-head"><span class="lcj-num">1</span>Create a GitHub account</div>' +
      '<div class="lcj-body"><p style="margin-top:0">GitHub hosts the course and proves who you are. Already have an account? Just confirm.</p>' +
      '<div class="lcj-row"><a class="lcj-btn alt" href="https://github.com/signup" target="_blank" rel="noopener">Open GitHub signup →</a>' +
      '<button type="button" class="lcj-btn" data-a="have">I have an account ✓</button></div></div></div>' +

      '<div class="lcj-step off" data-n="2"><div class="lcj-head"><span class="lcj-num">2</span>Create your course key</div>' +
      '<div class="lcj-body"><p style="margin-top:0">A course key lets this site open your private lessons. The link pre-fills the right scope and name — set <b>Expiration → Custom</b> past your course’s end (a semester), <b>Generate token</b>, copy, paste below.</p>' +
      '<div class="lcj-row"><a class="lcj-btn alt" href="' + keyUrl + '" target="_blank" rel="noopener">🪜 Create the key →</a></div>' +
      '<div class="lcj-row"><input class="lcj-key" type="password" placeholder="ghp_…" autocomplete="off" spellcheck="false">' +
      '<button type="button" class="lcj-btn" data-a="checkkey">Check key ✓</button></div>' +
      '<div class="lcj-msg" data-m="2"></div></div></div>' +

      '<div class="lcj-step off" data-n="3"><div class="lcj-head"><span class="lcj-num">3</span>Your enrollment</div>' +
      '<div class="lcj-body"><p style="margin-top:0">Your teacher enrolls you; GitHub emails you an <b>invitation</b> — accept it, then check:</p>' +
      '<div class="lcj-row"><a class="lcj-btn alt" href="https://github.com/notifications" target="_blank" rel="noopener">📬 My invitations →</a>' +
      '<button type="button" class="lcj-btn" data-a="checkaccess">Check my access ✓</button></div>' +
      '<div class="lcj-msg" data-m="3"></div>' +
      '<div class="lcj-row" style="display:none" data-open><a class="lcj-btn" href="' + openUrl + '">📖 Open the course →</a></div></div></div>';
    el.parentNode.replaceChild(wrap, el);

    var steps = {}; wrap.querySelectorAll(".lcj-step").forEach(function (s) { steps[s.getAttribute("data-n")] = s; });
    function msg(n, text, cls) { var m = wrap.querySelector('[data-m="' + n + '"]'); m.textContent = text; m.className = "lcj-msg " + (cls || ""); }
    function setState(n, state) {           // state: on | ok | off
      var s = steps[n]; s.classList.remove("on", "ok", "off");
      if (state !== "open") s.classList.add(state);
      var head = s.querySelector(".lcj-head");
      var old = head.querySelector(".lcj-change"); if (old) old.remove();
      if (state === "ok") {                 // done steps reopen (cockpit rule)
        var chg = document.createElement("span");
        chg.className = "lcj-change"; chg.textContent = "change";
        chg.addEventListener("click", function () {
          setState(n, "on");
          if (n === "2") { var k = wrap.querySelector(".lcj-key"); k.value = ""; setTimeout(function(){ k.focus(); }, 200); msg(2, "", ""); }
        });
        head.appendChild(chg);
      }
    }

    function pat() { try { return localStorage.getItem("lc_ed_pat") || ""; } catch (e) { return ""; } }

    function checkAccess(auto) {
      var p = pat(); if (!p) { setState("3", "on"); msg(3, "Connect your key first (step 2).", "err"); return; }
      msg(3, "Checking…", "");
      fetch("https://api.github.com/repos/" + vault + "/contents/" + entry,
            { headers: { Authorization: "Bearer " + p, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" } })
        .then(function (r) {
          if (r.ok) {
            setState("3", "on");            // stays open — it hosts the door
            msg(3, "✅ You’re in — enjoy the course!", "ok");
            wrap.querySelector("[data-open]").style.display = "";
          } else {
            setState("3", "on");
            msg(3, auto ? "" : "⏳ Not yet: your key is valid but can’t reach the course. Accept your invitation (📬 above), or ask your teacher to enroll you — then check again.", auto ? "" : "err");
          }
        })
        .catch(function () { if (!auto) msg(3, "❌ Could not reach GitHub — try again.", "err"); });
    }

    wrap.addEventListener("click", function (e) {
      var b = e.target.closest("[data-a]"); if (!b) return;
      var a = b.getAttribute("data-a");
      if (a === "have") { setState("1", "ok"); setState("2", "on"); }
      if (a === "checkaccess") checkAccess(false);
      if (a === "checkkey") {
        var val = wrap.querySelector(".lcj-key").value.trim();
        if (!val) { msg(2, "Paste your key first.", "err"); return; }
        b.disabled = true; msg(2, "Checking…", "");
        fetch("https://api.github.com/user", { headers: { Authorization: "Bearer " + val, "X-GitHub-Api-Version": "2022-11-28" } })
          .then(function (r) {
            var scopes = r.headers.get("X-OAuth-Scopes") || "";
            return r.json().then(function (u) { return { ok: r.ok, user: u, scopes: scopes }; });
          })
          .then(function (d) {
            b.disabled = false;
            if (!d.ok) { msg(2, "❌ Key not recognised — generate a new one and try again.", "err"); return; }
            var hasRepo = val.indexOf("github_pat_") === 0 ||
              d.scopes.split(",").map(function (s) { return s.trim(); }).indexOf("repo") >= 0;
            if (!hasRepo) { msg(2, "⚠️ Key is valid but missing the repo permission — regenerate with the repo box checked.", "err"); return; }
            try {
              localStorage.setItem("lc_ed_pat", val);
              localStorage.setItem("lc_gh_user", JSON.stringify(d.user));
              localStorage.setItem("lc_gh_user_for", val);
            } catch (e) {}
            msg(2, "✅ Key saved — logged in as @" + d.user.login + ".", "ok");
            if (window.lcUserPillRefresh) window.lcUserPillRefresh();
            setTimeout(function () { setState("1", "ok"); setState("2", "ok"); setState("3", "on"); checkAccess(true); }, 600);
          })
          .catch(function () { b.disabled = false; msg(2, "❌ Could not reach GitHub — check your connection.", "err"); });
      }
    });

    /* returning student: key already stored → straight to the door */
    if (pat()) { setState("1", "ok"); setState("2", "ok"); setState("3", "on"); checkAccess(true); }
    else setState("1", "on");
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.course_join", upgrade);
})();
</script>
