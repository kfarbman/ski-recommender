import unittest

import pandas as pd

from src.comb_tables import CombineTables


class TestCombineTables(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCombineTables, self).__init__(*args, **kwargs)
        self.combine = CombineTables()

    def test_add_groomed_col(self):
        df_trails = pd.read_csv("./data/combined_data_20200421.csv")
        
        df_trails = self.combine.add_groomed_col(df=df_trails)

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)
        self.assertTrue("Groomed" in df_trails.columns)
