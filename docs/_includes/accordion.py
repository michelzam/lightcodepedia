@component(methods=["open", "close", "sections"])
class Accordion(Block):
    """🪗 Sections that fold — a heading and its content, opened one at a time by a tap."""
    opened = Attr(bool, column="open")      # starts open, not folded (a section heading's own word)
    quiet = Attr(bool)                      # a few grey words, no frame; shut, its text takes no room but stays in the page for readers that are not eyes

    def sections(self):
        return [s.text for s in self._qq("summary, .lc-acc-head")]

    def open(self, n=0):
        if self._el is not None:
            ds = self._el.querySelectorAll("details")
            if ds is not None and int(ds.length) > n:
                ds.item(n).open = True
        return self

    def close(self, n=0):
        if self._el is not None:
            ds = self._el.querySelectorAll("details")
            if ds is not None and int(ds.length) > n:
                ds.item(n).open = False
        return self
