from __Learning_PyQt5.pyQt5_window_template import TemplateUi
from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as mc
import json
import shutil
import os


# don't use reload() if you want to keep ui position
class SaveInMultFolders(TemplateUi):
    WINDOW_TITLE = "Saving UI"
    dlg_instance = None
    PATH_LIST = []
    FILE_FILTER = "JSON(*.json);;ALL(*.*)"
    selected_filter = "JSON(*.json)"
    default_json_path = mc.internalVar(upd=True)

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = SaveInMultFolders()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self):
        super(SaveInMultFolders, self).__init__()
        
        self.geometry = None
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(500,400)
        self.pre_load_path_list()

    def create_widgets(self):
        self.add_path_btn = QtWidgets.QPushButton("Add Saving Path")
        self.del_path_btn = QtWidgets.QPushButton("Del Saving Path")
        self.save_paths_btn = QtWidgets.QPushButton("Save Path\nto 'file.json'")
        self.load_paths_btn = QtWidgets.QPushButton("Load Path\nfrom 'file.json'")
        
        self.add_path_btn.setMinimumSize(50, 50)
        self.del_path_btn.setMinimumSize(50, 50)
        self.save_paths_btn.setMinimumSize(50, 50)
        self.load_paths_btn.setMinimumSize(50, 50)
        
        self.save_ascii_btn = QtWidgets.QPushButton("Save Ascii")
        self.save_binary_btn = QtWidgets.QPushButton("Save Binary")
        self.save_ascii_btn.setMinimumSize(50, 50)
        self.save_binary_btn.setMinimumSize(50, 50)
        
        self.dir_lab = QtWidgets.QLabel("Directorie:")
        self.path_list = QtWidgets.QListWidget()
        self.path_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.name_lab = QtWidgets.QLabel("File Name :")
        self.file_name = QtWidgets.QLineEdit()
        self.file_name.setText((self.get_current_scene()).split(".")[0])

    def create_layouts(self):
        paths_layout = QtWidgets.QVBoxLayout()
        paths_layout.addWidget(self.add_path_btn)
        paths_layout.addWidget(self.del_path_btn)
        paths_layout.addWidget(self.save_paths_btn)
        paths_layout.addWidget(self.load_paths_btn)
        paths_layout.addStretch()
        paths_layout.addWidget(self.save_ascii_btn)
        paths_layout.addWidget(self.save_binary_btn)
        
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(self.name_lab)
        name_layout.addWidget(self.file_name)
        
        dir_layout = QtWidgets.QVBoxLayout()
        dir_layout.addWidget(self.dir_lab)
        dir_layout.addWidget(self.path_list)
        dir_layout.addLayout(name_layout)
        
        up_layout = QtWidgets.QHBoxLayout()
        up_layout.addLayout(dir_layout)
        up_layout.addLayout(paths_layout)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(up_layout)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(5)

    def create_connections(self):
        self.add_path_btn.clicked.connect(self.add_path)
        self.del_path_btn.clicked.connect(self.del_path)

        self.save_paths_btn.clicked.connect(self.save_to_json)
        self.load_paths_btn.clicked.connect(self.load_path_file)
        
        self.save_ascii_btn.clicked.connect(self.save_ascii)
        self.save_binary_btn.clicked.connect(self.save_binary)
        
        self.path_list.itemDoubleClicked.connect(self.open_explorer_from_path)

    def add_path(self):
        self.search_for_path()
        self.refresh_path_table()

    def del_path(self):
        selected_items = self.retrieve_data()
        for p in selected_items:
            if [p,p] in self.PATH_LIST:
                self.PATH_LIST.remove([p,p])
        
        self.refresh_path_table()
        
    def save_ascii(self): self.save_file(extension=".ma", file_type="mayaAscii")
        
    def save_binary(self): self.save_file(extension=".mb", file_type="mayaBinary")

    def save_file(self, extension, file_type):
        selected_paths = self.retrieve_data()
        name = self.file_name.text()
        continuing = True
        
        for i, path in enumerate(selected_paths):
            if len(name)>0:
                full_path = path+"/"+name+extension
                if i==0:
                    if self.file_exists(full_path): 
                        if not self.question():
                            print("Stopping Saving process for {0}".format(full_path))
                            continuing = False
                        else:
                            mc.file(rename=full_path)
                            mc.file(s=True, f=True, typ=file_type)
                    else:
                        mc.file(rename=full_path)
                        mc.file(s=True, f=True, typ=file_type)
                        
                elif continuing:
                    shutil.copyfile((selected_paths[0]+"/"+name+extension), full_path)
                
                else:
                    mc.warning("Canceled Saving Operation")
    
    def refresh_path_table(self):
        self.path_list.clear()
        
        for path in self.PATH_LIST:
            path_list_item = QtWidgets.QListWidgetItem(path[0])
            path_list_item.setData(QtCore.Qt.UserRole, [path[1]])
            self.path_list.addItem(path_list_item)

    def search_for_path(self):
        file_dialog = QtWidgets.QFileDialog()
        path = file_dialog.getExistingDirectory(self, "Open Directory", "", file_dialog.ShowDirsOnly|file_dialog.DontResolveSymlinks)
        if [path, path] not in self.PATH_LIST:
            p_list = [path, path]
            self.PATH_LIST.append(p_list)
            
    def retrieve_data(self):
        selected_data = []
        selected_items = self.path_list.selectedItems()
        
        for item in selected_items:
            path = item.data(QtCore.Qt.UserRole)
            
            if path[0] not in selected_data: 
                selected_data.append(path[0])
                
        return selected_data
        
    def file_exists(self,path): return os.path.isfile(path)
        
    def question(self):
        button_pressed = QtWidgets.QMessageBox.question(self, "Question", "File Already exists.\nWould you like to continue anyway?")
        if button_pressed == QtWidgets.QMessageBox.Yes:
            return(True)
        else:
            return(False)
            
    def get_current_scene(self): return mc.file(q=True, sn=True, shn=True)
    
    def read_from_json(self, file_path):
        try:
            with open(file_path, "r") as jsonFile:
                return json.load(jsonFile)
        except:
            print("Could not read : {0}".format(file_path))
            
    def save_to_json(self):
        default_path = mc.internalVar(upd=True)

        file_dialog = QtWidgets.QFileDialog()
        file_path, self.selected_filter = file_dialog.getSaveFileName(self, "Get Directory for Path File", default_path, self.FILE_FILTER, self.selected_filter)
        
        json_name = file_path # +"/SavingLocation.json" Not needed when using "file_dialog.getSaveFileName()"
        
        if len(self.PATH_LIST) >= 1:
            
            with open(json_name, "w") as jsonFile:
                json.dump(self.PATH_LIST, jsonFile, indent=4)
                print("Data was successfully written to : {0}".format(json_name))
    
    def load_path_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, self.selected_filter = file_dialog.getOpenFileName(self, "Search for Path File", self.default_json_path, self.FILE_FILTER, self.selected_filter)

        if self.file_exists(file_path):
            path_data = self.read_from_json(file_path)
            for path in path_data:
                if path not in self.PATH_LIST: 
                    self.PATH_LIST.append(path)
                
        self.refresh_path_table()
        print("Data was successfully loaded from : {0}".format(file_path))
    
    def pre_load_path_list(self):
        path_file = self.default_json_path + "SavingLocation.json"

        if self.file_exists(path_file):
            path_data = self.read_from_json(path_file)
            for path in path_data:
                if path not in self.PATH_LIST: 
                    self.PATH_LIST.append(path)
            print("Preloaded path file from : {0}".format(path_file))

        self.refresh_path_table()

    def open_explorer_from_path(self):
        print("is double clicked")
        double_clicked_path = (self.retrieve_data())[0]
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.getOpenFileName(self, "Selected Directory", double_clicked_path)


if __name__ == "__main__":
    
    try:    
        save_ui.close()
        save_ui.deleteLater()
    except:
        pass
        
    save_ui = save_ui.SaveInMultFolders()
    save_ui.show_dialog()