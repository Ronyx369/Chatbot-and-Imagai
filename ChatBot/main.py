import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from chatbot import *
from openai import OpenAI
from info import InfoWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QTextCursor
import requests
from datetime import datetime
import locale  # Gün isminin türkçe olamsı için


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # OpenAI client'ını oluştur
        self.client = OpenAI(api_key="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")

        # Gönder butonuna tıklandığında `send_to_api` fonksiyonunu çağır
        self.button1.clicked.connect(self.send_to_api)

        # Kopyala butonuna tıklandığında `copy_to_clipboard` fonksiyonunu çağır
        self.pushButton.clicked.connect(self.copy_to_clipboard)

        # Temizle butonuna tıklandığında `clear_text_browser` fonksiyonunu çağır
        self.pushButton_2.clicked.connect(self.clear_text_browser)

        # QLineEdit'da Enter tuşuna basıldığında `send_to_api` fonksiyonunu çağır
        self.lineEdit.returnPressed.connect(self.send_to_api)

        self.lineEdit.setPlaceholderText("Yazmak için tıklayınız...")

        self.pushButton_3.clicked.connect(self.open_info_window)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setFixedSize(self.size())  # Pencerenin boyutunu sabitle

        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)  # Pencere stilini MSWindowsFixedSizeDialogHint (Tam Ekran) olarak ayarla

        self.set_background("arkaplan1.png")

        self.pushButton_4.clicked.connect(self.ask_for_city)

        self.update_time_and_date()

        locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.type_text)
        self.typing_index = 0
        self.typing_text = ""

    @staticmethod
    def translate_condition(condition):
        translations = {
            'Clear': 'Açık',
            'Partly cloudy': 'Parçalı bulutlu',
            'Cloudy': 'Bulutlu',
            'Overcast': 'Kapalı',
            'Mist': 'Sisli',
            'Patchy rain possible': 'Yer yer yağmur olası',
            'Patchy snow possible': 'Yer yer kar yağışı olası',
            'Patchy sleet possible': 'Yer yer karla karışık yağmur olası',
            'Patchy freezing drizzle possible': 'Yer yer dondurucu çisenti olası',
            'Moderate or heavy rain with thunder' : 'Orta veya şiddetli yağmur ve gök gürültüsü',
            # Diğer durumlar için İngilizce ifadeleri kullan
        }

        return translations.get(condition, condition)

    def send_to_api(self):
        try:
            # QLineEdit'den metni al
            text = self.lineEdit.text()

            # Anlık saati al
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            if 'hava durumu' in text:
                city = text.split('hava durumu ')[-1].split(' ')[0]  # Şehri al
                temp, condition = self.get_weather(city)  # Hava durumu bilgilerini al
                # Anlık tarihi al
                current_date = now.strftime("%m/%d/%Y")
                response = f'{city} şehrindeki hava durumu ({current_date}): {temp}°C, {condition}'
            else:
                # API'ye gönder
                chat_completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo-0613",
                    messages=[{"role": "user", "content": text}]
                )

                # API'den gelen yanıtı al
                response = chat_completion.choices[0].message.content

            # QTextBrowser'da göster
            self.textBrowser.append(f"<b>Siz:</b> {text}<br>")
            self.typing_text = f"{response}"
            self.typing_index = 0
            self.textBrowser.moveCursor(QTextCursor.End)
            self.textBrowser.insertHtml(f"<b>ChatBot:</b> ")
            self.typing_timer.start(50)  # 50 milisaniye aralıklarla harf yazdır

            # QLineEdit'deki metni sil
            self.lineEdit.clear()
        except Exception as e:
            print(f"Hata: {e}")

    def type_text(self):
        if self.typing_index < len(self.typing_text):
            self.textBrowser.moveCursor(QTextCursor.End)
            self.textBrowser.insertPlainText(self.typing_text[self.typing_index])
            self.typing_index += 1
            self.textBrowser.ensureCursorVisible()
        else:
            self.typing_timer.stop()
            self.textBrowser.append("")  # Yeni bir satır ekleyerek sonraki metinlerin ayrı satırlarda görünmesini sağla

    def copy_to_clipboard(self):
        # QTextBrowser'dan metni al ve kopyala
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textBrowser.toPlainText())

    def clear_text_browser(self):
        # QTextBrowser'ın içeriğini temizle
        self.textBrowser.clear()

    def open_info_window(self):
        self.info_window = InfoWindow()
        self.info_window.show()

    def set_background(self, filename):
        # QPixmap nesnesi oluştur
        pixmap = QPixmap(filename)

        # Pencerenin paletini al ve arka plan fırçasını ayarla
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))

        # Paleti pencereye uygula
        self.setPalette(palette)

    def get_weather(self, city):
        try:
            response = requests.get(f'http://api.weatherapi.com/v1/current.json?key=18d3fbcff361463bbd995653242205&q={city}')
            response.raise_for_status()  # HTTP durum kodunu kontrol et
        except requests.exceptions.HTTPError as err:
            print(f"HTTP hata oluştu: {err}")
            return None, 'Hava durumu bilgisi alınamadı'
        except requests.exceptions.RequestException as err:
            print(f"Hata oluştu: {err}")
            return None, 'Hava durumu bilgisi alınamadı'

        data = response.json()

        # API'den dönen veriyi kontrol et
        if 'current' in data:
            temp = data['current']['temp_c']
            condition = self.translate_condition(data['current']['condition']['text'])
            return temp, condition
        else:
            return None, 'Hava durumu bilgisi alınamadı'
        
    def ask_for_city(self):
        city, ok = QInputDialog.getText(self, 'Hava Durumu Sorgusu', 'Hava durumunu öğrenmek istediğiniz şehri yazınız:')
        
        if ok:
            temp, condition = self.get_weather(city)
            response = f'{city} şehrindeki hava durumu: {temp}°C, {condition}'
            self.textBrowser.append(f"<b>ChatBot:</b> {response}<br><br>")

    def update_time_and_date(self):
        # Anlık tarih ve saati al
        now = datetime.now()

        # Saati al ve label'a yaz
        current_time = now.strftime("%H:%M:%S")
        self.label.setText(current_time)

        # Gün isimlerini Türkçe'ye çevir
        days = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        day_of_week = days[now.weekday()]

        # Tarihi al ve label_2'ye yaz
        current_date = now.strftime("%d/%m/%Y, ") + day_of_week
        self.label_2.setText(current_date)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
