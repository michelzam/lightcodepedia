@component(attrs=[{"n": "loaded", "t": "bool"}, {"n": "last_log", "t": "str"}],
           methods=["bark", "run", "wag_tail", "swim", "blow_bubble"])
class Scene3d(Block):
    """🧊 A 3D scene a learner drives with calls — a dog that barks, runs, swims, and the code each move writes."""
    height  = Attr(int, 440)                # pixels
    goal    = Attr(str)                     # a quest the scene checks — adopt_wanda
    trail   = Attr(bool)                    # leaves a trail where it walks
    console = Attr(bool)                    # the log of the code each move wrote — on unless a quest hides it

    @property
    def loaded(self):
        return bool(self._el is not None
                    and self._el.querySelector("canvas") is not None)

    @property
    def last_log(self):
        if self._el is None:
            return ""
        nl = self._el.querySelectorAll(".lc-s3d-console div")
        n = int(nl.length)
        return str(nl.item(n - 1).textContent or "").strip() if n else ""

    def _method_btn(self, name):
        if self._el is not None:
            nl = self._el.querySelectorAll(".lc-s3d-methods button")
            for i in range(int(nl.length)):
                b = nl.item(i)
                if str(b.textContent or "").strip() == name + "()":
                    return Block(b)
        return Block(None)

    def bark(self):
        return self._method_btn("bark").click()

    def run(self):
        return self._method_btn("run").click()

    def wag_tail(self):
        return self._method_btn("wag_tail").click()

    def swim(self):
        return self._method_btn("swim").click()

    def blow_bubble(self):
        return self._method_btn("blow_bubble").click()
