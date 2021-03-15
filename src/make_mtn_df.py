"""
Webscrape mountain statistics from JollyTurns

1. Request all mountain data
2. Format/ preprocess data
3. Save data to CSV
"""

import os
import time
import warnings
from datetime import date

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

from src.webscrape_trails import WebscrapeTrails

warnings.filterwarnings("ignore")


class MakeMountainDF:
    def __init__(self):

        self.CURRENT_DIRECTORY = os.getcwd()

        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument("--no-sandbox")
        self.browser_options.add_argument("--headless")
        self.browser_options.add_argument("--disable-gpu")

        self.browser = webdriver.Chrome(options=self.browser_options)

        # 2020 ticket prices, fetched manually
        self.dict_resort_prices = {
            "Alpine Meadows": 169,
            "Arapahoe Basin": 109,
            "Aspen Snowmass": 179,
            "Bald Mountain": 145,
            "Beaver Creek": 209,
            "Copper": 119,
            "Crested Butte": 129,
            "Diamond Peak": 104,
            "Eldora": 140,
            "Jackson Hole": 165,
            "Loveland": 89,
            "Monarch": 94,
            "Steamboat": 199,
            "Taos": 110,
            "Telluride": 149,
            "Vail": 209,
            "Winter Park": 139,
            "Wolf Creek": 76,
        }

    def get_mountain_data(self, URL: str) -> pd.core.frame.DataFrame:
        """
        Inputs:
            URL from URLs (str)
        Outputs:
            Pandas DataFrame of ski resort information
        """

        self.browser.get(URL)

        time.sleep(3)

        soup = BeautifulSoup(self.browser.page_source, "html.parser")

        # JollyTurns parsing (runs breakdown)
        X_runs = soup.select(
            "resort-glance div.row div.col-xs-12 div.row.text-left.statistics.ng-scope span.ng-binding"
        )
        lst_runs = [run.text for run in X_runs]
        lst_runs = [run.replace(" ski runs: ", "") for run in lst_runs]
        df_ski_runs = pd.DataFrame({"Runs": lst_runs[0::2], "total": lst_runs[1::2]})
        df_ski_runs = df_ski_runs.set_index("Runs").T.reset_index(drop=True)

        # JollyTurns parsing (Chairlifts / total runs)
        X_lifts = soup.select("div.content-in-circle")
        lst_lifts = [lift.text.lstrip() for lift in X_lifts]
        df_lifts = pd.DataFrame({"Lifts": lst_lifts[0]}, index=[0])

        # JollyTurns parsing (Elevations)
        X_elevations = soup.select("resort-glance div.row div.col-xs-12 table tr td")
        lst_elevations = [
            elevation.text for elevation in X_elevations if "Lift" not in elevation.text
        ]
        lst_elevations = [
            elevation.replace(" \xa0", "") for elevation in lst_elevations
        ]
        lst_elevations = [elevation.replace(" ft", "") for elevation in lst_elevations]
        lst_elevations = [elevation.replace(":", "") for elevation in lst_elevations]

        df_elevations = pd.DataFrame(
            {"Elevation": lst_elevations[0::2], "Total": lst_elevations[1::2]}
        )
        df_elevations = df_elevations.set_index("Elevation").T.reset_index(drop=True)

        # Combine total runs, total lifts, and elevation data
        df_ski = pd.concat([df_ski_runs, df_lifts, df_elevations], axis=1)

        df_ski["URL"] = URL

        return df_ski

    def format_mountain_data_frame_values(
        self, df: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """
        Pivot DataFrame, and format values

        Input
            df: Pandas DataFrame

        Output
            Formatted Pandas DataFrame
        """

        lst_columns = [
            "Top",
            "Base",
            "Lifts",
            "Vertical rise",
            "black",
            "blue",
            "double black",
            "green",
            "terrain park",
        ]

        df[lst_columns] = df[lst_columns].fillna(0)

        df[lst_columns] = df[lst_columns].astype("int")

        return df

    def save_mountain_data(
        self, df: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """
        Save formatted mountain data to Parquet file
        """

        current_date = date.today().strftime("%Y%m%d")

        df.to_parquet(
            f"{self.CURRENT_DIRECTORY}/data/mountain_data_{current_date}.parquet",
            index=False,
        )


if __name__ == "__main__":

    mountain = MakeMountainDF()

    ws = WebscrapeTrails()

    # Request mountain data from all resorts
    lst_mountain_data = [mountain.get_mountain_data(URL=url) for url in tqdm(ws.URLs)]

    # Combine mountain data
    df_mountain = pd.concat(lst_mountain_data).reset_index(drop=True)

    df_mountain = ws.rename_resorts(df=df_mountain)

    # Fill prices
    df_mountain["Price"] = df_mountain["Resort"].map(mountain.dict_resort_prices)

    # Convert column data types
    df_mountain = mountain.format_mountain_data_frame_values(df=df_mountain)

    # Convert total runs to percentage of total runs per resort
    lst_run_types = ["black", "blue", "double black", "green", "terrain park"]
    df_mountain["Total Runs"] = df_mountain[lst_run_types].sum(axis=1)
    df_mountain[lst_run_types] = (
        df_mountain[lst_run_types]
        .div(df_mountain["Total Runs"], axis=0)
        .mul(100)
        .round()
        .astype(int)
    )

    # Rename columns
    df_mountain.rename(
        columns={
            "Vertical rise": "Vertical Rise (ft)",
            "black": "Percent Blacks",
            "blue": "Percent Blues",
            "double black": "Percent Double Blacks",
            "green": "Percent Greens",
            "terrain park": "Percent Terrain Parks",
        },
        inplace=True,
    )

    # Save data
    # mountain.save_mountain_data(df=df_mountain)
