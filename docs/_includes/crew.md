{%- comment -%}
🧑‍🤝‍🧑 Crew — agents as rows, a loop with its bounds, one line.

    ```csv
    name,kind,system,checked_by,reads
    Sid,rules,sort,,
    Rey,reader,"One line — VERDICT: VISIT, PAY or CALL",Chuck,
    Chuck,checker,"The dog cards win — AGREE or DISAGREE",,dogs
    ```
    {: .dataset #members }

    [The front desk](#)
    {: .crew members="members" inbox="inbox" lanes="VISIT, PAY, CALL" tries="2" budget="6" fallback="CALL" #desk }

THE AGENTS ARE DATA (Michel, 2026-10-23: "data-driven dynamic instances
initiated by a simple dataset … encapsulated, declarative, with clear
bounds"). One row, one member — an agent whose attributes are the
columns (name, system, and provider, model, temperature, max_tokens if
set); kind, checked_by and reads wire it into the crew. Three kinds:
- rules   — system names a function of the page's .model; it answers a
            lane or None. Free.
- reader  — an AI ask: system is its instructions; it must name a lane.
- checker — an AI ask on a reader's verdict: AGREE or DISAGREE, with why.
checked_by wires a reader to its checker; reads names a dataset whose rows
travel with the ask (the cards a checker trusts).

THE LOOP, PER MESSAGE: the rules in order; if none answers, the reader
proposes, its checker checks; a DISAGREE goes back to the reader with the
checker's words, until tries= per message or budget= AI asks in all; what
is still open takes fallback= — a person, never a guess. The crew writes
only its own datasets: <id>.sorted (each message with its lane and tries)
and <id>.log (every step: who, what in, what out, its tokens); the inbox
shows from the start and fills a row at a time, pace= seconds apart, the
row at work selected. The page acts on them;
the crew acts on nothing (the tutor rule).

Members ask with the reader's own key, the way an agent panel asks
(lcAgentAsk, agent.md: retries, a retired model healed) — no panel, the same ring. No key: the AI
members are skipped and say so; the rules still work.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-crew { border: 1px solid #d8dee4; border-radius: 10px; background: #fbfcfd; padding: .8em 1.1em; margin: 1.2em 0; }
.lc-crew-head { display: flex; align-items: center; gap: .8em; flex-wrap: wrap; }
.lc-crew-title { font-weight: 700; }
.lc-crew-members { display: flex; gap: .4em; flex-wrap: wrap; font-size: .9em; }
.lc-crew-member { background: #eef2f6; border-radius: 999px; padding: .1em .65em; }
.lc-crew-run { margin-left: auto; font-weight: 700; padding: .35em 1em; border-radius: 8px; border: 1px solid #2563eb; background: #2563eb; color: #fff; cursor: pointer; }
.lc-crew-run:disabled { background: #e5e7eb; border-color: #d1d5db; color: #9ca3af; cursor: default; }
.lc-crew-bounds { font-size: .85em; color: #57606a; margin-top: .4em; }
.lc-crew-status { font-size: .9em; color: #24292f; margin-top: .3em; min-height: 1.3em; }
@media print { .lc-crew-run { display: none; } }
</style>

<script>
(function () {
  if (window._lcCrewReady) return;
  window._lcCrewReady = true;

  var ICON = { rules: "🐍", reader: "🤖", checker: "🧐" };
  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  var rowsOf = function (id) { return ((window.lcDatasets || {})[id] || []).filter(function (r) { return r && !r["⚠️"]; }); };

  /* a rules member: the page's own Python function, in the page's MicroPython */
  var waiting = {}, nCall = 0;
  window.lcCrewAnswer = function (cid, ok, result) {
    var w = waiting[cid]; delete waiting[cid];
    if (w) w(ok ? String(result || "") : "", ok ? "" : String(result || ""));
  };
  function rule(fn, text) {
    var mp = window._lcMpReady || (window.lcMpy ? (window._lcMpReady = window.lcMpy()) : null);
    if (!mp) return Promise.resolve({ lane: "", error: "no Python on this page" });
    return mp.then(function (m) {
      return new Promise(function (ok) {
        var cid = "crew" + (++nCall);
        waiting[cid] = function (lane, error) { ok({ lane: lane, error: error }); };
        var pre = window._lcModelPreIn === m ? "" : ((document.getElementById("lc-steps-preamble") || {}).textContent || "") + "\n";
        var run = m.runPython || m.exec || m.pyexec || m.run;
        try { run.call(m, pre + "_lc_crew_rule(" + JSON.stringify(cid) + "," + JSON.stringify(fn) + "," + JSON.stringify(text) + ")"); window._lcModelPreIn = m; }
        catch (e) { delete waiting[cid]; ok({ lane: "", error: String(e && e.message || e) }); }
      });
    });
  }

  /* an AI member: one ask, made as the agent panel makes it (lcAgentAsk:
     the ring's key, a busy service retried, a retired model healed) */
  /* a member's own column wins, else the crew's knob (the crew is an agent:
     provider, model, temperature, max_tokens), else the crew's defaults */
  var pick1 = function (v, d) { return v != null && String(v).trim() !== "" ? v : d; };
  function ask(member, text, crew) {
    if (!window.lcAgentAsk) return Promise.resolve({ text: "", error: "this page has no agent engine", tokens: 0, unsent: true });
    return window.lcAgentAsk({
      system: member.system, provider: pick1(member.provider, crew.provider || ""), model: pick1(member.model, crew.model || ""),
      temperature: pick1(member.temperature, pick1(crew.temperature, 0)),
      max_tokens: pick1(member.max_tokens, pick1(crew.max_tokens, 300)) }, text).then(function (r) {
        var u = r.usage || {};
        return { text: String(r.text || ""), error: r.error ? String(r.error) : "", unsent: !!r.unsent,
                 tokens: parseInt(u.total_tokens || ((u.prompt_tokens || 0) + (u.completion_tokens || 0)), 10) || 0 };
      }, function (e) { return { text: "", error: String(e && e.message || e), tokens: 0 }; });
  }

  /* the first lane an answer names, VERDICT: first */
  function laneIn(text, lanes) {
    var t = String(text || "").toUpperCase(), v = t.split("VERDICT:")[1] || t;
    var best = null, at = Infinity;
    lanes.forEach(function (l) { var i = v.indexOf(l.toUpperCase()); if (i >= 0 && i < at) { at = i; best = l; } });
    return best;
  }
  var disagrees = function (text) { return /\bDISAGREE\b/i.test(text || ""); };

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var id = el.id || ("crew" + (++nCall));
    var knob = function (k, d) { var v = el.getAttribute(k); return v == null || v === "" ? d : v; };
    var membersId = knob("members", "members"), inboxId = knob("inbox", "inbox"), textCol = knob("text", "message");
    var lanes = knob("lanes", "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    var tries = Math.max(1, parseInt(knob("tries", "2"), 10) || 2), budget = Math.max(0, parseInt(knob("budget", "6"), 10) || 0);
    var fallback = knob("fallback", lanes[lanes.length - 1] || "CALL");
    var crewCfg = { provider: knob("provider", ""), model: knob("model", ""), temperature: knob("temperature", ""), max_tokens: knob("max_tokens", "") };
    /* pace= seconds between steps: the work is seen, a row at a time (Michel, 2026-10-23: "progressively sorted, with the selection and sleeps") */
    var pace = Math.max(0, parseFloat(knob("pace", "0.5")) || 0);
    var nap = function () { return new Promise(function (ok) { setTimeout(ok, pace * 1000); }); };
    /* the row at work, selected in every grid that shows the crew's result */
    var pick = function (who) { [].forEach.call(document.querySelectorAll(".lc-datagrid[data-bind='" + id + ".sorted']"), function (g) { if (g._lcSelectRow) g._lcSelectRow(who); }); };

    var box = document.createElement("div");
    box.className = "lc-crew";
    box.id = id; box.setAttribute("data-lc-id", id);
    ["members", "inbox", "lanes", "tries", "budget", "fallback", "text", "pace", "provider", "model", "temperature", "max_tokens"].forEach(function (k) { if (el.hasAttribute(k)) box.setAttribute(k, el.getAttribute(k)); });
    box.innerHTML = "<div class='lc-crew-head'><span class='lc-crew-title'>" + esc(el.textContent.trim() || "The crew") + "</span>" +
      "<span class='lc-crew-members'></span><button type='button' class='lc-crew-run'>▶ Run</button></div>" +
      "<div class='lc-crew-bounds'></div><div class='lc-crew-status'></div>";
    el.parentNode.replaceChild(box, el);
    var btn = box.querySelector(".lc-crew-run"), status = box.querySelector(".lc-crew-status");
    /* the crew is an agent: the agent's own desk — 🔑 and the ring of engines —
       in its head, open while no key is held, the engine named beside the bounds */
    var desk = window.lcAgentDesk ? window.lcAgentDesk(crewCfg) : null;
    if (desk) {
      box.querySelector(".lc-crew-head").insertBefore(desk.key, btn);
      box.insertBefore(desk.auth, box.querySelector(".lc-crew-bounds"));
    }
    box.querySelector(".lc-crew-bounds").textContent = "lanes " + lanes.join(" · ") + " — at most " + tries + " tr" + (tries === 1 ? "y" : "ies") +
      " a message, " + budget + " AI ask" + (budget === 1 ? "" : "s") + " in all — still open: " + fallback +
      (desk ? " — asks " + desk.engine() : "");
    /* the inbox shows from the start, its lanes still open; the run fills them in */
    var unsorted = function () { return rowsOf(inboxId).map(function (r) { return Object.assign({}, r, { lane: "", tries: "", tokens: "" }); }); };
    window.lcSetDataset(id + ".sorted", unsorted());
    window.lcSetDataset(id + ".log", []);
    box.setAttribute("data-asks", "0");
    box.setAttribute("data-tokens", "0");

    /* the members, as the dataset says them now — a new row is a new member */
    var members = function () { return rowsOf(membersId).map(function (r) { return Object.assign({}, r, { kind: String(r.kind || "").trim().toLowerCase(), name: String(r.name || "").trim() }); }); };
    var paint = function () {
      var ms = members(), names = {};
      ms.forEach(function (m) { names[m.name] = m; });
      box.querySelector(".lc-crew-members").innerHTML = ms.map(function (m) {
        return "<span class='lc-crew-member' title='" + esc(m.system) + "'>" + (ICON[m.kind] || "❔") + " " + esc(m.name) +
          (m.checked_by && names[m.checked_by] ? " ⇄ " + esc(m.checked_by) : "") + "</span>";
      }).join("");
      btn.disabled = !ms.length || !rowsOf(inboxId).length;
      btn.title = !ms.length ? "No members yet: " + membersId + " has no rows" : !rowsOf(inboxId).length ? "Nothing to sort: " + inboxId + " has no rows" : "";
    };
    paint();
    var L = window.lcDatasetListeners = window.lcDatasetListeners || {};
    [membersId, inboxId].forEach(function (k) { (L[k] = L[k] || []).push(paint); });

    btn.addEventListener("click", function () {
      var ms = members(), byName = {};
      ms.forEach(function (m) { byName[m.name] = m; });
      var rules = ms.filter(function (m) { return m.kind === "rules"; });
      var reader = ms.filter(function (m) { return m.kind === "reader"; })[0] || null;
      var inbox = rowsOf(inboxId), out = unsorted(), log = [], asks = 0, n = 0, tokens = 0, failed = 0;
      var say = function (who, kind, said, heard, tk) {
        tokens += tk || 0; box.setAttribute("data-tokens", String(tokens));
        if (kind !== "rules" && /^⚠️/.test(String(heard))) failed++;
        log.push({ n: ++n, who: who, kind: kind, in: said, out: heard, tokens: tk || 0 }); window.lcSetDataset(id + ".log", log.slice());
      };
      window.lcSetDataset(id + ".sorted", out.slice());
      btn.disabled = true; box.setAttribute("data-state", "running");
      var step = function (i) {
        if (i >= inbox.length) {
          box.setAttribute("data-state", "done");
          status.textContent = "✓ " + out.length + " sorted, " + asks + " of " + budget + " AI asks, " + tokens + " tokens" +
            (failed ? " — ⚠️ the AI did not answer " + failed + " time" + (failed === 1 ? "" : "s") + ": 🔑 your keys" : "");
          /* an engine that did not answer: the desk opens, where the key is fixed */
          if (failed && desk) desk.open();
          btn.disabled = false;
          return Promise.resolve();
        }
        var row = inbox[i], text = String(row[textCol] == null ? "" : row[textCol]);
        var lane = null, tried = 0, note = "", spent = tokens;
        var who = row.family || row.name || ("#" + (i + 1));
        status.textContent = "… " + who;
        out[i] = Object.assign({}, out[i], { lane: "⏳" });
        window.lcSetDataset(id + ".sorted", out.slice());
        pick(who);
        var byRules = rules.reduce(function (p, m) {
          return p.then(function () {
            if (lane) return;
            return rule(String(m.system || "").trim(), text).then(function (r) {
              say(m.name, "rules", text, r.error ? "⚠️ " + r.error : (r.lane || "—"));
              var l = laneIn(r.lane, lanes); if (l) lane = l;
            });
          });
        }, nap());
        var loop = function () {
          if (lane || !reader || tried >= tries || asks >= budget) return Promise.resolve();
          tried++;
          status.textContent = "… " + who + ": " + reader.name + " reads";
          var context = reader.reads ? "\n\nWhat you know:\n" + JSON.stringify(rowsOf(reader.reads)) : "";
          asks++; box.setAttribute("data-asks", String(asks));
          return ask(reader, text + note + context, crewCfg).then(function (a) {
            /* an ask that never left this device (no key) costs nothing: not counted */
            if (a.unsent) { asks--; box.setAttribute("data-asks", String(asks)); }
            say(reader.name, "reader", text + note, a.error ? "⚠️ " + a.error : a.text, a.tokens);
            var verdict = laneIn(a.text, lanes);
            if (!verdict) return a.error ? null : loop();
            var checker = reader.checked_by ? byName[reader.checked_by] : null;
            if (!checker) { lane = verdict; return null; }
            if (asks >= budget) return null;
            status.textContent = "… " + who + ": " + checker.name + " checks " + verdict;
            var cctx = checker.reads ? "\n\nWhat you know:\n" + JSON.stringify(rowsOf(checker.reads)) : "";
            asks++; box.setAttribute("data-asks", String(asks));
            return ask(checker, "The message: " + text + "\nThe verdict: " + verdict + cctx, crewCfg).then(function (c) {
              say(checker.name, "checker", verdict, c.error ? "⚠️ " + c.error : c.text, c.tokens);
              if (c.error) return null;
              if (disagrees(c.text)) { note = "\n\n" + checker.name + " disagreed with " + verdict + ": " + c.text; return loop(); }
              lane = verdict;
              return null;
            });
          });
        };
        return byRules.then(loop).then(function () {
          out[i] = Object.assign({}, row, { lane: lane || fallback, tries: tried, tokens: tokens - spent });
          window.lcSetDataset(id + ".sorted", out.slice());
          pick(who);
          return nap().then(function () { return step(i + 1); });
        });
      };
      status.textContent = "…";
      step(0).catch(function (e) { status.textContent = "⚠️ " + (e && e.message || e); btn.disabled = false; box.setAttribute("data-state", "done"); });
    });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.crew", upgrade);
})();
</script>
