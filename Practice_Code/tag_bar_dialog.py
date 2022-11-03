from functools import partial

from PySide2 import QtWidgets as qtw
from PySide2 import QtCore as qtc
from PySide2 import QtGui as qtg

import MaxPlus
from pymxs import runtime as rt

class TagBar(qtw.QDialog):
    def __init__(self):
        super(TagBar, self).__init__(parent=MaxPlus.GetQMaxMainWindow())
        self.setWindowTitle('Tag Bar')
        self.tags = []

        self.setMinimumSize(400, 200)

        self.h_layout = qtw.QHBoxLayout()
        self.h_layout.setSpacing(4)

        self.v_layout = qtw.QVBoxLayout(self)
        self.v_layout.addLayout(self.h_layout)

        self.line_edit = qtw.QLineEdit()
        self.line_edit.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Maximum)
        self.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)
        
        self.setContentsMargins(2,2,2,2)
        self.h_layout.setContentsMargins(2,2,2,2)
        self.refresh()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.line_edit.returnPressed.connect(self.create_tags)

    def create_tags(self):
        new_tags = self.line_edit.text().split(', ')
        self.line_edit.setText('')
        self.tags.extend(new_tags)
        self.tags = list(set(self.tags))
        self.tags.sort(key=lambda x: x.lower())
        self.refresh()

    def refresh(self):
        for i in reversed(range(self.h_layout.count())):
            self.h_layout.itemAt(i).widget().setParent(None)

        for tag in self.tags:
            self.add_tag_to_bar(tag)

        self.v_layout.addWidget(self.line_edit)
        self.line_edit.setFocus()

    def add_tag_to_bar(self, text):
        tag = qtw.QFrame()
        tag.setStyleSheet(
            'border:1px solid; '
            'border-color: red;'
            'border-radius: 10px;'
            'border-style: outset;'
            'background-color: yellow;'
            )
        tag.setContentsMargins(2, 2, 2, 2)
        tag.setFixedHeight(28)

        hbox = qtw.QHBoxLayout()
        hbox.setContentsMargins(4, 4, 4, 4)
        hbox.setSpacing(10)
        tag.setLayout(hbox)

        label = qtw.QLabel(text)
        label.setStyleSheet(
            'border:0px;'
            'color: black;'
            'size: 18px;'
            'font-weight:bold;'
            )
        label.setFixedHeight(16)
        hbox.addWidget(label)

        x_button = qtw.QPushButton('x')
        x_button.setFixedSize(20, 20)
        x_button.setStyleSheet(
            'border:0px;'
            'font-weight:bold;'
            )
        x_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        x_button.clicked.connect(partial(self.delete_tag, text))
        
        hbox.addWidget(x_button)
        tag.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Preferred)
        self.h_layout.addWidget(tag)

    def delete_tag(self, tag_name):
        self.tags.remove(tag_name)
        self.refresh()

# TESTING CODE
if __name__ == "__main__":
    """
    If the code is executed from this file refresh everything
    """
    rt.clearListener()
        
    tag_bar = TagBar()
    tag_bar.show()