{%- comment -%}
Model check — structural integrity of the page's declared associations.
Walks every reference an author can declare (bind=, bound-to=, avatar
target=, avatar at: selectors) and verifies it resolves to something real:
a published dataset, an element with that id / data-lc-id, a registered
avatar, a matching selector. The X-ray self-test, as a component.

Usage:
  Model integrity.
  {: .modelcheck }

window.lcModelCheck(root?) is exposed for tests and consoles — returns
{ checked, broken: [{kind, ref, from}] }. The card re-checks a few times
after upgrade (async components settle), then on demand.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-modelcheck {
  border: 1px solid #e2e8f0; border-radius: 8px;
  padding: 0.55em 0.9em; margin: 0.6em 0;
  font-size: 0.85em; color: #334155; background: #f8fafc;
}
.lc-modelcheck.ok { border-color: #bbf7d0; background: #f0fdf4; }
.lc-modelcheck.bad { border-color: #fecaca; background: #fef2f2; }
.lc-modelcheck ul { margin: 0.3em 0 0 1.2em; padding: 0; }
.lc-modelcheck button {
  margin-left: 0.8em; border: 1px solid #cbd5e1; border-radius: 6px;
  background: #fff; cursor: pointer; font-size: 0.9em; padding: 0.1em 0.6em;
}
</style>

<script>
(function () {
  if (window._lcModelCheckReady) return;
  window._lcModelCheckReady = true;

  function resolvesId(id) {
    if (!id) return false;
    if (window.lcDatasets && window.lcDatasets[id] !== undefined) return true;
    if (document.getElementById(id)) return true;
    try {
      if (document.querySelector("[data-lc-id='" + id + "']")) return true;
    } catch (e) {}
    return false;
  }

  function where(el) {
    var c = (el.className && String(el.className).split(" ")[0]) || el.tagName.toLowerCase();
    return c + (el.id ? "#" + el.id : "");
  }

  window.lcModelCheck = function (root) {
    root = root || document;
    var checked = 0, broken = [];

    /* data bindings: grid/chart/form → dataset or component id */
    root.querySelectorAll("[data-bind], [bind], [data-bound-to], [bound-to], [data-bound]")
      .forEach(function (el) {
        var id = el.getAttribute("data-bind") || el.getAttribute("bind") ||
                 el.getAttribute("data-bound-to") || el.getAttribute("bound-to") ||
                 el.getAttribute("data-bound");
        if (!id) return;
        checked++;
        if (!resolvesId(id)) {
          broken.push({ kind: "bind", ref: id, from: where(el) });
        }
      });

    /* avatar triggers → registered avatar (snake_case canonical + kebab aliases) */
    root.querySelectorAll("[data-avt-target], .avatar-trigger[target], .avatar-studio[target], .avatar-voices[target], .avatar_trigger[target], .avatar_studio[target], .avatar_voices[target]")
      .forEach(function (el) {
        var id = el.getAttribute("data-avt-target") || el.getAttribute("target");
        if (!id) return;
        checked++;
        var reg = window._lcAvatars || {};
        if (!reg[id] && !resolvesId(id)) {
          broken.push({ kind: "target", ref: id, from: where(el) });
        }
      });

    /* avatar walks: every at: selector in scripts and cues must match */
    var avs = window._lcAvatars || {};
    Object.keys(avs).forEach(function (aid) {
      var seen = {};
      function checkSel(sel) {
        if (!sel || seen[sel]) return;
        seen[sel] = 1;
        checked++;
        var hit = null;
        /* resolve exactly like the avatar itself: bare component ids or selectors */
        if (window.lcAvatarResolve) hit = window.lcAvatarResolve(sel);
        else { try { hit = document.querySelector(sel); } catch (e) {} }
        if (!hit) broken.push({ kind: "at", ref: sel, from: "avatar#" + aid });
      }
      (avs[aid].script || []).forEach(function (line) {
        checkSel(line.at);
        (line.cues || []).forEach(function (c) { checkSel(c.at); });
      });
    });

    return { checked: checked, broken: broken };
  };

  function upgradeModelCheck(el) {
    if (el.dataset.lcMcDone) return;
    el.dataset.lcMcDone = "1";
    var wrap = document.createElement("div");
    wrap.className = "lc-modelcheck";
    wrap.innerHTML = "🧪 checking…";
    el.parentNode.replaceChild(wrap, el);

    function run() {
      var r = window.lcModelCheck();
      wrap.setAttribute("data-checked", r.checked);
      wrap.setAttribute("data-broken", r.broken.length);
      wrap.setAttribute("data-acc-summary",
        r.broken.length ? "🧪 ⚠️ " + r.broken.length + " broken" : "🧪 ✅ " + r.checked);
      wrap.classList.toggle("ok", !r.broken.length);
      wrap.classList.toggle("bad", !!r.broken.length);
      var head = r.broken.length
        ? "⚠️ Model integrity: <b>" + r.broken.length + "</b> of " + r.checked + " references broken"
        : "🧪 Model integrity: <b>" + r.checked + "/" + r.checked + "</b> references resolved ✅";
      var list = r.broken.map(function (b) {
        return "<li><code>" + b.kind + " → " + b.ref + "</code> (in " + b.from + ")</li>";
      }).join("");
      wrap.innerHTML = head + " <button>↻ re-check</button>" + (list ? "<ul>" + list + "</ul>" : "");
      wrap.querySelector("button").addEventListener("click", run);
    }
    /* async components (datasets, avatars, lazy sections) settle in waves */
    [800, 3000, 7000].forEach(function (ms) { setTimeout(run, ms); });
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.modelcheck, div.modelcheck, li.modelcheck", upgradeModelCheck);
  }
})();
</script>
