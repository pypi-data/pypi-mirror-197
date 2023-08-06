import os
from concurrent.futures import ThreadPoolExecutor

import geopandas as gpd
import shapely
from shapely.geometry import Polygon
from tqdm import tqdm

# Define all pre-processing functions


def compute_GDD(df):
    """Computes Growing Degree Days (GDD) index for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tavg (average temperature).

    Returns:
        pandas.DataFrame: Dataframe with GDD index computed and added as a new column.

    """
    base_temperature = 0
    df["T2M_MEAN"] = (df["T2M_MAX"] + df["T2M_MIN"]) / 2.0
    df["GDD"] = df["T2M_MEAN"] - base_temperature
    df["GDD"] = df["GDD"].apply(lambda x: max(x, 0))
    return df


def compute_EHDD(df):
    """Computes Extended Heat Degree Days (EHDD) index for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tmax (maximum temperature).

    Returns:
        pandas.DataFrame: Dataframe with EHDD index computed and added as a new column.

    """
    crop_max_temperature = 27.2222  # 81 F
    df["EHDD"] = df["T2M_MAX"] - crop_max_temperature
    df["EHDD"] = df["EHDD"].apply(lambda x: max(x, 0))
    return df


def compute_ECDD(df):
    """Computes Extended Cold Degree Days (ECDD) index for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tmin (minimum temperature).

    Returns:
        pandas.DataFrame: Dataframe with ECDD index computed and added as a new column.

    """
    crop_min_temperature = -4.44444
    df["ECDD"] = crop_min_temperature - df["T2M_MIN"]
    df["ECDD"] = df["ECDD"].apply(lambda x: max(x, 0))
    return df


def compute_Index(df):
    """Computes all three temperature indices (GDD, EHDD, ECDD) for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tavg, tmax, and tmin.

    Returns:
        pandas.DataFrame: Dataframe with all three temperature indices computed and added as new columns.

    """
    df = compute_GDD(df)
    df = compute_EHDD(df)
    df = compute_ECDD(df)
    return df


def create_weather_list(row):
    return list(row.drop(exclude=["YEAR", "location", "MO", "DY"]))


def get_counties_boundries():

    """

    Get the boundries of all counties in the US

    """

    # get current file path :

    shape_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tmp", "gz_2010_us_050_00_500k.shp"
    )

    # shape_file_path = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), "tmp", "cb_2018_us_county_5m.shp"
    # )

    # Get the shape file :

    shp = gpd.read_file(shape_file_path)

    # Get the counties boundries :

    shp = shp[["COUNTY", "geometry"]]

    # Remove leading zeros from the COUNTY column

    shp["COUNTY"] = shp["COUNTY"].astype(int)

    return shp


# define yield data pre-processing : pre_process_yield


def pre_process_yield(yield_df):

    bounds = get_counties_boundries()

    # Get only the 'class_desc' == WINTER

    yield_df = yield_df[yield_df["class_desc"] == "WINTER"]

    # Remove leading zeros from the county code column

    yield_df = yield_df.dropna(subset=["county_code"])

    # Remove unnecessary columns :

    yield_df = yield_df[["county_code", "year", "Value"]]

    # Merge the yield data with the counties boundries :

    yield_df = yield_df.merge(bounds, how="left", left_on="county_code", right_on="COUNTY")

    yield_df = gpd.GeoDataFrame(yield_df)

    # print(yield_df)
    # add centeroid column, the geocenter on the Polygon, using geopandas:

    # Remove all 'geometry' NoneType values :
    yield_df = yield_df[~yield_df["geometry"].isna()]
    # yield_df["centroid"] = yield_df["geometry"].map(lambda p: p.centroid)
    # yield_df["geometry"] = yield_df["geometry"].simplify(10000)
    # print(type(yield_df['geometry'][0].centroid))

    # Remove 'county_code' after merging :

    yield_df = yield_df.drop(columns=["COUNTY"])

    # Convert the 'centroid' & 'geometry' to strings, for saving as a parquet file :

    # yield_df["geometry"] = yield_df["geometry"].astype(str)

    # yield_df["centroid"] = yield_df["centroid"].astype(str)


    return yield_df


# def pre_process_weather(weather_df):

#     # Use compute_Index
#     # weather_df = compute_Index(weather_df)

#     # create a new column with a list of all the weather variables for each row
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(create_weather_list, (row for _, row in weather_df.iterrows())))

#     weather_df["weather_list"] = results

#     return weather_df.groupby(["YEAR", "location"]).agg({"weather_list": list}).reset_index()
