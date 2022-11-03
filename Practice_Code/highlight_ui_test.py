from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc

import pymxs
from pymxs import runtime as rt
import MaxPlus


class StandaloneApp(qtw.QDialog):
    WINDOW_TITLE = 'Test Switch StyleSheet'
    dlg_instance = None
    style_sheet = None

    all_widgets = list()
    on_off = False

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = StandaloneApp()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=MaxPlus.GetQMaxMainWindow(), style_sheet=None):
        super(StandaloneApp, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ qtc.Qt.WindowContextHelpButtonHint | qtc.Qt.WindowMinMaxButtonsHint)

        self.geometry = None

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self._on_button_pressed()

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
        for i in range(5):
            the_lineEdit = qtw.QLineEdit()
            the_lineEdit.setPlaceholderText("I am LineEdit {num}".format(num=i))
            self.all_widgets.append(the_lineEdit)

        # self.the_button = qtw.QPushButton('I am a Button')
        # self.the_button.setMinimumHeight(50)


    def create_layouts(self):
        """
        Creates all layouts used by Standalone app and adds all widgets to them
        """
        self.main_layout = qtw.QVBoxLayout(self)
        for i in range(5):
            self.main_layout.addWidget(self.all_widgets[i])

        # self.main_layout.addWidget(self.the_button)

    def create_connections(self):
        """
        Creates all connections between widgets and functions for Standalone app
        """
        for widget in self.all_widgets:
            widget.textChanged.connect(self._on_button_pressed)
        # self.the_button.clicked.connect(self._on_button_pressed)

    def _on_button_pressed(self):
        # print("[_on_button_pressed] - All widgets : {widgets}".format(widgets=self.all_widgets))
        for widget in self.all_widgets:
            if widget.text()!="" and len(widget.text().strip())>0:
                widget.setStyleSheet('')
                    
            else:
                widget.setStyleSheet(#'background-color: red;'
                                    'border-style: outset;'
                                    'border-width: 2px;'
                                    # 'border-radius: 10px;'
                                    'border-color: yellow;'
                                    # 'font: bold 14px;'
                                    # 'min-width: 10em;'
                                    # 'padding: 6px;'
                                    )


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
    # app = qtw.QApplication(sys.argv)
    # Create and show the form
    # ranApp = StandaloneApp()
    # ranApp.show()

    # Run the main Qt loop
    # sys.exit(app.exec_())

    #FOR DCC APP
    rt.clearListener()
    try:
        template_ui.close()
        template_ui.deleteLater()
    except:
        pass

    template_ui = StandaloneApp()
    template_ui.show_dialog()

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