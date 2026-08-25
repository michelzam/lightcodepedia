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
    var pass = ["focus", "editable", "navigable", "open"]
      .filter(function (k) { return q[k] !== undefined; })
      .map(function (k) { return k + "=" + encodeURIComponent(q[k]); }).join("&");
    location.replace((window.lcHref ? window.lcHref("/run.html") : "/run.html")
      + (pass ? "?" + pass : "") + "#src=gh:" + vault + "/" + target);
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.course_door", upgrade);
})();
</script>
