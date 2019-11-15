from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from draft import Ui_MainWindow
import sys


class App(QMainWindow):
    def __init__(self):
        self.ui = Ui_MainWindow()
        super().__init__()
        self.ui.setupUi(self)

app = QApplication([])
form = App()
form.show()
sys.exit(app.exec_())