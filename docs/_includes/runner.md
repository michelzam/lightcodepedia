{%- comment -%}
Runner (RT) — Phase A. Renders a raw-markdown source into live components using
the SAME client-side pipeline as the editor preview (marked → inline IAL →
block IAL via lcApplyIAL → lcScanElement). Behaviour parity with Jekyll, not
identical DOM. Activated by IAL {: .runner } on the /run page.

Phase A: #src=<url-to-raw-markdown> (public, no auth). Later phases add
gh:owner/repo/path (private benches via PAT) and edit/commit. The page stays
pure md + IAL (P1); all logic lives here in the engine.

The bar replaces the /run page title while a source renders and names the
source (the working hint). Two zones, by repo: the VAULT is read-only
(repo privacy); a BENCH is the student's own repo, edited directly. New
weekly modules arrive as NEW files via Sync, so they never conflict with
files a student is already working in.
{%- endcomment -%}
<style>
/* the bar IS the runner's presence: it replaces the page title, names what is
   rendering (the working hint), and carries ownership + actions on benches */
.lc-run-bar { font-size: 0.85em; color: #6b7280; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.45em 0.8em; margin-bottom: 1.1em; }
.lc-run-bar .lc-run-chip { font-family: monospace; }
.lc-run-bar a { color: #0066cc; text-decoration: none; font-weight: 600; }
.lc-run-bar.lc-run-vault { background: #fff8e6; border-color: #f0d98a; }
.lc-run-bar .lc-run-badge { font-weight: 700; color: #8a6d00; }
</style>
<script>
(function () {
  if (window._lcRunnerReady) return;
  window._lcRunnerReady = true;

  function hashSrc() {
    var ref = "";
    try { ref = decodeURIComponent((location.hash || "").replace(/^#/, "")); }
    catch (e) { ref = (location.hash || "").replace(/^#/, ""); }
    var m = /^src=(.+)$/.exec(ref);
    return m ? m[1] : "";
  }

  /* Resolve a src to a {url, headers, gh} fetch spec.
       gh:owner/repo/path[@ref]        → GitHub API (works on PRIVATE repos with a PAT)
       raw.githubusercontent.com/…     → same, via the API, when a PAT is connected
       /path or full public URL        → plain fetch (healed for a project base)
     The Contents API + "Accept: raw" returns the file body directly, and unlike
     raw.githubusercontent it accepts the PAT in-browser (CORS-friendly). */
  function resolveSrc(src) {
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    var auth = pat ? { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw", "X-GitHub-Api-Version": "2022-11-28" } : { Accept: "application/vnd.github.v3.raw" };
    var api = function (o, r, p, ref) { return "https://api.github.com/repos/" + o + "/" + r + "/contents/" + p + (ref ? "?ref=" + encodeURIComponent(ref) : ""); };
    var m = /^gh:([^\/]+)\/([^\/]+)\/(.+?)(?:@([^@]+))?$/.exec(src);
    if (m) return { url: api(m[1], m[2], m[3], m[4]), headers: auth, gh: true };
    var rm = /^https?:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/([^\/]+)\/(.+)$/.exec(src);
    if (rm && pat) return { url: api(rm[1], rm[2], rm[4], rm[3]), headers: auth, gh: true };
    if (rm) return { url: src, headers: null, gh: true };   // public raw, no PAT
    return { url: window.lcHref ? window.lcHref(src) : src, headers: null, gh: false };
  }

  function edKey() { try { return localStorage.getItem("lc_ed_pat") || ""; } catch (e) { return ""; } }

  /* the /run page's own title gives way to the bar while a source renders */
  function pageTitle(wrap, hide) {
    var n = wrap;
    while (n && n.previousElementSibling) {
      n = n.previousElementSibling;
      if (n.tagName === "H1") { n.style.display = hide ? "none" : ""; return; }
    }
  }

  /* The bar names what is rendering. On a bench (topbar bench mode) the repo
     + filename already live up there, so the bar just shows the path; a
     plain gh: render shows the full chip. No ownership dance: the vault is
     R/O by repo privacy, the bench is the student's to edit directly. */
  function paintBar(bar, st) {
    if (!bar) return;
    bar._lcState = st;
    var tb = document.getElementById("lc-topbar");
    if (tb && st.repo && tb.dataset.benchMode === st.repo) {
      bar.style.display = "none";           // topbar carries it in bench mode
      return;
    }
    /* The vault still IS the library (readonly marking, no editing tools) —
       but it no longer says so out loud. Since work saves into the learner's
       own space from ANY page, "read-only" stopped being news the reader
       needs and became noise over every lesson (Michel 2026-08-03). */
    var vault = st.repo && /-vault$/.test(st.repo);
    bar.className = "lc-run-bar" + (vault ? " lc-run-vault" : "");
    bar.innerHTML = '<span class="lc-run-chip">🔬 ' + (st.repo ? st.repo + "/" : "") + (st.path || st.src) + '</span>' +
                    (st.loading ? " ⏳ rendering…" : "");
    bar.style.display = "";
  }

  /* Phase B, step 1: RELATIVE links in a rendered page navigate WITHIN the
     same repo through the runner — a vault module links the next module, a
     bench README its exercises, and clicking only changes the hash (fast).
     External, site-absolute (/…) and #fragment links stay untouched. */
  function healRelLinks(root, repo, path) {
    var dir = path.indexOf("/") >= 0 ? path.split("/").slice(0, -1).join("/") : "";
    var runUrl = (window.lcHref ? window.lcHref("/run.html") : "/run.html");
    root.querySelectorAll("a[href]").forEach(function (a) {
      var h = a.getAttribute("href") || "";
      if (!h || /^([a-z][a-z0-9+.-]*:|\/|#)/i.test(h)) return;
      var clean = h.split("#")[0].split("?")[0];
      if (!clean) return;
      var parts = dir ? dir.split("/") : [];
      clean.split("/").forEach(function (seg) {
        if (!seg || seg === ".") return;
        if (seg === "..") parts.pop(); else parts.push(seg);
      });
      a.setAttribute("href", runUrl + "#src=gh:" + repo + "/" + parts.join("/"));
    });
  }

  /* Phase B, step 2: IMAGES in a rendered page. An <img> cannot send the PAT
     header, and a private repo's raw URLs 404 anonymously — so RELATIVE image
     paths (the only kind that can mean "file in this repo") resolve against
     the rendered file's folder and are fetched through the contents API, then
     swapped to blob: URLs. Root-absolute and external srcs stay untouched
     (site assets, CDNs). Without a key, srcs rewrite to raw URLs — right for
     public repos, and no worse than today's 404 for private ones. */
  function healImages(root, repo, path) {
    var dir = path.indexOf("/") >= 0 ? path.split("/").slice(0, -1).join("/") : "";
    (root._lcImgUrls || []).forEach(function (u) { try { URL.revokeObjectURL(u); } catch (e) {} });
    root._lcImgUrls = [];
    var pat = edKey();
    root.querySelectorAll("img[src]").forEach(function (img) {
      var s = img.getAttribute("src") || "";
      if (!s || /^([a-z][a-z0-9+.-]*:|\/)/i.test(s)) return;   // external, data:, site-absolute
      var parts = dir ? dir.split("/") : [];
      s.split("#")[0].split("?")[0].split("/").forEach(function (seg) {
        if (!seg || seg === ".") return;
        if (seg === "..") parts.pop(); else parts.push(seg);
      });
      var full = parts.join("/");
      if (!pat) {
        img.src = "https://raw.githubusercontent.com/" + repo + "/HEAD/" + full;
        return;
      }
      fetch("https://api.github.com/repos/" + repo + "/contents/" + full,
            { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw", "X-GitHub-Api-Version": "2022-11-28" }, cache: "no-store" })
        .then(function (r) {
          if (!r.ok) throw 0;
          /* same media-type quirk as fetchMd: some proxies return the JSON
             envelope despite Accept raw — unwrap the base64 into bytes */
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
          var u = URL.createObjectURL(b);
          root._lcImgUrls.push(u);
          img.src = u;
        })
        .catch(function () {});   // leave the broken image; the alt text speaks
    });
  }

  /* src comes from the IAL attribute (embedded examples) or the page hash
     (the /run page). Attribute wins, so a component page can host a live demo. */
  function render(status, root, fixedSrc, bar) {
    var src = fixedSrc || hashSrc();
    if (!src) {
      status.style.display = ""; status.textContent = "No source. Open with #src=<url to markdown>."; root.innerHTML = "";
      if (bar) { bar.style.display = "none"; pageTitle(bar.parentNode, false); }
      return;
    }
    status.style.display = ""; status.textContent = "Loading…"; root.innerHTML = "";
    var spec = resolveSrc(src);
    /* Advertise the source on the render root so editors (xray) commit to the
       RENDERED file, not the /run page. gh:/raw carry their repo; a same-origin
       path implies the connected repo (docs/ is the Pages source root). */
    var gm = /^gh:([^\/]+)\/([^\/]+)\/(.+?)(?:@[^@]+)?$/.exec(src),
        rw = /^https?:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/[^\/]+\/(.+)$/.exec(src);
    root.dataset.lcSrcRepo = gm ? gm[1] + "/" + gm[2] : (rw ? rw[1] + "/" + rw[2] : "");
    root.dataset.lcSrcPath = gm ? gm[3] : (rw ? rw[3] : (src.charAt(0) === "/" ? "docs" + src : ""));
    /* the vault is the LIBRARY — read-only for everyone. Mark the render so
       xray refuses to edit it (a student has no write access anyway, but the
       editor must not even offer it). */
    if (/-vault$/.test(root.dataset.lcSrcRepo)) root.dataset.lcReadonly = "1";
    else delete root.dataset.lcReadonly;
    var barSt = { repo: root.dataset.lcSrcRepo, path: root.dataset.lcSrcPath, src: src, loading: true };
    if (bar) { pageTitle(bar.parentNode, true); paintBar(bar, barSt); }
    function fetchMd(headers) {
      /* no-store: api.github.com answers carry max-age=60 — after a Keep, a
         reload within the minute would render the STALE cached body ("my
         edit had no effect"). Course pages are small; always read fresh. */
      return fetch(spec.url, headers ? { headers: headers, cache: "no-store" } : { cache: "no-store" })
        .then(function (r) { if (!r.ok) throw { status: r.status, gh: spec.gh }; return r.text(); });
    }
    fetchMd(spec.headers)
      .catch(function (err) {
        /* educator fallback: the cockpit's org key may read what the author
           key can't — a student's bench lives in the org, not under the
           author's account. Students never have lc_org_pat; no-op for them. */
        var opat = ""; try { opat = localStorage.getItem("lc_org_pat") || ""; } catch (e) {}
        if (spec.gh && opat && err && (err.status === 404 || err.status === 401))
          return fetchMd({ Authorization: "Bearer " + opat, Accept: "application/vnd.github.v3.raw", "X-GitHub-Api-Version": "2022-11-28" });
        throw err;
      })
      .then(function (md) {
        /* some proxies/media-type quirks return the JSON envelope despite
           Accept raw — unwrap it (base64, UTF-8 safe) so the lesson renders */
        if (spec.gh && md.charAt(0) === "{") {
          try {
            var env = JSON.parse(md);
            if (env && env.content && env.encoding === "base64")
              md = decodeURIComponent(escape(atob(env.content.replace(/\n/g, ""))));
          } catch (e) {}
        }
        /* strip optional YAML front matter */
        if (md.indexOf("---") === 0) {
          var e = md.indexOf("\n---", 3);
          if (e >= 0) { var nl = md.indexOf("\n", e + 1); md = nl >= 0 ? md.slice(nl + 1) : ""; }
        }
        window.lcLoadMarked(function () {
          /* IAL on its own paragraph so block-IAL applies — mirrors the
             server-side normalisation the editor preview also does */
          var norm = md.replace(/([^\n])\n(\{:)/g, "$1\n\n$2").trim();
          if (window.lcClientFootnotes) norm = window.lcClientFootnotes(norm);
          root.innerHTML = (window.lcInlineIAL || function (h) { return h; })(marked.parse(norm));
          if (window.lcApplyIAL)    window.lcApplyIAL(root);
          /* Parity with the page-level scan: auto-id class-carrying fences and
             snapshot them BEFORE upgraders replace them, so xray edits inside
             an RT render read the verbatim fence source (ids auto-assigned
             when omitted — the author is never forced to set one). */
          var n = 0;
          root.querySelectorAll("pre[class], div[class^='language-']").forEach(function (el) {
            if (!el.id && el.className) el.id = "run_" + (++n);
          });
          if (window.lcSnapshotSources) window.lcSnapshotSources(root);
          if (window.lcScanElement) window.lcScanElement(root);
          if (window.lcRebase)      window.lcRebase(root);
          if (window.lcCellsRescan) window.lcCellsRescan();   // {= } cells in the rendered page
          if (spec.gh && barSt.repo) {
            healRelLinks(root, barSt.repo, barSt.path);
            healImages(root, barSt.repo, barSt.path);
          }
          /* RT slides parity: the deck census ran at page load, before this
             render existed — rebuild it around the rendered sections. Page-
             level runner only: an embedded demo must not hijack its host
             page's deck. */
          if (!fixedSrc && window.lcSlidesRebuild) window.lcSlidesRebuild(root);
          status.style.display = "none";
          if (bar) {
            /* a bench (any gh: source that isn't the course vault) flips the
               topbar into the student's safe playground */
            if (spec.gh && barSt.repo && !/-vault$/.test(barSt.repo) && window.lcBenchMode)
              window.lcBenchMode(barSt.repo, barSt.path);
            barSt.loading = false; paintBar(bar, barSt);
          }
        });
      })
      .catch(function (err) {
        status.style.display = "";
        if (bar) { barSt.loading = false; paintBar(bar, barSt); }
        var st = err && err.status;
        var hasPat = false; try { hasPat = !!localStorage.getItem("lc_ed_pat"); } catch (e) {}
        if (err && err.gh && (st === 404 || st === 401) && !hasPat)
          status.innerHTML = "🔑 This source is private. Connect a GitHub PAT (topbar “Get started”), then reload.";
        else if (err && err.gh && st === 404 && hasPat) {
          var keyFor = gm ? gm[1] : (rw ? rw[1] : "course");
          var keyNote = encodeURIComponent("Lightcode course key — " + keyFor);
          var repoName = (barSt.repo || "") + "/" + (barSt.path || "");
          var ladder = "<a href=\"https://github.com/settings/tokens/new?scopes=repo&description=" + keyNote + "\" target=\"_blank\" rel=\"noopener\" " +
            "style=\"display:inline-block;margin:0.4em 0;padding:0.4em 0.9em;border:1px solid #d0e3f5;border-radius:8px;background:#fff;color:#0066cc;font-weight:600;text-decoration:none\">🪜 Create a classic course key</a>";
          /* DIAGNOSE, don't guess: probe the key live. The message then names
             the ACTUAL cause — bad key / missing scope / fine-grained can't
             reach this repo / a real 404 — instead of a catch-all. */
          status.innerHTML = "🔎 Checking your key…";
          var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
          fetch("https://api.github.com/user", { headers: { Authorization: "Bearer " + pat, "X-GitHub-Api-Version": "2022-11-28" }, cache: "no-store" })
            .then(function (r) {
              var scopes = r.headers.get("X-OAuth-Scopes");
              return r.json().then(function (u) { return { ok: r.ok, login: u && u.login, scopes: scopes }; });
            })
            .then(function (d) {
              var fine = pat.indexOf("github_pat_") === 0;
              if (!d.ok) {
                status.innerHTML = "🔑 Your key isn’t valid anymore — generate a fresh one.<br>" + ladder + " → paste it in <b>Get started</b> (top right), reload.";
              } else if (!fine && (d.scopes || "").split(",").map(function (s) { return s.trim(); }).indexOf("repo") < 0) {
                status.innerHTML = "🔑 Signed in as <b>@" + (d.login || "?") + "</b>, but your key is missing the <code>repo</code> scope.<br>" + ladder + " → paste, reload.";
              } else if (fine) {
                status.innerHTML = "🔑 Signed in as <b>@" + (d.login || "?") + "</b> with a fine-grained token that can’t reach <code>" + repoName + "</code> (HTTP 404). Fine-grained tokens are limited to selected repos — use a <b>classic</b> key instead:<br>" + ladder + " → paste, reload.";
              } else {
                /* valid repo key + 404 on the file: is it the REPO that's
                   missing (no bench / not enrolled) or just the FILE (bench
                   behind — needs a Refresh)? Probe the repo to tell them apart. */
                var doorUrl = (window.lcHref ? window.lcHref("/courses/join") : "/courses/join") + "?go=bench&hub=" + (barSt.repo.split("/")[1] || "").replace(/-[^-]+$/, "");
                fetch("https://api.github.com/repos/" + barSt.repo, { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }, cache: "no-store" })
                  .then(function (r2) {
                    if (r2.ok)
                      status.innerHTML = "🔄 Your bench is <b>behind</b> — this page (<code>" + (barSt.path || "") + "</code>) isn’t in it yet. Open your course and <b>Refresh</b> to pull the latest:<br>" +
                        "<a href=\"" + doorUrl + "\" style=\"display:inline-block;margin:0.4em 0;padding:0.4em 0.9em;border:1px solid #d0e3f5;border-radius:8px;background:#fff;color:#0066cc;font-weight:600;text-decoration:none\">🎓 Open my course → Refresh</a>";
                    else
                      status.innerHTML = "🎒 No bench <code>" + repoName.split("/").slice(0, 2).join("/") + "</code> yet for <b>@" + (d.login || "?") + "</b> — open your course to create one:<br>" +
                        "<a href=\"" + doorUrl + "\" style=\"display:inline-block;margin:0.4em 0;padding:0.4em 0.9em;border:1px solid #d0e3f5;border-radius:8px;background:#fff;color:#0066cc;font-weight:600;text-decoration:none\">🎓 Open my course → Create bench</a>";
                  })
                  .catch(function () { status.innerHTML = "⚠️ <code>" + repoName + "</code> returns HTTP 404 — reload, or tell your teacher."; });
              }
            })
            .catch(function () {
              status.innerHTML = "🔑 Your key can’t open <code>" + repoName + "</code> (HTTP 404).<br>" + ladder + " → paste, reload.";
            });
        }
        else
          status.textContent = "⚠️ Could not load: " + (st ? "HTTP " + st : (err && err.message) || err);
      });
  }

  function upgradeRunner(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var fixedSrc = (el.getAttribute && el.getAttribute("src")) || "";
    var wrap = document.createElement("div");
    wrap.className = "lc-runner";
    /* one page-level runner (the /run page) publishes canonical ids; embedded
       demos get scoped classes so several can coexist without id clashes */
    var idAttr = fixedSrc ? "" : ' id="lc-run"';
    wrap.innerHTML = (fixedSrc ? "" : '<div class="lc-run-bar" style="display:none"></div>') +
                     '<div class="lc-run-status" style="color:#6b7280;font-size:0.9em">Loading…</div>' +
                     '<div class="lc-run markdown-body"' + idAttr + '></div>';
    el.parentNode.replaceChild(wrap, el);
    var status = wrap.querySelector(".lc-run-status");
    var root = wrap.querySelector(".lc-run");
    var bar = wrap.querySelector(".lc-run-bar");
    render(status, root, fixedSrc, bar);
    if (!fixedSrc) window.addEventListener("hashchange", function () { render(status, root, "", bar); });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.runner", upgradeRunner);
})();
</script>
