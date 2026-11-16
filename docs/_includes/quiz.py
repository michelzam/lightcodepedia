@component(attrs=[{"n": "graded", "t": "bool"}], methods=["pick", "check"], states=["pending", "graded"])
class Quiz(Block):
    """❓ A question, its options, and why each is right or wrong — the learner checks; a page never answers."""
    multi  = Attr(bool)                     # more than one option is right — boxes, not a single pick
    kind   = Attr(str)                      # essay, upload or matching — a Canvas quiz's other kinds of question
    points = Attr(float)                    # what it is worth in a Canvas quiz, 1 unless said

    @property
    def passed(self):
        """Did the learner get it right? READ ONLY, on purpose: a proof may
        ask a quiz how it went, and may never answer it (doctrine 5)."""
        return self._attr("data-passed") == "1"

    @property
    def graded(self):
        # a quiz is graded once any option has been revealed as ✓ or ✗
        return any(o._el.classList.contains("lc-quiz-correct") or
                   o._el.classList.contains("lc-quiz-wrong")
                   for o in self._qq("li"))

    def pick(self, n):
        opts = self._qq("li")
        if n < len(opts):
            opts[n]._el.click()
        return self

    @transition(["pending"], "graded")
    def check(self):
        return self._tap(".lc-quiz-check, [data-lc-check]")
