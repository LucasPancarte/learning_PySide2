from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg


import MaxPlus
import pymxs

class CollapsibleArrow(qtw.QFrame):

    h_poly = [qtc.QPoint(4.0, 8.0), qtc.QPoint(20.0, 8.0), qtc.QPoint(12.0, 16.0)]
    v_poly = [qtc.QPoint(8.0, 4.0), qtc.QPoint(16.0, 12.0), qtc.QPoint(8.0, 20.0)]

    def __init__(self, parent=None):
        super(CollapsibleArrow, self).__init__(parent)
        
        self.isCollapsed = False
        self.setFixedSize(22, 22)

        self.h_arrow = qtg.QPolygon(CollapsibleArrow.h_poly)
        self.v_arrow = qtg.QPolygon(CollapsibleArrow.v_poly)
        self.arrow_is_pointing = self.h_arrow
        
    def setArrow(self, arrowDir):
        self.arrow_is_pointing = self.h_arrow if arrowDir else self.v_arrow        
       
    def paintEvent(self, event):        
        painter = qtg.QPainter()
        painter.begin(self)
        painter.setBrush(qtg.QColor(192, 192, 192))
        painter.setPen(qtg.QColor(64, 64, 64))
        painter.drawPolygon(self.arrow_is_pointing)
        painter.end()

class CollapsableWidget(qtw.QWidget):

    fixed_height = 30

    def __init__(self, parent=None, label="", is_collapsed=True):
        super(CollapsableWidget, self).__init__(parent)

        self.is_collapsed = is_collapsed

        self.label = qtw.QLabel(label)
        self.label.setFixedHeight(CollapsableWidget.fixed_height)

        self.arrow = CollapsibleArrow()
        
        self.lab_layout = qtw.QHBoxLayout()
        self.lab_layout.addWidget(self.arrow)
        self.lab_layout.addWidget(self.label)

        self.f_layout = qtw.QVBoxLayout()
        self.title_frame = qtw.QFrame()
        self.title_frame.setLayout(self.f_layout)
        
        self.main_layout = qtw.QVBoxLayout(self)
        self.main_layout.addLayout(self.lab_layout)
        self.main_layout.addWidget(self.title_frame)

        self.title_frame.setVisible(not self.is_collapsed)
        self.arrow.setArrow(not self.is_collapsed)

    def set_collapsed(self):
        self.is_collapsed = not self.is_collapsed
        self.title_frame.setVisible(not self.is_collapsed)
        self.arrow.setArrow(not self.is_collapsed)

    def mousePressEvent(self, event):
        if event.pos().y()<=CollapsableWidget.fixed_height:
            self.set_collapsed()
        return super(CollapsableWidget, self).mousePressEvent(event)

    def add_widget(self, widget):
        self.f_layout.addWidget(widget)

    def add_layout(self, layout):
        self.f_layout.addLayout(layout)



# USAGE
if __name__=='__main__':
    class MyUI(qtw.QDialog):

        def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
            super(MyUI, self).__init__(parent)
            
            self.collapsible = CollapsableWidget(label="Testing Widget :")
            for i in range(5):
                self.collapsible.add_widget(CollapsableWidget(label="Test widget {}".format(i)))

            self.main_layout = qtw.QVBoxLayout(self)
            self.main_layout.addWidget(self.collapsible)
            self.main_layout.addStretch()


    collapsible_ui = MyUI()
    collapsible_ui.show()