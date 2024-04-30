import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt
import geopy.distance as dst

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

def cities_latlon_to_xyz(cities_coordinates_latlon):
    n = len(cities_coordinates_latlon)
    cities = np.zeros((n, 3))
    for i in range(n):
        lat = cities_coordinates_latlon[i][0]
        lon = cities_coordinates_latlon[i][1]
        x = math.cos(np.deg2rad(lat)) * math.cos(np.deg2rad(lon))
        y = math.cos(np.deg2rad(lat)) * math.sin(np.deg2rad(lon))
        z = math.sin(np.deg2rad(lat))
        cities[i] = [x, y, z]
    return cities