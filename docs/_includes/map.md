{%- comment -%}
Map — MapLibre map with CSV/JSON markers, activated from md + IAL:
a code block of label/lat/lon rows + {: .map zoom="12" height="350" }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-map { margin: 1em 0; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
</style>

<script>
(function () {
  if (window._lcMapReady) return;
  window._lcMapReady = true;

  var _maplibreQ = null;
  function loadMapLibre(cb) {
    if (window.maplibregl) { cb(); return; }
    if (_maplibreQ) { _maplibreQ.push(cb); return; }
    _maplibreQ = [cb];
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/npm/maplibre-gl@4/dist/maplibre-gl.css";
    document.head.appendChild(link);
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/maplibre-gl@4/dist/maplibre-gl.js";
    s.onload = function() { var q = _maplibreQ; _maplibreQ = null; q.forEach(function(f){ f(); }); };
    document.head.appendChild(s);
  }

  function upgradeMap(el) {
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var zoom = parseInt(el.getAttribute("zoom") || "12", 10);
    var h = el.getAttribute("height") || "350";
    var gid = "lc-map-" + Math.random().toString(36).slice(2, 7);
    var wrap = document.createElement("div");
    wrap.className = "lc-map";
    wrap.id = gid;
    wrap.style.height = h + "px";
    el.parentNode.replaceChild(wrap, el);
    var markers = [];
    try {
      var parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        parsed.forEach(function(item) {
          var mlat = parseFloat(item.lat), mlon = parseFloat(item.lon != null ? item.lon : item.lng);
          if (!isNaN(mlat) && !isNaN(mlon)) markers.push({ lat: mlat, lon: mlon, label: item.label || item.name || "" });
        });
      }
    } catch(e) {
      var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
      if (lines.length >= 2) {
        var hdrs = lines[0].split(",").map(function(v){ return v.trim(); });
        var nI = ["label","name"].reduce(function(a, k){ return hdrs.indexOf(k) >= 0 ? hdrs.indexOf(k) : a; }, 0);
        var laI = hdrs.indexOf("lat") >= 0 ? hdrs.indexOf("lat") : 1;
        var lnI = ["lon","lng"].reduce(function(a, k){ return hdrs.indexOf(k) >= 0 ? hdrs.indexOf(k) : a; }, 2);
        lines.slice(1).forEach(function(l) {
          var c = l.split(",").map(function(v){ return v.trim(); });
          var mlat = parseFloat(c[laI]), mlon = parseFloat(c[lnI]);
          if (!isNaN(mlat) && !isNaN(mlon)) markers.push({ lat: mlat, lon: mlon, label: c[nI] || "" });
        });
      }
    }
    var centerLat = markers.length ? markers.reduce(function(s,m){ return s+m.lat; }, 0)/markers.length : parseFloat(el.getAttribute("lat") || "48.86");
    var centerLon = markers.length ? markers.reduce(function(s,m){ return s+m.lon; }, 0)/markers.length : parseFloat(el.getAttribute("lon") || "2.35");
    loadMapLibre(function() {
      var map = new maplibregl.Map({
        container: gid,
        style: "https://tiles.openfreemap.org/styles/positron",
        center: [centerLon, centerLat],
        zoom: zoom,
        pitch: parseFloat(el.getAttribute("pitch") || "0"),
        bearing: parseFloat(el.getAttribute("bearing") || "0"),
        maxPitch: 85
      });
      map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");
      if (window.lcRegisterCleanup) window.lcRegisterCleanup(wrap, function() { try { map.remove(); } catch(e) {} });

      // Shift+drag to pivot in 3D (bearing + pitch), like deck.gl / Streamlit.
      // Horizontal → rotate (bearing); vertical → tilt (pitch).
      var canvas = map.getCanvas();
      var pivot = null;
      canvas.addEventListener("mousedown", function(e) {
        if (!e.shiftKey || e.button !== 0) return;
        pivot = { x: e.clientX, y: e.clientY, bearing: map.getBearing(), pitch: map.getPitch() };
        map.dragPan.disable();
        canvas.style.cursor = "move";
        e.preventDefault();
        e.stopPropagation();
      });
      window.addEventListener("mousemove", function(e) {
        if (!pivot) return;
        map.setBearing(pivot.bearing - (e.clientX - pivot.x) * 0.5);
        map.setPitch(Math.max(0, Math.min(85, pivot.pitch + (e.clientY - pivot.y) * 0.5)));
      });
      window.addEventListener("mouseup", function() {
        if (!pivot) return;
        pivot = null;
        map.dragPan.enable();
        canvas.style.cursor = "";
      });

      markers.forEach(function(m) {
        var dot = document.createElement("div");
        dot.style.cssText = "width:13px;height:13px;background:#e05454;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,0.35);cursor:pointer";
        new maplibregl.Marker({ element: dot })
          .setLngLat([m.lon, m.lat])
          .setPopup(new maplibregl.Popup({ offset: 12 }).setText(m.label))
          .addTo(map);
      });

      // bind="formid": a movable dot that follows a form's lat/lon. Shows
      // learners that values (the form) drive behaviour (where the dot lands) —
      // params → a function call, felt now, named later.
      var bind = el.getAttribute("bind") || "";
      if (bind) {
        var pin = document.createElement("div");
        pin.textContent = el.getAttribute("bindicon") || "📍";
        pin.style.cssText = "font-size:1.7em;line-height:1;cursor:grab;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))";
        var bmarker = new maplibregl.Marker({ element: pin, anchor: "bottom" })
          .setLngLat([centerLon, centerLat])
          .addTo(map);
        function moveBound() {
          var f = document.querySelector(".lc-form[data-lc-id='" + bind + "']");
          if (!f) return;
          try {
            var d = JSON.parse(f.getAttribute("data-lc-value") || "{}");
            var la = parseFloat(d.lat), lo = parseFloat(d.lon != null ? d.lon : d.lng);
            if (!isNaN(la) && !isNaN(lo)) bmarker.setLngLat([lo, la]);
          } catch (e) {}
        }
        document.addEventListener("lc-model-changed", moveBound);
        if (window.lcRegisterCleanup) window.lcRegisterCleanup(wrap, function() {
          document.removeEventListener("lc-model-changed", moveBound);
        });
        moveBound();
      }

      // Hint overlay
      var hint = document.createElement("div");
      hint.textContent = "⇧ Shift + drag to tilt / rotate";
      hint.style.cssText = "position:absolute;bottom:8px;left:8px;background:rgba(255,255,255,0.85);color:#555;font-size:0.72em;padding:3px 8px;border-radius:4px;pointer-events:none;z-index:2";
      wrap.style.position = "relative";
      wrap.appendChild(hint);
    });
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.map, pre.map", upgradeMap);
  }

})();
</script>
