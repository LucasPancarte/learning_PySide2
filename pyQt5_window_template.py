from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui


# don't use reload() if you want to keep ui position
class TemplateUi(QtWidgets.QDialog):
    WINDOW_TITLE = "Template"
    dlg_instance = None

    # override in child class (change 'cls.dlg_instance = TemplateUi()' to 'cls.dlg_instance = ChildClassName()')
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = TemplateUi()
            
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
        super(TemplateUi, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        pass

    def create_layouts(self):
        pass

    def create_connections(self):
        pass
    
    def showEvent(self, e):
        super(TemplateUi, self).showEvent(e)
        if self.geometry:
            self.restoreGeometry(self.geometry)
   
    def closeEvent(self, e):
        if isinstance(self, TemplateUi):
            super(TemplateUi, self).closeEvent(e)
            self.geometry = self.saveGeometry()

    
if __name__ == "__main__":
    
    try:    
        template_ui.close()
        template_ui.deleteLater()
    except:
        pass
        
    template_ui = TemplateUi()
    template_ui.show_dialog()