import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import pickle

LL_URL = 'https://jollyturns.com/resort/united-states-of-america/loveland-ski-area/skiruns-green'
AB_URL = 'https://jollyturns.com/resort/united-states-of-america/arapahoe-basin/skiruns-green'
C_URL = 'https://jollyturns.com/resort/united-states-of-america/copper-mountain-resort/skiruns-green'
E_URL = 'https://jollyturns.com/resort/united-states-of-america/eldora-mountain-resort/skiruns-green'
AM_URL = 'https://jollyturns.com/resort/united-states-of-america/alpine-meadows/skiruns-green'
V_URL = 'https://jollyturns.com/resort/united-states-of-america/vail-ski-resort/skiruns-green'
M_URL = 'https://jollyturns.com/resort/united-states-of-america/monarch-ski-area/skiruns-green'
CB_URL = 'https://jollyturns.com/resort/united-states-of-america/crested-butte-mountain-resort/skiruns-green'
T_URL = 'https://jollyturns.com/resort/united-states-of-america/taos-ski-valley/skiruns-green'
DP_URL = 'https://jollyturns.com/resort/united-states-of-america/diamond-peak/skiruns-green'
WP_URL = 'https://jollyturns.com/resort/united-states-of-america/winter-park-resort/skiruns-green'
BC_URL = 'https://jollyturns.com/resort/united-states-of-america/beaver-creek-resort/skiruns-green'

URLs = [LL_URL,AB_URL,C_URL,E_URL,AM_URL,V_URL,M_URL,CB_URL,T_URL,DP_URL,WP_URL,BC_URL]

LL_nums = [10,17,38,23,12,1]
AB_nums = [7,6,33,37,36,2] # A basin
C_nums = [22,27,30,50,25,9]
E_nums = [9,6,26,9,8,0]
AM_nums = [13,2,39,49,0,1]
V_nums = [29,29,59,104,7,1]
M_nums = [5,13,16,25,7,3]
CB_nums = [13,24,41,18,44,0]
T_nums = [13,13,20,37,50,0]
DP_nums = [6,2,14,14,0,1]
WP_nums = [25,32,38,78,9,7] # WP
BC_nums = [24,42,47,39,12,2]

nums = [LL_nums,AB_nums,C_nums,E_nums,AM_nums,V_nums,M_nums,CB_nums,T_nums,DP_nums,WP_nums,BC_nums]

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

loveland_script = ['Loveland', 'Arapahoe Basin', 'Copper', 'Eldora', 'Alpine Meadows']
vail_script = ['Vail']
monarch_script = ['Monarch', 'Crested Butte', 'Taos']
DP_script = ['Diamond Peak']
WP_script = ['Winter Park']
BC_script = ['Beaver Creek']

resorts = loveland_script + vail_script + monarch_script + DP_script + WP_script + BC_script

dct = {} # {resort: {level: level_df}}
for resort,URL,nums in zip(resorts,URLs,nums):
    dct[resort] = make_df_dicts(URL,nums)
    
    
output = open('../data/resort_dict.pkl', 'wb')
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