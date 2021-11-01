from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

class Card(QWidget):
    def __init__(self, question: str, answer: str):
        super().__init__()
        uic.loadUi("ui/card.ui", self)
        self.visible = False
        self.question_label.setText(question)
        self.answer = answer
        self.answer_button.clicked.connect(self.set_answer)

    def set_answer(self):
        if not self.visible:
            self.answer_button.setIcon(QIcon())
            self.answer_button.setText(self.answer)
            self.visible = True
        else:
            self.answer_button.setIcon(QIcon('ui/show_card.png'))
            self.answer_button.setText("")
            self.visible = False