class MySwitch(qtw.QPushButton):
    def __init__(self, parent = None):
        super(MySwitch, self).__init__(parent)
        print('init')
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = qtc.Qt.green if self.isChecked() else qtc.Qt.red

        radius = 10
        width = 32
        center = self.rect().center()

        painter = qtg.QPainter(self)
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(qtg.QColor(0,0,0))

        pen = qtg.QPen(qtc.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(qtc.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(qtg.QBrush(bg_color))
        sw_rect = qtc.QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)

        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, qtc.Qt.AlignCenter, label)