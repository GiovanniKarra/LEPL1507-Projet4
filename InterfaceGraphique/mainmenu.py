from PyQt5.QtCore import (
	Qt
)
from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QLabel,
	QPushButton
)
from PyQt5.QtGui import (
	QMovie
)


class MainMenu(QWidget):
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

		layout = QVBoxLayout()
		self.setLayout(layout)

		layout.addWidget(title)
		layout.addWidget(image_widget)
		layout.addWidget(start_button)
		layout.addWidget(quit_button)