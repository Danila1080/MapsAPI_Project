from PyQt5.QtWidgets import QMainWindow, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        self.setWindowTitle('Карты')