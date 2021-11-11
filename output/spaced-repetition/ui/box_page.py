from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from .card import CardWidget
from .box_page_style import BoxPageUi

class BoxPage(QWidget, BoxPageUi):
    def __init__(self, cards: list[CardWidget], parent):
        super().__init__()
        self.setupUi(self)
        for i, cur_card_db in enumerate(cards):
            self.card_layout.addWidget(CardWidget(cur_card_db, parent), i // 3 , i % 3)