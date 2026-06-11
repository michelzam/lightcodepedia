{%- comment -%}
Avatar — speaking overlay character driven by Web Speech API, with an
animated built-in face (or a Lottie animation) that follows the content
it narrates.

Usage:
  ```yaml
  name: "Prof. LC"
  voice: en-US
  rate: 0.95
  script:
    - "Hello! Let's explore Python objects together."
    - at: "#dog_grid_tuto"
      say: "This grid is editable — click a cell."
    - at: "#how-it-works"
      say: "Here is how everything fits."
  ```
  {: .avatar #prof }

  [▶ Play](#)
  {: .avatar-trigger target="prof" label-stop="⏹ Stop" }

Script lines are strings (the avatar wanders) or {at, say} objects: `at` is
a CSS selector — the avatar scrolls there, parks beside the element,
spotlights it, and speaks the line.

Attributes on .avatar:
  id        — referenced by .avatar-trigger's target=""
  path      — left | center | right | wander (fallback for untargeted lines)
  voice     — BCP-47 tag; the best-quality matching browser voice is picked
  rate/pitch (YAML) — speech tuning (defaults 0.95 / 1.05)
  lottie    — URL to a Lottie JSON animation (optional; default: built-in face)
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
}
.lc-avatar-char:hover { transform: scale(1.07); }
/* built-in animated face */
.lc-avatar-face { width: 100%; height: 100%; }
.lc-avatar-face svg { width: 100%; height: 100%; display: block; }
.lc-avatar-face .eye,
.lc-avatar-face .mouth { transform-box: fill-box; transform-origin: center; }
.lc-avatar-face .eye { animation: lc-avt-blink 4.2s infinite; }
@keyframes lc-avt-blink {
  0%, 93%, 100% { transform: scaleY(1); }
  95%, 97%      { transform: scaleY(0.08); }
}
.lc-avatar-talking .lc-avatar-face .mouth {
  animation: lc-avt-mouth 0.24s ease-in-out infinite alternate;
}
@keyframes lc-avt-mouth { from { transform: scaleY(1); } to { transform: scaleY(3.6); } }
/* Lottie fills the bubble */
.lc-avatar-lottie { width: 100%; height: 100%; }
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
  /* voices arrive asynchronously in most browsers */
  var _voices = [];
  function refreshVoices() {
    _voices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
  }
  if (window.speechSynthesis) {
    refreshVoices();
    window.speechSynthesis.onvoiceschanged = refreshVoices;
  }

  /* prefer the highest-quality voice for the requested language: neural /
     natural / premium voices first, cloud voices over robotic local ones */
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

  function speak(text, voiceTag, tune, onEnd) {
    if (!window.speechSynthesis) { onEnd && onEnd(); return; }
    window.speechSynthesis.cancel();
    var utt = new SpeechSynthesisUtterance(text);
    utt.rate  = (tune && tune.rate)  || 0.95;
    utt.pitch = (tune && tune.pitch) || 1.05;
    var v = pickVoice(voiceTag);
    if (v) utt.voice = v;
    utt.onend = function () { if (onEnd) onEnd(); };
    window.speechSynthesis.speak(utt);
  }

  /* ── script lines: "text" or { at: selector, say: text } ── */
  function lineSpec(x) {
    if (x && typeof x === "object") {
      return { at: String(x.at || ""), say: String(x.say || x.text || "") };
    }
    return { at: "", say: String(x) };
  }

  /* park the character beside the element it describes (after the smooth
     scroll settles), preferring its right side, staying in the viewport */
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
      av.host.style.bottom = "auto";
      av.host.style.top = top + "px";
      av.host.style.left = left + "px";
    }, 480);
    return true;
  }

  function clearSpot(av) {
    if (av.spot) { av.spot.classList.remove("lc-avatar-spot"); av.spot = null; }
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
      var autoplay = cfg.autoplay === true || el.getAttribute("autoplay") === "true";

      /* build overlay host — stagger instances so they never stack */
      var host = document.createElement("div");
      host.className = "lc-avatar-host";
      host.id = "lc-avatar-" + elId;
      host.setAttribute("data-lc-id", elId);
      host.style.left = (6 + (slot % 5) * 16) + "vw";

      var char = document.createElement("div");
      char.className = "lc-avatar-char";
      char.style.width  = size + "px";
      char.style.height = size + "px";
      host.appendChild(char);

      var bubble = document.createElement("div");
      bubble.className = "lc-avatar-speech";
      char.appendChild(bubble);

      document.body.appendChild(host);

      /* register for trigger lookup */
      (window._lcAvatars = window._lcAvatars || {})[elId] = {
        host: host, bubble: bubble, char: char,
        script: script, path: pathName, voice: voiceTag,
        tune: { rate: parseFloat(cfg.rate) || 0, pitch: parseFloat(cfg.pitch) || 0 },
        lottie: lottieUrl, size: size, spot: null,
        playing: false, idx: 0, lottieDone: false
      };

      /* init character graphic */
      initChar(elId, lottieUrl, char, size);

      /* click to play/stop */
      char.addEventListener("click", function () { togglePlay(elId); });

      if (autoplay) {
        /* slight delay so voices list populates */
        setTimeout(function () { startPlay(elId); }, 800);
      }
    });
  }

  function initChar(id, lottieUrl, char, size) {
    if (lottieUrl) {
      loadLottie().then(function (lottie) {
        if (!lottie) { addFace(char); return; }
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
      addFace(char);
    }
  }

  /* built-in face: warm circle, blinking eyes, mouth that flaps while
     speaking (the host carries .lc-avatar-talking during each line) */
  function addFace(char) {
    var face = document.createElement("div");
    face.className = "lc-avatar-face";
    face.innerHTML =
      '<svg viewBox="0 0 100 100" aria-hidden="true">' +
      '<circle cx="50" cy="50" r="50" fill="#ffd166"/>' +
      '<circle cx="29" cy="60" r="7" fill="#f4978e" opacity="0.55"/>' +
      '<circle cx="71" cy="60" r="7" fill="#f4978e" opacity="0.55"/>' +
      '<circle class="eye" cx="35" cy="43" r="5.2" fill="#1e293b"/>' +
      '<circle class="eye" cx="65" cy="43" r="5.2" fill="#1e293b"/>' +
      '<path d="M30 36 Q35 32 40 36" stroke="#b98a3f" stroke-width="2.2" fill="none" stroke-linecap="round"/>' +
      '<path d="M60 36 Q65 32 70 36" stroke="#b98a3f" stroke-width="2.2" fill="none" stroke-linecap="round"/>' +
      '<ellipse class="mouth" cx="50" cy="68" rx="11" ry="3.2" fill="#7c2d12"/>' +
      '</svg>';
    char.appendChild(face);
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
    if (av.lottieAnim) av.lottieAnim.play();
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
      av.host.style.top = "auto";
      av.host.style.bottom = "90px";
      Object.assign(av.host.style, (PATHS[av.path] || PATHS.wander)(av.idx - 1));
    }

    /* show bubble + animate the mouth while this line is spoken */
    av.bubble.textContent = line.say;
    av.bubble.classList.add("visible");
    av.host.classList.add("lc-avatar-talking");

    speak(line.say, av.voice, av.tune, function () {
      av.host.classList.remove("lc-avatar-talking");
      av.bubble.classList.remove("visible");
      setTimeout(function () { nextLine(id); }, 500);
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
