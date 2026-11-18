@component(icon="🎯")
class ImpactMap(Block):
    """🎯 How the product reaches its goal — a tree: goal, persona, impacts (how), features (what)."""
    valuated  = Attr(bool)                  # each feature shows the value it was given
    estimated = Attr(bool)                  # each feature shows the effort it was estimated at
    pitch     = Attr("Pitch")               # the pitch it grows from — its goal and persona

    @pitch.getter
    def pitch(self):
        return _lc_ref(self, "data-pitch")

    @property
    def data(self):
        """The map as rendered: goal, who, and impacts — each leaf's how,
        what, and the value/effort it may carry (with their reasons)."""
        return _lc_doc_data(self)

    @property
    def features(self):
        """The features its leaves name, in map order — the link from the
        problem space to the solution. A leaf whose card is missing wraps
        None, so .exists says so."""
        out = []
        for o in self._qq(".lc-imap-what a[data-feature]"):
            fid = str(o._el.getAttribute("data-feature") or "")
            el = js.window.document.querySelector(".lc-feature[data-lc-id='" + fid + "']")
            out.append(Feature(el))
        return out
