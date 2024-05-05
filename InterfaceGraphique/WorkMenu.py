import sys
sys.path.insert(1, "../opti/")

from PyQt5.QtWidgets import (
	QHBoxLayout,
	QWidget,
	QMessageBox,
	QLabel
)
from PyQt5.QtCore import (
	pyqtSignal
)

from VisuWidget import Visuals
from ControlWidget import Controls
from solver import solve, get_cities
from utils import popup_error


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
		try:
			self.file = filename

			self.right_widget.cities = get_cities(filename)
			self.right_widget.sat_pos = []
			self.right_widget.grid = []
			self.right_widget.show_names = show_names

			if self.right_widget.threeD: self.right_widget.plot3D()
			else: self.right_widget.plot2D()
		except FileNotFoundError:
			pass
		except Exception as e:
			popup_error("File not compatible: %s"%filename, e)


	def solve(self, N_sat, threeD, radius, grid_size, zones_file, visu=False):
		try:
			self.right_widget.radius = radius

			satellites, covered = solve(self.file, N_sat, radius, grid_size, zones_file, visu)

			self.right_widget.sat_pos = satellites
		except Exception as e:
			popup_error("Solver error", e)

		try:
			if threeD: self.right_widget.plot3D()
			else: self.right_widget.plot2D()
		except Exception as e:
			popup_error("plotting error", e)
		
		popup_error(f"Covered population: {covered*100:.2f}%")