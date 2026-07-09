{%- comment -%}
Store — the browser-instance structural state store.

Learner state persists in this browser only (localStorage, per-origin), keyed by
the structural path node.component.field — the same path used at design time
(the IAL #id), in {= cells }, and in Python. Files/inline are design-time seeds;
only what the learner actually sets reaches the Store (seeds never pollute it).

  window.lcStore.get(path)      -> value, or undefined if unset
  window.lcStore.set(path, v)   -> writes + fires lc-model-changed
  window.lcStore.reset()        -> clears the whole store
  window.lcStore.tree()         -> the raw JSON blob (Python reads this)

Auto-included by docs/_layouts/default.html (before the components that read it).
{%- endcomment -%}

<script>
(function () {
  if (window.lcStore) return;
  var KEY = "lc_state";
  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; }
    catch (e) { return {}; }
  }
  function write(tree) {
    try { localStorage.setItem(KEY, JSON.stringify(tree)); } catch (e) {}
  }
  function announce(path) {
    try { document.dispatchEvent(new CustomEvent("lc-model-changed", { detail: { source: "store", path: path || "" } })); } catch (e) {}
  }
  window.lcStore = {
    tree: function () {
      try { return localStorage.getItem(KEY) || "{}"; } catch (e) { return "{}"; }
    },
    get: function (path) {
      var node = read(), segs = String(path).split(".");
      for (var i = 0; i < segs.length; i++) {
        if (node && typeof node === "object" && Object.prototype.hasOwnProperty.call(node, segs[i])) node = node[segs[i]];
        else return undefined;   // unset — the seed wins on the capturing page
      }
      return node;
    },
    set: function (path, value) {
      var tree = read(), node = tree, segs = String(path).split(".");
      for (var i = 0; i < segs.length - 1; i++) {
        if (!node[segs[i]] || typeof node[segs[i]] !== "object") node[segs[i]] = {};
        node = node[segs[i]];
      }
      node[segs[segs.length - 1]] = value;
      write(tree);
      announce(path);
    },
    reset: function () {
      try { localStorage.removeItem(KEY); } catch (e) {}
      announce("");
    }
  };
})();
</script>
