@component()
class Database(Block):
    """🗄️ A database, named on the page — its link's scheme says the kind; classes and datasets keep their rows there."""
    unlisted = Attr(str)                    # the unlisted name that opens its tables
    live     = Attr(bool)                   # hears its tables change, and the page follows

