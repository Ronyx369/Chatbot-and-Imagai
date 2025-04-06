import sys
import openai
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QMessageBox
from dalle import Ui_Dialog

class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.generate_images)
        self.ui.pushButton_2.clicked.connect(self.save_image)
        self.ui.pushButton_3.clicked.connect(self.set_next_prompt)
        self.image = None  # Görüntüyü saklamak için bir değişken

        # Önceden belirlenmiş cümleler
        self.prompts = [
            "A sunlit indoor lounge area with a pool containing a flamingo",
            "A white Siamese cat",
            "A serene mountain landscape at sunrise.",
            "A misty forest with a hidden waterfall.",
            "A beautiful sunset over a calm beach.",
            "A group of playful dolphins in the ocean.",
            "A majestic eagle soaring above the mountains.",
            "A family of elephants walking through the savannah.",
            "A futuristic cityscape with flying cars.",
            "A magical forest with glowing plants and creatures.",
            "A medieval castle on a hill surrounded by a moat."

        ]
        self.current_prompt_index = -1  # Şu anki cümle indeksini saklar, başlangıçta -1 olacak

    def generate_images(self):
        prompt = self.ui.lineEdit.text()
        image_urls = self.get_images_from_api(prompt)
        if image_urls:
            images = [self.load_image_from_url(url) for url in image_urls]
            if images:
                self.image = images[0]  # İlk görüntüyü sakla
                self.display_images(images)

    def get_images_from_api(self, prompt):
        openai.api_key = 'API KEY'  # OpenAI API anahtarınızı buraya ekleyin
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Bir adet resim istiyoruz
            size="1024x1024"
        )

        if response and 'data' in response:
            image_urls = [data['url'] for data in response['data']]
            return image_urls
        else:
            print(f"Error: {response}")
            return None

    def load_image_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            image = QImage()
            image.loadFromData(response.content)
            return image
        else:
            print(f"Error loading image: {response.status_code}")
            return None

    def display_images(self, images):
        scene = QGraphicsScene()
        x_offset = 0
        for image in images:
            if image:
                pixmap = QPixmap.fromImage(image)
                scene.addPixmap(pixmap).setOffset(x_offset, 0)
                x_offset += pixmap.width() + 10  # Resimleri yan yana koymak için aralık ekleyin
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def save_image(self):
        if self.image:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)")
            if file_path:
                self.image.save(file_path)
        else:
            QMessageBox.warning(self, "Uyarı", "İndirilecek bir resim bulunamadı.")

    def set_next_prompt(self):
        # Eski cümleyi temizle
        self.ui.lineEdit.clear()
        # Sıradaki cümleyi lineEdit'e yaz
        self.current_prompt_index = (self.current_prompt_index + 1) % len(self.prompts)
        self.ui.lineEdit.setText(self.prompts[self.current_prompt_index])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = MyDialog()
    Dialog.show()
    sys.exit(app.exec_())
