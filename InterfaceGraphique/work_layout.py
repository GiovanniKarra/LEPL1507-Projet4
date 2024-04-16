from PyQt5.QtCore import (
	Qt
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


class WorkLayout(QHBoxLayout):
	def __init__(self, mainwindow):
		super().__init__()

		left_widget = QWidget()
		right_widget = QWidget()

		self.addWidget(left_widget)
		self.addWidget(right_widget)

		controls = Controls(left_widget)
		left_widget.setFixedWidth(mainwindow.size().width()//2)

		visuals = Visuals(right_widget)
		right_widget.setFixedWidth(mainwindow.size().width()//2)
		

class Controls(QVBoxLayout):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.addWidget(QPushButton("OMG"))


class Visuals(QVBoxLayout):
	def __init__(self, parent):
		super().__init__(parent)

		self.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

		image = QLabel()
		image.setPixmap(QPixmap("images/ComplAnal.png").scaledToWidth(parent.width()))

		self.addWidget(image)
		
		