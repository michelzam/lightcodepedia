{%- comment -%}
imgload — "type a URL, click Analyse, embed the image".

Renders a two-section accordion: a Source-URL field, and an Analysis section
with a button that loads the image from that URL. Nothing is fetched until the
button is clicked, and the URL lives only in the field (remembered per-browser
in localStorage) — so a presenter can load an external image live (e.g. while
screen-recording) without putting the URL on screen or committing the image to
the repo. Collapse the URL section to keep it off-camera.

Usage:
  [Analyse](#)
  {: .imgload #karma_analysis }

  [Analyse](#)
  {: .imgload placeholder="paste an image URL…" }

Auto-included by docs/_layouts/default.html. Reuses the .lc-accordion styling.
{%- endcomment -%}

<style>
.lc-imgload { margin: 1em 0; }
.lc-imgload .lc-ac-body { padding: 0.8em 1em; }
.lc-imgload-url { width: 100%; box-sizing: border-box; padding: 0.5em 0.7em; border: 1px solid #cbd5e1;
  border-radius: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.9em; color: #1e293b; }
.lc-imgload-url:focus { outline: none; border-color: #0066cc; box-shadow: 0 0 0 2px rgba(0,102,204,0.15); }
.lc-imgload-hint { margin: 0.4em 0 0; font-size: 0.78em; color: #94a3b8; }
.lc-imgload-btn { background: #0066cc; color: #fff; border: none; border-radius: 6px; padding: 0.5em 1.3em;
  font-size: 0.92em; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.lc-imgload-btn:hover { background: #0052a3; }
.lc-imgload-out { margin-top: 0.8em; }
.lc-imgload-out:empty { display: none; }
.lc-imgload-img { max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0; display: block; }
.lc-imgload-msg { color: #64748b; font-size: 0.88em; margin: 0.4em 0 0; }
.lc-imgload-err { color: #c62828; }
</style>

<script>
(function () {
  if (window._lcImgloadReady) return;
  window._lcImgloadReady = true;

  var SEQ = 0;

  function section(open, summary) {
    var d = document.createElement("details");
    if (open) d.open = true;
    var s = document.createElement("summary");
    s.textContent = summary;
    d.appendChild(s);
    var body = document.createElement("div");
    body.className = "lc-ac-body";
    d.appendChild(body);
    return { el: d, body: body };
  }

  function upgrade(el) {
    if (el.dataset.lcImgloadDone) return;
    el.dataset.lcImgloadDone = "1";

    var label = (el.getAttribute("label") || el.textContent || "Analyse").trim() || "Analyse";
    var placeholder = el.getAttribute("placeholder") || "paste an image URL…";
    var key = el.id || ("imgload" + (++SEQ));

    var wrap = document.createElement("div");
    wrap.className = "lc-imgload lc-accordion";
    if (el.id) { wrap.id = el.id; wrap.setAttribute("data-lc-id", el.id); }

    /* section 1 — the source URL (collapsed by default to keep it off-camera) */
    var s1 = section(false, "🔗 Source URL");
    var input = document.createElement("input");
    input.type = "text";
    input.className = "lc-imgload-url";
    input.placeholder = placeholder;
    input.spellcheck = false;
    var hint = document.createElement("p");
    hint.className = "lc-imgload-hint";
    hint.textContent = "Stays here only (remembered in this browser). Collapse this section to hide it.";
    s1.body.appendChild(input);
    s1.body.appendChild(hint);

    /* section 2 — analyse + the embedded image */
    var s2 = section(false, "🔬 Analysis");
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "lc-imgload-btn";
    btn.textContent = label;
    var out = document.createElement("div");
    out.className = "lc-imgload-out";
    s2.body.appendChild(btn);
    s2.body.appendChild(out);

    wrap.appendChild(s1.el);
    wrap.appendChild(s2.el);
    el.parentNode.replaceChild(wrap, el);

    /* remember the URL per browser so it survives reloads (never leaves the page) */
    var LSK = "lc_imgload_" + key;
    try { var saved = localStorage.getItem(LSK); if (saved) input.value = saved; } catch (e) {}
    input.addEventListener("input", function () { try { localStorage.setItem(LSK, input.value); } catch (e) {} });

    function msg(text, isErr) {
      out.innerHTML = "";
      var p = document.createElement("p");
      p.className = "lc-imgload-msg" + (isErr ? " lc-imgload-err" : "");
      p.textContent = text;
      out.appendChild(p);
    }

    btn.addEventListener("click", function () {
      var url = (input.value || "").trim();
      s2.el.open = true;
      if (!url) { msg("Enter a URL in the Source URL section first."); return; }
      msg("⏳ loading…");
      var img = new Image();
      img.className = "lc-imgload-img";
      img.alt = "analysis";
      img.onload = function () { out.innerHTML = ""; out.appendChild(img); };
      img.onerror = function () { msg("⚠ Could not load an image from that URL.", true); };
      img.src = url;
    });
  }

  /* code_chrome.md provides the scan registry — one registration covers the
     initial scan and every re-scan. */
  window.lcRegisterUpgrader &&
    window.lcRegisterUpgrader("p.imgload, a.imgload", upgrade);
})();
</script>
