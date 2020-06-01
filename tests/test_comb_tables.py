import unittest

import pandas as pd

from src.comb_tables import CombineTables


class TestCombineTables(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCombineTables, self).__init__(*args, **kwargs)
        self.combine = CombineTables()

    def test_map_resort_locations(self):
        """
        GIVEN trail and mountain DataFrames

        WHEN location is mapped based on resort name

        THEN test if the data structure is a DataFrame
            and Location column is in DataFrame
        """

        self.combine.map_resort_location()

        self.assertIsInstance(self.combine.df_mountains, pd.core.frame.DataFrame)
        self.assertTrue("Location" in self.combine.df_mountains.columns)

    def test_add_groomed_col(self):
        """
        GIVEN trail data as DataFrame

        WHEN a Groomed column is added based on trail name

        THEN test if data structure is a DataFrame
            and Groomed column is in DataFrame
        """    

        self.combine.add_groomed_col()

        self.assertIsInstance(self.combine.df_trails, pd.core.frame.DataFrame)
        self.assertTrue("Groomed" in self.combine.df_trails.columns)

    def test_merge_data_frames(self):
        """
        GIVEN trail and mountain DataFrames

        WHEN trail and mountain DataFrames are merged

        THEN test if data structure is a DataFrame
            and new DataFrame has 2,125 trails
            and new DataFrame has 19 columns
        """

        df_merged = self.combine.merge_data_frames()

        self.assertIsInstance(df_merged, pd.core.frame.DataFrame)

        self.assertEqual(len(df_merged), 2125, msg="Missing trails in merged DataFrame")
        
        self.assertEqual(df_merged.shape[1], 19, msg="Incorrect number of columns in merged DataFrame")
