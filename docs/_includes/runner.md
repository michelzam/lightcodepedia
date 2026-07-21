{%- comment -%}
Runner (RT) — Phase A. Renders a raw-markdown source into live components using
the SAME client-side pipeline as the editor preview (marked → inline IAL →
block IAL via lcApplyIAL → lcScanElement). Behaviour parity with Jekyll, not
identical DOM. Activated by IAL {: .runner } on the /run page.

Phase A: #src=<url-to-raw-markdown> (public, no auth). Later phases add
gh:owner/repo/path (private benches via PAT) and edit/commit. The page stays
pure md + IAL (P1); all logic lives here in the engine.

The bar replaces the /run page title while a source renders: it names the
source (the working hint) and, on benches, carries the ownership convention —
course/… (teacher's, synced) gets ✍️ Make it mine; my/… (student's, never
synced) links its original and flags when that original moved on.
{%- endcomment -%}
<style>
/* the bar IS the runner's presence: it replaces the page title, names what is
   rendering (the working hint), and carries ownership + actions on benches */
.lc-run-bar { font-size: 0.85em; color: #6b7280; border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.45em 0.8em; margin-bottom: 1.1em; }
.lc-run-bar .lc-run-chip { font-family: monospace; }
.lc-run-bar a { color: #0066cc; text-decoration: none; font-weight: 600; }
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

  /* Ownership convention on benches (never collides with the vault's
     "courses/"): course/… = the teacher's material, synced from the hub;
     my/… = the student's space, never touched by a sync. */
  function paintBar(bar, st) {
    if (!bar) return;
    bar._lcState = st;
    var chip = '<span class="lc-run-chip">🔬 ' + (st.repo ? st.repo + "/" : "") + (st.path || st.src) + '</span>' +
               (st.loading ? " ⏳ rendering…" : "");
    var own = "";
    if (!st.loading && st.repo && st.path) {
      if (st.path.indexOf("course/") === 0)
        own = ' · 📦 Course page — updates arrive via Sync · <a href="#" data-lcr="mine">✍️ Make it mine</a>';
      else if (st.path.indexOf("my/") === 0)
        own = ' · ✍️ Your page · <a href="#" data-lcr="orig">📦 View original</a><span data-lcr="upd"></span>';
    }
    bar.innerHTML = chip + own;
    bar.style.display = "";
  }

  /* copy course/x → my/x with the student's own key, then open the copy.
     A 422 means the copy already exists — never overwrite their work. */
  function makeMine(st) {
    var key = edKey(); if (!key) { alert("Connect your course key first (Get started, top right)."); return; }
    var myPath = "my/" + st.path.slice(7);
    var H = { Authorization: "Bearer " + key, Accept: "application/vnd.github+json",
              "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json" };
    var api = "https://api.github.com/repos/" + st.repo + "/contents/";
    /* no-store: the render just fetched this URL with Accept raw — don't let
       a cached raw body answer this json request (FF Vary quirk) */
    fetch(api + st.path, { headers: H, cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d.content) throw new Error(d.message || "could not load the original");
        try { localStorage.setItem("lc_orig_sha:" + st.repo + "/" + myPath, d.sha); } catch (e) {}
        return fetch(api + myPath, { method: "PUT", headers: H,
          body: JSON.stringify({ message: "Make it mine: " + st.path, content: d.content.replace(/\n/g, "") }) })
          .then(function (r) {
            if (r.ok || r.status === 422) return;
            return r.json().then(function (x) { throw new Error(x.message || ("HTTP " + r.status)); });
          });
      })
      .then(function () { location.hash = "src=gh:" + st.repo + "/" + myPath; })
      .catch(function (e) { alert("Could not copy: " + e.message); });
  }

  /* on a my/ page: has the original moved since the copy was taken? The sha
     remembered at copy time is this browser's memory — absent elsewhere, the
     check stays silent rather than guessing. */
  function checkOrig(bar, st) {
    var key = edKey(); if (!key) return;
    var stored = "";
    try { stored = localStorage.getItem("lc_orig_sha:" + st.repo + "/" + st.path) || ""; } catch (e) {}
    if (!stored) return;
    fetch("https://api.github.com/repos/" + st.repo + "/contents/course/" + st.path.slice(3),
          { headers: { Authorization: "Bearer " + key, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }, cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        var slot = bar.querySelector("[data-lcr='upd']");
        if (d && d.sha && slot && d.sha !== stored)
          slot.innerHTML = ' · ⬆️ <a href="#" data-lcr="orig">the original changed since your copy</a>';
      })
      .catch(function () {});
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
    var barSt = { repo: root.dataset.lcSrcRepo, path: root.dataset.lcSrcPath, src: src, loading: true };
    if (bar) { pageTitle(bar.parentNode, true); paintBar(bar, barSt); }
    function fetchMd(headers) {
      return fetch(spec.url, headers ? { headers: headers } : undefined)
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
          status.style.display = "none";
          if (bar) {
            barSt.loading = false; paintBar(bar, barSt);
            if (barSt.path && barSt.path.indexOf("my/") === 0) checkOrig(bar, barSt);
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
          /* fine-grained tokens and out-of-scope classics answer 404 (not 403).
             Guide, don't strand: the deep link opens GitHub with the repo scope
             ALREADY ticked and the note naming THIS course's org, so a student's
             keys stay identifiable (one per class, revocable per class). */
          var keyFor = gm ? gm[1] : (rw ? rw[1] : "course");
          var keyNote = encodeURIComponent("Lightcode course key — " + keyFor);
          status.innerHTML = "🔑 Your key can’t open this course yet — course reading needs a key with the <code>repo</code> scope (and your enrollment accepted).<br>" +
            "<a href=\"https://github.com/settings/tokens/new?scopes=repo&description=" + keyNote + "\" target=\"_blank\" rel=\"noopener\" " +
            "style=\"display:inline-block;margin:0.5em 0;padding:0.4em 0.9em;border:1px solid #d0e3f5;border-radius:8px;background:#fff;color:#0066cc;font-weight:600;text-decoration:none\">" +
            "🪜 Create your course key</a> — the scope and name are pre-filled: set <b>Expiration → Custom</b> to a date past your course’s end " +
            "(a semester, not 30 days), <b>Generate token</b>, copy it, then paste it in <b>Get started</b> (top right) and reload this page.";
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
    if (bar) bar.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lcr]"); if (!a) return;
      e.preventDefault();
      var st = bar._lcState || {};
      if (a.getAttribute("data-lcr") === "orig" && st.path) location.hash = "src=gh:" + st.repo + "/course/" + st.path.slice(3);
      if (a.getAttribute("data-lcr") === "mine" && st.path) makeMine(st);
    });
    render(status, root, fixedSrc, bar);
    if (!fixedSrc) window.addEventListener("hashchange", function () { render(status, root, "", bar); });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.runner", upgradeRunner);
})();
</script>
