from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg


class Buttons(qtw.QPushButton):
    """
    Custom button widget added right-click event, 
    initialize with : label, icon_path, size
    """
    rightClicked = Signal()
    middleClicked = Signal()

    def __init__(self, size, label=None, icon=None) #, rc_event=None, lc_event=None, mc_event=None):
        """
        Initialization

        """
        super(Buttons, self).__init__()

        self.label = label
        self.icon = icon
        self.size = size

        if self.icon!=None:
            self.setIcon(self.icon)
            self.setIconSize(self.size)
            self.setToolTip(self.label)
        else:
            self.setText(self.label)
            self.setMinimumSize(self.size)

    def mousePressEvent(self, event):
        """
        Re-define mousePressEvent to implement right-click/left-click/middle-click
        """ 
        if event.type() == qtc.QEvent.MouseButtonPress:
            if event.button() == qtc.Qt.LeftButton:
                super(Buttons, self).mousePressEvent(event)
            
            elif event.button() == qtc.Qt.RightButton:
                self.rightClicked.emit()

            elif event.button() == qtc.Qt.MidButton:
                self.middleClicked.emit()