@component(attrs=[{"n": "playing", "t": "bool"}, {"n": "label", "t": "str"}])
class AvatarTrigger(Block):
    """▶️ "Ask Doc for a tour!" — the line a reader taps to start a guide."""
    target     = Attr("Avatar")                     # the guide it starts
    story      = Attr(str)                          # the story it asks for
    pick       = Attr(str)                          # the face the guide wears for it
    label_stop = Attr(str, column="label-stop")     # what it says while the guide talks — tap to stop
    @property
    def playing(self):
        return self.has_class("playing")

    @property
    def label(self):
        return self.text

    @target.getter
    def target(self):
        gid = self._attr("data-avt-target") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
        return _wrap(el)


def _lc_doc_data(obj):
    """The problem-space documents register their data as a dataset under
    their own id — hand back that JS object so a proof asserts on fields
    (self.page.<id>.data.name), not markup."""
    ds = getattr(js.window, "lcDatasets", None)
    eid = obj._attr("data-lc-id") or ""
    return getattr(ds, eid, None) if (ds and eid) else None


def _lc_ref(obj, attr):
    gid = obj._attr(attr) or ""
    el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
    return _wrap(el)
