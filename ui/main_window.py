import datetime

from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QAction, QMenu

from .card import Card
from .box import Box
from .box_page import BoxPage
from .card_on_main_page import CardOnMainPage, NoneOnMainPage
from app import session, Session, Box as BoxDB, Card as CardDB
from .main_style import MainUI


class MainWindow(QMainWindow, MainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initDrag()

        self.setWindowFlags(Qt.WindowFlags(Qt.FramelessWindowHint))

        self.toggled = False
        self.toggle_button.clicked.connect(self.open_menu)
        self.animation = QPropertyAnimation(self.left_frame, b"maximumWidth")
        self.animation.setDuration(180)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.home_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        self.settings_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.settings_page))
        self.edit_button.clicked.connect(self.switch_edit_page)
        self.new_card_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.new_card_page))


        self.close_button.clicked.connect(lambda: exit())
        self.tray_button.clicked.connect(lambda: self.hide())

        self.fullscreen = False
        self.fullscreen_button.clicked.connect(self.fullscreen_function)

        self.dragPos = QPoint()

        self.LABEL_HEIGHT = self.app_name_label.height()
        self.StartWidth = 60
        self.EndWidth = 250

        self.setMouseTracking(True)

        self.create_tray()
        self.set_home_page()
        self.stacked_widget.setCurrentWidget(self.home_page)

        self.create_button.clicked.connect(self.new_card)

    def initDrag(self):
        self.bottom_drag = False
        self.right_drag = False
        self.right_rect = [
            x for x in range(self.width() - 5,
                             self.width() + 1)
        ]
        self.bottom_rect = [
            y for y in range(self.height() - 5,
                             self.height() + 1)
        ]

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
        if event.buttons() == Qt.LeftButton and event.pos().y(
        ) in self.bottom_rect:
            self.bottom_drag = True
        if event.buttons() == Qt.LeftButton and event.pos().x(
        ) in self.right_rect:
            self.right_drag = True

    def mouseReleaseEvent(self, event):
        self.right_drag = False
        self.bottom_drag = False
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        if event.pos().y() in self.bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif event.pos().x() in self.right_rect:
            self.setCursor(Qt.SizeHorCursor)

        if event.buttons() == Qt.LeftButton and event.pos().y() <= self.LABEL_HEIGHT and not self.fullscreen:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

        if event.buttons() == Qt.LeftButton and self.bottom_drag:
            self.resize(self.width(), event.pos().y())

        if event.buttons() == Qt.LeftButton and self.right_drag:
            self.resize(event.pos().x(), self.height())

    def mouseDoubleClickEvent(self, event):
        if event.pos().y() <= self.LABEL_HEIGHT:
            self.fullscreen_function()

    def resizeEvent(self, event):
        self.right_rect = [
            x for x in range(self.width() - 10,
                             self.width() + 5)
        ]
        self.bottom_rect = [
            y for y in range(self.height() - 10,
                             self.height() + 5)
        ]

    def switch_edit_page(self):
        self.set_edit_page()
        self.stacked_widget.setCurrentWidget(self.edit_page)

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

    def set_edit_page(self):
        for i in reversed(range(self.edit_layout.count())):
            self.edit_layout.itemAt(i).widget().deleteLater()
        boxes = session.query(BoxDB).all()
        for cur_box in boxes:
            cards = session.query(CardDB).filter(
                CardDB.id_of_box == cur_box.id).all()
            box_page = BoxPage(cards)
            self.stacked_widget.addWidget(box_page)

            box = Box(cur_box.name, box_page, self.stacked_widget)
            self.edit_layout.addWidget(box)

    def set_home_page(self):
        for i in reversed(range(self.home_page_layout.count())):
            self.home_page_layout.itemAt(i).widget().deleteLater()

        cur_box = session.query(BoxDB).filter(
            BoxDB.next_repetition == datetime.date.today()).first()
        if cur_box is not None:
            card_on_main_page = CardOnMainPage(
                session.query(CardDB).filter(
                    CardDB.id_of_box == cur_box.id).first(), self)
        else:
            card_on_main_page = NoneOnMainPage()
        self.home_page_layout.addWidget(card_on_main_page)

    def new_card(self):
        box = session.query(BoxDB.repeat_time == self.interval_spin_box.value()).first()
        if not box[0]:
            box = BoxDB(f'раз в {self.interval_spin_box.value()} дней', self.interval_spin_box.value())
            session.add(box)
            session.commit()
        card = CardDB(self.question_text.toPlainText(), self.answer_text.toPlainText(), box)
        session.add(card)
        session.commit()
        self.switch_edit_page()