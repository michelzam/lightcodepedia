from behave import given, then

# MapLibre's engine and tiles live on CDNs this harness cannot reach, so a
# tiny recording stub stands in for it. That keeps the assertions on OUR
# side of the line: which bounds the component asks the engine to frame.


@given("a recording map engine is preinstalled")
def step_stub_maplibre(context):
    context.page.add_init_script("""
      (function () {
        var calls = { fit: [], made: 0 };
        window.__lcMapCalls = calls;
        function Bounds(a, b) {
          this.pts = [];
          if (a) this.pts.push(a);
          if (b) this.pts.push(b);
        }
        Bounds.prototype.extend = function (p) { this.pts.push(p); return this; };
        function Marker() {}
        Marker.prototype.setLngLat = function () { return this; };
        Marker.prototype.setPopup = function () { return this; };
        Marker.prototype.addTo = function () { return this; };
        Marker.prototype.getElement = function () { return document.createElement('div'); };
        Marker.prototype.remove = function () { return this; };
        function Map(opts) {
          calls.made++;
          this._h = {};
          this.opts = opts;
          var el = typeof opts.container === 'string'
            ? document.getElementById(opts.container) : opts.container;
          this._el = el || document.createElement('div');
        }
        Map.prototype.addControl = function () { return this; };
        Map.prototype.on = function (ev, fn) { (this._h[ev] = this._h[ev] || []).push(fn); return this; };
        Map.prototype.once = function (ev, fn) {
          // fire "load" on the next tick — the real engine does the same
          if (ev === 'load') setTimeout(fn, 0); else this.on(ev, fn);
          return this;
        };
        Map.prototype.getCanvas = function () { return document.createElement('canvas'); };
        Map.prototype.getContainer = function () { return this._el; };
        Map.prototype.fitBounds = function (b, o) {
          calls.fit.push({ pts: (b && b.pts) || [], opts: o || {} });
          return this;
        };
        Map.prototype.setBearing = Map.prototype.setPitch = function () { return this; };
        Map.prototype.getBearing = Map.prototype.getPitch = function () { return 0; };
        Map.prototype.getBounds = function () {
          return { getSouthWest: function () { return { lng: 0, lat: 0 }; } };
        };
        Map.prototype.getCenter = function () { return { lng: 0, lat: 0 }; };
        Map.prototype.remove = function () {};
        Map.prototype.dragPan = { disable: function () {}, enable: function () {} };
        window.maplibregl = {
          Map: Map, Marker: Marker, LngLatBounds: Bounds,
          NavigationControl: function () {}, Popup: function () {
            this.setHTML = function () { return this; };
          }
        };
      })();
    """)


@then("the map was fitted around all {n:d} markers")
def step_fitted(context, n):
    context.page.wait_for_function(
        "() => window.__lcMapCalls && window.__lcMapCalls.fit.length > 0",
        timeout=15_000)
    fit = context.page.evaluate("() => window.__lcMapCalls.fit[0]")
    pts = fit["pts"]
    # the first point seeds the bounds twice (sw, ne), then every marker
    # extends it — so all n must be in there
    assert len(pts) >= n, "fit saw %d points, expected at least %d" % (len(pts), n)
    lats = sorted(p[1] for p in pts)
    assert lats[-1] - lats[0] > 0.5, "bounds too tight to hold every campus: %s" % pts


@then("the map was never fitted")
def step_not_fitted(context):
    context.page.wait_for_timeout(1500)
    n = context.page.evaluate(
        "() => (window.__lcMapCalls && window.__lcMapCalls.fit.length) || 0")
    made = context.page.evaluate(
        "() => (window.__lcMapCalls && window.__lcMapCalls.made) || 0")
    assert made > 0, "the map never rendered — the stub was not used"
    assert n == 0, "the map fitted anyway (%d call(s))" % n
