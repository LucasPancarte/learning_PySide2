"""
Pyside2

usage:

player = MoviePlayer(fileName = "//directory/file.gif")
player.show() 

"""

"""
Learn about QtGui.QImageReader()
"""

from __Learning_PyQt5.pyQt5_window_template import TemplateUi
from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

class MoviePlayer(TemplateUi):
    WINDOW_TITLE="Gif Player"
    FILE_FILTER = "GIF (*.gif)"
    selected_filter = "GIF (*.gif)"
    # fileName = ""
    
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = MoviePlayer()
                    
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()
            
    def __init__(self, fileName=''):
        self.fileName = fileName
        super(MoviePlayer, self).__init__()
        self.setMinimumSize(300, 300)
        self.geometry = None

        
    def create_widgets(self):        
        self.movie_screen = QtWidgets.QLabel()
        self.movie_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        
        self.path_btn = QtWidgets.QPushButton("Search For A Gif File")

        self.rewind_btn = QtWidgets.QPushButton()
        self.rewind_btn.setIcon(QtGui.QIcon(":timeprevSequencer.png"))
        self.rewind_btn.setMaximumWidth(50)

        self.btn_start = QtWidgets.QPushButton("Start Animation")
        self.btn_stop = QtWidgets.QPushButton("Stop Animation")

        self.forward_btn = QtWidgets.QPushButton()
        self.forward_btn.setIcon(QtGui.QIcon(":timenextSequencer.png"))
        self.forward_btn.setMaximumWidth(50)
        
        self.movie = QtGui.QMovie(self.fileName, QtCore.QByteArray(), self)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)        
        self.movie_screen.setMovie(self.movie)
    
    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.rewind_btn)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.forward_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.path_btn)
        main_layout.addWidget(self.movie_screen)
        main_layout.addLayout(btn_layout)
    
    def create_connections(self):
        self.path_btn.clicked.connect(self.search_for_gif)
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.forward_btn.clicked.connect(self.go_to_next_frame)
        self.rewind_btn.clicked.connect(self.go_to_previous_frame)
        self.movie.start()
        self.movie.stop()

    def search_for_gif(self):
        self.fileName, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self,"Select File", "", self.FILE_FILTER, self.selected_filter)
        self.movie.setFileName(self.fileName)
        self.start()
        
    def start(self): self.movie.start()

    def stop(self): self.movie.stop()

    def go_to_next_frame(self): self.movie.jumpToFrame(self.movie.currentFrameNumber()+1)

    def go_to_previous_frame(self): self.movie.jumpToFrame(self.movie.currentFrameNumber()-1)
        
        

if __name__ == "__main__":

    try:    
        template_ui.close()
        template_ui.deleteLater()
    except:
        pass
        
    template_ui = MoviePlayer()
    template_ui.show_dialog()