"""
Webscrape mountain statistics from JollyTurns

1. Request all mountain data
2. Format/ preprocess data
3. Save data to CSV
"""

import pickle
import time
import warnings

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

from src.webscrape_trails import WebscrapeTrails

warnings.filterwarnings('ignore')


class MakeMountainDF:

    def __init__(self):
        
        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument('--no-sandbox')
        self.browser_options.add_argument('--window-size=1420,1080')
        self.browser_options.add_argument('--headless')
        self.browser_options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(options=self.browser_options)
        
        # 2020 ticket prices, fetched manually
        self.dict_resort_prices = {'Alpine Meadows': 169,
                                   'Arapahoe Basin': 109,
                                   'Aspen Snowmass': 179,
                                   'Bald Mountain': 145,
                                   'Beaver Creek': 209,
                                   'Copper': 119,
                                   'Crested Butte': 129,
                                   'Diamond Peak': 104,
                                   'Eldora': 140,
                                   'Jackson Hole': 165,
                                   'Loveland': 89,
                                   'Monarch': 94,
                                   'Steamboat': 199,
                                   'Taos': 110,
                                   'Telluride': 149,
                                   'Vail': 209,
                                   'Winter Park': 139,
                                   'Wolf Creek': 76}
    
    def get_mountain_data(self, URL):
        '''
        Inputs:
            URL from URLs (str)
        Outputs:
            Pandas DataFrame of ski resort information
        '''

        self.browser.get(URL)

        time.sleep(2)

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        # JollyTurns parsing (runs breakdown)
        X = soup.select("resort-glance div.row div.col-xs-12 div.row.text-left.statistics.ng-scope span.ng-binding")
        lst_dev = [x.text for x in X]
        lst_dev = [x.replace(" ski runs: ", "") for x in lst_dev]
        df_ski_runs = pd.DataFrame({"Runs": lst_dev[0::2], "total": lst_dev[1::2]})
        df_ski_runs = df_ski_runs.set_index("Runs").T.reset_index(drop=True)

        # JollyTurns parsing (Chairlifts / total runs)
        Y = soup.select("resort-glance div.row div.col-xs-12 div.row.text-center a")
        lst_y = [y.text.lstrip() for y in Y]
        df_lifts = pd.DataFrame({"Lifts": lst_y[0]}, index=[0])
        
        # JollyTurns parsing (Elevations)
        Z = soup.select("resort-glance div.row div.col-xs-12 table tr td")
        lst_z = [z.text for z in Z if "Lift" not in z.text]
        lst_z = [z.replace(" \xa0", "") for z in lst_z]
        lst_z = [z.replace(" ft", "") for z in lst_z]
        lst_z = [z.replace(":", "") for z in lst_z]

        df_elevations = pd.DataFrame({"Elevation": lst_z[0::2], "Total": lst_z[1::2]})
        df_elevations = df_elevations.set_index("Elevation").T.reset_index(drop=True)
        
        df_ski = pd.concat([df_ski_runs, df_lifts, df_elevations], axis=1)
        df_ski["URL"] = URL

        return df_ski

    def format_mountain_data_frame_values(self, df):
        """
        Pivot DataFrame, and format values

        Input
            df: Pandas DataFrame
        
        Output
            Formatted Pandas DataFrame
        """

        lst_columns = ["Top", "Base", "Lifts", "Vertical rise", "black","blue", "double black", "green", "terrain park"]

        df[lst_columns] = df[lst_columns].astype("int")

        return df

    def save_mountain_data(self, df):
        """
        Save formatted mountain data to Parquet file
        """
        current_date = str(pd.Timestamp.now().date()).replace("-", "")

        df.to_parquet(f"../data/mountain_data_{current_date}.parquet", index=False)

if __name__ == '__main__':

    mountain = MakeMountainDF()

    ws = WebscrapeTrails()

    # Request mountain data from all resorts
    lst_mountain_data = []
    for url in tqdm(ws.URLs[0:3]):
        df_resort = mountain.get_mountain_data(URL=url)
        lst_mountain_data.append(df_resort)
    
    # Combine mountain data
    df_mountain = pd.concat(lst_mountain_data).reset_index(drop=True)

    df_mountain = ws.rename_resorts(df=df_mountain)

    # Fill prices
    df_mountain["Price"] = df_mountain["Resort"].map(mountain.dict_resort_prices)

    # Drop columns
    df_mountain.drop("URL", axis=1, inplace=True)

    # Fill missing values
    df_mountain.fillna(0, inplace=True)

    # Convert column data types
    df_mountain = mountain.format_mountain_data_frame_values(df=df_mountain)

    df_mountain["Total Runs"] = df_mountain[["black", "blue", "double black", "green", "terrain park"]].sum(axis=1)

    # Convert to percentage of total runs per resort
    df_mountain[["green", "blue", "black", "double black", "terrain park"]] = df_mountain[
        ["green", "blue", "black", "double black", "terrain park"]].div(
        df_mountain["Total Runs"], axis=0).round(2)

    # Rename columns
    df_mountain.rename(columns={
        "Vertical rise": "Vertical Rise (ft)",
        "black": "Black",
        "blue": "Blue",
        "double black": "Double Black",
        "green": "Green",
        "terrain park": "Terrain Park"
        }, inplace=True)

    # Save data
    # df_mountain.to_csv("../data/formatted/mountain_data_20200220.csv", index=False, header=True)
