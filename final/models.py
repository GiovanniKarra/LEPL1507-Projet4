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

def basemodel(N_sat, N_grid, population, coverage):
    """
    N_sat:      number of satellites to place
    N_grid:     number of grid points (possible satellite positions)
    population: numpy array of size N_cities containing the population of each city
    coverage:   binary numpy array of size N_cities x N_grid containing the coverage of each city by each satellite:
                coverage[i][j] == True if city i is covered by satellite j, 0 otherwise
    """
    N_cities = len(population)
    
    # Variables
    y = cp.Variable(N_cities, name="y", boolean=True) # y[i] = 1 si ville i est couverte par un satellite, 0 sinon
    x = cp.Variable(N_grid, name="x", boolean=True)   # x[j] = 1 si satellite placé à la position j, 0 sinon

    # Objectif
    cout = cp.multiply(population, y) # population couverte (multiplication elementwise)
    objectif = cp.Maximize(cp.sum(cout)) # maximise la norme 1 (somme) des populations couvertes

    # Contraintes
    contraintes = []

    # N satellites
    contraintes.append(cp.sum(x) <= N_sat)
    contraintes.append(1 <= cp.sum(x))
    
    # Couverture
    for i in range(N_cities):
        vec_couverture = np.zeros(N_grid, dtype=bool)
        vec_couverture[coverage[i]] = True
        contraintes.append(y[i] <= cp.sum(cp.multiply(x, vec_couverture)))

    # Solveur problème
    return cp.Problem(objectif, contraintes)