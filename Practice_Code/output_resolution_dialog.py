from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMayaUI as omui


def maya_main_window():
    """ Return Maya main window as Python Object """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class OutputResolutionDialog(QtWidgets.QDialog):
    
    RESOLUTION_ITEMS = [
        ["1920x1080 (1080p)", 1920.0, 1080.0],
        ["1280x720 (720p)", 1280.0, 720.0],
        ["960x540 (540p)", 960.0, 540.0],
        ["640x480 (480)", 640.0, 480.0],
        ["320x240 (240)", 320.0, 240.0]
    ]
    
    def __init__(self, parent=maya_main_window()):
        super(OutputResolutionDialog, self).__init__(parent)

        self.setWindowTitle("Output Resolution")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    def create_widgets(self):
        self.res_list_wdg = QtWidgets.QListWidget()
        # self.res_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)       
        # self.res_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)       
        # self.res_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)       
        # self.res_list_wdg.addItems(["1920x1080 (1080p)", "1280x720 (720p)", "960x540 (540p)"])
        
        for res in self.RESOLUTION_ITEMS:
            list_res_item = QtWidgets.QListWidgetItem(res[0])
            list_res_item.setData(QtCore.Qt.UserRole, [res[1], res[2]])
            self.res_list_wdg.addItem(list_res_item)
        
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.res_list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

    def create_connections(self):
        self.res_list_wdg.itemClicked.connect(self.set_output_resolution)
        self.close_btn.clicked.connect(self.close)
        
    def set_output_resolution(self, item):
        resolution = item.data(QtCore.Qt.UserRole)
        mc.setAttr("defaultResolution.width", resolution[0])
        mc.setAttr("defaultResolution.height", resolution[1])
        mc.setAttr("defaultResolution.deviceAspectRatio", resolution[0]/resolution[1])
        
        print("Resolution is : {0}".format(resolution))
        
if __name__ == "__main__":
    
    try:    
        out_res.close()
        out_res.deleteLater()
    except:
        pass
        
    out_res = OutputResolutionDialog()
    out_res.show()