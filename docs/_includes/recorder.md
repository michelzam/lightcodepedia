{%- comment -%}
Recorder — screen + face recorder with floating HUD, review panel and
YouTube upload (OAuth implicit flow; the upload IIFE talks to the
recorder via window.lcYtUploadBlob / lcOpenYtUpload).

Activated by IAL on a paragraph: {: .recorder pip="bottom-right" }.
Exposes window.lcOpenRecorder for programmatic launch. The recorder CSS
is injected into <head> at runtime so the floating HUD survives the
launcher modal's teardown.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window._lcRecorderReady) return;
  window._lcRecorderReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  // ── Screen + face recorder ────────────────────────────────────────────────
  // Inject the recorder CSS once into <head> so it is NOT tied to any widget's
  // lifecycle. (The floating HUD outlives the launcher modal; if its styles lived
  // inside the modal, closing the modal would un-style the HUD and make it vanish.)
  function ensureRecorderStyles() {
    if (document.getElementById("lc-rec-styles")) return;
    var st = document.createElement("style");
    st.id = "lc-rec-styles";
    st.textContent = [
      '.lc-recorder{border:1px solid #ddd;border-radius:10px;overflow:hidden;max-width:480px;font-family:inherit}',
      '.lc-rec-head{background:#1e1e2e;color:#cdd6f4;display:flex;align-items:center;gap:10px;padding:10px 14px;font-size:.9em;font-weight:600}',
      '.lc-rec-dot{width:10px;height:10px;border-radius:50%;background:#555;flex-shrink:0}',
      '.lc-rec-dot.live{background:#f33;animation:lcBlink 1s infinite}',
      '@keyframes lcBlink{0%,100%{opacity:1}50%{opacity:.2}}',
      '.lc-rec-body{padding:14px 16px;background:#fafafa}',
      '.lc-rec-opts{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}',
      '.lc-rec-opt{font-size:.82em;padding:4px 10px;border:1px solid #ccc;border-radius:20px;cursor:pointer;background:#fff;color:#333;user-select:none}',
      '.lc-rec-opt.on{background:#0066cc;color:#fff;border-color:#0066cc}',
      '.lc-rec-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}',
      '.lc-rec-btn{padding:.45em 1.2em;border:none;border-radius:6px;cursor:pointer;font-size:.9em;font-weight:600}',
      '.lc-rec-btn.start{background:#0066cc;color:#fff}.lc-rec-btn.start:hover{background:#0052a3}',
      '.lc-rec-btn.stop{background:#c00;color:#fff}.lc-rec-btn.stop:hover{background:#a00}',
      '.lc-rec-btn.again{background:#eee;color:#333}.lc-rec-btn.again:hover{background:#ddd}',
      '.lc-rec-status{font-size:.82em;color:#888;margin-top:8px;min-height:1.2em}',
      '.lc-rec-status.ok{color:#1a7a1a}.lc-rec-status.err{color:#c00}',
      '.lc-rec-ios{font-size:.84em;line-height:1.6;color:#444;background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:10px 12px;margin-top:4px}',
      '.lc-rec-ios ol{margin:6px 0 0 16px;padding:0}',
      '.lc-rec-ios li{margin-bottom:2px}',
      /* HUD styles */
      '.lc-rec-hud{position:fixed;z-index:2147483647;background:transparent;padding:0;display:flex;flex-direction:column;align-items:center;gap:6px;user-select:none;touch-action:none;cursor:grab}',
      '.lc-rec-hud:active{cursor:grabbing}',
      '.lc-rec-hud-pip{width:96px;height:96px;border-radius:50%;overflow:hidden;border:3px solid rgba(255,255,255,.9);flex-shrink:0;background:#111;position:relative;box-shadow:0 6px 24px rgba(0,0,0,.45)}',
      '.lc-rec-hud-pip video{width:100%;height:100%;object-fit:cover;display:block;transform:scaleX(-1)}',
      '.lc-rec-hud-pip .lc-cam-off{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2em}',
      '.lc-rec-hud-timer{color:#fff;font-size:.85em;font-variant-numeric:tabular-nums;font-weight:700;letter-spacing:.04em;min-height:1.2em;background:rgba(15,15,25,.78);padding:2px 10px;border-radius:12px}',
      '.lc-rec-hud-stop{background:#c00;color:#fff;border:none;border-radius:14px;padding:5px 14px;cursor:pointer;font-size:.85em;font-weight:600;box-shadow:0 3px 12px rgba(0,0,0,.4)}',
      '.lc-rec-hud-stop:hover{background:#a00}',
      '.lc-rec-hud-ios{font-size:.72em;color:#fff;text-align:center;max-width:140px;line-height:1.4;background:rgba(15,15,25,.78);padding:6px 10px;border-radius:10px}',
      '.lc-rec-hud-timer-btn{font-size:.75em;color:#fff;background:rgba(15,15,25,.78);border:1px solid #777;border-radius:12px;padding:3px 10px;cursor:pointer}',
      '.lc-rec-hud-timer-btn.running{color:#f88;border-color:#f88}',
      '.lc-rec-hud-pip canvas{position:absolute;inset:0;width:100%;height:100%;display:none;transform:scaleX(-1)}',
      '.lc-rec-hud-ctrls{display:flex;gap:6px;align-items:center}',
      '.lc-rec-hud-pause{background:#333;color:#fff;border:none;border-radius:14px;padding:5px 12px;cursor:pointer;font-size:.85em;font-weight:600;box-shadow:0 3px 12px rgba(0,0,0,.4)}',
      '.lc-rec-hud-pause:hover{background:#222}',
      '.lc-rec-hud-pause.paused{background:#1a7a1a}.lc-rec-hud-pause.paused:hover{background:#156315}',
      /* Review + launcher modals */
      '.lc-rec-ov{position:fixed;inset:0;z-index:2147483646;background:rgba(10,10,20,.62);display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(3px)}',
      '.lc-rec-panel{background:#fff;border-radius:14px;box-shadow:0 20px 60px rgba(0,0,0,.4);max-width:560px;width:100%;max-height:90vh;overflow:auto;position:relative}',
      '.lc-rec-panel-close{position:absolute;top:8px;right:10px;background:none;border:none;font-size:1.3em;color:#888;cursor:pointer;line-height:1;z-index:2}',
      '.lc-rec-panel-close:hover{color:#333}',
      '.lc-rec-review-vid{width:100%;display:block;background:#000;border-radius:14px 14px 0 0;max-height:60vh}',
      '.lc-rec-review-body{padding:14px 18px 18px}',
      '.lc-rec-review-meta{font-size:.82em;color:#888;margin-bottom:12px}',
      '.lc-rec-review-warn{font-size:.84em;line-height:1.5;color:#7a4a00;background:#fff7e6;border:1px solid #ffd98a;border-radius:8px;padding:8px 10px;margin-bottom:10px}',
      '.lc-rec-review-acts{display:flex;gap:8px;flex-wrap:wrap}',
      '.lc-rec-review-acts button{padding:.5em 1.1em;border:none;border-radius:7px;cursor:pointer;font-size:.9em;font-weight:600}',
      '.lc-rb-save{background:#0066cc;color:#fff}.lc-rb-save:hover{background:#0052a3}',
      '.lc-rb-yt{background:#ff0000;color:#fff}.lc-rb-yt:hover{background:#cc0000}.lc-rb-yt:disabled{opacity:.5;cursor:default}',
      '.lc-rb-again{background:#eee;color:#333}.lc-rb-again:hover{background:#ddd}',
      '.lc-rb-discard{background:#fff;color:#c00;border:1px solid #f0caca!important}.lc-rb-discard:hover{background:#fff5f5}'
    ].join("");
    document.head.appendChild(st);
  }

  function upgradeRecorder(el, hooks) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    ensureRecorderStyles();
    hooks = hooks || {};
    var pipAttr = el.getAttribute("pip") || "bottom-right";
    var camOn = (el.getAttribute("camera") || "on") !== "off";
    var micOn = (el.getAttribute("mic") || "on") !== "off";
    var sndOn = (el.getAttribute("sound") || "off") === "on";
    var pipSize = parseInt(el.getAttribute("size") || "240", 10);
    var camZoom = parseFloat(el.getAttribute("zoom") || "1.35");
    var fps     = parseInt(el.getAttribute("fps")  || "25",  10);

    var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
                (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    var canScreen = !isIOS && !!navigator.mediaDevices && !!navigator.mediaDevices.getDisplayMedia;
    // macOS desktop: rely on the native Presenter Overlay for the face (it composites
    // the camera into the screen capture in higher quality and avoids a second camera
    // consumer that destabilises Safari). So we don't open our own camera there.
    var isMac = !isIOS && /Mac/.test(navigator.platform || navigator.userAgent || "");

    // Safari 16+ reports video/webm as supported (VP9 playback) but produces
    // poor/inconsistent recordings — prefer mp4 there. Chrome/Firefox use webm.
    var isSafari = /safari/i.test(navigator.userAgent) && !/chrome|chromium|crios|android/i.test(navigator.userAgent);
    var candidates = isSafari
      ? ["video/mp4;codecs=avc1","video/mp4;codecs=h264","video/mp4","video/webm"]
      : ["video/webm;codecs=vp9","video/webm","video/mp4"];
    var mimeType = candidates.find(function(t){ return MediaRecorder.isTypeSupported(t); }) || "";
    if (!mimeType && isSafari) mimeType = "video/mp4";
    var ext = mimeType.includes("mp4") ? "mp4" : "webm";

    // Presenter Overlay (the native face bubble) is ONLY offered to Safari on macOS.
    // Chrome/Edge/Firefox on Mac don't expose it — there we must use our own face
    // circle, exactly like Windows/Linux. So the "rely on native overlay, hide our
    // own camera" path is gated on Safari-on-Mac, not all Macs.
    var isMacSafari = isMac && isSafari;

    /* ── Widget (in-page launcher) ── */
    var wrap = document.createElement("div");
    wrap.className = "lc-recorder";
    wrap.innerHTML = [
      '<div class="lc-rec-head"><span class="lc-rec-dot" id="lc-rd"></span><span>🎬 Screen Recorder</span></div>',
      '<div class="lc-rec-body">',
      '  <div class="lc-rec-opts" id="lc-ropts">',
      isMacSafari ? '' : '    <span class="lc-rec-opt ' + (camOn ? 'on' : 'off') + '"  id="lc-ropt-cam">📷 Camera</span>',
      '    <span class="lc-rec-opt ' + (micOn ? 'on' : 'off') + '"  id="lc-ropt-mic">🎤 Mic</span>',
      canScreen ? '<span class="lc-rec-opt ' + (sndOn ? 'on' : 'off') + '" id="lc-ropt-snd">🔊 Screen audio</span>' : '',
      isMacSafari ? '' : '<span class="lc-rec-opt" id="lc-ropt-bg">🖼 BG: Off</span>',
      '  </div>',
      '  <div class="lc-rec-actions">',
      canScreen
        ? '<button class="lc-rec-btn start" id="lc-rbtn">🎬 Set up recording</button>'
        : '<button class="lc-rec-btn start" id="lc-rbtn">📱 Show camera</button>',
      '  </div>',
      isMacSafari ? [
        '<div class="lc-rec-ios" style="background:#eef4ff;border-color:#cdddff;color:#234">',
        '<strong>💡 Add your face with Presenter Overlay</strong>',
        '<div>After you share your screen, a green 🟢 <strong>camera/screen icon</strong> appears in the macOS menu bar (top-right). Click it → <strong>Presenter Overlay → Small</strong>, then press <strong>▶ Start</strong> on the floating panel. macOS composites your camera in higher quality than any in-page overlay. <em>(The menu only shows while we hold the camera.)</em></div>',
        '</div>'
      ].join("") : '',
      isIOS ? [
        '<div class="lc-rec-ios">',
        '<strong>📱 iPhone screen recording</strong>',
        '<ol>',
        '<li>Tap <strong>Show camera</strong> above — your face appears floating</li>',
        '<li>Open Control Center (swipe from top-right)</li>',
        '<li>Long-press <strong>⏺ Screen Recording</strong> → enable Microphone</li>',
        '<li>Tap ⏺ to start — record your demo</li>',
        '<li>Tap the red status bar to stop</li>',
        '</ol>',
        '<em>Video saves to your Photos app.</em>',
        '</div>'
      ].join("") : '',
      '  <div class="lc-rec-status" id="lc-rstat"></div>',
      '</div>'
    ].join("");
    el.parentNode.replaceChild(wrap, el);

    var btnEl   = wrap.querySelector("#lc-rbtn");
    var statEl  = wrap.querySelector("#lc-rstat");
    var dotEl   = wrap.querySelector("#lc-rd");
    var optCam  = wrap.querySelector("#lc-ropt-cam");
    var optMic  = wrap.querySelector("#lc-ropt-mic");
    var optSnd  = wrap.querySelector("#lc-ropt-snd");

    // On macOS we don't run our own camera — the native Presenter Overlay owns it.
    var useCam = !isMacSafari, useMic = true, useSnd = false;
    var bgMode = "none";
    var optBg  = wrap.querySelector("#lc-ropt-bg");
    var bgCycle  = ["none","blur","dark","blue","green","white"];
    var bgLabels = { none: "🖼 BG: Off", blur: "🌫 BG: Blur", dark: "⬛ BG: Dark", blue: "🔵 BG: Blue", green: "🟢 BG: Green", white: "⬜ BG: White" };
    if (optCam) optCam.addEventListener("click", function(){ useCam = !useCam; optCam.classList.toggle("on", useCam); refreshHUD(); });
    optMic.addEventListener("click", function(){ useMic = !useMic; optMic.classList.toggle("on", useMic); });
    if (optSnd) optSnd.addEventListener("click", function(){ useSnd = !useSnd; optSnd.classList.toggle("on", useSnd); });
    if (optBg) optBg.addEventListener("click", function() {
      bgMode = bgCycle[(bgCycle.indexOf(bgMode) + 1) % bgCycle.length];
      optBg.textContent = bgLabels[bgMode];
      optBg.classList.toggle("on", bgMode !== "none");
      if (hud) refreshHUDCam();
    });

    function setStatus(msg, cls) { statEl.className = "lc-rec-status " + (cls||""); statEl.textContent = msg; }
    function fmtTime(ms) {
      var s = Math.floor(ms/1000), m = Math.floor(s/60);
      return String(m).padStart(2,"0") + ":" + String(s%60).padStart(2,"0");
    }

    /* ── Floating HUD ── */
    var hud = null, hudCamVid = null, hudTimer = null, hudStop = null, hudPause = null, hudLabel = null;
    var hudIosTimer = null, hudIosBtn = null;
    var isPaused = false, pausedAccum = 0, pauseStart = 0;
    var armed = false, startTs = 0, activeStream = null, endNote = "";
    var bgCanvas = null, bgCtx = null, bgHidVid = null, bgSegmenter = null, bgAnimId = null, bgActive = false;

    function hudInitialPos() {
      var margin = 20;
      var w = 116; // approx hud width
      if (pipAttr === "bottom-right") return { right: margin + "px", bottom: margin + "px" };
      if (pipAttr === "bottom-left")  return { left:  margin + "px", bottom: margin + "px" };
      if (pipAttr === "top-right")    return { right: margin + "px", top:    margin + "px" };
      return { left: margin + "px", top: margin + "px" };
    }

    function createHUD() {
      if (hud) return;
      hud = document.createElement("div");
      hud.className = "lc-rec-hud";
      var pos = hudInitialPos();
      Object.keys(pos).forEach(function(k){ hud.style[k] = pos[k]; });

      // On macOS the face comes from the native Presenter Overlay, so we show only
      // the floating controls (timer + pause + stop) — no camera pip, no segmentation.
      if (!isMacSafari) {
        var pipWrap = document.createElement("div");
        pipWrap.className = "lc-rec-hud-pip";
        pipWrap.style.width = pipSize + "px";
        pipWrap.style.height = pipSize + "px";
        hudCamVid = document.createElement("video");
        hudCamVid.autoplay = true; hudCamVid.muted = true; hudCamVid.playsInline = true;
        // Zoom into the face (mirrored) so it fills the circle rather than showing the whole torso.
        hudCamVid.style.transform = "scaleX(-1) scale(" + camZoom + ")";
        var camOffEl = document.createElement("div");
        camOffEl.className = "lc-cam-off"; camOffEl.textContent = "📷";
        pipWrap.appendChild(hudCamVid);
        pipWrap.appendChild(camOffEl);
        bgCanvas = document.createElement("canvas");
        // Backing store rendered well above the CSS circle size so the composited
        // face stays as crisp as the rest of the (often retina/4K) screen capture.
        var bgScale = Math.min(3, Math.max(2, window.devicePixelRatio || 1));
        bgCanvas.width = Math.round(pipSize * bgScale);
        bgCanvas.height = Math.round(pipSize * bgScale);
        bgCtx = bgCanvas.getContext("2d");
        pipWrap.appendChild(bgCanvas);
        bgHidVid = document.createElement("video");
        bgHidVid.autoplay = true; bgHidVid.muted = true; bgHidVid.playsInline = true;
        bgHidVid.style.cssText = "position:absolute;width:1px;height:1px;opacity:0;pointer-events:none";
        document.body.appendChild(bgHidVid);
        hud.appendChild(pipWrap);
      } else {
        // small label so the floating control reads as "recording" without a face
        hudLabel = document.createElement("div");
        hudLabel.className = "lc-rec-hud-timer";
        hudLabel.style.cssText = "background:rgba(15,15,25,.78);color:#fff";
        hudLabel.textContent = "🎬 Ready";
        hud.appendChild(hudLabel);
      }

      hudTimer = document.createElement("div");
      hudTimer.className = "lc-rec-hud-timer";
      hud.appendChild(hudTimer);

      if (isIOS) {
        var iosNote = document.createElement("div");
        iosNote.className = "lc-rec-hud-ios";
        iosNote.textContent = "Start Screen Recording from Control Center";
        hud.appendChild(iosNote);
        hudIosBtn = document.createElement("button");
        hudIosBtn.className = "lc-rec-hud-timer-btn";
        hudIosBtn.textContent = "⏱ Start timer";
        hud.appendChild(hudIosBtn);
        var iosRunning = false, iosStart = 0, iosInterval = null;
        hudIosBtn.addEventListener("click", function(e) {
          e.stopPropagation();
          if (!iosRunning) {
            iosRunning = true; iosStart = Date.now();
            hudIosBtn.className = "lc-rec-hud-timer-btn running";
            hudIosBtn.textContent = "⏹ Stop timer";
            iosInterval = setInterval(function(){ hudTimer.textContent = fmtTime(Date.now()-iosStart); }, 500);
          } else {
            iosRunning = false;
            clearInterval(iosInterval);
            hudIosBtn.className = "lc-rec-hud-timer-btn";
            hudIosBtn.textContent = "⏱ Start timer";
          }
        });
      } else {
        var ctrls = document.createElement("div");
        ctrls.className = "lc-rec-hud-ctrls";
        hudPause = document.createElement("button");
        hudPause.className = "lc-rec-hud-pause";
        hudPause.textContent = "⏸";
        hudPause.title = "Pause";
        hudPause.addEventListener("click", function(e) { e.stopPropagation(); togglePause(); });
        hudPause.style.display = "none";
        hudStop = document.createElement("button");
        hudStop.className = "lc-rec-hud-stop";
        hudStop.textContent = "⏹ Stop";
        hudStop.addEventListener("click", function(e) { e.stopPropagation(); stopOrCancel(); });
        hudStop.style.display = "none";
        ctrls.appendChild(hudPause);
        ctrls.appendChild(hudStop);
        hud.appendChild(ctrls);
      }

      makeDraggable(hud);
      document.body.appendChild(hud);
      refreshHUDCam();
    }

    function destroyHUD() {
      stopBg();
      if (hud) { hud.parentNode && hud.parentNode.removeChild(hud); hud = null; hudCamVid = null; hudTimer = null; hudStop = null; hudPause = null; hudLabel = null; }
      if (bgHidVid) { bgHidVid.parentNode && bgHidVid.parentNode.removeChild(bgHidVid); bgHidVid = null; }
      bgCanvas = null; bgCtx = null;
      if (el && el._lcHidden) { el.style.display = ""; el._lcHidden = false; }
    }

    function refreshHUDCam() {
      if (!hud || isMacSafari || !hudCamVid) return;
      var pipWrap = hud.querySelector(".lc-rec-hud-pip");
      var offEl   = hud.querySelector(".lc-cam-off");
      var showBg  = bgMode !== "none" && useCam && !!camStream;
      if (bgCanvas) bgCanvas.style.display = showBg ? "block" : "none";
      if (useCam && camStream) {
        hudCamVid.srcObject = showBg ? null : camStream;
        hudCamVid.style.display = showBg ? "none" : "block";
        offEl.style.display = "none";
        pipWrap.style.border = "3px solid rgba(255,255,255,.85)";
        if (showBg) startBg(); else stopBg();
      } else {
        hudCamVid.srcObject = null;
        hudCamVid.style.display = "block";
        offEl.style.display = "flex";
        pipWrap.style.border = "3px solid rgba(255,255,255,.3)";
        stopBg();
      }
    }

    function refreshHUD() {
      if (hud) refreshHUDCam();
    }

    function togglePause() {
      if (!recorder) return;
      // Armed but not yet started → the ▶ button begins the actual recording.
      if (recorder.state === "inactive" && armed) { beginRecording(); return; }
      if (recorder.state === "recording") {
        recorder.pause();
        isPaused = true; pauseStart = Date.now();
        if (hudPause) { hudPause.className = "lc-rec-hud-pause paused"; hudPause.textContent = "▶"; hudPause.title = "Resume"; }
        dotEl.classList.remove("live");
        setStatus("⏸ Paused — resume from the floating panel.");
      } else if (recorder.state === "paused") {
        recorder.resume();
        isPaused = false; pausedAccum += Date.now() - pauseStart;
        if (hudPause) { hudPause.className = "lc-rec-hud-pause"; hudPause.textContent = "⏸"; hudPause.title = "Pause"; }
        dotEl.classList.add("live");
        setStatus("● Recording — stop via the floating panel.");
      }
    }

    // Actually begin encoding (called from the ▶ Start button once the user has set
    // up Presenter Overlay / is ready). Until then we only hold the streams.
    function beginRecording() {
      if (!recorder || recorder.state !== "inactive" || !armed) return;
      armed = false; endNote = "";
      try { recorder.start(1000); } catch (e) { setStatus("❌ " + e.message, "err"); return; }
      startTs = Date.now();
      isPaused = false; pausedAccum = 0;
      dotEl.classList.add("live");
      if (hudLabel) hudLabel.textContent = "🎬 Recording";
      if (hudPause) { hudPause.className = "lc-rec-hud-pause"; hudPause.textContent = "⏸"; hudPause.title = "Pause"; }
      if (hudStop)  hudStop.textContent = "⏹ Stop";
      btnEl.className = "lc-rec-btn stop"; btnEl.textContent = "⏹ Stop";
      clearInterval(timerInterval);
      timerInterval = setInterval(function(){
        if (!hudTimer) return;
        var elapsed = Date.now() - startTs - pausedAccum - (isPaused ? Date.now() - pauseStart : 0);
        hudTimer.textContent = fmtTime(elapsed);
      }, 500);
      setStatus("● Recording — stop via the floating panel.");
    }

    // Stop (after start) → review; cancel (while still armed) → discard, no review.
    function stopOrCancel() {
      if (!recorder) return;
      if (recorder.state === "recording" || recorder.state === "paused") { recorder.stop(); return; }
      if (recorder.state === "inactive" && armed) {
        armed = false;
        clearInterval(timerInterval);
        try { if (activeStream) activeStream.getTracks().forEach(function(t){ t.stop(); }); } catch (e) {}
        if (camStream) { camStream.getTracks().forEach(function(t){ t.stop(); }); camStream = null; }
        releaseAudioMix();
        destroyHUD();
        dotEl.classList.remove("live");
        isPaused = false; pausedAccum = 0;
        btnEl.disabled = false; btnEl.className = "lc-rec-btn again"; btnEl.textContent = "▶ Record again";
        [optCam, optMic, optSnd].filter(Boolean).forEach(function(o){ o.style.pointerEvents = ""; o.style.opacity = ""; });
        if (hooks.onStop) hooks.onStop();
        setStatus("Cancelled — nothing was saved.");
      }
    }

    /* ── Review before save ── */
    function showReview(blob) {
      var url = URL.createObjectURL(blob);
      var ts  = new Date().toISOString().slice(0,19).replace(/:/g,"-");
      var fname = "recording-" + ts + "." + ext;
      var mb = (blob.size / 1048576).toFixed(1);
      var ov = document.createElement("div");
      ov.className = "lc-rec-ov";
      ov.innerHTML = [
        '<div class="lc-rec-panel">',
        '  <button class="lc-rec-panel-close" title="Discard">✕</button>',
        '  <video class="lc-rec-review-vid" controls autoplay playsinline></video>',
        '  <div class="lc-rec-review-body">',
        endNote ? '    <div class="lc-rec-review-warn">⚠️ ' + endNote + '</div>' : '',
        '    <div class="lc-rec-review-meta">' + fname + ' · ' + mb + ' MB</div>',
        '    <div class="lc-rec-review-acts">',
        '      <button class="lc-rb-save">⬇ Save</button>',
        '      <button class="lc-rb-yt">📹 YouTube</button>',
        '      <button class="lc-rb-again">↻ Re-record</button>',
        '      <button class="lc-rb-discard">🗑 Discard</button>',
        '    </div>',
        '    <div class="lc-rb-yt-area" style="margin-top:10px;"></div>',
        '  </div>',
        '</div>'
      ].join("");
      document.body.appendChild(ov);
      ov.querySelector("video").src = url;
      function close() { URL.revokeObjectURL(url); ov.parentNode && ov.parentNode.removeChild(ov); }
      ov.querySelector(".lc-rb-save").addEventListener("click", function() {
        var a = document.createElement("a");
        a.href = url; a.download = fname; a.click();
        setStatus("✅ Saved as " + fname, "ok");
        close();
      });
      ov.querySelector(".lc-rb-yt").addEventListener("click", function() {
        var ytBtn = ov.querySelector(".lc-rb-yt");
        ytBtn.disabled = true;
        var area = ov.querySelector(".lc-rb-yt-area");
        var title = (document.title || "Lightcodepedia recording").replace(/\s*[|·—]\s*Lightcodepedia.*$/i, "").trim() || "Lightcodepedia recording";
        if (window.lcYtUploadBlob) {
          window.lcYtUploadBlob(blob, blob.type || "video/webm", title, area);
        } else {
          area.textContent = "⚠️ Upload module not ready, try again.";
          ytBtn.disabled = false;
        }
      });
      ov.querySelector(".lc-rb-again").addEventListener("click", function() {
        close();
        startRecording();
      });
      var discard = function() { setStatus("Recording discarded.", ""); close(); };
      ov.querySelector(".lc-rb-discard").addEventListener("click", discard);
      ov.querySelector(".lc-rec-panel-close").addEventListener("click", discard);
      ov.addEventListener("click", function(e) { if (e.target === ov) discard(); });
    }

    /* ── Virtual background (MediaPipe Selfie Segmentation) ── */
    function loadMediaPipe(cb) {
      if (window.SelfieSegmentation) { cb(); return; }
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation@0.1/selfie_segmentation.js";
      s.crossOrigin = "anonymous";
      s.onload  = function() { window.SelfieSegmentation ? cb() : setStatus("⚠️ BG model unavailable","err"); };
      s.onerror = function() { setStatus("⚠️ BG model failed to load","err"); };
      document.head.appendChild(s);
    }

    function startBg() {
      if (!bgCanvas || !bgHidVid || !camStream) return;
      bgActive = true;
      bgHidVid.srcObject = camStream;
      if (bgSegmenter) { bgLoop(); return; }
      setStatus("Loading background model…");
      loadMediaPipe(function() {
        bgSegmenter = new SelfieSegmentation({ locateFile: function(f) {
          return "https://cdn.jsdelivr.net/npm/@mediapipe/selfie_segmentation@0.1/" + f;
        }});
        bgSegmenter.setOptions({ modelSelection: 1 });
        bgSegmenter.onResults(onSegResults);
        bgSegmenter.initialize().then(function() { setStatus(""); bgLoop(); });
      });
    }

    function stopBg() {
      bgActive = false;
      if (bgAnimId) { cancelAnimationFrame(bgAnimId); bgAnimId = null; }
      if (bgHidVid) bgHidVid.srcObject = null;
    }

    function bgLoop() {
      if (!bgActive) return;
      bgAnimId = requestAnimationFrame(function() {
        if (!bgActive || bgMode === "none" || !bgSegmenter) return;
        if (bgHidVid && bgHidVid.readyState >= 2) {
          bgSegmenter.send({ image: bgHidVid }).then(bgLoop).catch(bgLoop);
        } else {
          bgLoop();
        }
      });
    }

    function onSegResults(results) {
      if (!bgCtx || !bgCanvas || bgMode === "none") return;
      var w = bgCanvas.width, h = bgCanvas.height;
      bgCtx.clearRect(0, 0, w, h);
      var iw = bgHidVid.videoWidth  || w;
      var ih = bgHidVid.videoHeight || h;
      // "cover" scale × user zoom so the face fills the circle, then re-centre.
      var scale = Math.max(w / iw, h / ih) * camZoom;
      var sw = iw * scale, sh = ih * scale;
      var dx = (w - sw) / 2, dy = (h - sh) / 2;
      // Feather amount scales with the (hi-res) canvas so the contour stays soft
      // regardless of circle size — this hides the jagged segmentation edge.
      var feather = Math.max(2, Math.round(w * 0.018));

      // Person pixels, then keep only what the (blurred → soft-edged) mask covers.
      bgCtx.save();
      bgCtx.drawImage(results.image, dx, dy, sw, sh);
      bgCtx.globalCompositeOperation = "destination-in";
      bgCtx.filter = "blur(" + feather + "px)";
      bgCtx.drawImage(results.segmentationMask, dx, dy, sw, sh);
      bgCtx.filter = "none";
      bgCtx.restore();

      // Background painted behind the person.
      bgCtx.save();
      bgCtx.globalCompositeOperation = "destination-over";
      if (bgMode === "blur") {
        bgCtx.filter = "blur(18px)";
        bgCtx.drawImage(results.image, dx, dy, sw, sh);
        bgCtx.filter = "none";
        bgCtx.fillStyle = "#111";
        bgCtx.fillRect(0, 0, w, h);
      } else {
        var bgColors = { dark: "#1a1a2e", blue: "#0d3b66", green: "#1a472a", white: "#f5f5f5" };
        bgCtx.fillStyle = bgColors[bgMode] || "#111";
        bgCtx.fillRect(0, 0, w, h);
      }
      bgCtx.restore();
    }

    /* ── Drag ── */
    function makeDraggable(el) {
      var startX, startY, startL, startT, startR, startB;
      function getPos(e) {
        return e.touches ? { x: e.touches[0].clientX, y: e.touches[0].clientY }
                         : { x: e.clientX,            y: e.clientY };
      }
      function onStart(e) {
        if (e.target.tagName === "BUTTON") return;
        var p = getPos(e);
        startX = p.x; startY = p.y;
        var r = el.getBoundingClientRect();
        startL = r.left; startT = r.top;
        el.style.right = el.style.bottom = "auto";
        el.style.left = startL + "px"; el.style.top = startT + "px";
        document.addEventListener("mousemove", onMove);
        document.addEventListener("touchmove", onMove, { passive: false });
        document.addEventListener("mouseup",   onEnd);
        document.addEventListener("touchend",  onEnd);
      }
      function onMove(e) {
        if (e.cancelable) e.preventDefault();
        var p = getPos(e);
        var nx = startL + p.x - startX;
        var ny = startT + p.y - startY;
        nx = Math.max(0, Math.min(window.innerWidth  - el.offsetWidth,  nx));
        ny = Math.max(0, Math.min(window.innerHeight - el.offsetHeight, ny));
        el.style.left = nx + "px"; el.style.top = ny + "px";
      }
      function onEnd() {
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("touchmove", onMove);
        document.removeEventListener("mouseup",   onEnd);
        document.removeEventListener("touchend",  onEnd);
      }
      el.addEventListener("mousedown",  onStart);
      el.addEventListener("touchstart", onStart, { passive: true });
    }

    /* ── Camera stream ── */
    var camStream = null;
    function initCam(cb) {
      if (!useCam) { if (cb) cb(); return; }
      navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 1280 } }, audio: false })
        .then(function(s) {
          camStream = s;
          refreshHUDCam();
          if (cb) cb();
        })
        .catch(function() {
          useCam = false; optCam.classList.remove("on");
          if (cb) cb();
        });
    }

    /* ── Button ── */
    btnEl.addEventListener("click", function() {
      if (recorder && (recorder.state === "recording" || recorder.state === "paused")) { recorder.stop(); return; }
      if (armed) { stopOrCancel(); return; }
      if (isIOS) {
        // iOS: show HUD with camera pip, user does native screen recording
        initCam(function() {
          createHUD();
          btnEl.textContent = "✅ Camera active";
          btnEl.disabled = true;
          setStatus("Your camera is floating. Follow the steps above.", "ok");
          if (hooks.onStart) hooks.onStart();
        });
        return;
      }
      startRecording();
    });

    /* ── Desktop recording ── */
    var recorder = null, chunks = [], timerInterval = null;
    var audioCtx = null, extraAudioTracks = [];

    // Releasing devices on navigation matters: desktop recording is single-page, and
    // Safari does NOT reliably free getDisplayMedia/getUserMedia when the page unloads.
    // A leaked camera/screen leaves the NEXT page's recording broken (no overlay,
    // dead controls). So we stop every track on pagehide, and warn before leaving.
    function releaseAudioMix() {
      extraAudioTracks.forEach(function(t){ try { t.stop(); } catch (e) {} });
      extraAudioTracks = [];
      if (audioCtx) { try { audioCtx.close(); } catch (e) {} audioCtx = null; }
    }
    function releaseAllTracks() {
      try { if (activeStream) activeStream.getTracks().forEach(function(t){ t.stop(); }); } catch (e) {}
      try { if (camStream)    camStream.getTracks().forEach(function(t){ t.stop(); }); } catch (e) {}
      releaseAudioMix();
      activeStream = null; camStream = null;
    }
    function isActive() {
      return armed || (recorder && (recorder.state === "recording" || recorder.state === "paused"));
    }
    window.addEventListener("pagehide", function(){ if (isActive()) releaseAllTracks(); });
    window.addEventListener("beforeunload", function(e){
      if (isActive()) { e.preventDefault(); e.returnValue = "You're recording — leaving this page will discard it."; return e.returnValue; }
    });

    function startRecording() {
      btnEl.disabled = true;
      setStatus("Requesting screen share…");
      // Hide the launcher overlay (or in-page widget) immediately — before
      // getDisplayMedia runs — so it's absent from every captured frame.
      if (hooks.onStart) hooks.onStart();
      else if (el) { el.style.display = "none"; el._lcHidden = true; }
      // getDisplayMedia MUST be called synchronously from the user gesture —
      // any preceding async call (e.g. getUserMedia) breaks the gesture chain in Safari.
      navigator.mediaDevices.getDisplayMedia({
            // Safari's MediaRecorder is unstable above ~1080p (crashes after a few
            // seconds), so cap it there. Chrome/Edge/Firefox are stable, so let them
            // capture at the display's native resolution for crisp text.
            video: isSafari
              ? { frameRate: fps, width: { max: 1920 }, height: { max: 1080 } }
              : { frameRate: fps, width: { ideal: 3840 }, height: { ideal: 2160 } },
            audio: useSnd
          })
          .then(function(screenStream) {
            createHUD();
            setStatus("Setting up…");
            // Request camera + mic in ONE getUserMedia call so the browser shows a
            // single permission prompt instead of two. The mic track joins the
            // recording; the camera is only for the HUD pip / Presenter Overlay
            // source (held on macOS so the overlay menu appears) and never recorded.
            var wantCam = useCam || isMacSafari;
            var constraints = {};
            // On macOS we only HOLD the camera so the Presenter Overlay menu appears
            // (macOS does its own high-quality capture for the overlay) — so request
            // it tiny/low-fps to minimise the load that may be crashing Safari.
            if (wantCam)  constraints.video = isMacSafari
              ? { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 }, frameRate: { ideal: 15 } }
              : { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 1280 } };
            if (useMic)   constraints.audio = true;

            var avPromise = (wantCam || useMic)
              ? navigator.mediaDevices.getUserMedia(constraints).then(function(s){ return s; }).catch(function(){ return null; })
              : Promise.resolve(null);

            avPromise.then(function(av) {
              var vidTracks = av && av.getVideoTracks ? av.getVideoTracks() : [];
              var micTracks = av && av.getAudioTracks ? av.getAudioTracks() : [];
              var sysTracks = screenStream.getAudioTracks ? screenStream.getAudioTracks() : [];

              // Get BOTH the page/system sound and the narration into the recording.
              // MediaRecorder only records ONE audio track, so if we have both we mix
              // them through a Web Audio graph into a single track.
              if (sysTracks.length && micTracks.length) {
                try {
                  var AC = window.AudioContext || window.webkitAudioContext;
                  audioCtx = new AC();
                  var dest = audioCtx.createMediaStreamDestination();
                  audioCtx.createMediaStreamSource(new MediaStream(sysTracks)).connect(dest);
                  audioCtx.createMediaStreamSource(new MediaStream(micTracks)).connect(dest);
                  sysTracks.forEach(function(t){ screenStream.removeTrack(t); extraAudioTracks.push(t); });
                  micTracks.forEach(function(t){ extraAudioTracks.push(t); });
                  dest.stream.getAudioTracks().forEach(function(t){ screenStream.addTrack(t); });
                } catch (e) {
                  micTracks.forEach(function(t){ screenStream.addTrack(t); }); // fall back: narration only
                }
              } else if (micTracks.length) {
                micTracks.forEach(function(t){ screenStream.addTrack(t); });
              } // (system audio only → already on screenStream)

              if (vidTracks.length) {
                camStream = new MediaStream(vidTracks);
                if (!isMacSafari) refreshHUDCam();
              } else if (!isMacSafari) {
                useCam = false; if (optCam) optCam.classList.remove("on"); refreshHUDCam();
              }
              launch(screenStream);
            });

            function launch(stream) {
              chunks = [];
              var vs = stream.getVideoTracks()[0].getSettings() || {};
              var W = vs.width || 1920, H = vs.height || 1080;
              var recOpts = {};
              // Safari ignores videoBitsPerSecond — omit it and let the native encoder decide.
              // Other browsers get a generous target scaled to screen resolution.
              if (!isSafari) {
                recOpts.videoBitsPerSecond = Math.min(40000000, Math.max(8000000, Math.round(W * H * fps * 0.25)));
              }
              if (mimeType) recOpts.mimeType = mimeType;
              recorder = new MediaRecorder(stream, recOpts);
              chunks = [];
              recorder.ondataavailable = function(e){ if (e.data.size) chunks.push(e.data); };
              recorder.onstop = function() {
                clearInterval(timerInterval);
                stream.getTracks().forEach(function(t){ t.stop(); });
                if (camStream) { camStream.getTracks().forEach(function(t){ t.stop(); }); camStream = null; }
                releaseAudioMix();
                destroyHUD();
                dotEl.classList.remove("live");
                isPaused = false; pausedAccum = 0; armed = false;
                btnEl.disabled = false; btnEl.className = "lc-rec-btn again"; btnEl.textContent = "▶ Record again";
                [optCam, optMic, optSnd].filter(Boolean).forEach(function(o){ o.style.pointerEvents = ""; o.style.opacity = ""; });
                if (hooks.onStop) hooks.onStop();
                var blob = new Blob(chunks, { type: mimeType || "video/webm" });
                if (!blob.size) { setStatus("Nothing was recorded.", "err"); return; }
                setStatus("Review your recording…");
                showReview(blob);
              };
              // Diagnostics: capture WHY a recording ends, so unexpected Safari/overlay
              // crashes are reported instead of vanishing silently.
              recorder.onerror = function(ev) {
                endNote = "MediaRecorder error: " + ((ev && ev.error && (ev.error.name || ev.error.message)) || "unknown");
                if (recorder && (recorder.state === "recording" || recorder.state === "paused")) { try { recorder.stop(); } catch (e) {} }
              };
              // Fires if the OS/Safari drops the capture (the ~20s overlay crash) OR the
              // user clicks the browser's own "Stop sharing" bar.
              stream.getVideoTracks()[0].addEventListener("ended", function() {
                if (recorder && (recorder.state === "recording" || recorder.state === "paused")) {
                  var secs = Math.round((Date.now() - startTs - pausedAccum) / 1000);
                  endNote = endNote || ("Screen capture ended on its own after " + secs + "s (Safari/Presenter-Overlay limit). Your clip up to that point is below.");
                  recorder.stop();
                } else if (armed) stopOrCancel();
              });

              // ARM, don't start: the screen is already being captured (so macOS
              // offers Presenter Overlay now), but we don't encode until the user
              // presses ▶ Start — giving them time to enable the overlay first.
              activeStream = stream;
              armed = true;
              isPaused = false; pausedAccum = 0;
              if (hudStop)  { hudStop.style.display  = ""; hudStop.textContent = "⏹ Cancel"; }
              if (hudPause) { hudPause.style.display = ""; hudPause.className = "lc-rec-hud-pause paused"; hudPause.textContent = "▶ Start"; hudPause.title = "Start recording"; }
              if (hudTimer) hudTimer.textContent = "Ready";
              if (hudLabel) hudLabel.textContent = "🎬 Ready";
              btnEl.disabled = false; btnEl.className = "lc-rec-btn stop"; btnEl.textContent = "⏹ Cancel";
              setStatus(isMacSafari
                ? "Ready — turn on Presenter Overlay (green icon in the menu bar), then press ▶ Start."
                : "Ready — press ▶ Start on the floating panel when you are.");
              [optCam, optMic, optSnd].filter(Boolean).forEach(function(o){ o.style.pointerEvents = "none"; o.style.opacity = ".5"; });
            }
          })
          .catch(function(e) {
            destroyHUD();
            btnEl.disabled = false;
            setStatus("❌ " + (e.name === "NotAllowedError" ? "Screen share was cancelled." : e.message), "err");
          });
    }
  }

  // Global launcher — open the recorder from anywhere (e.g. the topbar) without
  // needing a .recorder tag on the page. Builds a placeholder, upgrades it inside
  // a modal, and closes the modal chrome once recording starts so it isn't captured.
  window.lcOpenRecorder = function(opts) {
    opts = opts || {};
    if (document.getElementById("lc-rec-launcher")) return;
    var ov = document.createElement("div");
    ov.id = "lc-rec-launcher";
    ov.className = "lc-rec-ov";
    var panel = document.createElement("div");
    panel.className = "lc-rec-panel";
    panel.style.maxWidth = "480px";
    panel.style.background = "transparent";
    panel.style.boxShadow = "none";
    var close = document.createElement("button");
    close.className = "lc-rec-panel-close";
    close.title = "Close"; close.textContent = "✕"; close.style.color = "#fff";
    var p = document.createElement("p");
    p.className = "recorder";
    ["pip","size","zoom","fps","camera","mic","sound"].forEach(function(k){ if (opts[k] != null) p.setAttribute(k, opts[k]); });
    panel.appendChild(close);
    panel.appendChild(p);
    ov.appendChild(panel);
    document.body.appendChild(ov);
    function closeLauncher() { ov.parentNode && ov.parentNode.removeChild(ov); }
    close.addEventListener("click", closeLauncher);
    ov.addEventListener("click", function(e){ if (e.target === ov) closeLauncher(); });
    upgradeRecorder(p, { onStart: closeLauncher });
  };

  // ── YouTube Upload ────────────────────────────────────────────────────────
  (function() {
    var YT_CLIENT = "208252332658-4fmonl09j9qi2mr40ruq5oe5cnhqmeen.apps.googleusercontent.com";
    var YT_SCOPE  = "https://www.googleapis.com/auth/youtube.upload";

    function ytRedirect() { return window.location.origin + "/"; }

    function ytGetToken() {
      var access = localStorage.getItem("lc_yt_access");
      var expiry = parseInt(localStorage.getItem("lc_yt_expiry") || "0", 10);
      return (access && Date.now() < expiry - 60000) ? access : null;
    }

    function ytStartOAuth() {
      localStorage.setItem("lc_yt_return", window.location.href);
      window.location.href = "https://accounts.google.com/o/oauth2/v2/auth?" + new URLSearchParams({
        client_id: YT_CLIENT, redirect_uri: ytRedirect(),
        response_type: "token", scope: YT_SCOPE, state: "lc_yt_oauth"
      });
    }

    // Opens OAuth in a popup so the current page (and any blob) is preserved.
    function ytStartOAuthPopup(onToken) {
      var popup = window.open(
        "https://accounts.google.com/o/oauth2/v2/auth?" + new URLSearchParams({
          client_id: YT_CLIENT, redirect_uri: ytRedirect(),
          response_type: "token", scope: YT_SCOPE, state: "lc_yt_oauth_popup"
        }), "yt_oauth", "width=520,height=640,left=200,top=100"
      );
      function onStorage(e) {
        if (e.key !== "lc_yt_access" || !e.newValue) return;
        window.removeEventListener("storage", onStorage);
        clearInterval(poll);
        if (popup && !popup.closed) try { popup.close(); } catch(x){}
        onToken(e.newValue);
      }
      window.addEventListener("storage", onStorage);
      var poll = setInterval(function() {
        var t = ytGetToken();
        if (t) { clearInterval(poll); window.removeEventListener("storage", onStorage); if (popup && !popup.closed) try { popup.close(); } catch(x){} onToken(t); return; }
        if (popup && popup.closed) { clearInterval(poll); window.removeEventListener("storage", onStorage); }
      }, 600);
    }

    function handleYtCallback() {
      var hash = window.location.hash;
      if (hash && hash.indexOf("access_token") !== -1) {
        var hp = new URLSearchParams(hash.replace(/^#/, ""));
        var token = hp.get("access_token"), state = hp.get("state");
        var expiresIn = parseInt(hp.get("expires_in") || "3600", 10);
        if (token && (state === "lc_yt_oauth" || state === "lc_yt_oauth_popup")) {
          localStorage.setItem("lc_yt_access", token);
          localStorage.setItem("lc_yt_expiry", String(Date.now() + expiresIn * 1000));
          window.history.replaceState({}, "", window.location.pathname);
          if (state === "lc_yt_oauth_popup") { window.close(); return; }
          localStorage.setItem("lc_yt_open_upload", "1");
          window.location.href = localStorage.getItem("lc_yt_return") || "/";
        }
        return;
      }
      if (localStorage.getItem("lc_yt_open_upload") === "1") {
        localStorage.removeItem("lc_yt_open_upload");
        openYtModal();
      }
    }

    // Insert a .video embed into the current page file via GitHub API.
    function ytInsertIntoPage(videoUrl, statusEl) {
      var pat = localStorage.getItem("lc_ed_pat");
      if (!pat || !_lcSiteRepo) {
        if (statusEl) statusEl.textContent = "⚠️ Sign in to GitHub to insert into page.";
        return;
      }
      var pathname = window.location.pathname.replace(/\/$/, "") || "/index";
      var filePath = "docs" + (pathname === "/" ? "/index" : pathname) + ".md";
      var hdrs = { "Authorization": "token " + pat, "Content-Type": "application/json" };
      var base = "https://api.github.com/repos/" + _lcSiteRepo + "/contents/";
      if (statusEl) statusEl.textContent = "Saving to page…";
      fetch(base + filePath, { headers: hdrs })
        .then(function(r){ return r.json(); })
        .then(function(data) {
          var existing = decodeURIComponent(escape(atob(data.content.replace(/\s/g, ""))));
          var snippet = "\n\n[Recording](" + videoUrl + ")\n{: .video }\n";
          var updated = btoa(unescape(encodeURIComponent(existing + snippet)));
          return fetch(base + filePath, {
            method: "PUT", headers: hdrs,
            body: JSON.stringify({ message: "Add YouTube recording", content: updated, sha: data.sha })
          });
        })
        .then(function(r){ return r.json(); })
        .then(function(d){
          if (statusEl) statusEl.textContent = d.content ? "✅ Added to page!" : "❌ " + (d.message || "Save failed");
        })
        .catch(function(e){ if (statusEl) statusEl.textContent = "❌ " + e.message; });
    }

    // Core upload: takes a File or Blob, returns videoUrl via onDone(url) or onDone(null, err).
    function ytDoUpload(token, fileOrBlob, title, mimeType, onProgress, onDone) {
      fetch("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + token,
          "Content-Type": "application/json",
          "X-Upload-Content-Type": mimeType,
          "X-Upload-Content-Length": String(fileOrBlob.size)
        },
        body: JSON.stringify({
          snippet: { title: title, description: "Recorded on Lightcodepedia · " + new Date().toLocaleDateString() },
          status: { privacyStatus: "unlisted" }
        })
      }).then(function(r){
        if (!r.ok) return r.text().then(function(t){ throw new Error(r.status + ": " + t); });
        var uploadUrl = r.headers.get("Location");
        if (!uploadUrl) throw new Error("No upload URL returned");
        var xhr = new XMLHttpRequest();
        xhr.open("PUT", uploadUrl);
        xhr.setRequestHeader("Content-Type", mimeType);
        xhr.upload.onprogress = function(e){
          if (e.lengthComputable && onProgress) onProgress(Math.round(e.loaded/e.total*100), e.loaded, e.total);
        };
        xhr.onload = function(){
          if (xhr.status === 200 || xhr.status === 201) {
            var d; try { d = JSON.parse(xhr.responseText); } catch(x){ d = {}; }
            if (d.id) onDone("https://youtu.be/" + d.id);
            else onDone(null, "No video ID in response");
          } else { onDone(null, "Upload failed (" + xhr.status + ")"); }
        };
        xhr.onerror = function(){ onDone(null, "Network error"); };
        xhr.send(fileOrBlob);
      }).catch(function(e){ onDone(null, e.message); });
    }

    // Render upload progress + result UI into a container div.
    function ytShowUploadUI(container, fileOrBlob, mimeType, title) {
      container.innerHTML = [
        '<div style="background:#eee;border-radius:99px;height:6px;overflow:hidden;margin-bottom:6px;">',
          '<div class="lc-yt-bar" style="background:#ff0000;height:6px;width:0;transition:width .3s;border-radius:99px;"></div>',
        '</div>',
        '<div class="lc-yt-pct" style="font-size:0.8em;color:#555;text-align:center;margin-bottom:8px;">Starting upload…</div>',
        '<div class="lc-yt-result" style="display:none;">',
          '<input class="lc-yt-url" readonly style="width:100%;padding:7px 9px;border:1px solid #ddd;border-radius:7px;font-size:0.82em;box-sizing:border-box;background:#f9f9f9;margin-bottom:6px;">',
          '<div style="display:flex;gap:6px;flex-wrap:wrap;">',
            '<button class="lc-yt-copy" style="flex:1;padding:7px;background:#065fd4;color:#fff;border:none;border-radius:7px;cursor:pointer;font-size:0.85em;font-weight:600;">📋 Copy URL</button>',
            '<button class="lc-yt-insert" style="flex:1;padding:7px;background:#2e7d32;color:#fff;border:none;border-radius:7px;cursor:pointer;font-size:0.85em;font-weight:600;">📄 Insert into page</button>',
          '</div>',
          '<div class="lc-yt-insert-status" style="font-size:0.78em;color:#555;margin-top:5px;text-align:center;min-height:1em;"></div>',
        '</div>'
      ].join("");
      var barEl    = container.querySelector(".lc-yt-bar");
      var pctEl    = container.querySelector(".lc-yt-pct");
      var resultEl = container.querySelector(".lc-yt-result");
      var urlEl    = container.querySelector(".lc-yt-url");
      var copyEl   = container.querySelector(".lc-yt-copy");
      var insEl    = container.querySelector(".lc-yt-insert");
      var insStEl  = container.querySelector(".lc-yt-insert-status");

      function run(token) {
        ytDoUpload(token, fileOrBlob, title, mimeType,
          function(pct, loaded, total){
            barEl.style.width = pct + "%";
            pctEl.textContent = "Uploading… " + pct + "% (" + Math.round(loaded/1048576) + " / " + Math.round(total/1048576) + " MB)";
          },
          function(videoUrl, err){
            if (err) { pctEl.textContent = "❌ " + err; return; }
            barEl.style.width = "100%";
            pctEl.textContent = "✅ Upload complete!";
            resultEl.style.display = "block";
            urlEl.value = videoUrl;
            copyEl.onclick = function(){
              if (navigator.clipboard) navigator.clipboard.writeText(videoUrl);
              else { urlEl.select(); urlEl.setSelectionRange(0,99999); document.execCommand("copy"); }
              copyEl.textContent = "✅ Copied!";
            };
            insEl.onclick = function(){ insEl.disabled = true; ytInsertIntoPage(videoUrl, insStEl); };
          }
        );
      }

      var token = ytGetToken();
      if (token) { run(token); return; }
      pctEl.textContent = "Connecting YouTube…";
      ytStartOAuthPopup(function(t){ run(t); });
    }

    function openYtModal() {
      if (document.getElementById("lc-yt-modal")) return;
      var ov = document.createElement("div");
      ov.id = "lc-yt-modal";
      ov.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:2147483646;display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;";
      ov.innerHTML = [
        '<div style="background:#fff;border-radius:16px;padding:28px 24px;max-width:400px;width:100%;font-family:-apple-system,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.3);">',
          '<div style="font-size:1.1em;font-weight:700;margin-bottom:8px;">📹 Upload to YouTube</div>',
          '<div style="font-size:0.85em;color:#555;margin-bottom:20px;">Pick your recording. It will be uploaded as <strong>unlisted</strong> to your YouTube channel.</div>',
          '<input type="file" id="lc-yt-file" accept="video/*" style="width:100%;margin-bottom:16px;font-size:0.9em;box-sizing:border-box;">',
          '<div id="lc-yt-upload-area" style="margin-bottom:12px;"></div>',
          '<div style="display:flex;gap:8px;">',
            '<button id="lc-yt-upload-btn" style="flex:1;padding:10px;background:#ff0000;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.95em;">⬆ Upload</button>',
            '<button id="lc-yt-close" style="padding:10px 16px;background:#f0f0f0;border:none;border-radius:8px;cursor:pointer;font-size:0.9em;">Cancel</button>',
          '</div>',
          '<div id="lc-yt-disconnect" style="margin-top:14px;text-align:center;font-size:0.75em;color:#bbb;cursor:pointer;text-decoration:underline;">Disconnect YouTube account</div>',
        '</div>'
      ].join("");
      document.body.appendChild(ov);
      document.getElementById("lc-yt-close").onclick = function(){ ov.remove(); };
      document.getElementById("lc-yt-disconnect").onclick = function(){
        localStorage.removeItem("lc_yt_access"); localStorage.removeItem("lc_yt_expiry"); ov.remove();
      };
      document.getElementById("lc-yt-upload-btn").onclick = function(){
        var file = document.getElementById("lc-yt-file").files[0];
        if (!file) { alert("Please select a video file first."); return; }
        document.getElementById("lc-yt-upload-btn").style.display = "none";
        var title = (document.title || "Lightcodepedia recording").replace(/\s*[|·—]\s*Lightcodepedia.*$/i, "").trim() || "Lightcodepedia recording";
        ytShowUploadUI(document.getElementById("lc-yt-upload-area"), file, file.type || "video/mp4", title);
      };
    }

    handleYtCallback();

    window.lcOpenYtUpload = function() {
      var token = ytGetToken();
      if (token) openYtModal(); else ytStartOAuth();
    };

    // Called from the recorder review panel with the recorded blob.
    window.lcYtUploadBlob = function(blob, mimeType, title, container) {
      ytShowUploadUI(container, blob, mimeType, title);
    };
  })();

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.recorder", upgradeRecorder);
  }

})();
</script>
