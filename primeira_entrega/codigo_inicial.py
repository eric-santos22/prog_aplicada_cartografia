import pandas as pd
import geopandas as gpd


df = pd.read_csv("pontos.csv")

gdf = gpd.GeoDataFrame(df,
                       geometry=gpd.points_from_xy(
                           df.lon, df.lat),
                           crs="EPSG:4326"
                       )

print(gdf.head())