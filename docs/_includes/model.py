@component(attrs=[{"n": "classes", "t": "str"}])
class Model(Block):
    """🏛️ The page's classes, declared — structure, not ink: grids, forms and checks point at it."""
    editable = Attr(bool)                   # the declarations show as code the reader may change
    title    = Attr(str)                    # the code's title, when it shows
    source   = Attr("Database")             # the database its classes are kept in — a table each

    @property
    def classes(self):
        return " ".join(_LC_DECL.get(self.id) or [])
