{%- comment -%}
Avatar — speaking overlay character driven by Web Speech API + Lottie animation.

Usage:
  ```yaml
  name: "Prof. LC"
  script:
    - "Hello! Let's explore Python objects together."
    - "An object has attributes — the data it holds."
    - "And methods — the behaviors it can perform."
  path: wander
  voice: en-US
  lottie: "https://assets2.lottiefiles.com/packages/lf20_fnbsl4ky.json"
  ```
  {: .avatar }

  [▶ Play](#)
  {: .avatar-trigger target="my-avatar" label-stop="⏹ Stop" }

Attributes on .avatar:
  id        — referenced by .avatar-trigger's target=""
  path      — left | center | right | wander (default: wander)
  voice     — BCP-47 tag (default: first available)
  lottie    — URL to a Lottie JSON animation (optional)
  autoplay  — "true" to start on page load (default: false)
  size      — pixel size of the character bubble (default: 120)

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* ── overlay host ────────────────────────────────────── */
.lc-avatar-host {
  position: fixed; bottom: 90px; z-index: 900;
  pointer-events: none;
  transition: left 1.6s cubic-bezier(.4,0,.2,1),
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
/* built-in SVG face */
.lc-avatar-face {
  width: 80%; height: 80%;
  display: flex; align-items: center; justify-content: center;
  font-size: 2.6em; line-height: 1; user-select: none;
}
/* Lottie fills the bubble */
.lc-avatar-lottie { width: 100%; height: 100%; }
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

  /* ── path helpers ──────────────────────────────────── */
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
  function speak(text, voiceTag, onWord, onEnd) {
    if (!window.speechSynthesis) { onEnd && onEnd(); return; }
    window.speechSynthesis.cancel();
    var utt = new SpeechSynthesisUtterance(text);
    utt.rate = 0.95; utt.pitch = 1.05;
    if (voiceTag) {
      var voices = window.speechSynthesis.getVoices();
      var match = voices.find(function (v) { return v.lang.startsWith(voiceTag); });
      if (match) utt.voice = match;
    }
    utt.onboundary = function (e) { if (onWord) onWord(e); };
    utt.onend = function () { if (onEnd) onEnd(); };
    window.speechSynthesis.speak(utt);
  }

  /* ── upgrade .avatar code block ───────────────────── */
  var AVT_ID = 0;
  function upgradeAvatar(el) {
    if (el.dataset.lcAvatarDone) return;
    el.dataset.lcAvatarDone = "1";

    var raw  = (el.querySelector("code") || el).textContent.trim();
    var size = parseInt(el.getAttribute("size") || "120", 10);
    var elId = el.id || ("avt" + (++AVT_ID));
    el.style.display = "none"; /* hide source block */

    loadYaml().then(function (jsyaml) {
      var cfg = {};
      try { cfg = (jsyaml ? jsyaml.load(raw) : JSON.parse(raw)) || {}; } catch (e) {}

      var script   = Array.isArray(cfg.script) ? cfg.script : [];
      var pathName = cfg.path  || "wander";
      var voiceTag = cfg.voice || "";
      var lottieUrl= cfg.lottie || "";
      var autoplay = cfg.autoplay === true || el.getAttribute("autoplay") === "true";

      /* build overlay host */
      var host = document.createElement("div");
      host.className = "lc-avatar-host";
      host.id = "lc-avatar-" + elId;
      host.setAttribute("data-lc-id", elId);
      host.style.left = "6vw";

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
        lottie: lottieUrl, size: size,
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
        if (!lottie) { addFallbackFace(char); return; }
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
      addFallbackFace(char);
    }
  }

  function addFallbackFace(char) {
    var face = document.createElement("div");
    face.className = "lc-avatar-face";
    face.textContent = "🗣️";
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
    window.speechSynthesis && window.speechSynthesis.cancel();
    if (av.lottieAnim) av.lottieAnim.stop();
    av.bubble.classList.remove("visible");
    updateTriggers(id);
  }

  function nextLine(id) {
    var av = window._lcAvatars[id];
    if (!av || !av.playing) return;
    if (av.idx >= av.script.length) { stopPlay(id); return; }

    var line = String(av.script[av.idx]);
    av.idx++;

    /* move character */
    var pos = (PATHS[av.path] || PATHS.wander)(av.idx - 1);
    Object.assign(av.host.style, pos);

    /* show bubble */
    av.bubble.textContent = line;
    av.bubble.classList.add("visible");

    speak(line, av.voice, null, function () {
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
  function init(root) {
    (root || document).querySelectorAll(".highlighter-rouge.avatar, pre.avatar").forEach(upgradeAvatar);
    (root || document).querySelectorAll("p.avatar-trigger, a.avatar-trigger").forEach(upgradeTrigger);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { init(); });
  else init();

  var _os = window.lcScanElement;
  window.lcScanElement = function (root) {
    if (_os) _os(root);
    (root || document).querySelectorAll(".highlighter-rouge.avatar, pre.avatar").forEach(upgradeAvatar);
    (root || document).querySelectorAll("p.avatar-trigger, a.avatar-trigger").forEach(upgradeTrigger);
  };

})();
</script>
