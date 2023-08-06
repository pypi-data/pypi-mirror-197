import sys

sys.path.append("..")

import concurrent.futures
import itertools
import os
import time

import ee
import geemap
import numpy as np
import pandas as pd
import rasterio
from tqdm import tqdm

# Now you can import modules from your package
from bands import addAllBandsLandsat


def extract_info(image: ee.Image, county: ee.Feature) -> list:
    """
    Extracts vegetation indices from a Landsat image for a specific county.

    Args:
    - image: ee.Image object representing a Landsat image.
    - county: ee.Feature object representing a county geometry.

    Returns:
    - A list of spectral indices computed for the county.

    Raises:
    - Exception: If an error occurs during the computation.

    Notes:
    - This function downloads the image as a GeoTIFF, computes vegetation indices,
      and removes the downloaded file to avoid disk space issues.

    Example usage:
    ```
    >>> image = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318")
    >>> county = ee.FeatureCollection("TIGER/2018/Counties").filter(ee.Filter.eq('NAME', 'Los Angeles'))
    >>> indices = extract_info(image, county.first())
    ```
    """

    try:
        # Get the date of the image
        date = ee.Date(image.get("system:time_start")).format("YYYY-MM-dd").getInfo()

        # Define the parameters for reduceToVectors
        scale = 10

        # Download the image as GeoTIFF
        roi = ee.Feature(county, {}).geometry()

        # Exporting all bands as one single image
        out_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp", "downloads")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        filename = os.path.join(out_dir, f"Landsat-{date}.tif")
        geemap.ee_export_image(image, filename, region=roi, scale=scale, file_per_band=False)

        # Read the GeoTIFF into an array
        with rasterio.open(filename) as src:
            array = src.read()

        # Compute the mean value of each spectral index for the county
        segment_mean = []
        for index in range(array.shape[0]):
            mean = np.mean(array[index, :, :])
            segment_mean.append(mean)

        # Remove downloaded file
        os.remove(filename)

        # Return a list of the county geometry, date, and spectral indices
        return segment_mean

    except Exception as e:
        print(e)
        return None


def get_VIndices(year: int, county: ee.Geometry) -> pd.DataFrame:
    """
    This function retrieves vegetation indices from Landsat Surface Reflectance images for a given year and county.

    Parameters:
        year (int): The year of interest for the data collection.
        county (ee.Geometry): The study area geometry, represented as an ee.Geometry object.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the year, county geometry in GeoJSON format, and a list of vegetation indices.

    Example:
        # Import the necessary modules
        import ee
        import pandas as pd
        from sat_data_collector import get_VIndices

        # Initialize the Earth Engine API
        ee.Initialize()

        # Define the study area geometry
        county = ee.Geometry.Polygon([
            [-115.756156, 35.970222],
            [-115.752712, 35.966528],
            [-115.746858, 35.967259],
            [-115.746285, 35.969280],
            [-115.753492, 35.970396]
        ])

        # Retrieve the vegetation indices for the year 2010 and the study area
        vi_df = get_VIndices(2010, county)

        # Print the resulting DataFrame
        print(vi_df)
    """
    # Define the time period of interest (one year)
    start_date = f"{year}-09-01"
    end_date = f"{year+1}-08-30"

    # Load the Landsat Surface Reflectance collection
    sentinel2 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")

    # Filter the collection by time and study area
    filtered_sentinel2 = sentinel2.filterDate(start_date, end_date).filterBounds(county)

    # Add vegetation indices
    s2_with_bands = filtered_sentinel2.map(addAllBandsLandsat)

    # Get a list of images from the collection
    s2_list = s2_with_bands.toList(s2_with_bands.size())

    # Get the number of images in the collection
    range_length = s2_list.size().getInfo()
    print(f"Starting parallel sat data processing for {range_length} images...")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Extract vegetation index information in parallel using multiple threads
        results = list(
            tqdm(
                executor.map(
                    extract_info,
                    [ee.Image(s2_list.get(i)) for i in range(range_length)],
                    [county] * range_length,
                ),
                total=range_length,
            )
        )

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallel sat data processing completed in {elapsed_time:.2f} seconds.")

    # Return the resulting DataFrame
    return pd.DataFrame(
        [
            [year, county.toGeoJSON()]
            + [
                np.array(
                    list(
                        itertools.chain.from_iterable(
                            [x if isinstance(x, list) else [x] for x in results]
                        )
                    )
                )
            ]
        ],
        columns=["year", "county_json", "VI_list"],
    )


def get_sat_parallel(HIST_RANGE, county):
    """
    Collects satellite data for a given county over a range of years.

    Parameters:
    -----------
    HIST_RANGE : tuple
        A tuple containing the start and end years (inclusive) for which to collect satellite data.
    county : ee.Geometry.Polygon
        A polygon representing the county for which to collect satellite data.

    Returns:
    --------
    pandas.DataFrame
        A dataframe containing the collected satellite data, with columns for the year, county polygon as a GeoJSON
        string, and the vegetation index list.

    Example:
    --------
    # Collect satellite data for Alameda County in California for the years 2010-2015
    county = ee.Geometry.Polygon([
        [-122.46, 37.65],
        [-122.46, 37.98],
        [-121.68, 37.98],
        [-121.68, 37.65]
    ])
    HIST_RANGE = (2010, 2015)
    sat_data = get_sat_parallel(HIST_RANGE, county)
    """
    range_length = len(range(HIST_RANGE[0], HIST_RANGE[1] + 1))
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            executor.map(
                get_VIndices, range(HIST_RANGE[0], HIST_RANGE[1] + 1), [county] * range_length
            )
        )

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallel satellite data processing completed in {elapsed_time:.2f} seconds.")

    return pd.concat(results)


def get_sat_all_locations(HIST_RANGE: tuple, list_locations: list) -> pd.DataFrame:
    """
    Retrieves Sentinel-2 satellite data for a list of locations and time period of interest, and calculates
    vegetation indices for each location and time step in parallel.

    Args:
    - HIST_RANGE (tuple): A tuple specifying the start and end years of the time period of interest.
    - list_locations (list): A list of polygons defining the locations of interest.

    Returns:
    - A pandas dataframe with vegetation indices for each location and time step.
    """

    range_length = len(list_locations)
    print(f"Starting parallel satellite data processing for {range_length} locations...")

    # Execute get_sat_parallel function for each location in parallel
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(get_sat_parallel, [HIST_RANGE] * range_length, list_locations),
                total=range_length,
            )
        )
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Parallel satellite data processing completed in {elapsed_time:.2f} seconds.")

    # Concatenate results into a single dataframe
    return pd.concat(results)


def save_sat_data(HIST_RANGE: tuple, list_locations: list, file_path: str):
    """
    Retrieves and saves Remote sensing data for a range of years & loactions in parallel using the GEE python API as a parquet file.

    Args:
    - HIST_RANGE (tuple): A tuple specifying the start and end years of the time period of interest.
    - list_locations (list): A list of polygons defining the locations of interest.
    - file_path (str): The path where the parquet file will be saved.

    Example usage:
    ```
    >>> counties = [    ee.Geometry.Polygon(
          [
            [
                    [-122.090339, 37.422527],
                    [-122.084116, 37.422527],
                    [-122.084116, 37.417443],
                    [-122.090339, 37.417443],
                    [-122.090339, 37.422527],
              ]
          ]
      ),
      ee.Geometry.Polygon(
          [
            [
                    [-96.711303, 43.572573],
                    [-96.702557, 43.572573],
                    [-96.702557, 43.565838],
                    [-96.711303, 43.565838],
                    [-96.711303, 43.572573],
              ]
          ]
      ),
      ee.Geometry.Polygon(
            [
                [
                    [-112.062989, 33.388366],
                    [-112.058849, 33.388366],
                    [-112.058849, 33.384209],
                    [-112.062989, 33.384209],
                    [-112.062989, 33.388366],
              ]
          ]
      ),
      ee.Geometry.Polygon(
          [
            [
                    [-87.687279, 41.865074],
                    [-87.681543, 41.865074],
                    [-87.681543, 41.859338],
                    [-87.687279, 41.859338],
                    [-87.687279, 41.865074],
              ]
          ]
      ),
      ee.Geometry.Polygon(
          [
            [
                    [-71.144802, 42.354508],
                    [-71.138579, 42.354508],
                    [-71.138579, 42.349424],
                    [-71.144802, 42.349424],
                    [-71.144802, 42.354508],
              ]
          ]
      ),
      ee.Geometry.Polygon(
          [
                [
                    [-97.432956, 27.808077],
                    [-97.426733, 27.808077],
                    [-97.426733, 27.802655],
                    [-97.432956, 27.802655],
                    [-97.432956, 27.808077],
              ]
          ]
      )
    ]
    >>> save_sat_data((2019,2021), counities, "data/sat_data.parquet")
    ```
    """
    # Get the yield data
    sat_data = get_sat_all_locations(HIST_RANGE, counties)

    # Check if the path is valid
    if not os.path.exists(os.path.dirname(file_path)):
        # Create it using os.makedirs()
        os.makedirs(os.path.dirname(file_path))

    # Save the yield data as a parquet file
    sat_data.to_parquet(file_path)

    print(f"Sat data saved to {os.path.abspath(file_path)}")


# Main :
if __name__ == "__main__":

    ee.Initialize()

    counties = [
        ee.Geometry.Polygon(
            [
                [
                    [-122.090339, 37.422527],
                    [-122.084116, 37.422527],
                    [-122.084116, 37.417443],
                    [-122.090339, 37.417443],
                    [-122.090339, 37.422527],
                ]
            ]
        ),
        ee.Geometry.Polygon(
            [
                [
                    [-96.711303, 43.572573],
                    [-96.702557, 43.572573],
                    [-96.702557, 43.565838],
                    [-96.711303, 43.565838],
                    [-96.711303, 43.572573],
                ]
            ]
        ),
        ee.Geometry.Polygon(
            [
                [
                    [-112.062989, 33.388366],
                    [-112.058849, 33.388366],
                    [-112.058849, 33.384209],
                    [-112.062989, 33.384209],
                    [-112.062989, 33.388366],
                ]
            ]
        ),
        ee.Geometry.Polygon(
            [
                [
                    [-87.687279, 41.865074],
                    [-87.681543, 41.865074],
                    [-87.681543, 41.859338],
                    [-87.687279, 41.859338],
                    [-87.687279, 41.865074],
                ]
            ]
        ),
        ee.Geometry.Polygon(
            [
                [
                    [-71.144802, 42.354508],
                    [-71.138579, 42.354508],
                    [-71.138579, 42.349424],
                    [-71.144802, 42.349424],
                    [-71.144802, 42.354508],
                ]
            ]
        ),
        ee.Geometry.Polygon(
            [
                [
                    [-97.432956, 27.808077],
                    [-97.426733, 27.808077],
                    [-97.426733, 27.802655],
                    [-97.432956, 27.802655],
                    [-97.432956, 27.808077],
                ]
            ]
        ),
    ]

    results = get_sat_all_locations([2010, 2011], counties)

    print(results)
