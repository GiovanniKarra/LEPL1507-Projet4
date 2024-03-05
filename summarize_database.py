import sys
import pandas as pd
from geopy.distance import geodesic

# Assuming 'cities_df' is your DataFrame
# Install geopy if not already installed: pip install geopy

# Function to calculate distance between two cities
def calculate_distance(city1, city2):
    coord1 = city1["Coordinates"]
    coord2 = city2["Coordinates"]
    return geodesic(coord1, coord2).kilometers

if len(sys.argv) < 2: raise "Not enough arguments, expected >=2, got %d" % len(sys.argv)

for file in sys.argv[1:]:
    cities_df = pd.read_csv(file, sep=";")

    # Define merging criteria
    distance_threshold = 50  # Adjust this based on your preference
    population_threshold = 100000  # Adjust this based on your preference

    # Iterate through the DataFrame to merge close cities
    for index, city1 in cities_df.iterrows():
        for index2, city2 in cities_df.iterrows():
            if city1["Name"] != city2["Name"]:
                distance = calculate_distance(city1, city2)

                # Check if the cities should be merged based on distance and population
                if distance < distance_threshold and city2["Population"] < population_threshold:
                    # Merge city2 into city1
                    cities_df.at[index, "Population"] += city2["Population"]

                    # Drop city2 from the DataFrame
                    cities_df = cities_df.drop(index2)

    # Drop duplicate rows (if any) after merging
    cities_df = cities_df.drop_duplicates(subset=["Name"]).reset_index(drop=True)

    cities_df.to_csv(file.removesuffix(".csv") + "_summarized.csv", sep=";")