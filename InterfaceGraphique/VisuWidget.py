import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.patches
import numpy as np

from matplotlib.backends.backend_qt5agg import (
	FigureCanvasQTAgg, 
	NavigationToolbar2QT
)
from matplotlib.figure import Figure

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
	def __init__(self):
		super().__init__()

		self.cities = []
		self.sat_pos = []
		self.radius = 0
		self.grid = []
		self.show_names = False

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.sc = MapPlot()

		self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

		toolbar = NavigationToolbar2QT(self.sc)

		layout.addWidget(toolbar)
		layout.addWidget(self.sc)


	def plot2D(self):
		self.sc.axes.clear()

		for y in range(len(self.grid)):
			for x in range(len(self.grid[0])):
				self.sc.axes.plot(self.grid[y][x][0], self.grid[y][x][1], "o", color="black", alpha=0.3)


		for i in range(len(self.cities)):
			self.sc.axes.plot(self.cities[i][0], self.cities[i][1], "o", color="blue", alpha=0.6)
			
			if self.show_names:
				self.sc.axes.text(self.cities[i][0], self.cities[i][1], self.cities[i][3])

		indices_sat_positions = np.where(self.sat_pos[0] > 1-1e-3)[0]\
											if len(self.sat_pos) > 0 else []
		for i in indices_sat_positions:
			y,x = index_to_grid(i, len(self.grid), len(self.grid[0]))
			self.sc.axes.plot(self.grid[y][x][0], self.grid[y][x][1], "*", color="red", markersize=10)
			
			circle = matplotlib.patches.Circle((self.grid[y][x][0], self.grid[y][x][1]), self.radius, color='r', fill=False, linestyle="--", zorder=2)
			self.sc.axes.add_patch(circle)
			# circle = self.axes.Circle((grid[y][x][0], grid[y][x][1]), radius, color='r', fill=False, linestyle="--", zorder=2)
			# self.axes.gca().add_patch(circle)

		self.sc.draw()


class MapPlot(FigureCanvasQTAgg):

	def __init__(self):
		fig = Figure()
		self.axes = fig.add_subplot(111)
		super().__init__(fig)