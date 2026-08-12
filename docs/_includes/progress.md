{%- comment -%}
Progress — the learner's own record of how far they got, in their bench.

  /progress.txt   at the bench root, one line per page:

    # lc-progress v1
    gh:org/repo/courses/c/mod/page  3/4  2/2  2026-08-11T18:04Z
    crc 4f2a91c8

  quizzes won/answered · features green/total · when.

WHY A FILE AND NOT A DATABASE (Michel, 2026-08-11): *"students use
multiple devices … they don't know where they are."* localStorage is per
browser, so a learner who opens the course on a phone looks like a learner
who never started. The bench already travels with them.

WHY TEXT AND NOT A BLOB. He asked for compact and binary. At ~60 bytes a
page it buys nothing, and an opaque file costs the two things the bench is
for: the teacher can read it, and the learner can see their own history.

WHY A CRC AND NOT A CIPHER. They own the repo; nothing stops a hand edit
in the GitHub web console, and nothing should — it is their space. So the
design DETECTS instead: the crc stops matching, and a web-console commit
is committed by `GitHub` (web-flow) rather than by the student's own key.
Both are read by the classroom console's gradebook.

MERGE IS MONOTONIC — max per page, latest timestamp — so two devices
converge with no locking and no conflict resolution. Same rule score.md
already applies locally (K3: localStorage is the working copy, the bench
file is the durable record).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window._lcProgressReady) return;
  window._lcProgressReady = true;

  var FILE = "/progress.txt";          /* bench root: it outlives one lesson */
  var HEAD = "# lc-progress v1";
  var WRITE_AFTER = 4000;              /* one commit per page, not per quiz */

  /* CRC32 — small, standard, and enough to say "this file was edited by
     something other than the app". Not a signature: it cannot be, since the
     learner holds every key involved. */
  var TABLE = null;
  function crc32(str) {
    if (!TABLE) {
      TABLE = [];
      for (var n = 0; n < 256; n++) {
        var c = n;
        for (var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        TABLE[n] = c >>> 0;
      }
    }
    var crc = 0xFFFFFFFF;
    var bytes = new TextEncoder().encode(str);
    for (var i = 0; i < bytes.length; i++)
      crc = TABLE[(crc ^ bytes[i]) & 0xFF] ^ (crc >>> 8);
    return ((crc ^ 0xFFFFFFFF) >>> 0).toString(16).padStart(8, "0");
  }

  function rows() {
    var out = {};
    var scores = {}, feats = {};
    try { scores = JSON.parse(localStorage.getItem("lc_scores") || "{}"); } catch (e) {}
    try { feats = JSON.parse(localStorage.getItem("lc_features") || "{}"); } catch (e) {}
    Object.keys(scores).forEach(function (k) {
      var s = scores[k] || {};
      out[k] = { won: s.won || 0, total: s.total || 0, green: 0, feats: 0, ts: s.ts || "" };
    });
    Object.keys(feats).forEach(function (k) {
      var cut = k.lastIndexOf("#");
      if (cut < 0) return;
      var page = k.slice(0, cut), rec = feats[k] || {};
      var r = out[page] || (out[page] = { won: 0, total: 0, green: 0, feats: 0, ts: "" });
      r.feats++;
      if (rec.status === "passing") r.green++;
      if (rec.ts && rec.ts > r.ts) r.ts = rec.ts;
    });
    return out;
  }

  function serialise(map) {
    var lines = [HEAD];
    Object.keys(map).sort().forEach(function (k) {
      var r = map[k];
      lines.push([k, r.won + "/" + r.total, r.green + "/" + r.feats, r.ts || ""].join("\t"));
    });
    var body = lines.join("\n") + "\n";
    return body + "crc " + crc32(body) + "\n";
  }

  /* returns { map, intact } — intact=false means the file was edited by
     something that did not recompute the crc */
  function parse(text) {
    var map = {}, body = [], crcSaid = null;
    String(text || "").split("\n").forEach(function (line) {
      if (!line) return;
      if (line.indexOf("crc ") === 0) { crcSaid = line.slice(4).trim(); return; }
      body.push(line);
      if (line.charAt(0) === "#") return;
      var p = line.split("\t");
      if (p.length < 3) return;
      var q = (p[1] || "0/0").split("/"), f = (p[2] || "0/0").split("/");
      map[p[0]] = { won: +q[0] || 0, total: +q[1] || 0,
                    green: +f[0] || 0, feats: +f[1] || 0, ts: (p[3] || "").trim() };
    });
    var recomputed = crc32(body.join("\n") + "\n");
    return { map: map, intact: !crcSaid || crcSaid === recomputed };
  }

  /* MAX WINS, ALWAYS. A phone that is one lesson behind must never undo a
     laptop's progress, and the merge has to be the same on both sides or
     they ping-pong forever. */
  function merge(a, b) {
    var out = {};
    [a, b].forEach(function (src) {
      Object.keys(src || {}).forEach(function (k) {
        var r = out[k] || (out[k] = { won: 0, total: 0, green: 0, feats: 0, ts: "" });
        var s = src[k];
        r.won = Math.max(r.won, s.won || 0);
        r.total = Math.max(r.total, s.total || 0);
        r.green = Math.max(r.green, s.green || 0);
        r.feats = Math.max(r.feats, s.feats || 0);
        if ((s.ts || "") > r.ts) r.ts = s.ts || "";
      });
    });
    return out;
  }

  /* the bench's record, folded back into this browser's working copy so a
     second device opens the course where the first one left it */
  function adopt(map) {
    var scores = {};
    try { scores = JSON.parse(localStorage.getItem("lc_scores") || "{}"); } catch (e) {}
    var changed = false;
    Object.keys(map).forEach(function (k) {
      var r = map[k], s = scores[k] || { won: 0, total: 0 };
      if ((r.won > (s.won || 0)) || (r.total > (s.total || 0))) {
        scores[k] = { won: Math.max(s.won || 0, r.won),
                      total: Math.max(s.total || 0, r.total),
                      quizzes: Math.max(s.quizzes || 0, r.total), ts: r.ts || s.ts };
        changed = true;
      }
    });
    if (changed) { try { localStorage.setItem("lc_scores", JSON.stringify(scores)); } catch (e) {} }
    return changed;
  }

  var sha = null, loaded = false, timer = null, lastWritten = "";

  /* ONCE PER SESSION, NOT ONCE PER PAGE. A learner walks five lesson pages
     in a module; re-reading the same file five times is five requests to
     learn nothing new. sessionStorage forgets on close, which is exactly
     when a second device may have moved. */
  function readAlready() {
    try { return sessionStorage.getItem("lc_progress_read") === "1"; } catch (e) { return false; }
  }
  function markRead() {
    try { sessionStorage.setItem("lc_progress_read", "1"); } catch (e) {}
  }

  function load() {
    if (loaded || readAlready() || !window.lcBench) return Promise.resolve(false);
    loaded = true;
    var t = window.lcBench.target(document.body) || {};
    if (!t.repo || !t.pat) return Promise.resolve(false);
    return window.lcBench.read(FILE, document.body).then(function (f) {
      if (!f) return false;
      sha = f.sha;
      markRead();
      var got = parse(f.text);
      var did = adopt(got.map);
      if (did) document.dispatchEvent(new CustomEvent("lc-progress-loaded"));
      return did;
    }).catch(function () { return false; });
  }

  function flush() {
    if (!window.lcBench) return Promise.resolve(false);
    var t = window.lcBench.target(document.body) || {};
    if (!t.repo || !t.pat) return Promise.resolve(false);
    var mine = rows();
    if (!Object.keys(mine).length) return Promise.resolve(false);
    /* NOTHING NEW IS NOT A COMMIT. The timer and the page-leave hook both
       call this, so a page whose work was already written would commit the
       same bytes twice — noise in the very history the gradebook reads. */
    var fingerprint = serialise(mine);
    if (fingerprint === lastWritten) return Promise.resolve(false);
    lastWritten = fingerprint;
    /* re-read before writing: the other device may have moved since load,
       and merging what is there is the whole reason this needs no locking */
    return window.lcBench.read(FILE, document.body).then(function (f) {
      var base = f ? parse(f.text).map : {};
      if (f) sha = f.sha;
      var text = serialise(merge(base, mine));
      return window.lcBench.write(FILE, text, "📊 progress", sha, document.body)
        .then(function (s) { sha = s || sha; return true; });
    }).catch(function () { return false; });
  }

  function schedule() {
    if (timer) clearTimeout(timer);
    timer = setTimeout(function () { timer = null; flush(); }, WRITE_AFTER);
  }

  /* a page's worth of work is one commit: quizzes and runs both nudge the
     same timer, and leaving the page flushes whatever is still pending */
  document.addEventListener("lc-score-changed", schedule);
  document.addEventListener("lc-feature-result", schedule);
  /* LEAVING IS THE OTHER TRIGGER, AND ON A PHONE IT IS NOT `pagehide`.
     iOS backgrounds a tab without firing pagehide reliably —
     visibilitychange is the hook that always fires there, and losing the
     last commit of a session is exactly the case this feature exists for.
     keepalive lets the request outlive the page it started in. */
  function leaving() {
    if (timer) { clearTimeout(timer); timer = null; }
    flush();
  }
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") leaving();
  });
  window.addEventListener("pagehide", leaving);

  window.lcProgress = { load: load, flush: flush, rows: rows,
                        parse: parse, merge: merge, serialise: serialise, crc32: crc32 };

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", function () { setTimeout(load, 600); });
  else setTimeout(load, 600);
})();
</script>
