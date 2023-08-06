import os
import ee
from shapely import wkt
from tqdm import tqdm
import concurrent.futures

import pandas as pd
from impute_weather_data import (
    get_weather_all_locations,
    get_weather_parallel,
    save_weather_data,
)
from preprocessor import pre_process_yield # pre_process_weather
from yield_data_collector import get_yield_parallel
from sat_data_collector import get_sat_all_locations
from soil_data_collector import get_soil_all_locations

# Define the data path
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
RAW_DATA = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA = os.path.join(DATA_DIR, "processed")


# Set the start and end years
# Define the historical range : the last considered year id upper_bound - 1
# HIST_RANGE = [1996, 2022]

# yield_df = get_yield_parallel(HIST_RANGE[0], HIST_RANGE[1])

# Get counties boundries :
# yield_df = pre_process_yield(yield_df)


# print(yield_df.head())

# Save the df to a parquet file :
# path_to_save_yield = os.path.join(RAW_DATA, "yield-data", "historical-yield-data-final.csv")
# yield_df.to_csv(path_to_save_yield, index=False)

# Get all unique locations, of yield_df : 'centroid'
# get weather data :
# weather_df = get_weather_all_locations(HIST_RANGE, yield_df["centroid"].unique().tolist())

# # Save the weather data to parquet :
# save_weather_data(HIST_RANGE, yield_df["centroid"].unique().tolist()[3000:], path_to_save_weather)

# weather_dfs = []
# for weather_index in range(1, 8):
#     # Get the path of te parquet file :
#     path_to_save_weather = os.path.join(RAW_DATA, "weather-data", f"historical-weather-data-v3-p{weather_index}.parquet")
#     # Load the parquet file into a dataframe :
#     weather_df = pd.read_parquet(path_to_save_weather)
#     # Append the weather data to the yield data :
#     weather_dfs.append(weather_df)

# # Concat all weather dfs :
# weather_df = pd.concat(weather_dfs)
# # Export the dataframe into a parquet file :
# path_to_save_weather = os.path.join(RAW_DATA, "weather-data", "historical-weather-data-final.parquet")
# weather_df.to_parquet(path_to_save_weather, index=False)



# print(weather_df)

# Read the weather data from parquet :
# weather_df = pd.read_parquet(path_to_save_weather)

# print(weather_df)

# for year in range(1999, 2022, 1):
#     # HIST_RANGE = [1996, 2022]
#     HIST_RANGE = [year, year]

#     # Read the yield data into a dataframe :
#     # path_to_save_yield = os.path.join(RAW_DATA, "yield-data", "historical-yield-data-final.csv")

#     # yield_df = pd.read_csv(path_to_save_yield)

#     # print(yield_df.head())

#     yield_df = get_yield_parallel(HIST_RANGE[0], HIST_RANGE[1])

#     yield_df = pre_process_yield(yield_df)

#     print(yield_df)

#     path_to_save_yield = os.path.join(RAW_DATA, "yield-data", f"historical-yiled-data-final-{HIST_RANGE[0]}-{HIST_RANGE[1]}.parquet")
#     yield_df.to_parquet(path_to_save_yield)


#     list_of_polygons = yield_df['geometry'].unique().tolist()

#     def shapely_to_gee_polygon(shapely_polygon):

#         shapely_polygon = wkt.loads(shapely_polygon)
#         if shapely_polygon.geom_type == 'Polygon':
#             exterior_coords = shapely_polygon.exterior.coords[:]
#             coords = [[coord[0], coord[1]] for coord in exterior_coords]
#             return ee.Geometry.Polygon(coords)
#         elif shapely_polygon.geom_type == 'MultiPolygon':
#             polys = []
#             for poly in shapely_polygon.geoms:
#                 exterior_coords = poly.exterior.coords[:]
#                 coords = [[coord[0], coord[1]] for coord in exterior_coords]
#                 polys.append(ee.Geometry.Polygon(coords))
#             return ee.Geometry.MultiPolygon(polys)

#     def shapely_to_gee_polygon_wrapper(poly):
#         return shapely_to_gee_polygon(poly)

#     ee.Initialize()

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         gee_polygons = list(tqdm(executor.map(shapely_to_gee_polygon_wrapper, list_of_polygons), total=len(list_of_polygons)))


#     sat_df = get_sat_all_locations(HIST_RANGE, gee_polygons)

#     print(sat_df)

#     # Save the sat data to parquet file :
#     path_to_save_sat = os.path.join(RAW_DATA, "sat-data", f"historical-sat-data-final-{HIST_RANGE[0]}-{HIST_RANGE[1]}.parquet")
#     os.makedirs(os.path.dirname(path_to_save_sat), exist_ok=True)
#     yield_df.to_parquet(path_to_save_yield, index=False)



# HIST_RANGE = [1996, 2022]
HIST_RANGE = [1999, 2022]

yield_df = get_yield_parallel(HIST_RANGE[0], HIST_RANGE[1])

yield_df = pre_process_yield(yield_df)

# print(yield_df.head(30))

list_of_polygons = yield_df['geometry'].unique().tolist()

print(f"len of the polygons list {len(list_of_polygons)}")
# print(f"list of polygons {list_of_polygons}")

# Divide 'list_of_polygons' into small chunks lists
list_of_polygons = [list_of_polygons[i:i + 10] for i in range(0, len(list_of_polygons), 10)]

for poly_list in list_of_polygons :

    part_indicator = 1

    soil_df = get_soil_all_locations(poly_list)

    # print(soil_df)

    # Save the sat data to parquet file :
    path_to_save_soil = os.path.join(
        RAW_DATA, "soil-data", f"historical-soil-data-final-p{part_indicator}.parquet"
    )
    # os.makedirs(os.path.dirname(path_to_save_sat), exist_ok=True)
    yield_df.to_parquet(path_to_save_soil, index=False)

    part_indicator += 1











