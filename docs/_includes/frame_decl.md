{%- comment -%}
Frame declaration — the PAGE's half of the frame flags (Michel,
2026-08-25: "override some url params for a given module … while having a
generic shortcut in the invitations or canvas iframes").

  [frame](#)
  {: .frame up="0" reel="1" }

Two levels, per the strict= precedent (2026-08-13: "global by url, local
by knob"): the URL is the host's word and ALWAYS wins — a flag the host
spelled out is never touched. The declaration fills what the URL left
unsaid, merging into the address itself so everything downstream (the
lcFrame consumers, reel's own machinery, the flag-carry on every in-frame
hop) inherits it for free. A module whose cover declares up="0" reel="1"
is a sealed reel pod behind the same generic /go door as every other page.

Declare it near the top of the page: upgraders run in document order, and
the components below the declaration must render into the declared frame.
{%- endcomment -%}
<script>
(function () {
  if (window._lcFrameDeclReady) return;
  window._lcFrameDeclReady = true;

  var KNOWN = ["focus", "editable", "navigable", "open", "open_in",
               "crumb", "up", "strict", "reel"];

  function upgrade(el) {
    if (el.dataset.lcUpgraded) return; el.dataset.lcUpgraded = "1";
    el.style.display = "none";           /* a declaration, not content */
    var url = new URL(location.href);
    var applied = [];
    KNOWN.forEach(function (k) {
      var v = el.getAttribute(k);
      if (v == null) return;
      if (url.searchParams.has(k)) return;   /* the host said it — the host wins */
      url.searchParams.set(k, v);
      applied.push(k);
    });
    if (!applied.length) return;
    try { history.replaceState(null, "", url.toString()); } catch (e) {}
    if (window.lcFrameApply) window.lcFrameApply();
    /* reel read its param at page load, long before this declaration
       rendered — enter it now through the mode registry */
    var rv = el.getAttribute("reel");
    if (applied.indexOf("reel") >= 0 && rv !== "0" && rv !== "false" && window.lcMode) {
      window.lcMode.set("reel");
    }
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.frame", upgrade);
})();
</script>
