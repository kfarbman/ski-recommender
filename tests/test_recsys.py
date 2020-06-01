import unittest

from web_app.recsys import SkiRunRecommender
import pandas as pd
import numpy as np


class TestSkiRunRecommender(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSkiRunRecommender, self).__init__(*args, **kwargs)
        self.recsys = SkiRunRecommender()

    def test_load_resort_data(self):
        """
        GIVEN merged trail and mountain data

        WHEN data is imported into script

        THEN test if data structure is a DataFrame
        
        """
        df_trails = self.recsys.load_resort_data()

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

    def test_dummy_features(self):
        """
        GIVEN merged trail and mountain data

        WHEN data is dummied into categorical values

        THEN test if data structure is a DataFrame
            and original columns were removed
            and specified columns are in DataFrame
        """

        LST_DUMMIED_COLUMNS = ['Bottom Elev (ft)',
                                'Top Elev (ft)',
                                'Slope Length (ft)',
                                'Lifts',
                                'Percent Blacks',
                                'Percent Blues',
                                'Percent Double Blacks',
                                'Percent Greens',
                                'Percent Terrain Parks',
                                'Price',
                                'Difficulty_Black',
                                'Difficulty_Blue',
                                'Difficulty_Double Black',
                                'Difficulty_Green',
                                'Groomed_Groomed',
                                'Groomed_Ungroomed',
                                'Location_CA',
                                'Location_CO',
                                'Location_NM',
                                'Location_NV',
                                'Location_WY',
                                'Resort_Alpine Meadows',
                                'Resort_Arapahoe Basin',
                                'Resort_Aspen Snowmass',
                                'Resort_Bald Mountain',
                                'Resort_Beaver Creek',
                                'Resort_Copper',
                                'Resort_Crested Butte',
                                'Resort_Diamond Peak',
                                'Resort_Eldora',
                                'Resort_Jackson Hole',
                                'Resort_Loveland',
                                'Resort_Monarch',
                                'Resort_Steamboat',
                                'Resort_Taos',
                                'Resort_Telluride',
                                'Resort_Vail',
                                'Resort_Winter Park',
                                'Resort_Wolf Creek']

        df_dummy = self.recsys.load_resort_data()

        df_dummy = self.recsys.dummy_features(df=df_dummy)

        # Test if data is in DataFrame format
        self.assertIsInstance(df_dummy, pd.core.frame.DataFrame)

        # Test if original features were removed
        self.assertTrue(all([col not in df_dummy.columns for col in self.recsys.DUMMY_FEATURES]))

        # Test if all columns are in DataFrame
        self.assertTrue(all([col in df_dummy.columns for col in LST_DUMMIED_COLUMNS]))

    def test_transform_features(self):
        """
        GIVEN a dummied DataFrame 

        WHEN features are transformed

        THEN test if standard deviation is 1 and mean is 0
        
        """
        df_transform = pd.read_csv("./tests/test_transform_features_20200421.csv")

        X_transform = self.recsys.transform_features(df=df_transform, features=list(df_transform.columns))

        # Test if standard deviation is 1
        self.assertAlmostEqual(round(np.std(X_transform)), 1, places=2)

        # Test if mean is 0
        self.assertAlmostEqual(np.mean(X_transform), 0, places=2)


    def test_mountain_recommendations(self):
        """
        GIVEN a dummied, transformed DataFrame

        WHEN mountain recommendations are requested

        THEN test if requested row is a DataFrame
            and if the recommended mountains data structure is a list
        
        """
        requested_row, mountain_recs = self.recsys.mountain_recommendations(index=2)

        self.assertIsInstance(requested_row, pd.core.frame.DataFrame)
        self.assertIsInstance(mountain_recs, list)

    def test_trail_recommendations(self):
        """
        GIVEN a dummied, transformed DataFrame

        WHEN trail recommendations are requested

        THEN test if returned data structure is a DataFrame 
        
        """        
        df_total = self.recsys.trail_recommendations(index=1000, n=5, resort="Alpine Meadows", color=None)

        self.assertIsInstance(df_total, pd.core.frame.DataFrame)
