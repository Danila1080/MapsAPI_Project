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

    def get_data(self, address, spn_custom_value=None):
        # получение данных
        data = get_image(address, spn_custom_value)
        self.maps_image = data[0]
        self.current_spn = data[1]
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

        if event.key() == Qt.Key_Up or event.key() == Qt.Key_PageUp:
            new_current_spn = [(x - 0.05) for x in self.current_spn]
        if event.key() == Qt.Key_Down or event.key() == Qt.Key_PageDown:
            new_current_spn = [(x + 0.05) for x in self.current_spn]

        # проверка ограничений
        if 0 < new_current_spn[0] < 90 and 0 < new_current_spn[1] < 90:
            self.current_spn = new_current_spn
            self.get_data(self.current_address, self.current_spn)
