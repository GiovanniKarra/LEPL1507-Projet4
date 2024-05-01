import plotly.express as px
import pandas as pd

def visu():
    df = pd.read_csv("test.csv")
    
    fig = px.scatter_mapbox(
    df,
    lat=df["lat"],
    lon=df["long"],
    hover_name= df["villeID"], # column added to hover information
    mapbox_style="open-street-map",
    # color_discrete_sequence=px.colors.qualitative.Dark24,
    )

    fig.show()
    

if __name__ == "__main__":
	visu()
	print("done")
