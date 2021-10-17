import sys

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QAction, QStyle, qApp, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)

        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))

        self.toggled = False
        self.toggle_button.clicked.connect(self.open_menu)
        self.animation = QPropertyAnimation(self.left_frame, b"maximumWidth")
        self.animation.setDuration(180)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.home_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home_page))
        self.settings_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page))
        self.edit_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.edit_page))

        self.create_tray()

        self.close_button.clicked.connect(lambda: exit())
        self.tray_button.clicked.connect(lambda: self.hide())

        self.fullscreen = False
        self.fullscreen_button.clicked.connect(self.fullscreen_function)



        self.dragPos = QPoint()

        self.LABEL_HEIGHT = self.app_name_label.height()
        self.StartWidth = 60
        self.EndWidth = 250


    def open_menu(self):
        if not self.toggled:
            self.animation.setStartValue(self.StartWidth)
            self.animation.setEndValue(self.EndWidth)

            self.home_button.setIcon(QIcon())
            self.home_button.setText("Главная")

            self.settings_button.setIcon(QIcon())
            self.settings_button.setText("Настройки пользователя")

            self.edit_button.setIcon(QIcon())
            self.edit_button.setText("Все карточки")

        else:
            self.animation.setStartValue(self.EndWidth)
            self.animation.setEndValue(self.StartWidth)

            self.home_button.setIcon(QIcon("ui/home.png"))
            self.home_button.setText("")

            self.settings_button.setIcon(QIcon("ui/settings.png"))
            self.settings_button.setText("")

            self.edit_button.setIcon(QIcon("ui/editing.png"))
            self.edit_button.setText("")

        self.toggled = not self.toggled
        self.animation.start()

    def fullscreen_function(self):
        if not self.fullscreen:
            self.showMaximized()
            self.fullscreen_button.setIcon(QIcon("ui/fullscreen_exit.png"))
        else:
            self.showNormal()
            self.fullscreen_button.setIcon(QIcon("ui/fullscreen.png"))

        self.fullscreen = not self.fullscreen

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.pos().y() <= self.LABEL_HEIGHT:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.pos().y() <= self.LABEL_HEIGHT:
            self.fullscreen_function()


    def create_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("ui/repeat.svg"))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(lambda: exit())
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
