@component(methods=["pan_to", "set_zoom"])
class Map(Block):
    """🗺️ Places on a map — a dataset's rows as markers, or one point; a dot a form moves."""
    lat      = Attr(float, 48.86)           # where it opens, north–south, when no markers frame it
    lng      = Attr(float, 2.35)            # where it opens, east–west
    lon      = Attr(float)                  # the other spelling of lng
    zoom     = Attr(int, 12)                # 1 the world, 18 a street
    height   = Attr(int, 350)               # pixels
    tiles    = Attr(str, "positron")        # the map's look — positron, liberty, bright
    pitch    = Attr(float, 0)               # tilt, in degrees — 0 seen from above
    bearing  = Attr(float, 0)               # rotation, in degrees — 0 north up
    fit      = Attr(bool, True)             # frames all the markers; false keeps lat, lng and zoom
    engine   = Attr(str)                    # leaflet draws it with Leaflet and OpenStreetMap instead
    bindicon = Attr(str, "📍")              # the dot the form moves
    fetch    = Attr(str)                    # a Fetch button: this icon runs to the dot
    target   = Attr(str)                    # "lat,lon" — where the fetch should land
    radius   = Attr(float, 0.004)           # how near the target counts as there, in degrees
    source   = Attr("Dataset")              # the rows drawn as markers — lat, lng (or lon), label
    bind     = Attr("Form")                 # the form whose lat and lon move the dot

    def pan_to(self, lat, lng):
        if self._el is not None:
            self._el.setAttribute("data-lat", str(lat))
            self._el.setAttribute("data-lng", str(lng))
        return self

    def set_zoom(self, z):
        if self._el is not None:
            self._el.setAttribute("data-zoom", str(z))
        return self
