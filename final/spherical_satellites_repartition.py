import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import scipy as sp
import pre_processing as pre
import pandas as pd
from mpl_toolkits import mplot3d
from scipy.spatial import distance
import math
import time 
import models

import coverage_visualisation as visu


def spherical_satellites_repartition(N_satellites, cities_coordinates, cities_weights, grid_size=10000, h=1.2, radius_acceptable=0.21):
    """
    Calcule sur la sphère la répartition des satellites optimale pour obtenir une couverture de population maximale.

    Arguments:
    ---------
    N_satellites:       nombre de satellites à répartir
    cities_coordinates: coordonnées des villes
    cities_weights:     poids de chaque ville
	grid_size:          nombre de points dans le grid (par défaut 1000)
	h:                  hauteur des satellites (par défaut 1.2x le rayon de la Terre)
	radius_acceptable:  rayon autour des satellites à partir duquel l'intensité est jugée acceptable
    
    Returns:
    --------
    satellites_coordinates: coordonnées des satellites placés.
	covered_population: population couverte
    """


    #sqrtn = 3.09 / (2**0.5 * radius) # grid size idéale jsplus


    t0 = time.perf_counter()

    # Pre-processing
    grid = pre.calc_grid_3d(grid_size, h)
    matrix_adj = pre.calc_adj(cities_coordinates, grid, radius_acceptable)
    print("Pre-processing terminé")

    # Solve problem
    problem = models.basemodel(N_satellites, grid_size, cities_weights, matrix_adj)
    problem.solve(verbose=True, warm_start=True)
    print("Problème résolu")

    vars = problem.variables()
    for k in range(2):
        if vars[k].name() == "x":
            save_x = vars[k].value
        elif vars[k].name() == "y":
            save_y = (vars[k].value)

    covered_population = problem.value
    covered_population_relative = covered_population / np.sum(cities_weights)
    print("Covered population:", covered_population_relative)

    ids_sat = np.array(np.where(save_x > 0.9))[0]
    print("ID Satellites:", ids_sat)

    ids_villes = np.array(np.where(save_y > 0.9))[0]
    print("ID Villes couvertes:", ids_villes)

    satellites_coordinates = np.array([grid[i] for i in ids_sat])
    print("Coords Satellites:\n", satellites_coordinates)

    # for i in range(len(satellites_coordinates)):
    #     print("Norme :", np.linalg.norm(satellites_coordinates[i]))

    visu.visualise_coverage_3D(cities_coordinates, satellites_coordinates, radius_acceptable, use_cartesian=True, covered_ids=ids_villes)
    
    return satellites_coordinates, covered_population



N_satellites = 2
# cities_coordinates = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0)]
# cities_weights = [1, 2, 3, 4]

file = "../geonames_smol.csv"


cities_coordinates, cities_weights = pre.get_cities_old(file)

print(cities_coordinates)


satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, cities_coordinates, cities_weights)
print(satellites_coordinates)


