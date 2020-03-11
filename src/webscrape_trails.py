"""
Request trail data from all resorts
"""

import pickle
import time

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
        self.JACKSON_HOLE_URL = f"{self.MAIN_URL}/jackson-hole/"
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
            self.JACKSON_HOLE_URL,
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

        self.browser = webdriver.Chrome(options=self.browser_options)

        self.lst_run_difficulty = ["skiruns-green", "skiruns-blue", "skiruns-black", "skiruns-double-black"]

        self.blank_value = "__NA__"

    # def create_resort_urls(self):
    #     """
    #     Create URLs used to scrape data for each difficulty at each resort

    #     INPUT
    #         None
    #     OUTPUT
    #         list of resort URLs
    #     """
        
    #     lst_resort_urls = []

    #     for url in self.URLs:
    #         for difficulty in self.lst_run_difficulty:
    #             str_combined_url = url + difficulty
    #             lst_resort_urls.append(str_combined_url)
        
    #     return lst_resort_urls

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

        X_web_trail = soup.select('table.table-striped tr')

        if not X_web_trail:
            print(f"No runs for {URL}")
            df_combined = pd.DataFrame({
                "Trail Name": [self.blank_value],
                "Bottom Elev (ft)": [self.blank_value],
                "Top Elev (ft)": [self.blank_value],
                "Vertical Drop (ft)": [self.blank_value],
                "Length (mi)": [self.blank_value],
                "URL": [URL]
            })
        else:
            lst_rows = [x.text.strip() for x in X_web_trail]
            lst_rows = [i.replace("  ", "|") for i in lst_rows]
            lst_rows = [i.replace(" ft", "|") for i in lst_rows]
            lst_rows = [i.replace(" mi", "|") for i in lst_rows]

            lst_cols = ['Name Bottom Top Vertical rise',
                        'Name Bottom Top Vertical drop Length',
                        'Name Elevation']

            # Indices where headers start, separating runs by difficulty
            idx_headers = [i for i,j in enumerate(lst_rows) if j in lst_cols]

            df_trails = pd.DataFrame(lst_rows)
            
            df_trails = df_trails[0].str.split("|", expand=True)
            df_trails.columns = ["Trail Name", "Bottom Elev (ft)", "Top Elev (ft)", "Vertical Drop (ft)", "Length (mi)", "Blank"]

            df_trails.drop("Blank", axis=1, inplace=True)

            lst_difficulty = soup.select("h4")
            lst_difficulty = [l.text.strip() for l in lst_difficulty]
            lst_difficulty = [i.replace("Ski runs: ", "") for i in lst_difficulty]

            df_difficulties = pd.DataFrame(lst_difficulty, index=idx_headers)
            
            df_combined = pd.merge(df_trails, df_difficulties,
                left_index=True, right_index=True, how="outer")

            df_combined.rename(columns={0:"Difficulty"}, inplace=True)

            df_combined["Difficulty"].fillna(method="ffill", inplace=True)

            # Remove rows which are not trail names
            df_combined = df_combined[~df_combined["Trail Name"].isin(lst_cols)].reset_index(drop=True)
            
            # Correct column values with mapping
            # Replace None with NaN
            # Correct column names

            # Remove Lifts, Restaurants, and Terrain Park
            df_combined = df_combined[~df_combined["Difficulty"].isin(["Lifts", "Restaurants", "terrain park"])].reset_index(drop=True)

            # # Filter restaurants and chairlifts
            # df_ski = df_ski[df_ski['Length (mi)'].notnull()].reset_index(drop=True)

            # Add URL
            df_combined["URL"] = URL

        return df_combined

    def rename_resorts(self, df):
        """
        Rename resorts for recommendation system

        INPUT
            df: Pandas DataFrame
        OUTPUT
            Pandas DataFrame, with resort_name column altered
        """
        
        df["Resort"] = df["URL"].str.split("united-states-of-america/", 1, expand=True)[1]
        df["Resort"] = df["Resort"].str.split("/", 1, expand=True)[0]
        
        dict_webscrape_trail_names = {'alpine-meadows': "Alpine Meadows",
                            'arapahoe-basin': "Arapahoe Basin",
                            'aspen-snowmass': "Aspen Snowmass",
                            'bald-mountain': "Bald Mountain",
                            'beaver-creek-resort': "Beaver Creek",
                            'copper-mountain-resort': "Copper",
                            'crested-butte-mountain-resort': "Crested Butte",
                            'diamond-peak': "Diamond Peak",
                            'eldora-mountain-resort': "Eldora",
                            'jackson-hole': "Jackson Hole",
                            'loveland-ski-area': "Loveland",
                            'monarch-ski-area': "Monarch",
                            'steamboat-ski-resort': "Steamboat",
                            'taos-ski-valley': "Taos",
                            'telluride-ski-resort': "Telluride",
                            'vail-ski-resort': "Vail",
                            'winter-park-resort': "Winter Park",
                            'wolf-creek-ski-area': "Wolf Creek"}

        df["Resort"] = df["Resort"].map(
            dict_webscrape_trail_names).\
            fillna(df["Resort"])
        
        return df

    def save_resort_data(self, dict_resort):

        output = open('../data/resort_dict_DEV.pkl', 'wb')
        pickle.dump(dict_resort, output)
        output.close()


if __name__ == '__main__':

    ws = WebscrapeTrails()

    # Create list of all ski resort URL's
    # lst_resort_urls = ws.create_resort_urls()
    # lst_resort_urls = [i for i in lst_resort_urls if "vail" in i]

    # Request trail data from all ski resorts
    # TODO: Request resorts in parallel?
    lst_trail_data = []

    for url in tqdm(ws.URLs):
        print(f"Requesting {url}")
        df_resort = ws.make_tables(URL=url)
        lst_trail_data.append(df_resort)
        # df_resort = None

    # Combine trail data
    df_resorts = pd.concat(lst_trail_data)
    import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    # df_resorts = pd.read_csv("../data/trail_data_DEV_20200220_v2.csv")

    # Remove blank resorts
    df_resorts = df_resorts[df_resorts["Trail Name"].notnull()].reset_index(drop=True)
    df_resorts = df_resorts[df_resorts["Trail Name"] != ws.blank_value].reset_index(drop=True)

    df_resorts["Difficulty"] = df_resorts["URL"].str.split("skiruns-", 1, expand=True)[1]
    
    dict_colors = {
        "green": "Green",
        "blue": "Blue",
        "black":"Black",
        "double-black": "Double Black"}
    
    df_resorts["Difficulty"] = df_resorts["Difficulty"].map(dict_colors)

    # Format trail name
    df_resorts["Trail Name"] = df_resorts["Trail Name"].str.replace("\xa0 ", "").str.strip()

    # Get resort name for trails
    df_resorts = ws.rename_resorts(df=df_resorts)

    # Format run distance values
    df_resorts["Slope Length (ft)"] = df_resorts["Length (mi)"].str.split(" ", expand=True)[0]
    df_resorts["Slope Length (ft)"] = df_resorts["Slope Length (ft)"].astype(float)
    
    # Convert run distance from miles to feet
    df_resorts.loc[df_resorts["Slope Length (ft)"] < 1, "Slope Length (ft)"] = df_resorts["Slope Length (ft)"] * 5280

    # Get average steepness
    df_resorts["Vertical Drop (ft)"] = df_resorts["Vertical Drop (ft)"].str.split(" ", 1, expand=True)[0]
    df_resorts["Vertical Drop (ft)"] = df_resorts["Vertical Drop (ft)"].astype(float)
    df_resorts["Vertical Drop (ft)"].fillna(0, inplace=True)
    
    # TODO: Validate Average Stepness calculation
    # Average Steepness = (Vert Drop (feet) / 5280) / distance (miles))
    # df_resorts['Average Steepness'] = df_resorts['Vertical Drop (ft)'].astype(float)/(5280*df_resorts['distance'].astype(float))
    # df_resorts['Average Steepness'] = (df_resorts['Vertical Drop (ft)'] / 5280) / df_resorts['distance'].astype(float)
    df_resorts['Average Steepness'] = df_resorts['Vertical Drop (ft)'] / df_resorts['Slope Length (ft)']

    # Correct column values
    df_resorts["Bottom Elev (ft)"] = df_resorts["Bottom Elev (ft)"].str.replace(" ft", "").astype(float)
    df_resorts["Top Elev (ft)"] = df_resorts["Top Elev (ft)"].str.replace(" ft", "").astype(float)
    
    # Drop columns
    df_resorts.drop(["URL", "Length (mi)"], axis=1, inplace=True)

    # import pdb; pdb.set_trace()
    # df_resorts.to_csv("../data/formatted/trail_data_20200220.csv", index=False, header=True)
            
    # ['vert_rise_(ft)',
    # 'slope_length_(ft)',
    # 'avg_width_(ft)',
    # 'slope_area_(acres)',
    # 'avg_grade_(%)',
    # 'max_grade_(%)',
    # 'ability_level',
    # 'resort',
    # 'location']

    """
    WEB APP - TRAIL COLUMNS
    """
    lst_trail_columns = [
    # "Trail Name",
    # "Resort",
    "Location",
    # "Difficulty",
    "Groomed",
    # "Top Elev (ft)",
    # "Bottom Elev (ft)",
    "Vert Rise (ft)",
    # "Slope Length (ft)",
    "Avg Width (ft)",
    "Slope Area (acres)",
    "Avg Grade (%)",
    "Max Grade (%)"]
