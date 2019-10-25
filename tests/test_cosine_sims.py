import unittest

from src.cosine_sims import CosineSims
import pandas as pd
import numpy as np


class TestCosineSims(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCosineSims, self).__init__(*args, **kwargs)
        self.cs = CosineSims()

    def test_load_pickle_file(self):

        df_resorts = self.cs.load_pickle_file()

        self.assertIsInstance(df_resorts, pd.core.frame.DataFrame)

    def test_transform_data(self):

        df_resorts = self.cs.load_pickle_file()

        X_train = self.cs.transform_data(df=df_resorts)

        self.assertIsInstance(X_train, np.ndarray)

    def test_cos_sim_recommendations_resort(self):
        
        df_resorts = self.cs.load_pickle_file()

        X_train = self.cs.transform_data(df=df_resorts)
     
        df_recs = self.cs.cos_sim_recommendations_resort(
            df=df_resorts, trail_name='Sorensen Park', resort_name='Winter Park', X=X_train, n=5, resort='Winter Park')

        self.assertIsInstance(df_recs, pd.core.frame.DataFrame)
