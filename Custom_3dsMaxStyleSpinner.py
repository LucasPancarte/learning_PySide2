class QSpinner3DS(qtw.QDoubleSpinBox):
    """
    Custom button widget added right-click event, 
    initialize with : size, step
    """
    def __init__(self, size, step=1.0, default_value=0.0, parent=None):
        """
        Initialization
        """
        super(QSpinner3DS, self).__init__(parent)

        self.size = size
        self.step = step
        self.default_value = default_value
        self.mouseStartPosY = 0
        self.startValue = 0
        self.current_value = 0

        self.setMaximumSize(self.size)
        self.setSingleStep(self.step)
        self.setValue(self.default_value)

    def set_value_to_default(self):
        """
        Set value to default (for 3ds Max like behavior) --> used on right-click event
        """
        self.setValue(self.default_value)

    def mousePressEvent(self, event):
        """
        Re-define mousePressEvent to implement right-click/left-click/middle-click
        """ 
        if event.type() == qtc.QEvent.MouseButtonPress:
            if event.button() == qtc.Qt.RightButton:
                self.right_click_event()

            elif event.button() == qtc.Qt.LeftButton:
                self.left_click_event(event)
                self.mouseStartPosY = event.pos().y()
                self.startValue = self.value()

    def mouseMoveEvent(self, event):
        self.setCursor(QtCore.Qt.SizeVerCursor)

        multiplier = 0.01
        valueOffset = ((self.mouseStartPosY - event.pos().y()) * multiplier)
        value = self.startValue + valueOffset

        if value != self.current_value:
            self.current_value = value
            self.setValue(self.current_value)

    def mouseReleaseEvent(self, event):
        super(QSpinner3DS, self).mousePressEvent(event)
        super(QSpinner3DS, self).mouseReleaseEvent(event)
        self.unsetCursor()

    def left_click_event(self, event):
        """
        Left-click event
        :param event: click event
        """
        super(QSpinner3DS, self).mousePressEvent(event)

    def right_click_event(self):
        """
        Right-click event
        """
        self.set_value_to_default()
