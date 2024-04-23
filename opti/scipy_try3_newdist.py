import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy.optimize import minimize
import geopy.distance as dst
from pre_processing_3d import get_cities_old, calc_grid_3d

from coverage_visualisation import visualise_coverage_3D

def distance(lat1, lon1, lat2, lon2):
    return dst.distance((lat1, lon1), (lat2, lon2)).km

def objective_function(sat_coords, weights, R):
    # Fonction objectif à maximiser
    total_coverage = 0
    
    poids = np.copy(weights[:, 0])

    for j in range(len(weights)):
        d = dst.distance((sat_coords[0], sat_coords[1]), (weights[j][1], weights[j][2])).km
        total_coverage += poids[j] * (1/(1+np.exp(100*(d-R))))

    return -total_coverage  # On veut maximiser la couverture

def callback_function(xk):
    print("Iteration:", callback_function.iteration)
    print("Current solution:", xk)
    # print("Current objective value:", objective_function(xk))
    print("Time elapsed:", round(time.time() - callback_function.time, 5) , "s")
    print("-------------------------")
    callback_function.iteration += 1

def opti(matrix, R, init,grid):
    nbr_sat = int(len(init))
    
    weight = matrix[1]
    coords = matrix[0]

    tot_sol = 0
    tot_sat_coords = []

    start_time = time.time()

    # init_coverage = 0
    # for j in range(len(weight)):
    #     for i in range(len(initial_guess)//2):
    #         if distance(initial_guess[2*i], initial_guess[2*i+1], lat[j], lon[j]) <= R:
    #             init_coverage += weight[j]
    #             break

    # init_sol = init_coverage

    # delta_grid_lat = (grid[-1][-1][1] - grid[0][0][1])/ len(grid)
    # delta_grid_long = (grid[-1][-1][0] - grid[0][0][0]) / len(grid[0])  
        
    # bounds = [(-90, 90), (-180, 180)]

    full_data = [[coords[:][0], coords[:][1], coords[:][2] ,weight]]
    print(full_data)
    initial_guess = np.ravel(init)

    for i in range(nbr_sat):
        print("#"*20)
        print("Satellite", i+1)
        print("#"*20)

        callback_function.iteration = 0  # Initialisation du compteur d'itérations
        callback_function.time = time.time()  # Initialisation du compteur de temps
        
        # Optimisation
        result = initial_guess[3*i:3*(i+1)]
        print("Initial guess:", result)
        

        zone = pd.DataFrame(full_data, columns=["X", "population"])
        print(zone)
        # # zone = zone[zone["latitude"].between(result[0]-delta_grid_lat-R*(1/113)*(50/100),result[0]+delta_grid_lat+R*(1/113)*(50/100))]
        # zone = zone[zone["latitude"].between(result[0]-delta_grid_lat-R*(1/113)*(50/100),result[0]+delta_grid_lat+R*(1/113)*(50/100))]
        # # zone = zone[zone["longitude"].between(result[1]-delta_grid_long-R*(1/113)*(50/100),result[1]+delta_grid_long+R*(1/113)*(50/100))]
        # zone = zone[zone["longitude"].between(result[1]-delta_grid_long-R*(1/113)*(50/100),result[1]+delta_grid_long+R*(1/113)*(50/100))]
        zone = zone.to_numpy()
        continue
        result = minimize(objective_function, initial_guess[2*i:2*(i+1)], args=(zone, R)
                        #   , bounds=bounds
                          , callback=callback_function
                        #   , method="L-BFGS-B"
                        #   , options={'reshape': True}
                    )
        
        tot_sat_coords.append(result.x)

        for i in range(len(full_data)):
            if distance(result.x[0], result.x[1], full_data[i][1], full_data[i][2]) <= R:
                full_data[i][0] = 0

    # Calcul de la couverture pour tous les satellites
    # final_coverage = 0
    # for j in range(len(weight)):
    #     for i in range(nbr_sat):
    #         if distance(tot_sat_coords[i][0], tot_sat_coords[i][1], lat[j], lon[j]) <= R:
    #             final_coverage += weight[j]
    #             break
    # tot_sol = final_coverage

    print("Time to solve:", time.time() - start_time)
    print("Solution:", tot_sol)
    print("Total population:", np.sum(matrix[1]))
    # print("Coverage percentage:", 100*tot_sol / np.sum(matrix[:, 0]), "%")
    # print("initial solution:", 100*init_sol / np.sum(matrix[:, 0]), "%")
    print("Satellite coordinates:", tot_sat_coords)


    # tot_sat_long = [elem[1] for elem in tot_sat_coords]
    # tot_sat_lat = [elem[0] for elem in tot_sat_coords]

    # visualise_coverage_3D([("", elem[2], elem[1]) for elem in matrix], np.array([tot_sat_long, tot_sat_lat, [1000]*len(tot_sat_long)]).T, [R]*nbr_sat, show_names=False)
    return



if __name__ == "__main__":
    # name = "geonames_be_smol.csv"
    # name = "geonames_be.csv"
    name = "geonames_be_summarized.csv"
    # name = "geonames_smol.csv"
    # name = "geonames_cleared.csv"
    
    name = "../"+name

    # mat = get_cities_old(name)
    # print(mat)

    rayon = 40

    a = [1,0,0]
    b = [0,1,0]
    c = [0,0,1]
    d = [-1,0,0]
    cities_coordinates = [a, b, c, d]
    cities_weights = [1, 2, 3, 4]
    mat = [cities_coordinates, cities_weights]
    
    init = [[ 0.06373773, -0.02327692, 1.19808 ], [-1.19853149, 0.01430091, -0.0576]]
    grid = calc_grid_3d(20, 20)


    opti(mat,rayon, init, grid)