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

    df_trails = pd.read_parquet("./data/trail_data_extract_20220113.parquet")

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
    df_trails = mountain.rename_resorts(df=df_trails)

    # Count total runs per resort by difficulty
    df_trails["Total Runs"] = df_trails.groupby(["Resort", "Difficulty"])[
        "Name"
    ].transform("count")

    # Create count of runs by difficulty per resort
    df_total_trails_by_difficulty = pd.crosstab(
        df_trails["Resort"], df_trails["Difficulty"]
    ).reset_index()

    # Combine trails and aggregate trail metrics
    df_combined = pd.merge(
        df_trails, df_total_trails_by_difficulty, on="Resort", how="inner"
    )

    # Convert total runs to percentage of total runs per resort
    lst_run_difficulty = df_combined["Difficulty"].unique().tolist()

    df_combined[lst_run_difficulty] = (
        df_combined[lst_run_difficulty]
        .div(df_combined["Total Runs"], axis=0)
        .mul(100)
        .round()
        .astype(int)
    )

    # Rename difficulty columns to reflect percent calculation
    df_combined = df_combined.rename(
        columns={
            "Black": "Percent Blacks",
            "Blue": "Percent Blues",
            "Double-Black": "Percent Double Blacks",
            "Green": "Percent Greens",
        }
    ).copy()

    # Format trail values
    lst_formatted_cols = [
        "Bottom Elev (ft)",
        "Top Elev (ft)",
        "Vertical Drop (ft)",
        "Length (mi)",
    ]

    import pdb

    pdb.set_trace()

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

    # # Request mountain data from all resorts
    # df_mountain = mountain.get_mountain_data()

    # # Fill prices
    # df_mountain["Price"] = (
    #     df_mountain["Title"].map(mountain.dict_resort_prices).fillna(0)
    # )

    # Save data
    # mountain.save_mountain_data(df=df_mountain)
