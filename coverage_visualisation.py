import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def visualise_coverage_2D(cities : list[tuple[str, float, float]] | pd.DataFrame,
                       satellites : list[tuple[float, float, float]],
                       power : float | list[float],
                       threashold : float,
                       show_names : bool = True):
    """
    @pre :
        cities : a list of tuples (name, longitude, latitude), or a pandas dataframe from a geonames_*.csv file
        satellites : a list of tuples (longitude, latitude, altitude)
        power : the power of the satellites in MW
        threashold : the minimum intensity needed to be convered
        show_names : if the names of the cities are shown on the plot, set to `True` by default
    @post :
        a 2D plot of the coverage of the satellites
    """
    
    if isinstance(power, float): power = [power]*len(satellites)

    if isinstance(cities, pd.DataFrame):
        cities = [(city, *[float(x) for x in coord.split(",")[::-1]])
              for _, city, _, _, _, coord in cities.to_records()]

    plt.figure()

    plt.xlabel("longitude [°]")
    plt.ylabel("latitude [°]")

    for i, (x, y, z) in enumerate(satellites):
        critical_r = np.sqrt(power[i]/(4*np.pi*threashold))/1000 # en km
        if critical_r <= z:
            print(f"sattelite {i} doesn't cover anything")
            continue

        critical_d = np.sqrt(critical_r*critical_r - z*z)

        x_ = np.linspace(-critical_d, critical_d, 100)
        y_ = np.sqrt(-np.power(x_, 2)+critical_d*critical_d)
        y2 = -y_
        plt.fill((x_/111.2)+x, (y_/111.2)+y, "orange", (x_/111.2)+x, (y2/111.2)+y, "orange")

    city_locations = np.array([city[1:] for city in cities]).T
    plt.scatter(city_locations[0], city_locations[1])

    if show_names:
        for name, x, y in cities:
            plt.text(x, y, name)


    if len(satellites) > 0:
        satellite_locations = np.array(satellites).T
        plt.scatter(satellite_locations[0], satellite_locations[1], c="r")

    plt.show()


def visualise_coverage_3D(cities : list[tuple[str, float, float]] | pd.DataFrame,
                       satellites : list[tuple[float, float, float]],
                       power : float | list[float],
                       threashold : float,
                       show_names : bool = True):
    """
    @pre :
        cities : a list of tuples (name, longitude, latitude), or a pandas dataframe from a geonames_*.csv file
        satellites : a list of tuples (longitude, latitude, altitude)
        power : the power of the satellites in MW
        threashold : the minimum intensity needed to be convered
        show_names : if the names of the cities are shown on the plot, set to `True` by default
    @post :
        a 3D plot of the coverage of the satellites
    """
    
    if isinstance(power, float): power = [power]*len(satellites)

    if isinstance(cities, pd.DataFrame):
        cities = [(city, *[float(x) for x in coord.split(",")[::-1]])
              for _, city, _, _, _, coord in cities.to_records()]

    ax = plt.figure().add_subplot(projection="3d")

    # plt.xlabel("longitude [°]")
    # plt.ylabel("latitude [°]")

    #plt.subplot()

    # for i, (x, y, z) in enumerate(satellites):
    #     critical_r = np.sqrt(power[i]/(4*np.pi*threashold))/1000 # en km
    #     if critical_r <= z:
    #         print(f"sattelite {i} doesn't cover anything")
    #         continue

    #     critical_d = np.sqrt(critical_r*critical_r - z*z)

    #     x_ = np.linspace(-critical_d, critical_d, 100)
    #     y_ = np.sqrt(-np.power(x_, 2)+critical_d*critical_d)
    #     y2 = -y_
    #     plt.fill((x_/111.2)+x, (y_/111.2)+y, "orange", (x_/111.2)+x, (y2/111.2)+y, "orange")

    city_locations = np.array([(*city[1:], 0) for city in cities])
    for i, (long, lat, _) in enumerate(city_locations):
        x = np.cos(long)*np.cos(lat); y = np.sin(long)*np.cos(lat); z = np.sin(lat)
        city_locations[i] = np.array((x, y, z))*40000
    city_locations = city_locations.T
    ax.scatter(city_locations[0], city_locations[1], city_locations[2])

    # if show_names:
    #     for name, x, y in cities:
    #         plt.text(x, y, name)


    if len(satellites) > 0:
        satellite_locations = np.array(satellites).T
        #plt.scatter(satellite_locations[0], satellite_locations[1], c="r")

    plt.show()


if __name__ == "__main__":
    data_be_smol : pd.DataFrame = pd.read_csv("geonames_be_smol.csv", sep=";")
    data_be_big : pd.DataFrame = pd.read_csv("geonames_be.csv", sep=";")
    data_glob_big : pd.DataFrame = pd.read_csv("geonames_cleared.csv", sep=";")
    data_glob_smol : pd.DataFrame = pd.read_csv("geonames_smol.csv", sep=";")
    
    visualise_coverage_3D(data_glob_smol, [(4, 50, 1000)],
                          power=9.0e10, threashold=0.007, show_names=True)