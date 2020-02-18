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

    if lst[-2] in ['Adv.', 'Low', 'Advanced', 'Expert', 'Intermediate']:
        level = [' '.join(lst[-2:])]
        trail_name = [' '.join(lst[:-10])]
        stats = lst[-10:-2]
    else:
        level = [lst[-1]]
        trail_name = [' '.join(lst[:-9])]
        stats = lst[-9:-1]
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
    
    lst_level_endings = ['Beginner','Novice','Intermediate','Expert','Glade','Bowl','Hike-To', 'Advanced', 'Glade-Gated', 'Chute/Bowl-Gated', 'Bowl/Glade-Gated', 'Chute/Glade-Gated']

    trail_rows = []

    for row in lst_resort_data:
        if len(row.split()) > 1 and (row.split()[-1] in lst_level_endings):
            trail_rows.append(row)
        if (len(row) >= 1) and (row[-1] == "%"):            
            trail_rows.append(row + ' Advanced Intermediate')

    list_of_lists = [fix_a_row(row) for row in trail_rows]

    colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level']

    df = pd.DataFrame(list_of_lists, columns=colnames)
    
    return df
    

def preprocess_data(df, resort, location):
    '''
    Inputs:
        df: Pandas DataFrame
        resort: resort name (str)
        location: city (str)
    
    Output
        Pandas DataFrame with formatted columns
    '''

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

    df_resort = make_dataframe("../../data/resorts/Telluride.txt")

    df_resort = preprocess_data(df=df_resort,
        resort = "Telluride",
        location = "CO")
