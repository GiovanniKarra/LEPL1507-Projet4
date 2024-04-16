from PyQt5.QtCore import (
	Qt
)
from PyQt5.QtWidgets import (
	QVBoxLayout,
	QLabel,
	QPushButton
)
from PyQt5.QtGui import (
	QMovie
)


class MainMenu(QVBoxLayout):
	def __init__(self, mainwindow):
		super().__init__()
		title = QLabel()
		title.setText("<h1>Optimisateur 1315</h1>")
		title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

		image_widget = QLabel()
		gif = QMovie("images/NewtonRaphson.gif")
		image_widget.setMovie(gif)
		gif.start()
		image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

		start_button = QPushButton("Start")
		start_button.clicked.connect(mainwindow.goto_work)

		quit_button = QPushButton("Quit")
		quit_button.clicked.connect(mainwindow.close)

		self.addWidget(title)
		self.addWidget(image_widget)
		self.addWidget(start_button)
		self.addWidget(quit_button)