{%- comment -%}
Course join — the dedicated STUDENT wizard (distinct from /start, which is the
builder/LightNode journey). Activated by IAL on a link paragraph:

  [join](#)
  {: .course_join vault="uwm-build-ai/uwm-build-ai-vault" entry="courses/micro_build_ai/index.md" }

Five steps: ① GitHub account → ② course key (classic, repo scope — deep link
pre-fills scope + an org-named note) → ③ access check (tries the actual course
entry with the student's key; green = enrolled + key right → 📖 Open button)
→ ④ the bench: the student's private fork of the session hub, forked INTO the
org (org-owned, named <hub>-<login>) so teachers see the work at any time.

CLASSMATES MUST NOT — and that is a permission rule, not a wish. Private forks
inherit the upstream's TEAM permissions, so while the session team held pull on
the hub, every student on it could read every other bench. The team is now given
the VAULT only (nobody forks the vault); read on the hub is granted to each
student INDIVIDUALLY, because individual permissions are not inherited by forks.
The console's 🔒 column proves the team still has nothing on the hub. Org owners
keep seeing everything — ownership outranks both. (2026-08-11) Status is explicit — no bench → 🍴 fork; behind the hub →
🔄 sync (merge-upstream); the bench opens IN the runner (never the GitHub UI).
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
/* anchors-as-buttons: outrank the site's link color or the label is blue-on-blue */
.lc-join a.lcj-btn, .lc-join a.lcj-btn:visited { color: #fff; text-decoration: none; }
.lc-join .lcj-btn.alt, .lc-join a.lcj-btn.alt, .lc-join a.lcj-btn.alt:visited { background: #fff; color: #0066cc; border-color: #d0e3f5; }
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
    /* The LMS door: an iframe carries ONE src for every student, so the
       wizard resolves per visitor. ?hub=<session> scopes the bench step to
       THAT class (a student can hold several benches); ?go=bench forwards
       straight into the bench when everything is green. Plain /courses/join
       never forwards — the bench menu's 🎓 entry stays a status page. */
    var q = {};
    try { location.search.replace(/^\?/, "").split("&").forEach(function (kv) {
      var p = kv.split("="); if (p[0]) q[p[0]] = decodeURIComponent(p[1] || ""); }); } catch (e) {}
    var wantHub = q.hub || "";
    var goBench = q.go === "bench";
    var keyNote = encodeURIComponent("Lightcode course key — " + org);
    /* write:org lets the wizard ACCEPT the class invitation in-app (a student
       is admin of no org, so the scope is inert beyond that) — one click here
       instead of a trip through GitHub's UI */
    var keyUrl = "https://github.com/settings/tokens/new?scopes=repo,write:org&description=" + keyNote;
    var inviteUrl = "https://github.com/orgs/" + org + "/invitation";
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
      /* a REAL form with a named identity, exactly like the energy key below.
         A bare password field makes the browser hunt for a username to file
         the key under — and it grabs whatever text it saw last on the page
         (a grid cell said "Milwaukee" and became a credential). The readonly
         username gives the keychain its name; the browser then also OFFERS
         the key back on every device. Say yes to the save prompt — that is
         the design, under the right name. */
      '<form class="lcj-course" autocomplete="on">' +
      '<input type="text" name="username" value="lc-course-key" autocomplete="username" tabindex="-1" readonly aria-label="Key account name, used by your password manager" style="position:absolute;left:-9999px">' +
      '<div class="lcj-row"><input class="lcj-key" type="password" name="password" autocomplete="current-password" placeholder="ghp_…" spellcheck="false" aria-label="Course key">' +
      '<button type="submit" class="lcj-btn">Check key ✓</button></div>' +
      '</form>' +
      '<div class="lcj-msg" data-m="2"></div></div></div>' +

      '<div class="lcj-step off" data-n="3"><div class="lcj-head"><span class="lcj-num">3</span>Your enrollment</div>' +
      '<div class="lcj-body"><p style="margin-top:0">Your teacher enrolls you — that sends you a class <b>invitation</b>. Accept it right here:</p>' +
      '<div class="lcj-row"><button type="button" class="lcj-btn" data-a="accept">✅ Accept my invitation</button>' +
      '<button type="button" class="lcj-btn alt" data-a="checkaccess">Check my access ✓</button></div>' +
      '<div class="lcj-msg" data-m="3"></div>' +
      '<div class="lcj-row" style="display:none" data-open><a class="lcj-btn" href="' + openUrl + '">📖 Open the course →</a></div></div></div>' +

      '<div class="lcj-step off" data-n="4"><div class="lcj-head"><span class="lcj-num">4</span>Your bench</div>' +
      '<div class="lcj-body"><p style="margin-top:0">Your <b>bench</b> is your own private copy of the class workbench — visible only to you and your teachers. Create it once, keep it refreshed, and work: your teacher can see your bench at any time.</p>' +
      '<div class="lcj-msg" data-m="4"></div>' +
      '<div class="lcj-row" data-bench></div></div></div>' +

      '<div class="lcj-step off" data-n="5"><div class="lcj-head"><span class="lcj-num">5</span>Your energy key — the AI badge</div>' +
      '<div class="lcj-body"><p style="margin-top:0">The course’s AI helpers run on a second, free key — separate from your course key on purpose: one badge for your <b>work</b>, one for the AI’s <b>energy</b>. Create it (any Google account), paste it below, and when your browser offers to <b>save it as a password — say yes</b>: it will follow you to your other devices by itself.</p>' +
      '<div class="lcj-row"><a class="lcj-btn alt" href="https://aistudio.google.com/apikey" target="_blank" rel="noopener">⚡ Create the energy key →</a></div>' +
      '<form class="lcj-energy" autocomplete="on">' +
      '<input type="text" name="username" value="lc-gemini" autocomplete="username" tabindex="-1" readonly style="position:absolute;left:-9999px">' +
      '<div class="lcj-row"><input class="lcj-ekey" type="password" name="password" autocomplete="current-password" placeholder="AIza…" spellcheck="false">' +
      '<button type="submit" class="lcj-btn">Check key ✓</button></div>' +
      '</form>' +
      '<div class="lcj-msg" data-m="5"></div></div></div>';
    el.parentNode.replaceChild(wrap, el);

    var steps = {}; wrap.querySelectorAll(".lcj-step").forEach(function (s) { steps[s.getAttribute("data-n")] = s; });
    function msg(n, text, cls) { var m = wrap.querySelector('[data-m="' + n + '"]'); m.textContent = text; m.className = "lcj-msg " + (cls || ""); }
    function msgH(n, html, cls) { var m = wrap.querySelector('[data-m="' + n + '"]'); m.innerHTML = html; m.className = "lcj-msg " + (cls || ""); }
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
      var H = { Authorization: "Bearer " + p, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
      /* two stages so the message names the REAL blocker: repo visibility
         (enrollment/key) vs a missing lesson path (teacher-side publish) */
      fetch("https://api.github.com/repos/" + vault, { headers: H })
        .then(function (r0) {
          if (!r0.ok) {
            setState("3", "on");
            msg(3, auto ? "" : "⏳ Not yet: your key can’t see the course library. Click ✅ Accept my invitation above (or ask your teacher to enroll you), then check again.", auto ? "" : "err");
            return null;
          }
          return fetch("https://api.github.com/repos/" + vault + "/contents/" + entry, { headers: H });
        })
        .then(function (r) {
          if (!r) return;
          setState("3", "on");              // stays open — it hosts the door
          if (r.ok) {
            msg(3, "✅ You’re in — enjoy the course!", "ok");
            wrap.querySelector("[data-open]").style.display = "";
          } else {
            msg(3, "🎓 You HAVE access to the course library, but this lesson isn’t there (yet) — tell your teacher: “" + entry + " is missing from the vault”.", "err");
          }
          benchStart();                   // vault visible = enrolled → light the bench
        })
        .catch(function () { if (!auto) msg(3, "❌ Could not reach GitHub — try again.", "err"); });
    }

    /* ── step 4: the bench — a fork of the session hub INTO the org, named
       <hub>-<login>. Org-owned means the teacher reads the work at any time
       (owners see every org repo) and classmates never do (base permission
       none). The hub is discovered, not configured: with the student's key,
       the only template repo they can see in the org IS their session. */
    function sgh(path, opts) {
      opts = opts || {};
      opts.headers = { Authorization: "Bearer " + pat(), Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
      if (opts.body) { opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(opts.body); }
      return fetch("https://api.github.com" + path, opts);
    }
    var B = { hub: null, login: "", name: "", branch: "main" };
    function benchRow() { return wrap.querySelector("[data-bench]"); }

    /* the energy key as the DEVICE already holds it — agent.md owns the slot,
       so ask it; the raw read is the fallback when the engine isn't on the page */
    function haveEnergyKey() {
      if (window.lcBotAsk && window.lcBotAsk.ready) { try { return !!window.lcBotAsk.ready(); } catch (e) {} }
      try { return !!localStorage.getItem("lc_ai_key_gemini"); } catch (e) { return false; }
    }

    function benchStart() {
      setState("4", "on");
      /* A key already on this device means step 5 is DONE. The wizard used to
         reopen it on every visit — its own way of "asking every time after a
         refresh", even when nothing had been lost (Michel, 2026-08-05). */
      if (steps["5"] && !steps["5"].classList.contains("ok")) {
        if (haveEnergyKey()) {
          setState("5", "ok");
          msg(5, "✅ Your energy key is already saved on this device. Use “change” if you ever need a different one.", "ok");
        } else setState("5", "on");
      }
      msg(4, "Looking for your session…", ""); benchRow().innerHTML = "";
      var u = null; try { u = JSON.parse(localStorage.getItem("lc_gh_user") || "null"); } catch (e) {}
      (u && u.login ? Promise.resolve(u.login)
                    : sgh("/user").then(function (r) { return r.json(); }).then(function (d) { return d.login; }))
        .then(function (login) {
          B.login = login;
          return sgh("/orgs/" + org + "/repos?per_page=100").then(function (r) { return r.ok ? r.json() : []; });
        })
        .then(function (repos) {
          var hubs = (repos || []).filter(function (x) { return x.is_template && !x.fork; });
          if (wantHub) hubs = hubs.filter(function (x) { return x.name === wantHub; });
          if (!hubs.length) {
            msg(4, wantHub
              ? "🧑‍🏫 The session “" + wantHub + "” isn’t visible to you yet — your teacher enrolls you, then this step lights up."
              : "🧑‍🏫 No session is visible to you yet — your teacher adds you to one, then this step lights up.", "");
            return;
          }
          hubs.sort(function (a, b) { return new Date(b.updated_at || 0) - new Date(a.updated_at || 0); });
          B.hub = hubs[0]; B.name = B.hub.name + "-" + B.login;
          benchStatus();
        })
        .catch(function () { msg(4, "❌ Could not reach GitHub — reload to retry.", "err"); });
    }

    function benchStatus() {
      sgh("/repos/" + org + "/" + B.name)
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (repo) {
          if (!repo) { benchOffer(); return; }
          B.branch = repo.default_branch || "main";
          /* explicit status: how many hub commits the bench is missing */
          return sgh("/repos/" + org + "/" + B.name + "/compare/" + B.branch + "..." + org + ":" + B.hub.name + ":" + (B.hub.default_branch || "main"))
            .then(function (r) { return r.ok ? r.json() : { ahead_by: 0 }; })
            .then(function (cmp) { benchShow(cmp.ahead_by || 0); });
        })
        .catch(function () { msg(4, "❌ Could not reach GitHub — reload to retry.", "err"); });
    }

    function benchOffer() {
      msg(4, "🧰 No bench yet for session “" + B.hub.name + "” — create yours to start working:", "");
      benchRow().innerHTML = '<button type="button" class="lcj-btn" data-a="fork">🛠 Create my bench</button>';
    }

    function benchShow(behind) {
      /* the connection is a PAIR: step 2 stored the key, and THIS is the
         moment its repo half becomes known. Without it, every save="my/…"
         aimed at whatever repo was lying around from an earlier life (the
         author's site, or nothing at all) and the student's key answered
         404 for a repo it was never meant to cover. The bench is resolved
         per visitor from their own key, so pair them here. */
      try { localStorage.setItem("lc_ed_repo", org + "/" + B.name); } catch (e) {}
      msgH(4, "🛠 Your bench: <b>" + org + "/" + B.name + "</b> — " +
        (behind ? "⬆️ the hub has <b>" + behind + " update" + (behind > 1 ? "s" : "") + "</b> you don’t have yet."
                : "✅ up to date with the hub."), behind ? "" : "ok");
      /* the bench opens IN the runner — students never land in the GitHub UI;
         xray Keep commits their edits straight back to the bench */
      /* Carry the frame flags through. An LMS frames ONE url for every
         student and the wizard resolves the bench per visitor — so the flags
         have to survive the hop, or the bench opens with the full platform
         inside a page that is supposed to be focused. */
      var pass = ["focus", "editable", "navigable", "open"]
        .filter(function (k) { return q[k] !== undefined; })
        .map(function (k) { return k + "=" + encodeURIComponent(q[k]); }).join("&");
      var benchOpen = (window.lcHref ? window.lcHref("/run.html") : "/run.html")
        + (pass ? "?" + pass : "") + "#src=gh:" + org + "/" + B.name + "/index.md";
      function paintBenchRow() {
        benchRow().innerHTML =
          (behind ? '<button type="button" class="lcj-btn" data-a="sync">🔄 Refresh from hub</button>' : "") +
          '<a class="lcj-btn' + (behind ? " alt" : "") + '" href="' + benchOpen + '">🛠 Open my bench →</a>';
      }
      /* forward only when green AND the root actually exists in the bench —
         a bench that hasn't synced the index.md rename must NOT be flung at a
         404 (which the runner mis-reads as a key wall). */
      if (goBench && !behind) {
        sgh("/repos/" + org + "/" + B.name + "/contents/index.md")
          .then(function (r) {
            if (r.ok) { location.replace(benchOpen); return; }
            msg(4, "🔄 One more step — Refresh your bench to get the latest layout, then open it:", "");
            behind = behind || 1; paintBenchRow();
          })
          .catch(function () { paintBenchRow(); });
        return;
      }
      paintBenchRow();
    }

    /* step 5: a LIVE check against the provider — the same trip a desk
       makes. Success submits the form so the password manager offers to
       save (username lc-gemini, the exact identity every agent panel uses:
       autofill then hands the key to any desk on any page, any device). */
    /* step 2 submits through its form (Enter or the button) so the browser
       files the key under the lc-course-key identity instead of stealing a
       username from the page. The click delegation below skips submit
       buttons — one path, no double-fire. */
    var courseForm = wrap.querySelector(".lcj-course");
    if (courseForm) courseForm.addEventListener("submit", function (e) {
      e.preventDefault();
      checkKey(wrap.querySelector('.lcj-course button[type="submit"]'));
    });

    var energyForm = wrap.querySelector(".lcj-energy");
    if (energyForm) energyForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var k = (wrap.querySelector(".lcj-ekey").value || "").trim();
      if (!k) { msg(5, "Paste the key first — it starts with AIza…", "err"); return; }
      msg(5, "⏳ Asking the provider…", "");
      /* One code path for saving the energy key: agent.md owns the storage and
         the provider id, and it tells every open desk on the page. The door
         used to write "lc_ai_key_gemini" by hand — a second place to keep in
         step, and open panels never heard about it. The raw write stays as the
         fallback for a door rendered without the agent engine on the page. */
      var keep = function () {
        if (window.lcBotAsk && window.lcBotAsk.connect) { window.lcBotAsk.connect(k); return; }
        try { localStorage.setItem("lc_ai_key_gemini", k); } catch (e) {}
      };
      /* SAVE FIRST, then report. A key is only proven WRONG by the provider
         saying so (400/401); every other outcome — a 403 for a website-limited
         key, an ad-blocker eating the request, a VPN, a firewall — says nothing
         about the key and everything about the road. Throwing it away on those
         is what made a learner paste it again after every refresh (Michel,
         2026-08-05). Keep it, say plainly what we could and could not check. */
      fetch("https://generativelanguage.googleapis.com/v1beta/openai/models",
            { headers: { Authorization: "Bearer " + k } })
        .then(function (r) {
          if (r.ok) {
            /* saved like the course key — every desk on every page opens
               connected; the password manager remains the cross-DEVICE copy */
            keep();
            setState("5", "ok");
            msg(5, "✅ The key works — saved. Every AI helper in the course now opens connected on this device; if your browser also offered to save it, that copy follows you to your other devices.", "ok");
          } else if (r.status === 400 || r.status === 401) {
            msg(5, "❌ The provider rejected this key (" + r.status + ") — it is not a valid key. Copy the whole key from AI Studio and try again.", "err");
          } else {
            /* NOT setState ok: a done step folds its body away, and this
               message is the one a learner most needs to read. The key is
               saved either way — that is the part that matters. */
            keep();
            msg(5, "🔑 Key saved — but the provider would not let us test it (" + r.status + "). Your key is probably fine; it may be limited to certain websites, or the service is not switched on for it yet. Try an AI helper in a lesson: if it answers, you are set.", "");
          }
        })
        .catch(function () {
          keep();
          msg(5, "🔑 Key saved — but we could not reach the provider to test it. An ad-blocker, VPN or firewall may be on the road. Your key is kept, so you will not have to paste it again; clear the road and try an AI helper in a lesson.", "");
        });
    });

    wrap.addEventListener("click", function (e) {
      var b = e.target.closest("[data-a]"); if (!b) return;
      var a = b.getAttribute("data-a");
      if (a === "have") { setState("1", "ok"); setState("2", "on"); }
      if (a === "checkaccess") checkAccess(false);
      if (a === "fork") {
        b.disabled = true; msg(4, "🛠 Creating your bench… GitHub is copying the hub in.", "");
        sgh("/repos/" + org + "/" + B.hub.name + "/forks",
            { method: "POST", body: { organization: org, name: B.name, default_branch_only: true } })
          .then(function (r) {
            if (r.status === 202 || r.ok) {
              /* forking is async server-side — poll until the bench answers */
              var tries = 0;
              (function poll() {
                sgh("/repos/" + org + "/" + B.name).then(function (r2) {
                  if (r2.ok) benchStatus();
                  else if (++tries < 10) setTimeout(poll, 900);
                  else msg(4, "⏳ Still setting up your bench — reload this page in a minute.", "");
                });
              })();
            }
            else return r.json().then(function (d) {
              b.disabled = false;
              msg(4, "❌ Couldn't create your bench: " + (d.message || "HTTP " + r.status) + " — your teacher may need to allow members to create private repositories (cockpit, step 3).", "err");
            });
          })
          .catch(function () { b.disabled = false; msg(4, "❌ Could not reach GitHub — try again.", "err"); });
      }
      if (a === "sync") {
        b.disabled = true; msg(4, "🔄 Refreshing from the hub…", "");
        sgh("/repos/" + org + "/" + B.name + "/merge-upstream", { method: "POST", body: { branch: B.branch } })
          .then(function (r) {
            if (r.ok) { benchStatus(); return; }
            b.disabled = false;
            if (r.status === 409) msg(4, "⚠️ Your bench and the hub changed the same lines — tell your teacher (merge conflict).", "err");
            else msg(4, "❌ Refresh failed (HTTP " + r.status + ") — try again.", "err");
          })
          .catch(function () { b.disabled = false; msg(4, "❌ Could not reach GitHub — try again.", "err"); });
      }
      if (a === "accept") {
        var p0 = pat(); if (!p0) { msg(3, "Connect your key first (step 2).", "err"); return; }
        b.disabled = true; msg(3, "Accepting…", "");
        /* accept the org invitation in-app; needs the write:org scope the key
           link pre-selects. Any failure falls back to GitHub's focused
           invitation page — one green button, not the notifications jungle. */
        fetch("https://api.github.com/user/memberships/orgs/" + org,
              { method: "PATCH",
                headers: { Authorization: "Bearer " + p0, Accept: "application/vnd.github+json",
                           "Content-Type": "application/json", "X-GitHub-Api-Version": "2022-11-28" },
                body: JSON.stringify({ state: "active" }) })
          .then(function (r) {
            b.disabled = false;
            if (r.ok) { msg(3, "✅ Invitation accepted — checking your access…", "ok"); checkAccess(false); }
            else {
              msg(3, "", "");
              var m = wrap.querySelector('[data-m="3"]');
              m.className = "lcj-msg err";
              m.innerHTML = "Couldn’t accept from here (no pending invitation, or the key lacks the org permission). " +
                "<a href=\"" + inviteUrl + "\" target=\"_blank\" rel=\"noopener\">Open your invitation →</a> — one green button — then come back and Check my access.";
            }
          })
          .catch(function () { b.disabled = false; msg(3, "❌ Could not reach GitHub — try again.", "err"); });
      }
      if (a === "checkkey") { checkKey(b); }
    });

    function checkKey(b) {
        var val = wrap.querySelector(".lcj-key").value.trim();
        if (!val) { msg(2, "Paste your key first.", "err"); return; }
        if (b) b.disabled = true;
        msg(2, "Checking…", "");
        fetch("https://api.github.com/user", { headers: { Authorization: "Bearer " + val, "X-GitHub-Api-Version": "2022-11-28" } })
          .then(function (r) {
            var scopes = r.headers.get("X-OAuth-Scopes") || "";
            return r.json().then(function (u) { return { ok: r.ok, user: u, scopes: scopes }; });
          })
          .then(function (d) {
            if (b) b.disabled = false;
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
          .catch(function () { if (b) b.disabled = false; msg(2, "❌ Could not reach GitHub — check your connection.", "err"); });
    }

    /* returning student: key already stored → straight to the door */
    if (pat()) { setState("1", "ok"); setState("2", "ok"); setState("3", "on"); checkAccess(true); }
    else setState("1", "on");
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.course_join", upgrade);
})();
</script>
