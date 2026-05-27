<style>
#lc-topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 48px;
  background: rgba(255,255,255,0.95);
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  padding: 0 1.2rem;
  gap: 1.4rem;
  z-index: 1000;
  font-size: 0.9rem;
  backdrop-filter: blur(4px);
}
#lc-topbar .lc-brand {
  font-weight: bold;
  text-decoration: none;
  color: #333;
  margin-right: auto;
}
#lc-topbar .lc-links { display: flex; gap: 1.2rem; }
#lc-topbar .lc-links p { margin: 0; }
#lc-topbar a.lc-link {
  text-decoration: none;
  color: #333;
  margin-right: 1rem;
}
#lc-topbar a.lc-link:hover { color: #0066cc; }
body { padding-top: 56px; }
</style>
<div id="lc-topbar">
  <a class="lc-brand" href="/">💡 Lightcodepedia</a>
  <div class="lc-links">
{% include menu.md %}
  </div>
</div>
