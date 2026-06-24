{%- comment -%}
Scaffold — a small "page tab scaffolding" mock for the KARMA story.

Shows a page's tabs as chips. An "Edit-page mode" toggle reveals one extra,
intentionally EMPTY "Log" tab — the placeholder KARMA will fill. There is no
backend, no engine, no data here by design: the Log stays empty.

Usage:
  ```yaml
  title: "adopt_wanda.md"
  tabs:
    - "① The Platform Today"
    - "② The Gap"
    - "③ KARMA"
  log:
    label: "📋 Log"
    note: "Process Log — captured by KARMA · in development"
  ```
  {: .scaffold }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-scaffold { border: 1px solid #d8dee6; border-radius: 8px; margin: 1.3em 0; overflow: hidden; background: #fff; }
.lc-scaffold-head { display: flex; align-items: center; gap: 10px; padding: 8px 12px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-size: 0.85em; }
.lc-scaffold-title { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #475569; }
.lc-scaffold-toggle { margin-left: auto; background: #fff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px 11px; font-size: 0.92em; cursor: pointer; color: #334155; white-space: nowrap; }
.lc-scaffold-toggle:hover { background: #f1f5f9; }
.lc-scaffold.lc-scaffold-editing .lc-scaffold-toggle { background: #9333ea; color: #fff; border-color: #9333ea; }
.lc-scaffold-bar { display: flex; flex-wrap: wrap; align-items: flex-end; background: #f5f5f5; border-bottom: 1px solid #ddd; }
.lc-scaffold-chip { background: none; border: none; border-right: 1px solid #ddd; padding: 0.55em 1.1em; cursor: pointer; font-size: 0.95em; color: #555; }
.lc-scaffold-chip:hover { background: #eaeaea; }
.lc-scaffold-chip.active { background: #fff; color: #0066cc; font-weight: 600; box-shadow: inset 0 -3px 0 #0066cc; }
.lc-scaffold-chip-log { display: none; color: #9333ea; }
.lc-scaffold.lc-scaffold-editing .lc-scaffold-chip-log { display: inline-block; border: 1px dashed #c4b5fd; border-right: 1px dashed #c4b5fd; border-radius: 6px 6px 0 0; margin: 3px 3px 0; }
.lc-scaffold.lc-scaffold-editing .lc-scaffold-chip-log.active { background: #faf5ff; box-shadow: inset 0 -3px 0 #9333ea; }
.lc-scaffold-panel { padding: 1em 1.3em; min-height: 64px; }
.lc-scaffold-content { color: #94a3b8; font-style: italic; }
.lc-scaffold-lognote { color: #6b21a8; font-weight: 600; margin-bottom: 9px; }
.lc-scaffold-emptybox { border: 2px dashed #d8b4fe; border-radius: 8px; padding: 1.5em; text-align: center; color: #9a7fc0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.9em; background: repeating-linear-gradient(45deg, #fcfaff, #fcfaff 10px, #f7f0ff 10px, #f7f0ff 20px); }
.lc-scaffold.lc-scaffold-editing { border-color: #c4b5fd; box-shadow: 0 0 0 3px rgba(147,51,234,0.08); }
.lc-scaffold.lc-scaffold-editing .lc-scaffold-head { background: #faf5ff; }
</style>

<script>
(function () {
  if (window._lcScaffoldReady) return;
  window._lcScaffoldReady = true;

  function upgrade(el) {
    if (el.dataset.lcScaffoldDone) return;
    el.dataset.lcScaffoldDone = "1";
    var raw = (el.querySelector("code") || el).textContent.trim();
    var done = function () {
      var cfg = {};
      try { cfg = (window.jsyaml ? window.jsyaml.load(raw) : JSON.parse(raw)) || {}; } catch (e) {}
      build(el, cfg);
    };
    if (window.lcLoadJsYaml) window.lcLoadJsYaml().then(done); else done();
  }

  function build(el, cfg) {
    var tabs = Array.isArray(cfg.tabs) ? cfg.tabs : [];
    var logCfg = cfg.log || {};
    var logLabel = logCfg.label || "📋 Log";
    var logNote = logCfg.note || "Process Log — captured by KARMA · in development";
    var logIndex = tabs.length;   /* the Log chip sits after the content tabs */

    var wrap = document.createElement("div");
    wrap.className = "lc-scaffold";
    if (el.id) { wrap.id = el.id; wrap.setAttribute("data-lc-id", el.id); }

    var head = document.createElement("div");
    head.className = "lc-scaffold-head";
    var title = document.createElement("span");
    title.className = "lc-scaffold-title";
    title.textContent = cfg.title || "page tabs";
    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "lc-scaffold-toggle";
    head.appendChild(title);
    head.appendChild(toggle);
    wrap.appendChild(head);

    var bar = document.createElement("div");
    bar.className = "lc-scaffold-bar";
    var panel = document.createElement("div");
    panel.className = "lc-scaffold-panel";
    var chips = [];

    function renderPanel(i) {
      panel.innerHTML = "";
      if (i === logIndex) {
        var note = document.createElement("div");
        note.className = "lc-scaffold-lognote";
        note.textContent = logNote;
        var empty = document.createElement("div");
        empty.className = "lc-scaffold-emptybox";
        empty.textContent = "— empty by design · coming with KARMA —";
        panel.appendChild(note);
        panel.appendChild(empty);
      } else {
        var ph = document.createElement("div");
        ph.className = "lc-scaffold-content";
        ph.textContent = "(page content for “" + (tabs[i] || "") + "”)";
        panel.appendChild(ph);
      }
    }

    function select(i) {
      chips.forEach(function (c, j) { c.classList.toggle("active", j === i); });
      renderPanel(i);
    }

    tabs.forEach(function (label, i) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "lc-scaffold-chip";
      chip.textContent = label;
      chip.addEventListener("click", function () { select(i); });
      bar.appendChild(chip);
      chips.push(chip);
    });

    var logChip = document.createElement("button");
    logChip.type = "button";
    logChip.className = "lc-scaffold-chip lc-scaffold-chip-log";
    logChip.textContent = logLabel;
    logChip.addEventListener("click", function () { select(logIndex); });
    bar.appendChild(logChip);
    chips.push(logChip);

    wrap.appendChild(bar);
    wrap.appendChild(panel);

    var editing = false;
    function setEditing(on) {
      editing = on;
      wrap.classList.toggle("lc-scaffold-editing", on);
      toggle.textContent = on ? "🛠️ Edit-page mode: ON" : "🛠️ Edit-page mode";
      toggle.setAttribute("aria-pressed", on ? "true" : "false");
      select(on ? logIndex : 0);   /* ON → reveal & focus the empty Log tab */
    }
    toggle.addEventListener("click", function () { setEditing(!editing); });

    el.parentNode.replaceChild(wrap, el);
    setEditing(false);
  }

  /* code_chrome.md provides the scan registry — one registration covers the
     initial scan and every re-scan. */
  window.lcRegisterUpgrader &&
    window.lcRegisterUpgrader(".highlighter-rouge.scaffold, pre.scaffold", upgrade);
})();
</script>
