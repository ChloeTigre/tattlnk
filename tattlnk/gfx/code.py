"""Generate various xD barcodes

STUB
"""

class DotMatrix(object):
    def __init__(width, height, content=None):
        self.width = width
        self.height = height
        self.content = content

    def render_html(self):
        pass

    def render_svg(self):
        pass

    def render_console(self):
        pass


class Code(DotMatrix):
    def render_matrix(self):

class BarCode(Code):
    pass

class QRCode(Code):
    pass

