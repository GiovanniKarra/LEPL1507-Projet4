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
from solver import solve, get_cities


class WorkMenu(QWidget):
	def __init__(self):
		super().__init__()

		self.file = ""

		layout = QHBoxLayout()
		self.setLayout(layout)

		left_widget = Controls()
		self.right_widget = Visuals()

		# left_widget.setFixedWidth(self.size().width())
		# self.right_widget.setFixedWidth(self.size().width())

		left_widget.solve.connect(self.solve)
		left_widget.set_names.connect(lambda x: self.file_selected(self.file, bool(x)))

		layout.addWidget(left_widget)
		layout.addWidget(self.right_widget)

		left_widget.file_selected.connect(self.file_selected)


	def file_selected(self, filename, show_names=False):
		self.file = filename

		self.right_widget.cities = get_cities(filename)
		self.right_widget.sat_pos = []
		self.right_widget.grid = []
		self.right_widget.show_names = show_names

		self.right_widget.plot2D()


	def solve(self, N_sat, threeD, radius):
		cities, satellites, grid = solve(self.file, N_sat, 1, (30, 30))

		self.right_widget.sat_pos = satellites
		self.right_widget.grid = grid
		self.right_widget.radius = radius

		self.right_widget.plot2D()