import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from scipy.optimize import minimize
import geopy.distance as dst
from pre_processing_3d import get_cities_old, calc_grid_3d

from coverage_visualisation import visualise_coverage_2D

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
    
    weight = matrix[:, 0]
    lat = matrix[:, 1]
    lon = matrix[:, 2]

    tot_sol = 0
    tot_sat_coords = []

    start_time = time.time()

    # Initialisation aléatoire des coordonnées des satellites
    initial_guess = []
    for pos in init:
        col,row = index_to_grid(pos,len(grid),len(grid[0]))
        position = grid[col][row]
        initial_guess.append(position[1])
        initial_guess.append(position[0])

    # initial_guess = [-28.65517241, -114.4137931, -28.65517241, 29.37931034, 23.06896552, 115.65517241, 40.31034483, -104.82758621, 61.0 , -56.89655172]
    # nbr_sat = 5

    init_coverage = 0
    for j in range(len(weight)):
        for i in range(len(initial_guess)//2):
            if distance(initial_guess[2*i], initial_guess[2*i+1], lat[j], lon[j]) <= R:
                init_coverage += weight[j]
                break

    init_sol = init_coverage

    delta_grid_lat = (grid[-1][-1][1] - grid[0][0][1])/ len(grid)
    delta_grid_long = (grid[-1][-1][0] - grid[0][0][0]) / len(grid[0])  
        
    bounds = [(-90, 90), (-180, 180)]

    full_data = np.copy(matrix)

    for i in range(nbr_sat):
        # pass
        print("#"*20)
        print("Satellite", i+1)
        print("#"*20)

        callback_function.iteration = 0  # Initialisation du compteur d'itérations
        callback_function.time = time.time()  # Initialisation du compteur de temps
        
        # Optimisation
        result = initial_guess[2*i:2*(i+1)]

        zone = pd.DataFrame(full_data, columns=["population", "latitude", "longitude"])
        # zone = zone[zone["latitude"].between(result[0]-delta_grid_lat-R*(1/113)*(50/100),result[0]+delta_grid_lat+R*(1/113)*(50/100))]
        zone = zone[zone["latitude"].between(result[0]-delta_grid_lat-R*(1/113)*(50/100),result[0]+delta_grid_lat+R*(1/113)*(50/100))]
        # zone = zone[zone["longitude"].between(result[1]-delta_grid_long-R*(1/113)*(50/100),result[1]+delta_grid_long+R*(1/113)*(50/100))]
        zone = zone[zone["longitude"].between(result[1]-delta_grid_long-R*(1/113)*(50/100),result[1]+delta_grid_long+R*(1/113)*(50/100))]
        zone = zone.to_numpy()

        result = minimize(objective_function, initial_guess[2*i:2*(i+1)], args=(zone, R)
                          , bounds=bounds
                          , callback=callback_function
                        #   , method="L-BFGS-B"
                        #   , options={'reshape': True}
                    )
        
        tot_sat_coords.append(result.x)

        for i in range(len(full_data)):
            if distance(result.x[0], result.x[1], full_data[i][1], full_data[i][2]) <= R:
                full_data[i][0] = 0

    # Calcul de la couverture pour tous les satellites
    final_coverage = 0
    for j in range(len(weight)):
        for i in range(nbr_sat):
            if distance(tot_sat_coords[i][0], tot_sat_coords[i][1], lat[j], lon[j]) <= R:
                final_coverage += weight[j]
                break
    tot_sol = final_coverage

    print("Time to solve:", time.time() - start_time)
    print("Solution:", tot_sol)
    print("Total population:", np.sum(matrix[:, 0]))
    print("Coverage percentage:", 100*tot_sol / np.sum(matrix[:, 0]), "%")
    print("initial solution:", 100*init_sol / np.sum(matrix[:, 0]), "%")
    print("Satellite coordinates:", tot_sat_coords)


    tot_sat_long = [elem[1] for elem in tot_sat_coords]
    tot_sat_lat = [elem[0] for elem in tot_sat_coords]

    visualise_coverage_2D([("", elem[2], elem[1]) for elem in matrix], np.array([tot_sat_long, tot_sat_lat, [1000]*len(tot_sat_long)]).T, [R]*nbr_sat, show_names=False)
    return



if __name__ == "__main__":
    # name = "geonames_be_smol.csv"
    name = "geonames_be.csv"
    # name = "geonames_be_summarized.csv"
    # name = "geonames_smol.csv"
    # name = "geonames_cleared.csv"
    
    name = "../"+name
    df = pd.read_csv(name,delimiter=";")
    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    df.drop(columns=["Coordinates","Name","Country name EN","Elevation"],inplace=True)

    mat = df.to_numpy()

    rayon = 40

    # init = [11, 12, 13, 16, 17, 18]
    # cities, grid = calc_grid(name, 5, 5)
    
    # init = [44, 53, 56, 62, 64, 65]
    # cities, grid = calc_grid(name, 10, 10)
    
    # init = [112, 125, 130, 138, 156, 158]
    # cities, grid = calc_grid(name, 15, 15)
    
    init = [190, 227, 234, 264, 269, 272]
    cities, grid = calc_grid(name, 20, 20)


    opti(mat,rayon, init,grid)