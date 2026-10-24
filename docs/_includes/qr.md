{%- comment -%}
QR — QR code with optional caption, activated from md + IAL:
a code block (first line = text, rest = label) + {: .qr size="180" }
here="true" encodes this page; ship="<app>" encodes the app's latest ship
(the whole block is then the label).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-qr { display: inline-block; text-align: center; margin: 1em 0; padding: 1em 1.2em; background: #fff; border: 1px solid #ddd; border-radius: 8px; }
.lc-qr canvas, .lc-qr img { display: block; }
.lc-qr-label { font-size: 0.85em; color: #555; margin-top: 0.6em; }
</style>

<script>
(function () {
  if (window._lcQrReady) return;
  window._lcQrReady = true;

  var _qrcodeQ = null;
  function loadQRCode(cb) {
    if (window.QRCode) { cb(); return; }
    if (_qrcodeQ) { _qrcodeQ.push(cb); return; }
    _qrcodeQ = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/gh/davidshimjs/qrcodejs/qrcode.min.js";
    s.onload = function() { var q = _qrcodeQ; _qrcodeQ = null; q.forEach(function(f){ f(); }); };
    document.head.appendChild(s);
  }

  function upgradeQr(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
    var here = (el.getAttribute("here") || "") === "true";
    var ship = (el.getAttribute("ship") || "").trim();
    if (ship) return shipQr(el, ship, lines);
    /* THE PAGE YOU ARE ON, NOT A URL YOU TYPED (Michel, 2026-08-12: *"the
       qr should be generated from the current page — present mode already
       does it, reuse it"*). Present mode's 📷 share encodes location.href;
       so does this. In the runner that href already carries #src=gh:…, so
       a course page hands out its own address without naming its vault —
       and it stays right when the course moves. */
    /* on a shared page, "this page" is its short link — encoded and
       printed, so a slide or a whiteboard can carry it (share.md) */
    var short = here && window.lcShortHere ? window.lcShortHere : "";
    var text = here ? (short || location.href) : (lines[0] || "");
    var label = here ? lines.join(" ").trim()
                     : (lines.length > 1 ? lines.slice(1).join(" ").trim() : "");
    if (short) label = (label ? label + " · " : "") + short.replace(/^https?:\/\//, "");
    var size = parseInt(el.getAttribute("size") || "180", 10);
    if (!text) return;
    var wrap = document.createElement("div");
    wrap.className = "lc-qr";
    /* what was encoded, in the open: the drawing is a canvas nobody can read
       back, so the address lives on the element for a check (and for x-ray) */
    wrap.setAttribute("data-lc-text", text);
    var qrDiv = document.createElement("div");
    wrap.appendChild(qrDiv);
    if (label) {
      var cap = document.createElement("div");
      cap.className = "lc-qr-label";
      cap.textContent = label;
      wrap.appendChild(cap);
    }
    el.parentNode.replaceChild(wrap, el);
    loadQRCode(function() {
      new QRCode(qrDiv, { text: text, width: size, height: size, correctLevel: QRCode.CorrectLevel.M });
    });
  }

  /* THE DEPLOYED APP, NOT THIS PAGE: ship="<app>" encodes the address the
     🚀 button just made — resolved through the bay's ledger exactly like a
     runner's src="ship:<app>", so a phone opens the public copy, keyless.
     Before the first ship it waits, and redraws on every ship of its app. */
  function shipQr(el, app, lines) {
    var size = parseInt(el.getAttribute("size") || "180", 10);
    var hostEl = el.closest && el.closest("[data-lc-src-repo]");
    var host = (hostEl && hostEl.getAttribute("data-lc-src-repo")) || "";
    var bay = el.getAttribute("bay") || "";
    var wrap = document.createElement("div");
    wrap.className = "lc-qr lc-qr-ship";
    if (el.id) wrap.id = el.id;
    var qrDiv = document.createElement("div");
    var cap = document.createElement("div");
    cap.className = "lc-qr-label";
    wrap.appendChild(qrDiv); wrap.appendChild(cap);
    el.parentNode.replaceChild(wrap, el);
    var label = lines.join(" ").trim();
    function draw() {
      var resolve = window.lcResolveShip;
      if (!resolve) { cap.textContent = "🚀 Nothing shipped yet"; return; }
      resolve(app, bay, host).then(function (real) {
        if (!real) {
          qrDiv.innerHTML = ""; wrap.removeAttribute("data-lc-text");
          cap.textContent = "🚀 Nothing shipped yet — press Ship, and the square appears.";
          return;
        }
        var path = window.lcHref ? window.lcHref("/run.html") : "/run.html";
        var text = location.origin + path + "#src=" + real;
        wrap.setAttribute("data-lc-text", text);
        cap.textContent = label;
        loadQRCode(function () {
          qrDiv.innerHTML = "";
          new QRCode(qrDiv, { text: text, width: size, height: size, correctLevel: QRCode.CorrectLevel.M });
        });
      });
    }
    window.addEventListener("lc_shipped", function (e) {
      if (e.detail && e.detail.app === app) draw();
    });
    draw();
  }

  /* ONE PLACE DRAWS A QR. The classroom console hands out preview links and
     wants the same square a course page shows — same loader, same options,
     no second CDN dance (Michel, 2026-08-13). */
  window.lcQrInto = function (host, text, size) {
    if (!host || !text) return;
    host.innerHTML = "";
    host.setAttribute("data-lc-text", text);
    loadQRCode(function () {
      new QRCode(host, { text: text, width: size || 160, height: size || 160,
                         correctLevel: QRCode.CorrectLevel.M });
    });
  };

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.qr, pre.qr", upgradeQr);
  }

})();
</script>
