from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    """ Return Maya main window as Python Object """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class BasicDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(BasicDialog, self).__init__(parent)

        self.setWindowTitle("Open/Import/Reference")
        # self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.spin = QtWidgets.QSpinBox()
        self.spin.setFixedWidth(80)
        self.spin.setMinimum(-100)
        self.spin.setMaximum(100)
        self.spin.setSingleStep(5)
        self.spin.setPrefix("$ ")
        self.spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        
        self.doublespin = QtWidgets.QDoubleSpinBox()
        self.doublespin.setFixedWidth(80)
        self.doublespin.setRange(-50.5, 50.5)
        self.doublespin.setSuffix(" m")
        
    def create_layouts(self):
        main_layout = QtWidgets.QFormLayout(self)
        main_layout.addRow("Spin_Box : ", self.spin)
        main_layout.addRow("DoubleSpin_Box : ", self.doublespin)

    def create_connections(self):
        self.spin.valueChanged.connect(self.print_value)
        self.doublespin.valueChanged.connect(self.print_value)
        
    def print_value(self, value):
        print("Value is : {0}".format(value))
        
if __name__ == "__main__":
    
    try:    
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass
        
    open_import_dialog = BasicDialog()
    open_import_dialog.show()
    