{%- comment -%}
Homework — record karma across a reel/page set and hand it in.

A student opens a page (often the first of a reel) carrying a param chain:

  ?homework_number=6a&student_id=93629601&submit_info=<destination>

This include then:
  • remembers the homework session in localStorage, so the params only need to
    be on the FIRST page — every later page (reached by reel/sticky links)
    keeps recording without the params in its URL;
  • records every quiz/runner result (via window.lcQuizScore — see score.md)
    into a per-homework, per-page, timestamped karma log in localStorage;
  • shows a homework pill with the running score, a details popover, and a
    Submit button;
  • on Submit, POSTs { the original param chain + the karma } to submit_info.

Trust + reach (be honest about it):
  • localStorage is student-editable, so scores are HONOUR-SYSTEM unless the
    destination server re-verifies them. Volume is a non-issue — score records
    are bytes each and localStorage holds ~5–10 MB.
  • submit_info comes from the URL, so in PRODUCTION it should be a fixed /
    whitelisted endpoint, not a free param (an open POST target is a data-exfil
    smell). Submit always shows the destination and asks for confirmation.
  • A plain browser POST only reaches endpoints that accept CORS JSON (Google
    Apps Script web app, Formspree, a serverless function) or mailto:. Real LMS
    APIs (Canvas, etc.) need a server-side proxy for OAuth + CORS — the POST
    here falls back to Copy / Download when it can't reach the destination.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-hw-pill { position: fixed; bottom: 1em; left: 50%; transform: translateX(-50%);
  z-index: 1002; display: none; align-items: center; gap: 0.55em;
  background: #fffdf5; border: 1px solid #e8d6a0; border-radius: 22px;
  padding: 0.35em 0.5em 0.35em 0.95em; box-shadow: 0 2px 12px rgba(0,0,0,0.12);
  font-size: 0.86em; color: #7a5a12; max-width: calc(100vw - 2em); box-sizing: border-box; }
.lc-hw-pill.lc-hw-on { display: inline-flex; }
.lc-hw-label { font-weight: 600; white-space: nowrap; cursor: pointer; }
.lc-hw-score { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-hw-submit { border: none; background: #b45309; color: white; border-radius: 16px;
  padding: 0.34em 0.95em; font-size: 0.92em; font-weight: 600; cursor: pointer; }
.lc-hw-submit:hover { background: #92400e; }
.lc-hw-submit:disabled { background: #cbb994; cursor: default; }
.lc-hw-pop { position: fixed; bottom: 3.5em; left: 50%; transform: translateX(-50%);
  z-index: 1002; display: none; background: white; border: 1px solid #e8d6a0;
  border-radius: 10px; box-shadow: 0 8px 26px rgba(0,0,0,0.16); padding: 0.85em 1em;
  width: min(360px, calc(100vw - 2em)); font-size: 0.85em; color: #444; box-sizing: border-box; }
.lc-hw-pop.lc-hw-pop-on { display: block; }
.lc-hw-pop h4 { margin: 0 0 0.45em; color: #b45309; font-size: 0.95em; }
.lc-hw-row { display: flex; justify-content: space-between; gap: 0.6em; padding: 0.15em 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82em; }
.lc-hw-actions { margin-top: 0.65em; display: flex; gap: 0.9em; flex-wrap: wrap; }
.lc-hw-actions a { color: #0066cc; cursor: pointer; text-decoration: none; font-weight: 500; }
.lc-hw-actions a:hover { text-decoration: underline; }
.lc-hw-status { margin-top: 0.5em; font-size: 0.82em; color: #2e7d32; }
body.lc-slides-active .lc-hw-pill { bottom: 4em; }
.lc-embed-mode .lc-hw-pill, .lc-embed-mode .lc-hw-pop { display: none !important; }
</style>
<div class="lc-hw-pill" role="status" aria-live="polite">
  <span class="lc-hw-label">📋 <span class="lc-hw-num"></span> · <span class="lc-hw-score">0/0</span></span>
  <button class="lc-hw-submit" type="button">Submit</button>
</div>
<div class="lc-hw-pop" role="dialog" aria-label="Homework details"></div>
<script>
(function(){
  var sp = new URLSearchParams(location.search);
  var active = null;
  try { active = JSON.parse(localStorage.getItem('lc_hw_active') || 'null'); } catch (e) {}
  var hwNum = sp.get('homework_number'), sid = sp.get('student_id');
  if (hwNum && sid) {
    active = {
      homework_number: hwNum, student_id: sid,
      submit_info: sp.get('submit_info') || (active && active.submit_info) || '',
      param_chain: location.search.replace(/^\?/, ''),
      key: 'hw:' + hwNum + ':' + sid
    };
    try { localStorage.setItem('lc_hw_active', JSON.stringify(active)); } catch (e) {}
  }
  if (!active) return;   // not a homework session — zero overhead on normal pages

  var KEY = 'lc_hw_rec:' + active.key;
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(rec)); } catch (e) {} }
  var rec = load() || {
    homework_number: active.homework_number, student_id: active.student_id,
    submit_info: active.submit_info, param_chain: active.param_chain,
    started: new Date().toISOString(), pages: {}, events: []
  };
  if (active.submit_info) rec.submit_info = active.submit_info;     // refresh from latest link
  if (active.param_chain) rec.param_chain = active.param_chain;

  var pagePath = location.pathname;
  function now() { return new Date().toISOString(); }

  // record the current page's quiz state (from lcQuizScore) into the karma log
  function record(quizzes) {
    var ids = Object.keys(quizzes || {});
    var p = rec.pages[pagePath] || { quizzes: {} };
    var won = 0;
    ids.forEach(function(id){
      var q = quizzes[id], prev = p.quizzes[id];
      if (!prev || prev.correct !== !!q.correct || prev.attempts !== q.attempts) {
        rec.events.push({ ts: now(), page: pagePath, quiz: id, correct: !!q.correct, attempts: q.attempts });
        if (rec.events.length > 600) rec.events = rec.events.slice(-600);
      }
      p.quizzes[id] = { correct: !!q.correct, attempts: q.attempts, last: now() };
      if (q.correct) won++;
    });
    p.score = won; p.total = ids.length; p.last = now();
    rec.pages[pagePath] = p;
    save();
    render();
  }

  function totals() {
    var won = 0, tot = 0;
    for (var p in rec.pages) { if (!rec.pages.hasOwnProperty(p)) continue; won += rec.pages[p].score || 0; tot += rec.pages[p].total || 0; }
    return { won: won, tot: tot };
  }

  var pill = document.querySelector('.lc-hw-pill');
  var pop = document.querySelector('.lc-hw-pop');

  function render() {
    if (!pill) return;
    pill.querySelector('.lc-hw-num').textContent = rec.homework_number + ' · ' + rec.student_id;
    var t = totals();
    pill.querySelector('.lc-hw-score').textContent = t.won + '/' + t.tot;
    pill.classList.add('lc-hw-on');
    if (pop && pop.classList.contains('lc-hw-pop-on')) renderPop();
  }

  function renderPop() {
    if (!pop) return;
    var t = totals(), rows = '';
    for (var p in rec.pages) {
      if (!rec.pages.hasOwnProperty(p)) continue;
      var pg = rec.pages[p];
      rows += '<div class="lc-hw-row"><span>' + p + '</span><span>' + (pg.score || 0) + '/' + (pg.total || 0) +
        '<span style="color:#9a9a9a"> · ' + String(pg.last || '').slice(0, 16).replace('T', ' ') + '</span></span></div>';
    }
    pop.innerHTML = '<h4>Homework ' + rec.homework_number + ' — ' + rec.student_id + '</h4>' +
      (rows || '<div style="color:#999">No graded items yet.</div>') +
      '<div class="lc-hw-row" style="font-weight:600;color:#b45309;border-top:1px solid #eee;margin-top:.4em;padding-top:.4em"><span>Total</span><span>' + t.won + '/' + t.tot + '</span></div>' +
      '<div class="lc-hw-actions"><a data-hw="copy">Copy results</a><a data-hw="download">Download JSON</a><a data-hw="end" style="color:#c62828">End session</a></div>' +
      (rec.submitted_at ? '<div class="lc-hw-status">✓ Submitted ' + String(rec.submitted_at).slice(0, 16).replace('T', ' ') + '</div>' : '');
  }

  function payload() {
    var t = totals();
    return {
      homework_number: rec.homework_number, student_id: rec.student_id,
      param_chain: rec.param_chain, started: rec.started, submitted_at: now(),
      score: t.won + '/' + t.tot, pages: rec.pages, events: rec.events
    };
  }
  function asText() { return JSON.stringify(payload(), null, 2); }
  function copy() {
    var s = asText();
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(s).catch(function(){});
    else { try { var ta = document.createElement('textarea'); ta.value = s; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); } catch (e) {} }
  }
  function download() {
    try {
      var blob = new Blob([asText()], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'homework-' + rec.homework_number + '-' + rec.student_id + '.json';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
    } catch (e) {}
  }
  function markSubmitted() { rec.submitted_at = now(); save(); render(); }

  function submit() {
    var dest = rec.submit_info, data = payload();
    if (!dest) { openPop(); alert('No submit_info destination set — use Copy or Download to hand in your results.'); return; }
    if (!confirm('Submit homework ' + rec.homework_number + ' for student ' + rec.student_id + '\nto: ' + dest + ' ?')) return;
    if (/^mailto:/i.test(dest)) {
      var t = totals();
      var sub = 'Homework ' + rec.homework_number + ' — ' + rec.student_id + ' (' + t.won + '/' + t.tot + ')';
      var body = 'Homework: ' + rec.homework_number + '\nStudent: ' + rec.student_id + '\nScore: ' + t.won + '/' + t.tot + '\n\n' + asText().slice(0, 1500);
      location.href = dest + (dest.indexOf('?') >= 0 ? '&' : '?') + 'subject=' + encodeURIComponent(sub) + '&body=' + encodeURIComponent(body);
      markSubmitted(); return;
    }
    var btn = pill && pill.querySelector('.lc-hw-submit');
    if (btn) { btn.disabled = true; btn.textContent = 'Submitting…'; }
    fetch(dest, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function(r){ if (!r.ok) throw new Error('HTTP ' + r.status); markSubmitted(); if (btn) btn.textContent = '✓ Sent'; })
      .catch(function(e){
        if (btn) { btn.disabled = false; btn.textContent = 'Submit'; }
        openPop();
        alert('Could not POST to the destination (' + (e.message || e) + ').\nCross-origin and LMS endpoints usually need a server-side proxy. ' +
              'Use Copy or Download to hand in your results instead.');
      });
  }

  function openPop() { if (pop) { renderPop(); pop.classList.add('lc-hw-pop-on'); } }
  function closePop() { if (pop) pop.classList.remove('lc-hw-pop-on'); }

  if (pill) {
    pill.querySelector('.lc-hw-submit').addEventListener('click', function(e){ e.stopPropagation(); submit(); });
    pill.querySelector('.lc-hw-label').addEventListener('click', function(e){ e.stopPropagation(); pop && (pop.classList.contains('lc-hw-pop-on') ? closePop() : openPop()); });
  }
  if (pop) pop.addEventListener('click', function(e){
    var a = e.target.closest('a[data-hw]'); if (!a) return;
    var act = a.getAttribute('data-hw');
    if (act === 'copy') copy();
    else if (act === 'download') download();
    else if (act === 'end') {
      if (confirm('End this homework session on this device? Your recorded results stay in your browser.')) {
        try { localStorage.removeItem('lc_hw_active'); } catch (e) {}
        if (pill) pill.classList.remove('lc-hw-on');
        closePop();
      }
    }
  });
  document.addEventListener('click', function(e){ if (pop && pill && !pill.contains(e.target) && !pop.contains(e.target)) closePop(); });

  // hook the per-page score system (score.md), retrying until it is present
  function hook() { if (window.lcQuizScore && window.lcQuizScore.subscribe) { window.lcQuizScore.subscribe(record); return true; } return false; }
  if (!hook()) { var n = 0, iv = setInterval(function(){ if (hook() || ++n > 50) clearInterval(iv); }, 200); }

  // expose for scripting / tests
  window.lcHomework = { payload: payload, totals: totals, submit: submit, record: function(q){ record(q); } };

  render();
})();
</script>
