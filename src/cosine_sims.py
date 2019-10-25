import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')


class CosineSims:

    def __init__(self):
        pass

    def load_pickle_file(self):
        """
        Load pickle file containing formatted resort data
        """

        pkl_file = open('../data/df.pkl', 'rb')
        df = pickle.load(pkl_file)
        pkl_file.close()

        df = df.reset_index(drop=True)

        return df

    def transform_data(self, df):

        features = ['top_elev_(ft)',
                    'bottom_elev_(ft)',
                    'vert_rise_(ft)',
                    'slope_length_(ft)',
                    'avg_width_(ft)',
                    'slope_area_(acres)',
                    'avg_grade_(%)',
                    'max_grade_(%)',
                    'groomed']

        X = df[features].values

        ss = StandardScaler()

        X_train = ss.fit_transform(X)

        return X_train

    def cos_sim_recommendations_resort(self, df, trail_name, resort_name, X, n=5, resort=None):
        index = df.index[(df['trail_name'] == trail_name) &
                         (df['resort'] == resort_name)][0]
        trail = X[index].reshape(1, -1)
        cs = cosine_similarity(trail, X)
        rec_index = np.argsort(cs)[0][::-1][1:]
        ordered_df = df.loc[rec_index]
        if resort:
            ordered_df = ordered_df[ordered_df['resort'] == resort]
        rec_df = ordered_df.head(n)
        orig_row = df.loc[[index]].rename(lambda x: 'original')
        total = pd.concat((orig_row, rec_df))
        return total


if __name__ == '__main__':

    cs = CosineSims()

    df_resorts = cs.load_pickle_file()

    X_train = cs.transform_data(df=df_resorts)

    df_recs = cs.cos_sim_recommendations_resort(
        df=df_resorts, trail_name='Sorensen Park', resort_name='Winter Park', X=X_train, n=5, resort='Winter Park')
