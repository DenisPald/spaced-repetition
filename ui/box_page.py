from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from .card import Card
from .box_page_style import BoxPageUi

class BoxPage(QWidget, BoxPageUi):
    def __init__(self, cards: list[Card], parent):
        super().__init__()
        self.setupUi(self)
        for i, cur_card_db in enumerate(cards):
            self.card_layout.addWidget(Card(cur_card_db, parent), i // 3 , i % 3)