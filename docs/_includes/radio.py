@component(icon="📻", attrs=[{"n": "selected", "t": "str"}, {"n": "active", "t": "int"}], methods=["select"])
class Radio(Block):
    """📻 Sections as choices — one picked at a time, its content shown."""

    @property
    def selected(self):
        c = self._el.querySelector("input:checked") if self._el else None
        if not c:
            return ""
        lbl = c.parentElement
        return (lbl.textContent or "").strip() if lbl else ""

    @property
    def active(self):
        if self._el is None:
            return 0
        ins = self._el.querySelectorAll("input")
        for i in range(int(ins.length)):
            if ins.item(i).checked:
                return i
        return 0

    def select(self, n):
        if self._el is not None:
            ins = self._el.querySelectorAll("input")
            if ins is not None and int(ins.length) > n:
                ins.item(n).click()
        return self
