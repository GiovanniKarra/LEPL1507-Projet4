import plotly.express as px
import pandas as pd
import numpy as np


def plannar_2D_visu2(file_cities, statelites, coverred_id=None, radius=1000):
    df = pd.read_csv(file_cities, delimiter=";")
    lat = []
    long = []

    for i in range(len(df)):
        split = df["Coordinates"][i].split(",")
        lat.append(float(split[0]))
        long.append(float(split[1]))

    df.insert(3, "lat", lat, True)
    df.insert(4, "lon", long, True)
    df.insert(5, "color", ['red'] * len(df), True)

    data = pd.DataFrame(statelites, columns=['lat', 'lon'])
    data.insert(1, "radius", [1000] * len(data), True)
    
    fig1 = px.scatter_geo(df, lat="lat", lon="lon", projection="natural earth")
    fig2 = px.scatter_geo(data, lat="lat", lon="lon", size="radius", projection="natural earth")

    if coverred_id is not None:

        pass
    

    fig = px.scatter_geo()
    fig.add_traces(fig1._data)
    fig.add_traces(fig2._data)

    return fig



def plannar_2D_visu(cities_coordinates,tot_sat_coordsf,id_covered):

    covered_citites = []

    # cities_coordinates =np.reshape(cities_coordinates, (len(c)))
    # print(covered_citites.shape)  
    # print(cities_coordinates.shape)  

    for i, index in enumerate(id_covered):
        covered_citites.append([cities_coordinates[index][0],cities_coordinates[index][1]])

    covered_citites = np.array(covered_citites)

    df_covered = pd.DataFrame(covered_citites, columns=['lat', 'lon'])
    df_cities = pd.DataFrame(cities_coordinates, columns=['lat', 'lon'])
    df_sat =  pd.DataFrame(tot_sat_coordsf, columns=['lat', 'lon'])

    df_covered.insert(0, 'color', [1] * len(df_covered), True)
    df_cities.insert(1, 'color', [2] * len(df_cities), True)
    df_sat.insert(0, 'size', [1] * len(df_sat), True)

    fig1 = px.scatter_geo(df_cities, lat="lat", lon="lon", projection="natural earth", color='color')
    fig2 = px.scatter_geo(df_covered, lat="lat", lon="lon", projection="natural earth", color='color')
    fig3 = px.scatter_geo(df_sat, lat="lat", lon="lon", projection="natural earth", size='size')


    fig = px.scatter_geo()
    fig.add_traces(fig1._data)
    fig.add_traces(fig2._data)
    fig.add_traces(fig3._data)


    fig.show()



if __name__ == "__main__":

    file = "geonames_smol.csv"

    # df = pd.read_csv(file, delimiter=";")

    # lat = []
    # long = []
    # color_red = [1] * len(df)

    # print(color_red)

    # for i in range(len(df)):
    #     split = df["Coordinates"][i].split(",")
    #     lat.append(float(split[0]))
    #     long.append(float(split[1]))

    # df.insert(3, "lat", lat, True)
    # df.insert(4, "lon", long, True)
    # df.insert(5, "color", color_red, True)


    # print(df)

    # data = {'lat': [50.8476],
    #         'lon': [4.3572],
    #         'radius': [1000]}

    # fig1 = px.scatter_geo(df, lat="lat", lon="lon", projection="natural earth", color="Population")
    # fig2 = px.scatter_geo(data, lat="lat", lon="lon", size="radius", projection="natural earth" )

    # fig = px.scatter_geo()
    # fig.add_traces(fig1._data)
    # fig.add_traces(fig2._data)


    sat = [[50.8476, 4.3572]]

    fig =  plannar_2D_visu2(file, sat)


    fig.show()