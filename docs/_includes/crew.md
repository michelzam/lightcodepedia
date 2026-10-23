{%- comment -%}
🧑‍🤝‍🧑 Crew — agents as rows, a loop with its bounds, one line.

    ```csv
    name,kind,brief,checked_by,reads
    Sid,rules,sort,,
    Rey,reader,"One line — VERDICT: VISIT, PAY or CALL",Chuck,
    Chuck,checker,"The dog cards win — AGREE or DISAGREE",,dogs
    ```
    {: .dataset #members }

    [The front desk](#)
    {: .crew members="members" inbox="inbox" lanes="VISIT, PAY, CALL" tries="2" budget="6" fallback="CALL" #desk }

THE AGENTS ARE DATA (Michel, 2026-10-23: "data-driven dynamic instances
initiated by a simple dataset … encapsulated, declarative, with clear
bounds"). One row, one member; three kinds:
- rules   — brief names a function of the page's .model; it answers a
            lane or None. Free.
- reader  — an AI ask: brief is its instructions; it must name a lane.
- checker — an AI ask on a reader's verdict: AGREE or DISAGREE, with why.
checked_by wires a reader to its checker; reads names a dataset whose rows
travel with the ask (the cards a checker trusts).

THE LOOP, PER MESSAGE: the rules in order; if none answers, the reader
proposes, its checker checks; a DISAGREE goes back to the reader with the
checker's words, until tries= per message or budget= AI asks in all; what
is still open takes fallback= — a person, never a guess. The crew writes
only its own datasets: <id>.sorted (each message with its lane and tries)
and <id>.log (every step: who, what in, what out). The page acts on them;
the crew acts on nothing (the tutor rule).

Members ask with the reader's own key, through the agent's own request
(lcAgentRequest, agent.md) — no panel, the same ring. No key: the AI
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

  /* an AI member: one ask, the agent's own request, one retry when the service wobbles */
  function ask(member, text) {
    var req = window.lcAgentRequest ? window.lcAgentRequest({
      system: member.brief, provider: member.provider || "", model: member.model || "",
      temperature: member.temperature != null && member.temperature !== "" ? member.temperature : 0,
      max_tokens: member.max_tokens || 300 }, text) : null;
    if (!req) return Promise.resolve({ text: "", error: "no AI key on this device" });
    var once = function () {
      return fetch(req.url, { method: "POST", headers: { "Authorization": "Bearer " + req.token, "Content-Type": "application/json" }, body: req.body })
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (j) {
            if (!r.ok) throw { status: r.status, text: (j.error && j.error.message) || ("HTTP " + r.status) };
            var t = j.choices && j.choices[0] && j.choices[0].message ? j.choices[0].message.content : "";
            return { text: String(t || ""), error: "" };
          });
        });
    };
    return once().catch(function (e) {
      if (e && e.status >= 500) return once();
      throw e;
    }).catch(function (e) { return { text: "", error: (e && e.text) || String(e && e.message || e) }; });
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

    var box = document.createElement("div");
    box.className = "lc-crew";
    box.id = id; box.setAttribute("data-lc-id", id);
    ["members", "inbox", "lanes", "tries", "budget", "fallback", "text"].forEach(function (k) { if (el.hasAttribute(k)) box.setAttribute(k, el.getAttribute(k)); });
    box.innerHTML = "<div class='lc-crew-head'><span class='lc-crew-title'>" + esc(el.textContent.trim() || "The crew") + "</span>" +
      "<span class='lc-crew-members'></span><button type='button' class='lc-crew-run'>▶ Run</button></div>" +
      "<div class='lc-crew-bounds'></div><div class='lc-crew-status'></div>";
    el.parentNode.replaceChild(box, el);
    var btn = box.querySelector(".lc-crew-run"), status = box.querySelector(".lc-crew-status");
    box.querySelector(".lc-crew-bounds").textContent = "lanes " + lanes.join(" · ") + " — at most " + tries + " tr" + (tries === 1 ? "y" : "ies") +
      " a message, " + budget + " AI ask" + (budget === 1 ? "" : "s") + " in all — still open: " + fallback;
    window.lcSetDataset(id + ".sorted", []);
    window.lcSetDataset(id + ".log", []);
    box.setAttribute("data-asks", "0");

    /* the members, as the dataset says them now — a new row is a new member */
    var members = function () { return rowsOf(membersId).map(function (r) { return Object.assign({}, r, { kind: String(r.kind || "").trim().toLowerCase(), name: String(r.name || "").trim() }); }); };
    var paint = function () {
      var ms = members(), names = {};
      ms.forEach(function (m) { names[m.name] = m; });
      box.querySelector(".lc-crew-members").innerHTML = ms.map(function (m) {
        return "<span class='lc-crew-member' title='" + esc(m.brief) + "'>" + (ICON[m.kind] || "❔") + " " + esc(m.name) +
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
      var inbox = rowsOf(inboxId), out = [], log = [], asks = 0, n = 0;
      var say = function (who, kind, said, heard) { log.push({ n: ++n, who: who, kind: kind, in: said, out: heard }); window.lcSetDataset(id + ".log", log.slice()); };
      btn.disabled = true; box.setAttribute("data-state", "running");
      var step = function (i) {
        if (i >= inbox.length) {
          box.setAttribute("data-state", "done");
          status.textContent = "✓ " + out.length + " sorted, " + asks + " of " + budget + " AI asks";
          btn.disabled = false;
          return Promise.resolve();
        }
        var row = inbox[i], text = String(row[textCol] == null ? "" : row[textCol]);
        var lane = null, tried = 0, note = "";
        var who = row.family || row.name || ("#" + (i + 1));
        status.textContent = "… " + who;
        var byRules = rules.reduce(function (p, m) {
          return p.then(function () {
            if (lane) return;
            return rule(String(m.brief || "").trim(), text).then(function (r) {
              say(m.name, "rules", text, r.error ? "⚠️ " + r.error : (r.lane || "—"));
              var l = laneIn(r.lane, lanes); if (l) lane = l;
            });
          });
        }, Promise.resolve());
        var loop = function () {
          if (lane || !reader || tried >= tries || asks >= budget) return Promise.resolve();
          tried++;
          status.textContent = "… " + who + ": " + reader.name + " reads";
          var context = reader.reads ? "\n\nWhat you know:\n" + JSON.stringify(rowsOf(reader.reads)) : "";
          asks++; box.setAttribute("data-asks", String(asks));
          return ask(reader, text + note + context).then(function (a) {
            say(reader.name, "reader", text + note, a.error ? "⚠️ " + a.error : a.text);
            var verdict = laneIn(a.text, lanes);
            if (!verdict) return a.error ? null : loop();
            var checker = reader.checked_by ? byName[reader.checked_by] : null;
            if (!checker) { lane = verdict; return null; }
            if (asks >= budget) return null;
            status.textContent = "… " + who + ": " + checker.name + " checks " + verdict;
            var cctx = checker.reads ? "\n\nWhat you know:\n" + JSON.stringify(rowsOf(checker.reads)) : "";
            asks++; box.setAttribute("data-asks", String(asks));
            return ask(checker, "The message: " + text + "\nThe verdict: " + verdict + cctx).then(function (c) {
              say(checker.name, "checker", verdict, c.error ? "⚠️ " + c.error : c.text);
              if (c.error) return null;
              if (disagrees(c.text)) { note = "\n\n" + checker.name + " disagreed with " + verdict + ": " + c.text; return loop(); }
              lane = verdict;
              return null;
            });
          });
        };
        return byRules.then(loop).then(function () {
          out.push(Object.assign({}, row, { lane: lane || fallback, tries: tried }));
          window.lcSetDataset(id + ".sorted", out.slice());
          return step(i + 1);
        });
      };
      status.textContent = "…";
      step(0).catch(function (e) { status.textContent = "⚠️ " + (e && e.message || e); btn.disabled = false; box.setAttribute("data-state", "done"); });
    });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.crew", upgrade);
})();
</script>
