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
#lc-topbar a { text-decoration: none; color: #333; }
#lc-topbar a:hover { color: #0066cc; }
#lc-topbar .lc-brand { font-weight: bold; margin-right: auto; }
body { padding-top: 56px; }
</style>
<div id="lc-topbar">
  <a class="lc-brand" href="/">💡 Lightcodepedia</a>
  <a href="demo">🎬 Demo</a>
  <a href="chapters">📚 Chapters</a>
  <a href="ari">🤖 Ari</a>
  <a href="events">🎭 Events</a>
  <a href="about">ℹ️ About</a>
</div>
