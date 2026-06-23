{%- comment -%}
Session-only quiz score tracker.

A 🏆 FAB appears at the bottom-right (above the ✏️ pencil) once any
quiz on the page has been answered. The label shows "correct/attempted"
for the current session. Tap/click opens a small popover with a per-quiz
breakdown. No persistence — refresh clears the score.

Quiz widgets report via window.lcQuizScore.update(quizId, correct).
Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-score-fab { position: fixed; top: 56px; right: 1.2em; height: 40px; min-width: 56px; padding: 0 14px; border-radius: 20px; background: white; color: #b45309; border: 1px solid #f0c97a; display: none; align-items: center; gap: 0.4em; text-decoration: none; font-size: 0.86em; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.08); cursor: pointer; transition: background 0.15s, border-color 0.15s, box-shadow 0.15s, transform 0.15s; z-index: 999; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-score-fab.lc-score-visible { display: inline-flex; }
.lc-score-fab:hover { background: #fff8e1; border-color: #b45309; box-shadow: 0 4px 14px rgba(180, 83, 9, 0.18); transform: translateY(-1px); }
body.lc-slides-active .lc-score-fab { top: 1em; }
.lc-embed-mode .lc-score-fab { display: none !important; }
@media (max-width: 700px) { .lc-score-fab { top: 56px; right: 0.8em; } body.lc-slides-active .lc-score-fab { top: 0.6em; } }

.lc-score-popover { position: fixed; top: 104px; right: 1.2em; background: white; border: 1px solid #f0c97a; border-radius: 8px; padding: 0.8em 1em; box-shadow: 0 6px 20px rgba(0,0,0,0.14); z-index: 1000; min-width: 200px; max-width: 280px; display: none; font-size: 0.85em; }
.lc-score-popover.lc-score-popover-visible { display: block; }
body.lc-slides-active .lc-score-popover { top: 3.4em; }
.lc-score-popover h4 { margin: 0 0 0.4em; font-size: 0.9em; color: #b45309; font-weight: 600; }
.lc-score-popover .lc-score-line { display: flex; justify-content: space-between; gap: 0.6em; padding: 0.2em 0; color: #555; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; }
.lc-score-popover .lc-score-line .lc-score-mark { font-weight: 700; }
.lc-score-popover .lc-score-line .lc-score-mark.ok { color: #2e7d32; }
.lc-score-popover .lc-score-line .lc-score-mark.no { color: #c62828; }
.lc-score-popover .lc-score-total { margin-top: 0.5em; padding-top: 0.5em; border-top: 1px solid #f0c97a; font-weight: 600; color: #b45309; display: flex; justify-content: space-between; }
@media (max-width: 700px) { .lc-score-popover { right: 0.8em; top: 100px; } body.lc-slides-active .lc-score-popover { top: 3em; } }
/* a score remembered from a previous visit (no live answers yet this session) */
.lc-score-fab.lc-score-remembered { opacity: 0.9; }
/* per-page score tag in the corner of a card that links to that page */
.lc-card { position: relative; }
.lc-card-score { position: absolute; top: 8px; right: 8px; z-index: 1;
  font: 600 0.72em/1.4 ui-monospace, SFMono-Regular, Menlo, monospace;
  padding: 0.12em 0.5em; border-radius: 999px; background: #eef2f7; color: #64748b;
  pointer-events: none; }
.lc-card-score.partial { background: #fef9c3; color: #854d0e; }
.lc-card-score.full { background: #dcfce7; color: #166534; }
/* gray "remaining" = quizzes on the page you have not answered yet */
.lc-score-fab-remaining { color: #9ca3af; font-weight: 600; }
.lc-score-fab-remaining:empty { display: none; }
.lc-card-rem { color: #9ca3af; font-weight: 600; margin-left: 0.15em; }
</style>
<button class="lc-score-fab" type="button" aria-label="Show quiz score">
  <span class="lc-score-fab-icon" aria-hidden="true">🏆</span><span class="lc-score-fab-label">0/0</span><span class="lc-score-fab-remaining"></span>
</button>
<div class="lc-score-popover" role="status" aria-live="polite"></div>
<script>
(function(){
  /* ── persisted per-page scores (localStorage) ──────────────────────────
     Keyed by a normalised path so /foo, /foo.html and /foo/ all match. */
  function normPath(p){
    try { p = new URL(p || location.href, location.origin).pathname; }
    catch (e) { p = location.pathname; }
    p = p.replace(/index\.html?$/i, "").replace(/\.html?$/i, "");
    if (p.length > 1) p = p.replace(/\/+$/, "");
    return p || "/";
  }
  function loadScores(){ try { return JSON.parse(localStorage.getItem("lc_scores") || "{}"); } catch (e) { return {}; } }
  function saveScores(o){ try { localStorage.setItem("lc_scores", JSON.stringify(o)); } catch (e) {} }
  window.lcPageScores = { get: function(p){ return loadScores()[normPath(p)]; }, all: loadScores, norm: normPath };

  /* tag every card that links to a page you've scored with that score */
  function decorateCards(){
    var scores = loadScores();
    document.querySelectorAll(".lc-card").forEach(function(card){
      if (card.dataset.lcScored) return;
      var a = card.querySelector("a[href]"); if (!a) return;
      var s = scores[normPath(a.getAttribute("href"))];
      if (!s || !s.total) return;
      card.dataset.lcScored = "1";
      var tag = document.createElement("span");
      tag.className = "lc-card-score" + (s.won >= s.total ? " full" : (s.won > 0 ? " partial" : ""));
      var rem = Math.max(0, (s.quizzes || 0) - s.total);
      tag.innerHTML = s.won + "/" + s.total + (rem > 0 ? " <span class='lc-card-rem'>+" + rem + "</span>" : "");
      tag.title = "Your score on this page" + (rem > 0 ? " — " + rem + " quiz" + (rem > 1 ? "zes" : "") + " unanswered" : "");
      card.appendChild(tag);
    });
  }
  var _cardTick = false;
  function scheduleDecorate(){
    if (_cardTick) return; _cardTick = true;
    requestAnimationFrame(function(){ _cardTick = false; decorateCards(); });
  }

  window.lcQuizScore = window.lcQuizScore || (function(){
    var quizzes = {};  // {id: {correct: bool, attempts: N}}
    var order = [];
    var subscribers = [];
    var PATH = normPath();
    var seed = loadScores()[PATH] || null;   // score remembered from a previous visit

    function sessionWon(){ return order.filter(function(id){ return quizzes[id].correct; }).length; }
    function persist(){
      if (!order.length) return;            // nothing answered this visit — don't overwrite
      var all = loadScores(), prev = all[PATH] || { won: 0, total: 0 };
      // keep the best: never regress a remembered score on a partial re-visit
      all[PATH] = { won: Math.max(prev.won || 0, sessionWon()),
                    total: Math.max(prev.total || 0, order.length),
                    quizzes: Math.max(prev.quizzes || 0, document.querySelectorAll('.lc-quiz').length),
                    ts: new Date().toISOString() };
      seed = all[PATH];
      saveScores(all);
    }

    function fab(){ return document.querySelector('.lc-score-fab'); }
    function pop(){ return document.querySelector('.lc-score-popover'); }
    function notify(){
      subscribers.forEach(function(cb){ try { cb(quizzes); } catch (e) {} });
    }

    function render() {
      var f = fab(); if (!f) return;
      var sTotal = order.length, sWon = sessionWon();
      var total = sTotal, won = sWon, remembered = false;
      if (seed && seed.total) {
        if (sTotal === 0) { total = seed.total; won = seed.won; remembered = true; }  // show last visit's score
        else { won = Math.max(won, seed.won); total = Math.max(total, seed.total); }
      }
      if (total === 0) { f.classList.remove('lc-score-visible'); return; }
      f.querySelector('.lc-score-fab-label').textContent = won + '/' + total;
      /* gray count of quizzes on this page not yet answered */
      var quizCount = document.querySelectorAll('.lc-quiz').length;
      if (quizCount === 0 && seed && seed.quizzes) quizCount = seed.quizzes;
      var remaining = Math.max(0, quizCount - total);
      var remEl = f.querySelector('.lc-score-fab-remaining');
      if (remEl) {
        remEl.textContent = remaining > 0 ? ' +' + remaining : '';
        remEl.title = remaining > 0 ? remaining + ' quiz' + (remaining > 1 ? 'zes' : '') + ' not answered yet' : '';
      }
      f.classList.toggle('lc-score-remembered', remembered);
      f.classList.add('lc-score-visible');
    }

    function renderPopover() {
      var p = pop(); if (!p) return;
      var won = order.filter(function(id){ return quizzes[id].correct; }).length;
      var lines = order.map(function(id, i){
        var q = quizzes[id];
        var mark = q.correct ? '<span class="lc-score-mark ok">✓</span>' : '<span class="lc-score-mark no">✗</span>';
        var label = 'Q' + (i + 1);
        return '<div class="lc-score-line"><span>' + label + '</span>' + mark + '</div>';
      }).join('');
      p.innerHTML = '<h4>This session</h4>' + lines + '<div class="lc-score-total"><span>Score</span><span>' + won + '/' + order.length + '</span></div>';
    }

    return {
      update: function(quizId, correct) {
        if (!quizzes[quizId]) {
          order.push(quizId);
          quizzes[quizId] = { correct: false, attempts: 0 };
        }
        quizzes[quizId].correct = !!correct;
        quizzes[quizId].attempts++;
        persist();
        render();
        renderPopover();
        notify();
      },
      refresh: function(){ render(); },
      reset: function() {
        quizzes = {};
        order = [];
        render();
        renderPopover();
        var p = pop(); if (p) p.classList.remove('lc-score-popover-visible');
        notify();
      },
      get: function(quizId) { return quizzes[quizId]; },
      all: function() { return quizzes; },
      subscribe: function(cb) { subscribers.push(cb); }
    };
  })();

  function init() {
    var f = document.querySelector('.lc-score-fab');
    var p = document.querySelector('.lc-score-popover');
    if (!f || !p) return;
    f.addEventListener('click', function(e){
      e.stopPropagation();
      p.classList.toggle('lc-score-popover-visible');
    });
    document.addEventListener('click', function(e){
      if (!p.contains(e.target) && !f.contains(e.target)) {
        p.classList.remove('lc-score-popover-visible');
      }
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') p.classList.remove('lc-score-popover-visible');
    });
    // show a score remembered from a previous visit
    if (window.lcQuizScore && window.lcQuizScore.refresh) window.lcQuizScore.refresh();
    // tag cards now and as they upgrade (cards.md / sections.md render late)
    decorateCards();
    new MutationObserver(scheduleDecorate).observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
