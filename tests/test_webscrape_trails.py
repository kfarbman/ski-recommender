import unittest

import pandas as pd
from src.webscrape_trails import WebscrapeTrails


class TestWebscrapeTrails(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWebscrapeTrails, self).__init__(*args, **kwargs)
        self.webscrape = WebscrapeTrails()

    def test_get_mountain_data(self):
        """
        GIVEN a resort URL

        WHEN trail data is requested

        THEN test if data structure is a DataFrame
            and all columns exist in formatted DataFrame

        """

        TEST_URL = "https://jollyturns.com/resort/united-states-of-america/aspen-snowmass/skiruns-green"

        df_trails = self.webscrape.request_resort_data(URL=TEST_URL)

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

        test_lst_cols = [
            "Name",
            "Top",
            "Bottom",
            "Vertical drop",
            "Length",
            "URL",
        ]

        self.assertTrue(all([col in df_trails.columns for col in test_lst_cols]))
