@component(attrs=[{"n": "size", "t": "int", "data": True, "attr": "size", "d": 180, "hint": "its face's size, in pixels"},
                  {"n": "playing", "t": "bool"},
                  {"n": "speech", "t": "str"}],
           assoc=[{"n": "points", "target": "Block", "list": True}],
           methods=["play", "stop", "video"],
           states=["idle", "speaking"])
class Avatar(Block):
    """🗣️ A guide with a face — Doc — who walks the page and says its lines, in a studio voice or the device's."""
    _lc_keep = ("size",)
    dock     = Attr(bool)                   # it waits docked in the corner, a tap away
    autoplay = Attr(bool)                   # it starts walking as the page opens
    step     = Attr(bool)                   # one line per tap, not the whole tour
    story    = Attr(str)                    # the story it tells, of those its fence keeps
    pick     = Attr(str)                    # the face it wears
    src      = Attr(str)                    # a file its script comes from
    def _reg(self):
        regs = getattr(js.window, "_lcAvatars", None)
        aid = self.id
        return getattr(regs, aid, None) if regs is not None and aid else None

    @property
    def playing(self):
        av = self._reg()
        return bool(av.playing) if av is not None else False

    @property
    def points(self):
        """Every part its scripts walk to (at:) — the app it shows, the
        check it runs: the x-ray draws one pipe each."""
        av = self._reg()
        if av is None:
            return []
        scripts = [getattr(av, "script", None), getattr(av, "_tourScript", None)]
        st = getattr(av, "stories", None)
        if st:
            for k in js.window.Object.keys(st):
                scripts.append(getattr(st, k, None))
        out, seen = [], set()
        for sc in scripts:
            if not sc:
                continue
            for i in range(int(sc.length or 0)):
                at = str(getattr(sc[i], "at", "") or "")
                el = js.window.lcAvatarResolve(at) if at else None
                w = _wrap(el) if el else None
                if w is None or type(w) is Block or not w.id or w.id in seen:
                    continue
                seen.add(w.id)
                out.append(w)
        return out

    @property
    def speech(self):
        b = self._el.querySelector(".lc-avatar-speech") if self._el is not None else None
        return str(b.textContent or "").strip() if b is not None else ""

    @property
    def size(self):
        c = self._el.querySelector(".lc-avatar-char") if self._el is not None else None
        if c is None:
            return 0
        try:
            return int(str(c.style.width).replace("px", "") or 0)
        except Exception:
            return 0

    @transition(["idle"], "speaking")
    def play(self):
        if not self.playing:
            self._tap(".lc-avatar-char")
        return self

    @transition(["speaking"], "idle")
    def stop(self):
        if self.playing:
            self._tap(".lc-avatar-char")
        return self

    def video(self, url):
        """Set a runtime video source (direct .mp4/.webm URL or a YouTube link)
        for this avatar — e.g. from a button on_click, so the URL never lives in
        the repo. A script line with `video: true` then plays this source with
        its cues; YouTube links play through the embed, file URLs keep alpha."""
        fn = getattr(js.window, "lcAvatarSetVideo", None)
        if fn is not None and self.id:
            fn(self.id, str(url or ""))
        return self
