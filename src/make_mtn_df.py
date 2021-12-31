"""
Webscrape mountain statistics from JollyTurns

1. Request all mountain data
2. Format/ preprocess data
3. Save data to CSV
"""

import os
from datetime import date

import pandas as pd
import requests


class MakeMountainDF:
    def __init__(self):

        self.CURRENT_DIRECTORY = os.getcwd()
        self.ORIGIN_URL = "https://www.coloradoski.com/resort-statistics"

        # 2020 ticket prices, fetched manually
        self.dict_resort_prices = {
            "Alpine Meadows": 169,
            "Arapahoe Basin": 109,
            "Aspen Snowmass": 179,  # TODO: Rename to Snowmass?
            "Aspen Highlands": 0,
            "Aspen Mountain": 0,
            "Bald Mountain": 145,
            "Buttermilk": 0,
            "Cooper": 0,
            "Beaver Creek": 209,
            "Copper Mountain": 119,
            "Crested Butte": 129,
            "Diamond Peak": 104,
            "Echo Mountain": 0,
            "Eldora": 140,
            "Granby Ranch": 0,
            "Hesperus Ski Area": 0,
            "Howelsen Hill": 0,
            "Jackson Hole": 165,
            "Kendall Mountain": 0,
            "Loveland": 89,
            "Monarch": 94,
            "Powderhorn": 0,
            "Purgatory Resort": 0,
            "Silverton": 0,
            "Snowmass": 0,
            "Steamboat": 199,
            "Sunlight": 0,
            "Taos": 110,
            "Telluride": 149,
            "Vail": 209,
            "Winter Park": 139,
            "Wolf Creek": 76,
        }

    def get_mountain_data(self) -> pd.core.frame.DataFrame:
        """
        Inputs:
            URL from URLs (str)
        Outputs:
            Pandas DataFrame of ski resort information
        """

        URL = "https://www.coloradoski.com/resort-statistics"
        html_request_doc = requests.get(self.ORIGIN_URL).text

        df_mtn = pd.read_html(html_request_doc)[0]

        # https://stackoverflow.com/questions/66603854/futurewarning-the-default-value-of-regex-will-change-from-true-to-false-in-a-fu
        df_mtn["Peak"] = (
            df_mtn["Peak"].str.replace(r"[^0-9]+", "", regex=True).astype(int)
        )

        df_mtn["Base"] = (
            df_mtn["Base"].str.replace(r"[^0-9]+", "", regex=True).astype(int)
        )

        df_mtn["10 Year Snowfall Avg."] = (
            df_mtn["10 Year Snowfall Avg."]
            .str.replace(r"[^0-9]+", "", regex=True)
            .astype(int)
        )

        df_mtn["Total Runs"] = df_mtn[
            ["Green Runs", "Blue Runs", "Black Runs", "Double-Black Runs"]
        ].sum(axis=1)

        df_mtn["Vertical Rise (ft)"] = df_mtn["Peak"] - df_mtn["Base"]

        return df_mtn

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

    # Request mountain data from all resorts
    df_mountain = mountain.get_mountain_data()

    # Fill prices
    df_mountain["Price"] = (
        df_mountain["Title"].map(mountain.dict_resort_prices).fillna(0)
    )

    # Convert total runs to percentage of total runs per resort
    lst_run_types = ["Green Runs", "Blue Runs", "Black Runs", "Double-Black Runs"]

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
            "Black Runs": "Percent Blacks",
            "Blue Runs": "Percent Blues",
            "Double-Black Runs": "Percent Double Blacks",
            "Green Runs": "Percent Greens",
        },
        inplace=True,
    )

    # Save data
    # mountain.save_mountain_data(df=df_mountain)
