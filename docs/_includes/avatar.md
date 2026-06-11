{%- comment -%}
Avatar — speaking overlay character that narrates content and follows the
elements it describes. Voice: per-line audio files (studio TTS, with real
amplitude lip-sync) or the Web Speech API. Face: built-in animated SVG
(blinks, breathes, eyes track the spotlighted element, mouth follows the
audio) or any Lottie animation.

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

Attributes on .avatar:
  id        — referenced by .avatar-trigger's target=""
  path      — left | center | right | wander (fallback for untargeted lines)
  voice     — BCP-47 tag; the best-quality matching browser voice is picked
  rate/pitch (YAML) — TTS tuning (defaults 0.95 / 1.05)
  lottie    — URL to a Lottie JSON animation (optional; default: built-in face)
  video     — URL of a recorded character clip (e.g. an iPhone Memoji, H.264
              mp4) — script lines with video: true play it with sound: real
              face, real lips, real voice
  autoplay  — "true" to start on page load (default: false)
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
   breathing so the transforms don't fight) */
.lc-avatar-pose { transition: transform 0.5s ease; }
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
/* video character (recorded narration — e.g. a Memoji) fills the bubble */
.lc-avatar-video { width: 100%; height: 100%; object-fit: cover; display: block; }
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

  /* ── YAML loader (reuse code_chrome's window.jsyaml if present) ─── */
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
    requestAnimationFrame(function () { mouthLoop(av); });
  }
  function resetMouth(av) {
    if (av.mouth) av.mouth.style.transform = "";
  }

  function playVideoLine(av, url, onEnd) {
    var v = av.videoEl;
    if (!v) { onEnd(); return; }
    var src = (url && url !== "true") ? url : av.video;
    if (src && v.getAttribute("src") !== src) v.src = src;
    v.muted = false;
    try { v.currentTime = 0; } catch (e) {}
    v.onended = function () { v.muted = true; onEnd(); };
    v.onerror = function () { onEnd(); };
    v.play().catch(function () { onEnd(); });
  }

  /* ── script lines: "text" or { at, say, audio } ─────── */
  function lineSpec(x) {
    if (x && typeof x === "object") {
      return { at: String(x.at || ""), say: String(x.say || x.text || ""),
               audio: String(x.audio || ""), video: String(x.video || "") };
    }
    return { at: "", say: String(x), audio: "", video: "" };
  }

  /* park the character beside the element it describes; eyes follow it */
  function anchorTo(av, sel) {
    var t = null;
    try { t = document.querySelector(sel); } catch (e) {}
    if (!t) return false;
    t.scrollIntoView({ behavior: "smooth", block: "center" });
    clearSpot(av);
    av.spot = t;
    t.classList.add("lc-avatar-spot");
    setTimeout(function () {
      if (!av.playing) return;
      var r = t.getBoundingClientRect(), s = av.size, pad = 10;
      var left = r.right + 18;
      if (left + s > window.innerWidth - pad) left = r.left - s - 18;
      left = Math.max(pad, Math.min(window.innerWidth - s - pad, left));
      var top = r.top + r.height / 2 - s / 2;
      top = Math.max(s * 0.8, Math.min(window.innerHeight - s - pad, top));
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
      var lottieUrl= cfg.lottie || "";
      var videoUrl = cfg.video || "";
      var autoplay = cfg.autoplay === true || el.getAttribute("autoplay") === "true";

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
      char.appendChild(bubble);

      document.body.appendChild(host);

      /* register for trigger lookup */
      var av = (window._lcAvatars = window._lcAvatars || {})[elId] = {
        host: host, bubble: bubble, char: char,
        script: script, path: pathName, voice: voiceTag,
        tune: { rate: parseFloat(cfg.rate) || 0, pitch: parseFloat(cfg.pitch) || 0 },
        lottie: lottieUrl, video: videoUrl, size: size, spot: null,
        pupils: null, mouth: null, audioEl: null, videoEl: null, analyser: null,
        playing: false, idx: 0, lottieDone: false
      };

      /* init character graphic */
      initChar(elId, videoUrl, lottieUrl, char, size);

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

  function initChar(id, videoUrl, lottieUrl, char, size) {
    if (videoUrl) {
      /* recorded character (e.g. a Memoji) — real lips, real voice;
         idle = paused first frame, video lines play it with sound */
      var v = document.createElement("video");
      v.className = "lc-avatar-video";
      v.src = videoUrl;
      v.muted = true;
      v.preload = "metadata";
      v.setAttribute("playsinline", "");
      char.appendChild(v);
      var av0 = window._lcAvatars[id];
      if (av0) av0.videoEl = v;
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

  /* ── playback ──────────────────────────────────────── */
  function togglePlay(id) {
    var av = window._lcAvatars && window._lcAvatars[id];
    if (!av) return;
    if (av.playing) { stopPlay(id); } else { startPlay(id); }
    updateTriggers(id);
  }

  function startPlay(id) {
    var av = window._lcAvatars[id];
    if (!av || av.playing) return;
    av.playing = true; av.idx = 0;
    av.host.setAttribute("data-state", "speaking");
    if (av.lottieAnim) { av.lottieAnim.play(); av.lottieAnim.setSpeed(1); }
    nextLine(id);
    updateTriggers(id);
  }

  function stopPlay(id) {
    var av = window._lcAvatars[id];
    if (!av) return;
    av.playing = false;
    av.host.setAttribute("data-state", "idle");
    av.host.classList.remove("lc-avatar-talking");
    clearSpot(av);
    stopAudio(av);
    resetMouth(av);
    if (av.videoEl) { try { av.videoEl.pause(); av.videoEl.muted = true; } catch (e) {} }
    window.speechSynthesis && window.speechSynthesis.cancel();
    if (av.lottieAnim) av.lottieAnim.stop();
    av.bubble.classList.remove("visible");
    updateTriggers(id);
  }

  function nextLine(id) {
    var av = window._lcAvatars[id];
    if (!av || !av.playing) return;
    if (av.idx >= av.script.length) { stopPlay(id); return; }

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
    if (av.lottieAnim) av.lottieAnim.setSpeed(1.5);

    var finish = function () {
      av.host.classList.remove("lc-avatar-talking");
      if (av.lottieAnim) av.lottieAnim.setSpeed(0.7);
      av.bubble.classList.remove("visible");
      setTimeout(function () { nextLine(id); }, 500);
    };

    if (line.video) {
      /* recorded narration: real face, real voice — the bubble is a caption */
      av.bubble.textContent = line.say;
      playVideoLine(av, line.video, finish);
      return;
    }

    if (line.audio) {
      /* studio voice: bubble shows the full line, mouth follows the waveform */
      av.bubble.textContent = line.say;
      playAudio(av, line.audio, finish);
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

  function updateTriggers(id) {
    var av = window._lcAvatars && window._lcAvatars[id];
    document.querySelectorAll("[data-avt-target='" + id + "']").forEach(function (btn) {
      var playing = av && av.playing;
      btn.textContent = playing
        ? (btn.getAttribute("data-avt-stop") || "⏹ Stop")
        : (btn.getAttribute("data-avt-play") || "▶ Play");
      btn.classList.toggle("playing", !!playing);
    });
  }

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry:
     one registration covers the initial page scan and all re-scans. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.avatar, pre.avatar", upgradeAvatar);
    window.lcRegisterUpgrader("p.avatar-trigger, a.avatar-trigger", upgradeTrigger);
  }

})();
</script>
