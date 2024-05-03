import sys
sys.path.insert(1, "../final")

import pandas as pd
import numpy as np

import pre_processing
import models


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


def solve3D(N_satellites, cities_coordinates, cities_weights, grid_size, radius, h=1.2):
	grid = pre_processing.calc_grid_3d(grid_size, h)

	matrix_adj = pre_processing.calc_adj(cities_coordinates, grid, radius)

	problem = models.basemodel(N_satellites, grid_size, cities_weights, matrix_adj)
	problem.solve(warm_start=True)

	vars = problem.variables()
	for k in range(2):
		if vars[k].name() == "x":
			save_x = vars[k].value
		elif vars[k].name() == "y":
			save_y = (vars[k].value)

	covered_population = problem.value
	# covered_population_relative = covered_population / np.sum(cities_weights)

	ids_sat = np.array(np.where(save_x > 0.9))[0]

	# ids_villes = np.array(np.where(save_y > 0.9))[0]

	satellites_coordinates = np.array([grid[i] for i in ids_sat])

	return satellites_coordinates, covered_population


def get_cities(filename):
	data : pd.DataFrame = pd.read_csv(filename)
	cities = [None for _ in range(len(data))]

	for i in range(len(data)):
		y = float(data["lat"][i])
		x = float(data["long"][i])
		weight = float(data["size"][i])
		name = data["villeID"][i]

		cities[i] = (x, y, weight, name)

	return cities


def index_to_grid(i, x, y):
	return pre_processing.index_to_grid(i, x, y)