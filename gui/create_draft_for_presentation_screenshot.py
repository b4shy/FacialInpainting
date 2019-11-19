'''
Sample Module to create the GUI
'''
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from draft import Ui_MainWindow


class App(QMainWindow):
    '''
    GUI Handle
    '''
    def __init__(self):
        self.ui = Ui_MainWindow()
        super().__init__()
        self.ui.setupUi(self)

APP = QApplication([])
FORM = App()
FORM.show()
sys.exit(APP.exec_())
