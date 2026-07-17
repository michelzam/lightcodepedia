{%- comment -%}
Avatar — speaking overlay character that narrates content and follows the
elements it describes. Voice: per-line audio files (studio TTS, with real
amplitude lip-sync) or the Web Speech API. Face: built-in animated "Prof. LC"
SVG (professor glasses, expressive brows, bow tie; blinks, breathes, eyes and
head turn toward the spotlighted element, mouth follows the audio), any Lottie
animation, a Rive state machine, or a recorded video.

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
  {: .avatar_trigger target="prof" label-stop="⏹ Stop" }

  (snake_case class names are canonical; avatar-trigger etc. remain as aliases)

Script lines are strings (the avatar wanders) or objects:
  at:    the id of the component (or heading) to walk to — scroll there, park
         beside it, spotlight it. Bare ids resolve wherever the platform put
         the element (#id, data-lc-id, form wrapper); any CSS selector also works
  say:   the line (spoken + shown in the bubble)
  audio: URL of a pre-generated audio file — plays instead of browser TTS,
         and the mouth follows the actual waveform. Generate these FROM the
         script text with packages/gen-audio.mjs (ElevenLabs, content-addressed
         so unchanged lines are never re-billed); missing files fall back to TTS
  input: drive the Rive character's state machine for this line —
         "bark" fires the trigger named bark, { run: true, speed: 7 }
         sets boolean/number inputs (also available inside cues)
  pause: seconds to hold after this line finishes, before the next one
         (default 0.5s). A video cue can take pause: too — after its actions
         the take pauses that many seconds, then resumes on its own.

Attributes on .avatar:
  id        — referenced by .avatar-trigger's target=""
  path      — left | center | right | wander (fallback for untargeted lines)
  voice     — BCP-47 tag; the best-quality matching browser voice is picked
              (default: the page language — en-US). "off" = silent: the
              bubble shows each line, dwells, moves on
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
  step      — "true" for step-by-step playback: a click on the trigger (or the
              character) advances one beat and waits (▶ Start → Next → ↺ Replay);
              a recorded take instead pauses/resumes at the current time index
              (⏸ / ▶). Per-beat overrides: a script line `step: false` chains on
              without stopping; `step: true` stops at that line even when the
              avatar isn't in step mode; a video cue `step: true` forces a stop
              at that cue.
  size      — pixel size of the character bubble (default: 140)
  bot       — a bot name (docs/bots/<name>.md): the docked guide gains 💬 Ask —
              questions go to that bot (agent brain, learner's own PAT, page
              knowledge) and the ANSWER is played as guided steps: a reply
              line "[form_id] Change the treats." walks there while speaking.
              The guide only ever walks, points and talks — never acts.
  dock      — "true": dock this avatar as the page's GUIDE — a small face in
              the bottom-right corner; tap → ▶ play tour · next · ⏹ stop.
              The full character hides while idle (the seed represents it) and
              appears only while performing. One silent "need a tour?" bubble
              on a visitor's first page, ever. Right-click (long-press) on the
              performing character opens the same verbs beside it.
  face.zoom — enlarge the facial features only (eyes, mouth…) — pair with a
              smaller size for a compact character with same-size features.
  face      — make the built-in character look like its author (all optional):
                face:
                  skin: "#e2a87e"       # head colour (default: LC yellow)
                  glasses: square       # round (default) | square | none
                  beard: "#e8e4de"      # goatee+mustache colour, or none
                  brows: "#4a3b30"      # eyebrow colour
                  hair: none            # none (default) | sides | full
                  hair_color: "#c9c9c9"
                  wear: shirt           # bow (default) | shirt | none
                  wear_color: "#3b4046"
                  head: oval            # round (default) | oval
                  blush: false          # default true
  elevenlabs — an ElevenLabs voice id (or { voice, model }): playback then
              looks for the pre-generated studio file of each line
              (/assets/audio/lc-<hash-of-voice|model|text>.mp3 — same naming
              as packages/gen-audio.mjs) and falls back to TTS if absent.

Voices studio (authoring, in the browser — no terminal):
  [🎙️ Generate voices](#)
  {: .avatar_voices target="prof" }
  Generates the missing studio files for that avatar's script: calls the
  ElevenLabs API from THIS browser (key prompted once, stored in this browser
  only as lc_11_key — same family as the editor's lc_ed_pat), previews the new
  audio immediately, and commits each mp3 to the repo via the GitHub contents
  API using the ✏️ editor's PAT + repo (lc_ed_pat / lc_ed_repo). Unchanged
  lines are content-addressed → never re-billed.

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
.lc-avatar-face { width: 100%; height: 100%; transition: transform 0.5s ease; } /* head tilts toward the target */
.lc-avatar-face svg { width: 100%; height: 100%; display: block; }
.lc-avatar-face .eye-g,
.lc-avatar-face .mouth,
.lc-avatar-face .brow { transform-box: fill-box; transform-origin: center; }
.lc-avatar-face .eye-g { animation: lc-avt-blink 4.2s infinite; }
.lc-avatar-face .pupil { transition: transform 0.3s ease; }
/* brows lift and settle while speaking */
.lc-avatar-talking .lc-avatar-face .brow { animation: lc-avt-brow 1.1s ease-in-out infinite; }
@keyframes lc-avt-brow {
  0%, 100% { transform: translateY(0); }
  30%      { transform: translateY(-1.6px); }
  60%      { transform: translateY(-0.4px); }
}
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
/* ── guide seed: the docked companion (dock="true") ──── */
/* when a page docks its guide, the SEED is the idle presence — the full
   character appears only while performing (and melts away after) */
.lc-avatar-host.lc-avatar-docked:not([data-state="speaking"]) {
  opacity: 0; pointer-events: none; transition: opacity 0.4s ease;
}
.lc-guide-seed {
  position: fixed; right: 16px; bottom: 16px; z-index: 940;
  width: 46px; height: 46px; border-radius: 50%;
  border: 1px solid #d8dee6; background: #fff; padding: 2px;
  cursor: pointer; box-shadow: 0 3px 12px rgba(0,0,0,0.16);
  transition: transform 0.15s ease;
}
.lc-guide-seed:hover { transform: scale(1.08); }
.lc-guide-seed:focus-visible { outline: 2px solid #0066cc; outline-offset: 2px; }
.lc-guide-seed svg { width: 100%; height: 100%; display: block; border-radius: 50%; }
@media (max-width: 700px) { .lc-guide-seed { bottom: 12px; right: 12px; } }
.lc-guide-menu {
  position: fixed; right: 16px; bottom: 70px; z-index: 941;
  display: none; flex-direction: column; min-width: 150px;
  background: #fff; border: 1px solid #d8dee6; border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.18); overflow: hidden;
}
.lc-guide-menu.open { display: flex; }
.lc-guide-menu button {
  border: none; background: none; text-align: left; cursor: pointer;
  padding: 0.55em 0.9em; font: inherit; font-size: 0.9em; color: #1f2937;
  border-bottom: 1px solid #f1f3f6;
}
.lc-guide-menu button:last-child { border-bottom: none; }
.lc-guide-menu button:hover { background: #f0f6ff; }
.lc-guide-ask {
  position: fixed; right: 16px; bottom: 70px; z-index: 941;
  display: none; flex-direction: column; gap: 6px; width: min(320px, calc(100vw - 32px));
  background: #fff; border: 1px solid #d8dee6; border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.18); padding: 10px;
}
.lc-guide-ask.open { display: flex; }
.lc-guide-ask textarea, .lc-guide-ask input[type=password] {
  width: 100%; box-sizing: border-box; padding: 0.5em 0.6em;
  border: 1px solid #ccc; border-radius: 6px; font: inherit; font-size: 0.9em;
}
.lc-guide-ask input[type=text] { position: absolute; left: -9999px; }
.lc-guide-ask-row { display: flex; gap: 6px; justify-content: flex-end; }
.lc-guide-ask button {
  border: none; border-radius: 6px; padding: 0.45em 0.9em; cursor: pointer;
  font: inherit; font-size: 0.88em; font-weight: 600; background: #0066cc; color: #fff;
}
.lc-guide-ask button:hover { background: #0052a3; }
.lc-guide-ask-hint { font-size: 0.76em; color: #6b7280; margin: 0; }
.lc-guide-hello {
  position: fixed; right: 70px; bottom: 22px; z-index: 941;
  background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
  padding: 6px 12px; font-size: 0.85em; color: #1e293b;
  box-shadow: 0 2px 10px rgba(0,0,0,0.10);
}
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
    /* no explicit voice → key on the page's language (en-US here). Without
       this the quality ranking ran over EVERY installed voice, so another
       language's "enhanced" voice could win and narrate the page with a
       foreign accent. Fallback relaxes region before language: exact tag
       (en-us) → base language (en) → anything. */
    if (!tag) tag = document.documentElement.lang || "en-US";
    tag = String(tag).toLowerCase().replace("_", "-");
    var byLang = function (t) {
      return _voices.filter(function (v) {
        return (v.lang || "").toLowerCase().replace("_", "-").indexOf(t) === 0;
      });
    };
    var cand = byLang(tag);
    if (!cand.length && tag.indexOf("-") > 0) cand = byLang(tag.split("-")[0]);
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
    /* also set the utterance language: if the voices list hasn't populated yet
       (it loads async), the synth then still picks a matching-language default
       instead of the OS voice */
    utt.lang = voiceTag || document.documentElement.lang || "en";
    var v = pickVoice(voiceTag);
    if (v) utt.voice = v;
    utt.onboundary = function (e) { if (onBoundary) onBoundary(e); };
    utt.onend = function () { if (onEnd) onEnd(); };
    window.speechSynthesis.speak(utt);
  }

  /* ── audio lines: real lip-sync from the waveform ─────
     ONE persistent element per avatar, "blessed" inside the user's tap:
     iOS only allows sound that starts in a gesture (or on an element that
     already played in one). A fresh Audio() per line therefore worked only
     while line 1 happened to carry audio — one TTS first line and every
     later play() was silently blocked. Priming a reusable element with
     40ms of silence during the tap makes every later line legal — and the
     analyser wires once (re-attaching to new elements is forbidden anyway). */
  var SILENCE = "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQAAAAA=";
  function voiceEl(av) {
    if (av.voiceAudio) return av.voiceAudio;
    var a = new Audio();
    a.setAttribute("playsinline", "");
    a.crossOrigin = "anonymous";
    av.voiceAudio = a;
    return a;
  }
  function primeVoice(av) {   /* call synchronously from a click handler */
    if (av._voicePrimed) return;
    av._voicePrimed = true;
    try {
      var a = voiceEl(av);
      a.muted = true; a.src = SILENCE;
      a.play().catch(function () { av._voicePrimed = false; });
      var AC = window.AudioContext || window.webkitAudioContext;
      if (AC && !av.actx) av.actx = new AC();
      if (av.actx && av.actx.state === "suspended") av.actx.resume();
    } catch (e) { av._voicePrimed = false; }
  }
  function stopAudio(av) {
    if (av.audioEl) { try { av.audioEl.pause(); } catch (e) {} }
    av.analyser = null;
  }
  function playAudio(av, url, onEnd, onErr) {
    stopAudio(av);
    var a = voiceEl(av);
    av.audioEl = a;
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (AC && !av.analyser0) {
        var ctx = av.actx || (av.actx = new AC());
        var src = ctx.createMediaElementSource(a);   /* once per element */
        var an = ctx.createAnalyser();
        an.fftSize = 256;
        src.connect(an); an.connect(ctx.destination);
        av.analyser0 = an;
      }
      if (av.actx && av.actx.state === "suspended") av.actx.resume();
      av.analyser = av.analyser0 || null;
      if (av.analyser) mouthLoop(av);
    } catch (e) { /* no analyser → CSS flap still runs */ }
    a.muted = false;
    if (a.getAttribute("src") !== url) a.src = url;
    try { a.currentTime = 0; } catch (e) {}
    var done = function () { stopAudio(av); resetMouth(av); onEnd(); };
    var fail = function () { stopAudio(av); resetMouth(av); (onErr || onEnd)(); };
    a.onended = done;
    a.onerror = fail;                 /* missing/unreachable file → caller's fallback */
    a.play().catch(fail);
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

  /* ── runtime video source (set from a form field, never in the repo) ──
     window.lcAvatarSetVideo(id, url): a direct .mp4/.webm plays through the
     avatar's <video> (alpha + frame-accurate cues); a YouTube link plays via
     the embed, with a <video>-like shim so the same cue logic still runs. */
  function _ytId(u) {
    var m = String(u).match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{6,})/);
    return m ? m[1] : "";
  }
  function _isYouTube(u) { return !!_ytId(u); }
  function _loadYTApi(cb) {
    if (window.YT && window.YT.Player) { cb(); return; }
    (window._lcYTQ = window._lcYTQ || []).push(cb);
    if (window._lcYTApiLoading) return;
    window._lcYTApiLoading = true;
    var prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = function () {
      if (prev) { try { prev(); } catch (e) {} }
      var q = window._lcYTQ || []; window._lcYTQ = [];
      q.forEach(function (f) { try { f(); } catch (e) {} });
    };
    var s = document.createElement("script");
    s.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(s);
  }
  function _ytTeardown(av) {
    if (!av) return;
    if (av._ytTimer)  { clearInterval(av._ytTimer); av._ytTimer = null; }
    if (av._ytPlayer) { try { av._ytPlayer.destroy(); } catch (e) {} av._ytPlayer = null; }
    var face = av.char && av.char.querySelector(".lc-avatar-face");
    if (face) face.style.display = "";
    if (av.videoEl) av.videoEl.style.display = "";
  }

  window.lcAvatarSetVideo = function (id, url) {
    var av = window._lcAvatars && window._lcAvatars[id];
    if (!av) return;
    url = String(url || "").trim();
    av.runtimeVideo = url;
    if (!url) return;
    if (_isYouTube(url)) { _loadYTApi(function () {}); return; }  /* warm the API; player built on play */
    /* direct file URL: face/TTS avatars have no <video> — build one now */
    if (!av.videoEl) {
      var v = document.createElement("video");
      v.className = "lc-avatar-video";
      v.muted = true; v.preload = "metadata"; v.setAttribute("playsinline", "");
      var face = av.char.querySelector(".lc-avatar-face"); if (face) face.style.display = "none";
      av.char.appendChild(v);
      av.videoEl = v;
    }
    av.videoEl.style.display = "";
    if (av.videoEl.getAttribute("src") !== url) av.videoEl.src = url;
  };

  /* play a YouTube clip in the avatar bubble; returns a <video>-like shim
     (currentTime/paused/ended/play/pause/timeupdate) so attachCues, togglePlay
     and stopPlay drive it exactly like a recorded <video>. */
  function playYouTubeLine(av, url, onEnd) {
    var vid = _ytId(url);
    if (!vid) { onEnd(); return null; }
    _ytTeardown(av);
    if (av.videoEl) { try { av.videoEl.pause(); } catch (e) {} av.videoEl.style.display = "none"; }
    var face = av.char.querySelector(".lc-avatar-face"); if (face) face.style.display = "none";
    var mount = document.createElement("div");
    mount.className = "lc-avatar-video";
    mount.style.cssText = "width:100%;height:100%";
    av.char.appendChild(mount);
    var ended = false, listeners = [];
    var shim = {
      get currentTime() { try { return av._ytPlayer ? (av._ytPlayer.getCurrentTime() || 0) : 0; } catch (e) { return 0; } },
      get paused()  { try { return av._ytPlayer ? av._ytPlayer.getPlayerState() !== 1 : true; } catch (e) { return true; } },
      get ended()   { return ended; },
      play:  function () { try { av._ytPlayer && av._ytPlayer.playVideo(); } catch (e) {} return Promise.resolve(); },
      pause: function () { try { av._ytPlayer && av._ytPlayer.pauseVideo(); } catch (e) {} },
      addEventListener: function (ev, fn) {
        if (ev !== "timeupdate") return;
        listeners.push(fn);
        if (!av._ytTimer) av._ytTimer = setInterval(function () { listeners.forEach(function (f) { f(); }); }, 150);
      },
      removeEventListener: function (ev, fn) {
        listeners = listeners.filter(function (x) { return x !== fn; });
        if (av._ytTimer && !listeners.length) { clearInterval(av._ytTimer); av._ytTimer = null; }
      }
    };
    av._media = shim;
    _loadYTApi(function () {
      try {
        av._ytPlayer = new window.YT.Player(mount, {
          width: "100%", height: "100%", videoId: vid,
          playerVars: { autoplay: 1, controls: 0, rel: 0, modestbranding: 1,
                        playsinline: 1, fs: 0, disablekb: 1, iv_load_policy: 3, cc_load_policy: 0 },
          events: {
            onReady: function (e) {
              try {
                var f = e.target.getIframe();
                /* fill the round avatar with a 16:9 cover and push YouTube's
                   chrome (top title, bottom progress + logo) outside the
                   circular crop; pointer-events:none kills the hover bar and
                   centre button — taps fall through to the avatar/trigger */
                f.style.border = "0";
                f.style.height = "100%";
                f.style.width = "177.78%";
                f.style.marginLeft = "-38.89%";
                f.style.pointerEvents = "none";
                e.target.playVideo();
              } catch (_) {}
            },
            onStateChange: function (e) { if (e.data === window.YT.PlayerState.ENDED) { ended = true; onEnd(); } }
          }
        });
      } catch (e) { onEnd(); }
    });
    return shim;
  }

  function playVideoLine(av, url, onEnd) {
    var rt = av.runtimeVideo || "";
    if (rt && _isYouTube(rt)) return playYouTubeLine(av, rt, onEnd);
    var v = av.videoEl;
    if (!v) { onEnd(); return null; }
    /* runtime URL wins; else per-line url override; else the <source> list */
    var src = rt || ((url && url !== "true") ? url : "");
    if (src && v.getAttribute("src") !== src) v.src = src;
    v.style.display = "";
    v.muted = false;
    try { v.currentTime = 0; } catch (e) {}
    v.onended = function () { v.muted = true; onEnd(); };
    v.onerror = function () { onEnd(); };
    v.play().catch(function (e) {
      /* A pause:/step: cue on the very first beat calls pause() while this
         play() is still starting, so the browser rejects it with AbortError.
         That is NOT the clip ending — swallow it so the cues stay attached and
         the pause's own timer resumes playback. Real failures (bad/empty source)
         reject with a different name and still fall through to onEnd. */
      if (e && e.name === "AbortError") return;
      onEnd();
    });
    av._media = v;
    return v;
  }

  /* ── timed cues inside one recorded take ─────────────
     cues: [{ t: seconds, at: selector, say: caption, slide: next|prev|start|exit }]
     While the media plays, each cue fires when currentTime crosses t: the
     character walks to `at`, the caption changes to `say`, slides advance. */
  function attachCues(av, media, cues, id) {
    if (!media || !Array.isArray(cues) || !cues.length) return;
    var sorted = cues.slice().sort(function (a, b) { return (Number(a.t) || 0) - (Number(b.t) || 0); });
    var i = 0;
    var onTime = function () {
      while (i < sorted.length && media.currentTime >= (Number(sorted[i].t) || 0)) {
        var c = sorted[i]; applyCue(av, c); i++;
        /* a cue can force a stop even when the avatar isn't in step mode:
           pause the take here and let a click resume it */
        if (c.step) { try { media.pause(); } catch (e) {} av._videoStep = true;
          if (id) updateTriggers(id); break; }
        /* or hold for a fixed beat: after the cue's actions, pause the take
           c.pause seconds, then resume on its own (before the next cue) */
        if (c.pause) { try { media.pause(); } catch (e) {}
          setTimeout(function () { try { media.play().catch(function () {}); } catch (e) {} },
                     (Number(c.pause) || 0) * 1000);
          break; }
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

  /* ── script lines: "text" or { at, say, audio } ─────── */
  function lineSpec(x) {
    if (x && typeof x === "object") {
      return { at: String(x.at || ""), say: String(x.say || x.text || ""),
               audio: String(x.audio || ""), video: String(x.video || ""),
               input: x.input || null,
               cues: Array.isArray(x.cues) ? x.cues : [],
               fn: (typeof x.fn === "function" ? x.fn : null),  /* action hook run as the line starts (lcAvatarPlay callers — e.g. demo replay re-applying a recorded edit) */
               step: (x.step === undefined ? null : x.step),   /* per-line override of the avatar's step */
               pause: (x.pause === undefined ? null : Number(x.pause)) };   /* seconds to hold after this line */
    }
    return { at: "", say: String(x), audio: "", video: "", input: null, cues: [], fn: null, step: null, pause: null };
  }

  /* resolve an at:/target reference the pythonistic way: a bare component id
     finds the element wherever the platform put it (#id, a component's
     data-lc-id, or a form's prefixed DOM id) — authors never write selectors.
     Full CSS selectors still work for power users. Shared with modelcheck so
     the integrity gate and the walk agree on what resolves. */
  function resolveRef(ref) {
    ref = String(ref || "").trim();
    if (!ref) return null;
    if (/^[A-Za-z_][A-Za-z0-9_-]*$/.test(ref)) {
      return document.getElementById(ref)
          || document.querySelector('[data-lc-id="' + ref + '"]')
          || document.getElementById("lc-form-" + ref);
    }
    try { return document.querySelector(ref); } catch (e) { return null; }
  }
  window.lcAvatarResolve = resolveRef;

  /* park the character beside the element it describes; eyes follow it */
  function anchorTo(av, sel) {
    var t = resolveRef(sel);
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

  /* pupils glance toward a viewport point; the head tilts the same way */
  function lookAt(av, x, y) {
    if (!av.pupils) return;
    var r = av.char.getBoundingClientRect();
    var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    var dx = x - cx, dy = y - cy, L = Math.hypot(dx, dy) || 1;
    var m = 2.4;
    av.pupils.forEach(function (p) {
      p.style.transform = "translate(" + (dx / L * m) + "px," + (dy / L * m) + "px)";
    });
    if (av.faceEl) av.faceEl.style.transform = "rotate(" + (dx / L * 5) + "deg)";
  }
  function lookIdle(av) {
    if (!av.pupils) return;
    var a = Math.random() * Math.PI * 2, m = Math.random() * 1.8;
    av.pupils.forEach(function (p) {
      p.style.transform = "translate(" + (Math.cos(a) * m) + "px," + (Math.sin(a) * m) + "px)";
    });
    if (av.faceEl) av.faceEl.style.transform = "rotate(" + (Math.random() * 3 - 1.5) + "deg)";
  }

  /* ── upgrade .avatar code block ───────────────────── */
  var AVT_ID = 0, AVT_SLOT = 0;
  /* the ✏️ editor's live preview runs the upgrade pipeline on its own copy of
     the page — an overlay character spawned from THERE would duplicate the
     real one (ghost avatar, overwritten registry, two voices at once) */
  function inEditorPreview(el) { return !!(el.closest && el.closest("#ed-preview")); }
  function upgradeAvatar(el) {
    if (el.dataset.lcAvatarDone) return;
    if (inEditorPreview(el)) return;
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
      var mute     = voiceTag === "off";           /* voice: off → silent bubbles */
      if (mute) voiceTag = "";
      /* elevenlabs: <voice_id> (or { voice, model }) — studio files are
         content-addressed, so playback can compute each line's URL itself */
      var gen = cfg.elevenlabs || "";
      var genVoice = (gen && typeof gen === "object") ? String(gen.voice || "") : String(gen || "");
      var genModel = (gen && typeof gen === "object" && gen.model) ? String(gen.model) : "eleven_multilingual_v2";
      if (genVoice && window.crypto && window.crypto.subtle) {
        script.forEach(function (l) {
          if (l.audio || l.video || !l.say) return;
          sha1hex(genVoice + "|" + genModel + "|" + String(l.say).trim()).then(function (h) {
            l.audio = "/assets/audio/lc-" + h.slice(0, 16) + ".mp3";
          });
        });
      }
      /* no config at all: the page's voice manifest maps each line's text to
         its committed studio file (missing lines just fall back to TTS) */
      if (window.crypto && window.crypto.subtle) {
        voxManifest().then(function (man) {
          var map = man && man[voxSlug()] && man[voxSlug()][elId];
          if (!map) return;
          script.forEach(function (l) {
            if (l.audio || l.video || !l.say) return;
            sha1hex(String(l.say).trim()).then(function (h) {
              var f = map[h.slice(0, 16)];
              if (f && !l.audio) l.audio = "/assets/audio/" + f;
            });
          });
        });
      }
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

      /* safety net: an avatar id is unique — if any stray re-upgrade already
         registered it, retire the older host and its timers first (no ghosts,
         no two-voice overlap, one instance owns the id) */
      var prevAv = (window._lcAvatars || {})[elId];
      if (prevAv) {
        try { clearInterval(prevAv._idleT); } catch (e) {}
        if (prevAv.host && prevAv.host.parentNode) { try { prevAv.host.parentNode.removeChild(prevAv.host); } catch (e) {} }
      }

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
        faceCfg: (cfg.face && typeof cfg.face === "object") ? cfg.face : null,
        size: size, spot: null,
        pupils: null, mouth: null, audioEl: null, videoEl: null, analyser: null,
        playing: false, idx: 0, lottieDone: false, step: step, mute: mute,
        genVoice: genVoice, genModel: genModel,
        botName: (cfg.bot ? String(cfg.bot) : "")
      };

      /* init character graphic */
      initChar(elId, char, size);

      /* dock="true" (or face knob dock: true): the page declares its guide —
         a small seed in the bottom-right, zero moves from the learner */
      if (el.getAttribute('dock') === 'true' || cfg.dock === true) buildSeed(elId, av);

      /* idle saccades keep the built-in face alive */
      av._idleT = setInterval(function () { if (!av.playing) lookIdle(av); }, 3200);

      /* click to play/stop; right-click (or long-press) → local verb menu */
      char.addEventListener("click", function () { togglePlay(elId); });
      char.addEventListener("contextmenu", function (e) { e.preventDefault(); openVerbMenu(elId, av); });

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

  /* built-in face — a parametric "Prof." character: every feature is a fence
     knob (face: skin / glasses / beard / brows / hair / wear) so the guide can
     look like its author. Defaults reproduce Prof. LC. Blinks, breathes, brows
     lift while speaking, eyes and head track the spotlight, mouth follows the
     voice. Fully procedural: no assets, any new text forever. */
  var FACE_ID = 0;
  function shade(hex, f) {   /* f in -1..1 → darken..lighten */
    var m = /^#?([0-9a-f]{6})$/i.exec(String(hex || "")); if (!m) return hex;
    var n = parseInt(m[1], 16), r = n >> 16, gg = (n >> 8) & 255, b = n & 255;
    var t = f < 0 ? 0 : 255, p = Math.abs(f);
    r = Math.round(r + (t - r) * p); gg = Math.round(gg + (t - gg) * p); b = Math.round(b + (t - b) * p);
    return "#" + ((1 << 24) + (r << 16) + (gg << 8) + b).toString(16).slice(1);
  }
  function buildFaceSvg(cfg) {
    cfg = cfg || {};
    var skin = cfg.skin || "#ffd166", custom = !!cfg.skin;
    var brows = cfg.brows || (custom ? shade(skin, -0.55) : "#8a6428");
    var glasses = cfg.glasses || "round";                 /* round | square | none */
    var beard = (cfg.beard && cfg.beard !== "none") ? cfg.beard : "";
    var hair = cfg.hair || "none", hairC = cfg.hair_color || "#c9c9c9";
    var wear = cfg.wear || "bow";                         /* bow | shirt | none */
    var wearC = cfg.wear_color || (wear === "shirt" ? "#3a3f45" : "#0066cc");
    var head = cfg.head || "round";                       /* round | oval */
    var zoom = parseFloat(cfg.zoom) || 1;                 /* enlarge features only (head/wear stay) */
    var g = "lcFaceG" + (++FACE_ID);   /* unique gradient id per instance */
    var s0 = custom ? shade(skin, 0.22) : "#ffe4a3";
    var s2 = custom ? shade(skin, -0.12) : "#f0b445";
    var nose = custom ? shade(skin, -0.3) : "#d9a441";
    var svg = '<svg viewBox="0 0 100 100" aria-hidden="true">'
      + '<defs><radialGradient id="' + g + '" cx="38%" cy="30%" r="80%">'
      + '<stop offset="0%" stop-color="' + s0 + '"/><stop offset="55%" stop-color="' + skin + '"/>'
      + '<stop offset="100%" stop-color="' + s2 + '"/></radialGradient></defs>'
      + (head === "oval"
          ? '<ellipse cx="50" cy="50" rx="43" ry="50" fill="url(#' + g + ')"/>'
          : '<circle cx="50" cy="50" r="50" fill="url(#' + g + ')"/>')
      + '<ellipse cx="50" cy="93" rx="42" ry="15" fill="rgba(60,40,20,0.06)"/>'
      + (zoom !== 1 ? '<g transform="translate(50 52) scale(' + zoom + ') translate(-50 -52)">' : '');
    if (hair === "full") svg += '<path d="M8 40 Q10 12 50 10 Q90 12 92 40 Q70 20 50 20 Q30 20 8 40 Z" fill="' + hairC + '"/>';
    if (hair === "sides") svg += '<path d="M4 46 Q2 72 22 86 Q10 66 14 47 Z" fill="' + hairC + '"/>'
      + '<path d="M96 46 Q98 72 78 86 Q90 66 86 47 Z" fill="' + hairC + '"/>';
    if (cfg.blush !== false) svg += '<circle cx="26" cy="62" r="6.5" fill="#f4978e" opacity="0.4"/>'
      + '<circle cx="74" cy="62" r="6.5" fill="#f4978e" opacity="0.4"/>';
    svg += '<path class="brow" d="M25 31 Q33 26 42 30" stroke="' + brows + '" stroke-width="2.8" fill="none" stroke-linecap="round"/>'
      + '<path class="brow" d="M58 30 Q67 26 75 31" stroke="' + brows + '" stroke-width="2.8" fill="none" stroke-linecap="round"/>';
    var frame = "#2e3947";
    if (glasses === "square") {
      svg += '<rect x="21.5" y="34" width="24" height="19" rx="4.5" fill="rgba(255,255,255,0.72)" stroke="' + frame + '" stroke-width="2.6"/>'
        + '<rect x="54.5" y="34" width="24" height="19" rx="4.5" fill="rgba(255,255,255,0.72)" stroke="' + frame + '" stroke-width="2.6"/>'
        + '<path d="M45.5 40 Q50 38.5 54.5 40" stroke="' + frame + '" stroke-width="2.4" fill="none" stroke-linecap="round"/>';
    } else if (glasses === "round") {
      svg += '<circle cx="34" cy="44" r="11" fill="rgba(255,255,255,0.75)" stroke="#334155" stroke-width="2.4"/>'
        + '<circle cx="66" cy="44" r="11" fill="rgba(255,255,255,0.75)" stroke="#334155" stroke-width="2.4"/>'
        + '<path d="M45 43 Q50 40 55 43" stroke="#334155" stroke-width="2.4" fill="none" stroke-linecap="round"/>';
    } else {
      svg += '<circle cx="34" cy="44" r="8" fill="#fff" stroke="' + shade(skin, -0.18) + '" stroke-width="1"/>'
        + '<circle cx="66" cy="44" r="8" fill="#fff" stroke="' + shade(skin, -0.18) + '" stroke-width="1"/>';
    }
    svg += '<g class="eye-g"><g class="pupil"><circle cx="34" cy="45" r="4.6" fill="#4a3120"/><circle cx="35.6" cy="43.2" r="1.5" fill="#fff"/></g></g>'
      + '<g class="eye-g"><g class="pupil"><circle cx="66" cy="45" r="4.6" fill="#4a3120"/><circle cx="67.6" cy="43.2" r="1.5" fill="#fff"/></g></g>'
      + '<path d="M47 56 Q50 59 53 56" stroke="' + nose + '" stroke-width="2.2" fill="none" stroke-linecap="round"/>';
    if (beard) {
      svg += '<path d="M39 73 L61 73 Q61 85 50 88 Q39 85 39 73 Z" fill="' + beard + '"/>'
        + '<path d="M36 63.5 Q50 57.5 64 63.5 Q50 67.5 36 63.5 Z" fill="' + beard + '"/>';
    }
    svg += '<path class="mouth" d="M38 66 Q50 75 62 66 Q50 70.5 38 66 Z" fill="#7c2d12"/>';
    if (zoom !== 1) svg += '</g>';
    if (wear === "shirt") {
      svg += '<path d="M6 86 Q50 104 94 86 L94 101 L6 101 Z" fill="' + wearC + '"/>'
        + '<path d="M6 86 Q50 104 94 86" stroke="' + shade(wearC, 0.18) + '" stroke-width="1.6" fill="none"/>';
    } else if (wear === "bow") {
      svg += '<path d="M50 90 L37 83.5 L37 96.5 Z" fill="' + wearC + '" stroke="' + shade(wearC, -0.22) + '" stroke-width="1.2"/>'
        + '<path d="M50 90 L63 83.5 L63 96.5 Z" fill="' + wearC + '" stroke="' + shade(wearC, -0.22) + '" stroke-width="1.2"/>'
        + '<circle cx="50" cy="90" r="3.4" fill="' + shade(wearC, -0.22) + '"/>';
    }
    return svg + '</svg>';
  }
  function addFace(id, char) {
    var av0 = window._lcAvatars[id] || {};
    var face = document.createElement("div");
    face.className = "lc-avatar-face";
    face.innerHTML = buildFaceSvg(av0.faceCfg || {});
    char.appendChild(face);
    var av = window._lcAvatars[id];
    if (av) {
      av.pupils = Array.prototype.slice.call(face.querySelectorAll(".pupil"));
      av.mouth = face.querySelector(".mouth");
      av.faceEl = face;   /* tilted toward the spotlighted element */
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
    primeVoice(av);   /* we're inside the user's tap — bless the audio element */
    if (!av.playing) {
      startPlay(id);
    } else if (av._waiting) {
      /* paused at a step boundary → advance to the next line */
      av._waiting = false; nextLine(id);
    } else if (av._videoStep && (av._media || av.videoEl) && !(av._media || av.videoEl).ended) {
      /* a recorded take is the step unit → pause/resume at the current time index */
      var m = av._media || av.videoEl;
      if (m.paused) { try { m.play().catch(function () {}); } catch (e) {} }
      else { try { m.pause(); } catch (e) {} }
    } else if (av._curStep || av.step) {
      /* mid-line in a step context → skip ahead to the next line */
      nextLine(id);
    } else {
      /* a normally-playing (non-step) line → stop */
      stopPlay(id);
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
    av._videoStep = null; av._waiting = false; av._curStep = false;
    av.host.setAttribute("data-state", "idle");
    av.host.classList.remove("lc-avatar-talking");
    clearSpot(av);
    stopAudio(av);
    resetMouth(av);
    if (av.videoEl) { try { av.videoEl.pause(); av.videoEl.muted = true; } catch (e) {} }
    if (av._media && av._media !== av.videoEl) { try { av._media.pause(); } catch (e) {} }
    _ytTeardown(av); av._media = null;
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
    /* effective step for THIS line: the line's own step overrides the avatar's */
    av._curStep = (line.step != null) ? !!line.step : !!av.step;
    av._waiting = false;       /* set when paused at a step boundary, click advances */
    av._videoStep = false;     /* set while a recorded take is the step unit */
    if (!line.video) _ytTeardown(av);   /* leaving a video take → drop any YT player */

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
    if (line.fn) { try { line.fn(); } catch (e) {} }   /* per-line action (demo replay re-applies the recorded value here) */

    var finish = function () {
      if (av._cueOff) av._cueOff();
      av.host.classList.remove("lc-avatar-talking");
      charTalk(av, false);
      if (av._curStep) { av._waiting = true; updateTriggers(id); return; }  /* wait for the next click */
      av.bubble.classList.remove("visible");
      /* hold for the line's configured pause (seconds) before the next line — default 0.5s */
      var _gap = (line.pause != null && !isNaN(line.pause)) ? line.pause * 1000 : 500;
      setTimeout(function () { nextLine(id); }, _gap);
    };

    if (line.video) {
      /* recorded narration: real face, real voice — the bubble is a caption.
         When this line is a step, a click pauses/resumes the take at the current
         time index (see togglePlay); the cues just overlay their funny comments. */
      av.bubble.textContent = line.say;
      av._videoStep = av._curStep;
      var media = playVideoLine(av, line.video, finish);
      attachCues(av, media || av.videoEl, line.cues, id);
      return;
    }

    if (line.audio) {
      /* studio voice: bubble shows the full line, mouth follows the waveform.
         If the file is missing/unreachable, fall back to TTS (or a silent
         dwell in mute mode) so the walk never breaks. */
      av.bubble.textContent = line.say;
      playAudio(av, line.audio, finish, function () {
        if (!av.playing) return;   /* the user stopped: play() rejection is not a missing file */
        if (av.mute || !window.speechSynthesis) {
          setTimeout(finish, Math.min(8000, 900 + line.say.split(" ").length * 260));
        } else {
          speak(line.say, av.voice, av.tune, null, finish);
        }
      });
      attachCues(av, av.audioEl, line.cues, id);
      return;
    }

    /* TTS: reveal the bubble word by word as boundaries fire */
    var words = line.say.split(" ");
    /* voice: "off" (or no TTS at all) — silent walkthrough: show the whole
       line and dwell long enough to read it, then move on */
    if (av.mute || !window.speechSynthesis) {
      av.bubble.textContent = line.say;
      setTimeout(finish, Math.min(8000, 900 + words.length * 260));
      return;
    }
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

  /* ── upgrade .avatar-trigger links ──────────────────
     A `pick` knob turns the trigger into a local-file picker instead of a play
     button: it plays a video off your disk as the avatar (an in-memory blob URL
     — never uploaded, committed, or typed; sound + alpha kept). The native
     picker is opened from this *synchronous* click so the user gesture survives
     (a button on_click runs async and the browser would block it). */
  function upgradeTrigger(el) {
    if (el.dataset.lcAvtTrigDone) return;
    if (inEditorPreview(el)) return;
    el.dataset.lcAvtTrigDone = "1";
    var targetId = el.getAttribute("target") || "";
    el.classList.add("lc-avatar-trigger");
    if (el.getAttribute("pick") != null) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        var inp = document.createElement("input");
        inp.type = "file"; inp.accept = "video/*"; inp.style.display = "none";
        inp.addEventListener("change", function () {
          var f = inp.files && inp.files[0];
          if (f && window.lcAvatarSetVideo) window.lcAvatarSetVideo(targetId, URL.createObjectURL(f));
          inp.remove();
        });
        document.body.appendChild(inp);
        inp.click();
      });
      return;
    }
    var labelPlay = el.textContent.trim() || "▶ Play";
    var labelStop = el.getAttribute("label-stop") || "⏹ Stop";
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
    if (inEditorPreview(el)) return;
    el.dataset.lcAvtStudioDone = "1";
    var targetId = el.getAttribute("target") || "";
    el.classList.add("lc-avatar-trigger");
    el.addEventListener("click", function (e) {
      e.preventDefault();
      var av0 = window._lcAvatars && window._lcAvatars[targetId];
      if (av0) primeVoice(av0);   /* the recorder flow starts playback async — bless now */
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
      var txt;
      if (!playing) {
        txt = (av && av.step && av.idx > 0) ? "↺ Replay"
            : (btn.getAttribute("data-avt-play") || (av && av.step ? "▶ Start" : "▶ Play"));
      } else if (av._waiting) {
        txt = "Next →";                                   /* paused at a step boundary */
      } else if (av._videoStep && (av._media || av.videoEl) && !(av._media || av.videoEl).ended) {
        txt = (av._media || av.videoEl).paused ? "▶ Resume" : "⏸ Pause"; /* recorded take in progress */
      } else if (av._curStep || av.step) {
        txt = "Next →";                                   /* a step context, mid-play */
      } else {
        txt = btn.getAttribute("data-avt-stop") || "⏹ Stop";
      }
      btn.textContent = txt;
      btn.classList.toggle("playing", !!playing);
    });
  }

  /* ── guide seed: the docked companion ─────────────────────────────────────
     dock="true" on an avatar fence puts a small face in the bottom-right
     corner — the guide is zero moves away, as the page designer decided.
     Tap → a tiny menu of the avatar's verbs (play / continue / stop). The
     seed never speaks first: one silent "need a tour?" bubble, once ever. */
  /* ── 💬 ask: the guide answers through its own body ────────────────────
     The bot (agent brain via lcBotAsk) replies; the answer is played as
     guided steps. Protocol: a line may start with a component id in square
     brackets — "[demo_form] Change the treats." — Doc walks there while
     saying it. Unresolvable ids degrade to plain speech; a malformed answer
     degrades to bubble lines. Never actions, only walk-point-talk. */
  function parseAnswerSteps(text) {
    var out = [];
    String(text || '').split(/\n+/).forEach(function (raw) {
      var t = raw.trim().replace(/[*`]+/g, '');
      if (!t) return;
      var m = /^\[([A-Za-z_][\w-]*)\]\s*(.+)$/.exec(t);
      var at = '', say = t;
      if (m) { at = m[1]; say = m[2]; }
      if (at && !(window.lcAvatarResolve && window.lcAvatarResolve(at))) at = '';
      while (say.length > 220) {                     /* bubble-sized chunks */
        var cut = say.lastIndexOf('. ', 200);
        if (cut < 60) cut = 200;
        out.push({ at: at, say: say.slice(0, cut + 1).trim(), pause: 0.6 });
        at = ''; say = say.slice(cut + 1).trim();
      }
      if (say) out.push({ at: at, say: say, pause: 0.8 });
    });
    return out.slice(0, 12);
  }
  function guideBubble(av, text) {   /* show the character with a message, engine-off */
    av.host.setAttribute('data-state', 'speaking');
    av.bubble.textContent = text;
    av.bubble.classList.add('visible');
  }
  function guideIdle(av) {
    av.bubble.classList.remove('visible');
    av.host.setAttribute('data-state', 'idle');
  }
  function askDoc(elId, av, question) {
    if (av.playing) stopPlay(elId);
    if (!av._tourScript) av._tourScript = av.script;   /* stash the authored tour */
    guideBubble(av, '🤔 …');
    var restore = function (ev) {
      if (ev && ev.detail && ev.detail.id !== elId) return;
      document.removeEventListener('lc-avatar-ended', restore);
      if (av._tourScript) { av.script = av._tourScript; av._tourScript = null; av.idx = 0; }
    };
    window.lcBotAsk.ask(av.botName, question).then(function (result) {
      if (!result || result.error) {
        guideBubble(av, '⚠ ' + ((result && result.error) || 'No answer.'));
        setTimeout(function () { guideIdle(av); restore(); }, 4000);
        return;
      }
      var steps = parseAnswerSteps(result.text);
      if (!steps.length) {
        guideBubble(av, 'I have no answer for that — try rephrasing?');
        setTimeout(function () { guideIdle(av); restore(); }, 4000);
        return;
      }
      av._lastAnswer = { question: question, steps: steps };   /* 📌 keepable */
      document.addEventListener('lc-avatar-ended', restore);
      av.script = steps.map(lineSpec);
      av.idx = 0;
      startPlay(elId);
    });
  }

  /* ── 📌 keep & voice: promote an answer into the authored tour ──────────
     Author-only (editor PAT + repo present). One click: append the answer's
     steps to THIS page's avatar fence (script grows — real questions become
     curriculum), commit via the contents API, voice the new lines with
     ElevenLabs (same content-addressed files + manifest as the 🎙️ studio),
     and extend the live tour immediately. Any ambiguity in locating the
     fence ABORTS — a keep can never corrupt a page. */
  function pageMdPathAv() {
    var p = location.pathname.replace(/\.html?$/, '').replace(/\/+$/, '');
    return (!p || p === '/') ? 'docs/index.md' : 'docs' + (p.charAt(0) === '/' ? p : '/' + p) + '.md';
  }
  function seedToast(text) {
    var n = document.createElement('div');
    n.className = 'lc-guide-hello';
    n.textContent = text;
    document.body.appendChild(n);
    setTimeout(function () { try { n.remove(); } catch (e) {} }, 5000);
  }
  async function keepAnswer(elId, av) {
    var ans = av._lastAnswer;
    if (!ans) return;
    var pat = localStorage.getItem('lc_ed_pat') || '';
    var repo = localStorage.getItem('lc_ed_repo') || '';
    if (!pat || !repo) { seedToast('⚠ connect the ✏️ editor first'); return; }
    var HAuth = { 'Authorization': 'token ' + pat, 'Accept': 'application/vnd.github+json' };
    seedToast('📌 keeping…');
    try {
      var path = pageMdPathAv();
      var api = 'https://api.github.com/repos/' + repo + '/contents/' + path;
      var cur = await fetch(api, { headers: HAuth }).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status + ' reading the page'); return r.json(); });
      var md = decodeURIComponent(escape(atob(String(cur.content || '').replace(/\n/g, ''))));
      /* locate THIS avatar's fence exactly (mask ````-examples first) */
      var masked = md.replace(/````[\s\S]*?````/g, function (m) { return Array(m.length + 1).join(' '); });
      var re = /```yaml\r?\n((?:(?!```)[\s\S])*?)```\s*\r?\n\{:\s*\.avatar\b([^}]*)\}/g, m, hit = null, hits = 0;
      while ((m = re.exec(masked)) !== null) {
        if (m[2].indexOf('#' + elId) >= 0) { hits++; hit = { start: m.index, body: m[1], full: m[0], ial: m[2] }; }
      }
      if (hits > 1) throw new Error('ambiguous fence');
      var newLines = [{ say: 'You might wonder: ' + ans.question }];
      ans.steps.forEach(function (st) {
        newLines.push(st.at ? { at: st.at, say: st.say } : { say: st.say });
      });
      var newMd, keptId = elId;
      if (hits === 1) {
        var cfg = window.jsyaml ? window.jsyaml.load(hit.body) : null;
        if (!cfg || !Array.isArray(cfg.script)) throw new Error('script not parseable');
        cfg.script = cfg.script.concat(newLines);
        var newBody = window.jsyaml.dump(cfg, { lineWidth: 100 });
        /* masking preserves length, so the match span maps 1:1 onto the real md */
        var newFence = '```yaml\n' + newBody + '```\n{: .avatar' + hit.ial + '}';
        newMd = md.substring(0, hit.start) + newFence + md.substring(hit.start + hit.full.length);
      } else if (elId === 'site_guide') {
        /* a config-docked page has no fence yet: the FIRST keep creates it —
           appended at end-of-file (creation, never surgery). The page owns
           its guide and its Q&A from now on. */
        keptId = 'guide';
        var born = { bot: av.botName || 'doc', face: { zoom: 1.2 },
                     script: newLines.map(function (l) { return l.at ? l : l.say; }) };
        newMd = md.replace(/\s*$/, '\n\n') +
          '```yaml\n' + window.jsyaml.dump(born, { lineWidth: 100 }) + '```\n' +
          '{: .avatar #guide dock="true" size="115" }\n';
      } else {
        throw new Error('fence not found');
      }
      var put = await fetch(api, {
        method: 'PUT', headers: HAuth,
        body: JSON.stringify({
          message: 'keep: "' + ans.question.slice(0, 60) + '" — Doc\'s answer joins the tour',
          content: btoa(unescape(encodeURIComponent(newMd))),
          sha: cur.sha
        })
      });
      if (!put.ok) throw new Error('HTTP ' + put.status + ' committing');
      /* extend the live tour this session */
      var specd = newLines.map(lineSpec);
      if (av._tourScript) av._tourScript = av._tourScript.concat(specd);
      else av.script = av.script.concat(specd);
      av._lastAnswer = null;
      /* voice the new lines (same files + manifest the 🎙️ studio uses) */
      var key = localStorage.getItem('lc_11_key') || '';
      var voice = av.genVoice || localStorage.getItem('lc_11_voice') || '';
      if (!key || !voice) { seedToast('📌 kept — tour updated (no voice key: 🎙️ later)'); return; }
      var model = av.genModel || 'eleven_multilingual_v2';
      var made = 0, failed = 0, vox = {};
      for (var i = 0; i < newLines.length; i++) {
        var text = String(newLines[i].say).trim();
        try {
          var th = (await sha1hex(text)).slice(0, 16);
          var h = await sha1hex(voice + '|' + model + '|' + text);
          var f = 'lc-' + h.slice(0, 16) + '.mp3';
          var head = await fetch('/assets/audio/' + f, { method: 'HEAD' }).catch(function () { return { ok: false }; });
          if (!head.ok) {
            var r = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + encodeURIComponent(voice) + '?output_format=mp3_44100_128', {
              method: 'POST', headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
              body: JSON.stringify({ text: text, model_id: model })
            });
            if (!r.ok) throw new Error('11labs ' + r.status);
            var blob = await r.blob();
            var b64 = await blobB64(blob);
            var pm = await fetch('https://api.github.com/repos/' + repo + '/contents/docs/assets/audio/' + f, {
              method: 'PUT', headers: HAuth,
              body: JSON.stringify({ message: 'voice: ' + f + ' (kept answer)', content: b64 })
            });
            if (!(pm.ok || pm.status === 422)) throw new Error('mp3 commit ' + pm.status);
            made++;
          }
          vox[th] = f;
        } catch (e) { failed++; }
      }
      if (Object.keys(vox).length) {
        try {
          var mApi = 'https://api.github.com/repos/' + repo + '/contents/docs/assets/audio/vox.json';
          var mc = await fetch(mApi, { headers: HAuth }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
          var man = {};
          if (mc && mc.content) { try { man = JSON.parse(atob(mc.content.replace(/\n/g, ''))) || {}; } catch (e2) {} }
          var pg = man[voxSlug()] = man[voxSlug()] || {};
          pg[keptId] = Object.assign(pg[keptId] || {}, vox);
          await fetch(mApi, {
            method: 'PUT', headers: HAuth,
            body: JSON.stringify({ message: 'voice manifest: kept answer (' + Object.keys(vox).length + ' lines)',
                                   content: btoa(unescape(encodeURIComponent(JSON.stringify(man, null, 1)))),
                                   sha: mc && mc.sha ? mc.sha : undefined })
          });
          _voxP = Promise.resolve(man);   /* this session's playback sees it too */
        } catch (e3) {}
      }
      seedToast('📌 kept · ' + (newLines.length) + ' lines in the tour · ' + made + ' voiced' + (failed ? ' · ' + failed + ' voice failed' : ''));
    } catch (err) {
      seedToast('⚠ could not keep automatically (' + (err && err.message) + ') — add it by hand');
    }
  }

  /* the ask panel: question box when connected, PAT paste when not */
  function openAskPanel(elId, av) {
    var panel = document.querySelector('.lc-guide-ask');
    if (panel) panel.remove();
    panel = document.createElement('div');
    panel.className = 'lc-guide-ask open';
    var ready = window.lcBotAsk && window.lcBotAsk.ready();
    if (ready) {
      panel.innerHTML =
        '<textarea rows="2" placeholder="Ask about this page…"></textarea>' +
        '<div class="lc-guide-ask-row"><button type="button">▶ Ask</button></div>';
      var ta = panel.querySelector('textarea');
      panel.querySelector('button').addEventListener('click', function () {
        var q = (ta.value || '').trim();
        if (!q) return;
        panel.remove();
        askDoc(elId, av, q);
      });
      setTimeout(function () { ta.focus(); }, 50);
    } else {
      panel.innerHTML =
        '<p class="lc-guide-ask-hint">Asking uses your own free credits — paste your GitHub PAT once (kept in memory only, like the agents on this page).</p>' +
        '<form autocomplete="on">' +
        '<input type="text" name="username" value="github-models" autocomplete="username" tabindex="-1" readonly>' +
        '<input type="password" name="password" autocomplete="current-password" placeholder="ghp_…" required>' +
        '<div class="lc-guide-ask-row" style="margin-top:6px"><button type="submit">Save &amp; ask</button></div>' +
        '</form>';
      panel.querySelector('form').addEventListener('submit', function (e) {
        e.preventDefault();
        var v = (panel.querySelector('input[type=password]').value || '').trim();
        if (!v) return;
        window.lcBotAsk.connect(v);
        panel.remove();
        openAskPanel(elId, av);   /* reopen in question state */
      });
    }
    document.body.appendChild(panel);
    setTimeout(function () {
      document.addEventListener('click', function onDoc(e) {
        if (!panel.contains(e.target)) { panel.remove(); document.removeEventListener('click', onDoc); }
      });
    }, 0);
  }

  /* local verb menu on the character itself: ▶ start / ↺ replay · next →
     · ⏹ stop · ✖ close — anchored beside the avatar, one at a time */
  function openVerbMenu(elId, av) {
    var old = document.querySelector('.lc-avatar-verbmenu');
    if (old) { old.remove(); if (old._for === elId) return; }
    var menu = document.createElement('div');
    menu.className = 'lc-guide-menu lc-avatar-verbmenu open';
    menu.setAttribute('role', 'menu');
    menu._for = elId;
    function item(label, fn) {
      var b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'menuitem'); b.textContent = label;
      b.addEventListener('click', function (e) { e.stopPropagation(); menu.remove(); fn(); });
      menu.appendChild(b);
    }
    if (!av.playing) {
      item(av.idx > 0 ? '↺ Replay' : '▶ Start', function () { togglePlay(elId); });
    } else {
      if (av._waiting || av._curStep || av.step) item('Next →', function () { togglePlay(elId); });
      item('⏹ Stop', function () { stopPlay(elId); });
    }
    item('✖ Close', function () { stopPlay(elId); });
    var r = av.char.getBoundingClientRect();
    menu.style.position = 'fixed';
    menu.style.left = Math.max(8, Math.min(window.innerWidth - 160, r.left)) + 'px';
    menu.style.top = Math.max(8, r.top - 8 - 140) + 'px';
    menu.style.right = 'auto'; menu.style.bottom = 'auto';
    document.body.appendChild(menu);
    setTimeout(function () {
      document.addEventListener('click', function onDoc(e) {
        if (!menu.contains(e.target)) { menu.remove(); document.removeEventListener('click', onDoc); }
      });
    }, 0);
  }

  function buildSeed(elId, av) {
    if (document.getElementById('guide_seed')) return;
    av.host.classList.add('lc-avatar-docked');   /* idle big face hides; the seed represents */
    var seed = document.createElement('button');
    seed.id = 'guide_seed'; seed.type = 'button';
    seed.className = 'lc-guide-seed';
    seed.setAttribute('aria-label', 'Guide — tour and help');
    seed.setAttribute('aria-haspopup', 'menu');
    seed.innerHTML = buildFaceSvg(av.faceCfg || {});
    var menu = document.createElement('div');
    menu.className = 'lc-guide-menu';
    menu.setAttribute('role', 'menu');
    document.body.appendChild(seed);
    document.body.appendChild(menu);

    function item(label, fn) {
      var b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'menuitem');
      b.textContent = label;
      b.addEventListener('click', function (e) { e.stopPropagation(); fn(); render(); });
      return b;
    }
    function render() {
      menu.innerHTML = '';
      if (!av.playing) {
        if (av.script.length) {
          menu.appendChild(item(av.idx > 0 ? '↺ Replay tour' : '▶ Play tour', function () { togglePlay(elId); menu.classList.remove('open'); }));
        }
        if (av.botName && window.lcBotAsk) {
          menu.appendChild(item('💬 Ask', function () { menu.classList.remove('open'); openAskPanel(elId, av); }));
        }
        var _pat0 = null, _repo0 = null;
        try { _pat0 = localStorage.getItem('lc_ed_pat'); _repo0 = localStorage.getItem('lc_ed_repo'); } catch (e) {}
        if (av._lastAnswer && _pat0 && _repo0) {
          menu.appendChild(item('📌 Keep & voice', function () { menu.classList.remove('open'); keepAnswer(elId, av); }));
        }
      } else if (av._waiting || av._curStep || av.step) {
        menu.appendChild(item('Next →', function () { togglePlay(elId); }));
        menu.appendChild(item('⏹ Stop', function () { stopPlay(elId); menu.classList.remove('open'); }));
      } else {
        menu.appendChild(item('⏹ Stop', function () { stopPlay(elId); menu.classList.remove('open'); }));
      }
    }
    seed.addEventListener('click', function (e) {
      e.stopPropagation();
      if (menu.classList.contains('open')) { menu.classList.remove('open'); return; }
      render(); menu.classList.add('open');
    });
    document.addEventListener('click', function (e) {
      if (!menu.contains(e.target) && e.target !== seed) menu.classList.remove('open');
    });
    document.addEventListener('lc-avatar-ended', render);

    /* the whisper: once ever, silent, self-dismissing */
    var seen = null;
    try { seen = localStorage.getItem('lc_guide_hello'); } catch (e) {}
    if (!seen) {
      var hello = document.createElement('div');
      hello.className = 'lc-guide-hello';
      hello.textContent = '👋 Need a tour?';
      document.body.appendChild(hello);
      setTimeout(function () { try { hello.remove(); } catch (e) {} }, 6000);
      try { localStorage.setItem('lc_guide_hello', '1'); } catch (e) {}
    }
  }

  /* ── learner-summoned guide ───────────────────────────────────────────────
     The pill's 🧑‍🏫 Guide toggle (persisted per device) brings the generic
     companion to ANY page the author left bare: classic face, no tour, 💬 Ask
     wired to the site's default bot (knowledge: self → he still knows the
     page). Authored guides always win — summoning is a no-op beside them. */
  var GUIDE_BOT = {{ site.guide_bot | default: "doc" | jsonify }};
  /* a page (or a whole section, via _config.yml scoped defaults) can decree
     its guide with a page variable — encapsulated: no fence, no per-page
     copies. guide: doc → the companion auto-docks, author-level (the
     learner's toggle cannot remove it). */
  var PAGE_GUIDE = {{ page.guide | default: "" | jsonify }};
  window.lcGuideOn = function (on) {
    try { on ? localStorage.setItem('lc_guide_on', '1') : localStorage.removeItem('lc_guide_on'); } catch (e) {}
    var seed = document.getElementById('guide_seed');
    if (!on) {
      if (seed && seed.dataset.lcGeneric) {
        seed.remove();
        var m = document.querySelector('.lc-guide-menu'); if (m) m.remove();
      }
      return;
    }
    if (seed) return;                       /* authored (or already summoned) guide wins */
    summonGuide(GUIDE_BOT, true);
  };
  function summonGuide(botName, generic) {
    if (document.getElementById('guide_seed')) return;
    var elId = 'site_guide';
    if (window._lcAvatars && window._lcAvatars[elId]) return;
    var host = document.createElement('div');
    host.className = 'lc-avatar-host lc-avatar-docked';
    host.id = 'lc-avatar-' + elId;
    host.setAttribute('data-lc-id', elId);
    host.style.left = '70vw';
    var pose = document.createElement('div'); pose.className = 'lc-avatar-pose'; host.appendChild(pose);
    var char = document.createElement('div'); char.className = 'lc-avatar-char';
    char.style.width = '115px'; char.style.height = '115px'; pose.appendChild(char);
    var bubble = document.createElement('div'); bubble.className = 'lc-avatar-speech'; pose.appendChild(bubble);
    document.body.appendChild(host);
    var av = (window._lcAvatars = window._lcAvatars || {})[elId] = {
      host: host, bubble: bubble, char: char,
      script: [], path: 'right', voice: '',
      tune: { rate: 0, pitch: 0 },
      lottie: '', lottieSeg: null, rive: '', riveSm: '',
      riveAnim: null, riveTalk: null, riveMouth: null, riveTriggers: [], riveInputs: null,
      video: '', transparent: false,
      faceCfg: { zoom: 1.2 },
      size: 115, spot: null,
      pupils: null, mouth: null, audioEl: null, videoEl: null, analyser: null,
      playing: false, idx: 0, lottieDone: false, step: false, mute: false,
      genVoice: '', genModel: 'eleven_multilingual_v2',
      botName: botName
    };
    initChar(elId, char, 115);
    av._idleT = setInterval(function () { if (!av.playing) lookIdle(av); }, 3200);
    char.addEventListener('click', function () { togglePlay(elId); });
    char.addEventListener('contextmenu', function (e) { e.preventDefault(); openVerbMenu(elId, av); });
    buildSeed(elId, av);
    var sd = document.getElementById('guide_seed');
    if (sd && generic) sd.dataset.lcGeneric = '1';
  }
  /* honor the page/section decree first, then the learner's persisted choice */
  setTimeout(function () {
    if (document.getElementById('guide_seed')) return;
    if (PAGE_GUIDE) { summonGuide(PAGE_GUIDE, false); return; }
    var on = null; try { on = localStorage.getItem('lc_guide_on'); } catch (e) {}
    if (on === '1') window.lcGuideOn(true);
  }, 900);

  /* ── voices studio: order studio audio from the page itself ──────────────
     [🎙️ Generate voices](#) {: .avatar-voices target="prof" }
     For each script line of the target avatar, computes the content-addressed
     filename (hash of voice|model|text — identical to packages/gen-audio.mjs),
     skips files the site already serves, calls the ElevenLabs API from THIS
     browser for the missing ones (key prompted once, stored in this browser
     only as lc_11_key), previews them immediately, and commits each mp3 to
     docs/assets/audio/ through the GitHub contents API with the ✏️ editor's
     credentials (lc_ed_pat / lc_ed_repo — the .record commit contract). */
  function sha1hex(s) {
    return crypto.subtle.digest("SHA-1", new TextEncoder().encode(s)).then(function (b) {
      return Array.prototype.map.call(new Uint8Array(b), function (x) { return ("0" + x.toString(16)).slice(-2); }).join("");
    });
  }
  /* the site's voice manifest — /assets/audio/vox.json (ONE file, seeded in
     the repo so it always exists — a per-page file would 404 on every page
     without audio and dirty the console, which the UX gate rightly rejects).
     Shape: { pageSlug: { avatarId: { textHash16: file } } }, committed by the
     🎙️ studio (or gen-audio.mjs). Playback reads it to find each line's
     studio audio with NO fence config. */
  function voxSlug() {
    var p = location.pathname.replace(/\.html?$/, "").replace(/^\/+|\/+$/g, "");
    return p ? p.replace(/\//g, "-") : "index";
  }
  var _voxP = null;
  function voxManifest() {
    if (_voxP) return _voxP;
    _voxP = fetch("/assets/audio/vox.json", { cache: "no-cache" })
      .then(function (r) { return r.ok ? r.json() : {}; })
      .catch(function () { return {}; });
    return _voxP;
  }
  function blobB64(b) {
    return new Promise(function (res, rej) {
      var r = new FileReader();
      r.onload = function () { res(String(r.result).split(",")[1]); };
      r.onerror = rej;
      r.readAsDataURL(b);
    });
  }
  function upgradeVoices(el) {
    if (el.dataset.lcAvtVoxDone) return;
    if (inEditorPreview(el)) return;
    el.dataset.lcAvtVoxDone = "1";
    var targetId = el.getAttribute("target") || "";
    el.classList.add("lc-avatar-trigger");
    var label0 = el.textContent.trim() || "🎙️ Generate voices";
    var busy = false;
    el.addEventListener("click", async function (e) {
      e.preventDefault();
      if (busy) return;
      var av = window._lcAvatars && window._lcAvatars[targetId];
      if (!av) { el.textContent = "✖ no avatar #" + targetId; return; }
      if (!av.genVoice) {
        /* no elevenlabs: in the fence — use the remembered voice id silently;
           ask only when nothing is stored yet (Shift-click to change it) */
        var vid = localStorage.getItem("lc_11_voice") || "";
        if (!vid || e.shiftKey) {
          vid = window.prompt("ElevenLabs voice id (from elevenlabs.io — your cloned voice works):", vid) || "";
        }
        if (!vid) return;
        av.genVoice = vid.trim(); av._genAdhoc = true;
        try { localStorage.setItem("lc_11_voice", av.genVoice); } catch (err) {}
      }
      var key = localStorage.getItem("lc_11_key") || "";
      if (!key || e.shiftKey) {
        key = window.prompt("ElevenLabs API key (kept in this browser only — like your GitHub PAT):", key) || "";
      }
      if (!key) return;
      key = key.trim();
      try { localStorage.setItem("lc_11_key", key); } catch (err) {}
      var pat = localStorage.getItem("lc_ed_pat") || "";
      var repo = localStorage.getItem("lc_ed_repo") || "";
      var HAuth = { "Authorization": "token " + pat, "Accept": "application/vnd.github+json" };
      busy = true;
      var lines = av.script.filter(function (l) { return l.say && !l.video; });
      var made = 0, cached = 0, committed = 0, failed = 0, vox = {};
      for (var i = 0; i < lines.length; i++) {
        var l = lines[i], text = String(l.say).trim();
        el.textContent = "🎙️ " + (i + 1) + "/" + lines.length + "…";
        try {
          var th = (await sha1hex(text)).slice(0, 16);                          /* manifest key: the text */
          var h = await sha1hex(av.genVoice + "|" + av.genModel + "|" + text);  /* file name: voice+text  */
          var f = "lc-" + h.slice(0, 16) + ".mp3", url = "/assets/audio/" + f;
          var head = await fetch(url, { method: "HEAD" }).catch(function () { return { ok: false }; });
          if (head.ok) { l.audio = url; vox[th] = f; cached++; continue; }
          var r = await fetch("https://api.elevenlabs.io/v1/text-to-speech/" +
              encodeURIComponent(av.genVoice) + "?output_format=mp3_44100_128", {
            method: "POST",
            headers: { "xi-api-key": key, "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, model_id: av.genModel })
          });
          if (!r.ok) throw new Error("ElevenLabs HTTP " + r.status);
          var blob = await r.blob();
          l.audio = URL.createObjectURL(blob);   /* hear it right now, this session */
          made++;
          if (pat && repo) {
            var put = await fetch("https://api.github.com/repos/" + repo + "/contents/docs/assets/audio/" + f, {
              method: "PUT", headers: HAuth,
              body: JSON.stringify({ message: "voice: " + f + " (ElevenLabs, avatar #" + targetId + ")",
                                     content: await blobB64(blob) })
            });
            /* 422 = the file is already in the repo (content-addressed → same bytes) */
            if (put.ok || put.status === 422) { committed++; vox[th] = f; }
            else failed++;
          }
        } catch (err) {
          failed++;
          /* a rejected key would fail every line — forget it so the next
             click asks again instead of failing silently forever */
          if (/HTTP 401/.test((err && err.message) || "")) { try { localStorage.removeItem("lc_11_key"); } catch (e4) {} }
          if (window.console) console.warn("[avatar-voices] “" + text.slice(0, 40) + "…” — " + (err && err.message));
        }
      }
      /* commit the page's voice manifest — playback then finds every file by
         itself (no fence config): { avatarId: { textHash16: file } } */
      var manifestOk = false;
      if (pat && repo && Object.keys(vox).length) {
        try {
          var api = "https://api.github.com/repos/" + repo + "/contents/docs/assets/audio/vox.json";
          var cur = await fetch(api, { headers: HAuth }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
          var man = {};
          if (cur && cur.content) { try { man = JSON.parse(atob(cur.content.replace(/\n/g, ""))) || {}; } catch (e2) {} }
          var pageMan = man[voxSlug()] = man[voxSlug()] || {};
          pageMan[targetId] = Object.assign(pageMan[targetId] || {}, vox);
          var putM = await fetch(api, {
            method: "PUT", headers: HAuth,
            body: JSON.stringify({ message: "voice manifest: " + voxSlug() + " #" + targetId + " (" + Object.keys(vox).length + " lines)",
                                   content: btoa(unescape(encodeURIComponent(JSON.stringify(man, null, 1)))),
                                   sha: cur && cur.sha ? cur.sha : undefined })
          });
          manifestOk = putM.ok;
          if (manifestOk) _voxP = Promise.resolve(man);   /* this session sees it too */
        } catch (e3) { if (window.console) console.warn("[avatar-voices] manifest: " + (e3 && e3.message)); }
      }
      busy = false;
      el.textContent = "✔ " + made + " generated · " + cached + " cached" +
        (committed ? " · " + committed + " committed" : ((pat && repo) ? "" : " · not committed — connect the ✏️ editor (PAT + repo) first")) +
        (manifestOk ? " · playback wired automatically" : "") +
        (failed ? " · ✖ " + failed + " failed (see console)" : "") +
        (av._genAdhoc && (made || cached) && !manifestOk ? " · add elevenlabs: " + av.genVoice + " to the fence to keep it" : "");
      setTimeout(function () { el.textContent = label0; }, 8000);
    });
  }

  /* ── programmatic playback (engine API) ───────────────
     window.lcAvatarPlay(lines, opts) builds a transient built-in-face avatar,
     plays a script, and removes itself when the script ends. It reuses the
     whole walk/spotlight/step machinery above — no config block, no upgrader.
       lines: [{ at: "#sel", say: "caption", pause?: seconds, step?: bool,
                 fn?: function }]         — fn runs as its line starts
       opts:  { voice, rate, pitch, step, size, onEnd(detail) } → transient id;
              voice: "off" = silent bubbles (no TTS), dwell-then-advance
     .demo replay uses this to turn a recorded trace into a narrated walk. */
  var PLAY_ID = 0;
  window.lcAvatarPlay = function (lines, opts) {
    opts = opts || {};
    var elId = "avtplay-" + (++PLAY_ID);
    var size = parseInt(opts.size, 10) || 132;
    var mute = opts.voice === "off";

    var host = document.createElement("div");
    host.className = "lc-avatar-host";
    host.id = "lc-avatar-" + elId;
    host.setAttribute("data-lc-id", elId);
    host.style.left = "70vw";
    var pose = document.createElement("div");
    pose.className = "lc-avatar-pose";
    host.appendChild(pose);
    var char = document.createElement("div");
    char.className = "lc-avatar-char";
    char.style.width = size + "px"; char.style.height = size + "px";
    pose.appendChild(char);
    var bubble = document.createElement("div");
    bubble.className = "lc-avatar-speech";
    pose.appendChild(bubble);
    document.body.appendChild(host);

    var av = (window._lcAvatars = window._lcAvatars || {})[elId] = {
      host: host, bubble: bubble, char: char,
      script: (Array.isArray(lines) ? lines : []).map(lineSpec),
      path: "right", voice: mute ? "" : (opts.voice || ""),
      tune: { rate: parseFloat(opts.rate) || 0, pitch: parseFloat(opts.pitch) || 0 },
      lottie: "", lottieSeg: null, rive: "", riveSm: "",
      riveAnim: null, riveTalk: null, riveMouth: null, riveTriggers: [], riveInputs: null,
      video: "", transparent: false,
      size: size, spot: null,
      pupils: null, mouth: null, audioEl: null, videoEl: null, analyser: null,
      playing: false, idx: 0, lottieDone: false, step: !!opts.step, mute: mute
    };
    initChar(elId, char, size);              /* no video/rive/lottie → built-in face */
    var idle = setInterval(function () { if (!av.playing) lookIdle(av); }, 3200);
    char.addEventListener("click", function () { togglePlay(elId); });

    var onEnd = function (ev) {
      if (!ev.detail || ev.detail.id !== elId) return;
      document.removeEventListener("lc-avatar-ended", onEnd);
      clearInterval(idle);
      setTimeout(function () {
        try { host.remove(); } catch (e) {}
        if (window._lcAvatars) delete window._lcAvatars[elId];
      }, 500);
      if (typeof opts.onEnd === "function") { try { opts.onEnd(ev.detail); } catch (e) {} }
    };
    document.addEventListener("lc-avatar-ended", onEnd);

    setTimeout(function () { startPlay(elId); }, 300);   /* let voices populate */
    return elId;
  };

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry:
     one registration covers the initial page scan and all re-scans. */

  /* pythonistic (snake_case) names are canonical; the kebab spellings stay
     as legacy aliases so older pages keep working */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.avatar, pre.avatar", upgradeAvatar);
    window.lcRegisterUpgrader("p.avatar_trigger, a.avatar_trigger, p.avatar-trigger, a.avatar-trigger", upgradeTrigger);
    window.lcRegisterUpgrader("p.avatar_studio, a.avatar_studio, p.avatar-studio, a.avatar-studio", upgradeStudio);
    window.lcRegisterUpgrader("p.avatar_voices, a.avatar_voices, p.avatar-voices, a.avatar-voices", upgradeVoices);
  }

})();
</script>
