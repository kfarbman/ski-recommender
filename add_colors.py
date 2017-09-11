# import comb_tables
# import webscrape_trails
import os
import warnings
warnings.filterwarnings('ignore')

'''
need to figure out how to get inputs from other scripts
'''

resorts = ['Loveland',
 'Arapahoe Basin',
 'Copper',
 'Eldora',
 'Alpine Meadows',
 'Vail',
 'Monarch',
 'Crested Butte',
 'Taos',
 'Diamond Peak',
 'Winter Park',
 'Beaver Creek']
levels = ['green','blue','black','bb']
resort_dfs = [loveland,AB,copper,eldora,AM,vail,monarch,CB,taos,DP,WP,BC]

def get_trails_list(resort,level):
    '''
    Inputs: 
    resort from resorts (str)
    level from levels (str)
    Outputs:
    list of trail names in a useable string format (list)
    '''
    if d[resort][level] is None:
        return []
    else:
        return [word.encode('ascii','ignore').strip().decode('utf-8') for word in d[resort][level]['Name']]
    
trails_by_color = {}
for resort in resorts:
    trails_by_color[resort] = {level: get_trails_list(resort,level) for level in levels}