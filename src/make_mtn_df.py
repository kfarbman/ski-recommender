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
        
        # self.resort_urls = {
        #                     'Alpine Meadows': 'california/squaw-valley-usa',
        #                     'Arapahoe Basin': 'colorado/arapahoe-basin-ski-area',
        #                     # TODO: Aspen Snowmass
        #                     # TODO: Bald Mountain
        #                     'Beaver Creek': 'colorado/beaver-creek',
        #                     'Copper': 'colorado/copper-mountain-resort',
        #                     'Crested Butte': 'colorado/crested-butte-mountain-resort',
        #                     'Diamond Peak': 'nevada/diamond-peak',
        #                     'Eldora': 'colorado/eldora-mountain-resort',
        #                     'Loveland': 'colorado/loveland',
        #                     'Monarch': 'colorado/monarch-mountain',
        #                     # TODO: Steamboat
        #                     'Taos': 'new-mexico/taos-ski-valley',
        #                     # TODO: Telluride
        #                     'Vail': 'colorado/vail',
        #                     'Winter Park': 'colorado/winter-park-resort'}
        
        # self.resort_elevation = {
        #                     'Alpine Meadows': 522,
        #                     'Arapahoe Basin': 513,
        #                     'Beaver Creek': 497,
        #                     'Copper': 509,
        #                     'Crested Butte': 514,
        #                     # 'Diamond Peak': 359,
        #                     'Eldora': 508,
        #                     'Loveland': 515,
        #                     'Monarch': 511,
        #                     # 'Taos': 338,
        #                     'Vail': 507,
        #                     'Winter Park': 503}
        
        # 2020 ticket prices, fetched manually
        self.dict_resort_prices = {'Alpine Meadows': 169,
                                   'Arapahoe Basin': 109,
                                   'Beaver Creek': 209,
                                   'Copper': 119,
                                   'Crested Butte': 129,
                                   'Diamond Peak': 104,
                                   'Eldora': 140,
                                   'Loveland': 89,
                                   'Monarch': 94,
                                   'Taos': 110,
                                   'Vail': 209,
                                   'Winter Park': 139}

    # def create_mountain_data_frame(self):
    #     """
    #     Run get_resort_terrain

    #     Output
    #         Pandas DataFrame of terrain data per resort
    #     """
    #     lst_resorts = []

    #     for resort in tqdm(self.resort_urls.keys()):
    #         lst_resorts.append(self.get_resort_terrain(resort))
        
    #     # Combine list of resort DataFrames
    #     df_terrain = pd.concat(lst_resorts).reset_index(drop=True)

    #     return df_terrain
    
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

        df_mountains = df.pivot(index='resort', columns='type', values='figures').reset_index()
        
        df_mountains["Advanced"] = df_mountains["Advanced"].str.replace("%", "").astype(int)
        df_mountains["Beginner"] = df_mountains["Beginner"].str.replace("%", "").astype(int)
        df_mountains["Expert"] = df_mountains["Expert"].str.replace("%", "").astype(int)
        df_mountains["Intermediate"] = df_mountains["Intermediate"].str.replace("%", "").astype(int)
        df_mountains["Longest Run"] = df_mountains["Longest Run"].str.replace(" mi", "").astype(float)
        df_mountains["Runs"] = df_mountains["Runs"].astype(int)
        df_mountains["Terrain Parks"] = df_mountains["Terrain Parks"].astype(int)
        
        # TODO: Convert Acres to Feet? ; multiply by 43560
        df_mountains["Skiable Terrain"] = df_mountains["Skiable Terrain"].str.replace(" ac", "").astype(int)
        df_mountains.drop(["mi Snow Making"], axis=1, inplace=True)
        
        df_mountains["Snow Making"].fillna("0 ac", inplace=True)
        
        # TODO: Convert Acres to Feet? ; multiply by 43560
        df_mountains["Snow Making"] = df_mountains["Snow Making"].str.replace(" ac", "").astype(int)

        return df_mountains

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
   