import numpy as np
import pandas as pd


"""
Current: for the AS_table script only

Refactor: all tables
AS
BC
BM
DP
Loveland
Monarch
Steamboat
Vail
WC
WP
"""


class CreateTables:

    def __init__(self):
        pass

    def fix_a_row(self, row):
        lst = row.split()
        # words = [x for x in lst if (x.strip('.').isalpha() or any(i in x for i in ['#','-',"'",'(']))]
        # stats = [x for x in lst if not (x.strip('.').isalpha() or any(i in x for i in ['#','-',"'",'(']))]
        if lst[-2] == 'Adv.' or lst[-2] == 'Low' or lst[-2] == 'Advanced' or lst[-2] == 'Expert' or lst[-2] == 'Intermediate':
            level = [' '.join(lst[-2:])]
            trail_name = [' '.join(lst[:-10])]
            stats = lst[-10:-2]
        else:
            level = [lst[-1]]
            trail_name = [' '.join(lst[:-9])]
            stats = lst[-9:-1]
        new_row = trail_name + stats + level
        return new_row

    def make_dataframe(self, filename):
        with open(filename) as f:
            stuff = f.read()
        stuff_split = stuff.split('\n')

        level_endings = ['Beginner', 'Novice', 'Intermediate', 'Expert', 'Glade', 'Bowl', 'Hike-To',
                         'Advanced', 'Glade-Gated', 'Chute/Bowl-Gated', 'Bowl/Glade-Gated', 'Chute/Glade-Gated']

        trail_rows = []
        for row in stuff_split:
            for level in level_endings:
                if len(row.split()) > 1:
                    if row.split()[-1] == level:
                        trail_rows.append(row)
            if len(row) >= 1:
                if row[-1] == '%':
                    # change THIS or something like it to deal with Vail line splits (in name and ability level)
                    trail_rows.append(row + ' Advanced Intermediate')

        list_of_lists = []
        for row in trail_rows:
            list_of_lists.append(self.fix_a_row(row))

        colnames = ['trail_name', 'top_elev_(ft)', 'bottom_elev_(ft)', 'vert_rise_(ft)', 'slope_length_(ft)',
                    'avg_width_(ft)', 'slope_area_(acres)', 'avg_grade_(%)', 'max_grade_(%)', 'ability_level']

        df = pd.DataFrame(list_of_lists, columns=colnames)
        return df

    def fix_dtype(self, filename, resort, location):
        '''
        Inputs:
        filename: .txt file (str)
        resort: resort name (str)
        location: city (str)
        '''
        df = self.make_dataframe(filename)
        columns_to_change = ['top_elev_(ft)', 'bottom_elev_(ft)',
                             'vert_rise_(ft)', 'slope_length_(ft)', 'avg_width_(ft)']
        for column in columns_to_change:
            df[column] = df[column].apply(
                lambda x: x.replace(',', '')).astype(float)
        df['slope_area_(acres)'] = df['slope_area_(acres)'].astype(float)
        for column in ['max_grade_(%)', 'avg_grade_(%)']:
            df[column] = df[column].apply(
                lambda x: x.replace('%', '')).astype(float)
        df['resort'] = resort
        df['location'] = location
        return df

    '''
    figure out how to deal with multi lines for Vail
    '''

    '''
    add columns for 
    -grooming
    -face
    -ski area
    '''
