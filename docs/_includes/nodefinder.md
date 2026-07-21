{%- comment -%}
LightNode finder — the 404 page doubles as a router. GitHub Pages serves
/404.html for every unknown path, so lightcodepedia.org/@student (or bare
/student) lands here with the name in hand: one anonymous API check, then a
redirect to https://student.github.io/lightcodepedia/. Unknown name → a
friendly "start yours" invitation instead of a dead end. Emitted ONLY into
the 404 page (Liquid guard), so every other page carries zero extra script.
{%- endcomment -%}
{% if page.permalink == '/404.html' %}
<script>
(function () {
  var BASE  = {{ site.baseurl | default: "" | jsonify }};
  var CANON = {{ site.lc_canonical_owner | default: "" | jsonify }};
  var path = location.pathname;
  if (BASE && path.indexOf(BASE) === 0) path = path.slice(BASE.length);
  var segs = path.split('/').filter(Boolean);
  if (segs.length !== 1) return;
  var cand = decodeURIComponent(segs[0]);
  if (cand.charAt(0) === '@') cand = cand.slice(1);
  if (!/^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$/.test(cand)) return;

  var main = document.querySelector('main') || document.body;
  /* a plausible name means this is (probably) a router hit, not a dead end —
     don't flash the 404 while the lookup runs; reveal it only on a miss */
  var hidden = [];
  Array.prototype.forEach.call(main.children, function (el) {
    hidden.push([el, el.style.display]); el.style.display = 'none';
  });
  function reveal() { hidden.forEach(function (p) { p[0].style.display = p[1]; }); }
  var note = document.createElement('p');
  note.style.cssText = 'padding:0.8em 1em;background:#f0f6ff;border:1px solid #c7ddf7;border-radius:8px;font-size:0.95em';
  note.textContent = '🔭 Looking for @' + cand + '’s LightNode…';
  main.insertBefore(note, main.firstChild);

  if (CANON && cand.toLowerCase() === CANON.toLowerCase()) { location.replace('/'); return; }
  var dest = 'https://' + cand + '.github.io/lightcodepedia/';
  function go() {
    note.textContent = '🚀 Found — taking you to @' + cand + '’s LightNode…';
    location.replace(dest);
  }
  /* The repo existing is NOT enough: GitHub never auto-enables Pages on a
     fork, so a fork without a live site redirected blindly lands on a GitHub
     404. Probe the built site itself with an image every fork ships
     (cross-origin img load/error is readable where fetch is opaque); a probe
     TIMEOUT stays optimistic — slow network is not a dead site. */
  function siteProbe(onUp, onDown) {
    var img = new Image(), done = false;
    var t = setTimeout(function () { if (!done) { done = true; onUp(); } }, 6000);
    img.onload  = function () { if (!done) { done = true; clearTimeout(t); onUp(); } };
    img.onerror = function () { if (!done) { done = true; clearTimeout(t); onDown(); } };
    img.src = dest + 'assets/lab.jpg?lcprobe=' + Date.now();
  }
  function forkNotLive() {
    reveal();
    note.innerHTML = '🌱 <b>@' + cand + '</b> has a LightNode fork, but its site isn’t switched on yet. ' +
      'The owner flips it on once: repo <b>Settings → Pages → Deploy from a branch → main, /docs</b>. ' +
      '<a href="' + dest + '">Try anyway →</a>';
  }
  fetch('https://api.github.com/repos/' + cand + '/lightcodepedia')
    .then(function (r) {
      if (r.ok) {
        /* The fork exists — but is its site ON? Pages deployments are public
           on public repos: any github-pages deployment = the site has built.
           Asset-independent, unlike the img probe (an old fork's live site
           may predate the probe asset); the img stays as rate-limit fallback. */
        fetch('https://api.github.com/repos/' + cand + '/lightcodepedia/deployments?environment=github-pages&per_page=1')
          .then(function (r2) { return r2.ok ? r2.json() : null; })
          .then(function (deps) {
            if (deps === null) siteProbe(go, forkNotLive);   /* rate-limited: let the img decide */
            else if (deps.length) go();
            else forkNotLive();
          })
          .catch(function () { siteProbe(go, go); });
      }
      else if (r.status === 403) siteProbe(go, go);   /* rate-limited: only the probe knows */
      else {
        reveal();   /* a genuine miss — now the 404 content has something to say */
        note.innerHTML = '🪐 No LightNode for <b>@' + cand + '</b> yet — ' +
          '<a href="/start">start yours</a>?';
      }
    })
    .catch(function () { siteProbe(go, go); });
})();
</script>
{% endif %}
