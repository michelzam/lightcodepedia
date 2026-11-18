@component()
class Ship(Block):
    """🚀 Ship it — copies the app to the learner's bay, public, versioned; its square opens it on a phone."""
    app     = Attr(str)                         # the app's name — its square, its versions
    files   = Attr(str)                         # the app first, then the files it needs (its windows follow by themselves)
    bay     = Attr(str)                         # where the copies go: owner/repo/folder — the learner's bay unless said
    comment = Attr(bool)                        # 🚀 Ship… asks one line: the version's name
    tools   = Attr(str)                         # 🧰 the bay's own tools in a strip — "ships"
    replay  = Attr(int, 2500)                   # the 🎞 time machine's pace, in ms per version
