{%- comment -%}
🎵 song.md — the browser's own synthesizer, for a run block's play().
A learner's Python says play("C5", 1); this schedules one oscillator with a
short envelope at the block's queue time, so a loop of notes plays one after
the other once the run is over (MicroPython cannot wait for audio). No
library, no server: Web Audio. The block is marked with what was queued —
data-lc-played (count) and data-lc-last-note — so a page's proof and the
suite can check a song without ears. Michel, 2026-10-27: "generate sounds
in the browser from our micropython examples so we can play a song".
{%- endcomment -%}
<script>
(function () {
  if (window.lcPlayNote) return;
  var ctx = null, queues = {};
  var STEP = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
  function context() {
    if (ctx) return ctx;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    try { ctx = new AC(); } catch (e) { return null; }
    return ctx;
  }
  /* "C4", "F#5", "Bb3" → Hz; "R" or "-" → a rest (0) */
  function hz(name) {
    var m = /^([A-Ga-g])([#b]?)(-?\d)$/.exec(String(name || "").trim());
    if (!m) return 0;
    var n = STEP[m[1].toUpperCase()] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + (parseInt(m[3], 10) + 1) * 12;
    return 440 * Math.pow(2, (n - 69) / 12);
  }
  function mark(id, name) {
    var el = document.getElementById("lc-pyrun-" + id);
    if (!el) return;
    el.setAttribute("data-lc-played", String((parseInt(el.getAttribute("data-lc-played") || "0", 10) || 0) + 1));
    el.setAttribute("data-lc-last-note", String(name));
  }
  /* one note on the block's queue: it starts when the previous one ends */
  window.lcPlayNote = function (id, name, seconds, wave) {
    mark(id, name);
    var c = context();
    seconds = Math.max(0.02, Number(seconds) || 0.25);
    if (!c) return seconds;
    if (c.state === "suspended") { try { c.resume(); } catch (e) {} }
    var q = queues[id] || (queues[id] = { at: 0 });
    var start = Math.max(q.at, c.currentTime + 0.02);
    var f = hz(name);
    if (f > 0) {
      var osc = c.createOscillator(), gain = c.createGain();
      osc.type = ["sine", "square", "triangle", "sawtooth"].indexOf(wave) >= 0 ? wave : "square";
      osc.frequency.value = f;
      gain.gain.setValueAtTime(0.0001, start);
      gain.gain.exponentialRampToValueAtTime(0.18, start + 0.01);
      gain.gain.setValueAtTime(0.18, Math.max(start + 0.01, start + seconds - 0.04));
      gain.gain.exponentialRampToValueAtTime(0.0001, start + seconds);
      osc.connect(gain); gain.connect(c.destination);
      osc.start(start); osc.stop(start + seconds + 0.01);
      (q.nodes || (q.nodes = [])).push(osc);
    }
    q.at = start + seconds;
    return seconds;
  };
  /* silence the block's queue; a new run starts from now */
  window.lcPlayStop = function (id) {
    var q = queues[id];
    if (!q) return;
    (q.nodes || []).forEach(function (o) { try { o.stop(); } catch (e) {} });
    queues[id] = { at: 0 };
  };
})();
</script>
