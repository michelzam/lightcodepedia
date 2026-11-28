{%- comment -%}
Visits — anonymous usage of a PUBLIC page, counted (Michel, 2026-11-27, for
the SIGCSE page: "I would like to be able to collect traces, to see who is
using what"). Activated from md + IAL: one sentence, the notice a visitor
reads, decorated {: .visits }. No sentence, no count: the notice IS the switch.

What leaves the browser, one small row per step: the page, the step
(arrive, press, check red/green, guide, heard, ask, edit, open, contact, link,
stay = seconds the page was in view), the id of the part touched, phone/tablet/desktop, where the visitor came from
(a host name, or ?from=…), and a visit number that lives for the tab only.
No name, no cookie, no stored id, no text a visitor typed, no key.
The store adds, from the request itself: the country, the system and the
browser as coarse words, and a mark for "the same visitor today" that it
cannot undo (tools/visits_setup.sql). The address is never kept.

Where it goes: the site's visits door — an address and a PUBLIC key in
_data/visits_door.yml, a file that stays in the lab. That pair is meant to be read by anyone: it opens
one function that only adds a capped row (tools/visits_setup.sql). It reads
nothing. With no door configured the line stays a sentence and nothing is
sent. (Michel, same day: "if the public pedia repo holds a … unlisted url
or key, then this would become exposed" — so nothing unlisted, nothing that
reads, and hard caps on what can be added.)

Stays silent for: a browser that says Do Not Track or Global Privacy
Control, an automated browser. The author's own visits are counted, and
told apart (kind: author / learner / visitor).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-visits { font-size: 0.8em; color: #64748b; margin: 1.5em 0 0.5em; }
.lc-visits::before { content: "👣 "; }
</style>

<script>
(function () {
  if (window._lcVisitsReady) return;
  window._lcVisitsReady = true;

  var SITE = { url: {{ site.data.visits_door.url | default: "" | jsonify }}, key: {{ site.data.visits_door.key | default: "" | jsonify }} };
  var MAX = 40;                       /* rows per visit, at most */
  var visit = Math.random().toString(36).slice(2, 10);
  var sent = 0, seen = {}, line = null;

  function door() {
    var d = window.lcVisitsDoor || SITE;
    return d && d.url && d.key ? d : null;
  }
  function quiet() {
    /* a door handed to the page by a check is always heard */
    if (window.lcVisitsDoor) return false;
    try {
      if (navigator.doNotTrack === "1" || window.doNotTrack === "1" || navigator.globalPrivacyControl) return true;
      if (navigator.webdriver) return true;
    } catch (e) {}
    return false;
  }
  /* WHO, AS A KIND, NEVER AS A NAME (Michel, 2026-11-27: "if ever the visitor
     is me, would I know? … or one of my students?"). A device that holds a
     key to a repo of the site's owner is the author's; one that holds a key
     to any other repo is a learner's (their bench); the rest are visitors.
     The repo's name, which would name the learner, never leaves. A page
     cannot know that someone is signed in to GitHub elsewhere. */
  var OWNER = String({{ site.github.repository_nwo | default: "" | jsonify }}).split("/")[0].toLowerCase();
  function kind() {
    try {
      if (!localStorage.getItem("lc_ed_pat")) return "visitor";
      var repo = String(localStorage.getItem("lc_ed_repo") || "").toLowerCase();
      return OWNER && repo.split("/")[0] === OWNER ? "author" : "learner";
    } catch (e) { return "visitor"; }
  }
  function device() {
    var w = Math.min(window.innerWidth || 0, screen.width || 9999);
    return w < 600 ? "phone" : w < 1000 ? "tablet" : "desktop";
  }
  function from() {
    var m = /[?&]from=([\w-]{1,24})/.exec(location.search);
    if (m) return m[1];
    try { var h = document.referrer ? new URL(document.referrer).host : ""; return h === location.host ? "" : h; }
    catch (e) { return ""; }
  }
  function idOf(el) {
    var p = el && el.closest ? el.closest("[data-lc-id]") : null;
    return p ? p.getAttribute("data-lc-id") : (el && el.id) || "";
  }

  function send(event, what, detail) {
    var d = door();
    if (!line || !d || quiet() || sent >= MAX) return;
    sent++;
    line.setAttribute("data-lc-sent", String(sent));
    var row = { site: location.host, page: location.pathname, visit: visit, event: String(event).slice(0, 24),
                what: String(what || "").slice(0, 60), detail: String(detail || "").slice(0, 120),
                device: device(), ref: from(), kind: kind() };
    try {
      fetch(d.url.replace(/\/+$/, "") + "/rest/v1/rpc/lc_visit", {
        method: "POST", keepalive: true,
        headers: { "Content-Type": "application/json", "apikey": d.key, "Authorization": "Bearer " + d.key },
        body: JSON.stringify({ p: row })
      }).catch(function () {});
    } catch (e) {}
  }
  function once(event, what, detail) {
    var k = event + ":" + what;
    if (seen[k]) return;
    seen[k] = 1;
    send(event, what, detail);
  }

  /* A CHECK COUNTS WHEN THE VISITOR RAN IT (found on Michel's first real
     rows, 2026-11-27: every reload on his phone said "check red" seconds
     after "arrive" — a card remembers its last verdict and shows it again on
     load, and that was counted as a run). So: ▶ is pressed, then the verdict
     that follows is told, once per press. */
  var ran = {};
  function checks() {
    document.querySelectorAll(".lc-feature[data-lc-id]").forEach(function (c) {
      var s = c.getAttribute("data-status") || "";
      if (s !== "passing" && s !== "failing") return;
      var id = c.getAttribute("data-lc-id");
      if (!ran[id]) return;
      ran[id] = 0;
      send("check", id, s === "passing" ? "green" : "red");
    });
  }

  /* seconds the page was in view: counted while visible, told when it hides */
  var shownAt = Date.now(), inView = 0, told = 0;
  function stay() {
    if (shownAt) { inView += Date.now() - shownAt; shownAt = 0; }
    var secs = Math.round(inView / 1000);
    if (secs - told < 5) return;
    told = secs;
    send("stay", "", String(secs));
  }

  function listen() {
    document.addEventListener("lc-feature-result", function () { setTimeout(checks, 50); });
    document.addEventListener("lc-avatar-ended", function (ev) {
      if (ev.detail && ev.detail.completed) send("heard", ev.detail.id || "");
    });
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") stay(); else shownAt = Date.now();
    });
    window.addEventListener("pagehide", stay);
    document.addEventListener("click", function (ev) {
      var t = ev.target;
      if (!t || !t.closest) return;
      var el;
      if ((el = t.closest(".lc-feature-run"))) { ran[idOf(el)] = 1; return; }
      if ((el = t.closest(".lc-avatar-trigger"))) return send("guide", el.getAttribute("story") || "tour");
      if ((el = t.closest(".lc-agent-send"))) return send("ask", idOf(el));
      if ((el = t.closest(".lc-button"))) return once("press", idOf(el));
      if ((el = t.closest("a[href^='mailto:']"))) return send("contact", "mail");
      if ((el = t.closest("a[href]"))) {
        var h = el.getAttribute("href") || "";
        if (h.charAt(0) === "/" && h.charAt(1) !== "/") once("link", h.split("#")[0].slice(0, 60));
      }
    }, true);
    document.addEventListener("input", function (ev) {
      var t = ev.target;
      if (t && t.classList && t.classList.contains("lc-mdpad-in")) once("edit", idOf(t));
    }, true);
    document.addEventListener("toggle", function (ev) {
      var t = ev.target;
      if (t && t.open && t.closest && t.closest(".lc-accordion")) once("open", idOf(t));
    }, true);
  }

  function upgradeVisits(el) {
    if (el.dataset.lcVisitsDone) return;
    el.dataset.lcVisitsDone = "1";
    el.classList.add("lc-visits");
    if (el.id && !el.getAttribute("data-lc-id")) el.setAttribute("data-lc-id", el.id);
    if (line) return;                 /* one count per page */
    line = el;
    line.setAttribute("data-lc-sent", "0");
    listen();
    send("arrive", "", "");
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.visits", upgradeVisits);
  }
})();
</script>
