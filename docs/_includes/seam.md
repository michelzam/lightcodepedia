{%- comment -%}
Seam — the border markdown already had.

    ---
    {: .seam label="The app starts here" }

A page speaks in registers: the course talking, the app the learner acts
in, the course's own tools. A beginner cannot infer a frame nobody gave
them (Michel, 2026-08-13: *"the blurry fuzzy mixture between lecture's
text, app and tools"*), so `---` stops being a decoration and becomes that
frame — the mark markdown already has, with a name on it.

THE LABEL CARRIES THE MEANING, THE COLOUR ONLY DECORATES. Red already
means something loud here (a failing check, a bomb on a broken wire); a
border that leans on colour says two things at once, and says nothing at
all to a colour-blind reader, a printed page or a screen reader. So
`label=` is required and the tint is optional: add `.red`, `.blue`,
`.amber`, `.green` or `.muted` beside `.seam` and the wave picks it up.

A SEAM MARKS, IT DOES NOT WRAP. It opens a region; the next seam or the
next heading ends it. Nothing nests, nothing has to be closed, and the
section splitters never meet a new container.

THREE LABELS, FOREVER (tests/course_audit.py enforces them):
    The app starts here · A course tool · Back to the lesson
The value of a border is that it is the SAME border on page 40 as on page
2. Free text would drift into "you're in the app now" by module 5.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* the torn edge: one repeating wave, tinted by the author's colour class.
   A background image costs a printer nothing, and it collapses to a plain
   rule when the ink is not wanted (@media print in colors.md keeps the
   label, drops the wave). */
.lc-seam {
  --lc-seam-tint: #94a3b8;
  position: relative;
  margin: 2.2em 0 1.4em;
  padding-top: 0.9em;
}
.lc-seam hr {
  border: none;
  height: 10px;
  margin: 0;
  background-repeat: repeat-x;
  background-position: center;
  background-image: url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' width='120' height='10' viewBox='0 0 120 10'>\
<path d='M0 5 Q 15 0 30 5 T 60 5 T 90 5 T 120 5' fill='none' stroke='%2394a3b8' stroke-width='2'/>\
</svg>");
}
.lc-seam-label {
  display: inline-block;
  margin-top: 0.5em;
  padding: 0.15em 0.85em;
  border-radius: 999px;
  background: #fff;
  border: 1px solid var(--lc-seam-tint);
  color: var(--lc-seam-tint);
  font-size: 0.82em;
  font-weight: 600;
  letter-spacing: 0.02em;
}
/* the author's own colour words, reused — no second vocabulary to learn */
.lc-seam-red    { --lc-seam-tint: #c0392b; }
.lc-seam-green  { --lc-seam-tint: #2e7d32; }
.lc-seam-blue   { --lc-seam-tint: #1565c0; }
.lc-seam-amber  { --lc-seam-tint: #b45309; }
.lc-seam-muted  { --lc-seam-tint: #6b7280; }
.lc-seam-red    hr { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='10' viewBox='0 0 120 10'><path d='M0 5 Q 15 0 30 5 T 60 5 T 90 5 T 120 5' fill='none' stroke='%23c0392b' stroke-width='2'/></svg>"); }
.lc-seam-green  hr { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='10' viewBox='0 0 120 10'><path d='M0 5 Q 15 0 30 5 T 60 5 T 90 5 T 120 5' fill='none' stroke='%232e7d32' stroke-width='2'/></svg>"); }
.lc-seam-blue   hr { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='10' viewBox='0 0 120 10'><path d='M0 5 Q 15 0 30 5 T 60 5 T 90 5 T 120 5' fill='none' stroke='%231565c0' stroke-width='2'/></svg>"); }
.lc-seam-amber  hr { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='10' viewBox='0 0 120 10'><path d='M0 5 Q 15 0 30 5 T 60 5 T 90 5 T 120 5' fill='none' stroke='%23b45309' stroke-width='2'/></svg>"); }
@media print {
  .lc-seam hr { background: none; border-top: 1px solid #999; height: 0; }
}
</style>

<script>
(function () {
  if (window._lcSeamReady) return;
  window._lcSeamReady = true;

  var TINTS = ["red", "green", "blue", "amber", "muted"];

  function upgradeSeam(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var label = (el.getAttribute("label") || "").trim();
    var box = document.createElement("div");
    box.className = "lc-seam";
    TINTS.forEach(function (t) { if (el.classList.contains(t)) box.classList.add("lc-seam-" + t); });
    if (el.id) { box.id = el.id; box.setAttribute("data-lc-id", el.id); }
    var rule = document.createElement("hr");
    /* the rule keeps its meaning for a screen reader, and the label IS the
       border — spoken, printed, searchable */
    if (label) rule.setAttribute("aria-label", label);
    box.appendChild(rule);
    if (label) {
      var cap = document.createElement("span");
      cap.className = "lc-seam-label";
      cap.textContent = label;
      box.appendChild(cap);
    }
    el.parentNode.replaceChild(box, el);
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("hr.seam", upgradeSeam);
})();
</script>
