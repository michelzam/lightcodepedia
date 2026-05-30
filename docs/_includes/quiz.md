{%- comment -%}
Quiz widget.

Single-choice (immediate feedback, click again to retry):
  - Bolds the text
  - Starts a new slide
  - Makes text smaller
  {: .quiz correct="2" }

`[x]` / `[ ]` GitHub-style task-list syntax works as sugar for `correct=`:
  - [ ] Bolds the text
  - [x] Starts a new slide
  - [ ] Makes text smaller
  {: .quiz }

Multi-select (toggle options, hit Check to grade) — square boxes signal multi:
  - [ ] Apples
  - [x] Carrots
  - [ ] Steak
  - [x] Spinach
  {: .quiz multi="true" }

Per-option explanation: nest a blockquote under each option (kramdown
requires blank lines around it). Shown only after the option is graded.
  - First option

    > Wrong because foo.

  - Second option

    > Right because bar.
  {: .quiz correct="2" }

Quizzes report their state to window.lcQuizScore (see _includes/score.md).
Auto-included by docs/_layouts/default.html on every page.
{%- endcomment -%}

<style>
ul.lc-quiz, ol.lc-quiz { background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.5em 0.4em; margin: 1em 0; list-style: none; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.lc-quiz li { display: block; padding: 0.55em 0.85em 0.55em 2.2em; margin: 0.15em 0; border-radius: 6px; border: 1px solid transparent; cursor: pointer; position: relative; transition: background 0.15s, border-color 0.15s; line-height: 1.5; }
.lc-quiz li::before { content: "○"; position: absolute; left: 0.75em; top: 0.5em; color: #b0b6bf; font-weight: 600; font-size: 1.15em; line-height: 1.4; }
.lc-quiz li:hover { background: #f5f9ff; border-color: #d0e3f5; }
.lc-quiz li > p:first-child { margin: 0; }
.lc-quiz li > p:not(:first-child) { margin: 0.3em 0 0; }

/* single-choice = radio look (default) */
.lc-quiz li.lc-quiz-selected:not(.lc-quiz-correct):not(.lc-quiz-wrong) { background: #f5f9ff; border-color: #d0e3f5; }
.lc-quiz li.lc-quiz-selected:not(.lc-quiz-correct):not(.lc-quiz-wrong)::before { content: "●"; color: #0066cc; }

/* multi-select = checkbox look */
ul.lc-quiz[multi="true"] li::before, ol.lc-quiz[multi="true"] li::before { content: "☐"; font-size: 1.05em; }
ul.lc-quiz[multi="true"] li.lc-quiz-selected:not(.lc-quiz-correct):not(.lc-quiz-wrong)::before,
ol.lc-quiz[multi="true"] li.lc-quiz-selected:not(.lc-quiz-correct):not(.lc-quiz-wrong)::before { content: "☑"; color: #0066cc; }

/* graded states (both modes) */
.lc-quiz li.lc-quiz-correct { background: #e8f5e9; border-color: #4caf50; }
.lc-quiz li.lc-quiz-correct::before { content: "✓"; color: #2e7d32; }
.lc-quiz li.lc-quiz-wrong { background: #ffebee; border-color: #ef5350; }
.lc-quiz li.lc-quiz-wrong::before { content: "✗"; color: #c62828; }

/* explanation blockquote inside an option */
.lc-quiz li > blockquote { display: none; margin: 0.5em 0 0; padding: 0.4em 0.8em; border-left: 3px solid #0066cc; background: rgba(245, 249, 255, 0.85); font-size: 0.88em; color: #444; font-style: italic; border-radius: 0 4px 4px 0; }
.lc-quiz li > blockquote p { margin: 0; }
.lc-quiz li.lc-quiz-correct > blockquote { display: block; border-left-color: #2e7d32; background: rgba(232, 245, 233, 0.6); color: #2e7d32; }
.lc-quiz li.lc-quiz-wrong > blockquote { display: block; border-left-color: #c62828; background: rgba(255, 235, 238, 0.6); color: #b00020; }

.lc-quiz-bar { display: flex; align-items: center; gap: 0.7em; margin: 0.5em 0 1em; padding: 0 0.4em; flex-wrap: wrap; }
.lc-quiz-check { background: #0066cc; color: white; border: none; padding: 0.45em 1.2em; border-radius: 4px; cursor: pointer; font-size: 0.88em; font-weight: 500; transition: background 0.12s; }
.lc-quiz-check:hover { background: #0052a3; }
.lc-quiz-check:disabled { background: #ccc; cursor: not-allowed; }
.lc-quiz-status { font-size: 0.88em; color: #666; }
.lc-quiz-status.lc-quiz-status-correct { color: #2e7d32; font-weight: 500; }
.lc-quiz-status.lc-quiz-status-pending { color: #c62828; }
</style>
<script>
(function(){
  function parseIndices(str) {
    return (str || '').split(',').map(function(s){
      return parseInt(s.trim(), 10) - 1;
    }).filter(function(n){ return !isNaN(n) && n >= 0; });
  }

  function reportScore(quizId, correct) {
    if (window.lcQuizScore && window.lcQuizScore.update) {
      window.lcQuizScore.update(quizId, correct);
    }
  }

  var QUIZ_SEQ = 0;

  function upgradeQuiz(el) {
    if (el.dataset.lcQuizUpgraded) return;
    el.dataset.lcQuizUpgraded = '1';
    el.classList.add('lc-quiz');

    var quizId = el.id || ('quiz-' + (++QUIZ_SEQ));
    el.dataset.lcQuizId = quizId;
    var multi = el.getAttribute('multi') === 'true';
    var correctSet = {};

    var items = Array.prototype.slice.call(el.children).filter(function(c){
      return c.tagName === 'LI';
    });

    // [x] / [ ] syntax detection: GFM-rendered <input> OR default-kramdown literal text
    var bracketSeen = false;
    items.forEach(function(li, idx){
      var cb = li.querySelector('input.task-list-item-checkbox, input[type="checkbox"]');
      if (cb) {
        bracketSeen = true;
        if (cb.checked) correctSet[idx] = true;
        cb.parentNode.removeChild(cb);
        li.classList.remove('task-list-item');
        return;
      }
      var firstP = li.querySelector('p');
      var node = firstP ? firstP.firstChild : li.firstChild;
      if (node && node.nodeType === 3) {
        var m = node.textContent.match(/^\s*\[([ xX])\]\s+/);
        if (m) {
          bracketSeen = true;
          if (m[1].toLowerCase() === 'x') correctSet[idx] = true;
          node.textContent = node.textContent.replace(/^\s*\[[ xX]\]\s+/, '');
        }
      }
    });

    // Fall back to correct="N,M,..." if no [x] markers found
    if (!bracketSeen) {
      parseIndices(el.getAttribute('correct')).forEach(function(i){
        correctSet[i] = true;
      });
    }
    el.classList.remove('task-list');

    var selected = {};

    function gradeAndReport(allCorrect) {
      reportScore(quizId, allCorrect);
    }

    if (multi) {
      var bar = document.createElement('div');
      bar.className = 'lc-quiz-bar';
      var checkBtn = document.createElement('button');
      checkBtn.className = 'lc-quiz-check';
      checkBtn.type = 'button';
      checkBtn.textContent = 'Check';
      var status = document.createElement('span');
      status.className = 'lc-quiz-status';
      bar.appendChild(checkBtn);
      bar.appendChild(status);
      el.parentNode.insertBefore(bar, el.nextSibling);

      items.forEach(function(li, i){
        li.addEventListener('click', function(e){
          e.stopPropagation();
          if (li.classList.contains('lc-quiz-correct') || li.classList.contains('lc-quiz-wrong')) {
            items.forEach(function(o){ o.classList.remove('lc-quiz-correct', 'lc-quiz-wrong'); });
          }
          if (selected[i]) {
            delete selected[i];
            li.classList.remove('lc-quiz-selected');
          } else {
            selected[i] = true;
            li.classList.add('lc-quiz-selected');
          }
          status.textContent = '';
          status.className = 'lc-quiz-status';
        });
      });

      checkBtn.addEventListener('click', function(){
        var allMatch = true;
        var anyCorrectExists = Object.keys(correctSet).length > 0;
        items.forEach(function(li, i){
          var isCorrect = !!correctSet[i];
          var isSelected = !!selected[i];
          li.classList.remove('lc-quiz-selected', 'lc-quiz-correct', 'lc-quiz-wrong');
          if (isCorrect && isSelected) {
            li.classList.add('lc-quiz-correct');
          } else if (isCorrect && !isSelected) {
            // Treasure-hunt: don't reveal missed correct answers
            allMatch = false;
          } else if (!isCorrect && isSelected) {
            li.classList.add('lc-quiz-wrong');
            allMatch = false;
          }
        });
        if (allMatch && anyCorrectExists) {
          status.textContent = '✓ All correct';
          status.className = 'lc-quiz-status lc-quiz-status-correct';
        } else {
          status.textContent = 'Not quite — adjust your picks and try again.';
          status.className = 'lc-quiz-status lc-quiz-status-pending';
        }
        gradeAndReport(allMatch && anyCorrectExists);
      });
    } else {
      items.forEach(function(li, i){
        li.addEventListener('click', function(e){
          e.stopPropagation();
          items.forEach(function(o){
            o.classList.remove('lc-quiz-correct', 'lc-quiz-wrong', 'lc-quiz-selected');
          });
          var hit = !!correctSet[i];
          if (hit) {
            li.classList.add('lc-quiz-correct');
          } else {
            // Treasure-hunt: only the clicked wrong answer is revealed;
            // the correct one stays hidden until the student finds it.
            li.classList.add('lc-quiz-wrong');
          }
          gradeAndReport(hit);
        });
      });
    }
  }

  function init() {
    Array.prototype.forEach.call(
      document.querySelectorAll('ul.quiz, ol.quiz'),
      upgradeQuiz
    );
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(init, 0); });
  } else {
    setTimeout(init, 0);
  }
})();
</script>
