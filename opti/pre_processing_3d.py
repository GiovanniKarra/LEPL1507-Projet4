import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.spatial import distance
import math
import time 


# TODO: fonction lat/lon <-> (x,y,z)
#       calc_grid_3d optimisé si possibl
#       calc_ajd_3d + optimiser


# basé sur la formule envoyée sur messenger 
def calc_grid_3d(file: str, grid_size_X = 10, grid_size_Y = 10, grid_size_Z = 10) -> np.ndarray:
    data : pd.DataFrame = pd.read_csv(file, sep=";")
    M = grid_size_Y
    N = grid_size_X

    grid = []

    for m in range(M):
        for n in range(N):
            grid.append(np.sin(np.pi * m/M)*np.cos(2*np.pi* n/N), np.sin(np.pi * m/M)*np.sin(2*np.pi* n/N), np.cos(np.pi * m/M))

    return grid



def calc_grid(file: str, grid_size_X = 10, grid_size_Y = 10) -> np.ndarray:
    data : pd.DataFrame = pd.read_csv(file, sep=";")
    cities = np.empty(len(data), dtype=tuple)

    maxX, maxY = -math.inf, -math.inf
    minX, minY = math.inf, math.inf

    for i in range(len(cities)):
        coor = data["Coordinates"][i].split(",")
        y  = float(coor[0])
        x = float(coor[1])
        weight =  float(data["Population"][i])

        maxX = max(maxX, x)
        maxY = max(maxY, y)
        minX = min(minX, x)
        minY = min(minY, y)

        cities[i] = (x, y, weight)

    grid = np.empty(grid_size_Y * grid_size_X, dtype=tuple).reshape(grid_size_Y, grid_size_X)

    x = np.linspace(np.floor(minX), np.ceil(maxX), grid_size_X)
    y = np.linspace(np.floor(minY), np.ceil(maxY), grid_size_Y)
    print(minX, minY, maxX, maxY)
    
    for i in enumerate(x):
        for j in enumerate(y):
            grid[j[0]][i[0]] = tuple((x[i[0]], y[j[0]]))

    return cities, grid


def get_min_max(data: pd.DataFrame):

    maxX, maxY = -math.inf, -math.inf
    minX, minY = math.inf, math.inf
    
    for i in range(len(data)):
        coor = data["Coordinates"][i].split(",")
        y = float(coor[0])
        x = float(coor[1])

        maxX = max(maxX, x)
        maxY = max(maxY, y)
        minX = min(minX, x)
        minY = min(minY, y)

    return minX, minY, maxX, maxY


def grid_avg(data: pd.DataFrame, grid_size_X = 300, grid_size_Y = 300):
    matrix = np.zeros((grid_size_X, grid_size_Y))
    mx, my, MX, MY = get_min_max(data)

    x = np.linspace(np.floor(mx), np.ceil(MX), grid_size_X)
    y = np.linspace(np.floor(my), np.ceil(MY), grid_size_Y)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    for i, c in enumerate(data["Coordinates"]):
        P = c.split(",")
        matrix[int((float(P[1]) - mx) // dx), int((float(P[0]) - my) // dy)] += float(data["Population"][i])

    return matrix

def calc_adj(cities, grid: np.ndarray, radius: float):
    matrix_adj = np.empty(len(cities), dtype=list)

    for i in range(len(cities)):
        x_c = cities[i][0]
        y_c = cities[i][1]
        matrix_adj[i] = list()

        for y in range(len(grid)):
            for x in range(len(grid[0])):   


                 if radius >= distance.euclidean((x_c, y_c), grid[y][x]):
                    
                    matrix_adj[i].append(y * len(grid) + x)


    return matrix_adj




def index_to_grid(index: int, grid_size_X: int, grid_size_Y: int) -> int:
    """Return (col, row) of the grid"""
    return index // grid_size_Y, index % grid_size_X

def grid_to_index(col: int, row: int, grid_size_Y: int):
    """Return the index from (col, row)"""
    return col * grid_size_Y + row




    


#### RUN #### 


if __name__ == "__main__":
    # file = "../geonames_smol.csv"
    file = "../geonames-all-cities-with-a-population-1000.csv"
    # file = "../geonames_be_smol.csv"
    data : pd.DataFrame = pd.read_csv(file, sep=";")
    print(get_min_max(data))


    s = time.time()
    # cities, grid = calc_grid(file)
    e = time.time()

    print(e -s)
    matrix = grid_avg(data)

    # f = plt.figure(1)

    # for i in range(len(cities)):
    #     plt.plot(cities[i][0], cities[i][1], "o", color="blue")
        



    # for y in range(len(grid)):
    #     for x in range(len(grid[0])):
    #         plt.plot(grid[y][x][0], grid[y][x][1], "o", color="red")



    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix, cmap=matplotlib.cm.Spectral_r)
    fig.colorbar(cax)

    # g = plt.figure(2)
            
    # matrix_adj = calc_adj(cities=cities, grid=grid, radius=1)

    # c_nb = 10

    # plt.plot(cities[c_nb][0], cities[c_nb][1], "o", color="green")

    # for i in range(len(matrix_adj[c_nb])):
    #     col, row = index_to_grid(matrix_adj[c_nb][i], 10, 10)
  
    #     plt.plot(grid[col][row][0], 
    #              grid[col][row][1],
    #              "o", color="yellow")

    

    plt.show()

    
