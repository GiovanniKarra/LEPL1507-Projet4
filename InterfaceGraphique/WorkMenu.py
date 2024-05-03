import sys
sys.path.insert(1, "../opti/")

from PyQt5.QtWidgets import (
	QHBoxLayout,
	QWidget,
	QDialog,
	QLabel
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
		self.right_widget.setFixedWidth((self.right_widget.width()*3)//2)

		left_widget.solve.connect(self.solve)
		left_widget.set_names.connect(lambda x: self.file_selected(self.file, bool(x)))
		left_widget.toggled_threeD.connect(self.right_widget.toggled_threeD)

		layout.addWidget(left_widget)
		layout.addWidget(self.right_widget)

		left_widget.file_selected.connect(self.file_selected)


	def file_selected(self, filename, show_names=False):
		self.file = filename

		self.right_widget.cities = get_cities(filename)
		self.right_widget.sat_pos = []
		self.right_widget.grid = []
		self.right_widget.show_names = show_names

		if self.right_widget.threeD: self.right_widget.plot3D()
		else: self.right_widget.plot2D()


	def solve(self, N_sat, threeD, radius, grid_size):
		self.right_widget.radius = radius

		cities = get_cities(self.file)
		satellites, covered = solve(self.file, N_sat, radius, grid_size)

		self.right_widget.sat_pos = satellites

		if threeD: self.right_widget.plot3D()
		else: self.right_widget.plot2D()
		return

		cities, satellites, grid = solve(self.file, N_sat, 1, (30, 30))

		self.right_widget.sat_pos = satellites
		self.right_widget.grid = grid

		self.right_widget.plot2D()