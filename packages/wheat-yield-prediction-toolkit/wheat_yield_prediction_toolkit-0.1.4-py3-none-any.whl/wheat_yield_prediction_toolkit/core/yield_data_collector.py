import concurrent.futures
import io
import os
import time

import geopandas as gpd
import pandas as pd
import requests
from tqdm import tqdm


def get_yield(year: int) -> pd.DataFrame:  # sourcery skip: extract-method
    """
    Retrieves county-level wheat yield data for a given year using the USDA Quick Stats API.

    Args:
    year (int): The year for which to retrieve the yield data.

    Returns:
    A pandas DataFrame containing the yield data for the specified year.

    Example usage:
    ```
    >>> yield_2019 = get_yield(2019)
    >>> print(yield_2019.head())
    ```
    """
    # Set the API endpoint
    url = "https://quickstats.nass.usda.gov/api/api_GET/"

    # Get the API key from environment variables
    usda_api_key = os.environ.get("USDA_API_KEY")
    if usda_api_key is None:
        raise ValueError("USDA_API_KEY environment variable not set.")

    # Set the API parameters
    params = {
        "key": usda_api_key,
        "sector_desc": "CROPS",
        "commodity_desc": "WHEAT",
        "statisticcat_desc": "YIELD",
        "freq_desc": "ANNUAL",
        "unit_desc": "BU / ACRE",
        "agg_level_desc": "COUNTY",
        "year": year,
        "format": "CSV",
    }

    try:
        # Make the API request
        response = requests.get(url, params=params)

        # Check the response status code
        response.raise_for_status()

        return pd.read_csv(io.StringIO(response.text))

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while retrieving data for year {year}: {e}")
        return pd.DataFrame()


def get_yield_parallel(start_year: int, end_year: int) -> gpd.GeoDataFrame:
    """
    Retrieves county-level wheat yield data for a range of years in parallel using the USDA Quick Stats API.

    Args:
    start_year (int): The first year for which to retrieve the yield data.
    end_year (int): The last year (exclusive) for which to retrieve the yield data.

    Returns:
    A GeoDataFrame containing the yield data for the specified year range.

    Example usage:
    ```
    >>> yield_data = get_yield_parallel(2019, 2021)
    >>> print(yield_data.head())
    ```
    """
    # Calculate the range length
    range_length = end_year - start_year + 1

    # Check the validity of the range
    if range_length <= 0:
        raise ValueError("End year must be greater than start year.")

    # Print the start message
    print(f"Starting parallel yield data processing for {range_length} years...")

    # Start the timer
    start_time = time.time()

    # Create a list of years to process
    years_to_process = list(range(start_year, end_year + 1))

    # Retrieve the yield data in parallel using threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(get_yield, years_to_process), total=range_length))

    # Concatenate the results into a single DataFrame
    yield_data = pd.concat(results)

    # Convert the yield data to a GeoDataFrame
    yield_gdf = gpd.GeoDataFrame(yield_data)

    # End the timer
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the completion message
    print(f"Parallel yield data processing completed in {elapsed_time:.2f} seconds.")

    return yield_gdf


def save_yield_data(start_year: int, end_year: int, file_path: str):
    """
    Retrieves and saves county-level wheat yield data for a range of years in parallel
    using the USDA Quick Stats API as a parquet file.

    Args:
    start_year (int): The first year for which to retrieve the yield data.
    end_year (int): The last year (exclusive) for which to retrieve the yield data.
    file_path (str): The path where the parquet file will be saved.

    Example usage:
    ```
    >>> save_yield_data(2019, 2021, "data/yield_data.parquet")
    ```
    """
    # Get the yield data
    yield_data = get_yield_parallel(start_year, end_year)

    # Check if the path is valid
    if not os.path.exists(os.path.dirname(file_path)):
        # Create it using os.makedirs()
        os.makedirs(os.path.dirname(file_path))

    # Save the yield data as a parquet file
    yield_data.to_parquet(file_path)

    print(f"Yield data saved to {os.path.abspath(file_path)}")
