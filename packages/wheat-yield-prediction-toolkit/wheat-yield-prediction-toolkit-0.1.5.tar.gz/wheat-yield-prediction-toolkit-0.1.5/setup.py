from setuptools import find_packages, setup



setup(
    name="wheat-yield-prediction-toolkit",
    version="0.1.5",
    author="Noureddine Ech-chouky",
    author_email="noureddineechchouky@gmail.com",
    description="Wheat Yield Prediction Toolkit is a package that provides tools for predicting wheat yield at the county level in the main wheat-producing regions of the US using deep learning approaches. The package includes modules for data collection, preprocessing, modeling, and uncertainty analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nour3467/wheat-yield-prediction-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    package_data={
        "wheat_yield_prediction_toolkit": [
            "core/tmp/*.shp",
            "core/tmp/*.dbf",
            "core/tmp/*.prj",
            "core/tmp/*.shx",
            "core/tmp/*.xml",
        ]
    },
    python_requires=">=3.9",
    install_requires=[
        "tqdm",
        "geopandas",
        "pytest",
        "pandas",
        "python-dotenv",
        "pyarrow",
        "earthengine-api",
        "geemap",
        "rasterio",
        "owslib",
        "scienceplots",
        "meteostat",
        # add any other dependencies here
    ]
)
