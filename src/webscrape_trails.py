"""
Request trail data from all resorts
"""

import os
import time
from datetime import date

import pandas as pd

# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


class WebscrapeTrails:
    def __init__(self):

        self.CURRENT_DIRECTORY = os.getcwd()

        self.MAIN_URL = "https://jollyturns.com/resort/united-states-of-america"

        self.ALPINE_MEADOWS_URL = f"{self.MAIN_URL}/palisades-tahoe-(alpine-meadows)/"
        self.ARAPAHOE_BASIN_URL = f"{self.MAIN_URL}/arapahoe-basin/"
        self.ASPEN_SNOWMASS_URL = f"{self.MAIN_URL}/aspen-snowmass/"
        self.BALD_MOUNTAIN_URL = f"{self.MAIN_URL}/bald-mountain/"
        self.BEAVER_CREEK_URL = f"{self.MAIN_URL}/beaver-creek-resort/"
        self.COPPER_URL = f"{self.MAIN_URL}/copper-mountain-resort/"
        self.CRESTED_BUTTE_URL = f"{self.MAIN_URL}/crested-butte-mountain-resort/"
        self.DIAMOND_PEAK_URL = f"{self.MAIN_URL}/diamond-peak/"
        self.ELDORA_URL = f"{self.MAIN_URL}/eldora-mountain-resort/"
        self.JACKSON_HOLE_URL = f"{self.MAIN_URL}/jackson-hole/"
        self.LOVELAND_URL = f"{self.MAIN_URL}/loveland-ski-area/"
        self.MONARCH_URL = f"{self.MAIN_URL}/monarch-ski-area/"
        self.STEAMBOAT_URL = f"{self.MAIN_URL}/steamboat-ski-resort/"
        self.TAOS_URL = f"{self.MAIN_URL}/taos-ski-valley/"
        self.TELLURIDE_URL = f"{self.MAIN_URL}/telluride-ski-resort/"
        self.VAIL_URL = f"{self.MAIN_URL}/vail-ski-resort/"
        self.WINTER_PARK_URL = f"{self.MAIN_URL}/winter-park-resort/"
        self.WOLF_CREEK_URL = f"{self.MAIN_URL}/wolf-creek-ski-area/"

        self.URLs = [
            self.ALPINE_MEADOWS_URL,
            self.ARAPAHOE_BASIN_URL,
            self.ASPEN_SNOWMASS_URL,
            self.BALD_MOUNTAIN_URL,
            self.BEAVER_CREEK_URL,
            self.COPPER_URL,
            self.CRESTED_BUTTE_URL,
            self.DIAMOND_PEAK_URL,
            self.ELDORA_URL,
            self.JACKSON_HOLE_URL,
            self.LOVELAND_URL,
            self.MONARCH_URL,
            self.STEAMBOAT_URL,
            self.TAOS_URL,
            self.TELLURIDE_URL,
            self.VAIL_URL,
            self.WINTER_PARK_URL,
            self.WOLF_CREEK_URL,
        ]

        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")

        self.browser = webdriver.Chrome(options=self.chrome_options)

        self.lst_run_difficulty = [
            "skiruns-green",
            "skiruns-blue",
            "skiruns-black",
            "skiruns-double-black",
        ]

        self.blank_value = "__NA__"

    def make_tables(self, URL: str) -> pd.core.frame.DataFrame:
        """
        Inputs:
            URL from URLs (str)
        Outputs:
            Pandas DataFrame of ski resort information
        """

        print(URL)
        self.browser.get(URL)
        time.sleep(3)
        render = self.browser.page_source

        try:
            # Use pd.read_html to format trail metrics from HTML source
            df_trails = pd.read_html(render)[0]
        except ValueError:
            print(f"No data for {URL}")
            return None

        df_trails["URL"] = URL
        df_trails["Difficulty"] = URL.split("skiruns-")[1]

        return df_trails

    def save_trail_data(self, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Save trail data to Parquet file
        """

        current_date = date.today().strftime("%Y%m%d")

        df.to_parquet(
            f"{self.CURRENT_DIRECTORY}/data/trail_data_extract_{current_date}.parquet",
            index=False,
        )


if __name__ == "__main__":

    ws = WebscrapeTrails()

    # Create list of all trail URL's
    lst_trail_urls = [
        f"{url}{difficulty}" for url in ws.URLs for difficulty in ws.lst_run_difficulty
    ]

    # Request trail data from all ski resorts
    # TODO: Request resorts in parallel?
    lst_trail_data = [ws.make_tables(URL=url) for url in tqdm(lst_trail_urls)]

    # Combine trail data
    df_trails = pd.concat(lst_trail_data)

    ws.save_trail_data(df=df_trails)
