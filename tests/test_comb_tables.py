import unittest

import pandas as pd

from src.comb_tables import CombineTables


class TestCombineTables(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCombineTables, self).__init__(*args, **kwargs)
        self.combine = CombineTables()

    def test_map_resort_locations(self):

        self.combine.map_resort_location()

        self.assertIsInstance(self.combine.df_mountains, pd.core.frame.DataFrame)
        self.assertTrue("Location" in self.combine.df_mountains.columns)

    def test_add_groomed_col(self):
        
        self.combine.add_groomed_col()

        self.assertIsInstance(self.combine.df_trails, pd.core.frame.DataFrame)
        self.assertTrue("Groomed" in self.combine.df_trails.columns)

    def test_merge_data_frames(self):

        df_merged = self.combine.merge_data_frames()

        self.assertIsInstance(df_merged, pd.core.frame.DataFrame)

        self.assertEqual(len(df_merged), 2125, msg="Missing trails in merged DataFrame")
        
        self.assertEqual(df_merged.shape[1], 19, msg="Incorrect number of columns in merged DataFrame")
