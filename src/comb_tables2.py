import pickle
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .create_tables import (AS_table, BM_table, WC_table, loveland_table,
                           steamboat_table)

warnings.filterwarnings('ignore')


# resorts = {'Telluride': ['../data/new/Telluride.txt', 'CO'],
#            'Bald Mountain': ['../data/new/Bald_Mountain.txt', 'CO'],
#            'Steamboat': ['../data/new/Steamboat.txt', 'CO'],
#            'Aspen Snowmass': ['../data/new/Aspen_Snowmass.txt', 'CO'],
#            'Wolf Creek': ['../data/new/Wolf_Creek.txt', 'CO']}

# which resorts work with which script
# loveland_script = ['Telluride']
# BM_script = ['Bald Mountain']
# steamboat_script = ['Steamboat']
# AS_script = ['Aspen Snowmass']
# WC_script = ['Wolf Creek']


# d = {}
# for resort in loveland_script:
#     filename, location = resorts[resort]
#     d[resort] = loveland_table.fix_dtype(
#         filename, resort, location)
# for resort in BM_script:
#     filename, location = resorts[resort]
#     d[resort] = BM_table.fix_dtype(filename, resort, location)
# for resort in steamboat_script:
#     filename, location = resorts[resort]
#     d[resort] = steamboat_table.fix_dtype(
#         filename, resort, location)
# for resort in AS_script:
#     filename, location = resorts[resort]
#     d[resort] = AS_table.fix_dtype(filename, resort, location)
# for resort in WC_script:
#     filename, location = resorts[resort]
#     d[resort] = WC_table.fix_dtype(filename, resort, location)
#     del d[resort]['plan_length']


# columns = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)',
#            'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level', 'resort', 'location']

# whole_table = pd.concat(d.values())
# making sure the columns are in the correct order
# whole_table = whole_table[columns]
# CO_resorts = whole_table[whole_table['location'] == 'CO']


### from my ipython notebook
# standardizing the ability levels
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Advanced Intermediate'] = 'Advanced'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Adv. Intermediate'] = 'Advanced'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Gladed Adv Inter'] = 'Advanced'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Hike To'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Hike-To'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Gladed Expert'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Intermediate Glade'] = 'Intermediate'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Exp Bowl'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Hike to'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Expert Glade-Gated'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Chute/Bowl-Gated'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Bowl/Glade-Gated'] = 'Expert'
# whole_table['ability_level'][whole_table['ability_level']
#                              == 'Chute/Glade-Gated'] = 'Expert'


# '''separating resorts back out'''
# telluride = whole_table[whole_table['resort'] == 'Telluride']
# BM = whole_table[whole_table['resort'] == 'Bald Mountain']
# steamboat = whole_table[whole_table['resort'] == 'Steamboat']
# AS = whole_table[whole_table['resort'] == 'Aspen Snowmass']
# WC = whole_table[whole_table['resort'] == 'Wolf Creek']


# resort_dfs = [telluride, BM, steamboat, AS, WC]


'''fixing trail names'''
# WC['trail_name'] = WC['trail_name'].apply(lambda x: ' '.join(x.split()[1:]))
WC['trail_name'] = WC['trail_name'].apply(lambda x: ' '.join(x.split()[1:]) if x.split()[
                                          0] in ['l', 'u', 'm', 'c', 'g', 'r'] else ' '.join(x.split()))


# '''groomed runs'''
# groomed_t = ['Meadows', 'Peaks Trail', 'Boomerang Lower', 'Boomerang Upper', 'Butterfly', 'Hoot Brown Expert Terrain Park',
#              'Village Bypass', 'Misty Maiden', 'Peak-A-Boo', 'Sheridan Headwall', 'Cakewalk', "South Henry’s", 'Polar Queen',
#              'Woozley’s Way Lower', 'Woozley’s Way Upper', 'Milk Run Lower', 'Milk Run Upper', 'Telluride Trail', 'Bail Out',
#              'Easy Out', 'Last Chance', 'Lookout Lower', 'Lookout Upper', 'Plunge Upper', 'Bridges', 'Double Cabin', 'Galloping Goose Upper',
#              'Galloping Goose Lower', 'Sundance', "Teddy’s Way", 'Beginner Park', 'Little Maude', 'Nellie', 'Magnolia', 'May Girl',
#              'UTE Park']

# groomed_BM = ['Upper College', 'Lower College', 'Lower River Run', 'Mid River Run', 'Olympic Lane/Ridge', 'Lower Olympic', 'Cut-Off',
#               'Blue Grouse', 'Canyon', 'Lower Warm Springs', 'Warm Springs Face', 'Upper Flying Squirrel', 'Lower Flying Squirrel',
#               'Hemingway', "Lower Picabo's Street", 'Cozy', 'Greyhawk']

# groomed_s = ['B.C. Ski Way', 'Boulevard', 'Lower Broadway', 'Giggle Gulch', 'Park Lane', 'Preview', 'Rendezvous Way', 'Lower Right-O-Way',
#              'Mid Right-O-Way', 'Upper Right-O-Way', 'Short Cut', 'Sitz', 'So What', 'South Peak Flats', 'Spur Run Road', 'Spur Run Face',
#              'Sundial', 'Swinger', 'Upper Why Not', 'Mid Why Not', 'Lower Why Not', 'Upper Yoo Hoo', 'Mid Yoo Hoo', 'Baby Powder gladed',
#              'Bashor Terrain Park', 'Betwixt', 'Blizzard', 'Buckshot', "Buddy's Run", 'Calf Roper', 'Lower Cowboy Coffee', 'Upper Cowboy Coffee',
#              'Daybreak', "Eagle's Nest", "Lower Eagle's Nest", 'Flintlock', 'Heavenly Daze', 'Lower High Noon', 'Upper High Noon', 'High Line',
#              "Huffman's", "Jess' Cut Off", 'Kit', 'Lightning', 'Main Drag', 'Meadow Lane', 'Moonlight', "One O'Clock", "Over Easy", 'Lower Quickdraw',
#              'Upper Quickdraw', 'Lower Rainbow', 'Upper Rainbow', 'Ramrod', 'Rooster', "Ruby's Run", 'Skyline', 'Spike', 'Sunshine Liftline',
#              'Upper Tomohawk', 'Lower Tomohawk', 'Tower', 'Tornado Lane', 'Traverse', 'Upper Vagabond', 'Lower Vagabond', 'Velvet', 'Vogue',
#              'Flying Z Gulch', 'Longhorn', 'Sunnyside', 'Lights Out Sunset', "Two O'Clock", 'Corridor', 'Drop Out', 'Flying Z', 'Last Chance',
#              'Middle Rib', 'Rolex', 'See Me', "Storm Peak Left", "Ted's Ridge", 'Upper Valley View', 'Lower Valley View', 'Voo Doo', 'West Side']

# groomed_AS = []

# groomed_WC = ['A­way', 'Bunny Hop – Lower', 'Bunny Hop – Middle', 'Bunny Hop – Upper', 'Divide Trail', 'Easy Out', 'Kelly Boyce Trail – Lower',
#               'Kelly Boyce Trail – Upper', 'Powder Puff – Lower', 'Powder Puff – Upper', 'Nova', "Susan's", 'Turnpike – Lower', 'Turnpike – Upper',
#               "Alberta's Trail", 'Bonanza Crossover – Upper', 'Bonanza Crossover – Lower', 'Bonanza Trail', 'Charisma', 'Criss Cross',
#               'Legs', 'Coyote Park Trail', 'Muskrat Ramble', 'Navajo Trail – Lower', 'Navajo Trail – Upper', 'Park Avenue', 'Summer Day',
#               'Tranquility – Lower', 'Tranquility – Upper', 'Magic Carpet']


# grooms = [groomed_t, groomed_BM, groomed_s, groomed_AS, groomed_WC]


# '''adding groomed column'''


# def add_groomed_col(df, groomed_lst):
#     '''  
#     Inputs:
#     resort_df from resort_dfs (DataFrame)
#     groomed_lst from grooms (list)
#     Outputs:
#     resort_df w/ groomed column added (DataFrame)
#     '''
#     df['groomed'] = 0
#     df['groomed'][df['trail_name'].isin(groomed_lst)] = 1
#     return df


# for resort, groom in zip(resort_dfs, grooms):
#     add_groomed_col(resort, groom)


# '''importing pickled dict from webscrape_trails.py'''
# pkl_file = open('../data/resort_dict2.pkl', 'rb')
# dct = pickle.load(pkl_file)
# pkl_file.close()

'''REDEFINING'''
# resorts = ['Telluride',
#            'Bald Mountain',
#            'Steamboat',
#            'Aspen Snowmass',
#            'Wolf Creek']
# levels = ['green', 'blue', 'black', 'bb']
# resort_dfs = [telluride, BM, steamboat, AS, WC]
# resort_dict = dict(zip(resorts, resort_dfs))


# def missing_trails(color_trails, resort):
#     '''
#     Inputs:
#     color_trails = trails_by_color[resort][level] (list)
#     resort from resort_dict (str)
#     Outputs:
#     list of trails by color from webscraping that weren't in the dataframe
#     '''
#     trail_lst = []
#     for trail in color_trails:
#         if trail not in list(resort_dict[resort]['trail_name']):
#              trail_lst.append(trail)
#     return trail_lst


# '''getting a useable list of trails to compare by color'''


# def get_trails_list(resort, level):
#     '''
#     Inputs: 
#     resort from resorts (str)
#     level from levels (str)
#     Outputs:
#     list of trail names in a useable string format (list)
#     '''
#     if dct[resort][level] is None:
#         return []
#     else:
#         return [word.encode('ascii', 'ignore').strip().decode('utf-8') for word in dct[resort][level]['Name']]


# trails_by_color = {}
# for resort in resort_dict:
#     trails_by_color[resort] = {level: get_trails_list(
#         resort, level) for level in levels}


# '''adding a colors column'''


# def make_colors(resort):
#     '''
#     Inputs:
#     resort_df from resort_dfs (DataFrame)
#     resort from resorts (str)
#     Outputs:
#     resort_df w/ colors column added (DataFrame)
#     '''
#     resort_dict[resort]['colors'] = 'color'
#     levels = ['green', 'blue', 'black', 'bb']
#     for level in levels:
#         resort_dict[resort]['colors'][resort_dict[resort]
#                                       ['trail_name'].isin(get_trails_list(resort, level))] = level
#     return resort_dict[resort]


# for resort in resort_dict:
#     make_colors(resort)


'''
Dictionary of dictionaries {resort: {level: [trails]}}
For trails that are in the resort_df but have slightly different names from the webscraping (by color)
'''
trails_to_add = {}
trails_to_add['Telluride'] = {'green': [],
                              'blue': [],
                              'black': [],
                              'bb': []}
trails_to_add['Bald Mountain'] = {'green': [],
                                  'blue': [],
                                  'black': [],
                                  'bb': []}
trails_to_add['Steamboat'] = {'green': [],
                              'blue': [],
                              'black': [],
                              'bb': []}
trails_to_add['Aspen Snowmass'] = {'green': [],
                                   'blue': [],
                                   'black': [],
                                   'bb': []}
trails_to_add['Wolf Creek'] = {'green': [],
                               'blue': [],
                               'black': [],
                               'bb': []}


'''add trails to colors'''


def add_trails_to_add(resort):
    '''
    Inputs:
    resort from resorts (str)
    Outputs:
    resort_df w/ class column updated w/ trail names that didn't make the list (DataFrame)
    '''
    levels = ['green', 'blue', 'black', 'bb']
    for level in levels:
        resort_dict[resort]['colors'][resort_dict[resort]
                                      ['trail_name'].isin(trails_to_add[resort][level])] = level
    return resort_dict[resort]


for resort in resort_dict:
    add_trails_to_add(resort)


'''trails to remove, since i don't have data on them other than the master plan'''
trails_to_remove_t = ['T-bar Road', 'Sani Flush', 'Awesome II', 'Rip Curl', '']
trails_to_remove_BM = ['High Noon Terrain Park',
                       'Treeline Terrain Park', 'Shooting Gallery', 'Poma Line']
trails_to_remove_s = ["Bruce's Way", 'Bee Road', 'Road Home', 'Cross Cut']
trails_to_remove_AS = []
trails_to_remove_WC = ['Meadows', 'Nirvana', 'Village Way - Primrose']


trails_to_remove = [trails_to_remove_t, trails_to_remove_BM,
                    trails_to_remove_s, trails_to_remove_AS, trails_to_remove_WC]


'''Remove Trails'''


def remove_trails(resort, trail_lst):
    '''
    Inputs:
    resort from resort_dict (str)
    trail_lst from trails_to_remove (list)
    Outputs:
    resort_df with trails removed (DataFrame)
    '''
    resort_df_new = resort_dict[resort][~resort_dict[resort]
                                        ['trail_name'].isin(trail_lst)]
    return resort_df_new


for resort, trail_lst in zip(resort_dict, trails_to_remove):
    resort_dict[resort] = remove_trails(resort, trail_lst)


'''put the dfs back together'''
final_df = pd.concat([resort for resort in resort_dict.values()])

ability_levels = {'Beginner': 1, 'Novice': 2, 'Low Intermediate': 3,
                  'Intermediate': 4, 'Advanced': 5, 'Expert': 6, 'Glade': 5}
colors = {'green': 1, 'blue': 2, 'black': 3, 'bb': 4, 'color': 0}

final_df['ability_nums'] = final_df['ability_level'].map(ability_levels)
final_df['color_nums'] = final_df['colors'].map(colors)

final_df = final_df.reset_index(drop=True)

# final_df['trail_name'].iloc[424] = 'Teaching Terrain 1'
# final_df['trail_name'].iloc[425] = 'Teaching Terrain 2'
# final_df['trail_name'].iloc[750] = 'Teaching Terrain 1'
# final_df['trail_name'].iloc[751] = 'Teaching Terrain 2'
# final_df['trail_name'].iloc[901] = 'Whistle Stop Lower'
# final_df['trail_name'].iloc[908] = 'Whistle Stop Upper'
# for i, j in zip(range(1116,1125),range(1,10)):
#     final_df['trail_name'].iloc[i] = final_df['trail_name'].iloc[i] + " " + str(j)
#
#
# '''fixing Monarch trail names'''
# a = list(final_df['trail_name'][final_df['resort'] == 'Monarch'])
# b = [x.split() for x in a]
# c = [''.join(x) if len(x[0]) == 1 else ' '.join(x) for x in b]
# c[19] = 'Quick Draw'
# c[20] = 'KC Cutoff'
# c[41] = "Doc's Run"
# c[42] = 'Dire Straits'
# c[47] = 'Great Divide'
# c[53] = "Geno's Meadow"
# final_df['trail_name'][final_df['resort'] == 'Monarch'] = c
#
# '''fix trail name'''
# final_df['trail_name'][final_df['trail_name'] == 'Litter Pierre'] = 'Little Pierre'


output = open('../data/df2.pkl', 'wb')
pickle.dump(final_df, output)
output.close()
