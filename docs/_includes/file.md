{%- comment -%}
📄 file.md — a fence is a file. A code block with {: .file name="x.csv" }
keeps its text under that name; a runner's open("x.csv") reads it like a
file (pyrun.md's bootstrap). A .dataset block answers to "<id>.csv" and
"<id>.json" too. Reading only: a page is not a disk. Michel, 2026-10-28:
"make/fake an open file from the micropython script who will in fact embed
a csv file containing the entertainer song, then play the song".
{%- endcomment -%}
<style>
.lc-file { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-file-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; }
.lc-file pre { margin: 0; border: 0; border-radius: 0; max-height: 14em; overflow: auto; }
.lc-file[hidden] { display: none; }
</style>
<script>
(function () {
  if (window.lcFileText) return;
  window.lcFiles = window.lcFiles || {};
  function csvOf(rows) {
    if (!rows || !rows.length) return "";
    var keys = Object.keys(rows[0]).filter(function (k) { return k.charAt(0) !== "_"; });
    var cell = function (v) { v = v == null ? "" : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    return keys.join(",") + "\n" + rows.map(function (r) { return keys.map(function (k) { return cell(r[k]); }).join(","); }).join("\n") + "\n";
  }
  /* the text behind a name, or null: a .file fence first, then a dataset's door */
  window.lcFileText = function (name) {
    name = String(name || "");
    if (Object.prototype.hasOwnProperty.call(window.lcFiles, name)) return window.lcFiles[name];
    var m = /^([A-Za-z_][\w-]*)\.(csv|json)$/.exec(name), rows = m && window.lcDatasets ? window.lcDatasets[m[1]] : null;
    if (!rows) return null;
    return m[2] === "json" ? JSON.stringify(rows, null, 2) : csvOf(rows);
  };
  function upgradeFile(el) {
    if (el.dataset.lcFileDone) return; el.dataset.lcFileDone = "1";
    var name = el.getAttribute("name") || el.id || "";
    if (!name) return;
    var code = el.querySelector("code") || el;
    var text = code.textContent.replace(/\n+$/, "") + "\n";
    window.lcFiles[name] = text;
    el.classList.add("lc-file");
    el.setAttribute("data-lc-file", name);
    var t = document.createElement("div"); t.className = "lc-file-title"; t.textContent = "📄 " + name;
    el.insertBefore(t, el.firstChild);
    if (el.hasAttribute("hidden") || el.getAttribute("folded") === "true") el.hidden = true;
  }
  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader(".highlighter-rouge.file, pre.file", upgradeFile);
  else document.querySelectorAll(".highlighter-rouge.file, pre.file").forEach(upgradeFile);
})();
</script>
