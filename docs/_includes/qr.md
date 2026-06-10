{%- comment -%}
QR — QR code with optional caption, activated from md + IAL:
a code block (first line = text, rest = label) + {: .qr size="180" }

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
    var text = lines[0] || "";
    var label = lines.length > 1 ? lines.slice(1).join(" ").trim() : "";
    var size = parseInt(el.getAttribute("size") || "180", 10);
    if (!text) return;
    var wrap = document.createElement("div");
    wrap.className = "lc-qr";
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

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.qr, pre.qr", upgradeQr);
  }

})();
</script>
