import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from chatbot_anamenu import Ui_AnaMenuWindow
from chatbot import Ui_MainWindow
from main import MainWindow

class AnaMenuWindow(QMainWindow, Ui_AnaMenuWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # Arkaplan resmi ayarlama
        self.background_label = QLabel(self)
        self.set_background_image("anamenu_background1.png")

        # Buton olayları
        self.pushButton.clicked.connect(self.open_chatbot)

    def set_background_image(self, image_path):
        # QLabel ile arka plan resmi ayarla
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setScaledContents(True)  # Resmi tam oturt
        self.background_label.lower()  # Arka planı diğer bileşenlerin arkasına gönder

    def resizeEvent(self, event):
        # Pencere boyutlandırıldığında arka plan resmini güncelle
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def open_chatbot(self):
        # ChatBot penceresini açacak işlemler
        self.chatbot_window = QMainWindow()
        self.chatbot_ui = Ui_MainWindow()
        self.chatbot_ui.setupUi(self.chatbot_window)
        self.chatbot_window.show()

        self.chatbot_window = QMainWindow()
        self.chatbot_ui = MainWindow()
        self.chatbot_ui.setupUi(self.chatbot_window)
        self.chatbot_window.show()

def main():
    app = QApplication(sys.argv)
    main_window = AnaMenuWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()