@component(methods=["load", "image"])
class EmbedPage(Block):
    """🖼️ A page, a picture or a learner's own file, shown inside this one."""
    height    = Attr(int, 400)              # pixels
    width     = Attr(str)                   # its width — pixels or a share of the page
    picture   = Attr(str, column="image")   # a picture beside it, or as it
    align     = Attr(str)                   # left, center or right
    shape     = Attr(str)                   # the picture's shape — round, rounded
    effect    = Attr(str)                   # how the picture appears
    poster    = Attr(str)                   # the picture shown before it plays
    field     = Attr(str)                   # the picked row's field it opens, when it follows a grid
    fresh     = Attr(bool)                  # read again on every visit, never from the cache
    kept_in   = Attr(str, column="save")    # a learner's file it shows, from their space
    master    = Attr("Datagrid")            # the grid whose picked row it follows
    def load(self, url):
        """Point the embedded iframe at a new URL (e.g. from a button on_click)."""
        if self._el is not None:
            self._el.src = url

    def image(self, url):
        """Show a single image, auto-fitted (object-fit: contain) inside the frame.
        A bare iframe pointed at an image shows the browser's raw image document,
        which the page can't style — so we wrap it in a tiny centred srcdoc."""
        if self._el is None:
            return
        doc = ("<!doctype html><meta charset=utf-8>"
               "<style>html,body{margin:0;height:100%;background:#fff}"
               "body{display:flex;align-items:center;justify-content:center}"
               "img{max-width:100%;max-height:100%;object-fit:contain;display:block}"
               "</style><img src='" + url + "'>")
        self._el.srcdoc = doc
