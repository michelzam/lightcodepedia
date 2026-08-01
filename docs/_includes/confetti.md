{%- comment -%}
Confetti — one verb, earned moments only.

  window.lcConfetti(el)   burst from the element's top edge; auto-cleans.

Who calls it:
  • a .feature with celebration="true", on its FIRST red→green transition;
  • any python step or .button via the runtime verb — self.page.<id>.confetti().

Never fires on page load, never on a re-run of an already-green card —
celebration is set by the page, not by the engine's mood. Users who prefer
reduced motion get a quiet ✨ pulse instead of the storm.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-confetti { position: absolute; width: 9px; height: 14px; top: 0; left: 50%; pointer-events: none; z-index: 3000; opacity: 0; border-radius: 2px; animation: lc-confetti-fall var(--lc-cf-t, 1.5s) ease-out forwards; }
@keyframes lc-confetti-fall {
  0%   { opacity: 1; transform: translate(0, 0) rotate(0deg); }
  100% { opacity: 0; transform: translate(var(--lc-cf-x, 0px), var(--lc-cf-y, 220px)) rotate(var(--lc-cf-r, 540deg)); }
}
.lc-confetti-quiet { position: absolute; top: -0.4em; left: 50%; transform: translateX(-50%); font-size: 1.6em; pointer-events: none; z-index: 3000; animation: lc-confetti-quiet 1.6s ease-out forwards; }
@keyframes lc-confetti-quiet { 0% { opacity: 0; } 25% { opacity: 1; } 100% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .lc-confetti { animation-duration: 0.01s; opacity: 0; }
}
</style>

<script>
(function () {
  if (window.lcConfetti) return;
  var COLORS = ["#f59e0b", "#22c55e", "#3b82f6", "#ec4899", "#a855f7", "#ef4444", "#14b8a6"];

  window.lcConfetti = function (el) {
    var host = el && el.nodeType === 1 ? el : document.body;
    var cs = getComputedStyle(host);
    if (cs.position === "static") host.style.position = "relative";
    var quiet = false;
    try { quiet = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
    if (quiet) {
      var star = document.createElement("div");
      star.className = "lc-confetti-quiet";
      star.textContent = "✨";
      host.appendChild(star);
      setTimeout(function () { if (star.parentNode) star.parentNode.removeChild(star); }, 1800);
      return;
    }
    var w = host.offsetWidth || 300;
    for (var i = 0; i < 36; i++) {
      var p = document.createElement("i");
      p.className = "lc-confetti";
      p.style.background = COLORS[i % COLORS.length];
      p.style.left = Math.round(10 + Math.random() * 80) + "%";
      p.style.setProperty("--lc-cf-x", Math.round((Math.random() - 0.5) * w * 0.6) + "px");
      p.style.setProperty("--lc-cf-y", Math.round(140 + Math.random() * 160) + "px");
      p.style.setProperty("--lc-cf-r", Math.round((Math.random() - 0.5) * 1080) + "deg");
      p.style.setProperty("--lc-cf-t", (1.1 + Math.random() * 0.9).toFixed(2) + "s");
      host.appendChild(p);
      (function (node) {
        setTimeout(function () { if (node.parentNode) node.parentNode.removeChild(node); }, 2300);
      })(p);
    }
  };
})();
</script>
