{%- comment -%}
"Present as slides" floating button (bottom-left) + slides engine.

Auto-included by docs/_layouts/default.html on every page. Reads the
already-rendered markdown DOM and partitions it on <h2> boundaries —
no special syntax needed in the source. Bullets auto-fragment; any
element tagged `{: .fragment }` in kramdown also fragments. A list
tagged `{: .nofragments }` opts out of auto-fragmentation.

Skipped on the 404 page and pages with `no_slides: true` in front matter.
Hidden if the page has no h2 (no real deck).

Navigation: → / Space / click → next; ← → previous; Esc → exit;
1–9 → jump; F → fullscreen. ?slides URL parameter enters slide mode
on load.
{%- endcomment -%}

{% if page.no_slides != true and page.permalink != "/404.html" %}
<style>
.lc-slides-fab { position: fixed; bottom: 1.2em; left: 1.2em; height: 44px; min-width: 44px; padding: 0 14px; border-radius: 22px; background: white; color: #0066cc; border: 1px solid #d0e3f5; display: inline-flex; align-items: center; gap: 0; text-decoration: none; font-size: 0.88em; font-weight: 500; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: gap 0.18s ease, padding 0.18s ease, background 0.15s, border-color 0.15s, box-shadow 0.15s, transform 0.15s; z-index: 999; overflow: hidden; white-space: nowrap; cursor: pointer; }
.lc-slides-fab .lc-slides-fab-icon { font-size: 1.2em; line-height: 1; }
.lc-slides-fab .lc-slides-fab-label { max-width: 0; opacity: 0; transition: max-width 0.22s ease, opacity 0.18s ease 0.04s; overflow: hidden; }
.lc-slides-fab:hover { background: #f5f9ff; border-color: #0066cc; box-shadow: 0 4px 14px rgba(0,102,204,0.18); transform: translateY(-1px); gap: 0.45em; padding-right: 16px; }
.lc-slides-fab:hover .lc-slides-fab-label { max-width: 140px; opacity: 1; }
.lc-slides-fab:focus-visible { outline: 2px solid #0066cc; outline-offset: 2px; }
.lc-slides-fab[data-no-slides="true"] { display: none; }
.lc-embed-mode .lc-slides-fab { display: none !important; }
@media (max-width: 700px) { .lc-slides-fab { bottom: 0.8em; left: 0.8em; } }

.lc-slide { display: block; }
body:not(.lc-slides-active) .lc-slide-fragment { opacity: 1 !important; }

body.lc-slides-active { overflow: hidden; background: #fafbfc; padding-top: 0 !important; }
body.lc-slides-active #lc-topbar, body.lc-slides-active .lc-edit-fab { display: none !important; }
body.lc-slides-active .markdown-body { max-width: none; margin: 0; padding: 0; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
body.lc-slides-active .lc-slide { display: none; }
body.lc-slides-active .lc-slide[data-active="true"] { display: block; flex: 1; padding: 3.5em 5em; overflow-y: auto; max-width: 1200px; width: 100%; margin: 0 auto; box-sizing: border-box; animation: lcSlideIn 0.22s ease-out; }
@keyframes lcSlideIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
body.lc-slides-active .lc-slide h1 { font-size: 2.6em; border-bottom: 2px solid #0066cc; padding-bottom: 0.3em; margin: 0 0 0.6em; }
body.lc-slides-active .lc-slide h2 { font-size: 2em; border-bottom: 2px solid #0066cc; padding-bottom: 0.3em; margin: 0 0 0.6em; color: #222; }
body.lc-slides-active .lc-slide h3 { font-size: 1.4em; }
body.lc-slides-active .lc-slide p, body.lc-slides-active .lc-slide li { font-size: 1.15em; line-height: 1.7; }
body.lc-slides-active .lc-slide ul, body.lc-slides-active .lc-slide ol { padding-left: 1.4em; }
body.lc-slides-active .lc-slide-fragment { opacity: 0.18; transition: opacity 0.28s ease; }
body.lc-slides-active .lc-slide-fragment[data-revealed="true"] { opacity: 1; }
@media (max-width: 700px) {
  body.lc-slides-active .lc-slide[data-active="true"] { padding: 2em 1.2em; }
  body.lc-slides-active .lc-slide h1 { font-size: 1.9em; }
  body.lc-slides-active .lc-slide h2 { font-size: 1.5em; }
}

.lc-slides-counter { position: fixed; bottom: 1em; right: 1em; background: rgba(30,30,30,0.7); color: white; padding: 0.3em 0.85em; border-radius: 14px; font-size: 0.82em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; z-index: 1001; pointer-events: none; opacity: 0; transition: opacity 0.2s; }
body.lc-slides-active .lc-slides-counter { opacity: 1; }
</style>
<a class="lc-slides-fab" href="#" title="Present as slides" aria-label="Present as slides">
  <span class="lc-slides-fab-icon" aria-hidden="true">📽️</span><span class="lc-slides-fab-label">Present</span>
</a>
<div class="lc-slides-counter" role="status" aria-live="polite"></div>
<script>
(function(){
  function init() {
    var fab = document.querySelector('.lc-slides-fab');
    var counter = document.querySelector('.lc-slides-counter');
    var body = document.body;
    var main = document.querySelector('main.markdown-body');
    if (!fab || !main) return;

    var slides = [];
    var current = 0;
    var revealed = [];
    var WIDGET_SEL = '.lc-pyrun, .lc-pyrepl, .lc-datagrid, .lc-form, .ag-root-wrapper, .lc-tabs';

    function partition() {
      var children = Array.prototype.slice.call(main.children);
      var groups = [];
      var cur = [];
      groups.push(cur);
      children.forEach(function(el){
        if (el.tagName === 'H2') {
          cur = [el];
          groups.push(cur);
        } else {
          cur.push(el);
        }
      });
      main.innerHTML = '';
      groups.forEach(function(group, i){
        if (!group.length) return;
        var section = document.createElement('section');
        section.className = 'lc-slide';
        section.setAttribute('data-slide-index', i);
        group.forEach(function(el){ section.appendChild(el); });
        main.appendChild(section);
        slides.push(section);
        var bullets = section.querySelectorAll('li');
        Array.prototype.forEach.call(bullets, function(li){
          if (li.closest(WIDGET_SEL)) return;
          if (li.parentElement && li.parentElement.classList.contains('nofragments')) return;
          li.classList.add('lc-slide-fragment');
        });
        Array.prototype.forEach.call(section.querySelectorAll('.fragment'), function(el){
          el.classList.add('lc-slide-fragment');
        });
      });
      revealed = slides.map(function(){ return 0; });
    }

    function hasDeck() { return slides.length > 1; }

    function showSlide() {
      slides.forEach(function(s, i){
        s.setAttribute('data-active', i === current ? 'true' : 'false');
        var frags = s.querySelectorAll('.lc-slide-fragment');
        Array.prototype.forEach.call(frags, function(f, j){
          f.setAttribute('data-revealed', j < revealed[i] ? 'true' : 'false');
        });
      });
      counter.textContent = (current + 1) + ' / ' + slides.length;
    }

    function next() {
      var slide = slides[current];
      var frags = slide.querySelectorAll('.lc-slide-fragment');
      if (revealed[current] < frags.length) {
        revealed[current]++;
        showSlide();
      } else if (current < slides.length - 1) {
        current++;
        showSlide();
        slides[current].scrollTop = 0;
      }
    }

    function prev() {
      if (revealed[current] > 0) {
        revealed[current]--;
        showSlide();
      } else if (current > 0) {
        current--;
        revealed[current] = slides[current].querySelectorAll('.lc-slide-fragment').length;
        showSlide();
      }
    }

    function jump(n) {
      if (n < 0 || n >= slides.length) return;
      current = n;
      showSlide();
    }

    function syncFab(active) {
      var icon = fab.querySelector('.lc-slides-fab-icon');
      var label = fab.querySelector('.lc-slides-fab-label');
      if (icon) icon.textContent = active ? '✕' : '📽️';
      if (label) label.textContent = active ? 'Exit' : 'Present';
      fab.setAttribute('title', active ? 'Exit slides (Esc)' : 'Present as slides');
      fab.setAttribute('aria-label', fab.getAttribute('title'));
    }

    function syncUrl(active) {
      try {
        var url = new URL(location.href);
        if (active) url.searchParams.set('slides', '');
        else url.searchParams.delete('slides');
        history.replaceState(null, '', url.toString().replace(/\?$/, ''));
      } catch (e) {}
    }

    function enter() {
      if (!hasDeck()) return;
      body.classList.add('lc-slides-active');
      showSlide();
      syncFab(true);
      syncUrl(true);
    }

    function exit() {
      body.classList.remove('lc-slides-active');
      syncFab(false);
      syncUrl(false);
    }

    function toggle() { body.classList.contains('lc-slides-active') ? exit() : enter(); }

    partition();
    if (!hasDeck()) {
      fab.setAttribute('data-no-slides', 'true');
      return;
    }

    fab.addEventListener('click', function(e){ e.preventDefault(); toggle(); });

    document.addEventListener('keydown', function(e){
      if (!body.classList.contains('lc-slides-active')) return;
      var t = e.target;
      if (t && (t.tagName === 'TEXTAREA' || t.tagName === 'INPUT' || t.isContentEditable)) return;
      if (e.key === 'Escape') { exit(); e.preventDefault(); }
      else if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { next(); e.preventDefault(); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { prev(); e.preventDefault(); }
      else if (e.key === 'f' || e.key === 'F') {
        if (document.fullscreenElement) document.exitFullscreen();
        else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
        e.preventDefault();
      } else if (e.key >= '1' && e.key <= '9') {
        jump(parseInt(e.key, 10) - 1);
        e.preventDefault();
      }
    });

    main.addEventListener('click', function(e){
      if (!body.classList.contains('lc-slides-active')) return;
      var t = e.target;
      if (t.closest('a, button, input, textarea, ' + WIDGET_SEL)) return;
      next();
    });

    try {
      var params = new URL(location.href).searchParams;
      if (params.has('slides')) setTimeout(enter, 0);
    } catch (e) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(init, 0); });
  } else {
    setTimeout(init, 0);
  }
})();
</script>
{% endif %}
