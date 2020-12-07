class ProgressBar(qtw.QStatusBar):
    """
    Custom Progress bar
    """
    def __init__(self, vis=False, stat_txt="", format_txt=""):
        super(ProgressBar, self).__init__()

        self.statusLabel = qtw.QLabel(" {0} : ...".format(stat_txt))
        self.statusLabel.setMaximumWidth(70)
        self.progressbar = qtw.QProgressBar()

        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(1)
        self.progressbar.setValue(0)
        self.progressbar.setFormat(" {0} : %v / %m".format(format_txt))

        self.addWidget(self.statusLabel, 1)
        self.addWidget(self.progressbar, 2)

        self.set_visibility(vis)

    def set_label_text(self, text):
        """
        Set status label text in case it need to change
        """
        self.statusLabel.setText(text)

    def update_progress(self, step, max_steps):
        """
        Update progress from a value and a maximum value
        """
        self.progressbar.setMaximum(max_steps)
        self.progressbar.setValue(step)

    def reset_prog_bar(self):
        """
        Reset progress bar value
        """
        self.progressbar.reset()

    def set_visibility(self, value):
        """
        Set progress bar visibility default=False
        """
        self.setVisible(value)