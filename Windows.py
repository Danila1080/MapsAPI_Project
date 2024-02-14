import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from finder import get_image


# главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        # инициализация интерфейса
        super().__init__()
        uic.loadUi('templates/main_window.ui', self)
        self.setStyleSheet("background-color: #FFCF48")
        self.Header.setFont(QFont('', 15))

        # объявление пустых переменных
        self.current_spn = None
        self.current_address = None
        self.maps_image = None

        # получение первых данных
        self.get_data('Москва')

    def get_data(self, address, spn_custom_value=None, coords=None):
        # получение данных
        data = get_image(address, spn_custom_value, coords)
        self.maps_image, self.current_spn, self.coords = data
        self.current_address = address

        # запись в файл
        with open('data/pictures/img.png', mode='wb') as img:
            img.write(self.maps_image.content)

        # применение картики из файла к label-виджету
        self.Map.setPixmap(QPixmap('data/pictures/img.png'))

        # стирание файла
        os.remove('data/pictures/img.png')

    # обработка кликов
    def keyPressEvent(self, event):
        new_current_spn = None
        new_coords = self.coords

        if event.key() == Qt.Key_Up or event.key() == Qt.Key_PageUp:
            x, y = self.coords
            new_coords = [x, y + 0.05]
            print('up')
        if event.key() == Qt.Key_Down or event.key() == Qt.Key_PageDown:
            x, y = self.coords
            new_coords = [x, y - 0.05]
            print('down')
        if event.key() == Qt.Key_End or event.key() == Qt.Key_Right:
            x, y = self.coords
            new_coords = [x + 0.05, y]
            print('right')
        if event.key() == Qt.Key_Home or event.key() == Qt.Key_Left:
            x, y = self.coords
            new_coords = [x - 0.05, y]
            print('left')

        print(new_coords)

        # проверка ограничений
        if 36.6 < new_coords[0] < 38.2 and 55.3 < new_coords[1] < 56.5:
            self.coords = new_coords
            self.get_data(self.current_address, self.current_spn, self.coords)
