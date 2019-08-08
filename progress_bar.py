from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
import time
import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui


# don't use reload() if you want to keep ui position
class ProgressBarUI(QtWidgets.QDialog):
    WINDOW_TITLE = "Progress Bar UI"
    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = ProgressBarUI()
            
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
        super(ProgressBarUI, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.do_it_btn = QtWidgets.QPushButton("Do It")

    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.do_it_btn)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)
                
    def create_connections(self):
        self.do_it_btn.clicked.connect(self.run_progress_bar)
    
    def run_progress_bar(self):
        number_of_operation = 10
        
        progress_dialog = QtWidgets.QProgressDialog("Wait to process...", "Cancel", 0, number_of_operation, self)
        progress_dialog.setWindowTitle("Progress...")
        progress_dialog.setValue(0)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.show()
        
        QtCore.QCoreApplication.processEvents() # processe QEvents before for loop ends
        
        for i in range(1, number_of_operation+1):
            if progress_dialog.wasCanceled():
                break
                
            progress_dialog.setLabelText("Processing operation : {0} /{1}".format(i, number_of_operation))
            progress_dialog.setValue(i)
            time.sleep(0.5)
            
            QtCore.QCoreApplication.processEvents() # processe QEvents before for loop ends

    
if __name__ == "__main__":
    
    try:    
        progress_bar.close()
        progress_bar.deleteLater()
    except:
        pass
        
    progress_bar = ProgressBarUI()
    progress_bar.show_dialog()