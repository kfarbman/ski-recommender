"""
Webscrape mountain statistics from JollyTurns

1. Request all mountain data
2. Format/ preprocess data
3. Save data to CSV
"""

import json
import os
from datetime import date
from itertools import chain

import pandas as pd


class MakeMountainDF:
    def __init__(self):

        self.CURRENT_DIRECTORY = os.getcwd()
        self.ORIGIN_URL = "https://www.coloradoski.com/resort-statistics"

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

        self.resort_locations = {
            "Alpine Meadows": "CA",
            "Arapahoe Basin": "CO",
            "Aspen Snowmass": "CO",
            "Bald Mountain": "CO",
            "Beaver Creek": "CO",
            "Copper": "CO",
            "Crested Butte": "CO",
            "Diamond Peak": "NV",
            "Eldora": "CO",
            "Jackson Hole": "WY",
            "Loveland": "CO",
            "Monarch": "CO",
            "Steamboat": "CO",
            "Taos": "NM",
            "Telluride": "CO",
            "Vail": "CO",
            "Winter Park": "CO",
            "Wolf Creek": "CO",
        }

    def add_groomed_col(self):
        """
        Add groomed column to trail data

        Inputs:
                None
        Outputs:
                df_trails DataFrame with "Groomed" column
        """

        with open("../groomed_trails.json") as groomed_trails:
            dict_groomed_trails = json.loads(groomed_trails)

        lst_groomed_runs = list(chain(*dict_groomed_trails.values()))

        df_trails["Groomed"] = "Ungroomed"
        df_trails["Groomed"][df_trails["Trail Name"].isin(lst_groomed_runs)] = "Groomed"

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
            f"{self.CURRENT_DIRECTORY}/data/trail_data_processed_{current_date}.parquet",
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

    # Convert run distance from miles to feet
    df_trails.loc[df_trails["Length"] < 1, "Length"] = df_trails["Length"] * 5280

    # Calculate average steepness
    df_trails["Average Steepness"] = (
        df_trails["Vertical drop"] / df_trails["Length"]
    ).round(2)

    # Get resort name for trails
    df_trails = mountain.rename_resorts(df=df_trails)

    # Get ticket price per resort
    df_trails["Location"] = (
        df_trails["Resort"].map(mountain.resort_locations).fillna("__NA__")
    )

    # Fill prices
    # TODO: Correct any with value of 0
    df_trails["Price"] = df_trails["Resort"].map(mountain.dict_resort_prices).fillna(0)

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

    # Format column names
    df_combined = df_combined.rename(
        columns={
            "Black": "Percent Blacks",
            "Blue": "Percent Blues",
            "Double-Black": "Percent Double Blacks",
            "Green": "Percent Greens",
            "Name": "Trail Name",
            "Top": "Top Elev (ft)",
            "Bottom": "Bottom Elev (ft)",
            "Vertical drop": "Vertical Drop (ft)",
            "Length": "Slope Length (ft)",
        }
    ).copy()

    # Save data
    # mountain.save_mountain_data(df=df_combined)
