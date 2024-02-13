import cvxpy as cp
import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt

def opti(matrix, R, nbr_sat):
    couverture = cp.Variable(len(matrix), nonneg=True)
    sat_lat = cp.Variable(nbr_sat)
    sat_long = cp.Variable(nbr_sat)

    weight = matrix[:,0]
    lat = matrix[:,1]
    long = matrix[:,2]
    dist = np.ones(len(matrix))

    objective = cp.sum(couverture*weight)
    constraints = [dist - R <= (1-couverture)* 10**8]

    problem = cp.Problem(cp.Maximize(objective), constraints) 
    start_time = time.time()
    solution = problem.solve(solver=cp.SCIPY, scipy_options={"method": "highs"})
    end_time = time.time()

    print("Time to solve:", end_time - start_time)
    print("Solution:", solution)
    print("poinds:", np.sum(weight))
    print("percentage:", solution/np.sum(weight))
    return


if __name__ == "__main__":
    df = pd.read_csv("geonames_be_smol.csv",delimiter=";")
    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    df.drop(columns=["Coordinates","Name","Country name EN","Elevation"],inplace=True)

    mat = df.to_numpy()
    print(mat)

    rayon = 1
    sat = 1

    opti(mat,rayon,sat)
