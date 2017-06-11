import gi
from gi.repository import GObject


class TextExtension(GObject.GInterface):
    __gtype_name__ = "TextExtension"
    def __init__(self):
        GObject.GInterface.__init__(self)

    def do_process(self, text):
        pass
