"""
Request trail data from all resorts
"""

import os
import time
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm


class WebscrapeTrails:
    def __init__(self):

        self.CURRENT_DIRECTORY = os.getcwd()

        self.MAIN_URL = "https://jollyturns.com/resort/united-states-of-america"

        self.ALPINE_MEADOWS_URL = f"{self.MAIN_URL}/alpine-meadows/"
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

        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument("--no-sandbox")
        self.browser_options.add_argument("--headless")
        self.browser_options.add_argument("--disable-gpu")

        self.browser = webdriver.Chrome(options=self.browser_options)

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

        self.browser.get(URL)

        time.sleep(3)

        soup = BeautifulSoup(self.browser.page_source, "html.parser")

        X_web_trail = soup.select("table.table-striped tr")

        lst_rows = [x.text.strip() for x in X_web_trail]
        lst_rows = [i.replace("  ", "|") for i in lst_rows]
        lst_rows = [i.replace(" ft", "|") for i in lst_rows]
        lst_rows = [i.replace(" mi", "|") for i in lst_rows]

        lst_cols = [
            "Name Bottom Top Vertical rise",
            "Name Bottom Top Vertical drop Length",
            "Name Elevation",
        ]

        # Indices where headers start, separating runs by difficulty
        idx_headers = [i for i, j in enumerate(lst_rows) if j in lst_cols]

        # Create DataFrame from rows
        df_trails = pd.DataFrame(lst_rows, columns=["trail_data"]).reset_index(
            drop=True
        )

        # Expand DataFrame values into separate columns
        df_trails = df_trails["trail_data"].str.split("|", expand=True)
        df_trails.columns = [
            "Trail Name",
            "Bottom Elev (ft)",
            "Top Elev (ft)",
            "Vertical Drop (ft)",
            "Length (mi)",
            "Blank",
        ]

        df_trails.drop("Blank", axis=1, inplace=True)

        lst_difficulty = soup.select("h4")
        lst_difficulty = [l.text.strip() for l in lst_difficulty]
        lst_difficulty = [i.replace("Ski runs: ", "") for i in lst_difficulty]

        df_difficulties = pd.DataFrame(lst_difficulty, index=idx_headers)

        df_combined = pd.merge(
            df_trails, df_difficulties, left_index=True, right_index=True, how="outer"
        )

        df_combined.rename(columns={0: "Difficulty"}, inplace=True)

        df_combined["Difficulty"].fillna(method="ffill", inplace=True)

        # Remove rows which are not trail names
        df_combined = df_combined[
            ~df_combined["Trail Name"].isin(lst_cols)
        ].reset_index(drop=True)

        # Remove runs with no name and trails with __NA__ value
        df_combined = df_combined[df_combined["Trail Name"].notnull()].reset_index(
            drop=True
        )
        df_combined = df_combined[
            df_combined["Trail Name"] != self.blank_value
        ].reset_index(drop=True)

        # Remove Lifts, Restaurants, and Terrain Park
        df_combined = df_combined[
            ~df_combined["Difficulty"].isin(["Lifts", "Restaurants", "terrain park"])
        ].reset_index(drop=True)

        # Add URL
        df_combined["URL"] = URL

        return df_combined

    def rename_resorts(self, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Rename resorts for recommendation system

        INPUT
            df: Pandas DataFrame
        OUTPUT
            Pandas DataFrame, with resort_name column altered
        """

        df["Resort"] = df["URL"].str.split("united-states-of-america/", 1, expand=True)[
            1
        ]
        df["Resort"] = df["Resort"].str.split("/", 1, expand=True)[0]

        dict_webscrape_trail_names = {
            "alpine-meadows": "Alpine Meadows",
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

    # Request trail data from all ski resorts
    # TODO: Request resorts in parallel?
    lst_trail_data = [ws.make_tables(URL=url) for url in tqdm(ws.URLs)]

    # Combine trail data
    df_resorts = pd.concat(lst_trail_data)

    # Capitalize trail difficulty
    df_resorts["Difficulty"] = df_resorts["Difficulty"].str.title()

    # Get resort name for trails
    df_resorts = ws.rename_resorts(df=df_resorts)

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
