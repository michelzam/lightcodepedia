@component(attrs=[{"n": "cards", "t": "int"}, {"n": "follows", "t": "str"}])
class Inspector(Block):
    """🧬 Live cards over the objects its fence builds — each field editable, each verb a button; the model's own view."""
    source   = Attr("Model")                # the model its objects come from
    bind     = Attr(str)                    # the older name of source
    follow   = Attr("Datagrid")             # the grid whose picked row it shows — a detail of it
    names    = Attr(str)                    # code shows the fields by their Python names
    readonly = Attr(bool)                   # a monitor — nothing typed, the verbs still live

    @source.getter
    def source(self):
        mid = self._attr("data-bind") or ""
        el = js.window.document.querySelector(".lc-model[data-lc-id='" + mid + "']")
        return Model(el) if el is not None else None

    @follow.getter
    def follow(self):
        gid = self._attr("data-bound-to") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']")
        return Datagrid(el) if el is not None else None

    @property
    def cards(self):
        return len(self._qq("[data-card]"))

    @property
    def follows(self):
        return str(self._attr("data-bound-to") or "")

    @property
    def grid(self):
        return self.follow
