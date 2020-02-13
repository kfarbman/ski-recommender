import pickle
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm


"""
Request trail data from all resorts


"""


class WebscrapeTrails:

    def __init__(self):

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
            self.LOVELAND_URL,
            self.MONARCH_URL,
            self.STEAMBOAT_URL,
            self.TAOS_URL,
            self.TELLURIDE_URL,
            self.VAIL_URL,
            self.WINTER_PARK_URL,
            self.WOLF_CREEK_URL]

        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument("headless")

        self.browser = webdriver.Chrome(chrome_options=self.browser_options)

        self.lst_run_difficulty = ["skiruns-green", "skiruns-blue", "skiruns-black", "skiruns-double-black"]

        self.blank_value = "__NA__"

    def create_resort_urls(self):
        """
        Create URLs used to scrape data for each difficulty at each resort

        INPUT
            None
        OUTPUT
            list of resort URLs
        """
        
        lst_resort_urls = []

        for url in self.URLs:
            for difficulty in self.lst_run_difficulty:
                str_combined_url = url + difficulty
                lst_resort_urls.append(str_combined_url)
        
        return lst_resort_urls

    def make_tables(self, URL):
        '''
        Inputs:
            URL from URLs (str)
        Outputs:
            Pandas DataFrame of ski resort information
        '''

        self.browser.get(URL)

        time.sleep(3)

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        rows = soup.select('table.table.table-striped tbody tr')

        table_lst = []
        for row in rows:
            cell_lst = [cell for cell in row if cell != ' ']
            cell_lst = [cell.text for cell in cell_lst]
            table_lst.append(cell_lst)

        df_ski = pd.DataFrame(table_lst)

        try:
            df_ski.columns = ['Name', 'Bottom (ft)', 'Top (ft)', 'Vertical Drop (ft)', 'Length (mi)']
        except ValueError:
            df_ski = pd.DataFrame({
                "Name": [self.blank_value],
                "Bottom (ft)": [self.blank_value],
                "Top (ft)": [self.blank_value],
                "Vertical Drop (ft)": [self.blank_value],
                "Length (mi)": [self.blank_value]
            })

        # Filter restaurants and chairlifts
        df_ski = df_ski[df_ski['Length (mi)'].notnull()].reset_index(drop=True)

        return df_ski

    def save_resort_data(self, dict_resort):

        output = open('../data/resort_dict_DEV.pkl', 'wb')
        pickle.dump(dict_resort, output)
        output.close()


if __name__ == '__main__':

    ws = WebscrapeTrails()

    # Create list of all ski resort URL's
    lst_resort_urls = ws.create_resort_urls()

    # Request data from all ski resorts
    lst_resort_data = []

    for url in tqdm(lst_resort_urls):
        df_resort = ws.make_tables(URL=url)
        df_resort["URL"] = url
        lst_resort_data.append(df_resort)

    # Combine resort data
    df_combined = pd.concat(lst_resort_data)
    df_combined["difficulty"] = df_combined["URL"].str.split("skiruns-", 1, expand=True)[1]

    # Format run name
    df_combined["Name"] = df_combined["Name"].str.replace("\xa0 ", "")
    df_combined["Name"] = df_combined["Name"].str.rstrip()

    # Get resort name
    df_combined["resort_name"] = df_combined["URL"].str.split("united-states-of-america/", 1, expand=True)[1]
    df_combined["resort_name"] = df_combined["resort_name"].str.split("/", 1, expand=True)[0]

    # Format distance values
    df_distance = df_combined["Length (mi)"].str.split(" ", expand=True)
    df_distance.columns = ["distance", "metric"]
    df_distance["distance"] = df_distance["distance"].map({"__NA__": "0"}).fillna(df_distance["distance"])

    # Convert feet to miles
    for idx in range(len(df_distance)):
        if df_distance["metric"].iloc[idx] == "ft":
            df_distance.iloc[idx].at["distance"] = float(df_distance.iloc[idx].at["distance"]) / 5280

    # Combine distance with resort data
    df_combined = pd.concat([df_combined, df_distance], axis=1)

    # Get average steepness
    df_combined["Vertical Drop (ft)"] = df_combined["Vertical Drop (ft)"].str.split(" ", 1, expand=True)[0]
    df_combined["Vertical Drop (ft)"] = df_combined["Vertical Drop (ft)"].map(
        {"__NA__": "0"}).fillna(df_combined["Vertical Drop (ft)"])
    
    df_combined['Average Steepness'] = df_combined['Vertical Drop (ft)'].astype(float)/(5280*df_combined['distance'].astype(float))
