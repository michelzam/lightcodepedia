{%- comment -%}
Widgets — small standalone content widgets, activated from md + IAL:

  ul + {: .carousel delay="4000" }      rotating item display
  code block + {: .scrollable height="300" }   fixed-height scroll pane
  ul + {: .dropdown label="Menu" }      dropdown of links
  ul/p of links + {: .menu }            horizontal icon nav
  link + {: .video } / {: .embed-page } / {: .embed }   media embeds
  code block + {: .code title="…" }   titled code viewer

Named widgets.md because carousel.md / scrollable.md / embed.md are
existing Liquid build-time includes (a separate mechanism, still in use
by content pages) — runtime upgraders must not shadow them.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* a bench slot: a thin frame is the only hint. The ⚙️ shows what can be
   changed and the lesson's own text does the guiding — a treasure hunt
   reads better than a label (Michel 2026-08-04). */
/* A: a tinted sheet — the learner's file is a different piece of paper laid
   on the lesson. B: a left accent bar carrying the save state, the same
   idiom feature and pitch cards already use. C: a header stripe naming the
   owner, with their avatar. Amber while it is still the lesson's copy,
   green once it is theirs. */
.lc-bench-slot { border: 1px solid #e6ecf5; border-left: 3px solid #f0b429;
                 border-radius: 8px; background: #fffdf7; margin: 1.1em 0;
                 padding: 0 0.9em 0.6em; overflow: hidden; }
.lc-bench-slot[data-state="draft"] { border-left-color: #3b82f6; background: #fbfdff; }
.lc-bench-slot[data-state="done"]  { border-left-color: #22c55e; background: #f8fffb; }
.lc-bench-lite { padding: 0 0 0.6em; }
.lc-bench-lite > .lc-bench-head { margin: 0 0 0.5em; }
.lc-bench-lite > :not(.lc-bench-head) { margin-left: 0.9em; margin-right: 0.9em; }
.lc-bench-head { position: relative; display: flex; align-items: center; gap: 0.5em;
                 margin: 0 -0.9em 0.7em; padding: 0.35em 0.9em;
                 background: rgba(255,255,255,0.72);
                 border-bottom: 1px solid #eef2f7; font-size: 0.78em; color: #6b7280; }
.lc-bench-avatar { width: 20px; height: 20px; border-radius: 50%; flex: none;
                   background: #e5e7eb; object-fit: cover; }
.lc-bench-avatar-none { display: inline-flex; align-items: center; justify-content: center;
                        background: transparent; font-size: 15px; }
.lc-bench-who { font-weight: 600; color: #374151; flex: none; }
.lc-bench-path { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
                 overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; }
.lc-bench-state { margin-left: auto; flex: none; padding: 0.05em 0.6em;
                  border-radius: 99px; font-weight: 500; }
.lc-bench-yours { background: #dcfce7; color: #15803d; }
.lc-bench-draft { background: #dbeafe; color: #1d4ed8; }
.lc-bench-seed  { background: #fef3c7; color: #92400e; }
.lc-bench-more { border: none; background: none; cursor: pointer; color: #6b7280;
                 font-size: 1.15em; line-height: 1; padding: 0 0.15em; flex: none; }
.lc-bench-more:hover { color: #111827; }
.lc-bench-save { flex: none; border: 1px solid #0969da; background: #0969da; color: #fff;
                 border-radius: 6px; cursor: pointer; font: inherit; font-size: 0.95em;
                 padding: 0.15em 0.7em; margin-left: 0.4em; }
.lc-bench-save:hover { background: #0b62c4; }
/* top:100% pins the sheet under the head — a plain margin let its first row
   ride up behind the header, where the one action that matters was clipped */
.lc-bench-menu { position: absolute; right: 0.6em; top: 100%; margin-top: 0.25em; z-index: 40;
                 background: #fff; border: 1px solid #e5e7eb; border-radius: 8px;
                 box-shadow: 0 6px 20px rgba(0,0,0,0.13); padding: 0.25em; min-width: 15em; }
.lc-bench-menu button { display: block; width: 100%; text-align: left; border: none;
                        background: none; padding: 0.45em 0.7em; border-radius: 6px;
                        font: inherit; font-size: 0.95em; color: #374151; cursor: pointer; }
.lc-bench-menu button:hover:not(:disabled) { background: #f3f4f6; }
.lc-bench-menu button:disabled { color: #b6bcc5; cursor: default; }
/* a phone has no room for the path — the owner and the state are what matter */
@media (max-width: 560px) { .lc-bench-path { display: none; } }

/* A SNIPPET IS ON GRAY (Michel, 2026-10-10: "dark mode for code", then "a
   gray not too light", then "too dark!", then "a way lighter gray"): a pale
   gray, read-only, a copy
   button in its title bar; markdown painted by the pad's own painter, CSV a
   piano by column, other languages in Rouge's classes. The pad's tokens are
   pastel for its dark pane; on the gray the same roles take darker inks —
   every one at least 6:1. */
.lc-code { border: 1px solid #dde1e8; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #f2f4f7; color: #262a36; }
.lc-code-title { background: #e7eaf0; padding: 0.4em 0.6em 0.4em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #262a36; border-bottom: 1px solid #dde1e8; display: flex; align-items: center; gap: 0.5em; }
.lc-code-title .lc-code-icon { font-size: 1.1em; }
.lc-code-title .lc-code-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #454b5c; letter-spacing: 0.05em; }
.lc-code-copy { font: inherit; font-size: 0.85em; padding: 0.15em 0.6em; border-radius: 5px; border: 1px solid #cfd4dd; background: #ffffff; color: #262a36; cursor: pointer; }
.lc-code-copy:hover { background: #f6f7f9; }
.lc-code > .highlighter-rouge, .lc-code > pre { margin: 0 !important; border-radius: 0 !important; background: transparent !important; border: none !important; }
.lc-code .highlight { background: transparent !important; }
.lc-code .highlight pre, .lc-code > pre { padding: 0.9em 1em !important; margin: 0 !important; overflow-x: auto; font-size: 0.85em; line-height: 1.5; background: transparent !important; color: #262a36; }
.lc-code pre code { background: transparent !important; color: inherit; white-space: pre; }
.lc-code > pre, .lc-code .highlight pre { max-height: 32em; overflow: auto; }
.lc-code .lc-code-md code { white-space: pre-wrap; overflow-wrap: break-word; }
.lc-code .lc-code-md .ln { display: block; min-height: 1.5em; }
.lc-code .highlight .c, .lc-code .highlight .c1, .lc-code .highlight .cm, .lc-code .highlight .cp, .lc-code .highlight .ch { color: #545a6b; font-style: italic; }
.lc-code .highlight .k, .lc-code .highlight .kd, .lc-code .highlight .kn, .lc-code .highlight .kc, .lc-code .highlight .kr, .lc-code .highlight .ow { color: #6b21a8; }
.lc-code .highlight .s, .lc-code .highlight .s1, .lc-code .highlight .s2, .lc-code .highlight .sa, .lc-code .highlight .sd, .lc-code .highlight .si, .lc-code .highlight .dl { color: #166534; }
.lc-code .highlight .m, .lc-code .highlight .mi, .lc-code .highlight .mf, .lc-code .highlight .kt, .lc-code .highlight .l { color: #9a3412; }
.lc-code .highlight .nf, .lc-code .highlight .nc, .lc-code .highlight .nb, .lc-code .highlight .bp { color: #1d4ed8; }
.lc-code .highlight .na, .lc-code .highlight .nt, .lc-code .highlight .py, .lc-code .highlight .n { color: #0e6377; }
.lc-code .highlight .o, .lc-code .highlight .p, .lc-code .highlight .w { color: #3a3f4d; }
.lc-code .highlight .err { color: #b0124f; background: none; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-h { color: #7c2d12; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-fence, .lc-code .md-comma { color: #545a6b; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-code { color: #262a36; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-ial { color: #454b5c; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-cls { color: #1d4ed8; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-id { color: #b0124f; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-key { color: #166534; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-val { color: #9a3412; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-link { color: #0e6377; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-em { color: #6b21a8; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-quote { color: #0e6377; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-li { color: #b0124f; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-c0 { color: #7c3a00; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-c1 { color: #1d4ed8; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-kw { color: #6b21a8; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-str { color: #166534; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-num { color: #9a3412; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-com { color: #545a6b; font-style: italic; }
:is(.lc-code, .lc-feature-step-impl) .lc-md-paint .md-fn { color: #1d4ed8; }
/* the painter's tokens — the pad's source pane and the snippets alike */
.lc-md-paint .md-h { color: #f9e2af; font-weight: 600; }
.lc-md-paint .md-fence { color: #6c7086; }
.lc-md-paint .md-code { color: #a6adc8; }
/* no bar and no shade of its own: the decoration is part of its block, and in
   the pad the blue bar marks the CURRENT block, from its link or fence down to
   its decoration (Michel, 2026-10-10) */
.lc-md-paint .md-ial { color: #9399b2; }
.lc-md-paint .md-cls { color: #89b4fa; font-weight: 600; }
.lc-md-paint .md-id { color: #f38ba8; }
.lc-md-paint .md-key { color: #a6e3a1; }
.lc-md-paint .md-val { color: #fab387; }
.lc-md-paint .md-link { color: #89dceb; }
.lc-md-paint .md-em { color: #cba6f7; }
.lc-md-paint .md-quote { color: #94e2d5; }
.lc-md-paint .md-li { color: #f5c2e7; }
.lc-md-paint .md-c0 { color: #f9e2af; }
.lc-md-paint .md-c1 { color: #89dceb; }
.lc-md-paint .md-comma { color: #6c7086; }
.lc-md-paint .md-kw { color: #cba6f7; }
.lc-md-paint .md-str { color: #a6e3a1; }
.lc-md-paint .md-num { color: #fab387; }
.lc-md-paint .md-com { color: #7f849c; font-style: italic; }
.lc-md-paint .md-fn { color: #89b4fa; }

.lc-carousel { position: relative; padding: 1.2em 2em; min-height: 4em; background: #fafafa; border-left: 4px solid #0066cc; border-radius: 0 6px 6px 0; margin: 1em 0; }
.lc-carousel-item { display: none; font-style: italic; color: #444; line-height: 1.5; }
.lc-carousel-item.active { display: block; animation: lc-fade 0.4s ease; }
@keyframes lc-fade { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: none; } }
.lc-carousel-dots { text-align: center; margin-top: 0.8em; }
.lc-carousel-dots span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ccc; margin: 0 3px; cursor: pointer; transition: background 0.2s; }
.lc-carousel-dots span.active { background: #0066cc; }

.lc-dropdown { position: relative; display: inline-block; margin: 0.3em 0; }
.lc-dd-toggle { background: #0066cc; color: white; border: none; padding: 0.5em 1em; border-radius: 4px; cursor: pointer; font-size: 0.95em; }
.lc-dd-toggle:hover { background: #0052a3; }
.lc-dd-menu { display: none; position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; border-radius: 4px; min-width: 180px; box-shadow: 0 2px 10px rgba(0,0,0,0.12); z-index: 500; margin-top: 4px; }
.lc-dd-menu.open { display: block; }
.lc-dd-menu a { display: block; padding: 0.6em 1em; color: #333; text-decoration: none; }
.lc-dd-menu a:hover { background: #f5f5f5; color: #0066cc; }
.lc-scrollable { overflow-y: auto; padding: 1em 1.4em; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; margin: 1em 0; }

.lc-menu { display: flex; flex-wrap: wrap; align-items: center; gap: 0.3em 1.5em; padding: 0.5em 0; margin: 0.5em 0 1.2em; border-bottom: 1px solid #eee; }
.lc-menu a { display: inline-flex; align-items: center; gap: 0.4em; text-decoration: none; color: #333; font-weight: 500; font-size: 0.96em; padding: 0.2em 0; }
.lc-menu a:hover { color: #0066cc; }
.lc-menu .lc-menu-ic { font-size: 1.1em; line-height: 1; }

.lc-embed { margin: 0.5em 0; }
/* image embeds with align="left|right": the text that follows wraps around
   the picture, so the amount of text decides the shape; floats drop on
   small screens where wrapping has no room to breathe */
.lc-embed-circle img { border-radius: 50%; aspect-ratio: 1 / 1; object-fit: cover;
                       object-position: center top; }
.lc-embed-left  { float: left;  margin: 0.2em 1.2em 0.8em 0; max-width: 60%; }
.lc-embed-right { float: right; margin: 0.2em 0 0.8em 1.2em; max-width: 60%; }
@media (max-width: 700px) {
  .lc-embed-left, .lc-embed-right { float: none; margin: 0.5em 0; max-width: 100%; }
}
/* effect="ambient": the still breathes — a slow Ken-Burns zoom with a soft
   light pulse, locked camera, no assets. Clipped by the container so the
   zoom never spills into the page. Honors reduced-motion preferences. */
.lc-embed-ambient { overflow: hidden; display: inline-block; max-width: 100%; border-radius: 8px; }
.lc-embed-ambient img { display: block; transform-origin: center;
  animation: lc-ambient 9s ease-in-out infinite alternate; }
@keyframes lc-ambient {
  from { transform: scale(1);     filter: brightness(1); }
  to   { transform: scale(1.045); filter: brightness(1.07) saturate(1.08); }
}
@media (prefers-reduced-motion: reduce) { .lc-embed-ambient img { animation: none; } }
</style>

<script>
/* IAL on its own paragraph so block-IAL applies — the client-side twin of
   kramdown's rule, OUTSIDE fences only. Inside a fence the text is verbatim:
   a pad's seed is a fence, and normalising it showed learners a blank line
   above every decoration the lesson had glued (Michel, 2026-10-09). A fence
   closes on the same character, at least as long as the one that opened it,
   so a `````markdown seed may hold ``` fences of its own. */
window.lcNormIAL = window.lcNormIAL || function (md) {
  var lines = String(md).split("\n"), out = [], fence = null;
  for (var i = 0; i < lines.length; i++) {
    var l = lines[i], m = /^ {0,3}(`{3,}|~{3,})/.exec(l);
    if (fence) {
      if (m && m[1].charAt(0) === fence.charAt(0) && m[1].length >= fence.length &&
          /^ {0,3}[`~]+\s*$/.test(l)) fence = null;
    } else if (m) {
      fence = m[1];
    } else if (/^\{:/.test(l) && out.length && out[out.length - 1] !== "") {
      out.push("");
    }
    out.push(l);
  }
  return out.join("\n");
};
/* component class (lower case, no _ or -) → its icon, from the one component
   model the x-ray and the editor read: 🛢️ dataset, ▦ datagrid, ☷ form … */
window.lcComponentIcons = window.lcComponentIcons || function () {
  if (window._lcCompIconsP) return window._lcCompIconsP;
  window._lcCompIconsP = fetch("{{ "/assets/component-model.json" | relative_url }}")
    .then(function (r) { return r.json(); })
    .then(function (d) {
      var m = (d && d.model) || {}, out = {};
      Object.keys(m).forEach(function (k) { if (m[k].icon) out[k.toLowerCase()] = m[k].icon; });
      return out;
    })
    .catch(function () { return {}; });
  return window._lcCompIconsP;
};
/* THE MARKDOWN PAINTER — one line at a time, shared by the pad's source pane
   and the read-only .code snippets, so a lesson's snippet and the pad beside
   it wear the same colours (Michel, 2026-10-08 for the pad, 2026-10-10 for
   the snippets). fence is null outside a fence, else the fence's info string
   ("csv", "sql", "" …). A CSV fence — or an untagged one holding commas, a
   dataset's rows — colours its columns in turns, a piano by column. */
(function () {
  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return c === "&" ? "&amp;" : c === "<" ? "&lt;" : "&gt;"; }); }
  var FENCE = /^\s*(`{3,}|~{3,})/;
  function ial(s) {
    return esc(s).replace(/(\.[A-Za-z_][\w-]*)|(#[A-Za-z_][\w-]*)|([A-Za-z_][\w-]*)=(&quot;[^&]*?&quot;|\S+)/g,
      function (all, cls, id, key, val) {
        if (cls) return "<span class='md-cls'>" + cls + "</span>";
        if (id) return "<span class='md-id'>" + id + "</span>";
        return "<span class='md-key'>" + key + "</span>=<span class='md-val'>" + val + "</span>";
      });
  }
  function inline(raw) {
    var h = esc(raw);
    h = h.replace(/^(\s*)([-*+]|\d+\.)(\s)/, "$1<span class='md-li'>$2</span>$3");
    h = h.replace(/\[([^\]]*)\]\(([^)]*)\)/g, "<span class='md-link'>[$1]($2)</span>");
    h = h.replace(/(\*\*[^*\n]+\*\*|\*[^*\n]+\*|_[^_\n]+_|`[^`\n]+`)/g, "<span class='md-em'>$1</span>");
    return h;
  }
  /* one CSV line: each cell in its column's colour, two colours in turn;
     a quoted cell keeps its commas */
  window.lcPaintCsvLine = function (raw) {
    if (!raw) return " ";
    var cells = [], cur = "", q = false;
    for (var i = 0; i < raw.length; i++) {
      var c = raw.charAt(i);
      if (c === '"') q = !q;
      if (c === "," && !q) { cells.push(cur); cur = ""; } else cur += c;
    }
    cells.push(cur);
    return cells.map(function (v, k) {
      return "<span class='md-c" + (k % 2) + "'>" + esc(v) + "</span>";
    }).join("<span class='md-comma'>,</span>");
  };
  /* CODE INSIDE A FENCE (Michel, 2026-10-10: "inside the editor, the sql
     should also be in colored syntax, and so on"): one small tokenizer per
     line — keywords, strings, numbers, comments, a name called with ( —
     for python, sql, yaml, json and gherkin (whose :::python step bodies
     are python). No library, so the runner, the pad and a card paint alike. */
  var KW = {
    python: "False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield self",
    sql: "select from where group by order as count sum avg min max join left right inner outer full on and or not in is null limit offset distinct having insert into values update set delete like between case when then else end asc desc union all create table drop alter",
    json: "true false null"
  };
  var KWSET = {};
  Object.keys(KW).forEach(function (k) { KWSET[k] = {}; KW[k].split(" ").forEach(function (w) { KWSET[k][w] = 1; }); });
  var COMMENT = { python: "#", sql: "--", yaml: "#" };
  function langOf(info) {
    var l = String(info || "").trim().toLowerCase().split(/\s+/)[0];
    if (l === "py") return "python";
    if (l === "yml") return "yaml";
    if (l === "feature") return "gherkin";
    if (l === "md") return "markdown";
    return l;
  }
  function tokens(raw, lang) {
    var kw = KWSET[lang] || {}, com = COMMENT[lang] || "", out = "";
    var re = /("(?:[^"\\]|\\.)*"?|'(?:[^'\\]|\\.)*'?)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+|[^\w\s"'])/g, m;
    while ((m = re.exec(raw))) {
      if (com && !m[1] && raw.substr(m.index, com.length) === com) {
        out += "<span class='md-com'>" + esc(raw.slice(m.index)) + "</span>";
        break;
      }
      if (m[1]) out += "<span class='md-str'>" + esc(m[1]) + "</span>";
      else if (m[2]) out += "<span class='md-num'>" + m[2] + "</span>";
      else if (m[3]) {
        var w = m[3], low = lang === "sql" ? w.toLowerCase() : w;
        if (kw[low]) out += "<span class='md-kw'>" + esc(w) + "</span>";
        else if (raw.charAt(re.lastIndex) === "(") out += "<span class='md-fn'>" + esc(w) + "</span>";
        else out += esc(w);
      } else out += esc(m[4]);
    }
    return out || " ";
  }
  window.lcPaintCodeLine = function (raw, info) {
    if (!raw) return " ";
    var lang = langOf(info);
    if (lang === "csv") return window.lcPaintCsvLine(raw);
    if (lang === "yaml") {
      var c = raw.match(/^(\s*)#.*$/);
      if (c) return "<span class='md-com'>" + esc(raw) + "</span>";
      var y = raw.match(/^(\s*(?:-\s+)?)([^\s:#][^:#]*?)(:)(\s.*|)$/);
      if (y) return esc(y[1]) + "<span class='md-key'>" + esc(y[2]) + "</span>" + y[3] + tokens(y[4], "yaml");
      return tokens(raw, "yaml");
    }
    if (lang === "gherkin") {
      if (/^\s*:::/.test(raw)) return "<span class='md-fence'>" + esc(raw) + "</span>";
      var g = raw.match(/^(\s*)(Feature|Scenario Outline|Scenario|Background|Examples|Rule|Given|When|Then|And|But|As an?|I want|So that)\b(.*)$/);
      if (g) return esc(g[1]) + "<span class='md-kw'>" + esc(g[2]) + "</span>" + esc(g[3]);
      if (/^\s*#/.test(raw)) return "<span class='md-com'>" + esc(raw) + "</span>";
      /* a step body: python, read as python */
      if (/^\s{4,}\S/.test(raw) && /[=()\[\]]|\bself\b|\bassert\b|\bimport\b/.test(raw)) return tokens(raw, "python");
      return esc(raw);
    }
    if (KWSET[lang]) return tokens(raw, lang);
    return esc(raw);
  };
  window.lcPaintCodeLang = langOf;
  function isCsv(fence, raw) {
    var info = String(fence || "").trim().toLowerCase();
    return info === "csv" || (info === "" && raw.indexOf(",") >= 0);
  }
  window.lcPaintMdLine = function (raw, fence) {
    if (!raw) return " ";
    if (FENCE.test(raw)) return "<span class='md-fence'>" + esc(raw) + "</span>";
    if (fence !== null && fence !== undefined && fence !== false) {
      if (fence === true) fence = "";
      return isCsv(fence, raw) ? window.lcPaintCsvLine(raw) : "<span class='md-code'>" + window.lcPaintCodeLine(raw, fence) + "</span>";
    }
    var m = raw.match(/^(\s*)\{:(.*)\}(\s*)$/);
    if (m) return esc(m[1]) + "<span class='md-ial'>{:" + ial(m[2]) + "}</span>" + esc(m[3]);
    if (/^\s*#{1,6}\s/.test(raw)) return "<span class='md-h'>" + esc(raw) + "</span>";
    if (/^\s*>/.test(raw)) return "<span class='md-quote'>" + esc(raw) + "</span>";
    return inline(raw);
  };
  /* a whole text, fences tracked: one painted line per source line */
  window.lcPaintMd = function (text) {
    var fence = null, close = null;
    return String(text).split("\n").map(function (l) {
      var h = window.lcPaintMdLine(l, fence);
      var m = FENCE.exec(l);
      if (m) {
        if (fence === null) { fence = l.trim().slice(m[1].length).trim(); close = m[1]; }
        else if (m[1].charAt(0) === close.charAt(0) && m[1].length >= close.length) { fence = null; close = null; }
      }
      return h;
    });
  };
})();
/* THE OTHER WAY ROUND, for a learner's own text: a decoration glued to the
   line it decorates — the blank lines right above a {: … } line go, outside
   fences. Pads saved before 2026-10-09 carry the runner's old gaps, and a
   gap is not harmless: a lone decoration lands on the NEXT block (a
   datagrid's turned the query below it into a grid — Michel, Module 05). */
window.lcGlueIAL = window.lcGlueIAL || function (md) {
  var lines = String(md).split("\n"), out = [], fence = null;
  for (var i = 0; i < lines.length; i++) {
    var l = lines[i], m = /^ {0,3}(`{3,}|~{3,})/.exec(l);
    if (fence) {
      if (m && m[1].charAt(0) === fence.charAt(0) && m[1].length >= fence.length &&
          /^ {0,3}[`~]+\s*$/.test(l)) fence = null;
    } else if (m) {
      fence = m[1];
    } else if (/^\{:.*\}\s*$/.test(l)) {
      var k = out.length;
      while (k > 0 && /^\s*$/.test(out[k - 1])) k--;
      if (k > 0) out.length = k;              /* never glue to the top of the text */
    }
    out.push(l);
  }
  return out.join("\n");
};
(function () {
  if (window._lcWidgetsReady) return;
  window._lcWidgetsReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  /* shared helpers from code_chrome.md (parsed earlier — topbar include) */
  var escapeHtml = window.lcEscapeHtml;
  var loadMarked = window.lcLoadMarked;

  /* SSOT for "which {: .embed } fragments does this markdown compose from" —
     the tutor's knowledge (agent.md) and the editor's ✨ context both use it,
     so an AI asked about "the page" reads the same composition the reader
     sees. Returns repo paths. Images and external targets are skipped
     (pictures aren't prose). dir = the md file's folder for course/hub
     files; docs files ('' or docs/…) use the site convention (docs/<x>.md,
     matching how the embed widget itself fetches on built pages). */
  window.lcEmbedRefs = function (md, dir) {
    var docsMode = !dir || /^docs(\/|$)/.test(dir);
    var out = [], re = /\]\(([^)#?\s]+)\)\s*\r?\n\{:[^}]*\.embed/g, m;
    while ((m = re.exec(md)) && out.length < 12) {
      var rel = m[1];
      if (/^[a-z][a-z0-9+.-]*:/i.test(rel)) continue;                 // external
      if (/\.(png|jpe?g|gif|webp|svg|avif)$/i.test(rel)) continue;    // pictures aren't prose
      rel = rel.replace(/^\/+/, "");
      if (!/\.md$/i.test(rel)) rel += ".md";
      if (docsMode) { out.push("docs/" + rel); continue; }
      var stack = [];
      (dir + "/" + rel).split("/").forEach(function (s) {
        if (s === "..") stack.pop(); else if (s && s !== ".") stack.push(s);
      });
      out.push(stack.join("/"));
    }
    return out;
  };

  /* ── Component verbs — the page's PRESENTATION vocabulary ──────────────
     Components expose what can be DONE to them; avatar stories and demo
     replay call verbs by name instead of poking the DOM. Only presentation
     verbs live here — view state, never content, edits or scores — so the
     "tutor never acts" ruling is structural: a consequential action simply
     has no verb to call. Names stay snake_case (doctrine 2).
       open / close [title]   fold or unfold accordion sections
       present / reel / read  page modes (same engine as the pill)
       xray [seconds]         the lens; with at: also the ⚙️ on that part */
  window.lcVerbs = (function () {
    var map = {};
    return {
      /* a verb may declare WHERE it happens (targetFn → its subject element);
         the avatar refines the at: walk onto that subject — open("Why") walks
         to that section's own title, not the whole accordion */
      register: function (verb, fn, targetFn) { map[verb] = { fn: fn, target: targetFn || null }; },
      has: function (verb) { return !!map[verb]; },   /* a page's meta check asks before a tour promises */
      act: function (verb, el, arg) {
        var v = map[verb];
        if (!v) return false;
        try { return v.fn(el || null, arg) !== false; } catch (e) { return false; }
      },
      target: function (verb, el, arg) {
        var v = map[verb];
        if (!v || !v.target) return null;
        try { return v.target(el || null, arg) || null; } catch (e) { return null; }
      },
      list: function () { return Object.keys(map).sort(); }
    };
  })();
  function _lcDetails(el, arg) {
    var all = el
      ? (el.tagName === "DETAILS" ? [el] : Array.prototype.slice.call(el.querySelectorAll("details")))
      : Array.prototype.slice.call(document.querySelectorAll(".markdown-body details"));
    if (arg) {
      var t = String(arg).toLowerCase();
      all = all.filter(function (d) {
        var sm = d.querySelector("summary");
        return sm && sm.textContent.toLowerCase().indexOf(t) >= 0;
      });
    }
    return all;
  }
  function _lcDetailsSubject(el, arg) {
    var d = _lcDetails(el, arg);
    return d.length ? (d[0].querySelector("summary") || d[0]) : null;
  }
  window.lcVerbs.register("open", function (el, arg) {
    var d = _lcDetails(el, arg); d.forEach(function (x) { x.open = true; }); return d.length > 0;
  }, _lcDetailsSubject);
  window.lcVerbs.register("close", function (el, arg) {
    var d = _lcDetails(el, arg); d.forEach(function (x) { x.open = false; }); return d.length > 0;
  }, _lcDetailsSubject);
  /* select: a datagrid row by matching text — through the grid's own
     selection API, the same path a human click takes (bound forms update,
     nothing is edited). el scopes to one grid; default: the page's first. */
  function _lcGridOf(el) {
    if (el && el.closest) {
      var g = el.closest(".lc-datagrid") || (el.querySelector && el.querySelector(".lc-datagrid"));
      if (g) return g;
    }
    return document.querySelector(".lc-datagrid");
  }
  function _lcGridApi(g) {
    if (!g || !window.lcMasterDetail || !window.lcMasterDetail._apis) return null;
    var apis = window.lcMasterDetail._apis;
    var keys = [g.id, (g.id || "").replace(/^lc-datagrid-/, ""), g.getAttribute("data-lc-id")];
    for (var i = 0; i < keys.length; i++) if (keys[i] && apis[keys[i]]) return apis[keys[i]];
    return null;
  }
  /* TWO ROADS DRAW A GRID: AG (a .datagrid fence) and the light table a
     dataset-bound grid gets from dataset.md. The verb knew only the first,
     so on a course page it silently did nothing — the light table now
     offers its own door and the verb takes whichever road this grid is on. */
  function _lcLightSelect(g, arg) {
    return (g && typeof g._lcSelectRow === "function") ? g._lcSelectRow(arg) : null;
  }
  window.lcVerbs.register("select", function (el, arg) {
    var g = _lcGridOf(el), api = _lcGridApi(g);
    if (!arg) return false;
    if (!api) return !!_lcLightSelect(g, arg);
    var t = String(arg).toLowerCase(), hit = null;
    api.forEachNode(function (n) {
      if (!hit && n.data && JSON.stringify(n.data).toLowerCase().indexOf(t) >= 0) hit = n;
    });
    if (!hit) return false;
    hit.setSelected(true);
    if (api.ensureNodeVisible) { try { api.ensureNodeVisible(hit); } catch (e) {} }
    return true;
  }, function (el, arg) {
    var g = _lcGridOf(el);
    if (!g || !arg) return null;
    var t = String(arg).toLowerCase();
    var rows = g.querySelectorAll(".ag-row, tbody tr");
    for (var i = 0; i < rows.length; i++)
      if (rows[i].textContent.toLowerCase().indexOf(t) >= 0) return rows[i];
    return g;   /* row virtualised out of the DOM: stand at the grid itself */
  });
  ["present", "reel", "read"].forEach(function (m) {
    window.lcVerbs.register(m, function () {
      if (window.lcMode) { window.lcMode.set(m); return true; } return false;
    });
  });
  /* xray is a mode too, but as a verb it is a pointing gesture, not a
     toggle: a second call while the pipes are up must hold them up (a bare
     set() would flip back to read). With seconds in `with:` the page comes
     home to read on its own, so a tour can flash the wiring from the
     datasources to the grids and walk on with nothing left switched on. */
  var _lcXrayBack;
  window.lcVerbs.register("xray", function (el, arg) {
    if (!window.lcMode) return false;
    if (window.lcMode.current() !== "xray") window.lcMode.set("xray");
    if (window.lcMode.current() !== "xray") return false;   /* engine absent, or exit vetoed */
    /* the mode is a lens — it paints nothing until asked. A tour has no
       pointer to ask with, so draw the pipelines scene ourselves: the given
       subject, or the first wired component on the page. */
    if (window.lcxReveal) window.lcxReveal(el);
    /* and, on a named part, the ⚙️ on its corner — the tour has no pointer
       to hover with, so the verb shows what a hover would */
    if (el && window.lcxShowGear) window.lcxShowGear(el);
    var s = parseFloat(arg);
    clearTimeout(_lcXrayBack);
    if (s > 0) _lcXrayBack = setTimeout(function () {
      if (window.lcMode.current() === "xray") window.lcMode.set("read");
    }, Math.min(s, 120) * 1000);
    return true;
  }, function (el) {
    return (window.lcxSubject && window.lcxSubject(el || null)) || null;
  });

  function upgradeCarousel(el) {
    var lis = Array.from(el.querySelectorAll("li"));
    if (!lis.length) return;
    var delay = parseInt(el.getAttribute("delay") || "4000", 10);
    var gid = el.id || ("lc-car-" + Math.random().toString(36).slice(2, 7));
    var wrapper = document.createElement("div");
    wrapper.className = "lc-carousel";
    wrapper.id = gid;
    /* MOVE the nodes, never copy their HTML. A relative image is healed
       ASYNCHRONOUSLY (runner.md fetches it through the contents API and
       swaps in a blob), so innerHTML copied at upgrade time froze the raw
       src and the slide never appeared — three Workbench screenshots on
       410's module 04, broken while the same files rendered fine as
       embeds (Michel, 2026-09-19). Moving the live nodes keeps whatever
       lands on them later, healing and upgrades alike. */
    lis.forEach(function (li, i) {
      var item = document.createElement("div");
      item.className = "lc-carousel-item" + (i === 0 ? " active" : "");
      while (li.firstChild) item.appendChild(li.firstChild);
      wrapper.appendChild(item);
    });
    var dots = document.createElement("div");
    dots.className = "lc-carousel-dots";
    dots.innerHTML = lis.map(function(_, i){
      return '<span class="' + (i === 0 ? "active" : "") + '" data-idx="' + i + '"></span>';
    }).join("");
    wrapper.appendChild(dots);
    el.parentNode.replaceChild(wrapper, el);
    var elItems = wrapper.querySelectorAll(".lc-carousel-item");
    dots = wrapper.querySelectorAll(".lc-carousel-dots span");
    var idx = 0;
    function show(n) {
      elItems.forEach(function(x){ x.classList.remove("active"); });
      dots.forEach(function(x){ x.classList.remove("active"); });
      elItems[n].classList.add("active");
      dots[n].classList.add("active");
      idx = n;
    }
    dots.forEach(function(d){ d.addEventListener("click", function(){ show(parseInt(d.dataset.idx, 10)); }); });
    setInterval(function(){ show((idx + 1) % elItems.length); }, delay);
  }

  function upgradeScrollable(el) {
    var h = el.getAttribute("height") || "300";
    var code = el.querySelector("code");
    var content = code ? code.innerHTML : el.innerHTML;
    var wrap = document.createElement("div");
    wrap.className = "lc-scrollable";
    wrap.style.maxHeight = h + "px";
    wrap.innerHTML = "<pre style=\"margin:0;white-space:pre-wrap;\">" + content + "</pre>";
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeDropdown(el) {
    var label = el.getAttribute("label") || "Menu";
    var gid = el.id || ("lc-dd-" + Math.random().toString(36).slice(2, 7));
    var links = Array.from(el.querySelectorAll("li a")).map(function(a){
      return "<a href=\"" + a.href + "\">" + a.textContent + "</a>";
    }).join("");
    var wrap = document.createElement("div");
    wrap.className = "lc-dropdown";
    wrap.id = "lc-dd-" + gid;
    wrap.innerHTML = "<button class=\"lc-dd-toggle\">" + label + "</button><div class=\"lc-dd-menu\">" + links + "</div>";
    var btn = wrap.querySelector(".lc-dd-toggle");
    var menu = wrap.querySelector(".lc-dd-menu");
    btn.addEventListener("click", function(e){ e.stopPropagation(); menu.classList.toggle("open"); });
    document.addEventListener("click", function(){ menu.classList.remove("open"); }, { passive: true });
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeMenu(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var links = el.querySelectorAll("a");
    if (!links.length) return;
    var nav = document.createElement("nav");
    nav.className = "lc-menu";
    Array.prototype.forEach.call(links, function(a) {
      var t = (a.textContent || "").trim();
      var sp = t.indexOf(" ");
      var icon = "", label = t;
      if (sp > 0) { icon = t.slice(0, sp); label = t.slice(sp + 1); }
      var na = document.createElement("a");
      na.href = a.getAttribute("href") || "#";
      if (a.getAttribute("target")) na.target = a.getAttribute("target");
      na.innerHTML = (icon ? '<span class="lc-menu-ic">' + escapeHtml(icon) + '</span>' : '')
        + '<span class="lc-menu-lb">' + escapeHtml(label) + '</span>';
      nav.appendChild(na);
    });
    el.parentNode.replaceChild(nav, el);
  }

  function _iframeEl(src, h, cls) {
    var f = document.createElement("iframe");
    if (cls) f.className = cls;
    f.src = src; f.width = "100%"; f.height = h || "400";
    f.setAttribute("loading", "lazy"); f.setAttribute("allowfullscreen", "");
    // Delegate screen capture / camera / mic, or a recorder inside the frame
    // can never prompt — Permissions-Policy denies it with no dialog at all.
    f.setAttribute("allow", "display-capture; camera; microphone");
    f.style.border = "none";
    return f;
  }
  function upgradeEmbedPage(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var h = el.getAttribute("height") || "400";
    var src = (window.lcHref || String)(a.getAttribute("href"));
    if (src && src.indexOf("?") === -1) src += "?embed=true"; else src += "&embed=true";
    /* fresh="true" — for bot-regenerated pages (the behave report): Pages
       caches HTML ~10 min, so an embedded report could contradict the
       cache-busted JSON grids beside it. A per-load stamp keeps them honest. */
    if (el.getAttribute("fresh") === "true") src += "&v=" + Date.now();
    var f = _iframeEl(src, h, "lc-embed-page");
    if (el.id) { f.id = el.id; f.setAttribute("data-lc-id", el.id); }   /* so self.page.<id>.load() works */
    el.parentNode.replaceChild(f, el);
  }
  /* ── THE SAME FRAME, ON EVERYTHING THAT SAVES ────────────────────────
     Michel, 2026-08-11: *"the bench visual indicator should be used all
     over the place where those local files are used (cv, grids for
     dogs.yaml, etc)"*. A pad, a grid, a persona card and a page slot all
     write to the learner's own repo, and until now only the slot said so —
     so the most important fact about a block (this file is YOURS) was
     visible in one place out of four.

     lcBenchFrame wraps any element in the slot's stripe: the owner's face,
     the path, and the state. It deliberately carries NO menu and NO 💾: a
     pad and a grid already own their keep bar, and two save buttons on one
     block is worse than none. The page slot keeps its own richer head. */
  window.lcBenchFrame = function (el, opts) {
    opts = opts || {};
    if (!el || el._lcFramed) return null;
    var path = opts.path || "";
    if (!path) return null;
    el._lcFramed = true;
    /* SOME COMPONENTS WIRE THEMSELVES BEFORE THEY ARE IN THE PAGE — the
       persona card is built, wired, and only then swapped in. Framing a
       node with no parent threw and took the whole upgrade with it (the
       card rendered nothing at all). So wait for the mount instead. */
    if (!el.parentNode) {
      var want = !!opts.mine, real = null, tries = 0;
      (function wait() {
        if (el.parentNode) {
          el._lcFramed = false;
          real = window.lcBenchFrame(el, opts);
          if (real) real.setMine(want);
          return;
        }
        if (++tries > 40) return;
        setTimeout(wait, 50);
      })();
      return { el: null,
               repaint: function () { if (real) real.repaint(); },
               setMine: function (v) { want = !!v; if (real) real.setMine(v); } };
    }
    /* ONE FRAME PER SPACE, NOT ONE PER FILE (Michel, 2026-08-12: *"why
       having multiple levels?"*). A page in the learner's bench, rendered
       inside a lesson, can hold saving blocks of its own — and each one
       drew its own stripe inside the first, three headers deep for one
       idea: this is your space. The outer frame already said it. Inside a
       slot the blocks render bare, and the checking moves where it belongs:
       a feature on the lesson page that reads their files. */
    if (el.closest && el.closest(".lc-bench-slot")) {
      return { el: el, repaint: function () {}, setMine: function () {} };
    }
    var box = document.createElement("div");
    box.className = "lc-bench-slot lc-bench-lite";
    el.parentNode.insertBefore(box, el);
    var head = document.createElement("div");
    head.className = "lc-bench-head";
    box.appendChild(head);
    box.appendChild(el);

    var mine = !!opts.mine;
    var gradesId = opts.id || "";
    function graders() {
      return gradesId
        ? [].slice.call(document.querySelectorAll('.lc-feature[data-grades="' + gradesId + '"]'))
        : [];
    }
    function state() {
      if (!mine) return "starter";
      var g = graders();
      if (g.length && g.every(function (c) { return c.getAttribute("data-status") === "passing"; }))
        return "done";
      return "draft";
    }
    function paint() {
      var repo = (window.lcBench ? window.lcBench.target(box).repo : "") || "";
      var me = null;
      try { me = JSON.parse(localStorage.getItem("lc_gh_user") || "null"); } catch (e) {}
      var login = (me && me.login) || repo.split("/")[0] || "";
      var pic = (me && me.avatar_url)
        ? "<img class='lc-bench-avatar' src='" + escapeHtml(me.avatar_url) + "' alt='' loading='lazy'>"
        : (login
            ? "<img class='lc-bench-avatar' src='https://github.com/" + encodeURIComponent(login) +
              ".png?size=48' alt='' loading='lazy'>"
            : "<span class='lc-bench-avatar lc-bench-avatar-none'>🎒</span>");
      var st = state();
      box.setAttribute("data-state", st);
      /* the RESOLVED path, not the knob: `cv.md` beside a lesson lives at
         courses/<course>/<module>/cv.md, and that is the file the learner
         will look for in their own repo */
      var full = path;
      try { full = window.lcBench ? window.lcBench.resolve(path, box) : path; } catch (e) {}
      head.innerHTML = pic +
        "<span class='lc-bench-who'>" + (repo ? "@" + escapeHtml(login) : "your space") + "</span>" +
        "<span class='lc-bench-path' title='" + escapeHtml(full) + "'>" +
          escapeHtml(repo ? benchLabel(full) : "not connected yet") + "</span>" +
        "<span class='lc-bench-state " + STATES[st][1] + "'>" + STATES[st][0] + "</span>";
    }
    document.addEventListener("lc-model-changed", function () { if (box.isConnected) paint(); });
    paint();
    return { el: box, repaint: paint,
             setMine: function (v) { mine = !!v; paint(); } };
  };

  /* WHAT A LEARNER NEEDS TO READ IS THE ADDRESS INSIDE THEIR COURSE, not the
     whole path (Michel, 2026-08-12: *"the file names should be displayed
     relative to course's root — ex module_03/pitch.md, not the whole path"*).
     `courses/micro_build_ai/` is the same on every slot on every page, so it
     is pure noise in a chip that has to fit next to an avatar. The full path
     stays in the tooltip for the one moment it matters. */
  function benchLabel(p) {
    return String(p || "").replace(/^courses\/[^/]+\//, "");
  }

  /* one wording for every state, wherever the frame appears */
  var STATES = {
    starter: ["the lesson's copy", "lc-bench-seed"],
    draft:   ["draft — yours", "lc-bench-draft"],
    done:    ["✓ checked", "lc-bench-yours"]
  };

  /* ── a BENCH SLOT inside a read-only lesson ──────────────────────────
     {: .embed save="wiring.md" } on a fenced block: the fence is the
     author's seed, the learner's copy lives at that path in their own
     bench, and the region is stamped as ITS OWN source. That last part is
     the whole trick — the x-ray editor already resolves its commit target
     with closest(), so a ⚙️ inside the slot writes to the bench through
     the path that already exists. The lesson around it stays the vault's.
     Same seed/override/starter/versions contract as a pad or a grid. */
  function upgradeBenchSlot(el) {
    var benchPath = el.getAttribute("save") || "";
    var code = el.querySelector("code");
    var seed = (code || el).textContent.replace(/\n+$/, "");
    var box = document.createElement("div");
    box.className = "lc-embed lc-bench-slot";
    var t = window.lcBench ? window.lcBench.target(el) : {};
    /* stamp BEFORE the seed renders: components inside must upgrade with
       the slot's source already in place, or the first gear resolves the
       lesson instead of the bench */
    if (t.repo) box.setAttribute("data-lc-src-repo", t.repo);
    box.classList.add("lc-run");            /* the marker closest() looks for */
    el.parentNode.replaceChild(box, el);

    /* A THIN FRAME WAS TOO THIN. "Your own space" was carried by a 1px
       border nobody notices on a phone, so the most important fact about
       this block — that it is the learner's file and not the lesson's —
       was the least visible thing on the page. The slot now says whose it
       is: a tinted sheet, an accent bar that carries the save state, and a
       header stripe with the bench owner's avatar. (Michel, 2026-08-11 —
       trial, to be settled after seeing it.) */
    var slotId = el.getAttribute("id") || "";
    if (slotId) { box.id = slotId; box.setAttribute("data-lc-id", slotId); }
    var head = document.createElement("div");
    head.className = "lc-bench-head";
    var body = document.createElement("div");
    body.className = "lc-bench-body";
    box.appendChild(head);
    box.appendChild(body);

    /* ── the slot's three states ──────────────────────────────────────
       starter  the lesson's copy — nothing of the learner's yet
       draft    they saved; the file is theirs now
       done     the LESSON's check on this slot passes
       Green is never self-declared: the card that grades a slot names it
       with grades="<slot id>" and lives in the vault, where the person
       being marked cannot reach it. A check the learner writes inside
       their own file still teaches — it just does not award the colour. */
    function graders() {
      return slotId
        ? [].slice.call(document.querySelectorAll('.lc-feature[data-grades="' + slotId + '"]'))
        : [];
    }
    function computeState() {
      if (!mine) return "starter";
      var g = graders();
      if (g.length && g.every(function (c) { return c.getAttribute("data-status") === "passing"; }))
        return "done";
      return "draft";
    }

    function paintHead(path) {
      var repo = (window.lcBench ? window.lcBench.target(box).repo : "") || "";
      /* WHOSE FACE? Not the repo owner's — a class bench is forked INTO the
         org, so every learner would see the same organisation logo over
         their own work. The topbar already caches the signed-in account
         (lc_gh_user); that is the person whose file this is. Fall back to
         the repo owner for a personal bench. */
      var me = null;
      try { me = JSON.parse(localStorage.getItem("lc_gh_user") || "null"); } catch (e) {}
      var login = (me && me.login) || repo.split("/")[0] || "";
      var pic = (me && me.avatar_url)
        ? "<img class='lc-bench-avatar' src='" + escapeHtml(me.avatar_url) + "' alt='' loading='lazy'>"
        : (login
            ? "<img class='lc-bench-avatar' src='https://github.com/" + encodeURIComponent(login) +
              ".png?size=48' alt='' loading='lazy'>"
            : "<span class='lc-bench-avatar lc-bench-avatar-none'>🎒</span>");
      var who = repo
        ? "<span class='lc-bench-who'>@" + escapeHtml(login) + "</span>"
        : "<span class='lc-bench-who'>your space</span>";
      var full = path || benchPath;
      var where = repo
        ? "<span class='lc-bench-path' title='" + escapeHtml(full) + "'>" +
            escapeHtml(benchLabel(full)) + "</span>"
        : "<span class='lc-bench-path'>not connected yet</span>";
      var st = computeState();
      box.setAttribute("data-state", st);
      var chip = "<span class='lc-bench-state " + STATES[st][1] + "'>" + STATES[st][0] + "</span>";
      /* THE ONE ACTION A BEGINNER NEEDS IS NOT IN A MENU. On a starter the
         only useful move is "make this mine", and it was hidden behind ⋯ —
         where it also happened to be the row most easily clipped. So it is a
         button, in the header, saying 💾 like every other saved thing on the
         platform (Michel, 2026-08-11). */
      var canSave = st === "starter" && !!(window.lcBench && window.lcBench.target(box).repo);
      head.innerHTML = pic + who + where + chip +
        (canSave ? "<button type='button' class='lc-bench-save'>💾 Save to my space</button>" : "") +
        /* TWO SCOPES, TWO AFFORDANCES, AND THE SMALLER ONE IS THE GEAR
           (Michel, 2026-08-13: *"there is some confusion between ⋯ and ⚙️"*).
           ⚙️ belongs to whatever is UNDER THE POINTER — a part, its wiring.
           ⋯ belongs to the STRIPE it sits in, which is the file. Using the
           gear for both would say the file is just another part. So the
           glyph stays and stops being mystery meat: it names its scope. */
        "<button type='button' class='lc-bench-more' title='This file — copy, open on its own, versions, start over' aria-label='what I can do with this file'>⋯</button>";
      var saveBtn = head.querySelector(".lc-bench-save");
      if (saveBtn) saveBtn.addEventListener("click", function (ev) {
        ev.stopPropagation(); act("clone");
      });
      head.querySelector(".lc-bench-more").addEventListener("click", function (ev) {
        ev.stopPropagation();
        openMenu(st);
      });
      /* a repaint rewrites the stripe — put the versions handle back, or the
         second visit to ⋯ opens a panel wired to a button nobody holds */
      if (versions) head.appendChild(versions.button);
    }

    /* AN ALERT BOX IS NOT A VERSION LIST. The first cut printed the commit
       messages into window.alert — no dates you could read, no way to see
       what a version said, no way to bring it back (Michel, 2026-08-11).
       The pad and the grid already have the real panel; the slot borrows the
       same one, opened from ⋯ instead of its own button. "Bring back" here
       writes a new version rather than staging one: the slot has no separate
       💾, and nothing is lost — the older text is still in 🕘. */
    var versions = null;
    function versionsHandle() {
      if (versions || !window.lcVersions) return versions;
      versions = window.lcVersions.attach({
        path: benchPath, el: box, anchor: head,
        current: function () { return md; },
        apply: function (text) {
          box._lcSlot.save(function () { return text; }, "🕘 back to an earlier version")
            .catch(function (e) { alert("Could not bring that version back: " + (e.message || e)); });
        }
      });
      versions.button.hidden = false;
      versions.button.style.display = "none";   /* the ⋯ row is its handle */
      head.appendChild(versions.button);
      return versions;
    }

    /* ── the transitions, with guards doing the greying ──────────────── */
    function openMenu(st) {
      var old = box.querySelector(".lc-bench-menu");
      if (old) { old.remove(); return; }
      var repo = (window.lcBench ? window.lcBench.target(box).repo : "") || "";
      var path = box.getAttribute("data-lc-src-path") || benchPath;
      var items = [
        { key: "clone", icon: "📋", label: "Copy the starter into my space",
          on: st === "starter" && !!repo,
          why: !repo ? "connect your space first" : "you already have your own copy" },
        /* A STARTER HAS NO FILE TO OPEN. The frame shows the lesson's copy
           until the learner saves; opening its bench address then 404s, and
           the runner — which cannot know this page was never meant to come
           from the hub — offers a Refresh that can never bring it (Michel,
           2026-08-11). So the door stays shut until 💾 has made a file. */
        { key: "open", icon: "📄", label: "Open it on its own",
          on: !!repo && st !== "starter",
          why: !repo ? "connect your space first" : "save it first — there is no file yet" },
        { key: "versions", icon: "🕘", label: "Every version I saved",
          on: st !== "starter", why: "nothing saved yet" },
        { key: "reset", icon: "↺", label: "Start over from the lesson's copy",
          on: st !== "starter", why: "this IS the lesson's copy" }
      ];
      var menu = document.createElement("div");
      menu.className = "lc-bench-menu";
      menu.innerHTML = items.map(function (i) {
        return "<button type='button' data-a='" + i.key + "'" + (i.on ? "" : " disabled title='" +
          escapeHtml(i.why) + "'") + ">" + i.icon + " " + escapeHtml(i.label) + "</button>";
      }).join("");
      head.appendChild(menu);
      menu.addEventListener("click", function (ev) {
        var b = ev.target.closest("button[data-a]");
        if (!b || b.disabled) return;
        menu.remove();
        act(b.getAttribute("data-a"), path, repo);
      });
      setTimeout(function () {
        document.addEventListener("click", function once() {
          menu.remove(); document.removeEventListener("click", once);
        });
      }, 0);
    }

    function act(a, path, repo) {
        if (a === "clone") {
          window.lcBench.write(benchPath, md, window.lcStarterMsg || "🌱 starter", sha, box)
            .then(function (s) { sha = s || sha; paint(md, true); })
            .catch(function (e) { alert("Could not copy it in: " + (e.message || e)); });
        } else if (a === "open") {
          var url = (window.lcHref ? window.lcHref("/run.html") : "/run.html")
                  + "#src=gh:" + repo + "/" + path;
          window.location.href = url;
        } else if (a === "versions") {
          var v = versionsHandle();
          if (v) v.button.click();
        } else if (a === "reset") {
          if (!confirm("Replace your copy with the lesson's? Your saved versions stay in 🕘.")) return;
          window.lcBench.write(benchPath, seed, "↺ start over", sha, box)
            .then(function (s) { sha = s || sha; paint(seed, true); })
            .catch(function (e) { alert("Could not start over: " + (e.message || e)); });
        }
    }

    var md = seed;        /* the markdown this slot currently holds */
    var sha = null;       /* the bench file's sha — null while nothing is saved */
    var mine = false;

    function paint(text, isMine) {
      md = String(text);
      mine = !!isMine || mine;
      var path = window.lcBench ? window.lcBench.resolve(benchPath, box) : benchPath;
      box.setAttribute("data-lc-src-path", path);
      if (isMine) box.setAttribute("data-lc-mine", "1");
      paintHead(path);
      var norm = window.lcNormIAL(md.trim());
      loadMarked(function () {
        if (window.lcClientFootnotes) norm = window.lcClientFootnotes(norm);
        body.innerHTML = (window.lcInlineIAL || function (h) { return h; })(marked.parse(norm));
        if (window.lcApplyIAL)    window.lcApplyIAL(body);
        /* re-render = new knobs: forget the previous render's snapshot, or
           the ⚙️ would offer the value the learner has already replaced */
        if (window.lcSnapshotSources) window.lcSnapshotSources(body, true);
        if (window.lcScanElement) window.lcScanElement(body);
        if (window.lcRebase)      window.lcRebase(body);
        /* a slot renders after the page's cells were collected: a {= cell }
           inside it stayed a literal (Module 02's tally, 2026-09-17). Same
           idempotent, document-wide rescan a block makes. */
        if (window.lcCellsRescan) window.lcCellsRescan();
      });
    }

    /* The slot OWNS its file, so it is the one that writes it. An editor
       inside the frame hands over a transform of the markdown rather than a
       finished commit: the file may not exist yet (the learner has only ever
       seen the seed), and the first save must lay the author's starter down
       first so the very first change is readable in 🕘 — the same contract
       the pad and the grid follow. */
    box._lcSlot = {
      path: benchPath,
      text: function () { return md; },
      /* Apply on the frame's own gear: repaint from the edited text without
         touching the bench — what the learner sees before they Save */
      preview: function (text) { paint(text, mine); },
      save: function (transform, label) {
        var next;
        try { next = transform(md); } catch (e) { next = null; }
        if (next == null) {
          /* say what was looked for — "couldn't locate" fits a dozen causes
             (Michel, 2026-09-16, desk two on North Burns: the toast alone
             left nothing to reason from) */
          var dg = (transform && transform.diag) || {};
          var anchor = String(dg.anchor == null ? "" : dg.anchor).split("\n")[0].slice(0, 60);
          return Promise.reject(new Error("couldn't locate that part in your file — looked for «"
            + anchor + "…», found it " + (dg.hits == null ? "?" : dg.hits) + " time(s) in "
            + benchPath + " (" + md.length + " chars)"));
        }
        if (!window.lcBench) return Promise.reject(new Error("no bench connected"));
        var first = !mine;
        return (first
          ? window.lcBench.write(benchPath, md, window.lcStarterMsg, sha, box)
              .then(function (s) { sha = s || sha; }).catch(function () {})
          : Promise.resolve()
        ).then(function () {
          return window.lcBench.write(benchPath, next, label || ("✍️ " + benchPath), sha, box);
        }).then(function (s) {
          sha = s || sha;
          paint(next, true);
          return s;
        });
      }
    };

    /* THE GRADE ARRIVES LATER. A check turns green when the learner presses
       ▶, long after this slot rendered — and feature.md already announces
       every settled status on the model bus, so the stripe listens rather
       than polls. Head only: repainting the body would tear down the very
       components the check just measured. */
    document.addEventListener("lc-model-changed", function () {
      if (box.isConnected) paintHead(box.getAttribute("data-lc-src-path") || benchPath);
    });

    if (window.lcBench && t.repo && t.pat) {
      window.lcBench.read(benchPath, box)
        .then(function (f) { if (f) sha = f.sha; paint(f ? f.text : seed, !!f); })
        .catch(function () { paint(seed, false); });
    } else {
      paint(seed, false);                   /* not joined yet: the lesson's own */
    }
  }
  /* the door the x-ray editor knocks on: "am I standing inside someone's
     own file, and if so, who writes it?" */
  window.lcBenchSlotOf = function (el) {
    var b = el && el.closest ? el.closest(".lc-bench-slot") : null;
    return (b && b._lcSlot) || null;
  };

  function upgradeEmbedExternal(el) {
    var a = el.querySelector("a");
    /* a fenced .embed with save= is a bench slot, not a media embed */
    if (!a && el.getAttribute("save")) { upgradeBenchSlot(el); return; }
    if (!a) return;
    var href = a.getAttribute("href");
    /* master="<grid id>": the frame FOLLOWS the selection — the link's own
       href is what shows before a click (an issue page), the clicked row's
       field="page" afterwards (that story's page). A "#" href starts blank.
       (Michel, 2026-10-04, the stories example.) */
    var masterId = el.getAttribute("master") || "";
    if (masterId) {
      var field = el.getAttribute("field") || "page";
      var start = (href && href !== "#") ? href : "about:blank";
      var frame = _iframeEl(start, el.getAttribute("height") || "600", "lc-embed-page");
      frame.setAttribute("data-master", masterId);
      el.parentNode.replaceChild(frame, el);
      if (window.lcMasterDetail) window.lcMasterDetail.subscribe(masterId, function (row) {
        var u = row && row[field];
        if (typeof u === "string" && /^(https?:\/\/|\/)/i.test(u) && frame.src !== u) frame.src = u;
      });
      return;
    }
    // External URLs → iframe — EXCEPT images: a photo is a picture, not a
    // page, and hotlinks as an <img> further down (all sizing knobs apply).
    // URL-API images carry no extension (placedog, unsplash source…) —
    // image="true" declares the intent explicitly.
    var forceImg = el.getAttribute("image") === "true";
    if (/^https?:\/\//i.test(href) && !forceImg && !/\.(png|jpe?g|gif|webp|svg|avif)$/i.test(href)) {
      el.parentNode.replaceChild(_iframeEl(href, el.getAttribute("height") || "600", "lc-embed-page"), el);
      return;
    }
    // Local module → fetch the raw markdown source and render it inline.
    // [Lucky](/_dog) → docs/_dog.md fetched from raw.githubusercontent.
    var container = document.createElement("div");
    container.className = "lc-embed";
    container.innerHTML = "<div style='color:#aaa;font-style:italic;padding:0.5em 0'>⏳ Loading…</div>";
    el.parentNode.replaceChild(container, el);
    var rel = href.replace(/^\/+|\/+$/g, "");
    /* an image target is a picture, not a markdown module — embedding one
       used to append .md and 404 (module_00, 2026-07-29). Do what the author
       meant: render an <img>, resolved exactly like the module would be. */
    var isImg = /\.(png|jpe?g|gif|webp|svg|avif)$/i.test(rel) || forceImg;
    if (!isImg && !/\.md$/i.test(rel)) rel += ".md";
    var pat = localStorage.getItem("lc_ed_pat") || "";
    var unpublished = /(^|\/)_[^\/]*$/.test(rel);   // _-prefixed: repo tree only, never in the Pages build
    /* Folder-relative embeds. A surface that renders a file from OUTSIDE the
       Pages tree — the runner's bench/vault render, the editor preview of a
       course page — advertises that file on an ancestor via data-lc-src-path,
       the same contract xray and .folder already follow. Under it, "/x" and
       "x" both mean "my sibling": courses/ and hubs/ never exist under docs/,
       so the site-root reading is guaranteed dead there. docs/ renders keep
       the site-root meaning untouched. */
    var srcEl  = container.closest ? container.closest("[data-lc-src-path]") : null;
    var srcDir = srcEl ? (srcEl.getAttribute("data-lc-src-path") || "").split("/").slice(0, -1).join("/") : "";
    /* A MIRROR IS THE COURSE, RENDERED ELSEWHERE. docs/_410/databases/… is
       the publish gate's copy of courses/databases/… — under docs/, but an
       underscore folder Pages never builds, so "/x" can only mean the
       sibling file. Read as a site asset, every slide of the setup page
       404'd on pedia (Michel, 2026-09-13). Same rule the voice manifest
       learned on 2026-09-03. */
    var based  = !!(srcDir && (!/^docs(\/|$)/.test(srcDir) || /^docs\/_[^\/]+(\/|$)/.test(srcDir)));
    /* height="400" knob (same as embed-page): sizes the image; width follows.
       width="40%" sizes relative to the container (or px) so the picture
       scales with the page; align="left|right" floats it so text wraps. */
    var embH = parseInt(el.getAttribute("height") || "", 10) || 0;
    var embW = (el.getAttribute("width") || "").trim();
    if (/^\d+$/.test(embW)) embW += "px";
    if (!/^\d+(\.\d+)?(px|%|em|rem|vw)$/.test(embW)) embW = "";
    var imgStyle = "max-width:100%" +
      (embW ? ";width:" + embW : "") +
      (embH ? ";height:" + embH + "px" + (embW ? "" : ";width:auto") : "");
    var embAlign = (el.getAttribute("align") || "").toLowerCase();
    if (isImg && (embAlign === "left" || embAlign === "right"))
      container.classList.add("lc-embed-" + embAlign);
    if (isImg && (el.getAttribute("effect") || "").toLowerCase() === "ambient")
      container.classList.add("lc-embed-ambient");
    /* shape="circle": a portrait, not a poster (Michel, 2026-08-12). The
       crop is square-from-centre, so a rectangular photo keeps its face
       instead of squeezing. */
    if (isImg && (el.getAttribute("shape") || "").toLowerCase() === "circle")
      container.classList.add("lc-embed-circle");
    if (isImg && /^https?:\/\//i.test(href)) {
      /* EXTERNAL image: hotlink as-is — a partner site's photo, a public
         image API. Never rebased, never treated as a sibling; every sizing
         knob (height/width/align/effect) applies like any other image. */
      container.innerHTML = "<img src='" + escapeHtml(href) + "' alt='" + escapeHtml((a.textContent || "").trim()) + "' style='" + imgStyle + "'>";
      return;
    }
    if (isImg && (href.charAt(0) === "/" || !based)) {
      /* IMAGES follow the platform's link rule, unlike md fragments: a
         site-absolute src is a SITE asset everywhere — including inside a
         course render (module_00 hit this: /courses/AI-Builders.png must
         not become a sibling lookup). Relative image srcs under a based
         render stay folder-relative below. */
      container.innerHTML = "<img src='" + escapeHtml(window.lcHref ? window.lcHref("/" + rel) : "/" + rel) + "' alt='" + escapeHtml((a.textContent || "").trim()) + "' style='" + imgStyle + "'>";
      return;
    }
    /* req = the read we try first. anon = the SAME read without the key, kept
       as a thunk for when a key is refused. A stored key that GitHub no longer
       accepts must never break a node a keyless visitor can read — pedia's
       tutorial showed "HTTP 401" on every proxy while anonymous raw answered
       200 (2026-08-10). null = no keyless route exists (private repo). */
    var req, anon = null;
    if (based) {
      var srcRepo = srcEl.getAttribute("data-lc-src-repo") || _lcSiteRepo;
      /* normalise ../ so a module can embed a fragment shared one level up */
      var stack = [];
      (srcDir + "/" + rel).split("/").forEach(function (s) {
        if (s === "..") stack.pop(); else if (s && s !== ".") stack.push(s);
      });
      var full = stack.join("/");
      if (isImg) {
        var alt = escapeHtml((a.textContent || "").trim());
        if (!pat) {   // public repo: raw serves images anonymously
          container.innerHTML = "<img src='https://raw.githubusercontent.com/" + srcRepo + "/HEAD/" + full + "' alt='" + alt + "' style='" + imgStyle + "'>";
          return;
        }
        fetch("https://api.github.com/repos/" + srcRepo + "/contents/" + full,
              { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw" } })
          .then(function (r) {
            if (!r.ok) throw new Error("HTTP " + r.status);
            /* media-type quirk: some proxies return the JSON envelope despite
               Accept raw — unwrap the base64 into bytes */
            if ((r.headers.get("content-type") || "").indexOf("json") >= 0)
              return r.json().then(function (env) {
                var bin = atob((env.content || "").replace(/\n/g, ""));
                var u8 = new Uint8Array(bin.length);
                for (var i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
                return new Blob([u8]);
              });
            return r.blob();
          })
          .then(function (b) {
            /* GitHub types raw answers vnd.github.v3.raw — retype from the
               extension so stricter engines (Safari) decode the blob too */
            var ext = (full.match(/\.(\w+)$/) || [])[1];
            var mime = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", gif: "image/gif", webp: "image/webp", svg: "image/svg+xml", avif: "image/avif" }[(ext || "").toLowerCase()];
            if (mime && b.type !== mime) b = new Blob([b], { type: mime });
            var img = document.createElement("img");
            img.src = URL.createObjectURL(b);
            img.alt = (a.textContent || "").trim();
            img.setAttribute("style", imgStyle);
            container.innerHTML = "";
            container.appendChild(img);
          })
          .catch(function (err) {
            /* Same rule as the markdown proxy: a refused key must not hide a
               picture anonymous raw serves. Only a private repo has nowhere
               else to look. */
            if (/HTTP 40[13]$/.test(err.message || "") &&
                !(window.lcRepoPrivate && srcRepo === _lcSiteRepo)) {
              container.innerHTML = "<img src='https://raw.githubusercontent.com/" + srcRepo + "/HEAD/" + full + "' alt='" + alt + "' style='" + imgStyle + "'>";
              return;
            }
            container.innerHTML = "<div style='color:#c00'>⚠️ Could not load " + escapeHtml(href) + ": " + escapeHtml(err.message) + "</div>";
          });
        return;
      }
      if (pat) {
        /* builder key reads course material wherever the render came from */
        req = fetch("https://api.github.com/repos/" + srcRepo + "/contents/" + full,
                    { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw" } });
        if (!(window.lcRepoPrivate && srcRepo === _lcSiteRepo))
          anon = function () { return fetch("https://raw.githubusercontent.com/" + srcRepo + "/HEAD/" + full); };
      } else if (window.lcRepoPrivate && srcRepo === _lcSiteRepo) {
        container.innerHTML = "<div style='color:#6b7280;font-style:italic;padding:0.5em 0'>🔑 Private node — connect a GitHub PAT (topbar “Get started”) to preview it.</div>";
        return;
      } else {
        req = fetch("https://raw.githubusercontent.com/" + srcRepo + "/HEAD/" + full);
      }
    } else if (pat && _lcSiteRepo) {
      /* builder: the API + PAT reaches every node, published or not */
      req = fetch("https://api.github.com/repos/" + _lcSiteRepo + "/contents/docs/" + rel,
                  { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw" } });
      /* the keyless route this node would have taken with no key at all */
      if (!unpublished)
        anon = function () { return fetch(window.lcHref ? window.lcHref("/" + rel) : "/" + rel); };
      else if (!window.lcRepoPrivate)
        anon = function () { return fetch("https://raw.githubusercontent.com/" + _lcSiteRepo + "/HEAD/docs/" + rel); };
    } else if (unpublished) {
      /* only raw serves an unpublished node. On a PRIVATE repo raw 404s for
         anonymous visitors — don't fetch a URL we know will 404 (console error,
         nothing to show); invite a PAT. Public repos still preview it via raw. */
      if (window.lcRepoPrivate) {
        container.innerHTML = "<div style='color:#6b7280;font-style:italic;padding:0.5em 0'>🔑 Private node — connect a GitHub PAT (topbar “Get started”) to preview it.</div>";
        return;
      }
      req = fetch("https://raw.githubusercontent.com/" + _lcSiteRepo + "/HEAD/docs/" + rel);
    } else {
      /* published node: the Pages site serves its .md same-origin — works on the
         private lab too (raw would 404 there), no rate limit, no CORS */
      req = fetch(window.lcHref ? window.lcHref("/" + rel) : "/" + rel);
    }
    function readOr401(r) {
      if (r.ok) return r.text();
      /* 401 = the key is bad (expired, revoked, regenerated); 403 = it is out
         of API quota. Neither says anything about the node — so retry the way
         a keyless visitor reads it, once. */
      if ((r.status === 401 || r.status === 403) && anon) {
        var again = anon();
        anon = null;
        return again.then(readOr401);
      }
      throw new Error("HTTP " + r.status);
    }
    req
      .then(readOr401)
      .then(function(text) {
        // strip optional YAML front matter
        if (text.indexOf("---") === 0) {
          var end = text.indexOf("\n---", 3);
          if (end >= 0) { var nl = text.indexOf("\n", end + 1); text = nl >= 0 ? text.slice(nl + 1) : ""; }
        }
        loadMarked(function() {
          /* full component parity, like the runner and the editor preview: an
             embedded fragment is PART of the page — its quizzes, grids and
             blocks must upgrade too. Without normalise+apply+scan, a
             {: .quiz } marker rendered as literal text and the checkboxes
             stayed dead (module_00's settling quiz, 2026-07-30). */
          var norm = window.lcNormIAL(text.trim());
          if (window.lcClientFootnotes) norm = window.lcClientFootnotes(norm);
          container.innerHTML = (window.lcInlineIAL || function (h) { return h; })(marked.parse(norm));
          if (window.lcApplyIAL)    window.lcApplyIAL(container);
          if (window.lcScanElement) window.lcScanElement(container);
          if (window.lcRebase) window.lcRebase(container); // heal root-absolute paths under a project base
        });
      })
      .catch(function(err) {
        /* A refused key is a key problem, not a missing node — say so, and say
           what to do about it. "HTTP 401" sent readers hunting for a broken
           link that was never broken. */
        var msg = /HTTP 40[13]$/.test(err.message || "")
          ? "🔑 Your GitHub key was refused — reconnect it from the topbar (“Get started”)."
          : "⚠️ Could not load " + escapeHtml(href) + ": " + escapeHtml(err.message);
        container.innerHTML = "<div style='color:#c00'>" + msg + "</div>";
      });
  }
  /* YouTube host for embeds. -nocookie serves the same player without the
     tracking cookie until someone actually presses play — the right default
     for a classroom, where the audience did not choose to be measured. It
     supports enablejsapi exactly like the main host, so nothing is given up. */
  var YT_HOST = "https://www.youtube-nocookie.com";
  /* A FILE IS NOT A FRAME (Michel, 2026-08-13: an mp4 beside the course
     index, playing itself in a loop). YouTube and Drive are somebody else's
     player, so they get an iframe; an .mp4/.webm/.ogv in the material is OUR
     file and deserves a real <video> — which is also the only way to say
     loop, muted and autoplay. And when it lives in a private repo beside the
     page, it is read the way images are: through the contents API with the
     reader's own key, into a blob. */
  var NATIVE_MEDIA = /\.(mp4|webm|ogv|ogg|m4v|mov)(\?|#|$)/i;
  function nativeVideo(el, a, href) {
    var v = document.createElement("video");
    v.className = "lc-video lc-video-file";
    /* the same soft corner the hive and every embedded frame wear, so a clip
       beside them reads as one family (Michel, 2026-08-13) */
    v.style.borderRadius = "8px";
    v.setAttribute("controls", "");
    v.setAttribute("preload", "metadata");
    v.style.width = "100%";
    var h = el.getAttribute("height");
    if (h) v.style.maxHeight = /^\d+$/.test(h) ? h + "px" : h;
    if (el.hasAttribute("poster")) v.setAttribute("poster", el.getAttribute("poster"));
    var on = function (k) { var x = el.getAttribute(k); return x !== null && !/^(false|0|no|off)$/i.test(x); };
    if (on("loop")) v.setAttribute("loop", "");
    if (on("playsinline") || on("autoplay")) v.setAttribute("playsinline", "");
    if (on("autoplay")) {
      /* every browser refuses to autoplay sound nobody asked for, so an
         autoplaying clip is a MUTED clip — state it rather than let the
         browser silently ignore the knob */
      v.setAttribute("muted", ""); v.muted = true;
      v.setAttribute("autoplay", "");
    } else if (on("muted")) { v.setAttribute("muted", ""); v.muted = true; }
    v.setAttribute("title", a.textContent || "video");
    if (el.id) { v.id = el.id; v.setAttribute("data-lc-id", el.id); }
    var relative = !/^([a-z][a-z0-9+.-]*:|\/)/i.test(href);
    var runRoot = relative && el.closest ? el.closest(".lc-run[data-lc-src-path]") : null;
    if (!runRoot) { v.src = href; }
    else if (window.lcMediaBlob) window.lcMediaBlob(runRoot, href).then(function (u) {
      if (u) v.src = u; else v.src = href;
    });
    if (window.lcCarryCellKnobs) window.lcCarryCellKnobs(el, v);
    el.parentNode.replaceChild(v, el);
    if (window.lcCellsRescan) window.lcCellsRescan();
  }

  function upgradeVideo(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var href = a.getAttribute("href");
    if (NATIVE_MEDIA.test(href)) { nativeVideo(el, a, href); return; }
    var src = href, isYt = false;
    var gdrive = href.match(/^gdrive:(.+)/);
    if (gdrive) src = "https://drive.google.com/file/d/" + gdrive[1] + "/preview";
    var yt = href.match(/(?:youtube(?:-nocookie)?\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([^&?\/]+)/);
    if (yt) {
      isYt = true;
      /* enablejsapi is what lets the page TALK to the player (the play/pause
         verbs below postMessage to it); rel=0 keeps YouTube from offering
         strangers' videos when a lesson clip ends. */
      src = YT_HOST + "/embed/" + yt[1] + "?enablejsapi=1&rel=0&modestbranding=1"
          + (location.origin && location.origin.indexOf("http") === 0
             ? "&origin=" + encodeURIComponent(location.origin) : "");
    }
    var f = _iframeEl(src, el.getAttribute("height") || "400", "lc-video");
    /* carry the author's id onto the frame — same move upgradeEmbedPage makes,
       and for the same reason: without it nothing on the page can address this
       video, so an avatar cannot play it and a proof cannot check it. */
    if (el.id) { f.id = el.id; f.setAttribute("data-lc-id", el.id); }
    if (isYt) {
      f.setAttribute("data-lc-yt", yt[1]);
      /* a cross-origin frame cannot start playing unless the PARENT delegates
         autoplay to it — without this the play verb postMessages into a player
         that is not allowed to obey */
      f.setAttribute("allow", (f.getAttribute("allow") || "") + "; autoplay; encrypted-media");
    }
    f.setAttribute("title", a.textContent || "video");
    /* a gated video is the point of gating one: visible="= quiz.passed" makes
       the clip the REWARD for answering, and the knob has to survive the swap
       or the frame renders unconditionally (Michel, 2026-08-10) */
    if (window.lcCarryCellKnobs) window.lcCarryCellKnobs(el, f);
    el.parentNode.replaceChild(f, el);
    if (window.lcCellsRescan) window.lcCellsRescan();
  }

  /* ── play / pause / seek, so an avatar can narrate over a clip ─────────
     An avatar script says   - do: play / at: recap   and then keeps talking
     while the clip runs; the manim recaps are SILENT on purpose, so the
     avatar is the only soundtrack and nothing has to be mixed.

     A YouTube frame is driven by postMessage (the documented command channel
     that enablejsapi opens) rather than by loading YouTube's iframe_api
     script: one less third-party script on every course page, and the command
     is the same either way. A native <video> just gets .play(). */
  function _lcMedia(el) {
    if (el) {
      if (el.tagName === "IFRAME" || el.tagName === "VIDEO") return el;
      var inner = el.querySelector && el.querySelector("iframe.lc-video, video");
      if (inner) return inner;
    }
    return document.querySelector("iframe.lc-video, video");
  }
  function _lcYtCmd(frame, func, args) {
    if (!frame.contentWindow) return false;
    try {
      frame.contentWindow.postMessage(JSON.stringify(
        { event: "command", func: func, args: args || [] }), "*");
      return true;
    } catch (e) { return false; }
  }
  /* THE PLAYER ANSWERS ONCE IT LISTENS. A YouTube frame only speaks back
     after the page has said "listening"; from then on every message it
     sends marks the frame ready, and the asking below stops. */
  window.addEventListener("message", function (e) {
    var frames = document.querySelectorAll("iframe.lc-video[data-lc-yt]");
    for (var i = 0; i < frames.length; i++) {
      if (frames[i].contentWindow === e.source) { frames[i].setAttribute("data-lc-yt-ready", "1"); return; }
    }
  });
  /* ONE COMMAND INTO A FRAME STILL LOADING IS LOST. The recap clip sits
     far down the page, lazily loaded; the tour scrolls to it on the very
     line that plays it, so the single playVideo used to land before the
     player existed (Michel, 2026-09-16: "the video never played"). Wake
     the frame, say "listening", and ask again every half second until the
     player answers or eight seconds pass. And MUTED: the recaps are silent
     by design — the guide is the soundtrack — and a muted clip may start
     everywhere a scripted, unmuted one is refused (a frame inside Canvas,
     Safari without a tap on the player itself). */
  function _lcYtPlay(frame, seekTo) {
    if (frame.getAttribute("loading") === "lazy") frame.setAttribute("loading", "eager");
    var tries = 0;
    function ask() {
      if (!frame.isConnected) return;
      try { frame.contentWindow.postMessage(JSON.stringify({ event: "listening", id: frame.id || "lc" }), "*"); } catch (e) {}
      _lcYtCmd(frame, "mute");
      if (seekTo != null) _lcYtCmd(frame, "seekTo", [seekTo, true]);
      _lcYtCmd(frame, "playVideo");
      tries += 1;
      if (frame.getAttribute("data-lc-yt-ready") !== "1" && tries < 16) setTimeout(ask, 500);
    }
    ask();
    return true;
  }
  function _lcMediaCmd(el, func, args) {
    var m = _lcMedia(el);
    if (!m) return false;
    if (m.tagName === "VIDEO") {
      try {
        if (func === "playVideo") { m.play(); return true; }
        if (func === "pauseVideo") { m.pause(); return true; }
        if (func === "seekTo") { m.currentTime = Number(args[0]) || 0; return true; }
      } catch (e) { return false; }
      return false;
    }
    if (!m.getAttribute("data-lc-yt")) return false;
    return _lcYtCmd(m, func, args);
  }
  window.lcVerbs.register("play", function (el, arg) {
    /* with: 12 → start from twelve seconds in, so a script can narrate one
       beat of a clip without replaying the whole thing */
    var at = (arg !== null && arg !== undefined && arg !== "") ? (Number(arg) || 0) : null;
    var m = _lcMedia(el);
    if (!m) return false;
    if (m.tagName === "VIDEO") {
      try { m.muted = true; if (at != null) m.currentTime = at; m.play().catch(function () {}); return true; }
      catch (e) { return false; }
    }
    if (!m.getAttribute("data-lc-yt")) return false;
    return _lcYtPlay(m, at);
  }, _lcMedia);
  window.lcVerbs.register("pause", function (el) {
    return _lcMediaCmd(el, "pauseVideo");
  }, _lcMedia);
  window.lcVerbs.register("seek", function (el, arg) {
    return _lcMediaCmd(el, "seekTo", [Number(arg) || 0, true]);
  }, _lcMedia);

  /* .code — a READ-ONLY SNIPPET (Michel, 2026-10-10: "the snippets should
     also be in dark mode, syntax coloured, still R/O with a copy button …
     a title with the nice emoji"). Dark, a title bar with an icon, the title
     and the language, and 📋 Copy. Markdown is painted by the pad's own
     painter, so the lesson's snippet and the pad beside it match; CSV is a
     piano by column; other languages keep Rouge's classes. The icon is the
     title's own emoji when it starts with one, else the component the
     snippet's first decoration makes (☷ for {: .form }), else 📄.
     A LINK decorated .code shows the file it points to, live:
       [dogs.csv](../module_00/dogs.csv)
       {: .code }                                                       */
  var LANG_OF_EXT = { md: "markdown", markdown: "markdown", csv: "csv", yml: "yaml", yaml: "yaml",
                      py: "python", json: "json", js: "javascript", sql: "sql", feature: "gherkin" };
  function codeText(el) {
    var c = el.querySelector("code") || el;
    return String(c.textContent || "").replace(/\n$/, "");
  }
  function fetchCodeFile(el, href) {
    if (/^(https?:)?\/\//.test(href) || href.charAt(0) === "/")
      return fetch(href).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); });
    var srcEl = el.closest ? el.closest("[data-lc-src-path]") : null;
    if (!srcEl) srcEl = document.querySelector(".lc-run[data-lc-src-path]");
    if (!srcEl) return fetch(href).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); });
    var srcPath = srcEl.getAttribute("data-lc-src-path") || "";
    var dir = srcPath.indexOf("/") >= 0 ? srcPath.replace(/\/[^\/]*$/, "") : "";
    var parts = [];
    (dir ? dir + "/" + href : href).split("/").forEach(function (p) {
      if (!p || p === ".") return;
      if (p === "..") parts.pop(); else parts.push(p);
    });
    var repo = srcEl.getAttribute("data-lc-src-repo") || _lcSiteRepo;
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    var h = { Accept: "application/vnd.github.v3.raw" };
    if (pat) h.Authorization = "Bearer " + pat;
    return fetch("https://api.github.com/repos/" + repo + "/contents/" + parts.join("/"), { headers: h })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); });
  }
  function upgradeCode(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var link = el.tagName === "P" ? el.querySelector("a[href]") : null;
    var href = link ? link.getAttribute("href") : "";
    var cls = el.className + " " + ((el.querySelector("code") || {}).className || "");
    var m = cls.match(/language-([\w+-]+)/);
    var ext = (href.split(/[?#]/)[0].match(/\.(\w+)$/) || [])[1];
    var lang = (el.getAttribute("lang") || (m ? m[1] : "") || (ext ? (LANG_OF_EXT[ext.toLowerCase()] || ext) : "") || "text").toLowerCase();
    if (lang === "md") lang = "markdown";
    var title = el.getAttribute("title") || (link ? (link.textContent || href).trim() : "");
    var text = link ? "" : codeText(el);

    var wrap = document.createElement("div");
    wrap.className = "lc-code";
    wrap.setAttribute("data-lang", lang);
    if (el.id) { wrap.setAttribute("data-lc-id", el.id); }
    var bar = document.createElement("div");
    bar.className = "lc-code-title";
    var icon = document.createElement("span");
    icon.className = "lc-code-icon";
    var lead = title.match(/^(\p{Extended_Pictographic}️?|[☀-➿■-◿]️?)\s*/u);
    icon.textContent = lead ? lead[1] : "📄";
    var t = document.createElement("span");
    t.className = "lc-code-name";
    t.textContent = lead ? title.slice(lead[0].length) : title;
    var lg = document.createElement("span");
    lg.className = "lc-code-lang";
    lg.textContent = lang;
    var copy = document.createElement("button");
    copy.type = "button";
    copy.className = "lc-code-copy";
    copy.textContent = "📋 Copy";
    copy.title = "Copy the snippet";
    bar.appendChild(icon); bar.appendChild(t); bar.appendChild(lg); bar.appendChild(copy);
    wrap.appendChild(bar);

    /* every language the painter knows is painted by it — the same colours
       on the built site and in the runner, where Rouge never ran */
    var painted = /^(markdown|csv|python|sql|yaml|json|gherkin)$/.test(window.lcPaintCodeLang(lang));
    var body = el;
    function fill(txt) {
      text = txt;
      wrap.setAttribute("data-lc-value", JSON.stringify({ text: txt, lang: lang }));
      if (!painted && !link) return;
      var pre = document.createElement("pre");
      pre.className = "lc-code-md lc-md-paint";
      var code = document.createElement("code");
      var lines = lang === "markdown" ? window.lcPaintMd(txt)
        : txt.split("\n").map(function (l) { return painted ? window.lcPaintCodeLine(l, lang) : (escapeHtml(l) || " "); });
      code.innerHTML = lines.map(function (h) { return "<span class='ln'>" + h + "</span>"; }).join("");
      pre.appendChild(code);
      if (body.parentNode === wrap) wrap.replaceChild(pre, body); else wrap.appendChild(pre);
      body = pre;
    }
    copy.addEventListener("click", function () {
      var done = function () { copy.textContent = "✓ Copied"; setTimeout(function () { copy.textContent = "📋 Copy"; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText)
        navigator.clipboard.writeText(text).then(done, function () { copy.textContent = "⚠️ Copy failed"; });
    });

    el.parentNode.insertBefore(wrap, el);
    if (link) {
      el.parentNode.removeChild(el);
      body = document.createElement("pre");
      body.textContent = "…";
      wrap.appendChild(body);
      fetchCodeFile(el, href).then(fill, function (e) {
        body.textContent = "⚠️ could not read " + href + " — " + ((e && e.message) || e);
      });
    } else {
      wrap.appendChild(el);
      fill(text);
    }
    /* the icon of the component the snippet makes, when the title brought none */
    if (!lead && lang === "markdown" && window.lcComponentIcons) {
      window.lcComponentIcons().then(function (icons) {
        var re = /^\s*\{:\s*(?:[^}]*?\s)?\.([A-Za-z][\w-]*)/gm, mm;
        while ((mm = re.exec(text))) {
          var ic = icons[mm[1].replace(/[-_]/g, "").toLowerCase()];
          if (ic) { icon.textContent = ic; return; }
        }
      });
    }
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("ul.carousel", upgradeCarousel);
    window.lcRegisterUpgrader(".highlighter-rouge.scrollable, pre.scrollable", upgradeScrollable);
    window.lcRegisterUpgrader("ul.dropdown", upgradeDropdown);
    window.lcRegisterUpgrader("p.menu, ul.menu", upgradeMenu);
    window.lcRegisterUpgrader("p.embed-page", upgradeEmbedPage);
    window.lcRegisterUpgrader("p.embed", upgradeEmbedExternal);
    /* fenced form: kramdown wraps a fence in .highlighter-rouge / pre */
    window.lcRegisterUpgrader(".highlighter-rouge.embed, pre.embed", upgradeBenchSlot);
    window.lcRegisterUpgrader("p.video", upgradeVideo);
    window.lcRegisterUpgrader(".highlighter-rouge.code, pre.code, p.code", upgradeCode);
  }

})();
</script>
