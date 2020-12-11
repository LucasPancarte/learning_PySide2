from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMayaUI as omui


def maya_main_window():
    """ Return Maya main window as Python Object """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class TreeViewDialog(QtWidgets.QDialog):
    WINDOW_TITLE = "Tree View "
    dlg_instance = None
    # don't use reload() if you want to keep ui position
    
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = TreeViewDialog()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()
    
    @classmethod
    def maya_main_window(cls):
        """ Return Maya main window as Python Object """
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(TreeViewDialog, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        if mc.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif mc.about(mcOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)
        
        self.setMinimumSize(500,400)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        root_path = "{0}".format(mc.internalVar(userAppDir=True))
        
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(root_path)
        
        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(root_path))
        self.tree_view.hideColumn(1)
        self.tree_view.setColumnWidth(0, 290)
        
        # self.model.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
        self.model.setNameFilters(["*.py"])
        self.model.setNameFilterDisables(False)
        
    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addWidget(self.tree_view)
    
    def create_connections(self):
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
    
    def on_double_clicked(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            print("Directory Selected {0}".format(path))
        else:
            print("File Selected {0}".format(path))
            
    
if __name__ == "__main__":
    
    try:    
        tree_view.close()
        tree_view.deleteLater()
    except:
        pass
        
    tree_view = TreeViewDialog()
    tree_view.show()