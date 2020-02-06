import pickle
import time
import warnings
from tqdm import tqdm

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

warnings.filterwarnings('ignore')


class MakeMountainDF:

    def __init__(self):
        
        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument("headless")

        self.browser = webdriver.Chrome(chrome_options=self.browser_options)
        
        self.resort_urls = {
                            'Alpine Meadows': 'california/squaw-valley-usa',
                            'Arapahoe Basin': 'colorado/arapahoe-basin-ski-area',
                            'Beaver Creek': 'colorado/beaver-creek',
                            'Copper': 'colorado/copper-mountain-resort',
                            'Crested Butte': 'colorado/crested-butte-mountain-resort',
                            'Diamond Peak': 'nevada/diamond-peak',
                            'Eldora': 'colorado/eldora-mountain-resort',
                            'Loveland': 'colorado/loveland',
                            'Monarch': 'colorado/monarch-mountain',
                            'Taos': 'new-mexico/taos-ski-valley',
                            'Vail': 'colorado/vail',
                            'Winter Park': 'colorado/winter-park-resort'}
        
        self.resort_elevation = {
                            'Alpine Meadows': 522,
                            'Arapahoe Basin': 513,
                            'Beaver Creek': 497,
                            'Copper': 509,
                            'Crested Butte': 514,
                            # 'Diamond Peak': 359,
                            'Eldora': 508,
                            'Loveland': 515,
                            'Monarch': 511,
                            # 'Taos': 338,
                            'Vail': 507,
                            'Winter Park': 503}
        
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

    # def load_pickle_file(self):
    #     """
    #     Load pickle file containing formatted resort data
    #     """

    #     pkl_file = open('../data/df.pkl', 'rb')
    #     df = pickle.load(pkl_file)
    #     pkl_file.close()

    #     return df

    def get_resort_terrain(self, resort):
        """
        Request elevation, run colors, chairlifts, and prices from each resort
        """
        
        URL = f'http://www.onthesnow.com/{self.resort_urls[resort]}/ski-resort.html'
        
        print(URL)
        
        self.browser.get(URL)

        # time.sleep(5)
        
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
        
        return df_terrain

    def get_resort_elevation_and_lifts(self, resort):
        """
        Request elevation, total runs, and total lifts per resort
        """
        
        URL = f"https://skimap.org/SkiAreas/view/{self.resort_elevation[resort]}.json"
                
        json_resort = requests.get(URL).json()

        dict_resort_elevation = {}

        dict_resort_elevation["resort"] = json_resort["name"]
        dict_resort_elevation["lift_count"] = json_resort["lift_count"]
        dict_resort_elevation["run_count"] = json_resort["run_count"]
        
        # Meters: Multipy by 3.281 to get feet
        dict_resort_elevation["top_elevation"] = json_resort["top_elevation"] * 3.281
        dict_resort_elevation["bottom_elevation"] = json_resort["bottom_elevation"] * 3.281

        return dict_resort_elevation

    def create_mountain_data_frame(self):
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

    def create_elevation_data_frame(self):
        """
        Run get_resort_elevation_and_lifts
        Append missing resort data
        """
        
        lst_resorts = [self.get_resort_elevation_and_lifts(resort)
                   for resort in tqdm(self.resort_elevation)]
        
        # Create missing values from skimap website
        dict_diamond_peak = {"resort": "Diamond Peak",
                            "lift_count": 7,
                            "run_count": 30,
                            "top_elevation": 8540,
                            "bottom_elevation": 6700}
        
        dict_taos = {"resort": "Taos",
                            "lift_count": 14,
                            "run_count": 110,
                            "top_elevation": 12481,
                            "bottom_elevation": 9200}

        lst_resorts.append(dict_diamond_peak)
        lst_resorts.append(dict_taos)

        df_elevations = pd.DataFrame(lst_resorts)

        return df_elevations


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

if __name__ == '__main__':

    mountain = MakeMountainDF()

    df_mountains = mountain.create_mountain_data_frame()
        
    df_elevations = mountain.create_elevation_data_frame()

    df_elevations["resort"] = df_elevations["resort"].str.replace(" Resort", "")
    df_elevations["resort"] = df_elevations["resort"].str.replace(" Mountain", "")
    df_elevations["resort"] = df_elevations["resort"].str.replace(" Ski Area", "")

    # Combine DataFrames
    df_combined = pd.merge(df_mountains, df_elevations, on="resort", how="outer")
    
    df_combined["price"] = df_combined["resort"].map(mountain.dict_resort_prices)
