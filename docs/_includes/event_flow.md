{%- comment -%}
Event flow — a page's story as an event-storming sequence.

  ```yaml
  - user: The family
  - ui: The dog board
  - command: Name a dog
  - event: A dog is named
  - ui: The meet card opens
  ```
  {: .event_flow #adoption_flow legend="true" }

One list, one key per step — the KEY is the sticky-note color, the value
is the words. Kinds: user 👤🍦 · ui 🖥️🟩 · data 📦🟨 · command 🗣️🟦 ·
rule 📏🟪 · event ⚡🟧 · external 🌐🩷.

PLAIN WORDS, NOT JARGON (Michel, 2026-08-11). Event storming calls these
actor / read model / aggregate / policy; a learner needs the word for the
thing. The SOTA names all still parse as aliases — actor, view, reader,
aggregate, entity, policy — so a page written either way renders, and the
catalog can teach both spellings.

THE BEAT, and it is the whole grammar:

    user → ui|data → command → [rule →] event

A user heads their beats. A beat OPENS on the screen they are sitting at
(name it after the component: `ask`, `dog_grid`), then what they ASK FOR
— a rule can never make a person act — then the rule that governs it,
then what became true. The event closes the beat. One beat per line, one
grid per user so the columns line up; a user with a single beat is
written on one line, not two.

AUTHORED v1, by decision (Michel 2026-08-11). The computed v2 is the
point of the shape: a page's gates (visible= formulas) ARE its policies
and its button handlers ARE its commands, so a scope= knob can one day
generate this sequence from the page's own wiring. The yaml stays as the
authored override either way — hold the knob, don't fake it.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-event-flow { display: flex; flex-direction: column; gap: 1.4em; margin: 1em 0; padding: 1.1em 1.2em; border: 1px solid #e5e7eb; border-radius: 10px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); overflow-x: auto; }
/* THE PERSON HEADS THEIR OWN BEATS. A single wrapping ribbon of notes made
   a ten-step story unreadable; putting the actor in a left column then read
   as if the rule beside them issued the command. It cannot — a person does
   (Michel, 2026-08-11). So the actor takes a line, their beats are indented
   under it, and each beat begins with the command that person gives. */
.lc-ef-group { display: flex; flex-direction: column; align-items: start; gap: 0.55em; }
/* one grid per group: commands under commands, events under events */
.lc-ef-beats { display: grid; grid-template-columns: repeat(var(--lc-ef-cols, 1), max-content); align-items: center; gap: 0.7em 0.5em; margin-left: 1.8em; }
.lc-ef-line { display: contents; }
/* one beat, one line: the person's name heads it instead of standing above */
.lc-ef-solo { flex-direction: row; align-items: center; gap: 0.5em; }
.lc-ef-solo .lc-ef-beats { margin-left: 0; }
/* the default: marked-up words, not cardboard. notes="sticky" brings the
   workshop wall back for a page that wants it */
.lc-ef-plain .lc-ef-step { box-shadow: none; padding: 0.1em 0.4em; border-radius: 3px; max-width: 22em; }
.lc-ef-plain { gap: 1em; padding: 0.8em 1em; box-shadow: none; }
.lc-ef-plain .lc-ef-beats { gap: 0.45em 0.4em; }
.lc-ef-step { padding: 0.45em 0.8em; border-radius: 4px; font-size: 0.88em; line-height: 1.35; max-width: 15em; box-shadow: 1px 2px 4px rgba(0,0,0,0.12); color: #1f2937; }
.lc-ef-arrow { color: #9ca3af; user-select: none; text-align: center; }
@media (max-width: 560px) { .lc-ef-beats { margin-left: 0.8em; } }
/* the classic sticky-note palette — the kind IS the color */
.lc-ef-user    { background: #fdf3d7; }
.lc-ef-command  { background: #bfdbfe; }
.lc-ef-event    { background: #fdba74; }
.lc-ef-rule   { background: #e9d5ff; }
.lc-ef-data     { background: #fef08a; }
.lc-ef-ui       { background: #86efac; }
.lc-ef-external { background: #fbcfe8; }
.lc-ef-unknown  { background: #e5e7eb; }
.lc-ef-legend { display: flex; flex-wrap: wrap; gap: 0.4em 1em; margin-top: 0.2em; padding-top: 0.55em; border-top: 1px dashed #e5e7eb; font-size: 0.78em; color: #4b5563; }
.lc-ef-legend span::before { content: "■ "; }
.lc-ef-legend .lc-ef-l-user::before    { color: #fdf3d7; }
.lc-ef-legend .lc-ef-l-command::before  { color: #bfdbfe; }
.lc-ef-legend .lc-ef-l-event::before    { color: #fdba74; }
.lc-ef-legend .lc-ef-l-rule::before   { color: #e9d5ff; }
.lc-ef-legend .lc-ef-l-data::before { color: #fef08a; }
.lc-ef-legend .lc-ef-l-ui::before     { color: #86efac; }
.lc-ef-legend .lc-ef-l-external::before { color: #fbcfe8; }
</style>

<script>
(function () {
  if (window._lcEventFlowReady) return;
  window._lcEventFlowReady = true;

  var escapeHtml = window.lcEscapeHtml;
  var parseData = window.lcParseDataText;
  var KINDS = ["user", "ui", "data", "command", "rule", "event", "external"];
  /* THE STATE OF THE ART KEEPS ITS NAMES, THE LEARNER GETS WORDS. Event
     storming says actor / read model / aggregate / policy; a beginner needs
     user / ui / data / rule. Every SOTA spelling parses to the same kind, so
     a page written either way renders (Michel, 2026-08-11). */
  var ALIAS = { actor: "user", view: "ui", reader: "ui", screen: "ui",
                aggregate: "data", entity: "data", policy: "rule" };
  /* THE COLOR IS THE GRAMMAR, AND A COLOR IS NOT ENOUGH. Print it, hand it
     to a colour-blind reader, or read it aloud, and 🟦 and 🟪 are the same
     note. The glyph says the kind in words the colour only implies, and it
     is automatic — an author writes the sentence, never the icon
     (Michel, 2026-08-11). */
  var ICON = { user: "👤", ui: "🖥️", data: "📦", command: "🗣️",
               rule: "📏", event: "⚡", external: "🌐", unknown: "❔" };

  function upgradeEventFlow(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = (el.querySelector("code") || {}).textContent || "";
    var legend = el.getAttribute("legend") === "true";
    /* PLAIN BY DEFAULT (Michel, 2026-08-11). The cardboard is beautiful on a
       workshop wall and heavy inside a lesson; a flow should read as a
       sentence unless a page asks for the wall. */
    var sticky = el.getAttribute("notes") === "sticky";
    parseData(raw, "yaml").then(function (rows) {
      var steps = (Array.isArray(rows) ? rows : []).map(function (r) {
        if (r && typeof r === "object") {
          var k = Object.keys(r)[0] || "", kind = ALIAS[k] || k;
          return { kind: KINDS.indexOf(kind) >= 0 ? kind : "unknown", text: String(r[k] == null ? "" : r[k]) };
        }
        return { kind: "unknown", text: String(r == null ? "" : r) };
      });
      var box = document.createElement("div");
      box.className = "lc-event-flow" + (sticky ? "" : " lc-ef-plain");
      var id = el.id || "event_flow";
      box.id = id;
      box.setAttribute("data-lc-id", id);
      box.setAttribute("role", "list");
      box.setAttribute("aria-label", "event flow");
      function chip(s) {
        return "<span class='lc-ef-step lc-ef-" + s.kind + "' role='listitem' data-kind='" + s.kind + "'>" +
               ICON[s.kind] + " " + escapeHtml(s.text) + "</span>";
      }
      /* A RULE CANNOT MAKE A PERSON DO ANYTHING — a person does (Michel,
         2026-08-11). One beat is
             ui|data → command → [rule →] event
         under the user who gives the command. The splitting rule below is
         the whole of it: an event closes the beat, and the next note opens
         the next one. */
      var groups = [], g = null, line = null, state = "start";
      function newGroup(who) { g = { who: who, lines: [] }; groups.push(g); line = null; state = "start"; }
      function newLine(s) { line = [s]; if (!g) newGroup(null); g.lines.push(line); state = "open"; }
      steps.forEach(function (s) {
        if (s.kind === "user") { newGroup(s); return; }
        /* THE EVENT CLOSES THE BEAT, and a 🖥️ ui always OPENS one: it is
           where the person sits to decide, not a consequence hung off the
           end (Michel, 2026-08-11). So the next note after an event starts
           the next line, whatever it is. */
        if (state === "start") { newLine(s); return; }
        line.push(s);
        if (s.kind === "event") state = "start";
      });
      var html = groups.map(function (grp) {
        /* one grid per group, so the commands line up under each other and
           the events under those — a column you can read down */
        var wide = grp.lines.reduce(function (n, l) { return Math.max(n, l.length); }, 0);
        var cols = Math.max(1, wide * 2 - 1);
        var cells = grp.lines.map(function (l) {
          /* the line stays a real element (display:contents) so a reader,
             and a scenario, can still ask "what is this beat?" while its
             chips sit in the group's grid and line up */
          var out = "";
          for (var c = 0; c < wide; c++) {
            if (c) out += l[c] ? "<span class='lc-ef-arrow' aria-hidden='true'>→</span>" : "<span></span>";
            out += l[c] ? chip(l[c]) : "<span></span>";
          }
          return "<div class='lc-ef-line'>" + out + "</div>";
        }).join("");
        /* ONE BEAT NEEDS ONE LINE. Giving a person a heading and then a
           single indented beat under it wastes a line and reads as if more
           were coming (Michel, 2026-08-11). With one beat, the name sits at
           the head of that beat. */
        var solo = grp.lines.length === 1;
        return "<div class='lc-ef-group" + (solo ? " lc-ef-solo" : "") + "'>" +
               (grp.who ? "<span class='lc-ef-who'>" + chip(grp.who) + "</span>" : "") +
               "<div class='lc-ef-beats' style='--lc-ef-cols:" + cols + "'>" + cells + "</div>" +
               "</div>";
      }).join("");
      if (legend) {
        html += "<div class='lc-ef-legend'>" +
          "<span class='lc-ef-l-user'>👤 user — a person</span>" +
          "<span class='lc-ef-l-ui'>🖥️ ui — the screen they act on</span>" +
          "<span class='lc-ef-l-data'>📦 data — what the beat is about</span>" +
          "<span class='lc-ef-l-command'>🗣️ command — what they ask for</span>" +
          "<span class='lc-ef-l-rule'>📏 rule — what governs it</span>" +
          "<span class='lc-ef-l-event'>⚡ event — what became true</span>" +
          "</div>";
      }
      box.innerHTML = html;
      el.parentNode.replaceChild(box, el);
      if (window.lcSetDataset) window.lcSetDataset(id, steps);
    }).catch(function (e) {
      var d = document.createElement("div");
      d.className = "lc-event-flow";
      d.innerHTML = "<div style='color:#c00'>" + escapeHtml(e.message || String(e)) + "</div>";
      el.parentNode.replaceChild(d, el);
    });
  }

  if (window.lcRegisterUpgrader)
    window.lcRegisterUpgrader(".highlighter-rouge.event_flow, pre.event_flow", upgradeEventFlow);
})();
</script>
