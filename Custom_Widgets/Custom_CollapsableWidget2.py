from PySide2 import QtWidgets as qtw
from PySide2 import qtg as qtg
import MaxPlus


class Header(qtw.QWidget):
    """Header class for collapsible group"""

    def __init__(self, name, content_widget):
        """Header Class Constructor to initialize the object.
        Args:
            name (str): Name for the header
            content_widget (qtw.QWidget): Widget containing child elements
        """
        super(Header, self).__init__()
        self.content = content_widget
        self.expand_ico = qtg.QPixmap(":teDownArrow.png")
        self.collapse_ico = qtg.QPixmap(":teRightArrow.png")

        self.setFixedHeight(20)

        stacked = qtw.QStackedLayout(self)
        stacked.setStackingMode(qtw.QStackedLayout.StackAll)
        background = qtw.QLabel()
        background.setStyleSheet("QLabel{ background-color: rgb(93, 93, 93); border-radius:2px}")

        widget = qtw.QWidget()
        layout = qtw.QHBoxLayout(widget)

        self.icon = qtw.QLabel()
        self.icon.setPixmap(self.expand_ico)
        layout.addWidget(self.icon)
        layout.setContentsMargins(11, 0, 11, 0)

        font = qtg.QFont()
        font.setBold(True)
        label = qtw.QLabel(name)
        label.setFont(font)

        layout.addWidget(label)
        layout.addItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding))

        stacked.addWidget(widget)
        stacked.addWidget(background)
        background.setMinimumHeight(layout.sizeHint().height() * 1.5)

    def mousePressEvent(self, *args):
        """Handle mouse events, call the function to toggle groups"""
        self.expand() if not self.content.isVisible() else self.collapse()

    def expand(self):
        self.content.setVisible(True)
        self.icon.setPixmap(self.expand_ico)

    def collapse(self):
        self.content.setVisible(False)
        self.icon.setPixmap(self.collapse_ico)


class Container(qtw.QWidget):
    """Class for creating a collapsible group similar to how it is implement in Maya
        Examples:
            Simple example of how to add a Container to a QVBoxLayout and attach a QGridLayout
            >>> layout = qtw.QVBoxLayout()
            >>> container = Container("Group")
            >>> layout.addWidget(container)
            >>> content_layout = qtw.QGridLayout(container.contentWidget)
            >>> content_layout.addWidget(qtw.QPushButton("Button"))
    """
    def __init__(self, name, color_background=False):
        super(Container, self).__init__()
        """Container Class Constructor to initialize the object
        Args:
            name (str): Name for the header
            color_background (bool): whether or not to color the background lighter like in maya
        """
        layout = qtw.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._content_widget = qtw.QWidget()
        if color_background:
            self._content_widget.setStyleSheet("QWidget{background-color: rgb(73, 73, 73); "
                                               "margin-left: 2px; margin-right: 2px}")
        header = Header(name, self._content_widget)
        layout.addWidget(header)
        layout.addWidget(self._content_widget)

        # assign header methods to instance attributes so they can be called outside of this class
        self.collapse = header.collapse
        self.expand = header.expand
        self.toggle = header.mousePressEvent

    @property
    def contentWidget(self):
        """Getter for the content widget
        Returns: Content widget
        """
        return self._content_widget


if __name__ == "__main__":

    main_widget = qtw.QDialog(MaxPlus.GetQMaxMainWindow())
    layout = qtw.QVBoxLayout(main_widget)
    container = Container("Group", False)
    layout.addWidget(container)

    content_layout = qtw.QGridLayout(container.contentWidget)
    content_layout.addWidget(qtw.QPushButton("Button"))
    layout.addStretch()

    main_widget.show()