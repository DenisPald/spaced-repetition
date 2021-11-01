from app import session
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from app import Card

class RightOrNot(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/right_or_not.ui', self)

class CardOnMainPage(QWidget):
    def __init__(self, card: Card, parent):
        super().__init__()
        uic.loadUi('ui/card_on_main_page.ui', self)
        self.visible = False
        self.card = card
        self.parent = parent
        self.box_name_label.setText('1')
        self.question_label.setText(self.card.question)
        self.answer_button.clicked.connect(self.show_answer)
        self.delete_button.clicked.connect(self.delete_card)


    def show_answer(self):
        if not self.visible:
            self.answer_button.setText(self.card.answer)
            self.answer_layout.addWidget(RightOrNot())
            self.visible = True


    def delete_card(self):
        session.query(Card).filter(Card.id == self.card.id).delete()
        session.commit()
        self.parent.set_home_page()
