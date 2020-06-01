import unittest

from src.webscrape_trails import WebscrapeTrails
import pandas as pd
import numpy as np


class TestWebscrapeTrails(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWebscrapeTrails, self).__init__(*args, **kwargs)
        self.webscrape = WebscrapeTrails()
        
    def test_make_tables(self):
        """
        GIVEN a URL for trails at a resort

        WHEN trails are webscraped and processed

        THEN test if data structure is a DataFrame
            and if specified columns exist in DataFrame
        """
    
        TEST_URL = "https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green"
        
        df_trails = self.webscrape.make_tables(URL=TEST_URL)

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

        test_cols = ['Trail Name', 'Bottom Elev (ft)', 'Top Elev (ft)', 'Vertical Drop (ft)', 'Length (mi)', 'URL']

        self.assertTrue(all([col in df_trails.columns for col in test_cols]))
    
    def test_rename_resorts(self):
        """
        GIVEN a Pandas DataFrame of trail data

        WHEN resorts are renamed based on the URL

        THEN test if data structure is a DataFrame
            and Resort column is in DataFrame
            and tested resort name is Beaver Creek
        """

        df_trails = pd.DataFrame({'Trail Name': {0: '\xa0 Anderson Way ', 1: '\xa0 Bear Paw '},
                                  'Bottom Elev (ft)': {0: '8025 ft', 1: '8501 ft'},
                                  'Top Elev (ft)': {0: '8238 ft', 1: '8547 ft'},
                                  'Vertical Drop (ft)': {0: '213 ft', 1: '43 ft'},
                                  'Length (mi)': {0: '0.73 mi', 1: '0.17 mi'},
                                  'URL': {0: 'https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green',
                                          1: 'https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green'}})
        
        df_trails = self.webscrape.rename_resorts(df=df_trails)
        
        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

        self.assertTrue("Resort" in list(df_trails.columns))
        self.assertTrue(all(df_trails["Resort"] == "Beaver Creek"))
