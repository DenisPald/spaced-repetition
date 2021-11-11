from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from .notification_widget_style import NotificationWidgetUI


class NotificationWidget(QWidget, NotificationWidgetUI):
    def __init__(self, parent=None):
        super(NotificationWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint) | Qt.WindowStaysOnTopHint)
        self.move(1505, 815)
        self.pushButton.clicked.connect(self.hide)
