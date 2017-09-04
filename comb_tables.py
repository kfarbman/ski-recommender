import pandas as pd
import loveland_table
import vail_table
import monarch_table
import DP_table
import WP_table

resorts = {'Loveland': ['Loveland.txt', 'CO'],
           'Arapahoe Basin': ['Arapahoe_Basin.txt', 'CO'],
           'Copper': ['Copper.txt', 'CO'],
           'Eldora': ['Eldora.txt', 'CO'],
           'Alpine Meadows': ['Alpine_Meadows.txt', 'CA'],
           'Vail': ['Vail.txt', 'CO'],
           'Monarch': ['Monarch.txt', 'CO'],
           'Crested Butte': ['Crested_Butte.txt', 'CO'],
           'Taos': ['Taos.txt', 'NM'],
           'Diamond Peak': ['DP.txt', 'NV'],
           'Winter Park': ['WP.csv', 'CO']}
           
loveland_script = ['Loveland', 'Arapahoe Basin', 'Copper', 'Eldora', 'Alpine Meadows']
vail_script = ['Vail']
monarch_script = ['Monarch', 'Crested Butte', 'Taos']
DP_script = ['Diamond Peak']
WP_script = ['Winter Park']

d = {}

for resort in loveland_script:
    filename, location = resorts[resort]
    d[resort]= loveland_table.fix_dtype(filename,resort,location)
for resort in vail_script:
    filename, location = resorts[resort]
    d[resort]= vail_table.fix_dtype(filename,resort,location)
    del d[resort]['horiz_length']
for resort in monarch_script:
    filename, location = resorts[resort]
    d[resort]= monarch_table.fix_dtype(filename,resort,location)
    del d[resort]['plan_length']
for resort in DP_script:
    filename, location = resorts[resort]
    d[resort]= DP_table.fix_dtype(filename,resort,location)
    d[resort].drop(['plan_length', 'pct_inc', 'plan_area'],axis=1,inplace=True)
for resort in WP_script:
    filename, location = resorts[resort]
    d[resort] = WP_table.fix_dtype(filename,resort,location)
    
columns = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level','resort','location']   

whole_table = pd.concat(d.values())
whole_table = whole_table[columns]
CO_resorts = whole_table[whole_table['location'] == 'CO']