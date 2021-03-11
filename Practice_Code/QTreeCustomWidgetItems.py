import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class CustomWidget(QWidget):
    def __init__(self, parent=None, name="", placeholderText=""):
        super(CustomWidget, self).__init__(parent)
        self.main_layout = QHBoxLayout(self)

        self.label = QLabel(name)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholderText)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.line_edit)  

class TreeWidgetWithWidgetItems(QDialog):
    def __init__(self):
        super(TreeWidgetWithWidgetItems, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)

        self.label = QLabel("I'm going to inform you about the buttons")
        # Adding the widgets
        self.vboxLayout.addWidget(self.treeWidget)
        self.vboxLayout.addWidget(self.label)
        self.treeWidget.setHeaderLabels(["TreeWidget with Buttons", "Custome Widgets"])
        self.topLevelItem = QTreeWidgetItem(["I m Top Level", ""])

        # Creating top level and child widgets
        self.topLevelButton = QPushButton("Top Level Button")
        self.childButton_1 = QPushButton("Child 1")
        self.childButton_2 = QPushButton("Child 2")
        self.childButton_3 = CustomWidget(name="Name :", placeholderText="Input Name Please")
        self.childLineEdit = QLineEdit()
        self.childLineEdit.setPlaceholderText("Add Text Here")

        # ..................(contd) ... from part-1
        # Adding the child to the top level item
        self.childItems = []

        for i in range(4):
            self.childItems.append(QTreeWidgetItem(["I m Child Level", ""]))
            self.topLevelItem.addChild(self.childItems[i])

        self.treeWidget.addTopLevelItem(self.topLevelItem)
        self.treeWidget.setItemWidget(self.topLevelItem, 1, self.topLevelButton)

        # Replacing the child items with widgets
        self.treeWidget.setItemWidget(self.childItems[0], 1, self.childButton_1)
        self.treeWidget.setItemWidget(self.childItems[1], 1, self.childButton_2)
        self.treeWidget.setItemWidget(self.childItems[2], 1, self.childButton_3)
        self.treeWidget.setItemWidget(self.childItems[3], 1, self.childLineEdit)

        # Connecting the widgets with corresponding slots
        self.topLevelButton.clicked.connect(self.top_button_clicked)
        self.childButton_1.clicked.connect(self.child_button_1_clicked)
        self.childButton_2.clicked.connect(self.child_button_2_clicked)

        self.childLineEdit.textEdited.connect(self.child_lineedit_edited)

        # Setting the layout
        self.setWindowTitle("QTreeWidget with Button Example")
        self.setLayout(self.vboxLayout)

    # Connects
    def top_button_clicked(self, clicked):
        self.label.setText("Top Level Button was Clicked")

    def child_button_1_clicked(self, clicked):
        self.label.setText("Child button 1 was clicked")

    def child_button_2_clicked(self, clicked):
        self.label.setText("Child button 2 was clicked")

    def child_button_3_clicked(self, clicked):
        self.label.setText("Child button 3 was clicked")

    def child_lineedit_edited(self, edited_text):
        self.label.setText(str(edited_text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = TreeWidgetWithWidgetItems()
    treeWidgetDialog.show()
    sys.exit(app.exec_())