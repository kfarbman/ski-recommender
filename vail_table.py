import pandas as pd
import numpy as np

'''txt files'''
files = {'AB': 'Arapahoe-Basin-2012-Master-Development-Plan_FINAL.txt', 
    'Loveland': 'Loveland-Ski-Area-2013-Master-Plan.txt',
    'Monarch': 'Monarch.txt',
    'DP': 'DP.txt',
    'Vail': 'Vail.txt'}


def fix_a_row(row):
    lst = row.split()
    # words = [x for x in lst if (x.strip('.').isalpha() or any(i in x for i in ['#','-',"'",'(']))]
    # stats = [x for x in lst if not (x.strip('.').isalpha() or any(i in x for i in ['#','-',"'",'(']))]
    if lst[-2] == 'Adv.' or lst[-2] == 'Low' or lst[-2] == 'Advanced' or lst[-2] == 'Exp' or lst[-2] == 'Hike':
        level = [' '.join(lst[-2:])]
        trail_name = [' '.join(lst[:-11])]
        stats = lst[-11:-2]
    else:
        level = [lst[-1]]
        trail_name = [' '.join(lst[:-10])]
        stats = lst[-10:-1]
    new_row = trail_name + stats + level
    return new_row


def make_dataframe(filename):
    with open(filename) as f:
        stuff = f.read()
    stuff_split = stuff.split('\n')
    
    level_endings = ['Beginner','Novice','Intermediate','Expert','Glade','Bowl','To']

    trail_rows = []
    for i,row in enumerate(stuff_split):
        for level in level_endings:
            if len(row.split()) > 4:
                if row.split()[-1] == level:
                    if ',' in row.split()[0]:
                        trail_rows.append(stuff_split[i-1]+stuff_split[i+1]+row)
                    else:
                        trail_rows.append(row)
        if len(row) >= 1:            
            if row[-1] == '%':
                if ',' in row.split()[0]:
                    trail_rows.append(' '.join([x for x in stuff_split[i-1].split() if x != 'Advanced'])+' '.join([x for x in stuff_split[i+1].split() if x != 'Intermediate'])+row+' Advanced Intermediate')
                else:
                    trail_rows.append(row + ' Advanced Intermediate') # change THIS or something like it to deal with Vail line splits (in name and ability level)
        

    list_of_lists = []                
    for row in trail_rows:
        list_of_lists.append(fix_a_row(row))
        
    colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'horiz_length','slope_length_(ft)', 'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level']

    df = pd.DataFrame(list_of_lists, columns=colnames)
    return df
    

def fix_dtype(filename,resort,location):
    '''
    Inputs:
    filename: .txt file (str)
    resort: resort name (str)
    location: city (str)
    '''
    df = make_dataframe(filename)
    columns_to_change = ['top_elev_(ft)','bottom_elev_(ft)','vert_rise_(ft)','horiz_length','slope_length_(ft)','avg_width_(ft)']
    for column in columns_to_change:
        df[column] = df[column].apply(lambda x: x.replace(',','')).astype(float)
    df['slope_area_(acres)'] = df['slope_area_(acres)'].astype(float)
    for column in ['max_grade_(%)','avg_grade_(%)']:
        df[column] = df[column].apply(lambda x: x.replace('%','')).astype(float)
    df['resort'] = resort
    df['location'] = location
    return df



'''
add columns for 
-grooming
-face
-ski area
'''
          