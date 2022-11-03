class TagWidget(qtw.QFrame):

    leftClicked = qtc.Signal()
    rightClicked = qtc.Signal()
    middleClicked = qtc.Signal()
    xButtonClicked = qtc.Signal(str)

    def __init__(self, tag_text, color=None, prefix_to_remove=None, parent=None, *args, **kwargs):
        super(TagWidget, self).__init__(parent=parent, *args, **kwargs)
        self.text = tag_text
        self.color = color

        self.prefix_to_remove = list() if prefix_to_remove is None else prefix_to_remove

        self.setFixedHeight(18)
        # self.setToolTip(self.text)
        self.setStyleSheet(
            'border:2px solid; '
            'border-color:#1787b7;'
            'border-radius:5px;'
            'background-color:#404040;'
        )

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.tag_label = qtw.QLabel()
        self.tag_label.setText(self.__remove_prefix(self.text).capitalize())
        self.tag_label.setStyleSheet(
            'border:0px;'
            'color:white;'
            'font-size:10px;'
            'font-weight:bold;'
        )
        self.tag_label.setAlignment(qtc.Qt.AlignLeft)
        self.tag_label.setFixedHeight(12)
        self.tag_label.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)

        self.x_button = qtw.QPushButton('X')
        self.x_button.setFixedSize(20, 20)
        self.x_button.setStyleSheet(
            'border:1px;'
            'font-weight:bold;'
            )
        self.x_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)

    def create_layouts(self):
        tag_layout = qtw.QHBoxLayout()
        tag_layout.setContentsMargins(4, 2, 4, 2)
        tag_layout.setSpacing(10)
        self.setLayout(tag_layout)

        if self.color:
            tag_layout.addWidget(self.__make_color_tag(self.color))

        tag_layout.addWidget(self.tag_label)
        tag_layout.addWidget(self.x_button)

    def create_connections(self):
        self.x_button.clicked.connect(self.delete_widget)
        self.middleClicked.connect(self.delete_widget)

    def delete_widget(self, *args):
        self.setParent(None)
        self.xButtonClicked.emit(self.text)

    def mousePressEvent(self, event):
        """
        Re-define mousePressEvent to implement right-click/left-click/middle-click
        """ 
        if event.type() == qtc.QEvent.MouseButtonPress:
            if event.button() == qtc.Qt.LeftButton:
                self.leftClicked.emit()

            elif event.button() == qtc.Qt.MidButton:
                self.middleClicked.emit()

            else:
                super(TagWidget, self).mousePressEvent(event)

    def __remove_prefix(self, tag_text):
        """
        Removes the prefixes of certain tags to be user friendly
        Args:
        tag_text: string, the tag to truncate
        Returns:
        string, the tag without prefixes
        """

        temp_tag_text = tag_text
        for prefix in self.prefix_to_remove:
            temp_tag_text = temp_tag_text.replace(prefix, '')

        return temp_tag_text

    def __make_color_tag(self, color):
        """
        Creates a pushbutton used as an Icon holder
        Args:
            color: hexadecimal code -> default should be #FFFFFF (white)
        Returns:
            QPushButton, the button used to display the icon
        """
        size = 10
        icon = qtw.QPushButton()
        icon.setFixedSize(qtc.QSize(size, size))
        icon.setStyleSheet('border: 0px;')
        pixmap = qtg.QPixmap(size, size)
        pixmap.fill(qtc.Qt.transparent)
        painter = qtg.QPainter(pixmap)
        painter.setRenderHints(qtg.QPainter.Antialiasing, True)
        painter.setBrush(qtg.QColor(color))
        painter.setPen(qtg.QColor(color))
        painter.drawEllipse(pixmap.rect())
        painter.end()
        icon.setIcon(qtg.QIcon(pixmap))

        return icon