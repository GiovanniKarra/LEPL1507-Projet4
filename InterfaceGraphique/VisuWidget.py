from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QLabel
)
from PyQt5.QtGui import (
	QPixmap
)


class Visuals(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)

		image = QLabel()
		image.setPixmap(QPixmap("images/ComplAnal.png").scaledToWidth(self.width()))

		layout.addWidget(image)
		