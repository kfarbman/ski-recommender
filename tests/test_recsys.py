import unittest

from web_app.recsys import SkiRunRecommender
import pandas as pd
import numpy as np


class TestSkiRunRecommender(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSkiRunRecommender, self).__init__(*args, **kwargs)
        self.recsys = SkiRunRecommender()

    def test_load_trail_data(self):
        """
        Test loaded trail data being in DataFrame structure
        """

        df_trails = self.recsys.load_trail_data()

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

    def test_load_mountain_data(self):
        """
        Test loaded mountain data being in DataFrame structure
        """

        df_mountains = self.recsys.load_mountain_data()

        self.assertIsInstance(df_mountains, pd.core.frame.DataFrame)

    def test_mountain_recommendations(self):
        """
        Test if mountain recommendations return a DataFrame and list
        """

        requested_row, mountain_recs = self.recsys.mountain_recommendations(index=2)

        self.assertIsInstance(requested_row, pd.core.frame.DataFrame)
        self.assertIsInstance(mountain_recs, list)

    def test_trail_recommendations(self):
        """
        Test if trail recommendations return a DataFrame
        """
        
        df_total = self.recsys.trail_recommendations(index=1000, n=5, resort="Alpine Meadows", color=None)

        self.assertIsInstance(df_total, pd.core.frame.DataFrame)