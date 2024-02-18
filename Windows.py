import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QLineEdit
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

        # объявление переменных
        self.current_spn = None
        self.current_address = None
        self.maps_image = None
        self.coords = None
        self.mes = Message('Ошибка!', 'Запрошенные данные не получены')

        self.Find_button.clicked.connect(self.find_address)

        # получение первых данных
        self.get_data('Москва', set_pt=True)

    def get_data(self, address, spn_custom_value=None, coords=None, set_pt=False):
        # получение данных
        data = get_image(address, spn_custom_value, coords, set_pt)
        if data:
            self.maps_image, self.current_spn, self.coords = data
            self.current_address = address
        else:
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

        if event.key() == Qt.Key_Up:
            x, y = self.coords
            new_coords = [x, y + 0.05]

        if event.key() == Qt.Key_Down:
            x, y = self.coords
            new_coords = [x, y - 0.05]

        if event.key() == Qt.Key_End or event.key() == Qt.Key_Right:
            x, y = self.coords
            new_coords = [x + 0.05, y]

        if event.key() == Qt.Key_Home or event.key() == Qt.Key_Left:
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
                self.get_data(self.current_address, self.current_spn, self.coords)

        # проверка ограничений
        if new_coords:
            # if 36.6 < new_coords[0] < 38.2 and 55.3 < new_coords[1] < 56.5:
            self.coords = new_coords
            self.get_data(self.current_address, self.current_spn, self.coords)

    # Убирает фокус со строки ввода кликом мыши
    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()

    # поиск
    def find_address(self):
        # Убирает фокус со строки ввода, позволяет адекватно перемещать карту
        self.Address_input.clearFocus()
        self.Find_button.clearFocus()

        self.current_address = self.Address_input.text()
        self.get_data(self.current_address, set_pt=True)


# окно ошибки
class Message(QMessageBox):
    def __init__(self, name, message):
        super().__init__()
        self.setWindowTitle(name)
        self.setText(message)
