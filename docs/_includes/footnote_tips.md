{%- comment -%}
Footnote popover engine.

Intercepts clicks (and hover-with-delay on desktop) on kramdown footnote
references, rendering the footnote content as a small popover near the
ref instead of jumping the user to the bottom of the page. The footnotes
section at the bottom still exists for no-JS / printing.

Auto-included by docs/_layouts/default.html on every page. No setup
required per page — the moment a page contains a `[^name]` footnote,
the popover engine kicks in.
{%- endcomment -%}

<style>
.lc-fn-popover { position: absolute; background: white; border: 1px solid #d0e3f5; border-radius: 8px; padding: 0.9em 1.1em 0.7em; font-size: 0.9em; line-height: 1.55; color: #333; max-width: 380px; min-width: 220px; box-shadow: 0 6px 24px rgba(0,0,0,0.14); z-index: 10000; opacity: 0; pointer-events: none; transition: opacity 0.14s ease; box-sizing: border-box; }
.lc-fn-popover.lc-fn-visible { opacity: 1; pointer-events: auto; }
.lc-fn-popover-arrow { position: absolute; width: 12px; height: 12px; background: white; border-left: 1px solid #d0e3f5; border-top: 1px solid #d0e3f5; transform: rotate(45deg); top: -7px; left: 16px; }
.lc-fn-popover-close { position: absolute; top: 4px; right: 6px; background: none; border: none; color: #888; font-size: 0.95em; cursor: pointer; padding: 2px 6px; line-height: 1; border-radius: 3px; }
.lc-fn-popover-close:hover { color: #222; background: #f0f0f0; }
.lc-fn-popover-body p:first-child { margin-top: 0; }
.lc-fn-popover-body p:last-child { margin-bottom: 0; }
.lc-fn-popover-body code { background: #eef; padding: 0.1em 0.35em; border-radius: 3px; font-size: 0.92em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-fn-popover-body a.reversefootnote, .lc-fn-popover-body a.footnote-backref { display: none; }
.lc-fn-popover-body pre { background: #f8f8f8; padding: 0.6em 0.8em; border-radius: 4px; overflow-x: auto; font-size: 0.85em; }
.lc-fn-popover-body ul, .lc-fn-popover-body ol { margin: 0.4em 0; padding-left: 1.4em; }

/* Style footnote refs themselves (kramdown emits <sup id="fnref:X"><a href="#fn:X" class="footnote">N</a></sup>) */
a.footnote, sup.footnote a, sup[id^="fnref"] a {
  text-decoration: none;
  color: #0066cc;
  background: #e7f1fe;
  padding: 0 5px;
  border-radius: 8px;
  font-size: 0.72em;
  margin-left: 1px;
  font-weight: 600;
  vertical-align: super;
  line-height: 1;
  border: 1px solid transparent;
  transition: background 0.12s, border-color 0.12s;
}
a.footnote:hover, sup.footnote a:hover, sup[id^="fnref"] a:hover {
  background: #d0e3f5;
  border-color: #0066cc;
}
sup.footnote, sup[id^="fnref"] { font-size: inherit; }

/* Tweak the footnotes section heading */
div.footnotes::before { content: "Definitions"; display: block; font-weight: 600; color: #444; margin: 2em 0 0.4em; padding-top: 1em; border-top: 1px solid #eee; }
div.footnotes ol { font-size: 0.9em; color: #555; }
</style>
<script>
(function(){
  function init() {
    var refs = document.querySelectorAll('a[href^="#fn:"]');
    if (!refs.length) return;

    var popover = document.createElement('div');
    popover.className = 'lc-fn-popover';
    popover.innerHTML = '<button class="lc-fn-popover-close" aria-label="Close">✕</button><div class="lc-fn-popover-arrow"></div><div class="lc-fn-popover-body"></div>';
    document.body.appendChild(popover);
    var body = popover.querySelector('.lc-fn-popover-body');
    var closeBtn = popover.querySelector('.lc-fn-popover-close');
    var arrow = popover.querySelector('.lc-fn-popover-arrow');
    var current = null;
    var hoverTimer = null;
    var leaveTimer = null;
    var touchOnly = window.matchMedia('(hover: none)').matches;

    function show(ref) {
      var href = ref.getAttribute('href');
      if (!href || href.charAt(0) !== '#') return;
      var target = document.getElementById(href.substring(1));
      if (!target) return;

      body.innerHTML = target.innerHTML;
      Array.prototype.forEach.call(body.querySelectorAll('a.reversefootnote, a.footnote-backref'), function(el){
        el.parentNode.removeChild(el);
      });

      popover.classList.add('lc-fn-visible');
      current = ref;

      // Position after layout so width is known
      requestAnimationFrame(function(){
        var rect = ref.getBoundingClientRect();
        var scrollY = window.pageYOffset;
        var scrollX = window.pageXOffset;
        var pRect = popover.getBoundingClientRect();
        var margin = 10;

        var left = rect.left + scrollX;
        var maxLeft = scrollX + window.innerWidth - pRect.width - margin;
        if (left > maxLeft) left = maxLeft;
        if (left < scrollX + margin) left = scrollX + margin;

        // Below by default; flip above if it would overflow viewport bottom
        var top = rect.bottom + scrollY + 8;
        if (rect.bottom + pRect.height + 20 > window.innerHeight) {
          top = rect.top + scrollY - pRect.height - 8;
          arrow.style.top = 'auto';
          arrow.style.bottom = '-7px';
          arrow.style.transform = 'rotate(225deg)';
        } else {
          arrow.style.top = '-7px';
          arrow.style.bottom = 'auto';
          arrow.style.transform = 'rotate(45deg)';
        }

        popover.style.left = left + 'px';
        popover.style.top = top + 'px';

        var arrowX = (rect.left + scrollX) - left + (rect.width / 2) - 6;
        if (arrowX < 8) arrowX = 8;
        if (arrowX > pRect.width - 20) arrowX = pRect.width - 20;
        arrow.style.left = arrowX + 'px';
      });
    }

    function hide() {
      popover.classList.remove('lc-fn-visible');
      current = null;
    }

    Array.prototype.forEach.call(refs, function(ref){
      ref.addEventListener('click', function(e){
        e.preventDefault();
        if (current === ref) hide();
        else show(ref);
      });
      if (!touchOnly) {
        ref.addEventListener('mouseenter', function(){
          clearTimeout(leaveTimer);
          hoverTimer = setTimeout(function(){ show(ref); }, 200);
        });
        ref.addEventListener('mouseleave', function(){
          clearTimeout(hoverTimer);
          leaveTimer = setTimeout(function(){
            if (!popover.matches(':hover')) hide();
          }, 200);
        });
      }
    });

    if (!touchOnly) {
      popover.addEventListener('mouseenter', function(){ clearTimeout(leaveTimer); });
      popover.addEventListener('mouseleave', function(){ leaveTimer = setTimeout(hide, 200); });
    }

    closeBtn.addEventListener('click', hide);
    document.addEventListener('click', function(e){
      if (current && !popover.contains(e.target) && !current.contains(e.target)) hide();
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') hide();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
