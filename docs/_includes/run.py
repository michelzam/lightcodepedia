@component(icon="🐍", attrs=[{"n": "output", "t": "str"},
                  {"n": "played", "t": "int"},
                  {"n": "last_note", "t": "str"},
                  {"n": "doctests", "t": "str"}],
           methods=["run", "test"])
class Run(Block):
    rows       = Attr(int, 6)               # the code's height, in lines
    folded     = Attr(bool)                 # it opens folded
    silent     = Attr(bool)                 # it runs without showing its output
    readonly   = Attr(bool)                 # the code can be run, not changed
    init       = Attr(str)                  # code that runs first, unseen — the setup
    expected   = Attr(str)                  # the output it should print — compared after each run
    bound      = Attr(str)                  # what its code reads from the page
    mypy       = Attr(str)                  # its code checked with mypy
    pep8       = Attr(bool)                 # its code checked for PEP 8 style
    subtitles  = Attr(str)                  # lines shown while it plays
    outside_in = Attr(bool)                 # the test first, then the code
    """A Python runner, by its id: self.page.coin.played, .last_note, .output,
    .doctests.green — what the block itself records; no selector in a step."""
    def run(self):
        return self._tap(".lc-pyrun-run, .lc-run-btn, [data-lc-run]")

    def test(self):
        """Press 🧪 Test, as a person would; the tally lands on the block."""
        return self._tap(".lc-pyrun-test")

    @property
    def output(self):
        o = self._q(".lc-pyrun-out")
        return str(o._el.textContent) if o and o._el is not None else ""

    @property
    def played(self):
        """Notes play() queued since the page opened (song.md)."""
        return int(self._attr("data-lc-played") or 0)

    @property
    def last_note(self):
        return str(self._attr("data-lc-last-note") or "")

    @property
    def doctests(self):
        return _Doctests(self._attr("data-lc-doctest"))
