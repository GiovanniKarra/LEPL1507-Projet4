import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def visualise_coverage_2D(cities : list[tuple[str, float, float]] | pd.DataFrame,
                       satellites : list[tuple[float, float, float]],
                       power : float | list[float],
                       threashold : float):
    """
    @pre :
        cities : a list of tuples (name, longitude, latitude), or a pandas dataframe from a geonames_*.csv file
        satellites : a list of tuples (longitude, latitude, altitude)
        power : the power of the satellites in MW
        threashold : the minimum intensity needed to be convered
    @post :
        a plot of the coverage of the satellites
    """
    
    if isinstance(power, float): power = [power]*len(satellites)

    if isinstance(cities, pd.DataFrame):
        cities = [(city, *[float(x) for x in coord.split(",")[::-1]])
              for _, city, _, _, _, coord in cities.to_records()]

    plt.figure()

    plt.xlabel("longitude [°]")
    plt.ylabel("latitude [°]")

    for i, (x, y, z) in enumerate(satellites):
        critical_r = np.sqrt(power[i]/(4*np.pi*threashold))
        if critical_r <= z:
            print(f"sattelite {i} doesn't cover anything")
            continue

        critical_d = np.sqrt(critical_r*critical_r - z*z)

        x_ = np.linspace(-critical_d, critical_d, 100)
        y_ = np.sqrt(-np.power(x_, 2)+critical_d*critical_d)
        y2 = -y_
        plt.fill(x_+x, y_+y, "orange", x_+x, y2+y, "orange")

    city_locations = np.array([city[1:] for city in cities]).transpose()
    plt.scatter(city_locations[0], city_locations[1])
    for name, x, y in cities:
        plt.text(x, y, name)


    if len(satellites) > 0:
        satellite_locations = np.array(satellites).transpose()
        plt.scatter(satellite_locations[0], satellite_locations[1], c="r")

    plt.show()


if __name__ == "__main__":
    # visualise_coverage_2D([("Mons", 0, 0), ("LLN", -5.587, 9.58461)],
    #                    [(-2, 2, 10), (-5, 10, 10)], 10.0, 0.007)

    data : pd.DataFrame = pd.read_csv("geonames_be_smol.csv", sep=";")
    
    visualise_coverage_2D(data, [(4, 50, 10)], 9.0, 0.007)