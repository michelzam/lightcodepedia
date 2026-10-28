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
  function schedule(id, name, seconds, wave) {
    var c = context();
    if (!c) return;
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
  }
  window.lcPlayNote = function (id, name, seconds, wave) {
    if (window._lcPlayMuted === id) return 0;      /* under 🧪 Test the program runs silent */
    mark(id, name);
    seconds = Math.max(0.02, Number(seconds) || 0.25);
    var c = context();
    if (!c) return seconds;
    /* SCHEDULE AT ONCE, NEVER WAIT (2026-10-27, Mac Safari went silent when
       a note waited for resume() to settle — on Safari that promise can stay
       pending): the nodes are queued on the context's own clock whatever its
       state; the click's unlock (lcPlayWarm) is what makes it run, and a
       resume is asked again here, fire and forget. This is the first
       jingles' path, the one that rang. */
    if (c.state !== "running") { try { c.resume(); } catch (e) {} }
    schedule(id, name, seconds, wave);
    carryUntil(1.5);
    return seconds;
  };
  /* what the page's suite and a curious author may ask: the context's state and what was queued */
  window.lcPlayState = function () {
    var q = {}; Object.keys(queues).forEach(function (k) { q[k] = (queues[k].nodes || []).length; });
    return { state: ctx ? ctx.state : "none", queued: q, carrier: carrier ? (carrier.paused ? "paused" : "playing") : "none" };
  };
  /* SAFARI AND THE IPHONE PLAY NOTHING SCHEDULED OUTSIDE A GESTURE (Michel,
     2026-10-27: "why the sound doesn't ring anymore in safari or in my
     iphone?"): the notes are queued after MicroPython ran, past the click's
     own call stack. The ▶ Run click warms the context first — created and
     resumed inside the gesture — so what the program queues later plays. */
  /* THE IPHONE'S SWITCH (Michel, 2026-10-28: the Mac rings — Safari, Chrome,
     Canvas — "but still not on my iPhone"): iOS mutes Web Audio under the
     ring/silent switch, unless a media element is playing — then the page is
     in playback mode and the switch no longer applies. So the ▶ Run tap also
     plays a silent <audio> (a WAV built here, inline), looped while notes
     are queued and stopped a moment after the last one ends. */
  var carrier = null, carrierOff = null;
  /* iOS only (Michel, 2026-10-28: "do not break what works already" — the
     Mac rings as is): an iPhone or iPad, the iPad that calls itself a Mac
     included; the suite may say so to the page */
  window.lcPlayCarrier = /iP(hone|od|ad)/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  function silentWav(seconds) {
    var rate = 8000, n = Math.round(rate * seconds), b = new Uint8Array(44 + n), v = new DataView(b.buffer);
    function str(o, t) { for (var i = 0; i < t.length; i++) b[o + i] = t.charCodeAt(i); }
    str(0, "RIFF"); v.setUint32(4, 36 + n, true); str(8, "WAVE"); str(12, "fmt "); v.setUint32(16, 16, true);
    v.setUint16(20, 1, true); v.setUint16(22, 1, true); v.setUint32(24, rate, true); v.setUint32(28, rate, true);
    v.setUint16(32, 1, true); v.setUint16(34, 8, true); str(36, "data"); v.setUint32(40, n, true);
    for (var i = 0; i < n; i++) b[44 + i] = 128;
    var s = ""; for (var j = 0; j < b.length; j++) s += String.fromCharCode(b[j]);
    return "data:audio/wav;base64," + btoa(s);
  }
  function carry() {
    if (!window.lcPlayCarrier) return;
    try {
      if (!carrier) {
        carrier = document.createElement("audio");
        carrier.setAttribute("playsinline", ""); carrier.setAttribute("aria-hidden", "true");
        carrier.className = "lc-play-carrier"; carrier.loop = true; carrier.preload = "auto";
        carrier.src = silentWav(0.5);
        document.body.appendChild(carrier);
      }
      var p = carrier.play(); if (p && p.catch) p.catch(function () {});
    } catch (e) {}
    carryUntil(1.5);
  }
  /* stop the carrier `seconds` after the last queued note ends */
  function carryUntil(seconds) {
    if (!carrier) return;
    var c = ctx, last = 0;
    Object.keys(queues).forEach(function (k) { last = Math.max(last, queues[k].at || 0); });
    var wait = Math.max(seconds, c ? last - c.currentTime + 1 : seconds);
    if (carrierOff) clearTimeout(carrierOff);
    carrierOff = setTimeout(function () { try { carrier.pause(); } catch (e) {} }, wait * 1000);
  }
  window.lcPlayWarm = function () {
    carry();
    var c = context();
    if (!c) return false;
    try { c.resume(); } catch (e) {}
    /* the classic unlock: one silent sample played inside the gesture is what
       Safari (Mac and iOS) counts as "this page may make sound" */
    try {
      var b = c.createBuffer(1, 1, 22050), src = c.createBufferSource();
      src.buffer = b; src.connect(c.destination); src.start(0);
    } catch (e) {}
    return true;
  };
  /* 🔈 THE SOUND CHECK (Michel, 2026-10-27, Mac Safari and the iPhone:
     "Still no sound!" — not reproducible here, no WebKit): one note played
     inside the tap itself, no MicroPython, no queue. If this rings and the
     program does not, the fault is in what is scheduled after the gesture;
     if this is silent too, the page is not allowed to sound (tab, site or
     the phone's switch). Marks nothing: it is not the program's note. */
  window.lcPlayBeep = function (id) {
    window.lcPlayWarm();
    var c = context();
    if (!c) return "none";
    queues[id] = { at: 0 };
    schedule(id, "C5", 0.3, "square");
    return c.state;
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
