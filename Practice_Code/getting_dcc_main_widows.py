from Pyside2.QtWidgets import *

# Get 3dsMax 2020 Main Window
def get_qmax_main_window():
    """Get the 3DS MAX main window.
    
    Returns:
        PySide2.QtWidgets.QMainWindow: 'QMainWindow' 3DS MAX main window.
    """
    for w in QApplication.topLevelWidgets():
        if w.inherits('QMainWindow') and w.metaObject().className() == 'QmaxApplicationWindow':
            return w
    raise RuntimeError('Count not find QmaxApplicationWindow instance.')


# Get Houdini 18 Main Window
import hou
def getHoudiniMainWindow():
    """Get the Houdini main window.
    
    Returns:
        PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
    """
    return hou.qt.mainWindow()


# Get Katana 3 Main Window
from UI4.App import MainWindow
def getKatanaMainWindow():
    """Get the Katana main window.
    Returns:
        UI4.App.MainWindow.KatanaWindow: 'KatanaWindow' Katana main window.
    """
    return MainWindow.GetMainWindow()


# Get Mari 4 Main Window
import mari
def getMariMainWindow():
    """Get the Mari main window.
    
    Returns:
        PySide2.QtWidgets.QWidget: 'MriMainWindow' Mari main window.
    """
    # Set Mari main window to be in focus.
    mari.app.activateMainWindow()
    # Returns the window that has focus.
    return QApplication.activeWindow()


# Get Maya 2020 Main Window
import shiboken2
import maya.OpenMayaUI as omui
def getMayaMainWindow():
    """Get the Maya main window.
    
    Returns: 
        PySide2.QtWidgets.QWidget:  'TmainWindow' Maya main window.
    """
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(long(ptr), QWidget)


# Get Nuke 12 Main Window
def getNukeMainWindow():
    """Get the Nuke main window.
    Returns:
        PySide2.QtWidgets.QMainWindow: 'DockMainWindow' Nuke main window.
    """
    for w in QApplication.topLevelWidgets():
        if w.inherits('QMainWindow') and w.metaObject().className() == 'Foundry::UI::DockMainWindow':
            return w
    raise RuntimeError('Could not find DockMainWindow instance')