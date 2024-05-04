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
import add_func
from scipy.optimize import minimize
import visu_plot as visu

def euclidean_satellites_repartition(N_satellites, file, grid_size=10000, radius_acceptable_km=100, verbose=False):
    """
    Calcule sur le plan Euclidien la répartition des satellites optimale pour obtenir une couverture de villes maximale.

    Arguments:
    ---------
    N_satellites: nombre de satellites à répartir
    file: chemin vers le fichier .csv à traiter
    grid_size: nombre de points du grid
    radius_acceptable_km: rayon d'intensité acceptable en km
    verbose: outil de débogage
    
    Returns:
    --------
    satellites_coordinates: coordonnées des satellites placés
    covered_population: population couverte
    """
    data = pd.read_csv(file)
    cities_weights = data["size"].to_numpy()
    cities_coordinates = data[["lat", "long"]].to_numpy()
    
    # Pre-processing
    grid = pre.calc_grid_2d(grid_size, cities_coordinates)
    radius_acceptable_deg = radius_acceptable_km/113
    matrix_adj = pre.calc_adj(cities_coordinates, grid, radius_acceptable_deg)
    if verbose:
        print("Pre-processing terminé")

    # Solve problem
    problem = models.basemodel(N_satellites, grid_size, cities_weights, matrix_adj)
    problem.solve(verbose=True, warm_start=True)
    if verbose:
        print("Problème résolu")

    vars = problem.variables()
    for k in range(2):
        if vars[k].name() == "x":
            save_x = vars[k].value
        elif vars[k].name() == "y":
            save_y = (vars[k].value)

    covered_population = problem.value
    covered_population_relative = covered_population / np.sum(cities_weights)
    if verbose:
        print("Covered population:", covered_population_relative)

    ids_sat = np.array(np.where(save_x > 0.9))[0]
    if 0 in ids_sat:
        ids_sat = ids_sat[1:]
    # if verbose:
    #     print("ID Satellites:", ids_sat)

    ids_villes = np.array(np.where(save_y > 0.9))[0]
    # if verbose:
    #     print("ID Villes couvertes:", ids_villes)

    satellites_coordinates = np.array([grid[i] for i in ids_sat])
    if verbose:
        print("Coords Satellites:\n", satellites_coordinates)

    return satellites_coordinates, covered_population


if __name__ == "__main__":
    N_satellites = 10

    # file = "../test.csv"
    # file = "../refactored_smol.csv"
    file = "../exemple_data_sphere.csv"
    # file = "../Afrique_10k.csv"
    
    # zone = (lat_min, lat_max, long_min, long_max)
    ZI = [(0,50,105,150),(30,55,10,100)]

    t0 = time.perf_counter()
    satellites_coordinates, covered_population = euclidean_satellites_repartition(N_satellites, file, 
                                                                                # grid_size=1000,
                                                                                  verbose=True,
                                                                                  radius_acceptable_km=1500
                                                                                  )
    print("Time to solve:", time.perf_counter() - t0)   
