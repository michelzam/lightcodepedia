<!--
🧠 Cognitive load check — the ♿ Audit pane's second button (Michel,
2026-09-22). Deterministic, from the page as rendered and its source:
  coherence  — validations on the page (quizzes + proofs), proofs tagged
               with a skill, a prerequisite declared
  load       — per section (one screen in reel): distinct component kinds
               shown at once, and the largest cluster of blocks bound
               together (element interactivity — Sweller)
  friction   — interactive parts no validation or binding ever reads
  seduction  — media nothing points at (seductive details — coherence
               principle)
Every score expands into its factors, one row per component, clickable
like an audit finding. Rules carry defaults the author answers for
(window.lcLoadRules). Each run is remembered per page on this device,
with the audit's own numbers, so the panel says what changed since the
previous version — improvement is the point. No LLM here; a semantic
pass on prose is a later, key-gated step.
-->
<style>
#ed-load-bar { display: flex; align-items: center; gap: 0.6em; padding: 0.5em 0.9em; border-top: 1px solid #f0f0f0; font-size: 0.85em; }
#ed-load-list { font-size: 0.85em; }
.ed-load-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; padding: 0.6em 0.9em; }
.ed-load-card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.45em 0.6em; background: #fff; }
.ed-load-card b { display: block; font-size: 1.1em; }
.ed-load-card[data-verdict="ok"] { border-color: #86efac; background: #f0fdf4; }
.ed-load-card[data-verdict="warn"] { border-color: #fcd34d; background: #fffbeb; }
.ed-load-card small { color: #6b7280; }
.ed-load-delta { color: #6b7280; font-size: 0.85em; }
.ed-load-delta.better { color: #15803d; } .ed-load-delta.worse { color: #b45309; }
#ed-load-hist { font-size: 0.85em; }
#ed-load-hist summary { padding: 0.5em 0.9em; cursor: pointer; color: #4b5563; }
.ed-load-grid { margin: 0 0.9em 0.8em; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.ed-load-grid th { text-align: left; font-weight: 600; color: #374151; background: #f3f4f6; padding: 0.3em 0.6em; border-bottom: 1px solid #e5e7eb; cursor: help; }
.ed-load-grid td { padding: 0.3em 0.6em; border-bottom: 1px solid #f0f0f0; color: #4b5563; }
.ed-load-grid td.better { background: #dcfce7; color: #15803d; font-weight: 600; }
.ed-load-grid td.worse { background: #fee2e2; color: #b91c1c; font-weight: 600; }
.ed-load-sha { font-family: ui-monospace, Menlo, monospace; cursor: help; border-bottom: 1px dotted #9ca3af; }
</style>
<script>
(function () {
  if (window._lcLoadReady) return;
  window._lcLoadReady = true;

  var RULES = window.lcLoadRules = window.lcLoadRules || {
    validations_min: 1,        /* coherence: quizzes + proofs on the page, at least */
    untagged_proofs_max: 0,    /* coherence: proofs that name no skill (tags=) */
    prerequisite_declared: "look", /* coherence: a page with none — first page, or a gap? look */
    kinds_per_section_max: 4,  /* load: distinct component kinds one section shows at once */
    cluster_max: 3,            /* load: blocks bound together, to be read as one */
    loose_controls_max: 0,     /* friction: interactive parts no validation or binding reads */
    orphan_media_max: 1        /* seduction: media nothing points at — one hero is fine */
  };
  var WORDS = {
    validations_min: ["validations, at least", "quizzes and proofs on the page: below this, the page cannot tell what was learned"],
    untagged_proofs_max: ["untagged proofs, at most", "a proof without tags= names no skill: the target it validates is unknown"],
    prerequisite_declared: ["prerequisite declared", "no prerequisite block: a first page, or a gap — look"],
    kinds_per_section_max: ["kinds per section, at most", "distinct component kinds a section (one reel screen) shows at once"],
    cluster_max: ["bound cluster, at most", "blocks reading each other (bindings, masters, cells) must be understood together"],
    loose_controls_max: ["loose controls, at most", "an interactive part (form, agent, runner, grid…) no validation or binding reads: work with no path to a target"],
    orphan_media_max: ["orphan media, at most", "a video, map, scene, demo nothing points at: engaging, target-less"]
  };
  var INTERACTIVE = /^(form|agent|runner|editor|datagrid|grid|pytutor|playfield|cells?|recorder|studio)$/;
  var TRANSPARENT = /^(embed|slot|blocks|accordion|tabs|cards)$/;   /* wrappers: the parts inside are the parts */
  var MEDIA = /^(video|audio|map|scene3d|demo|qr|slides)$/;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function kindOf(el) {
    var m = (typeof el.className === "string" ? el.className : "").match(/(?:^|\s)lc-([a-z0-9]+)/);
    if (m) return m[1];
    var p = el.parentElement, pm = p && typeof p.className === "string" ? p.className.match(/(?:^|\s)lc-([a-z0-9]+)/) : null;
    return pm ? pm[1] : el.tagName.toLowerCase();
  }
  function attrsText(root) {
    var out = [];
    function take(el) { for (var i = 0; i < el.attributes.length; i++) { var a = el.attributes[i]; if (!/^(class|style|id|data-lc-id|aria-[a-z]+|role|tabindex)$/.test(a.name)) out.push(a.value); } }
    take(root);
    root.querySelectorAll("*").forEach(function (el) { if (!el.hasAttribute("data-lc-id")) take(el); });
    return out.join(" ");
  }
  function mentions(text, id) {
    if (!id) return false;
    return new RegExp("(^|[^A-Za-z0-9_])" + id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![A-Za-z0-9_])").test(text);
  }
  function analyse() {
    var body = document.querySelector(".markdown-body") || document.body;
    var src = ""; try { src = (document.getElementById("ed-input") || {}).value || ""; } catch (e) {}
    var roots = Array.prototype.filter.call(body.querySelectorAll("[data-lc-id]"), function (el) {
      if (el.closest("#ed-drawer, .lc-avatar-host, .lc-guide-menu")) return false;
      var up = el.parentElement ? el.parentElement.closest("[data-lc-id]") : null;
      /* nested parts belong to their block — unless the block is a wrapper
         (an embed, a bench slot, a tab set): then the part inside is the part */
      while (up && TRANSPARENT.test(kindOf(up))) up = up.parentElement ? up.parentElement.closest("[data-lc-id]") : null;
      return !up;
    });
    var parts = roots.map(function (el) { return { el: el, id: el.getAttribute("data-lc-id"), kind: kindOf(el), attrs: attrsText(el) }; });
    parts = parts.filter(function (p) { return !TRANSPARENT.test(p.kind) || !p.el.querySelector("[data-lc-id]"); });
    /* what a validation READS: its attributes, and the words of its own
       fence in the source (a proof's steps name the parts they drive) */
    var fenceText = {};
    if (src) {
      var re = /```[^\n]*\n([\s\S]*?)```[ \t]*\n\{:\s*\.(feature|quiz)\b([^}]*)\}/g, m;
      while ((m = re.exec(src)) !== null) {
        var idm = /#([A-Za-z0-9_-]+)/.exec(m[3]);
        if (idm) fenceText[idm[1]] = m[1] + " " + m[3];
      }
    }
    var heads = Array.prototype.slice.call(body.querySelectorAll("h2"));
    heads.forEach(function (h, i) { if (!h.id) h.id = "lc_section_" + (i + 1); });
    function sectionOf(el) {
      var s = "";
      for (var i = 0; i < heads.length; i++) if (heads[i].compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) s = heads[i].textContent.trim().slice(0, 40);
      return s || "(top)";
    }
    parts.forEach(function (p) { p.section = sectionOf(p.el); });
    /* the graph: a part reads another when its attributes or a cell in the
       source name it */
    var referenced = {}, parent = {};
    parts.forEach(function (p) { parent[p.id] = p.id; });
    function find(x) { while (parent[x] !== x) x = parent[x]; return x; }
    function union(a, b) { parent[find(a)] = find(b); }
    parts.forEach(function (a) {
      var reads = a.attrs + " " + (fenceText[a.id] || "") + (a.kind === "feature" || a.kind === "quiz" ? " " + a.el.textContent : "");
      parts.forEach(function (b) {
        if (a === b) return;
        if (mentions(reads, b.id)) { referenced[b.id] = (referenced[b.id] || []).concat(a.kind + " #" + a.id); union(a.id, b.id); }
      });
      if (src && new RegExp("\\{=\\s*" + a.id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b").test(src)) referenced[a.id] = (referenced[a.id] || []).concat("a cell");
    });
    var validations = parts.filter(function (p) { return p.kind === "quiz" || p.kind === "feature"; });
    var untagged = parts.filter(function (p) { return p.kind === "feature" && !p.el.querySelector(".lc-feature-tags *"); });
    var prereq = !!body.querySelector(".lc-prereq, .lc-prereq-met, .prerequisite");
    var sections = {};
    parts.forEach(function (p) {
      var s = sections[p.section] || (sections[p.section] = { kinds: {}, ids: [] });
      s.kinds[p.kind] = true; s.ids.push(p.id);
    });
    var clusters = {};
    parts.forEach(function (p) { var r = find(p.id); clusters[r] = (clusters[r] || []).concat(p.id); });
    var loadRows = [];
    Object.keys(sections).forEach(function (name) {
      var s = sections[name], nk = Object.keys(s.kinds).length;
      var hi = heads.map(function (h) { return h.textContent.trim().slice(0, 40); }).indexOf(name);
      s.sel = hi >= 0 ? "#" + heads[hi].id : "";
      var big = 0, bigIds = [], here = {};
      s.ids.forEach(function (id) { here[id] = true; });
      s.ids.forEach(function (id) {
        var c = clusters[find(id)].filter(function (x) { return here[x]; });   /* members on this screen */
        if (c.length > big) { big = c.length; bigIds = c; }
      });
      loadRows.push({ section: name, sel: s.sel, kinds: nk, kindList: Object.keys(s.kinds), cluster: big, clusterIds: bigIds, ids: s.ids });
    });
    var loose = parts.filter(function (p) { return INTERACTIVE.test(p.kind) && !referenced[p.id]; });
    var orphan = parts.filter(function (p) { return MEDIA.test(p.kind) && !referenced[p.id]; });
    var maxKinds = loadRows.reduce(function (m, r) { return Math.max(m, r.kinds); }, 0);
    var maxCluster = loadRows.reduce(function (m, r) { return Math.max(m, r.cluster); }, 0);
    return {
      parts: parts, validations: validations, untagged: untagged, prereq: prereq,
      loadRows: loadRows, loose: loose, orphan: orphan,
      numbers: { validations: validations.length, untagged: untagged.length, kinds: maxKinds, cluster: maxCluster, loose: loose.length, orphan: orphan.length }
    };
  }

  /* ── memory: one line per run, per page, on this device ── */
  function pageKey() {
    var rt = document.querySelector("#lc-run[data-lc-src-path]");
    return rt ? (rt.dataset.lcSrcRepo + "/" + rt.dataset.lcSrcPath) : (window.lcPagePath ? window.lcPagePath() : location.pathname);
  }
  function hist() { try { return JSON.parse(localStorage.getItem("lc_load_hist") || "{}"); } catch (e) { return {}; } }
  /* THE HISTORY LIVES BESIDE THE PAGE (Michel, 2026-09-22: "store all that
     in an __pagename_audit.yaml so we can see the progress in time"): a
     dunder file in the page's own folder — never published, never rendered —
     written with the editor's key, one row per version. The browser keeps
     a mirror for a device without the key. */
  function auditFile() {
    var rt = document.querySelector("#lc-run[data-lc-src-path]"), repo, path;
    if (rt && rt.dataset.lcSrcRepo && rt.dataset.lcSrcPath) { repo = rt.dataset.lcSrcRepo; path = rt.dataset.lcSrcPath; }
    else { repo = window.lcEdRepo || ""; path = window.lcEdPath || ""; }
    if (!repo || !path) return null;
    var segs = path.split("/"), base = segs.pop().replace(/\.md$/, "");
    return { repo: repo, path: (segs.length ? segs.join("/") + "/" : "") + "__" + base + "_audit.yaml" };
  }
  function ghHeaders() {
    var key = ""; try { key = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    return key ? { Authorization: "token " + key, Accept: "application/vnd.github+json", "Content-Type": "application/json" } : null;
  }
  var _fileRows = null, _fileSha = null, _fileLoaded = false;
  function loadFile() {
    var f = auditFile(), H = ghHeaders();
    if (!f || !H || !window.jsyaml) { _fileLoaded = true; return Promise.resolve(null); }
    return fetch("https://api.github.com/repos/" + f.repo + "/contents/" + f.path, { headers: H })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        _fileLoaded = true;
        if (!d || !d.content) { _fileRows = []; _fileSha = null; return _fileRows; }
        _fileSha = d.sha;
        try { _fileRows = window.jsyaml.load(decodeURIComponent(escape(atob(String(d.content).replace(/\s/g, ""))))) || []; }
        catch (e) { _fileRows = []; }
        if (!Array.isArray(_fileRows)) _fileRows = [];
        var all = hist(); all[pageKey()] = _fileRows.slice(-20);
        try { localStorage.setItem("lc_load_hist", JSON.stringify(all)); } catch (e) {}
        return _fileRows;
      }).catch(function () { _fileLoaded = true; return null; });
  }
  function saveFile(rows, note) {
    var f = auditFile(), H = ghHeaders();
    if (!f || !H || !window.jsyaml) return Promise.resolve(false);
    var body = { message: "audit: " + f.path.split("/").pop().replace(/^__|_audit\.yaml$/g, "") + " — " + note,
                 content: btoa(unescape(encodeURIComponent("# audit history — one row per version, written by the editor's ♿/🧠 checks\n" + window.jsyaml.dump(rows, { lineWidth: 120 })))) };
    if (_fileSha) body.sha = _fileSha;
    return fetch("https://api.github.com/repos/" + f.repo + "/contents/" + f.path, { method: "PUT", headers: H, body: JSON.stringify(body) })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d && d.content) { _fileSha = d.content.sha; return true; } return false; });
  }
  /* the commit behind the file the editor holds — its message is the
     tooltip on the version, so a line reads "what changed", not a hash */
  var _commitFor = {};
  function commitOf(sha) {
    if (_commitFor[sha] !== undefined) return Promise.resolve(_commitFor[sha]);
    var repo = window.lcEdRepo, path = window.lcEdPath, key = "";
    try { key = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    if (!repo || !path || !key) return Promise.resolve(null);
    return fetch("https://api.github.com/repos/" + repo + "/commits?path=" + encodeURIComponent(path) + "&per_page=1",
                 { headers: { Authorization: "token " + key, Accept: "application/vnd.github+json" } })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (cs) { var c = cs && cs[0]; _commitFor[sha] = c ? { sha: c.sha, message: ((c.commit || {}).message || "").split("\n")[0] } : null; return _commitFor[sha]; })
      .catch(function () { return null; });
  }
  function record(patch) {
    var all = hist(), key = pageKey(), rows = all[key] || [], sha = window.lcEdSha || "live";
    var last = rows[rows.length - 1], entry;
    if (last && last.sha === sha) { entry = last; Object.keys(patch).forEach(function (k) { last[k] = patch[k]; }); last.when = new Date().toISOString(); }
    else { entry = { when: new Date().toISOString(), sha: sha }; Object.keys(patch).forEach(function (k) { entry[k] = patch[k]; }); rows.push(entry); }
    all[key] = rows.slice(-20);
    try { localStorage.setItem("lc_load_hist", JSON.stringify(all)); } catch (e) {}
    renderHist();
    var note = Object.keys(patch).map(function (k) {
      var v = patch[k];
      return k === "a11y" ? ("♿ " + v.violations + " issues, " + v.review + " to look at") : ("🧠 " + v.validations + " validations, " + v.loose + " loose, " + v.orphan + " orphan");
    }).join(" · ");
    var done = entry.commit ? Promise.resolve(entry.commit) : commitOf(sha).then(function (c) {
      if (!c) return null;
      var again = hist(), rs = again[key] || [];
      rs.forEach(function (r) { if (r.sha === sha) r.commit = c; });
      try { localStorage.setItem("lc_load_hist", JSON.stringify(again)); } catch (e) {}
      renderHist();
      return c;
    });
    done.then(function () {
      var latest = hist()[key] || [];
      return saveFile(latest, note);
    }).then(function (ok) { var st = document.getElementById("ed-load-file"); if (st) st.textContent = ok ? "📄 history committed beside the page" : (auditFile() ? "📄 history kept on this device only" : ""); });
  }
  window.lcLoadRecord = record;
  /* the previous VERSION: the latest run whose file differed from this one */
  function previous() {
    var rows = hist()[pageKey()] || [], sha = window.lcEdSha || "live";
    for (var i = rows.length - 1; i >= 0; i--) if (rows[i].sha !== sha && rows[i].load) return rows[i];
    return null;
  }
  var LOWER_IS_BETTER = { untagged: 1, kinds: 1, cluster: 1, loose: 1, orphan: 1, violations: 1, review: 1, fail: 1 };
  function delta(name, now, before) {
    if (before == null || now == null) return "";
    var d = now - before; if (!d) return '<span class="ed-load-delta">= previous</span>';
    var better = LOWER_IS_BETTER[name] ? d < 0 : d > 0;
    return '<span class="ed-load-delta ' + (better ? "better" : "worse") + '">' + (d > 0 ? "+" : "") + d + ' vs previous</span>';
  }
  var COLS = [
    ["when", "When", "when this run was made"],
    ["version", "Version", "the file's version — hover: the commit behind it"],
    ["violations", "♿ Issues", "audit: confirmed WCAG failures"],
    ["review", "♿ Look", "audit: elements the engine could not decide — a human looks"],
    ["validations", "Validations", "coherence: quizzes and proofs on the page"],
    ["untagged", "Untagged", "coherence: proofs without a skill tag"],
    ["kinds", "Kinds", "load: most component kinds one section shows at once"],
    ["cluster", "Cluster", "load: largest set of blocks bound together on one screen"],
    ["loose", "Loose", "friction: interactive parts no validation or binding reads"],
    ["orphan", "Orphan", "seduction: media nothing points at"]
  ];
  function valueOf(r, k) {
    if (k === "violations" || k === "review") return (r.a11y || {})[k];
    return (r.load || {})[k];
  }
  function renderHist() {
    var box = document.getElementById("ed-load-hist"); if (!box) return;
    var rows = hist()[pageKey()] || [];
    if (!rows.length) { box.innerHTML = ""; return; }
    var html = '<details open><summary>📈 ' + rows.length + ' run' + (rows.length > 1 ? "s" : "") + ' remembered on this device — green improved, red regressed, against the run before</summary>'
      + '<table class="ed-load-grid"><thead><tr>' + COLS.map(function (c) { return '<th title="' + esc(c[2]) + '">' + esc(c[1]) + '</th>'; }).join("") + '</tr></thead><tbody>';
    for (var i = rows.length - 1; i >= 0; i--) {
      var r = rows[i], before = rows[i - 1] || null;
      html += '<tr data-sha="' + esc(r.sha) + '">';
      COLS.forEach(function (c) {
        var k = c[0];
        if (k === "when") { html += '<td>' + esc(r.when.slice(0, 16).replace("T", " ")) + '</td>'; return; }
        if (k === "version") {
          var tip = r.commit ? (String(r.commit.sha).slice(0, 7) + " — " + r.commit.message) : "the file as loaded in the editor";
          html += '<td><span class="ed-load-sha" title="' + esc(tip) + '">' + esc(String(r.sha).slice(0, 7)) + '</span></td>'; return;
        }
        var v = valueOf(r, k), b = before ? valueOf(before, k) : null, cls = "";
        if (v != null && b != null && v !== b) cls = (LOWER_IS_BETTER[k] ? v < b : v > b) ? "better" : "worse";
        html += '<td class="' + cls + '"' + (cls ? ' title="' + esc((v > b ? "+" : "") + (v - b) + " vs the run before") + '"' : "") + '>' + esc(v == null ? "·" : v) + '</td>';
      });
      html += '</tr>';
    }
    box.innerHTML = html + '</tbody></table></details>';
  }

  function row(p, note) {
    return '<div class="ed-a11y-row" data-sel="[data-lc-id=&quot;' + esc(p.id) + '&quot;]" data-kind="load"><b class="review">' + esc(p.kind) + '</b> #' + esc(p.id) + ' <span>' + esc(p.section) + (note ? " · " + note : "") + '</span></div>';
  }
  function run() {
    var list = document.getElementById("ed-load-list"); if (!list) return;
    var r = analyse(), n = r.numbers, prev = previous(), pl = (prev && prev.load) || {};
    var v = {
      coherence: n.validations >= RULES.validations_min && n.untagged <= RULES.untagged_proofs_max && (r.prereq || RULES.prerequisite_declared !== true),
      load: n.kinds <= RULES.kinds_per_section_max && n.cluster <= RULES.cluster_max,
      friction: n.loose <= RULES.loose_controls_max,
      seduction: n.orphan <= RULES.orphan_media_max
    };
    function card(name, title, main, sub, dn) {
      return '<div class="ed-load-card" data-score="' + name + '" data-verdict="' + (v[name] ? "ok" : "warn") + '"><small>' + title + '</small><b>' + main + '</b><small>' + sub + '</small>' + (dn || "") + '</div>';
    }
    var html = '<div class="ed-load-cards">'
      + card("coherence", "🎯 coherence", n.validations + " validation" + (n.validations === 1 ? "" : "s"), n.untagged + " untagged · " + (r.prereq ? "prerequisite ✓" : "no prerequisite"), delta("validations", n.validations, pl.validations))
      + card("load", "🧩 load", n.kinds + " kinds / section", "cluster of " + n.cluster, delta("kinds", n.kinds, pl.kinds))
      + card("friction", "⚙️ friction", n.loose + " loose control" + (n.loose === 1 ? "" : "s"), "no target reads them", delta("loose", n.loose, pl.loose))
      + card("seduction", "🎬 seduction", n.orphan + " orphan media", "nothing points at them", delta("orphan", n.orphan, pl.orphan))
      + '</div>';
    var rows = "";
    r.untagged.forEach(function (p) { rows += row(p, "a proof without a skill tag"); });
    r.loadRows.filter(function (s) { return s.kinds > RULES.kinds_per_section_max || s.cluster > RULES.cluster_max; }).forEach(function (s) {
      rows += '<div class="ed-a11y-row" data-kind="load-section" data-sel="' + esc(s.sel) + '"><b class="review">section</b> ' + esc(s.section) + ' <span>' + s.kinds + ' kinds (' + esc(s.kindList.join(", ")) + ')' + (s.cluster > RULES.cluster_max ? ' · cluster of ' + s.cluster + ': ' + esc(s.clusterIds.join(", ")) : "") + '</span></div>';
    });
    r.loose.forEach(function (p) { rows += row(p, "interactive, read by no validation and no binding"); });
    r.orphan.forEach(function (p) { rows += row(p, "media nothing points at"); });
    if (!rows) rows = '<p class="ed-a11y-ok" style="padding:0.6em 0.9em">✅ Nothing above the rules\' defaults — ' + r.parts.length + ' components across ' + r.loadRows.length + ' section' + (r.loadRows.length === 1 ? "" : "s") + '.</p>';
    var rules = '<details id="ed-load-rules"><summary>⚖️ ' + Object.keys(RULES).length + ' rules with defaults — the author answers for these</summary><table>'
      + Object.keys(RULES).map(function (k) { var w = WORDS[k] || [k, ""]; return '<tr><td>' + esc(w[0]) + '</td><td><b>' + esc(String(RULES[k])) + '</b></td><td>' + esc(w[1]) + '</td></tr>'; }).join("") + '</table></details>';
    list.innerHTML = html + rows + rules;
    record({ load: n });
  }

  function mount() {
    var pane = document.getElementById("ed-a11y-pane");
    if (!pane || document.getElementById("ed-load-bar")) return;
    var bar = document.createElement("div"); bar.id = "ed-load-bar";
    bar.innerHTML = '<a href="#" class="button" id="ed-load-run">🧠 Check load</a><span id="ed-load-note">coherence · load · friction · seduction — from the page as rendered; every run, with the audit\'s, is kept beside the page in __&lt;page&gt;_audit.yaml</span> <span id="ed-load-file"></span>';
    var list = document.createElement("div"); list.id = "ed-load-list";
    var h = document.createElement("div"); h.id = "ed-load-hist";
    pane.appendChild(bar); pane.appendChild(list); pane.appendChild(h);
    renderHist();
    loadFile().then(renderHist);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("#ed-load-run"); if (!b) return;
    e.preventDefault(); run();
  });
  var tries = 0;
  (function boot() { mount(); if (!document.getElementById("ed-load-bar") && tries++ < 60) setTimeout(boot, 500); })();
  window.lcLoadCheck = { run: run, analyse: analyse };
})();
</script>
