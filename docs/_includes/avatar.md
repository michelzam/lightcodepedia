{%- comment -%}
Avatar — speaking overlay character that narrates content and follows the
elements it describes. Voice: per-line audio files (studio TTS, with real
amplitude lip-sync) or the Web Speech API. Face: built-in animated SVG
(blinks, breathes, eyes track the spotlighted element, mouth follows the
audio), any Lottie animation, a Rive state machine, or a recorded video.

Usage:
  ```yaml
  name: "Prof. LC"
  voice: en-US
  rate: 0.95
  script:
    - "Hello! Let's explore Python objects together."
    - at: "#dog_grid_tuto"
      say: "This grid is editable — click a cell."
    - at: "#how_it_works"
      say: "Here is how everything fits."
      audio: /assets/audio/prof_03.mp3
  ```
  {: .avatar #prof }

  [▶ Play](#)
  {: .avatar-trigger target="prof" label-stop="⏹ Stop" }

Script lines are strings (the avatar wanders) or objects:
  at:    CSS selector — scroll there, park beside it, spotlight it
  say:   the line (spoken + shown in the bubble)
  audio: URL of a pre-generated audio file — plays instead of browser TTS,
         and the mouth follows the actual waveform
  input: drive the Rive character's state machine for this line —
         "bark" fires the trigger named bark, { run: true, speed: 7 }
         sets boolean/number inputs (also available inside cues)

Attributes on .avatar:
  id        — referenced by .avatar-trigger's target=""
  path      — left | center | right | wander (fallback for untargeted lines)
  voice     — BCP-47 tag; the best-quality matching browser voice is picked
  rate/pitch (YAML) — TTS tuning (defaults 0.95 / 1.05)
  lottie    — URL to a Lottie JSON animation (optional; default: built-in
              face), or { url, idle: [from,to], talk: [from,to] } — frame
              segments looped per state instead of just changing tempo
  rive      — URL to a .riv file, or { url, stateMachine: "name" }: the
              state machine's inputs are auto-wired — a boolean named like
              "talk" follows the speaking state, a number named like "mouth"
              follows the live waveform, triggers fire as each line starts
  video     — recorded character clip URL, or a list of fallbacks (alpha
              WebM first, H.264 mp4 second) — script lines with video: true
              play it with sound: real face, real lips, real voice
  transparent — true + an alpha WebM source: black background keyed away,
              the character floats free (non-VP9-alpha browsers keep the
              round crop via the mp4 fallback)
  autoplay  — "true" to start on page load (default: false)
  step      — "true" for step-by-step playback: each click on the trigger (or
              the character) speaks the next line and stops; the trigger reads
              ▶ Start → Next → (n/total) → ↺ Replay. Ideal for live walk-throughs.
  size      — pixel size of the character bubble (default: 140)

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* ── overlay host ────────────────────────────────────── */
.lc-avatar-host {
  position: fixed; bottom: 90px; z-index: 900;
  pointer-events: none;
  transition: left 1.6s cubic-bezier(.4,0,.2,1),
              top 1.6s cubic-bezier(.4,0,.2,1),
              bottom 0.8s ease;
}
/* pose layer: travel lean + landing bounce (separate from the char's
   breathing so the transforms don't fight); also hosts the speech bubble —
   inside the char it was clipped by the circular crop's overflow:hidden */
.lc-avatar-pose { position: relative; transition: transform 0.5s ease; }
.lc-avatar-host.lc-avt-move-r .lc-avatar-pose { transform: rotate(5deg); }
.lc-avatar-host.lc-avt-move-l .lc-avatar-pose { transform: rotate(-5deg); }
.lc-avatar-host.lc-avt-land .lc-avatar-pose { animation: lc-avt-land 0.45s ease; }
@keyframes lc-avt-land {
  0% { transform: scale(1, 1); }
  40% { transform: scale(1.06, 0.9); }
  70% { transform: scale(0.97, 1.04); }
  100% { transform: scale(1, 1); }
}
/* ── character bubble ────────────────────────────────── */
.lc-avatar-char {
  pointer-events: auto;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 4px 18px rgba(0,0,0,0.18);
  background: #fff;
  display: flex; align-items: center; justify-content: center;
  position: relative;
  animation: lc-avt-breathe 4s ease-in-out infinite;
}
@keyframes lc-avt-breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.025); } }
.lc-avatar-char:hover { filter: brightness(1.06); }
/* built-in animated face */
.lc-avatar-face { width: 100%; height: 100%; }
.lc-avatar-face svg { width: 100%; height: 100%; display: block; }
.lc-avatar-face .eye-g,
.lc-avatar-face .mouth { transform-box: fill-box; transform-origin: center; }
.lc-avatar-face .eye-g { animation: lc-avt-blink 4.2s infinite; }
.lc-avatar-face .pupil { transition: transform 0.3s ease; }
@keyframes lc-avt-blink {
  0%, 93%, 100% { transform: scaleY(1); }
  95%, 97%      { transform: scaleY(0.08); }
}
/* TTS lines flap the mouth on a loop; audio lines drive it per-frame in JS */
.lc-avatar-talking .lc-avatar-face .mouth {
  animation: lc-avt-mouth 0.24s ease-in-out infinite alternate;
}
@keyframes lc-avt-mouth { from { transform: scaleY(1); } to { transform: scaleY(3.6); } }
/* Lottie fills the bubble */
.lc-avatar-lottie { width: 100%; height: 100%; }
/* Rive state-machine character fills the bubble */
.lc-avatar-rive { width: 100%; height: 100%; display: block; }
/* video character (recorded narration — e.g. a Memoji) fills the bubble */
.lc-avatar-video { width: 100%; height: 100%; object-fit: cover; display: block; }
/* transparent character (alpha webm): no porthole — the face floats free */
.lc-avatar-alpha .lc-avatar-char {
  background: transparent; box-shadow: none; border-radius: 0; overflow: visible;
}
.lc-avatar-alpha .lc-avatar-video {
  object-fit: contain;
  filter: drop-shadow(0 6px 14px rgba(0,0,0,0.25));
}
/* ── spotlight on the element being described ────────── */
.lc-avatar-spot {
  outline: 3px solid #f59e0b; outline-offset: 4px;
  border-radius: 6px;
  transition: outline-color 0.3s;
}
/* ── speech bubble ───────────────────────────────────── */
.lc-avatar-speech {
  position: absolute; bottom: 105%; left: 50%;
  transform: translateX(-50%);
  background: #fff; border: 1px solid #e2e8f0;
  border-radius: 12px; padding: 8px 12px;
  font-size: 0.82em; color: #1e293b;
  max-width: 220px; min-width: 120px;
  text-align: center; line-height: 1.4;
  box-shadow: 0 2px 10px rgba(0,0,0,0.10);
  white-space: normal; pointer-events: none;
  opacity: 0; transition: opacity 0.25s;
}
.lc-avatar-speech::after {
  content: ""; position: absolute; top: 100%; left: 50%;
  transform: translateX(-50%);
  border: 7px solid transparent;
  border-top-color: #fff;
}
.lc-avatar-speech.visible { opacity: 1; }
/* ── trigger button ──────────────────────────────────── */
.lc-avatar-trigger {
  display: inline-flex; align-items: center; gap: 0.4em;
  background: #0066cc; color: #fff;
  border: none; border-radius: 6px;
  padding: 0.4em 1em; font-size: 0.88em;
  cursor: pointer; margin: 0.5em 0;
}
/* the markdown link inside the trigger keeps the theme's blue otherwise */
.lc-avatar-trigger a, .lc-avatar-trigger a:visited {
  color: #fff !important; text-decoration: none !important;
}
.lc-avatar-trigger:hover { background: #0052a3; }
.lc-avatar-trigger.playing { background: #64748b; }
</style>

<script>
(function () {
  if (window._lcAvatarReady) return;
  window._lcAvatarReady = true;

  /* ── Lottie loader ─────────────────────────────────── */
  var _lottieP = null;
  function loadLottie() {
    if (window.lottie) return Promise.resolve(window.lottie);
    if (_lottieP) return _lottieP;
    _lottieP = new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/lottie-web@5/build/player/lottie.min.js";
      s.onload  = function () { resolve(window.lottie || null); };
      s.onerror = function () { resolve(null); };
      document.head.appendChild(s);
    });
    return _lottieP;
  }

  /* ── Rive loader (state-machine characters) ────────── */
  var _riveP = null;
  function loadRive() {
    if (window.rive) return Promise.resolve(window.rive);
    if (_riveP) return _riveP;
    _riveP = new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = "https://unpkg.com/@rive-app/canvas@2";
      s.onload  = function () { resolve(window.rive || null); };
      s.onerror = function () { resolve(null); };
      document.head.appendChild(s);
    });
    return _riveP;
  }
  var _yP = null;
  function loadYaml() {
    if (window.jsyaml) return Promise.resolve(window.jsyaml);
    if (_yP) return _yP;
    _yP = new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js";
      s.onload  = function () { resolve(window.jsyaml || null); };
      s.onerror = function () { resolve(null); };
      document.head.appendChild(s);
    });
    return _yP;
  }

  /* ── path helpers (fallback for untargeted lines) ───── */
  var PATHS = {
    left:   function () { return { left: "5vw" };   },
    center: function () { return { left: "calc(50vw - 60px)" }; },
    right:  function () { return { left: "calc(90vw - 120px)" }; },
    wander: function (i) {
      var stops = ["6vw","22vw","48vw","70vw","88vw"];
      return { left: stops[i % stops.length] };
    }
  };

  /* ── speech synthesis ──────────────────────────────── */
  var _voices = [];
  function refreshVoices() {
    _voices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
  }
  if (window.speechSynthesis) {
    refreshVoices();
    window.speechSynthesis.onvoiceschanged = refreshVoices;
  }

  /* prefer the highest-quality voice for the requested language */
  var _RANK = ["neural", "natural", "premium", "enhanced", "google", "siri", "aria", "samantha"];
  function pickVoice(tag) {
    if (!_voices.length) refreshVoices();
    if (!_voices.length) return null;
    var cand = tag
      ? _voices.filter(function (v) { return (v.lang || "").toLowerCase().indexOf(tag.toLowerCase()) === 0; })
      : _voices.slice();
    if (!cand.length) cand = _voices.slice();
    function score(v) {
      var n = (v.name || "").toLowerCase(), s = 0;
      for (var i = 0; i < _RANK.length; i++) {
        if (n.indexOf(_RANK[i]) >= 0) { s = Math.max(s, _RANK.length - i); }
      }
      if (!v.localService) s += 0.5;
      return s;
    }
    cand.sort(function (a, b) { return score(b) - score(a); });
    return cand[0];
  }

  function speak(text, voiceTag, tune, onBoundary, onEnd) {
    if (!window.speechSynthesis) { onEnd && onEnd(); return; }
    window.speechSynthesis.cancel();
    var utt = new SpeechSynthesisUtterance(text);
    utt.rate  = (tune && tune.rate)  || 0.95;
    utt.pitch = (tune && tune.pitch) || 1.05;
    var v = pickVoice(voiceTag);
    if (v) utt.voice = v;
    utt.onboundary = function (e) { if (onBoundary) onBoundary(e); };
    utt.onend = function () { if (onEnd) onEnd(); };
    window.speechSynthesis.speak(utt);
  }

  /* ── audio lines: real lip-sync from the waveform ───── */
  function stopAudio(av) {
    if (av.audioEl) { try { av.audioEl.pause(); } catch (e) {} av.audioEl = null; }
    av.analyser = null;
  }
  function playAudio(av, url, onEnd) {
    stopAudio(av);
    var a = new Audio();
    a.crossOrigin = "anonymous";
    a.src = url;
    av.audioEl = a;
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (AC) {
        var ctx = av.actx || (av.actx = new AC());
        if (ctx.state === "suspended") ctx.resume();
        var src = ctx.createMediaElementSource(a);
        var an = ctx.createAnalyser();
        an.fftSize = 256;
        src.connect(an); an.connect(ctx.destination);
        av.analyser = an;
        mouthLoop(av);
      }
    } catch (e) { /* no analyser → CSS flap still runs */ }
    var done = function () { stopAudio(av); resetMouth(av); onEnd(); };
    a.onended = done;
    a.onerror = done;
    a.play().catch(done);
  }
  function mouthLoop(av) {
    if (!av.analyser || !av.playing) { resetMouth(av); return; }
    var data = new Uint8Array(av.analyser.frequencyBinCount);
    av.analyser.getByteFrequencyData(data);
    var sum = 0;
    for (var i = 2; i < 40; i++) sum += data[i];   // voice band
    var v = Math.min(1, (sum / 38) / 110);
    if (av.mouth) av.mouth.style.transform = "scaleY(" + (1 + v * 3.4) + ")";
    if (av.riveMouth) { try { av.riveMouth.value = v * 100; } catch (e) {} }
    requestAnimationFrame(function () { mouthLoop(av); });
  }
  function resetMouth(av) {
    if (av.mouth) av.mouth.style.transform = "";
    if (av.riveMouth) { try { av.riveMouth.value = 0; } catch (e) {} }
  }

  function playVideoLine(av, url, onEnd) {
    var v = av.videoEl;
    if (!v) { onEnd(); return; }
    /* per-line url overrides; otherwise the character's <source> list rules */
    var src = (url && url !== "true") ? url : "";
    if (src && v.getAttribute("src") !== src) v.src = src;
    v.muted = false;
    try { v.currentTime = 0; } catch (e) {}
    v.onended = function () { v.muted = true; onEnd(); };
    v.onerror = function () { onEnd(); };
    v.play().catch(function () { onEnd(); });
  }

  /* ── timed cues inside one recorded take ─────────────
     cues: [{ t: seconds, at: selector, say: caption, slide: next|prev|start|exit }]
     While the media plays, each cue fires when currentTime crosses t: the
     character walks to `at`, the caption changes to `say`, slides advance. */
  function attachCues(av, media, cues) {
    if (!media || !Array.isArray(cues) || !cues.length) return;
    var sorted = cues.slice().sort(function (a, b) { return (Number(a.t) || 0) - (Number(b.t) || 0); });
    var i = 0;
    var onTime = function () {
      while (i < sorted.length && media.currentTime >= (Number(sorted[i].t) || 0)) {
        applyCue(av, sorted[i]); i++;
      }
    };
    media.addEventListener("timeupdate", onTime);
    av._cueOff = function () { media.removeEventListener("timeupdate", onTime); av._cueOff = null; };
    onTime();
  }
  function applyCue(av, c) {
    if (c.at) anchorTo(av, String(c.at));
    if (c.input) setRiveInputs(av, c.input);
    if (c.say != null) av.bubble.textContent = String(c.say);
    if (c.slide != null && window.lcSlides) {
      var sl = String(c.slide);
      if (sl === "next") window.lcSlides.next();
      else if (sl === "prev") window.lcSlides.prev();
      else if (sl === "start") window.lcSlides.enter();
      else if (sl === "exit") window.lcSlides.exit();
    }
  }

  /* step mode over a recorded take: play to each cue, then PAUSE and wait for
     the next click — so one video walks beat by beat at the presenter's pace
     (and reaches its end, where the next click stops it). */
  function attachCuesStep(av, media, cues, id) {
    if (!media || !Array.isArray(cues) || !cues.length) return;
    var sorted = cues.slice().sort(function (a, b) { return (Number(a.t) || 0) - (Number(b.t) || 0); });
    var i = 0;
    while (i < sorted.length && (Number(sorted[i].t) || 0) <= 0.1) { applyCue(av, sorted[i]); i++; }
    var onTime = function () {
      if (i < sorted.length && media.currentTime >= (Number(sorted[i].t) || 0)) {
        try { media.pause(); } catch (e) {}
        applyCue(av, sorted[i]); i++;
        av._stepResume = function () {
          av._stepResume = null;
          try { media.play().catch(function () {}); } catch (e) {}
          updateTriggers(id);
        };
        updateTriggers(id);
      }
    };
    media.addEventListener("timeupdate", onTime);
    av._cueOff = function () { media.removeEventListener("timeupdate", onTime); av._cueOff = null; av._stepResume = null; };
  }

  /* ── script lines: "text" or { at, say, audio } ─────── */
  function lineSpec(x) {
    if (x && typeof x === "object") {
      return { at: String(x.at || ""), say: String(x.say || x.text || ""),
               audio: String(x.audio || ""), video: String(x.video || ""),
               input: x.input || null,
               cues: Array.isArray(x.cues) ? x.cues : [] };
    }
    return { at: "", say: String(x), audio: "", video: "", input: null, cues: [] };
  }

  /* park the character beside the element it describes; eyes follow it */
  function anchorTo(av, sel) {
    var t = null;
    try { t = document.querySelector(sel); } catch (e) {}
    if (!t) return false;
    var S = window.lcSlides;
    if (S && S.isActive && S.isActive() && S.slideOf) {
      /* slide mode: walk the deck to the slide that holds the target and
         disclose it (all fragments) — the narration drives the presentation */
      var si = S.slideOf(t);
      if (si >= 0) S.goto(si, true);
    } else {
      t.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    clearSpot(av);
    av.spot = t;
    t.classList.add("lc-avatar-spot");
    setTimeout(function () {
      if (!av.playing) return;
      var r = t.getBoundingClientRect(), s = av.size, pad = 10;
      var left, top;
      var roomR = window.innerWidth - r.right, roomL = r.left;
      if (Math.max(roomR, roomL) >= s + 28) {
        /* desktop: park on the roomier side, vertically centered */
        left = roomR >= s + 28 ? r.right + 18 : r.left - s - 18;
        top = r.top + r.height / 2 - s / 2;
        top = Math.max(s * 0.8, Math.min(window.innerHeight - s - pad, top));
      } else {
        /* narrow viewport (phone): float above the element, centered —
           beside it there is no margin and the character covers the text */
        left = r.left + r.width / 2 - s / 2;
        top = r.top - s - 22;
        if (top < 90) top = Math.min(window.innerHeight - s - pad, r.bottom + 22);
      }
      left = Math.max(pad, Math.min(window.innerWidth - s - pad, left));
      moveHost(av, left + "px", top + "px");
      lookAt(av, r.left + r.width / 2, r.top + r.height / 2);
    }, 480);
    return true;
  }

  function clearSpot(av) {
    if (av.spot) { av.spot.classList.remove("lc-avatar-spot"); av.spot = null; }
  }

  /* travel with a lean in the direction of movement; bounce on arrival */
  function moveHost(av, left, top) {
    var fromX = av.host.getBoundingClientRect().left;
    if (top != null) { av.host.style.bottom = "auto"; av.host.style.top = top; }
    else { av.host.style.bottom = "90px"; av.host.style.top = "auto"; }
    if (left) av.host.style.left = left;
    requestAnimationFrame(function () {
      var dx = av.host.getBoundingClientRect().left - fromX;
      if (Math.abs(dx) < 4) return;
      av.host.classList.add(dx > 0 ? "lc-avt-move-r" : "lc-avt-move-l");
      clearTimeout(av._moveT);
      av._moveT = setTimeout(function () {
        av.host.classList.remove("lc-avt-move-r", "lc-avt-move-l");
        av.host.classList.add("lc-avt-land");
        setTimeout(function () { av.host.classList.remove("lc-avt-land"); }, 500);
      }, 1500);
    });
  }

  /* pupils glance toward a viewport point (built-in face only) */
  function lookAt(av, x, y) {
    if (!av.pupils) return;
    var r = av.char.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    var dx = x - cx, dy = y - cy, L = Math.hypot(dx, dy) || 1;
    var m = 2.4;
    av.pupils.forEach(function (p) {
      p.style.transform = "translate(" + (dx / L * m) + "px," + (dy / L * m) + "px)";
    });
  }
  function lookIdle(av) {
    if (!av.pupils) return;
    var a = Math.random() * Math.PI * 2, m = Math.random() * 1.8;
    av.pupils.forEach(function (p) {
      p.style.transform = "translate(" + (Math.cos(a) * m) + "px," + (Math.sin(a) * m) + "px)";
    });
  }

  /* ── upgrade .avatar code block ───────────────────── */
  var AVT_ID = 0, AVT_SLOT = 0;
  function upgradeAvatar(el) {
    if (el.dataset.lcAvatarDone) return;
    el.dataset.lcAvatarDone = "1";

    var raw  = (el.querySelector("code") || el).textContent.trim();
    var size = parseInt(el.getAttribute("size") || "140", 10);
    var elId = el.id || ("avt" + (++AVT_ID));
    var slot = AVT_SLOT++;
    el.style.display = "none"; /* hide source block */

    loadYaml().then(function (jsyaml) {
      var cfg = {};
      try { cfg = (jsyaml ? jsyaml.load(raw) : JSON.parse(raw)) || {}; } catch (e) {}

      var script   = Array.isArray(cfg.script) ? cfg.script.map(lineSpec) : [];
      var pathName = cfg.path  || "wander";
      var voiceTag = cfg.voice || "";
      /* lottie: URL, or { url, idle: [from,to], talk: [from,to] } */
      var lottieCfg = cfg.lottie || "";
      var lottieUrl = (lottieCfg && typeof lottieCfg === "object")
        ? String(lottieCfg.url || lottieCfg.src || "") : String(lottieCfg || "");
      var lottieSeg = (lottieCfg && typeof lottieCfg === "object" &&
                       Array.isArray(lottieCfg.idle) && Array.isArray(lottieCfg.talk))
        ? { idle: lottieCfg.idle, talk: lottieCfg.talk } : null;
      /* rive: URL, or { url, stateMachine: "name" } */
      var riveCfg = cfg.rive || "";
      var riveUrl = (riveCfg && typeof riveCfg === "object")
        ? String(riveCfg.url || riveCfg.src || "") : String(riveCfg || "");
      var riveSm  = (riveCfg && typeof riveCfg === "object")
        ? String(riveCfg.stateMachine || "") : "";
      var videoUrl = cfg.video || "";
      var transparent = cfg.transparent === true;
      var autoplay = cfg.autoplay === true || el.getAttribute("autoplay") === "true";
      var step = cfg.step === true || el.getAttribute("step") === "true";

      /* build overlay host — stagger instances so they never stack */
      var host = document.createElement("div");
      host.className = "lc-avatar-host";
      host.id = "lc-avatar-" + elId;
      host.setAttribute("data-lc-id", elId);
      host.style.left = (6 + (slot % 5) * 16) + "vw";

      var pose = document.createElement("div");
      pose.className = "lc-avatar-pose";
      host.appendChild(pose);

      var char = document.createElement("div");
      char.className = "lc-avatar-char";
      char.style.width  = size + "px";
      char.style.height = size + "px";
      pose.appendChild(char);

      var bubble = document.createElement("div");
      bubble.className = "lc-avatar-speech";
      pose.appendChild(bubble);

      document.body.appendChild(host);

      /* register for trigger lookup */
      var av = (window._lcAvatars = window._lcAvatars || {})[elId] = {
        host: host, bubble: bubble, char: char,
        script: script, path: pathName, voice: voiceTag,
        tune: { rate: parseFloat(cfg.rate) || 0, pitch: parseFloat(cfg.pitch) || 0 },
        lottie: lottieUrl, lottieSeg: lottieSeg,
        rive: riveUrl, riveSm: riveSm,
        riveAnim: null, riveTalk: null, riveMouth: null,
        riveTriggers: [], riveInputs: null,
        video: videoUrl, transparent: transparent,
        size: size, spot: null,
        pupils: null, mouth: null, audioEl: null, videoEl: null, analyser: null,
        playing: false, idx: 0, lottieDone: false, step: step
      };

      /* init character graphic */
      initChar(elId, char, size);

      /* idle saccades keep the built-in face alive */
      setInterval(function () { if (!av.playing) lookIdle(av); }, 3200);

      /* click to play/stop */
      char.addEventListener("click", function () { togglePlay(elId); });

      if (autoplay) {
        /* slight delay so voices list populates */
        setTimeout(function () { startPlay(elId); }, 800);
      }
    });
  }

  function initChar(id, char, size) {
    var av1 = window._lcAvatars[id];
    var videoUrl  = av1 ? av1.video  : "";
    var lottieUrl = av1 ? av1.lottie : "";
    if (videoUrl) {
      /* recorded character (e.g. a Memoji) — real lips, real voice;
         idle = paused first frame, video lines play it with sound.
         A list of URLs becomes <source> fallbacks (alpha webm first,
         mp4 for browsers without VP9-alpha); transparent styling only
         applies when the alpha source actually got picked. */
      var v = document.createElement("video");
      v.className = "lc-avatar-video";
      var av0 = window._lcAvatars[id];
      var list = Array.isArray(videoUrl) ? videoUrl : [videoUrl];
      list.forEach(function (u) {
        var so = document.createElement("source");
        so.src = String(u);
        if (/\.webm(\?|$)/i.test(String(u))) so.type = 'video/webm; codecs="vp9"';
        v.appendChild(so);
      });
      v.muted = true;
      v.preload = "metadata";
      v.setAttribute("playsinline", "");
      v.addEventListener("loadeddata", function () {
        /* "picked the webm" is not enough: WebKit decodes VP9 but drops the
           alpha plane (black background). Probe a real pixel instead — the
           frame corner is always background, so transparent there means the
           alpha actually survived decoding. */
        if (!av0 || !av0.transparent) return;
        try {
          var c = document.createElement("canvas");
          c.width = 32; c.height = 24;
          var cx = c.getContext("2d", { willReadFrequently: true });
          cx.drawImage(v, 0, 0, 32, 24);
          if (cx.getImageData(1, 1, 1, 1).data[3] < 16) {
            av0.host.classList.add("lc-avatar-alpha");
          }
        } catch (e) { /* tainted/unsupported → keep the round crop */ }
      });
      char.appendChild(v);
      if (av0) av0.videoEl = v;
      return;
    }
    if (av1 && av1.rive) {
      /* Rive character: a live state machine, not a recording — its inputs
         (talk / mouth / triggers) are discovered on load and driven by the
         narration. */
      loadRive().then(function (rive) {
        if (!rive) { addFace(id, char); return; }
        var cv = document.createElement("canvas");
        cv.className = "lc-avatar-rive";
        cv.width = size * 2; cv.height = size * 2;
        char.appendChild(cv);
        var opts = {
          src: av1.rive, canvas: cv, autoplay: true,
          onLoad: function () {
            try { av1.riveAnim.resizeDrawingSurfaceToCanvas(); } catch (e) {}
            wireRiveInputs(av1, rive);
          }
        };
        if (av1.riveSm) opts.stateMachines = av1.riveSm;
        try { opts.layout = new rive.Layout({ fit: rive.Fit.Cover }); } catch (e) {}
        try { av1.riveAnim = new rive.Rive(opts); }
        catch (e) { cv.remove(); addFace(id, char); }
      });
      return;
    }
    if (lottieUrl) {
      loadLottie().then(function (lottie) {
        if (!lottie) { addFace(id, char); return; }
        var div = document.createElement("div");
        div.className = "lc-avatar-lottie";
        char.appendChild(div);
        var anim = lottie.loadAnimation({
          container: div, renderer: "svg", loop: true,
          autoplay: false, path: lottieUrl
        });
        var av = window._lcAvatars[id];
        if (av) { av.lottieAnim = anim; av.lottieDone = true; }
      });
    } else {
      addFace(id, char);
    }
  }

  /* built-in face: blinks, breathes, pupils track the spotlight, mouth
     flaps for TTS and follows the waveform for audio lines */
  function addFace(id, char) {
    var face = document.createElement("div");
    face.className = "lc-avatar-face";
    face.innerHTML =
      '<svg viewBox="0 0 100 100" aria-hidden="true">' +
      '<circle cx="50" cy="50" r="50" fill="#ffd166"/>' +
      '<circle cx="29" cy="60" r="7" fill="#f4978e" opacity="0.55"/>' +
      '<circle cx="71" cy="60" r="7" fill="#f4978e" opacity="0.55"/>' +
      '<g class="eye-g">' +
      '<circle cx="35" cy="43" r="7" fill="#fff" stroke="#e0c285" stroke-width="1"/>' +
      '<circle class="pupil" cx="35" cy="43" r="3.4" fill="#1e293b"/>' +
      '</g>' +
      '<g class="eye-g">' +
      '<circle cx="65" cy="43" r="7" fill="#fff" stroke="#e0c285" stroke-width="1"/>' +
      '<circle class="pupil" cx="65" cy="43" r="3.4" fill="#1e293b"/>' +
      '</g>' +
      '<path d="M28 34 Q35 30 42 34" stroke="#b98a3f" stroke-width="2.2" fill="none" stroke-linecap="round"/>' +
      '<path d="M58 34 Q65 30 72 34" stroke="#b98a3f" stroke-width="2.2" fill="none" stroke-linecap="round"/>' +
      '<ellipse class="mouth" cx="50" cy="68" rx="11" ry="3.2" fill="#7c2d12"/>' +
      '</svg>';
    char.appendChild(face);
    var av = window._lcAvatars[id];
    if (av) {
      av.pupils = Array.prototype.slice.call(face.querySelectorAll(".pupil"));
      av.mouth = face.querySelector(".mouth");
    }
  }

  /* discover the loaded Rive state machine's inputs: a boolean named like
     "talk" follows the speaking state, a number named like "mouth" follows
     the live waveform (vector lip-sync), every trigger fires line by line —
     and ALL inputs are reachable by name through input: on lines and cues */
  function wireRiveInputs(av, rive) {
    var r = av.riveAnim;
    if (!r) return;
    var names = av.riveSm ? [av.riveSm] : (r.stateMachineNames || []);
    if (!av.riveSm && names.length) { try { r.play(names[0]); } catch (e) {} }
    var T = rive.StateMachineInputType || {};
    av.riveInputs = {};
    names.forEach(function (nm) {
      var inputs = [];
      try { inputs = r.stateMachineInputs(nm) || []; } catch (e) {}
      inputs.forEach(function (inp) {
        var n = String(inp.name || "").toLowerCase();
        av.riveInputs[n] = inp;
        if (inp.type === T.Boolean) {
          if (!av.riveTalk && /talk|speak|active|play|press|hover/.test(n)) av.riveTalk = inp;
        } else if (inp.type === T.Number) {
          if (!av.riveMouth && /mouth|talk|loud|level|volume/.test(n)) av.riveMouth = inp;
        } else if (typeof inp.fire === "function") {
          av.riveTriggers.push(inp);
        }
      });
    });
    /* surface what this character can do — authors read this in the
       console to write their input: lines without opening the editor */
    var found = Object.keys(av.riveInputs).map(function (k) {
      var i = av.riveInputs[k];
      var kind = typeof i.fire === "function" ? "trigger"
        : typeof i.value === "boolean" ? "boolean" : "number";
      return k + " (" + kind + ")";
    });
    if (found.length) {
      console.info("[avatar] rive inputs of \"" + (names[0] || "?") + "\": " + found.join(", "));
    }
  }

  /* drive named state-machine inputs declaratively:
     "bark"                  → fire the trigger named bark
     { run: true, speed: 7 } → set boolean / number inputs (truthy fires
                               a trigger of that name too) */
  function setRiveInputs(av, spec) {
    if (!spec || !av.riveInputs) return;
    if (typeof spec === "string") {
      var t = av.riveInputs[spec.toLowerCase()];
      if (t && typeof t.fire === "function") { try { t.fire(); } catch (e) {} }
      return;
    }
    Object.keys(spec).forEach(function (k) {
      var inp = av.riveInputs[k.toLowerCase()];
      if (!inp) return;
      try {
        if (typeof inp.fire === "function") { if (spec[k]) inp.fire(); }
        else inp.value = spec[k];
      } catch (e) {}
    });
  }

  /* flip the character into/out of its talking state, whatever it's made
     of: Lottie → talk/idle segments (or tempo), Rive → talk input (or fire
     a trigger so even input-less hello-world files visibly react — unless
     the line drives inputs explicitly) */
  function charTalk(av, on, explicit) {
    if (av.lottieAnim) {
      if (av.lottieSeg) {
        av.lottieAnim.playSegments(on ? av.lottieSeg.talk : av.lottieSeg.idle, true);
      } else {
        av.lottieAnim.setSpeed(on ? 1.5 : 0.7);
      }
    }
    if (av.riveTalk) { try { av.riveTalk.value = on; } catch (e) {} }
    else if (on && !explicit && av.riveTriggers.length) {
      try { av.riveTriggers[(av.idx - 1) % av.riveTriggers.length].fire(); } catch (e) {}
    }
    if (!on && av.riveMouth) { try { av.riveMouth.value = 0; } catch (e) {} }
  }

  /* ── playback ──────────────────────────────────────── */
  function togglePlay(id) {
    var av = window._lcAvatars && window._lcAvatars[id];
    if (!av) return;
    if (av.step) {
      /* step mode: advance one beat per click — a script line, or, inside a
         recorded take, the next cue (the video pauses between cues) */
      if (!av.playing) startPlay(id);
      else if (av._stepResume) av._stepResume();
      else nextLine(id);
    } else {
      if (av.playing) { stopPlay(id); } else { startPlay(id); }
    }
    updateTriggers(id);
  }

  function startPlay(id) {
    var av = window._lcAvatars[id];
    if (!av || av.playing) return;
    av.playing = true; av.idx = 0;
    av.host.setAttribute("data-state", "speaking");
    if (av.lottieAnim) {
      if (av.lottieSeg) av.lottieAnim.playSegments(av.lottieSeg.idle, true);
      else { av.lottieAnim.play(); av.lottieAnim.setSpeed(1); }
    }
    nextLine(id);
    updateTriggers(id);
  }

  function stopPlay(id, completed) {
    var av = window._lcAvatars[id];
    if (!av) return;
    av.playing = false;
    try {
      av.host.dispatchEvent(new CustomEvent("lc-avatar-ended",
        { bubbles: true, detail: { id: id, completed: !!completed } }));
    } catch (e) {}
    if (av._cueOff) av._cueOff();
    av._stepResume = null;
    av.host.setAttribute("data-state", "idle");
    av.host.classList.remove("lc-avatar-talking");
    clearSpot(av);
    stopAudio(av);
    resetMouth(av);
    if (av.videoEl) { try { av.videoEl.pause(); av.videoEl.muted = true; } catch (e) {} }
    window.speechSynthesis && window.speechSynthesis.cancel();
    if (av.lottieAnim) av.lottieAnim.stop();
    if (av.riveTalk) { try { av.riveTalk.value = false; } catch (e) {} }
    av.bubble.classList.remove("visible");
    updateTriggers(id);
  }

  function nextLine(id) {
    var av = window._lcAvatars[id];
    if (!av || !av.playing) return;
    if (av.idx >= av.script.length) { stopPlay(id, true); return; }

    var line = av.script[av.idx];
    av.idx++;

    /* move the character: to the element it describes, or along the path */
    var anchored = line.at && anchorTo(av, line.at);
    if (!anchored) {
      clearSpot(av);
      moveHost(av, "", null);
      Object.assign(av.host.style, (PATHS[av.path] || PATHS.wander)(av.idx - 1));
      if (av.pupils) lookAt(av, window.innerWidth / 2, 0);
    }

    av.bubble.classList.add("visible");
    av.host.classList.add("lc-avatar-talking");
    charTalk(av, true, !!line.input);
    if (line.input) setRiveInputs(av, line.input);

    var finish = function () {
      if (av._cueOff) av._cueOff();
      av.host.classList.remove("lc-avatar-talking");
      charTalk(av, false);
      if (av.step) { updateTriggers(id); return; }   /* keep the caption; wait for the next click */
      av.bubble.classList.remove("visible");
      setTimeout(function () { nextLine(id); }, 500);
    };

    if (line.video) {
      /* recorded narration: real face, real voice — the bubble is a caption */
      av.bubble.textContent = line.say;
      playVideoLine(av, line.video, finish);
      if (av.step && Array.isArray(line.cues) && line.cues.length) attachCuesStep(av, av.videoEl, line.cues, id);
      else attachCues(av, av.videoEl, line.cues);
      return;
    }

    if (line.audio) {
      /* studio voice: bubble shows the full line, mouth follows the waveform */
      av.bubble.textContent = line.say;
      playAudio(av, line.audio, finish);
      attachCues(av, av.audioEl, line.cues);
      return;
    }

    /* TTS: reveal the bubble word by word as boundaries fire */
    var words = line.say.split(" ");
    av.bubble.textContent = "";
    var revealed = 0;
    var revealT = setTimeout(function () {
      /* no boundary events (some browsers) → show the whole line */
      if (!av.bubble.textContent) av.bubble.textContent = line.say;
    }, 400);
    speak(line.say, av.voice, av.tune, function (e) {
      if (e && e.name === "word" && revealed < words.length) {
        revealed += 1;
        av.bubble.textContent = words.slice(0, revealed).join(" ");
      }
    }, function () {
      clearTimeout(revealT);
      av.bubble.textContent = line.say;
      finish();
    });
  }

  /* ── upgrade .avatar-trigger links ────────────────── */
  function upgradeTrigger(el) {
    if (el.dataset.lcAvtTrigDone) return;
    el.dataset.lcAvtTrigDone = "1";
    var targetId  = el.getAttribute("target") || "";
    var labelPlay = el.textContent.trim() || "▶ Play";
    var labelStop = el.getAttribute("label-stop") || "⏹ Stop";
    el.classList.add("lc-avatar-trigger");
    el.setAttribute("data-avt-target", targetId);
    el.setAttribute("data-avt-play", labelPlay);
    el.setAttribute("data-avt-stop", labelStop);
    el.addEventListener("click", function (e) {
      e.preventDefault();
      togglePlay(targetId);
    });
  }

  /* ── studio trigger: record the narrated walk ─────────
     Opens the screen recorder; once recording starts (the stop button
     appears — the screen picker needs a real user gesture), enters slide
     mode and plays the avatar; when the script completes, stops the
     recording and leaves the deck. The recorder's review panel then offers
     the YouTube upload. */
  function upgradeStudio(el) {
    if (el.dataset.lcAvtStudioDone) return;
    el.dataset.lcAvtStudioDone = "1";
    var targetId = el.getAttribute("target") || "";
    el.classList.add("lc-avatar-trigger");
    el.addEventListener("click", function (e) {
      e.preventDefault();
      if (!window.lcOpenRecorder) return;
      /* the avatar is the face and the voice: no camera, no mic —
         and screen/tab audio ON so the narration lands in the video */
      window.lcOpenRecorder({ camera: "off", mic: "off", sound: "on" });
      var deadline = Date.now() + 60000;
      var poll = setInterval(function () {
        if (Date.now() > deadline) { clearInterval(poll); return; }
        var stopBtn = document.querySelector(".lc-rec-stop, [data-lc-stop]");
        if (!stopBtn) return;
        clearInterval(poll);
        if (window.lcSlides) window.lcSlides.enter();
        setTimeout(function () { startPlay(targetId); updateTriggers(targetId); }, 800);
        var onEnd = function (ev) {
          if (!ev.detail || ev.detail.id !== targetId || !ev.detail.completed) return;
          document.removeEventListener("lc-avatar-ended", onEnd);
          setTimeout(function () {
            var sb = document.querySelector(".lc-rec-stop, [data-lc-stop]");
            if (sb) sb.click();
            if (window.lcSlides) window.lcSlides.exit();
          }, 1200);
        };
        document.addEventListener("lc-avatar-ended", onEnd);
      }, 400);
    });
  }

  function updateTriggers(id) {
    var av = window._lcAvatars && window._lcAvatars[id];
    document.querySelectorAll("[data-avt-target='" + id + "']").forEach(function (btn) {
      var playing = av && av.playing;
      if (av && av.step) {
        /* step mode: Start → Next → … → Replay */
        btn.textContent = !playing
          ? (av.idx > 0 ? "↺ Replay" : (btn.getAttribute("data-avt-play") || "▶ Start"))
          : (av._stepResume ? "Next →" : "Next → (" + av.idx + "/" + av.script.length + ")");
      } else {
        btn.textContent = playing
          ? (btn.getAttribute("data-avt-stop") || "⏹ Stop")
          : (btn.getAttribute("data-avt-play") || "▶ Play");
      }
      btn.classList.toggle("playing", !!playing);
    });
  }

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry:
     one registration covers the initial page scan and all re-scans. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.avatar, pre.avatar", upgradeAvatar);
    window.lcRegisterUpgrader("p.avatar-trigger, a.avatar-trigger", upgradeTrigger);
    window.lcRegisterUpgrader("p.avatar-studio, a.avatar-studio", upgradeStudio);
  }

})();
</script>
