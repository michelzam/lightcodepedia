@component(methods=["start", "stop"], states=["idle", "recording", "stopped"])
class Recorder(Block):
    """🎥 A screen and face recording, made in the browser — the page, the camera in a corner, the voice."""
    pip    = Attr(str, "bottom-right")      # the camera's corner — bottom-right, bottom-left, top-right, top-left
    size   = Attr(int, 240)                 # the camera bubble's size, in pixels
    zoom   = Attr(float, 1.35)              # how close the camera frames the face
    fps    = Attr(int, 25)                  # frames per second
    camera = Attr(str, "on")                # off records without the face
    mic    = Attr(str, "on")                # off records without the voice
    sound  = Attr(str, "off")               # on records the page's own sound too
    into   = Attr(str)                      # where the take is kept — a learner's file

    @transition(["idle"], "recording")
    def start(self):
        return self._tap(".lc-rec-start, [data-lc-start]")

    @transition(["recording"], "stopped")
    def stop(self):
        return self._tap(".lc-rec-stop, [data-lc-stop]")
