from app import Box, Card, session
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from .new_card_style import NewCardUI


class NewCard(QWidget, NewCardUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.create_button.clicked.connect(self.new_card)

    def find_a_box(self):
        box: Box = session.query(Box).filter(Box.repeat_time == self.interval_spin_box.value()).first()
        if not box:
            box = Box('Раз в ' + str(self.interval_spin_box.value()) + ' дней', self.interval_spin_box.value())
            session.add(box)
            session.commit()

        return box

    def new_card(self):
        box = self.find_a_box()
        card = Card(self.question_text.toPlainText(), self.answer_text.toPlainText(), box)
        session.add(card)
        session.commit()
        self.parent.switch_edit_page()


    def update_mode(self, card: Card):
        box = session.query(Box).filter(Box.id == card.id_of_box).first()
        self.label_4.setText('Редактирование карточки.\nОбязательно укажите интервал!')
        self.question_text.setPlaceholderText(card.question)
        self.answer_text.setPlaceholderText(card.answer)
        self.label_3.setText(f'Интервал повтора. Было {box.repeat_time}')
        self.create_button.setText('Сохранить')
        self.create_button.clicked.disconnect(self.new_card)
        self.create_button.clicked.connect(lambda: self.update_card(card))

    def update_card(self, card: Card):
        box = self.find_a_box()
        if self.question_text.toPlainText():
            card.update_question(self.question_text.toPlainText())
        if self.answer_text.toPlainText():
            card.update_answer(self.answer_text.toPlainText())
        card.update_box(box)
        session.commit()
        self.parent.switch_edit_page()
