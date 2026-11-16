@component(icon="🤖",
           attrs=[{"n": "system", "t": "long", "data": True, "d": "", "hint": "its brain — what it is told before every question"},
                  {"n": "replies", "t": "list"},
                  {"n": "last", "t": "str"},
                  {"n": "asked", "t": "int"}],
           events=["on_response"],
           methods=["ask", "clear"])
class Agent(Block):
    """🤖 A page agent — a part a proof, a guide or another agent can act on: read or rewrite its brain (system), ask it, read what it said."""
    _lc_keep = ("system",)
    bot         = Attr(str)                                     # a crew member by name — Bill, Tedd, Stan — its brain and face
    name        = Attr(str)                                     # its name in the panel
    rows        = Attr(int, 3)                                  # the question box's height, in lines
    model       = Attr(str, "openai/gpt-4o-mini", column="data-model")    # the model it asks
    temperature = Attr(float, 0.7, column="data-temperature")  # 0 says the same each time; higher, more varied
    max_tokens  = Attr(int, 500, column="data-max-tokens")     # the longest answer, in tokens
    intro       = Attr(str, column="data-intro")               # its first line, before anyone asks
    placeholder = Attr(str, "Ask anything...", column="data-placeholder")  # the empty question box's hint
    bound       = Attr("Mdpad")                                 # what it reads — a pad, or a dict of the page's values
    target      = Attr("Feature")                               # the check its answers aim at

    @bound.getter
    def bound(self):
        """The pad it reads (bound=) — the x-ray draws the pipe."""
        return _lc_ref(self, "data-lc-bound")

    @target.getter
    def target(self):
        """The check it aims at (target=)."""
        return _lc_ref(self, "data-lc-target")

    @property
    def asked_at(self):
        """When the learner last asked this agent, on this page (0: never) —
        compare it with a document's saved_at: changed after the answer?"""
        return _lc_did_at(self, "ask")

    @property
    def asked(self):
        """How many questions the learner asked this agent, on this page —
        or, for a crew's worker, how many asks it made in the last run."""
        row = getattr(self, "_row", None)
        if self._el is None and row is not None:
            return int(row.get("asks") or 0)
        return _lc_did(self, "ask")

    @property
    def tokens(self):
        """A crew's worker: the tokens its asks spent in the last run."""
        row = getattr(self, "_row", None)
        return int(row.get("tokens") or 0) if row is not None else 0

    @property
    def response(self):
        """The last answer, cut in its areas: .text (all of it), .direction,
        .question, .example (the lines it offers, a catalogue part expanded).
        What an on_response handler reads."""
        r = getattr(self._el, "_lcResponse", None) if self._el is not None else None
        return _AgentResponse(r)

    @property
    def todos(self):
        """The "# TODO" lines of the editor this agent is bound to, in source
        order — what the tutor scans when asked (todos="true")."""
        label = self._q(".lc-agent-bound")
        m = re.search(r"#([\w-]+)", str(label._el.textContent or "")) if label._el is not None else None
        if not m:
            return []
        ta = js.window.document.querySelector("#lc-pyrun-" + m.group(1) + " .lc-pyrun-code")
        if ta is None:   # a pad: the builder's checklist (- [ ] lines)
            ta = js.window.document.querySelector('.lc-mdpad[data-lc-id="' + m.group(1) + '"] .lc-mdpad-in')
        if ta is None:
            return []
        out = []
        for line in str(ta.value).split("\n"):
            mm = re.match(r"^\s*#\s*[Tt][Oo][Dd][Oo][:\s-]*(.*)$", line)   # MicroPython re: no flags, no \b
            if mm is None:
                mm = re.match(r"^\s*-\s\[ \]\s*(.*)$", line)
            if mm:
                out.append(mm.group(1).strip())
        return out

    @property
    def system(self):
        cfg = getattr(self._el, "_lcCfg", None) if self._el is not None else None
        v = getattr(cfg, "system", None) if cfg is not None else None
        return str(v) if v is not None else str(self._attr("data-system") or "")

    @system.setter
    def system(self, v):
        """Rewrite the instructions the NEXT ask runs under — the assignment
        move: disturb the agent, change its brain, prove the change."""
        if self._el is None:
            return
        cfg = getattr(self._el, "_lcCfg", None)
        if cfg is not None:
            cfg.system = str(v)
        self._el.setAttribute("data-system", str(v))

    @property
    def last(self):
        row = getattr(self, "_row", None)
        if self._el is None and row is not None:
            return str(row.get("last") or "")
        r = self.replies
        return r[-1] if r else ""

    def clear(self):
        """Forget this sitting's exchanges, so the next verdict is read alone."""
        for sel in (".lc-agent-log-entry", ".lc-agent-msg-bot", ".lc-agent-msg-user"):
            for o in self._qq(sel):
                o._el.remove()
        return self

    @property
    def replies(self):
        """Every answer the agent has given this sitting — the panel shows
        one exchange, the ledger keeps them all, so a rubric can read
        verdict lines out of the whole conversation."""
        out = [m.text for m in self._qq(".lc-agent-log-entry")]
        return out if out else [m.text for m in self._qq(".lc-agent-msg-bot")]

    def _bound_text(self, prompt):
        """What the panel would send: the bound document under review, read
        from the page as it stands, then the request. The expression is the
        panel's own ({= dict(dog=ask.dog, …) }), evaluated over every part
        that publishes its data — forms, documents, feature cards."""
        expr = self._attr("data-bound-expr") or ""
        if not expr:
            return str(prompt)
        ns = {}
        nodes = js.window.document.querySelectorAll("[data-lc-id][data-lc-value]")
        for i in range(int(nodes.length)):
            n = nodes.item(i)
            try:
                ns[str(n.getAttribute("data-lc-id"))] = _Attrs(json.loads(str(n.getAttribute("data-lc-value"))))
            except Exception:
                pass
        cards = js.window.document.querySelectorAll(".lc-feature[data-lc-id]")
        for i in range(int(cards.length)):
            c = cards.item(i)
            cid = str(c.getAttribute("data-lc-id"))
            if cid not in ns:
                ns[cid] = _Attrs({"status": str(c.getAttribute("data-status") or ""),
                                  "title": str(c.getAttribute("data-title") or ""),
                                  "text": str(c.getAttribute("data-gherkin") or "")})
        try:
            v = eval(expr, {"dict": dict, "str": str, "len": len, "int": int, "float": float, "list": list}, ns)
        except Exception as e:
            return str(prompt)
        return "The document under review:\n\n```\n" + str(v) + "\n```\n\nThe request:\n\n" + str(prompt)

    def ask(self, prompt, wait=True):
        """Send a message, as a person would — and, by default, WAIT for the
        answer, so the next line of the scenario can read `last`. The panel
        hands the runtime the exact request it would send; a synchronous
        call carries it and the reply is filed in the panel's own box and
        ledger. wait=False only presses Ask (the prompt box is named: the
        first input in the panel is the key field, not the question)."""
        if self._el is None:
            return self
        api = getattr(self._el, "_lcAgent", None) if wait else None
        req = api.request(self._bound_text(prompt)) if api is not None else None
        if req is not None:
            xhr = js.XMLHttpRequest.new()
            xhr.open("POST", str(req.url), False)
            xhr.setRequestHeader("Authorization", "Bearer " + str(req.token))
            xhr.setRequestHeader("Content-Type", "application/json")
            xhr.send(str(req.body))
            status = int(xhr.status)
            if status < 200 or status >= 300:
                raise AssertionError("the agent's engine answered " + str(status) + " — ask it by hand once, then run again")
            data = json.loads(str(xhr.responseText))
            try:
                text = data["choices"][0]["message"]["content"]
            except Exception:
                raise AssertionError("the agent's engine sent no answer text")
            api.record(str(prompt), str(text))
            return self
        box = self._el.querySelector(".lc-agent-prompt")
        if box is None:
            box = self._el.querySelector("textarea")
        if box is not None:
            box.value = str(prompt)
        self._tap(".lc-agent-send")
        return self
