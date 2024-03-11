import cvxpy as cp
import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt

from coverage_visualisation import visualise_coverage_2D

def opti(matrix, R, nbr_sat):
    couverture = []
    for i in range(nbr_sat):
        cv = cp.Variable(len(matrix), boolean=True)
        couverture.append(cv)

    sat_lat = cp.Variable(nbr_sat)
    sat_long = cp.Variable(nbr_sat)

    weight = matrix[:,0]
    lat = matrix[:,1]
    long = matrix[:,2]
    constraints = [sat_lat >= 0, sat_lat <= 90, sat_long >= 0, sat_long <= 180]

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
            constraints += [ (cp.power(delta_lat,2) + cp.power(delta_lon,2)) * 111.13**2 - R**2 <= (1-couverture[j][i]) * 10**6]

        objective = cp.sum(couverture[j]*weight)
    
    problem = cp.Problem(cp.Maximize(objective), constraints) 
    start_time = time.time()
    solution = problem.solve(solver="SCIP")
    end_time = time.time()

    print("Time to solve:", end_time - start_time)
    print("Solution:", solution)
    print("poinds:", np.sum(weight))
    print("percentage:", solution/np.sum(weight))
    print("couverture:", [couverture[i].value for i in range(nbr_sat)])
    print("sat_lat:", sat_lat.value)
    print("sat_long:", sat_long.value)

    visualise_coverage_2D([("", elem[2], elem[1]) for elem in matrix], np.array([sat_long.value, sat_lat.value, [1000]*nbr_sat]).T, (R**2+1000**2)*1000**2*4*3.14159, show_names=False)
    return


if __name__ == "__main__":
    df = pd.read_csv("geonames_be_smol.csv",delimiter=";")
    # df = pd.read_csv("geonames_be.csv",delimiter=";")
    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    df.drop(columns=["Coordinates","Name","Country name EN","Elevation"],inplace=True)

    mat = df.to_numpy()
    print(mat)

    rayon = 10
    sat = 1

    opti(mat,rayon,sat)
