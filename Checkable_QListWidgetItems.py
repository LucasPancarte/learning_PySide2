# -*- coding: utf-8 -*-

import sys

from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc
from PySide2 import QtWidgets as qtw

class StandaloneApp(qtw.QDialog):

    WINDOW_TITLE = 'Standalone App'

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = StandaloneApp()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=None):
        super(StandaloneApp, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ qtc.Qt.WindowContextHelpButtonHint|qtc.Qt.WindowMinMaxButtonsHint)
        self.setMinimumSize(500, 200)

        self.geometry=None

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.create_list_items()
    
    # UI CREATION
    def create_actions(self):
        """
        Create all actions used by Addon Manager
        """
        pass

    def create_widgets(self):
        """
        Create all widgets used by Addon Manager
        """
        self.my_list = qtw.QListWidget()


    def create_layouts(self):
        """
        Creates all layouts used by Addon Manager and adds all widgets to them
        """
        main_layout = qtw.QVBoxLayout(self)
        main_layout.addWidget(self.my_list)

    def create_connections(self):
        """
        Creates all connections between widgets and functions for Addon Manager
        """
        self.costume_list.itemChanged.connect(self.print_item_changed)

    def create_list_items(self):
    	"""
        Creates 10 checkable QListWidgetItems
        """
    	for i in range(10):
    		item = qtw.QListWidgetItem("Checkable Item #{0}".format(i))
			item.setFlags(item.flags() | qtc.Qt.ItemIsUserCheckable)
			item.setCheckState(qtc.Qt.Checked if not cost.isHidden else qtc.Qt.Unchecked)

			self.my_list.addItem(item)

	def print_item_changed(self):
		"""
        Print the state of the selected items, 
        and sets all state to the changed item s state
        """
        is_hidden = item.checkState()
        items = self.costume_list.selectedItems()

        for it in items:
            it.setCheckState(is_hidden)
            chck_state = False if is_hidden == qtc.Qt.CheckState.Unchecked else True

            print("{0} : is checked : {1}".format(it.text(), chck_state) )

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
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    ranApp = StandaloneApp()
    ranApp.show()

    # Run the main Qt loop
    sys.exit(app.exec_())