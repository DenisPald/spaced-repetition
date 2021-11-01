from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from .box_page import BoxPage
from app import session, Card

class Box(QWidget):
    def __init__(self, name: str, box_page: BoxPage, stacked_widget):
        super().__init__()
        uic.loadUi("ui/box.ui", self)
        self.name_label.setText(name)
        self.box_page = box_page
        self.stacked_widget = stacked_widget
        self.open_page_button.clicked.connect(self.open_box_page)

    def open_box_page(self):
        self.stacked_widget.setCurrentWidget(self.box_page)
