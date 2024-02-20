import cvxpy as cp
import numpy as np
import pandas as pd
import math
import time
import matplotlib.pyplot as plt

def obj():
    pass



def opti_scipy(Matrix,R,nbr_sat):
    pass


if __name__ == "__main__":
    df = pd.read_csv("geonames_be_smol.csv",delimiter=";")
    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    df.drop(columns=["Coordinates","Name","Country name EN","Elevation"],inplace=True)

    mat = df.to_numpy()
    print(mat)

    rayon = 40
    sat = 1

    opti_scipy(mat,rayon,sat)