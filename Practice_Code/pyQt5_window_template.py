# -*- coding: utf-8 -*-

import re
import sys
import random

from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc

class StandaloneApp(qtw.QDialog):

    WINDOW_TITLE = 'Standalone App'
    dlg_instance = None
    style_sheet = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = StandaloneApp()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=None, style_sheet=None):
        super(StandaloneApp, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ qtc.Qt.WindowContextHelpButtonHint|qtc.Qt.WindowMinMaxButtonsHint)

        if style_sheet:
            self.style_sheet = style_sheet
            self.setStyleSheet(self.style_sheet)

        self.setMinimumSize(500, 200)

        self.geometry=None

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
    
    # UI CREATION
    def create_actions(self):
        """
        Create all actions used by Standalone app
        """
        pass

    def create_widgets(self):
        """
        Create all widgets used by Standalone app
        """
        pass

    def create_layouts(self):
        """
        Creates all layouts used by Standalone app and adds all widgets to them
        """
        main_layout = qtw.QVBoxLayout(self)

    def create_connections(self):
        """
        Creates all connections between widgets and functions for Standalone app
        """
        pass

    # OPEN/CLOSE EVENTS
    def showEvent(self, e):
        """
        Event used on UI startup, 
        restore size and position if the ui already existed
        """
        super(StandaloneApp, self).showEvent(e)
        if self.geometry:
            self.restoreGeometry(self.geometry)
   
    def closeEvent(self, e):
        """
        Event used on UI close
        saves size and position for the next ui showEvent
        """
        if isinstance(self, StandaloneApp):
            super(StandaloneApp, self).closeEvent(e)
            self.geometry = self.saveGeometry()



if __name__ == '__main__':
    #FOR STANDALONE APP
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    ranApp = StandaloneApp()
    ranApp.show()

    # Run the main Qt loop
    sys.exit(app.exec_())

    #FOR DCC APP
    # try:    
    #     template_ui.close()
    #     template_ui.deleteLater()
    # except:
    #     pass
        
    # template_ui = StandaloneApp()
    # template_ui.show_dialog()


### DCC SPECIFICS
# MAYA
# from shiboken2 import wrapInstance

# import maya.cmds as mc
# import maya.api.OpenMaya as om
# import maya.OpenMayaUI as omui
# @classmethod
# def maya_main_window(cls):
#     """ Return Maya main window as Python Object """
#     main_window_ptr = omui.MQtUtil.mainWindow()
#     return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

# 3DS MAX
# from pymxs import runtime as rt
# import MaxPlus
# def __init__(self, parent=MaxPlus.GetQMaxMainWindow())


# EXEMPLE STYLESHEET
exemple_style_sheet = """
QDialog{
    background-color : rgb(24,24,24);
    color : rgb(122,122,122);
    border-radius : 7px;
}

QLineEdit{
    background-color : rgb(24,24,24);
    border-radius : 5px;
    color : rgb(255, 255, 255);
}

QListWidget{
    background-color : rgb(24,24,24);
    border-radius : 7px;
    color : rgb(255, 255, 255);
}

QTableWidget{
    background-color : rgb(24,24,24);
    border-radius : 7px;
    color : rgb(255, 255, 255);
}
QLabel{
    color : rgb(255,255,255);
}

QPushButton{
    background-color : rgb(40,40,40);
    border-radius : 10px;
}

"""