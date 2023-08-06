import concurrent
import time
from datetime import datetime

import pandas as pd
import shapely
from meteostat import Daily, Hourly, Monthly, Point
from tqdm import tqdm


def compute_GDD(df):
    """Computes Growing Degree Days (GDD) index for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tavg (average temperature).

    Returns:
        pandas.DataFrame: Dataframe with GDD index computed and added as a new column.

    """
    base_temperature = 0
    df["gdd"] = df["tavg"] - base_temperature
    df["gdd"] = df["gdd"].apply(lambda x: max(x, 0))
    return df


def compute_EHDD(df):
    """Computes Extended Heat Degree Days (EHDD) index for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tmax (maximum temperature).

    Returns:
        pandas.DataFrame: Dataframe with EHDD index computed and added as a new column.

    """
    crop_max_temperature = 27.2222  # 81 F
    df["ehdd"] = df["tmax"] - crop_max_temperature
    df["ehdd"] = df["ehdd"].apply(lambda x: max(x, 0))
    return df


def compute_ECDD(df):
    """Computes Extended Cold Degree Days (ECDD) index for a given dataframe.

    Args:
        df (pandas.DataFrame): Dataframe containing weather data with columns for tmin (minimum temperature).

    Returns:
        pandas.DataFrame: Dataframe with ECDD index computed and added as a new column.

    """
    crop_min_temperature = -4.44444
    df["ecdd"] = crop_min_temperature - df["tmin"]
    df["ecdd"] = df["ecdd"].apply(lambda x: max(x, 0))
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


def get_weather(year, location=(38.97167, -95.23525, 70)):
    """Fetches weather data for a given year and location using Meteostat API.

    Args:
        year (int): Year for which weather data is needed.
        location (tuple): Latitude, longitude, and elevation of location.

    Returns:
        pandas.DataFrame: Dataframe containing weather data for the given year and location.

    """
    LOCATION = Point(location[0], location[1], location[2])

    start = datetime(year, 9, 1)
    end = datetime(year + 1, 8, 30)

    data = Daily(LOCATION, start, end)
    data = data.fetch()

    data = compute_Index(data)

    data["location"] = shapely.Point(location[0], location[1]).astype(str)

    return data


def get_weather_parallel(HIST_RANGE, location):
    """
    Fetches weather data for a single location across a range of years in parallel.

    Args:
        HIST_RANGE (Tuple[int, int]): A tuple containing the start and end years for the data range.
        location (Tuple[float, float, float]): A tuple containing the latitude, longitude, and elevation of the location.

    Returns:
        pandas.DataFrame: A DataFrame containing weather data for the location across the specified years.
    """
    range_length = len(range(HIST_RANGE[0], HIST_RANGE[1]))
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            executor.map(
                get_weather, range(HIST_RANGE[0], HIST_RANGE[1]), [location] * range_length
            )
        )

    return pd.concat(results)


def get_weather_all_locations(HIST_RANGE, list_locations):
    """
    Fetches weather data for multiple locations across a range of years in parallel.

    Args:
        HIST_RANGE (Tuple[int, int]): A tuple containing the start and end years for the data range.
        list_locations (List[Tuple[float, float, float]]): A list of tuples containing the latitude, longitude, and elevation of each location.

    Returns:
        pandas.DataFrame: A DataFrame containing weather data for all locations across the specified years.
    """
    range_length = len(list_locations)
    print(f"Starting parallel weather data processing for {range_length} locations...")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(get_weather_parallel, [HIST_RANGE] * range_length, list_locations),
                total=range_length,
            )
        )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallel weather data processing completed in {elapsed_time:.2f} seconds.")
    return pd.concat(results)


# -- Main :
if __name__ == "__main__":
    # -- Test code :
    HIST_RANGE = (2010, 2019)
    list_locations = [(38.97167, -95.23525, 70), (38.97167, -95.23525, 70)]
    df = get_weather_all_locations(HIST_RANGE, list_locations)
    print(df)
