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
.lc-dg-pages { display: flex; align-items: center; gap: 0.5em; margin-top: 0.5em; font-size: 0.82em; color: #6b7280; }
.lc-dg-pages button { background: none; border: 1px solid #d1d5db; border-radius: 4px; padding: 0.15em 0.55em; cursor: pointer; color: #374151; }
.lc-dg-pages button:hover { background: #f3f4f6; }
.lc-dg-table tbody tr { cursor: pointer; }
.lc-dg-table tr.lc-dg-selected td { background: #e8f0fe !important; }

/* ── button ─────────────────────────────────────────── */
.lc-button { display: inline-block; background: #0066cc; color: #fff; border: none; border-radius: 6px; padding: 0.4em 1.1em; font-size: 0.88em; font-weight: 500; cursor: pointer; margin: 0.5em 0; }
.lc-button:hover { background: #0052a3; }
.lc-button[data-color="muted"]   { background: #9ca3af; }
.lc-button[data-color="danger"]  { background: #ef4444; }
.lc-button[data-color="success"] { background: #22c55e; }
</style>

<script>
(function () {

  window.lcDatasets = window.lcDatasets || {};
  window.lcDatasetListeners = window.lcDatasetListeners || {};

  /* ── async dataset registration ─────────────────── */
  if (!window.lcSetDataset) {
    window.lcSetDataset = function (id, data) {
      window.lcDatasets[id] = data;
      (window.lcDatasetListeners[id] || []).forEach(function (fn) { try { fn(data); } catch (e) {} });
    };
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
            .then(function (text) { if (text !== null) setFromText(text, fmt, el, id); })
            .catch(function (e) { if (!window.lcDatasets[id]) window.lcSetDataset(id, [{ "⚠️": e.message }]); });
        };
        pull();
        /* refresh="30" → live mode: re-pull every N seconds. Republishing to
           the bus repaints every bound grid/stat/chart with no page reload —
           the generic auto-refresh, not a dashboard special-case. */
        var every = parseInt(el.getAttribute("refresh") || "0", 10);
        if (every > 0) setInterval(pull, Math.max(10, every) * 1000);
        return;
      }
    }

    /* inline code block variant */
    var code = el.querySelector("code") || el;
    var seed = code.textContent.trim();
    var fmt = (el.getAttribute("format") || "").toLowerCase();

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
    var lcId = el.getAttribute("id") || "";
    var masterId = el.getAttribute("master") || el.getAttribute("detail-of") || "";
    var filterExpr = el.getAttribute("filter") || "";
    var wrap = document.createElement("div");
    wrap.className = "lc-datagrid";
    wrap.setAttribute("data-bind", bindId);
    if (lcId) wrap.setAttribute("data-lc-id", lcId);
    el.parentNode.replaceChild(wrap, el);
    el = wrap;

    var sortCol = null, sortAsc = true, page = 0;

    /* grid-to-grid master/detail, the light-table half: the AG road had
       master= + filter="local=masterKey" and this road silently ignored
       both, so on a runner page the detail grid showed everything and a
       click upstream changed nothing (Michel, 2026-08-21). Same contract,
       same attributes — one selection bus for both roads. */
    var masterRow = null, lastData = null, publishedFirst = false;
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
      if (data && filterKeys && masterRow) {
        data = data.filter(function (r) {
          return r[filterKeys.local] === masterRow[filterKeys.master];
        });
      }
      if (!data || !data.length) {
        el.innerHTML = emptyMsg
          ? "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>" + emptyMsg + "</p>"
          : "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em'>⚠ No data: <code>" + bindId + "</code></p>";
        return;
      }
      var allCols = Object.keys(data[0]);
      var urlCol  = allCols.indexOf("url") >= 0 ? "url" : null;
      var cols    = allCols.filter(function (c) { return c !== "url"; });

      var sorted = data.slice();
      if (sortCol !== null) {
        sorted.sort(function (a, b) {
          var va = a[sortCol], vb = b[sortCol];
          var diff = va > vb ? 1 : va < vb ? -1 : 0;
          return sortAsc ? diff : -diff;
        });
      }
      var total = sorted.length, pp = perPage || total;
      var pages = Math.ceil(total / pp);
      page = Math.min(page, Math.max(0, pages - 1));
      var slice = sorted.slice(page * pp, (page + 1) * pp);

      var html = "<table class='lc-dg-table'><thead><tr>"
        + cols.map(function (c) {
            var arrow = sortCol === c ? (sortAsc ? " ↑" : " ↓") : "";
            var hint = hints[c] ? " title='" + hints[c].replace(/'/g, "&#39;") + "' class='lc-th-hint'" : "";
            var label = window.lcPrettifyKey ? window.lcPrettifyKey(c) : c;
            return "<th data-col='" + c + "'" + hint + ">" + label + arrow + "</th>";
          }).join("") + "</tr></thead><tbody>"
        + slice.map(function (row) {
            var urlVal = urlCol ? (row[urlCol] || "") : "";
            var trAttrs = urlVal ? " data-url='" + urlVal.replace(/'/g, "&#39;") + "' style='cursor:pointer'" : "";
            return "<tr" + trAttrs + ">"
              + cols.map(function (c) {
                  var v = row[c] !== undefined ? row[c] : "";
                  if (!editable) return "<td>" + v + "</td>";
                  /* the row is found again by its position in the CURRENT
                     sort, so an edit after sorting still lands on the row
                     the reader is looking at */
                  return "<td contenteditable='true' class='lc-dg-edit'" +
                         " data-col='" + c + "' data-row='" + sorted.indexOf(row) + "'" +
                         " inputmode='" + (typeof row[c] === "number" ? "decimal" : "text") +
                         "'>" + v + "</td>";
                }).join("") + "</tr>";
          }).join("") + "</tbody></table>";

      if (pages > 1) {
        html += "<div class='lc-dg-pages'>";
        if (page > 0)         html += "<button data-pg='" + (page - 1) + "'>←</button>";
        html += "<span>Page " + (page + 1) + " / " + pages + "</span>";
        if (page < pages - 1) html += "<button data-pg='" + (page + 1) + "'>→</button>";
        html += "</div>";
      }

      el.innerHTML = html;
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
      el.querySelectorAll("th[data-col]").forEach(function (th) {
        th.addEventListener("click", function () {
          var col = th.getAttribute("data-col");
          sortAsc = sortCol === col ? !sortAsc : true;
          sortCol = col; page = 0; render(window.lcDatasets[bindId] || data);
        });
      });
      el.querySelectorAll("[data-pg]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          page = +btn.getAttribute("data-pg"); render(window.lcDatasets[bindId] || data);
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
        trs.forEach(function (tr, i) {
          tr.addEventListener("click", function () {
            trs.forEach(function (x) { x.classList.remove("lc-dg-selected"); });
            tr.classList.add("lc-dg-selected");
            if (lcId) window.lcMasterDetail.publish(lcId, slice[i] || null);
          });
        });
        /* a master with data selects its first row at once, like the AG
           road — a bound form should never sit empty waiting for a click */
        if (lcId && !publishedFirst && slice.length && window.lcMasterDetail) {
          publishedFirst = true;
          if (trs[0]) trs[0].classList.add("lc-dg-selected");
          window.lcMasterDetail.publish(lcId, slice[0]);
        }
      }
    }

    /* repo-file source: fetch once and render (no dataset listener) */
    if (fileRef) {
      el.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
      var useCdn = window.lcUseCdn ? window.lcUseCdn() : false;
      var srcs = window.lcFileSrc(fileRef);
      fetch(useCdn ? srcs.cdn : srcs.raw)
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status + " fetching " + fileRef); return r.text(); })
        .then(function (text) { return window.lcParseDataText(text, fileFmt); })
        .then(function (data) { render(Array.isArray(data) ? data : [data]); })
        .catch(function (e) { el.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em'>⚠ " + e.message + "</p>"; });
      return;
    }

    /* register as persistent listener so auto-refresh re-renders */
    window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || [];
    window.lcDatasetListeners[bindId].push(render);

    if (window.lcDatasets[bindId]) render(window.lcDatasets[bindId]);
    else el.innerHTML = "<p style='color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
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
