import re

import numpy as np
import pandas as pd


def fix_a_row(row):
    """
    Correct values in each row of data

    Input
        row: list of values
    
    Output
        list of corrected values
    """

    lst = row.split()

    if lst[-3] == 'Gladed':
        level = [' '.join(lst[-3:])]
        trail_name = [' '.join(lst[:-12])]
        stats = lst[-12:-3]    
    elif lst[-2] in ["Adv.", "Gladed", "Low"]:
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
    """
    Create Pandas DataFrame from text file

    Input
        filename: file for processing
    
    Output
        Pandas DataFrame
    """
        
    with open(filename) as f:
        lst_resort_data = f.read().split("\n")
      
    lst_level_endings = ['Beginner','Novice','Intermediate','Expert','Advanced', 'Inter']

    trail_rows = []

    for row in lst_resort_data:
        if (len(row.split()) > 1) and (row.split()[-1] in lst_level_endings):
            trail_rows.append(row)
        if (len(row) >= 1) and (row[-1] == '%'):            
        # TODO: Change to handle Vail line splits (in name and ability level)
            trail_rows.append(row + ' Advanced Intermediate') 
    
    list_of_lists = [fix_a_row(row) for row in trail_rows]
    
    colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'plan_length', 'slope_length_(ft)', 'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level']

    df = pd.DataFrame(list_of_lists, columns=colnames)
    
    return df
    

def preprocess_data(df,resort,location):
    """
    Create Pandas DataFrame from text file

    Input
        filename: file for processing
    
    Output
        Pandas DataFrame
    """

    columns_to_change = ['top_elev_(ft)','bottom_elev_(ft)','vert_rise_(ft)','slope_length_(ft)','avg_width_(ft)']
    
    for column in columns_to_change:
        df[column] = df[column].apply(lambda x: x.replace(',','')).astype(float)
    
    df['slope_area_(acres)'] = df['slope_area_(acres)'].astype(float)
    df['max_grade_(%)'] = df['max_grade_(%)'].astype(float)
    df['avg_grade_(%)'] = df['avg_grade_(%)'].astype(float)
    df['resort'] = resort
    df['location'] = location

    df["trail_name"] = fix_trail_names(df=df)
    
    return df

def fix_trail_names(df):
    '''
    Inputs:
        df from trail_names_to_fix (DataFrame)
    Outputs:
        df w/ trail name fixed - removing number at beginning (DataFrame)
    '''
    df['trail_name'] = df['trail_name'].apply(
        lambda x: ' '.join(x.split()[1:]))

    df["trail_name"] = [re.sub(r'\d+','', trail) for trail in df["trail_name"]]
    df["trail_name"] = df["trail_name"].str.lstrip()

    df["new_trail"] = df.trail_name.apply(lambda x: " ".join(x.split()[1:]))
    df.loc[df["new_trail"] == '', 'new_trail'] = df["trail_name"]

    df["trail_name"] = df["new_trail"]

    df.drop("new_trail", axis=1, inplace=True)
    
    df["trail_name"] = df["trail_name"].str.rstrip()
    
    return df

if __name__ == '__main__':

    df_resort = make_dataframe("../../data/resorts/Wolf_Creek.txt")

    df_resort = preprocess_data(df=df_resort,
        resort = "Wolf Creek",
        location = "CO")
