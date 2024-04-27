import sys
sys.path.insert(1, "../opti/")

from PyQt5.QtWidgets import (
	QHBoxLayout,
	QWidget,
	QDialog
)

from VisuWidget import Visuals
from ControlWidget import Controls


class WorkMenu(QWidget):
	def __init__(self, mainwindow):
		super().__init__()

		self.file = ""

		layout = QHBoxLayout()
		self.setLayout(layout)

		left_widget = Controls()
		right_widget = Visuals()

		left_widget.setFixedWidth(mainwindow.size().width()//2)
		right_widget.setFixedWidth(mainwindow.size().width()//2)

		layout.addWidget(left_widget)
		layout.addWidget(right_widget)

		left_widget.file_selected.connect(self.file_selected)


	def file_selected(self, filename):
		print(filename)
		self.file = filename
