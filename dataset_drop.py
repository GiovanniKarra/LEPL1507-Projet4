import pandas as pd

data = pd.read_csv("geonames_cleared.csv", sep=";")

cond = data["Population"] < 500_000

print(data.size)

data.drop(data[cond].index, inplace=True)

print(data.size)

data.to_csv("geonames_smol.csv", index=False, sep=";")