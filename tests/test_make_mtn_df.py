import unittest

from src.make_mtn_df import MakeMountainDF
import pandas as pd
import numpy as np


class TestMakeMountainDF(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMakeMountainDF, self).__init__(*args, **kwargs)
        self.mountain = MakeMountainDF()

    def test_get_mountain_data(self):
        """
        GIVEN a resort URL

        WHEN trail data is requested

        THEN test if data structure is a DataFrame
            and all columns exist in formatted DataFrame
        
        """

        TEST_URL = "https://jollyturns.com/resort/united-states-of-america/aspen-snowmass/"

        df_ski = self.mountain.get_mountain_data(URL=TEST_URL)

        self.assertIsInstance(df_ski, pd.core.frame.DataFrame)
        
        test_lst_cols = ['black', 'blue', 'double black', 'green', 'terrain park', 'Lifts', 'Base', 'Top', 'Vertical rise', 'URL']

        self.assertTrue(all([col in df_ski.columns for col in test_lst_cols]))

    def test_format_mountain_data_frame_values(self):
        """
        GIVEN a webscraped DataFrame

        WHEN trail data is formatted

        THEN test if data structure is a DataFrame
            and all columns exist in formatted DataFrame
        
        """

        df_mountain = pd.DataFrame({'black': {0: '28'},
            'blue': {0: '49'},
            'double black': {0: '30'},
            'green': {0: '8'},
            'terrain park': {0: '3'},
            'Lifts': {0: '17'},
            'Base': {0: '8116'},
            'Top': {0: '12542'},
            'Vertical rise': {0: '4426'},
            'URL': {0: 'https://jollyturns.com/resort/united-states-of-america/aspen-snowmass/'}}
            )
        
        df_mountain = self.mountain.format_mountain_data_frame_values(df=df_mountain)

        self.assertIsInstance(df_mountain, pd.core.frame.DataFrame)

        test_formatted_cols = ["Top", "Base", "Lifts", "Vertical rise", "black","blue", "double black", "green", "terrain park"]

        self.assertTrue(all(["int" == df_mountain[col].dtype for col in test_formatted_cols]))
