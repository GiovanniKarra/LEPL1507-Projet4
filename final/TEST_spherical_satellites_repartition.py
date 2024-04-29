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

    # satellites_coordinates






    weight = cities_weights
    lat = cities_coordinates[:, 0]
    lon = cities_coordinates[:, 1]

    tot_sol = 0
    tot_sat_coords = []
    # R = 0.21 * 6371  # Rayon de couverture des satellites en km
    R = 40

    start_time = time.time()

    # Initialisation aléatoire des coordonnées des satellites
    initial_guess = []
    for pos in satellites_coordinates:
        initial_guess.append(np.arcsin(pos[2]/h))
        initial_guess.append(np.arccos(pos[0]/(np.cos(np.arcsin(pos[2]/h))*h)))

    init_coverage = 0
    for j in range(len(weight)):
        for i in range(len(initial_guess)//2):
            if add_func.distance(initial_guess[2*i], initial_guess[2*i+1], lat[j], lon[j]) <= R:
                init_coverage += weight[j]
                break

    init_sol = init_coverage
        
    bounds = [(-90, 90), (-180, 180)]

    full_data_pd = pd.DataFrame(np.column_stack((cities_weights, lat,lon)), columns=["population", "latitude", "longitude"])
    full_data = full_data_pd.to_numpy()
    print(full_data)

    for i in range(N_satellites):
        # pass
        print("#"*20)
        print("Satellite", i+1)
        print("#"*20)

        add_func.callback_function.iteration = 0  # Initialisation du compteur d'itérations
        add_func.callback_function.time = time.time()  # Initialisation du compteur de temps
        
        # Optimisation
        result = initial_guess[2*i:2*(i+1)]

        zone = pd.DataFrame(full_data, columns=["population", "latitude", "longitude"])
        # zone = zone[zone["latitude"].between(result[0]-delta_grid_lat-R*(1/113)*(50/100),result[0]+delta_grid_lat+R*(1/113)*(50/100))]
        zone = zone[zone["latitude"].between(result[0]-R*(1/113)*(50/100),result[0]+R*(1/113)*(50/100))]
        # zone = zone[zone["longitude"].between(result[1]-delta_grid_long-R*(1/113)*(50/100),result[1]+delta_grid_long+R*(1/113)*(50/100))]
        zone = zone[zone["longitude"].between(result[1]-R*(1/113)*(50/100),result[1]+R*(1/113)*(50/100))]
        zone = zone.to_numpy()

        result = minimize(add_func.objective_function, initial_guess[2*i:2*(i+1)], args=(zone, R)
                          , bounds=bounds
                          , callback=add_func.callback_function
                        #   , method="L-BFGS-B"
                        #   , options={'reshape': True}
                    )
        
        tot_sat_coords.append(result.x)

        for i in range(len(full_data)):
            if add_func.distance(result.x[0], result.x[1], full_data[i][1], full_data[i][2]) <= R:
                full_data[i][0] = 0

    # Calcul de la couverture pour tous les satellites
    final_coverage = 0
    for j in range(len(weight)):
        for i in range(N_satellites):
            if add_func.distance(tot_sat_coords[i][0], tot_sat_coords[i][1], lat[j], lon[j]) <= R:
                final_coverage += weight[j]
                break
    tot_sol = final_coverage

    print("Time to solve:", time.time() - start_time)
    print("Solution:", tot_sol)
    print("Total population:", np.sum(cities_weights))
    print("Coverage percentage:", 100*tot_sol / np.sum(cities_weights), "%")
    print("initial solution:", 100*init_sol / np.sum(cities_weights), "%")

    visu.visualise_coverage_3D(cities_coordinates, satellites_coordinates, radius_acceptable, use_cartesian=True, covered_ids=ids_villes)
    
    return satellites_coordinates, covered_population



N_satellites = 5
# cities_coordinates = [(1,0,0), (0,1,0), (0,0,1), (-1,0,0)]
# cities_weights = [1, 2, 3, 4]

file = "../geonames_smol.csv"


cities_coordinates, cities_weights = pre.get_cities_old(file)

print(cities_coordinates)


satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, cities_coordinates, cities_weights)
print(satellites_coordinates)


