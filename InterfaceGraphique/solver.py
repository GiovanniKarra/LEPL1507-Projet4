import sys
sys.path.insert(1, "../final")

import pandas as pd
import numpy as np

import pre_processing
from spherical_satellites_repartition import spherical_satellites_repartition


def solve(filename, N_sat, radius, grid_size):
	h = 1.2
	radius_acceptable = np.sqrt((radius/6371)**2+(h-1)**2)
	sat_pos, sol = spherical_satellites_repartition(N_sat, filename,
								  grid_size=grid_size, radius_acceptable=radius_acceptable,
								  verbose=True)
	
	return sat_pos, sol

# def solve(filename, N_sat, radius, grid_size):
# 	grid_size_X, grid_size_Y = grid_size

# 	cities, grid = pre_processing.calc_grid(filename, grid_size_X, grid_size_Y)
# 	N_cities = len(cities)
# 	N_grid = len(grid) * len(grid[0])

# 	population = [cities[i][2] for i in range(len(cities))]

# 	covered_adj = pre_processing.calc_adj(cities=cities, grid=grid, radius=radius)

# 	problem = basemodel(N_sat, N_cities, N_grid, population, covered_adj)

# 	problem.solve(warm_start=True)

# 	vars = problem.variables()

# 	sat_pos = [0, 0]

# 	for k in range(2):
# 		if vars[k].name() == "x":
# 			sat_pos[0] = vars[k].value
# 		elif vars[k].name() == "y":
# 			sat_pos[1] = vars[k].value

# 	return cities, sat_pos, grid


# def solve3D(N_satellites, cities_coordinates, cities_weights, grid_size, radius, h=1.2):
# 	cities = coord_to_xyz(cities_coordinates)
	
# 	grid = pre_processing.calc_grid_3d(grid_size, h)

# 	matrix_adj = pre_processing.calc_adj(cities, grid, radius)

# 	problem = models.basemodel(N_satellites, grid_size, cities_weights, matrix_adj)
# 	problem.solve(warm_start=True)

# 	vars = problem.variables()
# 	for k in range(2):
# 		if vars[k].name() == "x":
# 			save_x = vars[k].value
# 		elif vars[k].name() == "y":
# 			save_y = (vars[k].value)

# 	covered_population = problem.value
# 	# covered_population_relative = covered_population / np.sum(cities_weights)

# 	ids_sat = np.array(np.where(save_x > 0.9))[0]

# 	# ids_villes = np.array(np.where(save_y > 0.9))[0]

# 	satellites_coordinates = np.array([grid[i] for i in ids_sat])

# 	return satellites_coordinates, covered_population


def get_cities(filename):
	data : pd.DataFrame = pd.read_csv(filename)
	cities = [None for _ in range(len(data))]

	for i in range(len(data)):
		y = float(data["lat"][i])
		x = float(data["long"][i])
		weight = float(data["size"][i])
		name = data["villeID"][i]

		cities[i] = (y, x, weight, name)

	return cities


def index_to_grid(i, x, y):
	return pre_processing.index_to_grid(i, x, y)


def xyz_to_coord(x, y, z):
	lat = np.rad2deg(np.arctan2(z, np.sqrt(x**2+y**2)))
	long = np.rad2deg(np.sign(y)*np.arccos(x/np.sqrt(x**2+y**2)))

	return lat, long


def coord_to_xyz(coord):
    n = len(coord)
    cities = np.zeros((n, 3))
    for i in range(n):
        lat = coord[i][0]
        lon = coord[i][1]
        x = np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
        y = np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))
        z = np.sin(np.deg2rad(lat))
        cities[i] = [x, y, z]
    return cities