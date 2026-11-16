@component(icon="✍️",
           attrs=[{"n": "folded", "t": "bool", "data": True, "attr": "folded", "hint": "it opens folded: a ✎ to unfold it"},
                  {"n": "numbers", "t": "bool", "data": True, "attr": "numbers", "hint": "line numbers in the margin"},
                  {"n": "replay", "t": "float", "data": True, "attr": "replay", "d": 1.5, "hint": "seconds per step when its versions replay"},
                  {"n": "layout", "t": "str", "data": True, "attr": "layout", "d": "cols", "hint": "cols — text and preview side by side — or rows, one above the other"},
                  {"n": "rendered", "t": "str"},
                  {"n": "source", "t": "str"},
                  {"n": "titles", "t": "list"},
                  {"n": "sections", "t": "list"},
                  {"n": "bolds", "t": "list"},
                  {"n": "italics", "t": "list"},
                  {"n": "bullets", "t": "list"},
                  {"n": "numbered", "t": "list"},
                  {"n": "links", "t": "list"},
                  {"n": "images", "t": "int"},
                  {"n": "components", "t": "list"},
                  {"n": "versions", "t": "list"},
                  {"n": "replayed", "t": "int"}])
class Mdpad(Block):
    """✍️ A markdown pad — the text and its live page side by side — saved in the learner's own space."""
    _lc_keep = ("folded", "numbers", "replay")
    rows        = Attr(int)                 # the text's height, in lines
    kept_in     = Attr(str, column="save")  # the learner's file it is read from, and 💾 kept in
    comment     = Attr(bool)                # a line for a commit message beside 💾
    decorations = Attr(bool)                # the page's parts drawn in the preview — grids, proofs, agents
    piano       = Attr(bool)                # the markdown keys bar under the text
    tools       = Attr(str)                 # the 🧰 metrics tools on it, comma-separated
    mypy        = Attr(str)                 # its Python checked with mypy
    doctest     = Attr(str)                 # its Python's doctests run
    demo        = Attr(str)                 # a recorded demo it plays
    # The preview half IS the document being made — every property reads it,
    # so a rubric feature can grade what the learner typed without any js.
    def _preview_texts(self, css):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        if o is None:
            return []
        nl = o.querySelectorAll(css)
        return [str(nl.item(i).textContent or "").strip()
                for i in range(int(nl.length))]

    @property
    def versions(self):
        """The names of the versions the learner kept, newest first — what
        each 💾 said it did. The lesson's starter is not one of them."""
        h = getattr(self._el, "_lcHist", None) if self._el is not None else None
        if h is None:
            return []
        return [str(h[i]) for i in range(int(h.length))]

    @property
    def replayed(self):
        """How many times the film of this pad was played (🎞 / Watch it grow)."""
        return _lc_did(self, "replay")

    @property
    def rendered(self):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        return str(o.textContent or "").strip() if o is not None else ""

    @property
    def source(self):
        """What the learner actually typed — for criteria about HOW the
        markdown is written, not just what it renders to."""
        ta = self._el.querySelector(".lc-mdpad-in") if self._el is not None else None
        return str(ta.value) if ta is not None else ""

    @source.setter
    def source(self, text):
        """Write the pad as a person would: one render, now — the preview,
        its model and its wires follow (pad.broken says which hang)."""
        f = getattr(self._el, "_lcApply", None) if self._el is not None else None
        if f is not None:
            f(str(text))

    def painted(self, kind):
        """The source's painted tokens of one kind, in order — 'cls' for the
        decorations' classes ('.pitch'), 'id', 'key', 'val', 'fence', 'h',
        'link', 'ial' (whole decoration lines)."""
        k = self._el.querySelector(".lc-mdpad-piano") if self._el is not None else None
        if k is None:
            return []
        nl = k.querySelectorAll(".md-" + str(kind))
        return [str(nl.item(i).textContent or "") for i in range(int(nl.length))]

    @property
    def broken(self):
        """The wires to nothing in the preview, as the pad draws them:
        ['source «pets»'] — a renamed or deleted id shows here at once."""
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        if o is None:
            return []
        nl = o.querySelectorAll("[data-lc-broken]")
        out = []
        for i in range(int(nl.length)):
            for part in str(nl.item(i).getAttribute("data-lc-broken") or "").split(", "):
                if part:
                    out.append(part)
        return out

    @property
    def caret(self):
        """Where the caret is in the source, as a character offset."""
        ta = self._el.querySelector(".lc-mdpad-in") if self._el is not None else None
        return int(ta.selectionStart) if ta is not None else 0

    @caret.setter
    def caret(self, pos):
        """Move the caret the way a person would — the pad then shows the
        caret's block on both sides (pad.focus, pad.focused, pad.keys)."""
        f = getattr(self._el, "_lcCaret", None) if self._el is not None else None
        if f is not None:
            f(int(pos))

    @property
    def focus(self):
        """The block the caret is in, counted as the preview counts them;
        None on a blank line."""
        v = self._attr("data-lc-focus")
        return int(v) if v not in (None, "") else None

    @property
    def focused(self):
        """The preview element wearing the pulse, or None."""
        o = self._el.querySelector(".lc-mdpad-out .lc-mdpad-focus") if self._el is not None else None
        return _wrap(o) if o is not None else None

    @property
    def keys(self):
        """The piano: one class string per block ('k0' / 'k1', the caret's
        block with ' now'), in source order. Empty without piano= or numbers=."""
        nl = self._el.querySelectorAll(".lc-mdpad-piano > div") if self._el is not None else None
        out = []
        if nl is not None:
            for i in range(int(nl.length)):
                c = str(nl.item(i).className or "")
                if not c.startswith("ln"):
                    out.append(c)
        return out

    # ── ✎ fold: the editor tucks away, the preview takes the whole width ──
    @property
    def folded(self):
        """True while the editor is folded away and the preview alone shows."""
        return self._attr("data-lc-folded") == "1"

    def fold(self):
        f = getattr(self._el, "_lcFold", None) if self._el is not None else None
        if f is not None:
            f(True)

    def unfold(self):
        f = getattr(self._el, "_lcFold", None) if self._el is not None else None
        if f is not None:
            f(False)

    # ── 🎞 replay: the saved versions as frames, read-only ──
    def replay(self):
        """Press 🎞 — the frames load (a promise the page resolves), the
        pane turns into a diff pane and the slider appears."""
        r = getattr(self._el, "_lcReplay", None) if self._el is not None else None
        return r.start() if r is not None else None

    def stop(self):
        r = getattr(self._el, "_lcReplay", None) if self._el is not None else None
        if r is not None:
            r.stop()

    @property
    def replaying(self):
        return self._attr("data-lc-replay") == "1"

    @property
    def frames(self):
        v = self._attr("data-lc-frames")
        return int(v) if v else 0

    @property
    def frame(self):
        """The frame shown, counted from zero (the starter); None when not replaying."""
        v = self._attr("data-lc-frame")
        return int(v) if v not in (None, "") else None

    @frame.setter
    def frame(self, n):
        r = getattr(self._el, "_lcReplay", None) if self._el is not None else None
        if r is not None:
            r.go(int(n))

    @property
    def diff(self):
        """The diff pane, one (sign, line) per row: '+' came, '-' went, ' ' stayed."""
        nl = self._el.querySelectorAll(".lc-mdpad-diff .ln") if self._el is not None else None
        out = []
        if nl is not None:
            for i in range(int(nl.length)):
                sp = nl.item(i); c = str(sp.className or ""); t = str(sp.textContent or "")
                out.append(("+" if " add" in c else "-" if " del" in c else " ", t))
        return out

    @property
    def numbers(self):
        """The line numbers the gutter shows, in order."""
        nl = self._el.querySelectorAll(".lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln") if self._el is not None else None
        return [int(nl.item(i).getAttribute("data-n")) for i in range(int(nl.length))] if nl is not None else []

    @property
    def titles(self):
        """The # lines — a page opens with exactly one."""
        return self._preview_texts("h1")

    @property
    def sections(self):
        """The ## lines — the document's real structure."""
        return self._preview_texts("h2")

    @property
    def bolds(self):
        return self._preview_texts("strong, b")

    @property
    def italics(self):
        return self._preview_texts("em, i")

    @property
    def bullets(self):
        """Unordered list items — the • kind."""
        return self._preview_texts("ul li")

    @property
    def numbered(self):
        """Ordered list items — the 1. 2. 3. kind, where rank matters."""
        return self._preview_texts("ol li")

    @property
    def links(self):
        return self._preview_texts("a")

    @property
    def images(self):
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        return int(o.querySelectorAll("img").length) if o is not None else 0

    @property
    def components(self):
        """The live components in the preview (decorations="true"), by kind:
        ['cards', 'pitch'] — a fence the learner decorated came alive."""
        o = self._el.querySelector(".lc-mdpad-out") if self._el is not None else None
        if o is None:
            return []
        kinds = []
        # A plain link-button is the one part whose class carries no lc-
        # prefix ({: .button }); a learner's first decoration must count.
        for token, cls in _WRAP:
            name = cls.__name__.lower()
            if (token.startswith("lc-") or token == "button") and name not in kinds \
                    and o.querySelector("." + token) is not None:
                kinds.append(name)
        return sorted(kinds)
