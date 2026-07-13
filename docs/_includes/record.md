<!-- © 2026 KarmicSoft — LightCode Platform. Proprietary, All Rights Reserved. License: /license -->
{%- comment -%}
Record — a schema-driven record editor: typed form (lcSchema) + live preview
with in-place WYSIWYG + lossless YAML round-trip (lcYaml) + optional in-form AI
+ optional git commit (edit_on_github contract). Domain-agnostic: schema and the
relation index are supplied by the author as .dataset blocks.

  ```json
  [ {"name":"title","label":"Nom","widget":"string","wysiwyg":true},
    {"name":"periods","label":"Époques","widget":"relation","collection":"periods","multiple":true} ]
  ```
  {: .dataset #person_schema }

  ```json
  { "periods":[{"slug":"commune-de-1871","title":"Commune de 1871"}] }
  ```
  {: .dataset #paris_index }

  ```yaml
  title: A. de Longpré
  periods: [revolutions-de-1848]
  body: président
  ```
  {: .record schema="person_schema" index="paris_index" ai="true" commit="true" }

Knobs:
  schema="id"   required — a .dataset holding the schema array
  index="id"    optional — a .dataset holding the relation index
                {coll:[{slug,title,lat,lng}]} — entries with lat/lng are mappable
  map="true"    show a map of the record's geolocated points (reuses .map);
                any index entry with lat/lng whose slug appears in the record
  mapengine=""  "leaflet" for Leaflet+OSM, else default MapLibre
  mapheight=""  map height in px (default 240)
  ai="true"     show the in-form AI panel (Suggest → Apply/Ignore)
  endpoint="…"  default AI endpoint URL (author-configurable; learner can override)
  commit="true" show the git-commit panel (PAT from edit_on_github's lc_ed_pat)
  path="…"      default repo path for commit
  #id           optional

Round-trip preserves the record's own key order (minimal git diffs), keeps dates
as strings, and uses faithful | / |- / |+ chomping. Auto-included by default.html.
{%- endcomment -%}

<style>
.lc-rec { margin: 1.5em 0; font-size: 0.95em; }
.lc-rec .lc-rec-cols { display: flex; gap: 1em; flex-wrap: wrap; align-items: flex-start; }
.lc-rec .lc-rec-card { flex: 1 1 300px; border: 1px solid #e3e3e3; border-radius: 8px; padding: 1em; background: #fff; }
.lc-rec .lc-rec-card h3 { margin: 0 0 0.7em; font-size: 0.95em; }
.lc-rec .lc-rec-yaml { background: #0f1720; color: #d6e2ef; padding: 0.9em; border-radius: 6px; overflow: auto; max-height: 520px; white-space: pre; font-size: 0.8em; line-height: 1.45; }
.lc-rec .lc-rec-mut { color: #888; font-size: 0.9em; }
.lc-rec .lc-rec-row { display: flex; gap: 0.8em; flex-wrap: wrap; align-items: center; margin-bottom: 0.6em; }
.lc-rec .lc-rec-row > label { font-size: 0.85em; display: flex; flex-direction: column; gap: 0.2em; }
.lc-rec .lc-rec-row input { padding: 0.4em 0.55em; border: 1px solid #ccc; border-radius: 5px; font: inherit; }
.lc-rec button { font: inherit; cursor: pointer; }
.lc-rec .lc-rec-go { background: #2563eb; color: #fff; border: none; border-radius: 6px; padding: 0.5em 1em; }
.lc-rec .lc-rec-x { border: none; background: #f2f2f2; border-radius: 5px; padding: 0 0.6em; }
.lc-rec .lc-rec-add { border: 1px dashed #bbb; background: #fafafa; border-radius: 5px; padding: 0.3em 0.7em; font-size: 0.85em; }
.lc-rec .lc-rec-sug-row { display: flex; align-items: center; gap: 0.5em; padding: 0.4em 0; border-bottom: 1px solid #f2f2f2; }
.lc-rec .lc-rec-sug-row span { flex: 1; font-size: 0.9em; }
.lc-rec .lc-rec-sug-empty { padding: 0.45em 0.6em; color: #c0392b; font-size: 0.85em; }
.lc-rec .pv-row { margin: 0.25em 0; }
.lc-rec .pv-lab { font-weight: 600; color: #556; font-size: 0.85em; margin-right: 0.3em; }
.lc-rec .pv-chip { display: inline-block; background: #f1f3f6; border-radius: 12px; padding: 0.1em 0.55em; font-size: 0.85em; margin: 0.1em 0.15em 0.1em 0; }
.lc-rec .pv-chip.pv-rel { background: #eef4ff; border: 1px solid #cfe0ff; }
.lc-rec .pv-edit { cursor: text; border-radius: 3px; transition: box-shadow .1s; }
.lc-rec .pv-edit:hover { box-shadow: inset 0 -2px 0 #cfe0ff; }
.lc-rec .pv-edit:focus { outline: 2px solid #2563eb; outline-offset: 2px; background: #fbfdff; }
.lc-rec .pv-name { font-size: 1.25em; font-weight: 600; margin: 0 0 0.15em; }
.lc-rec .pv-name.pv-edit:empty::before { content: "(click to name)"; color: #bbb; }
.lc-rec .pv-body { margin-top: 0.7em; }
.lc-rec .pv-body p { margin: 0.4em 0; }
.lc-rec .pv-body.pv-edit:empty::before { content: "(click to add text)"; color: #bbb; }
</style>

<script>
(function () {
  if (window._lcRecordReady) return; window._lcRecordReady = true;
  "use strict";

  function el(t, c) { var e = document.createElement(t); if (c) e.className = c; return e; }
  function isArr(v) { return Object.prototype.toString.call(v) === "[object Array]"; }
  function isObj(v) { return v && typeof v === "object" && !isArr(v); }
  function escHtml(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function escAttr(s) { return escHtml(s).replace(/"/g, "&quot;"); }
  function b64e(s) { return btoa(unescape(encodeURIComponent(s))); }

  // Read a .dataset by id, now or when it registers.
  function onDataset(id, cb) {
    if (!id) { cb(null); return; }
    if (window.lcDatasets && window.lcDatasets[id] !== undefined) { cb(window.lcDatasets[id]); return; }
    window.lcDatasetListeners = window.lcDatasetListeners || {};
    (window.lcDatasetListeners[id] = window.lcDatasetListeners[id] || []).push(cb);
  }

  // Generic geo: the index owns coordinates; plot every index entry that has
  // lat/lng AND whose slug appears anywhere in the record. Works for any shape
  // (person.addresses, event.location.points, …) — no per-record config.
  function collectSlugs(v, out) {
    if (v == null) return;
    if (typeof v === "string") { out[v] = 1; return; }
    if (isArr(v)) { for (var i = 0; i < v.length; i++) collectSlugs(v[i], out); return; }
    if (isObj(v)) { for (var k in v) if (v.hasOwnProperty(k)) collectSlugs(v[k], out); }
  }
  function geoPoints(record, index) {
    var used = {}; collectSlugs(record, used); var pts = [], coll, i, e, lng;
    for (coll in index) {
      if (!index.hasOwnProperty(coll)) continue;
      var arr = index[coll] || [];
      for (i = 0; i < arr.length; i++) {
        e = arr[i]; lng = e && (e.lng != null ? e.lng : e.lon);
        if (e && e.lat != null && lng != null && used[e.slug]) pts.push({ lat: e.lat, lon: lng, label: e.title || e.slug });
      }
    }
    return pts;
  }

  function mdMini(t) {
    var paras = String(t == null ? "" : t).split(/\n\s*\n/), h = "", i;
    for (i = 0; i < paras.length; i++) if (paras[i].trim()) h += "<p>" + escHtml(paras[i].trim()).replace(/\n/g, "<br>") + "</p>";
    return h;
  }

  function upgrade(el0) {
    var code = el0.querySelector("code");
    var raw = (code ? code.textContent : el0.textContent);
    var schemaId = el0.getAttribute("schema") || "";
    var indexId = el0.getAttribute("index") || "";
    var id = el0.id || "";

    var wrap = el("div", "lc-rec");
    if (id) wrap.setAttribute("data-lc-id", id);
    wrap.innerHTML =
      '<div class="lc-rec-cols">' +
        '<section class="lc-rec-card"><h3>Form (schema → widgets)</h3><div class="lc-rec-form"></div></section>' +
        '<section class="lc-rec-card"><h3>Preview — ✎ editable</h3><div class="lc-rec-preview"></div></section>' +
        '<section class="lc-rec-card"><h3>YAML (lossless round-trip)</h3><pre class="lc-rec-yaml">…</pre><p class="lc-rec-mut lc-rec-integrity"></p></section>' +
      '</div>';
    el0.parentNode.replaceChild(wrap, el0);

    var state = { rec: {}, schema: [], index: {}, origKeys: [] };

    function syncYaml() {
      wrap.querySelector(".lc-rec-yaml").textContent = window.lcYaml.dump(state.rec, null);
      var lost = 0, i, k;
      for (i = 0; i < state.origKeys.length; i++) { k = state.origKeys[i]; if (!state.rec.hasOwnProperty(k)) lost++; }
      wrap.querySelector(".lc-rec-integrity").textContent = lost === 0
        ? "✔ " + state.origKeys.length + " keys preserved — no loss."
        : "⚠ " + lost + " key(s) lost.";
    }
    function renderPreview() {
      var box = wrap.querySelector(".lc-rec-preview");
      box.innerHTML = genericPreview(state.rec, state.schema, state.index);
      wireInlineEdit(box);
    }
    function refresh() { syncYaml(); renderPreview(); renderMap(false); }  // value edit: keep form DOM
    function rebuildAll() { buildForm(); refresh(); }          // structural: rebuild form too

    // Map (map="true"): reuse the .map component, fed generic points from the
    // record + index. Rebuilt only when the point set changes (not on typing).
    var _mapCard = null, _mapSig = null;
    var mapEngine = el0.getAttribute("mapengine") || "", mapH = el0.getAttribute("mapheight") || "240";
    function renderMap(force) {
      if (!_mapCard) return;
      var pts = geoPoints(state.rec, state.index), sig = JSON.stringify(pts);
      _mapCard.querySelector(".lc-rec-map-note").textContent =
        pts.length ? (pts.length + " geolocated point(s).") : "No geolocated points in this record.";
      if (!force && sig === _mapSig) return;
      _mapSig = sig;
      var host = _mapCard.querySelector(".lc-rec-map"); host.innerHTML = "";
      if (!pts.length) return;
      var pre = document.createElement("pre");
      pre.className = "map";
      if (mapEngine) pre.setAttribute("engine", mapEngine);
      pre.setAttribute("height", mapH);
      pre.textContent = JSON.stringify(pts);
      host.appendChild(pre);
      if (window.lcScanElement) window.lcScanElement(host);
    }
    function addMap() {
      _mapCard = el("section", "lc-rec-card");
      _mapCard.innerHTML = '<h3>Map (from the record’s points)</h3><div class="lc-rec-map"></div><p class="lc-rec-mut lc-rec-map-note"></p>';
      wrap.appendChild(_mapCard);
      renderMap(true);
    }

    function genericPreview(rec, schema, index) {
      var h = '<div class="pv-fiche">', i, fd, v;
      for (i = 0; i < schema.length; i++) {
        fd = schema[i]; v = rec[fd.name];
        if (fd.wysiwyg) {
          var single = fd.widget !== "text" && fd.widget === "string";
          h += '<div class="pv-edit ' + (single ? "pv-name" : "pv-body") + '" contenteditable="true" data-fld="' +
               escAttr(fd.name) + '" data-single="' + (single ? "1" : "0") + '">' +
               (single ? escHtml(v || "") : mdMini(v || "")) + '</div>';
        } else if (isArr(v) && v.length) {
          h += '<div class="pv-row"><span class="pv-lab">' + escHtml(fd.label || fd.name) + '</span>';
          for (var j = 0; j < v.length; j++) {
            var item = v[j], rel = fd.collection && window.lcSchema;
            var label = rel ? window.lcSchema.relTitle(index, fd.collection, item)
                            : (isObj(item) || isArr(item) ? "•" : String(item));
            h += '<span class="pv-chip' + (fd.collection ? " pv-rel" : "") + '">' + escHtml(label) + '</span>';
          }
          h += '</div>';
        } else if (v != null && v !== "" && !isArr(v) && !isObj(v)) {
          h += '<div class="pv-row"><span class="pv-lab">' + escHtml(fd.label || fd.name) + '</span> ' + escHtml(String(v)) + '</div>';
        }
      }
      return h + '</div>';
    }
    function wireInlineEdit(box) {
      var els = box.querySelectorAll(".pv-edit"), i;
      for (i = 0; i < els.length; i++) {
        (function (e) {
          var fld = e.getAttribute("data-fld"), single = e.getAttribute("data-single") === "1";
          function read() { return (single ? e.textContent : e.innerText).replace(/ /g, " "); }
          e.oninput = function () { state.rec[fld] = read(); syncYaml(); };     // typing: only re-sync YAML (keep caret)
          e.onblur = function () { state.rec[fld] = read().replace(/\n+$/, ""); rebuildAll(); };
          if (single) e.onkeydown = function (ev) { if (ev.key === "Enter" || ev.keyCode === 13) { ev.preventDefault(); e.blur(); } };
        })(els[i]);
      }
    }

    function buildForm() {
      var box = wrap.querySelector(".lc-rec-form");
      if (window.lcSchema) window.lcSchema.buildForm(box, state.rec, state.schema, state.index, refresh);
      else box.textContent = "lcSchema not loaded";
    }

    // ── optional panels ──────────────────────────────────────────────────────
    function addAI() {
      var card = el("section", "lc-rec-card"), endpoint = el0.getAttribute("endpoint") || "";
      card.innerHTML = '<h3>AI — “suggests, you decide”</h3>' +
        '<div class="lc-rec-row"><button type="button" class="lc-rec-ai-btn">🪄 Suggest</button>' +
        '<input class="lc-rec-ai-endpoint" placeholder="AI endpoint URL (optional)" style="flex:1;min-width:180px"></div>' +
        '<div class="lc-rec-ai"></div>';
      wrap.appendChild(card);
      if (endpoint) card.querySelector(".lc-rec-ai-endpoint").value = endpoint;
      card.querySelector(".lc-rec-ai-btn").onclick = function () {
        var box = card.querySelector(".lc-rec-ai"), url = card.querySelector(".lc-rec-ai-endpoint").value.trim();
        box.innerHTML = "<p class='lc-rec-mut'>Analysing…</p>";
        if (url) {
          fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ record: state.rec, schema: state.schema }) })
            .then(function (r) { return r.json(); })
            .then(function (d) { renderSuggestions(box, d.suggestions || [], false); })
            .catch(function (e) { box.innerHTML = "<p class='lc-rec-sug-empty'>AI endpoint unreachable: " + escHtml(e.message) + "</p>"; });
        } else { renderSuggestions(box, localSuggest(), true); }
      };
    }
    function localSuggest() {                                   // generic, domain-agnostic fallback
      var s = [], i, fd;
      for (i = 0; i < state.schema.length; i++) {
        fd = state.schema[i];
        var v = state.rec[fd.name];
        if (fd.wysiwyg && (v == null || !String(v).trim())) {
          (function (name, label) {
            s.push({ text: "“" + label + "” is empty → insert a stub to fill in",
                     apply: function (r) { r[name] = "TODO: " + label + "."; } });
          })(fd.name, fd.label || fd.name);
        }
      }
      if (!s.length) s.push({ text: "No structural suggestion (set an endpoint for real AI).", apply: null });
      return s;
    }
    function renderSuggestions(box, list, demo) {
      box.innerHTML = "";
      if (demo) { var n = el("p", "lc-rec-mut"); n.textContent = "Local demo (no AI call). Set an endpoint URL for real suggestions."; box.appendChild(n); }
      list.forEach(function (sg) {
        var row = el("div", "lc-rec-sug-row"), t = el("span"); t.textContent = sg.text || sg.label || "(suggestion)"; row.appendChild(t);
        var ap = typeof sg.apply === "function" ? sg.apply : (sg.field ? function (r) { r[sg.field] = sg.value; } : null);
        if (ap) { var b = el("button", "lc-rec-add"); b.type = "button"; b.textContent = "Apply"; b.onclick = function () { ap(state.rec); rebuildAll(); row.style.opacity = 0.5; b.disabled = true; }; row.appendChild(b); }
        var ig = el("button", "lc-rec-x"); ig.type = "button"; ig.textContent = "Ignore"; ig.onclick = function () { if (row.parentNode) row.parentNode.removeChild(row); }; row.appendChild(ig);
        box.appendChild(row);
      });
    }
    function addCommit() {
      var card = el("section", "lc-rec-card");
      card.innerHTML = '<h3>💾 Commit to git</h3>' +
        '<div class="lc-rec-row"><label>Repo <input class="lc-rec-repo" placeholder="owner/repo"></label>' +
        '<label>Path <input class="lc-rec-path" value="' + escAttr(el0.getAttribute("path") || "") + '"></label>' +
        '<label>Branch <input class="lc-rec-branch" value="main"></label></div>' +
        '<div class="lc-rec-row"><button type="button" class="lc-rec-go lc-rec-commit">💾 Commit YAML</button>' +
        '<span class="lc-rec-mut lc-rec-status"></span></div>' +
        '<p class="lc-rec-mut">Uses the edit_on_github PAT (lc_ed_pat). Editing needs no account; only the commit writes to git.</p>';
      wrap.appendChild(card);
      card.querySelector(".lc-rec-commit").onclick = function () {
        var st = card.querySelector(".lc-rec-status");
        var pat = localStorage.getItem("lc_ed_pat");
        var repo = card.querySelector(".lc-rec-repo").value || localStorage.getItem("lc_ed_repo") || "";
        var path = card.querySelector(".lc-rec-path").value, branch = card.querySelector(".lc-rec-branch").value || "main";
        if (!pat) { st.textContent = "No PAT in lc_ed_pat — set it via ✏️ (edit_on_github)."; return; }
        if (!repo || !path) { st.textContent = "Repo and path required."; return; }
        st.textContent = "Reading SHA…";
        var api = "https://api.github.com/repos/" + repo + "/contents/" + path;
        var H = { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
        fetch(api + "?ref=" + encodeURIComponent(branch), { headers: H, cache: "no-store" })
          .then(function (r) { return r.json(); })
          .then(function (cur) {
            var body = { message: "record: edit " + (state.rec.id || path), content: b64e(window.lcYaml.dump(state.rec, null)), branch: branch };
            if (cur && cur.sha) body.sha = cur.sha;
            return fetch(api, { method: "PUT", headers: H, body: JSON.stringify(body) }).then(function (r) { return r.json(); });
          })
          .then(function (res) { st.textContent = res && res.commit ? "✔ Commit " + res.commit.sha.substring(0, 7) : "✖ " + ((res && res.message) || "failed"); })
          .catch(function (e) { st.textContent = "✖ " + e.message; });
      };
    }

    // ── boot: load libs + schema/index, then render ──────────────────────────
    function start() {
      onDataset(schemaId, function (sch) {
        state.schema = isArr(sch) ? sch : (sch && isArr(sch.fields) ? sch.fields : []);
        onDataset(indexId, function (idx) {
          state.index = isObj(idx) ? idx : {};
          window.lcYaml.ready(function () {
            try { state.rec = window.lcYaml.load(raw) || {}; }
            catch (e) { wrap.querySelector(".lc-rec-form").innerHTML = "<p style='color:#c00'>Unreadable YAML: " + escHtml(e.message) + "</p>"; return; }
            state.origKeys = []; for (var k in state.rec) if (state.rec.hasOwnProperty(k)) state.origKeys.push(k);
            buildForm(); refresh();
            if ((el0.getAttribute("map") || "") === "true") addMap();
            if ((el0.getAttribute("ai") || "") === "true") addAI();
            if ((el0.getAttribute("commit") || "") === "true") addCommit();
          });
        });
      });
    }
    start();
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader(".highlighter-rouge.record, pre.record", upgrade);
})();
</script>
