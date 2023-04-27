# -*- coding: utf-8 -*-
"""Performs simulation of BMSB spread via Monte Carlo simulation."""

import os

import pandas as pd
from random import random
from tqdm import tqdm

from pandas import DataFrame
from typing import List

__author__ = "Luke Zaruba"
__credits__ = ["Luke Zaruba", "Mattie Gisselbeck"]
__status__ = "Production"


class Simulation:
    """
    A class used to simulate BMSB spread using different spatial interaction models.

    Methods
    -------
    monte_carlo(model, num_sims, increase_prob)
        Runs entire simulation a given number of times using a specified model.
    _run_single_sim(probability_field, transition_cnt_field, starting_presence)
        Private method. Used for running a single simulation.

    Example
    -------
    > gravity_sim = Simulation(df)
    > gravity_sim_df = gravity_sim.monte_carlo("GRAVITY_SIMPLE", 100, True)
    """

    def __init__(
        self,
        df: DataFrame,
        dist_field="Distance",
        from_presence_field="BMSB Presence: From",
        from_id_field="City: From",
        from_w_field="W: From",
        to_presence_field="BMSB Presence: To",
        to_id_field="City: To",
        to_w_field="W: To",
    ) -> None:
        """Initializes the Simulation class.

        :param DataFrame df: Input dataframe for simulation
        :param str dist_field: Name of series that represents lags, defaults to "Distance"
        :param str from_presence_field: Name of series that represents origin presence, defaults to "BMSB Presence: From"
        :param str from_id_field: Name of series that represents origin ID, defaults to "City: From"
        :param str from_w_field: Name of series that represents origin weight, defaults to "W: From"
        :param str to_presence_field: Name of series that represents destination presence, defaults to "BMSB Presence: To"
        :param str to_id_field: Name of series that represents destination ID, defaults to "City: To"
        :param str to_w_field: Name of series that represents destination weight, defaults to "W: To"
        """
        self.df = df.copy()
        self.dist_field = dist_field
        self.from_presence_field = from_presence_field
        self.from_id_field = from_id_field
        self.from_w_field = from_w_field
        self.to_presence_field = to_presence_field
        self.to_id_field = to_id_field
        self.to_w_field = to_w_field

    def monte_carlo(self, model: str, num_sims: int, increase_prob=False) -> DataFrame:
        """Method used to run a monte carlo simulation.

        :param str model: Name of model to use, options are ["HUFF_SIMPLE", "HUFF_DECAY", "GRAVITY_SIMPLE"]
        :param int num_sims: The number of simulations that will be run
        :param bool increase_prob: Determines whether probability is artificially inflated by 100x, defaults to False
        :raises ValueError: Error raised when invalid model is passed
        :return DataFrame: Simulation results
        """
        # Get Initial List of Starting Presence
        starting_presence = list(self.df[self.from_presence_field])

        # Probability Fields
        if model == "HUFF_SIMPLE":
            probability_numerator = "HS: Wi/Dij"
            probability_field = "Huff: Simple"
            transition_cnt_field = "HS: Transition Count"

            # Calculate
            self.df[probability_numerator] = (
                self.df[self.to_w_field] / self.df[self.dist_field]
            )
            sum_prob_num = self.df[probability_numerator].sum()
            self.df[probability_field] = self.df[probability_numerator] / sum_prob_num

        elif model == "HUFF_DECAY":
            probability_numerator = "HD2: Wi/Dij"
            probability_field = "Huff: Decay of 2"
            transition_cnt_field = "HD2: Transition Count"

            # Calculate
            self.df[probability_numerator] = self.df[self.to_w_field] / (
                self.df[self.dist_field] ** 2
            )
            sum_prob_num = self.df[probability_numerator].sum()
            self.df[probability_field] = self.df[probability_numerator] / sum_prob_num

        elif model == "GRAVITY_SIMPLE":
            probability_numerator = "Gravity"
            probability_field = "Gravity: Probability"
            transition_cnt_field = "G: Transition Count"

            # Calculate
            self.df[probability_numerator] = (
                self.df[self.to_w_field] * self.df[self.from_w_field]
            ) / self.df[self.dist_field]
            sum_prob_num = self.df[probability_numerator].sum()
            self.df[probability_field] = self.df[probability_numerator] / sum_prob_num

        else:
            raise ValueError(
                "Model must be in ['HUFF_SIMPLE', 'HUFF_DECAY', 'GRAVITY_SIMPLE']"
            )

        # Artificially Increase Probability by 100x
        if increase_prob:
            self.df[probability_field] *= 100

        # Init Transition Count Field
        self.df[transition_cnt_field] = 0

        # Run Sims
        for i in tqdm(range(num_sims)):
            self._run_single_sim(
                probability_field, transition_cnt_field, starting_presence
            )

        # Return
        return self.df

    def _run_single_sim(
        self, probability_field: str, transition_cnt_field: str, starting_presence: List
    ) -> None:
        """Private method used to run a simgle simulation.

        :param str probability_field: Name of series that represents probability of transition
        :param str transition_cnt_field: Name of series that represents transition count
        :param List starting_presence: Name of series that represents list of starting presence
        """
        # Loop through Rows & Simulate Transfer
        for index, row in self.df.iterrows():
            if row[self.from_presence_field] == 1:
                # Generate Random Number
                n = random()

                # Check if n < probability
                if n < row[probability_field]:
                    self.df.loc[index, self.to_presence_field] = 1
                    self.df.loc[index, transition_cnt_field] += 1

        # Get List of Cities with End Presence
        end_presence = list(
            self.df.loc[self.df[self.to_presence_field] == 1][self.to_id_field]
        )

        # Reset Starting Presence to 0
        self.df[self.from_presence_field] = 0

        # Set New Starting Presence
        self.df.loc[
            self.df[self.from_id_field].isin(end_presence), [self.from_presence_field]
        ] = 1

        # If All Vals are 0, reset to initial settings
        if (self.df[self.from_presence_field] == 0).all() == True:
            self.df[self.from_presence_field] = starting_presence
