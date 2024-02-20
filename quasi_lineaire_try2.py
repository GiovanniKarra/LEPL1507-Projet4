import cvxpy as cp
import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt

from coverage_visualisation import visualise_coverage_2D

def opti(matrix, R, nbr_sat):
    

    weight = matrix[:,0]
    lat = matrix[:,1]
    long = matrix[:,2]

    tot_sol = 0
    tot_sat_lat = np.zeros(nbr_sat)
    tot_sat_long = np.zeros(nbr_sat)
    tot_couverture = []

    start_time = time.time()
    # distance orthodromique
    for j in range(nbr_sat):
        couverture = cp.Variable(len(matrix), boolean=True)

        sat_lat = cp.Variable(1)
        sat_long = cp.Variable(1)
        
        constraints = [sat_lat >= 0, sat_lat <= 90, sat_long >= 0, sat_long <= 180]

        if j > 0:

            weight = weight - np.round(prev_couv) * weight

        # Coordonnées sphériques du satellite actuel
        # satellite_coords = np.array([sat_lat[i], sat_long[i]])
        for i in range(len(matrix)):
            # constraints += [111.2*(sat_lat - lat[i]) + 111.2*(sat_long - long[i]) - R <= (1-couverture[i])* 10**15]
            # constraints += [np.arccos(np.sin(np.radians(matrix[i,1])) * np.sin(np.radians(satellite_coords[0])) +
            #                 np.cos(np.radians(matrix[i,1])) * np.cos(np.radians(satellite_coords[0])) *
            #                 np.cos(np.radians(matrix[i,2] - satellite_coords[1]))) * 6371 - R <= (1-couverture[i])* 10**15 ]

            # Calcul de la distance géodésique entre le satellite et le point de référence
            delta_lat = cp.abs(sat_lat[0] - lat[i])
            delta_lon = cp.abs(sat_long[0] - long[i])
            constraints += [ (cp.power(delta_lat,2) + cp.power(delta_lon,2)) * 111.13**2 - R**2 <= (1-couverture[i]) * 10**6]

        objective = cp.sum(couverture*weight)
        problem = cp.Problem(cp.Maximize(objective), constraints) 
        solution = problem.solve(solver="SCIP")
        tot_sol += solution
        tot_sat_lat[j] = sat_lat[0].value  
        tot_sat_long[j] = sat_long[0].value
        tot_couverture.append(couverture.value)
        prev_couv = couverture.value
        print("sat")

    end_time = time.time()

    print("Time to solve:", end_time - start_time)
    print("Solution:", tot_sol)
    print("Total:", np.sum(matrix[:,0]))
    print("percentage:", tot_sol/np.sum(matrix[:,0]))
    print("couverture:", tot_couverture)
    print("sat_lat:", tot_sat_lat)
    print("sat_long:", tot_sat_long)

    visualise_coverage_2D([("", elem[2], elem[1]) for elem in matrix], np.array([tot_sat_long, tot_sat_lat, [1000]*nbr_sat]).T, (R**2+1000**2)*1000**2*4*3.14159, 1, show_names=False)
    return


if __name__ == "__main__":
    # df = pd.read_csv("geonames_be_smol.csv",delimiter=";")
    df = pd.read_csv("geonames_be.csv",delimiter=";")
    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    df.drop(columns=["Coordinates","Name","Country name EN","Elevation"],inplace=True)

    mat = df.to_numpy()
    print(mat)

    rayon = 100
    sat = 3

    opti(mat,rayon,sat)