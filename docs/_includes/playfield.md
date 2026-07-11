{%- comment -%}
Playfield — a little park scene for "throw the ball, Lucky fetches".
A 🌳 park (the target), a 🎾 ball that follows a bound slider form's x/y (0–100),
and 🐕 Lucky who runs to the ball on Fetch. Pure JS: reads the form's published
data-lc-value on lc-model-changed. No account, nothing saved.

  ```
  ```
  {: .playfield #field bind="hunt" park="70,30" }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-playfield { position: relative; height: 240px; background: linear-gradient(#cdeeb0, #93d06d);
  border: 1px solid #6ab04c; border-radius: 10px; overflow: hidden; margin: 1em 0; }
.lc-pf-marker { position: absolute; transform: translate(-50%, -50%); font-size: 1.9em; user-select: none; line-height: 1; }
.lc-pf-lucky { transition: left .5s ease, top .5s ease; }
.lc-pf-ball  { transition: left .12s linear, top .12s linear; }
.lc-pf-msg { position: absolute; left: 50%; bottom: 8px; transform: translateX(-50%);
  background: rgba(255,255,255,.88); padding: 2px 12px; border-radius: 12px; font-size: .85em; white-space: nowrap; }
.lc-pf-btn { position: absolute; right: 8px; top: 8px; padding: .35em .85em; border-radius: 6px;
  border: 1px solid #6ab04c; background: #fff; cursor: pointer; font: inherit; }
.lc-pf-btn:hover { background: #eaf6df; }
</style>
<script>
(function () {
  if (window._lcPlayfieldReady) return; window._lcPlayfieldReady = true;

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return; el.dataset.lcUpgraded = "1";
    var bind = el.getAttribute("bind") || "";
    var park = (el.getAttribute("park") || "70,30").split(",").map(Number);
    var id = el.id || "";

    var wrap = document.createElement("div");
    wrap.className = "lc-playfield";
    if (id) wrap.setAttribute("data-lc-id", id);

    function pos(d, x, y) { d.style.left = x + "%"; d.style.top = (100 - y) + "%"; d._x = x; d._y = y; }
    function mk(txt, cls, x, y) { var d = document.createElement("div"); d.className = "lc-pf-marker " + cls; d.textContent = txt; pos(d, x, y); return d; }

    var tree  = mk("🌳", "lc-pf-tree", park[0], park[1]);
    var ball  = mk("🎾", "lc-pf-ball", 20, 80);
    var lucky = mk("🐕", "lc-pf-lucky", 8, 8);
    var msg = document.createElement("div"); msg.className = "lc-pf-msg"; msg.textContent = "Slide to move the ball 🎾";
    var btn = document.createElement("button"); btn.className = "lc-pf-btn"; btn.textContent = "🐕 Fetch!";
    wrap.appendChild(tree); wrap.appendChild(ball); wrap.appendChild(lucky); wrap.appendChild(msg); wrap.appendChild(btn);
    el.parentNode.replaceChild(wrap, el);

    function inPark() { return Math.hypot(ball._x - park[0], ball._y - park[1]) <= 12; }

    function refresh() {
      if (bind) {
        var f = document.querySelector(".lc-form[data-lc-id='" + bind + "']");
        if (f) { try { var d = JSON.parse(f.getAttribute("data-lc-value") || "{}");
          if (typeof d.x === "number" && typeof d.y === "number") pos(ball, d.x, d.y); } catch (e) {} }
      }
      msg.textContent = inPark() ? "🎯 In the park! Hit Fetch 🐕" : "Slide to move the ball 🎾";
    }

    btn.addEventListener("click", function () {
      pos(lucky, ball._x, ball._y);              // Lucky runs to the ball
      setTimeout(function () {
        msg.textContent = inPark() ? "🎾 Fetched! Good boy, Lucky! 🐾" : "🐕 Got it — but throw it in the park 🌳!";
      }, 520);
    });

    document.addEventListener("lc-model-changed", refresh);
    refresh();
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader(".highlighter-rouge.playfield, pre.playfield", upgrade);
})();
</script>
