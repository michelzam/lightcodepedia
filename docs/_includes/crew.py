@component(assoc=[{"n": "members", "target": "Agent", "list": True}], methods=["run"])
class Crew(Agent):
    """🧑‍🤝‍🧑 An agent made of agents — its members the rows of a dataset, run over an inbox with clear bounds."""
    actions  = Attr(str)                    # the steps each message goes through, in order
    stages   = Attr(str)                    # the older name of actions
    tries    = Attr(int, 2)                 # attempts per message
    budget   = Attr(int, 6)                 # AI asks in all, for the whole run
    fallback = Attr(str)                    # what a message still open at the end becomes
    text     = Attr(str, "message")         # the inbox's column holding the message
    pace     = Attr(float, 0.5)             # seconds between steps — the work seen, a row at a time
    costs    = Attr(str, "1, 30, 900")      # what each kind of step costs: code, AI, a person
    inbox    = Attr("Dataset")              # the messages it works through
    provider    = Attr(str)                 # its members' engine, unless a member's row says another
    model       = Attr(str)                 # its members' model, by default
    temperature = Attr(float)               # its members' temperature, by default
    max_tokens  = Attr(int, column="max_tokens")  # its members' longest answer, by default
    reasoning_effort = Attr(str, column="reasoning_effort")  # how hard its members think, where the model allows

    @property
    def asked(self):
        """The AI asks this crew made, in its last run."""
        return self.asks

    @property
    def replies(self):
        """What its members said, step by step, in its last run."""
        return [str(v) for v in self.log.values("out")]

    @property
    def last(self):
        r = self.replies
        return r[-1] if r else ""

    def ask(self, prompt, wait=True):
        raise AssertionError("a crew works its inbox, not one question — put the message in the inbox, then run()")

    @property
    def members(self):
        """Its members: a list of agents (Michel, 2026-10-24: "Crew's members
        is a list of agents") — the composite: a crew is an agent made of
        agents, so a member may one day be a crew itself (the tree). Each is
        the live instance of its row: .asked, .tokens, .last after a run."""
        ds = getattr(js.window, "lcDatasets", None)
        arr = getattr(ds, str(self.id) + ".agents", None) if ds else None
        if not arr:
            arr = getattr(ds, self._attr("members") or "members", None) if ds else None
        rows = json.loads(str(js.JSON.stringify(arr))) if arr else []
        return [_lc_agent_of(r) for r in rows if isinstance(r, dict)]


    @property
    def sorted(self):
        return Dataset(str(self.id) + ".sorted")

    @property
    def log(self):
        return Dataset(str(self.id) + ".log")

    @property
    def asks(self):
        return int(self._attr("data-asks") or 0)

    @property
    def tokens(self):
        return int(self._attr("data-tokens") or 0)

    @property
    def done(self):
        return self._attr("data-state") == "done"

    # THE COST, THREE WORKERS (Michel, 2026-10-24: "python code: the cheapest,
    # the easier to verify, rigid too; ai: more flexible, but more expensive;
    # human: the most flexible, creative, and expensive"): costs= gives each
    # one's price — a rule run, an AI ask, a message left for a person
    # the crew counts them, once (crew.md), and publishes them as a form does
    @property
    def runs(self):
        """🐍 The rule runs of the last run: the cheapest worker."""
        return int(self._attr("data-runs") or 0)

    @property
    def open(self):
        """🧑 The messages the last run left for a person (its fallback stage)."""
        return int(self._attr("data-open") or 0)

    @property
    def cost(self):
        """💰 runs × 1 + asks × 30 + open × 900 — or the prices costs= gives."""
        return int(self._attr("data-cost") or 0)

    def run(self):
        """Press ▶ Run, as a person would; the crew works on, the page repaints."""
        self._tap(".lc-crew-run")
        return self
