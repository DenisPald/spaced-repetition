from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from .card import Card

class BoxPage(QWidget):
    def __init__(self, cards: list[Card]):
        super().__init__()
        uic.loadUi("ui/box_page.ui", self)
        for i, cur_card_db in enumerate(cards):
            self.card_layout.addWidget(Card(cur_card_db.question, cur_card_db.answer), i // 3 , i % 3)

