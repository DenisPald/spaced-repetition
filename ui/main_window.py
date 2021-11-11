import datetime
import json

from app import Box as BoxDB
from app import Card as CardDB
from app import session
from PyQt5.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QSystemTrayIcon

from .box import Box
from .box_page import BoxPage
from .card import Card
from .card_on_main_page import CardOnMainPage, NoneOnMainPage
from .main_style import MainUI
from .new_card import NewCard
from .notification_widget import NotificationWidget


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

        self.home_button.clicked.connect(self.open_home_page)
        self.settings_button.clicked.connect(self.open_settings_page)
        self.edit_button.clicked.connect(self.switch_edit_page)
        self.close_button.clicked.connect(lambda: exit())
        self.tray_button.clicked.connect(lambda: self.hide())
        self.new_card_button.clicked.connect(self.set_new_card_page)
        self.fullscreen = False
        self.fullscreen_button.clicked.connect(self.fullscreen_function)

        self.dragPos = QPoint()

        self.LABEL_HEIGHT = self.app_name_label.height()
        self.StartWidth = 60
        self.EndWidth = 250

        self.timer_for_db = QTimer(self)
        self.timer_for_notification = QTimer(self)
        self.timer_for_db.timeout.connect(self.update_db)
        self.timer_for_notification.timeout.connect(self.check_notification)
        self.timer_for_db.start(3600000)
        self.timer_for_notification.start(60000)

        self.setMouseTracking(True)

        self.update_db()
        self.create_tray()
        self.set_edit_page()
        self.set_home_page()
        self.stacked_widget.setCurrentWidget(self.home_page)

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

        if event.buttons() == Qt.LeftButton and event.pos().y(
        ) <= self.LABEL_HEIGHT and not self.fullscreen:
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
        # Удаление предыдущего edit layout
        for i in reversed(range(self.edit_layout.count())):
            self.edit_layout.itemAt(i).widget().deleteLater()

        boxes = session.query(BoxDB).all()
        for cur_box in boxes:
            cards = session.query(CardDB).filter(
                CardDB.id_of_box == cur_box.id).all()
            box_page = BoxPage(cards, self)
            self.stacked_widget.addWidget(box_page)

            box = Box(cur_box.name, box_page, self.stacked_widget)
            self.edit_layout.addWidget(box)

    def update_db(self):
        # Проверяем не устарели ли даты в коробках. Если дата следующего повтора оказалась в прошлом она обновляется
        boxes = session.query(BoxDB).all()
        for cur_box in boxes:
            if cur_box.next_repetition < datetime.date.today():
                cur_box.update_repetition()
                session.commit()

    def check_notification(self):
        # Проверяем не время ли напомнить о карточках
        boxes = session.query(BoxDB).all()
        with open('settings.json') as f:
            time = datetime.datetime.now().time().strftime('%H:%M')
            settings = json.load(f)
            for cur_box in boxes:
                if cur_box.next_repetition == datetime.date.today(
                ) and settings['time'] == time and settings['enabled']:
                    self.flash()
                    break

    def set_home_page(self):
        for i in reversed(range(self.home_page_layout.count())):
            self.home_page_layout.itemAt(i).widget().deleteLater()

        cur_box_list = session.query(BoxDB).filter(
            BoxDB.next_repetition == datetime.date.today()).all()
        flag = False
        for cur_box in cur_box_list:
            cur_card = session.query(CardDB).filter(
                CardDB.id_of_box == cur_box.id).first()
            if cur_card:
                card_on_main_page = CardOnMainPage(cur_card, self)
                flag = True
                break

        if not flag:
            card_on_main_page = NoneOnMainPage()
        self.home_page_layout.addWidget(card_on_main_page)

    def set_new_card_page(self):
        for i in reversed(range(self.new_card_layout.count())):
            self.new_card_layout.itemAt(i).widget().deleteLater()

        self.new_card_widget = NewCard(self)
        self.new_card_layout.addWidget(self.new_card_widget)
        self.stacked_widget.setCurrentWidget(self.new_card_page)

    def open_home_page(self):
        self.set_home_page()
        self.stacked_widget.setCurrentWidget(self.home_page)

    def set_settings_page(self):
        with open('settings.json') as f:
            self.settings = json.load(f)

        self.notification_button.setChecked(self.settings['enabled'])
        time = self.settings['time'].split(':')
        self.time_settings.setTime(
            datetime.time(hour=int(time[0]), minute=int(time[1])))

        self.save_button.clicked.connect(lambda: self.change_json(
            self.notification_button.isChecked(), self.time_settings.time()))

    def open_settings_page(self):
        self.set_settings_page()
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def change_json(self, enabled, time):
        self.settings['enabled'] = enabled
        self.settings['time'] = f'{time.hour()}:{time.minute()}'
        with open('settings.json', 'w') as w:
            json.dump(self.settings, w, ensure_ascii=False, indent=4)
        self.open_home_page()

    def flash(self):
        self.notification = NotificationWidget()
        self.notification.show()
