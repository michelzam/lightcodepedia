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
body.lc-slides-active .lc-slide[data-active="true"] { display: block; flex: 1; padding: 3em 5em 6em; overflow-y: auto; max-width: 1200px; width: 100%; margin: 0 auto; box-sizing: border-box; animation: lcSlideIn 0.22s ease-out; -webkit-overflow-scrolling: touch; }
@keyframes lcSlideIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
body.lc-slides-active .lc-slide h1 { font-size: 2.6em; border-bottom: 2px solid #0066cc; padding-bottom: 0.3em; margin: 0 0 0.6em; }
body.lc-slides-active .lc-slide h2 { font-size: 2em; border-bottom: 2px solid #0066cc; padding-bottom: 0.3em; margin: 0 0 0.6em; color: #222; }
body.lc-slides-active .lc-slide h3 { font-size: 1.4em; }
body.lc-slides-active .lc-slide p, body.lc-slides-active .lc-slide li { font-size: 1.15em; line-height: 1.7; }
body.lc-slides-active .lc-slide ul, body.lc-slides-active .lc-slide ol { padding-left: 1.4em; }
body.lc-slides-active .lc-slide-fragment { opacity: 0.18; transition: opacity 0.28s ease; }
body.lc-slides-active .lc-slide-fragment[data-revealed="true"] { opacity: 1; }
@media (max-width: 700px) {
  body.lc-slides-active .lc-slide[data-active="true"] { padding: 1.6em 1.2em 5em; }
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

.lc-slides-share-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.88); display: none; align-items: center; justify-content: center; z-index: 10002; padding: 1em; }
.lc-slides-share-overlay.lc-share-open { display: flex; }
.lc-slides-share-panel { background: white; padding: 1.5em 2em 1.4em; border-radius: 12px; max-width: 90vw; max-height: 90vh; text-align: center; position: relative; box-shadow: 0 20px 60px rgba(0,0,0,0.4); display: flex; flex-direction: column; align-items: center; gap: 1em; }
.lc-slides-share-panel h4 { margin: 0; font-size: 1.4em; color: #222; font-weight: 600; }
.lc-slides-share-close { position: absolute; top: 0.5em; right: 0.7em; background: none; border: none; font-size: 1.4em; cursor: pointer; color: #888; line-height: 1; padding: 0.2em 0.4em; border-radius: 4px; }
.lc-slides-share-close:hover { color: #222; background: #f0f0f0; }
.lc-slides-share-qr { width: min(60vh, 360px); height: min(60vh, 360px); display: flex; align-items: center; justify-content: center; padding: 0.5em; background: white; }
.lc-slides-share-qr svg, .lc-slides-share-qr img { width: 100%; height: 100%; }
.lc-slides-share-qr-fallback { font-size: 0.9em; color: #888; padding: 2em; }
.lc-slides-share-url { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.78em; color: #666; word-break: break-all; max-width: 90%; padding: 0.5em 0.8em; background: #f5f5f5; border-radius: 4px; line-height: 1.4; }
.lc-slides-share-copy { padding: 0.55em 1.6em; background: #0066cc; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.95em; font-weight: 500; }
.lc-slides-share-copy:hover { background: #0052a3; }
.lc-slides-share-copy.lc-copied { background: #2e7d32; }
@media (max-width: 480px) {
  .lc-slides-share-panel { padding: 1em; gap: 0.7em; }
  .lc-slides-share-qr { width: min(70vw, 280px); height: min(70vw, 280px); }
}
</style>
<a class="lc-slides-fab" href="#" title="Present as slides" aria-label="Present as slides">
  <span class="lc-slides-fab-icon" aria-hidden="true">📽️</span><span class="lc-slides-fab-label">Present</span>
</a>
<nav class="lc-slides-nav" role="toolbar" aria-label="Slide navigation">
  <button class="lc-slides-nav-prev" type="button" title="Previous (←)" aria-label="Previous slide">◀</button>
  <select class="lc-slides-nav-jump" title="Jump to slide" aria-label="Jump to slide"></select>
  <button class="lc-slides-nav-next" type="button" title="Next (→ or Space)" aria-label="Next slide / fragment">▶</button>
  <button class="lc-slides-nav-share" type="button" title="Share with QR code (Q)" aria-label="Share with QR code">📷</button>
</nav>
<div class="lc-slides-share-overlay" role="dialog" aria-modal="true" aria-label="Share slide">
  <div class="lc-slides-share-panel">
    <button class="lc-slides-share-close" type="button" aria-label="Close">✕</button>
    <h4>Scan to follow along</h4>
    <div class="lc-slides-share-qr"></div>
    <div class="lc-slides-share-url"></div>
    <button class="lc-slides-share-copy" type="button">Copy link</button>
  </div>
</div>
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

    function slideQuizElements(s) {
      // Anything graded on this slide: quizzes + runners with expected=
      return Array.prototype.slice.call(s.querySelectorAll('[data-lc-quiz-id]'));
    }

    function slideScoreMarker(s) {
      var quizEls = slideQuizElements(s);
      if (quizEls.length === 0) return '';
      if (!window.lcQuizScore || !window.lcQuizScore.get) return ' ⚠️';
      var allCorrect = quizEls.every(function(q){
        var id = q.dataset.lcQuizId;
        var entry = id && window.lcQuizScore.get(id);
        return entry && entry.correct;
      });
      return allCorrect ? ' ✅' : ' ⚠️';
    }

    function slideTitle(s, i) {
      var h = s.querySelector('h1, h2');
      var t = h ? (h.textContent || '').trim().replace(/\s+/g, ' ') : '';
      if (!t) t = 'Slide ' + (i + 1);
      if (t.length > 38) t = t.substring(0, 36) + '…';
      return t + slideScoreMarker(s);
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
      if (document.body.classList.contains('lc-slides-active')) syncUrl(true);
    }

    function next() {
      var slide = slides[current];
      var frags = slide.querySelectorAll('.lc-slide-fragment');
      if (revealed[current] < frags.length) {
        revealed[current]++;
        showSlide();
        var newFrag = slide.querySelectorAll('.lc-slide-fragment')[revealed[current] - 1];
        if (newFrag && newFrag.scrollIntoView) {
          try { newFrag.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); } catch (e) {}
        }
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
        if (active) url.searchParams.set('slides', String(current));
        else url.searchParams.delete('slides');
        history.replaceState(null, '', url.toString().replace(/\?$/, ''));
        refreshShareIfOpen();
      } catch (e) {}
    }

    var _qrLoading = null;
    function loadQrcode() {
      if (window.qrcode) return Promise.resolve();
      if (_qrLoading) return _qrLoading;
      _qrLoading = new Promise(function(resolve){
        var s = document.createElement('script');
        s.src = 'https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js';
        s.onload = function(){ resolve(); };
        s.onerror = function(){ resolve(); };
        document.head.appendChild(s);
      });
      return _qrLoading;
    }

    function refreshShareIfOpen() {
      var overlay = document.querySelector('.lc-slides-share-overlay');
      if (!overlay || !overlay.classList.contains('lc-share-open')) return;
      renderShare();
    }

    function renderShare() {
      var overlay = document.querySelector('.lc-slides-share-overlay');
      if (!overlay) return;
      var qrBox = overlay.querySelector('.lc-slides-share-qr');
      var urlBox = overlay.querySelector('.lc-slides-share-url');
      var href = location.href;
      urlBox.textContent = href;
      if (!window.qrcode) {
        qrBox.innerHTML = '<div class="lc-slides-share-qr-fallback">loading QR…</div>';
        return;
      }
      try {
        var qr = window.qrcode(0, 'M');
        qr.addData(href);
        qr.make();
        qrBox.innerHTML = qr.createSvgTag({ scalable: true, margin: 1 });
      } catch (e) {
        qrBox.innerHTML = '<div class="lc-slides-share-qr-fallback">QR error</div>';
      }
    }

    function openShare() {
      var overlay = document.querySelector('.lc-slides-share-overlay');
      if (!overlay) return;
      overlay.classList.add('lc-share-open');
      renderShare();
      loadQrcode().then(renderShare);
    }

    function closeShare() {
      var overlay = document.querySelector('.lc-slides-share-overlay');
      if (overlay) overlay.classList.remove('lc-share-open');
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

    var navShare = nav ? nav.querySelector('.lc-slides-nav-share') : null;
    var shareOverlay = document.querySelector('.lc-slides-share-overlay');
    if (navShare) navShare.addEventListener('click', function(e){ e.preventDefault(); openShare(); });
    if (shareOverlay) {
      shareOverlay.addEventListener('click', function(e){
        if (e.target === shareOverlay) closeShare();
      });
      var closeBtn = shareOverlay.querySelector('.lc-slides-share-close');
      if (closeBtn) closeBtn.addEventListener('click', closeShare);
      var copyBtn = shareOverlay.querySelector('.lc-slides-share-copy');
      if (copyBtn) {
        copyBtn.addEventListener('click', function(){
          var href = location.href;
          var done = function(){
            copyBtn.textContent = '✓ Copied';
            copyBtn.classList.add('lc-copied');
            setTimeout(function(){
              copyBtn.textContent = 'Copy link';
              copyBtn.classList.remove('lc-copied');
            }, 1500);
          };
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(href).then(done, function(){});
          } else {
            try {
              var ta = document.createElement('textarea');
              ta.value = href;
              document.body.appendChild(ta);
              ta.select();
              document.execCommand('copy');
              document.body.removeChild(ta);
              done();
            } catch (e) {}
          }
        });
      }
    }

    // Rebuild picker option labels when any quiz/runner score changes
    if (window.lcQuizScore && window.lcQuizScore.subscribe) {
      window.lcQuizScore.subscribe(buildJumpOptions);
    }

    document.addEventListener('keydown', function(e){
      if (!body.classList.contains('lc-slides-active')) return;
      var t = e.target;
      if (t && (t.tagName === 'TEXTAREA' || t.tagName === 'INPUT' || t.isContentEditable)) return;
      var overlay = document.querySelector('.lc-slides-share-overlay');
      if (overlay && overlay.classList.contains('lc-share-open')) {
        if (e.key === 'Escape' || e.key === 'q' || e.key === 'Q') { closeShare(); e.preventDefault(); }
        return;
      }
      if (e.key === 'Escape') { exit(); e.preventDefault(); }
      else if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { next(); e.preventDefault(); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { prev(); e.preventDefault(); }
      else if (e.key === 'f' || e.key === 'F') {
        if (document.fullscreenElement) document.exitFullscreen();
        else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
        e.preventDefault();
      } else if (e.key === 'q' || e.key === 'Q') {
        openShare(); e.preventDefault();
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
      if (params.has('slides')) {
        var startN = parseInt(params.get('slides'), 10);
        if (!isNaN(startN) && startN >= 0 && startN < slides.length) current = startN;
        setTimeout(enter, 0);
      }
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
