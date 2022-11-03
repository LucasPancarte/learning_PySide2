from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg

import pymxs
from pymxs import runtime as rt
import MaxPlus

class DynamicTreeWidget(qtw.QTreeWidget):

	dummy_item_list = [ # dummy item column strings -> 3 columns
		["First_item", "", ""], 
		["second_Item", "", ""],
		["The_item", "", ""], 
		["blablabla", "", ""],
		["some_other_item", "", ""]
	]

	def __init__(self):
		super(DynamicTreeWidget, self).__init__()

		self.setColumnCount(3)
		self.setHeaderLabels(["Name", "2nd Column", "Last Column"])

		self.create_items_and_popuplate()

		self.header().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)

	def create_items_and_popuplate(self):
		"""
		Create top level items with an "add child" button
		"""
		for i, item_name in enumerate(self.dummy_item_list):
			item = qtw.QTreeWidgetItem([item_name[0], item_name[1], item_name[2]])
			self.addTopLevelItem(item)
			self.expandItem(item)

			add_child_button = qtw.QPushButton("Add Child")
			add_child_button.clicked.connect(self.add_child_item)

			self.setItemWidget(item, 1, add_child_button)
			add_item_widget = self.itemWidget(item, 1)

	def add_child_item(self):
		"""
		Adds a child item to the item under the mouse
		This item is added with a pair of "add child" and "remove me" buttons
		!!! NOTE : when the "remove me" button is clicked it will also remove all the current item's children !!!
		"""
		current_item = self.itemAt(self.get_mouse_position())

		if current_item:
			add_child_button = qtw.QPushButton("Add Child")
			remove_child_button = qtw.QPushButton("Remove Me (and my kids)")
			add_child_button.clicked.connect(self.add_child_item)
			remove_child_button.clicked.connect(self.remove_child_item)

			child_item = qtw.QTreeWidgetItem(["New_Child", "", ""])

			current_item.addChild(child_item)
			self.setItemWidget(child_item, 1, add_child_button)
			self.setItemWidget(child_item, 2, remove_child_button)
			add_item_widget = self.itemWidget(child_item, 1)
			remove_item_widget = self.itemWidget(child_item, 2)
			self.expandItem(child_item)

	def remove_child_item(self):
		"""
		Here we get the item's parent to delete it s child 
		either the items's direct parent or the tree's invisible root item
		if we are trying to delete a top level item
		"""
		current_item = self.itemAt(self.get_mouse_position())
		(current_item.parent() or self.invisibleRootItem()).removeChild(current_item)

	def get_mouse_position(self):
		"""
		We map to the qtreewidget's viewport instead of the widget itself to mimic event.pos()*
		"""
		return self.viewport().mapFromGlobal(qtg.QCursor.pos())


class DynamicTreeUI(qtw.QDialog):

	dlg_instance = None

	@classmethod
	def show_dialog(cls):
		"""
		Holds and instance of the UI so that any further uses will keep all values (selections, size, position etc)
		"""
		if not cls.dlg_instance:
			cls.dlg_instance = DynamicTreeUI()

		if cls.dlg_instance.isHidden():
			cls.dlg_instance.show()
		else:
			cls.dlg_instance.raise_()
			cls.dlg_instance.activateWindow()

	def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
		super(DynamicTreeUI, self).__init__(parent)

		self.geometry = None

		self.setMinimumWidth(400)

		self.create_actions()
		self.create_widgets()
		self.create_layouts()
		self.create_connections()

	def create_actions(self):
		pass

	def create_widgets(self):
		self.tree_widget = DynamicTreeWidget()

	def create_layouts(self):
		main_layout = qtw.QVBoxLayout(self)
		main_layout.addWidget(self.tree_widget)

	def create_connections(self):
		pass

	def mousePressEvent(self, event):
		self.tree_widget.mousePressEvent(event)
		super(DynamicTreeUI, self).mousePressEvent(event)

	# OPEN/CLOSE EVENTS
	def showEvent(self, e):
		"""
		Event used on UI startup, 
		restore size and position if the ui already existed
		"""
		super(DynamicTreeUI, self).showEvent(e)
		if self.geometry:
			self.restoreGeometry(self.geometry)

	def closeEvent(self, e):
		"""
		Event used on UI close
		saves size and position for the next ui showEvent
		"""
		if isinstance(self, DynamicTreeUI):
			super(DynamicTreeUI, self).closeEvent(e)
			self.geometry = self.saveGeometry()



if __name__ == "__main__":

	rt.clearListener()

	try:    
		dynamic_tree_ui.close()
		dynamic_tree_ui.deleteLater()
	except:
		pass

	dynamic_tree_ui = DynamicTreeUI()
	dynamic_tree_ui.show_dialog()
