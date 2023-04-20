# -*- coding: utf-8 -*-
"""Simplifies the extraction, transformation, and loading of data into a local FGDB."""

import os

import pandas as pd
import requests

import arcgis
import arcpy

from os import PathLike
from pandas import DataFrame, Series
from typing import List

__author__ = "Luke Zaruba"
__credits__ = ["Luke Zaruba", "Mattie Gisselbeck"]
__status__ = "Development"


def load_raster():
    ...


class WeatherLoader:
    """
    A class used to extract and transform daily MN weather data automatically.

    Methods
    -------
    multi_month(months, year)
        Class method. Runs extraction/transformation on multiple months.
    load(geodatabase, fc_name, df)
        Static method. Loads df to geodatabase.
    _extractColumn(df, field)
        Static, private method. Used for converting JSON to DataFrame.
    extract()
        Runs the extraction process for the data and returns as either JSON or DataFrame.
    transform()
        Performs QAQC Process on DataFrame.
    aggregate()
        Aggregates and calculates average values for stations.

    Example
    -------
    > weather_etl = WeatherLoader(3, 2022)
    > raw_df = weather_etl.extract()
    > transformed_df = weather_etl.transform()
    > aggregated_df = weather_etl.aggregate()
    > WeatherLoader.load("/path/to/example.gdb", "feature_class", aggregated_df)
    """

    def __init__(self, month=1, year=2023):
        """Initializes the WeatherLoader class.

        :param int month: Month that data will be queried for, defaults to 1
        :param int year: Year that data will be queried for, defaults to 2023
        """
        self.month = month
        self.year = year

        # Set Base URL
        self.url = r"https://mesonet.agron.iastate.edu/api/1/daily.geojson?network=MN_RWIS&month=_M_&year=_Y_".replace(
            "_M_", str(self.month)
        ).replace(
            "_Y_", str(self.year)
        )

    @classmethod
    def multi_month(cls, months: List[int], year: int) -> DataFrame:
        """Extracts daily values across multiple months, cleans, and aggregates into a single df.

        :param List[int] months: Months that data will be queried for
        :param int year: Year that data will be queried for
        :return DataFrame: _description_
        """
        # Loop through months, clean, create df, and append to list
        aggregated_df = pd.DataFrame(
            columns=("station", "name", "x", "y", "max_tmpf", "min_tmpf", "precip")
        )

        for m in months:
            # Create Monthly Loader, Extract & Clean
            wl = WeatherLoader(m, year)
            wl.extract()
            wl.transform()

            # Append Cleaned DF to Final DF
            aggregated_df = pd.concat([wl.df, aggregated_df], axis=0)

        # Perform Aggregation by Station
        agg_functions = {
            "station": "first",
            "name": "first",
            "x": "first",
            "y": "first",
            "max_tmpf": "mean",
            "min_tmpf": "mean",
            "precip": "mean",
        }

        # Perform Aggregation
        aggregated_df = aggregated_df.groupby(aggregated_df["station"]).aggregate(
            agg_functions
        )

        # Return DF
        return aggregated_df

    @staticmethod
    def load(geodatabase: PathLike, fc_name: str, df: DataFrame) -> None:
        """Loads aggregated data to feature class.

        :param PathLike geodatabase: Path to the geodatabase where the output feature class will be stored
        :param str fc_name: Name of the output feature class
        :param DataFrame df: Input dataframe that will be converted to a feature class
        """
        # Convert Weather Observations from DF to SEDF
        sedf = arcgis.GeoAccessor.from_xy(df, "x", "y")

        # Convert Weather Observations from SEDF to FC
        sedf.spatial.to_featureclass(location=os.path.join(geodatabase, fc_name))

    @staticmethod
    def _extractToCol(df: DataFrame, field: Series) -> None:
        """Function to extract fields from dicts that are columns in DF.

        :param DataFrame df: DataFrame containing raw values that need to be seperated
        :param Series field: Name of Series/column that will be created
        """
        df[field] = df["properties"].apply(lambda x: dict(x)[field])

    def aggregate(self) -> DataFrame:
        """Aggregates daily values to monthly summary at each weather station.

        :return DataFrame: DataFrame containing aggregated data is returned
        """
        # Define Aggregate Functions
        agg_functions = {
            "station": "first",
            "name": "first",
            "x": "first",
            "y": "first",
            "max_tmpf": "mean",
            "min_tmpf": "mean",
            "precip": "mean",
        }

        # Perform Aggregation
        self.aggregated_df = self.df.groupby(self.df["station"]).aggregate(
            agg_functions
        )

        # Return DF
        return self.aggregated_df

    def extract(self) -> None:
        """Extracts data from API and performs miminal cleaning to return as a DataFrame."""
        # Get Response & Convert to DF
        response = requests.get(self.url)
        json = response.json()["features"]
        df_raw = pd.DataFrame.from_records(json)

        # Series Conversion from Dicts to Actual Vals
        desiredSeries = ["station", "date", "max_tmpf", "min_tmpf", "precip", "name"]

        for s in desiredSeries:
            self._extractToCol(df_raw, s)

        # Extract Geometries
        df_raw["x"] = df_raw["geometry"].apply(lambda x: dict(x)["coordinates"][0])
        df_raw["y"] = df_raw["geometry"].apply(lambda x: dict(x)["coordinates"][1])

        # Copy Useful Columns to new DF
        self.df = df_raw[
            ["station", "date", "max_tmpf", "min_tmpf", "precip", "name", "x", "y"]
        ].copy()

    def transform(self) -> None:
        """Transforms and performs QAQC on raw DataFrame to create cleaned DataFrame."""
        # Fill NA Precip Values
        self.df["precip"].fillna(0, inplace=True)

        # Drop Rows where 'precip' < 0
        self.df = self.df.loc[self.df["precip"] >= 0]

        # Drop Rows with Null 'Latitude' or 'Longitude'
        self.df = self.df.dropna(subset=["x", "y", "max_tmpf", "min_tmpf"])

        # Convert Data Types
        self.df["station"] = self.df["station"].astype(str)
        self.df["name"] = self.df["name"].astype(str)
        self.df["date"] = self.df["date"].astype("datetime64[ns]")

        # Drop Rows where Lat/Lon are Outside MN BBox
        self.df = self.df.loc[self.df["x"] > -97.5]
        self.df = self.df.loc[self.df["x"] < -89.0]
        self.df = self.df.loc[self.df["y"] > 43.0]
        self.df = self.df.loc[self.df["y"] < 49.5]


class ObservationLoader:
    def __init__(self):
        ...

    @staticmethod
    def load():
        ...

    def extract(self):
        ...

    def transform(self):
        ...


class Aggregator:
    def __init__(self, cities, landcover, elevation, weather, observations) -> None:
        self.cities = cities
        self.landcover = landcover
        self.elevation = elevation
        self.weather = weather
        self.observations = observations

    @staticmethod
    def raster_agg(raster, features, unique_id, table, quantitaive=True):
        ...

    @staticmethod
    def point_agg_near(points, features, table):
        ...

    @staticmethod
    def point_agg_within(points, features, table):
        ...

    def aggregate(self) -> None:
        ...
