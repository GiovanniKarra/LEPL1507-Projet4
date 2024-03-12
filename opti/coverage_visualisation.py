import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def visualise_coverage_2D(cities : list[tuple[str, float, float]] | pd.DataFrame,
                       satellites : list[tuple[float, float, float]],
                       radius : float | list[float],
                       show_names : bool = True):
    """
    @pre :
        cities : a list of tuples (name, longitude, latitude), or a pandas dataframe from a geonames_*.csv file
        satellites : a list of tuples (longitude, latitude, altitude)
        radius : sattelite coverage radius in km
        show_names : if the names of the cities are shown on the plot, set to `True` by default
    @post :
        a 2D plot of the coverage of the satellites
    """
    
    if isinstance(radius, float): radius = [radius]*len(satellites)

    if isinstance(cities, pd.DataFrame):
        cities = [(city, *[float(x) for x in coord.split(",")[::-1]])
              for _, city, _, _, _, coord in cities.to_records()]

    plt.figure()

    plt.xlabel("longitude [°]")
    plt.ylabel("latitude [°]")

    for i, (x, y, z) in enumerate(satellites):

        t = np.linspace(0, np.pi*2, 100)
        circle_x = np.cos(t)*radius[i]
        circle_y = np.sin(t)*radius[i]
        plt.fill(x+circle_x/111.12, y+circle_y/111.12, "orange")

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
                       radius : float | list[float],
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
    
    if isinstance(radius, float): radius = [radius]*len(satellites)

    if isinstance(cities, pd.DataFrame):
        cities = [(city, *[float(x) for x in coord.split(",")[::-1]])
              for _, city, _, _, _, coord in cities.to_records()]

    ax = plt.figure().add_subplot(projection="3d")

    city_locations = np.array([(*city[1:], 0) for city in cities])
    for i, (long, lat, _) in enumerate(city_locations):
        long = np.deg2rad(long); lat = np.deg2rad(lat)
        x = np.cos(long)*np.cos(lat); y = np.sin(long)*np.cos(lat); z = np.sin(lat)
        city_locations[i] = np.array((x, y, z))
    city_locations = city_locations.T
    ax.scatter(city_locations[0], city_locations[1], city_locations[2], s=3)

    # if show_names:
    #     for name, x, y in cities:
    #         plt.text(x, y, name)


    if len(satellites) > 0:
        satellite_locations = np.array(satellites, dtype=float)
        for i, (long, lat, alt) in enumerate(satellite_locations):
            long = np.deg2rad(long); lat = np.deg2rad(lat)
            x = np.cos(long)*np.cos(lat); y = np.sin(long)*np.cos(lat); z = np.sin(lat)
            satellite_locations[i] = np.array((x, y, z))

            # rad = radius[i]
            # t = np.linspace(0, 2*np.pi, 100)
            # circle_long = np.cos(t)*rad/111.12+long
            # circle_lat = np.sin(t)*rad/111.12+lat

            # circle_x = np.cos(circle_long)*np.cos(circle_lat)
            # circle_y = np.sin(circle_long)*np.cos(circle_lat)
            # circle_z = np.sin(circle_lat)

            # np.append(circle_x, x)
            # np.append(circle_y, y)
            # np.append(circle_z, z)

            # circle_points = np.array([circle_x, circle_y, circle_z])

            # ax.plot_surface(circle_x, circle_y, np.array([circle_z, circle_z]),
            #                 color="orange")

        satellite_locations = satellite_locations.T*1.2
        ax.scatter(satellite_locations[0], satellite_locations[1], satellite_locations[2],
                   color="r")

    # sphère
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
    scale = 0.95
    x = np.cos(u)*np.sin(v)*scale
    y = np.sin(u)*np.sin(v)*scale
    z = np.cos(v)*scale
    #ax.plot_surface(x, y, z, color="white", shade=False)


    plt.show()


if __name__ == "__main__":

    if len(sys.argv) not in {3, 4}:
        raise Exception("Expected 2 (or 3) arguments (filename, 2D/3D(, show names)),\
                        got %d" % len(sys.argv)) 

    filename = sys.argv[1]; visu_type = sys.argv[2]
    show = bool(int(sys.argv[3])) if len(sys.argv) == 4 else False
    data : pd.DataFrame = pd.read_csv(filename, sep=";")
    
    if visu_type == "2D":
        visualise_coverage_2D(data, [(4, 50, 1000)],
                            radius=100.0, show_names=show)
        
    if visu_type == "3D":
        visualise_coverage_3D(data, [(4, 50, 1000)],
                            radius=1000.0, show_names=show)
        
    else:
        raise Exception("Dimension argument not used correctly,"
                        "expected '2D' or '3D', but got '%s'" % visu_type)