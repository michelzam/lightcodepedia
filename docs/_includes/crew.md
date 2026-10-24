{%- comment -%}
🧑‍🤝‍🧑 Crew — agents as rows, a loop with its bounds, one line.

    ```csv
    name,kind,system,checked_by,reads
    Sid,rules,sort,,
    Rey,reader,"One line — VERDICT: asked, met or home",Chuck,
    Chuck,checker,"One stage at a time — AGREE or DISAGREE",,
    ```
    {: .dataset #members }

    [The front desk](#)
    {: .crew members="members" inbox="inbox" stages="asked, met, home" tries="2" budget="6" #desk }

THE AGENTS ARE DATA (Michel, 2026-10-23: "data-driven dynamic instances
initiated by a simple dataset … encapsulated, declarative, with clear
bounds"). One row, one member — an agent whose attributes are the
columns (name, system, and provider, model, temperature, max_tokens if
set); kind, checked_by and reads wire it into the crew. Three kinds:
- rules   — system names a function of the page's .model; it answers a
            stage or None. Free.
- reader  — an AI ask: system is its instructions; it reads the message's
            words only, and must name a stage.
- checker — an AI ask on a reader's verdict, with the message's whole row
            (the family's stage): AGREE or DISAGREE, with why.
checked_by wires a reader to its checker; reads names a dataset whose rows
travel with the ask too.

STAGES, not lanes (Michel, 2026-10-24: "stage instead of lane, to remain
consistent with the previous module"): module 06's families move from
stage to stage; the inbox's row says where a family is, the crew writes
where it goes next — next_stage.

THE LOOP, PER MESSAGE: the rules in order; if none answers, the reader
proposes, its checker checks; a DISAGREE goes back to the reader with the
checker's words, until tries= per message or budget= AI asks in all; what
is still open takes fallback= (OPEN by default) — a person, never a guess. The crew writes
only its own datasets: <id>.sorted (each message with its next_stage, why,
tries, asks — a try is a read and its check, two asks — tokens), <id>.flow (the run as an event flow, each step's cost and
the result's confidence: ✅ a rule or a check, ⚠️ unchecked or open)
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
/* the bounds, played with: a stepper per bound, a gauge for the budget */
.lc-crew-step { display: inline-flex; align-items: center; gap: .15em; white-space: nowrap; }
.lc-crew-step button { font: inherit; line-height: 1; width: 1.6em; height: 1.6em; border-radius: 6px; border: 1px solid #c7cdd6; background: #fff; cursor: pointer; padding: 0; }
.lc-crew-step button:disabled { color: #c0c4ca; cursor: default; }
.lc-crew-step b { min-width: 1.4em; text-align: center; color: #24292f; }
.lc-crew-gauge { display: flex; align-items: center; gap: .6em; font-size: .85em; color: #57606a; margin-top: .45em; }
.lc-crew-gauge-bar { flex: 0 1 14em; height: .55em; border-radius: 999px; background: #eef2f6; overflow: hidden; }
.lc-crew-gauge-bar i { display: block; height: 100%; width: 0; background: #2563eb; transition: width .3s; }
.lc-crew-gauge[data-level="high"] .lc-crew-gauge-bar i { background: #f59e0b; }
.lc-crew-gauge[data-level="spent"] .lc-crew-gauge-bar i { background: #dc2626; }
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
    if (!mp) return Promise.resolve({ stage: "", error: "no Python on this page" });
    return mp.then(function (m) {
      return new Promise(function (ok) {
        var cid = "crew" + (++nCall);
        waiting[cid] = function (stage, error) { ok({ stage: stage, error: error }); };
        var pre = window._lcModelPreIn === m ? "" : ((document.getElementById("lc-steps-preamble") || {}).textContent || "") + "\n";
        var run = m.runPython || m.exec || m.pyexec || m.run;
        try { run.call(m, pre + "_lc_crew_rule(" + JSON.stringify(cid) + "," + JSON.stringify(fn) + "," + JSON.stringify(text) + ")"); window._lcModelPreIn = m; }
        catch (e) { delete waiting[cid]; ok({ stage: "", error: String(e && e.message || e) }); }
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
        return { text: String(r.text || ""), error: r.error ? String(r.error) : "", unsent: !!r.unsent, usage: r.usage || null, engine: r.engine || null,
                 tokens: parseInt(u.total_tokens || ((u.prompt_tokens || 0) + (u.completion_tokens || 0)), 10) || 0 };
      }, function (e) { return { text: "", error: String(e && e.message || e), tokens: 0 }; });
  }

  /* the first stage an answer names, VERDICT: first */
  function stageIn(text, stages) {
    var t = String(text || "").toUpperCase(), v = t.split("VERDICT:")[1] || t;
    var best = null, at = Infinity;
    /* a whole word: "met" is not in "METHOD" */
    stages.forEach(function (l) { var m = new RegExp("\\b" + l.toUpperCase() + "\\b").exec(v); if (m && m.index < at) { at = m.index; best = l; } });
    return best;
  }
  var disagrees = function (text) { return /\bDISAGREE\b/i.test(text || ""); };

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var id = el.id || ("crew" + (++nCall));
    var knob = function (k, d) { var v = el.getAttribute(k); return v == null || v === "" ? d : v; };
    var membersId = knob("members", "members"), inboxId = knob("inbox", "inbox"), textCol = knob("text", "message");
    var stages = knob("stages", "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    var tries = Math.max(1, parseInt(knob("tries", "2"), 10) || 2), budget = Math.max(0, parseInt(knob("budget", "6"), 10) || 0);
    /* OPEN by default: what the desk could not settle reads as undecided, never
       as a stage someone chose (Michel, 2026-10-24: "open lane") */
    var fallback = knob("fallback", "OPEN");
    var crewCfg = { provider: knob("provider", ""), model: knob("model", ""), temperature: knob("temperature", ""), max_tokens: knob("max_tokens", "") };
    /* pace= seconds between steps: the work is seen, a row at a time (Michel, 2026-10-23: "progressively sorted, with the selection and sleeps") */
    var pace = Math.max(0, parseFloat(knob("pace", "0.5")) || 0);
    var nap = function () { return new Promise(function (ok) { setTimeout(ok, pace * 1000); }); };
    /* the row at work, selected in every grid that shows the crew's result */
    var pick = function (who) { [].forEach.call(document.querySelectorAll(".lc-datagrid[data-bind='" + id + ".sorted']"), function (g) { if (g._lcSelectRow) g._lcSelectRow(who); }); };

    var box = document.createElement("div");
    box.className = "lc-crew";
    box.id = id; box.setAttribute("data-lc-id", id);
    ["members", "inbox", "stages", "tries", "budget", "fallback", "text", "pace", "provider", "model", "temperature", "max_tokens"].forEach(function (k) { if (el.hasAttribute(k)) box.setAttribute(k, el.getAttribute(k)); });
    box.innerHTML = "<div class='lc-crew-head'><span class='lc-crew-title'>" + esc(el.textContent.trim() || "The crew") + "</span>" +
      "<span class='lc-crew-members'></span><button type='button' class='lc-crew-run'>▶ Run</button></div>" +
      "<div class='lc-crew-bounds'></div>" +
      "<div class='lc-crew-gauge' role='meter' aria-label='AI asks spent'><span class='lc-crew-gauge-bar'><i></i></span><span class='lc-crew-gauge-text'></span></div>" +
      "<div class='lc-crew-status'></div>" +
      "<div class='lc-agent-usage'>Used 0 tokens this session.</div>";
    el.parentNode.replaceChild(box, el);
    var btn = box.querySelector(".lc-crew-run"), status = box.querySelector(".lc-crew-status");
    /* the crew is an agent: the agent's own desk — 🔑 and the ring of engines —
       in its head, open while no key is held, the engine named beside the bounds,
       and the engine's 🔋 asks and tokens left per day, per minute, under its usage */
    var desk = window.lcAgentDesk ? window.lcAgentDesk(crewCfg) : null;
    if (desk) {
      box.querySelector(".lc-crew-head").insertBefore(desk.key, btn);
      box.insertBefore(desk.auth, box.querySelector(".lc-crew-bounds"));
      if (desk.quota) box.appendChild(desk.quota);
    }
    /* THE BOUNDS, PLAYED WITH (Michel, 2026-10-24: "make visible the constraints
       … play with the knob's values: tries and budget, maybe with jauges"): a
       stepper per bound, kept on the crew (desk.tries, desk.budget in Python),
       and a gauge of the budget filling as the run spends it */
    var bounds = box.querySelector(".lc-crew-bounds");
    var stepper = function (k, v, unit) {
      return "<span class='lc-crew-step' data-bound='" + k + "'><button type='button' data-d='-1' aria-label='" + k + " minus one'>−</button>" +
        "<b>" + v + "</b><button type='button' data-d='1' aria-label='" + k + " plus one'>+</button></span> " + unit;
    };
    var paintBounds = function () {
      bounds.innerHTML = "stages " + esc(stages.join(" · ")) + " — " + stepper("tries", tries, "tr" + (tries === 1 ? "y" : "ies") + " a message") +
        " — " + stepper("budget", budget, "AI ask" + (budget === 1 ? "" : "s") + " in all") + " — still open: " + esc(fallback) +
        (desk ? " — asks " + esc(desk.engine()) : "");
      [].forEach.call(bounds.querySelectorAll("button"), function (b) {
        var k = b.parentNode.getAttribute("data-bound"), v = k === "tries" ? tries : budget;
        b.disabled = box.getAttribute("data-state") === "running" || (+b.getAttribute("data-d") < 0 && v <= (k === "tries" ? 1 : 0));
      });
    };
    bounds.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-d]");
      if (!b || b.disabled) return;
      var k = b.parentNode.getAttribute("data-bound"), d = +b.getAttribute("data-d");
      if (k === "tries") tries = Math.max(1, tries + d); else budget = Math.max(0, budget + d);
      box.setAttribute(k, String(k === "tries" ? tries : budget));
      paintBounds(); gauge(+box.getAttribute("data-asks"));
    });
    var gaugeEl = box.querySelector(".lc-crew-gauge");
    var gauge = function (asks) {
      var f = budget ? Math.min(1, asks / budget) : 1;
      gaugeEl.querySelector("i").style.width = Math.round(f * 100) + "%";
      gaugeEl.setAttribute("data-level", asks >= budget ? "spent" : f >= 0.75 ? "high" : "low");
      gaugeEl.setAttribute("aria-valuenow", String(asks)); gaugeEl.setAttribute("aria-valuemax", String(budget));
      gaugeEl.querySelector(".lc-crew-gauge-text").textContent = asks + " of " + budget + " AI asks spent";
    };
    paintBounds();
    /* the inbox shows from the start, its stages still open; the run fills them in */
    /* next_stage: where each message moves its family — module 06's stages, a
       state each; the run moves each message to its next one (Michel, 2026-10-24) */
    var unsorted = function () { return rowsOf(inboxId).map(function (r) { return Object.assign({}, r, { next_stage: "", why: "", tries: "", asks: "", tokens: "" }); }); };
    window.lcSetDataset(id + ".sorted", unsorted());
    window.lcSetDataset(id + ".log", []);
    window.lcSetDataset(id + ".flow", []);
    box.setAttribute("data-asks", "0");
    box.setAttribute("data-tokens", "0");
    gauge(0);
    /* the crew is an agent: its tokens read as any agent's — the session, this
       run, who answered — and count in the day's total (Michel, 2026-10-24) */
    var usageEl = box.querySelector(".lc-agent-usage"), session = 0;

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
      var spend = function (d) { asks += d; box.setAttribute("data-asks", String(asks)); gauge(asks); };
      var say = function (who, kind, said, heard, tk, a) {
        tokens += tk || 0; session += tk || 0; box.setAttribute("data-tokens", String(tokens));
        if (a && a.usage) {
          if (window.lcTokens) window.lcTokens.add(a.usage);
          var eng = a.engine ? " · " + (a.engine.name || a.engine.pid || "") + " · " + (a.engine.model || "") : "";
          usageEl.textContent = "Session: " + session + " tokens · this run: " + tokens + eng + ".";
          if (desk && desk.showQuota) desk.showQuota(a.engine && a.engine.pid);
        }
        if (kind !== "rules" && /^⚠️/.test(String(heard))) failed++;
        log.push({ n: ++n, who: who, kind: kind, in: said, out: heard, tokens: tk || 0 }); window.lcSetDataset(id + ".log", log.slice());
      };
      /* THE RUN AS AN EVENT FLOW (Michel, 2026-10-24: "go flow"): who wrote, what
         each worker did, what governed it, and the event — a transition to a
         state, the message's next stage — with its cost, and the result's
         confidence: ✅ a rule or a check said so, ⚠️ unchecked or left open
         ("I would add the cost and benefit"). .event_flow source="<id>.flow" draws it. */
      var flow = [];
      var beat = function (kind, text) { var r = {}; r[kind] = text; flow.push(r); window.lcSetDataset(id + ".flow", flow.slice()); };
      var cost = function (tk) { return tk ? " · " + tk + " tokens" : ""; };
      window.lcSetDataset(id + ".flow", []);
      window.lcSetDataset(id + ".sorted", out.slice());
      btn.disabled = true; box.setAttribute("data-state", "running"); paintBounds(); gauge(0);
      var step = function (i) {
        if (i >= inbox.length) {
          box.setAttribute("data-state", "done"); paintBounds();
          status.textContent = "✓ " + out.length + " sorted, " + asks + " of " + budget + " AI asks, " + tokens + " tokens" +
            (failed ? " — ⚠️ the AI did not answer " + failed + " time" + (failed === 1 ? "" : "s") + ": 🔑 your keys" : "");
          /* an engine that did not answer: the desk opens, where the key is fixed */
          if (failed && desk) desk.open();
          btn.disabled = false;
          return Promise.resolve();
        }
        var row = inbox[i], text = String(row[textCol] == null ? "" : row[textCol]);
        var stage = null, tried = 0, note = "", spent = tokens, asked0 = asks, why = "", trouble = "", broke = false, sure = false;
        var spentBeat = function () { if (!broke) { broke = true; beat("rule", "budget spent: " + asks + " of " + budget + " AI asks"); } };
        var who = row.family || row.name || ("#" + (i + 1));
        status.textContent = "… " + who;
        out[i] = Object.assign({}, out[i], { next_stage: "⏳" });
        beat("user", who);
        beat("data", text);
        window.lcSetDataset(id + ".sorted", out.slice());
        pick(who);
        var byRules = rules.reduce(function (p, m) {
          return p.then(function () {
            if (stage) return;
            return rule(String(m.system || "").trim(), text).then(function (r) {
              say(m.name, "rules", text, r.error ? "⚠️ " + r.error : (r.stage || "—"));
              var l = stageIn(r.stage, stages); if (l) { stage = l; why = m.name + "'s rule"; sure = true; }
              beat("command", m.name + " sorts it");
              beat("event", l ? m.name + ": " + l : r.error ? "⚠️ " + r.error : m.name + ": no rule fits");
            });
          });
        }, nap());
        var loop = function () {
          if (stage || !reader || tried >= tries || asks >= budget) return Promise.resolve();
          tried++;
          status.textContent = "… " + who + ": " + reader.name + " reads";
          /* the reader reads the words; the checker checks them against the row */
          var context = reader.reads ? "\n\nWhat you know:\n" + JSON.stringify(rowsOf(reader.reads)) : "";
          spend(1);
          beat("command", reader.name + " reads it" + (note ? ", with " + (reader.checked_by || "the checker") + "'s words" : ""));
          return ask(reader, text + note + context, crewCfg).then(function (a) {
            /* an ask that never left this device (no key) costs nothing: not counted */
            if (a.unsent) spend(-1);
            say(reader.name, "reader", text + note, a.error ? "⚠️ " + a.error : a.text, a.tokens, a);
            if (a.error) trouble = a.unsent ? "no AI key" : "the AI did not answer";
            var verdict = stageIn(a.text, stages);
            beat("event", a.error ? "⚠️ " + (a.unsent ? "no AI key" : "the AI did not answer") : reader.name + " proposes " + (verdict || "no stage") + cost(a.tokens));
            if (!verdict) return a.error ? null : loop();
            var checker = reader.checked_by ? byName[reader.checked_by] : null;
            if (!checker) { stage = verdict; why = reader.name; return null; }
            if (asks >= budget) { spentBeat(); beat("event", checker.name + " cannot check"); return null; }
            status.textContent = "… " + who + ": " + checker.name + " checks " + verdict;
            beat("rule", checker.name + " checks " + verdict + " against " + who + "'s row" + (checker.reads ? " and " + checker.reads : ""));
            var cctx = checker.reads ? "\n\nWhat you know:\n" + JSON.stringify(rowsOf(checker.reads)) : "";
            spend(1);
            return ask(checker, "The message: " + text + "\nIts row: " + JSON.stringify(row) + "\nThe verdict: " + verdict + cctx, crewCfg).then(function (c) {
              say(checker.name, "checker", verdict, c.error ? "⚠️ " + c.error : c.text, c.tokens, c);
              beat("event", c.error ? "⚠️ the AI did not answer" : (disagrees(c.text) ? checker.name + " disagrees: " : checker.name + " agrees: ") + String(c.text).replace(/^\s*(DIS)?AGREE\W*/i, "").slice(0, 90) + cost(c.tokens));
              if (c.error) { trouble = "the AI did not answer"; return null; }
              if (disagrees(c.text)) { note = "\n\n" + checker.name + " disagreed with " + verdict + ": " + c.text; return loop(); }
              stage = verdict; why = checker.name + " agreed"; sure = true;
              return null;
            });
          });
        };
        return byRules.then(loop).then(function () {
          /* WHY, in words: who decided, or what stopped the desk (Michel, 2026-10-24:
             "how come Lindqvist were classified as CALL instead of visit?") */
          if (!stage) why = !reader ? "no reader" : trouble || (asks >= budget ? "budget spent" : "no agreement in " + tried + " tr" + (tried === 1 ? "y" : "ies"));
          if (!stage && why === "budget spent") spentBeat();
          var tk = tokens - spent;
          beat("event", who + " → " + (stage || fallback) + (sure ? " ✅" : " ⚠️ " + why) + (tk ? cost(tk) : " · free"));
          /* asks per message: a try is a read and its check — two asks — so the
             column adds up to the gauge (Michel, 2026-10-24: "the grid shows less") */
          out[i] = Object.assign({}, row, { next_stage: stage || fallback, why: why, tries: tried, asks: asks - asked0, tokens: tk });
          window.lcSetDataset(id + ".sorted", out.slice());
          pick(who);
          return nap().then(function () { return step(i + 1); });
        });
      };
      status.textContent = "…";
      step(0).catch(function (e) { status.textContent = "⚠️ " + (e && e.message || e); btn.disabled = false; box.setAttribute("data-state", "done"); paintBounds(); });
    });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.crew", upgrade);
})();
</script>
