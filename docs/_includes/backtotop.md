<style>
#lc-btt {
  position: fixed;
  bottom: 2rem; right: 2rem;
  width: 42px; height: 42px;
  border-radius: 50%;
  background: #444;
  color: white;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 999;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
#lc-btt:hover { background: #222; }
</style>
<button id="lc-btt" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="Back to top">↑</button>
<script>
const _btt = document.getElementById('lc-btt');
window.addEventListener('scroll', () => {
  _btt.style.display = window.scrollY > 300 ? 'flex' : 'none';
});
</script>
