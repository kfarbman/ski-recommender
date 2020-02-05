import pickle
import time
import warnings
from tqdm import tqdm

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')


class MakeMountainDF:

    def __init__(self):
        
        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument("headless")

        self.browser = webdriver.Chrome(chrome_options=self.browser_options)
        
        self.resort_urls = {'Loveland': 'colorado/loveland',
                            'Arapahoe Basin': 'colorado/arapahoe-basin-ski-area',
                            'Copper': 'colorado/copper-mountain-resort',
                            'Eldora': 'colorado/eldora-mountain-resort',
                            'Alpine Meadows': 'california/squaw-valley-usa',
                            'Vail': 'colorado/vail',
                            'Monarch': 'colorado/monarch-mountain',
                            'Crested Butte': 'colorado/crested-butte-mountain-resort',
                            'Taos': 'new-mexico/taos-ski-valley',
                            'Diamond Peak': 'nevada/diamond-peak',
                            'Winter Park': 'colorado/winter-park-resort',
                            'Beaver Creek': 'colorado/beaver-creek'}

    def load_pickle_file(self):
        """
        Load pickle file containing formatted resort data
        """

        pkl_file = open('../data/df.pkl', 'rb')
        df = pickle.load(pkl_file)
        pkl_file.close()

        return df

    def get_resort_terrain(self, resort):
        """
        Request elevation, run colors, chairlifts, and prices from each resort
        """
        
        URL = f'http://www.onthesnow.com/{self.resort_urls[resort]}/ski-resort.html'
        
        print(URL)
        
        self.browser.get(URL)

        time.sleep(5)
        
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        lst_terrain = soup.select('div#resort_terrain p')
        lst_terrain = [i.get_text() for i in lst_terrain]

        # terrain types
        lst_terrain_type = lst_terrain[::2]

        # terrain figures and numbers
        lst_terrain_figures = lst_terrain[1::2]
        
        df_terrain = pd.DataFrame({'type': lst_terrain_type, 'figures': lst_terrain_figures})

        df_terrain["type"] = df_terrain["type"].str.replace(" Runs", "")
        
        df_terrain["resort"] = resort
        
        # TODO: Get elevation
        # bottom = int(''.join([x for x in elevs.split()[0] if x.isnumeric()]))
        # top = int(''.join([x for x in elevs.split()[2] if x.isnumeric()]))
                
        # TODO: Get lifts and price
        # lifts = int(lifts)
        # price = int(
        #     ''.join([x if x.isnumeric() else '0' for x in price.split()[0]]))
        # return [bottom, top, greens, blues, blacks, bbs, lifts, price]

        return df_terrain

    def create_data_frame(self):
        """
        Run get_resort_terrain

        Output
            Pandas DataFrame of terrain data per resort
        """
        lst_resorts = []

        for resort in tqdm(self.resort_urls.keys()):
            lst_resorts.append(self.get_resort_terrain(resort))

        # Combine list of resort DataFrames
        df_terrain = pd.concat(lst_resorts).reset_index(drop=True)

        return df_terrain

    def format_data_frame(self, df):
        """
        Format DataFrame containing elevations, difficulty, and price
        """
        new_cols = ['resort_bottom', 'resort_top', 'greens',
                    'blues', 'blacks', 'bbs', 'lifts', 'price']
        df = df.reindex(
            columns=[*df.columns.tolist(), *new_cols], fill_value=0)
        return df

    def format_elev_prices(self, df, elevs_colors_lifts_price):

        for resort in elevs_colors_lifts_price:
            df['resort_bottom'][df['resort'] ==
                                resort] = elevs_colors_lifts_price[resort][0]
            df['resort_top'][df['resort'] ==
                             resort] = elevs_colors_lifts_price[resort][1]
            df['greens'][df['resort'] == resort] = elevs_colors_lifts_price[resort][2]
            df['blues'][df['resort'] == resort] = elevs_colors_lifts_price[resort][3]
            df['blacks'][df['resort'] == resort] = elevs_colors_lifts_price[resort][4]
            df['bbs'][df['resort'] == resort] = elevs_colors_lifts_price[resort][5]
            df['lifts'][df['resort'] == resort] = elevs_colors_lifts_price[resort][6]
            df['price'][df['resort'] == resort] = elevs_colors_lifts_price[resort][7]

        return df

    def save_mountain_data(self, df):
        """
        Save formatted mountain data to Parquet file
        """
        current_date = str(pd.Timestamp.now().date()).replace("-", "")

        df.to_parquet(f"../data/mtn_df_{current_date}.parquet", index=False)
        
        # output = open('../data/mtn_df.pkl', 'wb')
        # pickle.dump(df, output)
        # output.close()

if __name__ == '__main__':

    mountain = MakeMountainDF()

    df_mountains = mountain.create_data_frame()