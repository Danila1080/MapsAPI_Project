import sys

from PyQt5.QtWidgets import QApplication
from Windows import MainWindow


# проверка ошибок
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# зауск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
