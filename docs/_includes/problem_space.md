{%- comment -%}
Problem space — the three documents every product carries, as components:

  ```yaml … ```
  {: .persona #coordinator source="persona_src" save="persona.yaml" }
  ```yaml … ```
  {: .pitch #pitch source="pitch_src" save="pitch.yaml" persona="coordinator" }
  ```yaml … ```
  {: .impact_map pitch="pitch" }

The fence is the author's seed. Two optional wires:

  source="<form id>"  the form is the EDITOR, this card the live view —
                      every keystroke re-renders (lc-model-changed +
                      data-lc-value, the form's own bus). data-bind carries
                      the wire, so the x-ray pipes it.
  save="<file>"       the two-repo contract, exactly the datagrid's: the
                      learner's 💾 keeps THEIR document in their bench and
                      it overrides the seed on the next visit — from any
                      page in the module that names the same file.

All three register their data via lcSetDataset, so cells, agents and the
x-ray see them; pitch checks itself against the persona it reads (soft
drift warning); the impact map pulls goal/who from its pitch and collects
the page's .feature proofs. Dead KISS by decision (Michel 2026-08-10);
room held for the AI-drawn portrait (photo slot) and folder-wide scope.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-persona { border: 1px solid #e5e7eb; border-radius: 10px; margin: 1em 0; background: #fff; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.lc-persona-head { display: flex; align-items: center; gap: 0.9em; padding: 0.8em 1em; background: #f9fafb; border-bottom: 1px solid #e5e7eb; }
.lc-persona-photo { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; flex: none; background: #eef2f7; }
.lc-persona-photo-empty { display: flex; align-items: center; justify-content: center; font-size: 1.6em; }
.lc-persona-name { font-weight: 700; color: #111827; }
.lc-persona-role { font-size: 0.85em; color: #6b7280; }
.lc-persona-body { padding: 0.7em 1em; font-size: 0.92em; }
.lc-persona-row { margin: 0.35em 0; }
.lc-persona-row b { color: #374151; }
.lc-persona-quote { font-style: italic; color: #4b5563; border-left: 3px solid #d1d5db; padding-left: 0.8em; margin: 0.6em 0; }
.lc-empathy { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #e5e7eb; border-top: 1px solid #e5e7eb; }
.lc-empathy-cell { background: #fff; padding: 0.6em 0.9em; font-size: 0.88em; }
.lc-empathy-cell h5 { margin: 0 0 0.3em; font-size: 0.82em; color: #6b7280; text-transform: uppercase; letter-spacing: 0.04em; }
.lc-empathy-cell ul { margin: 0; padding-left: 1.1em; }
@media (max-width: 560px) { .lc-empathy { grid-template-columns: 1fr; } }

.lc-pitch { border: 1px solid #e5e7eb; border-left: 4px solid #7b6cf6; border-radius: 0 10px 10px 0; margin: 1em 0; background: #fff; padding: 0.9em 1.1em; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
/* ONE BLANK PER LINE (Michel, 2026-08-12: *"the display should show them in
   different lines to make the reading and checking easy"*). The pitch is a
   sentence, but it is READ as a form: you check it blank by blank, and a
   missing one has to be findable at a glance instead of hunted inside a
   paragraph. The connectives keep the sentence audible top to bottom. */
.lc-pitch-text { font-size: 1.02em; line-height: 1.5; color: #111827; }
.lc-pitch-text b { color: #4c3fd4; }
.lc-pitch-line { display: grid; grid-template-columns: 4.4em 1fr; gap: 0.5em;
                 align-items: baseline; padding: 0.12em 0; }
.lc-pitch-lead { color: #6b7280; font-size: 0.86em; text-align: right; }
@media (max-width: 560px) {
  .lc-pitch-line { grid-template-columns: 3.2em 1fr; gap: 0.35em; }
}
.lc-pitch-blank { color: #9ca3af; letter-spacing: 0.1em; }
/* a derived blank: filled by a wire, not by typing */
.lc-pitch-calc { color: #4c3fd4; border-bottom: 2px dotted #a5b4fc; cursor: help; }
.lc-pitch-meta { margin-top: 0.6em; font-size: 0.82em; display: flex; gap: 0.5em; flex-wrap: wrap; }
.lc-pitch-chip { display: inline-block; background: #eef2f7; border-radius: 99px; padding: 0.1em 0.7em; color: #374151; text-decoration: none; }
.lc-pitch-chip:hover { background: #e2e8f0; }
.lc-pitch-warn { margin-top: 0.5em; font-size: 0.85em; color: #b45309; background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 0.4em 0.7em; }

.lc-imap { border: 1px solid #e5e7eb; border-radius: 10px; margin: 1em 0; background: #fff; padding: 0.9em 1.1em; font-size: 0.92em; box-shadow: 0 1px 3px rgba(0,0,0,0.05); overflow-x: auto; }
.lc-imap ul { list-style: none; margin: 0; padding-left: 1.4em; border-left: 2px solid #eef2f7; }
.lc-imap > ul { padding-left: 0; border-left: none; }
.lc-imap li { margin: 0.3em 0; }
.lc-imap-goal { font-weight: 700; color: #111827; }
.lc-imap-who { font-weight: 600; color: #374151; }
.lc-imap-what a { text-decoration: none; }
.lc-imap-found { margin-top: 0.7em; font-size: 0.85em; color: #6b7280; }

/* save= — the learner's keep bar, same grammar as the datagrid's */
.lc-ps-savebar { display: flex; align-items: center; gap: 0.5em; padding: 0.4em 0.9em; border-top: 1px solid #e5e7eb; background: #fafafa; font-size: 0.85em; }
.lc-pitch .lc-ps-savebar { border-top: none; padding: 0.4em 0 0; background: transparent; }
.lc-ps-mine { color: #16a34a; }
.lc-ps-empty { color: #6b7280; font-style: italic; }
.lc-ps-save { font: inherit; padding: 0.3em 0.9em; border-radius: 6px; border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; margin-left: auto; }
.lc-ps-save:hover { background: #0052a3; }
</style>

<script>
(function () {
  if (window._lcProblemSpaceReady) return;
  window._lcProblemSpaceReady = true;

  var escapeHtml = window.lcEscapeHtml;
  var parseData = window.lcParseDataText;

  function carryId(el, node, fallback) {
    var id = el.id || fallback;
    node.id = id;
    node.setAttribute("data-lc-id", id);
    return id;
  }
  function asList(v) {
    if (v == null || v === "") return [];
    return Array.isArray(v) ? v : [v];
  }
  function fail(el, cls, e) {
    var d = document.createElement("div");
    d.className = cls;
    d.innerHTML = "<div style='color:#c00;padding:0.6em 1em'>" + escapeHtml(e.message || String(e)) + "</div>";
    el.parentNode.replaceChild(d, el);
  }
  /* words that carry meaning — the drift check compares these */
  function words(s) {
    return String(s || "").toLowerCase().split(/[^a-zà-ÿ0-9]+/).filter(function (w) { return w.length > 3; });
  }

  /* ── the two wires every document shares ─────────────────────────────
     source="<form id>": the form is the editor, we are the live view.
     save="<file>":      the learner's own copy, in their bench. */
  function readSource(id) {
    var el = document.querySelector("[data-lc-id='" + id + "']");
    if (el) {
      var v = el.getAttribute("data-lc-value");
      if (v) { try { return JSON.parse(v); } catch (e) {} }
    }
    return (window.lcDatasets || {})[id] || null;
  }
  function onSourceChange(id, fn) {
    document.addEventListener("lc-model-changed", function () { fn(); });
    if (window.lcDatasetListeners)
      (window.lcDatasetListeners[id] = window.lcDatasetListeners[id] || []).push(function () { fn(); });
  }
  /* minimal YAML out: flat scalars, lists, and lists of flat objects —
     exactly the shapes the three documents use. Strings go out JSON-quoted,
     which YAML reads back verbatim. */
  function dumpYaml(obj) {
    var out = [];
    Object.keys(obj || {}).forEach(function (k) {
      var v = obj[k];
      if (Array.isArray(v)) {
        out.push(k + ":");
        v.forEach(function (item) {
          if (item && typeof item === "object") {
            var keys = Object.keys(item);
            keys.forEach(function (ik, i) {
              out.push((i ? "    " : "  - ") + ik + ": " + JSON.stringify(String(item[ik] == null ? "" : item[ik])));
            });
          } else {
            out.push("  - " + JSON.stringify(String(item == null ? "" : item)));
          }
        });
      } else if (v && typeof v === "object") {
        out.push(k + ":");
        Object.keys(v).forEach(function (ik) {
          out.push("  " + ik + ": " + JSON.stringify(String(v[ik] == null ? "" : v[ik])));
        });
      } else {
        out.push(k + ": " + JSON.stringify(String(v == null ? "" : v)));
      }
    });
    return out.join("\n") + "\n";
  }
  /* the learner's bench copy arrives AFTER the page rendered: push it into
     the editor form field by field, through the same path a human edit takes
     (lcFormSet → grid → bus), so the view follows for free. The form's grid
     may still be booting — retry, then give up quietly. */
  function pushToForm(formId, obj, tries) {
    var any = false;
    Object.keys(obj || {}).forEach(function (k) {
      if (window.lcFormSet && window.lcFormSet(formId, k, obj[k])) any = true;
    });
    if (!any && tries > 0) setTimeout(function () { pushToForm(formId, obj, tries - 1); }, 700);
    return any;
  }
  /* wire one document card: live source + bench save. getData/render come
     from the component; this helper owns the plumbing. */
  function wireDoc(node, opts) {
    if (opts.srcId) {
      node.setAttribute("data-bind", opts.srcId);
      var pull = function () {
        var d = readSource(opts.srcId);
        if (d) { opts.setData(d); opts.render(); }
        return !!d;
      };
      pull();
      /* the editor form publishes its first value when ITS upgrade lands,
         without firing the bus — look again until it has */
      var tries = 0;
      (function again() {
        if (pull() || ++tries > 6) return;
        setTimeout(again, 600);
      })();
      onSourceChange(opts.srcId, pull);
    }
    if (!opts.save || !window.lcBench) return;
    /* WRITABLE ONLY WHERE SOMETHING CAN BE TYPED. save= without source= is a
       READ-ONLY view of the learner's saved document — the later pages of a
       module showing back what an earlier page built. A 💾 there offers to
       save a document nobody can edit, and on an empty card it would write
       the seed over their real work (Michel, 2026-08-10: "r/o where it
       should not be save buttons"). */
    var writable = !!opts.srcId;
    var bar = document.createElement("div");
    bar.className = "lc-ps-savebar";
    /* AND THE BUTTON BELONGS TO THE EDITOR. The card is a view; the form is
       where the typing happens, so that is where 💾 goes — a save button under
       a read-only rendering reads as "save the view" (Michel, 2026-08-10:
       "the form should be editable with a save button"). */
    function editorEl() {
      return opts.srcId ? document.querySelector(".lc-form[data-lc-id='" + opts.srcId + "']") : null;
    }
    var mine = document.createElement("span");
    mine.className = "lc-ps-mine";
    mine.hidden = true;
    mine.textContent = writable ? "✓ yours — saved in your space" : "✓ yours";
    bar.appendChild(mine);
    var keep = null;
    if (writable) {
      keep = document.createElement("button");
      keep.type = "button";
      keep.className = "lc-ps-save";
      keep.textContent = "💾 Save";
      keep.title = "Keep this document in your own space";
      bar.appendChild(keep);
    } else {
      /* nothing saved yet: say where it gets built, instead of showing the
         author's empty seed as if it were the learner's document */
      var empty = document.createElement("span");
      empty.className = "lc-ps-empty";
      empty.textContent = "📄 nothing saved yet — build it on the page that has the editor, then press 💾.";
      bar.appendChild(empty);
      node.setAttribute("data-lc-readonly", "1");
      bar._lcEmpty = empty;
    }
    if (!writable) {
      node.appendChild(bar);
    } else {
      /* the editor may still be upgrading — wait for it rather than fall back
         to the card, which is the placement this rule exists to avoid */
      (function place(tries) {
        var host = editorEl();
        if (host) { host.appendChild(bar); return; }
        if (tries <= 0) { node.appendChild(bar); return; }
        setTimeout(function () { place(tries - 1); }, 400);
      })(12);
    }

    /* the stripe every saved block wears (widgets.md): a persona card IS a
       file in the learner's space, on the page that edits it and on every
       later page that reads it back */
    var psFrame = window.lcBenchFrame
      ? window.lcBenchFrame(node, { path: opts.save, id: node.id || "", mine: false })
      : null;

    var sha = null;
    window.lcBench.read(opts.save, node).then(function (f) {
      if (!f) return;
      return parseData(f.text, "yaml").then(function (obj) {
        if (!obj) return;
        sha = f.sha;
        mine.hidden = false;
        if (psFrame) psFrame.setMine(true);
        if (bar._lcEmpty) bar._lcEmpty.hidden = true;
        node.setAttribute("data-lc-mine", "1");
        if (!(opts.srcId && pushToForm(opts.srcId, obj, 5))) {
          opts.setData(obj);
          opts.render();
        }
      });
    }).catch(function () {});

    if (!keep) return;
    keep.addEventListener("click", function () {
      keep.disabled = true;
      window.lcBench.write(opts.save, dumpYaml(opts.getData()), "✍️ " + (node.id || opts.save), sha, node)
        .then(function (s) {
          sha = s || sha;
          mine.hidden = false;
          if (psFrame) psFrame.setMine(true);
          node.setAttribute("data-lc-mine", "1");
        })
        .catch(function (e) { alert("Save failed: " + (e.message || e)); })
        .then(function () { keep.disabled = false; });
    });
  }

  /* ── .persona — the empathy-map card ─────────────────────────────── */
  function personaHtml(p) {
    var photo = p.photo
      ? "<img class='lc-persona-photo' src='" + escapeHtml(p.photo) + "' alt='" + escapeHtml(p.name || "persona") + "'>"
      : "<div class='lc-persona-photo lc-persona-photo-empty'>👤</div>";
    var h = "<div class='lc-persona-head'>" + photo +
      "<div><div class='lc-persona-name'>" + escapeHtml(p.name || "Unnamed") + "</div>" +
      "<div class='lc-persona-role'>" + escapeHtml(p.role || "") + "</div></div></div>";
    var b = "<div class='lc-persona-body'>";
    if (p.goal) b += "<div class='lc-persona-row'>🎯 <b>Goal</b> — " + escapeHtml(p.goal) + "</div>";
    asList(p.frustrations).forEach(function (f) {
      b += "<div class='lc-persona-row'>😖 <b>Frustration</b> — " + escapeHtml(f) + "</div>";
    });
    if (p.quote) b += "<div class='lc-persona-quote'>“" + escapeHtml(p.quote) + "”</div>";
    b += "</div>";
    var cells = [["🗣️ Says", p.says], ["💭 Thinks", p.thinks], ["🏃 Does", p.does], ["💗 Feels", p.feels]]
      .filter(function (c) { return asList(c[1]).length; });
    var g = "";
    if (cells.length) {
      g = "<div class='lc-empathy'>" + cells.map(function (c) {
        return "<div class='lc-empathy-cell'><h5>" + c[0] + "</h5><ul>" +
          asList(c[1]).map(function (v) { return "<li>" + escapeHtml(v) + "</li>"; }).join("") +
          "</ul></div>";
      }).join("") + "</div>";
    }
    return h + b + g;
  }
  function upgradePersona(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = (el.querySelector("code") || {}).textContent || "";
    var srcId = el.getAttribute("source") || "";
    var save = el.getAttribute("save") || "";
    parseData(raw, "yaml").then(function (seed) {
      var data = seed || {};
      var card = document.createElement("div");
      card.className = "lc-persona";
      var id = carryId(el, card, "persona");
      var body = document.createElement("div");
      card.appendChild(body);
      function render() {
        body.innerHTML = personaHtml(data);
        /* data-lc-value is the platform's "here is my object" contract — the
           same one forms publish, so a {= persona.goal } cell reads a document
           exactly as it reads a form field. */
        card.setAttribute("data-lc-value", JSON.stringify(data));
        if (window.lcSetDataset) window.lcSetDataset(id, data);
      }
      /* IN THE PAGE FIRST, WIRED SECOND. wireDoc resolves save= against the
         rendered lesson's folder, and a detached card has no ancestors to
         resolve against (2026-08-13). */
      render();
      el.parentNode.replaceChild(card, el);
      wireDoc(card, {
        srcId: srcId, save: save, render: render,
        getData: function () { return data; },
        setData: function (d) { data = d; }
      });
    }).catch(function (e) { fail(el, "lc-persona", e); });
  }

  /* ── .pitch — the assembled two sentences, one emoji per blank ────── */
  var SHAPE = [
    ["For", "who", "👥"], ["who", "need", "🎯"], ["our", "product", "📦"],
    ["is a", "category", "🗂️"], ["that", "benefit", "💎"],
    ["Unlike", "alternative", "🆚"], ["it", "difference", "⚡"]
  ];
  /* who = the persona this pitch reads. A pitch that names a persona does not
     get to invent its own audience — the knob IS the answer, so who is
     derived, never typed (Michel, 2026-08-10). Without a persona knob the
     field stays the author's to fill. */
  function pitchWho(p, ref) {
    var persona = ref ? (window.lcDatasets || {})[ref] : null;
    if (!persona) return { v: p.who || "", calc: false };
    /* the PERSONA, not its subtitle: the name is who the pitch serves —
       the role is how the card explains them (Michel, 2026-08-24) */
    return { v: persona.name || persona.role || "", calc: true };
  }
  function pitchHtml(p, ref) {
    var who = pitchWho(p, ref);
    var text = SHAPE.map(function (part) {
      var v = part[1] === "who" ? who.v : p[part[1]];
      var calc = part[1] === "who" && who.calc;
      var body;
      if (v && calc)
        body = "<b class='lc-pitch-calc' title='read from #" + escapeHtml(ref) + "'>" + escapeHtml(v) + "</b>";
      else
        body = v ? "<b>" + escapeHtml(v) + "</b>"
                 : "<span class='lc-pitch-blank' title='" + part[1] + "'>＿＿＿</span>";
      return "<div class='lc-pitch-line' data-field='" + part[1] + "'>"
        + "<span class='lc-pitch-lead'>" + escapeHtml(part[0]) + "</span>"
        + "<span>" + part[2] + " " + body + "</span></div>";
    }).join("");
    var meta = ref
      ? "<div class='lc-pitch-meta'><a class='lc-pitch-chip' href='#" + escapeHtml(ref) + "'>👤 reads #" + escapeHtml(ref) + "</a></div>"
      : "";
    return "<div class='lc-pitch-text'>" + text + "</div>" + meta +
      "<div class='lc-pitch-warn' hidden></div>";
  }
  function upgradePitch(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = (el.querySelector("code") || {}).textContent || "";
    var ref = el.getAttribute("persona") || "";
    var srcId = el.getAttribute("source") || "";
    var save = el.getAttribute("save") || "";
    parseData(raw, "yaml").then(function (seed) {
      var data = seed || {};
      var box = document.createElement("div");
      box.className = "lc-pitch";
      var id = carryId(el, box, "pitch");
      if (ref) box.setAttribute("data-persona", ref);
      var body = document.createElement("div");
      box.appendChild(body);
      /* soft drift check: who/need should echo the persona this pitch
         reads. A finding, not an error — the documents check each other. */
      function check() {
        var warn = body.querySelector(".lc-pitch-warn");
        var persona = ref ? (window.lcDatasets || {})[ref] : null;
        if (!warn || !persona) return;
        /* who is DERIVED from this persona, so it cannot drift. What the
           learner types is the need — and a need that echoes nothing on the
           card is the real finding. */
        var mine = words(data.need);
        var theirs = words(persona.goal)
          .concat(words(persona.role), asList(persona.frustrations).join(" ").split(/\s+/));
        theirs = theirs.filter(function (w) { return w.length > 3; });
        if (!mine.length || !theirs.length) return;
        var hit = mine.some(function (w) { return theirs.indexOf(w.toLowerCase()) >= 0; });
        warn.hidden = hit;
        if (!hit) warn.textContent = "⚠️ the need echoes nothing on #" + ref + " — one of the two documents may be off.";
      }
      function render() {
        body.innerHTML = pitchHtml(data, ref);
        /* publish the document AS RENDERED — the derived who included — so
           cells, proofs and the impact map all read the same pitch a reader
           sees, not the half of it that was typed. */
        var pub = {}, who = pitchWho(data, ref);
        Object.keys(data).forEach(function (k) { pub[k] = data[k]; });
        pub.who = who.v;
        pub.who_calculated = who.calc;
        box.setAttribute("data-lc-value", JSON.stringify(pub));
        if (window.lcSetDataset) window.lcSetDataset(id, pub);
        check();
      }
      render();
      el.parentNode.replaceChild(box, el);
      wireDoc(box, {                        /* attached first — see .persona */
        srcId: srcId, save: save, render: render,
        getData: function () { return data; },
        setData: function (d) { data = d; }
      });
      /* RE-RENDER, not just re-check: the persona may register AFTER this
         pitch upgraded (a card further down the page), and the who is derived
         from it — a pitch that only re-checked kept showing the typed value
         forever. render() calls check() itself. */
      if (ref && window.lcDatasetListeners)
        (window.lcDatasetListeners[ref] = window.lcDatasetListeners[ref] || []).push(render);
    }).catch(function (e) { fail(el, "lc-pitch", e); });
  }

  /* ── .impact_map — goal → who → how → what, proofs collected ─────── */
  function statusDot(card) {
    if (card.classList.contains("lc-feature-passing")) return "🟢";
    if (card.classList.contains("lc-feature-failing")) return "🔴";
    return "🟡";
  }
  function upgradeImpactMap(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var raw = (el.querySelector("code") || {}).textContent || "";
    var pitchRef = el.getAttribute("pitch") || "";
    parseData(raw, "yaml").then(function (m) {
      m = m || {};
      var box = document.createElement("div");
      box.className = "lc-imap";
      carryId(el, box, "impact_map");
      if (pitchRef) box.setAttribute("data-pitch", pitchRef);
      function render() {
        var pitch = pitchRef ? (window.lcDatasets || {})[pitchRef] : null;
        var goal = m.goal || (pitch && pitch.benefit) || "";
        var who = m.who || (pitch && pitch.who) || "";
        var rows = Array.isArray(m.impacts) ? m.impacts : [];
        var html = "<ul><li class='lc-imap-goal'>🎯 " + (goal ? escapeHtml(goal) : "<span class='lc-pitch-blank'>＿＿＿</span>");
        html += "<ul><li class='lc-imap-who'>👥 " + (who ? escapeHtml(who) : "<span class='lc-pitch-blank'>＿＿＿</span>") + "<ul>";
        html += rows.map(function (r) {
          var what = r.feature
            ? "<a href='#" + escapeHtml(r.feature) + "'>" + escapeHtml(r.what || r.feature) + "</a>"
            : escapeHtml(r.what || "");
          return "<li class='lc-imap-how'>🔀 " + escapeHtml(r.how || "") +
            "<ul><li class='lc-imap-what'>🧩 " + what + "</li></ul></li>";
        }).join("");
        html += "</ul></li></ul></li></ul>";
        if (pitchRef) html += "<div class='lc-pitch-meta'><a class='lc-pitch-chip' href='#" + escapeHtml(pitchRef) + "'>✨ reads #" + escapeHtml(pitchRef) + "</a></div>";
        html += "<div class='lc-imap-found' hidden></div>";
        box.innerHTML = html;
      }
      render();
      el.parentNode.replaceChild(box, el);
      if (pitchRef && window.lcDatasetListeners)
        (window.lcDatasetListeners[pitchRef] = window.lcDatasetListeners[pitchRef] || []).push(render);

      /* collect the page's proofs as leaves — a map that names features
         which actually run. Proofs upgrade after us, so look twice. */
      var referenced = (Array.isArray(m.impacts) ? m.impacts : [])
        .map(function (r) { return r.feature; }).filter(Boolean);
      function collect() {
        var found = [];
        document.querySelectorAll(".lc-feature").forEach(function (card) {
          var id = card.getAttribute("data-lc-id") || card.id;
          if (referenced.indexOf(id) >= 0) return;
          var name = (card.querySelector(".lc-feature-name") || {}).textContent || id || "proof";
          found.push(statusDot(card) + " <a href='#" + escapeHtml(id || "") + "'>" + escapeHtml(name.trim()) + "</a>");
        });
        var slot = box.querySelector(".lc-imap-found");
        if (!slot) return;
        slot.hidden = !found.length;
        if (found.length) slot.innerHTML = "🧩 proofs on this page, not yet on the map: " + found.join(" · ");
      }
      setTimeout(collect, 1000);
      setTimeout(collect, 4000);
    }).catch(function (e) { fail(el, "lc-imap", e); });
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.persona, pre.persona", upgradePersona);
    window.lcRegisterUpgrader(".highlighter-rouge.pitch, pre.pitch", upgradePitch);
    window.lcRegisterUpgrader(".highlighter-rouge.impact_map, pre.impact_map", upgradeImpactMap);
  }
})();
</script>
