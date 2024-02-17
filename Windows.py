import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox
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
        self.coords = None
        self.shown_check = False

        self.Find_button.clicked.connect(self.find_address)
        self.Address_input.hide()

        # получение первых данных
        self.get_data('Москва')

    def get_data(self, address, spn_custom_value=None, coords=None, pt=False):
        # получение данных
        data = get_image(address, spn_custom_value, coords, pt)
        if data:
            self.maps_image, self.current_spn, self.coords = data
            self.current_address = address
        else:
            self.mes = Message('Ошибка!', 'Запрошенные данные не получены')
            self.mes.show()

        # запись в файл
        with open('img.png', mode='wb') as img:
            img.write(self.maps_image.content)

        # применение картики из файла к label-виджету
        self.Map.setPixmap(QPixmap('img.png'))

        # стирание файла
        os.remove('img.png')

    # обработка кликов
    def keyPressEvent(self, event):
        new_current_spn = None
        new_coords = None

        if event.key() == Qt.Key_W:
            x, y = self.coords
            new_coords = [x, y + 0.05]

        if event.key() == Qt.Key_S:
            x, y = self.coords
            new_coords = [x, y - 0.05]

        if event.key() == Qt.Key_End or event.key() == Qt.Key_D:
            x, y = self.coords
            new_coords = [x + 0.05, y]

        if event.key() == Qt.Key_Home or event.key() == Qt.Key_A:
            x, y = self.coords
            new_coords = [x - 0.05, y]

        if event.key() == Qt.Key_PageUp:
            new_current_spn = [(x - 0.05) for x in self.current_spn]
        if event.key() == Qt.Key_PageDown:
            new_current_spn = [(x + 0.05) for x in self.current_spn]

        # проверка ограничений
        if new_current_spn:
            if 0 < new_current_spn[0] < 90 and 0 < new_current_spn[1] < 90:
                self.current_spn = new_current_spn
                self.get_data(self.current_address, self.current_spn)

        # проверка ограничений
        if new_coords:
            if 36.6 < new_coords[0] < 38.2 and 55.3 < new_coords[1] < 56.5:
                self.coords = new_coords
                self.get_data(self.current_address, self.current_spn, self.coords)

    # поиск
    def find_address(self):
        if self.shown_check:
            self.current_address = self.Address_input.text()
            self.get_data(self.current_address, pt=True)
            self.Address_input.hide()
            self.shown_check = False
        else:
            self.Address_input.show()
            self.shown_check = True


# окно ошибки
class Message(QMessageBox):
    def __init__(self, name, message):
        super().__init__()
        self.setWindowTitle(name)
        self.setText(message)
