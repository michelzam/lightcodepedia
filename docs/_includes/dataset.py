@component(attrs=[{"n": "loaded", "t": "bool"}, {"n": "count", "t": "int"}])
class Dataset(Object):
    """🛢️ Rows of things, named once on the page — a fence, a link, a learner's file, a sheet or a warehouse."""
    format   = Attr(str, "csv")             # csv, yaml or json — the fence's
    kept_in  = Attr(str, column="save")     # the learner's file the rows are read from, and 💾 kept in
    path     = Attr(str)                    # where the rows sit in a fetched answer — data, items
    refresh  = Attr(int)                    # seconds between two reads of a link or a warehouse
    sheet    = Attr(str)                    # a Google Sheet's tab the rows come from
    write    = Attr(bool)                   # the sheet takes writes
    apikey   = Attr(str)                    # the name of the key a database asks for
    unlisted = Attr(str)                    # the table's unlisted name — shared without signing in
    of       = Attr(str)                    # the class that adopts the rows (the older way: source= on the class)
    dbx      = Attr(str)                    # a Databricks warehouse id — the fence is SQL
    host     = Attr(str)                    # the warehouse's door, /dbx unless said
    source   = Attr("Database")             # the database a SQL fence runs on

    def __init__(self, id):
        self._el = None
        self._id = id

    @property
    def id(self):
        return self._id or ""

    def __bool__(self):
        return self.loaded

    def __eq__(self, other):
        if isinstance(other, Dataset):
            return self._id == other._id
        return NotImplemented

    @property
    def loaded(self):
        ds = getattr(js.window, "lcDatasets", None)
        return ds is not None and getattr(ds, self._id, None) is not None

    @property
    def count(self):
        ds = getattr(js.window, "lcDatasets", None)
        if not ds:
            return 0
        arr = getattr(ds, self._id, None)
        return int(arr.length) if arr else 0

    def row(self, **kw):
        """The first row whose fields match: the object itself when the dataset
        is a class (a class is a dataset), a dict when it is a list —
        self.page.Family.row(family="Nguyen").adopt(),
        self.page.reservations.row(family="Nguyen")["stage"]."""
        ds = getattr(js.window, "lcDatasets", None)
        arr = getattr(ds, self._id, None) if ds else None
        n = int(arr.length) if arr else 0
        for i in range(n):
            r = arr[i]
            if all(str(getattr(r, k, "") if getattr(r, k, None) is not None else "") == str(v)
                   for k, v in kw.items()):
                cls = _CLASSES.get(self._id)
                nm = getattr(r, "obj", None)
                if cls is not None and nm:
                    inst = globals().get(str(nm))
                    if inst is not None:
                        return inst
                return json.loads(str(js.window.JSON.stringify(r)))
        raise AssertionError("no row in " + self.id + " with " +
                             ", ".join(k + "=" + str(v) for k, v in kw.items()))

    def save(self):
        """Send what changed since the list was read — new, changed, gone —
        to the database it lives in; then read it again (💾 Save)."""
        fn = getattr(js.window, "lcDatasetSave", None)
        if fn is not None:
            fn(self._id)

    def reload(self):
        """Read the list again from where it lives (↻)."""
        fn = getattr(js.window, "lcRemoteReload", None)
        if fn is not None:
            fn(self._id)

    def put(self, row, key="id"):
        """The row whose `key` matches takes these fields; no such row, it is
        added (Michel, 2026-10-31: a button assigns the stakeholder's values
        and the builder's notes to each feature). Returns True when a row
        was updated, False when one was added."""
        fn = getattr(js.window, "lcDatasetPut", None)
        if fn is None:
            raise RuntimeError("this page cannot write rows")
        return bool(fn(self._id, json.dumps(row), key))

    def replace(self, rows):
        """Every row at once, in this order — the list becomes exactly these
        (Michel, 2026-11-04: page 4's features mirror the map, one per
        feature, nothing left over). The grid repaints; nothing is saved."""
        fn = getattr(js.window, "lcDatasetReplace", None)
        if fn is None:
            raise RuntimeError("this page cannot write rows")
        fn(self._id, json.dumps([dict(r) for r in rows]))

    def append(self, row):
        """One more row: on the page at once, and — when the list lives in a
        sheet that takes writes — in the sheet too, then read back
        (Michel, 2026-10-16: "an API where data is read but also written")."""
        fn = getattr(js.window, "lcDatasetAppend", None)
        if fn is None:
            raise RuntimeError("this page cannot add rows")
        fn(self._id, json.dumps(row))

    def values(self, field):
        """Every row's value for one field, in order, as strings.

        COUNTING IS NOT ENOUGH. A check could say "nine rows" but not
        "and none of them already went home" — so the first proof a
        learner writes about their own list had nothing to assert on
        (module 05, 2026-08-11). A missing field reads as "", so a
        blank cell and an absent column look the same to a reader,
        which is what a reader means by empty."""
        ds = getattr(js.window, "lcDatasets", None)
        arr = getattr(ds, self._id, None) if ds else None
        if not arr:
            return []
        out = []
        for i in range(int(arr.length)):
            v = getattr(arr[i], field, None)
            out.append("" if v is None else str(v))
        return out
