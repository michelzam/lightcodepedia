{%- comment -%}
Course door — the ONE short address a Canvas iframe embeds (Michel,
2026-08-25: "the url to access the root page of the course, simplified").

  [go](#)
  {: .course_door vault="uwm-build-ai/uwm-build-ai-vault" course="courses/micro_build_ai" }

/go opens the course root; /go?p=module_00/00_welcome opens a lesson
(".md" optional). The door only rewrites the address — the runner still
demands the visitor's own key, so a public door guards nothing and leaks
nothing new (the vault name is already published on the join page).
Frame flags (focus/editable/navigable/open) pass through untouched, so
the LMS keeps framing one URL per page and nothing else.
{%- endcomment -%}
<script>
(function () {
  if (window._lcCourseDoorReady) return;
  window._lcCourseDoorReady = true;

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return; el.dataset.lcUpgraded = "1";
    var vault = el.getAttribute("vault") || "";
    var course = el.getAttribute("course") || "";
    if (!vault) return;
    var q = {};
    try { location.search.replace(/^\?/, "").split("&").forEach(function (kv) {
      var p = kv.split("="); if (p[0]) q[p[0]] = decodeURIComponent(p[1] || ""); }); } catch (e) {}
    /* the path stays INSIDE the course — no climbing out of it */
    var p = (q.p || "").replace(/\.\./g, "").replace(/^\/+/, "");
    if (p && !/\.md$/.test(p)) p += ".md";
    var target = (course ? course + "/" : "") + (p || "index.md");
    /* the standard learner flags are BAKED — that is the whole point of a
       short address. A query param still overrides its default. crumb= is
       what makes the LMS view (topbar → one read-only course line, no
       source pill); without it a bare tap lands on the full platform.
       editable is NOT among them (Michel, 2026-08-30, Canvas with no key:
       "I can still switch to edit mode"). It was baked as "1", and an
       explicit editable is the one thing that OVERRIDES the frame's own
       rule — course material in a teacher's frame is read-only (2026-08-18:
       the editor opened on it empty and useless). So the door says nothing,
       the rule decides: the course is closed, a learner's own bench stays
       open, and ?editable=1 still reopens it for whoever means it. */
    /* THE DOOR NAMES THE SESSION IT TEACHES (Michel, 2026-08-31). The join
       wizard used to guess it — newest template in the org wins — and a
       teacher (or a returning student) with last term's bench got paired to
       it: module_00's dogs arrived already repaired, from
       build-ai-summer26-…, and Save filed this year's work there without a
       word. The door carries hub=<session> so every page opened through it
       knows which class it belongs to. One line, in the lab, per term. */
    var flags = { focus: "1",
                  crumb: el.getAttribute("crumb") || "",
                  hub: el.getAttribute("session") || "",
                  open: "gh:" + vault + "/" + (course.split("/")[0] || "courses") + "/*" };
    var pass = ["focus", "editable", "navigable", "open", "crumb", "hub", "up", "strict"]
      .filter(function (k) { return q[k] !== undefined || flags[k]; })
      .map(function (k) {
        return k + "=" + encodeURIComponent(q[k] !== undefined ? q[k] : flags[k]);
      }).join("&");
    location.replace((window.lcHref ? window.lcHref("/run.html") : "/run.html")
      + (pass ? "?" + pass : "") + "#src=gh:" + vault + "/" + target);
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.course_door", upgrade);
})();
</script>
