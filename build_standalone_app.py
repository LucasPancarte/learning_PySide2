import sys
from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc
import random
import re

class RandomApp(qtw.QDialog):

    WINDOW_TITLE = 'Choice App'

    def __init__(self, parent=None):
        super(RandomApp, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(500, 200)

        self.geometry=None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        self.my_label = qtw.QLabel("Enter a list of \npossible choices\n seperated by ',':")
        self.my_line = qtw.QLineEdit()
        self.my_line.setFixedHeight(25)
        # self.my_line.setText("burger king, mcDo, subway, ranch, chat perche")


        self.button = qtw.QPushButton("CHOOSE !!!")
        self.button.setFixedHeight(50)

    def create_layouts(self):
        list_layout = qtw.QHBoxLayout()
        list_layout.addWidget(self.my_label)
        list_layout.addWidget(self.my_line)

        main_layout = qtw.QVBoxLayout(self)
        main_layout.addLayout(list_layout)
        main_layout.addWidget(self.button)

    def create_connections(self):
        self.button.clicked.connect(self.build_list_from_input)

    def build_list_from_input(self):
        self.ret_string = ""
        # choice_list = (self.my_line.text()).split(",")
        choice_list = re.split(' ,|,|, ',self.my_line.text())
        self.decide_for_me(choice_list)
        self.build_return_message_ui()

    def build_return_message_ui(self):
        message = qtw.QDialog()
        message.setWindowTitle("I Chose")
        mssg_layout= qtw.QHBoxLayout(message)
        choice_mssg = qtw.QLabel(self.ret_string)
        print(choice_mssg.fontInfo().family())
        choice_mssg.setFont(qtg.QFont("Times", 12, False))

        mssg_layout.addWidget(choice_mssg)
        message.exec_()

    def decide_for_me(self, user_input=None):
        if user_input != None:
            a_eliminer = random.choice(list(user_input))
            ind = user_input.index(a_eliminer)

            if len(user_input)!=1:
                user_input.pop(ind)
                self.ret_string+='"{0}" a été éliminé!\n'.format(a_eliminer)
                self.decide_for_me(user_input)
            else:
                self.ret_string+='\n\nLe choix est : \n\t-- "{0}" --\n'.format(user_input[0])

    

if __name__ == '__main__':
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    ranApp = RandomApp()
    ranApp.show()

    # Run the main Qt loop
    sys.exit(app.exec_())