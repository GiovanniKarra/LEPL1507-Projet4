import sys
sys.path.insert(1, "../opti")

import pandas as pd

import pre_processing
from basemodel import basemodel


def solve(filename, N_sat, radius, grid_size):
	grid_size_X, grid_size_Y = grid_size

	cities, grid = pre_processing.calc_grid(filename, grid_size_X, grid_size_Y)
	N_cities = len(cities)
	N_grid = len(grid) * len(grid[0])

	population = [cities[i][2] for i in range(len(cities))]

	covered_adj = pre_processing.calc_adj(cities=cities, grid=grid, radius=radius)  

	problem = basemodel(N_sat, N_cities, N_grid, population, covered_adj)
	
	problem.solve(warm_start=True)

	vars = problem.variables()

	sat_pos = [0, 0]

	for k in range(2):
		if vars[k].name() == "x":
			sat_pos[0] = vars[k].value
		elif vars[k].name() == "y":
			sat_pos[1] = vars[k].value

	return cities, sat_pos, grid


def get_cities(filename):
	data : pd.DataFrame = pd.read_csv(filename, sep=";")
	cities = [tuple() for i in range(len(data))]

	for i in range(len(data)):
		y, x = tuple(map(float, data["Coordinates"][i].split(",")))
		weight = float(data["Population"][i])
		name = data["Name"][i]

		cities[i] = (x, y, weight, name)
	
	return cities


def index_to_grid(i, x, y):
	return pre_processing.index_to_grid(i, x, y)