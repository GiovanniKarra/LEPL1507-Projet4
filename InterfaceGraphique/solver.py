import sys
sys.path.insert(1, "../final")

import pandas as pd
import numpy as np

import pre_processing
from spherical_satellites_repartition import spherical_satellites_repartition


def solve(filename, N_sat, radius, grid_size, zones_file, visu=False):
	h = 1.2
	radius_acceptable = np.sqrt((radius/6371)**2+(h-1)**2)
	sat_pos, sol = spherical_satellites_repartition(N_sat, filename,
								  grid_size=grid_size, radius_acceptable=radius_acceptable,
								  verbose=True, visualise=visu, zone=get_zones(zones_file))
	
	return sat_pos, sol


def get_zones(filename):
	try:
		data = pd.read_csv(filename)
		N = len(data)

		ret = list(data.itertuples(index=False, name=None))

		return ret
	except:
		return []


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