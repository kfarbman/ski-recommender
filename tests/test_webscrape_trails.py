import unittest

from src.webscrape_trails import WebscrapeTrails
import pandas as pd
import numpy as np


class TestWebscrapeTrails(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestWebscrapeTrails, self).__init__(*args, **kwargs)
        self.webscrape = WebscrapeTrails()
    
    def test_create_resort_urls(self):
        """
        Test if resort URL's are in list format
        """
        
        lst_resort_urls = self.webscrape.create_resort_urls()

        self.assertIsInstance(lst_resort_urls, list)
        self.assertEqual(len(lst_resort_urls), 72)
    
    def test_make_tables(self):
        """
        Test if webscraped trail data is in DataFrame format
        Test if columns are in DataFrame
        """

        TEST_URL = "https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green"
        
        df_trails = self.webscrape.make_tables(URL=TEST_URL)

        df_trails.to_csv("DEV.csv", header=True, index=False)

        self.assertIsInstance(df_trails, pd.core.frame.DataFrame)

        test_cols = ['Trail Name', 'Bottom Elev (ft)', 'Top Elev (ft)', 'Vertical Drop (ft)', 'Length (mi)', 'URL']

        self.assertTrue(all([col in df_trails.columns for col in test_cols]))
    
    def test_rename_resorts(self):
        """
        Test resort gets renamed correctly
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

        self.assertTrue("Resort" in df_trails.columns)
        self.assertTrue(all(df_trails["Resort"] == "Beaver Creek"))
