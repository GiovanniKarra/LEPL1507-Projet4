import sys
sys.path.insert(1, "../opti/")

from PyQt5.QtWidgets import (
	QHBoxLayout,
	QWidget,
	QDialog
)
from PyQt5.QtCore import (
	pyqtSignal
)

from VisuWidget import Visuals
from ControlWidget import Controls
from solver import solve


class WorkMenu(QWidget):
	def __init__(self):
		super().__init__()

		self.file = ""

		layout = QHBoxLayout()
		self.setLayout(layout)

		left_widget = Controls()
		self.right_widget = Visuals()

		left_widget.setFixedWidth(self.size().width())
		self.right_widget.setFixedWidth(self.size().width())

		left_widget.solve.connect(self.solve)

		layout.addWidget(left_widget)
		layout.addWidget(self.right_widget)

		left_widget.file_selected.connect(self.file_selected)


	def file_selected(self, filename):
		self.file = filename

	def solve(self, N_sat, threeD):
		cities, satellites, grid, index_to_grid = solve(self.file, N_sat, 1, (30, 30))

		self.right_widget.plot2D(cities, satellites, 1, grid, index_to_grid)


