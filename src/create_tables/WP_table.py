import pandas as pd

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
    
    df.drop(['horiz_dist','plan_acres','deg_grade'],axis=1, inplace=True)

    df = df[df['ability_level'] > 0]
    
    columns_to_change = ['top_elev_(ft)','bottom_elev_(ft)','slope_length_(ft)']
    
    # TODO: Correct syntax to remove warnings
    for column in columns_to_change:
        df[column] = df[column].astype(float)
    
    df['vert_rise_(ft)'] = df['vert_rise_(ft)'].astype(float)
    df['avg_grade_(%)'] = df['avg_grade_(%)'].apply(lambda x: x.replace('%','')).astype(float)
    df['resort'] = resort
    df['location'] = location
    df.loc[df['avg_width_(ft)'] == 'None', 'avg_width_(ft)'] = round((df['slope_area_(acres)']/df['slope_length_(ft)'])*43560,2)
    df['avg_width_(ft)'] = df['avg_width_(ft)'].astype(float)
    
    df["ability_level"] = df["ability_level"].astype(int).map(skill_levels)              

    return df


if __name__ == '__main__':

    colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'horiz_dist', 'slope_length_(ft)', 'avg_grade_(%)', 'plan_acres', 'slope_area_(acres)', 'deg_grade', 'max_grade_(%)', 'avg_width_(ft)', 'ability_level']

    df_resort = pd.read_csv("../../data/WP.csv",
        header=None,
        names=colnames)

    df_resort = preprocess_data(df=df_resort,
        resort="Winter Park",
        location="CO")
