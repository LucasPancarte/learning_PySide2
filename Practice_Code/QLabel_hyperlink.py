import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import MaxPlus
from pymxs import runtime as rt


"""
NOTE 
# for opening a folder
    link = "<a href=\"file:///{0}\">The title of the link</a>".format(the_folder_link_as_string) 

# for opening an internet link
    link = "<a href=\"{0}\">he title of the link</a>".format(the_internet_link_as_string) 
"""

class CustomWidget(QWidget):
    def __init__(self, parent=None, name="", link="", display_text="Click Me", link_type="file"):
        """
        link_type (string): either file or internet
        """
        super(CustomWidget, self).__init__(parent)
        if link_type is "file":
            full_link = "<a href=\"file:///{0}\">{1}</a>".format(link, display_text)
        else:
            full_link = "<a href=\"{0}\">{1}</a>".format(link, display_text)

        self.main_layout = QHBoxLayout(self)

        self.label = QLabel(name)
        self.hyper_link = QLabel()
        self.hyper_link.setAlignment(Qt.AlignLeft)
        self.hyper_link.setText(full_link)
        self.hyper_link.setTextFormat(Qt.RichText)
        self.hyper_link.setOpenExternalLinks(True)
        self.hyper_link.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.hyper_link)
        self.main_layout.addStretch()
        # self.main_layout.addWidget(self.line_edit)  

class TreeWidgetWithWidgetItems(QDialog):
    folder_link = "X:\\Main\\data\\Personal\\lpancarte\\Meshio_dev_tests\\"
    website_link = "https://www.google.com"

    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(TreeWidgetWithWidgetItems, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(3)

        self.label = QLabel("I'm going to inform you about the buttons")
        # Adding the widgets
        self.vboxLayout.addWidget(self.treeWidget)
        self.vboxLayout.addWidget(self.label)
        self.treeWidget.setHeaderLabels(["Item Names", "Stuff", "Custom Widgets"])
        self.topLevelItem = QTreeWidgetItem(["I m Top Level", "", ""])

        # Creating top level and child widgets
        self.topLevelButton = QPushButton("I m a top level button")
        self.childButton_01 = QPushButton("I m a child button")
        self.childLineEdit_01 = QLineEdit()
        self.childLineEdit_01.setPlaceholderText("Add Text Here")
        
        self.internet_link = CustomWidget(name="WebSite :", link=self.website_link, display_text="Click Me (Internet Link)", link_type="internet")
        self.explorer_link = CustomWidget(name="Folder :", link=self.folder_link, display_text="Click Me (Explorer Link)", link_type="file")
        self.childLineEdit_02 = QLineEdit()
        self.childLineEdit_02.setPlaceholderText("Add Text Here")

        self.childItems = []

        for i in range(4):
            self.childItems.append(QTreeWidgetItem(["Child : %s" % i, "", ""]))
            self.topLevelItem.addChild(self.childItems[i])

        self.treeWidget.addTopLevelItem(self.topLevelItem)
        self.treeWidget.setItemWidget(self.topLevelItem, 2, self.topLevelButton)

        # Replacing the child items with widgets
        self.treeWidget.setItemWidget(self.childItems[0], 1, self.childButton_01)
        self.treeWidget.setItemWidget(self.childItems[0], 2, self.childLineEdit_01)
        self.treeWidget.setItemWidget(self.childItems[1], 2, self.internet_link)
        self.treeWidget.setItemWidget(self.childItems[2], 2, self.explorer_link)
        self.treeWidget.setItemWidget(self.childItems[3], 2, self.childLineEdit_02)

        # Connecting the widgets with corresponding slots
        self.topLevelButton.clicked.connect(self.top_button_clicked)
        self.childButton_01.clicked.connect(self.child_button_1_clicked)
        self.childLineEdit_01.textEdited.connect(self.child_lineedit_01_edited)
        self.childLineEdit_02.textEdited.connect(self.child_lineedit_02_edited)

        # Setting the layout
        self.setWindowTitle("QTreeWidget With Custom Widgets")
        self.setLayout(self.vboxLayout)

    # Connects
    def top_button_clicked(self):
        self.label.setText("Top Level Button was Clicked")

    def child_button_1_clicked(self):
        self.label.setText("Child button 1 was clicked")

    def child_lineedit_01_edited(self):
        self.label.setText(self.childLineEdit_01.text())

    def child_lineedit_02_edited(self):
        self.label.setText(self.childLineEdit_02.text())


if __name__ == '__main__':
    rt.clearListener()

    treeWidgetDialog = TreeWidgetWithWidgetItems()
    treeWidgetDialog.show()