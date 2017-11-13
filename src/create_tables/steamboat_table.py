import pandas as pd
import numpy as np


def fix_a_row(row):
    name = [' '.join(row[:-14])]
    stats = row[-13:-9]+row[-8:-4]+[row[-3]]
    new_row = name + stats
    return new_row


def make_dataframe(filename):
    with open(filename) as f:
        stuff = f.read()
    stuff_split = stuff.split('\n')
    stuff_stripped = [x.strip() for x in stuff_split]
    stuff_stripped2 = [x for x in stuff_stripped if len(x) > 1]
    
    bad_words = ['TABLE',
                 'STEAMBOAT',
                 'SKI',
                 'Elevation',
                 'Trail',
                 'Lift',
                 'Name',
                 'Lifts',
                 'Total',
                 'Steamboat',
                 '2011',
                 'Subtotal',
                 'Tree',
                 'Other',
                 'GRAND']
                 
    stuff_removed = [x for x in stuff_stripped2 if x.split()[0] not in bad_words]
    
    stuff_removed_lsts = []
    for row in stuff_removed:
        y = [x for x in row.split() if ((x != 'area') and (x != 'dens.') and (x != 'half') and ('/' not in x))]
        name = y[:-14]
        if len(name) > 0:
            stuff_removed_lsts.append(y)


    list_of_lists = []                
    for row in stuff_removed_lsts:
        list_of_lists.append(fix_a_row(row))
        
    colnames = ['trail_name', 'ability_level', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_grade_(%)', 'max_grade_(%)', 'avg_width_(ft)', 'slope_area_(acres)']

    df = pd.DataFrame(list_of_lists, columns=colnames)
    return df
    

def fix_dtype(filename,resort,location):
    '''
    Inputs:
    filename: .txt file (str)
    resort: resort name (str)
    location: State (str)
    '''
    df = make_dataframe(filename)
    
    skill_levels = {1: 'Beginner',
                    2: 'Novice',
                    3: 'Low Intermediate',
                    4: 'Intermediate',
                    5: 'Adv. Intermediate',
                    6: 'Expert',
                    7: 'Expert'}
                  
    for num in skill_levels.keys():
        df.loc[df['ability_level'] == str(num), 'ability_level'] = skill_levels[num]
    
    columns_to_change = ['top_elev_(ft)','bottom_elev_(ft)','vert_rise_(ft)','slope_length_(ft)','avg_width_(ft)']
    for column in columns_to_change:
        df[column] = df[column].apply(lambda x: x.replace(',','')).astype(float)
    df['slope_area_(acres)'] = df['slope_area_(acres)'].astype(float)
    for column in ['max_grade_(%)','avg_grade_(%)']:
        df[column] = df[column].apply(lambda x: x.replace('%','')).astype(float)
    df['resort'] = resort
    df['location'] = location
    return df