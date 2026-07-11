---
title: PoC — Éditeur de fiches YAML
---

# Pour Toni — est-ce ce que tu veux ?

Ce prototype tourne **sur lightcodepedia (GitHub Pages), sans serveur, sans base, sans Sveltia**.
Il édite tes fiches YAML **structurées** avec un formulaire **piloté par le schéma** — et il te pose
la question : **est-ce la direction que tu veux ?**

En direct (essaie sur ton tél) :

- **bascule Personnage ⇄ Événement** — *deux schémas différents, un seul moteur* (c'est le test de généralisation) ;
- édite : texte, listes, **vocabulaire fermé** (menu), **relations par nom** (recherche → puce), **objets imbriqués**
  (la datation), **liste d'objets** (les points d'un itinéraire, chacun relié à une adresse) ;
- à droite : le **YAML ré-émis** sans perte de champ ; au milieu : l'**aperçu rendu** — l'aperçu fidèle que Sveltia n'a pas ;
- **💾 Commiter** écrit dans git via l'API GitHub (historique, PR, workflow, comme d'habitude).

**Est-ce ce que tu veux ?** Si oui, la suite est de replier ce moteur dans un composant réutilisable
(usage 100 % Markdown/IAL) et de le brancher sur le vrai corpus. Dis-nous ce qui manque.

<div id="pfe" markdown="0">
  <div class="pfe-meta">
    <span class="pfe-tag" id="pfe-type">type</span>
    <b id="pfe-id">id</b> · <span id="pfe-slug" class="pfe-mut">slug</span>
  </div>
  <div class="pfe-row">
    <label>Type de fiche
      <select id="pfe-type-sel">
        <option value="persons">Personnage</option>
        <option value="events">Événement</option>
      </select>
    </label>
  </div>
  <div class="pfe-cols">
    <section class="pfe-card">
      <h3>Formulaire typé (schéma → widgets)</h3>
      <div id="pfe-form"><p class="pfe-mut">Chargement…</p></div>
      <p id="pfe-source" class="pfe-mut"></p>
    </section>
    <section class="pfe-card">
      <h3>Aperçu rendu (live) — ✎ éditable</h3>
      <p class="pfe-mut">Clique le <b>nom</b> ou la <b>bio</b> pour éditer directement sur le rendu (WYSIWYG).</p>
      <div id="pfe-preview" class="pfe-preview"></div>
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
      <button id="pfe-reload-btn" type="button">🔄 Recharger depuis le fichier</button>
      <span id="pfe-status" class="pfe-mut"></span>
    </div>
    <p class="pfe-mut">Le PAT est lu dans <code>localStorage.lc_ed_pat</code> — renseigne-le d'abord
    via l'éditeur ✏️ en bas à droite. Pour écrire dans <code>noventa98/Paris-Rev</code> (privé),
    mets le dépôt + le chemin réel et un PAT qui y a accès.</p>
  </section>
</div>

<script type="application/yaml" id="pfe-fiche-persons">
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

<script type="application/yaml" id="pfe-fiche-events">
id: 4eme-siege-de-la-maison-d-edition-gallimard
slug: 4eme-siege-de-la-maison-d-edition-gallimard
type: event
title: 4ème siège de la maison d'édition Gallimard
daterange:
  startYear: 1930
  endYear: 1945
  precision: year
location:
  ordered: false
  approximate: false
  points:
    - street: 5-rue-sebastien-bottin
      primary: true
      note: Siège de la maison d'édition Gallimard
epochs:
  - entre-deux-guerres
themes:
  - litterature
districts:
  - 7
people:
  - albert-camus
  - robert-desnos
  - paul-eluard
  - jules-supervielle
  - roger-martin-du-gard
bibliography:
  - id: dictionnaire-historique-des-rues-de-paris-hillairet-jacques
    page: t2 p 584
externalLinks: []
body: ""
workflow:
  draft: false
  aiText: null
  edited: false
  validated: false
  reviewRequested: true
  reviewNote: Migré de l'export XWiki 2026-04-05 — à vérifier.
</script>

<style>
#pfe { margin: 1.5em 0; font-size: 0.95em; }
#pfe .pfe-meta { margin-bottom: 0.6em; }
#pfe .pfe-tag { background:#eef; color:#446; border-radius:4px; padding:0.1em 0.5em; font-size:0.8em; margin-right:0.5em; }
#pfe .pfe-mut { color:#888; }
#pfe .pfe-cols { display:flex; gap:1em; flex-wrap:wrap; align-items:flex-start; }
#pfe .pfe-card { flex:1 1 300px; border:1px solid #e3e3e3; border-radius:8px; padding:1em; background:#fff; }
#pfe .pfe-card h3 { margin:0 0 0.7em; font-size:0.95em; }
#pfe .pfe-yaml { background:#0f1720; color:#d6e2ef; padding:0.9em; border-radius:6px; overflow:auto; max-height:520px; white-space:pre; font-size:0.8em; line-height:1.45; }
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
#pfe .pfe-row > label { font-size:0.85em; display:flex; flex-direction:column; gap:0.2em; }
#pfe .pfe-commit button { background:#2563eb; color:#fff; border:none; border-radius:6px; padding:0.5em 1em; cursor:pointer; font:inherit; }
#pfe .pfe-group { border-left:3px solid #e3e3e3; padding-left:0.8em; margin:0.2em 0; }
#pfe .pfe-item { border:1px solid #eee; border-radius:6px; padding:0.6em 0.8em; margin-bottom:0.5em; }
#pfe .pfe-item-hd { display:flex; justify-content:space-between; align-items:center; font-weight:600; color:#556; font-size:0.82em; margin-bottom:0.4em; }
#pfe .pfe-suggest { border:1px solid #e0e0e0; border-radius:6px; margin-top:0.2em; overflow:hidden; }
#pfe .pfe-sug { padding:0.45em 0.6em; cursor:pointer; border-bottom:1px solid #f0f0f0; }
#pfe .pfe-sug:last-child { border-bottom:none; }
#pfe .pfe-sug:hover, #pfe .pfe-sug:active { background:#eef4ff; }
#pfe .pfe-sug-empty { padding:0.45em 0.6em; color:#c0392b; font-size:0.85em; }
#pfe .pfe-preview { font-size:0.95em; }
#pfe .pv-fiche { line-height:1.5; }
#pfe .pv-portrait { float:right; max-width:120px; border-radius:6px; margin:0 0 0.5em 0.8em; }
#pfe .pv-name { margin:0 0 0.15em; font-size:1.25em; }
#pfe .pv-vitals { color:#666; margin:0 0 0.6em; font-style:italic; }
#pfe .pv-row { margin:0.25em 0; }
#pfe .pv-lab { font-weight:600; color:#556; font-size:0.85em; margin-right:0.3em; }
#pfe .pv-chip { display:inline-block; background:#f1f3f6; border-radius:12px; padding:0.1em 0.55em; font-size:0.85em; margin:0.1em 0.15em 0.1em 0; }
#pfe .pv-chip.pv-rel { background:#eef4ff; border:1px solid #cfe0ff; }
#pfe .pv-list { margin:0.2em 0 0.5em 1.1em; padding:0; }
#pfe .pv-mut { color:#999; font-size:0.9em; }
#pfe .pv-body { margin-top:0.7em; }
#pfe .pv-body p { margin:0.4em 0; }
#pfe .pv-edit { cursor:text; border-radius:3px; transition:box-shadow .1s; }
#pfe .pv-edit:hover { box-shadow: inset 0 -2px 0 #cfe0ff; }
#pfe .pv-edit:focus { outline:2px solid #2563eb; outline-offset:2px; background:#fbfdff; }
#pfe .pv-name.pv-edit:empty::before { content:"(cliquer pour nommer)"; color:#bbb; }
#pfe .pv-body.pv-edit:empty::before { content:"(cliquer pour ajouter une bio)"; color:#bbb; }
</style>

<script>
(function () {
  "use strict";

  // ── Index de relations (en prod : généré au build depuis le corpus) ───────
  var INDEX = {
    periods: [
      { slug: "revolution-francaise", title: "Révolution française" },
      { slug: "revolutions-de-1848", title: "Révolutions de 1848" },
      { slug: "commune-de-paris", title: "Commune de Paris" },
      { slug: "second-empire", title: "Second Empire" },
      { slug: "troisieme-republique", title: "Troisième République" },
      { slug: "belle-epoque", title: "Belle Époque" },
      { slug: "entre-deux-guerres", title: "Entre-deux-guerres" },
      { slug: "ere-contemporaine", title: "Ère contemporaine" }
    ],
    themes: [
      { slug: "litterature", title: "Littérature" },
      { slug: "arts-plastiques", title: "Arts plastiques" },
      { slug: "femmes-artistes", title: "Femmes artistes" },
      { slug: "montmartre", title: "Montmartre" }
    ],
    addresses: [
      { slug: "5-rue-sebastien-bottin", title: "5 rue Sébastien-Bottin" },
      { slug: "12-rue-cortot", title: "12 rue Cortot" },
      { slug: "place-charles-de-gaulle", title: "Place Charles-de-Gaulle" }
    ],
    persons: [
      { slug: "albert-camus", title: "Albert Camus" },
      { slug: "robert-desnos", title: "Robert Desnos" },
      { slug: "paul-eluard", title: "Paul Éluard" },
      { slug: "jules-supervielle", title: "Jules Supervielle" },
      { slug: "roger-martin-du-gard", title: "Roger Martin du Gard" },
      { slug: "a-de-longpre", title: "A. de Longpré" },
      { slug: "suzanne-valadon", title: "Suzanne Valadon" }
    ]
  };

  // ── Types : deux schémas, un seul moteur ──────────────────────────────────
  var PERSON_ORDER = ["id","slug","type","title","entityType","gender","sortName","bornName","aka","image","birth","death","professions","qualificatifs","fate","nationalities","periods","themes","addresses","bibliography","externalLinks","body","workflow"];
  var EVENT_ORDER  = ["id","slug","type","title","image","daterange","location","epochs","themes","districts","people","bibliography","externalLinks","body","workflow"];

  var TYPES = {
    persons: {
      label: "Personnage", path: "docs/paris/sample/a-de-longpre.yaml", inlineId: "pfe-fiche-persons", order: PERSON_ORDER,
      schema: [
        { name: "title", label: "Nom affiché", widget: "string" },
        { name: "gender", label: "Genre", widget: "select", options: ["", "masculin", "féminin", "non-binaire", "inconnu"] },
        { name: "professions", label: "Professions / activités", widget: "list", hint: "vocabulaire contrôlé v1.3" },
        { name: "periods", label: "Époques", widget: "relation", collection: "periods", multiple: true }
      ],
      preview: personPreview
    },
    events: {
      label: "Événement", path: "docs/paris/sample/gallimard-siege.yaml", inlineId: "pfe-fiche-events", order: EVENT_ORDER,
      schema: [
        { name: "title", label: "Titre", widget: "string" },
        { name: "daterange", label: "Datation", widget: "object", fields: [
          { name: "startYear", label: "Année de début", widget: "number" },
          { name: "endYear", label: "Année de fin", widget: "number" },
          { name: "precision", label: "Précision", widget: "select", options: ["exact", "month", "year", "circa", "unknown"] }
        ]},
        { name: "location", label: "Localisation", widget: "object", fields: [
          { name: "ordered", label: "Itinéraire ordonné", widget: "boolean" },
          { name: "approximate", label: "Approximatif", widget: "boolean" },
          { name: "points", label: "Point", widget: "objectlist", fields: [
            { name: "street", label: "Adresse (relation)", widget: "relation", collection: "addresses" },
            { name: "role", label: "Rôle", widget: "string" },
            { name: "primary", label: "Point principal", widget: "boolean" },
            { name: "note", label: "Nom du lieu", widget: "string" }
          ]}
        ]},
        { name: "epochs", label: "Époques", widget: "relation", collection: "periods", multiple: true },
        { name: "themes", label: "Thèmes", widget: "relation", collection: "themes", multiple: true },
        { name: "people", label: "Personnages", widget: "relation", collection: "persons", multiple: true }
      ],
      preview: eventPreview
    }
  };

  var _type = "persons", _rec = null, _origKeys = [];

  // ── Helpers ───────────────────────────────────────────────────────────────
  function $(id) { return document.getElementById(id); }
  function el(t, c) { var e = document.createElement(t); if (c) e.className = c; return e; }
  function txt(s) { return document.createTextNode(s); }
  function rep(s, n) { var o = ""; for (var i = 0; i < n; i++) o += s; return o; }
  function isArr(v) { return Object.prototype.toString.call(v) === "[object Array]"; }
  function isObj(v) { return v && typeof v === "object" && !isArr(v); }
  function escHtml(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function escAttr(s) { return escHtml(s).replace(/"/g, "&quot;"); }
  function norm(s) { s = (s || "").toLowerCase().trim(); return s.normalize ? s.normalize("NFD").replace(new RegExp("[\\u0300-\\u036f]", "g"), "") : s; }
  function relTitle(coll, slug) { var a = INDEX[coll] || [], i; for (i = 0; i < a.length; i++) if (a[i].slug === slug) return a[i].title; return slug; }
  function matchRel(coll, q, exclude) {
    var a = INDEX[coll] || [], n = norm(q); exclude = exclude || [];
    if (!n) return [];
    var starts = [], incl = [], i, p, t;
    for (i = 0; i < a.length; i++) {
      p = a[i]; if (exclude.indexOf(p.slug) !== -1) continue;
      t = norm(p.title);
      if (t.indexOf(n) === 0 || p.slug.indexOf(n) === 0) starts.push(p);
      else if (t.indexOf(n) !== -1 || p.slug.indexOf(n) !== -1) incl.push(p);
    }
    return starts.concat(incl).slice(0, 8);
  }

  // ── Sérialiseur YAML (générique, schéma-ordonné, style bloc) ──────────────
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
      var lines = s.replace(/\n+$/, "").split("\n"), out = "|-", i;
      for (i = 0; i < lines.length; i++) out += "\n" + pad + "  " + lines[i];
      return out;
    }
    return scalarStr(s);
  }
  function orderedKeys(map, order) {
    var keys = [], seen = {}, k, i;
    if (order) for (i = 0; i < order.length; i++) { k = order[i]; if (map.hasOwnProperty(k)) { keys.push(k); seen[k] = 1; } }
    for (k in map) if (map.hasOwnProperty(k) && !seen[k]) keys.push(k);
    return keys;
  }
  function emitMap(map, indent, order) {
    var keys = orderedKeys(map, order), out = [], i;
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
  function toYaml(rec) { return emitMap(rec, 0, TYPES[_type].order) + "\n"; }

  // ── Rendu ─────────────────────────────────────────────────────────────────
  function renderHead() {
    $("pfe-type").textContent = _rec.type || "?";
    $("pfe-id").textContent = _rec.id || "(sans id)";
    $("pfe-slug").textContent = _rec.slug || "";
  }
  function syncYaml() {
    $("pfe-yaml").textContent = toYaml(_rec);
    var lost = 0, k, i;
    for (i = 0; i < _origKeys.length; i++) { k = _origKeys[i]; if (!_rec.hasOwnProperty(k)) lost++; }
    $("pfe-integrity").textContent = lost === 0
      ? "✔ " + _origKeys.length + " clés d'origine préservées — aucune perte."
      : "⚠ " + lost + " clé(s) perdue(s).";
  }
  function renderYaml() { syncYaml(); renderPreview(); }
  function renderPreview() { var e = $("pfe-preview"); if (!e) return; e.innerHTML = TYPES[_type].preview(_rec); wireInlineEdit(); }
  // WYSIWYG en place : les éléments .pv-edit de l'aperçu sont éditables au clic.
  // Pendant la frappe on ne resynchronise QUE le YAML (pas l'aperçu) pour garder le curseur.
  function wireInlineEdit() {
    var els = $("pfe-preview").querySelectorAll(".pv-edit"), i;
    for (i = 0; i < els.length; i++) {
      (function (e) {
        var fld = e.getAttribute("data-fld"), single = e.getAttribute("data-single") === "1";
        function read() { return (single ? e.textContent : e.innerText).replace(/ /g, " "); }
        e.oninput = function () { _rec[fld] = read(); syncYaml(); };
        e.onblur = function () { _rec[fld] = read().replace(/\n+$/, ""); rerender(); };
        if (single) e.onkeydown = function (ev) { if (ev.key === "Enter" || ev.keyCode === 13) { ev.preventDefault(); e.blur(); } };
      })(els[i]);
    }
  }
  function rerender() { renderForm(); renderYaml(); }
  function renderForm() {
    var box = $("pfe-form"); box.innerHTML = "";
    var s = TYPES[_type].schema, i;
    for (i = 0; i < s.length; i++) box.appendChild(buildField(_rec, s[i]));
  }

  // ── Widgets (génériques, liés à (obj, fieldDef)) ──────────────────────────
  function buildField(obj, fd) {
    var wrap = el("div", "pfe-field"), lab = el("label");
    lab.appendChild(txt(fd.label));
    if (fd.hint) { var h = el("span", "pfe-hint"); h.appendChild(txt(" — " + fd.hint)); lab.appendChild(h); }
    wrap.appendChild(lab); wrap.appendChild(ctrlFor(obj, fd)); return wrap;
  }
  function ctrlFor(obj, fd) {
    var w = fd.widget;
    if (w === "string") return strCtrl(obj, fd);
    if (w === "number") return numCtrl(obj, fd);
    if (w === "boolean") return boolCtrl(obj, fd);
    if (w === "select") return selCtrl(obj, fd);
    if (w === "list") return listCtrl(obj, fd);
    if (w === "relation") return relCtrl(obj, fd);
    if (w === "object") return objCtrl(obj, fd);
    if (w === "objectlist") return objListCtrl(obj, fd);
    return txt("(widget inconnu)");
  }
  function strCtrl(obj, fd) {
    var i = el("input"); i.type = "text"; i.value = obj[fd.name] != null ? obj[fd.name] : "";
    i.oninput = function () { obj[fd.name] = i.value; renderYaml(); };
    return i;
  }
  function numCtrl(obj, fd) {
    var i = el("input"); i.type = "text"; i.setAttribute("inputmode", "numeric");
    i.value = obj[fd.name] == null ? "" : obj[fd.name];
    i.oninput = function () {
      var v = i.value.trim();
      if (v === "") delete obj[fd.name];
      else { var n = Number(v); obj[fd.name] = isNaN(n) ? v : n; }
      renderYaml();
    };
    return i;
  }
  function boolCtrl(obj, fd) {
    var c = el("input"); c.type = "checkbox"; c.checked = !!obj[fd.name];
    c.onchange = function () { obj[fd.name] = c.checked; renderYaml(); };
    return c;
  }
  function selCtrl(obj, fd) {
    var s = el("select"), j;
    for (j = 0; j < fd.options.length; j++) {
      var op = el("option"); op.value = fd.options[j];
      op.textContent = fd.options[j] === "" ? "—" : fd.options[j];
      if ((obj[fd.name] || "") === fd.options[j]) op.selected = true;
      s.appendChild(op);
    }
    s.onchange = function () { if (s.value === "") delete obj[fd.name]; else obj[fd.name] = s.value; renderYaml(); };
    return s;
  }
  function listCtrl(obj, fd) {
    if (!isArr(obj[fd.name])) obj[fd.name] = [];
    var box = el("div");
    obj[fd.name].forEach(function (val, idx) {
      var row = el("div", "pfe-listrow"), i = el("input");
      i.type = "text"; i.value = val;
      i.oninput = function () { obj[fd.name][idx] = i.value; renderYaml(); };
      i.onchange = function () { obj[fd.name][idx] = i.value.trim(); i.value = obj[fd.name][idx]; renderYaml(); };
      var x = el("button", "pfe-x"); x.type = "button"; x.appendChild(txt("×"));
      x.onclick = function () { obj[fd.name].splice(idx, 1); rerender(); };
      row.appendChild(i); row.appendChild(x); box.appendChild(row);
    });
    var add = el("button", "pfe-add"); add.type = "button"; add.appendChild(txt("＋ ajouter"));
    add.onclick = function () { obj[fd.name].push(""); rerender(); };
    box.appendChild(add); return box;
  }
  function relChipNode(coll, slug, onRemove) {
    var c = el("span", "pfe-chip"); c.appendChild(txt(relTitle(coll, slug)));
    var b = el("button"); b.type = "button"; b.appendChild(txt("×")); b.onclick = onRemove;
    c.appendChild(b); return c;
  }
  function suggestBox(coll, exclude, onPick) {
    var box = el("div"), row = el("div", "pfe-listrow"), i = el("input");
    i.type = "text"; i.setAttribute("autocomplete", "off"); i.placeholder = "Chercher dans « " + coll + " » par nom…";
    var add = el("button", "pfe-add"); add.type = "button"; add.appendChild(txt("＋"));
    row.appendChild(i); row.appendChild(add); box.appendChild(row);
    var sug = el("div", "pfe-suggest"); box.appendChild(sug);
    function draw() {
      var q = i.value, m = matchRel(coll, q, exclude); sug.innerHTML = "";
      if (!q.trim()) return;
      if (!m.length) { var e = el("div", "pfe-sug-empty"); e.appendChild(txt("✗ aucun résultat « " + q.trim() + " »")); sug.appendChild(e); return; }
      m.forEach(function (p) {
        var d = el("div", "pfe-sug"); d.appendChild(txt(p.title));
        d.onmousedown = function (ev) { ev.preventDefault(); onPick(p); };
        sug.appendChild(d);
      });
    }
    i.oninput = draw;
    i.onkeydown = function (e) { if (e.key === "Enter" || e.keyCode === 13) { e.preventDefault(); var m = matchRel(coll, i.value, exclude); if (m.length) onPick(m[0]); } };
    add.onclick = function () { var m = matchRel(coll, i.value, exclude); if (m.length) onPick(m[0]); };
    return box;
  }
  function relCtrl(obj, fd) {
    var coll = fd.collection, box = el("div");
    if (fd.multiple) {
      if (!isArr(obj[fd.name])) obj[fd.name] = [];
      var chips = el("div", "pfe-chips");
      obj[fd.name].forEach(function (slug) {
        chips.appendChild(relChipNode(coll, slug, function () { var k = obj[fd.name].indexOf(slug); if (k !== -1) obj[fd.name].splice(k, 1); rerender(); }));
      });
      box.appendChild(chips);
      box.appendChild(suggestBox(coll, obj[fd.name], function (p) { if (obj[fd.name].indexOf(p.slug) === -1) obj[fd.name].push(p.slug); rerender(); }));
    } else if (obj[fd.name]) {
      var chips2 = el("div", "pfe-chips");
      chips2.appendChild(relChipNode(coll, obj[fd.name], function () { delete obj[fd.name]; rerender(); }));
      box.appendChild(chips2);
    } else {
      box.appendChild(suggestBox(coll, [], function (p) { obj[fd.name] = p.slug; rerender(); }));
    }
    return box;
  }
  function objCtrl(obj, fd) {
    if (!isObj(obj[fd.name])) obj[fd.name] = {};
    var g = el("div", "pfe-group"), i;
    for (i = 0; i < fd.fields.length; i++) g.appendChild(buildField(obj[fd.name], fd.fields[i]));
    return g;
  }
  function objListCtrl(obj, fd) {
    if (!isArr(obj[fd.name])) obj[fd.name] = [];
    var box = el("div");
    obj[fd.name].forEach(function (item, idx) {
      if (!isObj(item)) { item = {}; obj[fd.name][idx] = item; }
      var g = el("div", "pfe-group pfe-item"), hd = el("div", "pfe-item-hd");
      hd.appendChild(txt(fd.label + " " + (idx + 1)));
      var x = el("button", "pfe-x"); x.type = "button"; x.appendChild(txt("×"));
      x.onclick = function () { obj[fd.name].splice(idx, 1); rerender(); };
      hd.appendChild(x); g.appendChild(hd);
      for (var k = 0; k < fd.fields.length; k++) g.appendChild(buildField(item, fd.fields[k]));
      box.appendChild(g);
    });
    var add = el("button", "pfe-add"); add.type = "button"; add.appendChild(txt("＋ ajouter " + (fd.label || "élément")));
    add.onclick = function () { obj[fd.name].push({}); rerender(); };
    box.appendChild(add); return box;
  }

  // ── Aperçus (par type) ────────────────────────────────────────────────────
  function pvChips(label, arr) {
    if (!isArr(arr) || !arr.length) return "";
    var h = '<div class="pv-row"><span class="pv-lab">' + label + '</span>', i;
    for (i = 0; i < arr.length; i++) h += '<span class="pv-chip">' + escHtml(arr[i]) + '</span>';
    return h + '</div>';
  }
  function pvRel(label, coll, arr) {
    if (!isArr(arr) || !arr.length) return "";
    var h = '<div class="pv-row"><span class="pv-lab">' + label + '</span>', i;
    for (i = 0; i < arr.length; i++) h += '<span class="pv-chip pv-rel">' + escHtml(relTitle(coll, arr[i])) + '</span>';
    return h + '</div>';
  }
  function mdMini(t) {
    var paras = String(t).split(/\n\s*\n/), h = "", i;
    for (i = 0; i < paras.length; i++) if (paras[i].trim()) h += '<p>' + escHtml(paras[i].trim()).replace(/\n/g, "<br>") + '</p>';
    return h;
  }
  function personPreview(r) {
    var fem = r.gender === "féminin", h = '<div class="pv-fiche">';
    if (r.image && r.image.src) h += '<img class="pv-portrait" src="' + escAttr(r.image.src) + '" alt="' + escAttr(r.image.alt || "") + '">';
    h += '<h2 class="pv-name pv-edit" contenteditable="true" data-fld="title" data-single="1">' + escHtml(r.title || "") + '</h2>';
    var v = [];
    if (r.birth && (r.birth.year || r.birth.place)) v.push((fem ? "Née" : "Né") + " " + [r.birth.year, r.birth.place].filter(Boolean).join(" à "));
    if (r.death && (r.death.year || r.death.place)) v.push((fem ? "Morte" : "Mort") + " " + [r.death.year, r.death.place].filter(Boolean).join(" à "));
    if (v.length) h += '<p class="pv-vitals">' + escHtml(v.join(" · ")) + '</p>';
    h += pvChips("Professions", r.professions) + pvChips("Qualificatifs", r.qualificatifs) + pvChips("Nationalités", r.nationalities) + pvRel("Époques", "periods", r.periods);
    h += '<div class="pv-body pv-edit" contenteditable="true" data-fld="body">' + mdMini(r.body || "") + '</div>';
    return h + '</div>';
  }
  function eventPreview(r) {
    var h = '<div class="pv-fiche"><h2 class="pv-name pv-edit" contenteditable="true" data-fld="title" data-single="1">' + escHtml(r.title || "") + '</h2>';
    if (r.daterange) {
      var d = r.daterange, dr = d.startYear != null ? String(d.startYear) : "";
      if (d.endYear != null && d.endYear !== d.startYear) dr += (dr ? "–" : "") + d.endYear;
      if (dr) h += '<p class="pv-vitals">' + escHtml(dr) + (d.precision && d.precision !== "exact" ? " (" + escHtml(d.precision) + ")" : "") + '</p>';
    }
    if (r.location && isArr(r.location.points) && r.location.points.length) {
      h += '<div class="pv-row"><span class="pv-lab">Lieux</span></div><ul class="pv-list">';
      r.location.points.forEach(function (p) {
        var name = p.note || relTitle("addresses", p.street || "") || p.role || "(point)";
        h += '<li>' + escHtml(name) + (p.street ? ' <span class="pv-mut">(' + escHtml(relTitle("addresses", p.street)) + ')</span>' : "") + (p.primary ? " ★" : "") + '</li>';
      });
      h += '</ul>';
    }
    h += pvRel("Époques", "periods", r.epochs) + pvRel("Thèmes", "themes", r.themes) + pvRel("Personnages", "persons", r.people);
    h += '<div class="pv-body pv-edit" contenteditable="true" data-fld="body">' + mdMini(r.body || "") + '</div>';
    return h + '</div>';
  }

  // ── Commit / chargement (API GitHub — même contrat que edit_on_github) ─────
  function b64e(s) { return btoa(unescape(encodeURIComponent(s))); }
  function wireCommit() {
    $("pfe-reload-btn").onclick = loadFiche;
    $("pfe-commit-btn").onclick = function () {
      var pat = localStorage.getItem("lc_ed_pat");
      var repo = $("pfe-repo").value || localStorage.getItem("lc_ed_repo") || "";
      var path = $("pfe-path").value, branch = $("pfe-branch").value || "main", st = $("pfe-status");
      if (!pat) { st.textContent = "Aucun PAT dans lc_ed_pat — renseigne-le via ✏️."; return; }
      if (!repo || !path) { st.textContent = "Dépôt et chemin requis."; return; }
      st.textContent = "Lecture du SHA…";
      var api = "https://api.github.com/repos/" + repo + "/contents/" + path;
      var H = { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
      fetch(api + "?ref=" + encodeURIComponent(branch), { headers: H, cache: "no-store" })
        .then(function (r) { return r.json(); })
        .then(function (cur) {
          var body = { message: "PoC: édition " + _type + " " + (_rec.id || path), content: b64e(toYaml(_rec)), branch: branch };
          if (cur && cur.sha) body.sha = cur.sha;
          return fetch(api, { method: "PUT", headers: H, body: JSON.stringify(body) }).then(function (r) { return r.json(); });
        })
        .then(function (res) { st.textContent = res && res.commit ? "✔ Commit " + res.commit.sha.substring(0, 7) : "✖ " + ((res && res.message) || "échec"); })
        .catch(function (e) { st.textContent = "✖ " + e.message; });
    };
  }
  function initFrom(raw, srcLabel) {
    try { _rec = window.jsyaml.load(raw) || {}; }
    catch (e) { $("pfe-form").innerHTML = "<p style='color:#c00'>YAML illisible : " + e.message + "</p>"; return; }
    _origKeys = []; for (var k in _rec) if (_rec.hasOwnProperty(k)) _origKeys.push(k);
    renderHead(); renderForm(); renderYaml();
    var se = $("pfe-source"); if (se) se.textContent = "Fiche chargée depuis : " + srcLabel;
  }
  function loadFiche() {
    var repo = $("pfe-repo").value || localStorage.getItem("lc_ed_repo") || "michelzam/lightcodepedia";
    var branch = $("pfe-branch").value || "main";
    var path = $("pfe-path").value || TYPES[_type].path;
    var pat = localStorage.getItem("lc_ed_pat");
    var url = "https://api.github.com/repos/" + repo + "/contents/" + path + "?ref=" + encodeURIComponent(branch) + "&t=" + (new Date().getTime());
    var H = { Accept: "application/vnd.github.raw", "X-GitHub-Api-Version": "2022-11-28" };
    if (pat) H.Authorization = "Bearer " + pat;
    var se = $("pfe-source"); if (se) se.textContent = "Chargement depuis " + path + " (API GitHub) …";
    fetch(url, { headers: H, cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
      .then(function (t) { initFrom(t, path + " @ " + branch + " (API GitHub, frais)"); })
      .catch(function () { initFrom($(TYPES[_type].inlineId).textContent, "copie intégrée (" + _type + ", repli)"); });
  }
  function wireType() {
    var sel = $("pfe-type-sel"); sel.value = _type;
    sel.onchange = function () { _type = sel.value; $("pfe-path").value = TYPES[_type].path; $("pfe-status").textContent = ""; loadFiche(); };
  }

  function boot() { wireCommit(); wireType(); $("pfe-path").value = TYPES[_type].path; loadFiche(); }
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

## Note technique (productisation)

Même moteur pour **Personnage** et **Événement** : le formulaire, la sérialisation et l'aperçu sont
**pilotés par un schéma** (widgets `string / number / boolean / select / list / relation / object / objectlist`).
Ajouter un type = ajouter une entrée de schéma — **pas de code**. Le sérialiseur YAML est générique
(objets et listes imbriqués), en round-trip **valide-schéma** (comme Sveltia). La productisation :
replier ce moteur dans `_includes/fiche_editor.md` pour un usage **100 % Markdown/IAL**
(`{: .fiche-editor collection="persons" }`), et générer l'index de relations au build.
