import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QFont
from finder import get_image


# главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        # инициализация интерфейса
        super().__init__()
        uic.loadUi('templates/main_window.ui', self)
        self.setStyleSheet("background-color: #FFCF48")
        self.Header.setFont(QFont('', 15))

        # получение изображения карты и запись в файл
        self.maps_image = get_image('Москва')
        with open('data/pictures/img.png', mode='wb') as img:
            img.write(self.maps_image.content)

        # применение картики из файла к label-виджету
        self.Map.setPixmap(QPixmap('data/pictures/img.png'))

        os.remove('data/pictures/img.png')
