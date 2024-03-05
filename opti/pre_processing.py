import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import math



def calc_grid(file: str, grid_size_X = 10, grid_size_Y = 10) -> np.ndarray:
    data : pd.DataFrame = pd.read_csv(file, sep=";")
    cities = np.empty(len(data), dtype=tuple)

    coor = data["Coordinates"].apply(lambda x: x.split(","))
    data["x"] = coor.apply(lambda x: float(x[1]))
    data["y"] = coor.apply(lambda x: float(x[0]))
    data["weight"] = data["Population"].apply(float)

    maxX = data["x"].max()
    maxY = data["y"].max()
    minX = data["x"].min()
    minY = data["y"].min()

    cities = np.array(list(zip(data["x"], data["y"], data["weight"])))

    grid = np.empty(grid_size_Y * grid_size_X, dtype=tuple).reshape(grid_size_Y, grid_size_X)

    x = np.linspace(minX, maxX, grid_size_X)
    y = np.linspace(minY, maxY, grid_size_Y)
    
    grid = np.array(np.meshgrid(x, y)).T.reshape(-1, 2)

    return cities, grid




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

    cities, grid = calc_grid("../geonames_be_smol.csv")


    for i in range(len(cities)):
        plt.plot(cities[i][0], cities[i][1], "o", color="blue")
        



    for y in range(len(grid)):
        for x in range(len(grid[0])):
            plt.plot(grid[y][x][0], grid[y][x][1], "o", color="red")




    # print(grid)
            
    matrix_adj = calc_adj(cities=cities, grid=grid, radius=1)

    c_nb = 10

    plt.plot(cities[c_nb][0], cities[c_nb][1], "o", color="green")

    for i in range(len(matrix_adj[c_nb])):
        col, row = index_to_grid(matrix_adj[c_nb][i], 10, 10)
  
        plt.plot(grid[col][row][0], 
                 grid[col][row][1],
                 "o", color="yellow")

    

    plt.show()

    
