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
@media (hover: hover) and (pointer: fine) {
  .lc-slides-fab:hover { background: #f5f9ff; border-color: #0066cc; box-shadow: 0 4px 14px rgba(0,102,204,0.18); transform: translateY(-1px); gap: 0.45em; padding-right: 16px; }
  .lc-slides-fab:hover .lc-slides-fab-label { max-width: 140px; opacity: 1; }
}
.lc-slides-fab.lc-fab-expanded { background: #f5f9ff; border-color: #0066cc; box-shadow: 0 4px 14px rgba(0,102,204,0.18); transform: translateY(-1px); gap: 0.45em; padding-right: 16px; }
.lc-slides-fab.lc-fab-expanded .lc-slides-fab-label { max-width: 140px; opacity: 1; }
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

.lc-slides-nav { position: fixed; bottom: 0.9em; left: 50%; transform: translateX(-50%); display: none; align-items: center; gap: 0.3em; background: rgba(255,255,255,0.96); border: 1px solid #d0e3f5; border-radius: 26px; padding: 4px 6px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 1001; max-width: calc(100vw - 130px); backdrop-filter: blur(4px); }
body.lc-slides-active .lc-slides-nav { display: inline-flex; }
.lc-slides-nav button { width: 40px; height: 40px; border: none; background: transparent; color: #0066cc; font-size: 1.05em; cursor: pointer; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: background 0.12s; padding: 0; }
.lc-slides-nav button:hover:not(:disabled) { background: #f5f9ff; }
.lc-slides-nav button:disabled { color: #c8d2dc; cursor: not-allowed; }
.lc-slides-nav-jump { border: none; background: transparent; font-size: 0.85em; color: #333; padding: 0.45em 1.6em 0.45em 0.6em; cursor: pointer; max-width: 180px; min-width: 64px; text-overflow: ellipsis; outline: none; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; appearance: none; -webkit-appearance: none; background-image: linear-gradient(45deg, transparent 50%, #0066cc 50%), linear-gradient(135deg, #0066cc 50%, transparent 50%); background-position: calc(100% - 12px) calc(50% - 2px), calc(100% - 7px) calc(50% - 2px); background-size: 5px 5px; background-repeat: no-repeat; }
.lc-slides-nav-jump:hover { background-color: #f5f9ff; border-radius: 4px; }
@media (max-width: 480px) {
  .lc-slides-nav { padding: 3px 4px; gap: 0.15em; max-width: calc(100vw - 100px); }
  .lc-slides-nav button { width: 36px; height: 36px; }
  .lc-slides-nav-jump { font-size: 0.78em; max-width: 130px; min-width: 50px; padding: 0.4em 1.4em 0.4em 0.5em; }
}
</style>
<a class="lc-slides-fab" href="#" title="Present as slides" aria-label="Present as slides">
  <span class="lc-slides-fab-icon" aria-hidden="true">📽️</span><span class="lc-slides-fab-label">Present</span>
</a>
<nav class="lc-slides-nav" role="toolbar" aria-label="Slide navigation">
  <button class="lc-slides-nav-prev" type="button" title="Previous (←)" aria-label="Previous slide">◀</button>
  <select class="lc-slides-nav-jump" title="Jump to slide" aria-label="Jump to slide"></select>
  <button class="lc-slides-nav-next" type="button" title="Next (→ or Space)" aria-label="Next slide / fragment">▶</button>
</nav>
<script>
(function(){
  function init() {
    var fab = document.querySelector('.lc-slides-fab');
    var nav = document.querySelector('.lc-slides-nav');
    var navPrev = nav ? nav.querySelector('.lc-slides-nav-prev') : null;
    var navNext = nav ? nav.querySelector('.lc-slides-nav-next') : null;
    var navJump = nav ? nav.querySelector('.lc-slides-nav-jump') : null;
    var body = document.body;
    var main = document.querySelector('main.markdown-body');
    if (!fab || !main) return;

    var slides = [];
    var current = 0;
    var revealed = [];
    var WIDGET_SEL = '.lc-pyrun, .lc-pyrepl, .lc-datagrid, .lc-form, .ag-root-wrapper, .lc-tabs, .lc-quiz, .lc-quiz-bar';

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
        // Each top-level code block / runner / grid / form becomes its own fragment too
        Array.prototype.forEach.call(section.children, function(el){
          if (el.classList.contains('nofragments')) return;
          if (el.tagName === 'PRE' ||
              el.classList.contains('highlighter-rouge') ||
              el.classList.contains('highlight') ||
              el.classList.contains('lc-pyrun') ||
              el.classList.contains('lc-pyrepl') ||
              el.classList.contains('lc-datagrid') ||
              el.classList.contains('lc-form')) {
            el.classList.add('lc-slide-fragment');
          }
        });
      });
      revealed = slides.map(function(){ return 0; });
    }

    function hasDeck() { return slides.length > 1; }

    function slideTitle(s, i) {
      var h = s.querySelector('h1, h2');
      var t = h ? (h.textContent || '').trim().replace(/\s+/g, ' ') : '';
      if (t.length > 36) t = t.substring(0, 34) + '…';
      return (i + 1) + '/' + slides.length + (t ? ' · ' + t : '');
    }

    function buildJumpOptions() {
      if (!navJump) return;
      navJump.innerHTML = '';
      slides.forEach(function(s, i){
        var opt = document.createElement('option');
        opt.value = String(i);
        opt.textContent = slideTitle(s, i);
        navJump.appendChild(opt);
      });
    }

    function showSlide() {
      slides.forEach(function(s, i){
        s.setAttribute('data-active', i === current ? 'true' : 'false');
        var frags = s.querySelectorAll('.lc-slide-fragment');
        Array.prototype.forEach.call(frags, function(f, j){
          f.setAttribute('data-revealed', j < revealed[i] ? 'true' : 'false');
        });
      });
      if (navJump) navJump.value = String(current);
      var totalFrags = slides[current].querySelectorAll('.lc-slide-fragment').length;
      var atFirst = current === 0 && revealed[0] === 0;
      var atLast = current === slides.length - 1 && revealed[current] === totalFrags;
      if (navPrev) navPrev.disabled = atFirst;
      if (navNext) navNext.disabled = atLast;
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
    buildJumpOptions();

    var touchOnly = window.matchMedia('(hover: none)').matches;
    var fabCollapseTimer = null;
    function collapseFab(){ fab.classList.remove('lc-fab-expanded'); }
    fab.addEventListener('click', function(e){
      e.preventDefault();
      if (touchOnly && !body.classList.contains('lc-slides-active') && !fab.classList.contains('lc-fab-expanded')) {
        fab.classList.add('lc-fab-expanded');
        clearTimeout(fabCollapseTimer);
        fabCollapseTimer = setTimeout(collapseFab, 3000);
        return;
      }
      clearTimeout(fabCollapseTimer);
      collapseFab();
      toggle();
    });
    document.addEventListener('click', function(e){
      if (!fab.contains(e.target)) collapseFab();
    });

    if (navPrev) navPrev.addEventListener('click', function(e){ e.preventDefault(); prev(); });
    if (navNext) navNext.addEventListener('click', function(e){ e.preventDefault(); next(); });
    if (navJump) navJump.addEventListener('change', function(){ jump(parseInt(navJump.value, 10)); });

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
      if (t.closest('a, button, input, textarea, select, ' + WIDGET_SEL)) return;
      if (e.clientX < window.innerWidth / 2) prev();
      else next();
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
