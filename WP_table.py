import pandas as pd

colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'horiz_dist', 'slope_length_(ft)', 'avg_grade_(%)', 'plan_acres', 'slope_area_(acres)', 'deg_grade', 'max_grade_(%)', 'avg_width_(ft)', 'ability_level']

filename = 'WP.csv'

skill_levels = {1: 'Beginner',
                2: 'Novice',
                3: 'Low Intermediate',
                4: 'Intermediate',
                5: 'Adv. Intermediate',
                6: 'Expert',
                7: 'Expert'}

def fix_dtype(filename,resort,location):
    '''
    Inputs:
    filename: .csv file (str)
    resort: resort name (str)
    location: city (str)
    '''
    df = pd.read_csv(filename,header=None,names=colnames)
    df = df[df['ability_level'] != 0]
    columns_to_change = ['top_elev_(ft)','bottom_elev_(ft)','slope_length_(ft)']
    for column in columns_to_change:
        df[column] = df[column].apply(lambda x: x.replace(',','')).astype(float)
    df['vert_rise_(ft)'] = df['vert_rise_(ft)'].astype(float)
    df['avg_grade_(%)'] = df['avg_grade_(%)'].apply(lambda x: x.replace('%','')).astype(float)
    df['resort'] = resort
    df['location'] = location
    df.drop(['horiz_dist','plan_acres','deg_grade'],axis=1, inplace=True)
    df.loc[df['avg_width_(ft)'] == 'None', 'avg_width_(ft)'] = round((df['slope_area_(acres)']/df['slope_length_(ft)'])*43560,2)
    for num in skill_levels.keys():
        df.loc[df['ability_level'] == num, 'ability_level'] = skill_levels[num]
    return df
    