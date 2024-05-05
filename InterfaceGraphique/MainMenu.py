from PyQt5.QtCore import (
	Qt,
	pyqtSignal
)
from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QLabel,
	QPushButton
)
from PyQt5.QtGui import (
	QMovie,
	QPixmap
)


class MainMenu(QWidget):
	start = pyqtSignal()
	quit = pyqtSignal()

	def __init__(self):
		super().__init__()
		
		title = QLabel()
		title.setText("<h1>Optimisateur d'emplacements de satellites</h1>")
		title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

		image_widget = QLabel()
		# gif = QMovie("images/NewtonRaphson.gif")
		# image_widget.setMovie(gif)
		# gif.start()

		image_widget.setPixmap(QPixmap("images/sat.png"))
		# image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

		start_button = QPushButton("Start")
		# start_button.setFixedWidth(100)
		start_button.clicked.connect(self.start)

		quit_button = QPushButton("Quit")
		# quit_button.setFixedWidth(100)
		quit_button.clicked.connect(self.quit)

		layout = QVBoxLayout()
		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.setLayout(layout)

		layout.addWidget(title)
		layout.addWidget(image_widget)
		layout.addWidget(start_button)
		layout.addWidget(quit_button)