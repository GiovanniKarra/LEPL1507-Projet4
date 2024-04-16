from PyQt5.QtWidgets import QApplication
import sys

from main_window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()