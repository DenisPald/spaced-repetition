import sys
from PyQt5.QtWidgets import QApplication

from ui import MainWindow
from app import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())