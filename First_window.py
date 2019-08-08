# from PyQt5 import uic 
# from PyQt5.QWidgets import QApplication, QLabel

# app = QApplication([])
# label = QLabel('Hello World')
# label.show()
# app.exec_()

# # To install pyside2 :
# 	# pip install --index-url=http://download.qt.io/snapshots/ci/pyside/5.13/latest/ pyside2 --trusted-host download.qt.io

from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

def maya_main_window():
    """
        Return Maya main window as Python Object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class MyLineEdit(QtWidgets.QLineEdit):
    
    enter_pressed = QtCore.Signal(str)
    
    def keyPressEvent(self, e):
        super(MyLineEdit, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Enter:
            self.enter_pressed.emit("Enter Key Pressed")
        elif e.key() == QtCore.Qt.Key_Return:
            self.enter_pressed.emit("Return Key Pressed")
            

class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("PySide2 Test Win")
        self.setMinimumWidth(200)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """
            Create every widget for the UI
        """
        self.cust_lineedit = MyLineEdit()

        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["Item 01", "Item 02", "Item 03", "Item 04"])
        
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox()
        self.checkbox2 = QtWidgets.QCheckBox()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

    def create_layouts(self):
        """
            Create Layouts and add existing widgets to these layouts
        """
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("custom :", self.cust_lineedit)
        form_layout.addRow("Combo :", self.combobox)
        form_layout.addRow("Name :", self.lineedit)
        form_layout.addRow("Hidden :", self.checkbox1)
        form_layout.addRow("Locked :", self.checkbox2)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
    def create_connections(self):
        """
            Connect existing widgets to functions
        """
        self.cust_lineedit.enter_pressed.connect(self.on_enter_pressed)
        # self.cust_lineedit.keyPressEvent(QtCore.Qt.Key_Enter)
    
        self.combobox.activated.connect(self.on_activated_int)
        self.combobox.activated[str].connect(self.on_activated_str)
        
        self.cancel_button.clicked.connect(self.close)
        self.lineedit.textChanged.connect(self.print_lineedit)
        self.checkbox1.toggled.connect(self.print_isHidden)
    
    
    @QtCore.Slot(int)
    def on_activated_int(self, index): print("Combo index is {0}".format(index))
        
    @QtCore.Slot(str)
    def on_activated_str(self, text): print("Combo text is {0}".format(text))
    
    def on_enter_pressed(self, text): print(text)
    
    def print_lineedit(self, name):
        #name = self.lineedit.text()
        print("The text is ===>> {0}".format(name))
        
    def print_isHidden(self, checked):
        #hidden = self.checkbox1.isChecked()
        if checked:
            print("it's HIDDEN ")
        else:
            print("it's VISIBLE")
            
    
if __name__ == "__main__":
    
    try:    
        pySide2_window.close()
        pySide2_window .deleteLater()
    except:
        pass
        
    pySide2_window = TestDialog()
    pySide2_window.show()
        