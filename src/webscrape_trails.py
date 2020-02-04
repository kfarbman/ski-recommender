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

        self.LL_URL = 'https://jollyturns.com/resort/united-states-of-america/loveland-ski-area/'
        self.AB_URL = 'https://jollyturns.com/resort/united-states-of-america/arapahoe-basin/'
        self.C_URL = 'https://jollyturns.com/resort/united-states-of-america/copper-mountain-resort/'
        self.E_URL = 'https://jollyturns.com/resort/united-states-of-america/eldora-mountain-resort/'
        self.AM_URL = 'https://jollyturns.com/resort/united-states-of-america/alpine-meadows/'
        self.V_URL = 'https://jollyturns.com/resort/united-states-of-america/vail-ski-resort/'
        self.M_URL = 'https://jollyturns.com/resort/united-states-of-america/monarch-ski-area/'
        self.CB_URL = 'https://jollyturns.com/resort/united-states-of-america/crested-butte-mountain-resort/'
        self.T_URL = 'https://jollyturns.com/resort/united-states-of-america/taos-ski-valley/'
        self.DP_URL = 'https://jollyturns.com/resort/united-states-of-america/diamond-peak/'
        self.WP_URL = 'https://jollyturns.com/resort/united-states-of-america/winter-park-resort/'
        self.BC_URL = 'https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/'
        self.TELLURIDE_URL = 'https://jollyturns.com/resort/united-states-of-america/telluride-ski-resort/'
        self.BM_URL = 'https://jollyturns.com/resort/united-states-of-america/bald-mountain/'
        self.S_URL = 'https://jollyturns.com/resort/united-states-of-america/steamboat-ski-resort/'
        self.AS_URL = 'https://jollyturns.com/resort/united-states-of-america/aspen-snowmass/'
        self.WC_URL = 'https://jollyturns.com/resort/united-states-of-america/wolf-creek-ski-area/'

        self.URLs = [self.LL_URL,
                     self.AB_URL,
                     self.C_URL,
                     self.E_URL,
                     self.AM_URL,
                     self.V_URL,
                     self.M_URL,
                     self.CB_URL,
                     self.T_URL,
                     self.DP_URL,
                     self.WP_URL,
                     self.BC_URL,
                     self.TELLURIDE_URL,
                     self.BM_URL,
                     self.S_URL,
                     self.AS_URL,
                     self.WC_URL]

        self.browser_options = webdriver.ChromeOptions()
        self.browser_options.add_argument("headless")

        self.browser = webdriver.Chrome(chrome_options=self.browser_options)

        self.lst_run_difficulty = ["skiruns-green", "skiruns-blue", "skiruns-black", "skiruns-double-black"]

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
                "Name": ["__NA__"],
                "Bottom (ft)": ["__NA__"],
                "Top (ft)": ["__NA__"],
                "Vertical Drop (ft)": ["__NA__"],
                "Length (mi)": ["__NA__"]
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
