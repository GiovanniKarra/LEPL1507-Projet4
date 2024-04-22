from PyQt5.QtWidgets import (
	QHBoxLayout,
	QWidget,
)

from VisuWidget import Visuals
from ControlWidget import Controls


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
