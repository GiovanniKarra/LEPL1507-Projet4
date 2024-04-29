import matplotlib
matplotlib.use('Qt5Agg')

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


class Visuals(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.sc = MapPlot()

		self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

		toolbar = NavigationToolbar2QT(self.sc)

		butt = QPushButton("LOOOL")
		butt2 = QPushButton("MDRRR")
		butt.pressed.connect(self.sc.plot2D)
		butt2.pressed.connect(self.sc.plot3D)

		layout.addWidget(toolbar)
		layout.addWidget(self.sc)
		layout.addWidget(butt)
		layout.addWidget(butt2)

	def plot2D(self, cities, sat_pos, radius, grid, index_to_grid):
		self.sc.plot2D(cities, sat_pos, radius, grid, index_to_grid)


class MapPlot(FigureCanvasQTAgg):

	def __init__(self):
		fig = Figure()
		self.axes = fig.add_subplot(111)
		super().__init__(fig)


	def plot2D(self, cities, sat_pos, radius, grid, index_to_grid):
		self.axes.clear()

		for y in range(len(grid)):
			for x in range(len(grid[0])):
				self.axes.plot(grid[y][x][0], grid[y][x][1], "o", color="black", alpha=0.3)


		for i in range(len(cities)):
			self.axes.plot(cities[i][0], cities[i][1], "o", color="blue", alpha=0.6)

		print(sat_pos)
		indices_sat_positions = np.where(sat_pos[0] > 1-1e-3)[0]
		print("Positions satellites (id grid) :", indices_sat_positions)
		for i in indices_sat_positions:
			y,x = index_to_grid(i, len(grid), len(grid[0]))
			self.axes.plot(grid[y][x][0], grid[y][x][1], "*", color="red", markersize=10)
			# circle = self.axes.Circle((grid[y][x][0], grid[y][x][1]), radius, color='r', fill=False, linestyle="--", zorder=2)
			# self.axes.gca().add_patch(circle)

		self.draw()

	def plot3D(self):
		print("plot 3D")
		# self.axes.clear()
		self.axes.plot([0,1,2,3,4], [10,10,20,10,40])
		self.draw()