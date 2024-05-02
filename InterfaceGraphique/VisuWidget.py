import matplotlib
matplotlib.use("Qt5Agg")

import matplotlib.patches
import numpy as np

from matplotlib.backends.backend_qt5agg import (
	FigureCanvasQTAgg,
	NavigationToolbar2QT
)
from matplotlib.figure import Figure

from PyQt5.QtCore import (
	pyqtSignal
)
from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QPushButton
)
from PyQt5.QtGui import (
	QPixmap
)

from solver import index_to_grid


class Visuals(QWidget):

	toggled_threeD = pyqtSignal(bool)

	def __init__(self):
		super().__init__()

		self.cities = []
		self.sat_pos = []
		self.radius = 0
		self.grid = []
		self.show_names = False

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.plot = MapPlot()
		self.toggled_threeD.connect(self.plot.switch_projection)

		toolbar = NavigationToolbar2QT(self.plot)

		layout.addWidget(toolbar)
		layout.addWidget(self.plot)


	def plot2D(self):
		self.plot.axes.clear()

		for i in range(len(self.cities)):
			x, y, z = self.cities[i]
			self.plot.axes.plot(x, y, z, "o", color="blue", alpha=0.6)

		indices_sat_positions = np.where(self.sat_pos[0] > 1-1e-3)[0]\
											if len(self.sat_pos) > 0 else []
		for i in indices_sat_positions:
			y,x = index_to_grid(i, len(self.grid), len(self.grid[0]))
			self.plot.axes.plot(self.grid[y][x][0], self.grid[y][x][1], "*", color="red", markersize=10)
			
			circle = matplotlib.patches.Circle((self.grid[y][x][0], self.grid[y][x][1]), self.radius, color='r', fill=False, linestyle="--", zorder=2)
			self.plot.axes.add_patch(circle)

		self.plot.draw()

	
	def plot3D(self):
		pass


class MapPlot(FigureCanvasQTAgg):

	def __init__(self):
		fig = Figure()
		self.axes = fig.add_subplot(111)
		super().__init__(fig)

	def switch_projection(self, threeD):
		self.figure.delaxes(self.axes)
		if threeD:
			self.axes = self.figure.add_subplot(111, projection="3d")
		else:
			self.axes = self.figure.add_subplot(111)

		self.draw()