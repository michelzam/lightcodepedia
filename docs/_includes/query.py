@component(attrs=[{"n": "query", "t": "str"}, {"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"}],
           methods=["run"])
class Query(Dataset):
    """🔎 A dataset computed by SQL over other datasets — it publishes its rows under its id, like any dataset.

    With editable, the SQL comes from a live editor instead of the source."""
    editable = Attr(bool)                   # the SQL shows in an editor the reader can change and run
    bind     = Attr(str)                    # the older name of source
    source   = Attr("Dataset")              # the datasets its SQL reads, comma-separated
    def __init__(self, ref=None):
        self._el = None
        if ref is not None and hasattr(ref, "getAttribute"):   # X-ray wraps by element
            self._el = ref
            self._id = ref.getAttribute("data-lc-id") or ""
        else:                                                  # resolver builds by id
            self._id = ref or ""

    @property
    def query(self):
        return str(self._el.getAttribute("data-query") or "") if self._el is not None else ""

    @editable.getter
    def editable(self):
        return self._el is not None and self._el.getAttribute("data-editable") == "true"

    @source.getter
    def source(self):
        sid = self._el.getAttribute("data-bind") if self._el is not None else None
        return Dataset((str(sid).split(",")[0] if sid else ""))

    def run(self, sql=None):
        """Run SQL in this query — exactly what the reader does by typing in
        the editor and pressing Run. Omit sql to re-run what is there.

        Lets a check rehearse the learner's own move: rewrite the query the
        other way and show that one question, said twice, gives one answer
        (Michel, 2026-09-19). The result is published before this returns,
        so the next step can read it."""
        if self._el is None:
            raise AttributeError("no query #" + str(self._id) + " on this page")
        try:
            fn = self._el._lcRun
        except AttributeError:
            fn = None
        if fn is None:
            raise AttributeError("this query cannot be run from here")
        return str(fn(sql) if sql is not None else fn())
