from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui


def maya_main_window():
    """ Return Maya main window as Python Object """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class TestModalDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(TestModalDialog, self).__init__(parent)

        self.setWindowTitle("Open/Import/Reference")
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.warning_btn = QtWidgets.QPushButton("Warning")
        self.folder_btn = QtWidgets.QPushButton("Folder Select")
        self.color_btn = QtWidgets.QPushButton("Color Select")
        self.custom_btn = QtWidgets.QPushButton("Model(Custom)")

    def create_layouts(self):
        pass

    def create_connections(self):
        pass
        
    def show_warning_dialog(self):
        QtWidgets.QMessageBox.warning(self, "Object not Found", "Camera 'shot cam' not found")
    
    def show_folder_select(self):
        pass
        
if __name__ == "__main__":
    
    try:    
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass
        
    open_import_dialog = TestModalDialog()
    open_import_dialog.show()from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMayaUI as omui


def maya_main_window():
    """ Return Maya main window as Python Object """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class CustomDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(CustomDialog, self).__init__(parent)

        self.setWindowTitle("Custom Dialog")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.ok_btn = QtWidgets.QPushButton("OK")
        
    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout(self)
        btn_layout.addWidget(self.lineedit)
        btn_layout.addWidget(self.ok_btn)
        
    def create_connections(self):
       self.ok_btn.clicked.connect(self.accept)
       
    def get_text(self):
        return(self.lineedit.text())
        
    


class TestModalDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(TestModalDialog, self).__init__(parent)

        self.setWindowTitle("Modal Dialog Test")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.initial_dir = mc.internalVar(upd=True)
        self.initial_color = QtGui.QColor(255,0,0)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.warning_btn = QtWidgets.QPushButton("Warning")
        self.folder_btn = QtWidgets.QPushButton("Folder Select")
        self.color_btn = QtWidgets.QPushButton("Color Select")
        self.custom_btn = QtWidgets.QPushButton("Model(Custom)")

    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout(self)
        btn_layout.addWidget(self.warning_btn)
        btn_layout.addWidget(self.folder_btn)
        btn_layout.addWidget(self.color_btn)
        btn_layout.addWidget(self.custom_btn)


    def create_connections(self):
        self.warning_btn.clicked.connect(self.show_warning_dialog)
        self.folder_btn.clicked.connect(self.show_folder_select)
        self.color_btn.clicked.connect(self.show_color_select)
        self.custom_btn.clicked.connect(self.show_custom_dialog)
        
        
    def show_warning_dialog(self):
        QtWidgets.QMessageBox.warning(self, "Object not Found", "Camera 'shot cam' not found")
    
    def show_folder_select(self):
        new_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", self.initial_dir)
        if new_dir:
            self.initial_dir = new_dir
        print("Selected Folder : {0}".format(self.initial_dir))
        
    def show_color_select(self):
        self.initial_color = QtWidgets.QColorDialog.getColor(self.initial_color, self)
        print("""Selected Color is :
            Red : {0}
            Green : {1}
            Blue : {2}""".format( self.initial_color.red(),
                                    self.initial_color.green(),
                                    self.initial_color.blue()
                                    ))
        
    def show_custom_dialog(self):
        custom_dialog = CustomDialog()
        result = custom_dialog.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            print("Names : {0}".format(custom_dialog.get_text()))
        
        
if __name__ == "__main__":
    
    try:    
        modal_dialog.close()
        modal_dialog.deleteLater()
    except:
        pass
        
    modal_dialog = TestModalDialog()
    modal_dialog.show()