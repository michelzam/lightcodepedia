@component(attrs=[{"n": "title", "t": "str"}], methods=["run"])
class Feature(Block):
    """🦄 A proof in Gherkin — Given, When, Then — its steps carrying their Python, run on the page."""
    status      = Attr(str, "pending")      # pending, passing, failing or wanted — what it shows before it runs
    tags        = Attr(str)                 # its tags, comma-separated — the suite groups and counts by them
    visible     = Attr(bool)                # its steps show open
    celebration = Attr(bool)                # confetti when it turns green
    pace        = Attr(str)                 # how fast its steps paint, one after the other
    saves       = Attr(str)                 # the files it checks were saved first, comma-separated
    tools       = Attr(str)                 # the plug-ins the card wears, by name — "impact": what each step touched, as a tree
    src         = Attr(str)                 # a .feature file its Gherkin comes from
    flow        = Attr("EventFlow")         # the event flow it checks — Given the setup, When the command, Then the event
    grades      = Attr("Mdpad")             # the work it grades — a pad, or a grid

    @flow.getter
    def flow(self):
        """The event flow this feature checks (flow= knob) — Given is the
        setup, When the command, Then the event; the pipe says which story."""
        fid = self._attr("data-flow") or ""
        el = js.window.document.querySelector("[data-lc-id='" + fid + "']")
        return EventFlow(el) if el is not None else None

    @classmethod
    def nth(cls, n=0):
        nl = js.window.document.querySelectorAll(".lc-feature")
        return cls(nl.item(n) if n < int(nl.length) else None)

    @property
    def title(self):
        return str(self._attr("data-title") or "")

    @status.getter
    def status(self):
        v = self._attr("data-status")
        return str(v) if v else "none"

    @property
    def wanted(self):
        """A request from the problem space: steps written, none implemented."""
        return self.status == "wanted"

    @tags.getter
    def tags(self):
        return [str(o._el.getAttribute("data-tag") or "") for o in self._qq(".lc-feature-tag")]

    @property
    def text(self):
        """The feature as written — Gherkin only, no step bodies."""
        return str(self._attr("data-gherkin") or "")

    def run(self):
        """▶ Run the proof — what the card's ▶ Run button does."""
        return self._tap(".lc-feature-run-btn")
