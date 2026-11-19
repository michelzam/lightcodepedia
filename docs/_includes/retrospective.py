@component()
class Retrospective(Block):
    """🔁 A sprint's retrospective — keep, improve, stop, start."""
    kept_in = Attr(str, column="save")      # the learner's file it is read from, and 💾 kept in
    source  = Attr("Form")                  # the form whose fields it reads, when it has no fence of its own

    @source.getter
    def source(self):
        return _lc_ref(self, "data-bind")

    @property
    def data(self):
        return _lc_doc_data(self)
