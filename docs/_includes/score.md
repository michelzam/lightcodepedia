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
.lc-score-fab { position: fixed; bottom: 5em; right: 1.2em; height: 40px; min-width: 56px; padding: 0 14px; border-radius: 20px; background: white; color: #b45309; border: 1px solid #f0c97a; display: none; align-items: center; gap: 0.4em; text-decoration: none; font-size: 0.86em; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.08); cursor: pointer; transition: background 0.15s, border-color 0.15s, box-shadow 0.15s, transform 0.15s; z-index: 999; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-score-fab.lc-score-visible { display: inline-flex; }
.lc-score-fab:hover { background: #fff8e1; border-color: #b45309; box-shadow: 0 4px 14px rgba(180, 83, 9, 0.18); transform: translateY(-1px); }
.lc-embed-mode .lc-score-fab { display: none !important; }
@media (max-width: 700px) { .lc-score-fab { bottom: 4.4em; right: 0.8em; } }

.lc-score-popover { position: fixed; bottom: 8em; right: 1.2em; background: white; border: 1px solid #f0c97a; border-radius: 8px; padding: 0.8em 1em; box-shadow: 0 6px 20px rgba(0,0,0,0.14); z-index: 1000; min-width: 200px; max-width: 280px; display: none; font-size: 0.85em; }
.lc-score-popover.lc-score-popover-visible { display: block; }
.lc-score-popover h4 { margin: 0 0 0.4em; font-size: 0.9em; color: #b45309; font-weight: 600; }
.lc-score-popover .lc-score-line { display: flex; justify-content: space-between; gap: 0.6em; padding: 0.2em 0; color: #555; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; }
.lc-score-popover .lc-score-line .lc-score-mark { font-weight: 700; }
.lc-score-popover .lc-score-line .lc-score-mark.ok { color: #2e7d32; }
.lc-score-popover .lc-score-line .lc-score-mark.no { color: #c62828; }
.lc-score-popover .lc-score-total { margin-top: 0.5em; padding-top: 0.5em; border-top: 1px solid #f0c97a; font-weight: 600; color: #b45309; display: flex; justify-content: space-between; }
@media (max-width: 700px) { .lc-score-popover { right: 0.8em; bottom: 7em; } }
</style>
<button class="lc-score-fab" type="button" aria-label="Show quiz score">
  <span class="lc-score-fab-icon" aria-hidden="true">🏆</span><span class="lc-score-fab-label">0/0</span>
</button>
<div class="lc-score-popover" role="status" aria-live="polite"></div>
<script>
(function(){
  window.lcQuizScore = window.lcQuizScore || (function(){
    var quizzes = {};  // {id: {correct: bool, attempts: N}}
    var order = [];
    var subscribers = [];

    function fab(){ return document.querySelector('.lc-score-fab'); }
    function pop(){ return document.querySelector('.lc-score-popover'); }
    function notify(){
      subscribers.forEach(function(cb){ try { cb(quizzes); } catch (e) {} });
    }

    function render() {
      var f = fab(); if (!f) return;
      var total = order.length;
      if (total === 0) {
        f.classList.remove('lc-score-visible');
        return;
      }
      var won = order.filter(function(id){ return quizzes[id].correct; }).length;
      f.querySelector('.lc-score-fab-label').textContent = won + '/' + total;
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
        render();
        renderPopover();
        notify();
      },
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
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
