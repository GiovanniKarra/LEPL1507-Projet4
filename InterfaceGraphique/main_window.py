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

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Projet4 - Groupe 5")
		self.setFixedSize(QSize(1280, 720))

		main_menu = QVBoxLayout()

		title = QLabel()
		title.setText("<h1>Optimisateur 1315</h1>")
		title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

		start_button = QPushButton("Start")
		start_button.clicked.connect(self.change_menu)

		quit_button = QPushButton("Quit")
		quit_button.clicked.connect(self.close)

		main_menu.addWidget(title)
		main_menu.addWidget(start_button)
		main_menu.addWidget(quit_button)

		self.second_menu = QVBoxLayout()

		widget = QWidget()
		widget.setLayout(main_menu)
		self.setCentralWidget(widget)

	def change_menu(self):
		new_widget = QWidget()
		new_widget.setLayout(self.second_menu)
		self.setCentralWidget(new_widget)