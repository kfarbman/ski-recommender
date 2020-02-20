"""
Webscrape mountain statistics from OnTheSnow and SkiMap

1. Request all mountain data
2. Format/ preprocess data
3. Combine mountain and elevation data
4. Save data to Parquet file
"""

import pickle
import warnings
from tqdm import tqdm

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

warnings.filterwarnings('ignore')

from webscrape_trails import WebscrapeTrails
import time


class MakeMountainDF:

    def __init__(self):
        
        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument('--no-sandbox')
        self.browser_options.add_argument('--window-size=1420,1080')
        self.browser_options.add_argument('--headless')
        self.browser_options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(chrome_options=self.browser_options)
        
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

        df.to_parquet(f"../data/mtn_df_{current_date}.parquet", index=False)

if __name__ == '__main__':

    mountain = MakeMountainDF()

    ws = WebscrapeTrails()

    # Request mountain data from all resorts
    lst_mountain_data = []
    for url in tqdm(ws.URLs):
        df_resort = mountain.get_mountain_data(URL=url)
        df_resort["URL"] = url
        lst_mountain_data.append(df_resort)
    
    # Combine mountain data
    df_mountain = pd.concat(lst_mountain_data).reset_index(drop=True)

    df_mountain = ws.rename_resorts(df=df_mountain)

    # Fill prices
    df_mountain["price"] = df_mountain["resort_name"].map(mountain.dict_resort_prices)

    # Fill missing values
    df_mountain.fillna(0, inplace=True)

    # Convert column data types
    df_mountain = mountain.format_mountain_data_frame_values(df=df_mountain)
    