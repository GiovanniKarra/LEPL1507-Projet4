import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math



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
    


    for i in enumerate(x):
        for j in enumerate(y):
            grid[j[0]][i[0]] = tuple((x[i[0]], y[j[0]]))





    return cities, grid




#### RUN #### 


if __name__ == "__main__":

    cities, grid = calc_grid("../geonames_be_smol.csv")

    print(grid[0])


    for i in range(len(cities)):
        plt.plot(cities[i][0], cities[i][1], "o", color="blue")
        



    for y in range(len(grid)):
        for x in range(len(grid[0])):
            plt.plot(grid[y][x][0], grid[y][x][1], "o", color="red")




    # print(grid)

    # plt.show()


    