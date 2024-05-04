from PyQt5.QtWidgets import QApplication, QStyleFactory
import sys
import os

from MainWindow import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()