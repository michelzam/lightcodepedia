---
title: PoC — Éditeur de fiches YAML
---

# PoC — Éditeur de fiches structurées (Paris révolutionnaire)

Preuve de concept **isolée** (`docs/paris/`) : lire une **fiche YAML structurée** →
la rendre dans un **formulaire typé piloté par un schéma** → la réécrire en YAML
**valide-schéma** (ordre de clés stable, aucun champ perdu), le tout **sur GitHub Pages**,
sans Sveltia ni backend. C'est le *test décisif nº 1* de Toni transformé en démo :
« éditer nos fiches structurées **sans les casser** ».

- **Sous-ensemble édité** (schéma) : `title` (texte), `gender` (select fermé),
  `professions` (liste), `periods` (relation par nom → époques).
- **Tout le reste de la fiche est préservé** tel quel (round-trip sans perte).
- Le panneau de droite montre le YAML **ré-émis en direct** à chaque frappe.
- Le bouton **Commiter** réutilise le PAT de l'éditeur pedia (icône ✏️ → `lc_ed_pat`) et
  l'API GitHub — même contrat que `edit_on_github`.

<div id="pfe" markdown="0">
  <div class="pfe-meta">
    <span class="pfe-tag" id="pfe-type">type</span>
    <b id="pfe-id">id</b> · <span id="pfe-slug" class="pfe-mut">slug</span>
  </div>
  <div class="pfe-cols">
    <section class="pfe-card">
      <h3>Formulaire typé (schéma → widgets)</h3>
      <div id="pfe-form"><p class="pfe-mut">Chargement…</p></div>
    </section>
    <section class="pfe-card">
      <h3>YAML ré-émis (round-trip valide-schéma)</h3>
      <pre id="pfe-yaml" class="pfe-yaml">…</pre>
      <p class="pfe-mut" id="pfe-integrity"></p>
    </section>
  </div>
  <section class="pfe-card pfe-commit">
    <h3>Commiter (optionnel — écrit via l'API GitHub)</h3>
    <div class="pfe-row">
      <label>Dépôt <input id="pfe-repo" placeholder="michelzam/lightcodepedia"></label>
      <label>Chemin <input id="pfe-path" value="docs/paris/sample/a-de-longpre.yaml"></label>
      <label>Branche <input id="pfe-branch" value="main"></label>
    </div>
    <div class="pfe-row">
      <button id="pfe-commit-btn" type="button">💾 Commiter le YAML ré-émis</button>
      <span id="pfe-status" class="pfe-mut"></span>
    </div>
    <p class="pfe-mut">Le PAT est lu dans <code>localStorage.lc_ed_pat</code> — renseigne-le d'abord
    via l'éditeur ✏️ en bas à droite. Pour écrire dans <code>noventa98/Paris-Rev</code> (privé),
    mets le dépôt + le chemin réel (<code>poc/content/persons/…</code>) et un PAT qui y a accès.</p>
  </section>
</div>

<script type="application/yaml" id="pfe-fiche">
id: a-de-longpre
slug: a-de-longpre
type: person
title: A. de Longpré
sortName: Longpré, A. de
professions:
  - homme politique
nationalities:
  - France
periods:
  - revolutions-de-1848
themes: []
addresses: []
bibliography: []
externalLinks: []
body: président
workflow:
  draft: false
  aiText: null
  edited: true
  validated: true
  reviewRequested: false
  reviewNote: Enrichi par IA (suggestions §7.2), revu et accepté.
entityType: person
gender: masculin
qualificatifs:
  - républicain
</script>

<style>
#pfe { margin: 1.5em 0; font-size: 0.95em; }
#pfe .pfe-meta { margin-bottom: 0.8em; }
#pfe .pfe-tag { background:#eef; color:#446; border-radius:4px; padding:0.1em 0.5em; font-size:0.8em; margin-right:0.5em; }
#pfe .pfe-mut { color:#888; }
#pfe .pfe-cols { display:flex; gap:1em; flex-wrap:wrap; align-items:flex-start; }
#pfe .pfe-card { flex:1 1 320px; border:1px solid #e3e3e3; border-radius:8px; padding:1em; background:#fff; }
#pfe .pfe-card h3 { margin:0 0 0.7em; font-size:0.95em; }
#pfe .pfe-yaml { background:#0f1720; color:#d6e2ef; padding:0.9em; border-radius:6px; overflow:auto; max-height:520px; white-space:pre; font-size:0.82em; line-height:1.45; }
#pfe .pfe-field { margin-bottom:0.9em; }
#pfe .pfe-field > label { display:block; font-weight:600; margin-bottom:0.25em; }
#pfe .pfe-field .pfe-hint { font-weight:400; color:#999; font-size:0.82em; }
#pfe input[type=text], #pfe select { width:100%; box-sizing:border-box; padding:0.4em 0.55em; border:1px solid #ccc; border-radius:5px; font:inherit; }
#pfe .pfe-listrow { display:flex; gap:0.4em; margin-bottom:0.35em; }
#pfe .pfe-listrow input { flex:1; }
#pfe .pfe-x { border:none; background:#f2f2f2; border-radius:5px; cursor:pointer; padding:0 0.6em; }
#pfe .pfe-add { border:1px dashed #bbb; background:#fafafa; border-radius:5px; cursor:pointer; padding:0.3em 0.7em; font-size:0.85em; }
#pfe .pfe-chips { display:flex; flex-wrap:wrap; gap:0.35em; margin-bottom:0.4em; }
#pfe .pfe-chip { background:#eef4ff; border:1px solid #cfe0ff; border-radius:14px; padding:0.15em 0.6em; font-size:0.85em; }
#pfe .pfe-chip button { border:none; background:transparent; cursor:pointer; color:#667; margin-left:0.3em; }
#pfe .pfe-row { display:flex; gap:0.8em; flex-wrap:wrap; align-items:center; margin-bottom:0.6em; }
#pfe .pfe-row label { font-size:0.85em; display:flex; flex-direction:column; gap:0.2em; }
#pfe .pfe-commit button { background:#2563eb; color:#fff; border:none; border-radius:6px; padding:0.5em 1em; cursor:pointer; font:inherit; }
</style>

<script>
(function () {
  "use strict";

  // ── Schéma du sous-ensemble édité (donnée, pas code) — miroir du config.yml Sveltia ──
  var SCHEMA = [
    { name: "title", label: "Nom affiché", widget: "string" },
    { name: "gender", label: "Genre", widget: "select",
      options: ["", "masculin", "féminin", "non-binaire", "inconnu"] },
    { name: "professions", label: "Professions / activités", widget: "list",
      hint: "Vocabulaire contrôlé v1.3 — forme masculin singulier" },
    { name: "periods", label: "Époques", widget: "relation", collection: "periods",
      hint: "Relation par nom → stocke le slug, affiche le titre" }
  ];

  // Ordre canonique de sérialisation (schéma persons). Les clés absentes sont sautées ;
  // les clés inconnues sont préservées, ajoutées à la fin.
  var PERSON_ORDER = ["id","slug","type","title","entityType","gender","sortName","bornName",
    "aka","image","birth","death","professions","qualificatifs","fate","nationalities",
    "periods","themes","addresses","bibliography","externalLinks","body","workflow"];

  // Index minimal d'époques pour le widget relation (en prod : index JSON pré-généré au build).
  var PERIODS = [
    { slug: "revolution-francaise", title: "Révolution française" },
    { slug: "revolutions-de-1848", title: "Révolutions de 1848" },
    { slug: "commune-de-paris", title: "Commune de Paris" },
    { slug: "second-empire", title: "Second Empire" },
    { slug: "troisieme-republique", title: "Troisième République" },
    { slug: "belle-epoque", title: "Belle Époque" },
    { slug: "entre-deux-guerres", title: "Entre-deux-guerres" },
    { slug: "ere-contemporaine", title: "Ère contemporaine" }
  ];

  var _rec = null;
  var _origKeys = [];

  function $(id) { return document.getElementById(id); }
  function rep(s, n) { var o = ""; for (var i = 0; i < n; i++) o += s; return o; }
  function isArr(v) { return Object.prototype.toString.call(v) === "[object Array]"; }
  function isObj(v) { return v && typeof v === "object" && !isArr(v); }
  function periodTitle(slug) {
    for (var i = 0; i < PERIODS.length; i++) if (PERIODS[i].slug === slug) return PERIODS[i].title;
    return slug;
  }
  function periodSlug(title) {
    var t = (title || "").toLowerCase().trim();
    for (var i = 0; i < PERIODS.length; i++) {
      if (PERIODS[i].title.toLowerCase() === t || PERIODS[i].slug === t) return PERIODS[i].slug;
    }
    return null;
  }

  // ── Sérialiseur YAML (schéma-ordonné, style bloc) ─────────────────────────
  function quote(s) { return '"' + s.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"'; }
  function scalarStr(s) {
    if (s === "") return '""';
    if (/^\s|\s$/.test(s)) return quote(s);
    if (/:\s/.test(s) || /:$/.test(s)) return quote(s);
    if (/\s#/.test(s)) return quote(s);
    if (/^[>|&*!%@`"'\[\]{}?,]/.test(s)) return quote(s);
    if (/^-(\s|$)/.test(s)) return quote(s);
    if (/^(true|false|null|~|yes|no|on|off)$/i.test(s)) return quote(s);
    if (/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s)) return quote(s);
    return s;
  }
  function scalarInline(v, pad) {
    if (v === null) return "null";
    var t = typeof v;
    if (t === "number" || t === "boolean") return String(v);
    var s = String(v);
    if (s.indexOf("\n") !== -1) {
      var lines = s.replace(/\n+$/, "").split("\n");
      var out = "|-";
      for (var i = 0; i < lines.length; i++) out += "\n" + pad + "  " + lines[i];
      return out;
    }
    return scalarStr(s);
  }
  function orderedKeys(map, order) {
    var keys = [], seen = {}, k, i;
    if (order) {
      for (i = 0; i < order.length; i++) { k = order[i]; if (map.hasOwnProperty(k)) { keys.push(k); seen[k] = 1; } }
    }
    for (k in map) if (map.hasOwnProperty(k) && !seen[k]) keys.push(k);
    return keys;
  }
  function emitMap(map, indent, order) {
    var pad = rep("  ", indent), keys = orderedKeys(map, order), out = [], i;
    for (i = 0; i < keys.length; i++) out.push(emitKV(map, keys[i], indent));
    return out.join("\n");
  }
  function emitKV(map, k, indent) {
    var pad = rep("  ", indent), v = map[k], i;
    if (v === null || v === undefined) return pad + k + ": null";
    if (isArr(v)) {
      if (v.length === 0) return pad + k + ": []";
      var o = pad + k + ":";
      for (i = 0; i < v.length; i++) o += "\n" + emitSeqItem(v[i], indent + 1);
      return o;
    }
    if (isObj(v)) return pad + k + ":\n" + emitMap(v, indent + 1, null);
    return pad + k + ": " + scalarInline(v, pad);
  }
  function emitSeqItem(item, indent) {
    var pad = rep("  ", indent);
    if (isObj(item)) {
      var mt = emitMap(item, indent + 1, null), lead = rep("  ", indent + 1), lines = mt.split("\n");
      lines[0] = pad + "- " + lines[0].substring(lead.length);
      return lines.join("\n");
    }
    if (isArr(item)) return pad + "- []";
    return pad + "- " + scalarInline(item, pad);
  }
  function toYaml(rec) { return emitMap(rec, 0, PERSON_ORDER) + "\n"; }

  // ── Rendu ─────────────────────────────────────────────────────────────────
  function renderHead() {
    $("pfe-type").textContent = _rec.type || "?";
    $("pfe-id").textContent = _rec.id || "(sans id)";
    $("pfe-slug").textContent = _rec.slug || "";
  }
  function renderYaml() {
    $("pfe-yaml").textContent = toYaml(_rec);
    var lost = 0, k;
    for (var i = 0; i < _origKeys.length; i++) { k = _origKeys[i]; if (!_rec.hasOwnProperty(k)) lost++; }
    $("pfe-integrity").textContent = lost === 0
      ? "✔ " + _origKeys.length + " clés d'origine préservées — aucune perte."
      : "⚠ " + lost + " clé(s) perdue(s).";
  }
  function field(label, hint, node) {
    var wrap = document.createElement("div"); wrap.className = "pfe-field";
    var lab = document.createElement("label"); lab.textContent = label;
    if (hint) { var h = document.createElement("span"); h.className = "pfe-hint"; h.textContent = " — " + hint; lab.appendChild(h); }
    wrap.appendChild(lab); wrap.appendChild(node); return wrap;
  }
  function renderForm() {
    var box = $("pfe-form"); box.innerHTML = "";
    for (var i = 0; i < SCHEMA.length; i++) box.appendChild(widget(SCHEMA[i]));
  }
  function widget(f) {
    if (f.widget === "string") {
      var inp = document.createElement("input"); inp.type = "text"; inp.value = _rec[f.name] || "";
      inp.oninput = function () { _rec[f.name] = inp.value; renderYaml(); };
      return field(f.label, f.hint, inp);
    }
    if (f.widget === "select") {
      var sel = document.createElement("select"), j;
      for (j = 0; j < f.options.length; j++) {
        var op = document.createElement("option"); op.value = f.options[j];
        op.textContent = f.options[j] === "" ? "—" : f.options[j];
        if ((_rec[f.name] || "") === f.options[j]) op.selected = true;
        sel.appendChild(op);
      }
      sel.onchange = function () {
        if (sel.value === "") delete _rec[f.name]; else _rec[f.name] = sel.value;
        renderYaml();
      };
      return field(f.label, f.hint, sel);
    }
    if (f.widget === "list") {
      if (!isArr(_rec[f.name])) _rec[f.name] = [];
      var host = document.createElement("div");
      drawList(host, f); return field(f.label, f.hint, host);
    }
    if (f.widget === "relation") {
      if (!isArr(_rec[f.name])) _rec[f.name] = [];
      var host2 = document.createElement("div");
      drawRelation(host2, f); return field(f.label, f.hint, host2);
    }
    return field(f.label, f.hint, document.createTextNode("(widget inconnu)"));
  }
  function drawList(host, f) {
    host.innerHTML = ""; var arr = _rec[f.name], i;
    for (i = 0; i < arr.length; i++) host.appendChild(listRow(f, i));
    var add = document.createElement("button"); add.type = "button"; add.className = "pfe-add";
    add.textContent = "＋ ajouter";
    add.onclick = function () { _rec[f.name].push(""); drawList(host, f); renderYaml(); };
    host.appendChild(add);
  }
  function listRow(f, idx) {
    var row = document.createElement("div"); row.className = "pfe-listrow";
    var inp = document.createElement("input"); inp.type = "text"; inp.value = _rec[f.name][idx];
    inp.oninput = function () { _rec[f.name][idx] = inp.value; renderYaml(); };
    var x = document.createElement("button"); x.type = "button"; x.className = "pfe-x"; x.textContent = "×";
    x.onclick = function () { _rec[f.name].splice(idx, 1); drawList(inp.parentNode.parentNode, f); renderYaml(); };
    row.appendChild(inp); row.appendChild(x); return row;
  }
  function drawRelation(host, f) {
    host.innerHTML = "";
    var chips = document.createElement("div"); chips.className = "pfe-chips";
    var arr = _rec[f.name], i;
    for (i = 0; i < arr.length; i++) chips.appendChild(relChip(f, arr[i], host));
    host.appendChild(chips);
    var row = document.createElement("div"); row.className = "pfe-listrow";
    var inp = document.createElement("input"); inp.type = "text";
    inp.setAttribute("list", "pfe-periods-dl"); inp.placeholder = "Chercher une époque par nom…";
    var dl = document.getElementById("pfe-periods-dl");
    if (!dl) {
      dl = document.createElement("datalist"); dl.id = "pfe-periods-dl";
      for (i = 0; i < PERIODS.length; i++) { var o = document.createElement("option"); o.value = PERIODS[i].title; dl.appendChild(o); }
      document.body.appendChild(dl);
    }
    var add = document.createElement("button"); add.type = "button"; add.className = "pfe-add"; add.textContent = "＋";
    function commitPick() {
      var slug = periodSlug(inp.value);
      if (!slug) { inp.value = ""; return; }
      if (_rec[f.name].indexOf(slug) === -1) _rec[f.name].push(slug);
      inp.value = ""; drawRelation(host, f); renderYaml();
    }
    add.onclick = commitPick;
    inp.onkeydown = function (e) { if (e.key === "Enter") { e.preventDefault(); commitPick(); } };
    row.appendChild(inp); row.appendChild(add); host.appendChild(row);
  }
  function relChip(f, slug, host) {
    var c = document.createElement("span"); c.className = "pfe-chip";
    c.appendChild(document.createTextNode(periodTitle(slug)));
    var b = document.createElement("button"); b.type = "button"; b.textContent = "×";
    b.onclick = function () {
      var idx = _rec[f.name].indexOf(slug);
      if (idx !== -1) _rec[f.name].splice(idx, 1);
      drawRelation(host, f); renderYaml();
    };
    c.appendChild(b); return c;
  }

  // ── Commit (API GitHub — même contrat que edit_on_github) ─────────────────
  function b64e(s) { return btoa(unescape(encodeURIComponent(s))); }
  function wireCommit() {
    $("pfe-commit-btn").onclick = function () {
      var pat = localStorage.getItem("lc_ed_pat");
      var repo = $("pfe-repo").value || localStorage.getItem("lc_ed_repo") || "";
      var path = $("pfe-path").value, branch = $("pfe-branch").value || "main";
      var st = $("pfe-status");
      if (!pat) { st.textContent = "Aucun PAT dans lc_ed_pat — renseigne-le via ✏️."; return; }
      if (!repo || !path) { st.textContent = "Dépôt et chemin requis."; return; }
      st.textContent = "Lecture du SHA…";
      var api = "https://api.github.com/repos/" + repo + "/contents/" + path;
      var H = { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
      fetch(api + "?ref=" + encodeURIComponent(branch), { headers: H })
        .then(function (r) { return r.json(); })
        .then(function (cur) {
          var body = { message: "PoC: édition fiche " + (_rec.id || path), content: b64e(toYaml(_rec)), branch: branch };
          if (cur && cur.sha) body.sha = cur.sha;
          return fetch(api, { method: "PUT", headers: H, body: JSON.stringify(body) }).then(function (r) { return r.json(); });
        })
        .then(function (res) {
          st.textContent = res && res.commit ? "✔ Commit " + res.commit.sha.substring(0, 7) : "✖ " + ((res && res.message) || "échec");
        })
        .catch(function (e) { st.textContent = "✖ " + e.message; });
    };
  }

  // ── Boot ──────────────────────────────────────────────────────────────────
  function boot() {
    var raw = $("pfe-fiche").textContent;
    try { _rec = window.jsyaml.load(raw); }
    catch (e) { $("pfe-form").innerHTML = "<p style='color:#c00'>YAML illisible : " + e.message + "</p>"; return; }
    _origKeys = []; for (var k in _rec) if (_rec.hasOwnProperty(k)) _origKeys.push(k);
    renderHead(); renderForm(); renderYaml(); wireCommit();
  }
  if (window.jsyaml) { boot(); }
  else {
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4.1.0/dist/js-yaml.min.js";
    s.onload = boot;
    s.onerror = function () { $("pfe-form").innerHTML = "<p style='color:#c00'>Échec du chargement de js-yaml (CDN).</p>"; };
    document.head.appendChild(s);
  }
})();
</script>

---

## Comment ça marche (et pourquoi c'est fidèle à ta philosophie)

**Runtime** : page statique GitHub Pages + JS navigateur + API GitHub. Aucun serveur, aucune base,
aucun Sveltia. Le YAML est parsé par `js-yaml` (jsDelivr, comme les autres composants pedia) ;
la **ré-émission** est un sérialiseur maison **ordonné par le schéma** (clés stables, `null` gérés,
clés inconnues préservées) — c'est un round-trip **valide-schéma**, pas octet-pour-octet, exactement
comme Sveltia.

**Fidélité à « md/kd/IAL »** : ici le PoC est volontairement câblé à la main (un `<script>` dans la page).
La productisation consiste à replier ce moteur dans un **composant** `_includes/` — comme `map`/`form`/`datagrid` —
dont l'usage devient une simple directive IAL, ex. un bloc + `{: .fiche-editor collection="persons" }`.
Le moteur (JS) vit alors **une seule fois** dans l'include ; l'auteur, lui, n'écrit que du md/kramdown/IAL.
C'est le contrat déjà en vigueur pour tous les composants pedia.

**Ce qui manque encore** pour la parité complète avec le `config.yml` (hors périmètre de ce PoC) :
les widgets `object`/`image` imbriqués, la validation de vocabulaire fermé sur `professions`,
l'index de relations pré-généré au build (ici : liste minimale en dur), et le passage `PUT main` → branche/PR
pour le workflow brouillon→revue→publié.
