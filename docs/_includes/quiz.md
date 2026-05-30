{%- comment -%}
Quiz widget — turns a kramdown bullet list into an interactive
single-choice or multi-select question via a `{: .quiz correct="N" }`
IAL on the list.

Single-choice (immediate feedback, click again to retry):
  - Bolds the text
  - Starts a new slide
  - Makes text smaller
  {: .quiz correct="2" }

Multi-select (toggle options, hit Check to grade):
  - Apples
  - Carrots
  - Steak
  - Spinach
  {: .quiz multi="true" correct="2,4" }

The `correct=` attribute is 1-indexed and comma-separated. Auto-included
by docs/_layouts/default.html on every page.
{%- endcomment -%}

<style>
ul.lc-quiz, ol.lc-quiz { background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.5em 0.4em; margin: 1em 0; list-style: none; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.lc-quiz li { display: block; padding: 0.55em 0.85em 0.55em 2.2em; margin: 0.15em 0; border-radius: 6px; border: 1px solid transparent; cursor: pointer; position: relative; transition: background 0.15s, border-color 0.15s; line-height: 1.5; }
.lc-quiz li::before { content: "○"; position: absolute; left: 0.75em; top: 0.5em; color: #b0b6bf; font-weight: 600; font-size: 1.15em; line-height: 1.4; }
.lc-quiz li:hover { background: #f5f9ff; border-color: #d0e3f5; }
.lc-quiz li.lc-quiz-selected:not(.lc-quiz-correct):not(.lc-quiz-wrong) { background: #f5f9ff; border-color: #d0e3f5; }
.lc-quiz li.lc-quiz-selected:not(.lc-quiz-correct):not(.lc-quiz-wrong)::before { content: "●"; color: #0066cc; }
.lc-quiz li.lc-quiz-correct { background: #e8f5e9; border-color: #4caf50; }
.lc-quiz li.lc-quiz-correct::before { content: "✓"; color: #2e7d32; }
.lc-quiz li.lc-quiz-wrong { background: #ffebee; border-color: #ef5350; }
.lc-quiz li.lc-quiz-wrong::before { content: "✗"; color: #c62828; }
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

  function upgradeQuiz(el) {
    if (el.dataset.lcQuizUpgraded) return;
    el.dataset.lcQuizUpgraded = '1';
    el.classList.add('lc-quiz');

    var multi = el.getAttribute('multi') === 'true';
    var correctIdx = parseIndices(el.getAttribute('correct'));
    var correctSet = {};
    correctIdx.forEach(function(i){ correctSet[i] = true; });

    var items = Array.prototype.slice.call(el.children).filter(function(c){
      return c.tagName === 'LI';
    });

    var selected = {};

    function clearAll() {
      items.forEach(function(li){
        li.classList.remove('lc-quiz-correct', 'lc-quiz-wrong', 'lc-quiz-selected');
      });
      selected = {};
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
        items.forEach(function(li, i){
          var isCorrect = !!correctSet[i];
          var isSelected = !!selected[i];
          li.classList.remove('lc-quiz-selected');
          if (isCorrect && isSelected) {
            li.classList.add('lc-quiz-correct');
          } else if (isCorrect && !isSelected) {
            li.classList.add('lc-quiz-wrong');
            allMatch = false;
          } else if (!isCorrect && isSelected) {
            li.classList.add('lc-quiz-wrong');
            allMatch = false;
          } else {
            li.classList.remove('lc-quiz-correct', 'lc-quiz-wrong');
          }
        });
        if (allMatch && correctIdx.length > 0) {
          status.textContent = '✓ All correct';
          status.className = 'lc-quiz-status lc-quiz-status-correct';
        } else {
          status.textContent = 'Not quite — adjust your picks and try again.';
          status.className = 'lc-quiz-status lc-quiz-status-pending';
        }
      });
    } else {
      items.forEach(function(li, i){
        li.addEventListener('click', function(e){
          e.stopPropagation();
          clearAll();
          if (correctSet[i]) {
            li.classList.add('lc-quiz-correct');
          } else {
            li.classList.add('lc-quiz-wrong');
            for (var j = 0; j < items.length; j++) {
              if (correctSet[j]) { items[j].classList.add('lc-quiz-correct'); break; }
            }
          }
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
