<!--
Share unlisted — one row in the account menu, lab builds only, key
connected. The owner copies the current page (and the files it references relatively)
into docs/share/<id>/ of the lab, with their own key. The lab's Pages build
renders it like any lab page — unlisted, noindex — at
https://share.lightcodepedia.org/share/<id>/<name>. The id is random once
and then belongs to the page: a share again refreshes the same folder, so
the link never changes; Unshare deletes the folder. The dialog opens on the STATE (not shared / shared: link, iframe, QR) and
acts on a press: Share · Refresh · Unshare. A page under /share/<id>/ wears
a reader's chrome — brand and menu to lightcodepedia.org, no Get started,
no account, no modes. Existing shares are found by
listing docs/share/ through the API (front matter lc_share_of) — no index
file, nothing public to leak. share/ sits in the publish excludes, so
nothing under it ever reaches pedia (Michel, 2026-09-20).
-->
<style>
.lc-share-ov{position:fixed;inset:0;z-index:2147483645;background:rgba(10,10,20,.55);display:flex;align-items:center;justify-content:center;padding:20px}
.lc-share{background:#fff;border-radius:14px;box-shadow:0 20px 60px rgba(0,0,0,.35);max-width:520px;width:100%;padding:18px 20px 20px;position:relative;font-size:.95em}
.lc-share h3{margin:0 0 .5em;font-size:1.1em}
.lc-share .lc-share-x{position:absolute;top:8px;right:10px;background:none;border:none;font-size:1.3em;color:#888;cursor:pointer}
.lc-share label{display:block;font-weight:600;margin:.9em 0 .3em}
.lc-share .lc-share-row{display:flex;gap:6px}
.lc-share input,.lc-share textarea{flex:1;font:inherit;font-size:.85em;padding:6px 8px;border:1px solid #ccc;border-radius:7px;box-sizing:border-box;width:100%}
.lc-share textarea{font-family:ui-monospace,Menlo,monospace;height:4.4em;resize:vertical}
.lc-share button.copy{padding:6px 12px;border:none;border-radius:7px;background:#0066cc;color:#fff;cursor:pointer;font:inherit;font-size:.85em;font-weight:600}
.lc-share .lc-share-qr{display:flex;justify-content:center;padding:8px 0}
.lc-share .lc-share-status{font-size:.85em;color:#555;min-height:1.2em;margin-top:.8em}
.lc-share .lc-share-acts{display:flex;gap:8px;margin-top:.9em}
.lc-share .lc-share-acts button{padding:.5em 1em;border:none;border-radius:7px;cursor:pointer;font:inherit;font-size:.9em;font-weight:600}
.lc-share .lc-share-go{background:#2e7d32;color:#fff}
.lc-share .lc-share-off{background:#fff;color:#c00;border:1px solid #f0caca!important}
.lc-share .lc-share-go,.lc-share .lc-share-refresh{background:#2e7d32;color:#fff}
/* a shared page wears a reader's chrome: no doors into the lab */
html.lc-shared #lc-start-pill,html.lc-shared #lc-user-pill,html.lc-shared .lc-slides-fab,html.lc-shared .lc-edit-fab{display:none!important}
</style>
<script>
(function () {
  if (window._lcShareReady) return;
  window._lcShareReady = true;
  var LAB = {{ site.github.repository_nwo | default: "" | jsonify }};
  var IS_LAB = {{ site.github.repository_name | default: "" | jsonify }} === "lightcodelab";
  var API = "https://api.github.com/repos/";

  function key() { try { return localStorage.getItem("lc_ed_pat") || ""; } catch (e) { return ""; } }
  function hdrs() { return { "Authorization": "token " + key(), "Accept": "application/vnd.github+json", "Content-Type": "application/json" }; }
  function b64(s) { return btoa(unescape(encodeURIComponent(s))); }
  function unb64(s) { return decodeURIComponent(escape(atob(String(s || "").replace(/\s/g, "")))); }
  function hex(n) {
    var a = new Uint8Array(n); (window.crypto || window.msCrypto).getRandomValues(a);
    return Array.prototype.map.call(a, function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
  }
  /* the page being shared: a runner render says where it came from, a site
     page is its own docs/*.md (the rule 📌 Keep and the Short's embed use) */
  function source() {
    var rt = document.querySelector("#lc-run[data-lc-src-path]");
    if (rt && rt.dataset.lcSrcRepo && rt.dataset.lcSrcPath) return { repo: rt.dataset.lcSrcRepo, path: rt.dataset.lcSrcPath };
    var p = (window.lcPagePath ? window.lcPagePath() : location.pathname).replace(/\.html?$/, "").replace(/\/+$/, "");
    return { repo: LAB, path: (!p || p === "/") ? "docs/index.md" : "docs" + (p.charAt(0) === "/" ? p : "/" + p) + ".md" };
  }
  function getFile(repo, path) {
    return fetch(API + repo + "/contents/" + path, { headers: hdrs() })
      .then(function (r) {
        if (r.status === 404 && !/\/index\.md$/.test(path)) return getFile(repo, path.replace(/\.md$/, "/index.md"));
        /* a private repo the key was not granted answers 404, not 403 —
           say what to do, not the status (Michel, 2026-09-20) */
        if (r.status === 404 || r.status === 403)
          throw new Error("Your key cannot see " + repo + ". On GitHub, open the key's settings, add " + repo +
                          " to its repository access with Contents read and write, then paste the key again.");
        if (!r.ok) throw new Error("HTTP " + r.status + " reading " + path);
        return r.json();
      });
  }
  function putFile(path, content, sha, message) {
    var body = { message: message, content: content };
    if (sha) body.sha = sha;
    return fetch(API + LAB + "/contents/" + path, { method: "PUT", headers: hdrs(), body: JSON.stringify(body) })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status + " committing " + path); return r.json(); });
  }
  /* the folder that already holds this page's share, if any */
  function findShare(srcPath) {
    return fetch(API + LAB + "/contents/docs/share", { headers: hdrs() })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (dirs) {
        dirs = (dirs || []).filter(function (d) { return d.type === "dir"; });
        var chain = Promise.resolve(null);
        dirs.forEach(function (d) {
          chain = chain.then(function (hit) {
            if (hit) return hit;
            return fetch(API + LAB + "/contents/" + d.path, { headers: hdrs() })
              .then(function (r) { return r.ok ? r.json() : []; })
              .then(function (files) {
                var md = (files || []).filter(function (f) { return /\.md$/.test(f.name); });
                var c2 = Promise.resolve(null);
                md.forEach(function (f) {
                  c2 = c2.then(function (h2) {
                    if (h2) return h2;
                    return getFile(LAB, f.path).then(function (data) {
                      var m = /^---[\s\S]*?\nlc_share_of:\s*(\S+)/.exec(unb64(data.content));
                      return (m && m[1] === srcPath) ? { id: d.name, name: f.name, files: files } : null;
                    }).catch(function () { return null; });
                  });
                });
                return c2;
              });
          });
        });
        return chain;
      });
  }
  /* relative references — ](x.md), ](img.png), ](data.csv) — travel with the page */
  function relatives(md) {
    var out = {}, re = /\]\(([^)\s#?]+)(?:[#?][^)]*)?\)/g, m;
    while ((m = re.exec(md)) !== null) {
      var p = m[1];
      if (/^(https?:|\/|mailto:|data:|gh:)/.test(p) || p.indexOf("..") === 0) continue;
      out[p] = true;
    }
    return Object.keys(out);
  }
  function withFrontMatter(md, srcPath) {
    var fm = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(md);
    if (fm) {
      var body = fm[1].replace(/^lc_share_of:.*$/m, "").replace(/\n+$/, "");
      return "---\n" + (body ? body + "\n" : "") + "lc_share_of: " + srcPath + "\n---\n" + md.slice(fm[0].length);
    }
    return "---\nlc_share_of: " + srcPath + "\n---\n" + md;
  }
  function shareUrl(id, name) {
    return location.origin + (window.lcResolveUrl ? window.lcResolveUrl("/share/" + id + "/" + name.replace(/\.md$/, "")) : "/share/" + id + "/" + name.replace(/\.md$/, ""));
  }

  /* share(): copy (or refresh) → { id, name, url } */
  function share(status) {
    var src = source(), srcDir = src.path.split("/").slice(0, -1).join("/");
    var name = src.path.split("/").pop();
    if (name === "index.md") name = (srcDir.split("/").pop() || "index") + ".md";
    status("Looking for an earlier share…");
    return findShare(src.path).then(function (hit) {
      var id = hit ? hit.id : hex(6);
      var existing = {};
      (hit ? hit.files : []).forEach(function (f) { existing[f.name] = f.sha; });
      status(hit ? "Refreshing the share…" : "Sharing…");
      return getFile(src.repo, src.path).then(function (data) {
        var md = unb64(data.content);
        var page = withFrontMatter(md, src.path);
        var when = new Date().toISOString().slice(0, 10);
        return putFile("docs/share/" + id + "/" + name, b64(page), existing[name], "share: " + name + " — " + when)
          .then(function () {
            var rels = relatives(md), chain = Promise.resolve(), n = 0;
            rels.forEach(function (rel) {
              chain = chain.then(function () {
                var from = (srcDir ? srcDir + "/" : "") + rel;
                return getFile(src.repo, from).then(function (d) {
                  n++;
                  return putFile("docs/share/" + id + "/" + rel, String(d.content || "").replace(/\s/g, ""), existing[rel.split("/").pop()], "share: " + rel + " travels with " + name);
                }).catch(function () { /* a reference that is not a file of ours — leave it */ });
              });
            });
            return chain.then(function () { return { id: id, name: name, url: shareUrl(id, name), rels: n, refreshed: !!hit }; });
          });
      });
    });
  }
  function unshare(status) {
    var src = source();
    status("Looking for the share…");
    return findShare(src.path).then(function (hit) {
      if (!hit) return false;
      status("Unsharing…");
      var chain = Promise.resolve();
      hit.files.forEach(function (f) {
        chain = chain.then(function () {
          return fetch(API + LAB + "/contents/" + f.path, { method: "DELETE", headers: hdrs(),
            body: JSON.stringify({ message: "unshare: " + f.name, sha: f.sha }) });
        });
      });
      return chain.then(function () { return true; });
    });
  }

  /* ── a shared page (under /share/<id>/) reads as pedia: brand and menu
     point at lightcodepedia.org, no Get started, no account, no modes ── */
  var SHARED = /\/share\/[0-9a-f]{12}\//.test(location.pathname);
  function readerChrome() {
    if (!SHARED) return;
    document.documentElement.classList.add("lc-shared");
    var brand = document.querySelector("#lc-topbar .lc-brand");
    if (brand) { brand.href = "https://lightcodepedia.org/"; brand.textContent = "💡 Lightcodepedia"; }
    document.querySelectorAll("#lc-topbar .lc-links a[href^='/']").forEach(function (a) {
      a.href = "https://lightcodepedia.org" + a.getAttribute("href");
    });
  }

  /* ── the dialog is a switch: it opens on the STATE, and acts on a press ── */
  function dialog() {
    if (document.querySelector(".lc-share-ov")) return;
    var ov = document.createElement("div");
    ov.className = "lc-share-ov";
    ov.innerHTML = [
      '<div class="lc-share" role="dialog" aria-label="Share unlisted">',
      '  <button class="lc-share-x" title="Close">✕</button>',
      '  <h3>🔗 Share unlisted</h3>',
      '  <div class="lc-share-status" aria-live="polite">Looking…</div>',
      '  <div class="lc-share-body" style="display:none">',
      '    <label>Link</label><div class="lc-share-row"><input class="lc-share-url" readonly aria-label="Share link"><button class="copy" data-for="lc-share-url">📋 Copy</button></div>',
      '    <label>Iframe</label><div class="lc-share-row"><textarea class="lc-share-iframe" readonly aria-label="Iframe snippet"></textarea><button class="copy" data-for="lc-share-iframe">📋 Copy</button></div>',
      '    <label>QR code</label><div class="lc-share-qr"></div>',
      '  </div>',
      '  <div class="lc-share-acts">',
      '    <button class="lc-share-go" style="display:none">🔗 Share</button>',
      '    <button class="lc-share-refresh" style="display:none">🔄 Refresh</button>',
      '    <button class="lc-share-off" style="display:none">🗑 Unshare</button>',
      '  </div>',
      '</div>'
    ].join("");
    document.body.appendChild(ov);
    var st = ov.querySelector(".lc-share-status"), body = ov.querySelector(".lc-share-body");
    var goB = ov.querySelector(".lc-share-go"), refB = ov.querySelector(".lc-share-refresh"), offB = ov.querySelector(".lc-share-off");
    function status(t) { st.textContent = t; }
    function close() { ov.remove(); }
    function buttons(shared) {
      goB.style.display = shared ? "none" : "";
      refB.style.display = offB.style.display = shared ? "" : "none";
    }
    function fill(url) {
      ov.querySelector(".lc-share-url").value = url;
      ov.querySelector(".lc-share-iframe").value = '<iframe src="' + url + '" width="100%" height="720" style="border:0" loading="lazy" allow="display-capture; microphone; camera"></iframe>';
      if (window.lcQrInto) window.lcQrInto(ov.querySelector(".lc-share-qr"), url, 180);
      body.style.display = "";
    }
    function showState() {
      body.style.display = "none"; buttons(false);
      goB.disabled = refB.disabled = offB.disabled = true;
      return findShare(source().path).then(function (hit) {
        goB.disabled = refB.disabled = offB.disabled = false;
        if (hit) { fill(shareUrl(hit.id, hit.name)); buttons(true); status("✅ Shared — same link every time; Refresh after an edit."); }
        else { buttons(false); status("Not shared. Share copies this page to an unlisted address."); }
      }).catch(function (e) { status("❌ " + e.message); });
    }
    ov.querySelector(".lc-share-x").addEventListener("click", close);
    ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
    ov.querySelectorAll("button.copy").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = ov.querySelector("." + b.getAttribute("data-for"));
        if (navigator.clipboard) navigator.clipboard.writeText(f.value);
        else { f.select(); document.execCommand("copy"); }
        b.textContent = "✅ Copied"; setTimeout(function () { b.textContent = "📋 Copy"; }, 1500);
      });
    });
    function doShare() {
      goB.disabled = refB.disabled = offB.disabled = true;
      share(status).then(function (r) {
        fill(r.url); buttons(true);
        goB.disabled = refB.disabled = offB.disabled = false;
        status((r.refreshed ? "✅ Refreshed" : "✅ Shared") + (r.rels ? " with " + r.rels + " file" + (r.rels > 1 ? "s" : "") : "") + " — live in about a minute, same link every time.");
      }).catch(function (e) { status("❌ " + e.message); goB.disabled = refB.disabled = offB.disabled = false; });
    }
    goB.addEventListener("click", doShare);
    refB.addEventListener("click", doShare);
    offB.addEventListener("click", function () {
      body.style.display = "none";
      goB.disabled = refB.disabled = offB.disabled = true;
      unshare(status).then(function (ok) {
        buttons(false); goB.disabled = false;
        status(ok ? "✅ Unshared — the link is dead once the site rebuilds." : "Nothing was shared.");
      }).catch(function (e) { status("❌ " + e.message); offB.disabled = false; });
    });
    showState();
  }

  /* the row: lab builds, key connected — the same gate as Publish to pedia.
     No ownership probe: the lab is unlisted, and a key without push rights
     fails at the commit with the API's own answer. (An async probe kept the
     row hidden on the live lab — Michel, 2026-09-20.) */
  function wire() {
    if (!IS_LAB) return;
    var row = document.getElementById("lc-ud-share");
    if (!row || !key()) return;
    row.style.display = "";
    row.addEventListener("click", function (e) {
      e.stopPropagation();
      var u = document.getElementById("lc-user-drop"); if (u) u.classList.remove("open");
      dialog();
    });
  }
  function boot() { readerChrome(); wire(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
  window.lcShare = { open: dialog, source: source };
})();
</script>
