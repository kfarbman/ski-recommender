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

    def rename_resorts(self, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Rename resorts for recommendation system

        INPUT
            df: Pandas DataFrame
        OUTPUT
            Pandas DataFrame, with resort_name column altered
        """

        # TODO: Better way to slice strings than arbitrary column
        df["Resort"] = df["URL"].str.split("/", expand=True)[5]

        dict_webscrape_trail_names = {
            "palisades-tahoe-(alpine-meadows)": "Alpine Meadows",
            "arapahoe-basin": "Arapahoe Basin",
            "aspen-snowmass": "Aspen Snowmass",
            "bald-mountain": "Bald Mountain",
            "beaver-creek-resort": "Beaver Creek",
            "copper-mountain-resort": "Copper",
            "crested-butte-mountain-resort": "Crested Butte",
            "diamond-peak": "Diamond Peak",
            "eldora-mountain-resort": "Eldora",
            "jackson-hole": "Jackson Hole",
            "loveland-ski-area": "Loveland",
            "monarch-ski-area": "Monarch",
            "steamboat-ski-resort": "Steamboat",
            "taos-ski-valley": "Taos",
            "telluride-ski-resort": "Telluride",
            "vail-ski-resort": "Vail",
            "winter-park-resort": "Winter Park",
            "wolf-creek-ski-area": "Wolf Creek",
        }

        df["Resort"] = df["Resort"].map(dict_webscrape_trail_names).fillna(df["Resort"])

        # Drop URL column
        df.drop("URL", axis=1, inplace=True)

        # Reset index
        df = df.reset_index(drop=True)

        return df

    def save_trail_data(self, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Save trail data to Parquet file
        """

        current_date = date.today().strftime("%Y%m%d")

        df.to_parquet(
            f"{self.CURRENT_DIRECTORY}/data/trail_data_{current_date}.parquet",
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

    # Capitalize trail difficulty
    df_trails["Difficulty"] = df_trails["Difficulty"].str.title()

    # Remove trailing strings from metric columns
    df_trails["Top"] = df_trails["Top"].str.replace(" ft", "").astype(int)
    df_trails["Bottom"] = df_trails["Bottom"].str.replace(" ft", "").astype(int)
    df_trails["Vertical drop"] = (
        df_trails["Vertical drop"].str.replace(" ft", "").astype(int)
    )

    # TODO: Convert all to feet when removing strings
    df_trails["Length"] = (
        df_trails["Length"].str.replace(" mi", "").str.replace(" ft", "").astype(float)
    )

    # Get resort name for trails
    df_trails = ws.rename_resorts(df=df_trails)

    # Count total runs per resort by difficulty
    df_trails["Total Runs"] = df_trails.groupby(["Resort", "Difficulty"])[
        "Name"
    ].transform("count")

    import pdb

    pdb.set_trace()

    # Create count of runs by difficulty per resort
    df_total_trails_by_difficulty = pd.crosstab(
        df_trails["Resort"], df_trails["Difficulty"]
    ).reset_index()

    # Combine trails and aggregate trail metrics
    df_combined = pd.merge(
        df_trails, df_total_trails_by_difficulty, on="Resort", how="inner"
    )

    # Format trail values
    lst_formatted_cols = [
        "Bottom Elev (ft)",
        "Top Elev (ft)",
        "Vertical Drop (ft)",
        "Length (mi)",
    ]
    df_resorts[lst_formatted_cols] = df_resorts[lst_formatted_cols].astype("float64")

    # Convert run distance from miles to feet
    df_resorts.loc[df_resorts["Length (mi)"] < 1, "Length (mi)"] = (
        df_resorts["Length (mi)"] * 5280
    )

    # Format trail values as integers
    df_resorts[lst_formatted_cols] = df_resorts[lst_formatted_cols].astype(int)

    # Rename Length column
    df_resorts.rename(columns={"Length (mi)": "Slope Length (ft)"}, inplace=True)

    # Calculate average steepness
    df_resorts["Average Steepness"] = (
        df_resorts["Vertical Drop (ft)"] / df_resorts["Slope Length (ft)"]
    ).round(2)

    # Save trail data
    # ws.save_trail_data(df=df_resorts)
