from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMayaUI as omui


def maya_main_window():
    """ Return Maya main window as Python Object """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class TransformTable(QtWidgets.QDialog):
    
    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole + 1
    
    def __init__(self, parent=maya_main_window()):
        super(TransformTable, self).__init__(parent)

        self.setWindowTitle("Transform Table")
        self.setMinimumWidth(325)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        self.refresh_ui()

    def create_widgets(self):
        self.table_wdg = QtWidgets.QTableWidget()
        self.table_wdg.setColumnCount(3)

        self.table_wdg.setHorizontalHeaderLabels(["QPushButton", "QSpinBox", "QComboBox"])
        
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(2)
        btn_layout.addStretch()
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.close_btn)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        
        main_layout.addWidget(self.table_wdg)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.refresh_ui)
        self.close_btn.clicked.connect(self.close)
        

    def refresh_ui(self):
        self.table_wdg.setRowCount(0)
        self.table_wdg.insertRow(0)
        
        btn = QtWidgets.QPushButton("Button")
        btn.clicked.connect(self.on_button_pressed)
        self.table_wdg.setCellWidget(0,0,btn)
        
        spin = QtWidgets.QSpinBox()
        spin.valueChanged.connect(self.on_value_changed)
        self.table_wdg.setCellWidget(0,1,spin)
        
        combo = QtWidgets.QComboBox()
        combo.addItems(["item01", "item02", "item03"])
        combo.currentTextChanged.connect(self.on_combo_changed)
        self.table_wdg.setCellWidget(0, 2, combo)

        
    def on_button_pressed(self):
        print("Button was pressed")
        
    def on_value_changed(self, value):
        print("Spinbox was changed to : {0}".format(value))
        
    def on_combo_changed(self, text):
        print("Combobox value changed to : {0}".format(text))
   
    
        
if __name__ == "__main__":
    
    try:    
        transform_table.close()
        transform_table.deleteLater()
    except:
        pass
        
    transform_table = TransformTable()
    transform_table.show()