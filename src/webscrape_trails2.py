import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import pickle

T_URL = 'https://jollyturns.com/resort/united-states-of-america/telluride-ski-resort/skiruns-green'
BM_URL = 'https://jollyturns.com/resort/united-states-of-america/bald-mountain/skiruns-green'
S_URL = 'https://jollyturns.com/resort/united-states-of-america/steamboat-ski-resort/skiruns-green'
AS_URL = 'https://jollyturns.com/resort/united-states-of-america/aspen-snowmass/skiruns-green'
WC_URL = 'https://jollyturns.com/resort/united-states-of-america/wolf-creek-ski-area/skiruns-green'

URLs = [T_URL,BM_URL,S_URL,AS_URL,WC_URL]

T_nums = [16,15,38,26,52,3]
BM_nums = [2,7,5,9,0,0] # A basin
S_nums = [18,22,54,70,9,5]
AS_nums = [17,8,49,28,30,3]
WC_nums = [7,8,36,41,35,0]

nums = [T_nums,BM_nums,S_nums,AS_nums,WC_nums]

browser = webdriver.PhantomJS()

def make_tables(URL,nums):
    '''
    Inputs:
    URL from URLs (str)
    nums of trails of each color from nums (list)
    Outputs:
    4 tables of trails by color (tuple of tables)
    '''
    browser.get(URL)
    time.sleep(3)

    soup = BeautifulSoup(browser.page_source,'html.parser')
    rows = soup.select('table.table.table-striped tbody tr')

    table_lst = []
    for row in rows:
        cell_lst = [cell for cell in row if cell != ' ']
        cell_lst = [cell.text for cell in cell_lst]
        table_lst.append(cell_lst)
      
    a,b,c,d,e,f = nums
    
    lifts = table_lst[:a]
    greens = table_lst[a:a+b]
    blues = table_lst[a+b:a+b+c]
    blacks = table_lst[a+b+c:a+b+c+d]
    bb = table_lst[a+b+c+d:a+b+c+d+e]
    tp = table_lst[a+b+c+d+e:a+b+c+d+e+f]
    restaurants = table_lst[a+b+c+d+e+f:]
    return greens, blues, blacks, bb

lift_cols = ['Name', 'Bottom', 'Top', 'Vertical Rise']

def make_run_df(lst):
    '''
    Inputs:
    table from make_tables (table)
    Outputs:
    dataframe of trails of that color (DataFrame)
    '''
    runs_cols = ['Name', 'Bottom (ft)', 'Top (ft)', 'Vertical Drop (ft)', 'Length (mi)']
    df = pd.DataFrame(lst)
    df.columns = runs_cols
    for i in range(len(df['Length (mi)'])):
        if df['Length (mi)'][i][-2:] == 'ft':
            df['Length (mi)'][i] = round(float(df['Length (mi)'][i][:-2])/5280,2)
        else:
            df['Length (mi)'][i] = float(df['Length (mi)'][i][:-2])
    for col in runs_cols[1:-1]:
        df[col] = df[col].apply(lambda x: float(x[:-2])) ## except some lengths are in feet...
    df['Average Steepness'] = (df['Vertical Drop (ft)']/(5280*df['Length (mi)'])).astype(float)
    df['Length (mi)'] = df['Length (mi)'].astype(float)
    return df

# WP_runs = make_tables(WP_URL,WP_nums)
# AB_runs = make_tables(AB_URL,AB_nums)
# 
# WP_greens, WP_blues, WP_blacks, WP_bb = WP_runs
# AB_greens, AB_blues, AB_blacks, AB_bb = AB_runs
# 
# WP_green_df = make_run_df(WP_greens)
# WP_blue_df = make_run_df(WP_blues)
# WP_black_df = make_run_df(WP_blacks)
# WP_bb_df = make_run_df(WP_bb)
# 
# AB_green_df = make_run_df(AB_greens)
# AB_blue_df = make_run_df(AB_blues)
# AB_black_df = make_run_df(AB_blacks)
# AB_bb_df = make_run_df(AB_bb)

def make_df_dicts(URL,nums):
    '''
    Inputs:
    URL from URLs (str)
    nums from nums (list)
    Outputs:
    dictionary of {level: level_df} (dict)
    '''
    resort = {}
    greens, blues, blacks, bb = make_tables(URL,nums)
    levels = ['green','blue','black','bb']
    for i,j in zip(levels,[greens,blues,blacks,bb]):
        if len(j) == 0:
            resort[i] = None
        else:
            resort[i] = make_run_df(j)
    return resort


resorts = ['Telluride', 'Bald Mountain', 'Steamboat', 'Aspen Snowmass', 'Wolf Creek']

dct = {} # {resort: {level: level_df}}
for resort,URL,nums in zip(resorts,URLs,nums):
    dct[resort] = make_df_dicts(URL,nums)
    
    
output = open('../data/resort_dict2.pkl', 'wb')
pickle.dump(dct, output)
output.close()
    
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