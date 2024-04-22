from PyQt5.QtCore import (
	QSize,
	Qt
)
from PyQt5.QtWidgets import (
	QMainWindow,
)
from PyQt5.QtGui import (
	QMovie
)

from MainMenu import MainMenu
from WorkMenu import WorkMenu


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Projet4 - Groupe 5")
		self.setFixedSize(QSize(1280, 720))

		self.setCentralWidget(MainMenu(self))

	def goto_work(self):
		self.setCentralWidget(WorkMenu(self))