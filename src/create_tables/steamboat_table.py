import pandas as pd
import numpy as np


def fix_a_row(row):
    """
    Correct row formatting

    Input
        row: list of ski run data

    Output
        formatted list of ski run data
    """

    name = [' '.join(row[:-14])]
    stats = row[-13:-9]+row[-8:-4]+[row[-3]]
    new_row = name + stats
    return new_row


def make_dataframe(filename):
    """
    Create Pandas DataFrame from text file

    Input
        filename: text file, Bald Mountain data
    
    Output
        Pandas DataFrame of formatted resort data
    """    

    with open(filename) as f:
        resort_data = f.read().split("\n")
    
    lst_resort_data = [x.strip() for x in resort_data]
    lst_resort_data = [x for x in lst_resort_data if len(x) > 1]
    
    bad_words = ['2011',
                 'Elevation',
                 'GRAND',
                 'Lift',
                 'Lifts',
                 'Name',
                 'Other',
                 'SKI',
                 'STEAMBOAT',
                 'Steamboat',
                 'Subtotal',
                 'TABLE',
                 'Total',
                 'Trail',
                 'Tree']
                 
    lst_resort_data = [x for x in lst_resort_data if x.split()[0] not in bad_words]
     
    lst_formatted_resort_data = []

    for ski_run in lst_resort_data:
        lst_ski_run = [x for x in ski_run.split() if ((x not in ["area", "dens.", "half"]) and ('/' not in x))]
        name = lst_ski_run[:-14]
        if len(name) > 0:
            lst_formatted_resort_data.append(lst_ski_run)


    list_of_lists = [fix_a_row(row) for row in lst_formatted_resort_data]
       
    colnames = ['trail_name', 'ability_level', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_grade_(%)', 'max_grade_(%)', 'avg_width_(ft)', 'slope_area_(acres)']

    df = pd.DataFrame(list_of_lists, columns=colnames)
    
    return df
    

def preprocess_data(df,resort,location):
    '''
    Inputs:
        df: Pandas DataFrame
        resort: resort name (str)
        location: city (str)
    
    Output
        Pandas DataFrame with formatted columns
    '''
    
    skill_levels = {1: 'Beginner',
                    2: 'Novice',
                    3: 'Low Intermediate',
                    4: 'Intermediate',
                    5: 'Adv. Intermediate',
                    6: 'Expert',
                    7: 'Expert'}
                  
    df["ability_level"] = df["ability_level"].astype(int).map(skill_levels)              
    
    columns_to_change = ['top_elev_(ft)','bottom_elev_(ft)','vert_rise_(ft)','slope_length_(ft)','avg_width_(ft)']
    
    for column in columns_to_change:
        df[column] = df[column].apply(lambda x: x.replace(',','')).astype(float)
    
    df['slope_area_(acres)'] = df['slope_area_(acres)'].astype(float)
    
    for column in ['max_grade_(%)','avg_grade_(%)']:
        df[column] = df[column].apply(lambda x: x.replace('%','')).astype(float)
    
    df['resort'] = resort
    df['location'] = location
    
    return df

if __name__ == '__main__':

    df_resort = make_dataframe("../../data/resorts/Steamboat.txt")

    df_resort = preprocess_data(df=df_resort,
        resort = "Steamboat",
        location = "CO")
