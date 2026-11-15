@component(attrs=[{"n": "row_count", "t": "int"},          # computed, not settings
                  {"n": "headers", "t": "str", "list": True},
                  {"n": "rows", "t": "ref", "list": True}])
class Datagrid(Block):
    """▦ Rows in a table — from its own fence, or from a dataset it is bound to."""
    title        = Attr(str)                     # its title bar
    height       = Attr(int, 400)                # pixels; a bound grid scrolls when set
    format       = Attr(str, "yaml")             # yaml, csv or json — the fence's or the file's
    editable     = Attr(bool)                    # cells can be edited
    filter       = Attr(str)                     # which rows show
    save         = Attr(str)                     # the learner's file — 💾 keeps the rows there
    empty        = Attr(str)                     # what it says when no row arrives
    hints        = Attr(str)                     # a tip per column — col: tip | …
    sort         = Attr(str)                     # the column it opens sorted by
    columns      = Attr(str)                     # which columns show, in order, comma-separated
    dates        = Attr(str)                     # columns shown as dates, comma-separated
    autocomplete = Attr(bool)                    # typing in a cell offers the column's values
    bind         = Attr(str)                     # the older name of source
    page_size    = Attr(int, column="rows")      # rows per page (a link-line grid)
    locked       = Attr(str)                     # columns kept read-only on an editable grid
    compute      = Attr(str)                     # ƒ columns computed from others (a fence grid)
    reorder      = Attr(bool, True)              # the reader may drag columns (a link-line grid)
    detail_of    = Attr(str, column="detail-of")  # the older name of master
    source       = Attr("Dataset")               # the dataset it shows, or file:path
    master       = Attr("Datagrid")              # the grid whose picked row filters this one

    @source.getter
    def source(self):
        b = self._attr("data-bind") or ""
        # bind="Student" names a CLASS: the source is the model block that
        # declared it — the x-ray pipes grid → model (Michel, 2026-08-24)
        for mid in _LC_DECL:
            if b in _LC_DECL[mid]:
                el = js.window.document.querySelector(
                    ".lc-model[data-lc-id='" + mid + "']")
                if el is not None:
                    return Model(el)
        return Dataset(b)

    # THE SELECTED ROW, READ AND WRITTEN (Michel, 2026-10-09, Module 05:
    # "currentline.met = today's weekday, and select the next line — KISS").
    # `grid.row.met = weekday()` writes into the DATASET the grid shows
    # (through its query, to the base row), so the query re-runs, the grid
    # repaints and every count recounts; `grid.next()` selects the row after
    # the one just written — or the one that slid into its place when the
    # write took it out of the query's answer.
    @property
    def row(self):
        return _Row(self)

    @property
    def saved(self):
        """How many times the learner pressed 💾 Save on this grid (this device)."""
        return _lc_did(self, "save")

    def next(self):
        """⏭ Pick the row after — False on the last one."""
        # True when it moved, False on the last row — so a loop can stop by
        # itself: `while grid.next() and grid.row.met: pass` (Michel,
        # 2026-10-13, Module 05's first loop: skip the families already met)
        door = getattr(self._el, "_lcRow", None) if self._el is not None else None
        if door is None:
            raise AssertionError("#" + str(self.id) + " has no rows to walk yet")
        moved = door.next()
        return moved is not None and bool(moved)


    def _api(self):
        # AG-backed grids register their api under their id — the honest
        # source inside a synchronous step run, where the DOM's rows only
        # repaint after the run ends.
        md = getattr(js.window, "lcMasterDetail", None)
        if md is None:
            return None
        try:
            return getattr(md._apis, self.id, None)
        except Exception:
            return None

    def _waiting_for(self):
        # the query this grid is bound to, if it is still waiting for one of
        # its own sources — see query.md: it publishes nothing until then
        b = self._attr("data-bind") or ""
        if not b:
            return ""
        q = js.window.document.querySelector(".lc-query[data-lc-id='" + b + "']")
        return (q.getAttribute("data-waiting") or "") if q is not None else ""

    @property
    def row_count(self):
        # a grid whose query is still waiting has NO count yet: 0 would pass
        # a proof early, and a half-computed join failed one for the wrong
        # reason ("12 dog(s) still invisible", Michel 2026-09-16). Name the
        # wait, so the reader runs again once the page has finished loading.
        w = self._waiting_for()
        if w:
            raise AssertionError((self._attr("data-lc-id") or "this grid")
                                 + " is still waiting for " + w
                                 + " - the page has not finished loading; run again")
        # three renderers back a datagrid: the AG api (code-block grids —
        # its row model updates synchronously, the painted rows do not),
        # the custom HTML table (source-bound grids), and painted AG rows
        # as the last resort.
        api = self._api()
        if api is not None:
            try:
                return int(api.getDisplayedRowCount())
            except Exception:
                pass
        n = len(self._qq("tbody tr"))
        if n:
            return n
        ag = self._qq(".ag-center-cols-container .ag-row")
        return len(ag) if ag else len(self._qq(".ag-row"))

    @property
    def headers(self):
        ths = [th.text.rstrip(" ↑↓") for th in self._qq("th")]
        if ths:
            return ths
        return [h.text for h in self._qq(".ag-header-cell-text")]

    @property
    def rows(self):
        cols = self.headers
        out = []
        for tr in self._qq("tbody tr"):
            cells = tr._qq("td")
            out.append({cols[i]: cells[i].text if i < len(cells) else ""
                        for i in range(len(cols))})
        return out

    def header(self, name):
        """▥ The column header named name."""
        for th in self._qq("th"):
            if th.text.rstrip(" ↑↓") == name:
                return th
        return Block(None)

    def select(self, n=1):
        """👉 Select row n (1-based) — what a reader's click does: master-bound
        forms and detail grids receive the row, inside the same step."""
        api = self._api()
        if api is not None:
            node = api.getDisplayedRowAtIndex(n - 1)
            if node is not None:
                node.setSelected(True, True)
                # AG batches its selection event to a later tick — after a
                # synchronous step run has already ended. Publish the row
                # now; the batched event re-publishes the same row, harmless.
                md = getattr(js.window, "lcMasterDetail", None)
                if md is not None:
                    md.publish(self.id, node.data)
                return self
        rows = self._qq("tbody tr") or self._qq(".ag-row")
        if rows and 1 <= n <= len(rows):
            rows[n - 1]._el.click()
        return self
