from PyQt5.QtCore import (
	QSize,
	Qt
)
from PyQt5.QtWidgets import (
	QMainWindow,
	QVBoxLayout,
	QLabel,
	QWidget,
	QPushButton
)
from PyQt5.QtGui import (
	QMovie
)

from mainmenu import MainMenu
from work_layout import WorkLayout


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Projet4 - Groupe 5")
		self.setFixedSize(QSize(1280, 720))

		self.set_layout(MainMenu(self))

	def set_layout(self, layout):
		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)

	def goto_work(self):
		self.set_layout(WorkLayout(self))