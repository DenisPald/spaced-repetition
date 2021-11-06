from app import session
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from app import Card
from app import Box

class RightOrNot(QWidget):
    def __init__(self, card: Card, parent):
        super().__init__()
        uic.loadUi('ui/right_or_not.ui', self)
        self.parent = parent
        self.card = card
        self.right_button.clicked.connect(self.right)
        self.wrong_button.clicked.connect(self.wrong)

    def right(self):
        question = self.card.question
        answer = self.card.answer

        current_box = session.query(Box).filter(Box.id == self.card.id_of_box).first()
        list_of_possible_boxes = session.query(Box).filter(Box.repeat_time > current_box.repeat_time).all()
        if list_of_possible_boxes:
            min_repeat_time_box = list_of_possible_boxes[0]
            for possible_box in list_of_possible_boxes[1:]:
                if possible_box.repeat_time < min_repeat_time_box.repeat_time:
                    min_repeat_time_box = possible_box
            transferred = Card(question, answer, min_repeat_time_box)
            session.add(transferred)

        session.query(Card).filter(Card.id == self.card.id).delete()
        session.commit()

        self.parent.set_home_page()


    def wrong(self):
        pass


class CardOnMainPage(QWidget):
    def __init__(self, card: Card, parent):
        super().__init__()
        uic.loadUi('ui/card_on_main_page.ui', self)
        self.visible = False
        self.card = card
        self.parent = parent
        box = session.query(Box).filter(Box.id == card.id_of_box).first()
        self.box_name_label.setText(f'Коробка {box.name}')
        self.question_label.setText(self.card.question)
        self.answer_button.clicked.connect(self.show_answer)
        self.delete_button.clicked.connect(self.delete_card)


    def show_answer(self):
        if not self.visible:
            self.answer_button.setText(self.card.answer)
            self.answer_layout.addWidget(RightOrNot(self.card, self.parent))
            self.visible = True


    def delete_card(self):
        session.query(Card).filter(Card.id == self.card.id).delete()
        session.commit()
        self.parent.set_home_page()
