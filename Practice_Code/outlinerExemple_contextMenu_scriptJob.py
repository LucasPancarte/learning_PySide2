from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
from functools import partial

import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui


class OutlinerExemple(QtWidgets.QDialog):
    WINDOW_TITLE = "Custom Outliner"
    dlg_instance = None
    # don't use reload() if you want to keep ui position
    
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = OutlinerExemple()
            
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
        super(OutlinerExemple, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(300)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.transform_icon = QtGui.QIcon(":transform.svg")
        self.camera_icon = QtGui.QIcon(":Camera.png")
        self.mesh_icon = QtGui.QIcon(":mesh.svg")
        
        self.script_job_number = -1
        
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        self.refresh_tree_widget()
    
    def create_actions(self):
        self.about_action = QtWidgets.QAction("About", self)
        
        self.display_shape_action = QtWidgets.QAction("Shapes", self)
        self.display_shape_action.setCheckable(True)
        self.display_shape_action.setChecked(True)    
        self.display_shape_action.setShortcut(QtGui.QKeySequence("ctrl+shift+h"))    
    
    def create_widgets(self):
        self.menu_bar = QtWidgets.QMenuBar()
        display_menu = self.menu_bar.addMenu("Display")
        display_menu.addAction(self.display_shape_action)
        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction(self.about_action)
        
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # header = self.tree_widget.headerItem()
        # header.setText(0, "Column 0 Text")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layouts(self):
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.refresh_btn)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.setMenuBar(self.menu_bar)
        main_layout.addWidget(self.tree_widget)
        main_layout.addLayout(btn_layout)
        
    def create_connections(self):
        self.about_action.triggered.connect(self.about)
        self.display_shape_action.toggled.connect(self.set_shape_node_visible)
        self.refresh_btn.clicked.connect(self.refresh_tree_widget)
        self.tree_widget.itemCollapsed.connect(self.update_icon)
        self.tree_widget.itemExpanded.connect(self.update_icon)
        self.tree_widget.itemSelectionChanged.connect(self.select_items)
        
    def refresh_tree_widget(self):
        self.shape_nodes = mc.ls(shapes=True)
        
        self.tree_widget.clear()
        
        top_obj = mc.ls(assemblies=True)
        for obj in top_obj:
            item = self.create_item(obj)
            self.tree_widget.addTopLevelItem(item)
            
        self.update_selection()
        
    def create_item(self, name):
        item = QtWidgets.QTreeWidgetItem([name])
        self.add_children(item)
        self.update_icon(item)
        
        is_shape = name in self.shape_nodes
        item.setData(0, QtCore.Qt.UserRole, is_shape)
        
        return item
    
    def add_children(self, item):
        children = mc.listRelatives(item.text(0), c=True)
        if children:
            for child in children:
                child_item = self.create_item(child)
                item.addChild(child_item)
    
    def update_icon(self, item):
        obj_type = ""
        
        if item.isExpanded():
            obj_type = "transform"
        else:
            child_count = item.childCount()
            if child_count ==0:
                obj_type = mc.objectType(item.text(0))
            elif child_count == 1:
                child_item = item.child(0)
                obj_type = mc.objectType(child_item.text(0))
            else:
                obj_type = "transform"
        if obj_type == "transform":
            item.setIcon(0, self.transform_icon)
        elif obj_type == "camera":
            item.setIcon(0,self.camera_icon)
        elif obj_type == "mesh":
            item.setIcon(0,self.mesh_icon)
            
    def select_items(self):
        items = self.tree_widget.selectedItems()
        names = []
        for i in items:
            names.append(i.text(0))
            
        mc.select(names, replace=True)
        
    def about(self):
        QtWidgets.QMessageBox.about(self, "About outlinerExemple", "Add text here")
    
    def set_shape_node_visible(self, visible):
        iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        
        while iterator.value():
            item = iterator.value()
            is_shape = item.data(0, QtCore.Qt.UserRole)
            if is_shape:
                item.setHidden(not visible)
                
            iterator += 1
            
    def show_context_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addAction(self.display_shape_action)
        context_menu.addSeparator()
        context_menu.addAction(self.about_action)
        
        context_menu.exec_(self.mapToGlobal(point))
    
    def update_selection(self):
        selection = mc.ls(sl=True)
        iterator = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while iterator.value():
            item = iterator.value()
            is_selected = item.text(0) in selection
            item.setSelected(is_selected)
            
            iterator += 1
            
    def set_scriptjob_enabled(self, enabled):
        if enabled and self.script_job_number < 0:
            self.script_job_number = mc.scriptJob(event=["SelectionChanged", partial(self.update_selection)], protected=True)
            
        elif not enabled and self.script_job_number >= 0:
            mc.scriptJob(kill=self.script_job_number, force=True)
            self.script_job_number = -1
            
    def showEvent(self, e):
        super(OutlinerExemple, self).showEvent(e)
        self.set_scriptjob_enabled(True)
        
    def closeEvent(self, e):
        if isinstance(self, OutlinerExemple): 
            super(OutlinerExemple, self).closeEvent(e)
            self.set_scriptjob_enabled(False)
    
if __name__ == "__main__":
    
    try:   
        outliner_exp.set_script_job_enabled(False)
        outliner_exp.close()
        outliner_exp.deleteLater()
    except:
        pass
        
    outliner_exp = OutlinerExemple()
    outliner_exp.show()