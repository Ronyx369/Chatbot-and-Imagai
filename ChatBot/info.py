from PyQt5.QtWidgets import QMainWindow
from chatbot_info import Ui_Info

class InfoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(InfoWindow, self).__init__(parent)
        self.ui = Ui_Info()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())