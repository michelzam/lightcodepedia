@component()
class Pytutor(Block):
    """🔬 Python, stepped line by line in Python Tutor — the frames and the objects, drawn."""
    height    = Attr(int, 400)              # pixels
    master    = Attr("Run")                 # the code box whose code it steps
    bound_to  = Attr(str, column="bound-to")  # the older name of master

    @master.getter
    def master(self):
        """The code box it steps (master= or bound-to=)."""
        return _lc_ref(self, "data-bound-to")
