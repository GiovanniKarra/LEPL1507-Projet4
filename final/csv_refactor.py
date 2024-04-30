import pandas as pd
import numpy as np

if __name__ == "__main__":
    
    file = "geonames_be_summarized.csv"
    

    data = pd.read_csv(file, sep=";")

    ville = data["Name"]
    weights = data["Population"]           
    lat = data["Coordinates"].str.split(",",expand=True)[0].astype(float)
    lon = data["Coordinates"].str.split(",",expand=True)[1].astype(float)

    new_df = pd.DataFrame({"villeID": ville, "size": weights, "lat": lat, "long": lon})
    
    splt = file.split("_")
    new_name = "refactored_" + splt[1] + "_" + splt[2]
    new_df.to_csv(new_name)