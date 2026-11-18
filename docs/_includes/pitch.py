@component(icon="✨")
class Pitch(Block):
    """✨ Why the product exists — the elevator pitch: for whom, their need, the product, its benefit, unlike, it."""
    kept_in = Attr(str, column="save")      # the learner's file it is read from, and 💾 kept in
    source  = Attr("Form")                  # the form whose fields it reads, when it has no fence of its own
    persona = Attr("Persona")               # the persona it speaks for — its who and need echo it

    @source.getter
    def source(self):
        return _lc_ref(self, "data-bind")

    @persona.getter
    def persona(self):
        return _lc_ref(self, "data-persona")

    @property
    def data(self):
        return _lc_doc_data(self)

    @property
    def drifting(self):
        """True while the who/need stopped echoing the persona this pitch
        reads — the soft warning a proof can assert on."""
        w = self._el.querySelector(".lc-pitch-warn") if self._el is not None else None
        return bool(w is not None and w.hasAttribute("hidden") is False)
