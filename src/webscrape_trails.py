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

        self.browser = webdriver.PhantomJS()

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

    def make_run_df(self, lst):
        '''
        Inputs:
        table from make_tables (table)
        Outputs:
        dataframe of trails of that color (DataFrame)
        '''
        runs_cols = [
            'Name', 'Bottom (ft)', 'Top (ft)', 'Vertical Drop (ft)', 'Length (mi)']
        df = pd.DataFrame(lst)
        df.columns = runs_cols
        for i in range(len(df['Length (mi)'])):
            if df['Length (mi)'][i][-2:] == 'ft':
                df['Length (mi)'][i] = round(
                    float(df['Length (mi)'][i][:-2])/5280, 2)
            else:
                df['Length (mi)'][i] = float(df['Length (mi)'][i][:-2])
        for col in runs_cols[1:-1]:
            # except some lengths are in feet...
            df[col] = df[col].apply(lambda x: float(x[:-2]))
        df['Average Steepness'] = (
            df['Vertical Drop (ft)']/(5280*df['Length (mi)'])).astype(float)
        df['Length (mi)'] = df['Length (mi)'].astype(float)
        return df

    def make_df_dicts(self, URL, nums):
        '''
        Inputs:
        URL from URLs (str)
        nums from nums (list)
        Outputs:
        dictionary of {level: level_df} (dict)
        '''
        resort = {}
        greens, blues, blacks, bb = self.make_tables(URL, nums)
        levels = ['green', 'blue', 'black', 'bb']
        for i, j in zip(levels, [greens, blues, blacks, bb]):
            if len(j) == 0:
                resort[i] = None
            else:
                resort[i] = self.make_run_df(j)
        return resort

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
    import pdb; pdb.set_trace()
    for url in tqdm(lst_resort_urls):
        df_resort = ws.make_tables(URL=url)
        df_resort["URL"] = url
        lst_resort_data.append(df_resort)
        time.sleep(10)

    # Combine resort data
    df_combined = pd.concat(lst_resort_data)
    df_combined["difficulty"] = df_combined["URL"].str.split("skiruns-", 1, expand=True)[1]

# loveland_greens = [word.encode('ascii','ignore').strip().decode('utf-8') for word in d['Loveland']['green']['Name']]
# loveland_blues = [word.encode('ascii','ignore').strip().decode('utf-8') for word in d['Loveland']['blue']['Name']]
# loveland_blacks = [word.encode('ascii','ignore').strip().decode('utf-8') for word in d['Loveland']['black']['Name']]
# loveland_bbs = [word.encode('ascii','ignore').strip().decode('utf-8') for word in d['Loveland']['bb']['Name']]
#
# def get_trails_list(resort,level):
#     if d[resort][level] is None:
#         return []
#     else:
#         return [word.encode('ascii','ignore').strip().decode('utf-8') for word in d[resort][level]['Name']]


#
# def get_table(URL):
#     content = requests.get(URL).content
#
#     soup = BeautifulSoup(content, "html.parser")
#
#     rows = soup.select('tr')
#
#     table_lst = []
#     for row in rows:
#         cell_lst = [cell for cell in row if cell != '\n']
#         cell_lst = [cell.text for cell in cell_lst]
#         table_lst.append(cell_lst)
#
#     ranking = pd.DataFrame(table_lst)
#     column_names = [x.strip('\n') for x in table_lst[0]]
#     ranking.columns = column_names
#     ranking = ranking.drop(0)
#     if len(ranking['Resort Name'][1]) == 1:
#         ranking = ranking.drop(1)
#     ranking['Last Updated'] = ranking['Resort Name'].apply(lambda x: x.split('\n')[3])
#     ranking['Resort Location'] = ranking['Resort Name'].apply(lambda x: x.split('\n')[2])
#     ranking['Resort Name'] = ranking['Resort Name'].apply(lambda x: x.split('\n')[1])
#     ranking['User Rating'] = ranking['User Rating'].apply(lambda x: x.split('\n')[1:3])
#     return ranking
#
# terrain = get_table(URL_RM_terrain)
# mtn_stats = get_table(URL_RM_stats)
#
# terrain['Runs'] = terrain['Runs'].apply(lambda x: int(x.strip('\n').replace('/','')))
# levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
# level_columns = dict()
# for level in levels:
#     terrain[level] = terrain[level].apply(lambda x: int(x[:-1]) if len(x) > 2 else 0)
#     level_columns[level] = '% '+level
# terrain = terrain.rename(columns = level_columns)
#
# num_fields = ['Base','Summit','Vertical Drop','Longest Run','Snow Making']
# field_columns = dict()
# for field in num_fields:
#     field_columns[field] = field+' ({})'.format(mtn_stats[field][1][-2:])
#     mtn_stats[field] = mtn_stats[field].apply(lambda x: float(x[:-2]) if x != 'N/A' else 0)
# mtn_stats = mtn_stats.rename(columns=field_columns)
