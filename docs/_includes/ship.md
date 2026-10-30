{%- comment -%}
🚀 Ship — deploy an app to a public bay.

    [Ship it](#)
    {: .ship app="adoption_day" files="_app_dogs.md, dogs.yaml" bay="owner/repo/bays" }

SHIP IS GENERIC (Michel, 2026-08-15: *"It could be just ship an app"*): it
copies the named files from wherever the page renders — a bench, a vault
page, any RT render — into a public bay, so the app gets a shareable life
of its own. A course assignment is one USE of it: there, the author writes
the component into the page (capability is placement) and puts a
{: .prerequisite features="true" } above it so nothing ships before the
checks run green. One job per component: prerequisite gates, feature
proves, ship copies, runner shows.

THE BAY DEFAULTS TO YOURS: with no bay= knob, ship targets <bench>-bay —
the public sister of the bench this page is paired with (lc_ed_repo). The
author names a bay explicitly only to override that. Bays are provisioned
by the TEACHER from the classroom console (⛵) with the org key — the
learner never creates one, and the org never has to allow members to
create public repositories.

WHAT A SHIP IS: the learner's own key copies the named files — from their
bench when it holds them (as a save= block reads), else from the rendered
page's repo — into the public bay, under <app>_<sha>/ — sha is the bench's
HEAD commit (the page's repo without a bench), so every ship is immutable, provenance-pinned
and enumerable by assignment. A manifest.json at the bay base records the
latest sha per app; the runner's src="ship:<app>" embeds resolve through it.

THE BAY: bay="owner/repo" or "owner/repo/base" — a public repo (or folder
in one). Public means: raw fetches need no key, links work for anyone who
holds them, and protection is unguessability (nothing lists or indexes the
folders). Anything shipped is "a stranger could read it tomorrow" tier —
the button's confirmation says so, once, honestly.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-ship {
  display: flex; align-items: center; gap: 0.9em; flex-wrap: wrap;
  border: 1px dashed #e6d3ae; border-radius: 10px; background: #fdfaf4;
  padding: 0.9em 1.2em; margin: 1.2em 0;
}
.lc-ship button {
  font-size: 1em; font-weight: 700; padding: 0.5em 1.3em;
  border-radius: 8px; border: 1px solid #b45309;
  background: #b45309; color: #fff; cursor: pointer;
}
.lc-ship button:disabled { background: #e5e7eb; border-color: #d1d5db; color: #9ca3af; cursor: default; }
.lc-ship .lc-ship-status { font-size: 0.9em; color: #6b7280; flex: 1; min-width: 200px; }
/* 🚀 Ship it… — the one-line box: what is in this copy? (the pad's 💾 Save… look) */
.lc-ship .lc-ship-commentbar { display: flex; gap: 0.5em; align-items: center; flex-basis: 100%; margin: 0.4em 0 0; font-size: 0.9em; }
.lc-ship .lc-ship-commentbar input { flex: 1; min-width: 120px; font: inherit; padding: 0.35em 0.6em; border: 1px solid #bbb; border-radius: 6px; }
.lc-ship .lc-ship-commentbar button { font: inherit; font-size: 0.9em; padding: 0.35em 0.7em; border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #444; cursor: pointer; }
.lc-ship .lc-ship-commentbar button.lc-ship-go { background: #b45309; border-color: #b45309; color: #fff; }
.lc-ship .lc-ship-commentbar button:disabled { opacity: 0.45; cursor: default; }
.lc-ship .lc-ship-note { color: #6b7280; font-style: italic; margin-left: 0.4em; }
.lc-ship .lc-ship-status a { color: #0066cc; font-weight: 600; text-decoration: none; }
.lc-ship .lc-ship-versions { flex-basis: 100%; font-size: 0.85em; color: #6b7280; border-top: 1px dashed #e6d3ae; padding-top: 0.6em; }
.lc-ship .lc-ship-versions a { color: #0066cc; font-weight: 600; text-decoration: none; font-family: ui-monospace, Menlo, monospace; }
.lc-ship .lc-ship-all summary { cursor: pointer; margin-top: 0.4em; color: #92400e; font-weight: 600; }
.lc-ship .lc-ship-all ol { margin: 0.4em 0 0 1.2em; padding: 0; line-height: 1.7; }
.lc-ship .lc-ship-all b { color: #15803d; font-size: 0.85em; }
.lc-ship .lc-ship-all li { border-radius: 6px; padding: 0 0.3em; }
.lc-ship .lc-ship-all li.lc-ship-on { background: #fef3c7; }
.lc-ship .lc-ship-pick { font: inherit; border: 0; background: none; cursor: pointer; color: #0066cc; font-weight: 600;
  font-family: ui-monospace, Menlo, monospace; padding: 0.1em 0; }
.lc-ship .lc-ship-pick span { color: #6b7280; font-weight: 400; font-family: system-ui, sans-serif; }
.lc-ship .lc-ship-replay { font: inherit; font-size: 0.95em; margin: 0.4em 0 0.1em; padding: 0.25em 0.8em; border-radius: 6px;
  border: 1px solid #e6d3ae; background: #fff; color: #92400e; cursor: pointer; font-weight: 600; }
@media print { .lc-ship { display: none; } }
</style>

<script>
(function () {
  if (window._lcShipReady) return;
  window._lcShipReady = true;

  var API = "https://api.github.com/repos/";
  /* the engine that ships a copy is stamped on it (Michel, 2026-10-25: "go
     engine stamp"): a copy from the past is drawn by today's engine, and
     the copy can say which one it was made with */
  var ENGINE = {{ site.github.build_revision | default: "local" | slice: 0, 7 | jsonify }};
  function edKey() { try { return localStorage.getItem("lc_ed_pat") || ""; } catch (e) { return ""; } }
  function hdrs(extra) {
    var h = { "X-GitHub-Api-Version": "2022-11-28" };
    var k = edKey();
    if (k) h.Authorization = "Bearer " + k;
    if (extra) for (var x in extra) h[x] = extra[x];
    return h;
  }
  function b64utf8(s) { return btoa(unescape(encodeURIComponent(s))); }

  /* bay="owner/repo" or "owner/repo/base/dir" — repo and base in one knob.
     No knob at all = the learner's own bay, <bench>-bay, derived from the
     bench pairing the join wizard stored. Convention over configuration:
     a shared course page cannot name a per-learner repo, so it names none. */
  function bayParts(bay) {
    var seg = String(bay || "").split("/").filter(Boolean);
    if (!seg.length) {
      var bench = "";
      try { bench = localStorage.getItem("lc_ed_repo") || ""; } catch (e) {}
      return { repo: bench ? bench + "-bay" : "", base: "", derived: bench };
    }
    return { repo: seg.slice(0, 2).join("/"), base: seg.slice(2).join("/") };
  }

  /* A DERIVED bay is only trustworthy inside its own org. The pairing is
     browser-global, and one browser hopping between accounts keeps the LAST
     pairing — an author-side lc_ed_repo of michelzam/lightcodepedia made
     ship derive "michelzam/lightcodepedia-bay" on a course page and fail as
     a 404 (2026-08-15). The page knows which org it renders from; a foreign
     pairing disarms with the truth instead of inventing a bay. */
  function foreignPairing(bay, ctx) {
    if (!bay.derived || !ctx.repo) return false;
    var pageOrg = ctx.repo.split("/")[0], bayOrg = bay.repo.split("/")[0];
    return pageOrg && bayOrg && pageOrg !== bayOrg;
  }
  /* the page this component rendered in — repo + folder, from the runner's
     advertisement on the render root. A built page has neither, and ship
     only makes sense on rendered course material anyway. */
  function ctxOf(el) {
    var host = el.closest("[data-lc-src-path]");
    var repoEl = el.closest("[data-lc-src-repo]");
    return {
      repo: (repoEl && repoEl.getAttribute("data-lc-src-repo")) || "",
      dir: host ? (host.getAttribute("data-lc-src-path") || "").split("/").slice(0, -1).join("/") : ""
    };
  }

  /* A collaborator grant can land as a PENDING INVITATION instead of a
     direct one (zamm-student, 2026-08-15: the bay existed, the console had
     granted push, and the PUT still answered 404 — GitHub's word for "you
     cannot write here"). The learner's key can accept its own invitations,
     so the button does it: sweep, accept the bay's, retry once. */
  function acceptBayInvite(bayRepo) {
    return fetch("https://api.github.com/user/repository_invitations",
                 { headers: hdrs(), cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (invs) {
        var inv = (invs || []).filter(function (i) {
          return i.repository && i.repository.full_name &&
                 i.repository.full_name.toLowerCase() === bayRepo.toLowerCase();
        })[0];
        if (!inv) return false;
        return fetch("https://api.github.com/user/repository_invitations/" + inv.id,
                     { method: "PATCH", headers: hdrs() })
          .then(function (r) { return r.ok; });
      })
      .catch(function () { return false; });
  }

  function escNote(t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function shipIt(box, btn, status, ctx, bay, app, files, note) {
    files = files.slice();   /* this ship's own list: the app's embeds join it below */
    note = String(note || "").trim().slice(0, 120);
    btn.disabled = true;
    status.textContent = "Shipping…";
    var folder, sha;
    /* THE LEARNER'S FILE, NOT THE COURSE'S SEED (zamm-student, 2026-10-25:
       the course renders from the vault, the page saved on page one lives in
       the bench — ship read the vault and found nothing). Each file is read
       the way a save= block reads it: the bench first (an author's pairing
       reads its __sandbox), the page's own repo as the fallback. And the
       folder is named after the bench's HEAD, so every 💾 + 🚀 is a new,
       frozen copy at a new address. */
    var bench = window.lcBench, tgt = bench && bench.target ? bench.target(box) : {};
    /* THE COURSE'S SHAPE, KEPT (Michel, 2026-10-25: "the app itself could
       have 3 tabs, each embedding different existing pages and data from
       previous modules"): an app embeds ../module_00/_app_dogs.md, so the
       shipped copy keeps the files where they sit relative to each other —
       below the folder, from their deepest common folder down. One file
       beside the page lands as before: <app>_<sha>/<file>. */
    var norm = function (p) {
      var out = [];
      ((ctx.dir ? ctx.dir + "/" : "") + p).split("/").forEach(function (g) {
        if (!g || g === ".") return; if (g === "..") out.pop(); else out.push(g);
      });
      return out;
    };
    var shaped = [];
    var shapeAll = function () {
      var segs = files.map(norm), common = segs[0].slice(0, -1);
      segs.forEach(function (sg) {
        var n = 0; while (n < common.length && n < sg.length - 1 && sg[n] === common[n]) n++;
        common = common.slice(0, n);
      });
      shaped = segs.map(function (sg) { return sg.slice(common.length).join("/"); });
    };
    /* THE APP SAYS WHAT SHIPS (Michel, 2026-10-25: "go auto-files"): every
       window the app embeds by a relative address ({: .runner src="…" })
       ships with it, so a new embed can never be left behind and break in
       the copy. files= names the app (first) and any extras. One level: the
       app's own windows. */
    var embedsOf = function (text, entry) {
      var dir = entry.split("/").slice(0, -1), found = [];
      String(text || "").replace(/\{:[^}\n]*\}/g, function (ial) {
        if (!/(^|\s)\.runner(\s|$)/.test(ial.slice(2, -1))) return ial;
        var m = /\bsrc="([^"]+)"/.exec(ial);
        var src = m ? m[1].trim() : "";
        if (!src || /^[a-z]+:/i.test(src) || src.charAt(0) === "/") return ial;
        var out = dir.slice();
        src.split("/").forEach(function (g) {
          if (!g || g === ".") return;
          if (g === ".." && out.length && out[out.length - 1] !== "..") out.pop(); else out.push(g);
        });
        found.push(out.join("/"));
        return ial;
      });
      return found;
    };
    var skipped = [], unchanged = [], entryText = null, pictures = [];
    /* A PICTURE SHIPS WITH ITS PAGE (Michel, 2026-10-29: Fern.jpg beside
       cv.md): a relative image in a shipped file is copied, bytes as they
       are, to the same place beside the copy — the bay is public, the
       bench is not, and a copy that shows a broken picture is no copy */
    var picturesOf = function (text, f, dest) {
      var dir = f.split("/").slice(0, -1), ddir = dest.split("/").slice(0, -1);
      String(text || "").replace(/!\[[^\]]*\]\(([^)\s]+)[^)]*\)/g, function (m, src) {
        src = src.trim();
        if (!src || /^[a-z]+:/i.test(src) || src.charAt(0) === "/" || src.charAt(0) === "#") return m;
        var up = dir.slice(), to = ddir.slice();
        src.split("/").forEach(function (g) {
          if (!g || g === ".") return;
          if (g === "..") { if (up.length) up.pop(); if (to.length) to.pop(); } else { up.push(g); to.push(g); }
        });
        var from = up.join("/"), into = to.join("/");
        if (!pictures.some(function (x) { return x.from === from; })) pictures.push({ from: from, into: into });
        return m;
      });
    };
    var shaRepo = (tgt && tgt.repo && !tgt.here) ? tgt.repo : ctx.repo;
    function fromBench(f) {
      if (!bench || !tgt || !tgt.repo || tgt.here) return Promise.resolve(null);
      return bench.read(f, box).then(function (got) { return got ? got.text : null; })
        .catch(function () { return null; });
    }
    /* WHAT THE PAD SHOWS: a file the page itself seeds (a pad with that
       save=) and the bench does not hold yet ships as the pad shows it —
       the lesson keeps the app once, in its pad, with no twin file to drift */
    function fromPad(f) {
      var pads = document.querySelectorAll("[data-lc-save], .mdpad[save]");
      for (var i = 0; i < pads.length; i++) {
        var sp = pads[i].getAttribute("data-lc-save") || pads[i].getAttribute("save") || "";
        if (sp !== f && sp.slice(-(f.length + 1)) !== "/" + f.replace(/^(\.\.\/)+/, "")) continue;
        /* an upgraded pad says what it shows; a fence not upgraded yet holds the seed */
        try { var v = JSON.parse(pads[i].getAttribute("data-lc-value") || "{}"); if (v && typeof v.source === "string") return v.source; } catch (e) {}
        if (!pads[i].hasAttribute("data-lc-save")) return (pads[i].querySelector("code") || pads[i]).textContent.replace(/\n+$/, "");
      }
      return null;
    }
    function fromPage(srcPath, f) {
      var padText = fromPad(f);
      if (padText != null) return Promise.resolve(padText);
      return fetch(API + ctx.repo + "/contents/" + srcPath,
                   { headers: hdrs({ Accept: "application/vnd.github.v3.raw" }), cache: "no-store" })
        .then(function (r) {
          if (!r.ok) throw new Error(tgt && tgt.stale
            ? "this browser is not paired to your bench for this class — open ⚙️ Setup (or sign in as your course account), then come back"
            : f + " is not saved in your space yet — 💾 it in its own lesson first, then ship again");
          return r.text();
        });
    }
    var entryPath = (ctx.dir ? ctx.dir + "/" : "") + files[0];
    fromBench(files[0])
      .then(function (t) { return t != null ? t : fromPage(entryPath, files[0]); })
      .then(function (t) {
        entryText = t;
        embedsOf(t, files[0]).forEach(function (f) {
          var key = norm(f).join("/");
          if (!files.some(function (g) { return norm(g).join("/") === key; })) files.push(f);
        });
        shapeAll();
        return fetch(API + shaRepo + "/commits?per_page=1", { headers: hdrs(), cache: "no-store" });
      })
      .then(function (r) { if (!r.ok) throw new Error("cannot read the source history (HTTP " + r.status + ")"); return r.json(); })
      .then(function (j) {
        sha = j[0] && j[0].sha;
        if (!sha) throw new Error("the source repo has no commits");
        folder = (bay.base ? bay.base + "/" : "") + app + "_" + sha;
        /* copy each named file: read from the source repo, write to the bay */
        return files.reduce(function (chain, f, k) {
          return chain.then(function () {
            var srcPath = (ctx.dir ? ctx.dir + "/" : "") + f;
            var dest = shaped[k];
            /* THE APP SHIPS EVEN IF A LEARNER IS LATE (Michel, 2026-10-25:
               "everyone can see their app on their phone, even if they are
               late with homework"): only the app itself (the first file) must
               be there; a piece not written yet is left out, said so, and the
               app's window on it says "not written yet" until the next ship */
            return (k === 0 && entryText != null ? Promise.resolve(entryText) : fromBench(f))
              .then(function (text) { return text != null ? text : fromPage(srcPath, f); })
              .catch(function (err) {
                if (k === 0 || (tgt && tgt.stale)) throw err;
                skipped.push(f.split("/").pop());
                return null;
              })
              .then(function (text) {
                if (text == null) return;
                picturesOf(text, f, dest);
                function put() {
                  return fetch(API + bay.repo + "/contents/" + folder + "/" + dest, {
                    method: "PUT", headers: hdrs({ "Content-Type": "application/json" }),
                    body: JSON.stringify({ message: "🚀 " + app + " @ " + sha.slice(0, 7) + (note ? " — " + note : ""),
                                           content: b64utf8(text) })
                  });
                }
                return put().then(function (r) {
                  if (r.ok) return;
                  /* 422 = THIS COPY IS ALREADY THERE (Michel, 2026-10-25: a
                     second 🚀 with no 💾 between): a copy is named after the
                     save it was made from, and it never changes. Same text:
                     nothing to do. Changed text: it needs a new save first. */
                  if (r.status === 422) {
                    return fetch(API + bay.repo + "/contents/" + folder + "/" + dest,
                                 { headers: hdrs({ Accept: "application/vnd.github.v3.raw" }), cache: "no-store" })
                      .then(function (g) { return g.ok ? g.text() : null; })
                      .then(function (was) {
                        if (was === text) { unchanged.push(dest); return; }
                        throw new Error("this copy (" + sha.slice(0, 7) + ") is already shipped, and your app changed since — 💾 save it, then ship again");
                      });
                  }
                  /* 404 on a write = no push. The grant may be a pending
                     invitation — accept it with this same key and go again */
                  if (r.status !== 404 && r.status !== 403)
                    throw new Error("the bay refused " + f + " (HTTP " + r.status + ")");
                  status.textContent = "Accepting the bay invitation…";
                  return acceptBayInvite(bay.repo).then(function (accepted) {
                    if (!accepted) throw new Error("your key cannot write " + bay.repo +
                      " (HTTP " + r.status + ") — ask your teacher to re-provision your bay");
                    return put().then(function (r2) {
                      if (!r2.ok) throw new Error("the bay still refused " + f + " (HTTP " + r2.status + ")");
                    });
                  });
                });
              });
          });
        }, Promise.resolve());
      })
      .then(function () {
        /* the pictures, after the pages: read as base64 from where the pages
           came (the bench first, the page's repo after), written as they are;
           a picture that is nowhere is left out, the page still ships */
        return pictures.reduce(function (chain, pic) {
          return chain.then(function () {
            var srcPath = (ctx.dir ? ctx.dir + "/" : "") + pic.from;
            var read = function (repo) {
              return fetch(API + repo + "/contents/" + srcPath, { headers: hdrs(), cache: "no-store" })
                .then(function (r) { return r.ok ? r.json() : null; })
                .then(function (env) { return env && env.content ? env.content.replace(/\n/g, "") : null; })
                .catch(function () { return null; });
            };
            return read(shaRepo).then(function (b64) { return b64 != null || shaRepo === ctx.repo ? b64 : read(ctx.repo); })
              .then(function (b64) {
                if (b64 == null) { skipped.push(pic.from); return; }
                return fetch(API + bay.repo + "/contents/" + folder + "/" + pic.into, {
                  method: "PUT", headers: hdrs({ "Content-Type": "application/json" }),
                  body: JSON.stringify({ message: "🖼 " + app + " @ " + sha.slice(0, 7) + " — " + pic.into.split("/").pop(), content: b64 })
                }).then(function (r) { if (!r.ok && r.status !== 422) skipped.push(pic.from); });
              });
          });
        }, Promise.resolve());
      })
      .then(function () {
        /* the manifest is the bay's ledger: latest sha per app. Read-merge-
           write, carrying the blob sha when the file already exists. */
        var mPath = (bay.base ? bay.base + "/" : "") + "manifest.json";
        return fetch(API + bay.repo + "/contents/" + mPath, { headers: hdrs(), cache: "no-store" })
          .then(function (r) { return r.ok ? r.json() : null; })
          .then(function (env) {
            var current = {};
            if (env && env.content) {
              try { current = JSON.parse(decodeURIComponent(escape(atob(env.content.replace(/\n/g, ""))))); }
              catch (e) {}
            }
            var by = "";
            try { by = (JSON.parse(localStorage.getItem("lc_gh_user") || "null") || {}).login || ""; } catch (e) {}
            /* EVERY COPY STAYS FINDABLE (Michel, 2026-10-25: "how to access all
               the versions shipped of a given app?"): the ledger keeps the
               latest per app and, under it, every earlier copy, newest first */
            var prev = current[app] || null, now = new Date().toISOString();
            var history = (prev && prev.history) ? prev.history.slice() : (prev && prev.sha ? [{ sha: prev.sha, at: prev.at, entry: prev.entry }] : []);
            history = history.filter(function (h) { return h.sha !== sha; });
            /* WHAT THE COPY HOLDS, IN TWO WORDS (Michel, 2026-10-26: "those 2
               steps … should be 2 shippings, tested in the proof"): the parts
               the app uses (its IAL classes) and the TODO_ markers still in it,
               so a proof can tell a pasted-as-is copy from a finished one */
            var parts = [], todo = (String(entryText || "").match(/TODO_/g) || []).length;
            String(entryText || "").replace(/\{:([^}\n]*)\}/g, function (m, body) {
              body.replace(/(?:^|\s)\.([A-Za-z][\w-]*)/g, function (x, c) { if (parts.indexOf(c) < 0) parts.push(c); return x; });
              return m;
            });
            /* THE SHIP'S OWN LINE (Michel, 2026-10-29: "the time machine
               shows no comments for the commits — follow the mdpad"): the
               line asked before the ship rides the copy's commit and its
               ledger entry, and the copies list shows it */
            history.unshift({ sha: sha, at: now, entry: shaped[0], engine: ENGINE, parts: parts, todo: todo, note: note || undefined });
            current[app] = { sha: sha, entry: shaped[0], files: shaped, by: by || undefined, engine: ENGINE,
                             at: now, history: history.slice(0, 50) };
            var body = { message: "📒 manifest: " + app + " @ " + sha.slice(0, 7),
                         content: b64utf8(JSON.stringify(current, null, 1)) };
            if (env && env.sha) body.sha = env.sha;
            return fetch(API + bay.repo + "/contents/" + mPath, {
              method: "PUT", headers: hdrs({ "Content-Type": "application/json" }),
              body: JSON.stringify(body)
            }).then(function (r) { if (!r.ok) throw new Error("the manifest refused the update (HTTP " + r.status + ")"); });
          });
      })
      .then(function () {
        var link = (window.lcHref ? window.lcHref("/run.html") : "/run.html") +
                   "#src=gh:" + bay.repo + "/" + folder + "/" + shaped[0];
        status.innerHTML = "";
        var strong = document.createElement("strong");
        var same = unchanged.length && unchanged.length === shaped.length - skipped.length;
        strong.textContent = same ? "✓ Already shipped, unchanged since your last 💾 · " + sha.slice(0, 7) + " · "
                                  : "🚀 Shipped · " + sha.slice(0, 7) + " · ";
        if (window.lcShipPicked) delete window.lcShipPicked[app];   /* a new ship shows the latest */
        var a = document.createElement("a");
        a.href = link; a.target = "_blank"; a.rel = "noopener";
        a.textContent = "open your deployed app";
        var note = document.createElement("span");
        note.textContent = " — public: anyone with this link can see it." +
          (skipped.length ? " Not shipped, not written yet: " + skipped.join(", ") + " — 💾 it in its own lesson, then ship again." : "");
        status.appendChild(strong); status.appendChild(a); status.appendChild(note);
        btn.disabled = false;
        showVersions(box, bay, app);
        /* the same-page ship: embeds re-render themselves on this */
        try { window.dispatchEvent(new CustomEvent("lc_shipped", { detail: { app: app } })); } catch (e) {}
      })
      .catch(function (err) {
        status.textContent = "⚠️ " + (err && err.message || "the ship did not complete");
        btn.disabled = false;
      });
  }

  /* THE SHIPPED COPIES, UNDER THE BUTTON (Michel, 2026-10-25: "the ship
     button should have a nice little panel to access them, especially the
     last one after a refresh in canvas"): the last copy, one click away, and
     the earlier ones folded under it — read from the bay's ledger. */
  function copyLink(bay, app, h) {
    return (window.lcHref ? window.lcHref("/run.html") : "/run.html") + "#src=gh:" + bay.repo + "/" +
      (bay.base ? bay.base + "/" : "") + app + "_" + h.sha + "/" + h.entry;
  }
  function when(at) {
    try { return new Date(at).toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }); }
    catch (e) { return ""; }
  }
  function showVersions(box, bay, app) {
    var mPath = (bay.base ? bay.base + "/" : "") + "manifest.json";
    fetch(API + bay.repo + "/contents/" + mPath, { headers: hdrs({ Accept: "application/vnd.github.v3.raw" }), cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (man) {
        var e = man && man[app];
        box._lcLastShipAt = e && e.at ? e.at : "";   /* the saves since then suggest the next line */
        var panel = box.querySelector(".lc-ship-versions");
        if (!e || !e.sha) { if (panel) panel.remove(); return; }
        var list = e.history && e.history.length ? e.history : [{ sha: e.sha, at: e.at, entry: e.entry }];
        /* the copies, newest first, as a proof reads them: Object._all(".lc-ship")[0]._attr("data-lc-copies") */
        box.setAttribute("data-lc-copies", JSON.stringify(list.map(function (h) {
          return { sha: h.sha, at: h.at || "", parts: h.parts || [], todo: h.todo == null ? -1 : h.todo };
        })));
        if (!panel) { panel = document.createElement("div"); panel.className = "lc-ship-versions"; box.appendChild(panel); }
        var wasOpen = !!(panel.querySelector(".lc-ship-all") || {}).open;
        /* THE COPIES AS A VERSION PANE (Michel, 2026-10-25: "show the list of
           shippings as in the version pane of a mdpad and refresh them when
           selected, including with the time machine"): picking a copy shows
           it in this page's window and square; 🆕 goes back to the latest;
           🎞 plays them oldest to newest */
        var picked = (window.lcShipPicked || {})[app];
        var row = function (h, i) {
          var on = picked ? picked.sha === h.sha : i === 0;
          return "<li class='" + (on ? "lc-ship-on" : "") + "'><button type='button' class='lc-ship-pick' data-i='" + i + "'>" +
            (i === 0 ? "🆕 " : "📦 ") + h.sha.slice(0, 7) + " <span>" + when(h.at) + "</span>" +
            (i === 0 ? " <b>latest</b>" : "") + (h.note ? " <em class='lc-ship-note'>" + escNote(h.note) + "</em>" : "") + "</button> <a href='" + copyLink(bay, app, h) +
            "' target='_blank' rel='noopener' title='open this copy on its own'>↗</a></li>";
        };
        /* 🎬 THE STAGE DOOR (Michel, 2026-10-30): stage="my_app.md" — the
           latest copy opens in its own tab with the camera on it, and the
           recording's link lands in that file of the learner's bench */
        var stageHtml = "";
        if (box._lcStage) {
          var intoPath = "";
          try { intoPath = window.lcBench && window.lcBench.resolve ? "/" + String(window.lcBench.resolve(box._lcStage, box)).replace(/^\/+/, "") : ""; } catch (e) { intoPath = ""; }
          var link = copyLink(bay, app, list[0]), cut = link.indexOf("#");
          var stageHref = link.slice(0, cut) + "?stage=1" + (intoPath ? "&into=" + encodeURIComponent(intoPath) : "") + link.slice(cut);
          stageHtml = " · <a class='lc-ship-stage' href='" + stageHref + "' target='_blank' rel='noopener' title='your shipped app, in its own tab, with the camera on it'>🎬 Step on stage ↗</a>";
        }
        panel.innerHTML = "<div class='lc-ship-last'>Last shipped " + when(list[0].at) + " · " +
          "<a href='" + copyLink(bay, app, list[0]) + "' target='_blank' rel='noopener'>open " + list[0].sha.slice(0, 7) + " ↗</a>" + stageHtml + "</div>" +
          (list.length > 1 ? "<details class='lc-ship-all'" + (wasOpen ? " open" : "") + "><summary>🗂 All " + list.length + " copies</summary>" +
            "<button type='button' class='lc-ship-replay'>🎞 Time machine</button><ol>" +
            list.map(row).join("") + "</ol></details>" : "");
        var pick = function (i) {
          window.lcShipPicked = window.lcShipPicked || {};
          if (i === 0) delete window.lcShipPicked[app];
          else window.lcShipPicked[app] = { sha: list[i].sha, entry: list[i].entry };
          [].forEach.call(panel.querySelectorAll(".lc-ship-all li"), function (li, k) { li.classList.toggle("lc-ship-on", k === i); });
          try { window.dispatchEvent(new CustomEvent("lc_ship_pick", { detail: { app: app, sha: list[i].sha } })); } catch (er) {}
        };
        [].forEach.call(panel.querySelectorAll(".lc-ship-pick"), function (b) {
          b.addEventListener("click", function () { stopReplay(); pick(+b.getAttribute("data-i")); });
        });
        var timer = null;
        var stopReplay = function () { if (timer) { clearInterval(timer); timer = null; } };
        var rb = panel.querySelector(".lc-ship-replay");
        if (rb) rb.addEventListener("click", function () {
          stopReplay();
          var i = list.length - 1;
          pick(i);
          timer = setInterval(function () {
            i -= 1;
            if (i < 0) { stopReplay(); return; }
            pick(i);
            if (i === 0) stopReplay();
          }, +(box.getAttribute("data-replay") || 2500));
        });
      }).catch(function () {});
  }

  function upgradeShip(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var app = (el.getAttribute("app") || "").trim();
    var files = (el.getAttribute("files") || "").split(",")
      .map(function (s) { return s.trim(); }).filter(Boolean);
    var bay = bayParts(el.getAttribute("bay"));
    var ctx = ctxOf(el);

    var box = document.createElement("div");
    box.className = "lc-ship";
    if (el.id) { box.id = el.id; box.setAttribute("data-lc-id", el.id); }
    var btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "🚀 Ship it";
    var status = document.createElement("span");
    status.className = "lc-ship-status";
    box.appendChild(btn);
    box.appendChild(status);
    el.parentNode.replaceChild(box, el);

    /* disarmed states name their reason — a dead control that explains
       itself is a course tool; one that doesn't is a bug report */
    var why = "";
    if (!app || !files.length) why = "The author must set app= and files= before anyone can ship.";
    else if (!bay.repo) why = "No bay to ship to yet — your teacher opens shipping by provisioning bays, or the author sets bay= explicitly.";
    else if (!ctx.repo) why = "Open this page through the runner (a rendered page — your bench, a course, a demo) to ship.";
    else if (foreignPairing(bay, ctx)) why = "This browser is paired to " + bay.derived +
      ", which is not part of this course's space — sign in as your course account and pass through the join wizard once, then come back.";
    else if (!edKey()) why = "Shipping uses your own key — add it via 🔑 Get started, then come back.";
    if (why) { btn.disabled = true; status.textContent = why; return; }

    status.textContent = "Ships " + files.join(", ") + " to " + bay.repo + " — publicly.";
    /* comment="true": 🚀 Ship it… asks one line first — what is in this
       copy — the way the pad's 💾 Save… does; Enter ships, Escape forgets */
    var askNote = el.getAttribute("comment") === "true";
    if (askNote) btn.textContent = "🚀 Ship it…";
    btn.addEventListener("click", function () {
      if (!askNote) return shipIt(box, btn, status, ctx, bay, app, files);
      if (box.querySelector(".lc-ship-commentbar")) return;
      var form = document.createElement("form");
      form.className = "lc-ship-commentbar"; form.setAttribute("autocomplete", "off");
      form.addEventListener("submit", function (e) { e.preventDefault(); });
      var inp = document.createElement("input");
      inp.type = "text"; inp.maxLength = 120; inp.name = "lc-ship-diary";
      inp.setAttribute("autocomplete", "off"); inp.setAttribute("data-lpignore", "true"); inp.setAttribute("data-1p-ignore", "true");
      inp.placeholder = "What is in this copy? — one line, e.g. the tour pasted";
      inp.setAttribute("aria-label", "What is in this copy?");
      var go = document.createElement("button"); go.type = "button"; go.className = "lc-ship-go"; go.textContent = "🚀 Ship"; go.disabled = true;
      var no = document.createElement("button"); no.type = "button"; no.className = "lc-ship-cancel"; no.textContent = "Cancel";
      form.appendChild(inp); form.appendChild(go); form.appendChild(no);
      box.insertBefore(form, status.nextSibling);
      var close = function () { if (form.parentNode) form.parentNode.removeChild(form); };
      var ship = function () { var n = inp.value.trim(); if (!n) return; close(); shipIt(box, btn, status, ctx, bay, app, files, n); };
      inp.addEventListener("input", function () { go.disabled = !inp.value.trim(); });
      inp.addEventListener("keydown", function (e) {
        if (e.key === "Enter") { e.preventDefault(); ship(); }
        if (e.key === "Escape") { e.preventDefault(); close(); }
      });
      go.addEventListener("click", ship); no.addEventListener("click", close);
      inp.focus();
      /* THE SAVES SUGGEST THE LINE (Michel, 2026-10-29: "I wish the comments
         of the saved versions could contribute too — suggested as default
         values"): the app's bench commits since the last ship, their lines
         joined with a middle dot, offered in the box; typing replaces it */
      try {
        var bench = window.lcBench, tg = bench && bench.target ? bench.target(box) : null;
        if (tg && tg.repo && tg.pat && !tg.here) {
          var path = bench.resolve(files[0], box), since = box._lcLastShipAt || "";
          fetch(API + tg.repo + "/commits?path=" + encodeURIComponent(path) + "&per_page=20" + (since ? "&since=" + encodeURIComponent(since) : ""),
                { headers: { Authorization: "Bearer " + tg.pat, "X-GitHub-Api-Version": "2022-11-28" }, cache: "no-store" })
            .then(function (r) { return r.ok ? r.json() : []; })
            .then(function (list) {
              if (inp.value.trim() || !form.parentNode) return;
              var lines = (list || []).map(function (c) { return String(c.commit && c.commit.message || "").split("\n")[0].replace(/^✍️\s*/, "").trim(); })
                .filter(function (m) { return m && m.indexOf(String(window.lcStarterMsg || "\u0000")) !== 0; });
              var seen = {}; lines = lines.filter(function (m) { if (seen[m]) return false; seen[m] = 1; return true; }).reverse();
              if (!lines.length) return;
              inp.value = lines.join(" · ").slice(0, 120); go.disabled = false; inp.select();
            }).catch(function () {});
        }
      } catch (x) {}
    });
    box._lcStage = (el.getAttribute("stage") || "").trim();   /* the file the stage's recording lands in */
    var rp = parseFloat(el.getAttribute("replay") || "");   /* the time machine's seconds per copy */
    if (rp > 0) box.setAttribute("data-replay", String(Math.round(rp * 1000)));
    showVersions(box, bay, app);
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.ship", upgradeShip);
})();
</script>
