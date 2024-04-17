from PyQt5.QtCore import (
	Qt,
	QSize
)
from PyQt5.QtWidgets import (
	QHBoxLayout,
	QVBoxLayout,
	QLayout,
	QPushButton,
	QLabel,
	QWidget
)
from PyQt5.QtGui import (
	QPixmap
)


class WorkMenu(QWidget):
	def __init__(self, mainwindow):
		super().__init__()

		layout = QHBoxLayout()
		self.setLayout(layout)

		left_widget = Controls()
		right_widget = Visuals()

		left_widget.setFixedWidth(mainwindow.size().width()//2)
		right_widget.setFixedWidth(mainwindow.size().width()//2)

		layout.addWidget(left_widget)
		layout.addWidget(right_widget)


class Controls(QWidget):
	def __init__(self):
		super().__init__()
		
		layout = QVBoxLayout()
		self.setLayout(layout)

		layout.addWidget(b := QPushButton("OMG"))

		b.setFixedWidth(200)


class Visuals(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)

		image = QLabel()
		image.setPixmap(QPixmap("images/ComplAnal.png").scaledToWidth(self.width()))

		layout.addWidget(image)
		
		