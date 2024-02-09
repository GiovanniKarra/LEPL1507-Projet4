import plotly.express as px
import pandas as pd

def visu():
    df = pd.read_csv("geonames_cleared.csv",delimiter=";")

    df["latitude"] = df["Coordinates"].str.split(",",expand=True)[0].astype(float)
    df["longitude"] = df["Coordinates"].str.split(",",expand=True)[1].astype(float)
    
    fig = px.scatter_mapbox(
    df,
    lat=df["latitude"],
    lon=df["longitude"],
    hover_name= df["Name"], # column added to hover information
    mapbox_style="open-street-map",
    # color_discrete_sequence=px.colors.qualitative.Dark24,
    )

    fig.show()
    

if __name__ == "__main__":
	visu()
	print("done")
