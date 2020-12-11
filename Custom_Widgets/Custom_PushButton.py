from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg


class Buttons(qtw.QPushButton):
    """
    Custom button widget added right-click event, 
    initialize with : label, icon_path, size, right-click/left-click/middle-click event functions
    """
    def __init__(self, size, label=None, icon=None, rc_event=None, lc_event=None, mc_event=None):
        """
        Initialization

        """
        super(Buttons, self).__init__()

        self.label = label
        self.icon = icon
        self.size = size
        self.rc_event = rc_event
        self.lc_event = lc_event
        self.mc_event = mc_event

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

            if event.button() == qtc.Qt.RightButton:
                self.right_click_event(self.rc_event)

            elif event.button() == qtc.Qt.LeftButton:
                self.left_click_event(self.lc_event)

            elif event.button() == qtc.Qt.MidButton:
                self.middle_click_event(self.lc_event)

    def left_click_event(self, lc_function=None):
        """
        Left-click event
        :param lc_function: function, define a function to execute on left-click
        """
        if callable(lc_function):
            lc_function()

    def right_click_event(self, rc_function=None):
        """
        Right-click event
        :param rc_function: function, define a function to execute on right-click
        """
        if callable(rc_function):
            rc_function()

    def middle_click_event(self, mc_function=None):
        """
        Middle-click event
        :param mc_function: function, define a function to execute on middle-click
        """
        if callable(mc_function):
            mc_function()


# USAGE
"""
class MyUI(qtw.QDialog):

    def __init__(self, parent=None):
        supper(MyUI, self).__init__(parent)
        
        self.btn = Buttons(qtc.QSize(50, 50), icon=qtg.QIcon("/my_icon_path.png"), label="My Tooltip" )
        self.main_layout = qtw.QVBoxLayout(self)
        self.main_layout.addWidget(self.btn)

        self.btn.rc_event = self.test_right_click
        self.btn.lc_event = self.test_left_click
        self.btn.mc_event = self.test_middle_click

    def test_right_click(self):
        print("Right-click Worked")

    def test_left_click(self):
        print("Left-click Worked")

    def test_middle_click(self):
        print("Middle-click Worked")

"""