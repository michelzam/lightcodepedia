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
.lc-ship .lc-ship-status a { color: #0066cc; font-weight: 600; text-decoration: none; }
@media print { .lc-ship { display: none; } }
</style>

<script>
(function () {
  if (window._lcShipReady) return;
  window._lcShipReady = true;

  var API = "https://api.github.com/repos/";
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

  function shipIt(box, btn, status, ctx, bay, app, files) {
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
    var segs = files.map(norm), common = segs[0].slice(0, -1);
    segs.forEach(function (sg) {
      var n = 0; while (n < common.length && n < sg.length - 1 && sg[n] === common[n]) n++;
      common = common.slice(0, n);
    });
    var shaped = segs.map(function (sg) { return sg.slice(common.length).join("/"); });
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
    fetch(API + shaRepo + "/commits?per_page=1", { headers: hdrs(), cache: "no-store" })
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
            return fromBench(f)
              .then(function (text) { return text != null ? text : fromPage(srcPath, f); })
              .then(function (text) {
                function put() {
                  return fetch(API + bay.repo + "/contents/" + folder + "/" + dest, {
                    method: "PUT", headers: hdrs({ "Content-Type": "application/json" }),
                    body: JSON.stringify({ message: "🚀 " + app + " @ " + sha.slice(0, 7),
                                           content: b64utf8(text) })
                  });
                }
                return put().then(function (r) {
                  if (r.ok) return;
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
            current[app] = { sha: sha, entry: shaped[0], files: shaped,
                             at: new Date().toISOString() };
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
        strong.textContent = "🚀 Shipped · " + sha.slice(0, 7) + " · ";
        var a = document.createElement("a");
        a.href = link; a.target = "_blank"; a.rel = "noopener";
        a.textContent = "open your deployed app";
        var note = document.createElement("span");
        note.textContent = " — public: anyone with this link can see it.";
        status.appendChild(strong); status.appendChild(a); status.appendChild(note);
        btn.disabled = false;
        /* the same-page ship: embeds re-render themselves on this */
        try { window.dispatchEvent(new CustomEvent("lc_shipped", { detail: { app: app } })); } catch (e) {}
      })
      .catch(function (err) {
        status.textContent = "⚠️ " + (err && err.message || "the ship did not complete");
        btn.disabled = false;
      });
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
    btn.addEventListener("click", function () { shipIt(box, btn, status, ctx, bay, app, files); });
  }

  if (window.lcRegisterUpgrader) window.lcRegisterUpgrader("p.ship", upgradeShip);
})();
</script>
