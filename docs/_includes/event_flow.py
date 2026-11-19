@component(attrs=[{"n": "count", "t": "int"}])
class EventFlow(Block):
    """🎏 The page's story as coloured notes — one beat under the user who gives it: ui|data → command → [rule] → event."""
    notes  = Attr(str)                      # sticky draws the notes as stickies; plain otherwise
    legend = Attr(bool, True)               # the legend under it, each chip a dimmer for its kind
    source = Attr("Dataset")                # the beats, read from a dataset instead of its fence
    map    = Attr("ImpactMap")              # the impact map this story tells — each beat serves an impact

    @map.getter
    def map(self):
        """The impact map this story tells (map=) — the pipe says which map."""
        mid = self._attr("data-map") or ""
        el = js.window.document.querySelector("[data-lc-id='" + mid + "']")
        return ImpactMap(el) if el is not None else None

    @property
    def count(self):
        return len(self._qq(".lc-ef-step"))

    def kinds(self):
        """The sequence of note kinds, in order — so a proof can assert
        the grammar (a command before its event, a rule that governs a
        command rather than issuing one)."""
        return [str(o._el.getAttribute("data-kind") or "") for o in self._qq(".lc-ef-step")]


    def elements(self):
        """The flow's cast — every ‘— ref’ tail, collected: #blocks, classes,
        Class.commands, Class[states]. The meta level checks each one against
        the page's own artifacts."""
        return [{"kind": str(o._el.getAttribute("data-el-kind") or ""),
                 "ref": str(o._el.getAttribute("data-el-ref") or "")}
                for o in self._qq(".lc-ef-el")]
