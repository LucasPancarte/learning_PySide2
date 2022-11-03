# -*- coding: utf-8 -*-

import sys
import inspect
import datetime
from contextlib import contextmanager

from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc

class TemplateApp(qtw.QDialog):

    WINDOW_TITLE = 'Standalone App'
    INSTANCE = None
    feedback = False

    @classmethod
    def show_dialog(cls, *args, **kwargs):
        if not cls.INSTANCE:
            cls.INSTANCE = TemplateApp(*args, **kwargs)
            
        if cls.INSTANCE.isHidden():
            cls.INSTANCE.show()
        else:
            cls.INSTANCE.raise_()
            cls.INSTANCE.activateWindow()

    @classmethod
    @contextmanager
    def feedback_context(cls):
        temp_feedback = cls.feedback
        cls.feedback = True 
        yield 
        cls.feedback = temp_feedback

    @classmethod
    def log(cls, string_to_log=''):
        if cls.feedback:
            time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            print("{} - [{}.{}] - {}".format(time, cls.__name__, inspect.stack()[1][3], string_to_log))

    @classmethod
    def log_error(cls, func, string_to_log=''):
        string_to_log = "[ERROR] - {}".format(string_to_log)
        with cls.feedback_context():
            cls.log(string_to_log)

        if callable(func):
            func()

        raise Exception(string_to_log)

    def __init__(self, feedback=False, parent=None):
        super(TemplateApp, self).__init__(parent)
        TemplateApp.feedback = feedback
        
        self.log("Initializing class...")

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ qtc.Qt.WindowContextHelpButtonHint|qtc.Qt.WindowMinMaxButtonsHint)

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
        self.log("Creating Actions")
        
    def create_widgets(self):
        """
        Create all widgets used by Standalone app
        """
        self.log("Creating Widgets")
        
    def create_layouts(self):
        """
        Creates all layouts used by Standalone app and adds all widgets to them
        """
        self.log("Creating Layouts")
        main_layout = qtw.QVBoxLayout(self)

    def create_connections(self):
        """
        Creates all connections between widgets and functions for Standalone app
        """
        self.log("Creating Connections")


    def add_callbacks(self):
        """
        Add callbacks (mostly for DCC apps)
        """
        self.log("Adding callbacks")
        
    def remove_callbacks(self):
        """
        Remove callbacks (mostly for DCC apps)
        """ 
        self.log("Removing callbacks")

    # OPEN/CLOSE EVENTS
    def showEvent(self, e):
        """
        Event used on UI startup, 
        restore size and position if the ui already existed
        """
        self.log("Show Event")
        super(TemplateApp, self).showEvent(e)
        if self.geometry:
            self.restoreGeometry(self.geometry)

        self.add_callbacks()
   
    def closeEvent(self, e):
        """
        Event used on UI close
        saves size and position for the next ui showEvent
        """
        self.log("Close Event")
        self.remove_callbacks()
        if isinstance(self, TemplateApp):
            super(TemplateApp, self).closeEvent(e)
            self.geometry = self.saveGeometry()


if __name__ == '__main__':
    #FOR STANDALONE APP
    try:    
        TemplateApp.INSTANCE.close()
        TemplateApp.INSTANCE.deleteLater()
    except:
        pass
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    TemplateApp.show_dialog(feedback=True)

    # Run the main Qt loop
    sys.exit(app.exec_())

    #FOR DCC APP
    # try:    
    #     TemplateApp.INSTANCE.close()
    #     TemplateApp.INSTANCE.deleteLater()
    # except:
    #     print("Did not find any TemplateApp instance")
        
    # TemplateApp.show_dialog(feedback=True)
    # template_app = TemplateApp.INSTANCE


### DCC SPECIFICS
# MAYA
# from shiboken2 import wrapInstance

# import maya.cmds as mc
# import maya.api.OpenMaya as om
# import maya.OpenMayaUI as omui

# @classmethod # add this to the UI class to get the maya window
# def maya_main_window(cls):
#     """ Return Maya main window as Python Object """
#     main_window_ptr = omui.MQtUtil.mainWindow()
#     return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

# 3DS MAX
# from pymxs import runtime as rt
# import MaxPlus
# def __init__(self, parent=MaxPlus.GetQMaxMainWindow())
