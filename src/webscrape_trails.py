import pickle
import time

"""
Request trail data from all resorts



"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm


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
        self.browser_options.add_argument('--no-sandbox')
        self.browser_options.add_argument('--window-size=1420,1080')
        self.browser_options.add_argument('--headless')
        self.browser_options.add_argument('--disable-gpu')

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

    def make_tables(self, URL):
        '''
        Inputs:
            URL from URLs (str)
        Outputs:
            Pandas DataFrame of ski resort information
        '''       
        
        self.browser.get(URL)

        time.sleep(2)

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
            print(URL)
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

    def rename_resorts(self, df):
        """
        Rename resorts for recommendation system

        INPUT
            df: Pandas DataFrame
        OUTPUT
            Pandas DataFrame, with resort_name column altered
        """
        
        df["resort_name"] = df["URL"].str.split("united-states-of-america/", 1, expand=True)[1]
        df["resort_name"] = df["resort_name"].str.split("/", 1, expand=True)[0]
        
        dict_webscrape_trail_names = {'alpine-meadows': "Alpine Meadows",
                            'arapahoe-basin': "Arapahoe Basin",
                            'aspen-snowmass': "Aspen Snowmass",
                            'bald-mountain': "Bald Mountain",
                            'beaver-creek-resort': "Beaver Creek",
                            'copper-mountain-resort': "Copper",
                            'crested-butte-mountain-resort': "Crested Butte",
                            'diamond-peak': "Diamond Peak",
                            'eldora-mountain-resort': "Eldora",
                            'loveland-ski-area': "Loveland",
                            'monarch-ski-area': "Monarch",
                            'steamboat-ski-resort': "Steamboat",
                            'taos-ski-valley': "Taos",
                            'telluride-ski-resort': "Telluride",
                            'vail-ski-resort': "Vail",
                            'winter-park-resort': "Winter Park",
                            'wolf-creek-ski-area': "Wolf Creek"}

        df["resort_name"] = df["resort_name"].map(
            dict_webscrape_trail_names).\
            fillna(df["resort_name"])
        
        return df

    def save_resort_data(self, dict_resort):

        output = open('../data/resort_dict_DEV.pkl', 'wb')
        pickle.dump(dict_resort, output)
        output.close()


if __name__ == '__main__':

    ws = WebscrapeTrails()

    # Create list of all ski resort URL's
    lst_resort_urls = ws.create_resort_urls()

    # Request trail data from all ski resorts
    lst_trail_data = []

    for url in tqdm(lst_resort_urls):
        df_resort = ws.make_tables(URL=url)
        df_resort["URL"] = url
        lst_trail_data.append(df_resort)

    # Combine trail data
    df_resorts = pd.concat(lst_trail_data)
    df_resorts["difficulty"] = df_resorts["URL"].str.split("skiruns-", 1, expand=True)[1]

    # Request mountain data from all resorts
    lst_mountain_data = []
    for url in tqdm(ws.URLs):
        df_resort = ws.get_mountain_data(URL=url)
        df_resort["URL"] = url
        lst_mountain_data.append(df_resort)
    
    # Combine mountain data
    df_mountain = pd.concat(lst_mountain_data).reset_index(drop=True)

    # Format run name
    df_resorts["Name"] = df_resorts["Name"].str.replace("\xa0 ", "")
    df_resorts["Name"] = df_resorts["Name"].str.rstrip()

    # Get resort name for trails
    df_resorts = ws.rename_resorts(df=df_resorts)
    
    # Get resort name for mountains
    df_mountains = ws.rename_resorts(df=df_mountains)
    import pdb; pdb.set_trace()
    
    # Rename columns
    df_resorts.rename(columns={"resort_name": "resort", "Name": "trail_name"}, inplace=True)
    
    # import pdb; pdb.set_trace()
    
    # TODO: Make this process simpler; process along index
    # Format distance values
    df_distance = df_resorts["Length (mi)"].str.split(" ", expand=True)
    df_distance.columns = ["distance", "metric"]
    df_distance["distance"] = df_distance["distance"].map({"__NA__": "0"}).fillna(df_distance["distance"])

    # Convert miles to feet
    # df_distance.loc[df_distance["metric"] == "ft", "distance"] = df_distance["distance"].astype(float) / 5280
    for idx in range(len(df_distance)):
        if df_distance["metric"].iloc[idx] == "mi":
            df_distance.iloc[idx].at["distance"] = float(df_distance.iloc[idx].at["distance"]) * 5280

    # Combine distance with resort data
    df_resorts = pd.concat([df_resorts, df_distance], axis=1)

    # Get average steepness
    df_resorts["Vertical Drop (ft)"] = df_resorts["Vertical Drop (ft)"].str.split(" ", 1, expand=True)[0]
    df_resorts["Vertical Drop (ft)"] = df_resorts["Vertical Drop (ft)"].map(
        {"__NA__": "0"}).fillna(df_resorts["Vertical Drop (ft)"])
    
    # Average Steepness = (Vert Drop (feet) / 5280) / distance (miles))
    # df_resorts['Average Steepness'] = df_resorts['Vertical Drop (ft)'].astype(float)/(5280*df_resorts['distance'].astype(float))
    df_resorts['Average Steepness'] = (df_resorts['Vertical Drop (ft)'].astype(float) / 5280) / df_resorts['distance'].astype(float)

    # Remove blank rows
    df_resorts = df_resorts[df_resorts["trail_name"] != "__NA__"].reset_index(drop=True)

    # Correct column values
    df_resorts["Bottom (ft)"] = df_resorts["Bottom (ft)"].str.replace(" ft", "")
    df_resorts["Bottom (ft)"] = df_resorts["Bottom (ft)"].astype(float)
    df_resorts["Top (ft)"] = df_resorts["Top (ft)"].str.replace(" ft", "")
    df_resorts["Top (ft)"] = df_resorts["Top (ft)"].astype(float)
    # df_resorts["Length (mi)"] = df_resorts["Length (mi)"].str.replace(" mi", "")
    
    # Drop columns
    df_resorts.drop(["URL", "metric", "Length (mi)"], axis=1, inplace=True)

    # Rename columns

    # ['Vertical Drop (ft)']
    ['vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)',
                   'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level', 'resort', 'location']

# [
#  'Vertical Drop (ft)',
#  'Difficulty',
#  'Resort',
#  'Slope Length (ft)',
#  'Average Steepness']

#     df_resorts.rename(columns={
#         "Bottom (ft)": "Bottom Elev (ft)",
#         "difficulty": "Difficulty",
#         "distance": "Slope Length (ft)",
#         "resort": "Resort",
#         "trail_name": "Trail Name",
#         "Top (ft)": "Top Elev (ft)"
#         }, inplace=True)

    # df.columns = [

    #     'Location',
    #     'Groomed',
    #     'Vert Rise (ft)',
    #     'Avg Width (ft)',
    #     'Slope Area (acres)',
    #     'Avg Grade (%)',
    #     'Max Grade (%)']
