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
  var note = document.createElement('p');
  note.style.cssText = 'padding:0.8em 1em;background:#f0f6ff;border:1px solid #c7ddf7;border-radius:8px;font-size:0.95em';
  note.textContent = '🔭 Looking for @' + cand + '’s LightNode…';
  var h1 = main.querySelector('h1');
  if (h1 && h1.insertAdjacentElement) h1.insertAdjacentElement('afterend', note);
  else main.insertBefore(note, main.firstChild);

  if (CANON && cand.toLowerCase() === CANON.toLowerCase()) { location.replace('/'); return; }
  var dest = 'https://' + cand + '.github.io/lightcodepedia/';
  fetch('https://api.github.com/repos/' + cand + '/lightcodepedia')
    .then(function (r) {
      if (r.ok) {
        note.textContent = '🚀 Found — taking you to @' + cand + '’s LightNode…';
        location.replace(dest);
      } else if (r.status === 403) {
        location.replace(dest);   /* rate-limited: go optimistically */
      } else {
        note.innerHTML = '🪐 No LightNode for <b>@' + cand + '</b> yet — ' +
          '<a href="/start">start yours</a>?';
      }
    })
    .catch(function () { location.replace(dest); });
})();
</script>
{% endif %}
