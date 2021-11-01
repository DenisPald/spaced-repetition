from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class Card(QWidget):
    def __init__(self, question, answer):
        super().__init__()
        uic.loadUi("ui/card.ui", self)
        self.question_layout.setText(question)
        self.answer_layout.setText(answer)
