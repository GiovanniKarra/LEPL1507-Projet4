import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits import mplot3d
from scipy.spatial import distance

import math
import time 
import numba as nb


def get_cities_old(file: str) -> np.ndarray:
    data : pd.DataFrame = pd.read_csv(file, sep=";")
    cities = np.empty(len(data), dtype=tuple)

    for i in range(len(cities)):
        coor = data["Coordinates"][i].split(",")
        y  = float(coor[0])
        x = float(coor[1])
        weight =  float(data["Population"][i])

        cities[i] = (x, y, weight)

    return cities



# def distance_carre(P1, P2, h):
#     return (P1[0] ** 2 - P2[0] ** 2) +(P1[1] ** 2 - P2[1] ** 2) + (P1[2] ** 2 - P2[2] ** 2)  - h ** 2

def calc_grid_3d(grid_size_X = 10, grid_size_Y = 10, h = 1.2,  R = 0.4):
    M = grid_size_Y
    N = grid_size_X
    R_carre = R * R

    grid = np.zeros((M*N, 3))
    Msat = np.empty((M - 1)* (N - 1), dtype=tuple)
    Mreg = np.empty((M - 1)* (N  - 1), dtype=set)

    for m in range(M):
        for n in range(N):
            sat = [h * np.sin(np.pi * m/M)*np.cos(2*np.pi* n/N), h * np.sin(np.pi * m/M)*np.sin(2*np.pi* n/N),  h * np.cos(np.pi * m/M)]
            grid[m*N+n,:] = sat


    for m in range(M - 1):
        for n in range(N - 1):
            Mreg[m * (M - 1) + n] = (grid[m * M + n], grid[m * M + n + 1], grid[(m + 1) * M + n], grid[(m + 1) * M + n + 1])
            Msat[m * (M - 1) + n] = set()


    for m in range(M):
        for n in range(N):

            for m_reg in range(M - 1):
                for n_reg in range(N - 1):

                    full_cover = 1
                    is_neighbor = False

                    for i in range(4):
                        if distance.euclidean(grid[m * M + n], 1/h * Mreg[m_reg * (M - 1) + n_reg][i])**2 <= R_carre:
                            is_neighbor = True
                        else:
                            full_cover = 0

                    if is_neighbor:
                        # Msat[m_reg * (M - 1) + n_reg].append((grid[m * M + n][0], grid[m * M + n][1], grid[m * M + n][2], full_cover))
                        Msat[m_reg * (M - 1) + n_reg].add((grid[m * M + n][0], grid[m * M + n][1], grid[m * M + n][2], full_cover, m * M + n))
                    

            
    return grid, Mreg, Msat


def calc_adj(file, grid, Mreg, Msat, grid_size_X, radius, h = 1.2):
    data : pd.DataFrame = pd.read_csv(file, sep=";")
    cities = np.empty(len(data), dtype=tuple)
    population = np.empty(len(data), dtype=float)
    matrix_adj = np.empty(len(cities), dtype=list)
    R_carre = radius ** 2

    for i in range(len(data)):
        coor = data["Coordinates"][i].split(",")
        lat = float(coor[0])
        lon = float(coor[1])
        weight =  float(data["Population"][i])
        x = math.cos(lat) * math.cos(lon)
        y = math.cos(lat) * math.sin(lon)
        z = math.sin(lat)
        cities[i] = (x, y, z)
        population[i] = weight

        flag1 = False
        flag2 = False
        index = len(grid) // 2
        Z_temp = grid[index]
        index_prv = index

        while True:
            if z >= Z_temp[2]:
                index_prv = index
                index = index // 2
                Z_temp = grid[index]

                if flag2 == True and flag1 == False:
                    break

                flag1 = True

            if z < Z_temp[2]:
                index_prv = index
                index = (index + len(grid)) // 2
                Z_temp = grid[index]

                if flag1 == True and flag2 == False:
                    break

                flag2 = True
    

        z_reg = (grid_size_X - 1) * (min(index, index_prv) // grid_size_X)
        Reg = z_reg
        min_dist = math.inf

        for region in range(z_reg, z_reg + grid_size_X):    
            center = [(Mreg[region][0][0] + Mreg[region][2][0])/ 2, (Mreg[region][0][1] + Mreg[region][2][1])/ 2, (Mreg[region][0][2] + Mreg[region][2][2])/ 2]
            dist = distance.euclidean(center, cities[i]) 
            if dist < min_dist:
                min_dist = dist
                Reg = region

        matrix_adj[i] = list()

        for sat in Msat[Reg]:
            # if sat[3] == 1: # Full cover 
            #     matrix_adj[i].append(sat[4]) # Satellite number
            # else:
            if distance.euclidean((sat[0], sat[1], sat[2]), cities[i])** 2 - (h - 1)<=  R_carre:
                matrix_adj[i].append(sat[4]) # Satellite number


    return cities, population, matrix_adj




if __name__ == "__main__":




    file = "geonames-all-cities-with-a-population-1000.csv"


    s = time.time()
    print("calc grid")
    grid, Mreg, Msat = calc_grid_3d(grid_size_X=30, grid_size_Y=30, R=0.4)
    print(time.time() - s)
    print("ADJ")
    cities, population, matrix_adj = calc_adj(file, grid, Mreg, Msat, grid_size_X=10, radius=0.4)
    print(time.time() - s)
    e = time.time()

    print(e - s)
    # for i in range(len(matrix_adj)):
    #     print(matrix_adj[i])

    