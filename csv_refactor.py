import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def refactorisator(file):
    data = pd.read_csv(file, sep=";")

    ville = data["Name"]
    weights = data["Population"]           
    lat = data["Coordinates"].str.split(",",expand=True)[0].astype(float)
    lon = data["Coordinates"].str.split(",",expand=True)[1].astype(float)

    new_df = pd.DataFrame({"villeID": ville, "size": weights, "lat": lat, "long": lon})
    
    splt = file.split("_")
    new_name = "refactored_" + splt[1] + "_" + splt[2]
    new_df.to_csv(new_name)

def el_coupe_coupe(file, min_lat, max_lat, min_lon, max_lon):
    data = pd.read_csv(file)
    new_data = data[data["lat"].between(min_lat, max_lat)]
    new_data = new_data[new_data["long"].between(min_lon, max_lon)]
    new_data.drop(new_data[new_data["size"] < 10000].index, inplace=True)
    print(len(new_data))
    new_data.to_csv("../test.csv")
    # new_data.to_csv("../Asie_1k.csv")

if __name__ == "__main__":
    
    file = "../refactored_cleared.csv"

    el_coupe_coupe(file, -10, 75, 50, 180)
    

