{%- comment -%}
Event flow — a page's story as an event-storming sequence.

  ```yaml
  - actor: The family
  - command: Name a dog
  - event: A dog is named
  - policy: The meet card opens when a dog is named
  - reader: The coordinator sees how far they got
  ```
  {: .event_flow #adoption_flow legend="true" }

One list, one key per step — the KEY is the sticky-note color, the value
is the words. Kinds: actor 🟨 · command 🟦 · event 🟧 · policy 🟪 ·
reader 🟩 · external 🩷. Unknown kinds render grey rather than failing.

AUTHORED v1, by decision (Michel 2026-08-11). The computed v2 is the
point of the shape: a page's gates (visible= formulas) ARE its policies
and its button handlers ARE its commands, so a scope= knob can one day
generate this sequence from the page's own wiring. The yaml stays as the
authored override either way — hold the knob, don't fake it.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-event-flow { display: flex; flex-wrap: wrap; align-items: center; gap: 0.45em; margin: 1em 0; padding: 0.9em 1em; border: 1px solid #e5e7eb; border-radius: 10px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.lc-ef-step { padding: 0.45em 0.8em; border-radius: 4px; font-size: 0.88em; line-height: 1.35; max-width: 15em; box-shadow: 1px 2px 4px rgba(0,0,0,0.12); color: #1f2937; }
.lc-ef-arrow { color: #9ca3af; flex: none; user-select: none; }
/* the classic sticky-note palette — the kind IS the color */
.lc-ef-actor    { background: #fff9b1; }
.lc-ef-command  { background: #bfdbfe; }
.lc-ef-event    { background: #fdba74; }
.lc-ef-policy   { background: #e9d5ff; }
.lc-ef-reader   { background: #bbf7d0; }
.lc-ef-external { background: #fbcfe8; }
.lc-ef-unknown  { background: #e5e7eb; }
.lc-ef-legend { flex-basis: 100%; display: flex; flex-wrap: wrap; gap: 0.4em 1em; margin-top: 0.5em; padding-top: 0.55em; border-top: 1px dashed #e5e7eb; font-size: 0.78em; color: #4b5563; }
.lc-ef-legend span::before { content: "■ "; }
.lc-ef-legend .lc-ef-l-actor::before    { color: #fff9b1; }
.lc-ef-legend .lc-ef-l-command::before  { color: #bfdbfe; }
.lc-ef-legend .lc-ef-l-event::before    { color: #fdba74; }
.lc-ef-legend .lc-ef-l-policy::before   { color: #e9d5ff; }
.lc-ef-legend .lc-ef-l-reader::before   { color: #bbf7d0; }
.lc-ef-legend .lc-ef-l-external::before { color: #fbcfe8; }
</style>

<script>
(function () {
  if (window._lcEventFlowReady) return;
  window._lcEventFlowReady = true;

  var escapeHtml = window.lcEscapeHtml;
  var parseData = window.lcParseDataText;
  var KINDS = ["actor", "command", "event", "policy", "reader", "external"];

  function upgradeEventFlow(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = (el.querySelector("code") || {}).textContent || "";
    var legend = el.getAttribute("legend") === "true";
    parseData(raw, "yaml").then(function (rows) {
      var steps = (Array.isArray(rows) ? rows : []).map(function (r) {
        if (r && typeof r === "object") {
          var k = Object.keys(r)[0] || "";
          return { kind: KINDS.indexOf(k) >= 0 ? k : "unknown", text: String(r[k] == null ? "" : r[k]) };
        }
        return { kind: "unknown", text: String(r == null ? "" : r) };
      });
      var box = document.createElement("div");
      box.className = "lc-event-flow";
      var id = el.id || "event_flow";
      box.id = id;
      box.setAttribute("data-lc-id", id);
      box.setAttribute("role", "list");
      box.setAttribute("aria-label", "event flow");
      var html = steps.map(function (s, i) {
        var chip = "<span class='lc-ef-step lc-ef-" + s.kind + "' role='listitem' data-kind='" + s.kind + "'>" + escapeHtml(s.text) + "</span>";
        return (i ? "<span class='lc-ef-arrow' aria-hidden='true'>→</span>" : "") + chip;
      }).join("");
      if (legend) {
        html += "<div class='lc-ef-legend'>" +
          "<span class='lc-ef-l-actor'>actor — a person</span>" +
          "<span class='lc-ef-l-command'>command — what they do</span>" +
          "<span class='lc-ef-l-event'>event — what became true</span>" +
          "<span class='lc-ef-l-policy'>policy — the rule that reacts</span>" +
          "<span class='lc-ef-l-reader'>reader — what the screen shows</span>" +
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
