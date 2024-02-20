import cvxpy as cp
import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt

def opti(matrix, R, nbr_sat):
    couverture = cp.Variable(len(matrix), boolean=True)
    sat_lat = cp.Variable(nbr_sat)
    sat_long = cp.Variable(nbr_sat)

    weight = matrix[:,0]
    lat = matrix[:,1]
    long = matrix[:,2]
    constraints = []

    # distance orthodromique
    for j in range(nbr_sat):
    # Coordonnées sphériques du satellite actuel
        # satellite_coords = np.array([sat_lat[i], sat_long[i]])
        for i in range(len(matrix)):
            # constraints += [111.2*(sat_lat - lat[i]) + 111.2*(sat_long - long[i]) - R <= (1-couverture[i])* 10**15]
            # constraints += [np.arccos(np.sin(np.radians(matrix[i,1])) * np.sin(np.radians(satellite_coords[0])) +
            #                 np.cos(np.radians(matrix[i,1])) * np.cos(np.radians(satellite_coords[0])) *
            #                 np.cos(np.radians(matrix[i,2] - satellite_coords[1]))) * 6371 - R <= (1-couverture[i])* 10**15 ]

            # Calcul de la distance géodésique entre le satellite et le point de référence
            delta_lat = cp.abs(sat_lat[j] - lat[i])
            delta_lon = cp.abs(sat_long[j] - long[i])
            constraints += [cp.sqrt(cp.power(delta_lat,2) + cp.power(delta_lon,2)) * 111.13 - R <= (1-couverture[i])* 10**15 ]

    objective = cp.sum(couverture*weight)
    
    problem = cp.Problem(cp.Maximize(objective), constraints) 
    start_time = time.time()
    solution = problem.solve(solver="ECOS")
    end_time = time.time()

    print("Time to solve:", end_time - start_time)
    print("Solution:", solution)
    print("poinds:", np.sum(weight))
    print("percentage:", solution/np.sum(weight))
    # print("distance:", dist)
    print("couverture:", couverture.value)
    print("sat_lat:", sat_lat.value)
    print("sat_long:", sat_long.value)
    return


if __name__ == "__main__":
    df = pd.read_csv("geonames_be_smol.csv",delimiter=";")
    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    df.drop(columns=["Coordinates","Name","Country name EN","Elevation"],inplace=True)

    mat = df.to_numpy()
    print(mat)

    rayon = 40
    sat = 1

    opti(mat,rayon,sat)
