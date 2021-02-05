class button(QtWidgets.QPushButton):
    hovered = QtCore.Signal()

    def __init__(self, parent=None):
        super(button, self).__init__(parent=parent)
        self.installEventFilter(self)
        self.hover = False

    def is_hover(self):
        return self.hover

    def eventFilter(self, qobject, qevent):
        qtype = qevent.type()
        if qtype == QtCore.QEvent.HoverEnter:
            self.hover = True
            self.hovered.emit()
        elif qtype == QtCore.QEvent.HoverLeave:
            self.hover = False
            self.hovered.emit()

        return super(button, self).eventFilter(qobject, qevent)


# USAGE
"""
def _connect_ui(self):
    self.btn.hovered.connect(self.set_icon_bg)

def set_icon_bg(self):
    if self.btn.is_hover():
        self.bg.setPixmap(self.pix_bg_hover)
    else:
        self.bg.setPixmap(self.pix_bg_default)

"""