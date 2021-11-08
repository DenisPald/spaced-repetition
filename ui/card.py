from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from .card_style import CardUI
from app import session, Card as CardDB


class Card(QWidget, CardUI):
    def __init__(self, card: CardDB, parent):
        super().__init__()
        self.setupUi(self)
        self.visible = False
        self.card = card
        self.parent = parent
        self.question_label.setText(card.question)
        self.answer = card.answer
        self.answer_button.clicked.connect(self.show_answer)
        self.delete_button.clicked.connect(self.delete)
        self.edit_button.clicked.connect(self.edit)

    def show_answer(self):
        if not self.visible:
            self.answer_button.setIcon(QIcon())
            self.answer_button.setText(self.answer)
            self.visible = True
        else:
            self.answer_button.setIcon(QIcon('ui/show_card.png'))
            self.answer_button.setText("")
            self.visible = False

    def delete(self):
        session.query(CardDB).filter(CardDB.id == self.card.id).delete()
        session.commit()
        self.parent.switch_edit_page()


    def edit(self):
        self.parent.set_new_card_page()
        self.parent.new_card_widget.update_mode(self.card)