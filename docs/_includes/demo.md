{%- comment -%}
Demo — record a demonstration session (the "black box" to the recorder's camera).
The student demonstrates how to use / how to build something; this logs the
learning actions (form/slider edits, clicks, quiz answers, timings, pause gaps),
not keystrokes or screen. Start / Pause / Resume / Finish, then Export one JSON
(name/id + event log + summary + sha-256 + optional YouTube link).

  Demonstrate: build a form
  {: .demo #build_a_form title="Build a form" }

Optional video reuses the existing .recorder (screen + face → YouTube): the 🎥
button opens it; paste the resulting link into the export before downloading.
Runs standalone and inside an iframe (log is in-memory; localStorage is only a
crash-backup, so third-party-storage limits don't break it). Auto-included by
docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-demo { border: 1px solid #d8d8e0; border-radius: 10px; margin: 1em 0; background: #fff; font-size: 0.92em; overflow: hidden; }
.lc-demo-hd { display: flex; align-items: center; gap: 0.6em; padding: 0.55em 0.85em; background: #1e1e2e; color: #cdd6f4; flex-wrap: wrap; }
.lc-demo-title { font-weight: 600; }
.lc-demo-dot { width: 9px; height: 9px; border-radius: 50%; background: #555; }
.lc-demo-dot.live { background: #f33; animation: lcDemoBlink 1s infinite; }
.lc-demo-dot.paused { background: #e0a800; }
@keyframes lcDemoBlink { 0%,100%{opacity:1} 50%{opacity:.25} }
.lc-demo-timer { font-variant-numeric: tabular-nums; font-weight: 700; margin-left: auto; }
.lc-demo-body { padding: 0.75em 0.9em; }
.lc-demo-row { display: flex; gap: 0.5em; align-items: center; flex-wrap: wrap; }
.lc-demo input[type=text] { padding: 0.4em 0.55em; border: 1px solid #ccc; border-radius: 6px; font: inherit; }
.lc-demo-btn { padding: 0.45em 1em; border: none; border-radius: 6px; cursor: pointer; font: inherit; font-weight: 600; }
.lc-demo-start { background: #0066cc; color: #fff; } .lc-demo-start:hover { background: #0052a3; }
.lc-demo-pause { background: #444; color: #fff; }
.lc-demo-resume { background: #1a7a1a; color: #fff; }
.lc-demo-finish { background: #c00; color: #fff; }
.lc-demo-vid { background: #eee; color: #333; }
.lc-demo-export { background: #166534; color: #fff; }
.lc-demo-copy { background: #eef2ff; color: #1e3a8a; border: 1px solid #c7d2fe; }
.lc-demo-mut { color: #777; font-size: 0.9em; }
.lc-demo-sum { margin: 0.5em 0; padding: 0.6em 0.8em; background: #f6f7fb; border-radius: 8px; font-size: 0.92em; }
.lc-demo-sum b { color: #333; }
.lc-demo-yt { width: 100%; box-sizing: border-box; margin: 0.4em 0; }
</style>

<script>
(function () {
  if (window._lcDemoReady) return; window._lcDemoReady = true;

  function pad2(n) { return (n < 10 ? "0" : "") + n; }
  function fmtClock(ms) { var s = Math.floor(ms / 1000); return pad2(Math.floor(s / 60)) + ":" + pad2(s % 60); }
  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  async function sha256(text) {
    try {
      var buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
      return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
    } catch (e) { return "(hash unavailable)"; }
  }

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return; el.dataset.lcUpgraded = "1";
    var id = el.id || ("demo-" + Math.random().toString(36).slice(2, 7));
    var title = el.getAttribute("title") || (el.textContent || "").trim() || "Demonstration";

    var wrap = document.createElement("div");
    wrap.className = "lc-demo"; wrap.setAttribute("data-lc-id", id);
    wrap.innerHTML =
      '<div class="lc-demo-hd"><span class="lc-demo-dot"></span>' +
        '<span class="lc-demo-title">🎬 ' + esc(title) + '</span>' +
        '<span class="lc-demo-timer" style="display:none">00:00</span></div>' +
      '<div class="lc-demo-body"></div>';
    el.parentNode.replaceChild(wrap, el);

    var hd = wrap.querySelector(".lc-demo-hd"), dot = wrap.querySelector(".lc-demo-dot"),
        timer = wrap.querySelector(".lc-demo-timer"), body = wrap.querySelector(".lc-demo-body");

    var st = { events: [], startWall: 0, running: false, since: 0, active: 0, student: null, finished: false, tick: null };

    // ── logging ──────────────────────────────────────────────────────────────
    function tnow() { return st.startWall ? Date.now() - st.startWall : 0; }
    function log(type, detail) {
      if (!st.running) return;
      st.events.push({ t: tnow(), type: type, detail: detail });
      try { localStorage.setItem("lc_demo_" + id, JSON.stringify({ student: st.student, events: st.events })); } catch (e) {}
    }
    function mark(type) { st.events.push({ t: tnow(), type: type }); }

    var _dbTimer = null;
    function onModel() {
      if (!st.running) return;
      clearTimeout(_dbTimer);
      _dbTimer = setTimeout(function () {
        var forms = {};
        document.querySelectorAll(".lc-form[data-lc-id]").forEach(function (f) {
          try { forms[f.getAttribute("data-lc-id")] = JSON.parse(f.getAttribute("data-lc-value") || "null"); } catch (e) {}
        });
        log("edit", { forms: forms });
      }, 400);
    }
    function onClick(e) {
      if (!st.running) return;
      if (e.target.closest(".lc-demo")) return;                 // ignore our own controls
      var t = e.target.closest("button, a, input, label, .lc-quiz li, .lc-card, [data-sort], [data-age], [data-tag]");
      if (!t) return;
      var label = (t.textContent || t.value || t.getAttribute("aria-label") || "").trim().slice(0, 60);
      log("click", { label: label, tag: t.tagName.toLowerCase() });
    }

    function addListeners() { document.addEventListener("lc-model-changed", onModel); document.addEventListener("click", onClick, true); }
    function rmListeners() { document.removeEventListener("lc-model-changed", onModel); document.removeEventListener("click", onClick, true); }

    // ── clock ────────────────────────────────────────────────────────────────
    function activeMs() { return st.active + (st.running ? Date.now() - st.since : 0); }
    function startTick() { st.tick = setInterval(function () { timer.textContent = fmtClock(activeMs()); }, 500); }
    function stopTick() { clearInterval(st.tick); st.tick = null; }

    // ── views ──────────────────────────────────────────────────────────────
    function renderIdle() {
      body.innerHTML =
        '<p class="lc-demo-mut">Demonstrate it, then export your log. Your name is stamped into the file.</p>' +
        '<div class="lc-demo-row">' +
          '<input type="text" class="lc-demo-name" placeholder="Your name" autocomplete="name">' +
          '<input type="text" class="lc-demo-id" placeholder="Student ID (optional)">' +
          '<button type="button" class="lc-demo-btn lc-demo-start">▶ Start</button>' +
          (window.lcOpenRecorder ? '<button type="button" class="lc-demo-btn lc-demo-vid">🎥 Record video</button>' : '') +
        '</div>';
      body.querySelector(".lc-demo-start").onclick = function () {
        var name = (body.querySelector(".lc-demo-name").value || "").trim();
        if (!name) { body.querySelector(".lc-demo-name").focus(); return; }
        st.student = { name: name, id: (body.querySelector(".lc-demo-id").value || "").trim() };
        start();
      };
      var v = body.querySelector(".lc-demo-vid"); if (v) v.onclick = function () { try { window.lcOpenRecorder(); } catch (e) {} };
    }
    function renderRecording() {
      dot.className = "lc-demo-dot live"; timer.style.display = "";
      body.innerHTML =
        '<div class="lc-demo-row">' +
          '<button type="button" class="lc-demo-btn lc-demo-pause">⏸ Pause</button>' +
          '<button type="button" class="lc-demo-btn lc-demo-finish">⏹ Finish</button>' +
          '<span class="lc-demo-mut">Recording ' + esc(st.student.name) + '’s demo…</span>' +
        '</div>';
      body.querySelector(".lc-demo-pause").onclick = pause;
      body.querySelector(".lc-demo-finish").onclick = finish;
    }
    function renderPaused() {
      dot.className = "lc-demo-dot paused";
      body.innerHTML =
        '<div class="lc-demo-row">' +
          '<button type="button" class="lc-demo-btn lc-demo-resume">⏵ Resume</button>' +
          '<button type="button" class="lc-demo-btn lc-demo-finish">⏹ Finish</button>' +
          '<span class="lc-demo-mut">Paused.</span>' +
        '</div>';
      body.querySelector(".lc-demo-resume").onclick = resume;
      body.querySelector(".lc-demo-finish").onclick = finish;
    }

    // ── transitions ──────────────────────────────────────────────────────────
    function start() { st.startWall = Date.now(); st.since = Date.now(); st.running = true; addListeners(); startTick(); mark("start"); renderRecording(); }
    function pause() { st.active += Date.now() - st.since; st.running = false; mark("pause"); stopTick(); renderPaused(); }
    function resume() { st.since = Date.now(); st.running = true; mark("resume"); startTick(); renderRecording(); }

    async function finish() {
      if (st.running) { st.active += Date.now() - st.since; st.running = false; }
      mark("finish"); stopTick(); rmListeners(); st.finished = true;
      dot.className = "lc-demo-dot"; timer.style.display = "none";

      var actions = st.events.filter(function (e) { return e.type === "click" || e.type === "edit"; }).length;
      var pauses = st.events.filter(function (e) { return e.type === "pause"; }).length;
      var quiz = null;
      try { var s = window.lcPageScores && window.lcPageScores.get(location.pathname); if (s) quiz = { correct: s.won || 0, answered: s.total || 0 }; } catch (e) {}
      var karma = actions + (quiz ? quiz.correct * 5 : 0);
      var durationSec = Math.round(activeMs() / 1000);

      var out = {
        demo: id, title: title,
        student: st.student,
        startedAt: new Date(st.startWall).toISOString(),
        durationSec: durationSec,
        summary: { actions: actions, pauses: pauses, quiz: quiz, karma: karma },
        video: "",
        events: st.events
      };
      out.sha256 = await sha256(JSON.stringify({ student: out.student, startedAt: out.startedAt, events: out.events }));

      body.innerHTML =
        '<div class="lc-demo-sum">✅ <b>' + esc(st.student.name) + '</b> — ' +
          actions + ' actions · ' + fmtClock(durationSec * 1000) + ' active · ' + pauses + ' pause(s)' +
          (quiz ? ' · quiz ' + quiz.correct + '/' + quiz.answered : '') +
          ' · <b>karma ' + karma + '</b></div>' +
        '<input type="text" class="lc-demo-yt" placeholder="Optional: paste your unlisted YouTube link">' +
        '<div class="lc-demo-row">' +
          '<button type="button" class="lc-demo-btn lc-demo-export">📤 Export</button>' +
          '<button type="button" class="lc-demo-btn lc-demo-copy">📋 Copy JSON</button>' +
          '<span class="lc-demo-mut lc-demo-note"></span>' +
        '</div>';

      function build() {
        out.video = (body.querySelector(".lc-demo-yt").value || "").trim();
        return JSON.stringify(out, null, 2);
      }
      var fname = "demo-" + id + "-" + ((st.student.id || st.student.name).replace(/[^\w-]+/g, "_")) + ".json";
      var note = body.querySelector(".lc-demo-note");
      body.querySelector(".lc-demo-export").onclick = function () {
        try {
          var blob = new Blob([build()], { type: "application/json" });
          var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = fname;
          document.body.appendChild(a); a.click(); a.remove();
          setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
          note.textContent = "Downloaded " + fname;
        } catch (e) { note.textContent = "Download blocked — use Copy JSON instead."; }
      };
      body.querySelector(".lc-demo-copy").onclick = function () {
        var json = build();
        (navigator.clipboard ? navigator.clipboard.writeText(json) : Promise.reject())
          .then(function () { note.textContent = "Copied — paste it into your submission."; })
          .catch(function () { window.prompt("Copy your demo JSON:", json); });
      };
      try { localStorage.removeItem("lc_demo_" + id); } catch (e) {}
    }

    renderIdle();
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.demo, .highlighter-rouge.demo, pre.demo", upgrade);
})();
</script>
