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


def spherical_satellites_repartition(N_satellites, file, grid_size=10000, h=1.2, radius_acceptable=0.200614975211322, verbose=False, visualise=False, zone=None):
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

    data = pd.read_csv(file)
    cities_weights = data["size"].to_numpy()
    cities_coordinates = data[["lat", "long"]].to_numpy()

    cities_xyz = add_func.cities_latlon_to_xyz(cities_coordinates)

    t0 = time.perf_counter()

    # Pre-processing
    grid = pre.calc_grid_3d(grid_size, h)
	
    # Check if 'zone iterdite' is not None
    if zone is not None: # zone = (lat_min, lat_max, long_min, long_max)
        for i in range(len(zone)):
            new_grid = []
            lat_min = zone[i][0] 
            lat_max = zone[i][1] 
            lon_min = zone[i][2] 
            lon_max = zone[i][3] 
            
            for i in range(1,len(grid)):
                # temp = pre.from_XYZ_to_lat_long(grid[i])
                temp = (np.rad2deg(np.arctan2(grid[i][2], np.sqrt(grid[i][0]**2 + grid[i][1]**2))), np.rad2deg(np.sign(grid[i][1])*np.arccos(grid[i][0]/(np.sqrt(grid[i][0]**2 + grid[i][1]**2)))))
                if lat_min > temp[0] or lat_max < temp[0] or lon_min > temp[1] or lon_max < temp[1]:
                    new_grid.append(grid[i]) 
            grid = np.array(new_grid)
	    
    matrix_adj = pre.calc_adj(cities_xyz, grid, radius_acceptable)
    if verbose:
        print("Pre-processing terminé")

    # Solve problem
    problem = models.basemodel(N_satellites, grid_size, cities_weights, matrix_adj)
    problem.solve(verbose=verbose, warm_start=True)
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
    # if verbose:
    #     print("Coords Satellites:\n", satellites_coordinates)

    weight = cities_weights
    lat = cities_coordinates[:, 0]
    lon = cities_coordinates[:, 1]

    tot_sol = 0
    tot_sat_coords = []
    R = np.sqrt(radius_acceptable**2 - (h-1)**2)*6371  # Rayon de couverture des satellites en km
    if verbose:
        print("Rayon du satellite:", R)

    start_time = time.time()
    
    # Initialisation aléatoire des coordonnées des satellites
    initial_guess = []
    for pos in satellites_coordinates:
        initial_guess.append(np.rad2deg(np.arctan2(pos[2], np.sqrt(pos[0]**2 + pos[1]**2))))
        initial_guess.append(np.rad2deg(np.sign(pos[1])*np.arccos(pos[0]/(np.sqrt(pos[0]**2 + pos[1]**2)))))

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

    for i in range(len(initial_guess)//2):
        if verbose:
            print("#"*20)
            print("Satellite", i+1)
            print("#"*20)

        add_func.callback_function.iteration = 0  # Initialisation du compteur d'itérations
        add_func.callback_function.time = time.time()  # Initialisation du compteur de temps
        
        result = initial_guess[2*i:2*(i+1)]

        # Sélection des villes dans la zone de couverture du satellite
        zone_know = pd.DataFrame(full_data, columns=["population", "latitude", "longitude"])
        if grid_size <= 10000:
            zone_know = zone_know[zone_know["latitude"].between(result[0]-(4999/99-(grid_size*49/9900))*R/113,result[0]+ (4999/99-(grid_size*49/9900))*R/113)]
            zone_know = zone_know[zone_know["longitude"].between(result[1]-(4999/99-(grid_size*49/9900))*R/113,result[1]+ (4999/99-(grid_size*49/9900))*R/113)]
        else:
            zone_know = zone_know[zone_know["latitude"].between(result[0]-R/113,result[0]+R/113)]
            zone_know = zone_know[zone_know["longitude"].between(result[1]-R/113,result[1]+R/113)] 
        zone_know = zone_know.to_numpy()

        # Optimisation de la position du satellite
        if verbose:
            result = minimize(add_func.objective_function, initial_guess[2*i:2*(i+1)], args=(zone_know, R)
                            , bounds=bounds
                            , callback=add_func.callback_function
                    )
        else:
            result = minimize(add_func.objective_function, initial_guess[2*i:2*(i+1)], args=(zone_know, R)
                            , bounds=bounds
                    )
        
        tot_sat_coords.append(result.x)

        for i in range(len(full_data)):
            if add_func.distance(result.x[0], result.x[1], full_data[i][1], full_data[i][2]) <= R:
                full_data[i][0] = 0

    # Calcul de la couverture pour tous les satellites
    final_coverage = 0
    id_covered = []
    for j in range(len(weight)):
        for i in range(len(initial_guess)//2):
            if add_func.distance(tot_sat_coords[i][0], tot_sat_coords[i][1], lat[j], lon[j]) <= R:
                final_coverage += weight[j]
                id_covered.append(j)
                break
    tot_sol = final_coverage

    tot_sat_coordsf = [l.tolist() for l in tot_sat_coords]

    if verbose:
        print("Time to solve:", time.time() - start_time)
        print("Solution:", tot_sol)
        print("Total population:", np.sum(cities_weights))
        print("Coverage percentage:", 100*tot_sol / np.sum(cities_weights), "%")
        print("initial solution:", 100*init_sol / np.sum(cities_weights), "%")
        print("Position:", tot_sat_coordsf)

    if visualise:
        visu.plannar_2D_visu(cities_coordinates,tot_sat_coordsf,id_covered,zone=zone)
    
    return tot_sat_coordsf, tot_sol, problem.value


if __name__ == "__main__":
    N_satellites = 200

    file = "../test.csv"
    file = "../refactored_smol.csv"
    # file = "../exemple_data_sphere.csv"
    # file = "../Afrique_10k.csv"
    
    # zone = (lat_min, lat_max, long_min, long_max)
    ZI = [(0,50,105,150),(0,55,10,100)]

    t0 = time.perf_counter()
    satellites_coordinates, covered_population = spherical_satellites_repartition(N_satellites, file, 
                                                                                #   grid_size=10000,
                                                                                  verbose=True,
                                                                                  visualise=True,
                                                                                #   zone=ZI,
                                                                                  )
    print("Time to solve:", time.perf_counter() - t0)   
