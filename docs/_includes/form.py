@component(methods=["submit", "set"])
class Form(Block):
    """☷ One record as a card — its own fence, a file, or the row picked in a grid."""
    title    = Attr(str)                    # its title bar
    format   = Attr(str, "yaml")            # yaml, csv or json — the fence's or the file's
    editable = Attr(bool)                   # fields can be typed in (a card on a class edits unless "false")
    fields   = Attr(str)                    # which fields show, in order — name: int takes a number (a card on a plain list)
    locked   = Attr(str)                    # fields shown, never typed in, comma-separated
    compute  = Attr(str)                    # ƒ fields the card derives from the others
    persist  = Attr(str)                    # where typed values are kept between visits
    sliders  = Attr(str)                    # numeric fields drawn as range gauges, comma-separated
    min      = Attr(float)                  # the gauges' lowest value
    max      = Attr(float)                  # the gauges' highest value
    step     = Attr(float)                  # the gauges' step
    options  = Attr(str)                    # pick lists — field=a|b|c; field2=x|y
    hints    = Attr(str)                    # a tip per field — field: tip; …
    bound    = Attr(str)                    # the older name of master
    master   = Attr("Datagrid")             # the grid whose picked row the card shows
    source   = Attr("Dataset")              # the file or dataset the card reads

    def __setattr__(self, name, value):
        """`page.ask.name = "Ada"` types the field, like a person would.

        Reading was already pythonistic (`.data.name`); writing needed
        `.set("name", …)`, and Michel wrote the natural line in a scenario
        (2026-09-01) — it set a dead attribute on the wrapper and the form
        never moved. A name that IS one of this form's fields now goes
        through the same edit path a keystroke takes; anything else stays a
        plain attribute, so the wrapper's own internals are untouched.
        """
        if not name.startswith("_"):
            try:
                if name in self.data._d:
                    self.set(name, value)
                    return
            except Exception:
                pass
        object.__setattr__(self, name, value)

    @master.getter
    def master(self):
        gid = self._attr("data-bound") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']") if gid else None
        return _wrap(el)

    @property
    def data(self):
        """Live field values as attributes: self.page.<form>.data.<field>.
        The form republishes its object to data-lc-value on every edit."""
        import json
        raw = self._attr("data-lc-value") or "{}"
        try:
            d = json.loads(raw)
        except Exception:
            d = {}
        return _Attrs(d)

    def set(self, field, value):
        """Type one field, the way a person does.

        A SCENARIO HAS TO BE ABLE TO ACT. Every When in this course read
        "when the page has settled", which changes nothing, so Given/When/Then
        collapsed into three ways of saying Then (Michel, 2026-08-06). This
        goes through the grid's own edit path — setDataValue, then
        onCellValueChanged, the model, data-lc-value and the lc-model-changed
        bus — so every cell watching this form recomputes exactly as it would
        for a human keystroke. Returns True when the field was found.
        """
        fn = getattr(js.window, "lcFormSet", None)
        if fn is None:
            return False
        # self.id, not self._id — a Form is an element wrapper (Object keeps
        # _el); only Dataset and its kin carry a bare _id string
        return bool(fn(self.id, field, value))

    def submit(self):
        return self._tap("button[type=submit], .lc-form-submit")
