@component(attrs=[{"n": "bar_count", "t": "int"},
                  {"n": "point_count", "t": "int"}],
           assoc=[{"n": "bars", "target": "Bar", "list": True}],
           methods=["beads", "chips", "tone"])
class Chart(Block):
    """📈 Rows drawn — bars, a line or a pie; a journey map with its bands and beats."""
    type      = Attr(str, "bar")                    # bar, line or pie
    x         = Attr(str)                           # the column along the bottom
    y         = Attr(str)                           # the column drawn — the bars' height, the line's points
    height    = Attr(int, 300)                      # pixels
    title     = Attr(str)                           # over the chart; [col] takes the picked row's value
    empty     = Attr(str)                           # what it says when there are no rows to draw
    measure   = Attr(str, column="bars")            # a second measure, drawn as bars behind the line
    series    = Attr(str)                           # one line per value of this column
    marks     = Attr(str)                           # rows whose value is set become diamonds — key points, their text on hover
    hover     = Attr(str)                           # extra text on every point's hover
    labels    = Attr(str)                           # the row's short text printed above its point
    top       = Attr(str)                           # a band of text above the plot, one cell per column
    bottom    = Attr(str)                           # a band under the x labels — chips, one per line
    color     = Attr(str)                           # the row's own colour for its point
    dips      = Attr(str)                           # the valley before the summit — setbacks met on the way
    trail     = Attr(str)                           # the row's beats in time order: ✗ ✓ ? — beads around the point
    hints     = Attr(str)                           # what a hover says about each part: "y: … | bars: …"
    filter    = Attr(str)                           # col=col — only the rows that match the picked row
    source    = Attr("Dataset")                     # the rows it draws
    bind      = Attr(str)                           # the older name of source
    master    = Attr("Datagrid")                    # the grid whose picked row it follows
    bound_to  = Attr(str, column="bound-to")        # the older name of master

    @source.getter
    def source(self):
        return Dataset(self._attr("data-bind") or "")

    @master.getter
    def master(self):
        gid = self._attr("data-bound-to") or ""
        el = js.window.document.querySelector("[data-lc-id='" + gid + "']")
        return Datagrid(el)

    # the title DRAWN, read in Python (Michel, 2026-11-10) — [col] filled in
    @title.getter
    def title(self):
        t = self._q(".lc-chart-title")
        return (t.text if t is not None else "").strip()

    @property
    def bars(self):
        return [Bar(r._el) for r in self._qq("rect")]

    @property
    def bar_count(self):
        """Rects when the chart drew SVG (a bound chart), otherwise the count
        the inline canvas recorded. A chart that is visibly drawing bars must
        never report zero — that turns a page's own proof into a liar."""
        rects = len(self._qq("rect"))
        if rects:
            return rects
        try:
            return int(self._attr("data-lc-bars") or 0)
        except Exception:
            return 0

    @property
    def point_count(self):
        return len(self._qq("circle"))

    @property
    def xs(self):
        """the x values drawn, in order — the pages of a journey"""
        out = []
        for c in self._qq("svg circle[pointer-events][data-x]"):
            x = c._attr("data-x")
            if x not in out:
                out.append(x)
        return out

    def beads(self, x):
        """the beats drawn before the point of x, in time order: ✗ ✓ ?"""
        return [c._attr("data-bead") for c in self._qq("svg circle[data-bead]") if c._attr("data-x") == x]

    def chips(self, x):
        """the chips under x, in order (a chip's own words, not its hover title)"""
        return [str(t._el.childNodes.item(0).textContent or "").strip() for t in self._qq("svg text[data-band='bottom']") if t._attr("data-x") == x]

    def tone(self, x):
        """the colour of x's point"""
        for c in self._qq("svg circle[data-tone][data-x]"):
            if c._attr("data-x") == x:
                return c._attr("data-tone")
        return ""
