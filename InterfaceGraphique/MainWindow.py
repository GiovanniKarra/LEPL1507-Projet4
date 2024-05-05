from PyQt5.QtCore import (
	QSize
)
from PyQt5.QtWidgets import (
	QMainWindow,
	QFileDialog,
	QMenuBar,
	QDialog,
	QLabel,
	QVBoxLayout,
	QPushButton
)
from PyQt5.QtGui import (
	QPixmap,
	QMovie
)

from MainMenu import MainMenu
from WorkMenu import WorkMenu


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Projet4 - Groupe 5")
		self.setFixedSize(QSize(1280, 720))

		mainmenu = MainMenu()
		mainmenu.start.connect(self.goto_work)
		mainmenu.quit.connect(self.close)

		menubar = QMenuBar()

		file_menu = menubar.addMenu("File")
		file_menu.addAction("create 'cities' file", self.create_cities)
		file_menu.addAction("create 'forbidden zones' file", self.create_zones)
		file_menu.addAction("quit", self.close)

		menubar.addAction("Help", self.show_tuto)

		about_menu = menubar.addMenu("About")

		about_menu.addAction("1315", self.show_1315)
		about_menu.addAction("Newton-Raphson", self.show_nf)

		self.setCentralWidget(mainmenu)
		self.setMenuBar(menubar)

	def goto_work(self):
		self.setCentralWidget(WorkMenu())


	def create_csv_file(self, header):
		diag = QFileDialog()

		path, _ = diag.getSaveFileName(filter="'Comma Separated Values' files (*.csv)")

		if len(path) == 0: return

		if path[-4:] != ".csv":
			path += ".csv"

		with open(path, "w") as f:
			f.write(header)

	
	def create_cities(self):
		self.create_csv_file("villeID,size,lat,long")


	def create_zones(self):
		self.create_csv_file("lat_min,lat_max,long_min,long_max")


	def show_tuto(self):
		diag = QDialog()
		diag.setLayout(QVBoxLayout())

		image = QPixmap("images/Tuto.png").scaled(1025, 633)

		label = QLabel()
		label.setPixmap(image)

		ok_button = QPushButton("OK")
		ok_button.pressed.connect(diag.close)

		diag.layout().addWidget(label)
		diag.layout().addWidget(ok_button)

		diag.exec()


	def show_nf(self):
		diag = QDialog()
		diag.setLayout(QVBoxLayout())

		gif = QMovie("images/NewtonRaphson.gif")

		label = QLabel()
		label.setMovie(gif)
		gif.start()

		ok_button = QPushButton("OK")
		ok_button.pressed.connect(diag.close)

		diag.layout().addWidget(label)
		diag.layout().addWidget(ok_button)

		diag.exec()


	def show_1315(self):
		diag = QDialog()
		diag.setLayout(QVBoxLayout())

		image = QPixmap("images/ComplAnal.png")

		label = QLabel()
		label.setPixmap(image)

		ok_button = QPushButton("OK")
		ok_button.pressed.connect(diag.close)

		diag.layout().addWidget(label)
		diag.layout().addWidget(ok_button)

		diag.exec()