from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)

        self.toggled = False
        self.toggle_button.clicked.connect(self.open_menu)
        self.animation = QPropertyAnimation(self.left_frame, b"maximumWidth")
        self.animation.setDuration(180)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.home_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home_page))
        self.settings_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page))
        self.edit_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.edit_page))

    def open_menu(self):
        if not self.toggled:
            self.animation.setStartValue(60)
            self.animation.setEndValue(250)

            self.home_button.setIcon(QIcon())
            self.home_button.setText("Главная")

            self.settings_button.setIcon(QIcon())
            self.settings_button.setText("Настройки пользователя")

            self.edit_button.setIcon(QIcon())
            self.edit_button.setText("Все карточки")

        else:
            self.animation.setStartValue(250)
            self.animation.setEndValue(60)

            self.home_button.setIcon(QIcon("ui/home.png"))
            self.home_button.setText("")

            self.settings_button.setIcon(QIcon("ui/settings.png"))
            self.settings_button.setText("")

            self.edit_button.setIcon(QIcon("ui/editing.png"))
            self.edit_button.setText("")

        self.toggled = not self.toggled
        self.animation.start()