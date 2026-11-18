@component()
class Video(Block):
    """🎬 A video in the page — a clip of the course, or YouTube and Drive in their own player."""
    height      = Attr(int, 400)            # pixels
    poster      = Attr(str)                 # the picture shown before it plays
    autoplay    = Attr(bool)                # plays on arrival — muted, as every browser wants
    loop        = Attr(bool)                # starts again at the end
    muted       = Attr(bool)                # no sound until the reader asks
    playsinline = Attr(bool)                # plays in the page on a phone, not full screen
