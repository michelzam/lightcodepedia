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

  // Glide a marker from one lng/lat to another over ms (rAF interpolation) —
  // smooth, and it doesn't fight MapLibre's own transform like a CSS transition would.
  function animateMarker(marker, from, to, ms, done) {
    var start = null;
    function frame(t) {
      if (start === null) start = t;
      var k = Math.min(1, (t - start) / ms);
      marker.setLngLat([from[0] + (to[0] - from[0]) * k, from[1] + (to[1] - from[1]) * k]);
      if (k < 1) requestAnimationFrame(frame); else if (done) done();
    }
    requestAnimationFrame(frame);
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

      // bind="formid": a movable dot that follows a form's lat/lon, plus an
      // optional fetch="🐕" button that runs a fetcher to the dot and cheers if
      // it landed near target=. Shows learners that values (the form) drive
      // behaviour (where the dot lands, whether Lucky reaches the park) —
      // params → a function call, felt now, named later.
      var bind = el.getAttribute("bind") || "";
      if (bind) {
        wrap.style.position = "relative";
        var ballLngLat = [centerLon, centerLat];
        var pin = document.createElement("div");
        pin.textContent = el.getAttribute("bindicon") || "📍";
        pin.style.cssText = "font-size:1.7em;line-height:1;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))";
        var bmarker = new maplibregl.Marker({ element: pin, anchor: "center" })
          .setLngLat(ballLngLat)
          .addTo(map);

        // fetch="icon": a Fetch button; the fetcher glides to the ball, then
        // cheers only if it's within radius= of target= (both in degrees).
        var fetchIcon = el.getAttribute("fetch") || "";
        var status = null, tgtLngLat = null, inPark = function () { return false; };
        if (fetchIcon) {
          var tg = (el.getAttribute("target") || "").split(",").map(function (s) { return parseFloat(s.trim()); });
          tgtLngLat = (tg.length >= 2 && !isNaN(tg[0]) && !isNaN(tg[1]))
            ? [tg[1], tg[0]]                                      // target= is "lat,lon"
            : (markers.length ? [markers[0].lon, markers[0].lat] : [centerLon, centerLat]);
          var radius = parseFloat(el.getAttribute("radius")); if (isNaN(radius)) radius = 0.004;
          // atomic: fit x AND y independently (a box), not the combined distance
          // — each slider stands on its own, easier to reason about and to land.
          inPark = function () {
            return Math.abs(ballLngLat[0] - tgtLngLat[0]) <= radius
                && Math.abs(ballLngLat[1] - tgtLngLat[1]) <= radius;
          };

          var dog = document.createElement("div");
          dog.textContent = fetchIcon;
          dog.style.cssText = "font-size:1.7em;line-height:1;filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))";
          var dogMarker = new maplibregl.Marker({ element: dog, anchor: "center" })
            .setLngLat(tgtLngLat)                                // waits at the park
            .addTo(map);

          status = document.createElement("div");
          status.style.cssText = "position:absolute;left:50%;top:8px;transform:translateX(-50%);z-index:3;background:rgba(255,255,255,.9);padding:3px 12px;border-radius:12px;font-size:.82em;white-space:nowrap";
          var fbtn = document.createElement("button");
          fbtn.textContent = fetchIcon + " Fetch!";
          fbtn.style.cssText = "position:absolute;left:50%;bottom:10px;transform:translateX(-50%);z-index:3;padding:.4em 1em;border-radius:8px;border:1px solid #6ab04c;background:#fff;cursor:pointer;font:inherit";
          fbtn.addEventListener("click", function () {
            var f0 = dogMarker.getLngLat();
            animateMarker(dogMarker, [f0.lng, f0.lat], ballLngLat, 700, function () {
              status.textContent = inPark() ? "🎾 Fetched! Good boy, Lucky! 🐾" : "🐕 Got it — now land it in the park 🌳!";
            });
          });
          wrap.appendChild(status);
          wrap.appendChild(fbtn);
        }

        // Frame every object (park, ball, Lucky) so they're all visible on load,
        // capped at the author's zoom so it never zooms in past the given level.
        var didFit = false;
        function fitAll() {
          var pts = markers.map(function (m) { return [m.lon, m.lat]; });
          pts.push(ballLngLat);
          if (tgtLngLat) pts.push(tgtLngLat);
          if (pts.length < 2) return;
          var b = new maplibregl.LngLatBounds(pts[0], pts[0]);
          pts.forEach(function (p) { b.extend(p); });
          map.fitBounds(b, { padding: 60, maxZoom: zoom, duration: 0 });
          didFit = true;
        }

        function moveBound() {
          var f = document.querySelector(".lc-form[data-lc-id='" + bind + "']");
          if (!f) return;
          try {
            var d = JSON.parse(f.getAttribute("data-lc-value") || "{}");
            var la = parseFloat(d.lat), lo = parseFloat(d.lon != null ? d.lon : d.lng);
            if (!isNaN(la) && !isNaN(lo)) { ballLngLat = [lo, la]; bmarker.setLngLat(ballLngLat); if (!didFit) fitAll(); }
          } catch (e) {}
          if (status) status.textContent = inPark() ? "🎯 In the park! Hit Fetch 🐕" : "Slide to move the ball 🎾";
        }
        document.addEventListener("lc-model-changed", moveBound);
        if (window.lcRegisterCleanup) window.lcRegisterCleanup(wrap, function () {
          document.removeEventListener("lc-model-changed", moveBound);
        });
        moveBound();
        if (!didFit) fitAll();   // fit park + initial ball even before the form publishes
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
