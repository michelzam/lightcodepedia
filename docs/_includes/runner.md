{%- comment -%}
Runner (RT) — Phase A. Renders a raw-markdown source into live components using
the SAME client-side pipeline as the editor preview (marked → inline IAL →
block IAL via lcApplyIAL → lcScanElement). Behaviour parity with Jekyll, not
identical DOM. Activated by IAL {: .runner } on the /run page.

Phase A: #src=<url-to-raw-markdown> (public, no auth). Later phases add
gh:owner/repo/path (private benches via PAT) and edit/commit. The page stays
pure md + IAL (P1); all logic lives here in the engine.
{%- endcomment -%}
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

  /* src comes from the IAL attribute (embedded examples) or the page hash
     (the /run page). Attribute wins, so a component page can host a live demo. */
  function render(status, root, fixedSrc) {
    var src = fixedSrc || hashSrc();
    if (!src) { status.style.display = ""; status.textContent = "No source. Open with #src=<url to markdown>."; root.innerHTML = ""; return; }
    status.style.display = ""; status.textContent = "Loading…"; root.innerHTML = "";
    var spec = resolveSrc(src);
    /* Advertise the source on the render root so editors (xray) commit to the
       RENDERED file, not the /run page. gh:/raw carry their repo; a same-origin
       path implies the connected repo (docs/ is the Pages source root). */
    var gm = /^gh:([^\/]+)\/([^\/]+)\/(.+?)(?:@[^@]+)?$/.exec(src),
        rw = /^https?:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/[^\/]+\/(.+)$/.exec(src);
    root.dataset.lcSrcRepo = gm ? gm[1] + "/" + gm[2] : (rw ? rw[1] + "/" + rw[2] : "");
    root.dataset.lcSrcPath = gm ? gm[3] : (rw ? rw[3] : (src.charAt(0) === "/" ? "docs" + src : ""));
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
        });
      })
      .catch(function (err) {
        status.style.display = "";
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
    wrap.innerHTML = '<div class="lc-run-status" style="color:#6b7280;font-size:0.9em">Loading…</div>' +
                     '<div class="lc-run markdown-body"' + idAttr + '></div>';
    el.parentNode.replaceChild(wrap, el);
    var status = wrap.querySelector(".lc-run-status");
    var root = wrap.querySelector(".lc-run");
    render(status, root, fixedSrc);
    if (!fixedSrc) window.addEventListener("hashchange", function () { render(status, root, ""); });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.runner", upgradeRunner);
})();
</script>
