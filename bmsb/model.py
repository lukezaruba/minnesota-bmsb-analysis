# -*- coding: utf-8 -*-
"""Performs simulation of BMSB spread via Monte Carlo simulation."""

import os

import arcgis
import arcpy
import pandas as pd
from random import random

from pandas import DataFrame
from typing import List

__author__ = "Luke Zaruba"
__credits__ = ["Luke Zaruba", "Mattie Gisselbeck"]
__status__ = "Development"


class Simulation:
    def __init__(self, features, gdb, table_name) -> None:
        self.features = features
        self.gdb = gdb
        self.table_name = table_name

    def configure(self) -> None:
        ...
        # Calculate lags - _calculate_lags()
        # Calculate weights - _calculate_weights()
        # Calculate huff - (Wi/Dij) / sum((Wi/Dij))
        # Set starting presence

    def monte_carlo(self, num_sims: int) -> None:
        # Get Initial List of Starting Presence
        starting_presence = list(df.loc[df["StartPresence"] == 1]["StartPresence"])

        # Run Sims
        for i in range(num_sims):
            self._run_single_sim()

    @staticmethod
    def _run_single_sim(df: DataFrame, starting_presence: List) -> None:
        # Loop through Rows & Simulate Transfer
        for index, row in df.iterrows():
            if row["StartPresence"] == 1:
                # Generate Random Number
                n = random()

                # Check if n < Huff
                if n < row["Huff"]:
                    df.loc[index, "EndPresence"] = 1
                    df.loc[index, "TransmissionCount"] += 1

        # Get List of Cities with End Presence
        end_presence = list(df.loc[df["EndPresence"] == 1]["To"])

        # Reset Starting Presence to 0
        df["StartPresence"] = 0

        # Set New Starting Presence
        df.loc[df["From"].isin(end_presence), ["StartPresence"]] = 1

        # If All Vals are 0, reset to initial settings
        if (df["Starting Presence"] == 0).all() == True:
            df["Starting Presence"] = starting_presence

        # Based on Huff/P, simulate if transition cccurs
        # If occurs, transition count += 1 & ending presence = 1
        # Set starting presence to 1 for every city that had at least 1 ending presence
        # Get list of unique cities with ending preseence of 1, use that to select in the "from"
        # Reset ending presence to 0

    def _calculate_weights(self) -> None:
        # Calculate Wi ("attractiveness")
        ...
