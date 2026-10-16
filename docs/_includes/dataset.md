{%- comment -%}
Dataset / Datagrid — data binding primitives.

.dataset  — hidden block that parses + registers data
.datagrid — sortable paginated table bound to a dataset
(.chart — bound and inline variants — lives in chart.md)

Usage:
  ```json
  [{"month":"Jan","sales":100},{"month":"Feb","sales":150}]
  ```
  {: .dataset #sales }

  [Sales Table](#)
  {: .datagrid bind="sales" rows="5" }

Formats: JSON (default) or CSV are auto-detected; add format="yaml" to parse a
YAML block. Arrays register as rows; a plain object (e.g. a schema/index) is
registered as-is, so components like .record can read structured config.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* ── dataset (invisible) ───────────────────────────── */
.highlighter-rouge.dataset, .dataset { display: none !important; }

/* ── datagrid ──────────────────────────────────────── */
.lc-datagrid { margin: 1em 0; font-size: 0.88em; overflow-x: auto; }
/* a titled grid: the form's bar at the form's size (the grid's text is 0.88em) */
.lc-datagrid .lc-dg-titlebar { font-size: 0.966em; }
.lc-datagrid .lc-dg-titlebar .lc-datagrid-name { color: #222; font-weight: 600; }
.lc-dg-table { width: 100%; border-collapse: collapse; }
.lc-dg-table th, .lc-dg-table td { padding: 0.4em 0.75em; border: 1px solid #e5e7eb; text-align: left; white-space: nowrap; }
.lc-dg-table th { background: #f9fafb; font-weight: 600; color: #374151; cursor: pointer; user-select: none; }
.lc-dg-table th.lc-th-hint { text-decoration: underline dotted #9ca3af; text-underline-offset: 3px; cursor: help; }
.lc-dg-table th:hover { background: #f3f4f6; }
/* an editable cell has to LOOK editable — a dotted underline and a caret,
   so a reader sees where the page invites them to type */
.lc-dg-table td.lc-dg-edit { cursor: text; background: #fcfdff;
  border-bottom: 1px dashed #9db6d0; }
.lc-dg-table td.lc-dg-edit:focus { outline: 2px solid #0066cc; outline-offset: -2px;
  background: #fff; }
.lc-dg-table tr:nth-child(even) td { background: #fafafa; }
.lc-dg-table td { color: #111827; user-select: text; }
.lc-dg-scroll { overflow: auto; }
.lc-dg-scroll .lc-dg-table thead th { position: sticky; top: 0; z-index: 1; }
.lc-dg-pages { display: flex; align-items: center; gap: 0.5em; margin-top: 0.5em; font-size: 0.82em; color: #6b7280; }
.lc-dg-pages button { background: none; border: 1px solid #d1d5db; border-radius: 4px; padding: 0.15em 0.55em; cursor: pointer; color: #374151; }
.lc-dg-pages button:hover { background: #f3f4f6; }
.lc-dg-table tbody tr { cursor: pointer; }
.lc-dg-table tr.lc-dg-selected td { background: #e8f0fe !important; }
/* A CLASS IS A DATASET (Michel, 2026-10-15): a grid on a class dresses the
   rows — the state cell wears a ⌄ that drops the row's verbs, legal ones
   live and the others grey; typed cells; ➕ New under the list. */
.lc-datagrid { position: relative; }
.lc-dg-table td.lc-dg-typed { border-bottom: 1px dashed #9db6d0; }
.lc-dg-table td.lc-dg-typed:focus { outline: 2px solid #0066cc; outline-offset: -2px; background: #fff; }
.lc-dg-table td.lc-dg-state { cursor: pointer; white-space: nowrap; }
/* the chip and the ⌄ sit on the row's own text line: an inline chip (its
   padding never lifts the line), the ⌄ nudged up to the x-height — a block
   chip rode high and a floated ⌄ sank (Michel, 2026-10-16) */
.lc-dg-chip { display: inline-block; vertical-align: baseline; background: #eef2ff; color: #3730a3; border-radius: 1em; padding: 0 .6em; line-height: 1.45; }
/* every stage's chip as wide as the longest stage: the ⌄ line up in one column (Michel, 2026-10-16) */
.lc-dg-state .lc-dg-chip { box-sizing: content-box; }
.lc-dg-caret { display: inline-block; margin-left: .45em; color: #6b7280; position: relative; top: -.22em; line-height: 1; }
.lc-dg-state .lc-dg-chip { text-align: center; }
.lc-dg-table th { position: relative; }
/* the grip SHOWS (Michel, 2026-10-16: "why can't the columns be resized?" —
   an invisible 7 px strip, and a click beside it sorted instead): a thin bar
   on every header's right edge, blue under the pointer, 10 px to grab */
.lc-dg-grip { position: absolute; top: 15%; right: 0; width: 10px; height: 70%; cursor: col-resize; z-index: 2; touch-action: none;
  background: linear-gradient(90deg, transparent 4px, #cbd5e1 4px, #cbd5e1 6px, transparent 6px); }
.lc-dg-grip:hover, .lc-dg-grip:active { background: linear-gradient(90deg, transparent 3px, #0066cc 3px, #0066cc 7px, transparent 7px); }
.lc-dg-table td.lc-dg-rowmenu { position: relative; padding-right: 1.8em; }
.lc-dg-table td.lc-dg-rowmenu::after { content: "⌄"; position: absolute; right: .55em; top: 50%; transform: translateY(-62%);
  color: #6b7280; cursor: pointer; line-height: 1; }
.lc-dg-table td.lc-dg-rowmenu:hover::after { color: #0066cc; }
.lc-dg-table td.lc-dg-rowmenu.lc-dg-typing::after { display: none; }
.lc-dg-table td.lc-dg-typed.lc-dg-typing { background: #fff; outline: 2px solid #0066cc; outline-offset: -2px; cursor: text; }
.lc-dg-state:hover .lc-dg-caret { color: #0066cc; }
.lc-dg-pick { font: inherit; font-size: .95em; border: 1px solid #d1d5db; border-radius: 4px; background: #fff; padding: .1em .3em; }
.lc-dg-menu { position: absolute; z-index: 1000; background: #fff; border: 1px solid #d1d5db; border-radius: 8px; box-shadow: 0 6px 18px rgba(0,0,0,.14); padding: .25em; min-width: 11em; }
.lc-dg-verb { display: flex; justify-content: space-between; gap: 1em; width: 100%; text-align: left; background: none; border: 0; padding: .4em .7em; cursor: pointer; font: inherit; color: #111827; border-radius: 5px; }
.lc-dg-verb:hover { background: #f3f4f6; }
.lc-dg-verb small { color: #6b7280; }
.lc-dg-verb.lc-dg-off { color: #9ca3af; }
.lc-dg-verb.lc-dg-off small { color: #c4c7cc; }
.lc-dg-verb.lc-dg-danger { color: #b91c1c; border-top: 1px solid #eee; border-radius: 0 0 5px 5px; }
.lc-dg-foot { margin-top: .4em; }
.lc-dg-new { font: inherit; font-size: .85em; font-weight: 500; padding: .35em 1em; border-radius: 6px; border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; }
.lc-dg-new:hover { background: #0052a3; border-color: #0052a3; }
.lc-dg-reload { float: right; font: inherit; font-size: 1em; line-height: 1; padding: .1em .45em; border-radius: 6px;
  border: 1px solid #cbd5e1; background: #fff; color: #0066cc; cursor: pointer; }
.lc-dg-reload:hover { background: #eff6ff; border-color: #0066cc; }
.lc-ds-key { display: flex; flex-wrap: wrap; gap: .5em; align-items: center; margin: .6em 0; padding: .55em .8em;
  border: 1px dashed #93c5fd; border-radius: 8px; background: #f8fbff; font-size: .9em; color: #1e3a8a; }
.lc-ds-key input { flex: 1 1 16em; font: inherit; padding: .3em .5em; border: 1px solid #cbd5e1; border-radius: 6px; }
.lc-ds-key button { font: inherit; font-weight: 500; padding: .3em 1em; border-radius: 6px; border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; }
.lc-dg-say { margin-top: .4em; padding: .35em .7em; border-radius: 6px; background: #fff7ed; color: #9a3412; border: 1px solid #fed7aa; font-size: .9em; }

/* ── button ─────────────────────────────────────────── */
.lc-button { display: inline-block; background: #0066cc; color: #fff; border: none; border-radius: 6px; padding: 0.4em 1.1em; font-size: 0.88em; font-weight: 500; cursor: pointer; margin: 0.5em 0; }
.lc-button:hover { background: #0052a3; }
.lc-button[data-color="muted"]   { background: #9ca3af; }
.lc-button[data-color="danger"]  { background: #ef4444; }
.lc-button[data-color="success"] { background: #22c55e; }
.lc-dbx { font-size: 0.85em; color: #6b7280; border: 1px dashed #d1d5db; border-radius: 8px; padding: 6px 10px; margin: 6px 0 10px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.lc-dbx input { flex: 1 1 220px; font-family: monospace; font-size: 0.95em; padding: 4px 6px; border: 1px solid #cbd5e1; border-radius: 6px; }
.lc-dbx button { font-size: 0.9em; padding: 3px 10px; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; cursor: pointer; }
.lc-dbx .lc-dbx-ok { color: #166534; }
.lc-dbx .lc-dbx-err { color: #b91c1c; }
</style>

<script>
(function () {

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  window.lcDatasets = window.lcDatasets || {};
  window.lcDatasetListeners = window.lcDatasetListeners || {};

  /* ── async dataset registration ─────────────────── */
  if (!window.lcSetDataset) {
    window.lcSetDataset = function (id, data) {
      window.lcDatasets[id] = data;
      /* A LISTENER DIES WITH ITS PART. A pad re-renders its preview on every
         pause in typing; each new grid, chart or class added a listener and
         the replaced ones kept repainting off-screen — one more per pause, the
         freeze growing with it (Michel, 2026-10-16: "typing is slow"). A
         listener tagged with its element (_lcEl) is dropped once that element
         has left the page. */
      var L = window.lcDatasetListeners[id] || [];
      var live = L.filter(function (fn) {
        var e = fn._lcEl;
        if (!e) return true;
        if (e.isConnected) { fn._lcSeen = 1; return true; }
        return !fn._lcSeen;
      });
      if (live.length !== L.length) window.lcDatasetListeners[id] = live;
      live.forEach(function (fn) { try { fn(data); } catch (e) {} });
    };
  }
  /* what a class's grid says when a verb or an edit is refused: one line
     under every grid bound to that class, gone after a few seconds */
  window.lcGridSay = function (cls, msg) {
    document.querySelectorAll(".lc-datagrid[data-bind='" + cls + "']").forEach(function (g) {
      var s = g.querySelector(".lc-dg-say");
      if (!s) { s = document.createElement("div"); s.className = "lc-dg-say"; g.appendChild(s); }
      s.textContent = msg;
      clearTimeout(s._t);
      s._t = setTimeout(function () { if (s.parentNode) s.parentNode.removeChild(s); }, 4500);
    });
  };

  /* ONE MORE ROW (Michel, 2026-10-16: "an API where data is read but also
     written"). dataset.append(row) from Python lands here: the row shows at
     once; a list read from a sheet that takes writes (a key: link) also gets
     it POSTed — a simple request, so no preflight — then is read back, the
     sheet's truth replacing the guess. */
  window.lcRemote = window.lcRemote || {};
  /* A LIST THAT LIVES ELSEWHERE IS READ AGAIN (Michel, 2026-10-16: "how to
     refresh the grid after a change made directly in the sheet?"): coming
     back to the page — from the sheet's tab — re-reads every such list once
     (not more often than every 5 s); its grid's ↻ re-reads it on demand;
     refresh="30" on the dataset re-reads it every 30 s. */
  window.lcRemoteReload = function (id) {
    var r = window.lcRemote[id];
    if (!r) return false;
    r.at = performance.now();
    r.pull();
    return true;
  };
  if (!window._lcRemoteVis) {
    window._lcRemoteVis = 1;
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState !== "visible") return;
      Object.keys(window.lcRemote).forEach(function (id) {
        var r = window.lcRemote[id];
        if (r && performance.now() - (r.at || 0) > 5000) window.lcRemoteReload(id);
      });
    });
  }
  window.lcDatasetAppend = function (id, rowJson) {
    var row = typeof rowJson === "string" ? JSON.parse(rowJson) : rowJson;
    var arr = Array.isArray(window.lcDatasets[id]) ? window.lcDatasets[id].filter(function (r) { return !r["⚠️"]; }) : [];
    arr.push(row);
    window.lcSetDataset(id, arr);
    var r = window.lcRemote[id];
    if (!r || !r.write) return;
    fetch(r.href, { method: "POST", mode: "no-cors", headers: { "Content-Type": "text/plain;charset=utf-8" },
                    body: JSON.stringify({ append: row }) })
      .then(function () { setTimeout(r.pull, 1200); })
      .catch(function (e) {
        if (window.lcGridSay) window.lcGridSay(id, "⚠️ the sheet did not take the row: " + e.message);
      });
  };
  /* A LINK THAT IS A KEY. [the walk sheet](key:walk_sheet) — the address of a
     sheet that takes writes is a key: it lives on the device, never in the
     page or the repo (the keys-in-browser ruling). Missing, the page asks
     for it once, in a small field under where the list would be. */
  function linkKey(name) { try { return localStorage.getItem("lc_link_" + name) || ""; } catch (e) { return ""; } }
  function askLink(el, id, name, label) {
    var box = document.createElement("div");
    box.className = "lc-ds-key";
    box.setAttribute("data-lc-key", name);
    box.innerHTML = "<span>🔑 " + (label || name).replace(/</g, "&lt;") + " — paste its link (kept on this device only)</span>"
      + "<input type='url' placeholder='https://…' aria-label='the link of " + (label || name).replace(/'/g, "") + "'>"
      + "<button type='button'>Connect</button>";
    el.parentNode.insertBefore(box, el.nextSibling);
    var inp = box.querySelector("input"), go = box.querySelector("button");
    var done = function () {
      var v = (inp.value || "").trim();
      if (!/^https:\/\//.test(v)) { inp.focus(); return; }
      try { localStorage.setItem("lc_link_" + name, v); } catch (e) {}
      box.parentNode.removeChild(box);
      delete el.dataset.lcDsDone;
      upgradeDataset(el);
    };
    go.addEventListener("click", done);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); done(); } });
    window.lcSetDataset(id, []);
  }

  /* ── CSV parser ─────────────────────────────────── */
  function parseCSV(text) {
    var lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return [];
    var headers = splitCSVRow(lines[0]);
    return lines.slice(1).filter(function (l) { return l.trim(); }).map(function (l) {
      var vals = splitCSVRow(l);
      var row = {};
      headers.forEach(function (h, i) {
        var v = vals[i] !== undefined ? vals[i] : "";
        row[h] = v !== "" && !isNaN(v) ? +v : v;
      });
      return row;
    });
  }
  function splitCSVRow(line) {
    var out = [], cur = "", inQ = false;
    for (var i = 0; i < line.length; i++) {
      var ch = line[i];
      if (ch === '"') { inQ = !inQ; }
      else if (ch === ',' && !inQ) { out.push(cur.trim()); cur = ""; }
      else cur += ch;
    }
    out.push(cur.trim());
    return out;
  }

  /* extract a nested array (path="a.b") and turn an object-of-equal-length-
     arrays (e.g. Open-Meteo's daily/hourly) into rows — so live APIs that nest
     or columnarise their data still bind to grids and charts. */
  function shapeData(data, el) {
    var path = el.getAttribute("path");
    if (path) {
      path.split(".").forEach(function (k) {
        if (data && typeof data === "object" && data[k] != null) data = data[k];
      });
    }
    if (data && !Array.isArray(data) && typeof data === "object") {
      var keys = Object.keys(data);
      if (keys.length && keys.every(function (k) { return Array.isArray(data[k]); })) {
        var n = data[keys[0]].length;
        if (keys.every(function (k) { return data[k].length === n; })) {
          var rows = [];
          for (var i = 0; i < n; i++) {
            var row = {};
            keys.forEach(function (k) { row[k] = data[k][i]; });
            rows.push(row);
          }
          return rows;
        }
      }
    }
    if (Array.isArray(data)) return data;
    if (data && typeof data === "object") return data;   // a plain object (e.g. a schema index) is kept as-is, not wrapped
    return [data];
  }

  /* parse inline/remote text as JSON, YAML (format="yaml"), or CSV, then register */
  function setFromText(text, fmt, el, id) {
    if ((fmt === "yaml" || fmt === "yml") && window.lcYaml) {
      window.lcYaml.ready(function () {
        var data; try { data = window.lcYaml.load(text); } catch (e) { data = [{ "⚠️": "YAML: " + e.message }]; }
        window.lcSetDataset(id, shapeData(data, el));
      });
      return;
    }
    var data;
    try { data = JSON.parse(text); } catch (e) { data = parseCSV(text); }
    window.lcSetDataset(id, shapeData(data, el));
  }

  /* ── .dataset upgrade ───────────────────────────── */
  function upgradeDataset(el) {
    if (el.dataset.lcDsDone) return; el.dataset.lcDsDone = "1";
    /* of="SomeModel": the rows are ADOPTED by a model class — same fence,
       one grammar (Michel, 2026-08-22: "KISS that"). The model machinery
       owns the hydration; retry briefly if its include has not parsed yet. */
    if (el.getAttribute("of")) {
      (function adopt(tries) {
        if (window.lcAdoptRows) { delete el.dataset.lcRowsDone; window.lcAdoptRows(el); return; }
        if (tries < 50) setTimeout(function () { adopt(tries + 1); }, 200);
      })(0);
      return;
    }
    var id = el.id || el.getAttribute("id");
    if (!id) return;

    /* remote variant: apply {: .dataset #x } to a link → fetch its href */
    var link = el.querySelector("a[href]");
    if (link) {
      var href = link.getAttribute("href");
      /* forgiving: authors often write the URL as the visible link text
         with a dummy "#" href — use the text when it looks like a URL */
      if (!/^(https?:\/\/|\/)/.test(href) && /^https?:\/\//.test((link.textContent || "").trim())) {
        href = link.textContent.trim();
      }
      var keyName = (/^key:([A-Za-z_][\w-]*)$/.exec(href) || [])[1] || "";
      if (keyName) {
        href = linkKey(keyName);
        if (!href) { askLink(el, id, keyName, (link.textContent || "").trim()); return; }
      }
      /* A GOOGLE SHEET'S OWN LINK READS AS ROWS (Michel, 2026-10-16: the grid
         stayed empty on a …/edit?usp=sharing link — that address sends the
         editor's web page, which a page may not read). Its CSV door does,
         for a sheet shared "anyone with the link can view"; #gid= keeps the tab. */
      var gsh = /^https:\/\/docs\.google\.com\/spreadsheets\/d\/([\w-]+)/.exec(href);
      if (gsh && !/\/gviz\/|\/export|output=csv|\/pub/.test(href)) {
        var gid = (/[#&?]gid=(\d+)/.exec(href) || [])[1];
        href = "https://docs.google.com/spreadsheets/d/" + gsh[1] + "/gviz/tq?tqx=out:csv" + (gid ? "&gid=" + gid : "");
      }
      /* sheet="Sheet1" — WHICH TAB (Michel, 2026-10-16: "why don't you use the
         Sheet1 name anywhere?"): a sheet with no tab named sends its first
         one; sheet= names it, for the CSV door and for the sheet's script
         (both read ?sheet=, the script writes there too) */
      var tab = el.getAttribute("sheet");
      if (tab && /^https:\/\//.test(href) && !/[?&]sheet=/.test(href))
        href += (href.indexOf("?") < 0 ? "?" : "&") + "sheet=" + encodeURIComponent(tab);
      if (/^(https?:\/\/|\/)/.test(href)) {
        var fmt = (el.getAttribute("format") || "").toLowerCase();
        if (!fmt && /\.ya?ml($|\?)/i.test(href)) fmt = "yaml";
        var tick = 0;
        var pull = function () {
          /* cache-bust so a just-landed file (results, fleet) is seen now,
             not from the 60s API/Pages cache — this is the whole point of
             refresh= (a counter, since Date is engine-blocked) */
          fetch(href + (href.indexOf("?") < 0 ? "?" : "&") + "_t=" + (tick++), { cache: "no-store" })
            .then(function (r) {
              /* 404 is not a fault — it means this node carries no such data.
                 The fleet board and the backlog are lab-only instruments the
                 gate never publishes, so on pedia they are simply absent, and
                 the page already promises "an empty board". Showing ⚠️ HTTP 404
                 turned a by-design absence into what looks like a broken site.
                 Every other status stays an error, because those ARE faults. */
              if (r.status === 404) { window.lcSetDataset(id, []); return null; }
              if (!r.ok) throw new Error("HTTP " + r.status);
              return r.text();
            })
            .then(function (text) {
              if (text === null) return;
              /* a web page is not rows: say so, instead of an empty table */
              if (/^\s*<(!doctype|html|head|body)/i.test(text))
                throw new Error("this link sends a web page, not rows — use the sheet's data link");
              setFromText(text, fmt, el, id);
            })
            .catch(function (e) {
              var cur = window.lcDatasets[id];
              if (!cur || !cur.length) window.lcSetDataset(id, [{ "⚠️": e.message === "Failed to fetch"
                ? "this link cannot be read from a page (not shared, or not a data link)" : e.message }]);
            });
        };
        window.lcRemote[id] = { href: href, pull: pull, write: !!keyName || el.getAttribute("write") === "true", at: performance.now() };
        pull();
        /* refresh="30" → live mode: re-pull every N seconds. Republishing to
           the bus repaints every bound grid/stat/chart with no page reload —
           the generic auto-refresh, not a dashboard special-case. */
        var every = parseInt(el.getAttribute("refresh") || "0", 10);
        if (every > 0) setInterval(pull, Math.max(10, every) * 1000);
        return;
      }
      /* RELATIVE LINK — a pile that LIVES IN A FILE (Michel, 2026-10-03:
         "why is there a yaml if we use the dogs yaml file?"). The fence was
         a second truth for the same rows, so a dataset can now be declared
         by its file alone: [dogs](../module_00/dogs.yaml) + {: .dataset #dogs }.
         The learner's bench copy wins when there is one; otherwise the
         lesson's own copy, read from the course repo beside the page. */
      if (href && href !== "#") {
        var rfmt = (el.getAttribute("format") || "").toLowerCase();
        if (window.lcInferFormat) rfmt = window.lcInferFormat(href, rfmt);
        var fromSource = function () {
          var srcEl = el.closest ? el.closest("[data-lc-src-path]") : null;
          if (!srcEl) srcEl = document.querySelector(".lc-run[data-lc-src-path]");
          var srcPath = srcEl ? (srcEl.getAttribute("data-lc-src-path") || "") : "";
          var dir = srcPath.indexOf("/") >= 0 ? srcPath.replace(/\/[^\/]*$/, "") : "";
          var parts = [];
          (dir ? dir + "/" + href : href).split("/").forEach(function (p) {
            if (!p || p === ".") return;
            if (p === "..") parts.pop(); else parts.push(p);
          });
          var repo = (srcEl && srcEl.getAttribute("data-lc-src-repo")) || _lcSiteRepo;
          var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
          var h = { Accept: "application/vnd.github.v3.raw" };
          if (pat) h.Authorization = "Bearer " + pat;
          return fetch("https://api.github.com/repos/" + repo + "/contents/" + parts.join("/"), { headers: h })
            .then(function (r) {
              if (r.status === 404) return null;
              if (!r.ok) throw new Error("HTTP " + r.status);
              return r.text();
            });
        };
        var bench = window.lcBench
          ? window.lcBench.read(href, el).then(function (f) { return f ? f.text : null; })
          : Promise.resolve(null);
        bench.catch(function () { return null; })
          .then(function (text) {
            if (text !== null) { el.setAttribute("data-lc-mine", "1"); return text; }
            return fromSource();
          })
          .then(function (text) {
            if (text === null) { window.lcSetDataset(id, []); return; }
            setFromText(text, rfmt, el, id);
          })
          .catch(function (e) { if (!window.lcDatasets[id]) window.lcSetDataset(id, [{ "⚠️": e.message }]); });
        return;
      }
    }

    /* Databricks variant: the fence is SQL, dbx="<warehouse id>" names the
       warehouse. The statement goes through a same-origin proxy (host=,
       default /dbx) that forwards the browser's OWN token and stores nothing
       — the key lives on this device like every other key here, and no
       server ever holds it (Michel, 2026-09-26: "the perfect match with
       the CFO's need to not share strategic data with anyone else"). */
    if (el.getAttribute("dbx")) { dbxDataset(el, id); return; }

    /* inline code block variant */
    var code = el.querySelector("code") || el;
    var seed = code.textContent.trim();
    var fmt = (el.getAttribute("format") || window.lcFenceFormat(el) || "").toLowerCase();

    /* save="…" — the same contract every other component with a save= knob
       already follows: the fence is the AUTHOR'S seed, the learner's file is
       the truth. A dataset could not read a bench until now, so a lesson had
       no way to feed today's screen from the file the reader repaired
       yesterday — and "watch your own fix land somewhere new" is the whole
       reason the second lesson is worth sitting through.
       Seed FIRST, then replace: a bench read is a network round trip and a
       page that starts blank teaches nothing while it waits. lcSetDataset
       notifies every listener, so the swap re-derives each bound view. */
    var savePath = el.getAttribute("save") || "";
    if (savePath && window.lcBench) {
      setFromText(seed, fmt, el, id);
      window.lcBench.read(savePath, el).then(function (f) {
        if (!f) return;
        el.setAttribute("data-lc-mine", "1");
        setFromText(f.text, window.lcInferFormat
          ? window.lcInferFormat(savePath, fmt) : fmt, el, id);
      }).catch(function () {});
      return;
    }
    setFromText(seed, fmt, el, id);
  }

  /* ── Databricks: a SQL statement on a warehouse, with this device's token ── */
  var DBX_KEY = "lc_key_dbx";
  function dbxToken() { try { return localStorage.getItem(DBX_KEY) || ""; } catch (e) { return ""; } }
  function dbxKeep(v) { try { if (v) localStorage.setItem(DBX_KEY, v); else localStorage.removeItem(DBX_KEY); } catch (e) {} }
  var DBX_NUM = /^(INT|LONG|SHORT|BYTE|FLOAT|DOUBLE|DECIMAL)/i;
  function dbxDataset(el, id) {
    var code = el.querySelector("code") || el;
    var sql = code.textContent.trim();
    var wh = el.getAttribute("dbx");
    var host = (el.getAttribute("host") || "/dbx").replace(/\/$/, "");
    var every = parseInt(el.getAttribute("refresh") || "0", 10);
    /* the fence is invisible, as every dataset is; the bar beside it is
       where the token is pasted once and where the run reports */
    var bar = document.createElement("div");
    bar.className = "lc-dbx"; bar.setAttribute("data-lc-dbx", id);
    bar.innerHTML = '<span class="lc-dbx-status"></span>' +
      '<input type="password" class="lc-dbx-token" placeholder="Databricks token — stays in this browser" aria-label="Databricks token" hidden>' +
      '<button type="button" class="lc-dbx-save" hidden>Save</button>' +
      '<button type="button" class="lc-dbx-change">🔑 token</button>';
    el.parentNode.insertBefore(bar, el.nextSibling);
    var status = bar.querySelector(".lc-dbx-status"), input = bar.querySelector(".lc-dbx-token"),
        save = bar.querySelector(".lc-dbx-save"), change = bar.querySelector(".lc-dbx-change");
    function say(t, cls) { status.textContent = t; status.className = "lc-dbx-status" + (cls ? " " + cls : ""); }
    function ask(open) { input.hidden = save.hidden = !open; if (open) input.focus(); }
    change.addEventListener("click", function () { ask(input.hidden); });
    save.addEventListener("click", function () { dbxKeep(input.value.trim()); input.value = ""; ask(false); run(); });
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") save.click(); });
    function headers(tok) { return { Authorization: "Bearer " + tok, "Content-Type": "application/json", Accept: "application/json" }; }
    function asJson(r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); }
    function run() {
      var tok = dbxToken();
      if (!tok) { window.lcSetDataset(id, []); say("🔑 paste your Databricks token to run this query", "lc-dbx-err"); ask(true); return; }
      say("⏳ running on warehouse " + wh + "…");
      var H = headers(tok);
      fetch(host + "/api/2.0/sql/statements", { method: "POST", headers: H, cache: "no-store",
        body: JSON.stringify({ warehouse_id: wh, statement: sql, wait_timeout: "30s", disposition: "INLINE", format: "JSON_ARRAY" }) })
        .then(asJson)
        .then(function step(d) {
          if (!d.ok) throw new Error(d.status === 401 || d.status === 403 ? "token refused — paste a fresh one" : ("HTTP " + d.status + (d.j && d.j.message ? " — " + d.j.message : "")));
          var st = d.j.status && d.j.status.state;
          if (st === "PENDING" || st === "RUNNING")
            return new Promise(function (res) { setTimeout(res, 1000); })
              .then(function () { return fetch(host + "/api/2.0/sql/statements/" + d.j.statement_id, { headers: H, cache: "no-store" }); })
              .then(asJson).then(step);
          if (st !== "SUCCEEDED") throw new Error((d.j.status && d.j.status.error && d.j.status.error.message) || ("statement " + (st || "failed")));
          var cols = ((d.j.manifest || {}).schema || {}).columns || [];
          var rows = [];
          var take = function (arr) {
            (arr || []).forEach(function (a) {
              var o = {};
              cols.forEach(function (c, i) {
                var v = a[i];
                o[c.name] = (v !== null && v !== undefined && DBX_NUM.test(c.type_name || "") && v !== "" && !isNaN(v)) ? Number(v) : v;
              });
              rows.push(o);
            });
          };
          take((d.j.result || {}).data_array);
          /* a large result comes in chunks — follow them to the end */
          var more = function (link) {
            if (!link) return rows;
            return fetch(host + link, { headers: H, cache: "no-store" }).then(asJson).then(function (c) {
              if (!c.ok) throw new Error("HTTP " + c.status + " on a result chunk");
              take(c.j.data_array); return more(c.j.next_chunk_internal_link);
            });
          };
          return more((d.j.result || {}).next_chunk_internal_link);
        })
        .then(function (rows) { window.lcSetDataset(id, rows); say("✓ " + rows.length + " row" + (rows.length === 1 ? "" : "s") + " from warehouse " + wh, "lc-dbx-ok"); })
        .catch(function (e) { window.lcSetDataset(id, [{ "⚠️": e.message }]); say("⚠️ " + e.message, "lc-dbx-err"); });
    }
    run();
    if (every > 0) setInterval(run, Math.max(10, every) * 1000);
  }

  /* ── .datagrid upgrade ──────────────────────────── */
  function upgradeDatagridBound(el) {
    if (el.dataset.lcDgDone || el.dataset.lcUpgraded) return;
    var bindId = el.getAttribute("source") || el.getAttribute("bind");
    if (!bindId) return; /* skip old-style code-block datagrids */
    /* source="file:path" loads a repo file (read format now — el is replaced below) */
    var fileRef = bindId.indexOf("file:") === 0 ? bindId.slice(5).trim() : "";
    var fileFmt = fileRef && window.lcInferFormat ? window.lcInferFormat(fileRef, el.getAttribute("format")) : "yaml";
    el.dataset.lcDgDone = "1";
    var perPage = parseInt(el.getAttribute("rows") || "0", 10) || 0;
    /* height="…" — a SCROLLING table with a sticky header, never pages: a
       roster of a class is read in one glance, not in pages of eight with
       the last one half empty (Michel, 2026-09-04). height wins over rows. */
    var height = parseInt(el.getAttribute("height") || "0", 10) || 0;
    if (height) perPage = 0;
    /* hints="col: explanation | col2: ..." → header tooltips. Read from the
       declaration HERE — below, el is reassigned to the fresh wrapper and
       the original attributes are gone with the replaced element. */
    var hints = {};
    (el.getAttribute("hints") || "").split("|").forEach(function (h) {
      var i = h.indexOf(":");
      if (i > 0) hints[h.slice(0, i).trim()] = h.slice(i + 1).trim();
    });

    /* empty="…" — what to say when the dataset is legitimately empty. The
       default reads like a fault, which is wrong for a grid that is simply
       waiting on a choice made elsewhere (pick a course → see its pages). */
    var emptyMsg = el.getAttribute("empty") || "";
    /* EDITABLE WAS SILENTLY IGNORED HERE. A grid bound to a dataset is
       rendered by this light table, not by the AG path in datagrid.md — so
       `editable="true"` looked like a knob and did nothing at all: "the grid
       looks r/o", and on iPhone "double tap did not work" while tutorial-01
       (an AG grid) was fine (Michel, 2026-08-20).

       Editing lands here instead of borrowing AG, and it is BETTER on the
       device this course is read on: a contenteditable cell takes ONE tap,
       where AG needs a double-click that phones barely deliver. */
    var editable = el.getAttribute("editable") === "true";
    /* a grid on a CLASS edits by default — a double click (or a second tap
       on the selected row) opens a cell; editable="false" says otherwise
       (Michel, 2026-10-16) */
    var editSaid = el.getAttribute("editable") || "";
    var pendingNew = null, typeNew = null;   /* the objects before ➕ New: the one that is not among them gets selected */
    var lcId = el.getAttribute("id") || "";
    var masterId = el.getAttribute("master") || el.getAttribute("detail-of") || "";
    var filterExpr = el.getAttribute("filter") || "";
    /* sort="<column>": the order the table opens in — a roster by name
       (Canvas writes "Last, First", so that is by last name), a work
       table by module (Michel, 2026-09-11). A header click still re-sorts. */
    var sortAttr = el.getAttribute("sort") || null;
    /* columns="topic, title": the table SHOWS these, in this order, and still
       PUBLISHES the whole row — a narrow list on the left of a bound card that
       reads every field (Michel, 2026-10-04, the stories example). */
    var shownCols = (el.getAttribute("columns") || "").split(",")
      .map(function (c) { return c.trim(); }).filter(Boolean);
    /* A TITLE BAR LIKE THE FORM'S (Michel, 2026-10-10: "the grid's header
       should be as big as the Form one"): ▦ and the words of the link that
       declared it — [The dogs](#) — or title="…". The table goes under it. */
    var link = el.querySelector ? el.querySelector("a") : null;
    var gridTitle = el.getAttribute("title") || (link ? (link.textContent || "").trim() : "");
    var wrap = document.createElement("div");
    wrap.className = "lc-datagrid";
    wrap.setAttribute("data-bind", bindId);
    if (lcId) wrap.setAttribute("data-lc-id", lcId);
    el.parentNode.replaceChild(wrap, el);
    el = wrap;
    var bodyEl = el;
    if (gridTitle) {
      var bar = document.createElement("div");
      bar.className = "lc-datagrid-title lc-dg-titlebar";
      bar.appendChild(document.createTextNode("▦ "));
      var tn = document.createElement("span");
      tn.className = "lc-datagrid-name";
      tn.textContent = gridTitle;
      bar.appendChild(tn);
      bodyEl = document.createElement("div");
      bodyEl.className = "lc-dg-body";
      el.appendChild(bar);
      el.appendChild(bodyEl);
      el.classList.add("lc-dg-titled");
    }

    var sortCol = sortAttr, sortAsc = true, page = 0;
    var colW = {};   /* a column's width the reader dragged, kept across repaints */

    /* grid-to-grid master/detail, the light-table half: the AG road had
       master= + filter="local=masterKey" and this road silently ignored
       both, so on a runner page the detail grid showed everything and a
       click upstream changed nothing (Michel, 2026-08-21). Same contract,
       same attributes — one selection bus for both roads. */
    var masterRow = null, lastData = null, publishedFirst = false;
    var lastPubJson = null;   /* the selected row as last re-published after a repaint */
    var selKey = null;   /* the selected row's identity (obj name, else its index) */
    var touched = null;  /* the row a button just wrote — next() walks on from it */
    var filterKeys = null;
    if (masterId && filterExpr) {
      var fm = filterExpr.match(/^\s*([\w-]+)\s*=\s*([\w-]+)\s*$/);
      if (fm) filterKeys = { local: fm[1], master: fm[2] };
    }
    if (filterKeys && window.lcMasterDetail) {
      window.lcMasterDetail.subscribe(masterId, function (row) {
        masterRow = row;
        /* the master moved: this grid's own detail (a bound form) must not
           keep showing a row that just got filtered away */
        publishedFirst = false;
        if (lastData) render(lastData);
      });
    }

    function render(data) {
      lastData = data;
      /* a list read from elsewhere: a ↻ in the title bar reads it again */
      if (window.lcRemote && window.lcRemote[bindId] && el.querySelector(".lc-dg-titlebar") && !el.querySelector(".lc-dg-reload")) {
        var rb = document.createElement("button");
        rb.type = "button"; rb.className = "lc-dg-reload"; rb.textContent = "↻";
        rb.title = "read it again — the list lives elsewhere";
        rb.setAttribute("aria-label", "read the list again");
        rb.addEventListener("click", function (e) { e.stopPropagation(); window.lcRemoteReload(bindId); });
        el.querySelector(".lc-dg-titlebar").appendChild(rb);
      }
      if (data && filterKeys && masterRow) {
        data = data.filter(function (r) {
          return r[filterKeys.local] === masterRow[filterKeys.master];
        });
      }
      if (!data || !data.length) {
        if (selKey && lcId && window.lcMasterDetail) { selKey = null; window.lcMasterDetail.publish(lcId, null); }
        /* empty for a moment (a class publishes before its rows arrive):
           when rows come, the first one is selected AND announced again —
           the card said "(no data)" over a lit row (Michel, 2026-10-16) */
        publishedFirst = false; lastPubJson = null;
        bodyEl.innerHTML = emptyMsg
          ? "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>" + emptyMsg + "</p>"
          : "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em'>⚠ No data: <code>" + bindId + "</code></p>";
        return;
      }
      var allCols = Object.keys(data[0]);
      var urlCol  = allCols.indexOf("url") >= 0 ? "url" : null;
      /* a grid on a CLASS (a class is a dataset): the model says which cell
         is the state, which are typed, which are locked; obj is the object's
         name, the grid's own business, never a column */
      var model = (window.lcModels || {})[bindId] || null;
      var cols    = allCols.filter(function (c) { return c !== "url" && !(model && (c === "obj" || c.charAt(0) === "_" || !model.fields[c])); });
      if (shownCols.length) cols = shownCols.filter(function (c) { return allCols.indexOf(c) >= 0; });
      function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/'/g, "&#39;"); }
      function dressedCell(row, c, idx) {
        var html = dressedCell0(row, c, idx);
        if (model.state || c !== cols[0]) return html;
        return html.replace(/^<td( class='([^']*)')?/, function (_, k, cls) {
          return "<td class='" + (cls ? cls + " " : "") + "lc-dg-rowmenu' data-row='" + idx + "'";
        });
      }
      function dressedCell0(row, c, idx) {
        var v = row[c] !== undefined && row[c] !== null ? row[c] : "";
        var f = model.fields[c];
        if (f && f.state) {
          var wide = (f.enum || []).reduce(function (m, s) { return Math.max(m, String(s).length); }, String(v).length);
          return "<td class='lc-dg-state' data-row='" + idx + "' title='what this one can do'>"
            + "<span class='lc-dg-chip' style='min-width:" + wide + "ch'>" + esc(v) + "</span><span class='lc-dg-caret'>⌄</span></td>";
        }
        /* a tap on a row SELECTS it; cells open for typing only when the
           grid says editable="true" — the detail form is where one edits
           (Michel, 2026-10-16) */
        if (!f || f.ro || editSaid === "false") return "<td>" + esc(v) + "</td>";
        if (f.enum)
          return "<td><select class='lc-dg-pick' data-col='" + c + "' data-row='" + idx + "'>"
            + [""].concat(f.enum).map(function (o) { return "<option" + (String(o) === String(v) ? " selected" : "") + ">" + esc(o) + "</option>"; }).join("")
            + "</select></td>";
        return "<td class='lc-dg-typed' title='double click to edit' data-col='" + c + "' data-row='" + idx + "'"
          + " inputmode='" + (f.t === "int" || f.t === "float" ? "decimal" : "text") + "'>" + esc(v) + "</td>";
      }

      var sorted = data.slice();
      if (sortCol !== null) {
        sorted.sort(function (a, b) {
          var va = a[sortCol], vb = b[sortCol];
          /* words compare as a reader would: "abeera" before "DWLERS" */
          var diff = (typeof va === "string" && typeof vb === "string")
            ? va.localeCompare(vb, undefined, { sensitivity: "base" })
            : (va > vb ? 1 : va < vb ? -1 : 0);
          return sortAsc ? diff : -diff;
        });
      }
      var total = sorted.length, pp = perPage || total;
      var pages = Math.ceil(total / pp);
      page = Math.min(page, Math.max(0, pages - 1));
      var slice = sorted.slice(page * pp, (page + 1) * pp);

      var html = (height ? "<div class='lc-dg-scroll' style='max-height:" + height + "px'>" : "")
        + "<table class='lc-dg-table'><thead><tr>"
        + cols.map(function (c) {
            var arrow = sortCol === c ? (sortAsc ? " ↑" : " ↓") : "";
            var hint = hints[c] ? " title='" + hints[c].replace(/'/g, "&#39;") + "' class='lc-th-hint'" : "";
            var label = window.lcPrettifyKey ? window.lcPrettifyKey(c) : c;
            var cw = colW[c] ? " style='width:" + colW[c] + "px;min-width:" + colW[c] + "px'" : "";
            return "<th data-col='" + c + "'" + hint + cw + ">" + label + arrow + "<span class='lc-dg-grip' title='drag to resize'></span></th>";
          }).join("") + "</tr></thead><tbody>"
        + slice.map(function (row) {
            var urlVal = urlCol ? (row[urlCol] || "") : "";
            var trAttrs = urlVal ? " data-url='" + urlVal.replace(/'/g, "&#39;") + "' style='cursor:pointer'" : "";
            return "<tr" + trAttrs + ">"
              + cols.map(function (c) {
                  if (model) return dressedCell(row, c, sorted.indexOf(row));
                  var v = row[c] !== undefined ? row[c] : "";
                  /* a UTC stamp prints on the reader's clock, UTC on hover;
                     an editable cell keeps the raw value it will write back */
                  var w = !editable && window.lcWhen ? window.lcWhen(v) : null;
                  if (w) return "<td title='" + w.utc + "'>" + w.text + "</td>";
                  if (!editable) return "<td>" + v + "</td>";
                  /* the row is found again by its position in the CURRENT
                     sort, so an edit after sorting still lands on the row
                     the reader is looking at */
                  return "<td contenteditable='true' class='lc-dg-edit'" +
                         " data-col='" + c + "' data-row='" + sorted.indexOf(row) + "'" +
                         " inputmode='" + (typeof row[c] === "number" ? "decimal" : "text") +
                         "'>" + v + "</td>";
                }).join("") + "</tr>";
          }).join("") + "</tbody></table>" + (height ? "</div>" : "");

      if (model) html += "<div class='lc-dg-foot'><button class='lc-dg-new' type='button' title='a new " + esc(bindId) + ", at its first stage'>➕ New" + ((model.subs || []).length ? " ⌄" : "") + "</button></div>";
      if (pages > 1) {
        html += "<div class='lc-dg-pages'>";
        if (page > 0)         html += "<button data-pg='" + (page - 1) + "'>←</button>";
        html += "<span>Page " + (page + 1) + " / " + pages + "</span>";
        if (page < pages - 1) html += "<button data-pg='" + (page + 1) + "'>→</button>";
        html += "</div>";
      }

      /* THE SCROLL SURVIVES A REPUBLISH. Picking a seat binds its card,
         the card republishes the class, and this table is rebuilt from
         the new rows: the selection was kept (below), the scroll was not —
         the box came back at the top and the picked row sat out of view
         (Michel, 2026-09-15, the desk's roster). Keep where the reader was. */
      var scrollBox = bodyEl.querySelector(".lc-dg-scroll");
      var keepTop = scrollBox ? scrollBox.scrollTop : 0;
      bodyEl.innerHTML = html;
      if (keepTop) { var nb = bodyEl.querySelector(".lc-dg-scroll"); if (nb) nb.scrollTop = keepTop; }
      if (editable) {
        el.querySelectorAll("td.lc-dg-edit").forEach(function (td) {
          /* commit on blur and on Enter — never on every keystroke, or the
             chart would redraw under the finger mid-number */
          var commit = function () {
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            if (!row) return;
            var col = td.getAttribute("data-col");
            var was = row[col];
            var txt = (td.textContent || "").trim();
            /* a column that held numbers keeps holding numbers: a chart
               cannot plot "120 " and a blank must stay blank, not 0 */
            var val = txt;
            if (typeof was === "number" || (was === "" && txt !== "" && !isNaN(Number(txt))))
              val = txt === "" ? "" : Number(txt);
            if (val === was) return;
            row[col] = val;
            if (window.lcSetDataset)
              window.lcSetDataset(bindId, window.lcDatasets[bindId] || data);
          };
          td.addEventListener("blur", commit);
          td.addEventListener("keydown", function (e) {
            if (e.key === "Enter") { e.preventDefault(); td.blur(); }
          });
        });
      }
      if (model) {
        var py = function (code) { if (window.lcPySend) window.lcPySend(code); };
        var objOf = function (td) { var r = sorted[parseInt(td.getAttribute("data-row"), 10)]; return r ? String(r.obj) : ""; };
        /* a typed cell: the value goes through the object — type, enum and
           lock apply there, and a refused value says why under the grid */
        /* a tap SELECTS the row; a double click — or a second tap on the
           row already selected, which a phone can deliver — opens the cell,
           its text selected so typing replaces it; Enter or leaving commits,
           Escape gives up (Michel, 2026-10-16) */
        el.querySelectorAll("td.lc-dg-typed").forEach(function (td) {
          var was = "";
          var open = function () {
            if (td.isContentEditable) return;
            was = td.textContent;
            td.setAttribute("contenteditable", "true");
            td.classList.add("lc-dg-typing");
            td.focus();
            try {
              var r = document.createRange(); r.selectNodeContents(td);
              var sl = window.getSelection(); sl.removeAllRanges(); sl.addRange(r);
            } catch (e) {}
          };
          var shut = function () { td.removeAttribute("contenteditable"); td.classList.remove("lc-dg-typing"); };
          var commit = function () {
            if (!td.isContentEditable) return;
            shut();
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            if (!row) return;
            var col = td.getAttribute("data-col"), txt = (td.textContent || "").trim();
            if (String(row[col] == null ? "" : row[col]) === txt) return;
            py("_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(col) + "," + JSON.stringify(txt) + ")");
          };
          td.addEventListener("click", function () {
            var tr = td.parentNode;
            if (tr && tr.classList.contains("lc-dg-selected")) open();
          });
          td.addEventListener("dblclick", open);
          td.addEventListener("blur", commit);
          td.addEventListener("keydown", function (e) {
            if (!td.isContentEditable) return;
            typeNew = null;   /* typing has begun: no repaint re-opens a fresh cell over it */
            if (e.key === "Enter") { e.preventDefault(); td.blur(); }
            else if (e.key === "Escape") { e.preventDefault(); td.textContent = was; shut(); }
          });
        });
        /* a click in a typed cell or a picklist still selects its row — the
           bound card follows the row being edited (a swallowed click left
           the first row selected, classroom 4's roster, 2026-10-16) */
        el.querySelectorAll("select.lc-dg-pick").forEach(function (sel) {
          sel.addEventListener("change", function () {
            var row = sorted[parseInt(sel.getAttribute("data-row"), 10)];
            if (row) py("_lc_set(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(sel.getAttribute("data-col")) + "," + JSON.stringify(sel.value) + ")");
          });
        });
        /* the ⌄: the row's verbs — a transition is live when the row's state
           is in its pre, grey otherwise (pressing a grey one says what it
           needs); plain verbs always; Delete last, born of Object */
        var closeMenu = function () { document.querySelectorAll(".lc-dg-menu").forEach(function (m) { m.parentNode.removeChild(m); }); };
        var verbsMenu = function (td, e) {
          {
            e.stopPropagation();
            var open = document.querySelector(".lc-dg-menu");
            closeMenu();
            if (open && open._lcFor === td) return;
            var row = sorted[parseInt(td.getAttribute("data-row"), 10)];
            if (!row) return;
            /* the row is marked as selected too (no publish: a follower's
               republish would repaint the table and take the menu with it) */
            var tr = td.parentNode;
            el.querySelectorAll("tbody tr").forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            tr.classList.add("lc-dg-selected");
            selKey = row.obj != null ? "o:" + row.obj : "i:" + parseInt(td.getAttribute("data-row"), 10);
            /* a subclass's row wears its own verbs */
            var rm = (row._kind && (window.lcModels || {})[row._kind]) || model;
            var cur = String(row[rm.state] == null ? "" : row[rm.state]);
            var items = [];
            Object.keys(rm.transitions).forEach(function (n) {
              var tr = rm.transitions[n], ok = !tr.pre.length || tr.pre.indexOf(cur) >= 0;
              items.push({ n: n, ok: ok, hint: ok ? ("→ " + (tr.post || cur)) : ("needs " + tr.pre.join(" / ")) });
            });
            rm.verbs.forEach(function (n) { items.push({ n: n, ok: true, hint: "" }); });
            items.push({ n: "delete", ok: true, hint: "", label: "🗑 Delete", danger: true });
            var menu = document.createElement("div");
            menu.className = "lc-dg-menu";
            menu._lcFor = td;
            menu.innerHTML = items.map(function (it) {
              var label = it.label || (window.lcPrettifyKey ? window.lcPrettifyKey(it.n) : it.n);
              return "<button type='button' class='lc-dg-verb" + (it.ok ? "" : " lc-dg-off") + (it.danger ? " lc-dg-danger" : "")
                + "' data-verb='" + it.n + "' data-ok='" + (it.ok ? 1 : 0) + "' title='" + esc(it.hint) + "'>"
                + "<span>" + esc(label) + "</span>" + (it.hint ? "<small>" + esc(it.hint) + "</small>" : "") + "</button>";
            }).join("");
            /* on the body, fixed: a scrolling grid clipped the last row's
               menu under its frame (Michel, 2026-10-16) */
            var r = td.getBoundingClientRect();
            menu.style.left = (Math.max(4, Math.min(r.left, window.innerWidth - 200)) + window.scrollX) + "px";
            menu.style.top = (r.bottom + window.scrollY) + "px";
            document.body.appendChild(menu);
            var box = el.querySelector(".lc-dg-scroll");
            if (box) box.addEventListener("scroll", closeMenu, { once: true, passive: true });
            menu.querySelectorAll("button[data-verb]").forEach(function (b) {
              b.addEventListener("click", function (ev) {
                ev.stopPropagation();
                var verb = b.getAttribute("data-verb");
                if (b.getAttribute("data-ok") !== "1") { closeMenu(); window.lcGridSay(bindId, "⛔ " + verb + " " + b.getAttribute("title")); return; }
                if (verb === "delete") {
                  var who = cols.filter(function (c) { return c !== model.state; }).map(function (c) { return row[c]; }).filter(Boolean)[0];
                  if (!window.confirm("Delete " + (who || "this one") + "?")) return;
                }
                closeMenu();
                py("_lc_verb(" + JSON.stringify(bindId) + "," + JSON.stringify(String(row.obj)) + "," + JSON.stringify(verb) + ")");
              });
            });
            setTimeout(function () { document.addEventListener("click", closeMenu, { once: true }); }, 0);
          }
        };
        el.querySelectorAll("td.lc-dg-state").forEach(function (td) {
          td.addEventListener("click", function (e) { verbsMenu(td, e); });
        });
        /* A CLASS WITH NO STATE STILL HAS VERBS (Michel, 2026-10-16) — and
           Delete always: the ⌄ sits in the row's first cell, drawn by CSS
           (never part of the value), and only the ⌄ opens the menu; the rest
           of the cell selects and edits as before */
        el.querySelectorAll("td.lc-dg-rowmenu").forEach(function (td) {
          /* capture: the ⌄ wins over the second-tap edit of a selected row */
          td.addEventListener("click", function (e) {
            if (td.classList.contains("lc-dg-typing")) return;
            var r = td.getBoundingClientRect();
            if (e.clientX < r.right - 26) return;
            e.stopImmediatePropagation();
            verbsMenu(td, e);
          }, true);
        });
        /* ➕ New: the class itself, or — when the page declares subclasses —
           a pick of the class and each one; the new row gets selected
           (Michel, 2026-10-16) */
        var nb = el.querySelector(".lc-dg-new");
        var make = function (kind) {
          pendingNew = {};
          (window.lcDatasets[bindId] || []).forEach(function (r) { pendingNew[String(r.obj)] = 1; });
          setTimeout(function () { pendingNew = null; }, 4000);
          py("_lc_new(" + JSON.stringify(bindId) + (kind && kind !== bindId ? "," + JSON.stringify(kind) : "") + ")");
        };
        if (nb) nb.addEventListener("click", function (e) {
          e.stopPropagation();
          var subs = model.subs || [];
          var open = document.querySelector(".lc-dg-menu");
          closeMenu();
          if (!subs.length) { make(bindId); return; }
          if (open && open._lcFor === nb) return;
          var menu = document.createElement("div");
          menu.className = "lc-dg-menu lc-dg-kinds";
          menu._lcFor = nb;
          menu.innerHTML = [bindId].concat(subs).map(function (k) {
            return "<button type='button' class='lc-dg-verb' data-kind='" + esc(k) + "'><span>" + esc(k) + "</span></button>";
          }).join("");
          var r = nb.getBoundingClientRect();
          menu.style.left = (Math.max(4, Math.min(r.left, window.innerWidth - 200)) + window.scrollX) + "px";
          menu.style.top = (r.bottom + window.scrollY) + "px";
          document.body.appendChild(menu);
          menu.querySelectorAll("button[data-kind]").forEach(function (b) {
            b.addEventListener("click", function (ev) { ev.stopPropagation(); closeMenu(); make(b.getAttribute("data-kind")); });
          });
          setTimeout(function () { document.addEventListener("click", closeMenu, { once: true }); }, 0);
        });
      }
      /* COLUMNS RESIZE (Michel, 2026-10-16): drag the right edge of a header */
      el.querySelectorAll("th[data-col] .lc-dg-grip").forEach(function (g) {
        g.addEventListener("click", function (e) { e.stopPropagation(); });
        g.addEventListener("pointerdown", function (e) {
          e.preventDefault(); e.stopPropagation();
          var th = g.parentNode, c = th.getAttribute("data-col"), x0 = e.clientX, w0 = th.getBoundingClientRect().width;
          try { g.setPointerCapture(e.pointerId); } catch (x) {}
          var move = function (ev) {
            var w = Math.max(40, Math.round(w0 + ev.clientX - x0));
            colW[c] = w; th.style.width = w + "px"; th.style.minWidth = w + "px";
          };
          var up = function () { g.removeEventListener("pointermove", move); g.removeEventListener("pointerup", up); g.removeEventListener("pointercancel", up); };
          g.addEventListener("pointermove", move);
          g.addEventListener("pointerup", up);
          g.addEventListener("pointercancel", up);
        });
      });
      el.querySelectorAll("th[data-col]").forEach(function (th) {
        th.addEventListener("click", function () {
          var col = th.getAttribute("data-col");
          sortAsc = sortCol === col ? !sortAsc : true;
          sortCol = col; page = 0; render(window.lcDatasets[bindId] || data);
        });
      });
      el.querySelectorAll("[data-pg]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          /* A NEW PAGE SELECTS ITS FIRST ROW, AND SAYS SO (Michel, 2026-10-10:
             "when the grid goes to the next page and the first line gets
             selected, any detail form should follow"): the selection is
             dropped and the first-row rule below picks and publishes again. */
          page = +btn.getAttribute("data-pg");
          selKey = null; publishedFirst = false;
          render(window.lcDatasets[bindId] || data);
        });
      });
      if (urlCol) {
        el.querySelectorAll("tr[data-url]").forEach(function (tr) {
          var u = tr.getAttribute("data-url");
          if (u) tr.addEventListener("click", function () { window.open(u, "_blank", "noopener"); });
        });
      } else {
        /* every bound grid: clicking a row selects it (visual highlight). If the
           grid has an id it also publishes, so bound-to charts and bound forms
           can hang off it (dataset → grid → detail). */
        var trs = el.querySelectorAll("tbody tr");
        function keyOf(r) { return r && r.obj != null ? "o:" + r.obj : null; }
        trs.forEach(function (tr, i) {
          tr.addEventListener("click", function () {
            trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            tr.classList.add("lc-dg-selected");
            selKey = keyOf(slice[i]) || "i:" + i;
            if (lcId) window.lcMasterDetail.publish(lcId, slice[i] || null);
          });
        });
        /* THE GUIDE'S HANDS. A grid bound to a dataset is drawn by this
           light table, not by AG — so the select verb, which only knew the
           AG api, moved nothing here: on 410 module_01 Doc said "there is
           our winner: one row" over a table where nothing was ever picked
           (Michel, 2026-08-30, reading the quiz that claimed otherwise).
           Selection belongs to whoever draws the rows, so this table hands
           the verb its own door instead of letting anyone guess from
           outside. Same effect as a finger, minus a link row's navigation. */
        el._lcSelectRow = function (text) {
          var t = String(text == null ? "" : text).toLowerCase();
          for (var i = 0; i < trs.length; i++) {
            if (trs[i].textContent.toLowerCase().indexOf(t) < 0) continue;
            trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            trs[i].classList.add("lc-dg-selected");
            selKey = keyOf(slice[i]) || "i:" + i;
            if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, slice[i] || null);
            try { trs[i].scrollIntoView({ block: "nearest" }); } catch (e) {}
            return trs[i];
          }
          return null;
        };
        /* A BUTTON'S HANDS (Michel, 2026-10-09, Module 05: "currentline.met
           = today's weekday, and select the next line"). current() is the
           selected row; set() writes one field into the DATASET this table
           shows — through a query, to the base row with the same values —
           and republishes it, so the query re-runs, this table repaints and
           every cell recounts, all in the same tick; next() selects the row
           after the one just written, or the row that slid into its place
           when the write took it out of the answer. */
        function curIndex() {
          if (!selKey) return 0;
          if (selKey.indexOf("i:") === 0) return parseInt(selKey.slice(2), 10) || 0;
          for (var i = 0; i < slice.length; i++) if (keyOf(slice[i]) === selKey) return i;
          return 0;
        }
        function sameRow(a, b) {
          if (!a || !b) return false;
          for (var k in a) if (Object.prototype.hasOwnProperty.call(b, k) && String(b[k]) !== String(a[k])) return false;
          return true;
        }
        function pick(i) {
          trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
          if (trs[i]) trs[i].classList.add("lc-dg-selected");
          selKey = keyOf(slice[i]) || "i:" + i;
          if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, slice[i] || null);
          return slice[i] || null;
        }
        el._lcRow = {
          current: function () { return slice[curIndex()] || null; },
          set: function (field, value) {
            var cur = slice[curIndex()];
            if (!cur) return false;
            var baseId = bindId, target = cur;
            var q = document.querySelector(".lc-query[data-lc-id='" + bindId + "']");
            if (q) {
              baseId = (q.getAttribute("data-bind") || "").split(",")[0].trim();
              target = null;
              (window.lcDatasets[baseId] || []).forEach(function (b) { if (!target && sameRow(cur, b)) target = b; });
            }
            if (!target || !window.lcDatasets[baseId]) return false;
            touched = {};
            for (var k in cur) touched[k] = cur[k];
            touched[field] = value;
            target[field] = value;
            window.lcSetDataset(baseId, window.lcDatasets[baseId]);
            return true;
          },
          next: function () {
            var k = curIndex();
            if (touched) {
              var j = -1;
              for (var i = 0; i < slice.length && j < 0; i++) if (sameRow(touched, slice[i])) j = i;
              k = j >= 0 ? j + 1 : k;
              touched = null;
            } else k = k + 1;
            if (k >= slice.length) return null;
            return pick(k);
          }
        };
        /* ➕ New just made one: it is the row nobody had before — select it,
           show it, and the bound card follows */
        if (pendingNew) {
          for (var ni = 0; ni < slice.length; ni++) {
            if (slice[ni].obj != null && !pendingNew[String(slice[ni].obj)]) {
              pendingNew = null;
              selKey = keyOf(slice[ni]);
              lastPubJson = JSON.stringify(slice[ni]);
              publishedFirst = true;
              trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
              if (trs[ni]) { trs[ni].classList.add("lc-dg-selected"); try { trs[ni].scrollIntoView({ block: "nearest" }); } catch (e) {} }
              if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, slice[ni]);
              typeNew = { key: selKey, until: Date.now() + 1500 };
              break;
            }
          }
        }
        /* ➕ New leaves the caret in the new row's first cell, ready to type
           (Michel, 2026-10-16) — again after the repaints that follow it */
        if (typeNew && Date.now() < typeNew.until) {
          for (var ti = 0; ti < slice.length; ti++) {
            if (keyOf(slice[ti]) !== typeNew.key || !trs[ti]) continue;
            var first = trs[ti].querySelector("td.lc-dg-typed");
            if (first && !first.isContentEditable) first.dispatchEvent(new MouseEvent("dblclick", { bubbles: true }));
            break;
          }
        } else typeNew = null;
        /* the selection survives a republish: a model's verb repaints the
           whole table, and the row you were on must stay lit (Michel,
           2026-08-22: "the datagrid does not show the selected row") */
        if (selKey) {
          var stillThere = false;
          slice.forEach(function (r, i) {
            if ((keyOf(r) || "i:" + i) === selKey && trs[i]) {
              stillThere = true;
              trs[i].classList.add("lc-dg-selected");
              /* a verb moved the object and the table repainted: the bound
                 form must show the row as it is now, not as it was clicked.
                 Only when the row CHANGED — a follower that republishes the
                 class on every selection (classroom 4's inspector) would
                 otherwise chase this repaint forever (2026-10-16). */
              if (model && lcId && window.lcMasterDetail) {
                var pj = JSON.stringify(r);
                if (pj !== lastPubJson) { lastPubJson = pj; window.lcMasterDetail.publish(lcId, r); }
              }
            }
          });
          /* the selected row is gone (deleted): the first row takes the
             selection and the bound card follows, never a ghost */
          if (!stillThere) { selKey = null; publishedFirst = false; lastPubJson = null; }
        }
        /* a master with data selects its first row at once, like the AG
           road — a bound form should never sit empty waiting for a click */
        if (!publishedFirst && slice.length) {
          publishedFirst = true;
          if (!selKey) {
            selKey = keyOf(slice[0]) || "i:0";
            if (trs[0]) trs[0].classList.add("lc-dg-selected");
          }
          var firstRow = slice[curIndex()] || slice[0];   /* the lit row, which is not always the first */
          lastPubJson = JSON.stringify(firstRow);
          if (lcId && window.lcMasterDetail) window.lcMasterDetail.publish(lcId, firstRow);
        }
        /* never a grid with rows and nothing lit (Michel, 2026-10-16: "a
           line should always be selected, after a refresh, on opening") */
        if (slice.length && !el.querySelector("tbody tr.lc-dg-selected") && trs[curIndex()])
          trs[curIndex()].classList.add("lc-dg-selected");
      }
    }

    /* repo-file source: fetch once and render (no dataset listener) */
    if (fileRef) {
      bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
      var useCdn = window.lcUseCdn ? window.lcUseCdn() : false;
      var srcs = window.lcFileSrc(fileRef);
      fetch(useCdn ? srcs.cdn : srcs.raw)
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + fileRef); return r.text(); })
        .then(function (text) { return window.lcParseDataText(text, fileFmt); })
        .then(function (data) { render(Array.isArray(data) ? data : [data]); })
        .catch(function (e) { bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em'>⚠ " + e.message + "</p>"; });
      return;
    }

    /* register as persistent listener so auto-refresh re-renders */
    window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || [];
    render._lcEl = el;
    window.lcDatasetListeners[bindId].push(render);

    if (window.lcDatasets[bindId]) render(window.lcDatasets[bindId]);
    else {
      bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
      /* a source that is merely slow arrives inside the grace; one that will
         never arrive — a name that matches nothing, a query still waiting
         for ITS source — stops pretending to load and says what the author
         wrote for the case. Same knob as the datagrid and the chart. A late
         arrival still renders straight over this through the listener. */
      var grace = window.lcDatagridBindGrace;
      if (grace == null) grace = 4000;
      setTimeout(function () {
        if (window.lcDatasets[bindId] === undefined)
          bodyEl.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>"
            + (emptyMsg || "Nothing arrives here yet.") + "</p>";
      }, grace);
    }
  }

  /* NOTE: .button upgrade (incl. optional Python on_click handler) lives in
     pyrun.md's upgradeButton — it owns p.button. Keeping the .lc-button CSS
     above; no upgrader here. */

  /* ── boot ─────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry.
     Datasets register before grids so data is available when grids read
     it; the .chart variants live in chart.md. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".dataset", upgradeDataset);
    window.lcRegisterUpgrader(".datagrid", upgradeDatagridBound);
  }

})();
</script>
